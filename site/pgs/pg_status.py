"""Page 10: plan and status, generated from the snapshot (bundles, queue, gates). Day-to-day work lives in the Slack lists."""
from pagekit import *  # noqa: F401,F403
import bundles as L4
import theses as L3

SNAP = __import__("common").SNAP
items = SNAP["items"]
cnt = {}
for i in items:
    cnt[i["status"]] = cnt.get(i["status"], 0) + 1
ab = [b for b in SNAP["bundles"] if b.get("plan") == "audit"]
q1 = [b for b in SNAP["bundles"] if b.get("plan", "q1") == "q1"]
q2 = [b for b in SNAP["bundles"] if b.get("plan") == "q2"]


def tile(num, label_):
    return (f'<div style="padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">'
            f'<div style="font-family: {COND}; font-size: 34px; line-height: 38px; font-weight: 700">{num}</div>'
            f'<div style="font-size: 14px; color: #4E5751">{label_}</div></div>')


tiles = grid([tile(cnt.get("done", 0), "tracker items done, of %d" % len(items)),
              tile(cnt.get("in_progress", 0), "in progress"),
              tile(cnt.get("blocked", 0), "blocked, each on a named person or run"),
              tile("%d / %d" % (sum(b["status"] == "done" for b in ab), len(ab)), "audit bundles done"),
              tile("%d / %d" % (sum(b["status"] == "done" for b in q1), len(q1)), "Q1 bundles done"),
              tile("%d / %d" % (sum(b["status"] == "done" for b in q2), len(q2)), "Q2 build bundles done")], min_w=180)


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
], caption="Semantic / formula where two values are given. Each bundle was frozen before its held-out read; B1's first read "
           "stopped on a build error and was re-read once after a class fix (analysis/reports/q2_build_results.md).")

Q2_BUNDLES = table(["Bundle", "Title", "Status"],
                   [[b["id"], b["title"], b["status"].replace("_", " ")] for b in q2], mono_cols=(0,),
                   caption="Each bundle's result is in analysis/reports/q2_b&lt;k&gt;_*.md and in the Slack lists.")


def you(h):
    return h.replace("your live runs", "Uzair's live runs").replace("waits on you", "waits on Uzair").replace("waiting on you", "waiting on Uzair").replace("Waiting on you", "Waiting on Uzair").replace("WAITING ON YOU", "WAITING ON UZAIR")


BODY = "\n".join([
    question("What is done, what is next, and what is waiting on whom?",
             before="nothing: this page is generated from the tracker and can be read on its own."),
    P(f"The team works from two Slack lists, kept in sync with the tracker; this page is the same state, for recentering. Work "
      f"comes in {T('bundle', 'bundles')}: each closes a set of {T('ticket', 'tickets')} and has a must-show list. {T('live', 'LIVE')} "
      f"work spends model calls and is started only by Uzair. Decisions happen at {T('gate', 'gates')} with tests stated in advance."),
    tiles,
    H2("Q2 build: the landmarks after the first held-out pass"),
    P(f"The paper needs ER-F, ER-1, ER-2, ER-3 and ER-4a; the wedge needs ER-F, ER-1, ER-2, ER-3 and ER-4b. After the held-out "
      f"reads, {t('q2.paper.met')} of 5 paper constraints and {t('q2.wedge.met')} of 5 wedge constraints are met."),
    Q2_TABLE, Q2_BUNDLES,
    you(L4.audit_intro), you(L4.audit_host),
    H2("Quarter 1 plan"),
    delevel(L4.legend), delevel(L4.host),
    f'<div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: stretch">{you(delevel(L4.detail))}{you(delevel(L4.queue))}</div>',
    delevel(L3.gates),
    answer(f"{cnt.get('done', 0)} of {len(items)} tracked items are done. The audit chapter is closed and the Q2 build has had its "
           f"first held-out pass: floors and provenance are met; precision, calibration, accuracy and RCA landmarks are not yet. "
           f"The next step is choosing which of those to chase with a second kernel version.",
           "What changed since you last looked?"),
])
