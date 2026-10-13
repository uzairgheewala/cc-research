from common import *


# ---- Projection 2: the Q x R matrix at the Q1 setting, built from the snapshot
def cell(pillar_key, lines, status, thick=False, dashed=False, label=None):
    col, tint, name = PILLAR[pillar_key] if pillar_key else ("#6A716B", "#FFFFFF", "")
    bd = ("2.5px solid " if thick else "1.5px dashed " if dashed else "1.5px solid ") + (col if pillar_key else "#6A716B")
    head = f'<span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: {col}">{label or name}</span>' if pillar_key else ""
    body = "".join(f'<span><span style="color: #4E5751">{k}</span> {v}</span>' if k else f"<span>{v}</span>" for k, v in lines)
    return (f'<div style="display: flex; flex-direction: column; gap: 8px; padding: 14px; background: {tint if pillar_key else "#FFFFFF"}; '
            f'border: {bd}; border-radius: 10px; font-size: 14px; line-height: 20px{"; color: #4E5751" if not pillar_key else ""}">{head}{body}'
            f'<span style="margin-top: auto; font-size: 12px; font-weight: 600; letter-spacing: 0.6px">{status}</span></div>')


def rowhead(name, q, metric, dashed=False):
    return (f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 14px; background: #FFFFFF; border: 1px {"dashed #6A716B" if dashed else "solid #C9CEC6"}; border-radius: 10px">'
            f'<span style="font-family: {COND}; font-size: 20px; font-weight: 700">{name}</span><span style="font-size: 14px">{q}</span>'
            f'<span style="font-size: 12px; color: #4E5751">{metric}</span></div>')


def colhead(b, sub):
    return f'<div style="padding: 10px 14px; background: #17201B; color: #F2F3EF; border-radius: 10px"><b>{b}</b><br><span style="font-size: 13px; color: #C7CFC9">{sub}</span></div>'


