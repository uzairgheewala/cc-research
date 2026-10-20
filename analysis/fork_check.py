"""INF-06 / BLD-06 / EXT-03: what the fork branches' stub (or live) runs show, from their run folders. Read-only.

Tickets: INF-06, BLD-06, EXT-03

    python analysis/fork_check.py --plan fork_bld06_stub      -> analysis/results/fork/fork_bld06_stub.json

Per run: the branch identity the harness recorded (meta.json fork: branch, commit, head_ok, patch sha256), the pipeline
status, whether the cycle step crashed (KeyError 'nodes' in the failure), and whether the console shows refinement v2
running ("Refinement v2 (" from the BLD-06 branch's Judge). For capped live plans, reads plans/results/<plan>.capped.json.
"""
import argparse, glob, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_ids(plan):
    capped = ROOT / "plans" / "results" / ("%s.capped.json" % plan)
    if capped.exists():
        return [r["run_id"] for r in json.loads(capped.read_text())["runs"].values() if r.get("run_id")]
    res = sorted(glob.glob(str(ROOT / "plans" / "results" / ("*_%s.result.json" % plan))))
    if not res:
        return []
    return [r["run_id"] for r in json.loads(Path(res[-1]).read_text())["results"] if r.get("run_id")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    a = ap.parse_args()
    rows = []
    for rid in run_ids(a.plan):
        d = ROOT / "runs" / rid
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
        summ = json.loads((d / "summary.json").read_text(encoding="utf-8"))
        con = (d / "console.log").read_text(encoding="utf-8", errors="replace") if (d / "console.log").exists() else ""
        fail = json.dumps(meta.get("failure") or summ.get("must_show", {}).get("2_pipeline", ""))
        rows.append({"run_id": rid, "status": summ.get("status"), "fork": meta.get("fork"),
                     "identity": summ.get("must_show", {}).get("1_code_identity"),
                     "cycle_step_keyerror": "KeyError" in fail and "nodes" in fail,
                     "refinement_v2_ran": "Refinement v2 (" in con})
    out = {"tickets": ["INF-06", "BLD-06", "EXT-03"], "plan": a.plan, "runs": len(rows),
           "identity_ok_all": bool(rows) and all(r["identity"] == "OK" and (r["fork"] or {}).get("head_ok") for r in rows),
           "completed": sum(1 for r in rows if r["status"] == "COMPLETED"),
           "cycle_step_keyerrors": sum(1 for r in rows if r["cycle_step_keyerror"]),
           "refinement_v2_ran": sum(1 for r in rows if r["refinement_v2_ran"]),
           "branches": sorted({(r["fork"] or {}).get("branch") or "?" for r in rows}), "rows": rows}
    p = ROOT / "analysis" / "results" / "fork" / ("%s.json" % a.plan)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))
    return 0 if rows else 1


if __name__ == "__main__":
    sys.exit(main())
