from common import *
from theses_map import spacemap



def thesis(tid, pillar, claim, refuted, status_text, status, evidence, route, nxt):
    col, tint, _ = PILLAR[pillar]
    ev = "".join(f"<li>{e}</li>" for e in evidence)
    return f"""<article style="display: flex; flex-direction: column; gap: 10px; padding: 18px 20px; background: #FFFFFF; border: 1px solid #C9CEC6; border-top: 4px solid {col}; border-radius: 10px">
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px">
<span style="font-family: {MONO}; font-size: 14px; font-weight: 600; color: {col}">{tid}</span>
{pill(status_text, status)}
</div>
<p style="margin: 0; font-size: 17px; line-height: 24px; font-weight: 600">{claim}</p>
<p style="margin: 0; font-size: 14px; line-height: 20px; color: #4E5751"><b style="color: #8E2A2A">Refuted if</b> {refuted}</p>
<div style="border-top: 1px solid #E3E6E0; padding-top: 10px">
{tag("Evidence today", "#4E5751")}
<ul style="margin: 6px 0 0; padding-left: 18px; font-size: 14px; line-height: 20px; display: flex; flex-direction: column; gap: 4px">{ev}</ul>
</div>
<div style="padding: 10px 12px; background: {tint}; border-radius: 8px; font-size: 14px; line-height: 20px"><b>Route to the bound:</b> {route}</div>
<p style="margin: 0; font-size: 13px; line-height: 18px; color: #4E5751"><b>Next:</b> {nxt}</p>
</article>"""


def pillar_col(pid, question, owns, distance, count, cards):
    col, tint, name = PILLAR[pid]
    return f"""<section style="flex: 1 1 400px; min-width: 0; display: flex; flex-direction: column; gap: 14px">
<div style="padding: 16px 18px; background: {tint}; border: 1.5px solid {col}; border-radius: 10px; display: flex; flex-direction: column; gap: 6px">
{tag(name, col)}
<p style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px; font-weight: 600">{question}</p>
<p style="margin: 0; font-size: 14px; line-height: 20px"><b>Owns in the space:</b> {owns}</p>
<p style="margin: 0; font-size: 14px; line-height: 20px"><b>Acts on the distance:</b> {distance}</p>
<p style="margin: 0; font-size: 13px; line-height: 18px; font-family: {MONO}; color: {col}">{count}</p>
</div>
{cards}
</section>"""


T1 = thesis("T1", "P1",
            "The source of a method's order information explains most of its directed-edge accuracy.",
            "GES, FCI and the pretrained models do not show PC's pattern: directions near chance, a large gain from oracle order.",
            "Partly refuted", "dec",
            [f"PC orients {n('pc.q', '{:.0%}')} of committed directions right; given true depth, regression reaches {n('oracle.depth.reg')} (BND-04, REP-06).",
             f"GES orients {n('m.GES.q', '{:.0%}')}, FCI {n('m.FCI.q', '{:.0%}')}: not near chance. The claim holds for PC, not for score-based search.",
             "Pretrained models (AVICI, CDFM) not measured: checkpoints blocked by the network allowlist."],
            f"restate as two parts. For constraint methods, order is most of the gap; for all methods, the skeleton loses about {v('lim.sem.D') - v('pc.S'):.2f} that order cannot recover.",
            "rewrite T1 in the report with the GES/FCI numbers; run the pretrained models once the allowlist opens.")

T2 = thesis("T2", "P1",
            "Deployed agents take their order from names and layout, not from the numbers.",
            "Causal-Copilot keeps its score under neutral names and shuffled columns.",
            "Supported on S2", "done",
            [f"Final directed F1 by name arm (forced choice): real {n('cc.real.S3.F1_forced')}, neutral {n('cc.neutral.S3.F1_forced')}, swapped {n('cc.swapped.S3.F1_forced')} (BND-08, 10 scenarios x 3 arms).",
             f"M3 {t('cc.M3.verdict').lower()} {n('cc.M3.hits')}/{n('cc.M3.n')}, M4 {t('cc.M4.verdict').lower()} {n('cc.M4.hits')}/{n('cc.M4.n')}; M2 {t('cc.M2.verdict').lower()} {n('cc.M2.hits')}/{n('cc.M2.n')} (names help in fewer families than predicted).",
             f"The released files leak order through column layout: {n('leak.released')} as released vs {n('leak.shuffled')} shuffled.",
             f"{n('cc.crashed')} of {n('cc.runs')} runs crashed in the cycle step (judge_functions.py:562), {n('cc.crashed.real')} of them with real names."],
            "this thesis measures the distance rather than closing it. Its reach is the field-wide audit (E1): the same controls on every agent with public code.",
            "DLV-02 decision on the 6 crashed arms; second model in BND-12.")

