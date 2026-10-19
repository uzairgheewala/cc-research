"""2026-10-15: kernel v3 (bundles K0-K4 of docs/design/q2_kernel_v3_design.md), built and measured on dev, frozen, and read
held out (the second read of the CausalArena test splits). Issues BLD-16; updates TGT-18, TGT-19, CAP-07, CAP-11 notes and
evidence; adds /cache/ to .gitignore. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p17" in c, "apply p17 first"
assert "# ---- overrides p18" not in c, "already applied"
block = r'''
# ---- overrides p18 (2026-10-15): kernel v3 (K0-K4), dev experiments, freeze 0cda331ea81cf0dd, second held-out read
_V3 = "analysis/results/q2_v3/"
_V3R, _V3D, _V3K0 = "analysis/reports/q2_v3_heldout.md", "analysis/reports/q2_v3_k1_k2_dev.md", "analysis/reports/q2_v3_k0_engine_cache.md"
ITEMS.append(item("BLD-16", "BLD", "Kernel v3: engine cache, direction view, ledger-feature confidence, pooled-replicates regime", "done",
                  criterion="K0: cache rebuild reproduces v2 dev ledgers hash-for-hash and B4 stability; K1-K4 measured on dev with their "
                            "predictions judged; v3 pre-registered, frozen and read held out once",
                  evidence=["kernel/cache.py", "kernel/harness.py", "kernel/experiment.py", "kernel/v3.py", "kernel/claim_features.py",
                            "plans/v3_prereg.json", "plans/v3_freeze.json", "manifests/evidence/v3_prereg_2026-10-15.sha256",
                            _V3 + "k0_check_v2_semantic.json", _V3 + "k0_check_v2_formula.json", _V3 + "k0_check_b4_semantic.json",
                            _V3 + "v3_test.json", _V3 + "access_log.jsonl", _V3K0, _V3D, _V3R],
                  checks=[J(_V3 + "k0_check_v2_semantic.json", ["pass"], "true"), J(_V3 + "k0_check_v2_formula.json", ["pass"], "true"),
                          J(_V3 + "k0_check_b4_semantic.json", ["pass"], "true"),
                          {"t": "manifest", "path": "manifests/evidence/v3_prereg_2026-10-15.sha256"},
                          J(_V3 + "v3_test.json", ["freeze"], "eq", "0cda331ea81cf0dd")],
                  note="K0: 1,250/1,250 v2 dev ledgers rebuilt hash-for-hash from cache; a dev experiment now takes ~10 s per family "
                       "(30-70 min in v2). K1 link-recovery levers fail on dev (recovered links 33% precise; GES penalty 0.5 lowers F1); "
                       "floor measured (9.0% / 6.8% of true links have no usable signal). K2 weights refuted as a landmark lever. "
                       "v3 = v2 ledger + direction view (Meek R1/R3 not acted on) + feature confidence model; held out (second read): "
                       "ER-2 met for formula (D 0.908 [0.876], DxR 0.911 [0.863]), not semantic (D 0.830 [0.783], DxR 0.866 [0.799]); "
                       "ECE 0.021-0.026, ER-3 not met (upper ends 0.051-0.074)."))
_P18 = {
    "TGT-18": dict(note="v2 (B4, first read): semantic 0.812 [0.756], formula 0.899 [0.854]. v3 (second read, 125 files per family): "
                        "semantic 0.830 [0.783], formula 0.908 [0.876] (met for formula); pooled 5,000 rows: semantic 0.866 [0.799] "
                        "(short by 0.001), formula 0.911 [0.863]. Not met: semantic's lower end is below 0.80 in both regimes. "
                        "Semantic is capped by missed links (analysis/reports/q2_v3_k1_k2_dev.md section 3)."),
    "TGT-19": dict(note="Measured, not met (v2). v3 dev: route A still ties GES even with 5,000 rows (C3 0.551 vs GES 0.559, semantic "
                        "pooled); a lower GES penalty lowers F1 (0.522 -> 0.466). Route B: Meek propagation from knowledge adds "
                        "+0.001; the oracle ceiling of the orient-only rule is +0.060 / +0.044. Needs direction evidence beyond the "
                        "equivalence class (v4)."),
    "CAP-07": dict(note="v3 confidence model (ledger features, isotonic on cross-fitted scores): held-out ECE 0.021 semantic / 0.025 "
                        "formula (v2 0.057 / 0.036); realised >= claimed at every threshold in D; ER-3 not met because the ECE "
                        "upper ends (0.063 / 0.051) exceed 0.05 on 25 scenario clusters."),
    "CAP-11": dict(note="50/50 repeat builds give the same ledger hash (B1 R3) within one host. Across hosts the hash needs the "
                        "OpenBLAS kernel family pinned (OPENBLAS_CORETYPE=SKYLAKEX, threads 1): without it every p-value moves in the "
                        "14th digit (found by K0, 15 Oct); kernel/cache.py keys on both."),
}
for _i in ITEMS:
    if _i["id"] in _P18:
        _i.update({k: v for k, v in _P18[_i["id"]].items() if v is not None})
        if _i["id"] in ("TGT-18", "CAP-07"):
            _i["evidence"] = list(_i["evidence"]) + [_V3 + "v3_test.json", _V3R]
        if _i["id"] == "TGT-19":
            _i["evidence"] = list(_i["evidence"]) + [_V3D]
        if _i["id"] == "CAP-11":
            _i["evidence"] = list(_i["evidence"]) + [_V3K0, "kernel/cache.py"]
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p18 applied to catalogue.py")
g = ROOT / ".gitignore"
t = g.read_text(encoding="utf-8")
if "/cache/" not in t:
    t = t.replace("/queue/\n", "/queue/\n/cache/\n", 1) if "/queue/\n" in t else t + "\n/cache/\n"
    g.write_text(t, encoding="utf-8")
    print(".gitignore: /cache/ (the engine cache, ~30 KB per table, rebuilt by kernel.harness fill)")
