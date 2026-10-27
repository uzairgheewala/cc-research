"""2026-10-22, wave B readback (sheet B, second run): the tracker side. Refuses to run twice; apply p32 first.

Records what sheet B decided by its pre-written rules: no v4 knob clears the rule (v3 stays; no held-out file read);
BEN-13 S2 complete for MeanDifference (P1 fails, P2-P4 hold); the v4 held-out family written and sealed; the data
manifest re-taken. No prod status is set here.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p32" in c, "apply p32 first"
assert "# ---- overrides p33" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p33 (2026-10-22): wave B readback
_W33 = {
    "BLD-18": ["analysis/results/v4/dev.json", "analysis/results/v4/decision.json", "analysis/results/v4/heldout_seal.json",
               "analysis/results/v4/CONTRACT.json", "jobs/waves/B/verdict.json"],
    "TGT-18": ["analysis/results/v4/decision.json"],
    "BEN-13": ["analysis/reports/ben13_s1_s2.md", "analysis/results/ben13/CONTRACT.json"],
}
_N33 = {
    "BLD-18": (" 22 Oct, sheet B (analysis/results/v4/decision.json): no knob clears the pre-registered rule, so v3 stays and no "
               "held-out file is read. Semantic dev precision at half coverage, paired gain over G0 (0.808): A1 +0.040 "
               "[-0.011, 0.094], R1 +0.030 [-0.020, 0.076], A2 +0.015 [-0.031, 0.065]; A1 is also ineligible on formula (0.866 "
               "against G0's 0.881). The new scores cut GES's false adjacencies by 38-60 % per file (Q3 holds) and raise "
               "skeleton F1 (Q1 holds), but under every new score the true DAG still never scores as high as GES's output on a "
               "semantic file (Q2 fails: 0 of 125 for A1, A2 and R1). The G0 canary reproduces v3's dev number (0.8077 against 0.8078). Dropping the turning phase "
               "is neutral (Q4). Held-out family 2 replicate 1: 500 files written and sealed, scored by no kernel."),
    "TGT-18": (" 22 Oct: the score lever (BLD-18) moved semantic dev precision in the predicted direction for all three nonlinear "
               "scores, but no gain's interval excludes zero on 25 dev scenarios; ER-2 stays not met."),
    "BEN-13": (" 22 Oct, sheet B: S2 complete for MeanDifference (analysis/reports/ben13_s1_s2.md). P1 fails (placement shares "
               "0.07-0.14), P2 holds in all 4 cells, P3 holds (0.90 / 0.95), P4 holds (STRING links 0.132 vs at most 0.113 for "
               "same-size random networks in K562, 0.118 vs 0.099 in RPE1). MeanDifference's false omission rate is within the "
               "tolerance of random networks' in all three computable cells, so the FOR metric does not separate it from "
               "random. Other published methods not yet audited (criterion: per published method)."),
}
for _i in ITEMS:
    if _i["id"] in _W33:
        _i["evidence"] = list(_i["evidence"]) + [e for e in _W33[_i["id"]] if e not in _i["evidence"]]
    if _i["id"] in _N33:
        _i["note"] = (_i.get("note") or "") + _N33[_i["id"]]
    if _i["id"] == "BLD-18":
        _i["checks"] = list(_i["checks"]) + [
            {"t": "json", "path": "analysis/results/v4/decision.json", "ptr": ["winner"], "op": "eq", "v": None, "tol": None},
            {"t": "json", "path": "analysis/results/v4/heldout_seal.json", "ptr": ["files"], "op": "eq", "v": 500, "tol": None}]
    if _i["id"] == "BEN-13":
        _i["checks"] = list(_i["checks"]) + [
            {"t": "json", "path": "analysis/results/ben13/summary.json", "ptr": ["predictions", "P1", "verdict"], "op": "eq", "v": "fails", "tol": None},
            {"t": "json", "path": "analysis/results/ben13/summary.json", "ptr": ["predictions", "P4", "verdict"], "op": "eq", "v": "holds", "tol": None}]
'''
p.write_text(c + "\n", encoding="utf-8")
print("p33 applied")
