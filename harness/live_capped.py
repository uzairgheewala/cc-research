"""Run a live plan one run at a time under a dollar cap (INF-10 for live jobs). Host side, standard library only.

Tickets: INF-10, BLD-06

    python harness/live_capped.py --plan plans/fork_bld06_live.json --cap-usd 25 [--model gpt-4o] [--branch B]

Each run of the plan becomes a one-run plan (plans/_capped_<plan>_<k>.json; cc.ps1 reads plans from plans\ only) started with `cc.ps1 plan` (on Windows; any
other host: set CC_PLAN_CMD to the command that runs one plan file). After each run the run's own summary.json gives its
prompt and completion tokens (must_show 3_llm_calls), priced at the served model's list price. A run starts only while
spent + 1.5 x the largest run cost so far stays under the cap, so the cap holds unless one run costs more than 1.5 times
any earlier run. Progress is in plans/results/<plan>.capped.json (resumable: finished runs are not started again).
A provider quota or billing refusal stops the series as an infrastructure stop (status "quota"), never as a result.
"""
import argparse, json, os, platform, subprocess, sys, time
from pathlib import Path

RESEARCH = Path(__file__).resolve().parent.parent
PRICES = {"gpt-4o-mini": (0.15, 0.60), "gpt-4o": (2.50, 10.00), "gpt-4.1": (2.00, 8.00), "gpt-4.1-mini": (0.40, 1.60)}


def price(models):
    m = (models or ["gpt-4o"])[0]
    for k in sorted(PRICES, key=len, reverse=True):
        if m.startswith(k):
            return PRICES[k]
    return PRICES["gpt-4o"]


def run_cost(run_id):
    s = json.loads((RESEARCH / "runs" / run_id / "summary.json").read_text(encoding="utf-8"))
    ll = s["must_show"]["3_llm_calls"]
    pi, po = price(ll.get("served_models"))
    t = ll.get("tokens") or {}
    return (t.get("prompt_tokens", 0) * pi + t.get("completion_tokens", 0) * po) / 1e6, s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--cap-usd", type=float, required=True)
    ap.add_argument("--model", default="")
    ap.add_argument("--branch", default="", help="sets CC_BRANCH for every run (a fork ticket branch)")
    a = ap.parse_args()
    plan_path = RESEARCH / a.plan
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    pid = plan["plan_id"]
    prog_path = RESEARCH / "plans" / "results" / ("%s.capped.json" % pid)
    prog_path.parent.mkdir(parents=True, exist_ok=True)
    prog = json.loads(prog_path.read_text(encoding="utf-8")) if prog_path.exists() else {"plan_id": pid, "cap_usd": a.cap_usd, "runs": {}}
    env = dict(os.environ)
    if a.branch:
        env["CC_BRANCH"] = a.branch
    one_dir = RESEARCH / "plans"
    runs = [r for r in plan["runs"] for _ in range(r.get("repeats", 1))]
    status = "ok"
    for k, r in enumerate(runs):
        key = "%03d" % k
        if prog["runs"].get(key, {}).get("status") == "done":
            continue
        spent = sum(x.get("usd", 0) for x in prog["runs"].values())
        worst = max([x.get("usd", 0) for x in prog["runs"].values()] or [0])
        if spent + 1.5 * worst > a.cap_usd:
            status = "cap"
            break
        one = dict(plan, plan_id="%s_%s" % (pid, key), runs=[dict(r, repeats=1)])
        leaf = "_capped_%s_%s.json" % (pid, key)
        (one_dir / leaf).write_text(json.dumps(one, indent=1), encoding="utf-8")
        before = {p.name for p in (RESEARCH / "plans" / "results").glob("*.result.json")}
        cmd = os.environ.get("CC_PLAN_CMD")
        if cmd:
            argv = cmd.split() + [leaf]
        elif platform.system() == "Windows":
            argv = ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(RESEARCH / "cc.ps1"), "plan", leaf]
            if a.model:
                argv.append(a.model)
        else:
            raise SystemExit("set CC_PLAN_CMD on a non-Windows host")
        t0 = time.time()
        rc = subprocess.call(argv, cwd=str(RESEARCH), env=env)
        new = sorted(set(p.name for p in (RESEARCH / "plans" / "results").glob("*.result.json")) - before)
        rec = {"label": r.get("label"), "dataset": r.get("dataset"), "exit": rc, "wall_min": round((time.time() - t0) / 60, 1)}
        try:
            res = json.loads((RESEARCH / "plans" / "results" / new[-1]).read_text(encoding="utf-8"))
            run_id = res["results"][0]["run_id"]
            usd, s = run_cost(run_id)
            rec.update({"run_id": run_id, "usd": round(usd, 4), "run_status": s.get("status"), "status": "done",
                        "fork": (json.loads((RESEARCH / "runs" / run_id / "meta.json").read_text(encoding="utf-8")).get("fork"))})
            txt = json.dumps(s).lower()
            if "insufficient_quota" in txt or ("billing" in txt and "error" in txt):
                rec["status"], status = "quota", "quota"
        except Exception as e:
            rec.update({"status": "failed", "error": "%s: %s" % (type(e).__name__, str(e)[:200])})
        prog["runs"][key] = rec
        prog["usd_total"] = round(sum(x.get("usd", 0) for x in prog["runs"].values()), 4)
        prog_path.write_text(json.dumps(prog, indent=1), encoding="utf-8")
        print("[capped] %s %s  $%.3f  total $%.2f of $%.2f" % (key, rec.get("status"), rec.get("usd", 0), prog["usd_total"], a.cap_usd), flush=True)
        if status == "quota":
            break
    prog["status"] = status
    prog["usd_total"] = round(sum(x.get("usd", 0) for x in prog["runs"].values()), 4)
    prog["finished"] = sum(1 for x in prog["runs"].values() if x.get("status") == "done") == len(runs)
    prog_path.write_text(json.dumps(prog, indent=1), encoding="utf-8")
    print("[capped] %s: %s, $%.2f, %d of %d runs" % (pid, status, prog["usd_total"],
                                                    sum(1 for x in prog["runs"].values() if x.get("status") == "done"), len(runs)))
    return 0 if status in ("ok",) else 3 if status == "cap" else 4


if __name__ == "__main__":
    sys.exit(main())
