from common import *
from plots import plane_Sa, plane_cq

# ---------------------------------------------------------------- derivation of F1 = S x a
dev_sem = max(abs(v("m.%s.aS" % k) - v("m.%s.F1_forced_reported" % k)) for k in ("PC", "GES", "FCI", "LiNGAM", "NOTEARS"))
ident = deriv("From a graph to one number: F1 = S × a", [
    (f"Compare the system's connected pairs with the truth: {m('TP')} found, {m('FP')} extra, {m('FN')} missed. {m('P = TP/(TP+FP)')}, {m('R = TP/(TP+FN)')}, {m('S = 2PR/(P+R)')}.", "skeleton F1"),
    (f"Of the {m('TP')} found pairs, a share {m('c')} is given a direction and a share {m('q')} of those is right. The other {m('1 − c')} are undecided.", ""),
    (f"Forced choice orients each undecided pair at random, half right on average, so the share of found pairs pointing the right way is {m('a = c·q + (1 − c)/2')}.", ""),
    (f"Every predicted pair becomes exactly one arrow: {m('TP + FP')} arrows, of which {m('a·TP')} are right. An extra pair can never give a right arrow.", ""),
    (f"Directed precision {m('= a·TP/(TP+FP) = a·P')}; directed recall {m('= a·TP/(TP+FN) = a·R')}.", ""),
    (f"So directed F1 {m('= 2(aP)(aR)/(aP + aR) = a·S')}.",
     "exact per scenario; over a family, mean(a·S) differs from mean(a)·mean(S) by their covariance: here at most %.3f on the five semantic methods below" % dev_sem),
    (f"Differentiate: {m('∂F1/∂c = S·(q − ½)')}. Committing a direction pays only when {m('q > ½')}; below that, leaving the pair to the coin scores more.", "the case for abstention, T4"),
], note="Check: analysis/space_coords.py, gate C1; results in analysis/results/space/.")

ROWS = [("PC", "PC"), ("GES*", "GES"), ("FCI*", "FCI"), ("LiNGAM", "LiNGAM"), ("NOTEARS", "NOTEARS")]
td = "padding: 4px 8px"
trs = "".join(
    f'<tr style="border-top: 1px solid #E3E6E0"><td style="{td}">{lab}</td>'
    + "".join(f'<td style="{td}">{n("m.%s.%s" % (k, c))}</td>' for c in ("S", "c", "q", "a", "aS", "F1_forced_reported")) + "</tr>"
    for lab, k in ROWS)
nt_abstain = 0.5 * v("m.NOTEARS.S")
worked = f"""<section style="display: flex; flex-direction: column; gap: 10px; padding: 18px 20px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; font-size: 14px; line-height: 20px">
<h3 style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px">Worked through, semantic family</h3>
<div style="overflow-x: auto"><table style="border-collapse: collapse; font-family: {MONO}; font-size: 13px; line-height: 18px">
<thead><tr style="text-align: left; color: #4E5751">{''.join(f'<th style="{td}">{h}</th>' for h in ("system", "S", "c", "q", "a", "a·S", "reported"))}</tr></thead>
<tbody>{trs}</tbody></table></div>
<p style="margin: 0">* on the {n('m.GES.scenarios')} scenarios where it runs. Reported values are means of per-scenario F1; a·S is computed from family means, hence the small gaps. Every number links to its file.</p>
<p style="margin: 0"><b>Three readings.</b> PC's directions are barely better than a coin (q {n('m.PC.q')}). FCI is the cautious one: it commits only {n('m.FCI.c', '{:.0%}')} of its pairs, but {n('m.FCI.q', '{:.0%}')} of those are right. NOTEARS commits everything at q {n('m.NOTEARS.q')}, below a coin: abstaining everywhere would lift it from {n('m.NOTEARS.F1_forced_reported')} to {nt_abstain:.3f}.</p>
</section>"""

