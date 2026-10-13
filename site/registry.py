"""Every number the site shows, with the file it comes from.

Each entry is one of
  J(path, *ptr)          the value at that JSON pointer
  F(path, fn)            fn(parsed JSON) -> value (for lists or derived values; keep fn trivial)
  L(path, value)         a literal that must appear verbatim in the cited text file (checked at snapshot time)
tracker/snapshot.py evaluates all of them, records value + source path + source sha256, and fails if any cannot be
read. site/build.py may only print numbers through this registry (or counts computed from the snapshot's items).
"""
R = "analysis/results/"
EB = R + "error_budget/error_budget.json"
OV = R + "error_budget/order_value.json"
OB = R + "causalarena_calibration/order_baseline.json"
PUB = R + "published/leaderboard.json"
SC = R + "space/space_coords.json"
PS = R + "stability_s2/partial_stages.json"
B8 = R + "stability_s2/bnd08_summary.json"
V1 = R + "refinement_v1/test_live_s2.json"
V1D = R + "refinement_v1/diagnosis_test_live_s2.json"
V2 = R + "refinement_v2/exploratory_s2_live.json"
D9 = R + "dom09/ida_timing.json"
IA = R + "intervention_audit/intervention_audit.json"
CH = R + "chambers/sample/sample_status.json"
REP11 = "analysis/reports/rep11_sachs_data.md"
B8R = "analysis/reports/bnd08_s2_results.md"


def J(path, *ptr):
    return {"src": path, "ptr": list(ptr)}


def F(path, fn):
    return {"src": path, "fn": fn}


def L(path, value, context=None):
    """value must appear in the file; with context, inside that exact phrase."""
    return {"src": path, "literal": value, "context": context}


def _ov(label, col):
    return lambda d: next(r for r in d if r["order knowledge"] == label)[col]


