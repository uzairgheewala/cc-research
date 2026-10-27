"""2026-10-22, wave B build: the tracker side. Refuses to run twice; apply p31 first.

New tickets: BLD-18 (kernel v4 score candidates, pre-registered), BLD-17 (pretrained engine beside GES: decided against by
X5), CAP-19 (cross-host determinism of the claim structure). Records: the BLD-06 live comparison (pre-registered, rule
'drop_in'), the DLV-04 preview, the EXT-03 upstream draft, the BEN-13 fix and report generator, the explanation ledger,
the TA agenda and the Q1 checkpoint outline. No prod status is set here.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p31" in c, "apply p31 first"
assert "# ---- overrides p32" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p32 (2026-10-22): wave B build
ITEMS.append(item("BLD-18", "BLD", "Kernel v4 candidates: a GES score that fits nonlinear and discrete mechanisms (pre-registered knobs on dev)",
                  "in_progress", kind="task",
                  criterion=("Knobs, metrics, predictions and the decision rule hashed before any ledger-level dev number "
                             "(plans/v4_prereg.json); dev evaluation and the rule's outcome (analysis/results/v4/dev.json, decision.json); "
                             "if a knob is adopted: frozen and read once on the sealed held-out family (family 2, replicate 1)"),
                  evidence=["plans/v4_prereg.json", "manifests/evidence/v4_prereg_2026-10-22.sha256", "v4/scores.py", "v4/dev.py",
                            "v4/heldout_gen.py", "tests/test_v4_scores.py", "jobs/waves/B/sheet.json"],
                  note=("22 Oct: from X1-X4 and the family-2 read (linear track 0.851, nonlinear 0.742). Knobs: G0 (v3), G1 (gauss, no "
                        "turning), A1 / A2 (additive hinge + discrete-indicator design, lam 1 / 2), R1 (random Fourier features, ridge). "
                        "Turning is dropped for the new scores, which are not score-equivalent (first smoke file: turning did not finish "
                        "in 8 min; forward + backward 13 s). Sheet B runs the dev grid; no held-out file is read on sheet B.")))
ITEMS.append(item("BLD-17", "BLD", "Pretrained engine beside GES in the ledger (D2-engine)", "done", kind="decision",
                  criterion="X5's pre-registered rule (plans/x5_prereg.json): adopt only if AVICI's paired F1 over GES has a lower end above 0",
                  evidence=["plans/x5_prereg.json", "analysis/results/x5/x5_dev.json"],
                  checks=[{"t": "json", "path": "analysis/results/x5/x5_dev.json", "ptr": ["families", "semantic", "paired", "avici_shuffled_minus_ges", "hi"],
                           "op": "le", "v": 0.0, "tol": None}],
                  note="Decided against 20 Oct (X5): AVICI scm-v0 is below GES on both families (semantic -0.281 [-0.330, -0.232])."))
ITEMS.append(item("CAP-19", "CAP", "Cross-host determinism: the same claims on every machine, the same hash on one CPU family", "done", kind="task",
                  criterion=("The wave canary recomputes ledgers from scratch on Uzair's machine and matches the agent's claim structure "
                             "(claims_sha256) on every file; full ledger hashes are compared per CPU family only"),
                  evidence=["analysis/wave_canary.py", "jobs/waves/A/out/canary.json", "jobs/waves/A/canary_expected.json"],
                  checks=[{"t": "json", "path": "jobs/waves/A/out/canary.json", "ptr": ["match"], "op": "true", "v": None, "tol": None}],
                  note=("Sheet A: an AVX2 host (HASWELL kernel) and the AVX-512 sandbox give different test statistics in the last digits, so "
                        "different full ledger hashes, and identical claims on all three canary files. Qualifies CAP-11.")))
_W32 = {
    "BLD-06": ["plans/bld06_live_prereg.json", "manifests/evidence/bld06_live_prereg_2026-10-22.sha256", "analysis/bld06_live_compare.py",
               "analysis/results/fork/bld06_live_compare.json"],
    "DLV-04": ["analysis/results/fork/bld06_live_compare.json", "plans/bld06_live_prereg.json"],
    "EXT-03": ["docs/drafts/bug_reports/causal_copilot_cycle_step_keyerror.md"],
    "BEN-13": ["analysis/ben13/report.py", "tests/test_ben13_summary.py", "tests/test_ben13_stream.py"],
    "TGT-18": ["analysis/explanation_ledger.py", "analysis/results/q2_v3/explanation_ledger.json"],
    "TGT-19": ["analysis/explanation_ledger.py", "analysis/results/q2_v3/explanation_ledger.json"],
    "CRS-01": ["docs/meetings/2026-10-29_ta_checkin_agenda.md"],
    "BND-13": ["docs/q1/checkpoint_skeleton.md"],
    "INF-10": ["jobs/waves/B/sheet.json"],
}
_N32 = {
    "BLD-06": (" 22 Oct, pre-registered comparison (plans/bld06_live_prereg.json; analysis/results/fork/bld06_live_compare.json): "
               "rule 'drop_in'. Delivered directed F1 +0.071 [0.035, 0.111] over main; on the 22 tables both completed, final "
               "adjacency F1 0.596 vs 0.321 (+0.276 [0.206, 0.335]) and directed F1 +0.014 [-0.017, 0.039]; S0 adjacency F1 "
               "within 0.01 (the two series ran comparable algorithms)."),
    "DLV-04": (" 22 Oct, live inside the real pipeline on S2 (BLD-06 branch, 30 runs): final adjacency F1 below the run's own "
               "algorithm output in 1 of 30 runs (by 0.006), against 22 of 22 completed unmodified runs; no crash; every v2 edge "
               "carries a source. The one 0.006 drop is reported, not rounded away; S1 has no live run of the branch yet."),
    "EXT-03": " 22 Oct: upstream report drafted (docs/drafts/bug_reports/causal_copilot_cycle_step_keyerror.md); Uzair decides whether to send.",
    "BEN-13": (" 22 Oct (wave B): the fast evaluator now keeps a dense network's Wasserstein and marks its FOR undefined; failed "
               "cells are re-run; P1-P4 are scored in summary.json and analysis/reports/ben13_s1_s2.md is generated from it."),
    "TGT-18": (" 22 Oct: explanation ledger (analysis/results/q2_v3/explanation_ledger.json): every dev gap of v3 split into typed "
               "segments that sum to the anatomy totals (semantic missed 1,647 = floor 459 walled + sample size 194 + nonlinear-only "
               "268 + search gap 726)."),
    "TGT-19": " 22 Oct: reversed directions in the explanation ledger: skeleton-caused, rule-caused, open on the true skeleton.",
    "CRS-01": " 22 Oct: agenda written (docs/meetings/2026-10-29_ta_checkin_agenda.md); sheet B numbers marked as pending.",
    "BND-13": " 22 Oct: outline with typed placeholders (docs/q1/checkpoint_skeleton.md); the TA's format answer on 29 Oct shapes the final document.",
}
for _i in ITEMS:
    if _i["id"] in _W32:
        _i["evidence"] = list(_i["evidence"]) + [e for e in _W32[_i["id"]] if e not in _i["evidence"]]
    if _i["id"] in _N32:
        _i["note"] = (_i.get("note") or "") + _N32[_i["id"]]
    if _i["id"] == "BLD-06":
        _i["checks"] = list(_i["checks"]) + [
            {"t": "json", "path": "analysis/results/fork/bld06_live_compare.json", "ptr": ["rule"], "op": "eq", "v": "drop_in", "tol": None},
            {"t": "json", "path": "analysis/results/fork/bld06_live_compare.json", "ptr": ["completed", "branch"], "op": "eq", "v": 30, "tol": None},
            {"t": "json", "path": "analysis/results/fork/bld06_live_compare.json", "ptr": ["completed", "main"], "op": "eq", "v": 22, "tol": None}]
'''
p.write_text(c + "\n", encoding="utf-8")
print("p32 applied")
