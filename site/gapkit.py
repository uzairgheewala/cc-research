"""Site v3 (s24, TEAM-10): the gap model behind Today, the gaps page, the story strips and the explorer.

Reads site/gaps_spec.json and site/deliverables.json; every value comes from the snapshot through the registry keys the
spec names. The gap type of a landmark is derived here, never written by hand:

  no binding value                                     -> reach
  board's ruler verdict is not "same"                  -> comparability (the derived value type is kept beside it)
  conservative end clears the bar                      -> met
  point clears, conservative end does not, and the
    interval need shrink by at most sqrt(max_factor)   -> measurement (with an estimate of the cases needed)
  otherwise                                            -> method

Explanation segments come from the explanation ledger (B1; shared record {board, gap, segment, size, unit, state, ticket,
report}) when the registry holds it; until then each gap is one "attributed" segment of its anatomy total.
Design: project doc claude/site-v3-design-2026-10-20.md.
"""
import html
import json
import math
from pathlib import Path

import common

HERE = Path(__file__).resolve().parent
SPEC = json.load(open(HERE / "gaps_spec.json", encoding="utf-8"))
DELIV = json.load(open(HERE / "deliverables.json", encoding="utf-8"))
RULES = SPEC["rules"]
TYPES = RULES["type_order"]
STATES = RULES["states"]
PLAIN = SPEC["plain"]
LM = SPEC["landmarks"]
BOARDS = {b["id"]: b for b in SPEC["boards"]}
GAPS = SPEC["gaps"]

TYPE_STYLE = {  # (text, background, border, border style)
    "met": ("#1D5C99", "#E6EEF6", "#1D5C99", "solid"),
    "measurement": ("#9A4A0E", "#FBEFE4", "#B85A12", "solid"),
    "method": ("#8E2A2A", "#F6E7E7", "#8E2A2A", "solid"),
    "comparability": ("#5B3E8E", "#EFEAF6", "#5B3E8E", "solid"),
    "reach": ("#4E5751", "#FFFFFF", "#6A716B", "dashed"),
}
STATE_COLOUR = {"unattributed": "#E3E6E0", "attributed": "#B9BFB6", "mechanism_known": "#8FB8E0", "walled": "#5E6660",
                "lever_disputed": "#E2A15F", "lever_chosen": "#1D5C99", "acted_on": "#1F6B45"}
STATE_INK = {"unattributed": "#17201B", "attributed": "#17201B", "mechanism_known": "#0B2E4F", "walled": "#FFFFFF",
             "lever_disputed": "#3D1F05", "lever_chosen": "#FFFFFF", "acted_on": "#FFFFFF"}
PROBLEMS = []          # spec / ledger problems; site/build.py turns them into errors
NOTES = []             # informational (e.g. a ticket the tracker does not have yet)


def esc(x):
    return html.escape(str(x), quote=True)


# ------------------------------------------------------------------ values
def why(text):
    """Spec prose with {registry.key} placeholders: each becomes the linked registry number (no figure is typed in the spec)."""
    import re as _re
    return _re.sub(r"\{([A-Za-z0-9_.\-]+)\}", lambda m: common.n(m.group(1)), esc(text))


def has(key):
    return key in common.SNAP.get("metrics", {})


def val(key):
    return common.v(key) if key else None


def ev(key, text):
    """An evidence link for a value that lives inside one registry entry (a ledger row): same markup as common.n."""
    common.USED.add(key)
    src = common.SNAP["metrics"][key]["src"]
    return f'<a class="ev" href="{common.EVBASE[0]}{src}" title="{key} · {src}">{esc(text)}</a>'