T3 = thesis("T3", "P2",
            "Order held as a typed, sourced partial order is (a) never below data-only, (b) boundedly harmed by wrong knowledge, (c) at or above the best published number in each regime.",
            "(a) or (b) fail on held-out scenarios. (c) is a target, reported whichever way it falls.",
            "(a) and (b) supported; (c) not met", "prog",
            [f"Refinement v1 (BND-10, pooled {n('v1.files')}): R1 {n('v1.R1.hits')}/{t('v1.files')} and R2 {n('v1.R2.hits')}/{t('v1.files')}, inconclusive. It dropped {n('v1.dropped.all')} connections, {n('v1.dropped.true')} of them true.",
             f"Refinement v2 (BND-11) keeps every data connection and uses names only where the data are silent. Held out (formula test, {n('v2.test.files')} files): R1 {n('v2.test.R1')}/{t('v2.test.files')}, R3 {n('v2.test.R3', '{:+.3f}')}. Swapped names cost nothing measurable (R5 {n('v2.names.R5')}/10); real names help in only {n('v2.names.R6')} of 10 families (R6 refuted).",
             f"Ledger kernel (Q2 B1, rule C3), held out: directed F1 against plain PC with maxP {n('q2.erf.sem.f1', '{:+.3f}')} / {n('q2.erf.for.f1', '{:+.3f}')} "
             f"(semantic / formula), against GES {n('q2.ges.sem.f1', '{:+.3f}')} / {n('q2.ges.for.f1', '{:+.3f}')}.",
             f"Tiers on open pairs only (Q2 B3): neutral names equal the data-only ledger on {n('q2.b3.sem.neutral')}/{t('q2.b3.sem.files')} and "
             f"{n('q2.b3.for.neutral')}/{t('q2.b3.for.files')} held-out files; moved names stay within the T3 bound on every file; real names add "
             f"{n('q2.b3.sem.gain', '{:+.3f}')} / {n('q2.b3.for.gain', '{:+.3f}')}, below the published bests."],
            f"B1 data-only kernel at or above PC ({n('pc.F1')}) → knowledge tiers B3 (oracle tiers reach {n('oracle.depth.reg')}, above the published {n('pub.sem.D.best')}) → interventions B2 toward the {n('lim.sem.DI')} limit.",
            "(a) and (b) now hold held out. (c) needs direction evidence beyond the equivalence class: kernel v3 found that neither a "
            "lower GES penalty, propagating knowledge, nor pairwise asymmetry gets there (analysis/reports/q2_dirsig_dev.md).")

NEXT = 'choose between more scenarios (every open landmark is within one interval width of its bar) and a v4 aimed at links: missed and false links cause most wrong answers and most wrong directions.'

T4 = thesis("T4", "P2",
            "Claims carry calibrated confidence and a machine-checkable derivation, so the system can decline to claim.",
            "Calibration error on held-out scenarios is no better than raw bootstrap frequencies, or the checker rejects its own derivations.",
            "Supported against raw frequencies; gate missed on one family", "prog",
            [f"Q2 B4, held out: calibrated error {n('q2.b4.sem.ece', historic=True)} semantic and {n('q2.b4.for.ece', historic=True)} formula, against {n('q2.b4.sem.raw', historic=True)} and "
             f"{n('q2.b4.for.raw', historic=True)} for raw bootstrap frequencies (the baseline Causal-Copilot's filter uses). The refutation test fails: calibration beats raw.",
             "The independent checker (K7) accepts every claim in every ledger built in B1-B3.",
             f"The pre-registered 0.05 gate is missed on semantic, in the safe direction (claims are right more often than stated). "
             f"Half-coverage precision {n('q2.b4.sem.prec', historic=True)} semantic, {n('q2.b4.for.prec', historic=True)} formula.",
             "B4 pre-registered an isotonic map on 10-resample stability, fitted on dev and frozen before the read (DOM-08 had proposed Platt scaling).",
             f"Kernel v3 (second read): a model on ledger features brings calibration error to {n('q2v3.sem.D.ece')} / "
             f"{n('q2v3.for.D.ece')} (semantic / formula); its upper end stays above 0.05 on 25 scenarios."],
            "precision at a stated coverage is the honest score once forced choice stops being the only view; it does not move F1 but tells a reader which claims to trust.",
            "scenario-level shrinkage of the map and more scenarios; the coverage guarantee stays within one family.")

