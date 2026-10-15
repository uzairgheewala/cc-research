"""Run a folder of agent-probe plans (AB-06, AUD-38), each in its own process, with a total spending cap.

  python /research/harness/agent_batch.py --plans /research/plans/ab06 [--stub] [--agent NAME ...] [--arm real ...]
         [--scenario NAME ...] [--tier A] [--workers N] [--max-usd-total 60] [--retry-failed]

- Plans are the files named <agent>__<scenario>__<arm>.json; other JSON files in the folder (BUDGET.json) are not plans.
- A plan whose output folder already holds summary.json with status "ok" is skipped (resumable; rerun after a stop).
  Live: a plan whose earlier attempt ended in a crash or cap is also skipped unless --retry-failed is given, so a
  deterministic crash is not paid for twice. A run stopped by Ctrl-C (status "interrupted") resumes without the flag.
  A retried or resumed run replays its earlier answers for free (harness/probe_llm.py),
  so only new calls are counted as spent ("usd_new").
- Spending (v2.1, 14 Oct, amendment 1): read from the call logs themselves. Every non-replayed live call record in every
  plan's calls*.jsonl carries its cost, so a run killed without a summary (a machine restart, 14 Oct ~08:29 UTC) is still
  counted. The log's usd/usd_new stay as per-attempt records.
- v2.2: a run stopped because the provider has no credits left ("aborted_quota", or an older "failed" whose message
  says so) resumes like a cap hit, and the first such stop ends the launching of new runs (exit 5).
- A run that ended "aborted_cap" or "interrupted" resumes without --retry-failed: neither is an agent failure, and the
  resume replays every paid answer free. "failed" (an agent failure) still needs --retry-failed.
- --workers N (v2, 14 Oct): up to N runs at once, interleaved across agents so concurrent runs use different models
  where possible. Before a run starts, the batch requires
      spent + (max_usd of every run still going) + (this run's estimate) <= --max-usd-total,
  i.e. running runs are reserved at their hard cap. The total can therefore pass the cap by at most one run's
  (max_usd - estimate), the same guarantee as one worker. With N > 1 each run's own output goes to
  <out>/probe_console.log and the batch prints one line per run.
- --tier NAME keeps only the plans listed under tiers[NAME] in <plans>/TIERS.json (AB-06: A and B, fixed before the
  live grid in plans/ab06_prereg.json); it combines with the other filters.
- The estimate is the plan's basis.live_est_usd (plans/calibrate_ab06.py), else basis.stub_est_usd, else max_usd.
- Exit codes of a run (agent_probe.py): 0 ok, 3 cap reached, 4 agent failed, 2 setup error. Failures are recorded and
  the batch continues; a setup error (2) stops new runs. The batch exits 0 when done, 3 at the total cap, 2 on a setup
  error.
Writes <plans>/BATCH_<live|stub>.jsonl, one line per run attempted. Never reads or prints the key.
"""
import argparse, json, os, subprocess, sys, time
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBE = Path(os.environ.get("AB06_PROBE_SCRIPT") or HERE / "agent_probe.py")    # override: tests only


def summary(out_dir):
    p = Path(out_dir) / "summary.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        return None


def usd_new(s):
    """USD of the calls actually sent in this attempt (replayed answers excluded when the summary says so)."""
    if not s:
        return 0.0
    v = s.get("est_usd_new_at_served_prices")
    return float(v if v is not None else (s.get("est_usd_at_served_prices") or 0))


def calls_spent(out_dir):
    """USD of the live calls actually sent into out_dir (all attempts): non-replayed, non-stub call records."""
    tot = 0.0
    for f in sorted(Path(out_dir).glob("calls*.jsonl")):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if '"usd"' not in line:
                    continue
                try:
                    r = json.loads(line)
                except ValueError:               # a line cut short by a hard stop: its call was never accounted
                    continue
                if "request" in r and not r.get("replayed") and not r.get("stub"):
                    tot += float(r.get("usd") or 0)
    return tot


