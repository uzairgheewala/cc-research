"""Today (s25, TEAM-11): the one-page landing. Where the measured results stand against every landmark, what stands in the
way, what it means for the deliverables, how well the gaps are understood, and what moved. Generated from the snapshot,
site/gaps_spec.json and site/deliverables.json; 600 words at most; no ticket ids or metric acronyms in the text (site/build.py
checks both). Design: project doc claude/site-v3-design-2026-10-20.md section 4."""
from pagekit import *  # noqa: F401,F403
import common
import gapkit as G

SNAP = common.SNAP
TODAY = (SNAP.get("generated_utc") or "")[:10]


def card(label, big, sub):
    return (f'<div style="padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; min-width: 0">'
            f'<div style="font-size: 13px; line-height: 18px; color: #4E5751">{label}</div>'
            f'<div style="font-family: {COND}; font-size: 34px; line-height: 40px; font-weight: 600">{big}</div>'
            f'<div style="font-size: 13px; line-height: 18px; color: #4E5751">{sub}</div></div>')


def _date(iso):
    import datetime as _d
    d = _d.date.fromisoformat(iso)
    return "%d %s" % (d.day, d.strftime("%b"))


D = {d["id"]: d for d in G.DELIV["deliverables"]}
need_any = sorted({lid for d in G.DELIV["deliverables"] for lid in d.get("needs", [])}, key=list(G.LM).index)
types = {lid: G.derive(lid)["type"] for lid in need_any}
open_ = [lid for lid in need_any if types[lid] != "met"]
meas = [lid for lid in open_ if types[lid] == "measurement"]
_, pc = G.deliverable_status(D["paper"])
_, prc = G.deliverable_status(D["product"])
upcoming = sorted((G.due_of(d), d) for d in G.DELIV["deliverables"] if G.due_of(d) and G.due_of(d) >= TODAY)
nxt = upcoming[0] if upcoming else None

cards = grid([
    card("Landmarks met for the paper", f'{pc["met"]} of {len(D["paper"]["needs"])}', f'and {prc["met"]} of {len(D["product"]["needs"])} for the product'),
    card("Open landmarks short only on test cases", f"{len(meas)} of {len(open_)}",
         "the result clears the bar, its range not yet"),
    card("Next deliverable", _date(nxt[0]) if nxt else "none set", esc(nxt[1]["plain"]) if nxt else ""),
], min_w=200)

rows = "".join(G.landmark_row(lid, compact=True) for lid in G.SPEC["today_rows"])

top = G.val("pub.sem.D.best")
steps = G.SPEC["staircase_steps"]
cross = next((i for i, (o, _l) in enumerate(steps) if G.val("q2h.sem.%s.f1" % o) >= top), None)
stair_sentence = ("If one kind of error at a time were repaired with the truth, the semantic score would pass the top published "
                  "number at the step “%s”%s." % (esc(steps[cross][1].lower()),
                                                  ", using only the links the ledger already finds" if cross <= 2 else "")
                  if cross is not None else "")


COUNT_WORD = {"met": "met", "measurement": "short on test cases", "method": "needing a better method",
              "comparability": "not comparable yet", "reach": "not run yet"}


def lower1(x):
    return x[:1].lower() + x[1:]


def dcard(d):
    if d.get("needs"):
        _, c = G.deliverable_status(d)
        bits = [f'{c[t]} {COUNT_WORD[t]}' for t in ("met", "measurement", "method", "comparability", "reach") if c[t]]
        blockers = [lower1(G.LM[lid]["plain"]) for lid in d["needs"] if G.derive(lid)["type"] == "method"]
        body = (f'Needs {len(d["needs"])} landmarks: {", ".join(bits)}.'
                + (f' The one blocking it: {esc(blockers[0])}.' if len(blockers) == 1 else
                   (f' Blocking it: {esc("; ".join(blockers))}.' if blockers else " Nothing needs a new method.")))
        body += f' <span style="color: #4E5751">{esc(d["fallback"])}</span>' if blockers and d.get("fallback") else ""
    else:
        body = f'Due {_date(G.due_of(d))}. {esc(d["what"])}'
    return box(f'{H3(esc(d["plain"]))}<p class="prose" style="margin: 0; font-size: 15px; line-height: 22px">{body}</p>')


lag = SNAP.get("changes_lag") or {}
latest = (SNAP.get("changes") or [{}])[0]
moved = (f'The last team post was on {_date(latest["posted_utc"][:10])}, with {len(latest.get("points", []))} updates.'
         if latest.get("posted_utc") else "No team post yet.")
if lag.get("dev_since_last_prod"):
    moved += f' {lag["dev_since_last_prod"]} working updates since; they appear here once posted.'

BODY = "\n".join([
    G.CSS,
    P("Causal discovery recovers which variables drive which from data. This project audits how well today's tools do it and "
      "builds a claim ledger: every claim keeps its source, says how sure it is, and declines when the data cannot decide. "
      "This page is rebuilt from the result files.", 17),
    cards,
    H2("Landmarks set in advance"),
    f'<div style="display: flex; flex-direction: column">{rows}</div>',
    G.legend_types(short=True),
    H2("What stands in the way"),
    P(stair_sentence, 15) if stair_sentence else "",
    G.staircase("causalarena-semantic", compact=True),
    H2("What this means for the deliverables"),
    grid([dcard(D[k]) for k in ("paper", "product", "ta", "checkpoint")], min_w=260),
    H2("How well the errors are understood"),
    f'<div style="display: flex; flex-direction: column">{"".join(G.understood_row(g) for g in ("sem-missed", "sem-false", "sem-reversed"))}</div>',
    G.legend_states(only=sorted({s for g in ("sem-missed", "sem-false", "sem-reversed") for s, v in G.shares(g)["by"].items() if v},
                                key=G.STATES.index)),
    H2("What moved"),
    P(moved + f' {link("changes", "What changed")}.', 15),
    P(f'{link("gaps", "Every gap in detail")} · {link("explore", "the research explorer")} · {link("primer", "the story from the start")}'
      ' · <a href="copilot/">how Causal-Copilot works, read from its code</a>', 15),  # S29 (TEAM-13); site/copilot/build.py checks it
])