T5 = thesis("T5", "P3",
            "The claims answer \"what happens if we set X?\" with a stated identification status, checkable on held-out interventions.",
            "Interventional predictions are no better than regression on all variables.",
            "Surveyed", "p3",
            [f"DOM-09: IDA on {n('ida.vars')} variables, {n('ida.pairs')} pairs in {n('ida.seconds', '{:.2f}')} s; {n('ida.identified', '{:.0%}')} of effects identified to a single value.",
             f"The true parents were among IDA's candidate sets for only {n('ida.parents.ok')} of {t('ida.vars')} targets: effects inherit the skeleton loss."],
            "effects are bounded by orientation: each direction the ledger fixes turns a set of possible effects into one. Scored on the released interventional rows and Causal Chambers.",
            "C1 (BLD-07) after B2; no bundle yet.")

T6 = thesis("T6", "P3",
            "The system can say which experiment would settle the most open directions, and that choice beats random on recorded experiments.",
            "No better than random selection on the Causal Chambers pool.",
            "Data ready", "p3",
            [f"Causal Chambers sample loaded: {n('chambers.regimes')} regimes, observational and interventional (BEN-10). Our CPDAG is identical to the authors' (REP-09).",
             f"{n('int.none')} of {n('int.total')} semantic interventions show no detectable shift (BEN-09): the pool has dead experiments to avoid.",
             "Baselines chosen (DOM-10): CBED and pcalg's optimal-target rule, plus random. R is blocked in both sandboxes, so pcalg waits for Q2."],
            f"each chosen experiment moves a pair from the D column to the D+I column; the limit with interventions is {n('lim.sem.DI')}.",
            "C2 (BLD-08) after B2; no bundle yet.")

carve = f"""<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; align-items: stretch">
<div style="padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 10px; font-size: 14px; line-height: 20px">
{tag("How the space is carved", "#17201B")}
<p style="margin: 6px 0 0">Level 1 is a grid of tasks (skeleton, orientation, effects, experiments) by information regimes (D, D+I, D+K, D+I+K). Each pillar owns a block of that grid and one piece of the distance on Level 2.</p>
</div>
<div style="padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 10px; font-size: 14px; line-height: 20px">
{tag("Read a card", "#17201B")}
<p style="margin: 6px 0 0">Claim, what would refute it (written before the evidence), what the evidence says today with its ticket, and the route from where it stands to the bound.</p>
</div>
<div style="padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 10px; font-size: 14px; line-height: 20px; display: flex; flex-wrap: wrap; gap: 8px; align-content: flex-start">
{tag("Status", "#17201B")}<span style="flex-basis: 100%; height: 0"></span>
{pill("Supported", "done")} {pill("In progress", "prog")} {pill("Refuted in part", "dec")} {pill("Not started", "todo")} {pill("Decisions pillar", "p3")}
</div>
</div>"""

_lim, _S, _F = v("lim.sem.D"), v("pc.S"), v("pc.F1")
cols = f"""<div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start">
{pillar_col("P1", "Where does each direction come from?",
            "the D column; layout and name controls on every row.",
            "explains it. Splits PC's %.3f loss into %.3f not identifiable, %.3f skeleton, %.3f direction." % (1 - _F, 1 - _lim, _lim - _S, _S - _F),
            pc_line("P1"), T1 + T2)}
{pillar_col("P2", "Use order knowledge on purpose, and say where it came from.",
            "orientation in D+K, D+I and D+I+K: the thesis cell.",
            "closes it. The direction loss (%.3f for PC) and, with interventions, part of the skeleton loss." % (_S - _F),
            pc_line("P2"), T3 + T4)}
{pillar_col("P3", "Turn claims into answers and the next experiment.",
            "the effects and experiments rows.",
            "spends it. Every direction fixed narrows an effect; every good experiment fixes directions.",
            pc_line("P3"), T5 + T6)}
</div>"""

