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
