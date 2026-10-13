"""Shared pieces for the Atlas level boards."""

SANS = "'IBM Plex Sans', 'Helvetica Neue', sans-serif"
COND = "'IBM Plex Sans Condensed', 'Arial Narrow', sans-serif"
MONO = "'IBM Plex Mono', monospace"

PILLAR = {
    "P1": ("#1D5C99", "#E6EEF6", "P1 Measurement"),
    "P2": ("#9A4A0E", "#FBEFE4", "P2 Claim ledger"),
    "P3": ("#5B3E8E", "#EFEAF6", "P3 Decisions"),
}

STATUS = {
    # key: (background, border, label colour, border style)
    "done": ("#E6EEF6", "#1D5C99", "#1D5C99", "solid"),
    "prog": ("#FBEFE4", "#B85A12", "#9A4A0E", "solid"),
    "dec": ("#F6E7E7", "#8E2A2A", "#8E2A2A", "solid"),
    "todo": ("#FFFFFF", "#6A716B", "#4E5751", "dashed"),
    "p3": ("#EFEAF6", "#5B3E8E", "#5B3E8E", "solid"),
    "gap": ("#FFFFFF", "#8E2A2A", "#8E2A2A", "dashed"),
}

LEVELS = [("Main.dc.html", "1 Space"), ("Bounds.dc.html", "2 Bounds"), ("Theses.dc.html", "3 Theses"),
          ("Bundles.dc.html", "4 Bundles"), ("Stages.dc.html", "5 Stages")]