INV = [
    ("I1", "Shuffling columns changes nothing", "Holds for the ledger (50/50 dev files, 120/120 oracle graphs). The vendored PC changes its output in %s of %s files (BND-06)" % (n("pc.order.changed"), n("pc.order.files")), "done", "a gate on every run"),
    ("I2", "Same inputs, same ledger hash", "Holds: 50/50 repeat builds (Q2 B1)", "done", "CAP-11"),
    ("I3", "D+K with no knowledge equals D", "Holds held out: %s/%s and %s/%s files (Q2 B3)" % (n("q2.b3.sem.neutral"), t("q2.b3.sem.files"), n("q2.b3.for.neutral"), t("q2.b3.for.files")), "done", "gives T3(a)"),
    ("I4", "No claim without evidence; the checker accepts every claim", "Holds: every claim cites records and K7 re-derives it (Q2 B1-B3)", "done", "CAP-09"),
    ("I5", "Knowledge never creates or removes a connection", "v1 violated it (dropped %s). The ledger enforces it by construction; the skeleton never moved in any B3 arm" % n("v1.dropped.all"), "done", "gives T3(b)"),
    ("I6", "An intervention beats knowledge", "Built (Q2 B2): an intervention overrides a data or knowledge direction and the claim records the conflict", "done", "CAP-03"),
    ("I7", "Malformed model output cannot crash a run", "Causal-Copilot violates it: %s of %s runs. Our names runner retries, then abstains" % (n("cc.crashed"), n("cc.runs")), "prog", "CAP-10"),
]
inv_cells = []
for iid, txt, now, st, link in INV:
    bg, bd, fg, style = STATUS[st]
    inv_cells.append(f"""<div style="padding: 12px 14px; background: {bg}; border: 1.5px {style} {bd}; border-radius: 8px; display: flex; flex-direction: column; gap: 6px; font-size: 13px; line-height: 18px">
<span style="font-family: {MONO}; font-weight: 600; color: {fg}">{iid}</span>
<span style="font-size: 14px; line-height: 19px; font-weight: 600">{txt}</span>
<span>{now}</span>
<span style="color: #4E5751">{link}</span>
</div>""")
invariants = f"""<section style="display: flex; flex-direction: column; gap: 12px">
{h2("The ledger's invariants, checked against what exists today")}
<p style="margin: 0; max-width: 900px; color: #2C3631">These are the P2 promises written as tests. Where Causal-Copilot or our refinement already exists, the cell says whether it holds there.</p>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px">
{''.join(inv_cells)}
</div>
</section>"""

GATES = [
    ("G1", "", "GES and FCI budgets (done, BND-04); knowledge elicitation A3 (done, AB-07: names alone order 69% of true edges; tiers alone 0.448)",
     "Decides: keep or drop the knowledge route. Evidence is in; the call is open." if bundle_status("AB-16") != "done" else
     "Decided by AB-16 (the wedge decision): knowledge stays as declared structure, never as a vote.", "prog" if bundle_status("AB-16") != "done" else "done"),
    ("G2", "", "Program v2: kernel B1 passes I1-I4, I7 and beats PC held-out. The Q1 DAG instead asks: refinement v1 or fallback (BND-13)",
     "The two plans disagree here" if item("DEC-01")["status"] != "done" else "Decided by DEC-01: program v2 adopted; refinement v2 runs beside it as the Causal-Copilot fix (BLD-06)",
     "dec" if item("DEC-01")["status"] != "done" else "done"),
    ("G3", "", "Scores in three regimes with all controls; scoreboard package (BND-14)", "Decides: what moves to Q2", "todo"),
    ("G4", "", "Calibration B4, effects C1, experiments C2, second model, Causal Chambers; paper draft", "Cut C2 first, then C1", "todo"),
]
gate_cells = []
for g, d, need, dec, st in GATES:
    bg, bd, fg, style = STATUS[st]
    gate_cells.append(f"""<div style="padding: 12px 14px; background: {bg}; border: 1.5px {style} {bd}; border-radius: 8px; font-size: 13px; line-height: 18px; display: flex; flex-direction: column; gap: 4px">
<span><b style="font-family: {MONO}; color: {fg}">{g}</b>{(" · " + d) if d else ""}</span>
<span>{need}</span>
<span style="color: #4E5751">{dec}</span>
</div>""")

_pc = pillar_counts()


