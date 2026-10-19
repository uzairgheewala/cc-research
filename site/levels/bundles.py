from common import *

CX = [170, 400, 630, 860, 1090]
CW, CH = 200, 90
HOST_W, HOST_H = 1320, 940


def card(col, y, bid, title, status, status_text, note):
    bg, bd, fg, style = STATUS[status]
    x = CX[col]
    return f"""<div style="position: absolute; left: {x}px; top: {y}px; width: {CW}px; height: {CH}px; box-sizing: border-box; padding: 7px 10px; background: {bg}; border: 1.5px {style} {bd}; border-radius: 8px; display: flex; flex-direction: column; gap: 2px; overflow: hidden">
<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 6px"><span style="font-family: {MONO}; font-size: 12px; line-height: 16px; font-weight: 600; color: {fg}">{bid}</span><span style="font-size: 11px; line-height: 16px; font-weight: 600; color: {fg}">{status_text}</span></div>
<span style="font-size: 14px; line-height: 18px; font-weight: 600">{title}</span>
<span style="font-size: 12px; line-height: 16px; color: #4E5751">{note}</span>
</div>"""


def arrow_path(left, top, w, h, d, colour="#4E5751"):
    import common
    common._arrow_n[0] += 1
    k = common._arrow_n[0]
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" style="position: absolute; left: {left}px; top: {top}px; width: {w}px; height: {h}px; overflow: visible; fill: none; stroke: {colour}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round">'
            f'<defs><marker id="dc-arrow-head-filled-{k}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible"><path d="M0 0 L4 2 L0 4 Z" fill="{colour}" stroke="none" style="stroke: none; fill: {colour}; fill: context-stroke"/></marker></defs>'
            f'<path d="{d}" marker-end="url(#dc-arrow-head-filled-{k})"></path></svg>')


parts = []
# lane bands
LANES = [(56, 118, "Spine", "ground rules and delivery", "#17201B", "#FFFFFF"),
         (176, 318, "P1 Measurement", "where order comes from", PILLAR["P1"][0], "#F7FAFD"),
         (496, 318, "P2 Claim ledger", "use order on purpose", PILLAR["P2"][0], "#FFFAF5"),
         (816, 118, "P3 Decisions", "effects, experiments", PILLAR["P3"][0], "#FAF8FD")]
for top, h, name, sub, col, bg in LANES:
    parts.append(f'<div style="position: absolute; left: 0; top: {top}px; width: {HOST_W}px; height: {h}px; background: {bg}; border-top: 1px solid #E3E6E0"></div>')
    parts.append(f'<div style="position: absolute; left: 16px; top: {top + 12}px; width: 136px; display: flex; flex-direction: column; gap: 2px">{tag(name, col)}<span style="font-size: 13px; line-height: 17px; color: #4E5751">{sub}</span></div>')

# column headers with milestones
HEAD = [("Start", "no blockers"), ("After BND-01", "gate G1"), ("Next", "TA check-in"),
        ("Checkpoint", "gate G2"), ("Final", "gate G3")]
for i, (a, b) in enumerate(HEAD):
    parts.append(f'<div style="position: absolute; left: {CX[i]}px; top: 12px; width: {CW}px; font-size: 13px; line-height: 17px"><b>{a}</b> · <span style="font-family: {MONO}; color: #8E2A2A">{b}</span></div>')

def bc(col, y, bid, title, note):
    """A bundle card whose status and ticket count come from the snapshot."""
    b = bundle(bid)
    st = b["status"]
    done = sum(1 for x in b["closes"] if item(x)["status"] == "done") if b["closes"] else 0
    txt = "done" if st == "done" else ("%d of %d done" % (done, len(b["closes"])) if b["closes"] else STATUS_TEXT.get(st, st))
    return card(col, y, bid, title, STATUS_OF.get(st, "todo"), txt, note)


_bundled = {x for b in SNAP["bundles"] for x in b["closes"]}
Q1B = [b for b in SNAP["bundles"] if b.get("plan", "q1") == "q1"]
AB = [b for b in SNAP["bundles"] if b.get("plan") == "audit"]


def gc(col, y, ids, title, note):
    """A build a thesis needs: a red dashed 'gap' card while no bundle closes it, else a normal card."""
    ids = ids.split("/")
    its = [item(i) for i in ids]
    if any(i in _bundled for i in ids):
        st = "done" if all(i["status"] == "done" for i in its) else "in_progress"
        return card(col, y, " / ".join(ids), title, STATUS_OF[st], "bundled", note)
    blocked = any(i["status"] == "blocked" for i in its)
    return card(col, y, " / ".join(ids), title, "gap", "no bundle" + (" · blocked" if blocked else ""), note)


