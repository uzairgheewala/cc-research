"""2026-10-16: collider-free direction signals, two pre-registered rounds on dev (analysis/reports/q2_dirsig_dev.md).
CAP-02 gets the measurement as its note and evidence (status unchanged: no licence); TGT-19 records that route A through
pairwise asymmetry is closed at 1,000 rows on CausalArena. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p20" in c, "apply p20 first"
assert "# ---- overrides p21" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p21 (2026-10-16): direction signals that do not depend on colliders (dirsig-1, dirsig-2; dev)
_DS = ["kernel/asym.py", "kernel/asym_cond.py", "tests/test_q2_asym.py", "tests/test_q2_asym_cond.py",
       "plans/dirsig_prereg.json", "plans/dirsig2_prereg.json", "manifests/evidence/dirsig_prereg_2026-10-16.sha256",
       "manifests/evidence/dirsig2_prereg_2026-10-16.sha256", "analysis/q2_dirsig.py", "analysis/q2_dirsig_diag.py",
       "analysis/q2_dirsig2.py", "analysis/results/q2_v3/dirsig_dev.json", "analysis/results/q2_v3/dirsig_diag_dev.json",
       "analysis/results/q2_v3/dirsig2_dev.json", "analysis/reports/q2_dirsig_dev.md", "docs/design/q2_lever_map.md"]
for _i in ITEMS:
    if _i["id"] == "CAP-02":
        _i["note"] = ("Measured 16 Oct (dev, two pre-registered rounds): nine collider-free direction signals (non-Gaussian, "
                      "additive-noise, regression-error, IGCI, heteroscedastic, conditional-distribution, and conditional "
                      "variants) are right 0.42-0.64 of the time on found links at 1,000 rows; no licence. Failure classes: "
                      "children with mass points (signals confidently wrong), children with several parents, mechanisms "
                      "outside every model. Lead: IGCI on pooled formula 0.86 on 153 links, to confirm on a fresh family.")
        _i["evidence"] = list(_i.get("evidence") or []) + [e for e in _DS if e not in (_i.get("evidence") or [])]
        _i["checks"] = list(_i.get("checks") or []) + [{"t": "manifest", "path": "manifests/evidence/dirsig_prereg_2026-10-16.sha256"},
                                                       {"t": "manifest", "path": "manifests/evidence/dirsig2_prereg_2026-10-16.sha256"}]
    if _i["id"] == "TGT-19":
        _i["note"] = _i["note"] + (" 16 Oct: route A through pairwise asymmetry is closed at 1,000 rows on CausalArena "
                                   "(analysis/reports/q2_dirsig_dev.md); open direction sources are interventions and knowledge.")
        _i["evidence"] = list(_i["evidence"]) + ["analysis/reports/q2_dirsig_dev.md"]
'''
p.write_text(c + "\n", encoding="utf-8")
print("p21 applied")
