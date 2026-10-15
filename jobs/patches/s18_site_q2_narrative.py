"""2026-10-15: the site's narrative pages after the Q2 build. s17 updated the status and theses pages; the home page and the
Level 4 bundles board still described the ledger as not yet built. Home gains a "What the build showed" block and a current
"Where this is heading"; the bundles board's footer says what is done. Numbers only through site/registry.py (q2.* keys from
s17). Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "site"

h = S / "pgs" / "pg_home.py"
s = h.read_text(encoding="utf-8")
assert "What the build showed" not in s, "already applied"
old = '''latest = (SNAP.get("changes") or [{}])[0]'''
new = '''build = ul([
    f"<b>The ledger never falls below its data, held out.</b> Against plain PC with maxP it gains {n('q2.erf.sem.f1', '{:+.3f}')} "
    f"(semantic) and {n('q2.erf.for.f1', '{:+.3f}')} (formula) directed F1 and its committed claims are more often right "
    f"({n('q2.erf.sem.dv', '{:+.3f}')} / {n('q2.erf.for.dv', '{:+.3f}')} DV-1 precision); it ties GES on F1 "
    f"({n('q2.ges.sem.f1', '{:+.3f}')} / {n('q2.ges.for.f1', '{:+.3f}')}). {link('status', 'Page 10')}",
    f"<b>Provenance holds on every held-out file.</b> Neutral names leave the ledger unchanged on {n('q2.b3.sem.neutral')}/{t('q2.b3.sem.files')} "
    f"and {n('q2.b3.for.neutral')}/{t('q2.b3.for.files')} files; wrong names cost at most the proven bound on every file; every claim "
    f"re-derives from its evidence. Real names add {n('q2.b3.sem.gain', '{:+.3f}')} / {n('q2.b3.for.gain', '{:+.3f}')}, below the bar of 0.03. "
    f"{link('theses', 'Page 8')}",
    f"<b>Calibrated confidence beats raw bootstrap shares.</b> Calibration error {n('q2.b4.sem.ece')} / {n('q2.b4.for.ece')} against "
    f"{n('q2.b4.sem.raw')} / {n('q2.b4.for.raw')} raw; precision of the half-coverage view {n('q2.b4.sem.prec')} / {n('q2.b4.for.prec')}. "
    f"The 0.80 and 0.05 bars are cleared on formula and missed on semantic.",
    f"<b>Root cause analysis runs through the ledger.</b> Declared topology as knowledge reproduces the audit's number exactly: "
    f"AC@3 {n('q2.b5.ac3')} at coverage {n('q2.b5.cov')}, against {n('q2.b5.learned')} for the learned graph alone; {n('q2.b5.answered')} "
    f"issues keep the interval's lower end at {n('q2.b5.ac3.lo')}. {link('rca', 'Page 7')}",
])

latest = (SNAP.get("changes") or [{}])[0]'''
assert s.count(old) == 1
s = s.replace(old, new)
old2 = s[s.index('    H2("Where this is heading"),'):s.index('    latest_html,')]
new2 = '''    H2("What the build showed (Q2, first pass)"),
    build,
    H2("Where this is heading"),
    box(f'<p class="prose" style="margin: 0">The evidence points to a product: an independent audit of the causal claims other '
        f'people\\'s AI agents make, starting with incident root cause analysis. The desk research on that market is on '
        f'{link("market", "page 9")}. The claim ledger is now built and tested in gated steps: of the seven landmarks set in advance, the '
        f'floors, provenance and the physical-truth row are met; precision at half coverage, calibration, accuracy above GES and '
        f'root-cause accuracy at 0.90 are measured and not yet met ({t("q2.paper.met")} of 5 paper constraints, {t("q2.wedge.met")} of 5 '
        f'for the product). {link("status", "Page 10")} has the table; {link("theses", "Page 8")} the claims. The next step is '
        f'choosing which landmark a second version of the ledger chases, each under its own pre-registration.</p>', tone="blue"),
'''
s = s.replace(old2, new2)
h.write_text(s, encoding="utf-8")
print("pg_home: build findings and heading updated")

b = S / "levels" / "bundles.py"
s = b.read_text(encoding="utf-8")
old = s[s.index('    footer("%d of %d Q1 bundles and %d of %d audit bundles are done.'):s.index('           "Stages.dc.html", "Zoom into one run"),')]
new = '''    footer("%d of %d Q1 bundles and %d of %d audit bundles are done; the audit chapter closed on 14 Oct (DEC-05). The Q2 build, six bundles B0-B5, "
           "was built and read held out on 15 Oct: the ledger kernel now exists and holds its invariants (status page)." % (
               sum(b["status"] == "done" for b in Q1B), len(Q1B), sum(b["status"] == "done" for b in AB), len(AB)),
           "choose which of the landmarks still open (accuracy above GES, semantic calibration, root-cause accuracy at 0.90) a second kernel version chases.",
'''
s = s.replace(old, new)
b.write_text(s, encoding="utf-8")
print("bundles: footer updated")
