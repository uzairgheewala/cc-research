"""AB-01 (AUD-33): the controlled scoreboard for CausalArena, complete. Extends rescore_controls.py (AUD-28, unchanged; its
coordinate functions are imported) to the synthetic family, the D+I regime (GIES with the released targets), and the PC
collider-rule variants, and writes the corrected leaderboard.

  python analysis/rescore_controls_v2.py --root external/causalarena --out analysis/results/rescore_v2

For every method x family: files paired across the released and shuffled arms (failed or timed-out files dropped from
both), S, c, q, a, directed F1 under the expectation rule (undecided pairs at random, per-file seed) and under the
authors' rule ("lower": earlier column -> later column, which reads the released order).
Layout channels, per method and family:
  authors' rule gain   F1_lower(released) - F1_random(shuffled)       what the authors' rule adds by reading the order
  conflict-rule gain   F1_random(released) - F1_random(shuffled)      what the method's own order dependence adds
                       (for PC it is the collider conflict rule; for an order-free method it is ~0)
  engine-copy gain     PC Causal-Copilot copy minus PC upstream, released arm, expectation rule
Predictions (written in plans/audit_dag.json before these runs):
  P1 GIES with targets: |shuffled - released| < 0.01 under the expectation rule, 0.01-0.04 authors'-rule gain (refuted: > 0.05)
  P2 PC with maxP: released and shuffled within 0.01 in all three families (refuted: > 0.03 in any)
Writes analysis/results/rescore_v2/: rescore_v2.json, leaderboard_controlled.json (+ .md table), CONTRACT.json. No model calls.
Tickets: AUD-33, BEN-07, REP-07, EXT-01
"""
import argparse, json, os, statistics as st, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
from causalarena_load import load_any  # noqa: E402
from rescore_controls import coords, mean, rows  # noqa: E402

FAMS = ("semantic", "formula", "synthetic")
PAIRS = {
    "PC (Causal-Copilot copy)": {"semantic": ("pc_semantic_obs_rel", "pc_semantic_obs_shuf"), "formula": ("pc_formula_obs_rel", "pc_formula_obs_shuf"),
                                 "synthetic": ("pc_synthetic100_rel", "pc_synthetic100_shuf")},
    "PC (upstream, default rule)": {f: ("pc_upstream_%s_obs_rel" % f, "pc_upstream_%s_obs_shuf" % f) for f in FAMS},
    "PC (upstream, maxP)": {f: ("pc_upstream_maxp_%s_obs_rel" % f, "pc_upstream_maxp_%s_obs_shuf" % f) for f in FAMS},
    "PC (upstream, definite maxP)": {f: ("pc_upstream_dmaxp_%s_obs_rel" % f, "pc_upstream_dmaxp_%s_obs_shuf" % f) for f in FAMS},
    "GES (BIC)": {"semantic": ("gesbic_semantic_obs", "gesbic_semantic_obs_shuf"), "formula": ("gesbic_formula_obs_rel", "gesbic_formula_obs_shuf"),
                  "synthetic": ("gesbic_synthetic100_rel", "gesbic_synthetic100_shuf")},
    "GIES with targets (D+I)": {f: ("gies_targets_%s_obsint_rel" % f, "gies_targets_%s_obsint_shuf" % f) for f in ("semantic", "formula")},
    "FCI": {"semantic": ("fci_semantic_obs", "fci_semantic_obs_shuf"), "formula": ("fci_formula_obs_rel", "fci_formula_obs_shuf"),
            "synthetic": ("fci_synthetic100_rel", "fci_synthetic100_shuf")},
    "DirectLiNGAM": {"semantic": ("lingam_semantic_obs_rel", "lingam_semantic_obs_shuf"), "formula": ("lingam_formula_obs_rel", "lingam_formula_obs_shuf"),
                     "synthetic": ("lingam_synthetic100_rel", "lingam_synthetic100_shuf")},
    "NOTEARS": {"semantic": ("notears_semantic_obs_rel", "notears_semantic_obs_shuf"), "formula": ("notears_formula_obs_rel", "notears_formula_obs_shuf"),
                "synthetic": ("notears_synthetic100_rel", "notears_synthetic100_shuf")},
}
PUBLISHED = {"PC (Causal-Copilot copy)": ("PC", "D"), "PC (upstream, default rule)": ("PC", "D"), "GES (BIC)": ("GIES", "D"),
             "GIES with targets (D+I)": ("GIES", "D+I"), "DirectLiNGAM": ("LiNGAM", "D"), "NOTEARS": ("NOTEARS", "D")}

_truth = {}