RESUMABLE = ("aborted_cap", "interrupted", "aborted_quota")
QUOTA_MARKERS = ("insufficient_quota", "no credits remaining", "exceeded your current quota", "quota exceeded")


def quota_failure(s):
    """True when a run stopped because the provider refused for billing. Since v2.2 the gate stops such runs as
    'aborted_quota'; older runs recorded them as agent failures, recognised here by the failure message."""
    if not s:
        return False
    if s.get("status") == "aborted_quota":
        return True
    fp = s.get("failure_point") or {}
    return s.get("status") == "failed" and any(m in (fp.get("message") or "").lower() for m in QUOTA_MARKERS)


def resumable(s):
    return s.get("status") in RESUMABLE or quota_failure(s)


def estimate(pl):
    b = pl.get("basis") or {}
    return float(b.get("live_est_usd") or b.get("stub_est_usd") or pl["run"]["max_usd"])


def interleave(sel):
    """Round-robin over agents, keeping each agent's own order."""
    by = OrderedDict()
    for p, pl in sel:
        by.setdefault(pl["agent"], []).append((p, pl))
    out = []
    while any(by.values()):
        for k in list(by):
            if by[k]:
                out.append(by[k].pop(0))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans", required=True)
    ap.add_argument("--stub", action="store_true")
    ap.add_argument("--agent", nargs="*", default=None)
    ap.add_argument("--arm", nargs="*", default=None)
    ap.add_argument("--scenario", nargs="*", default=None)
    ap.add_argument("--tier", default=None)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--max-usd-total", type=float, default=60.0)
    ap.add_argument("--retry-failed", action="store_true", help="live: rerun plans whose earlier attempt did not end ok")
    a = ap.parse_args()
    if a.workers < 1:
        ap.error("--workers must be at least 1")
    plans = sorted(p for p in Path(a.plans).glob("*.json") if p.name.count("__") == 2)
    keep = None
    if a.tier:
        tf = Path(a.plans) / "TIERS.json"
        if not tf.exists():
            ap.error("--tier needs %s" % tf)
        tiers = json.loads(tf.read_text(encoding="utf-8"))["tiers"]
        if a.tier not in tiers:
            ap.error("tier %s not in %s (have %s)" % (a.tier, tf, ", ".join(sorted(tiers))))
        keep = set(tiers[a.tier])
    sel = []
    for p in plans:
        if keep is not None and p.name not in keep:
            continue
        pl = json.loads(p.read_text(encoding="utf-8"))
        if a.agent and pl["agent"] not in a.agent:
            continue
        if a.arm and pl.get("arm") not in a.arm:
            continue
        if a.scenario and pl.get("scenario_id") not in a.scenario:
            continue
        sel.append((p, pl))
    sel = interleave(sel) if a.workers > 1 else sel
    log = Path(a.plans) / ("BATCH_%s.jsonl" % ("stub" if a.stub else "live"))
    by_plan = {}
    if not a.stub:
        for p in plans:
            by_plan[p.name] = calls_spent(json.loads(p.read_text(encoding="utf-8"))["run"]["out"])
    spent = sum(by_plan.values())
    print("[batch] %d plans selected (%s), workers %d, already spent (live) $%.2f, total cap $%.2f"
          % (len(sel), "STUB" if a.stub else "LIVE", a.workers, spent, a.max_usd_total), flush=True)
    done = failed = 0
    stop_code = 0
    queue = list(sel)
    running = []             # dicts: proc, plan path, plan, out, t0, fh

    def finish(job):
        nonlocal spent, done, failed, stop_code
        code = job["proc"].returncode
        if job["fh"]:
            job["fh"].close()
        s = summary(job["out"]) or {}
        u_all = float(s.get("est_usd_at_served_prices") or 0)
        u_new = usd_new(s)
        if not a.stub:
            by_plan[job["p"].name] = calls_spent(job["out"])
            spent = sum(by_plan.values())
        pl = job["pl"]
        rec = {"plan": job["p"].name, "agent": pl["agent"], "arm": pl.get("arm"), "scenario": pl.get("scenario_id"), "exit": code,
               "status": s.get("status"), "usd": round(u_all, 4), "usd_new": round(u_new, 4), "spent_total": round(spent, 4),
               "seconds": round(time.time() - job["t0"], 1), "f1": s.get("directed_f1_random_rule"), "workers": a.workers}
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        done += code == 0
        failed += code != 0
        print("[batch] %s exit %d status %s $%.3f new (total $%.2f) F1 %s" % (job["p"].name, code, s.get("status"), u_new, spent,
                                                                       s.get("directed_f1_random_rule")), flush=True)
        if code == 2:
            print("[batch] setup error: no new runs will start")
            stop_code = 2
        elif quota_failure(s) and not stop_code:
            print("[batch] the provider reports no credits or quota left: no new runs will start. Add credits, then run the "
                  "same command again; stopped runs resume from their recorded answers")
            stop_code = 5

    try:
        while True:
            while queue and len(running) < a.workers and stop_code == 0:
                p, pl = queue[0]
                out = pl["run"]["out_stub" if a.stub else "out"]
                s = summary(out)
                if s and s.get("status") == "ok":
                    queue.pop(0)
                    continue
                if s and not a.stub and not a.retry_failed and not resumable(s):
                    print("[batch] skip %s: a live attempt already ended with status %s (use --retry-failed to pay for it again)"
                          % (p.name, s.get("status")))
                    queue.pop(0)
                    continue
                need = estimate(pl)
                reserved = sum(float(j["pl"]["run"]["max_usd"]) for j in running)
                if not a.stub and spent + reserved + need > a.max_usd_total:
                    if running:
                        break                 # wait: a finishing run releases its reservation
                    print("[batch] stop: the next run's estimate $%.2f would pass the total cap ($%.2f spent of $%.2f)"
                          % (need, spent, a.max_usd_total))
                    stop_code = 3
                    break
                queue.pop(0)
                cmd = [sys.executable, str(PROBE), "--plan", str(p)] + (["--stub"] if a.stub else [])
                fh = None
                if a.workers > 1:
                    Path(out).mkdir(parents=True, exist_ok=True)
                    fh = open(Path(out) / "probe_console.log", "a", encoding="utf-8")
                    print("[batch] start %s (estimate $%.2f, cap $%.2f)" % (p.name, need, pl["run"]["max_usd"]), flush=True)
                proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT if fh else None)
                running.append({"proc": proc, "p": p, "pl": pl, "out": out, "t0": time.time(), "fh": fh})
            if not running:
                break
            finished = [j for j in running if j["proc"].poll() is not None]
            for j in finished:
                running.remove(j)
                finish(j)
            if not finished:
                time.sleep(0.5)
    except KeyboardInterrupt:
        for j in running:
            j["proc"].terminate()
        for j in running:
            j["proc"].wait()
            finish(j)                     # log what the stopped run spent, so the total stays honest on restart
        print("[batch] interrupted: %d ok, %d not ok, spent $%.2f" % (done, failed, spent))
        return 130
    if stop_code == 3:
        print("[batch] stopped at the total cap: %d ok, %d not ok, spent $%.2f" % (done, failed, spent))
        return 3
    if stop_code == 2:
        print("[batch] stopped after a setup error: %d ok, %d not ok, spent $%.2f" % (done, failed, spent))
        return 2
    if stop_code == 5:
        print("[batch] stopped: provider quota exhausted: %d ok, %d not ok, spent $%.2f" % (done, failed, spent))
        return 5
    print("[batch] finished: %d ok, %d not ok, spent $%.2f" % (done, failed, spent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
