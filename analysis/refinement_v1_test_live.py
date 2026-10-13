"""BND-10 part 2: the frozen refinement v1 rule on the live S2 runs' bootstrap tables (test data, read once).

  python analysis/refinement_v1_test_live.py --label s2 --out analysis/results/refinement_v1/test_live_s2.json

Why a separate file: refinement_v1.py is frozen by hash (RULE.json); editing it to add this input would break the freeze.
This driver imports it unchanged, refuses unless its sha256 equals the frozen one, appends to the same access log, and uses
its own v1() and evaluate(), so the rule and the scoring are byte-for-byte the frozen ones.

Items: every non-stub run labelled s2 whose dataset is in datasets/suite_q1s2 and that recorded the bootstrap step (runs that
crashed later, in the cycle step, still have it). One item per run (30 runs: 10 scenarios x real / neutral / swapped names on
identical numbers). Scored against the reference by data (the bootstrap and the algorithm see only data).
Decided before this file first ran (2026-10-12): the BND-10 verdicts are computed on all test tables pooled (the 25 replay
files of part 1 plus these live tables), as BND-09 pooled live tables and replays on dev; each part is also reported alone,
and the live part is also reported per scenario (mean of its three arms) because the three arms share their numbers.
"""
import argparse
import datetime
import glob
import json
import pickle
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import refinement_v1 as R  # noqa: E402
import cc_graph as G  # noqa: E402


def items(label):
    m = json.loads((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_text(encoding="utf-8"))
    by_arg = {arm["dataset_arg"]: (code, arm) for code, arm in m["arms"].items()}
    out = []
    for mf in sorted(glob.glob(str(ROOT / "runs" / "*" / "meta.json"))):
        meta = json.load(open(mf, encoding="utf-8"))
        if meta.get("stub_llm") or meta.get("label") != label:
            continue
        ds = meta.get("dataset") or ""
        if ds.startswith("/research/"):
            ds = "research:" + ds[len("/research/"):]
        if ds not in by_arg:
            continue
        code, arm = by_arg[ds]
        rd = Path(mf).parent
        bf, rf = sorted(rd.glob("artifacts/*_bootstrap.pkl")), sorted(rd.glob("artifacts/*_bootstrap_recommend.pkl"))
        if not bf or not rf:
            out.append({"key": rd.name, "missing": "bootstrap artifacts"})
            continue
        a = pickle.load(open(bf[0], "rb"))
        if a.get("error"):
            out.append({"key": rd.name, "missing": "bootstrap error %s" % a["error"]})
            continue
        S0 = np.asarray(a["args_before"]["kwargs"]["full_graph"])
        ref = np.load(ROOT / "datasets" / "suite_q1s2" / arm["reference_by_data"])
        out.append({"key": rd.name, "group": "live:s2:" + arm["role"], "family": arm["family"], "code": code, "S0": S0,
                    "boot": a["ret"][1], "buckets": pickle.load(open(rf[0], "rb"))["ret"], "E": G.truth_edges(ref), "p": S0.shape[0]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="s2")
    ap.add_argument("--replay-result", default=str(HERE / "results" / "refinement_v1" / "test_replay.json"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rule = json.loads(R.RULE.read_text())
    if rule["sha256"] != R.file_sha():
        sys.exit("refused: refinement_v1.py differs from the frozen rule")
    sys.path[:0] = [str(ROOT.parent / "Causal-Copilot"), str(ROOT.parent / "Causal-Copilot" / "externals" / "causal-learn")]
    with open(R.ACCESS, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z", "mode": "test",
                             "live_label": a.label, "driver": "analysis/refinement_v1_test_live.py", "rule_sha256": rule["sha256"]}) + "\n")
    its = items(a.label)
    missing = [i for i in its if "missing" in i]
    good = [i for i in its if "missing" not in i]
    rows, summary = R.evaluate(good)
    fam = {it["key"]: it["family"] for it in good}
    by_role = {}
    for g in sorted({r["group"] for r in rows}):
        _, by_role[g] = R.evaluate([it for it in good if it["group"] == g])
    per_fam = {}
    for r in rows:
        per_fam.setdefault(fam[r["key"]], []).append(r)
    fam_scores = {f: {s: round(float(np.mean([x["scores"][s]["adj_f1"] for x in rs])), 4) for s in ("S0", "S1", "v1")} for f, rs in per_fam.items()}
    fam_r1 = sum(v["v1"] >= v["S0"] - 0.02 for v in fam_scores.values())
    fam_r2 = sum(v["v1"] > v["S1"] for v in fam_scores.values())
    replay = json.loads(Path(a.replay_result).read_text(encoding="utf-8"))
    if replay.get("rule_sha256") != rule["sha256"] or replay.get("mode") != "test":
        sys.exit("refused: the part-1 result was not produced by the frozen rule in test mode")
    pooled = replay["rows"] + rows
    n = len(pooled)
    r1 = sum(r["scores"]["v1"]["adj_f1"] >= r["scores"]["S0"]["adj_f1"] - 0.02 for r in pooled)
    r2 = sum(r["scores"]["v1"]["adj_f1"] > r["scores"]["S1"]["adj_f1"] for r in pooled)
    r3 = float(np.mean([r["scores"]["v1"]["dir_f1_random"] - r["scores"]["S0"]["dir_f1_random"] for r in pooled]))
    v = lambda s: "SUPPORTED" if s >= 0.9 else ("REFUTED" if s < 0.7 else "INCONCLUSIVE")
    out = {"mode": "test", "tickets": ["BND-10", "TGT-09", "DLV-04"], "rule_sha256": rule["sha256"], "KEEP": R.KEEP, "ADD": R.ADD,
           "live": {"summary": summary, "by_role": by_role, "missing": missing,
                    "per_scenario": {"adj_f1_mean_of_arms": fam_scores, "R1_hits": fam_r1, "R2_hits": fam_r2, "scenarios": len(fam_scores)}},
           "pooled_test": {"files": n, "R1": {"hits": r1, "share": r1 / n, "verdict": v(r1 / n)},
                           "R2": {"hits": r2, "share": r2 / n, "verdict": v(r2 / n)},
                           "R3": {"mean_difference": r3, "verdict": "SUPPORTED" if r3 >= -0.01 else "REFUTED" if r3 <= -0.05 else "INCONCLUSIVE"},
                           "parts": {"replay": replay["summary"]["files"], "live": len(rows)}},
           "rows": rows}
    Path(a.out).write_text(json.dumps(out, indent=1, default=float) + "\n", encoding="utf-8")
    print(json.dumps({"live": {k: (x.get("verdict") if isinstance(x, dict) and "verdict" in x else x) for k, x in summary.items()},
                      "by_role": {g: {k: s[k].get("verdict") for k in ("R1", "R2", "R3")} for g, s in by_role.items()},
                      "per_scenario": out["live"]["per_scenario"], "pooled": out["pooled_test"], "missing": missing}, indent=1, default=float))


if __name__ == "__main__":
    main()
