"""AUD-45's title still said "two verticals"; AB-14 now covers a market map and three verticals (DAG v2). Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- additions p07" in c and "# ---- overrides p08" not in c
c = c.rstrip("\n") + '''
# ---- overrides p08 (2026-10-13): AUD-45 title follows DAG v2
for _i in ITEMS:
    if _i["id"] == "AUD-45":
        _i["title"] = "AB-14 Market map and three vertical briefs (RCA, marketing, pharma RWE), with public demand evidence"
'''
p.write_text(c + "\n", encoding="utf-8")
print("p08 applied")
