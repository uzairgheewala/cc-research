"""2026-10-15: prose that still said "the next step is choosing which landmark a second kernel version chases" after kernel
v3 was built and read. Status answer, the Level 3 gap box, T3(c), and the Level 3 / Level 4 footers now say what v3 found
and what the open choice is. Then status and theses back under the 1,800-word budget (shorter v3 wording, same numbers).
No new numbers. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "site"


def sub(path, pairs):
    s = path.read_text(encoding="utf-8")
    for old, new in pairs:
        assert s.count(old) == 1, (path.name, old[:60])
        s = s.replace(old, new)
    path.write_text(s, encoding="utf-8")
    print("%s: %d passage(s) updated" % (path.relative_to(ROOT), len(pairs)))


NEXT = ("choose between more scenarios (every open landmark is within one interval width of its bar) and a v4 aimed at the "
        "semantic search gap or at direction evidence beyond GES.")

sub(S / "pgs" / "pg_status.py", [(
    '''f"{cnt.get('done', 0)} of {len(items)} tracked items are done. The audit chapter is closed and the Q2 build has had its "
           f"first held-out pass: floors and provenance are met; precision, calibration, accuracy and RCA landmarks are not yet. "
           f"The next step is choosing which of those to chase with a second kernel version.",''',
    '''f"{cnt.get('done', 0)} of {len(items)} tracked items are done. The audit chapter is closed and the Q2 kernel has had two "
           f"held-out reads: floors and provenance are met, precision for formula only; calibration, accuracy above GES and RCA "
           f"at 0.90 are not.",''')])

sub(S / "levels" / "theses.py", [
    ('''"(a) and (b) now hold held out. (c) needs either a data-only gain over GES or a stronger knowledge source; candidates in "
            "docs/design/q2_kernel_v3_proposals.md.")''',
     '''"(a) and (b) now hold held out. (c) needs direction evidence beyond the equivalence class: kernel v3 found that neither a "
            "lower GES penalty nor propagating knowledge gets there (analysis/reports/q2_v3_k1_k2_dev.md).")'''),
    ('''<b>Choice:</b> which landmark a second kernel version chases first (docs/design/q2_kernel_v3_proposals.md).''',
     '''<b>Choice:</b> more scenarios, or a v4 on the semantic search gap (analysis/reports/q2_v3_heldout.md).'''),
    ('''"choose which landmark the second kernel version chases (accuracy above GES, calibration on semantic, or more RCA issues).",''',
     "NEXT,"),
])
th = S / "levels" / "theses.py"
s = th.read_text(encoding="utf-8")
s = s.replace("\nT4 = thesis(", "\nNEXT = %r\n\nT4 = thesis(" % NEXT, 1) if "\nNEXT = " not in s else s
th.write_text(s, encoding="utf-8")

sub(S / "levels" / "bundles.py", [(
    '''was built and read held out on 15 Oct: the ledger kernel now exists and holds its invariants (status page)." % (''',
    '''was built and read held out on 15 Oct, then read a second time as kernel v3: the ledger holds its invariants and meets "
           "the precision landmark for formula (status page)." % ('''), (
    '''"choose which of the landmarks still open (accuracy above GES, semantic calibration, root-cause accuracy at 0.90) a second kernel version chases.",''',
    repr(NEXT) + ","),
])

sub(S / "pgs" / "pg_status.py", [
    ('''P(f"Measured on dev: {n('q2v3.floor.sem', '{:.0%}')} / {n('q2v3.floor.for', '{:.0%}')} of true links (semantic / formula) "
      f"carry no usable signal at this sample size; a further {n('q2v3.gap.sem', '{:.0%}')} / {n('q2v3.gap.for', '{:.0%}')} are "
      f"a search gap no tested lever closed (analysis/reports/q2_v3_k1_k2_dev.md)."),''',
     '''P(f"On dev, {n('q2v3.floor.sem', '{:.0%}')} / {n('q2v3.floor.for', '{:.0%}')} of true links (semantic / formula) carry no "
      f"usable signal at 1,000 rows; {n('q2v3.gap.sem', '{:.0%}')} / {n('q2v3.gap.for', '{:.0%}')} more are a search gap no tested lever closed."),'''),
    ("ER-3 is not met in any row.", "ER-3 not met in any row."),
    ('''P("Bundles %s to %s are done; each result is in analysis/reports/q2_b&lt;k&gt;_*.md." % (q2[0]["id"], q2[-1]["id"]))''',
     '''P("%s-%s are done; results in analysis/reports/q2_b&lt;k&gt;_*.md." % (q2[0]["id"], q2[-1]["id"]))'''),
])
sub(S / "levels" / "theses.py", [(
    '''f"Kernel v3 (second read): a model on the ledger's own features brings calibration error to {n('q2v3.sem.D.ece')} semantic and "
             f"{n('q2v3.for.D.ece')} formula; realised precision is at or above the claim at every threshold, but the error's upper end "
             f"stays above 0.05 on 25 scenarios."''',
    '''f"Kernel v3 (second read): a model on ledger features brings calibration error to {n('q2v3.sem.D.ece')} / "
             f"{n('q2v3.for.D.ece')}; its upper end stays above 0.05 on 25 scenarios."''')])

# home "where this is heading" and T4's v3 bullet (found on the rendered re-read)
sub(S / "pgs" / "pg_home.py", [(
    '''the claims. The next step is '
        f'choosing which landmark a second version of the ledger chases, each under its own pre-registration.</p>''',
    '''the claims. A second version, '
        f'read once more held out, meets the precision landmark for formula but not semantic; the open choice is between more '
        f'scenarios to narrow every interval and a third version aimed at the links the search misses.</p>''')])
sub(S / "levels" / "theses.py", [(
    '''{n('q2v3.sem.D.ece')} / "
             f"{n('q2v3.for.D.ece')}; its upper end''',
    '''{n('q2v3.sem.D.ece')} / "
             f"{n('q2v3.for.D.ece')} (semantic / formula); its upper end''')])
