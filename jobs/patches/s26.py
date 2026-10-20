"""s26 (site v3, TEAM-10): the gaps page (Act IV, before status) and the 'where this stands now' strips at the foot of scoreboard, names, rca and theses. Renumbers the pages after it. Apply after s24."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARK = 'slug="gaps"'


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8", newline="\n")


def replace_once(rel, old, new):
    t = read(rel)
    n = t.count(old)
    assert n == 1, "%s: anchor found %d times (expected once): %r" % (rel, n, old[:80])
    write(rel, t.replace(old, new, 1))


def new_file(rel, text):
    p = ROOT / rel
    assert not p.exists(), "%s already exists" % rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def require(rel, marker, why):
    assert marker in read(rel), why


assert MARK not in read('site/pages.py'), "already applied: %r found in %s" % (MARK, 'site/pages.py')

require("site/registry.py", "# ---- s24 (site v3 data layer", "apply s24 first")
new_file("site/pgs/pg_gaps.py", '"""Gaps (s26, TEAM-10): how far each board\'s landmarks are, and why. One card per board from site/gaps_spec.json: what it\nmeasures, whether its bar is on our ruler, each landmark with its derived gap type, the repair staircase where the board has\none, and the explanation map of the remaining errors (map, explain, tackle). Design: claude/site-v3-design-2026-10-20.md s5."""\nfrom pagekit import *  # noqa: F401,F403\nimport common\nimport gapkit as G\n\n\ndef pct(x):\n    return "%d%%" % round(100 * x)\n\n\ndef overview():\n    head = ["Board", "Landmarks", "Errors traced", "Cause known", "Fix chosen or done"]\n    rows = []\n    for b in G.SPEC["boards"]:\n        chips = " ".join(G.chip(G.derive(lid)["type"]) for lid in b["landmarks"])\n        s = G.board_summary(b["id"])\n        cells = ([pct(s["map"]), pct(s["explain"]), pct(s["tackle"])] if s else ["–", "–", "–"])\n        if s and s["pending"]:\n            cells[1] += " (pending)"\n        rows.append([f\'<a href="#{b["id"]}">{esc(b["title"])}</a>\', chips] + cells)\n    return table(head, rows, caption="Shares are weighted by the size of each error class. A dash: the board has no error map "\n                                     "of its own (its landmarks are single numbers, or it has not been run).")\n\n\ndef seg_table(gid):\n    sh = G.shares(gid)\n    rows = []\n    key = G.RULES["explain_ledger"]["key"]\n    for r in sh["segs"]:\n        size = G.ev(key, f\'{r["size"]:,}\') if not sh["pending"] else common.n(G.GAPS[gid]["total"])\n        rep = (f\'<a href="{common.EVBASE[0]}{esc(r["report"])}">report</a>\' if r.get("report") else "")\n        rows.append([esc(r["segment"]), size, f\'<span style="display: inline-flex; align-items: center; gap: 6px"><span style="width: 10px; \'\n                     f\'height: 10px; border-radius: 2px; display: inline-block; background: {G.STATE_COLOUR[r["state"]]}"></span>\'\n                     f\'{esc(G.PLAIN["state"][r["state"]])}</span>\', esc(r.get("ticket") or ""), rep])\n    return table(["Part of the gap", "Size", "State", "Ticket", "Where"], rows)\n\n\ndef gap_block(gid):\n    g = G.GAPS[gid]\n    sh = G.shares(gid)\n    pending = ("The typed map of this gap comes from the explanation ledger, which is not in the result files yet; until then "\n               "it shows as one traced block." if sh["pending"] else "")\n    open_t = sorted({r.get("ticket") for r in sh["segs"] if r["state"] not in G.RULES["tackled"] and r.get("ticket")})\n    plan = (f\'Map: {pct(sh["attributed"])} traced. Explain: {pct(sh["understood"])} with a known cause. Tackle: \'\n            f\'{pct(sh["tackled"])} with a fix chosen or done.\' + (f\' Open investigations: {", ".join(open_t)}.\' if open_t else ""))\n    return section(H3(f\'{esc(g["plain"])} ({esc(g["family"])}): {common.n(g["total"])} {esc(g["unit"])}\'),\n                   G.state_bar(gid, 18), P(plan, 15), P(pending, 14) if pending else "", seg_table(gid), gap=8)\n\n\ndef card(b):\n    parts = [f\'<h2 id="{b["id"]}" style="margin: 0; font-family: {COND}; font-size: 28px; line-height: 34px">{esc(b["title"])}</h2>\',\n             P(esc(b["plain"]), 16),\n             P(f\'<b>Ruler:</b> {esc(G.PLAIN["verdict"][b["ruler"]["verdict"]])}; {G.why(b["ruler"]["why"])}\'\n               + (f\' (decided by {esc(b["ruler"]["ticket"])})\' if b["ruler"].get("ticket") else "")\n               + (f\' <b>Run by:</b> {esc(b["reach_ticket"])}.\' if b.get("reach_ticket") and any(G.derive(lid)["value_type"] == "reach" for lid in b["landmarks"]) else ""), 15),\n             f\'<div style="display: flex; flex-direction: column">{"".join(G.landmark_row(lid) for lid in b["landmarks"])}</div>\']\n    if b.get("staircase"):\n        parts += [H3("What would close the distance"), G.staircase(b["id"])]\n    for gid in b.get("gaps", []):\n        if b["id"] != "prereg":\n            parts.append(gap_block(gid))\n    if b["id"] == "prereg" and b.get("gaps"):\n        parts.append(P("The errors behind these landmarks are mapped on the two CausalArena cards below.", 15))\n    return box("".join(parts))\n\n\nBODY = "\\n".join([\n    G.CSS,\n    question("How far is each result from the bar set for it, and why?",\n             before="the theses and the landmarks (page 8). Every number below comes from the result files."),\n    P("A landmark\'s gap gets one of five types, worked out from the numbers: met; needs more test cases (the result clears the "\n      "bar, its likely range does not yet); needs a better method; not comparable yet (the bar was measured differently); not run "\n      "yet. The remaining errors are mapped in three steps: traced to a cause class, explained, then tackled."),\n    G.legend_types(),\n    G.legend_states(),\n    H2("Every board at a glance"),\n    overview(),\n    *[card(b) for b in G.SPEC["boards"]],\n    answer("Most open landmarks are short on test cases, not on method; the one that needs a new method is accuracy above the "\n           "best data-only search, where the errors trace to a score that fits straight lines to curved and discrete mechanisms.",\n           "What is done, what is next, and what is waiting on whom?"),\n])\n')
replace_once("site/pages.py", '    dict(slug="status", act="IV", n=10,',
             '    dict(slug="gaps", act="IV", n=10, short="How far, and why", module="pg_gaps", words=2600,\n'
             '         title="How far, and why", question="How far is each result from the bar set for it, and why?",\n'
             '         tickets=["TGT-18", "TGT-19", "CAP-07", "BEN-13", "TEAM-10"]),\n'
             '    dict(slug="status", act="IV", n=11,')
for slug, old, new in (("changes", 11, 12), ("glossary", 12, 13), ("evidence", 13, 14), ("about", 14, 15)):
    t = read("site/pages.py")
    a = 'dict(slug="%s", act="' % slug
    i = t.index(a)
    j = t.index("n=%d," % old, i)
    assert j - i < 40, slug
    write("site/pages.py", t[:j] + "n=%d," % new + t[j + len("n=%d," % old):])
# "Where this stands now" strips at the foot of the story pages that a gap board names
replace_once("site/build.py", "        body = mod.BODY\n",
             "        body = mod.BODY\n"
             "        import gapkit as _gk  # s26 (TEAM-10): the board strips (site/gaps_spec.json strip_on)\n"
             "        body += _gk.strip(p[\"slug\"])\n")

print("s26 applied")
