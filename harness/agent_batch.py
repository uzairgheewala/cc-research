"""Run a folder of agent-probe plans one by one (AB-06, AUD-38), each in its own process, with a total spending cap.

  python /research/harness/agent_batch.py --plans /research/plans/ab06 [--stub] [--agent NAME ...] [--arm real ...]
         [--max-usd-total 60] [--retry-failed]

- A plan whose output folder already holds summary.json with status "ok" is skipped (resumable; rerun after a stop).
  Live: a plan whose earlier attempt ended in a crash or cap is also skipped unless --retry-failed is given, so a
  deterministic crash is not paid for twice; spending counts every logged attempt.
- Live: before each run the batch adds the USD recorded in every finished live summary of this plan folder; it stops
  before a run whose ESTIMATED cost (plan basis.stub_est_usd, else its max_usd) would take the total past
  --max-usd-total. Each run is also hard-capped by its own max_calls / max_usd (plan file), so the total can pass the
  cap by at most one run's (max_usd - estimate).
- Exit codes of a run (agent_probe.py): 0 ok, 3 cap reached, 4 agent failed, 2 setup error. Failures are recorded and
  the batch continues; a setup error (2) stops the batch. The batch itself exits 0 when done, 3 at the total cap,
  2 on a setup error.
Writes <plans>/BATCH_<live|stub>.jsonl, one line per run attempted. Never reads or prints the key.
"""
import argparse, json, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def summary(out_dir):
    p = Path(out_dir) / "summary.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans", required=True)
    ap.add_argument("--stub", action="store_true")
    ap.add_argument("--agent", nargs="*", default=None)
    ap.add_argument("--arm", nargs="*", default=None)
    ap.add_argument("--max-usd-total", type=float, default=60.0)
    ap.add_argument("--retry-failed", action="store_true", help="live: rerun plans whose earlier attempt did not end ok")
    a = ap.parse_args()
    plans = sorted(p for p in Path(a.plans).glob("*.json") if p.name != "BUDGET.json")
    sel = []
    for p in plans:
        pl = json.loads(p.read_text(encoding="utf-8"))
        if a.agent and pl["agent"] not in a.agent:
            continue
        if a.arm and pl.get("arm") not in a.arm:
            continue
        sel.append((p, pl))
    log = Path(a.plans) / ("BATCH_%s.jsonl" % ("stub" if a.stub else "live"))
    spent = 0.0
    if not a.stub:
        # every attempt this batch logged (a retried run's earlier cost is kept), plus live runs made outside the batch
        logged = set()
        if log.exists():
            for line in log.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    spent += float(r.get("usd") or 0)
                    logged.add(r["plan"])
        for p in plans:
            if p.name in logged:
                continue
            s = summary(json.loads(p.read_text())["run"]["out"])
            if s and not s.get("stub"):
                spent += float(s.get("est_usd_at_served_prices") or 0)
    print("[batch] %d plans selected (%s), already spent (live summaries) $%.2f, total cap $%.2f"
          % (len(sel), "STUB" if a.stub else "LIVE", spent, a.max_usd_total), flush=True)
    done = failed = 0
    for p, pl in sel:
        out = pl["run"]["out_stub" if a.stub else "out"]
        local_out = out                                   # absolute container path (/research is the cc-research mount)
        s = summary(local_out)
        if s and s.get("status") == "ok":
            continue
        if s and not a.stub and not a.retry_failed:
            print("[batch] skip %s: a live attempt already ended with status %s (use --retry-failed to pay for it again)" % (p.name, s.get("status")))
            continue
        need = float((pl.get("basis") or {}).get("stub_est_usd") or pl["run"]["max_usd"])
        if not a.stub and spent + need > a.max_usd_total:
            print("[batch] stop: the next run's estimate $%.2f would pass the total cap ($%.2f spent of $%.2f)" % (need, spent, a.max_usd_total))
            print("[batch] stopped at the total cap: %d ok, %d not ok, spent $%.2f" % (done, failed, spent))
            return 3
        t = time.time()
        cmd = [sys.executable, str(HERE / "agent_probe.py"), "--plan", str(p)] + (["--stub"] if a.stub else [])
        code = subprocess.run(cmd).returncode
        s = summary(local_out) or {}
        usd = float(s.get("est_usd_at_served_prices") or 0)
        if not a.stub:
            spent += usd
        rec = {"plan": p.name, "agent": pl["agent"], "arm": pl.get("arm"), "scenario": pl.get("scenario_id"), "exit": code,
               "status": s.get("status"), "usd": round(usd, 4), "spent_total": round(spent, 4), "seconds": round(time.time() - t, 1),
               "f1": s.get("directed_f1_random_rule")}
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        done += code == 0
        failed += code != 0
        print("[batch] %s exit %d status %s $%.3f (total $%.2f) F1 %s" % (p.name, code, s.get("status"), usd, spent, s.get("directed_f1_random_rule")), flush=True)
        if code == 2:
            print("[batch] setup error: stopping")
            return 2
    print("[batch] finished: %d ok, %d not ok, spent $%.2f" % (done, failed, spent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