# spine
parts += [bc(0, 64, "BND-01", "Ground rules and infrastructure", "score contract, compute jobs"),
          bc(1, 64, "BND-05", "Freeze the Q1 dataset suite", "dev and held-out split frozen"),
          bc(3, 64, "BND-13", "Q1 checkpoint package", "after " + ", ".join(x[4:] for x in bundle("BND-13")["blocked_by"])),
          bc(4, 64, "BND-14", "Q1 final: report, package, rerun", "after " + ", ".join(x[4:] for x in bundle("BND-14")["blocked_by"])),
          arrow_h(372, 109, 26), arrow_h(1062, 109, 26)]
# P1
parts += [bc(0, 184, "BND-02", "Primary sources, deep reads", "DOM-07 waits on appendix B"),
          bc(0, 284, "BND-03", "Paper and code audit", "open: REP-03, AUD-14 job"),
          bc(1, 184, "BND-04", "GES and FCI error budgets", "directions right: %s, %s" % (t("m.GES.q", "{:.0%}"), t("m.FCI.q", "{:.0%}"))),
          bc(2, 184, "BND-06", "Baselines, order, package", "AVICI checkpoint download blocked"),
          bc(2, 284, "BND-08", "LIVE · Causal-Copilot x names", "DLV-02: %s crashed arms" % t("cc.crashed")),
          bc(2, 384, "BND-12", "LIVE · second model, replications", "live part waits on you"),
          arrow_h(602, 229, 26)]
# P2
parts += [bc(1, 504, "BND-09", "Refinement v1 on dev", "frozen rule"),
          bc(2, 504, "BND-10", "Refinement v1 held-out", "R1 %s/%s, R2 %s/%s: inconclusive" % (t("v1.R1.hits"), t("v1.files"), t("v1.R2.hits"), t("v1.files"))),
          bc(2, 604, "BND-11", "LIVE · Refinement v2", "free jobs, then names under $1"),
          gc(2, 704, "BLD-02", "B1 · claim ledger kernel", "I1-I4, I7; G2 in program v2"),
          gc(3, 704, "BLD-03/BLD-04", "B2 interventions · B3 tiers", "B3 waits on DEC-02"),
          gc(4, 704, "BLD-05", "B4 calibration, abstention", "T4; Platt scaling chosen"),
          arrow_h(602, 549, 26),
          arrow_path(496, 594, 134, 60, "M 4 0 L 4 55 L 130 55"),
          arrow_h(832, 749, 26), arrow_h(1062, 749, 26)]
# P3
parts += [bc(1, 824, "BND-07", "Causal Chambers audit", "CPDAG identical to authors'"),
          gc(3, 824, "BLD-07", "C1 · what-if answers", "T5; after B2"),
          gc(4, 824, "BLD-08", "C2 · next experiment", "T6; after B2"),
          arrow_v(960, 796, 26)]

host = f"""<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
<div style="position: relative; width: {HOST_W}px; height: {HOST_H}px">
{chr(10).join(parts)}
</div>
</div>"""

legend = f"""<div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; font-size: 13px">
{pill("done", "done")} {pill("in progress or measured", "prog")} {pill("to do", "todo")} {pill("needed by a thesis, no bundle yet", "gap")}
<span style="color: #4E5751">Arrows are direct dependencies within a lane; other blockers are written on the card. Columns are the order of work; the red labels name the gate each column feeds.</span>
</div>"""

steps = [("done", "v2 frozen (analysis/results/refinement_v2/RULE.json); unit tests run in CI"),
         ("you", "free: formula replay dev and test, AUD-14 wrapper job"),
         ("you", "free: names questions, stub run (786 questions)"),
         ("you", "live: names questions, under $1"),
         ("me", "apply names answers; held-out test on the formula replay"),
         ("me", "verdicts on TGT-09 (never below data-only) and TGT-13 (zero crashes)")]
step_html = []
for i, (who, txt) in enumerate(steps, 1):
    colour = {"done": "#1D5C99", "you": "#8E2A2A", "me": "#4E5751"}[who]
    label = {"done": "done", "you": "you", "me": "Claude"}[who]
    step_html.append(f'<li style="display: flex; gap: 10px; align-items: baseline"><span style="flex: 0 0 64px; font-family: {MONO}; font-size: 12px; font-weight: 600; color: {colour}">{i} · {label}</span><span>{txt}</span></li>')
