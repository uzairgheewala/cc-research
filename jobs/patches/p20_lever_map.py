"""2026-10-15: the lever map (docs/design/q2_lever_map.md) and the headroom ladder (analysis/q2_headroom.py, results in
analysis/results/q2_v3/headroom_dev.json) join TGT-18 and TGT-19's evidence. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p19" in c, "apply p19 first"
assert "# ---- overrides p20" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p20 (2026-10-15): lever map and headroom ladder (dev)
_LM = ["docs/design/q2_lever_map.md", "analysis/q2_headroom.py", "analysis/results/q2_v3/headroom_dev.json"]
for _i in ITEMS:
    if _i["id"] in ("TGT-18", "TGT-19"):
        _i["evidence"] = list(_i["evidence"]) + [e for e in _LM if e not in _i["evidence"]]
'''
p.write_text(c + "\n", encoding="utf-8")
print("p20 applied")
