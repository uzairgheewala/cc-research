"""2026-10-15: the site after the Q2 build's first held-out pass. Registry keys for every Q2 number; a Q2 section on the
status page (landmarks and bundles); theses T3 and T4, the invariant cells, the gap box and the footer of Level 3 brought
up to date. Numbers only through site/registry.py. Refuses to run twice."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "site"

# ---------------------------------------------------------------- registry
reg = S / "registry.py"
r = reg.read_text(encoding="utf-8")
assert "q2.erf.sem.f1" not in r, "already applied"
r = r.rstrip("\n") + '''

# ---- Q2 build, first held-out pass (2026-10-15; jobs/patches/s17_site_q2.py)
HO = R + "q2_b1/heldout.json"
B2S, B3S, B4E = R + "q2_b2/summary_test.json", R + "q2_b3/summary_test.json", R + "q2_b4/evaluate_test.json"
RV, B5T, AD, LM = R + "q2_b4/raw_vs_calibrated_test.json", R + "q2_b5/rca_test.json", R + "q2_b5/adapters.json", R + "q2_landmarks.json"
_q2 = {}
for _f, _k in (("semantic", "sem"), ("formula", "for")):
    for _vs, _p in (("vs_pc_maxp", "erf"), ("vs_ges", "ges")):
        for _e in ("point", "lo", "hi"):
            _s = "" if _e == "point" else "." + _e
            _q2["q2.%s.%s.f1%s" % (_p, _k, _s)] = J(HO, "families", _f, _vs, "f1_diff", _e)
            _q2["q2.%s.%s.dv%s" % (_p, _k, _s)] = J(HO, "families", _f, _vs, "dv1_pooled_diff", _e)
    _q2["q2.b2.%s.dv" % _k] = J(B2S, "families", _f, "dv1_pooled_diff", "point")
    _q2["q2.b2.%s.dv.lo" % _k] = J(B2S, "families", _f, "dv1_pooled_diff", "lo")
    _q2["q2.b2.%s.perfile" % _k] = J(B2S, "families", _f, "dv1_mean_per_file_diff")
    for _e in ("point", "lo", "hi"):
        _q2["q2.b3.%s.gain%s" % (_k, "" if _e == "point" else "." + _e)] = J(B3S, "families", _f, "arms", "real", "gain", _e)
    _q2["q2.b3.%s.files" % _k] = J(B3S, "families", _f, "arms", "neutral", "files")
    _q2["q2.b3.%s.neutral" % _k] = J(B3S, "families", _f, "arms", "neutral", "claims_identical_to_D")
    _q2["q2.b3.%s.t3" % _k] = J(B3S, "families", _f, "arms", "moved", "within_t3")
    _q2["q2.b3.%s.moved" % _k] = J(B3S, "families", _f, "arms", "moved", "gain", "point")
    for _e in ("point", "lo", "hi"):
        _q2["q2.b4.%s.prec%s" % (_k, "" if _e == "point" else "." + _e)] = J(B4E, "families", _f, "dv", "er2_interval", _e)
    _q2["q2.b4.%s.cov" % _k] = J(B4E, "families", _f, "dv", "selective_at_half_coverage", "coverage")
    _q2["q2.b4.%s.ece" % _k] = J(B4E, "families", _f, "dv", "ece")
    _q2["q2.b4.%s.ece.hi" % _k] = J(B4E, "families", _f, "dv", "ece_interval", "hi")
    _q2["q2.b4.%s.raw" % _k] = J(RV, "families", _f, "dv", "ece_raw", "point")
_CH = "chambers", "rows"
_q2.update({
    "q2.ch.kdi": J(B2S, *_CH, "kernel D+I (C3)", "precision"), "q2.ch.kd": J(B2S, *_CH, "kernel D (C3)", "precision"),
    "q2.ch.ges": J(B2S, *_CH, "GES (BIC)", "precision"), "q2.ch.pc": J(B2S, *_CH, "PC maxP (plain call)", "precision"),
    "q2.ch.agree": J(B2S, *_CH, "kernel D+I (C3)", "agreement_with_check_rows"),
    "q2.ch.true.agree": J(B2S, *_CH, "true DAG", "agreement_with_check_rows"),
    "q2.b5.ac3": J(B5T, "ER-4b", "AC@3_answered"), "q2.b5.ac3.lo": J(B5T, "ER-4b", "lo"), "q2.b5.cov": J(B5T, "ER-4b", "coverage"),
    "q2.b5.answered": J(B5T, "ER-4b", "answered"),
    "q2.b5.learned": J(B5T, "variants", "learned_ledger_only", "AC@3_answered"),
    "q2.b5.learned.cov": J(B5T, "variants", "learned_ledger_only", "coverage"),
    "q2.b5.cc.created": J(AD, "agents", "causal_copilot_gpt4o", "violations", "knowledge_created_connection"),
    "q2.b5.matmcd.reversed": J(AD, "agents", "matmcd", "violations", "knowledge_reversed_data"),
    "q2.paper.met": F(LM, lambda d: len(d["paper_constraints_met"])),
    "q2.wedge.met": F(LM, lambda d: len(d["wedge_constraints_met"])),
})
for _er in ("ER-F", "ER-1", "ER-2", "ER-3", "ER-4a", "ER-4b", "ER-C"):
    _q2["q2.lm." + _er] = F(LM, lambda d, _er=_er: "met" if d["landmarks"][_er]["met"] else "not met")
REG.update(_q2)
'''
reg.write_text(r + "\n", encoding="utf-8")
print("registry: Q2 keys added")

# ---------------------------------------------------------------- status page
st = S / "pgs" / "pg_status.py"
s = st.read_text(encoding="utf-8")
old = "q1 = [b for b in SNAP[\"bundles\"] if b.get(\"plan\", \"q1\") == \"q1\"]\n"
assert s.count(old) == 1
s = s.replace(old, old + "q2 = [b for b in SNAP[\"bundles\"] if b.get(\"plan\") == \"q2\"]\n")
old_t = '''              tile("%d / %d" % (sum(b["status"] == "done" for b in q1), len(q1)), "Q1 bundles done")], min_w=180)'''
assert s.count(old_t) == 1
s = s.replace(old_t, '''              tile("%d / %d" % (sum(b["status"] == "done" for b in q1), len(q1)), "Q1 bundles done"),
              tile("%d / %d" % (sum(b["status"] == "done" for b in q2), len(q2)), "Q2 build bundles done")], min_w=180)''')
s = s.replace('''

def you(h):''', '''

def _lm(er, what, value, rule):
    return [er, what, value, rule, "<b>%s</b>" % t("q2.lm." + er)]


Q2_TABLE = table(["", "Landmark", "Held-out value", "Rule (conservative end of the 95% interval)", "Verdict"], [
    _lm("ER-F", "Floors: never below plain PC with maxP",
        f"F1 {n('q2.erf.sem.f1', '{:+.3f}')} / {n('q2.erf.for.f1', '{:+.3f}')}; DV-1 {n('q2.erf.sem.dv', '{:+.3f}')} / {n('q2.erf.for.dv', '{:+.3f}')}",
        "lower ends >= -0.01, both families"),
    _lm("ER-1", "Provenance and invariance",
        f"neutral names = D on {n('q2.b3.sem.neutral')}/{t('q2.b3.sem.files')} and {n('q2.b3.for.neutral')}/{t('q2.b3.for.files')}; "
        f"moved names within T3 on {n('q2.b3.sem.t3')} and {n('q2.b3.for.t3')}",
        "100% of held-out files; every ledger verifies"),
    _lm("ER-2", "DV-1 precision at half coverage",
        f"{n('q2.b4.sem.prec')} [{n('q2.b4.sem.prec.lo')}, {n('q2.b4.sem.prec.hi')}] / {n('q2.b4.for.prec')} [{n('q2.b4.for.prec.lo')}, {n('q2.b4.for.prec.hi')}]",
        "lower end > 0.80, both families"),
    _lm("ER-3", "Calibration",
        f"ECE {n('q2.b4.sem.ece')} / {n('q2.b4.for.ece')} (raw {n('q2.b4.sem.raw')} / {n('q2.b4.for.raw')})",
        "ECE upper end <= 0.05; realised >= claimed - 0.03"),
    _lm("ER-4a", "Accuracy: route A (F1 above GES) or B (tiers > 0.03)",
        f"A: {n('q2.ges.sem.f1', '{:+.3f}')} / {n('q2.ges.for.f1', '{:+.3f}')}; B: {n('q2.b3.sem.gain', '{:+.3f}')} [{n('q2.b3.sem.gain.lo', '{:+.3f}')}] / "
        f"{n('q2.b3.for.gain', '{:+.3f}')} [{n('q2.b3.for.gain.lo', '{:+.3f}')}]",
        "A: lower end > 0; B: lower end > 0.03"),
    _lm("ER-4b", "RCA through the ledger (PetShop)",
        f"AC@3 {n('q2.b5.ac3')} at coverage {n('q2.b5.cov')}; lower end {n('q2.b5.ac3.lo')} ({n('q2.b5.answered')} answered issues)",
        "lower end >= 0.90 at coverage >= 0.5"),
    _lm("ER-C", "Causal Chambers (report)",
        f"kernel {n('q2.ch.kdi')} vs GES {n('q2.ch.ges')}, PC maxP {n('q2.ch.pc')}",
        "within 0.03 of GES"),
], caption="Semantic / formula where two values are given. Each bundle was frozen before its single held-out read "
           "(analysis/reports/q2_build_results.md).")

Q2_BUNDLES = table(["Bundle", "Title", "Status", "Result"],
                   [[b["id"], b["title"], b["status"].replace("_", " "), b["note"]] for b in q2], mono_cols=(0,))


def you(h):''')
old_b = '''    you(L4.audit_intro), you(L4.audit_host),'''
assert s.count(old_b) == 1
s = s.replace(old_b, '''    H2("Q2 build: the landmarks after the first held-out pass"),
    P(f"The paper needs ER-F, ER-1, ER-2, ER-3 and ER-4a; the wedge needs ER-F, ER-1, ER-2, ER-3 and ER-4b. After one held-out "
      f"read per bundle, {t('q2.paper.met')} of 5 paper constraints and {t('q2.wedge.met')} of 5 wedge constraints are met."),
    Q2_TABLE, Q2_BUNDLES,
''' + old_b)
old_a = '''    answer(f"{cnt.get('done', 0)} of {len(items)} tracked items are done. The audits that remain wait on live runs that are under way "
           f"and, when a chance arises, interviews. The next decision is the wedge (AB-16): which results carry the paper, and when "
           f"the ledger kernel starts.",'''
assert s.count(old_a) == 1
s = s.replace(old_a, '''    answer(f"{cnt.get('done', 0)} of {len(items)} tracked items are done. The audit chapter is closed and the Q2 build has had its "
           f"first held-out pass: floors and provenance are met; precision, calibration, accuracy and RCA landmarks are not yet. "
           f"The next step is choosing which of those to chase with a second kernel version.",''')
st.write_text(s, encoding="utf-8")
print("pg_status: Q2 section added")

# ---------------------------------------------------------------- Level 3 theses
th = S / "levels" / "theses.py"
s = th.read_text(encoding="utf-8")
rep = [
    ('''            "In progress", "prog",
            [f"Refinement v1 (BND-10''', '''            "(a) and (b) supported; (c) not met", "prog",
            [f"Refinement v1 (BND-10'''),
    ('''             "The claim ledger itself (BLD-02, kernel B1) is not started and has no Q1 bundle."],''',
     '''             f"Ledger kernel (Q2 B1, rule C3), held out: directed F1 against plain PC with maxP {n('q2.erf.sem.f1', '{:+.3f}')} / {n('q2.erf.for.f1', '{:+.3f}')} "
             f"(semantic / formula), against GES {n('q2.ges.sem.f1', '{:+.3f}')} / {n('q2.ges.for.f1', '{:+.3f}')}.",
             f"Tiers on open pairs only (Q2 B3): neutral names equal the data-only ledger on {n('q2.b3.sem.neutral')}/{t('q2.b3.sem.files')} and "
             f"{n('q2.b3.for.neutral')}/{t('q2.b3.for.files')} held-out files; moved names stay within the T3 bound on every file; real names add "
             f"{n('q2.b3.sem.gain', '{:+.3f}')} / {n('q2.b3.for.gain', '{:+.3f}')}, below the published bests."],'''),
    ('''            "B0, then B1, the data-only kernel (DEC-05 chose option B). B1's held-out gate: no more than 0.01 below plain PC with maxP "
            "on the test splits (plans/q2_build_prereg.json).")''',
     '''            "(a) and (b) now hold held out. (c) needs either a data-only gain over GES or a stronger knowledge source; candidates in "
            "docs/design/q2_kernel_v3_proposals.md.")'''),
    ('''            "Not started", "todo",
            ["Calibration method chosen (DOM-08): Platt scaling on bootstrap frequencies, fitted with whole scenarios held out; Brier score primary.",
             "Causal-Copilot's bootstrap filter uses raw bootstrap frequencies with no calibration: the baseline to beat."],''',
     '''            "Supported against raw frequencies; gate missed on one family", "prog",
            [f"Q2 B4, held out: calibrated error {n('q2.b4.sem.ece')} semantic and {n('q2.b4.for.ece')} formula, against {n('q2.b4.sem.raw')} and "
             f"{n('q2.b4.for.raw')} for raw bootstrap frequencies (the baseline Causal-Copilot's filter uses). The refutation test fails: calibration beats raw.",
             "The independent checker (K7) accepts every claim in every ledger built in B1-B3.",
             f"The pre-registered 0.05 gate is missed on semantic, in the safe direction (claims are right more often than stated). "
             f"Half-coverage precision {n('q2.b4.sem.prec')} semantic, {n('q2.b4.for.prec')} formula.",
             "B4 pre-registered an isotonic map on 10-resample stability, fitted on dev and frozen before the read (DOM-08 had proposed Platt scaling)."],'''),
    ('''            "B4 after B1; coverage guarantee within one family only.")''',
     '''            "scenario-level shrinkage of the map and more scenarios; the coverage guarantee stays within one family.")'''),
    ('''    ("I1", "Shuffling columns changes nothing", "Violated: the vendored PC changes its output in %s of %s files (BND-06)" % (n("pc.order.changed"), n("pc.order.files")), "dec", "a gate on every run"),
    ("I2", "Same inputs, same ledger hash", "Not measured", "todo", "CAP-11"),
    ("I3", "D+K with no knowledge equals D", "Not built", "todo", "gives T3(a)"),
    ("I4", "No claim without evidence; the checker accepts every claim", "Not built", "todo", "CAP-09"),''',
     '''    ("I1", "Shuffling columns changes nothing", "Holds for the ledger (50/50 dev files, 120/120 oracle graphs). The vendored PC changes its output in %s of %s files (BND-06)" % (n("pc.order.changed"), n("pc.order.files")), "done", "a gate on every run"),
    ("I2", "Same inputs, same ledger hash", "Holds: 50/50 repeat builds (Q2 B1)", "done", "CAP-11"),
    ("I3", "D+K with no knowledge equals D", "Holds held out: %s/%s and %s/%s files (Q2 B3)" % (n("q2.b3.sem.neutral"), t("q2.b3.sem.files"), n("q2.b3.for.neutral"), t("q2.b3.for.files")), "done", "gives T3(a)"),
    ("I4", "No claim without evidence; the checker accepts every claim", "Holds: every claim cites records and K7 re-derives it (Q2 B1-B3)", "done", "CAP-09"),'''),
    ('''    ("I5", "Knowledge never creates or removes a connection", "v1 violated it (dropped %s). v2 enforces it by construction (tests/test_refinement_v2.py)" % n("v1.dropped.all"), "prog", "gives T3(b)"),
    ("I6", "An intervention beats knowledge", "Not built", "todo", "needs B2"),''',
     '''    ("I5", "Knowledge never creates or removes a connection", "v1 violated it (dropped %s). The ledger enforces it by construction; the skeleton never moved in any B3 arm" % n("v1.dropped.all"), "done", "gives T3(b)"),
    ("I6", "An intervention beats knowledge", "Built (Q2 B2): an intervention overrides a data or knowledge direction and the claim records the conflict", "done", "CAP-03"),'''),
]
for a, b in rep:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
m = re.search(r'gap_box = f""".*?</div>"""\n', s, re.S)
assert m
s = s.replace(m.group(0), '''gap_box = f"""<div style="flex: 1 1 380px; padding: 18px 20px; background: #FFFFFF; border: 2px dashed #8E2A2A; border-radius: 10px; display: flex; flex-direction: column; gap: 8px">
{tag("The gap this level exposes", "#8E2A2A")}
<p style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px; font-weight: 600">The ledger exists and holds its promises; it does not yet beat the field's best numbers.</p>
<p style="margin: 0; font-size: 14px; line-height: 20px">After the Q2 build's first held-out pass, {t("q2.paper.met")} of 5 paper constraints are met (floors, provenance). Precision at half coverage, calibration, accuracy above GES and RCA at 0.90 are not yet: P1 is {_share["P1"]:.0f}% done, P2 {_share["P2"]:.0f}%, P3 {_share["P3"]:.0f}%.</p>
<p style="margin: 0; font-size: 14px; line-height: 20px"><b>Choice:</b> which landmark a second kernel version chases first (docs/design/q2_kernel_v3_proposals.md).</p>
</div>"""
''')
m = re.search(r'    footer\("measurement is mostly done.*?"Bundles\.dc\.html", "See the bundles"\),\n', s, re.S)
assert m
s = s.replace(m.group(0), '''    footer("measurement is done and corrected one thesis (T1 holds for PC, not for GES or FCI). The ledger is built: T3(a) and (b) hold "
           "held out, and T4 beats raw frequencies but misses its own gate on one family.",
           "choose which landmark the second kernel version chases (accuracy above GES, calibration on semantic, or more RCA issues).",
           "Bundles.dc.html", "See the bundles"),
''')
th.write_text(s, encoding="utf-8")
print("theses: T3, T4, invariants, gap box, footer updated")
