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
    "ab05.crash.runs": L(AB05R, "18", "Of 19 live entries into the cycle step, 18 crashed"),
    "ab05.crash.total": L(AB05R, "19", "Of 19 live entries into the cycle step, 18 crashed"),
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

# ---- 2026-10-14: AB-05 close-out and AB-06's Causal-Copilot second-model arm (page 6)
AB05C = R + "ab05/live_calibration.json"
CCR = "analysis/reports/ab06_cc_second_model.md"
PSM = R + "ab06_cc/partial_stages.json"
SVM = R + "ab06_cc/s2_verdicts.json"
REG.update({
    "ab05.vash.untagged": J(AB05C, "agents", "vashishtha", "vashishtha", "share_without_tag"),
    "ab05.vash.ties": J(AB05C, "agents", "vashishtha", "vashishtha", "pairs_tied"),
    "ab05.vash.pairs": J(AB05C, "agents", "vashishtha", "vashishtha", "pairs"),
    "ab05.vash.triplets": J(AB05C, "agents", "vashishtha", "vashishtha", "triplets"),
    "ab05.pywhy.f1": J(AB05C, "agents", "pywhyllm", "f1"),
    "ab06.cc.real.S0": J(PSM, "by_role", "real", "S0_dir_all"), "ab06.cc.real.S3": J(PSM, "by_role", "real", "S3_dir_all"),
    "ab06.cc.swapped.S3": J(PSM, "by_role", "swapped", "S3_dir_all"),
    "ab06.cc.reliance": L(CCR, "0.094", "**0.167** | **0.094**"),
    "ab06.cc.reliance.4o": L(CCR, "0.167", "**0.167** | **0.094**"),
    "ab06.cc.m4.hits": J(SVM, "M4", "hits"), "ab06.cc.m4.families": J(SVM, "M4", "families"),
    "ab06.cc.completed": L(CCR, "26", "| 26 | completed |"),
    "ab06.tierA.usd": L("analysis/reports/ab06_prep.md", "48.23", "| **$48.23** |"),
})

# ---- 2026-10-14: BND-11 (refinement v2 held-out and names part)
V2T = R + "refinement_v2/test_formula.json"
V2N = R + "refinement_v2/names_s2.json"
REG.update({
    "v2.test.files": J(V2T, "summary", "files"), "v2.test.R1": J(V2T, "summary", "R1", "hits"),
    "v2.test.R3": J(V2T, "summary", "R3", "mean_difference"),
    "v2.names.R5": J(V2N, "R5", "hits"), "v2.names.R6": J(V2N, "R6", "hits"),
})

# ---- 2026-10-14: AB-06 field audit (page 6)
AB6 = R + "ab06/ab06.json"
AB06R = "analysis/reports/ab06_field_audit.md"
_ab6 = {}
for _ag in ("causaliq", "matmcd"):
    for _arm in ("real", "neutral", "swapped"):
        _ab6["ab06.%s.%s" % (_ag, _arm)] = J(AB6, "agents", _ag, _arm, "f1_mean")
for _ag in ("pywhyllm", "vashishtha"):
    for _arm in ("real", "swapped"):
        _ab6["ab06.%s.%s" % (_ag, _arm)] = J(AB6, "agents", _ag, _arm, "f1_mean")
for _ag in ("causaliq", "pywhyllm", "matmcd", "vashishtha"):
    _ab6["ab06.%s.nr" % _ag] = J(AB6, "agents", _ag, "name_reliance_real_minus_swapped", "mean")
    _ab6["ab06.%s.nrn" % _ag] = J(AB6, "agents", _ag, "name_reliance_real_minus_swapped", "paired_scenarios")
for _ag in ("matmcd", "vashishtha"):
    _ab6["ab06.%s.floor" % _ag] = J(AB6, "agents", _ag, "data_only_floor_real_arm", "f1_data_only")
    _ab6["ab06.%s.dv" % _ag] = J(AB6, "agents", _ag, "data_only_floor_real_arm", "dv1_precision_final")
    _ab6["ab06.%s.dv.floor" % _ag] = J(AB6, "agents", _ag, "data_only_floor_real_arm", "dv1_precision_data_only")