gap = v("pub.sem.D.best") and (v("lim.sem.D") - v("pub.sem.D.best"))
M = [
    "<div></div>", colhead("D", "· numbers only, the public scoreboard's regime"), colhead("D+I", "· plus interventions"),
    colhead("D+K", "· plus declared knowledge (names, tiers)"), colhead("D+I+K", "· all three; no published method declares it"),
    rowhead("Skeleton", "Which pairs are directly connected?", "S, skeleton F1"),
    cell("P1", [("Limit", "<b>1.000</b> with unlimited rows, given faithfulness"), ("Published", "not reported on its own"),
                ("Ours", f"PC {n('pc.S', bold=True)} · GES {n('m.GES.S', bold=True)} ({t('m.GES.scenarios')} scenarios)")], "MEASURED"),
    cell("P1", [("Limit", "<b>1.000</b>, as in D"), ("Published", "not reported on its own"), ("Ours", "not measured")], "OPEN"),
    cell("P2", [("Limit", "the same as D: knowledge may order a pair, never connect one"),
                ("Causal-Copilot", f"S {n('cc.real.S0.S', bold=True)} → {n('cc.real.S1.S', bold=True)} at its bootstrap step; real names bring it back to {n('cc.real.S3.S', bold=True)}")],
         "AGENT MEASURED · LEDGER OPEN"),
    cell("P2", [("Limit", "the same as D+I"), ("Published", "none")], "OPEN"),
    rowhead("Orientation", "Which way does each edge point?", "directed-edge F1, the scoreboard's number"),
    cell("P1", [("Limit", f"{n('lim.sem.D', bold=True)}: what the data can identify"),
                ("Published", f"{n('pub.sem.D.best', bold=True)} {t('pub.sem.D.best.method')} · GIES {n('pub.sem.D.GIES')}"),
                ("Ours", f"PC {n('pc.F1', bold=True)} · GES {n('m.GES.F1_forced_reported', bold=True)} on the {t('m.GES.scenarios')} scenarios it runs"),
                ("Leak", f"column order alone {n('leak.released', bold=True)}")], "MEASURED · %.3f OF THE SCALE OPEN" % gap),
    cell("P1", [("Limit", f"at least {n('lim.sem.DI', bold=True)} with the released interventions"),
                ("Published", f"{n('pub.sem.DI.best', bold=True)} {t('pub.sem.DI.best.method')} · TabCausal {n('pub.sem.DI.TabCausal')}"),
                ("Ours", "not measured")], "OPEN"),
    cell("P2", [("Limit", "<b>1.000</b> if the knowledge is right"), ("Published", "no method declares this regime"),
                ("Causal-Copilot", f"{n('cc.real.S3.F1_forced', bold=True)} real · {n('cc.neutral.S3.F1_forced')} neutral · {n('cc.swapped.S3.F1_forced')} swapped names; its own first stage {n('cc.real.S0.F1_forced')}"),
                ("Oracle", f"true order + regression {n('oracle.depth.reg', bold=True)}")], "AGENT MEASURED · LEDGER OPEN",
         thick=True, label="P2 Claim ledger · the thesis cell"),
    cell("P2", [("Limit", "<b>1.000</b> if the knowledge is right"), ("Published", "none"), ("Rule", "an intervention outranks a name")], "OPEN"),
    rowhead("Effects", "What happens if we set X?", "error on held-out interventions"),
    cell("P3", [("Limit", "per pair: identified, a set of values, or not identifiable"),
                ("Ours", f"IDA at {n('ida.vars')} variables: {n('ida.pairs')} pairs in {n('ida.seconds', '{:.2f}')} s; {n('ida.identified', '{:.0%}')} identified")], "SURVEYED"),
    cell("P3", [("Target", "beat regression on all variables"), ("Caveat", f"{n('int.none')} of {n('int.total')} released interventions shift nothing we can detect")], "OPEN"),
    cell("P3", [("", "Answers carry the knowledge they rest on")], "OPEN"),
    cell("P3", [("", "No published entry")], "OPEN"),
    rowhead("Experiments", "Which experiment settles the most?", "directions settled per experiment"),
    cell(None, [("", "Needs the option to intervene")], "NOT APPLICABLE", dashed=True),
    cell("P3", [("Pool", f"Causal Chambers, {n('chambers.regimes')} recorded regimes"), ("Baselines", "CBED, pcalg opt.target"), ("Target", "beat random choice")], "DATA READY"),
    cell("P3", [("", "Knowledge suggests which pairs are worth testing")], "OPEN"),
    cell("P3", [("", "No published entry")], "OPEN"),
    rowhead("Harder settings", "Beyond Quarters 1 and 2", "the back slabs of projection 1", dashed=True),
    '<div style="grid-column: span 4; display: flex; flex-wrap: wrap; align-items: center; gap: 8px 24px; padding: 14px; background: #FFFFFF; border: 1.5px dashed #6A716B; border-radius: 10px; font-size: 14px; color: #4E5751">'
    + "".join(f"<span>{x}</span>" for x in ("Hidden common causes (PAG marks)", "Time series and lags", "100+ variables", "Feedback loops", "Counterfactuals for one unit", "Learned fusion of data and knowledge")) + "</div>",
]
matrix = ('<div style="overflow-x: auto"><div style="min-width: 1240px; display: grid; grid-template-columns: 200px repeat(4, minmax(0, 1fr)); gap: 10px">'
          + "\n".join(M) + "</div></div>")

legend = '<div style="display: flex; flex-direction: column; gap: 8px; flex: 1 1 320px; font-size: 13px; line-height: 18px">' + "".join(
    f'<span style="display: flex; align-items: center; gap: 8px"><span style="width: 18px; height: 14px; background: {PILLAR[p][1]}; border: 1.5px solid {PILLAR[p][0]}; border-radius: 3px"></span><b>{PILLAR[p][2]}</b> · {pc_line(p)}</span>'
    for p in ("P1", "P2", "P3")) + '<span style="display: flex; align-items: center; gap: 8px"><span style="width: 18px; height: 14px; background: #FFFFFF; border: 1.5px dashed #6A716B; border-radius: 3px"></span>Outside this project</span></div>'

SVGTXT = f"font-family: {SANS}"


