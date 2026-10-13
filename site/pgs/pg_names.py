"""Page 6: LLM agents read names, not data. Act II: BND-08 (Causal-Copilot stages), AB-07 (knowledge elicitation A3),
AB-05 (the upstream crash), AB-06 (the field audit, running)."""
from pagekit import *  # noqa: F401,F403
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
            f"{n('ab05.crash.runs')} of {n('ab05.crash.total')} live runs across two models. This is an upstream bug; we measure "
            f"Causal-Copilot as shipped and do not patch it.</p>"),
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
    H2("Next: the whole field"),
    P("One agent is an anecdote. The field audit runs four more LLM-using systems (causaliq-knowledge, PyWhy-LLM, MATMCD, "
      "Vashishtha et al.) on the same scenarios under the same three name arms, plus Causal-Copilot on a second model. Those runs "
      "are in progress; this page will add their results."),
    answer(f"From the names. Causal-Copilot's model review takes its directions from what the variables are called, follows "
           f"swapped labels against the data, and adds nothing when the names are neutral. Asked directly, the model orders "
           f"{t('ab07.o1.correct', '{:.0%}')} of true edges from names alone and follows swapped names, but its knowledge alone "
           f"scores below a data-only method.",
           "Is there any real setting where stated structure, used carefully, beats learning the graph?"),
])