for _k, _sys in (("cc4o", "causal_copilot_gpt4o"), ("ccmini", "causal_copilot_gpt4omini")):
    for _arm in ("real", "neutral", "swapped"):
        _ab6["ab06.%s.%s" % (_k, _arm)] = J(AB6, "causal_copilot", _sys, _arm, "f1_mean")
    _ab6["ab06.%s.nr" % _k] = J(AB6, "causal_copilot", _sys, "name_reliance_real_minus_swapped", "mean")
_ab6.update({
    "ab06.P9": J(AB6, "P9", "verdict"), "ab06.P10": J(AB6, "P10", "verdict"),
    "ab06.vash.llm_order": J(AB6, "agents", "vashishtha", "real", "direction_sources", "llm_order"),
    "ab06.vash.data": J(AB6, "agents", "vashishtha", "real", "direction_sources", "data"),
    "ab06.empty.dv": L(AB06R, "0.670", "scores DV-1 0.670 on these 10 scenarios"),
    "ab06.matmcd.below.neutral": L(AB06R, "9", "below its own PC graph in 9 and 8 of 10 scenarios"),
    "ab06.matmcd.below.swapped": L(AB06R, "8", "below its own PC graph in 9 and 8 of 10 scenarios"),
    "ab06.usd": L(AB06R, "32.11", "Tier A cost $32.11"),
})
REG.update(_ab6)

# ---- Q2 build, first held-out pass (2026-10-15; jobs/patches/s17_site_q2.py)
HO = R + "q2_b1/heldout.json"
B2S, B3S, B4E = R + "q2_b2/summary_test.json", R + "q2_b3/summary_test.json", R + "q2_b4/evaluate_test.json"
RV, B5T, AD, LM = R + "q2_b4/raw_vs_calibrated_test.json", R + "q2_b5/rca_test.json", R + "q2_b5/adapters.json", R + "q2_landmarks.json"
_q2 = {}
for _f, _k in (("semantic", "sem"), ("formula", "for")):
    for _vs, _p in (("vs_pc_maxp", "erf"), ("vs_ges", "ges")):
        for _e in ("point", "lo", "hi"):
            _s = "" if _e == "point" else "." + _e
            _q2["q2.%s.%s.f1%s" % (_p, _k, _s)] = J(HO, "families", _f, _vs, "f1_diff", _e)
            _q2["q2.%s.%s.dv%s" % (_p, _k, _s)] = J(HO, "families", _f, _vs, "dv1_pooled_diff", _e)
    _q2["q2.b2.%s.dv" % _k] = J(B2S, "families", _f, "dv1_pooled_diff", "point")
    _q2["q2.b2.%s.dv.lo" % _k] = J(B2S, "families", _f, "dv1_pooled_diff", "lo")
    _q2["q2.b2.%s.perfile" % _k] = J(B2S, "families", _f, "dv1_mean_per_file_diff")
    for _e in ("point", "lo", "hi"):
        _q2["q2.b3.%s.gain%s" % (_k, "" if _e == "point" else "." + _e)] = J(B3S, "families", _f, "arms", "real", "gain", _e)
    _q2["q2.b3.%s.files" % _k] = J(B3S, "families", _f, "arms", "neutral", "files")
    _q2["q2.b3.%s.neutral" % _k] = J(B3S, "families", _f, "arms", "neutral", "claims_identical_to_D")
    _q2["q2.b3.%s.t3" % _k] = J(B3S, "families", _f, "arms", "moved", "within_t3")
    _q2["q2.b3.%s.moved" % _k] = J(B3S, "families", _f, "arms", "moved", "gain", "point")
    for _e in ("point", "lo", "hi"):
        _q2["q2.b4.%s.prec%s" % (_k, "" if _e == "point" else "." + _e)] = J(B4E, "families", _f, "dv", "er2_interval", _e)
    _q2["q2.b4.%s.cov" % _k] = J(B4E, "families", _f, "dv", "selective_at_half_coverage", "coverage")
    _q2["q2.b4.%s.ece" % _k] = J(B4E, "families", _f, "dv", "ece")
    _q2["q2.b4.%s.ece.hi" % _k] = J(B4E, "families", _f, "dv", "ece_interval", "hi")
    _q2["q2.b4.%s.raw" % _k] = J(RV, "families", _f, "dv", "ece_raw", "point")
