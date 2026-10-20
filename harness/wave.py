"""Wave runner (INF-10; docs/WAVES.md). Runs one wave's run sheet on Uzair's machine, scores it, packs the readback.

  python harness/wave.py run   --sheet jobs/waves/A/sheet.json [--workers 4] [--mem 12] [--budget-seconds 0] [--only R1,R2]
  python harness/wave.py score --sheet jobs/waves/A/sheet.json
  python harness/wave.py pack  --sheet jobs/waves/A/sheet.json          -> jobs/waves/A/return_A.zip
  python harness/wave.py check --sheet jobs/waves/A/sheet.json          (validate the sheet; no run)

Standard library only (Python 3.8+), so it runs on the host interpreter and launches Docker itself. The sheet is JSON:

  wave, code_identity (sha256 of the identity manifest), identity_manifest (relative path; "sha256  path" lines),
  profiles {name: {image, network ("none" default), mounts [{src (relative to the folder above cc-research), dst, ro}],
            env {K: V}, workdir, built_by (the run that builds the image; preflight then does not require it)}},
  cpu_probe_image (an image whose shell reads /proc/cpuinfo; default: the first profile image), disk_gb,
  runs [{id, class (A0 static | A1 instrument | A2 probe | A3 full gate | L live), profile ("host" or a profile name),
         cmd [argv; "python" means the interpreter of the profile], est_min, mem_gb, parts, merge [argv], depends_on [ids],
         when (condition), done {file, contains}, decides [must-show ids], cost_from {file, ptr}, cap_usd}],
  must_shows [{id, bundle, metric, args, bar {op, value}, gate}],
  decisions [{if, then}],
  return_files [relative paths or globs, each packed if under 5 MB].

Conditions (when / if) use: pass(M) fail(M) notrun(M) ok(R) failed(R) skipped(R), and / or / not, parentheses.
Every run writes its log to jobs/waves/<wave>/logs/<run>.log; state.json and verdict.json are rewritten after every run, so
a crash or a reboot returns what finished, and running again resumes (a run whose done test passes is not started).
"""
import argparse, glob, hashlib, json, os, platform, re, shutil, subprocess, sys, threading, time, zipfile
from pathlib import Path

RESEARCH = Path(os.environ.get("WAVE_RESEARCH_ROOT") or Path(__file__).resolve().parent.parent)
ROOT = RESEARCH.parent
CLASS_ORDER = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "L": 4}
TOKEN = re.compile(r"\s*(pass|fail|notrun|ok|failed|skipped)\(([A-Za-z0-9_.\-]+)\)|\s*(and|or|not|\(|\))")
MAX_RETURN_FILE = 5 * 1024 * 1024


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------------------ sheet
def load_sheet(path):
    sheet = json.load(open(path, encoding="utf-8"))
    problems = validate(sheet)
    if problems:
        raise SystemExit("sheet invalid:\n  " + "\n  ".join(problems))
    return sheet


