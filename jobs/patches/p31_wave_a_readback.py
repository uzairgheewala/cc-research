"""2026-10-22, wave A readback (fourth run, return_A.zip of 22 Oct): the tracker side. Refuses to run twice; apply p30 first.

Records what sheet A decided, by its pre-written decision table and the pre-registrations, without changing any prod status:
  * INF-10 done: the runner ran a full sheet on Uzair's machine (35 runs; tests, canary, gates, resume, limits).
  * TGT-18 / CAP-07: the one family-2 read (500 files, 50 scenarios): precision at half coverage 0.795 [0.777, 0.811],
    ECE 0.042 [0.030, 0.053]. ER-2 and ER-3 not met; the pre-registered transfer rule holds (F1-F4 all hold).
  * BEN-13: S0 and S1 pass (shapes exact; all four published rows within tolerance). P1 refuted, P3 holds, P2 holds where
    computed; P4 and two P2 cells not computed (FOR undefined for dense networks; fixed on sheet B).
  * BLD-06 / EXT-03 / INF-06: the fork branch ran live: 30 of 30 completed vs 22 of 30 for unmodified main on the same image.
  * CAP-11: the ledger hash holds per CPU family; across families the claim structure is equal (canary), not the hash.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p30" in c, "apply p30 first"
assert "# ---- overrides p31" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p31 (2026-10-22): wave A readback (sheet A, fourth run)
_W31 = {
    "INF-10": ["jobs/waves/A/sheet.json", "jobs/waves/A/verdict.json", "jobs/waves/A/state.json"],
    "TGT-18": ["analysis/results/q2_v3/family2_read.json"],
    "CAP-07": ["analysis/results/q2_v3/family2_read.json"],
    "BEN-13": ["analysis/results/ben13/summary.json"],
    "BLD-06": ["analysis/results/fork/fork_bld06_live.json", "plans/results/fork_bld06_live.capped.json",
               "plans/results/fork_bld06_live_main.capped.json"],
    "EXT-03": ["analysis/results/fork/fork_ext03_stub.json", "plans/results/fork_bld06_live_main.capped.json"],
    "INF-06": ["analysis/results/fork/fork_bld06_stub.json", "analysis/results/fork/fork_ext03_stub.json",
               "jobs/waves/images/cc.json"],
    "CAP-11": ["jobs/waves/A/out/canary.json"],
    "TGT-19": ["analysis/results/q2_v3/explain_dev.json"],
}
_N31 = {
    "INF-10": (" 22 Oct: sheet A ran in full on Uzair's machine (fourth run: 35 runs, 26 must-shows scored, decisions "
               "matched; jobs/waves/A/verdict.json). Earlier runs found and fixed by class: CRLF fixtures, CPU-dependent "
               "digests, the freeze guard, empty downloads, a missing image, a hung build (time limits, Docker check)."),
    "TGT-18": (" 22 Oct, family-2 held-out read (one read, 500 files, 50 source scenarios, regime D; "
               "analysis/results/q2_v3/family2_read.json): precision at half coverage 0.795 [0.777, 0.811] at coverage "
               "0.545: ER-2 not met (the bar 0.80 lies inside the interval). Linear track 0.851 [0.826, 0.872] (meets the "
               "precision bar), nonlinear 0.742 [0.726, 0.758]. Pre-registered F1-F4 all hold; rule 'transfer'."),
    "CAP-07": (" 22 Oct, family 2: ECE 0.042 [0.030, 0.053]: the frozen semantic confidence model transfers within its "
               "calibration error (F3), but ER-3 is not met (upper end above 0.05). Under-confident on the linear track "
               "(realised minus claimed +0.064), over-confident on the nonlinear track (-0.046)."),
    "BEN-13": (" 22 Oct, sheet A: S0 shapes exact (K562 162,751 x 622; RPE1 162,733 x 383); S1 all four published "
               "MeanDifference rows within tolerance (Wasserstein to the third decimal). P1 refuted: edge placement "
               "carries 0.13 (K562) and 0.07 (RPE1) of MeanDifference's above-random Wasserstein at k = 1000, so the score "
               "rests on the specific pairs. P3 holds: MeanDifference reaches 0.90 / 0.95 of the test-split total-effect "
               "ceiling. P2 holds in the 3 cells computed. Not computed: random networks at k = 5000 and of literature "
               "size, because CausalBench's false omission rate takes negatives outside the path closure and a dense "
               "network leaves none; the cells also dropped their Wasserstein. Fixed on sheet B. CORUM not reachable."),
    "BLD-06": (" 22 Oct, live on the fork (branch bld-06-refinement-v2, 30 BND-08 tables, gpt-4o): 30 of 30 runs completed "
               "against 22 of 30 for unmodified main on the same rebuilt image (8 crashes in the cycle step; BND-08 had 6 of "
               "30 on the old image); $4.84 against $12.57; refinement v2 ran in all 30. Graph quality against the data "
               "reference is scored on sheet B."),
    "EXT-03": (" 22 Oct: the cycle-step KeyError recurs on unmodified main on the rebuilt image (8 of 30, LIVE_06M) and "
               "never on the branch stubs (fork_ext03_stub: 0)."),
    "INF-06": (" 22 Oct: both branch stubs pass identity and their checks; the Causal-Copilot base image was rebuilt "
               "(new id, jobs/waves/images/cc.json), so live comparisons use LIVE_06M's main control on the same image."),
    "CAP-11": (" 22 Oct: qualified. The ledger hash is the same for the same inputs on one CPU family (BLAS kernel); "
               "between an AVX-512 and an AVX2 host the test statistics differ in the last digits and the full hash "
               "differs, while the claim structure is identical (wave canary, claims_sha256)."),
    "TGT-19": (" 22 Oct: X4 on sheet A: KCI detects the nonlinear-only missed links far above its null "
               "(semantic +0.40, formula +0.52): those links carry signal a nonlinear test can use."),
}
for _i in ITEMS:
    if _i["id"] in _W31:
        _i["evidence"] = list(_i["evidence"]) + [e for e in _W31[_i["id"]] if e not in _i["evidence"]]
    if _i["id"] in _N31:
        _i["note"] = (_i.get("note") or "") + _N31[_i["id"]]
    if _i["id"] == "INF-10":
        _i["status"] = "done"
        _i["checks"] = list(_i["checks"]) + [
            {"t": "json", "path": "jobs/waves/A/verdict.json", "ptr": ["must_shows", "M_T_HOST", "status"], "op": "eq", "v": "pass", "tol": None},
            {"t": "json", "path": "jobs/waves/A/verdict.json", "ptr": ["must_shows", "M_CANARY", "status"], "op": "eq", "v": "pass", "tol": None}]
    if _i["id"] == "TGT-18":
        _i["checks"] = list(_i["checks"]) + [
            {"t": "json", "path": "analysis/results/q2_v3/family2_read.json", "ptr": ["subsets", "all", "ER-2_met"], "op": "false", "v": None, "tol": None},
            {"t": "json", "path": "analysis/results/q2_v3/family2_read.json", "ptr": ["subsets", "all", "precision_half"], "op": "approx", "v": 0.795, "tol": 0.001}]
    if _i["id"] == "BEN-13":
        _i["checks"] = list(_i["checks"]) + [
            {"t": "json", "path": "analysis/results/ben13/summary.json", "ptr": ["reproduction_all"], "op": "true", "v": None, "tol": None}]
    if _i["id"] == "CAP-11":
        _i["criterion"] = (_i.get("criterion") or "") + " (on one CPU family; across families: the same claim structure)"
'''
p.write_text(c + "\n", encoding="utf-8")
print("p31 applied")