REG = {
    # ---- limits (Level 2 derivation)
    "lim.sem.D": J(EB, "families", "semantic", "ceiling_obs_mean"),
    "lim.sem.D.min": J(EB, "families", "semantic", "ceiling_obs_min"),
    "lim.sem.DI": J(EB, "families", "semantic", "ceiling_int_mean"),
    "lim.for.D": J(EB, "families", "formula", "ceiling_obs_mean"),
    "lim.for.DI": J(EB, "families", "formula", "ceiling_int_mean"),
    "kappa.sem.D": J(EB, "families", "semantic", "share_compelled_obs"),
    "kappa.sem.DI": J(EB, "families", "semantic", "share_compelled_int"),
    "kappa.for.D": J(EB, "families", "formula", "share_compelled_obs"),
    "kappa.for.DI": J(EB, "families", "formula", "share_compelled_int"),
    # ---- published (CausalArena main leaderboard, all 100 scenarios per family)
    "pub.sem.D.best": J(PUB, "best", "semantic", "D", "f1"),
    "pub.sem.D.best.method": J(PUB, "best", "semantic", "D", "method"),
    "pub.sem.D.GIES": J(PUB, "table", "semantic", "D", "GIES", "f1"),
    "pub.sem.D.PC": J(PUB, "table", "semantic", "D", "PC", "f1"),
    "pub.sem.D.LiNGAM": J(PUB, "table", "semantic", "D", "LiNGAM", "f1"),
    "pub.sem.D.NOTEARS": J(PUB, "table", "semantic", "D", "NOTEARS", "f1"),
    "pub.sem.D.RandomRegress": J(PUB, "table", "semantic", "D", "RandomRegress", "f1"),
    "pub.sem.DI.best": J(PUB, "best", "semantic", "D+I", "f1"),
    "pub.sem.DI.best.method": J(PUB, "best", "semantic", "D+I", "method"),
    "pub.sem.DI.TabCausal": J(PUB, "table", "semantic", "D+I", "TabCausal", "f1"),
    "pub.for.D.best": J(PUB, "best", "formula", "D", "f1"),
    # ---- PC error budget (semantic, n = 1,000)
    "pc.P": J(EB, "pc_semantic_n1000", "skeleton_precision"),
    "pc.R": J(EB, "pc_semantic_n1000", "skeleton_recall"),
    "pc.S": J(EB, "pc_semantic_n1000", "pc_skeleton_with_perfect_orientation_f1"),
    "pc.F1": J(EB, "pc_semantic_n1000", "pc_as_scored_f1"),
    "pc.q": J(EB, "pc_semantic_n1000", "accuracy_of_committed_directions"),
    # ---- oracles and the layout leak
    "oracle.depth.reg": F(OV, _ov("full depth", "regression on earlier tiers, F1")),
    "oracle.inputs.pc": F(OV, _ov("inputs vs rest", "PC skeleton re-oriented, F1")),
    "pc.order.changed": J(R + "methods/pc_skeleton_order_vendored.json", "files_with_different_skeleton"),
    "pc.order.files": J(R + "methods/pc_skeleton_order_vendored.json", "scored"),
    "pc.order.changed.upstream": J(R + "methods/pc_skeleton_order_upstream.json", "files_with_different_skeleton"),
    "leak.released": J(OB, "families", "semantic", "as_released", "f1"),
    "leak.shuffled": J(OB, "families", "semantic", "columns_shuffled", "f1"),
    # ---- methods in (S, c, q, a) coordinates; GES and FCI on the scenarios where they run
    **{"m.%s.%s" % (name, k): J(SC, "methods", key, k)
       for name, key in (("PC", "pc_semantic"), ("GES", "gesbic_excl_failed"), ("FCI", "fci_excl_failed"),
                         ("LiNGAM", "lingam_semantic"), ("NOTEARS", "notears_semantic"))
       for k in ("S", "c", "q", "a", "aS", "F1_forced_reported", "scenarios")},
    # ---- Causal-Copilot on the 10 S2 test scenarios, by name arm and stage
    **{"cc.%s.%s.%s" % (role, st, k): J(SC, "causal_copilot_by_role", role, st, k)
       for role in ("real", "neutral", "swapped") for st in ("S0", "S1", "S2", "S3")
       for k in ("S", "c", "q", "a", "F1_forced", "F1_strict")},
    "cc.runs": J(PS, "runs"),
    "cc.crashed": J(PS, "cycle_step", "runs_cyclic_by_pipeline_test"),
    "cc.crashed.real": J(PS, "cycle_step", "by_role", "real"),
    "cc.M1.hits": J(B8, "M1", "hits"), "cc.M1.files": J(B8, "M1", "files"), "cc.M1.verdict": J(B8, "M1", "verdict"),
    "cc.M2.hits": J(B8, "M2", "hits"), "cc.M2.n": J(B8, "M2", "families"), "cc.M2.verdict": J(B8, "M2", "verdict"),
    "cc.M3.hits": J(B8, "M3", "labels_only"), "cc.M3.n": J(B8, "M3", "n"), "cc.M3.verdict": J(B8, "M3", "verdict"),
    "cc.M4.hits": J(B8, "M4", "hits"), "cc.M4.n": J(B8, "M4", "families"), "cc.M4.verdict": J(B8, "M4", "verdict"),
    "cc.cost.usd": L(B8R, "12.7", "about $12.7"),
    "cc.fci.runs": L(B8R, "29", "FCI in 29"),
    "cc.runs.S1_below_S0": F(SC, lambda d: sum(r["S1"]["S"] < r["S0"]["S"] for r in d["rows"])),
    "cc.runs.real.S2_up": F(SC, lambda d: sum(r["S2"]["S"] > r["S1"]["S"] for r in d["rows"] if r["role"] == "real")),
    "cc.runs.neutral.S2_same": F(SC, lambda d: sum(r["S2"] == r["S1"] for r in d["rows"] if r["role"] == "neutral")),
    "cc.runs.final_below_S0": F(SC, lambda d: sum(r["S3"]["F1_forced"] < r["S0"]["F1_forced"] for r in d["rows"])),
    "cc.runs.per_role": F(SC, lambda d: d["causal_copilot_by_role"]["real"]["runs"]),
    # ---- refinement v1 / v2
    "v1.R1.hits": J(V1, "pooled_test", "R1", "hits"), "v1.R2.hits": J(V1, "pooled_test", "R2", "hits"),
    "v1.files": J(V1, "pooled_test", "files"),
    "v1.dropped.true": J(V1D, "totals", "dropped_true"),
    "v1.dropped.all": F(V1D, lambda d: d["totals"]["dropped_true"] + d["totals"]["dropped_false"]),
    "v2.R1.hits": J(V2, "summary", "R1", "hits"), "v2.files": J(V2, "summary", "files"),
    # ---- decisions pillar inputs
    "ida.vars": J(D9, "variables"), "ida.pairs": J(D9, "ordered_pairs"), "ida.seconds": J(D9, "seconds_all_pairs"),
    "ida.identified": J(D9, "share_identified_in_class"), "ida.parents.ok": J(D9, "X_whose_true_parents_are_a_candidate_set"),
    "int.none": J(IA, "families", "semantic", "in_name_only"),
    "int.total": J(IA, "families", "semantic", "declared_target_instances"),
    "chambers.regimes": J(CH, "regimes"),
    "rep11.ours": L(REP11, "0.647"), "rep11.paper": L(REP11, "0.606"),
}