def page(title, current, zoom_note, height, body):
    nav = []
    for href, label in LEVELS:
        if href == current:
            nav.append(f'<a href="{href}" aria-current="page" style="padding: 11px 14px; border-radius: 22px; background: #17201B; color: #FFFFFF; text-decoration: none">{label}</a>')
        else:
            nav.append(f'<a href="{href}" style="padding: 11px 14px; border-radius: 22px; color: #17201B; text-decoration: none">{label}</a>')
    nav.append('<span style="padding: 11px 14px; color: #6A716B">6 Tickets</span>')
    nav.append('<span style="padding: 11px 14px; color: #6A716B">7 Evidence</span>')
    nav = "\n".join(nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&amp;family=IBM+Plex+Sans+Condensed:wght@500;600;700&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;display=swap">
<style>
body{{margin:0;background:#F2F3EF}}
a{{color:#1D5C99}}a:hover{{color:#123E69}}
</style>
</helmet>
<div style="min-height: {height}px; display: flex; flex-direction: column; background: #F2F3EF; color: #17201B; font-family: {SANS}; font-size: 15px; line-height: 22px">

<header style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 28px; padding: 14px 24px; border-bottom: 1px solid #C9CEC6; background: #FFFFFF">
<span style="font-family: {COND}; font-size: 24px; line-height: 30px; font-weight: 700">Causal Atlas</span>
<nav aria-label="Zoom level" style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px; font-size: 14px">
{nav}
</nav>
<span style="margin-left: auto; font-size: 13px; line-height: 18px; color: #4E5751">{zoom_note}<br>snapshot [COMMIT] · 12 Oct</span>
</header>

<main style="flex: 1 1 auto; box-sizing: border-box; padding: 32px 24px 40px">
<div style="max-width: 1360px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px">
{body}
</div>
</main>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{height}}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
"""


def title_block(h1, sub):
    return f"""<div style="display: flex; flex-direction: column; gap: 8px">
<h1 style="margin: 0; font-family: {COND}; font-size: 44px; line-height: 50px">{h1}</h1>
<p style="margin: 0; max-width: 900px; font-size: 17px; line-height: 26px; color: #2C3631">{sub}</p>
</div>"""


def h2(text, extra=""):
    return f'<h2 style="margin: 0; font-family: {COND}; font-size: 26px; line-height: 32px">{text}</h2>{extra}'


def tag(text, colour):
    return f'<span style="font-size: 12px; line-height: 16px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: {colour}">{text}</span>'


def pill(text, status):
    bg, bd, fg, style = STATUS[status]
    return f'<span style="display: inline-block; padding: 2px 10px; border-radius: 12px; border: 1.5px {style} {bd}; background: {bg}; color: {fg}; font-size: 12px; line-height: 18px; font-weight: 600">{text}</span>'


def footer(now, going, link_href, link_text):
    return f"""<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 16px">
<p style="margin: 0; padding: 16px 20px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 10px"><b>Where we are now:</b> {now}</p>
<p style="margin: 0; padding: 16px 20px; background: #17201B; color: #F2F3EF; border-radius: 10px"><b>Where we're going:</b> {going} <a href="{link_href}" style="color: #9CC7F0">{link_text}</a></p>
</div>"""


_arrow_n = [0]


def arrow_h(x, y, n, colour="#4E5751"):
    _arrow_n[0] += 1
    k = _arrow_n[0]
    return (f'<svg width="{n}" height="8" viewBox="0 0 {n} 8" preserveAspectRatio="none" style="position: absolute; left: {x}px; top: {y-4}px; width: {n}px; height: 8px; overflow: visible; fill: none; stroke: {colour}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round">'
            f'<defs><marker id="dc-arrow-head-filled-{k}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible"><path d="M0 0 L4 2 L0 4 Z" fill="{colour}" stroke="none" style="stroke: none; fill: {colour}; fill: context-stroke"/></marker></defs>'
            f'<path d="M 0 4 L {n-4} 4" marker-end="url(#dc-arrow-head-filled-{k})"></path></svg>')


def arrow_v(x, y, n, colour="#4E5751"):
    _arrow_n[0] += 1
    k = _arrow_n[0]
    return (f'<svg width="8" height="{n}" viewBox="0 0 8 {n}" preserveAspectRatio="none" style="position: absolute; left: {x-4}px; top: {y}px; width: 8px; height: {n}px; overflow: visible; fill: none; stroke: {colour}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round">'
            f'<defs><marker id="dc-arrow-head-filled-{k}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible"><path d="M0 0 L4 2 L0 4 Z" fill="{colour}" stroke="none" style="stroke: none; fill: {colour}; fill: context-stroke"/></marker></defs>'
            f'<path d="M 4 0 L 4 {n-4}" marker-end="url(#dc-arrow-head-filled-{k})"></path></svg>')


# ---------------------------------------------------------------- terms
TERMS = {
    "variable": ("Variable", "One measured quantity: one column of the data file."),
    "dag": ("Causal graph (DAG)", "Arrows X → Y meaning: setting X from outside would change Y with everything else held fixed. No loops, so it is a directed acyclic graph."),
    "adjacency": ("Edge, adjacency", "A direct connection between two variables, ignoring which way it points."),
    "skeleton": ("Skeleton", "The graph with arrowheads removed: only which pairs are adjacent."),
    "orientation": ("Orientation, direction", "Which way an edge points. The scoreboard counts an edge only if both the pair and the direction are right."),
    "ci": ("Conditional independence", "X and Y tell you nothing more about each other once Z is known. Observational data reveal these and nothing else about structure."),
    "mec": ("Equivalence class", "All graphs that imply exactly the same conditional independencies. Observational data cannot tell its members apart."),
    "cpdag": ("CPDAG", "One picture of an equivalence class: an arrow where every member agrees, an undirected edge where they disagree."),
    "compelled": ("Compelled edge, κ", "An edge whose direction is the same in every graph of the equivalence class. κ is the share of edges that are compelled."),
    "collider": ("Collider (v-structure)", "X → Z ← Y with X and Y not adjacent. The pattern observational data can orient; the propagation rules then orient more."),
    "faithful": ("Faithfulness", "Every independence in the data comes from the graph, none from causes cancelling out. Needed for any limit on this page."),
    "sufficient": ("Causal sufficiency", "Every common cause of two measured variables is itself measured. When it fails, methods output a PAG instead of a CPDAG."),
    "pag": ("PAG", "The output of FCI when hidden common causes are allowed; a circle mark means the end is not determined."),
    "intervention": ("Intervention (I)", "Data recorded after a variable was set from outside. Everything downstream of the target can shift; nothing upstream can."),
    "knowledge": ("Declared knowledge (K)", "Information not in the numbers: variable names, or tiers such as 'these are inputs'. Legitimate when declared; a leak when silent."),
    "tier": ("Tier, partial order", "Groups of variables where an earlier group may cause a later one but never the reverse. Pairs inside a tier stay unordered."),
    "regime": ("Information regime", "Which evidence a system may read: D (data), I (interventions), K (knowledge). D is always present, so there are four."),
    "arena": ("CausalArena", "The public scoreboard we audit: 100 scenarios per family (semantic: realistic named systems; formula: physical laws), 50 public, 1,000 rows each."),
    "arms": ("Name arms", "Controls on the names an agent sees: real, neutral (V1, V2, …) and swapped (real names moved to other columns)."),
    "leak": ("Layout leak", "The released files list columns in causal order, so a method that reads column positions gets the order for free (0.680)."),
    "prf": ("Precision, recall, F1", "Precision: share of claimed edges that are true. Recall: share of true edges claimed. F1 = 2PR/(P+R), their harmonic mean."),
    "S": ("S, skeleton F1", "F1 over adjacencies. Measures only whether the right pairs are connected."),
    "c": ("c, commit rate", "Of the true adjacencies a system found, the share it gave a direction to (right or wrong)."),
    "q": ("q, commit accuracy", "Of those committed directions, the share that are right. A coin scores 0.5."),
    "a": ("a, direction accuracy", "a = c·q + (1−c)/2: the share of found adjacencies pointing the right way once undecided ones are oriented at random."),
    "forced": ("Forced choice", "The scoreboard's rule: every undecided pair is given a direction (at random here). Published numbers use it."),
    "strict": ("Strict scoring", "Undecided pairs count as no prediction. Our stage-by-stage numbers for Causal-Copilot used it; this page shows both."),
    "limit": ("Limit (ceiling)", "The best score any method could reach with perfect statistics, given only the evidence its regime allows."),
    "oracle": ("Oracle", "A hypothetical input taken from the true graph, used to price a piece of information, never as a method."),
    "budget": ("Error budget", "1 − F1 split into named losses: not identifiable, wrong skeleton, wrong directions."),
    "iso": ("Iso-F1 curve", "All (S, a) points with the same directed F1: a = F1 / S."),
    "thesis": ("Thesis", "A claim we commit to, with what would refute it written down before the evidence comes in."),
    "invariant": ("Invariant", "A property every run of our system must satisfy, checked as a test rather than hoped for."),
    "ledger": ("Claim ledger", "Our planned system: every direction is stored with its source (data pattern, intervention or knowledge) and re-derived by a checker."),
    "calib": ("Calibration", "A claim tagged 80% is right 80% of the time across many claims."),
    "abstain": ("Abstention", "Declining to commit a direction. Under forced choice it is worth exactly ½ per pair, so it pays whenever q < ½."),
    "ident": ("Identified effect", "Data plus graph pin the effect of setting X down to one value, rather than a set of possible values."),
    "ida": ("IDA", "Computes the possible effects of X on Y over every graph in the equivalence class; one value means identified."),
    "gate": ("Gate", "A dated decision point with a pre-stated test (G1–G4)."),
    "bundle": ("Bundle", "A unit of work that closes a set of tickets and is checkable in one run, with a must-show list."),
    "ticket": ("Ticket", "One tracked item (REP, AUD, CAP, BLD, TGT, …) with a criterion and evidence files; mirrored to both Slack lists."),
    "live": ("LIVE / free", "LIVE bundles spend model calls through your key and are started only by you; free ones run locally at no cost."),
    "stages": ("Stages S0–S4", "Causal-Copilot's pipeline: S0 algorithm output, S1 bootstrap filter, S2 model review using names, S3 KCI pruning, S4 cycle step."),
    "bootstrap": ("Bootstrap", "Rerunning the algorithm on resampled rows; an edge's bootstrap frequency is the share of reruns that keep it."),
    "kci": ("KCI", "Kernel conditional independence test; Causal-Copilot uses it to prune edges after the model review."),
}


def terms_panel(keys, title="Terms on this level"):
    cells = []
    for k in keys:
        name, d = TERMS[k]
        cells.append(f'<div style="display: flex; flex-direction: column; gap: 2px"><dt style="font-weight: 600">{name}</dt><dd style="margin: 0; color: #2C3631">{d}</dd></div>')
    return f"""<section style="display: flex; flex-direction: column; gap: 12px; padding: 18px 20px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
{tag(title, "#17201B")}
<dl style="margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px 24px; font-size: 14px; line-height: 20px">{''.join(cells)}</dl>
</section>"""


def deriv(title, steps, note=""):
    """A numbered derivation block. steps: list of (statement, justification) html strings."""
    def _just(j):
        return ' <span style="color: #4E5751">— %s</span>' % j if j else ""
    lis = "".join(f'<li style="display: grid; grid-template-columns: 28px 1fr; gap: 8px"><span style="font-family: {MONO}; font-weight: 600; color: #4E5751">{i}</span><span>{s}{_just(j)}</span></li>' for i, (s, j) in enumerate(steps, 1))
    n = f'<p style="margin: 0; font-size: 13px; line-height: 18px; color: #4E5751">{note}</p>' if note else ""
    return f"""<section style="display: flex; flex-direction: column; gap: 10px; padding: 18px 20px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
<h3 style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px">{title}</h3>
<ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 15px; line-height: 22px">{lis}</ol>
{n}
</section>"""


def m(x):
    """Inline math-ish span."""
    return f'<span style="font-family: {MONO}; font-size: 14px; background: #F2F3EF; padding: 1px 5px; border-radius: 4px">{x}</span>'


# ---------------------------------------------------------------- snapshot access (site build)
SNAP = {}          # set by site/build.py before the level modules are imported
EVBASE = [""]      # prefix for evidence links, e.g. https://github.com/<owner>/cc-research/blob/<sha>/
USED = set()       # registry keys the page printed (build reports unused and missing ones)


def v(key):
    """Raw value of a registry number."""
    USED.add(key)
    return SNAP["metrics"][key]["value"]


def fmt(val, spec=None):
    if spec:
        return spec.format(val)
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, int) or float(val).is_integer() and abs(val) >= 2:
        return "{:,}".format(int(val))
    return "{:.3f}".format(val)


def n(key, spec=None, bold=False):
    """A registry number as text, linked to the file it comes from."""
    val = fmt(v(key), spec)
    src = SNAP["metrics"][key]["src"]
    inner = "<b>%s</b>" % val if bold else val
    return f'<a class="ev" href="{EVBASE[0]}{src}" title="{key} · {src}">{inner}</a>'


def t(key, spec=None):
    """A registry number as plain text (for SVG and attributes)."""
    return fmt(v(key), spec)


def pillar_counts():
    c = {}
    for i in SNAP["items"]:
        d = c.setdefault(i["pillar"], {"n": 0, "done": 0, "in_progress": 0})
        d["n"] += 1
        d["done"] += i["status"] == "done"
        d["in_progress"] += i["status"] == "in_progress"
    return c


def pc_line(p):
    c = pillar_counts()[p]
    extra = " · %d in progress" % c["in_progress"] if c["in_progress"] else ""
    return "%d of %d items done%s" % (c["done"], c["n"], extra)


def item(item_id):
    return next(i for i in SNAP["items"] if i["id"] == item_id)


def bundle(bid):
    return next(b for b in SNAP["bundles"] if b["id"] == bid)


STATUS_OF = {"done": "done", "in_progress": "prog", "todo": "todo", "blocked": "dec", "open": "todo", "reopened": "dec"}
STATUS_TEXT = {"done": "done", "in_progress": "in progress", "todo": "to do", "blocked": "blocked", "open": "open", "reopened": "reopened"}