_CH = "chambers", "rows"
_q2.update({
    "q2.ch.kdi": J(B2S, *_CH, "kernel D+I (C3)", "precision"), "q2.ch.kd": J(B2S, *_CH, "kernel D (C3)", "precision"),
    "q2.ch.ges": J(B2S, *_CH, "GES (BIC)", "precision"), "q2.ch.pc": J(B2S, *_CH, "PC maxP (plain call)", "precision"),
    "q2.ch.agree": J(B2S, *_CH, "kernel D+I (C3)", "agreement_with_check_rows"),
    "q2.ch.true.agree": J(B2S, *_CH, "true DAG", "agreement_with_check_rows"),
    "q2.b5.ac3": J(B5T, "ER-4b", "AC@3_answered"), "q2.b5.ac3.lo": J(B5T, "ER-4b", "lo"), "q2.b5.cov": J(B5T, "ER-4b", "coverage"),
    "q2.b5.answered": J(B5T, "ER-4b", "answered"),
    "q2.b5.learned": J(B5T, "variants", "learned_ledger_only", "AC@3_answered"),
    "q2.b5.learned.cov": J(B5T, "variants", "learned_ledger_only", "coverage"),
    "q2.b5.cc.created": J(AD, "agents", "causal_copilot_gpt4o", "violations", "knowledge_created_connection"),
    "q2.b5.matmcd.reversed": J(AD, "agents", "matmcd", "violations", "knowledge_reversed_data"),
    "q2.paper.met": F(LM, lambda d: len(d["paper_constraints_met"])),
    "q2.wedge.met": F(LM, lambda d: len(d["wedge_constraints_met"])),
})
for _er in ("ER-F", "ER-1", "ER-2", "ER-3", "ER-4a", "ER-4b", "ER-C"):
    _q2["q2.lm." + _er] = F(LM, lambda d, _er=_er: "met" if d["landmarks"][_er]["met"] else "not met")
REG.update(_q2)

# ---- kernel v3 (2026-10-15; jobs/patches/s19_site_v3.py)
V3T = R + "q2_v3/v3_test.json"
FLS, FLF = R + "q2_v3/floor_dev_semantic.json", R + "q2_v3/floor_dev_formula.json"
K0S = R + "q2_v3/k0_check_v2_semantic.json"
_v3 = {}
for _f, _k in (("semantic", "sem"), ("formula", "for")):
    for _r in ("D", "DxR"):
        _v3["q2v3.%s.%s.p" % (_k, _r)] = J(V3T, "families", _f, _r, "precision_half")
        _v3["q2v3.%s.%s.lo" % (_k, _r)] = J(V3T, "families", _f, _r, "er2_interval", "lo")
        _v3["q2v3.%s.%s.cov" % (_k, _r)] = J(V3T, "families", _f, _r, "coverage_half")
        _v3["q2v3.%s.%s.ece" % (_k, _r)] = J(V3T, "families", _f, _r, "ece")
        _v3["q2v3.%s.%s.ecehi" % (_k, _r)] = J(V3T, "families", _f, _r, "ece_interval", "hi")
        _v3["q2v3.%s.%s.er2" % (_k, _r)] = F(V3T, lambda d, _f=_f, _r=_r: "met" if d["families"][_f][_r]["ER-2_met"] else "not met")
_v3.update({
    "q2v3.floor.sem": J(FLS, "classes", "floor", "share_of_true_links"), "q2v3.floor.for": J(FLF, "classes", "floor", "share_of_true_links"),
    "q2v3.missed.sem": J(FLS, "missed_share"), "q2v3.missed.for": J(FLF, "missed_share"),
    "q2v3.gap.sem": J(FLS, "classes", "method_linear", "share_of_true_links"), "q2v3.gap.for": J(FLF, "classes", "method_linear", "share_of_true_links"),
    "q2v3.k0.equal": J(K0S, "row_hashes_equal"),
})
REG.update(_v3)



