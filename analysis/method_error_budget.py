"""BND-04: error budget per method on CausalArena's public semantic files, the published-row comparison, and Q4a/Q4b.

  python analysis/method_error_budget.py --rows analysis/results/methods/gesbic_semantic_obs.json --published GIES \
      --out analysis/results/methods/error_budget_gesbic.json

Budget (as for PC in error_budget.py), from each file's committed arrows and undecided pairs:
  skeleton precision / recall / F1 (an undecided pair counts as an adjacency)
  of the true adjacencies found: committed right, committed reversed, left undecided
  accuracy of committed directions = right / (right + reversed)                                  -> Q4a
  F1 with perfect orientation of the method's own skeleton (= skeleton F1)
  F1 as scored (undecided pairs: random orientation, per-file seed) and under the authors' rule ("lower")
  cost of direction errors = skeleton F1 - F1 as scored (random rule, order-free)                 -> Q4b
Means are replicate-averaged per scenario, then averaged over scenarios (CausalArena section 4.5); scm_std is across scenarios.
Published comparison: the method's row in CausalArena's main leaderboard (semantic obs-only) and its per-domain breakdown,
with tolerance 3 SE of a 50-of-100 scenario mean (finite-population correction), as in pc_calibration.json.
Gate C1: pc_calibration.json still reports the published PC F1 reproduced under the official configuration.
Predictions are read verbatim from plans/q1_dag.json (fixed before the runs); thresholds are parsed from that text.

--family (BND-06, default semantic): which public obs-only family the rows come from. It selects the truth files, the
published leaderboard column ("Semantic obs-only", "Formula obs-only", "Synthetic obs-only"), the per-domain / per-graph-family
breakdown table, the size of the published population for the finite-population correction (100 scenarios for semantic and
formula, 1000 for synthetic) and the expected file count (250, 250, 100). With the default the output is unchanged from
BND-04. For a non-default family the Q4a/Q4b verdicts are computed with the same thresholds but labelled as not
pre-registered for that family (the BND-04 predictions were fixed for semantic only).
  python analysis/method_error_budget.py --family formula --rows analysis/results/methods/pc_formula_obs_rel.json --published PC \
      --out analysis/results/methods/error_budget_pc_formula.json
"""
import argparse
import csv
import json
import math
import re
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "external" / "causalarena" / "results" / "tables"
FAMILY = {
    "semantic": {"column": "Semantic obs-only", "dir": "semantic/data/semantic_obs_only", "n_pub": 100, "files": 250,
                 "breakdown": ("semantic_domain_f1_representative.csv", "semantic_obs_only")},
    "formula": {"column": "Formula obs-only", "dir": "formula/data/formula_obs_only", "n_pub": 100, "files": 250,
                "breakdown": ("formula_domain_f1_representative.csv", "formula_obs_only")},
    "synthetic": {"column": "Synthetic obs-only", "dir": "synthetic/data/synthetic_obs_only", "n_pub": 1000, "files": 100,
                  "breakdown": ("synthetic_family_f1_representative.csv", "obs_only")},
}


