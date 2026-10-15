"""Page 6: LLM agents read names, not data. Act II: BND-08 (Causal-Copilot stages), AB-07 (knowledge elicitation A3),
AB-05 (the upstream crash, the Vashishtha truncation), AB-06 (Causal-Copilot on a second model; the field audit)."""
from pagekit import *  # noqa: F401,F403
from common import v
from common import arrow_h, STATUS as ST
from plots import plane_Sa, plane_cq

# ---- the pipeline, as shipped (no project additions on this page)
XS, W, BH, Y = [16, 252, 488, 724, 960], 190, 104, 54
_r = lambda k: v("cc.%s" % k)  # noqa: E731
_S0 = [_r(a + ".S0.S") for a in ("real", "neutral", "swapped")]
_S1 = [_r(a + ".S1.S") for a in ("real", "neutral", "swapped")]
STAGES = [("S0 · algorithm", "FCI in %s of %s runs" % (t("cc.fci.runs"), t("cc.runs")), "S %.2f–%.2f" % (min(_S0), max(_S0)), "done"),
          ("S1 · bootstrap filter", "halves the skeleton", "S → %.2f–%.2f" % (min(_S1), max(_S1)), "dec"),
          ("S2 · model review", "names enter here", "real names: S back to %.2f" % _r("real.S2.S"), "prog"),
          ("S3 · KCI pruning", "changes almost nothing", "", "todo"),
          ("S4 · cycle step", "%s of %s runs crashed" % (t("cc.crashed"), t("cc.runs")), "judge_functions.py:562", "dec")]
parts = ['<div style="position: absolute; left: 24px; top: 14px; font-size: 13px; color: #4E5751"><b style="color: #17201B">'
         'Causal-Copilot, unmodified</b> (upstream a31aa7c) · one run per scenario and name arm</div>']
