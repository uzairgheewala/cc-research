"""Page 3: the space of problems. Act I: axes, the 3D view and the Q x R grid with limits and published numbers only
(our measurements and the pillars come later)."""
from pagekit import *  # noqa: F401,F403
from common import deriv, m

axisQ = deriv("Axis Q · what is asked", [
    ("Rung 1, <b>skeleton</b>: which pairs are directly connected (scored by S).", ""),
    ("Rung 2, <b>orientation</b>: which way each connection points (directed F1, the leaderboard's number).",
     "needs rung 1: a direction is a property of a connection"),
    ("Rung 3, <b>effects</b>: what happens to Y if we set X. Computing it needs X's parents, so it needs the arrows into X.", "needs rung 2"),
    ("Rung 4, <b>experiments</b>: which X to set next. The best choice settles the most directions still open after rung 2.",
     "needs rung 2's open set"),
    ("Each rung consumes the one below, so Q is an ordered axis: a loss on a lower rung caps every rung above it.", ""),
])
axisR = deriv("Axis R · what may be read", [
    ("Three kinds of evidence: observational data <b>D</b>, interventional data <b>I</b>, declared knowledge <b>K</b>.", ""),
    (f"D is always present; I and K are each in or out, so there are {m('2 × 2 = 4')} regimes.", ""),
    ("Adding evidence can only raise the limit: D settles an equivalence class, I splits it further, correct K can collapse it "
     "to one graph.", "page 2"),
    (f"K has a second coordinate the others lack: it can be <b>wrong</b>. So K is tested at three qualities, the "
     f"{T('arms')}: real names, neutral names (V01, V02, …) and swapped names (real names moved to other columns).", ""),
])
axisW = deriv("Axis W · what the world is like", [
    (f"Five assumptions decide what can be identified and how hard the statistics are: whether every common cause is measured "
     f"({T('sufficient', 'causal sufficiency')}); independent rows or a time series; the number of variables; the number of "
     f"rows; the form of the mechanisms.", ""),
    (f"This project first works at one point, {T('q1')}: all variables observed, independent rows, 20-40 variables, 1,000 rows, "
     f"mixed nonlinear mechanisms, as in CausalArena.", ""),
    (f"With hidden common causes, methods return a {T('pag')} instead of a CPDAG. For the picture, W is collapsed to four "
     f"settings: the Q1 setting, hidden common causes, time series, and 100+ variables.", ""),
])

# ---- the 3D view, with neutral cells (limits and published numbers only)
X0, Y0, CW, CH, DX, DY = 190, 600, 150, 80, 92, 62
QL = ["Skeleton", "Orientation", "Effects", "Experiments"]
RL = ["D", "D+I", "D+K", "D+I+K"]
WL = [("Q1 setting", "all observed, iid, 20–40 vars"), ("hidden common causes", "PAG output"),
      ("time series", "lags, autocorrelation"), ("100+ variables", "runtime and statistics")]
NEUT, GREY = ("#FFFFFF", "#6A716B")
CELL = {
    (0, 0): ("limit 1.000", "with unlimited rows"), (0, 1): ("limit 1.000", ""), (0, 2): ("limit 1.000", "K never connects"),
    (0, 3): ("limit 1.000", ""),
    (1, 0): ("limit " + t("lim.sem.D"), "best published " + t("pub.sem.D.best")),
    (1, 1): ("limit ≥ " + t("lim.sem.DI"), "best published " + t("pub.sem.DI.best")),
    (1, 2): ("limit 1.000", "no published method"), (1, 3): ("limit 1.000", "no published method"),
    (2, 0): ("identified or not", "per pair"), (2, 1): ("beat regression", ""), (2, 2): ("open", ""), (2, 3): ("open", ""),
    (3, 0): ("not applicable", "needs I"), (3, 1): ("beat random", "choice of target"), (3, 2): ("open", ""), (3, 3): ("open", ""),
}
TXT = f"font-family: {SANS}"


def Pt(r, q, w):
    return X0 + w * DX + r * CW, Y0 - w * DY - q * CH


svg = []
for w in (3, 2, 1):
    x, y = Pt(0, 4, w)
    svg.append(f'<rect x="{x}" y="{y}" width="{4*CW}" height="{4*CH}" fill="#FFFFFF" fill-opacity="{1 - 0.18 * w:.2f}" stroke="#6A716B" stroke-width="1.2" stroke-dasharray="5 4"/>')
    for r in range(1, 4):
        xa, _ = Pt(r, 0, w)
        svg.append(f'<line x1="{xa}" y1="{y}" x2="{xa}" y2="{y + 4*CH}" stroke="#C9CEC6" stroke-width="1"/>')
    for q in range(1, 4):
        _, ya = Pt(0, q, w)
        svg.append(f'<line x1="{x}" y1="{ya}" x2="{x + 4*CW}" y2="{ya}" stroke="#C9CEC6" stroke-width="1"/>')
    a, b = WL[w]
    svg.append(f'<text x="{x + 10}" y="{y + 22}" font-size="13" font-weight="600" fill="#4E5751" style="{TXT}">{a}</text>')
    svg.append(f'<text x="{x + 10}" y="{y + 40}" font-size="12" fill="#4E5751" style="{TXT}">{b}</text>')
