"""Verify every tracker item's evidence and compute its evidence level. No LLM, no network, read-only on evidence.

  python tracker/verify.py                      check everything, write status.json / status.md, append evidence_log.jsonl
  python tracker/verify.py --repin ID [ID ...]  accept the current hashes of those items' evidence (after a deliberate change)
  python tracker/verify.py --reproduced ID --note "what was rerun"   record that the producing command was re-run (V4)

Evidence levels
  V0 claimed     no evidence recorded
  V1 pointer     evidence named but not checkable from here (project doc, chat, Slack, URL), or checkable files missing
  V2 pinned      every file evidence exists and its hash matches the pin taken when it was first verified
  V3 asserted    V2, and every machine check on the evidence passes now
  V4 reproduced  V3, and a reproduction of the producing command was recorded after the current pins

Closure rule: an item may be "done" only at V2 or above, and at V3 or above when it has checks.
A done item below its required level, or whose pinned evidence changed (drift), is reported as "reopened".
"""
import argparse, datetime, glob, hashlib, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
REPO = RESEARCH.parent / "Causal-Copilot"
sys.path.insert(0, str(HERE))
import catalogue as C  # noqa: E402

PINS = HERE / "pins.json"
LOG = HERE / "evidence_log.jsonl"
EMOJI = {"done": "✅", "done_needs_evidence": "✅", "in_progress": "👀", "todo": "⏳", "blocked": "🔴", "open": "🔵", "reopened": "👀"}
POINTER_PREFIXES = ("project:", "chat:", "slack:", "url:")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve(p):
    p = p.split(" (")[0].strip()          # drop trailing "(section ...)" notes
    if p.startswith("repo:"):
        return REPO / p[5:]
    return RESEARCH / p


# File-hash cache (local only; .gitignored). Rehashing every manifest-listed file on each run takes over three minutes on
# a cold Windows mount (the Causal Chambers extract alone is 34 s), more than the device shell allows. A file whose size
# and modification time (ns) are unchanged keeps its hash. CI never has the cache, so every CI run hashes from scratch;
# VERIFY_NO_CACHE=1 does the same locally.
_HC_PATH = HERE / ".hash_cache.json"
_HC = None
_HC_NEW = [0]


def _use_cache():
    return os.environ.get("VERIFY_NO_CACHE") != "1"


def _hc():
    global _HC
    if _HC is None:
        _HC = {}
        if _use_cache() and _HC_PATH.exists():
            try:
                _HC = json.load(open(_HC_PATH, encoding="utf-8"))
            except (OSError, ValueError):
                _HC = {}
    return _HC


def save_hash_cache():
    if _use_cache() and _HC is not None:
        tmp = _HC_PATH.with_suffix(".tmp")
        json.dump(_HC, open(tmp, "w", encoding="utf-8"))
        os.replace(tmp, _HC_PATH)


def sha(path):
    st = os.stat(path)
    key, sig = str(Path(path).resolve()), "%d:%d" % (st.st_size, st.st_mtime_ns)
    cache = _hc()
    hit = cache.get(key)
    if _use_cache() and hit and hit[0] == sig:
        return hit[1]
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    d = h.hexdigest()
    cache[key] = [sig, d]
    _HC_NEW[0] += 1
    if _HC_NEW[0] % 200 == 0:          # a run cut short by a time limit still leaves its work behind
        save_hash_cache()
    return d


DIGEST_POSIX = True   # s33: digests use POSIX relative paths and POSIX order on every OS


def _posix_rel(f, base):
    return Path(os.path.relpath(f, base)).as_posix()


