"""2026-10-15: the site after kernel v3. Registry keys for the v3 held-out read and the measured floor; a v3 table on the
status page; one home-page finding; T4's evidence. Numbers only through site/registry.py. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "site"

reg = S / "registry.py"
r = reg.read_text(encoding="utf-8")
assert "q2v3.sem.D.p" not in r, "already applied"
r = r.rstrip("\n") + '''

# ---- kernel v3 (2026-10-15; jobs/patches/s19_site_v3.py)
V3T = R + "q2_v3/v3_test.json"
FLS, FLF = R + "q2_v3/floor_dev_semantic.json", R + "q2_v3/floor_dev_formula.json"
K0S = R + "q2_v3/k0_check_v2_semantic.json"
_v3 = {}
for _f, _k in (("semantic", "sem"), ("formula", "for")):
    for _r in ("D", "DxR"):
        _v3["q2v3.%s.%s.p" % (_k, _r)] = J(V3T, "families", _f, _r, "precision_half")
        _v3["q2v3.%s.%s.lo" % (_k, _r)] = J(V3T, "families", _f, _r, "er2_interval", "lo")
        _v3["q2v3.%s.%s.cov" % (_k, _r)] = J(V3T, "families", _f, _r, "coverage_half")
        _v3["q2v3.%s.%s.ece" % (_k, _r)] = J(V3T, "families", _f, _r, "ece")
        _v3["q2v3.%s.%s.ecehi" % (_k, _r)] = J(V3T, "families", _f, _r, "ece_interval", "hi")
        _v3["q2v3.%s.%s.er2" % (_k, _r)] = F(V3T, lambda d, _f=_f, _r=_r: "met" if d["families"][_f][_r]["ER-2_met"] else "not met")
_v3.update({
    "q2v3.floor.sem": J(FLS, "classes", "floor", "share_of_true_links"), "q2v3.floor.for": J(FLF, "classes", "floor", "share_of_true_links"),
    "q2v3.missed.sem": J(FLS, "missed_share"), "q2v3.missed.for": J(FLF, "missed_share"),
    "q2v3.gap.sem": J(FLS, "classes", "method_linear", "share_of_true_links"), "q2v3.gap.for": J(FLF, "classes", "method_linear", "share_of_true_links"),
    "q2v3.k0.equal": J(K0S, "row_hashes_equal"),
})
REG.update(_v3)
'''
reg.write_text(r + "\n", encoding="utf-8")
print("registry: v3 keys added")

st = S / "pgs" / "pg_status.py"
s = st.read_text(encoding="utf-8")
old = '''Q2_BUNDLES = table('''
assert s.count(old) == 1
s = s.replace(old, '''def _v3row(fam, k, reg):
    return [fam, {"D": "1,000 rows (one file)", "DxR": "5,000 rows (five replicates pooled)"}[reg],
            f"{n('q2v3.%s.%s.p' % (k, reg))} (lower end {n('q2v3.%s.%s.lo' % (k, reg))}) at coverage {n('q2v3.%s.%s.cov' % (k, reg))}",
            f"{n('q2v3.%s.%s.ece' % (k, reg))} (upper end {n('q2v3.%s.%s.ecehi' % (k, reg))})", "<b>%s</b>" % t("q2v3.%s.%s.er2" % (k, reg))]


V3_TABLE = table(["Family", "Rows per table", "Precision at half coverage", "Calibration error", "ER-2"],
                 [_v3row(f, k, r) for f, k in (("semantic", "sem"), ("formula", "for")) for r in ("D", "DxR")],
                 caption="Kernel v3 (analysis/reports/q2_v3_heldout.md): the same ledger, with the weakest directions (Meek rule 1) not "
                         "acted on and a confidence model on the ledger's own features. Second read of the test splits; ER-3 is not met in "
                         "any row (calibration-error upper ends above 0.05 on 25 scenarios).")

''' + old)
old2 = '''    Q2_TABLE, Q2_BUNDLES,
'''
assert s.count(old2) == 1
s = s.replace(old2, '''    Q2_TABLE, Q2_BUNDLES,
    H3("Kernel v3: the same ledger, read more carefully"),
    P(f"Every engine result is now cached: v2's dev ledgers rebuild hash-for-hash ({n('q2v3.k0.equal')} of 625 per family), "
      f"so an experiment takes seconds instead of an hour. The floor is measured: of the true links the ledger misses "
      f"({n('q2v3.missed.sem', '{:.0%}')} semantic, {n('q2v3.missed.for', '{:.0%}')} formula), {n('q2v3.floor.sem', '{:.0%}')} and "
      f"{n('q2v3.floor.for', '{:.0%}')} of all true links leave no usable signal at this sample size; a further "
      f"{n('q2v3.gap.sem', '{:.0%}')} and {n('q2v3.gap.for', '{:.0%}')} are a search gap no tested lever closed without losing more precision."),
    V3_TABLE,
''')
st.write_text(s, encoding="utf-8")
print("pg_status: v3 section added")

h = S / "pgs" / "pg_home.py"
s = h.read_text(encoding="utf-8")
old = '''    f"issues keep the interval's lower end at {n('q2.b5.ac3.lo')}. {link('rca', 'Page 7')}",
])'''
assert s.count(old) == 1
s = s.replace(old, '''    f"issues keep the interval's lower end at {n('q2.b5.ac3.lo')}. {link('rca', 'Page 7')}",
    f"<b>Kernel v3 reads the same ledger more carefully.</b> Not acting on the weakest directions and scoring each answer from "
    f"the ledger's own features: formula answers are {n('q2v3.for.D.p')} precise at half coverage (lower end "
    f"{n('q2v3.for.D.lo')}, landmark met); semantic {n('q2v3.sem.D.p')}, capped by links the data cannot show "
    f"({n('q2v3.floor.sem', '{:.0%}')} of true links leave no usable signal). {link('status', 'Page 10')}",
])''')
h.write_text(s, encoding="utf-8")
print("pg_home: v3 finding added")

th = S / "levels" / "theses.py"
s = th.read_text(encoding="utf-8")
old = '''             "B4 pre-registered an isotonic map on 10-resample stability, fitted on dev and frozen before the read (DOM-08 had proposed Platt scaling)."],'''
assert s.count(old) == 1
s = s.replace(old, '''             "B4 pre-registered an isotonic map on 10-resample stability, fitted on dev and frozen before the read (DOM-08 had proposed Platt scaling).",
             f"Kernel v3 (second read): a model on the ledger's own features brings calibration error to {n('q2v3.sem.D.ece')} semantic and "
             f"{n('q2v3.for.D.ece')} formula; realised precision is at or above the claim at every threshold, but the error's upper end "
             f"stays above 0.05 on 25 scenarios."],''')
th.write_text(s, encoding="utf-8")
print("theses: T4 evidence updated")
