"""Compute-job runner (INF-04). Runs one whitelisted cc-research script repeatedly until it reports JOB-COMPLETE, logging every
chunk. Used two ways:
  - in the container, through `cc.ps1 compute <job.json>` (no network, the repo read-only, an empty file mounted over .env);
  - in a time-limited shell, with --max-wall: it stops before the limit and resumes on the next call.

Job file (cc-research/jobs/<name>.json):
  {"id": "smoke", "script": "analysis/smoke_job.py", "args": ["--out", "jobs/smoke/out/smoke.json"],
   "chunk_budget_s": 150, "outputs": ["jobs/smoke/out/smoke.json"]}

Only scripts under analysis/ that use jobkit may be run (whitelist: the job file may not name anything else).
"""
import argparse, datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path

RESEARCH = Path(__file__).resolve().parent.parent


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).exists() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--max-wall", type=float, default=0, help="stop before this many seconds (time-limited shells)")
    a = ap.parse_args()
    t0 = time.time()
    job = json.load(open(a.job, encoding="utf-8"))
    script = (RESEARCH / job["script"]).resolve()
    if RESEARCH / "analysis" not in script.parents or "jobkit" not in script.read_text(encoding="utf-8"):
        sys.exit("refused: job scripts must live in cc-research/analysis and use jobkit")
    d = RESEARCH / "jobs" / job["id"]
    d.mkdir(parents=True, exist_ok=True)
    log = d / "log.jsonl"
    chunk_s = float(job.get("chunk_budget_s", 150))
    n = sum(1 for _ in open(log)) if log.exists() else 0
    while True:
        budget = chunk_s
        if a.max_wall:
            remaining = a.max_wall - (time.time() - t0)
            if remaining < 20:
                print("[job] wall budget used; run again to resume"); return 3
            budget = min(budget, remaining - 10)
        start = now()
        p = subprocess.run([sys.executable, str(script)] + job["args"] + ["--budget-s", "%.0f" % budget],
                           cwd=RESEARCH, capture_output=True, text=True)
        n += 1
        rec = {"chunk": n, "start": start, "end": now(), "rc": p.returncode, "budget_s": round(budget),
               "stdout_tail": p.stdout[-600:], "stderr_tail": p.stderr[-600:], "host": "container" if os.path.exists("/.dockerenv") else "shell"}
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        print("[job] chunk %d rc=%d %s" % (n, p.returncode, p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""))
        if p.returncode == 0 and "JOB-COMPLETE" in p.stdout:
            done = {"job": job["id"], "completed_utc": now(), "chunks": n,
                    "outputs": {o: sha(RESEARCH / o) for o in job.get("outputs", [])}}
            json.dump(done, open(d / "done.json", "w"), indent=1)
            print("[job] complete: %s" % json.dumps(done["outputs"]))
            return 0
        if p.returncode != 3:
            print("[job] failed; see %s" % log); return p.returncode or 1


if __name__ == "__main__":
    sys.exit(main())