def parse_cell(c):
    m = re.match(r"\s*([\d.]+)\s*\(([\d.]+)\)", c)
    return (float(m.group(1)), float(m.group(2))) if m else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--published", default="", help="method name in the leaderboard, e.g. GIES (FCI has no row)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--family", default="semantic", choices=sorted(FAMILY))
    ap.add_argument("--exclude-failed", action="store_true",
                    help="drop every scenario in which any file failed (failed rows are otherwise scored as empty graphs, as the authors' runners do)")
    a = ap.parse_args()
    F = FAMILY[a.family]
    data = json.loads(Path(a.rows).read_text(encoding="utf-8"))
    rows = data["rows"]
    failed_scen = sorted({r["scenario"] for r in rows if r.get("failed")})
    if a.exclude_failed:
        rows = [r for r in rows if r["scenario"] not in failed_scen]
    per = {}
    for r in rows:
        dire = {tuple(e) for e in r["directed_edges"]}
        und = {frozenset(p[:2]) for p in r["undecided_pairs"]}
        per.setdefault(r["scenario"], []).append((r, dire, und))
    # truth from the released files
    import causalarena_io as CA  # noqa: E402
    from causalarena_load import load_any  # noqa: E402
    load = CA.load if a.family == "semantic" else load_any
    root = ROOT / "external" / "causalarena" / "scm" / F["dir"]
    stats = {}
    tot = {"found": 0, "right": 0, "wrong": 0, "undec": 0}
    for scen, lst in per.items():
        acc = []
        for r, dire, und in lst:
            E = CA.true_edges(load(root / r["file"])["g"])
            tadj = {frozenset(e) for e in E}
            padj = {frozenset(e) for e in dire} | und
            tp = len(padj & tadj)
            P = tp / len(padj) if padj else 0.0
            R = tp / len(tadj)
            right = sum(1 for e in dire if e in E)
            wrong = sum(1 for e in dire if (e[1], e[0]) in E)
            undec = len(und & tadj)
            tot["found"] += tp; tot["right"] += right; tot["wrong"] += wrong; tot["undec"] += undec
            skf1 = 2 * P * R / (P + R) if P + R else 0.0
            acc.append({"skel_precision": P, "skel_recall": R, "skel_f1": skf1,
                        "f1_random": r["scores"]["random"]["f1"], "f1_lower": r["scores"]["lower"]["f1"],
                        "shd_random": r["scores"]["random"]["shd"], "shd_lower": r["scores"]["lower"]["shd"],
                        "dir_acc": right / (right + wrong) if right + wrong else None,
                        "seconds": r["metrics"].get("seconds")})
        stats[scen] = {"domain": lst[0][0]["domain"], "split": lst[0][0].get("split"), "replicates": len(acc),
                       **{k: st.mean(x[k] for x in acc if x[k] is not None) for k in acc[0] if k != "dir_acc"},
                       "dir_acc": st.mean([x["dir_acc"] for x in acc if x["dir_acc"] is not None]) if any(x["dir_acc"] is not None for x in acc) else None}
    keys = ["skel_precision", "skel_recall", "skel_f1", "f1_random", "f1_lower", "shd_random", "shd_lower", "seconds"]
    fam = {k: round(st.mean(s[k] for s in stats.values()), 4) for k in keys}
    fam_std = {k: round(st.pstdev(s[k] for s in stats.values()), 4) for k in keys}
    acc_committed = tot["right"] / (tot["right"] + tot["wrong"]) if tot["right"] + tot["wrong"] else None
    cost = round(fam["skel_f1"] - fam["f1_random"], 4)
    # published
    pub = {}
    for metric, fn in (("f1", "main_leaderboard_f1_wide_with_std.csv"), ("shd", "main_leaderboard_shd_wide_with_std.csv")):
        for row in csv.DictReader(open(T / "main" / fn, encoding="utf-8-sig")):
            if (row.get("method") or row.get("Method")) == a.published:
                pub[metric] = parse_cell(row[F["column"]])
    pub = {k: v for k, v in pub.items() if v[0] is not None}     # "--" cells (no published value): nothing to compare
    n_pub, n_ours = F["n_pub"], len(stats)
    fpc = math.sqrt((n_pub - n_ours) / (n_pub - 1))
    tol = {m: round(3 * pub[m][1] / math.sqrt(n_ours) * fpc, 4) for m in pub}
    comp = {}
    for rule in (("random", "lower") if pub else ()):     # no published row (e.g. FCI): nothing to compare
        comp[rule] = {"f1": fam["f1_" + rule], "f1_gap": round(fam["f1_" + rule] - pub["f1"][0], 4),
                      "f1_within": abs(fam["f1_" + rule] - pub["f1"][0]) <= tol["f1"],
                      "shd": fam["shd_" + rule], "shd_gap": round(fam["shd_" + rule] - pub["shd"][0], 4),
                      "shd_within": abs(fam["shd_" + rule] - pub["shd"][0]) <= tol["shd"]}
    dom_pub = {}
    for row in csv.DictReader(open(T / "breakdown" / F["breakdown"][0], encoding="utf-8-sig")):
        if row["split"] == F["breakdown"][1] and row["paper_method"] == a.published:
            dom_pub[row["graph_family"]] = float(row["F1_mean"])
    by_dom = {}
    for s in stats.values():
        by_dom.setdefault(s["domain"], []).append(s)
    domains = {dname: {"scenarios_public": len(v), "f1_random": round(st.mean(x["f1_random"] for x in v), 4),
                       "f1_lower": round(st.mean(x["f1_lower"] for x in v), 4), "published_10_scenarios": dom_pub.get(dname)}
               for dname, v in sorted(by_dom.items())}
    # predictions, verbatim from the plan
    plan = json.loads((ROOT / "plans" / "q1_dag.json").read_text(encoding="utf-8"))
    preds = [p for b in plan["bundles"] if b["id"] == "BND-04" for p in b["predictions"]]
    q4a_txt = next(p for p in preds if p.startswith("Q4a"))
    q4b_txt = next(p for p in preds if p.startswith("Q4b"))
    a_sup, a_ref = [float(x) for x in re.findall(r"(?:<=|>=)\s*([\d.]+)", q4a_txt)[:2]]
    b_sup, b_ref = [float(x) for x in re.findall(r"(?:<=|>=)\s*([\d.]+)", q4b_txt)[:2]]
    q4a = None if acc_committed is None else ("supported" if acc_committed <= a_sup else "refuted" if acc_committed >= a_ref else "inconclusive")
    q4b = ("supported" if cost >= b_sup else "refuted" if cost <= b_ref else "inconclusive")
    cal = json.loads((ROOT / "analysis" / "results" / "causalarena_calibration" / "pc_calibration.json").read_text(encoding="utf-8"))
    out = {"rows_file": a.rows, "method": rows[0]["method"], "failed_files": sum(1 for r in data["rows"] if r.get("failed")),
           "scenarios_with_failures": failed_scen, "excluded_failed_scenarios": a.exclude_failed, "published_method": a.published, "files": len(rows), "scenarios": n_ours,
           "family_means": fam, "family_scm_std": fam_std,
           "of_true_adjacencies_found": {k: round(tot[k] / tot["found"], 4) for k in ("right", "wrong", "undec")},
           "accuracy_of_committed_directions": round(acc_committed, 4) if acc_committed is not None else None,
           "cost_of_direction_errors_f1": cost,
           "published": {"f1": pub.get("f1"), "shd": pub.get("shd"), "scenarios": n_pub} if pub else None, "tolerance_3se": tol, "vs_published": comp,
           "by_domain": domains,
           "predictions": {"Q4a": {"text": q4a_txt, "measured": round(acc_committed, 4) if acc_committed is not None else None, "verdict": q4a},
                           "Q4b": {"text": q4b_txt, "measured": cost, "verdict": q4b}},
           "gates": {"C1_pc_scorer_reproduces_published_F1": bool(cal.get("gate_C1_official_configuration_reproduces_published_F1")),
                     "split_labelled": all(r.get("split") for r in rows), "files_250": len(rows) == 250 or a.exclude_failed},
           "per_scenario": stats}
    if a.family != "semantic":
        out["family"] = a.family
        out["published_column"] = F["column"]
        out["predictions_note"] = ("Q4a/Q4b were pre-registered (plans/q1_dag.json, BND-04) for the semantic family only; for %s the same "
                                   "thresholds are applied descriptively (not pre-registered)" % a.family)
        out["gates"].pop("files_250")
        out["gates"]["files_all_public"] = len(rows) == F["files"] or a.exclude_failed
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    show = {k: v for k, v in out.items() if k not in ("per_scenario", "by_domain")}
    print(json.dumps(show, indent=1))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