# S23 (20 Oct): which reads a landmark binds to. A key under a superseded prefix may still be printed, but only as history
# (common.n(..., historic=True)); the build fails otherwise. v3's second held-out read binds ER-2 and ER-3 (plans/v3_freeze.json).
SUPERSEDED = {
    "q2.b4.": {"by": "q2v3.<family>.<regime>.*", "why": "B4 was the first held-out read; kernel v3's second read binds ER-2 / ER-3"},
}


# ---- s24 (site v3 data layer, TEAM-10): numbers for Today, gaps and explore (project doc claude/site-v3-design-2026-10-20.md)
def MDT(path, heading):
    """The first markdown table after the line starting with heading (rows as dicts keyed by the header; tracker/snapshot.py)."""
    return {"src": path, "mdtable": heading}


H3D, AN3 = R + "q2_v3/headroom_dev.json", R + "q2_v3/anatomy_dev.json"
_s24 = {}
for _f, _k in (("semantic", "sem"), ("formula", "for")):
    _s24["q2k.%s.f1" % _k] = J(HO, "families", _f, "vs_pc_maxp", "kernel", "f1")
    _s24["q2k.%s.n" % _k] = J(HO, "families", _f, "vs_ges", "f1_diff", "clusters")
    for _o in ("O0", "O1", "O2", "O3", "O4"):
        _s24["q2h.%s.%s.f1" % (_k, _o)] = J(H3D, "families", _f, "v3_D", "ladder", _o, "f1")
        _s24["q2h.%s.%s.p" % (_k, _o)] = J(H3D, "families", _f, "v3_D", "ladder", _o, "precision")
    for _g in ("true", "found", "missed", "false"):
        _s24["q2a.%s.%s" % (_k, _g)] = J(AN3, "families", _f, "v3_D", "links", _g)
    _s24["q2a.%s.reversed" % _k] = J(AN3, "families", _f, "v3_D", "directions", "reversed")
    _s24["q2v3.%s.D.n" % _k] = J(V3T, "families", _f, "D", "scenarios")
    _s24["q2v3.%s.D.rmc4" % _k] = J(V3T, "families", _f, "D", "realised_minus_claimed_intervals", "4", "point")
    _s24["q2v3.%s.D.rmc4.lo" % _k] = J(V3T, "families", _f, "D", "realised_minus_claimed_intervals", "4", "lo")
_BT = "docs/project_snapshots/2026-10-19/benchmark-targets.md"
_s24.update({
    "pub.real.D": L(_BT, "0.391", "0.391 observational (CDFM, 13 datasets)"),
    "pub.real.DI": L(_BT, "0.462", "0.462 with interventions (TabCausal, 7 datasets)"),
    "cb.k562.w": J("plans/ben13_prereg.json", "published", "k562", "md_k5000", "wasserstein"),
    "cb.k562.for": J("plans/ben13_prereg.json", "published", "k562", "md_k5000", "for"),
    "cb.rpe1.w": J("plans/ben13_prereg.json", "published", "rpe1", "md_k5000", "wasserstein"),
    "cb.rpe1.for": J("plans/ben13_prereg.json", "published", "rpe1", "md_k5000", "for"),
    "due.CRS-01": F("tracker/status.json", lambda d: next(i["due"] for i in d["items"] if i["id"] == "CRS-01")),
    "due.BND-13": F("tracker/status.json", lambda d: next(i["due"] for i in d["items"] if i["id"] == "BND-13")),
    "lev.links": MDT("docs/design/q2_lever_map.md", "## 2."),
    "lev.dirs": MDT("docs/design/q2_lever_map.md", "## 3."),
})
# files other parallel chats write (B1 explanation ledger, B4 power table): registered only once they exist, so the
# snapshot never fails on a file that is not there yet; site/gaps_spec.json says whether the site requires them.
import os as _os  # noqa: E402
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
for _key, _path in (("q2x.ledger", R + "q2_v3/explain_ledger_dev.json"), ("q2p.power", R + "q2_v3/power_dev.json")):
    if _os.path.exists(_os.path.join(_ROOT, _path)):
        _s24[_key] = F(_path, lambda d: d)
REG.update(_s24)

# visibility (s24; repo split, decision R-1 open): source paths that live in the private repository. A public page may not
# link them and the explorer export may not contain them (site/build.py fails). Empty until R-1 is decided.
PRIVATE_PATHS = []
