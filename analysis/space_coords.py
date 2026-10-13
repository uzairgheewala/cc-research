"""Coordinates of each system in the scoreboard's direction space: (S, c, q).

Definitions (one estimate M against the true DAG, p variables):
  S  skeleton F1: F1 over unordered adjacencies.
  c  commit rate: of the true adjacencies found, the share given a direction (right or wrong).
  q  commit accuracy: of those committed directions, the share that is right.
  a  effective direction accuracy under the scoreboard's forced-choice rule (undecided pairs oriented
     at random): a = c*q + (1-c)/2.
Identity: if every predicted adjacency yields exactly one directed prediction (forced choice), then
  directed precision = a*TP/(TP+FP) and directed recall = a*TP/(TP+FN), so F1_dir = a * S exactly
  (in expectation over the random orientation).

Inputs: Causal-Copilot runs (stages S0, S1, S2, S3 rebuilt exactly as partial_stages.py does; gate Q1 there
checks the rebuild) and the method error budgets in results/methods (which already report S and the
right / wrong / undecided split). Nothing here calls a model.

  python space_coords.py --runs-dir RUNS --label s2 --mapping datasets/suite_q1s2/MAPPING.json --repo CC --out DIR
"""
import argparse
import glob
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cc_graph as G  # noqa: E402
from lineage import step_bootstrap, step_kci, step_llm  # noqa: E402
from partial_stages import load_artifacts  # noqa: E402
from stability import arm_of, family_role  # noqa: E402

HERE = Path(__file__).resolve().parent


def coords(s):
    tp = s["adj_tp"]
    cor, rev, und = s["true_edges_correctly_directed"], s["true_edges_reversed"], s["true_edges_present_but_not_directed"]
    if not tp:
        return {"S": s["adj_f1"] or 0.0, "c": None, "q": None, "a": None, "F1_forced": 0.0, "F1_strict": s["dir_f1"]}
    c = (cor + rev) / tp
    q = cor / (cor + rev) if cor + rev else None
    a = (cor + und / 2) / tp
    return {"S": s["adj_f1"], "c": c, "q": q, "a": a, "F1_forced": a * (s["adj_f1"] or 0.0), "F1_strict": s["dir_f1"],
            "tp": tp, "fp": s["adj_fp"], "fn": s["adj_fn"], "correct": cor, "reversed": rev, "undecided": und}


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(float(np.mean(xs)), 4) if xs else None


def methods():
    out = {}
    for f in sorted(glob.glob(str(HERE / "results" / "methods" / "error_budget_*.json"))):
        d = json.load(open(f))
        m, t = d.get("family_means") or {}, d.get("of_true_adjacencies_found") or {}
        if not m or not t:
            continue
        right, wrong, und = t.get("right", 0.0), t.get("wrong", 0.0), t.get("undec", 0.0)
        c = right + wrong
        out[Path(f).stem.replace("error_budget_", "")] = {
            "scenarios": d.get("scenarios"), "failed_files": d.get("failed_files"),
            "excluded_failed": d.get("excluded_failed_scenarios"),
            "S": m["skel_f1"], "c": round(c, 4), "q": round(right / c, 4) if c else None,
            "a": round(right + und / 2, 4), "F1_forced_reported": m["f1_random"],
            "aS": round((right + und / 2) * m["skel_f1"], 4)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.path[:0] = [a.repo, os.path.join(a.repo, "externals", "causal-learn")]
    mapping = json.load(open(a.mapping, encoding="utf-8"))
    mdir = Path(a.mapping).resolve().parent
    rows = []
    for meta_f in sorted(Path(a.runs_dir).glob("*/meta.json")):
        meta = json.load(open(meta_f, encoding="utf-8"))
        if meta.get("label") != a.label or meta.get("stub_llm"):
            continue
        arm, spec = arm_of(meta, mapping)
        fam, role = family_role(arm, spec)
        arts = load_artifacts(str(meta_f.parent))
        need = ("quality_judge", "bootstrap_recommend", "llm_evaluation_new", "kci_pruning")
        if not all(k in arts for k in need) or arts["kci_pruning"][0].get("ret") is None:
            continue
        S0 = np.asarray(arts["quality_judge"][0]["args_before"]["kwargs"]["full_graph"]).copy()
        S1, _, _ = step_bootstrap(S0, arts["bootstrap_recommend"][0]["ret"])
        direct, forbid = arts["llm_evaluation_new"][0]["ret"]
        S2 = step_llm(S1, direct, forbid)
        S3 = step_kci(S2, arts["kci_pruning"][0]["ret"])
        E = G.truth_edges(np.load(mdir / spec["reference_by_data"]))
        p = S0.shape[0]
        row = {"run_id": meta["run_id"], "arm": arm, "family": fam, "role": role}
        for name, M in (("S0", S0), ("S1", S1), ("S2", S2), ("S3", S3)):
            row[name] = coords(G.score(M, E, p))
        rows.append(row)
    by_role = {}
    for role in ("real", "neutral", "swapped"):
        rr = [r for r in rows if r["role"] == role]
        by_role[role] = {"runs": len(rr)}
        for st in ("S0", "S1", "S2", "S3"):
            by_role[role][st] = {k: mean([r[st][k] for r in rr]) for k in ("S", "c", "q", "a", "F1_forced", "F1_strict")}
    meth = methods()
    dev = {k: round(abs(v["aS"] - v["F1_forced_reported"]), 4) for k, v in meth.items()}
    gates = {
        # The identity is exact per scenario; over a family, mean(a*S) differs from mean(a)*mean(S) by their covariance,
        # so the check is on the families used on the site (semantic, formula) and the rest are reported.
        "C1_identity_semantic_formula_within_0.02": all(d <= 0.02 for k, d in dev.items() if "synthetic" not in k),
        "C1_deviation_by_budget": dev,
        "C2_all_runs_scored": len(rows) == 30,
        "C3_strict_matches_partial_stages": None,
    }
    ps = HERE / "results" / "stability_s2" / "partial_stages.json"
    if ps.exists():
        P = json.load(open(ps))["by_role"]
        gates["C3_strict_matches_partial_stages"] = all(
            abs(by_role[r]["S3"]["F1_strict"] - P[r]["S3_dir_all"]) <= 0.002 and abs(by_role[r]["S3"]["S"] - P[r]["S3_adj_all"]) <= 0.002
            for r in by_role)
    os.makedirs(a.out, exist_ok=True)
    json.dump({"definitions": __doc__.split("Inputs:")[0].strip(), "gates": gates, "methods": meth,
               "causal_copilot_by_role": by_role, "rows": rows}, open(os.path.join(a.out, "space_coords.json"), "w"), indent=1)
    print(json.dumps({"gates": gates, "by_role": by_role}, indent=1))


if __name__ == "__main__":
    main()
