"""2026-10-15: the Q2 build, first pass. Bundles B0-B5 of plans/q2_dag.json (approved 15 Oct, amended once) built, each read
held-out once under its freeze. Issues TGT-18, TGT-19, TGT-20, BLD-15 and EXT-07; sets statuses and evidence from the gate
results; adds the Q2 bundles to BUNDLE_STATUS and the snapshot. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p16" in c, "apply p16 first"
assert "# ---- overrides p17" not in c, "already applied"
block = r'''
# ---- overrides p17 (2026-10-15): the Q2 build, first pass (B0-B5 of plans/q2_dag.json)
_Q = "analysis/results/"
_B0R, _B1R, _B2R, _B3R = ("analysis/reports/q2_b0_engines_guards.md", "analysis/reports/q2_b1_data_only_ledger.md",
                          "analysis/reports/q2_b2_interventions.md", "analysis/reports/q2_b3_knowledge_tiers.md")
_B4R, _B5R, _BR = "analysis/reports/q2_b4_confidence.md", "analysis/reports/q2_b5_audit_adapter_rca.md", "analysis/reports/q2_build_results.md"
_HO = _Q + "q2_b1/heldout.json"
_B2S, _B3S, _B4E, _B5T = _Q + "q2_b2/summary_test.json", _Q + "q2_b3/summary_test.json", _Q + "q2_b4/evaluate_test.json", _Q + "q2_b5/rca_test.json"
_LM = _Q + "q2_landmarks.json"
_MAN = {"t": "manifest", "path": "manifests/evidence/q2_build_2026-10-15.sha256"}
ITEMS.append(item("TGT-18", "TGT", "DV-1 precision > 0.80 at >= 50% coverage, both families, held out (landmark ER-2)", "todo", kind="target",
                  criterion="Lower end of the scenario-cluster 95% interval of DV-1 precision of the selective view at >= 0.50 coverage "
                            "> 0.80 on the CausalArena test split, semantic and formula (docs/decisions/2026-10-14_q2_landmarks.md)"))
ITEMS.append(item("TGT-19", "TGT", "Accuracy landmark ER-4a: data-only F1 above GES (route A), or knowledge tiers lift > 0.03 (route B)", "todo",
                  kind="target",
                  criterion="Route A: kernel D minus GES directed F1, lower end > 0 on one family; route B: D+K minus D (real names), "
                            "lower end > 0.03 on one family; held out"))
ITEMS.append(item("TGT-20", "TGT", "RCA through the ledger: AC@3 >= 0.90 at coverage >= 0.5 on PetShop held out (landmark ER-4b)", "todo",
                  kind="target",
                  criterion="Lower end of the 95% bootstrap interval over test issues (2,000 resamples, seed 20261015) of AC@3 on "
                            "answered issues >= 0.90, coverage >= 0.5"))
ITEMS.append(item("BLD-15", "BLD", "Audit adapter: other systems' outputs read as typed claims with violation classes", "todo",
                  criterion="Every flagged violation names a pair, a claim and a source; 0 unknown sources for agents that record "
                            "provenance; Causal-Copilot's provenance reconstructed from stage graphs and labelled as such (B5.1)"))
ITEMS.append(item("EXT-07", "EXT", "Note to causal-learn maintainers: PC's Meek step can return a directed cycle (stale ancestor matrix)",
                  "open", kind="decision",
                  criterion="Uzair decides whether to send; the draft states the measurement and a minimal reproduction",
                  evidence=["docs/drafts/bug_reports/causal_learn_meek_directed_cycle.md", _B1R],
                  checks=[G(_B1R, r"Two engine defects")],
                  note="Found in B1 rung R1 (6 dev and 6 held-out files). The kernel works around it (re-derivation, cycles withdrawn and "
                       "recorded), so nothing waits on the note."))
_P17 = {
    # ---------------- B0
    "CAP-05": dict(status="done", blocked_by=None, criterion="Engines see canonical column order only; claims and evidence identical under "
                   "column permutations (oracle and full reruns)",
                   evidence=[_Q + "q2_b0/oracle_check.json", _Q + "q2_b1/invariance_dev.json", _B0R, _B1R],
                   checks=[J(_Q + "q2_b0/oracle_check.json", ["order_invariant_dags"], "eq", 120),
                           J(_Q + "q2_b1/invariance_dev.json", ["content_identical"], "eq", 50)],
                   note="B0.1: 120/120 oracle DAGs order-invariant (6 orders each). B1 R3: 50/50 dev files identical claims and evidence "
                        "under 6 orders with full engine reruns. Names can still break ties among exactly identical columns (B3 finding; "
                        "docs/design/q2_kernel_v3_proposals.md K3-1)."),
    "CAP-11": dict(status="done", blocked_by=None, criterion="Same inputs, same ledger hash",
                   evidence=[_Q + "q2_b1/invariance_dev.json", _B1R],
                   checks=[J(_Q + "q2_b1/invariance_dev.json", ["hash_repeat_identical"], "eq", 50)],
                   note="50/50 repeat builds give the same ledger hash (B1 R3); single-threaded engines pinned in engines/MANIFEST.json."),
    # ---------------- B1
    "BLD-02": dict(status="done", blocked_by=None, criterion="Data-only ledger (B1) passes I1-I4, I7 on dev and its held-out gate B1.2",
                   evidence=["kernel/", "plans/b1_prereg.json", "plans/b1_prereg_amendment_1.json", "plans/b1_freeze.json", _HO,
                             _Q + "q2_b1/access_log.jsonl", _B1R],
                   checks=[J(_HO, ["B1.2_pass"], "true"), J(_HO, ["ER-F_met"], "true"), _MAN],
                   note="Rule C3 (GES-led, PC-audited) chosen on dev. Held out against plain PC maxP: F1 +0.053 / +0.115, DV-1 +0.073 / "
                        "+0.053 (semantic / formula), every interval above zero; against GES F1 -0.001 / +0.002, DV-1 +0.028 / +0.030. "
                        "One aborted read (build error on an engine defect), fixed as a class by amendment 1 and re-read once."),
    "BLD-14": dict(status="done", blocked_by=None,
                   evidence=["ledger/schema02.py", "ledger/verify02.py", "tests/test_q2_kernel.py", _B1R],
                   checks=[G(_B1R, r"1,250 dev and 500 held-out ledgers pass V1-V13 and K7")],
                   note="Ledger v0.2 fields (plan, deviations, assumptions with sensitivities, lineage, question, orientation convention, "
                        "engine outputs, reviews); the verifier runs every check (V1-V13) even after a failure."),
    "CAP-09": dict(status="done", blocked_by=None, criterion="Every claim cites its evidence; an independent NumPy checker (K7) re-derives "
                   "every claim from the records alone",
                   evidence=["kernel/checker.py", "kernel/derive.py", "tests/test_q2_kernel.py", _B1R, _B2R, _B3R],
                   checks=[G(_B1R, r"removing a load-bearing uncited test fails K7")],
                   note="0 failing ledgers across B1 (1,750), B2 (1,002) and B3 (750 held-out and 750 dev D+K ledgers)."),
    "TGT-10": dict(status="done", blocked_by=None, criterion="Zero change in claims when columns are shuffled",
                   evidence=[_Q + "q2_b1/invariance_dev.json", _Q + "q2_b0/oracle_check.json"],
                   checks=[J(_Q + "q2_b1/invariance_dev.json", ["pass"], "true")],
                   note="Met by construction and measured: 50/50 dev files, 120/120 oracle DAGs."),
    "TGT-19": dict(status="in_progress", blocked_by=None,
                   evidence=[_HO, _B3S, _LM, _B1R, _B3R, "docs/design/q2_kernel_v3_proposals.md"],
                   checks=[J(_HO, ["ER-4a_route_A_met"], "false"), J(_B3S, ["families", "formula", "ER-4a_route_B", "met"], "false")],
                   note="Measured, not met. Route A: F1 against GES -0.001 [-0.007, +0.005] / +0.002 [-0.012, +0.017]. Route B: tier gain "
                        "+0.019 [+0.010, +0.030] / +0.028 [+0.019, +0.037], lower ends below 0.03. Candidates for a v3 kernel in "
                        "docs/design/q2_kernel_v3_proposals.md."),
    # ---------------- B2
    "BLD-03": dict(status="done", blocked_by=None, criterion="Interventions as shift evidence orient adjacent pairs only; B2.1 and B2.2 pass",
                   evidence=["kernel/interventions.py", "kernel/run_b2.py", "plans/b2_prereg.json", "plans/b2_freeze.json", _B2S,
                             _Q + "q2_b2/chambers.json", _Q + "q2_b2/access_log.jsonl", _B2R],
                   checks=[J(_B2S, ["families", "semantic", "B2.2_family"], "true"), J(_B2S, ["families", "formula", "B2.2_family"], "true"),
                           J(_B2S, ["chambers", "B2.2_chambers"], "true")],
                   note="Held out: D+I DV-1 mean per-file gain +0.017 / +0.005 (semantic / formula); Chambers D+I 0.926 vs D 0.925; "
                        "0 failing ledgers."),
    "CAP-03": dict(status="done", blocked_by=None, evidence=[_B2S, _B2R],
                   checks=[J(_B2S, ["families", "semantic", "B2.2_family"], "true")],
                   note="Single-target intervention rows enter as shift evidence (Welch, alpha 0.01); an intervention overrides a data "
                        "direction and the claim records the conflict."),
    "TGT-06": dict(status="in_progress", blocked_by=None, evidence=[_Q + "q2_b2/chambers.json", _B2R],
                   checks=[J(_B2S, ["chambers", "ER-C", "within_0.03"], "eq", [True, True])],
                   note="ER-C met on DV-1 precision: kernel D 0.925, D+I 0.926, GES 0.916, PC maxP 0.887; agreement with held-back rows "
                        "0.985 (true DAG 0.943). The F1 comparison with CDFM's second-hand 0.727 needs its subset confirmed (REP-09) and "
                        "was not pre-registered for B2."),
    # ---------------- B3
    "BLD-04": dict(status="done", blocked_by=None, criterion="Declared knowledge as tiers on open pairs only; B3.1-B3.3 pass held out",
                   evidence=["kernel/knowledge.py", "kernel/run_b3.py", "supplier/tiers.py", "plans/b3_prereg.json", "plans/b3_freeze.json",
                             _B3S, _Q + "q2_b3/access_log.jsonl", _B3R],
                   checks=[J(_B3S, ["families", "semantic", "B3.1"], "true"), J(_B3S, ["families", "formula", "B3.1"], "true"),
                           J(_B3S, ["families", "semantic", "B3.2"], "true"), J(_B3S, ["families", "formula", "B3.2"], "true"),
                           J(_B3S, ["families", "semantic", "B3.3"], "true"), J(_B3S, ["families", "formula", "B3.3"], "true")],
                   note="No new model call: AB-07's recorded gpt-4o replies replayed through the supplier contract. Neutral arm equals D "
                        "125/125 per family; skeleton never moves; moved-arm loss within T3 125/125; 0 failing ledgers."),
    "CAP-04": dict(status="done", blocked_by=None, evidence=[_B3S, _B3R],
                   checks=[J(_B3S, ["families", "semantic", "B3.1"], "true")],
                   note="Tiers orient only pairs the data left open; consensus of the answering phrasings; no propagation; cycles skipped "
                        "and recorded."),
    "TGT-11": dict(status="done", blocked_by=None, criterion="Moved-names loss within the exact T3 bound on 100% of held-out files",
                   evidence=[_B3S, _B3R],
                   checks=[J(_B3S, ["families", "semantic", "B3.2"], "true"), J(_B3S, ["families", "formula", "B3.2"], "true")],
                   note="125/125 per family; realised moved-arm F1 change -0.001 [-0.007, +0.004] / +0.003 [-0.006, +0.013]."),
}
_RV = _Q + "q2_b4/raw_vs_calibrated_test.json"
_AD = _Q + "q2_b5/adapters.json"
_P17.update({
    # ---------------- B4
    "BLD-05": dict(status="done", blocked_by=None, criterion="B4 built (stability, isotonic maps frozen before the held-out read, selective "
                   "view at c/g = 1, 2, 4) and read held out once; gates B4.1 and B4.2 reported",
                   evidence=["kernel/confidence.py", "kernel/run_b4.py", "calibration/", "plans/b4_prereg.json", "plans/b4_freeze.json",
                             _B4E, _RV, _Q + "q2_b4/access_log.jsonl", _B4R],
                   checks=[J(_B4E, ["families", "formula", "dv", "ece"], "le", 0.05), _MAN],
                   note="Held out: B4.1 (ECE <= 0.05) fails on semantic (0.057) and passes on formula (0.036); B4.2 passes (realised >= "
                        "claimed - 0.03 at c/g = 1, 2, 4 on point estimates). The semantic miss is under-claiming: test claims are "
                        "right more often than dev claims at the same stability."),
    "CAP-07": dict(status="in_progress", blocked_by=None, evidence=[_B4E, _RV, _B4R],
                   checks=[J(_RV, ["TGT-12_met"], "true")],
                   note="Every claim carries a calibrated probability (isotonic map on 10-resample stability). Held-out ECE 0.057 "
                        "semantic / 0.036 formula against 0.199 / 0.165 raw; the 0.05 gate is missed on semantic. Proposals in "
                        "docs/design/q2_kernel_v3_proposals.md (K3-4)."),
    "CAP-08": dict(status="done", blocked_by=None, criterion="Selective view: claims kept by calibrated probability at stated cost "
                   "ratios; realised >= claimed - 0.03 (B4.2)",
                   evidence=[_B4E, _B4R], checks=[G(_B4R, r"\*\*B4.2\*\* realised >= claimed - 0.03 at c/g = 1, 2, 4 \| \*\*pass\*\*")],
                   note="Selective view at c/g = 1, 2, 4 (act when p >= 0.5, 0.667, 0.8) and at half coverage; realised precision at "
                        "or above claimed in both families."),
    "TGT-12": dict(status="done", blocked_by=None, criterion="Calibrated ECE below raw bootstrap-frequency ECE on held-out scenarios "
                   "(lower end of the scenario-cluster interval of the difference > 0), both families",
                   evidence=[_RV, _B4R], checks=[J(_RV, ["TGT-12_met"], "true")],
                   note="Raw minus calibrated ECE +0.143 [+0.090, +0.166] semantic, +0.129 [+0.081, +0.167] formula (DV-1 claims), "
                        "computed from the rows of B4's single logged read."),
    "TGT-18": dict(status="in_progress", blocked_by=None, evidence=[_B4E, _LM, _B4R],
                   checks=[J(_LM, ["landmarks", "ER-2", "met"], "false")],
                   note="Measured, not met: semantic 0.812 [0.756, 0.864] at coverage 0.578; formula 0.899 [0.854, 0.939] at 0.615 "
                        "(met for formula alone). 25 scenarios per family set the interval."),
    # ---------------- B5
    "BLD-15": dict(status="done", blocked_by=None, evidence=["audit/adapters.py", "audit/run_adapters.py", "audit/export_cc_stages.py", _AD, _B5R],
                   checks=[J(_AD, ["B5.1", "pass"], "true"), J(_AD, ["B5.1", "unknown_sources_where_provenance_recorded"], "eq", 0)],
                   note="Five systems' AB-06 outputs read as typed claims; Causal-Copilot's sources rebuilt from stage graphs (30/30 equal) "
                        "and labelled. Flags e.g. 384 connections Causal-Copilot's knowledge created against its data floor, 398 MATMCD "
                        "reversals of its own data."),
    "TGT-20": dict(status="in_progress", blocked_by=None, evidence=[_B5T, _LM, _B5R],
                   checks=[J(_B5T, ["ER-4b", "met"], "false"), J(_B5T, ["ER-4b", "answered"], "eq", 44)],
                   note="Measured, not met under the interval rule: AC@3 0.932 [0.841, 1.000] at coverage 0.917 on 44 answered issues "
                        "(reproduces AB-12 exactly). A lower end of 0.90 needs at most one miss at this sample size: more issues, not "
                        "a better ranking."),
})
for _i in ITEMS:
    if _i["id"] in _P17:
        _u = {k: v for k, v in _P17[_i["id"]].items() if v is not None or k == "blocked_by"}
        _i.update(_u)

_B17 = {"B0": "done", "B1": "done", "B2": "done", "B3": "done", "B4": "done", "B5": "done"}
BUNDLE_STATUS.update(_B17)
BUNDLE_NOTE.update({
    "B0": "Done 15 Oct: B0.1 oracle 720/720 exact, 120/120 order-invariant; B0.2 fault suite 7/7; scorer reproduces 102 audit numbers "
          "exactly; baselines on the test splits.",
    "B1": "Done 15 Oct: rule C3 held out beats PC maxP on F1 and DV-1 in both families (ER-F met); ties GES on F1 (route A not met), "
          "beats it on DV-1. 1,750 ledgers verify; one aborted read, fixed as a class.",
    "B2": "Done 15 Oct: D+I >= D on DV-1 held out (both families) and on Chambers; ER-C met (kernel 0.926 vs GES 0.916).",
    "B3": "Done 15 Oct, no live run (recorded AB-07 replies): ER-1 met (neutral = D, skeleton fixed, moved within T3, every ledger "
          "verifies); route B not met (+0.019 / +0.028).",
    "B4": "Done 15 Oct: calibrated ECE 0.057 / 0.036 vs raw 0.199 / 0.165 (TGT-12 met); B4.1 fails on semantic; ER-2 met for formula "
          "only (semantic lower end 0.756); ER-3 not met.",
    "B5": "Done 15 Oct: adapter B5.1 passes on five systems; RCA through the ledger reproduces AB-12 (0.932 at 0.917); ER-4b not met "
          "(lower end 0.841, 44 issues). Held-out read ran after B4.1 failed; B5 uses nothing from B4 (deviation recorded).",
})
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p17 applied to catalogue.py")

# snapshot: show the Q2 DAG's bundles next to the Q1 and audit bundles
q = ROOT / "tracker" / "snapshot.py"
t = q.read_text(encoding="utf-8")
old = '''    audit = load("plans/audit_dag.json")
    out = []
    for plan, b in [("q1", b) for b in dag["bundles"]] + [("audit", b) for b in audit["bundles"]]:'''
new = '''    audit = load("plans/audit_dag.json")
    q2 = load("plans/q2_dag.json")
    out = []
    for plan, b in [("q1", b) for b in dag["bundles"]] + [("audit", b) for b in audit["bundles"]] + [("q2", b) for b in q2["bundles"]]:'''
assert t.count(old) == 1
t = t.replace(old, new)
old2 = '''    return out, dag.get("milestones", []) + audit.get("milestones", [])'''
new2 = '''    return out, dag.get("milestones", []) + audit.get("milestones", []) + q2.get("milestones", [])'''
assert t.count(old2) == 1
t = t.replace(old2, new2)
q.write_text(t, encoding="utf-8")
print("snapshot.py: Q2 bundles included")