def fmt(x, spec):
    return spec.format(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else str(x)


def num(key, spec):
    return common.n(key, spec if spec != "{:,}" else None)


# ------------------------------------------------------------------ derivation
def _clears(x, bar, d, strict):
    if d == "higher":
        return x > bar if strict else x >= bar
    return x < bar if strict else x <= bar


def part_bar(p):
    if "bar_key" in p:
        return val(p["bar_key"]) + p.get("bar_offset", 0.0)
    return p.get("bar")


def derive_part(p, max_factor=None):
    """One measured part of a landmark -> dict(type, value, cons, bar, factor, n_needed)."""
    max_factor = RULES["measurement_max_factor"] if max_factor is None else max_factor
    bar = part_bar(p)
    if p.get("value") is None or not has(p["value"]):
        return {"type": "reach", "x": None, "c": None, "bar_v": bar}
    x = val(p["value"])
    c = val(p["cons"]) if p.get("cons") else x
    out = {"x": x, "c": c, "bar_v": bar, "factor": None, "n_needed": None, "n_now": None}
    if _clears(c, bar, p["dir"], p.get("strict", False)):
        out["type"] = "met"
        return out
    if not _clears(x, bar, p["dir"], p.get("strict", False)) or c == x:
        out["type"] = "method"
        return out
    half, margin = abs(x - c), abs(x - bar)
    factor = (half / margin) ** 2 if margin > 0 else math.inf
    out["factor"] = factor
    if p.get("n") and has(p["n"]):
        out["n_now"] = val(p["n"])
        out["n_needed"] = int(math.ceil(out["n_now"] * factor))
    out["type"] = "measurement" if factor <= max_factor else "method"
    out["too_close"] = factor > max_factor
    return out


def combine(types, how):
    """all: the worst part decides; any: the best part decides (order met < measurement < method < reach)."""
    order = ["met", "measurement", "method", "reach"]
    ranked = sorted(types, key=order.index)
    return ranked[-1] if how == "all" else ranked[0]


def board_of(lid):
    for b in SPEC["boards"]:
        if lid in b["landmarks"]:
            return b
    return None


def derive(lid):
    """A landmark -> dict(type, value_type, parts, board)."""
    lm = LM[lid]
    parts = [dict(p, **derive_part(p)) for p in lm["parts"]]
    vt = combine([p["type"] for p in parts], lm.get("combine", "all"))
    b = board_of(lid)
    t = vt
    if b and b["ruler"]["verdict"] != "same" and vt != "reach":
        t = "comparability"
    return {"id": lid, "type": t, "value_type": vt, "parts": parts, "board": b["id"] if b else None}


def power_override(lid, part):
    """B4's power file, when present, replaces the crude estimate (records {landmark, family, n_now, n_needed_est, ...})."""
    key = RULES["power"]["key"]
    if not has(key):
        return None
    recs = val(key)
    recs = recs.get("records", recs) if isinstance(recs, dict) else recs
    fam = part["label"].split(",")[0]
    for r in recs if isinstance(recs, list) else []:
        if r.get("landmark") == lid and (r.get("family") in (None, fam)):
            return r
    return None


# ------------------------------------------------------------------ explanation ledger
def ledger_rows():
    key = RULES["explain_ledger"]["key"]
    if not has(key):
        if RULES["explain_ledger"].get("required"):
            PROBLEMS.append("the explanation ledger %s is required (gaps_spec rules) but not in the registry" % RULES["explain_ledger"]["path"])
        return None
    d = val(key)
    rows = d.get("records", d.get("segments")) if isinstance(d, dict) else d
    if not isinstance(rows, list):
        PROBLEMS.append("explanation ledger: expected a list of records (or {records: [...]})")
        return []
    return rows


def segments(gid):
    """Segments of one gap: from the ledger when present, else one 'attributed' segment of the anatomy total."""
    g = GAPS[gid]
    total = val(g["total"])
    rows = ledger_rows()
    if rows is None:
        return {"total": total, "pending": True,
                "segs": [{"segment": "all, typed map pending", "size": total, "state": "attributed", "ticket": "TGT-18", "report": None}]}
    mine = [r for r in rows if r.get("board") in g["ledger"]["board"] and r.get("gap") in g["ledger"]["gap"]]
    for r in mine:
        if r.get("state") not in STATES:
            PROBLEMS.append("explanation ledger %s/%s/%s: state %r is not in the closed list" % (r.get("board"), r.get("gap"), r.get("segment"), r.get("state")))
    s = sum(r.get("size", 0) for r in mine)
    if not mine:
        PROBLEMS.append("explanation ledger has no rows for gap %s (board in %s, gap in %s)" % (gid, g["ledger"]["board"], g["ledger"]["gap"]))
    elif s != total:
        PROBLEMS.append("explanation ledger: gap %s segments sum to %s, anatomy total is %s" % (gid, s, total))
    return {"total": total, "pending": False, "segs": mine}


def unmapped_ledger_rows():
    rows = ledger_rows() or []
    known = [(tuple(g["ledger"]["board"]), tuple(g["ledger"]["gap"])) for g in GAPS.values()]
    return [r for r in rows if not any(r.get("board") in b and r.get("gap") in gg for b, gg in known)]


def shares(gid):
    """Share of a gap's size in each state, and the understood / tackled shares."""
    sg = segments(gid)
    tot = sg["total"] or 1
    by = {s: 0 for s in STATES}
    for r in sg["segs"]:
        by[r["state"]] = by.get(r["state"], 0) + r.get("size", 0)
    upto = STATES.index(RULES["understood_from"])
    understood = sum(v for s, v in by.items() if s in STATES[upto:]) / tot
    tackled = sum(v for s, v in by.items() if s in RULES["tackled"]) / tot
    attributed = sum(v for s, v in by.items() if s != "unattributed") / tot
    return {"by": by, "total": sg["total"], "understood": understood, "tackled": tackled, "attributed": attributed,
            "pending": sg["pending"], "segs": sg["segs"]}


# ------------------------------------------------------------------ checks (site/build.py)
def check_spec(items):
    """Spec-level problems: every key exists, every type and state is from the closed lists, every unmet landmark of a
    deliverable is typed, no landmark binds a superseded read."""
    import registry
    ids = {i["id"] for i in items}
    for lid, lm in LM.items():
        for p in lm["parts"]:
            for k in ("value", "cons", "bar_key", "n"):
                if p.get(k) and not has(p[k]):
                    PROBLEMS.append("gaps_spec %s: registry key %s (%s) not in the snapshot" % (lid, p[k], k))
                for pre in getattr(registry, "SUPERSEDED", {}):
                    if p.get(k) and p[k].startswith(pre):
                        PROBLEMS.append("gaps_spec %s binds %s, a superseded read (%s)" % (lid, p[k], pre))
        for h in lm.get("history", []):
            for k in ("value", "cons"):
                if h.get(k) and not has(h[k]):
                    PROBLEMS.append("gaps_spec %s history: registry key %s not in the snapshot" % (lid, h[k]))
    for b in SPEC["boards"]:
        if b["ruler"]["verdict"] not in PLAIN["verdict"]:
            PROBLEMS.append("board %s: ruler verdict %r not in the closed list" % (b["id"], b["ruler"]["verdict"]))
        for lid in b["landmarks"]:
            if lid not in LM:
                PROBLEMS.append("board %s: unknown landmark %s" % (b["id"], lid))
        for gid in b.get("gaps", []):
            if gid not in GAPS:
                PROBLEMS.append("board %s: unknown gap %s" % (b["id"], gid))
        for t in (b["ruler"].get("ticket"), b.get("reach_ticket")):
            if t and t not in ids:
                NOTES.append("board %s names %s, which the tracker does not have yet" % (b["id"], t))
        for lid in b["landmarks"]:
            d = derive(lid)
            if d["value_type"] == "reach" and not b.get("reach_ticket"):
                PROBLEMS.append("board %s: landmark %s is not run yet and names no ticket that runs it" % (b["id"], lid))
            if d["type"] == "comparability" and not b["ruler"].get("ticket"):
                PROBLEMS.append("board %s: not comparable yet, but no ticket makes it comparable" % b["id"])
    for d in DELIV["deliverables"]:
        for lid in d.get("needs", []):
            if lid not in LM:
                PROBLEMS.append("deliverable %s needs unknown landmark %s" % (d["id"], lid))
        if d.get("due") and not has(d["due"]):
            PROBLEMS.append("deliverable %s: due key %s not in the snapshot" % (d["id"], d["due"]))
        if d.get("ticket") and d["ticket"] not in ids:
            PROBLEMS.append("deliverable %s: ticket %s not in the tracker" % (d["id"], d["ticket"]))
    for gid in GAPS:
        segments(gid)
    for r in unmapped_ledger_rows():
        PROBLEMS.append("explanation ledger row not mapped to any gap: board %r gap %r" % (r.get("board"), r.get("gap")))
    for s in RULES["tackled"] + [RULES["understood_from"]]:
        if s not in STATES:
            PROBLEMS.append("rules: state %s not in the closed list" % s)
    # derived verdicts must agree with the landmark file the tracker uses (q2_landmarks.json), where both exist
    for lid in ("ER-F", "ER-1", "ER-2", "ER-3", "ER-4a", "ER-4b", "ER-C"):
        k = "q2.lm." + lid
        if has(k) and lid in LM:
            mine = "met" if derive(lid)["type"] == "met" else "not met"
            if val(k) != mine:
                PROBLEMS.append("landmark %s: derived %r but %s says %r" % (lid, mine, k, val(k)))
    return PROBLEMS


# ------------------------------------------------------------------ small parts
def chip(t, label=None):
    fg, bg, bd, st = TYPE_STYLE[t]
    return (f'<span class="gchip" data-type="{t}" style="display: inline-block; padding: 1px 9px; border-radius: 10px; '
            f'border: 1.5px {st} {bd}; background: {bg}; color: {fg}; font-size: 12px; line-height: 18px; font-weight: 600; '
            f'white-space: nowrap">{esc(label or PLAIN["type"][t])}</span>')


def bar_svg(x, c, bar, axis, d, t):
    """Dot = result, band = from the cautious end to the result, line = the bar. HTML shapes in %, so the dot stays round."""
    lo, hi = axis

    def px(v):
        return max(0.0, min(100.0, (v - lo) / (hi - lo) * 100.0))
    fg, bg, bd, _st = TYPE_STYLE[t]
    band = ""
    if c is not None and x is not None and c != x:
        a, b = sorted((px(c), px(x)))
        band = (f'<span style="position: absolute; left: {a:.2f}%; width: {max(b - a, 0.6):.2f}%; top: 7px; height: 6px; '
                f'border-radius: 3px; background: {bg}; border: 1px solid {bd}; box-sizing: border-box"></span>')
    dot = (f'<span style="position: absolute; left: calc({px(x):.2f}% - 5px); top: 5px; width: 10px; height: 10px; '
           f'border-radius: 50%; background: {fg}"></span>') if x is not None else ""
    line = (f'<span style="position: absolute; left: calc({px(bar):.2f}% - 1px); top: 0; width: 2px; height: 20px; '
            f'background: #17201B"></span>') if bar is not None else ""
    return (f'<span aria-hidden="true" style="position: relative; display: block; height: 20px; margin: 0 6px">'
            f'<span style="position: absolute; left: 0; right: 0; top: 9px; height: 2px; border-radius: 1px; background: #E3E6E0"></span>'
            f'{band}{line}{dot}</span>')


def landmark_row(lid, compact=False):
    """A landmark as a row: plain name, what was measured, a bar graphic for the deciding part, and the type chip."""
    d = derive(lid)
    lm = LM[lid]
    spec = lm.get("fmt", "{:.3f}")
    # the part that decides: for "all" the worst, for "any" the best
    order = ["met", "measurement", "method", "reach"]
    key = (lambda p: order.index(p["type"]))
    dp = (max if lm.get("combine", "all") == "all" else min)(d["parts"], key=key)
    pieces = []
    for p in d["parts"] if not compact else [dp]:
        if p["x"] is None:
            continue
        if lm.get("unit") == "files":
            pieces.append(f'{esc(p["label"])}: {common.n(p["value"])} of {common.n(p["bar_key"])}')
            continue
        bar_txt = common.n(p["bar_key"], spec) if "bar_key" in p and not p.get("bar_offset") else fmt(p["bar_v"], spec)
        if compact:
            s = f'{common.n(p["value"], spec)}'
            if p.get("cons") and val(p["cons"]) != val(p["value"]):
                s += f' (cautious end {common.n(p["cons"], spec)})'
            s += f', bar {bar_txt}' + (f', {esc(p["label"].split(",")[0])}' if len(d["parts"]) > 1 else "")
        else:
            s = f'{esc(p["label"])}: {common.n(p["value"], spec)}'
            if p.get("cons") and val(p["cons"]) != val(p["value"]):
                s += f' ({"lower" if p["dir"] == "higher" else "upper"} end {common.n(p["cons"], spec)})'
            s += f'; bar {bar_txt}'
        pieces.append(s)
    sub = "; ".join(pieces) if pieces else "not run yet"
    extra = ""
    if d["type"] == "measurement" and dp.get("n_needed"):
        po = power_override(lid, dp)
        if po:
            extra = f' About {ev(RULES["power"]["key"], po.get("n_needed_est"))} {esc(po.get("unit", dp.get("n_unit", "cases")))} needed, against {esc(po.get("n_now"))} now (power estimate).'
        elif compact:
            extra = f' About {dp["n_needed"]:,} {esc(dp.get("n_unit", "cases"))} needed, {fmt(dp["n_now"], "{:,}")} now (estimate).'
        else:
            extra = (f' Needs about {dp["n_needed"]:,} {esc(dp.get("n_unit", "cases"))} instead of {fmt(dp["n_now"], "{:,}")} '
                     f'(estimate: range width taken as shrinking with the square root of the count).')
    if d["value_type"] == "method" and dp.get("too_close") and not compact:
        extra = " The estimate sits too close to the bar for more test cases to settle it."
    if d["type"] == "comparability" and compact:
        extra = f' {esc(PLAIN["verdict"][BOARDS[d["board"]]["ruler"]["verdict"]]).capitalize()}.'
    elif d["type"] == "comparability":
        extra = f' {esc(PLAIN["verdict"][BOARDS[d["board"]]["ruler"]["verdict"]]).capitalize()}: {why(BOARDS[d["board"]]["ruler"]["why"])}.'
    graph = ""
    if lm.get("axis") and dp["x"] is not None and lm.get("unit") != "files":
        graph = bar_svg(dp["x"], dp["c"], dp["bar_v"], lm["axis"], dp["dir"], d["value_type"])
    return (f'<div class="lmrow" id="lm-{esc(lid)}" style="display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(90px, 1fr) auto; '
            f'gap: 6px 14px; align-items: center; padding: 10px 0; border-top: 1px solid #E3E6E0">'
            f'<div style="min-width: 0"><div style="font-weight: 600; font-size: 15px; line-height: 21px">{esc(lm["plain"])}</div>'
            f'<div style="font-size: 13px; line-height: 19px; color: #4E5751">{sub}.{extra}</div></div>'
            f'<div style="min-width: 0">{graph}</div><div>{chip(d["type"])}</div></div>')


CSS = ("<style>@media (max-width: 640px){.lmrow{grid-template-columns: minmax(0, 1fr) auto !important}"
       ".lmrow > div:first-child{grid-column: 1 / 3}}</style>")


def legend_types(short=False):
    if short:
        return ('<p style="margin: 0; font-size: 13px; line-height: 19px; color: #4E5751">Dot: the result. Band: to the cautious '
                'end of its likely range. Line: the bar. ' + " ".join(chip(t) for t in TYPES) + "</p>")
    return ('<p style="margin: 0; font-size: 13px; line-height: 19px; color: #4E5751">In each bar: the dot is the result, the band runs '
            'to the cautious end of its likely range, the line is the bar to clear. ' +
            " ".join(chip(t) for t in TYPES) + "</p>")


def state_bar(gid, height=14):
    sh = shares(gid)
    tot = sh["total"] or 1
    cells = "".join(f'<span title="{esc(PLAIN["state"][s])}: {sh["by"][s]:,}" style="display: block; width: {sh["by"][s] / tot * 100:.2f}%; '
                    f'background: {STATE_COLOUR[s]}"></span>' for s in STATES if sh["by"].get(s))
    return (f'<span style="display: flex; width: 100%; height: {height}px; border-radius: 4px; overflow: hidden; '
            f'background: #F2F3EF" aria-hidden="true">{cells}</span>')


def legend_states(only=None):
    show = [s for s in STATES if only is None or s in only]
    return ('<p style="margin: 0; display: flex; flex-wrap: wrap; gap: 6px 14px; font-size: 13px; line-height: 19px; color: #4E5751">' +
            "".join(f'<span style="display: inline-flex; align-items: center; gap: 6px"><span style="width: 12px; height: 12px; '
                    f'border-radius: 2px; background: {STATE_COLOUR[s]}; display: inline-block"></span>{esc(PLAIN["state"][s])}</span>'
                    for s in show) + "</p>")


def understood_row(gid):
    g = GAPS[gid]
    sh = shares(gid)
    pend = ' <span style="color: #9A4A0E">(typed map pending)</span>' if sh["pending"] else ""
    return (f'<div style="display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr) auto; gap: 6px 14px; align-items: center; '
            f'padding: 6px 0"><div style="font-size: 14px; line-height: 20px">{esc(g["plain"])}, {esc(g["family"])}: '
            f'{common.n(g["total"])} {esc(g["unit"])}{pend}</div><div>{state_bar(gid)}</div>'
            f'<div style="font-size: 13px; color: #4E5751; white-space: nowrap">{sh["understood"]:.0%} understood</div></div>')


# ------------------------------------------------------------------ staircase
def staircase(board_id, compact=False):
    """Oracle repairs on development data, as HTML rows (responsive), with the board's published lines across."""
    b = BOARDS[board_id]
    st = b["staircase"]
    k = st["family"]
    steps = SPEC["staircase_steps"]
    vals = [val("q2h.%s.%s.f1" % (k, o)) for o, _ in steps]
    lines = [(lk, lab, val(lk)) for lk, lab in st["lines"] if has(lk)]
    lo = math.floor(min(vals + [x for _, _, x in lines]) * 10) / 10 - 0.05
    lo = max(0.0, lo)
    hi = 1.0

    def px(x):
        return (x - lo) / (hi - lo) * 100

    gid_of = SPEC["staircase_gap"]
    left, right = [], []
    for i, (o, lab) in enumerate(steps):
        x = vals[i]
        if i == 0:
            seg = (f'<span style="position: absolute; left: 0; width: {px(x):.2f}%; top: 12px; height: 16px; background: #B9BFB6; '
                   f'border-radius: 3px"></span>')
            note = "where it is now, on development files"
        else:
            a, w = px(vals[i - 1]), max(px(x) - px(vals[i - 1]), 0.3)
            gk = gid_of.get(o)
            gid = "%s-%s" % (k, gk) if gk else None
            if gid and gid in GAPS:
                sh = shares(gid)
                cells, acc, tot = [], 0.0, (sh["total"] or 1)
                for s_ in STATES:
                    if sh["by"].get(s_):
                        cw = sh["by"][s_] / tot * w
                        cells.append(f'<span style="position: absolute; left: {a + acc:.2f}%; width: {cw:.2f}%; top: 12px; height: 16px; '
                                     f'background: {STATE_COLOUR[s_]}"></span>')
                        acc += cw
                seg = "".join(cells)
                note = f'{sh["understood"]:.0%} of these errors have a known cause'
            else:
                seg = (f'<span style="position: absolute; left: {a:.2f}%; width: {w:.2f}%; top: 12px; height: 16px; '
                       f'background: {STATE_COLOUR["walled"]}"></span>')
                note = "pairs the data's own patterns leave open"
        left.append(f'<div style="min-height: 40px; display: flex; flex-direction: column; justify-content: center; min-width: 0; padding: 3px 0">'
                    f'<div style="font-weight: 600; font-size: 14px; line-height: 18px">{esc(lab)}</div>'
                    f'<div style="font-size: 12px; line-height: 16px; color: #4E5751">{common.n("q2h.%s.%s.f1" % (k, o), "{:.3f}")}'
                    f'{"" if compact else " · " + esc(note)}</div></div>')
        right.append(seg)
    marks = "".join(f'<span title="{esc(lab)} {x:.3f}" style="position: absolute; left: {px(x):.2f}%; top: 0; bottom: 0; width: 0; '
                    f'border-left: 1.5px dashed {"#5B3E8E" if "published" in lab else "#4E5751"}"></span>' for _, lab, x in lines)
    labels = "".join(f'<span style="display: inline-flex; gap: 4px; align-items: center; margin-right: 12px; white-space: nowrap">'
                     f'<span style="width: 14px; border-top: 1.5px dashed {"#5B3E8E" if "published" in lab else "#4E5751"}; display: inline-block">'
                     f'</span>{esc(lab)} {common.n(lk, "{:.3f}")}</span>' for lk, lab, x in lines)
    first = int(math.ceil(lo * 10 - 1e-9))
    ticks = "".join(f'<span style="position: absolute; left: {px(t / 10):.2f}%; transform: translateX(-50%)">{t / 10:.1f}</span>'
                    for t in range(first, 11))
    tick_row = ("" if compact else
                '<div></div><div style="position: relative; height: 16px; font-size: 11px; color: #4E5751">' + ticks + '</div>')
    note = ("" if compact else
            '<p style="margin: 0; font-size: 12px; line-height: 17px; color: #4E5751">Each row repairs one kind of error with the '
            'truth, on development files: what the score would be, not what the ledger does. Colours as in the legend of '
            'error causes.</p>')
    body = "".join(f'<div style="min-width: 0">{lft}</div><div style="position: relative; min-height: 40px">{marks}{seg}</div>'
                   for lft, seg in zip(left, right))
    return ('<div class="stair" style="display: flex; flex-direction: column; gap: 6px">'
            '<div style="font-size: 12px; line-height: 18px; color: #4E5751; display: flex; flex-wrap: wrap">' + labels + '</div>'
            '<div style="display: grid; grid-template-columns: minmax(96px, 0.9fr) minmax(0, 2fr); column-gap: 14px; align-items: stretch">'
            + body + tick_row + '</div>' + note + '</div>')


# ------------------------------------------------------------------ strips, overview, deliverables
def strip(slug):
    """'Where this stands now' at the foot of a story page: the boards that name this page, as compact rows."""
    bs = [b for b in SPEC["boards"] if slug in b.get("strip_on", [])]
    extra = names_strip() if slug == "names" else ""
    if not bs and not extra:
        return ""
    rows = "".join(f'<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px 12px; padding: 4px 0; '
                   f'border-top: 1px solid #E3E6E0"><span>{esc(LM[lid]["plain"])}</span>{chip(derive(lid)["type"])}</div>'
                   for b in bs for lid in b["landmarks"])
    links = " · ".join(f'<a href="gaps.html#{b["id"]}">{esc(b["title"])}</a>' for b in bs)
    return (f'<section class="strip" style="padding: 16px 20px; background: #FFFFFF; border: 1.5px solid #1D5C99; border-radius: 12px; '
            f'display: flex; flex-direction: column; gap: 6px"><span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; '
            f'text-transform: uppercase; color: #1D5C99">Where this stands now</span>{CSS}{extra}{rows}'
            + (('<p style="margin: 6px 0 0; font-size: 14px">The full gap cards: ' + links + '</p>') if links else "") + '</section>')


def names_strip():
    st = {i["id"]: i["status"] for i in common.SNAP["items"]}
    word = {"done": "done", "in_progress": "in progress", "todo": "not started", "open": "open", "blocked": "blocked"}

    def w(t):
        return word.get(st.get(t), st.get(t, "not in the tracker"))
    return (f'<p style="margin: 0; font-size: 14px; line-height: 21px">The page above measures Causal-Copilot as shipped. Its fixes '
            f'live on separate branches of a fork: refinement that stays above its own data (BLD-06, {w("BLD-06")}), the cycle step '
            f'that reads the key it asks for (EXT-03, {w("EXT-03")}), and the fork that runs them (INF-06, {w("INF-06")}). The '
            f'changed pipeline is scored live once the fork exists; until then every number on this page is the unchanged one.</p>')


def board_summary(bid):
    """(map, explain, tackle) shares over a board's gaps, weighted by size; None when the board has no gaps."""
    b = BOARDS[bid]
    if not b.get("gaps"):
        return None
    tot = att = und = tac = 0
    pending = False
    for gid in b["gaps"]:
        sh = shares(gid)
        t = sh["total"] or 0
        tot += t
        att += sh["attributed"] * t
        und += sh["understood"] * t
        tac += sh["tackled"] * t
        pending |= sh["pending"]
    tot = tot or 1
    return {"map": att / tot, "explain": und / tot, "tackle": tac / tot, "pending": pending}


def deliverable_status(d):
    types = {lid: derive(lid)["type"] for lid in d.get("needs", [])}
    counts = {t: sum(1 for x in types.values() if x == t) for t in TYPES}
    return types, counts


def due_of(d):
    return val(d["due"]) if d.get("due") else None