def truth(root, fam, file):
    f = file.replace("_obs_int__", "_obs_only__")
    if (fam, f) not in _truth:
        _truth[(fam, f)] = CA.true_edges(load_any(Path(root) / "scm" / fam / "data" / ("%s_obs_only" % fam) / f)["g"])
    return _truth[(fam, f)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--out", default=str(HERE / "results" / "rescore_v2"))
    a = ap.parse_args()
    pub = json.load(open(HERE / "results" / "published" / "leaderboard.json"))
    out = {"tickets": ["AUD-33", "BEN-07", "REP-07", "EXT-01"], "methods": {}, "predictions": {}}
    for label, fams in PAIRS.items():
        for fam, (rel, shuf) in fams.items():
            R, S = rows(rel), rows(shuf)
            if R is None or S is None:
                continue
            common = sorted(set(R) & set(S))
            cr = [coords(R[f], truth(a.root, fam, f)) for f in common]
            cs = [coords(S[f], truth(a.root, fam, f)) for f in common]
            summ = {arm: {k: mean([x[k] for x in xs]) for k in ("S", "c", "q", "a", "F1_random", "F1_lower")} for arm, xs in (("released", cr), ("shuffled", cs))}
            d_rand = [y["F1_random"] - x["F1_random"] for x, y in zip(cr, cs)]
            rec = {"files_paired": len(common), "files_released_ok": len(R), "files_shuffled_ok": len(S), "sources": [rel, shuf], **summ,
                   "authors_rule_gain": round(summ["released"]["F1_lower"] - summ["shuffled"]["F1_random"], 4),
                   "conflict_rule_gain": round(summ["released"]["F1_random"] - summ["shuffled"]["F1_random"], 4),
                   "shuffled_minus_released_expectation": round(st.mean(d_rand), 4),
                   "files_better_shuffled": sum(d > 0 for d in d_rand), "files_worse_shuffled": sum(d < 0 for d in d_rand)}
            if label in PUBLISHED:
                pn, reg = PUBLISHED[label]
                rec["published"] = pub["table"].get(fam, {}).get(reg, {}).get(pn, {}).get("f1")
                rec["published_regime"] = reg
            out["methods"].setdefault(label, {})[fam] = rec
            print("%-30s %-9s n=%3d  q %s/%s  F1 rel(lower %.3f, rand %.3f) shuf %.3f  pub %s" % (
                label, fam, len(common), summ["released"]["q"], summ["shuffled"]["q"], summ["released"]["F1_lower"],
                summ["released"]["F1_random"], summ["shuffled"]["F1_random"], rec.get("published")), flush=True)
    M = out["methods"]
    for fam in FAMS:
        cp, up = M.get("PC (Causal-Copilot copy)", {}).get(fam), M.get("PC (upstream, default rule)", {}).get(fam)
        if cp and up:
            out.setdefault("engine_copy_gain", {})[fam] = round(cp["released"]["F1_random"] - up["released"]["F1_random"], 4)
    g = M.get("GIES with targets (D+I)", {})
    if g:
        worst = max(abs(v["shuffled_minus_released_expectation"]) for v in g.values())
        out["predictions"]["P1"] = {"values": {f: {"expectation": v["shuffled_minus_released_expectation"], "authors_rule_gain": v["authors_rule_gain"]} for f, v in g.items()},
                                    "verdict": "refuted" if worst > 0.05 else ("supported" if worst < 0.01 else "partly (expectation gap 0.01-0.05)")}
    mp = M.get("PC (upstream, maxP)", {})
    if mp:
        gaps = {f: v["shuffled_minus_released_expectation"] for f, v in mp.items()}
        worst = max(abs(x) for x in gaps.values())
        out["predictions"]["P2"] = {"values": gaps, "families": sorted(gaps), "verdict": "refuted" if worst > 0.03 else ("supported" if worst <= 0.01 else "partly (0.01-0.03)"),
                                    "complete": len(gaps) == 3}
    # corrected leaderboard: published vs our released (authors' rule), released (expectation), shuffled (expectation)
    board = []
    for label, fams in M.items():
        for fam, v in fams.items():
            board.append({"method": label, "family": fam, "regime": v.get("published_regime", "D"), "published": v.get("published"),
                          "ours_released_authors_rule": v["released"]["F1_lower"], "ours_released_expectation": v["released"]["F1_random"],
                          "ours_shuffled_expectation": v["shuffled"]["F1_random"], "files": v["files_paired"]})
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "rescore_v2.json"), "w"), indent=1)
    json.dump({"table": board, "note": "controlled number = ours_shuffled_expectation (columns shuffled, undecided pairs at random)"},
              open(os.path.join(a.out, "leaderboard_controlled.json"), "w"), indent=1)
    lines = ["| Family | Method | Regime | Published | Ours, released, authors' rule | Ours, released, expectation | **Ours, shuffled, expectation (controlled)** | Files |",
             "|---|---|---|---|---|---|---|---|"]
    for r in sorted(board, key=lambda r: (FAMS.index(r["family"]), -(r["ours_shuffled_expectation"] or 0))):
        lines.append("| %s | %s | %s | %s | %.3f | %.3f | **%.3f** | %d |" % (r["family"], r["method"], r["regime"], "%.3f" % r["published"] if r["published"] is not None else "-",
                                                                 r["ours_released_authors_rule"], r["ours_released_expectation"], r["ours_shuffled_expectation"], r["files"]))
    open(os.path.join(a.out, "leaderboard_controlled.md"), "w").write("\n".join(lines) + "\n")
    json.dump({"producer": "analysis/rescore_controls_v2.py", "score_bearing": True, "tickets": out["tickets"], "regime": "per-row",
               "regime_detail": "D for observational methods; D+I for GIES with targets", "split": "all-public (measurement, no tuning)",
               "controls": {"columns_shuffled": "both arms reported", "names": "not applicable", "supplier": "causalarena"},
               "orientation_rule": "both reported: lower (authors') and random (expectation)",
               "metric_defs": {'S': 'skeleton F1', 'c': 'commit rate', 'q': 'commit accuracy', 'a': 'c q + (1 - c)/2', 'F1_random': 'directed F1, undecided at random (per-file seed)', 'F1_lower': "directed F1, authors' rule (earlier column -> later column)", 'authors_rule_gain': 'F1_lower(released) - F1_random(shuffled): published-style number minus the controlled one', 'conflict_rule_gain': 'F1_random(released) - F1_random(shuffled)'}},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)
    print(json.dumps(out["predictions"], indent=1), out.get("engine_copy_gain"))


if __name__ == "__main__":
    main()
