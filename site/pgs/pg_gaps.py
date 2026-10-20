"""Gaps (s26, TEAM-10): how far each board's landmarks are, and why. One card per board from site/gaps_spec.json: what it
measures, whether its bar is on our ruler, each landmark with its derived gap type, the repair staircase where the board has
one, and the explanation map of the remaining errors (map, explain, tackle). Design: claude/site-v3-design-2026-10-20.md s5."""
from pagekit import *  # noqa: F401,F403
import common
import gapkit as G


def pct(x):
    return "%d%%" % round(100 * x)


def overview():
    head = ["Board", "Landmarks", "Errors traced", "Cause known", "Fix chosen or done"]
    rows = []
    for b in G.SPEC["boards"]:
        chips = " ".join(G.chip(G.derive(lid)["type"]) for lid in b["landmarks"])
        s = G.board_summary(b["id"])
        cells = ([pct(s["map"]), pct(s["explain"]), pct(s["tackle"])] if s else ["–", "–", "–"])
        if s and s["pending"]:
            cells[1] += " (pending)"
        rows.append([f'<a href="#{b["id"]}">{esc(b["title"])}</a>', chips] + cells)
    return table(head, rows, caption="Shares are weighted by the size of each error class. A dash: the board has no error map "
                                     "of its own (its landmarks are single numbers, or it has not been run).")


def seg_table(gid):
    sh = G.shares(gid)
    rows = []
    key = G.RULES["explain_ledger"]["key"]
    for r in sh["segs"]:
        size = G.ev(key, f'{r["size"]:,}') if not sh["pending"] else common.n(G.GAPS[gid]["total"])
        rep = (f'<a href="{common.EVBASE[0]}{esc(r["report"])}">report</a>' if r.get("report") else "")
        rows.append([esc(r["segment"]), size, f'<span style="display: inline-flex; align-items: center; gap: 6px"><span style="width: 10px; '
                     f'height: 10px; border-radius: 2px; display: inline-block; background: {G.STATE_COLOUR[r["state"]]}"></span>'
                     f'{esc(G.PLAIN["state"][r["state"]])}</span>', esc(r.get("ticket") or ""), rep])
    return table(["Part of the gap", "Size", "State", "Ticket", "Where"], rows)


def gap_block(gid):
    g = G.GAPS[gid]
    sh = G.shares(gid)
    pending = ("The typed map of this gap comes from the explanation ledger, which is not in the result files yet; until then "
               "it shows as one traced block." if sh["pending"] else "")
    open_t = sorted({r.get("ticket") for r in sh["segs"] if r["state"] not in G.RULES["tackled"] and r.get("ticket")})
    plan = (f'Map: {pct(sh["attributed"])} traced. Explain: {pct(sh["understood"])} with a known cause. Tackle: '
            f'{pct(sh["tackled"])} with a fix chosen or done.' + (f' Open investigations: {", ".join(open_t)}.' if open_t else ""))
    return section(H3(f'{esc(g["plain"])} ({esc(g["family"])}): {common.n(g["total"])} {esc(g["unit"])}'),
                   G.state_bar(gid, 18), P(plan, 15), P(pending, 14) if pending else "", seg_table(gid), gap=8)


def card(b):
    parts = [f'<h2 id="{b["id"]}" style="margin: 0; font-family: {COND}; font-size: 28px; line-height: 34px">{esc(b["title"])}</h2>',
             P(esc(b["plain"]), 16),
             P(f'<b>Ruler:</b> {esc(G.PLAIN["verdict"][b["ruler"]["verdict"]])}; {G.why(b["ruler"]["why"])}'
               + (f' (decided by {esc(b["ruler"]["ticket"])})' if b["ruler"].get("ticket") else "")
               + (f' <b>Run by:</b> {esc(b["reach_ticket"])}.' if b.get("reach_ticket") and any(G.derive(lid)["value_type"] == "reach" for lid in b["landmarks"]) else ""), 15),
             f'<div style="display: flex; flex-direction: column">{"".join(G.landmark_row(lid) for lid in b["landmarks"])}</div>']
    if b.get("staircase"):
        parts += [H3("What would close the distance"), G.staircase(b["id"])]
    for gid in b.get("gaps", []):
        if b["id"] != "prereg":
            parts.append(gap_block(gid))
    if b["id"] == "prereg" and b.get("gaps"):
        parts.append(P("The errors behind these landmarks are mapped on the two CausalArena cards below.", 15))
    return box("".join(parts))


BODY = "\n".join([
    G.CSS,
    question("How far is each result from the bar set for it, and why?",
             before="the theses and the landmarks (page 8). Every number below comes from the result files."),
    P("A landmark's gap gets one of five types, worked out from the numbers: met; needs more test cases (the result clears the "
      "bar, its likely range does not yet); needs a better method; not comparable yet (the bar was measured differently); not run "
      "yet. The remaining errors are mapped in three steps: traced to a cause class, explained, then tackled."),
    G.legend_types(),
    G.legend_states(),
    H2("Every board at a glance"),
    overview(),
    *[card(b) for b in G.SPEC["boards"]],
    answer("Most open landmarks are short on test cases, not on method; the one that needs a new method is accuracy above the "
           "best data-only search, where the errors trace to a score that fits straight lines to curved and discrete mechanisms.",
           "What is done, what is next, and what is waiting on whom?"),
])