k_sem, k_for, k_semI = v("kappa.sem.D"), v("kappa.for.D"), v("kappa.sem.DI")
limits = deriv("Deriving the limits", [
    ("Observational data reveal conditional independencies and, given faithfulness, nothing else about structure. No method can tell apart the graphs of one equivalence class.", ""),
    (f"So the best a method can do from D: a perfect skeleton ({m('S = 1')}), commit exactly the compelled edges ({m('c = κ, q = 1')}), and leave the rest to the coin: {m('a = κ + (1 − κ)/2 = (1 + κ)/2')}.", "this is L(orientation, D)"),
    (f"Semantic scenarios: κ = {n('kappa.sem.D')} gives {(1 + k_sem) / 2:.3f}; computed per scenario and averaged, {n('lim.sem.D', bold=True)} (lowest scenario {n('lim.sem.D.min')}). Formula: κ = {n('kappa.for.D')}, limit {n('lim.for.D')}.", ""),
    (f"Interventions: setting a target reveals the direction of every edge touching it, and the propagation rules carry it further. κ rises to at least {n('kappa.sem.DI')}, so the limit is at least {n('lim.sem.DI', bold=True)} (formula {n('lim.for.DI')}).", "a lower bound: only edges touching a target were counted"),
    (f"Knowledge: a correct order orients every connected pair, {m('κ = 1')}, limit <b>1.000</b>. Wrong knowledge costs at most the directions it decided, provided it never touches the skeleton (invariant I5).", ""),
    (f"Skeleton: S → 1 as rows → ∞, given faithfulness. At 1,000 rows there is no closed bound, only the best measured: GES, S = {n('m.GES.S')} where it runs.", ""),
    (f"Scope: these limits are for methods that use conditional independence. Methods that assume a mechanism form (LiNGAM: linear, non-Gaussian noise) can in principle orient more; here LiNGAM's q is {n('m.LiNGAM.q')}.", ""),
])

# ---------------------------------------------------------------- projection 3: one scale, positions from the data
Y = lambda val: 80 + (1 - val) * 640  # noqa: E731


def lane(x, entries, gap=19):
    """Markers at their true height; labels pushed down just enough not to overlap."""
    rows = []
    for e in entries:
        key, text, colour = e[0], e[1], e[2]
        w = e[3] if len(e) > 3 else 200
        bold = e[4] if len(e) > 4 else False
        val = v(key) if isinstance(key, str) else key
        label = n(key, bold=bold) if isinstance(key, str) else ("<b>%.3f</b>" % val if bold else "%.3f" % val)
        rows.append((Y(val), label, text, colour, w))
    out, last = [], -1e9
    for y, label, text, colour, w in sorted(rows, key=lambda r: r[0]):
        ly = max(y - 9.5, last + gap)
        last = ly
        tc = colour if colour in ("#8E2A2A", "#6A716B") else "#17201B"
        out.append(f'<div style="position: absolute; left: {x}px; top: {y - 1.5:.0f}px; width: 20px; height: 3px; background: {colour}"></div>'
                   f'<div style="position: absolute; left: {x + 28}px; top: {ly:.0f}px; width: {w}px; font-size: 13px; line-height: 18px; color: {tc}">{label} · {text}</div>')
    return "".join(out)


grid = "".join(f'<div style="position: absolute; left: 60px; top: {Y(g):.0f}px; width: 848px; height: 1px; background: {"#C9CEC6" if g in (0, 1) else "#E3E6E0"}"></div>'
               f'<div style="position: absolute; left: 8px; top: {Y(g) - 9:.0f}px; width: 44px; text-align: right; font-size: 12px; font-family: {MONO}; color: #4E5751">{g:.2f}</div>'
               for g in (1, 0.75, 0.5, 0.25, 0))
pcF, pcS, lim = v("pc.F1"), v("pc.S"), v("lim.sem.D")
budget = (f'<div style="position: absolute; left: 320px; top: {Y(1):.0f}px; width: 24px; height: {Y(lim) - Y(1):.0f}px; background: #D9DDD6"></div>'
          f'<div style="position: absolute; left: 320px; top: {Y(lim):.0f}px; width: 24px; height: {Y(pcS) - Y(lim):.0f}px; background: #F3C9A0"></div>'
          f'<div style="position: absolute; left: 320px; top: {Y(pcS):.0f}px; width: 24px; height: {Y(pcF) - Y(pcS):.0f}px; background: #F9E3CC"></div>'
          f'<div style="position: absolute; left: 320px; top: {Y(pcF):.0f}px; width: 24px; height: {Y(0) - Y(pcF):.0f}px; background: #1D5C99"></div>'
          f'<div style="position: absolute; left: 352px; top: {Y(1) + 2:.0f}px; width: 140px; font-size: 13px; line-height: 17px">{1 - lim:.3f} not identifiable</div>'
          f'<div style="position: absolute; left: 352px; top: {(Y(lim) + Y(pcS)) / 2 - 9:.0f}px; width: 140px; font-size: 13px; line-height: 17px"><b>{lim - pcS:.3f}</b> lost in the skeleton</div>'
          f'<div style="position: absolute; left: 352px; top: {(Y(pcS) + Y(pcF)) / 2 - 9:.0f}px; width: 140px; font-size: 13px; line-height: 17px"><b>{pcS - pcF:.3f}</b> lost in directions</div>'
          f'<div style="position: absolute; left: 352px; top: {(Y(pcF) + Y(0)) / 2 - 9:.0f}px; width: 140px; font-size: 13px; line-height: 17px">{n("pc.F1", bold=True)} scored</div>')
