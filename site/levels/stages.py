from common import *

HOST_W, HOST_H = 1320, 400
XS = [24, 288, 552, 816, 1080]
W, BH, Y = 200, 104, 64

_r = lambda k: v("cc.%s" % k)  # noqa: E731
_S0 = [_r(a + ".S0.S") for a in ("real", "neutral", "swapped")]
_S1 = [_r(a + ".S1.S") for a in ("real", "neutral", "swapped")]
STAGES = [("S0 · algorithm", "FCI in %s of %s runs" % (t("cc.fci.runs"), t("cc.runs")), "S %.2f–%.2f" % (min(_S0), max(_S0)), "done"),
          ("S1 · bootstrap filter", "halves the skeleton", "S → %.2f–%.2f, %s of %s" % (min(_S1), max(_S1), t("cc.runs.S1_below_S0"), t("cc.runs")), "dec"),
          ("S2 · model review", "names enter here", "real: S back to %.2f" % _r("real.S2.S"), "prog"),
          ("S3 · KCI pruning", "changes almost nothing", "", "todo"),
          ("S4 · cycle step", "%s of %s crashed" % (t("cc.crashed"), t("cc.runs")), "judge_functions.py:562", "dec")]

parts = []
parts.append(f'<div style="position: absolute; left: 24px; top: 20px; font-size: 13px; line-height: 17px; color: #4E5751"><b style="color: #17201B">Causal-Copilot, unmodified</b> (upstream a31aa7c) · one run per scenario and name arm</div>')
for i, (ttl, a, b, st) in enumerate(STAGES):
    bg, bd, fg, style = STATUS[st]
    x = XS[i]
    extra = f'<br><span style="font-size: 13px; color: #4E5751">{b}</span>' if b else ""
    parts.append(f'<div style="position: absolute; left: {x}px; top: {Y}px; width: {W}px; height: {BH}px; box-sizing: border-box; padding: 10px; display: flex; align-items: center; justify-content: center; text-align: center; background: {bg}; border: 1.5px {style} {bd}; border-radius: 10px; font-size: 15px; line-height: 20px"><span><b>{ttl}</b><br>{a}{extra}</span></div>')
    if i < 4:
        parts.append(arrow_h(x + W + 2, Y + BH // 2, 60, "#8E2A2A" if i == 3 else "#4E5751"))

# bracket for v2 under S1-S3
bx, bw = XS[1], XS[3] + W - XS[1]
parts.append(f'<div style="position: absolute; left: {bx}px; top: {Y + BH + 22}px; width: {bw}px; height: 12px; border: 2px solid #9A4A0E; border-top: none; border-radius: 0 0 6px 6px; box-sizing: border-box"></div>')
parts.append(arrow_v(bx + bw // 2, Y + BH + 36, 34, "#9A4A0E"))
parts.append(f"""<div style="position: absolute; left: {bx}px; top: {Y + BH + 74}px; width: {bw}px; box-sizing: border-box; padding: 14px 18px; background: #FBEFE4; border: 1.5px solid #B85A12; border-radius: 10px; font-size: 14px; line-height: 20px">
<b style="font-family: {MONO}; color: #9A4A0E">BND-11 · refinement v2</b> replaces S1 to S3 as a drop-in (BLD-06). Data part keeps every S0 connection and adds one only at 0.9 bootstrap frequency; the names part asks three paraphrases and orients a pair only if all agree, the PAG marks allow it and no cycle forms; malformed answers are retried, then dropped.<br>
<b>Exploratory, on these same {t("v2.files")} tables:</b> never below S0 in {n("v2.R1.hits")} of {t("v2.files")}. The held-out test is pre-registered and waits on the free jobs.
</div>""")
parts.append(f'<div style="position: absolute; left: {XS[4]}px; top: {Y + BH + 74}px; width: {W}px; box-sizing: border-box; padding: 12px 14px; background: #FFFFFF; border: 1.5px dashed #8E2A2A; border-radius: 10px; font-size: 13px; line-height: 18px"><b>Cycle step:</b> v2 commits no direction that closes a cycle, so S4 has nothing to repair and no model call to fail.</div>')

host = f"""<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
<div style="position: relative; width: {HOST_W}px; height: {HOST_H}px">
{chr(10).join(parts)}
</div>
</div>"""

DATA = {lab: [(st,) + tuple(v("cc.%s.%s.%s" % (role, st, k)) for k in ("S", "c", "q", "a", "F1_forced", "F1_strict"))
             for st in ("S0", "S1", "S2", "S3")]
        for lab, role in (("Real names", "real"), ("Neutral names", "neutral"), ("Swapped names", "swapped"))}
td = "padding: 8px 12px"
tdm = f"padding: 8px 12px; font-family: {MONO}"
trs = []
for arm, rows in DATA.items():
    for k, (st, S, c, q, a, ff, fs) in enumerate(rows):
        first = f'<td rowspan="4" style="{td}; font-weight: 600; vertical-align: top">{arm}</td>' if k == 0 else ""
        bt = "border-top: 1px solid #C9CEC6" if k == 0 else "border-top: 1px solid #ECEEE9"
        trs.append(f'<tr style="{bt}">{first}<td style="{tdm}">{st}</td><td style="{tdm}">{S:.3f}</td><td style="{tdm}">{c:.3f}</td><td style="{tdm}">{q:.3f}</td><td style="{tdm}">{a:.3f}</td><td style="{tdm}; font-weight: 600">{ff:.3f}</td><td style="{tdm}; color: #4E5751">{fs:.3f}</td></tr>')
table = f"""<section style="display: flex; flex-direction: column; gap: 12px">
{h2("The same run under three name arms, in the coordinates of Level 2")}
<p style="margin: 0; max-width: 980px; color: #2C3631">S is skeleton F1, c the share of found pairs given a direction, q the share of those that are right, a = c·q + (1 − c)/2. Forced-choice F1 = a × S is comparable with the published table; strict F1 counts undecided pairs as misses. The paths these numbers trace are drawn on <a href="Bounds.dc.html">Level 2, projections 4 and 5</a>.</p>
<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">
<table style="width: 100%; min-width: 860px; border-collapse: collapse; font-size: 14px; line-height: 20px">
<thead><tr style="background: #F2F3EF; text-align: left">
<th style="{td}">Name arm</th><th style="{td}">Stage</th><th style="{td}">S</th><th style="{td}">c</th><th style="{td}">q</th><th style="{td}">a</th><th style="{td}">F1, forced choice</th><th style="{td}">F1, strict</th>
</tr></thead>
<tbody>{''.join(trs)}</tbody>
</table>
</div>
<p style="margin: 0; font-size: 13px; color: #4E5751">{t("cc.runs.per_role")} S2 test scenarios x 3 arms, one run each, scored up to S3 because {t("cc.crashed")} runs never finished S4. Per run: S falls at S1 in {n("cc.runs.S1_below_S0")} of {t("cc.runs")}; the model raises S in {n("cc.runs.real.S2_up")} of {t("cc.runs.per_role")} real-name runs and changes nothing in {n("cc.runs.neutral.S2_same")} of {t("cc.runs.per_role")} neutral runs. Source: analysis/space_coords.py (gates C2, C3 pass; S3 equals partial_stages.json).</p>
</section>"""

reads = f"""<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 16px">
<div style="padding: 16px 18px; background: #FFFFFF; border: 1px solid #C9CEC6; border-top: 4px solid #1D5C99; border-radius: 10px; font-size: 14px; line-height: 20px">
{tag("What the run says · T2", "#1D5C99")}
<p style="margin: 6px 0 0">Direction and connections come from the names. With real names the model review puts pairs back (S {t("cc.real.S1.S", "{:.2f}")} → {t("cc.real.S2.S", "{:.2f}")}) and commits far more directions (c {t("cc.real.S1.c", "{:.2f}")} → {t("cc.real.S2.c", "{:.2f}")}), at lower accuracy than the data's own (q {t("cc.real.S1.q", "{:.2f}")} → {t("cc.real.S2.q", "{:.2f}")}). With neutral names it changes nothing at all. With swapped names it removes more pairs and its directions fall to q {t("cc.swapped.S2.q", "{:.2f}")}.</p>
</div>
<div style="padding: 16px 18px; background: #FFFFFF; border: 1px solid #C9CEC6; border-top: 4px solid #9A4A0E; border-radius: 10px; font-size: 14px; line-height: 20px">
{tag("What it costs · T3(a)", "#9A4A0E")}
<p style="margin: 6px 0 0">Scored by the scoreboard's rule, the final graph is below the pipeline's own first stage in {n("cc.runs.final_below_S0")} of {t("cc.runs")} runs: real {n("cc.real.S0.F1_forced")} → {n("cc.real.S3.F1_forced")}, neutral {n("cc.neutral.S0.F1_forced")} → {n("cc.neutral.S3.F1_forced")}, swapped {n("cc.swapped.S0.F1_forced")} → {n("cc.swapped.S3.F1_forced")}. The bootstrap filter does most of the damage, before any name is read. Refinement v2's data part keeps every S0 connection for exactly this reason.</p>
</div>
<div style="padding: 16px 18px; background: #FFFFFF; border: 1px solid #C9CEC6; border-top: 4px solid #8E2A2A; border-radius: 10px; font-size: 14px; line-height: 20px">
{tag("Where it breaks · I7", "#8E2A2A")}
<p style="margin: 6px 0 0">All {n("cc.crashed")} crashes are runs whose S3 graph had a cycle; the cycle step's model answer could not be applied at judge_functions.py:562. {n("cc.crashed.real")} of them are real-name runs, so the arm that gains most also crashes most.</p>
</div>
</div>"""

crumb = f"""<nav aria-label="Breadcrumb" style="display: flex; flex-wrap: wrap; gap: 8px; font-size: 14px; color: #4E5751">
<a href="Main.dc.html">Space</a><span>›</span><span>orientation x D+K</span><span>›</span><a href="Theses.dc.html">T2, T3</a><span>›</span><a href="Bundles.dc.html">BND-08, BND-11</a><span>›</span><b style="color: #17201B">one run</b>
</nav>"""

body = "\n".join([
    crumb,
    title_block("One run, stage by stage",
                "The deepest zoom: where in Causal-Copilot's pipeline the names enter, what each stage does to the graph, and where our replacement plugs in."),
    host, table, reads,
    terms_panel(["stages", "bootstrap", "kci", "forced", "strict", "arms", "S", "c", "q"]),
    footer("we know which stage loses true connections (S1, the bootstrap filter), which stage takes direction from names (S2, the model review) and which line crashes (S4).",
           "test v2 on held-out tables, then replace the patch with the ledger kernel so every direction carries its source.",
           "Main.dc.html", "Back to the space"),
])

BODY = body
ZOOM = "Zoomed into: one Causal-Copilot run"
TITLE = "5 Stages"