for i, (ttl, a_, b_, st) in enumerate(STAGES):
    bg, bd, fg, style = ST[st]
    extra = f'<br><span style="font-size: 13px; color: #4E5751">{b_}</span>' if b_ else ""
    parts.append(f'<div style="position: absolute; left: {XS[i]}px; top: {Y}px; width: {W}px; height: {BH}px; box-sizing: border-box; '
                 f'padding: 10px; display: flex; align-items: center; justify-content: center; text-align: center; background: {bg}; '
                 f'border: 1.5px {style} {bd}; border-radius: 10px; font-size: 15px; line-height: 20px"><span><b>{ttl}</b><br>{a_}{extra}</span></div>')
    if i < 4:
        parts.append(arrow_h(XS[i] + W + 2, Y + BH // 2, 42, "#8E2A2A" if i == 3 else "#4E5751"))
pipeline = f'<div style="position: relative; width: 1160px; height: {Y + BH + 24}px">{"".join(parts)}</div>'

rows = []
for lab, role in (("Real names", "real"), ("Neutral names", "neutral"), ("Swapped names", "swapped")):
    for k, st in enumerate(("S0", "S1", "S2", "S3")):
        vals = [n("cc.%s.%s.%s" % (role, st, c)) for c in ("S", "c", "q", "a", "F1_forced", "F1_strict")]
        rows.append([f"<b>{lab}</b>" if k == 0 else "", st] + vals)
stage_table = table(["Name arm", "Stage", "S", "c", "q", "a", "F1, forced choice", "F1, strict"], rows, mono_cols=range(1, 8),
                    caption=f"{t('cc.runs.per_role')} test scenarios × 3 name arms, one run each, scored up to S3 because "
                            f"{t('cc.crashed')} runs never finished S4.")

a3 = table(["Names shown to the model", "True edges ordered correctly", "Contradicted", "What it means"],
           [["Real names", n("ab07.o1.correct", "{:.1%}"), n("ab07.o1.contra", "{:.1%}"), "the model knows the order the names suggest"],
            ["Neutral names (V01, V02, …)", "—", "—", "it puts every variable in one tier: names were all it had"],
            ["Swapped names, scored against the labels", n("ab07.o3.label.correct", "{:.1%}"), n("ab07.o3.label.contra", "{:.1%}"),
             "the order follows the labels"],
            ["Swapped names, scored against the data", "", "", f"correct minus contradicted {n('ab07.o3.data')}: worse than chance"]],
           mono_cols=(1, 2),
           caption=f"AB-07: 900 pre-registered requests to gpt-4o, names only, no data, on 50 semantic and 50 formula scenarios. "
                   f"Regression on the model's tiers alone scores {n('ab07.o4')} (semantic), below a data-only method.")

orient = table(["GES on CausalArena semantic", "Directed F1", "Decision-value precision"],
               [["Data only", n("ab07.ges.data.f1"), n("ab07.ges.data.dv")],
                ["+ the model's tiers, used only to orient", n("ab07.ges.model.f1"), n("ab07.ges.model.dv")],
                ["+ tiers from the true order (oracle)", n("ab07.ges.oracle.f1"), n("ab07.ges.oracle.dv")],
                ["+ tiers from swapped names (wrong knowledge)", n("ab07.ges.moved.f1"), n("ab07.ges.moved.dv")]],
               mono_cols=(1, 2), caption="Exploratory, decided after the run: tiers may orient a connection GES already found, never add one.")

_f1 = figure(plane_Sa(), "S against a. The green region beats every published method.")
_f2 = figure(plane_cq(), "c against q. Committing more directions pays only above the red line (q above one half).")
PLOTS = ('<div style="display: flex; flex-wrap: wrap; gap: 20px"><div style="flex: 1 1 560px; min-width: 0">' + _f1 +
         '</div><div style="flex: 1 1 560px; min-width: 0">' + _f2 + '</div></div>')

# ---- the field audit (AB-06): one row per system, real / neutral / swapped mean directed F1, data-only tick for hybrids
_ROWS = [("Causal-Copilot, gpt-4o *", "cc4o", True, None), ("Causal-Copilot, gpt-4o-mini *", "ccmini", True, None),
         ("causaliq-knowledge", "causaliq", True, None), ("PyWhy-LLM", "pywhyllm", False, None),
         ("MATMCD", "matmcd", True, "ab06.matmcd.floor"), ("Vashishtha et al.", "vashishtha", False, "ab06.vashishtha.floor")]
_W, _L, _R, _RH, _T = 1000, 240, 200, 40, 34
_X = lambda f: _L + f / 0.6 * (_W - _L - _R)  # noqa: E731
_C = {"real": "#2A78D6", "swapped": "#EB6834", "neutral": "#1BAF7A"}
_parts = []
for _g in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
    _parts.append(f'<line x1="{_X(_g):.1f}" y1="{_T - 10}" x2="{_X(_g):.1f}" y2="{_T + _RH * len(_ROWS)}" stroke="#E2E4DF"/>'
                  f'<text x="{_X(_g):.1f}" y="{_T + _RH * len(_ROWS) + 18}" text-anchor="middle" font-size="12" fill="#4E5751">{_g:.1f}</text>')
for _i, (_lab, _k, _neu, _fl) in enumerate(_ROWS):
    _y = _T + _RH * _i + _RH / 2
    _re, _sw = v("ab06.%s.real" % _k), v("ab06.%s.swapped" % _k)
    _nr = v("ab06.%s.nr" % _k)
    _parts.append(f'<text x="{_L - 14}" y="{_y + 5:.1f}" text-anchor="end" font-size="14" fill="#17201B">{_lab}</text>'
                  f'<line x1="{_X(_sw):.1f}" y1="{_y:.1f}" x2="{_X(_re):.1f}" y2="{_y:.1f}" stroke="#C9CEC6" stroke-width="3"/>')
    if _fl:
        _parts.append(f'<line x1="{_X(v(_fl)):.1f}" y1="{_y - 15:.1f}" x2="{_X(v(_fl)):.1f}" y2="{_y + 15:.1f}" stroke="#17201B" stroke-width="3"/>')
    _parts.append(f'<circle cx="{_X(_sw):.1f}" cy="{_y:.1f}" r="6.5" fill="{_C["swapped"]}" stroke="#FFFFFF" stroke-width="2"/>'
                  f'<circle cx="{_X(_re):.1f}" cy="{_y:.1f}" r="6.5" fill="{_C["real"]}" stroke="#FFFFFF" stroke-width="2"/>')
    if _neu:
        _parts.append(f'<circle cx="{_X(v("ab06.%s.neutral" % _k)):.1f}" cy="{_y:.1f}" r="8" fill="none" stroke="{_C["neutral"]}" stroke-width="2.5"/>')
    _parts.append(f'<text x="{_W - _R + 16}" y="{_y + 5:.1f}" font-size="13" fill="#4E5751">real − swapped {_nr:+.3f}</text>')
_leg = "".join(f'<circle cx="{_L + 150 * j + 8}" cy="14" r="6.5" fill="{c if j != 1 else "none"}" stroke="{c if j == 1 else "#FFFFFF"}" '
               f'stroke-width="{2.5 if j == 1 else 2}"/><text x="{_L + 150 * j + 20}" y="19" font-size="13" fill="#4E5751">{lab}</text>'
               for j, (c, lab) in enumerate(((_C["real"], "real names"), (_C["neutral"], "neutral names"), (_C["swapped"], "swapped names"))))
_leg += (f'<line x1="{_L + 458}" y1="6" x2="{_L + 458}" y2="22" stroke="#17201B" stroke-width="3"/>'
         f'<text x="{_L + 468}" y="19" font-size="13" fill="#4E5751">own data-only graph</text>')
_svg = (f'<div style="overflow-x: auto"><svg viewBox="0 0 {_W} {_T + _RH * len(_ROWS) + 30}" width="100%" '
        f'style="max-width: {_W}px; min-width: 760px; display: block" role="img" '
        f'aria-label="Mean directed F1 by system and name arm">{_leg}{"".join(_parts)}</svg></div>')
FIELD = figure(_svg, f"Mean directed F1 with real, neutral and swapped names, columns shuffled. P9 (at least three of five systems "
                     f"lose 0.10 or more) is {t('ab06.P9')}; P10 (one agent falls below its own data-only graph) is "
                     f"{t('ab06.P10')}. * Causal-Copilot is scored on BND-08's ten test scenarios at the graph before its cycle "
                     f"step; PyWhy-LLM and Vashishtha ran the real and swapped arms on five scenarios.")

BODY = "\n".join([
    question("Where does an LLM agent's direction come from?",
             before=f'{link("scoring", "page 2")} (S, c, q, a) and {link("space", "page 3")} (name arms: real, neutral, swapped).'),
    P(f"LLM agents for causal discovery, such as Causal-Copilot, run a classical algorithm and then let a language model review "
      f"the result. The model sees the variable names. We ran Causal-Copilot as shipped on CausalArena's named scenarios under the "
      f"three name arms, with columns shuffled, and scored the graph after every stage, {T('stages')}."),
    figure(pipeline, f"Stage S1, a {T('bootstrap')} filter, removes about half of the true connections before any name is read. "
                     f"S2 is where names enter. S3 runs a {T('kci', 'KCI')} test. S4, the cycle step, crashed in "
                     f"{n('cc.crashed')} of {t('cc.runs')} runs."),
    stage_table,
    H2("What the stages show"),
    grid([
        box(f"{H3('Directions come from the names')}<p class='prose' style='margin: 0'>With real names the model review puts pairs "
            f"back and commits far more directions, at lower accuracy than the data's own (q {t('cc.real.S1.q', '{:.2f}')} → "
            f"{t('cc.real.S2.q', '{:.2f}')}). With neutral names it changes nothing in {n('cc.runs.neutral.S2_same')} of "
            f"{t('cc.runs.per_role')} runs. With swapped names it follows the labels on {n('cc.M3.hits')} of {n('cc.M3.n')} "
            f"edges.</p>"),
        box(f"{H3('The pipeline ends below its own start')}<p class='prose' style='margin: 0'>Scored by the leaderboard's rule, the "
            f"final graph is below the pipeline's first stage in {n('cc.runs.final_below_S0')} of {t('cc.runs')} runs: real "
            f"{n('cc.real.S0.F1_forced')} → {n('cc.real.S3.F1_forced')}, swapped {n('cc.swapped.S0.F1_forced')} → "
            f"{n('cc.swapped.S3.F1_forced')}.</p>"),
        box(f"{H3('It crashes on its own key')}<p class='prose' style='margin: 0'>The cycle step reads a key, <code>nodes</code>, "
            f"that its prompt never asks the model for. Whenever the model names it differently the run dies: "
            f"{n('ab05.crash.runs')} of {n('ab05.crash.total')} live entries into the cycle step crashed, across two models. This is "
            f"an upstream bug; we measure Causal-Copilot as shipped and do not patch it.</p>"),
    ], min_w=320),
    H2("The model's knowledge, measured without any agent"),
    P(f"To separate the model from the pipeline, we asked gpt-4o for {T('tier', 'tiers')} from the names alone, with no data at all, "
      f"in a pre-registered test ({T('elicit')})."),
    a3,
    P("Used carefully, that knowledge still helps: if the tiers may only orient connections the data already found, GES improves "
      "a little, and wrong tiers cost a bounded amount, exactly as page 5's bounded-harm result says."),
    orient,
    H2("The agent's path through the scoring space"),
    P(f"On page 2, every score was S × a. Plotting the stages in those coordinates shows the moves: the bootstrap filter moves "
      f"every arm left (fewer true connections), real names move it back right and down in accuracy, neutral names leave it "
      f"where it is. Grey curves are points of equal F1 ({T('iso', 'iso-F1 curves')})."),
    PLOTS,
    H2("A second model, and the rest of the field"),
    P(f"On gpt-4o-mini the same 30-run design gives the same structure with a smaller name effect. Swapped names cost "
      f"{n('ab06.cc.reliance')} directed F1 at S3, against {n('ab06.cc.reliance.4o')} on gpt-4o, and without names the agent "
      f"ends below plain PC in {n('ab06.cc.m4.hits')} of {n('ab06.cc.m4.families')} families. On the smaller model the review "
      f"lowers directed F1 even with real names ({n('ab06.cc.real.S0', '{:.3f}')} → {n('ab06.cc.real.S3', '{:.3f}')}): its "
      f"knowledge does not pay for what the pipeline throws away."),
    P(f"Output-format failures are not unique to Causal-Copilot. Vashishtha et al. ask the model for its reasoning before a "
      f"tagged answer and cap the reply at 300 tokens. On the model their README documents, {n('ab05.vash.untagged', '{:.0%}')} "
      f"of {n('ab05.vash.triplets', '{:,}')} triplet answers stop before the tag and cast no vote, which leaves "
      f"{n('ab05.vash.ties')} of {n('ab05.vash.pairs')} pairs to a tie-breaker. The run finishes without an error. Causal-Copilot "
      f"fails loudly; this fails silently."),
    P(f"The pre-registered field audit then ran four more systems under the same three name arms, with columns shuffled. Name "
      f"reliance is common: with swapped names, causaliq-knowledge loses {n('ab06.causaliq.nr', '{:.3f}')} directed F1, "
      f"Causal-Copilot {n('ab06.cc4o.nr', '{:.3f}')} and MATMCD {n('ab06.matmcd.nr', '{:.3f}')}; PyWhy-LLM loses "
      f"{n('ab06.pywhyllm.nr', '{:.3f}')} on {n('ab06.pywhyllm.nrn')} scenario pairs. The one system that resists, Vashishtha et "
      f"al. ({n('ab06.vashishtha.nr', '{:.3f}')}), is the one whose data decide its graph: PC's arrows are kept, and the "
      f"model's order only orients the pairs PC leaves open ({n('ab06.vash.llm_order')} arrows, against "
      f"{n('ab06.vash.data')} from PC)."),
    FIELD,
    P(f"Knowledge can also make an agent worse than its own data. MATMCD lets a model's 'no' forbid an edge, so its last PC "
      f"run deletes connections the data had found. With real names its {T('dv', 'decision-value')} precision falls from "
      f"{n('ab06.matmcd.dv.floor', '{:.3f}')} (its own PC graph) to {n('ab06.matmcd.dv', '{:.3f}')}. With neutral or swapped "
      f"names its F1 drops from {n('ab06.matmcd.floor', '{:.3f}')} to {n('ab06.matmcd.neutral', '{:.3f}')} and "
      f"{n('ab06.matmcd.swapped', '{:.3f}')}, below its own PC graph in {n('ab06.matmcd.below.neutral')} and "
      f"{n('ab06.matmcd.below.swapped')} of 10 scenarios."),
    answer(f"From the names, in every system that lets the model decide a connection. Swapped names cost three of the five "
           f"systems 0.10 or more in directed F1 (a fourth, PyWhy-LLM, loses as much on fewer pairs than the rule needs), and "
           f"one hybrid falls below its own data-only graph. The system that "
           f"resists is the one whose data decide the graph and whose model only orients what the data leave open. Asked "
           f"directly, the model orders {t('ab07.o1.correct', '{:.0%}')} of true edges from names alone and follows swapped "
           f"names, but its knowledge alone scores below a data-only method.",
           "Is there any real setting where stated structure, used carefully, beats learning the graph?"),
])