RED, GREY, ORANGE = "#8E2A2A", "#6A716B", "#B85A12"
lanes = (lane(80, [("lim.sem.D", "limit from data", "#17201B", 200, True), ("leak.released", "column layout alone", RED, 200),
                   ("pub.sem.D.best", "best published", "#1D5C99", 200, True), ("pub.sem.D.GIES", "GIES", "#1D5C99", 200),
                   ("m.GES.F1_forced_reported", "our GES*", "#1D5C99", 200), ("pc.F1", "our PC", "#1D5C99", 200),
                   ("leak.shuffled", "layout, shuffled", RED, 200), ("pub.sem.D.LiNGAM", "LiNGAM, published", "#1D5C99", 200),
                   ("m.NOTEARS.F1_forced_reported", "our NOTEARS", GREY, 200)])
         + lane(500, [("lim.sem.DI", "limit", "#17201B", 150, True), ("pub.sem.DI.best", "best published", "#1D5C99", 150, True),
                      ("pub.sem.DI.TabCausal", "TabCausal", "#1D5C99", 150)])
         + lane(680, [(1.0, "limit if knowledge is right", "#17201B", 210, True), ("oracle.depth.reg", "true order + regression", ORANGE, 210, True),
                      ("oracle.inputs.pc", "PC told the inputs", ORANGE, 210), ("cc.real.S0.F1_forced", "Causal-Copilot's own S0", GREY, 210),
                      ("cc.real.S3.F1_forced", "Causal-Copilot, real names", RED, 210, True), ("cc.neutral.S3.F1_forced", "neutral names", RED, 210),
                      ("cc.swapped.S3.F1_forced", "swapped names", RED, 210)]))
heads = "".join(f'<div style="position: absolute; left: {x}px; top: 28px; width: {w}px; font-size: 13px; line-height: 17px">{h}</div>'
                for x, w, h in ((80, 220, "<b>D</b> · numbers only"), (320, 160, "<b>PC's budget</b> in D"), (500, 160, "<b>D+I</b> · interventions"),
                                (680, 220, "<b>D+K</b> · declared knowledge")))
chart_host = f"""<div style="flex: 999 1 640px; min-width: 0; overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
<div style="position: relative; width: 920px; height: 790px">
{grid}
<div style="position: absolute; left: 60px; top: 80px; width: 1px; height: 640px; background: #6A716B"></div>
{heads}{budget}{lanes}
<div style="position: absolute; left: 80px; top: 742px; width: 820px; font-size: 12px; line-height: 16px; color: #4E5751">Semantic family. Published numbers are over all 100 scenarios; ours over the 50 public ones (* where the method runs). All forced choice. Causal-Copilot: 10 S2 test scenarios, stage before the cycle step (strict scoring: {n('cc.real.S3.F1_strict')} / {n('cc.neutral.S3.F1_strict')} / {n('cc.swapped.S3.F1_strict')}). D+K has no published method; its markers are oracles and the agent.</div>
</div>
</div>"""

gap = lim - v("pub.sem.D.best")
aside = f"""<aside style="flex: 1 1 380px; min-width: 0; display: flex; flex-direction: column; gap: 16px">
<section style="display: flex; flex-direction: column; gap: 10px; padding: 20px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
<h3 style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px">The distance</h3>
<p style="margin: 0">Between the best published result and the limit from data: <b>{gap:.3f}</b> of the scale. For plain PC, <b>{lim - pcS:.3f}</b> of what the data allow is lost in the skeleton and <b>{pcS - pcF:.3f}</b> in directions.</p>
<p style="margin: 0">Since F1 = S × a, matching {n('pub.sem.D.best')} needs, for example, S = 0.80 with a = 0.79; reaching the limit needs S = 1 and every compelled edge right.</p>
</section>
<section style="display: flex; flex-direction: column; gap: 10px; padding: 20px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
<h3 style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px">Where each part can be won back</h3>
<ol style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 10px">
<li><b>Skeleton (S).</b> One joint test per candidate edge, conditioned on the order the ledger holds; nonlinear tests next. <span style="color: #9A4A0E; font-weight: 600">P2</span></li>
<li><b>Directions the data can settle (q).</b> GES and FCI already reach q = {n('m.GES.q')} and {n('m.FCI.q')}; PC gets {n('m.PC.q')}, and its output also depends on column order (vendored causal-learn). <span style="color: #1D5C99; font-weight: 600">P1, measured</span></li>
<li><b>Directions the data cannot settle.</b> Only interventions (limit ≥ {n('lim.sem.DI')}) or declared knowledge (1.000 if right) reach them. <span style="color: #9A4A0E; font-weight: 600">P2</span></li>
<li><b>Wrong knowledge.</b> The agent follows swapped names on {n('cc.M3.hits')} of {n('cc.M3.n')} edges. In the ledger, knowledge may order a connected pair and nothing else, so wrong names can only cost the directions they decided. <span style="color: #9A4A0E; font-weight: 600">P2</span></li>
</ol>
</section>
<section style="display: flex; flex-direction: column; gap: 8px; padding: 20px; background: #17201B; color: #F2F3EF; border-radius: 12px">
<h3 style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px">Baselines to beat</h3>
<span>D · <b>{t('pub.sem.D.best')}</b> published ({t('pub.sem.D.best.method')})</span>
<span>D+I · <b>{t('pub.sem.DI.best')}</b> published ({t('pub.sem.DI.best.method')})</span>
<span>D+K · none published; the easy oracle sits at <b>{t('oracle.depth.reg')}</b></span>
<a href="Theses.dc.html" style="color: #9CC7F0">How the theses aim at these</a>
</section>
</aside>"""