for r, q in ((0, 4), (4, 4), (4, 0)):
    xa, ya = Pt(r, q, 0)
    xb, yb = Pt(r, q, 3)
    svg.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="#6A716B" stroke-width="1.2" stroke-dasharray="3 3"/>')
for (q, r), (l1, l2) in CELL.items():
    x, y = Pt(r, q + 1, 0)
    dash = ' stroke-dasharray="5 4"' if l1 == "not applicable" else ""
    svg.append(f'<rect x="{x + 3}" y="{y + 3}" width="{CW - 6}" height="{CH - 6}" rx="6" fill="{NEUT}" stroke="{GREY}" stroke-width="1.5"{dash}/>')
    svg.append(f'<text x="{x + 14}" y="{y + 34}" font-size="13" font-weight="600" fill="#17201B" style="{TXT}">{l1}</text>')
    if l2:
        svg.append(f'<text x="{x + 14}" y="{y + 54}" font-size="12" fill="#2C3631" style="{TXT}">{l2}</text>')
for q, lab in enumerate(QL):
    _, y = Pt(0, q, 0)
    svg.append(f'<text x="{X0 - 12}" y="{y - CH/2 + 5}" text-anchor="end" font-size="14" font-weight="600" fill="#17201B" style="{TXT}">{lab}</text>')
for r, lab in enumerate(RL):
    x, _ = Pt(r, 0, 0)
    svg.append(f'<text x="{x + CW/2}" y="{Y0 + 24}" text-anchor="middle" font-size="14" font-weight="600" fill="#17201B" style="{TXT}">{lab}</text>')
svg.append(f'<text x="{X0 - 12}" y="{Y0 - 4*CH - 14}" text-anchor="end" font-size="13" fill="#4E5751" style="{TXT}">Q · asked ↑</text>')
svg.append(f'<text x="{X0 + 2*CW}" y="{Y0 + 50}" text-anchor="middle" font-size="13" fill="#4E5751" style="{TXT}">R · evidence allowed →</text>')
xa, ya = Pt(4, 0, 0)
xb, yb = Pt(4, 0, 3)
svg.append(f'<text x="{(xa + xb)/2 + 16}" y="{(ya + yb)/2 + 18}" font-size="13" fill="#4E5751" style="{TXT}">W · world ↗</text>')
cube = f'<svg viewBox="0 0 1300 670" width="1300" height="670" role="img" aria-label="The space of problems: question by evidence by world">{"".join(svg)}</svg>'

EXT = ["Hidden common causes", "Time series and lags", "100+ variables", "Feedback loops", "Counterfactuals for one unit",
       "Learned fusion of data and knowledge"]
_pill = '<span style="padding: 6px 12px; border: 1.5px dashed #6A716B; border-radius: 16px; background: #FFFFFF; font-size: 14px">%s</span>'
EXT_HTML = '<div style="display: flex; flex-wrap: wrap; gap: 8px">' + "".join(_pill % x for x in EXT) + "</div>"

BODY = "\n".join([
    question("Which problems exist, and which one does this project work in?",
             before=f'{link("scoring", "page 2")}: S × a, the regimes D, D+I, D+K, D+I+K, and the limit of each.'),
    P("A causal discovery problem is a point with three coordinates: what is asked, what evidence may be read, and what kind of "
      "world produced the data. A method at that point returns a graph or an answer; scoring it gives a number; the limit is the "
      "best number any method could reach there. Every result on this site is a measurement or a claim about some region of this "
      "space."),
    f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(380px, 100%), 1fr)); gap: 16px; align-items: start">{axisQ}{axisR}{axisW}</div>',
    H2("The whole space"),
    P("The front slab is the Q1 setting, with the limit of each cell from page 2 and the best published number where one exists. "
      "The slabs behind it are the same grid in harder worlds. The upper rungs and the knowledge columns are mostly empty: no "
      "published method reports a number there."),
    figure(cube, "Q × R × W. Front slab: the Q1 setting. Orientation with declared knowledge (row 2, column D+K) has a limit of "
                 "1.000 if the knowledge is right, and no published method."),
    H2("Beyond the first setting"),
    P("Not planned for now, listed so the edge of the space is visible:"),
    EXT_HTML,
    answer("The leaderboard covers one cell of a larger grid: orientation, from data alone, in the simplest world. The cells "
           "above it (effects, experiments) and to its right (interventions, knowledge) are where the published field is thin.",
           "Inside the one cell the leaderboard does cover, do its numbers measure the methods, or something else?"),
])