_bundled = {x for b in SNAP["bundles"] for x in b["closes"]}
_unb = [i["id"] for i in SNAP["items"] if i["id"].startswith("BLD-") and i["pillar"] in ("P2", "P3") and i["id"] not in _bundled]
_share = {k: 100.0 * c["done"] / c["n"] for k, c in _pc.items()}
gap_box = f"""<div style="flex: 1 1 380px; padding: 18px 20px; background: #FFFFFF; border: 2px dashed #8E2A2A; border-radius: 10px; display: flex; flex-direction: column; gap: 8px">
{tag("The gap this level exposes", "#8E2A2A")}
<p style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px; font-weight: 600">The ledger exists and holds its promises; it does not yet beat the field's best numbers.</p>
<p style="margin: 0; font-size: 14px; line-height: 20px">After the Q2 build's first held-out pass, {t("q2.paper.met")} of 5 paper constraints are met (floors, provenance). Precision at half coverage, calibration, accuracy above GES and RCA at 0.90 are not yet: P1 is {_share["P1"]:.0f}% done, P2 {_share["P2"]:.0f}%, P3 {_share["P3"]:.0f}%.</p>
<p style="margin: 0; font-size: 14px; line-height: 20px"><b>Next:</b> the explanation round decides between measurement plus the ledger and a stronger engine inside it (analysis/reports/q2_explain_dev.md); a second held-out family widens the scenario count.</p>
</div>"""

dec_box = f"""<div style="flex: 1 1 300px; padding: 18px 20px; background: #F6E7E7; border: 1.5px solid #8E2A2A; border-radius: 10px; display: flex; flex-direction: column; gap: 8px; font-size: 14px; line-height: 20px">
{tag("Decisions that gate this level", "#8E2A2A")}
<p style="margin: 0"><b style="font-family: {MONO}">DEC-01</b> Adopt program v2 (these six theses) as the plan. <span style="color: #4E5751">tracker: {STATUS_TEXT[item("DEC-01")["status"]]}</span></p>
<p style="margin: 0"><b style="font-family: {MONO}">DEC-02</b> Knowledge elicitation A3, about 900 short calls asking only for tiers: approved and run (AB-07). Used only to orient, the model's tiers lift GES from 0.528 to 0.546; wrong tiers cost 0.19. <span style="color: #4E5751">tracker: {STATUS_TEXT[item("DEC-02")["status"]]}</span></p>
</div>"""

gates = f"""<section style="display: flex; flex-direction: column; gap: 12px">
{h2("Gates and the open choice")}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px">{''.join(gate_cells)}</div>
<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: stretch">{gap_box}{dec_box}</div>
</section>"""

EXT = [("E1", "Field-wide audit", "every agent with public code under the same controls"),
       ("E2", "Public agent track", "a scoreboard page with regime and control fields"),
       ("E3", "Real experiments", "the ledger choosing runs on Causal Chambers hardware"),
       ("E4", "Learned fusion", "a network trained to weigh data against stated knowledge"),
       ("E5", "Harder settings", "hidden causes, time series, 100+ variables")]
ext_cells = "".join(f"""<div style="padding: 10px 12px; border: 1.5px dashed #6A716B; border-radius: 8px; background: #FFFFFF; font-size: 13px; line-height: 18px"><b style="font-family: {MONO}">{e}</b> {t}<br><span style="color: #4E5751">{d}</span></div>""" for e, t, d in EXT)
ceiling = f"""<section style="display: flex; flex-direction: column; gap: 10px">
{h2("Beyond the theses: the edge of the space")}
<p style="margin: 0; max-width: 900px; color: #2C3631">Not planned. Listed so the ceiling is visible: E5 is the dashed bottom row of Level 1; E1 and E3 are how the D+I and D+K columns would be tested outside one benchmark.</p>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px">{ext_cells}</div>
</section>"""

body = "\n".join([
    title_block("Six theses, carved into three pillars",
                "Each pillar owns a block of the space and a piece of the distance to the bound. Each thesis says what we claim, what would refute it, what the evidence says today, and how it gets us closer."),
    carve, spacemap(), cols, invariants, gates, ceiling,
    terms_panel(["thesis", "invariant", "ledger", "tier", "calib", "abstain", "ident", "ida", "gate", "regime"]),
    footer("measurement is done and corrected one thesis (T1 holds for PC, not for GES or FCI). The ledger is built: T3(a) and (b) hold "
           "held out, and T4 beats raw frequencies but misses its own gate on one family.",
           NEXT,
           "Bundles.dc.html", "See the bundles"),
])

BODY = body
ZOOM = "Zoomed into: all six theses"
TITLE = "3 Theses"
