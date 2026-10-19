"""2026-10-15: the stage-by-stage anatomy (analysis/reports/q2_v3_anatomy.md and its two scripts/results) joins BLD-16's and
TGT-18's evidence; the dev report carries a correction to its section 3. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p18" in c, "apply p18 first"
assert "# ---- overrides p19" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p19 (2026-10-15): stage-by-stage anatomy of the ledger's losses (dev; corrects the dev report's blame table)
_AN = ["analysis/q2_anatomy.py", "analysis/q2_half_anatomy.py", "analysis/results/q2_v3/anatomy_dev.json",
       "analysis/results/q2_v3/half_anatomy_dev.json", "analysis/reports/q2_v3_anatomy.md"]
for _i in ITEMS:
    if _i["id"] in ("BLD-16", "TGT-18"):
        _i["evidence"] = list(_i["evidence"]) + [e for e in _AN if e not in _i["evidence"]]
'''
p.write_text(c + "\n", encoding="utf-8")
print("p19 applied")