scale = f"""<section style="display: flex; flex-direction: column; gap: 12px">
{h2("Projection 3 · every system on one scale")}
<p style="margin: 0; max-width: 980px; color: #2C3631">Directed-edge F1 by regime, from 0 to 1, each marker at its true height. Limits from the derivation above; published results; our reproductions; oracles that price a piece of information; and Causal-Copilot.</p>
<div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start">{chart_host}{aside}</div>
</section>"""

perf_intro = f"""<section style="display: flex; flex-direction: column; gap: 10px">
{h2("The performance space, and two projections of it")}
<p style="margin: 0; max-width: 980px; color: #2C3631">The derivation shows that any system's scoreboard number is fixed by three coordinates: {m('S')}, {m('c')} and {m('q')}. That is the performance space. Projection 4 shows {m('S')} against {m('a')} (which folds c and q together), where curves of equal F1 are hyperbolas. Projection 5 opens {m('a')} into {m('c')} and {m('q')}. Blue dots are methods; coloured paths are Causal-Copilot moving through its stages under each name arm.</p>
</section>"""

plots = f"""<div style="display: flex; flex-wrap: wrap; gap: 20px">
<figure style="flex: 1 1 640px; margin: 0; display: flex; flex-direction: column; gap: 8px">
<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; padding: 8px 0">{plane_Sa()}</div>
<figcaption style="font-size: 14px; line-height: 20px"><b>Projection 4 · S × a.</b> The green region beats every published method. Knowledge can only move a system straight up (it may orient pairs, never connect them); joint tests and interventions move it right. Causal-Copilot's bootstrap step moves every arm far left; real names then move it back right, neutral names leave it where it is.</figcaption>
</figure>
<figure style="flex: 1 1 640px; margin: 0; display: flex; flex-direction: column; gap: 8px">
<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; padding: 8px 0">{plane_cq()}</div>
<figcaption style="font-size: 14px; line-height: 20px"><b>Projection 5 · c × q.</b> Grey curves join points of equal direction accuracy a. Moving right pays only above the red line. With real names, the model's review commits more pairs (c {n('cc.real.S1.c', '{:.2f}')} → {n('cc.real.S2.c', '{:.2f}')}) at lower accuracy (q {n('cc.real.S1.q', '{:.2f}')} → {n('cc.real.S2.q', '{:.2f}')}): it guesses where the data are silent, which is the behaviour refinement v2 restricts.</figcaption>
</figure>
</div>"""

body = "\n".join([
    title_block("The limits, derived, and where the distance goes",
                "How one graph becomes one number, why the number cannot exceed a limit that depends on the evidence allowed, and where every measured system sits in the space those two facts define."),
    f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(520px, 100%), 1fr)); gap: 16px; align-items: start">{ident}{worked}</div>',
    limits, scale, perf_intro, plots,
    terms_panel(["prf", "S", "c", "q", "a", "forced", "strict", "compelled", "limit", "oracle", "budget", "iso", "leak"]),
    footer(f"the limits are derived for every regime and every measured system has coordinates. The distance from the best published {t('pub.sem.D.best')} to the {t('lim.sem.D')} limit is {gap:.3f} of the scale; for PC, {lim - pcS:.3f} of it is in the skeleton and {pcS - pcF:.3f} in directions.",
           "P2 moves systems up (better a, skeleton untouched) and P1 tells us which way each move came from. The theses are where each move is claimed.",
           "Theses.dc.html", "See the theses"),
])
BODY = body
ZOOM = "Zoomed into: the orientation row"
TITLE = "2 Bounds"
