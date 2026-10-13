"""Run a list of traced Causal-Copilot runs, one fresh Python process per run.

  python /research/harness/run_plan.py --plan /research/plans/<file>.json     run one plan and exit
  python /research/harness/run_plan.py --queue                                watch /research/queue/inbox

A plan is data, not code. It can only name: a dataset under the repo's data/dataset (or, with the
prefix "research:", under cc-research/datasets), a data mode, a query string, a label and a repeat
count; plus the plan-level switches "stub_llm" and "interleave" and an optional "run_timeout_s"
(300..10800; it can only shorten the per-run limit). Anything else in the file is rejected.

Queue mode lets plans dropped into queue/inbox start without further typing. It stops when
queue/STOP appears, on Ctrl+C, or after --max-runs runs (default 60).
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cc_common import REPO, RESEARCH  # noqa: E402

ALLOWED_PLAN_KEYS = {"plan_id", "note", "runs", "stub_llm", "interleave", "run_timeout_s"}
ALLOWED_RUN_KEYS = {"label", "dataset", "data_mode", "query", "repeats"}
LABEL_RE = re.compile(r"^[A-Za-z0-9_-]{1,40}$")
QUEUE = RESEARCH / "queue"
RESEARCH_PREFIX = "research:"      # "research:datasets/x/x.csv" -> <cc-research>/datasets/x/x.csv (derived datasets live outside the repo)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def validate(plan):
    errs = []
    if not isinstance(plan, dict):
        return ["plan must be a JSON object"]
    extra = set(plan) - ALLOWED_PLAN_KEYS
    if extra:
        errs.append("unknown plan keys: %s" % sorted(extra))
    if not LABEL_RE.match(str(plan.get("plan_id", ""))):
        errs.append("plan_id must match %s" % LABEL_RE.pattern)
    if not isinstance(plan.get("stub_llm", False), bool):
        errs.append("stub_llm must be true/false")
    if not isinstance(plan.get("interleave", False), bool):
        errs.append("interleave must be true/false")
    rt = plan.get("run_timeout_s")
    if rt is not None and (not isinstance(rt, int) or isinstance(rt, bool) or not 300 <= rt <= 10800):
        errs.append("run_timeout_s must be an integer between 300 and 10800")
    runs = plan.get("runs")
    if not isinstance(runs, list) or not runs:
        return errs + ["runs must be a non-empty list"]
    root = (REPO / "data" / "dataset").resolve()
    for i, r in enumerate(runs):
        tag = "runs[%d]" % i
        if not isinstance(r, dict):
            errs.append(tag + " must be an object")
            continue
        extra = set(r) - ALLOWED_RUN_KEYS
        if extra:
            errs.append("%s unknown keys: %s" % (tag, sorted(extra)))
        if not LABEL_RE.match(str(r.get("label", ""))):
            errs.append("%s label must match %s" % (tag, LABEL_RE.pattern))
        ds = r.get("dataset")
        if not isinstance(ds, str) or os.path.isabs(ds) or "\\" in ds:
            errs.append("%s dataset must be a relative path with forward slashes" % tag)
        elif ds.startswith(RESEARCH_PREFIX):
            base = (RESEARCH / "datasets").resolve()
            full = (RESEARCH / ds[len(RESEARCH_PREFIX):]).resolve()
            if base not in full.parents:
                errs.append("%s a research: dataset must be inside cc-research/datasets" % tag)
            elif not full.exists():
                errs.append("%s dataset not found: %s" % (tag, ds))
        else:
            full = (REPO / ds).resolve()
            if root not in full.parents and full != root:
                errs.append("%s dataset must be inside data/dataset (or use the research: prefix)" % tag)
            elif not full.exists():
                errs.append("%s dataset not found: %s" % (tag, ds))
        if r.get("data_mode") not in ("real", "simulated"):
            errs.append("%s data_mode must be 'real' or 'simulated'" % tag)
        q = r.get("query")
        if q is not None and (not isinstance(q, str) or not q.strip() or len(q) > 4000):
            errs.append("%s query must be null or a non-empty string up to 4000 chars" % tag)
        n = r.get("repeats", 1)
        if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= 25:
            errs.append("%s repeats must be an integer 1..25" % tag)
    return errs


def expand(plan):
    """Ordered list of (run spec, repeat number). With "interleave": true the repeats are taken
    round-robin (repeat 1 of every entry, then repeat 2, ...), so that the time of day and whatever
    the model provider changes over an hour are not confounded with the entry being compared."""
    out = []
    if plan.get("interleave", False):
        for k in range(max(r.get("repeats", 1) for r in plan["runs"])):
            for r in plan["runs"]:
                if k < r.get("repeats", 1):
                    out.append((r, k + 1))
        return out
    for r in plan["runs"]:
        for k in range(r.get("repeats", 1)):
            out.append((r, k + 1))
    return out


def run_plan(plan, budget, run_timeout, force_stub=False):
    """Execute a validated plan. Returns (result dict, runs executed)."""
    stub = bool(plan.get("stub_llm", False)) or force_stub
    run_timeout = min(run_timeout, plan.get("run_timeout_s") or run_timeout)     # a plan may shorten the limit, never extend it
    results, done = [], 0
    todo = expand(plan)
    print("[plan %s] %d run(s)%s" % (plan["plan_id"], len(todo), "  (STUB LLM)" if stub else ""))
    for r, k in todo:
        if done >= budget:
            results.append({"label": r["label"], "repeat": k, "skipped": "run budget for this session reached"})
            continue
        ds = Path(r["dataset"]).name.replace(".csv", "")
        run_id = "%s_%s_%s_r%02d%s_%s" % (utc(), r["label"], ds, k, "_STUB" if stub else "", uuid.uuid4().hex[:6])
        ds_arg = r["dataset"]
        if ds_arg.startswith(RESEARCH_PREFIX):
            ds_arg = str(RESEARCH / ds_arg[len(RESEARCH_PREFIX):]).replace(os.sep, "/")
        cmd = [sys.executable, str(HERE / "run_traced.py"), "--dataset", ds_arg, "--data-mode", r["data_mode"],
               "--label", r["label"], "--run-id", run_id]
        if r.get("query") is not None:
            cmd += ["--query", r["query"]]
        if stub:
            cmd.append("--stub-llm")
        t = time.time()
        print("\n[plan %s] starting %s (repeat %d)" % (plan["plan_id"], run_id, k))
        try:
            code = subprocess.run(cmd, cwd=str(REPO), timeout=run_timeout).returncode
        except subprocess.TimeoutExpired:
            code = "timeout after %ds" % run_timeout
        done += 1
        results.append({"run_id": run_id, "label": r["label"], "repeat": k, "exit_code": code,
                        "duration_s": round(time.time() - t, 1)})
    return {"plan_id": plan["plan_id"], "finished_utc": utc(), "stub_llm": stub, "results": results}, done


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def queue_loop(max_runs, poll, run_timeout, force_stub):
    dirs = {n: QUEUE / n for n in ("inbox", "running", "done", "rejected")}
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    stop = QUEUE / "STOP"
    if stop.exists():
        stop.rename(QUEUE / ("STOP.consumed_%s" % utc()))
    used = 0
    print("[queue] watching %s  (budget %d runs; create %s or press Ctrl+C to stop)" % (dirs["inbox"], max_runs, stop))
    while True:
        (QUEUE / "heartbeat.json").write_text(json.dumps(
            {"utc": utc(), "state": "idle", "runs_used": used, "max_runs": max_runs, "pid": os.getpid()}), encoding="utf-8")
        if stop.exists():
            stop.rename(QUEUE / ("STOP.consumed_%s" % utc()))
            print("[queue] STOP file found, exiting")
            break
        if used >= max_runs:
            print("[queue] run budget (%d) used up, exiting. Restart the watcher to continue." % max_runs)
            break
        pending = sorted(p for p in dirs["inbox"].glob("*.json"))
        if not pending:
            time.sleep(poll)
            continue
        src = pending[0]
        stamp = utc()
        try:
            plan = load(src)
            errs = validate(plan)
        except Exception as e:
            plan, errs = None, ["unreadable JSON: %r" % (e,)]
        if errs:
            dst = dirs["rejected"] / ("%s_%s" % (stamp, src.name))
            src.rename(dst)
            Path(str(dst) + ".errors.json").write_text(json.dumps(errs, indent=2), encoding="utf-8")
            print("[queue] REJECTED %s: %s" % (src.name, errs))
            continue
        running = dirs["running"] / src.name
        src.rename(running)
        (QUEUE / "heartbeat.json").write_text(json.dumps(
            {"utc": utc(), "state": "running", "plan": plan["plan_id"], "runs_used": used, "max_runs": max_runs,
             "pid": os.getpid()}), encoding="utf-8")
        result, n = run_plan(plan, max_runs - used, run_timeout, force_stub)
        used += n
        base = "%s_%s" % (stamp, src.name)
        running.rename(dirs["done"] / base)
        (dirs["done"] / (base + ".result.json")).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("[queue] finished plan %s (%d run(s); %d/%d of budget used)" % (plan["plan_id"], n, used, max_runs))
    (QUEUE / "heartbeat.json").write_text(json.dumps(
        {"utc": utc(), "state": "stopped", "runs_used": used, "max_runs": max_runs}), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--plan")
    g.add_argument("--queue", action="store_true")
    g.add_argument("--validate", help="check a plan file and exit")
    ap.add_argument("--max-runs", type=int, default=60)
    ap.add_argument("--poll", type=int, default=20, help="seconds between inbox checks (queue mode)")
    ap.add_argument("--run-timeout", type=int, default=3 * 3600, help="seconds allowed per run")
    ap.add_argument("--stub-llm", action="store_true", help="force every run to use the offline stub")
    a = ap.parse_args()
    if a.validate:
        errs = validate(load(a.validate))
        print("VALID" if not errs else "INVALID:\n  " + "\n  ".join(errs))
        sys.exit(0 if not errs else 1)
    if a.queue:
        try:
            queue_loop(a.max_runs, a.poll, a.run_timeout, a.stub_llm)
        except KeyboardInterrupt:
            print("\n[queue] interrupted, exiting")
        return
    plan = load(a.plan)
    errs = validate(plan)
    if errs:
        print("INVALID PLAN:\n  " + "\n  ".join(errs))
        sys.exit(1)
    result, _ = run_plan(plan, a.max_runs, a.run_timeout, a.stub_llm)
    out = RESEARCH / "plans" / "results"
    out.mkdir(parents=True, exist_ok=True)
    path = out / ("%s_%s.result.json" % (utc(), plan["plan_id"]))
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("\n[plan %s] done. Result index: %s" % (plan["plan_id"], path))
    for r in result["results"]:
        print("   %s" % r)
    bad = [r for r in result["results"] if r.get("exit_code") != 0]
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