# ---- section A: a worked example of what is discovered
def node(x, y, label, w=96):
    return (f'<rect x="{x - w/2}" y="{y - 16}" width="{w}" height="32" rx="16" fill="#FFFFFF" stroke="#17201B" stroke-width="1.5"/>'
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-size="14" fill="#17201B" style="{SVGTXT}">{label}</text>')


def edge(x1, y1, x2, y2, directed=True, colour="#17201B", k=0):
    mk = f' marker-end="url(#ah{k})"' if directed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="2"{mk}/>'


def marker(k, colour="#17201B"):
    return f'<marker id="ah{k}" orient="auto" markerWidth="8" markerHeight="8" refX="7" refY="4"><path d="M0 0 L8 4 L0 8 Z" fill="{colour}"/></marker>'


exA = f"""<svg viewBox="0 0 420 220" width="420" height="220" role="img" aria-label="Rain and Sprinkler both cause Wet road, which causes Skids">
<defs>{marker(1)}</defs>
{edge(92, 56, 178, 112, k=1)}{edge(328, 56, 242, 112, k=1)}{edge(210, 140, 210, 178, k=1)}
{node(70, 40, "Rain")}{node(350, 40, "Sprinkler")}{node(210, 126, "Wet road")}{node(210, 196, "Skids")}
</svg>"""
exB = f"""<svg viewBox="0 0 420 220" width="420" height="220" role="img" aria-label="A chain A, B, C whose directions observational data cannot settle">
<defs>{marker(2)}</defs>
{edge(116, 60, 168, 60, directed=False)}{edge(252, 60, 304, 60, directed=False)}
{node(70, 60, "A", 80)}{node(210, 60, "B", 80)}{node(350, 60, "C", 80)}
<text x="210" y="122" text-anchor="middle" font-size="13" fill="#4E5751" style="{SVGTXT}">three graphs fit the same data equally well:</text>
<text x="80" y="150" text-anchor="middle" font-size="14" fill="#17201B" style="font-family: {MONO}">A → B → C</text><text x="210" y="150" text-anchor="middle" font-size="14" fill="#17201B" style="font-family: {MONO}">A ← B ← C</text><text x="340" y="150" text-anchor="middle" font-size="14" fill="#17201B" style="font-family: {MONO}">A ← B → C</text>
<text x="210" y="184" text-anchor="middle" font-size="13" fill="#8E2A2A" style="{SVGTXT}">only A → B ← C is ruled out, because it is a collider</text>
</svg>"""

start = f"""<section style="display: flex; flex-direction: column; gap: 14px">
{h2("Start here: what is being discovered")}
<p style="margin: 0; max-width: 960px; color: #2C3631">A dataset has one column per variable. Causal discovery tries to recover the arrows between them: an arrow X → Y means that setting X from outside would change Y. Two sub-questions hide in every arrow: <b>are X and Y directly connected</b> (the skeleton) and <b>which way does it point</b> (the orientation). The two examples show why the second is harder.</p>
<div style="display: flex; flex-wrap: wrap; gap: 16px">
<figure style="flex: 1 1 440px; margin: 0; padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; display: flex; flex-direction: column; gap: 8px">
<div style="overflow-x: auto">{exA}</div>
<figcaption style="font-size: 14px; line-height: 20px"><b>Every direction recoverable.</b> Rain and Sprinkler are independent, but become dependent once you know the road is wet. That signature, a <i>collider</i>, fixes both arrows into Wet road. Skids is then forced: if it pointed into Wet road, Rain and Skids would form a second collider the data do not show.</figcaption>
</figure>
<figure style="flex: 1 1 440px; margin: 0; padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; display: flex; flex-direction: column; gap: 8px">
<div style="overflow-x: auto">{exB}</div>
<figcaption style="font-size: 14px; line-height: 20px"><b>No direction recoverable from the numbers.</b> All three graphs imply the same independence (A and C independent given B), so they form one <i>equivalence class</i>. Data alone can draw the skeleton A — B — C and no further. Only an experiment (set B, see whether A moves) or knowledge ("A is an input") orients it. On CausalArena's semantic scenarios {(1 - v("kappa.sem.D")):.1%} of edges are of this kind.</figcaption>
</figure>
</div>
</section>"""

# ---- section B: deriving the axes
axisQ = deriv("Axis Q · what is asked", [
    (f"Rung 1, <b>skeleton</b>: which pairs are directly connected. Scored by {m('S')}, the F1 over pairs.", ""),
    (f"Rung 2, <b>orientation</b>: which way each connection points. Scored by directed-edge F1, the scoreboard's number.", "needs rung 1: a direction is a property of a connection"),
    (f"Rung 3, <b>effects</b>: what happens to Y if we set X. Computing it needs X's parents (to adjust for them), so it needs the arrows into X.", "needs rung 2"),
    (f"Rung 4, <b>experiments</b>: which X to set next. The best choice is the one that settles the most directions still open after rung 2.", "needs rung 2's open set"),
    ("Because each rung consumes the one below, Q is an ordered axis, not a list of tasks, and a loss on a lower rung caps every rung above it.", ""),
])
axisR = deriv("Axis R · what may be read", [
    (f"Three kinds of evidence exist: the observational data <b>D</b>, interventional data <b>I</b>, declared knowledge <b>K</b>.", ""),
    (f"D is always present; I and K are each in or out, so there are {m('2 × 2 = 4')} regimes: D, D+I, D+K, D+I+K.", ""),
    ("Adding evidence can only raise the limit. D settles an equivalence class; I splits it further; correct K can collapse it to one graph.", "derived on Level 2"),
    ("K has a second coordinate the others lack: it can be <b>wrong</b>. So K is tested at three qualities, the name arms: real, neutral, swapped.", ""),
])
axisW = deriv("Axis W · what the world is like", [
    ("Five assumptions decide what is identifiable and how hard the statistics are: all common causes measured or not; independent rows or a time series; number of variables p; sample size n; form of the mechanisms.", ""),
    ("Q1 fixes one point: all variables observed, independent rows, p from 20 to 40, n = 1,000, mixed nonlinear mechanisms (CausalArena).", ""),
    ("For the picture, W is collapsed to four settings: the Q1 point, hidden common causes, time series, 100+ variables.", "the dashed row of the grid below"),
])
axes = f"""<section style="display: flex; flex-direction: column; gap: 14px">
{h2("Deriving the axes")}
<p style="margin: 0; max-width: 960px; color: #2C3631">A problem is a point {m('(q, r, w)')}: a question, the evidence allowed, and the kind of world. A system at that point returns a graph or an answer; scoring it gives a number; the <b>limit</b> {m('L(q, r, w)')} is the best number any system could reach there. Everything on this site is a measurement or a claim about some region of this space. A fourth axis, how an answer is scored, is derived on Level 2.</p>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 16px; align-items: start">{axisQ}{axisR}{axisW}</div>
</section>"""

# ---- section C: 3D projection
X0, Y0, CW, CH, DX, DY = 190, 600, 150, 80, 92, 62
QL = ["Skeleton", "Orientation", "Effects", "Experiments"]
RL = ["D", "D+I", "D+K", "D+I+K"]
WL = [("W1 · Q1 setting", "all observed, iid, 20–40 vars"),
      ("W2 · hidden common causes", "FCI baselines run (P1); PAG output"),
      ("W3 · time series", "one wrapper check (AUD-14)"),
      ("W4 · 100+ variables", "runtime only (CAP-12); E5")]
CELL = {  # (q, r): (fill, stroke, dash, line1, line2)
    (0, 0): ("#E6EEF6", "#1D5C99", "", "P1 · measured", "PC S " + t("pc.S")),
    (0, 1): ("#E6EEF6", "#1D5C99", "", "P1 · open", ""),
    (0, 2): ("#FBEFE4", "#B85A12", "", "P2 · agent measured", "S %s → %s" % (t("cc.real.S0.S", "{:.2f}"), t("cc.real.S3.S", "{:.2f}"))),
    (0, 3): ("#FBEFE4", "#B85A12", "", "P2 · open", ""),
    (1, 0): ("#E6EEF6", "#1D5C99", "", "P1 · limit " + t("lim.sem.D"), "best " + t("pub.sem.D.best")),
    (1, 1): ("#E6EEF6", "#1D5C99", "", "P1 · limit ≥ " + t("lim.sem.DI"), "best " + t("pub.sem.DI.best")),
    (1, 2): ("#FBEFE4", "#B85A12", "", "P2 · thesis cell", "limit 1.000 · none"),
    (1, 3): ("#FBEFE4", "#B85A12", "", "P2 · open", ""),
    (2, 0): ("#EFEAF6", "#5B3E8E", "", "P3 · surveyed", "IDA %s identified" % t("ida.identified", "{:.0%}")),
    (2, 1): ("#EFEAF6", "#5B3E8E", "", "P3 · open", ""),
    (2, 2): ("#EFEAF6", "#5B3E8E", "", "P3 · open", ""),
    (2, 3): ("#EFEAF6", "#5B3E8E", "", "P3 · open", ""),
    (3, 0): ("#FFFFFF", "#6A716B", "5 4", "not applicable", "needs I"),
    (3, 1): ("#EFEAF6", "#5B3E8E", "", "P3 · data ready", t("chambers.regimes") + " regimes"),
    (3, 2): ("#EFEAF6", "#5B3E8E", "", "P3 · open", ""),
    (3, 3): ("#EFEAF6", "#5B3E8E", "", "P3 · open", ""),
}


def P(r, q, w):
    return X0 + w * DX + r * CW, Y0 - w * DY - q * CH


svg = []
for w in (3, 2, 1):
    x, y = P(0, 4, w)
    op = 1 - 0.18 * w
    svg.append(f'<rect x="{x}" y="{y}" width="{4*CW}" height="{4*CH}" fill="#FFFFFF" fill-opacity="{op:.2f}" stroke="#6A716B" stroke-width="1.2" stroke-dasharray="5 4"/>')
    for r in range(1, 4):
        xa, _ = P(r, 0, w)
        svg.append(f'<line x1="{xa}" y1="{y}" x2="{xa}" y2="{y + 4*CH}" stroke="#C9CEC6" stroke-width="1"/>')
    for q in range(1, 4):
        _, ya = P(0, q, w)
        svg.append(f'<line x1="{x}" y1="{ya}" x2="{x + 4*CW}" y2="{ya}" stroke="#C9CEC6" stroke-width="1"/>')
    t, d = WL[w]
    svg.append(f'<text x="{x + 10}" y="{y + 22}" font-size="13" font-weight="600" fill="#4E5751" style="{SVGTXT}">{t}</text>')
    svg.append(f'<text x="{x + 10}" y="{y + 40}" font-size="12" fill="#4E5751" style="{SVGTXT}">{d}</text>')
# depth edges
for r, q in ((0, 4), (4, 4), (4, 0)):
    xa, ya = P(r, q, 0)
    xb, yb = P(r, q, 3)
    svg.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="#6A716B" stroke-width="1.2" stroke-dasharray="3 3"/>')
# front slab
for (q, r), (fill, stroke, dash, l1, l2) in CELL.items():
    x, y = P(r, q + 1, 0)
    thick = 3 if (q, r) == (1, 2) else 1.5
    da = f' stroke-dasharray="{dash}"' if dash else ""
    svg.append(f'<rect x="{x + 3}" y="{y + 3}" width="{CW - 6}" height="{CH - 6}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{thick}"{da}/>')
    svg.append(f'<text x="{x + 14}" y="{y + 34}" font-size="13" font-weight="600" fill="#17201B" style="{SVGTXT}">{l1}</text>')
    if l2:
        svg.append(f'<text x="{x + 14}" y="{y + 54}" font-size="12" fill="#2C3631" style="{SVGTXT}">{l2}</text>')
for q, lab in enumerate(QL):
    _, y = P(0, q, 0)
    svg.append(f'<text x="{X0 - 12}" y="{y - CH/2 + 5}" text-anchor="end" font-size="14" font-weight="600" fill="#17201B" style="{SVGTXT}">{lab}</text>')
for r, lab in enumerate(RL):
    x, _ = P(r, 0, 0)
    svg.append(f'<text x="{x + CW/2}" y="{Y0 + 24}" text-anchor="middle" font-size="14" font-weight="600" fill="#17201B" style="{SVGTXT}">{lab}</text>')
svg.append(f'<text x="{X0 - 12}" y="{Y0 - 4*CH - 14}" text-anchor="end" font-size="13" fill="#4E5751" style="{SVGTXT}">Q · asked ↑</text>')
svg.append(f'<text x="{X0 + 2*CW}" y="{Y0 + 50}" text-anchor="middle" font-size="13" fill="#4E5751" style="{SVGTXT}">R · evidence allowed →</text>')
xa, ya = P(4, 0, 0)
xb, yb = P(4, 0, 3)
svg.append(f'<text x="{(xa + xb)/2 + 16}" y="{(ya + yb)/2 + 18}" font-size="13" fill="#4E5751" style="{SVGTXT}">W · world ↗</text>')
cube = f"""<svg viewBox="0 0 1300 670" width="1300" height="670" role="img" aria-label="Three-dimensional view of the space: question by evidence by world setting">{''.join(svg)}</svg>"""

proj3 = f"""<section style="display: flex; flex-direction: column; gap: 12px">
{h2("Projection 1 · the whole space, Q × R × W")}
<p style="margin: 0; max-width: 960px; color: #2C3631">The front slab is the Q1 setting, filled in from the evidence. The slabs behind it are the same 4 × 4 grid in harder worlds; each says the one thing we have touched there. The thick cell is the thesis cell: orientation with declared knowledge, where no published method reports a number.</p>
<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; padding: 8px 0">{cube}</div>
</section>"""

proj2 = f"""<section style="display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 16px 40px">
<div style="display: flex; flex-direction: column; gap: 6px; flex: 999 1 560px">
{h2("Projection 2 · Q × R at the Q1 setting")}
<p style="margin: 0; max-width: 820px; color: #2C3631">The front slab opened up. Each cell holds the limit, the best published result and what we measured.</p>
</div>
{legend}
</div>
{matrix}
</section>"""

carve = f"""<section style="display: flex; flex-direction: column; gap: 12px">
{h2("How the pillars carve the space")}
<p style="margin: 0; max-width: 960px; color: #2C3631">The cut follows axis Q because it is nested: nothing on rung 3 or 4 can be claimed before rung 2 is. Within rungs 1–2 it follows axis R, because the K columns are where no published system exists.</p>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 12px">
<div style="padding: 14px 16px; background: #E6EEF6; border: 1.5px solid #1D5C99; border-radius: 10px; font-size: 14px; line-height: 20px">{tag("P1 Measurement", "#1D5C99")}<p style="margin: 6px 0 0">{m("{skeleton, orientation} × {D, D+I}")}, plus controlled audits of existing agents wherever they run. Question it answers: where does each system's direction come from, and how far is it from the limit?</p></div>
<div style="padding: 14px 16px; background: #FBEFE4; border: 1.5px solid #B85A12; border-radius: 10px; font-size: 14px; line-height: 20px">{tag("P2 Claim ledger", "#9A4A0E")}<p style="margin: 6px 0 0">{m("{skeleton, orientation} × {D+K, D+I+K}")}, with interventions entering as order evidence. Question: can a system use knowledge on purpose, say where each direction came from, and never fall below its data?</p></div>
<div style="padding: 14px 16px; background: #EFEAF6; border: 1.5px solid #5B3E8E; border-radius: 10px; font-size: 14px; line-height: 20px">{tag("P3 Decisions", "#5B3E8E")}<p style="margin: 6px 0 0">{m("{effects, experiments} × all R")}. Question: do better directions turn into better answers to "what if we set X" and better choices of experiment?</p></div>
</div>
</section>"""

body = "\n".join([
    title_block("The space of causal discovery and analysis",
                "Three axes define every problem here: what is asked, what evidence may be read, and what the world is like. This level derives them, shows the whole space in three dimensions, then opens the slice Q1 works in."),
    start, axes, proj3, proj2, carve,
    terms_panel(["variable", "dag", "adjacency", "skeleton", "orientation", "ci", "mec", "cpdag", "compelled", "collider",
                 "faithful", "sufficient", "pag", "intervention", "knowledge", "tier", "regime", "arena", "arms", "leak"]),
    footer("the D column is measured and its limit is known. The thesis cell, orientation with declared knowledge, has a measured agent and no system of ours yet. Of the harder worlds, only hidden common causes has been touched.",
           "fill the D+K column with a ledger that never drops below the D column, then the D+I column, then decisions; the back slabs wait for Q2 and beyond.",
           "Bounds.dc.html", "Derive the limits"),
    '<p style="margin: 0; font-size: 13px; color: #4E5751">Numbers: CausalArena semantic family, public half, unless stated. Directed F1 uses the scoreboard\'s forced-choice rule. Causal-Copilot rows are its 10 S2 test scenarios at the stage before the cycle step. Every number links to its evidence file in the live site.</p>',
])
BODY = body
ZOOM = "Zoomed out: the whole space"
TITLE = "1 Space"
