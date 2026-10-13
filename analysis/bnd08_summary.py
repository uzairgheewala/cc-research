"""BND-08 must-show summary: per-run table, M1-M5 with counts, leak gate, cost and time against the stub estimate.

  python analysis/bnd08_summary.py --out analysis/results/stability_s2/bnd08_summary.json

Inputs: plans/results/<live result index>, runs/<id>/summary.json, analysis/results/stability_s2/{s2_verdicts,partial_stages,
neutral_leak_scan}.json, jobs/bootstrap_replay_ca_dev/out/replay_dev.json (M1 on the dev split only, as fixed in
bootstrap_replay_ca.py), analysis/results/stub_cost/bnd08_estimate.json.
M1: share of usable dev replay files in which the pipeline's bootstrap step (S1) has lower adjacency F1 than PC's output (S0);
thresholds read from the replay file's header. M5 belongs to the optional names-only part d, which was not run.
"""
import argparse
import glob
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S2 = ROOT / "analysis" / "results" / "stability_s2"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", default=None, help="plan result index (default: the newest bnd08_live one)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res_f = Path(a.result) if a.result else sorted((ROOT / "plans" / "results").glob("*_bnd08_live.result.json"))[-1]
    res = json.loads(res_f.read_text(encoding="utf-8"))
    m = json.loads((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_text(encoding="utf-8"))
    part = json.loads((S2 / "partial_stages.json").read_text(encoding="utf-8"))
    reached = {r["arm"]: r for r in part["by_arm"]}
    runs, ptok, ctok, wall = [], 0, 0, []
    for r in res["results"]:
        s = json.loads((ROOT / "runs" / r["run_id"] / "summary.json").read_text(encoding="utf-8"))
        ms = s["must_show"]
        code = r["run_id"].split("_s2_")[1][:4]
        ll = ms["3_llm_calls"]
        ptok += ll["tokens"]["prompt_tokens"]
        ctok += ll["tokens"]["completion_tokens"]
        wall.append(float(s["pipeline_wall_time_s"]))
        runs.append({"run_id": r["run_id"], "arm": code, "family": m["arms"][code]["family"], "role": m["arms"][code]["role"],
                     "exit_code": r["exit_code"], "status": s["status"], "code_identity": ms["1_code_identity"],
                     "models": ll.get("served_models"), "algorithm": (ms.get("5_selection") or {}).get("algorithm"),
                     "stage_reached": "final" if s["status"] == "COMPLETED" else ("S3 (crashed in the cycle step)" if reached[code]["with_S3"] else "before S3"),
                     "failed_at": ms["2_pipeline"] if s["status"] != "COMPLETED" else None,
                     "prompt_tokens": ll["tokens"]["prompt_tokens"], "completion_tokens": ll["tokens"]["completion_tokens"],
                     "wall_s": float(s["pipeline_wall_time_s"]), "repo_after_run": ms["10_repo_after_run"]})
    rep = json.loads((ROOT / "jobs" / "bootstrap_replay_ca_dev" / "out" / "replay_dev.json").read_text(encoding="utf-8"))
    ok = [x for x in rep["rows"] if x["status"] == "ok"]
    m1_hits = sum(x["score_S1"]["adj_f1"] < x["score_S0"]["adj_f1"] for x in ok)
    h = rep["header"]["M1"]
    share = m1_hits / len(ok)
    m1 = {"text": h["text"], "split": "dev", "files": len(ok), "errors": len(rep["rows"]) - len(ok), "hits": m1_hits, "share": share,
          "verdict": "SUPPORTED" if share >= h["supported_if_share_at_least"] else ("REFUTED" if share <= h["refuted_if_share_at_most"] else "INCONCLUSIVE")}
    ver = json.loads((S2 / "s2_verdicts.json").read_text(encoding="utf-8"))
    leak = json.loads((S2 / "neutral_leak_scan.json").read_text(encoding="utf-8"))
    est = json.loads((ROOT / "analysis" / "results" / "stub_cost" / "bnd08_estimate.json").read_text(encoding="utf-8"))
    e = {c: {k: sum(r["estimate"][c][k] for r in est["stub_runs"]) / len(est["stub_runs"]) * len(runs) for k in ("prompt_tokens", "completion_tokens")}
         for c in ("crash", "loop")}
    out = {"tickets": ["BND-08", "AUD-10", "AUD-11", "DLV-02"], "result_index": str(res_f.relative_to(ROOT)), "runs": runs,
           "exit_codes": {str(k): sum(1 for r in runs if str(r["exit_code"]) == str(k)) for k in sorted({str(r["exit_code"]) for r in runs})},
           "reruns": [], "all_code_identity_ok": all(r["code_identity"] == "OK" for r in runs),
           "all_repo_intact": all(r["repo_after_run"].get("baseline_files_intact") for r in runs),
           "snapshots": sorted({x for r in runs for x in (r["models"] or [])}),
           "M1": m1, "M2": ver["M2"], "M2_sensitivity": ver["M2_sensitivity_unnumbered_names"], "M3": ver["M3"], "M4": ver["M4"],
           "M5": {"verdict": "NOT RUN", "why": "optional part d (names-only calls) was not part of the approved live plan"},
           "L1_neutral_leak_scan": leak["gate_L1_no_leak_before_final_graph"], "Q_gates": part["gates"],
           "cost": {"prompt_tokens": ptok, "completion_tokens": ctok, "per_run": [round(ptok / len(runs)), round(ctok / len(runs))],
                    "stub_estimate_30_runs": e, "usd_at_2.50_10_per_M": round(ptok * 2.5e-6 + ctok * 1e-5, 2)},
           "time": {"wall_s_min": min(wall), "wall_s_median": st.median(wall), "wall_s_max": max(wall)},
           "crashes": part["cycle_step"]}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: (v.get("verdict") if isinstance(v, dict) and "verdict" in v else v) for k, v in out.items() if k not in ("runs",)}, indent=1, default=str)[:2500])


if __name__ == "__main__":
    main()