# ---- Atlas v2 (2026-10-13): Act II and market pages. Report figures are literals checked against the cited text.
AB01R = "analysis/reports/ab01_controlled_scoreboard.md"
AB02R = "analysis/reports/ab02_second_scoreboard.md"
AB03R = "analysis/reports/ab03_engine_forensics.md"
AB04R = "analysis/reports/ab04_decision_value.md"
AB05R = "analysis/reports/ab05_probe_results.md"
AB09R = "analysis/reports/ab09_theory_pack.md"
AB12R = "analysis/reports/ab12_rca_probe.md"
AB14R = "analysis/reports/ab14_market.md"
A3 = R + "a3/a3.json"
A3O = R + "a3/a3_orient_only.json"
REPRO = R + "ab02/bayesys_repro.json"
_ges = lambda arm, k: J(A3O, "families", "semantic", "GES (BIC)", arm, k)  # noqa: E731
REG.update({
    # AB-01 controlled scoreboard
    "ab01.sem.maxp.ctrl": L(AB01R, "0.463", "| **0.463** |"),
    "ab01.for.maxp.ctrl": L(AB01R, "0.359", "| **0.359** |"),
    "ab01.syn.maxp.ctrl": L(AB01R, "0.435", "| **0.435** |"),
    "ab01.pub.for.pc": L(AB01R, "0.220", "0.359 on formula (published 0.220)"),
    "ab01.pub.syn.pc": L(AB01R, "0.307", "0.435 on synthetic (published 0.307)"),
    "ab01.ges.ctrl.sem": L(AB01R, "0.528", "| **0.528** |"),
    "ab01.gies.ctrl.sem": L(AB01R, "0.539", "| **0.539** |"),
    "ab01.fci.index.sem": L(AB01R, "+0.221", "| +0.221 / +0.207 / +0.225 |"),
    "ab01.maxp.index.sem": L(AB01R, "+0.067", "| +0.067 / +0.101 / +0.087 |"),
    "ab01.ges.index.sem": L(AB01R, "+0.022", "| +0.022 / +0.023 / +0.084 |"),
    "ab01.pc.conflict.sem": L(AB01R, "0.070", "| +0.068 | −0.070 |"),
    "ab01.maxp.conflict.sem": L(AB01R, "−0.001", "| −0.001 / +0.001 / +0.000 |"),
    # AB-02 Bayesys
    "ab02.repro.cells": J(REPRO, "gate_by_alpha", "0.05", "cells_reproduced"),
    "ab02.repro.compared": J(REPRO, "gate_by_alpha", "0.05", "cells_compared"),
    "ab02.repro.pc": F(REPRO, lambda d: sum(1 for c in d["cells"] if c["method"] == "pc" and c["alpha"] == 0.05 and c.get("reproduces"))),
    "ab02.repro.pc.n": F(REPRO, lambda d: sum(1 for c in d["cells"] if c["method"] == "pc" and c["alpha"] == 0.05 and "reproduces" in c)),
    "ab02.order.max.pc": L(AB02R, "0.03", "by at most 0.03"),
    "ab02.index.lo": L(AB02R, "+0.04", "+0.04 to +0.30"),
    "ab02.index.hi": L(AB02R, "+0.30", "+0.04 to +0.30"),
    "ab02.ges.property": L(AB02R, "0.09", "0.07-0.09 lower"),
    # AB-03 engines
    "ab03.vendored.exact": L(AB03R, "460", "| 460 | 56 |"),
    "ab03.vendored.inv": L(AB03R, "56", "| 460 | 56 |"),
    "ab03.dodiscover.exact": L(AB03R, "597", "597 of 717 completed"),
    "ab03.dodiscover.n": L(AB03R, "717", "597 of 717 completed"),
    # AB-04 decision value
    "ab04.sem.gies.prec": L(AB04R, "0.753", "| 1.000 | 0.753 | 0.643 | +0.110 |"),
    "ab04.sem.empty": L(AB04R, "0.643", "| 1.000 | 0.753 | 0.643 | +0.110 |"),
    "ab04.for.gies.prec": L(AB04R, "0.851", "| 1.000 | 0.851 | 0.704 |"),
    "ab04.for.empty": L(AB04R, "0.704", "| 1.000 | 0.851 | 0.704 |"),
    "ab04.syn.pc.prec": L(AB04R, "0.646", "0.630 / 0.646"),
    "ab04.syn.empty": L(AB04R, "0.748", "0.756 / 0.748"),
    "ab04.ch.ges.prec": L(AB04R, "0.916", "| 0.971 | 0.916 | 0.813 |"),
    "ab04.ch.empty": L(AB04R, "0.813", "| 0.971 | 0.916 | 0.813 |"),
    "ab04.ch.gap": L(AB04R, "0.084", "| 0.084 (GES) |"),
    "ab04.share.sem": L(AB04R, "33%", "| 33% (GES 29%"),
    "ab04.share.for": L(AB04R, "55%", "| 55% (GES 32%"),
    "ab04.share.syn": L(AB04R, "2%", "| 2%. GES, PC"),
    "ab04.rc.share": L(AB04R, "10-20%", "the most-agreed 10-20% of claims"),
    "ab04.rc.prec": L(AB04R, "0.80-0.92", "are 0.80-0.92 precise"),
    # AB-09 theory
    "ab09.t3.checks": L(AB09R, "51,392", "yes, 51,392 checks, 0 violations"),
    "ab09.t3.violations": L(AB09R, "0", "51,392 checks, 0 violations"),
    # AB-05 / AB-07
    "ab05.crash.runs": L(AB05R, "16", "Of 115 live runs, 16 (14%)"),
    "ab05.crash.total": L(AB05R, "115", "Of 115 live runs, 16 (14%)"),
    "ab07.o1.correct": J(A3, "verdicts", "O1", "value", "correct"),
    "ab07.o1.contra": J(A3, "verdicts", "O1", "value", "contradicted"),
    "ab07.o3.label.correct": J(A3, "verdicts", "O3", "by_label", "correct"),
    "ab07.o3.label.contra": J(A3, "verdicts", "O3", "by_label", "contradicted"),
    "ab07.o3.data": J(A3, "verdicts", "O3", "by_data", "value"),
    "ab07.o4": J(A3, "verdicts", "O4", "value"),
    "ab07.ges.data.f1": _ges("data only", "directed_f1"), "ab07.ges.data.dv": _ges("data only", "dv1_precision"),
    "ab07.ges.model.f1": _ges("+ model tiers", "directed_f1"), "ab07.ges.model.dv": _ges("+ model tiers", "dv1_precision"),
    "ab07.ges.oracle.f1": _ges("+ oracle depth", "directed_f1"), "ab07.ges.oracle.dv": _ges("+ oracle depth", "dv1_precision"),
    "ab07.ges.moved.f1": _ges("+ moved tiers", "directed_f1"), "ab07.ges.moved.dv": _ges("+ moved tiers", "dv1_precision"),
    # AB-12 RCA
    "ab12.a.ac3": L(AB12R, "0.799", "| D | 0.653 | 0.799 |"),
    "ab12.b.ac3": L(AB12R, "0.208", "| D | 0.208 | **0.208** |"),
    "ab12.c.ac3": L(AB12R, "0.901", "| D+K | 0.689 | **0.901** |"),
    "ab12.d.ac3": L(AB12R, "0.932", "| D+K | 0.735 | **0.932** |"),
    "ab12.d.cov": L(AB12R, "0.917", "| 0.917 (44/48) |"),
    "ab12.fabricated": L(AB12R, "40-83%", "On latency, 40-83% of windows"),
    # AB-14 market (labels on the page)
    "ab14.size.lo": L(AB14R, "$28.9M", "**$28.9M** (Global Market Insights)"),
    "ab14.size.hi": L(AB14R, "$59.22B", "**$59.22B** (The Insight Partners)"),
    "ab14.statsig": L(AB14R, "$1.1B", "Statsig **$1.1B** to OpenAI"),
    "ab14.eppo": L(AB14R, "~$220M", "Eppo **~$220M** reported"),
    "ab14.sre": L(AB14R, "$285.1M", "**$285.1M**"),
    "ab14.resolve": L(AB14R, "$125M", "Resolve AI $125M Series A"),
    "ab14.mmm": L(AB14R, "~$2.2B", "**~$2.2B** in 2026"),
    "ab14.rwe": L(AB14R, "$2.0-2.6B", "**$2.0-2.6B** in 2024-2025"),
    "ab14.est.rca": L(AB14R, "$1.8-9.0M", "| $1.8-9.0M ARR obtainable within three years |"),
    "ab14.est.mkt": L(AB14R, "$3-67.5M", "| $3-67.5M obtainable at maturity |"),
    "ab14.est.pharma": L(AB14R, "$2.8-11M", "| $2.8-11M a year for the regulatory core"),
    "ab14.est.pharma.broad": L(AB14R, "$20-100M", "$20-100M a year across all registered RWE studies"),
})