detail = f"""<section style="flex: 1 1 520px; padding: 18px 20px; background: #FFFFFF; border: 1.5px solid #B85A12; border-radius: 10px; display: flex; flex-direction: column; gap: 10px">
{tag("Zoom: the next bundle · BND-11", "#9A4A0E")}
<p style="margin: 0; font-family: {COND}; font-size: 22px; line-height: 28px; font-weight: 600">Refinement v2: names only where the data are silent</p>
<p style="margin: 0; font-size: 14px; line-height: 20px">Closes CAP-10 and TGT-13 (no crash from malformed model output), TGT-09 (never below its own data-only output, missed by v1), BLD-06 (drop-in replacement for Causal-Copilot's refinement stage) and DLV-04 (the Q1 refinement result). On the Atlas it is the first step into the thesis cell, still as a patch rather than the ledger.</p>
<ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 6px; font-size: 14px; line-height: 20px">{''.join(step_html)}</ol>
<a href="Stages.dc.html" style="font-size: 14px">Zoom into one Causal-Copilot run, stage by stage</a>
</section>"""

_dec = [(i["id"], i["title"]) for i in SNAP["items"] if i["id"].startswith("DEC-") and i["status"] != "done"]
_waits = [b["id"] for b in SNAP["bundles"] if b["status"] != "done" and (b["status"] == "blocked" or ("wait" in b["note"].lower() and "uzair" in b["note"].lower()))]
QUEUE = [("Free", "cc.ps1 compute: bootstrap_replay_ca_formula_dev.json, _test.json, aud14_ts_wrappers.json", "unblocks BND-11, BND-03"),
         ("Free", "cc.ps1 names bnd11_names_requests.jsonl stub", "checks the runner"),
         ("Live", "cc.ps1 names bnd11_names_requests.jsonl (under $1)", "BND-11")] if bundle("BND-11")["status"] != "done" else []
QUEUE += [("Decide", "%s %s" % (d, ttl), "tracker: open") for d, ttl in _dec]
QUEUE += [("Decide", "Bring kernel B1 into Q1 as a bundle, or start it after the G2 checkpoint", "what G2 tests")] if "BLD-02" not in _bundled else []
QUEUE += [("Waits", "%s: %s" % (b, bundle(b)["title"]), "the bundle note says it waits on you") for b in _waits if b != "BND-11" and not b.startswith("AB-")]
QUEUE += [("Live", "cc.ps1 probe ab05_probe_[pywhyllm|matmcd|vashishtha].json (AB-05; stub first)", "three agent probes left"),
          ("Live", "cc.ps1 plan ab06_cc_gpt4omini_s2.json gpt-4o-mini (AB-06, about $1)", "Causal-Copilot on a second model, BND-08 grid"),
          ("Live", "cc.ps1 probebatch ab06 live [causaliq|matmcd|vashishtha|pywhyllm] (AB-06, about $58 in all, total cap $60; stub first)", "the field audit of the four agents, cheapest first"),
          ("Get", "Bayesys results_noisyPaper.xlsx into external\\bayesys (AB-02)", "the reproduction gate before any claim on the published Bayesys numbers"),
          ("Ask", "Course staff: do the AB-10 interviews need an IRB determination?", "docs/interviews/human_subjects_check.md")] if any(b["id"] == "AB-05" for b in AB) else []
qrows = "".join(f'<li style="display: grid; grid-template-columns: 58px 1fr; gap: 8px"><span style="font-family: {MONO}; font-size: 12px; font-weight: 600; color: #8E2A2A">{k}</span><span>{t}<br><span style="color: #4E5751; font-size: 13px">{w}</span></span></li>' for k, t, w in QUEUE)
queue = f"""<section style="flex: 1 1 420px; padding: 18px 20px; background: #F6E7E7; border: 1.5px solid #8E2A2A; border-radius: 10px; display: flex; flex-direction: column; gap: 10px">
{tag("Waiting on you", "#8E2A2A")}
<ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 14px; line-height: 20px">{qrows}</ol>
</section>"""


# ---- audit program (plans/audit_dag.json, approved 2026-10-12): three tracks, columns = dependency depth
A_LANES = [("research", "Research", "scoreboards, engines, agents, theory", "#1D5C99", "#F7FAFD"),
           ("commercial", "Commercial", "buyers, vendors, rules", "#7A4BA8", "#FAF8FD"),
           ("wedge", "Wedge", "decide, then write", "#9A4A0E", "#FFFAF5")]
# columns = dependency depth (plans/audit_dag.json v2: AB-14 after AB-11 + AB-13; AB-16 after AB-14; AB-17 sits under AB-16)
A_POS = {"AB-01": (0, 0), "AB-03": (0, 1), "AB-05": (0, 2), "AB-09": (0, 3), "AB-02": (1, 0), "AB-04": (1, 1), "AB-07": (1, 2),
         "AB-06": (2, 0), "AB-08": (2, 1), "AB-10": (0, 0), "AB-13": (0, 1), "AB-11": (2, 0), "AB-12": (2, 1), "AB-14": (3, 0),
         "AB-15": (0, 0), "AB-16": (4, 0), "AB-17": (4, 1)}
ACH = 150
A_HEAD = ["No blockers", "One step in", "Two steps in", "Three steps in", "Decide, then write"]


