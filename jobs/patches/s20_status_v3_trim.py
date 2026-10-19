"""2026-10-15: s19's kernel v3 section put the status page at 1,953 words (budget 1,800). Same numbers, fewer words: the
regime goes in the family cell, intervals in brackets, the caption shrinks; the Q2 bundle table becomes one sentence
while every bundle is done (the tile above already counts them). Each part refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
st = ROOT / "site" / "pgs" / "pg_status.py"
s = st.read_text(encoding="utf-8")
assert "V3_TABLE" in s, "apply s19 first"
PART1 = "s20 trim" not in s
if PART1:
  old_row = s[s.index("def _v3row(fam, k, reg):"):s.index("Q2_BUNDLES = table(")]
  new_row = '''def _v3row(fam, k, reg):  # s20 trim
    return ["%s, %s" % (fam, {"D": "1,000 rows", "DxR": "5,000 rows (pooled)"}[reg]),
            f"{n('q2v3.%s.%s.p' % (k, reg))} [{n('q2v3.%s.%s.lo' % (k, reg))}]",
            f"{n('q2v3.%s.%s.ece' % (k, reg))} [{n('q2v3.%s.%s.ecehi' % (k, reg))}]", "<b>%s</b>" % t("q2v3.%s.%s.er2" % (k, reg))]


V3_TABLE = table(["Family, rows", "Precision at half coverage [lower end]", "Calibration error [upper end]", "ER-2"],
                 [_v3row(f, k, r) for f, k in (("semantic", "sem"), ("formula", "for")) for r in ("D", "DxR")],
                 caption="Second read of the test splits (analysis/reports/q2_v3_heldout.md). ER-3 is not met in any row.")

'''
  s = s.replace(old_row, new_row)

  i = s.index('    P(f"Every engine result is now cached')
  j = s.index("    V3_TABLE,", i)
  s = s[:i] + '''    P(f"Engine results are now cached, so an experiment takes seconds. On dev the ledger misses {n('q2v3.missed.sem', '{:.0%}')} / "
      f"{n('q2v3.missed.for', '{:.0%}')} of true links (semantic / formula): {n('q2v3.floor.sem', '{:.0%}')} / "
      f"{n('q2v3.floor.for', '{:.0%}')} carry no usable signal at this sample size, and {n('q2v3.gap.sem', '{:.0%}')} / "
      f"{n('q2v3.gap.for', '{:.0%}')} are a search gap no tested lever closed. v3 changes what is acted on, not the claims."),
''' + s[j:]
  print("pg_status: v3 section trimmed")

old = """    Q2_TABLE, Q2_BUNDLES,
    H3("Kernel v3: the same ledger, read more carefully"),"""
if old in s:
    s = s.replace(old, """    Q2_TABLE, (Q2_BUNDLES if any(b["status"] != "done" for b in q2) else
               P("Bundles %s to %s are done; each result is in analysis/reports/q2_b&lt;k&gt;_*.md." % (q2[0]["id"], q2[-1]["id"]))),
    H3("Kernel v3: the second held-out read"),""")
    print("pg_status: Q2 bundle table folds to a sentence while all are done")
old = '''v3 changes what is acted on, not the claims."),'''
if old in s:
    s = s.replace(old, '''"),''')
    s = s.replace("are a search gap no tested lever closed. ", "are a search gap no tested lever closed.")

i = s.find('    P(f"Engine results are now cached')
if i >= 0:
    j = s.index("    V3_TABLE,", i)
    s = s[:i] + '''    P(f"Measured on dev: {n('q2v3.floor.sem', '{:.0%}')} / {n('q2v3.floor.for', '{:.0%}')} of true links (semantic / formula) "
      f"carry no usable signal at this sample size; a further {n('q2v3.gap.sem', '{:.0%}')} / {n('q2v3.gap.for', '{:.0%}')} are "
      f"a search gap no tested lever closed (analysis/reports/q2_v3_k1_k2_dev.md)."),
''' + s[j:]
    s = s.replace('caption="Second read of the test splits (analysis/reports/q2_v3_heldout.md). ER-3 is not met in any row.")',
                  'caption="Second held-out read (analysis/reports/q2_v3_heldout.md); ER-3 is not met in any row.")')
    print("pg_status: v3 paragraph down to the floor and the search gap")
st.write_text(s, encoding="utf-8")
