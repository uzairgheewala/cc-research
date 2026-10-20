"""s25 (site v3, TEAM-11): Today, the one-page landing at index (pg_today), with a 600-word budget and a plain-language check (no ticket ids, no metric acronyms). The old home module stays on disk, unused. Apply after s24."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARK = 'module="pg_today"'


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
new_file("site/pgs/pg_today.py", '"""Today (s25, TEAM-11): the one-page landing. Where the measured results stand against every landmark, what stands in the\nway, what it means for the deliverables, how well the gaps are understood, and what moved. Generated from the snapshot,\nsite/gaps_spec.json and site/deliverables.json; 600 words at most; no ticket ids or metric acronyms in the text (site/build.py\nchecks both). Design: project doc claude/site-v3-design-2026-10-20.md section 4."""\nfrom pagekit import *  # noqa: F401,F403\nimport common\nimport gapkit as G\n\nSNAP = common.SNAP\nTODAY = (SNAP.get("generated_utc") or "")[:10]\n\n\ndef card(label, big, sub):\n    return (f\'<div style="padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; min-width: 0">\'\n            f\'<div style="font-size: 13px; line-height: 18px; color: #4E5751">{label}</div>\'\n            f\'<div style="font-family: {COND}; font-size: 34px; line-height: 40px; font-weight: 600">{big}</div>\'\n            f\'<div style="font-size: 13px; line-height: 18px; color: #4E5751">{sub}</div></div>\')\n\n\ndef _date(iso):\n    import datetime as _d\n    d = _d.date.fromisoformat(iso)\n    return "%d %s" % (d.day, d.strftime("%b"))\n\n\nD = {d["id"]: d for d in G.DELIV["deliverables"]}\nneed_any = sorted({lid for d in G.DELIV["deliverables"] for lid in d.get("needs", [])}, key=list(G.LM).index)\ntypes = {lid: G.derive(lid)["type"] for lid in need_any}\nopen_ = [lid for lid in need_any if types[lid] != "met"]\nmeas = [lid for lid in open_ if types[lid] == "measurement"]\n_, pc = G.deliverable_status(D["paper"])\n_, prc = G.deliverable_status(D["product"])\nupcoming = sorted((G.due_of(d), d) for d in G.DELIV["deliverables"] if G.due_of(d) and G.due_of(d) >= TODAY)\nnxt = upcoming[0] if upcoming else None\n\ncards = grid([\n    card("Landmarks met for the paper", f\'{pc["met"]} of {len(D["paper"]["needs"])}\', f\'and {prc["met"]} of {len(D["product"]["needs"])} for the product\'),\n    card("Open landmarks short only on test cases", f"{len(meas)} of {len(open_)}",\n         "the result clears the bar, its range not yet"),\n    card("Next deliverable", _date(nxt[0]) if nxt else "none set", esc(nxt[1]["plain"]) if nxt else ""),\n], min_w=200)\n\nrows = "".join(G.landmark_row(lid, compact=True) for lid in G.SPEC["today_rows"])\n\ntop = G.val("pub.sem.D.best")\nsteps = G.SPEC["staircase_steps"]\ncross = next((i for i, (o, _l) in enumerate(steps) if G.val("q2h.sem.%s.f1" % o) >= top), None)\nstair_sentence = ("If one kind of error at a time were repaired with the truth, the semantic score would pass the top published "\n                  "number at the step “%s”%s." % (esc(steps[cross][1].lower()),\n                                                  ", using only the links the ledger already finds" if cross <= 2 else "")\n                  if cross is not None else "")\n\n\nCOUNT_WORD = {"met": "met", "measurement": "short on test cases", "method": "needing a better method",\n              "comparability": "not comparable yet", "reach": "not run yet"}\n\n\ndef lower1(x):\n    return x[:1].lower() + x[1:]\n\n\ndef dcard(d):\n    if d.get("needs"):\n        _, c = G.deliverable_status(d)\n        bits = [f\'{c[t]} {COUNT_WORD[t]}\' for t in ("met", "measurement", "method", "comparability", "reach") if c[t]]\n        blockers = [lower1(G.LM[lid]["plain"]) for lid in d["needs"] if G.derive(lid)["type"] == "method"]\n        body = (f\'Needs {len(d["needs"])} landmarks: {", ".join(bits)}.\'\n                + (f\' The one blocking it: {esc(blockers[0])}.\' if len(blockers) == 1 else\n                   (f\' Blocking it: {esc("; ".join(blockers))}.\' if blockers else " Nothing needs a new method.")))\n        body += f\' <span style="color: #4E5751">{esc(d["fallback"])}</span>\' if blockers and d.get("fallback") else ""\n    else:\n        body = f\'Due {_date(G.due_of(d))}. {esc(d["what"])}\'\n    return box(f\'{H3(esc(d["plain"]))}<p class="prose" style="margin: 0; font-size: 15px; line-height: 22px">{body}</p>\')\n\n\nlag = SNAP.get("changes_lag") or {}\nlatest = (SNAP.get("changes") or [{}])[0]\nmoved = (f\'The last team post was on {_date(latest["posted_utc"][:10])}, with {len(latest.get("points", []))} updates.\'\n         if latest.get("posted_utc") else "No team post yet.")\nif lag.get("dev_since_last_prod"):\n    moved += f\' {lag["dev_since_last_prod"]} working updates since; they appear here once posted.\'\n\nBODY = "\\n".join([\n    G.CSS,\n    P("Causal discovery recovers which variables drive which from data. This project audits how well today\'s tools do it and "\n      "builds a claim ledger: every claim keeps its source, says how sure it is, and declines when the data cannot decide. "\n      "This page is rebuilt from the result files.", 17),\n    cards,\n    H2("Landmarks set in advance"),\n    f\'<div style="display: flex; flex-direction: column">{rows}</div>\',\n    G.legend_types(short=True),\n    H2("What stands in the way"),\n    P(stair_sentence, 15) if stair_sentence else "",\n    G.staircase("causalarena-semantic", compact=True),\n    H2("What this means for the deliverables"),\n    grid([dcard(D[k]) for k in ("paper", "product", "ta", "checkpoint")], min_w=260),\n    H2("How well the errors are understood"),\n    f\'<div style="display: flex; flex-direction: column">{"".join(G.understood_row(g) for g in ("sem-missed", "sem-false", "sem-reversed"))}</div>\',\n    G.legend_states(only=sorted({s for g in ("sem-missed", "sem-false", "sem-reversed") for s, v in G.shares(g)["by"].items() if v},\n                                key=G.STATES.index)),\n    H2("What moved"),\n    P(moved + f\' {link("changes", "What changed")}.\', 15),\n    P(f\'{link("gaps", "Every gap in detail")} · {link("explore", "the research explorer")} · {link("primer", "the story from the start")}\', 15),\n])\n')
replace_once("site/pages.py", 'dict(slug="index", act=None, n=0, short="Home", module="pg_home",\n         title="Causal Atlas", question="What is this project, and where should I start?",\n         tickets=["DEC-05", "AUD-45", "TGT-18", "TGT-19", "BEN-13", "INF-10"]),',
             'dict(slug="index", act=None, n=0, short="Today", module="pg_today", words=600, plain=True,\n         title="Causal Atlas", question="Where does the research stand today, against every landmark, and what does it mean for what we deliver?",\n         tickets=["DEC-05", "AUD-45", "TGT-18", "TGT-19", "BEN-13", "INF-10", "TEAM-11"]),')
replace_once("site/build.py", "WORD_BUDGET = 1800\n",
             "WORD_BUDGET = 1800\n"
             "# s25: pages marked plain=True (Today) may not use ticket ids or metric acronyms in their text\n"
             "PLAIN_BANNED = [(r\"\\b[A-Z]{2,5}-\\d+[a-z]?\\b\", \"a ticket or landmark id\"), (r\"\\bDV-1\\b\", \"DV-1\"), (r\"\\bECE\\b\", \"ECE\"),\n"
             "                (r\"\\bBIC\\b\", \"BIC\"), (r\"\\bKCI\\b\", \"KCI\"), (r\"\\bCPDAG\\b\", \"CPDAG\"), (r\"\\bAC@3\\b\", \"AC@3\"),\n"
             "                (r\"\\bSHD\\b\", \"SHD\"), (r\"\\bF1\\b\", \"F1\"), (r\"\\bMEC\\b\", \"MEC\")]\n")
replace_once("site/build.py",
             '        if words > WORD_BUDGET:\n            warnings.append("%s: %d words (budget %d)" % (p["slug"], words, WORD_BUDGET))\n',
             '        if words > (p.get("words") or WORD_BUDGET):\n'
             '            (errors if p.get("words") else warnings).append("%s: %d words (budget %d)" % (p["slug"], words, p.get("words") or WORD_BUDGET))\n'
             '        for _pat, _why in (PLAIN_BANNED if p.get("plain") else []):\n'
             '            _m = re.search(_pat, txt)\n'
             '            if _m:\n'
             '                errors.append("%s: plain-language page uses %s: ...%s..." % (p["slug"], _why, txt[max(0, _m.start() - 40): _m.end() + 40]))\n')

print("s25 applied")