def validate(sheet):
    p = []
    ids = [r["id"] for r in sheet.get("runs", [])]
    if len(ids) != len(set(ids)):
        p.append("duplicate run ids")
    ms = {m["id"] for m in sheet.get("must_shows", [])}
    for r in sheet.get("runs", []):
        for k in ("id", "class", "profile", "cmd", "done"):
            if k not in r:
                p.append("%s: missing %s" % (r.get("id"), k))
        if r.get("class") not in CLASS_ORDER:
            p.append("%s: class %r" % (r.get("id"), r.get("class")))
        if r.get("profile") != "host" and r.get("profile") not in sheet.get("profiles", {}):
            p.append("%s: unknown profile %r" % (r["id"], r.get("profile")))
        for d in r.get("depends_on", []):
            if d not in ids:
                p.append("%s: depends on unknown run %s" % (r["id"], d))
        for d in r.get("decides", []):
            if d not in ms:
                p.append("%s: decides unknown must-show %s" % (r["id"], d))
        if r.get("class") == "L" and "cap_usd" not in r:
            p.append("%s: a live run needs cap_usd" % r["id"])
        for k in ("when",):
            if r.get(k):
                try:
                    _compile(r[k])
                except ValueError as e:
                    p.append("%s: %s" % (r["id"], e))
    for m in sheet.get("must_shows", []):
        if m.get("metric") not in METRICS:
            p.append("%s: unknown metric %r" % (m.get("id"), m.get("metric")))
    for d in sheet.get("decisions", []):
        try:
            _compile(d["if"])
        except ValueError as e:
            p.append("decision %r: %s" % (d.get("if"), e))
    # dependency cycles
    deciders = {}
    for r in sheet.get("runs", []):
        for d in r.get("decides", []):
            deciders.setdefault(d, set()).add(r["id"])
    deps = {}
    for r in sheet.get("runs", []):
        ms, rs = refs(r.get("when"))
        deps[r["id"]] = (set(r.get("depends_on", [])) | rs | set().union(*[deciders.get(m, set()) for m in ms])) - {r["id"]}
    seen, stack = set(), set()

    def visit(n):
        if n in stack:
            p.append("dependency cycle at %s" % n)
            return
        if n in seen:
            return
        stack.add(n)
        for d in deps.get(n, ()):
            visit(d)
        stack.discard(n)
        seen.add(n)
    for n in deps:
        visit(n)
    return p


def _compile(expr):
    """-> python expression over the dicts M (must-show status) and R (run status); raises ValueError on anything else."""
    out, pos = [], 0
    expr = expr.strip()
    while pos < len(expr):
        m = TOKEN.match(expr, pos)
        if not m:
            raise ValueError("cannot parse condition at %r" % expr[pos:])
        pos = m.end()
        if m.group(1):
            fn, arg = m.group(1), m.group(2)
            if fn in ("pass", "fail", "notrun"):
                out.append("(M.get(%r) == %r)" % (arg, {"pass": "pass", "fail": "fail", "notrun": "not_run"}[fn]))
            else:
                out.append("(R.get(%r) == %r)" % (arg, {"ok": "ok", "failed": "failed", "skipped": "skipped"}[fn]))
        else:
            out.append(" %s " % m.group(3))
    code = "".join(out)
    try:
        compile(code, "<cond>", "eval")
    except SyntaxError:
        raise ValueError("condition is not well formed: %r" % expr)
    return code


def refs(expr):
    """-> (must-show ids, run ids) a condition reads."""
    ms, rs = set(), set()
    for m in TOKEN.finditer(expr or ""):
        if m.group(1):
            (ms if m.group(1) in ("pass", "fail", "notrun") else rs).add(m.group(2))
    return ms, rs


def cond(expr, M, R):
    if not expr:
        return True
    return bool(eval(_compile(expr), {"__builtins__": {}}, {"M": M, "R": R}))


# ------------------------------------------------------------------------------------------------------------ metrics
def _resolve(path):
    return RESEARCH / path


def _ptr(obj, ptr):
    for k in ptr:
        obj = obj[k] if not isinstance(obj, list) else obj[int(k)]
    return obj


def m_json(a):
    return _ptr(json.load(open(_resolve(a["file"]), encoding="utf-8")), a["ptr"])


def m_json_len(a):
    return len(m_json(a))


def m_exists(a):
    return _resolve(a["file"]).exists()


def m_digest(a):
    return sha_file(_resolve(a["file"]))


def m_contains(a):
    return a["text"] in _resolve(a["file"]).read_text(encoding="utf-8", errors="replace")


METRICS = {"json": m_json, "json_len": m_json_len, "exists": m_exists, "digest": m_digest, "contains": m_contains}
OPS = {">=": lambda x, y: x >= y, "<=": lambda x, y: x <= y, ">": lambda x, y: x > y, "<": lambda x, y: x < y,
       "==": lambda x, y: x == y, "!=": lambda x, y: x != y, "in": lambda x, y: x in y, "true": lambda x, y: bool(x),
       "false": lambda x, y: not x}