def digest(ev):
    """Hash of one evidence entry: a file, or every file under a directory / glob (sorted names + hashes)."""
    target = resolve(ev)
    raw = ev.split(" (")[0].strip()
    if any(ch in raw for ch in "*?["):
        files = sorted(glob.glob(str(target)), key=lambda f: Path(f).as_posix())
    elif target.is_dir():
        # generated caches are not evidence and are not in git: a pin taken on a machine with __pycache__ must equal CI's
        files = sorted((str(p) for p in target.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"),
                       key=lambda f: Path(f).as_posix())
        if len(files) > 2000:                      # large trees: hash names and sizes only
            h = hashlib.sha256()
            for f in files:
                h.update(("%s:%d\n" % (_posix_rel(f, target), os.path.getsize(f))).encode())
            return "tree:" + h.hexdigest(), len(files)
    elif target.is_file():
        return sha(target), 1
    else:
        return None, 0
    if not files:
        return None, 0
    h = hashlib.sha256()
    for f in files:
        h.update(("%s:%s\n" % (_posix_rel(f, RESEARCH.parent), sha(f))).encode())
    return "set:" + h.hexdigest(), len(files)


_METAS = {}


def _meta(f):
    """runs/<id>/meta.json, parsed once per process: several items check the same 159 runs, and each meta.json carries
    the code-tree identity listing (a full re-read per check took most of a verify run on the Windows mount)."""
    if f not in _METAS:
        _METAS[f] = json.load(open(f, encoding="utf-8"))
    return _METAS[f]


def get(obj, ptr):
    for k in ptr:
        obj = obj[k]
    return obj


def run_check(c):
    t = c["t"]
    try:
        if t == "exists":
            return resolve(c["path"]).exists(), "exists" if resolve(c["path"]).exists() else "missing"
        if t == "absent":
            return not resolve(c["path"]).exists(), "absent" if not resolve(c["path"]).exists() else "present"
        if t == "count":
            n = len(glob.glob(str(resolve(c["glob"]))))
            return n == c["eq"], "count %d (want %d)" % (n, c["eq"])
        if t == "grep":
            txt = resolve(c["path"]).read_text(encoding="utf-8", errors="replace")
            ok = re.search(c["pattern"], txt) is not None
            return ok, ("found" if ok else "pattern not found") + ": " + c["pattern"]
        if t == "json":
            v = get(json.load(open(resolve(c["path"]), encoding="utf-8")), c["ptr"])
            op, want = c["op"], c.get("v")
            ok = {"eq": lambda: v == want, "ge": lambda: v >= want, "le": lambda: v <= want, "true": lambda: v is True,
                  "false": lambda: v is False, "approx": lambda: abs(v - want) <= c.get("tol", 1e-9),
                  "len_eq": lambda: len(v) == want}[op]()
            return ok, "%s = %s (%s %s)" % ("/".join(map(str, c["ptr"])), json.dumps(v)[:60], op, "" if want is None else json.dumps(want))
        if t == "manifest":
            # every file listed (sha256sum format) still exists with the same hash; files added later do not matter
            bad = []
            for line in open(resolve(c["path"]), encoding="utf-8"):
                if line.strip():
                    h, f = line.rstrip("\n").split("  ", 1)
                    if not (RESEARCH / f).is_file() or sha(RESEARCH / f) != h:
                        bad.append(f)
            return not bad, "%d listed files changed or missing%s" % (len(bad), (": " + ", ".join(bad[:3])) if bad else "")
        if t == "runs":
            files = glob.glob(str(RESEARCH / "runs" / "*" / "meta.json"))
            if c.get("manifest"):           # restrict to the runs that existed when the ticket closed
                listed = {l.split("  ", 1)[1].strip() for l in open(resolve(c["manifest"]), encoding="utf-8") if l.strip()}
                files = [f for f in files if os.path.relpath(f, RESEARCH).replace(os.sep, "/") in listed]
            metas = [_meta(f) for f in files]
            live = [m for m in metas if not m.get("stub_llm")] if c.get("live") else metas
            failed = sum(1 for m in live if m.get("failure"))
            msgs, ok = [], True
            if "expect_total" in c:
                ok &= len(live) == c["expect_total"]; msgs.append("runs %d (want %d)" % (len(live), c["expect_total"]))
            if "expect_completed" in c:
                ok &= len(live) - failed == c["expect_completed"]; msgs.append("completed %d (want %d)" % (len(live) - failed, c["expect_completed"]))
            if "expect_failed" in c:
                ok &= failed == c["expect_failed"]; msgs.append("failed %d (want %d)" % (failed, c["expect_failed"]))
            if c.get("tree_ok"):
                # a run still in progress has no finished_utc and no tree_identity_after yet: not judged until it ends
                running = [m for m in live if "finished_utc" not in m]
                bad = [m.get("run_id") for m in live if "finished_utc" in m and
                       (not (m.get("tree_identity_after") or {}).get("ok") or m.get("new_unexpected_files_in_repo"))]
                ok &= not bad; msgs.append("tree identity bad in %d runs%s" % (len(bad), "; %d still running" % len(running) if running else ""))
            return ok, "; ".join(msgs)
        return False, "unknown check type " + t
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, str(e)[:120])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repin", nargs="*", default=None)
    ap.add_argument("--reproduced", default=None)
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    pins = json.load(open(PINS)) if PINS.exists() else {}
    log = [json.loads(l) for l in open(LOG, encoding="utf-8")] if LOG.exists() else []
    items = {i["id"]: i for i in C.ITEMS}
    stamp = now()
    if a.reproduced:
        assert a.reproduced in items, "unknown item"
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"t": stamp, "item": a.reproduced, "event": "reproduced", "note": a.note}) + "\n")
        print("recorded reproduction for", a.reproduced); return
    out, entries = [], []
    for it in C.ITEMS:
        file_ev = [e for e in it["evidence"] if not e.startswith(POINTER_PREFIXES)]
        ptr_ev = [e for e in it["evidence"] if e.startswith(POINTER_PREFIXES)]
        evrec, missing, drift = [], [], []
        for e in file_ev:
            d, n = digest(e)
            key = "%s|%s" % (it["id"], e)
            if d is None:
                missing.append(e)
            elif key not in pins or (a.repin is not None and (not a.repin or it["id"] in a.repin)):
                pins[key] = {"digest": d, "files": n, "pinned": stamp}
            elif pins[key]["digest"] != d:
                drift.append(e)
            evrec.append({"evidence": e, "digest": d, "files": n})
        checks = [dict(zip(("ok", "detail"), run_check(c)), check=c) for c in it["checks"]]
        failed = [c for c in checks if not c["ok"]]
        if not it["evidence"] and not it["checks"]:
            level = 0
        elif missing or (not file_ev and not checks):
            level = 1
        elif drift:
            level = 1
        else:
            level = 2 if file_ev else 1
            if checks and not failed and level >= 2:
                level = 3
            if checks and not failed and not file_ev:
                level = 3
        last_pin = max([pins.get("%s|%s" % (it["id"], e), {}).get("pinned", "") for e in file_ev] or [""])
        if level == 3 and any(r["item"] == it["id"] and r["event"] == "reproduced" and r["t"] >= last_pin for r in log):
            level = 4
        required = 3 if it["checks"] else 2
        status = it["status"]
        problems = []
        if status == "done" and level < required:
            problems.append("done but evidence level V%d < required V%d" % (level, required))
        if drift:
            problems.append("evidence changed since pinned: " + ", ".join(drift))
        if missing:
            problems.append("evidence missing: " + ", ".join(missing))
        if failed:
            problems.append("failed checks: " + "; ".join(c["detail"] for c in failed))
        # Objective failures (changed, missing or failing evidence) reopen a done item; a done item that is merely
        # below its required level keeps its status and is flagged "needs evidence".
        effective = "reopened" if status == "done" and (drift or failed or missing) else status
        if status == "done" and effective == "done" and level < required:
            effective = "done_needs_evidence"
        rec = {"id": it["id"], "category": C.CATS[it["cat"]], "title": it["title"], "kind": it["kind"], "status": status,
               "effective_status": effective, "emoji": EMOJI[effective], "level": "V%d" % level, "required_level": "V%d" % required if status == "done" else "",
               "criterion": it["criterion"], "evidence": it["evidence"], "pointers": ptr_ev, "checks": [{"ok": c["ok"], "detail": c["detail"]} for c in checks],
               "reproduce": it["reproduce"], "reopen_if": it["reopen_if"], "due": it["due"], "blocked_by": it["blocked_by"], "note": it["note"],
               "problems": problems}
        out.append(rec)
        entries.append({"t": stamp, "item": it["id"], "event": "verify", "status": status, "effective": effective, "level": rec["level"],
                        "evidence": evrec, "checks_failed": len(failed)})
    json.dump(pins, open(PINS, "w"), indent=1, sort_keys=True)
    save_hash_cache()
    with open(LOG, "a", encoding="utf-8") as fh:
        for e in entries:
            fh.write(json.dumps(e) + "\n")
    json.dump({"verified_utc": stamp, "items": out}, open(HERE / "status.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # markdown summary
    L = ["# Tracker status (verified %s)" % stamp, "", "Legend: ✅ done · 👀 in progress (or reopened) · ⏳ to-do · 🔴 blocked · 🔵 open. Evidence levels V0-V4: see README.md.", ""]
    cur = None
    for r in out:
        if r["category"] != cur:
            cur = r["category"]; L += ["", "## " + cur, "", "| ID | | Item | Level | Problems |", "|---|---|---|---|---|"]
        L.append("| %s | %s | %s | %s | %s |" % (r["id"], r["emoji"], r["title"].replace("|", "/"), r["level"], "; ".join(r["problems"]).replace("|", "/")))
    open(HERE / "status.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    done = [r for r in out if r["status"] == "done"]
    print("items %d; done %d (V4 %d, V3 %d, V2 %d, V1 %d); reopened %d; items with problems %d" % (
        len(out), len(done), *[sum(1 for r in done if r["level"] == "V%d" % k) for k in (4, 3, 2, 1)],
        sum(1 for r in out if r["effective_status"] == "reopened"), sum(1 for r in out if r["problems"])))
    print("done but below required evidence level:", [r["id"] for r in out if r["effective_status"] == "done_needs_evidence"])
    for r in out:
        if r["problems"] and r["status"] == "done":
            print("  ", r["id"], r["level"], "|", "; ".join(r["problems"])[:220])


if __name__ == "__main__":
    main()
