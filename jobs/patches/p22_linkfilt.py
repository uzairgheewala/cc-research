"""2026-10-16: link filters L8 (triangle order) and L7 (resampling stability), pre-registered and measured on dev
(analysis/reports/q2_linkfilt_dev.md). TGT-18 gets the report and a manifest check; its note records that both filters
are licensed on formula only and cannot act until an applicability condition exists (lever-map row L16). Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p21" in c, "apply p21 first"
assert "# ---- overrides p22" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p22 (2026-10-16): link filters L8 / L7 (linkfilt-1; dev)
_LF = ["kernel/linkfilt.py", "tests/test_q2_linkfilt.py", "plans/linkfilt_prereg.json",
       "manifests/evidence/linkfilt_prereg_2026-10-16.sha256", "analysis/q2_linkfilt.py", "analysis/q2_linkfilt_diag.py",
       "analysis/results/q2_v3/linkfilt_dev.json", "analysis/results/q2_v3/linkfilt_diag_dev.json", "analysis/reports/q2_linkfilt_dev.md"]
for _i in ITEMS:
    if _i["id"] == "TGT-18":
        _i["evidence"] = list(_i["evidence"]) + [e for e in _LF if e not in _i["evidence"]]
        _i["checks"] = list(_i.get("checks") or []) + [{"t": "manifest", "path": "manifests/evidence/linkfilt_prereg_2026-10-16.sha256"}]
        _i["note"] = _i["note"] + (" 16 Oct (dev): two link filters (triangle order, resampling stability) earn a licence on formula "
                                   "(cut precision 0.81; 25% / 38% of false links cut) and not on semantic, where 55% of true links "
                                   "sit beside a real mediated path; neither can act until an applicability condition exists "
                                   "(analysis/reports/q2_linkfilt_dev.md).")
'''
p.write_text(c + "\n", encoding="utf-8")
print("p22 applied")