def score_must_show(m):
    try:
        v = METRICS[m["metric"]](m.get("args", {}))
    except (FileNotFoundError, KeyError, IndexError, ValueError, TypeError) as e:
        return {"status": "not_run", "value": None, "why": "%s: %s" % (type(e).__name__, str(e)[:200])}
    bar = m.get("bar", {"op": "true"})
    try:
        ok = OPS[bar["op"]](v, bar.get("value"))
    except TypeError as e:
        return {"status": "not_run", "value": v, "why": "cannot compare: %s" % e}
    return {"status": "pass" if ok else "fail", "value": v}


# ------------------------------------------------------------------------------------------------------------ runner
class Wave:
    def __init__(self, sheet_path, workers=1, mem=0, budget=0, only=None, dry=False):
        self.sheet_path = Path(sheet_path).resolve()
        self.sheet = load_sheet(self.sheet_path)
        self.dir = self.sheet_path.parent
        self.logs = self.dir / "logs"
        self.logs.mkdir(parents=True, exist_ok=True)
        self.workers, self.mem, self.budget, self.only, self.dry = max(1, workers), mem, budget, only, dry
        self.state_path = self.dir / "state.json"
        self.state = {"runs": {}}
        if self.state_path.exists():
            with open(self.state_path, encoding="utf-8") as fh:
                self.state = json.load(fh)
        self.lock = threading.Lock()
        self.t0 = time.time()
        self.cls = {r["id"]: r["class"] for r in self.sheet["runs"]}

    # ---------------------------------------------------------------- identity
    def identity(self):
        man = self.sheet.get("identity_manifest")
        if not man:
            return {"ok": True, "checked": 0, "note": "no identity manifest declared"}
        mp = RESEARCH / man
        if not mp.exists():
            return {"ok": False, "why": "identity manifest missing: %s" % man}
        if sha_file(mp) != self.sheet.get("code_identity"):
            return {"ok": False, "why": "identity manifest digest differs from the sheet's code_identity"}
        bad = []
        n = 0
        for line in open(mp, encoding="utf-8"):
            if not line.strip():
                continue
            dg, rel = line.rstrip("\n").split("  ", 1)
            n += 1
            p = RESEARCH / rel
            if not p.exists() or sha_file(p) != dg:
                bad.append(rel)
        return {"ok": not bad, "checked": n, "changed_or_missing": bad[:20]}

    # ---------------------------------------------------------------- preflight
    def preflight(self):
        """Disk, Docker memory, and the CPU's BLAS kernel family. Writes env_overrides when the pinned family is missing."""
        pf = {"disk_free_gb": round(shutil.disk_usage(str(RESEARCH)).free / 1e9, 1)}
        images = sorted({self.sheet["profiles"][r["profile"]]["image"] for r in self.sheet["runs"] if r["profile"] != "host"
                         and (not self.only or r["id"] in self.only)})
        if images and not self.dry:
            try:
                pf["docker_mem_gb"] = round(int(subprocess.check_output(
                    ["docker", "info", "--format", "{{.MemTotal}}"], timeout=60).strip()) / 1e9, 1)
            except Exception as e:
                pf["docker_error"] = str(e)[:200]
            built_here = {P["image"] for P in self.sheet["profiles"].values()
                          if P.get("built_by") in {r["id"] for r in self.sheet["runs"]}}
            missing = []
            for img in images:
                if img not in built_here and subprocess.call(["docker", "image", "inspect", img],
                                                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
                    missing.append(img)
            pf["images_missing"] = missing
            try:
                probe = self.sheet.get("cpu_probe_image", images[0])
                flags = subprocess.check_output(["docker", "run", "--rm", "--network", "none", probe, "sh", "-c",
                                                 "grep -m1 '^flags' /proc/cpuinfo"], timeout=600).decode()
                pf["avx512f"], pf["avx2"] = " avx512f" in flags, " avx2" in flags
            except Exception as e:
                pf["cpu_error"] = str(e)[:200]
        pinned = {P.get("env", {}).get("OPENBLAS_CORETYPE") for P in self.sheet.get("profiles", {}).values()} - {None}
        ov = {}
        if "SKYLAKEX" in pinned and pf.get("avx512f") is False:
            ov["OPENBLAS_CORETYPE"] = "HASWELL" if pf.get("avx2") else "SANDYBRIDGE"
            pf["note"] = ("this CPU has no AVX-512: BLAS runs with %s; engine results can differ in the last digits from "
                          "the agent's cache, which the canary digest checks" % ov["OPENBLAS_CORETYPE"])
        self.state["env_overrides"] = ov
        if not self.mem and pf.get("docker_mem_gb"):
            self.mem = round(0.7 * pf["docker_mem_gb"], 1)
            pf["mem_budget_gb"] = self.mem
        self.state["preflight"] = pf
        problems = []
        if pf.get("images_missing"):
            problems.append("docker images missing (build them first): %s" % ", ".join(pf["images_missing"]))
        need_disk = float(self.sheet.get("disk_gb", 0) or 0)
        if need_disk and pf["disk_free_gb"] < need_disk and not self.dry:
            problems.append("free disk %.1f GB < %.1f GB the sheet needs" % (pf["disk_free_gb"], need_disk))
        if pf.get("docker_error"):
            problems.append("docker is not answering: %s" % pf["docker_error"])
        return problems

    # ---------------------------------------------------------------- commands
    def host_env(self, run):
        env = dict(os.environ)
        env.update({k: str(v) for k, v in run.get("env", {}).items()})
        return env

    def argv(self, run, part=None):
        cmd = list(run["cmd"])
        if part is not None:
            cmd += ["--part", "%d/%d" % part]
        prof = run["profile"]
        if prof == "host":
            if cmd and cmd[0] == "python":
                cmd[0] = sys.executable
            return cmd, str(RESEARCH)
        P = self.sheet["profiles"][prof]
        env = dict(P.get("env", {}))
        env.update(self.state.get("env_overrides", {}))
        env.update(run.get("env", {}))
        out = ["docker", "run", "--rm", "--init"]
        if P.get("network", "none") == "none":
            out += ["--network", "none"]
        out += ["-v", "%s:/research" % RESEARCH, "-w", P.get("workdir", "/research")]
        for mnt in P.get("mounts", []):
            src = (ROOT / mnt["src"]).resolve()
            if not src.exists():
                raise FileNotFoundError("mount source missing: %s" % src)
            out += ["-v", "%s:%s%s" % (src, mnt["dst"], ":ro" if mnt.get("ro") else "")]
        for k, v in sorted(env.items()):
            out += ["-e", "%s=%s" % (k, v)]
        if run.get("mem_gb"):
            out += ["--memory", "%dg" % max(1, int(round(run["mem_gb"] + 0.5)))]
        out += [P["image"]] + cmd
        return out, str(RESEARCH)

    def done(self, run, part=None):
        if part is None and run.get("parts"):
            return all(self.done(run, (k, run["parts"])) for k in range(1, run["parts"] + 1))
        d = run["done"]
        if d.get("glob"):                                   # e.g. a result file whose name carries a timestamp
            hits = sorted(glob.glob(str(RESEARCH / d["glob"])))
            if not hits:
                return False
            p = Path(hits[-1])
        else:
            f = d["file"] if part is None else d["file"].replace("{k}", str(part[0])).replace("{n}", str(part[1]))
            p = RESEARCH / f
        if not p.exists():
            return False
        if d.get("contains"):
            return d["contains"] in p.read_text(encoding="utf-8", errors="replace")
        return True

    # ---------------------------------------------------------------- one run
    def run_one(self, run):
        rid = run["id"]
        rec = {"id": rid, "class": run["class"], "start": now(), "parts": []}
        parts = [None] if not run.get("parts") else [(k, run["parts"]) for k in range(1, run["parts"] + 1)]
        status = "ok"
        t0 = time.time()
        for part in parts:
            if run.get("parts") and self.done(run, part):
                rec["parts"].append({"part": part[0], "status": "already_done"})
                continue
            try:
                argv, cwd = self.argv(run, part)
            except FileNotFoundError as e:
                status = "failed"
                rec["error"] = str(e)
                break
            log = self.logs / ("%s%s.log" % (rid, "" if part is None else ".part%d" % part[0]))
            with open(log, "a", encoding="utf-8") as fh:
                fh.write("\n# %s %s\n# argv: %s\n" % (now(), rid, json.dumps(argv)))
                fh.flush()
                if self.dry:
                    rc = 0
                else:
                    rc = subprocess.call(argv, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT,
                                         env=self.host_env(run) if run["profile"] == "host" else None)
            rec["parts"].append({"part": None if part is None else part[0], "exit": rc})
            if rc != 0:
                status = "failed"
                rec["exit"] = rc
                break
        if status == "ok" and run.get("merge"):
            argv, cwd = self.argv(dict(run, cmd=run["merge"]))
            with open(self.logs / ("%s.merge.log" % rid), "a", encoding="utf-8") as fh:
                rc = 0 if self.dry else subprocess.call(argv, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT)
            if rc != 0:
                status, rec["exit"] = "failed", rc
        if status == "ok" and not self.dry and not self.done(run):
            status, rec["error"] = "failed", "exit 0 but the done test fails: %s" % json.dumps(run["done"])
        rec.update(status=status, end=now(), wall_min=round((time.time() - t0) / 60, 2))
        if run.get("cost_from") and status == "ok":
            try:
                rec["usd"] = float(m_json(run["cost_from"]))
            except Exception as e:      # cost is recorded, never decided on here; the live harness enforces the cap
                rec["usd_error"] = str(e)[:200]
        return rec

    # ---------------------------------------------------------------- loop
    def statuses(self):
        R = {k: v["status"] for k, v in self.state["runs"].items()}
        M = {m["id"]: score_must_show(m)["status"] for m in self.sheet.get("must_shows", [])}
        return M, R

    def save(self):
        with self.lock:
            tmp = self.state_path.with_suffix(".tmp")
            json.dump(self.state, open(tmp, "w"), indent=1)
            os.replace(tmp, self.state_path)

    def waiting_on(self, run, running, pending):
        ms, rs = refs(run.get("when"))
        rs = set(rs)
        for r in self.sheet["runs"]:
            if ms & set(r.get("decides", [])):
                rs.add(r["id"])
        rs.discard(run["id"])
        live = set(running) | {p["id"] for p in pending}
        return bool(rs & live)

    def order(self):
        runs = [r for r in self.sheet["runs"] if not self.only or r["id"] in self.only]
        return sorted(runs, key=lambda r: (CLASS_ORDER[r["class"]], r.get("est_min", 0), r["id"]))

    def run(self):
        ident = self.identity()
        self.state["identity"] = ident
        self.state["host"] = {"platform": platform.platform(), "python": platform.python_version(), "cpus": os.cpu_count(),
                              "workers": self.workers, "mem_gb": self.mem, "started": self.state.get("host", {}).get("started", now())}
        if not ident["ok"]:
            self.save()
            self.write_verdict()
            print("[wave] REFUSED: code identity does not match the sheet (%s)" % (ident.get("why") or ident.get("changed_or_missing")))
            return 2
        problems = self.preflight()
        self.save()
        if problems:
            self.write_verdict()
            print("[wave] REFUSED by preflight:\n  " + "\n  ".join(problems))
            return 2
        if self.state["preflight"].get("note"):
            print("[wave] note: " + self.state["preflight"]["note"])
        pending = self.order()
        running = {}
        mem_in_use = 0.0
        while pending or running:
            # reap
            for rid, (th, res, memgb) in list(running.items()):
                if not th.is_alive():
                    self.state["runs"][rid] = res[0]
                    mem_in_use -= memgb
                    del running[rid]
                    self.save()
                    self.write_verdict()
                    print("[wave] %-28s %-7s %6.1f min" % (rid, res[0]["status"], res[0]["wall_min"]), flush=True)
            M, R = self.statuses()
            started = False
            for run in list(pending):
                rid = run["id"]
                if self.state["runs"].get(rid, {}).get("status") == "ok" and self.done(run):
                    pending.remove(run)
                    continue
                deps = run.get("depends_on", [])
                if any(d in running or any(p["id"] == d for p in pending) for d in deps):
                    continue                                   # a dependency has not finished
                if any(self.state["runs"].get(d, {}).get("status") != "ok" for d in deps):
                    self.state["runs"][rid] = {"id": rid, "status": "skipped", "why": "dependency not ok", "end": now()}
                    pending.remove(run)
                    self.save()
                    continue
                if self.waiting_on(run, running, pending):
                    continue                                   # the condition reads a run that has not finished
                if CLASS_ORDER[run["class"]] > 0 and any(self.cls[x] == "A0" for x in running):
                    continue                                   # static checks finish before anything else starts
                if not cond(run.get("when"), M, R):
                    self.state["runs"][rid] = {"id": rid, "status": "skipped", "why": "when: %s" % run["when"], "end": now()}
                    pending.remove(run)
                    self.save()
                    print("[wave] %-28s skipped (when: %s)" % (rid, run["when"]), flush=True)
                    continue
                if not run.get("parts") and self.done(run):
                    self.state["runs"][rid] = {"id": rid, "status": "ok", "why": "done test already passes", "end": now()}
                    pending.remove(run)
                    self.save()
                    continue
                if self.budget and time.time() - self.t0 > self.budget:
                    break
                need = float(run.get("mem_gb", 0) or 0)
                if len(running) >= self.workers or (self.mem and running and mem_in_use + need > self.mem):
                    break
                res = [None]
                th = threading.Thread(target=lambda r=run, out=res: out.__setitem__(0, self.run_one(r)), daemon=True)
                th.start()
                running[rid] = (th, res, need)
                mem_in_use += need
                pending.remove(run)
                started = True
                print("[wave] %-28s started (%s, est %s min)" % (rid, run["class"], run.get("est_min", "?")), flush=True)
            if self.budget and time.time() - self.t0 > self.budget and not running:
                print("[wave] budget used; run the same command again to resume")
                break
            if not started:
                time.sleep(0.2)
        self.state["host"]["finished"] = now()
        self.save()
        v = self.write_verdict()
        print("[wave] must-shows: %s" % ", ".join("%s=%s" % (k, x["status"]) for k, x in v["must_shows"].items()))
        print("[wave] decisions matched: %s" % ("; ".join(d["then"] for d in v["decisions_matched"]) or "no rule matched"))
        return 0

    # ---------------------------------------------------------------- verdict
    def write_verdict(self):
        ms = {}
        for m in self.sheet.get("must_shows", []):
            s = score_must_show(m)
            ms[m["id"]] = dict(s, bundle=m.get("bundle"), metric=m["metric"], bar=m.get("bar"), gate=bool(m.get("gate")))
        M = {k: v["status"] for k, v in ms.items()}
        R = {k: v["status"] for k, v in self.state["runs"].items()}
        matched = [d for d in self.sheet.get("decisions", []) if cond(d["if"], M, R)]
        runs = {}
        for r in self.sheet["runs"]:
            st = self.state["runs"].get(r["id"], {"status": "not_run"})
            runs[r["id"]] = {k: st.get(k) for k in ("status", "wall_min", "exit", "error", "why", "usd") if st.get(k) is not None}
        v = {"wave": self.sheet["wave"], "written": now(), "code_identity": self.sheet.get("code_identity"),
             "identity": self.state.get("identity"), "host": self.state.get("host"), "preflight": self.state.get("preflight"), "env_overrides": self.state.get("env_overrides", {}),
             "runs": runs, "must_shows": ms, "decisions_matched": matched,
             "no_rule_matched": not matched, "usd_total": round(sum(x.get("usd", 0) or 0 for x in runs.values()), 4)}
        tmp = self.dir / "verdict.tmp"
        json.dump(v, open(tmp, "w"), indent=1, default=str)
        os.replace(tmp, self.dir / "verdict.json")
        return v


# ------------------------------------------------------------------------------------------------------------ pack
def pack(sheet_path):
    sheet_path = Path(sheet_path).resolve()
    sheet = load_sheet(sheet_path)
    d = sheet_path.parent
    out = d / ("return_%s.zip" % sheet["wave"])
    files = [d / "verdict.json", d / "state.json", sheet_path]
    for pat in sheet.get("return_files", []):
        files += [Path(p) for p in sorted(glob.glob(str(RESEARCH / pat), recursive=True))]
    skipped = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        seen = set()
        for f in files:
            if not f.is_file() or f in seen:
                continue
            seen.add(f)
            if f.stat().st_size > MAX_RETURN_FILE:
                skipped.append(str(f.relative_to(RESEARCH)))
                continue
            z.write(f, str(f.relative_to(RESEARCH)))
        for log in sorted((d / "logs").glob("*.log")):              # only the tail of each log
            txt = log.read_text(encoding="utf-8", errors="replace")
            z.writestr(str(log.relative_to(RESEARCH)) + ".tail", txt[-4000:])
        z.writestr("PACKED.json", json.dumps({"packed": now(), "skipped_over_5MB": skipped}, indent=1))
    print("[wave] packed %s (%.1f KB); %d files over 5 MB left on this machine" % (out, out.stat().st_size / 1024, len(skipped)))
    return out


def identity(sheet_path, globs):
    """Agent side: hash every file matching the globs into the sheet's identity manifest; set code_identity."""
    sheet_path = Path(sheet_path).resolve()
    sheet = json.load(open(sheet_path, encoding="utf-8"))
    files = sorted({p for g in globs for p in glob.glob(str(RESEARCH / g), recursive=True) if Path(p).is_file()
                    and "__pycache__" not in p})
    man = RESEARCH / sheet["identity_manifest"]
    man.write_text("".join("%s  %s\n" % (sha_file(f), Path(f).relative_to(RESEARCH).as_posix()) for f in files), encoding="utf-8")
    sheet["code_identity"] = sha_file(man)
    sheet["identity_globs"] = list(globs)
    sheet_path.write_text(json.dumps(sheet, indent=1) + "\n", encoding="utf-8")
    print("identity: %d files, %s" % (len(files), sheet["code_identity"][:16]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "score", "pack", "check", "identity"))
    ap.add_argument("--globs", nargs="*", default=[])
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--mem", type=float, default=0, help="GB the parallel runs may claim together (their mem_gb)")
    ap.add_argument("--budget-seconds", type=float, default=0, help="stop starting runs after this many seconds")
    ap.add_argument("--only", default="", help="comma-separated run ids")
    ap.add_argument("--dry", action="store_true", help="print the commands; run nothing")
    a = ap.parse_args()
    if a.cmd == "check":
        s = load_sheet(a.sheet)
        print("sheet ok: %d runs, %d must-shows, %d decisions; est %.0f core-min" % (
            len(s["runs"]), len(s.get("must_shows", [])), len(s.get("decisions", [])),
            sum(r.get("est_min", 0) * (r.get("parts") or 1) for r in s["runs"])))
        return 0
    if a.cmd == "pack":
        pack(a.sheet)
        return 0
    if a.cmd == "identity":
        identity(a.sheet, a.globs)
        return 0
    w = Wave(a.sheet, a.workers, a.mem, a.budget_seconds, set(filter(None, a.only.split(","))) or None, a.dry)
    if a.cmd == "score":
        v = w.write_verdict()
        print(json.dumps({k: x["status"] for k, x in v["must_shows"].items()}, indent=1))
        return 0
    return w.run()


if __name__ == "__main__":
    sys.exit(main())