def acard(x, y, b):
    st = b["status"]
    done = sum(1 for t in b["closes"] if item(t)["status"] == "done") if b["closes"] else 0
    txt = {"done": "done", "in_progress": "in progress", "blocked": "waits on you"}.get(st, "to do")
    live = " · LIVE" if (b.get("llm_cost") or "none") != "none" else ""
    bg, bd, fg, style = STATUS[STATUS_OF.get(st, "todo")]
    return f"""<div style="position: absolute; left: {x}px; top: {y}px; width: {CW}px; height: {ACH}px; box-sizing: border-box; padding: 7px 10px; background: {bg}; border: 1.5px {style} {bd}; border-radius: 8px; display: flex; flex-direction: column; gap: 2px; overflow: hidden">
<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 6px"><span style="font-family: {MONO}; font-size: 12px; line-height: 16px; font-weight: 600; color: {fg}">{b["id"]}{live}</span><span style="font-size: 11px; line-height: 16px; font-weight: 600; color: {fg}">{txt}</span></div>
<span style="font-size: 13px; line-height: 17px; font-weight: 600">{html_escape(short_title(b["title"]))}</span>
<span title="{html_escape(b["note"])}" style="font-size: 12px; line-height: 16px; color: #4E5751; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 5; overflow: hidden">{html_escape(b["note"])}</span>
</div>"""


def short_title(t):
    import re as _re
    t = _re.sub(r"^LIVE( \(small\))?: ", "", t)
    return t.split(":")[0][:48]


def html_escape(x):
    import html as _h
    return _h.escape(x or "")


aparts, top = [], 44
for i, h in enumerate(A_HEAD):
    aparts.append(f'<div style="position: absolute; left: {CX[i]}px; top: 12px; width: {CW}px; font-size: 13px; line-height: 17px"><b>{h}</b></div>')
for key, name, sub, col, bg in A_LANES:
    lane = [b for b in AB if b.get("track") == key]
    rows = 1 + max((A_POS[b["id"]][1] for b in lane), default=0)
    h = rows * (ACH + 10) + 14
    aparts.append(f'<div style="position: absolute; left: 0; top: {top}px; width: {HOST_W}px; height: {h}px; background: {bg}; border-top: 1px solid #E3E6E0"></div>')
    aparts.append(f'<div style="position: absolute; left: 16px; top: {top + 12}px; width: 136px; display: flex; flex-direction: column; gap: 2px">{tag(name, col)}<span style="font-size: 13px; line-height: 17px; color: #4E5751">{sub}</span></div>')
    for b in lane:
        c, r = A_POS[b["id"]]
        aparts.append(acard(CX[c], top + 8 + r * (ACH + 10), b))
    top += h
audit_host = f"""<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
<div style="position: relative; width: {HOST_W}px; height: {top + 8}px">
{chr(10).join(aparts)}
</div>
</div>"""
audit_intro = '<div style="display: flex; flex-direction: column; gap: 6px">' + h2("Audit program: %d bundles, %d done, %d in progress, %d waiting on you" % (
    len(AB), sum(b["status"] == "done" for b in AB), sum(b["status"] == "in_progress" for b in AB), sum(b["status"] == "blocked" for b in AB))) + '<p style="margin: 0; max-width: 900px; font-size: 15px; line-height: 22px; color: #2C3631">%s</p></div>' % (
    "The audit program (plans/audit_dag.json) runs beside the Q1 plan and ends in the wedge decision (AB-16). Interviews (AB-10) no longer gate the market work or that decision. LIVE bundles spend API credit and are run by Uzair; every other bundle is free compute or desk work. Each card's note is the bundle's current result.")

body = "\n".join([
    title_block("%d Q1 bundles, and the pieces of the ledger with no bundle yet" % len(Q1B),
                "Bundles are how the theses get done. Each lane is a pillar from Level 3; red dashed cards are work a thesis needs that the Q1 plan does not yet schedule."),
    legend, host,
    f'<div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: stretch">{detail}{queue}</div>',
    audit_intro, audit_host,
    footer("%d of %d Q1 bundles and %d of %d audit bundles are done; the audit chapter closed on 14 Oct (DEC-05). The Q2 build, six bundles B0-B5, "
           "was built and read held out on 15 Oct, then read a second time as kernel v3: the ledger holds its invariants and meets "
           "the precision landmark for formula (status page)." % (
               sum(b["status"] == "done" for b in Q1B), len(Q1B), sum(b["status"] == "done" for b in AB), len(AB)),
           'choose between more scenarios (every open landmark is within one interval width of its bar) and a v4 aimed at links: missed and false links cause most wrong answers and most wrong directions.',
           "Stages.dc.html", "Zoom into one run"),
])

BODY = body
ZOOM = "Zoomed into: the Q1 plan"
TITLE = "4 Bundles"
