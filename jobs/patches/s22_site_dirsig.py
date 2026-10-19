"""2026-10-16: after the direction-signal rounds (analysis/reports/q2_dirsig_dev.md), the Level 3 / Level 4 "next" line and
T3(c) no longer offer "direction evidence beyond GES" as an open v4 route: pairwise asymmetry carries no licence at 1,000
rows. Same length, no new numbers. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "site"
OLD = "and a v4 aimed at the semantic search gap or at direction evidence beyond GES."
NEW = "and a v4 aimed at links: missed and false links cause most wrong answers and most wrong directions."
for f in (S / "levels" / "bundles.py", S / "levels" / "theses.py"):
    s = f.read_text(encoding="utf-8")
    assert s.count(OLD) == 1, f.name
    f.write_text(s.replace(OLD, NEW), encoding="utf-8")
    print(f.relative_to(ROOT), "next line updated")
th = S / "levels" / "theses.py"
s = th.read_text(encoding="utf-8")
old = '''"lower GES penalty nor propagating knowledge gets there (analysis/reports/q2_v3_k1_k2_dev.md).")'''
assert s.count(old) == 1
s = s.replace(old, '''"lower GES penalty, propagating knowledge, nor pairwise asymmetry gets there (analysis/reports/q2_dirsig_dev.md).")''')
th.write_text(s, encoding="utf-8")
print("theses: T3(c) updated")
