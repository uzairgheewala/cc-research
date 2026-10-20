"""2026-10-20, wave A intake (second rerun): the tracker side. Refuses to run twice; apply p25 first.

Wave A's rerun came back with three failure classes, fixed here (code in the kit, records in the catalogue):
  * F2_READ refused: the freeze's whole-tree hash covers three kernel files added after the freeze. The read now checks
    the frozen files one by one, the core, and the added files against a hashed deviation record, and blocks importing
    the added files (plans/v3_freeze_deviation_1.json; TGT-18).
  * FETCH_CB: figshare sent empty bodies and an empty rpe1.h5ad was accepted. Files are now checked (never empty, magic
    bytes, size, md5) and the two expression files are imported from a browser download (BEN-13).
  * STUB_03 / STUB_06: the Causal-Copilot runtime image was missing. cc.ps1 ensureimage builds only what is missing and
    records whether the base image is still BND-08's (INF-06); a main-control live arm runs only if it is not (BLD-06).
Also: the runner re-runs class A0 (tests, kit checks) when the kit changes (INF-10); X5 recorded (REP-07, BEN-07).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p25" in c, "apply p25 first"
assert "# ---- overrides p30" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p30 (2026-10-20): wave A intake, second rerun (freeze deviation, fetch checks, image check)
_W30 = {
    "TGT-18": ["plans/v3_freeze_deviation_1.json", "manifests/evidence/family2_freeze_deviation_2026-10-20.sha256",
               "tests/test_family2_guard.py"],
    "BEN-13": ["tests/test_ben13_fetch.py"],
    "INF-06": ["cc.ps1", "plans/fork_bld06_live_main.json"],
    "INF-10": ["tests/run_tests.py"],
    "REP-07": ["analysis/results/x5/x5_dev.json"],
    "BEN-07": ["analysis/results/x5/x5_dev.json"],
}
_N30 = {
    "TGT-18": (" 20 Oct (wave A rerun): the family-2 read refused because the freeze's whole-tree hash covers three kernel files "
               "added after it (kernel/asym.py, asym_cond.py, linkfilt.py); no frozen file changed and the core hash is equal. "
               "Deviation record written and hashed before the read (plans/v3_freeze_deviation_1.json): the read checks the "
               "frozen files one by one, the core and the added files' sha256, and blocks importing the added files. No "
               "family-2 file has been scored yet."),
    "BEN-13": (" 20 Oct (wave A rerun): figshare answers programmatic downloads with an empty body, and the old fetcher "
               "accepted a 0-byte rpe1.h5ad. Every file is now checked (not empty, HDF5/zip/gzip magic, published size and "
               "md5); the two expression files come from a browser download, imported from Downloads after the checks."),
    "INF-06": (" 20 Oct (wave A rerun): the stubs could not start (runtime image missing). cc.ps1 ensureimage builds only "
               "the missing images and writes jobs/waves/images/cc.json (is the base image still BND-08's?); "
               "manifests/image_ids.json keeps the earlier record when it rebuilds."),
    "INF-10": (" 20 Oct: class A0 runs (tests, kit checks) re-run when the kit's code identity changes; finished heavy runs "
               "keep their results (tests/test_wave_runner.py)."),
    "REP-07": (" 20 Oct (wave A): AVICI scm-v0 on CausalArena dev, 125 files per family, columns shuffled: mean directed F1 "
               "semantic 0.251 vs GES 0.532 (paired difference -0.281 [-0.330, -0.232]); formula 0.304 vs 0.450 (-0.146 "
               "[-0.193, -0.095]) (analysis/results/x5/x5_dev.json). Pre-registered rule: D1 stays the paper's line."),
    "BEN-07": " 20 Oct (wave A): AVICI's F1 is identical with original and shuffled column order (order effect 0.0): as its permutation-equivariant design implies.",
}
for _i in ITEMS:
    if _i["id"] in _W30:
        _i["evidence"] = list(_i["evidence"]) + [e for e in _W30[_i["id"]] if e not in _i["evidence"]]
    if _i["id"] in _N30:
        _i["note"] = (_i.get("note") or "") + _N30[_i["id"]]
'''
p.write_text(c + "\n", encoding="utf-8")
print("p30 applied")
