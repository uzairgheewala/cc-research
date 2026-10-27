"""Quarter 1: fixing Causal-Copilot's review step (S35, 27 Oct; BLD-06, EXT-03, DLV-04, DLV-07). The live comparison of
refinement v2 against the unmodified pipeline on the 30 Quarter 1 tables, why the original loses links and crashes, how cycles
are handled now, one link traced through both versions, and what is not established yet. Every number comes from the
registry (q1.*); the reproduction is the public Quarter 1 repository."""
from pagekit import *  # noqa: F401,F403
import common

n = common.n
F3, D3, USD = "{:.3f}", "{:+.3f}", "${:.2f}"
Q1REPO = "https://github.com/uzairgheewala/causal-copilot-q1"
FORK = "https://github.com/uzairgheewala/Causal-Copilot"


def iv(key):
    return f'{n("q1.%s.point" % key, D3)} (interval {n("q1.%s.lo" % key, D3)} to {n("q1.%s.hi" % key, D3)})'


TABLE = table(["", "Unmodified", "Refinement v2", "Paired difference"], [
    ["Runs completed", f'{n("q1.done.main")} of {n("q1.arms")}', f'{n("q1.done.branch")} of {n("q1.arms")}', ""],
    ["The algorithm's own graph: links recovered (all tables)", n("q1.S0_adj_f1.main", F3), n("q1.S0_adj_f1.branch", F3), iv("L3")],
    ["Delivered graph: links recovered (tables both completed)", n("q1.final_adj_f1.main", F3), n("q1.final_adj_f1.branch", F3), iv("L2")],
    ["Delivered graph: arrows recovered (same tables)", n("q1.final_dir_f1.main", F3), n("q1.final_dir_f1.branch", F3), iv("L2_dir")],
    ["Arrows a user receives (a crash delivers nothing, scored 0)", n("q1.delivered_dir_f1.main", F3), n("q1.delivered_dir_f1.branch", F3), iv("L1")],
    ["API cost of the series", n("q1.usd.main", USD), n("q1.usd.branch", USD), ""],
], caption="Links recovered is adjacency F1 (right pairs, any direction); arrows recovered is directed F1 (only committed arrows "
           "count). The paired difference is refinement v2 minus unmodified on the same table, with a 95% interval that resamples the "
           "10 scenarios.")

BODY = "\n".join([
    question("What does Causal-Copilot's review step do to the graph its algorithm found, and does our replacement do better?"),
    P(f'After Causal-Copilot runs a discovery algorithm, a review step refines the graph: it resamples the data, sorts every link '
      f'by how often it reappears, has the model review the doubtful ones, prunes with an independence test and breaks cycles. '
      f'<a href="copilot/step-refinement.html">Inside Causal-Copilot</a> walks through that step in its code. This page '
      f'is the Quarter 1 result: what the step does on tables whose true graph is known, and what our replacement changes.'),
    H2("The comparison"),
    ul(["The same 30 tables: 10 benchmark scenarios, each with real, neutral and swapped column names on identical numbers, "
        "columns shuffled.",
        "The same Docker image and the same model, run on 21-22 October; the agent's code checked before every run.",
        f'A rule written and hashed before any graph was scored (sha256 <code>{n("q1.prereg")}</code>). Its outcome: '
        f'<b>{n("q1.rule")}</b>: the replacement loses no more than 0.02 in links recovered, and the two versions start '
        f'from the same algorithm output.'], 15),
    TABLE,
    answer(f'The replacement keeps the links the data support ({n("q1.final_adj_f1.branch", F3)} against '
           f'{n("q1.final_adj_f1.main", F3)}), finishes every run, and costs {n("q1.usd.branch", USD)} against '
           f'{n("q1.usd.main", USD)}. Whether it also gets more arrows right is not established: that interval includes zero.',
           "When should the review commit to an arrow, and when should it leave the direction open?"),
    H2("Why the original loses links and crashes"),
    ul([f'<b>Links.</b> The original sorts each link by how often its <i>arrow</i> reappears in the resamples, not how often the '
        f'pair stays linked. A link the algorithm found but could not orient looks weak, and the rule deletes it. The algorithm\'s '
        f'own graphs recover links at {n("q1.S0_adj_f1.main", F3)} (all {n("q1.arms")} tables); the delivered graphs at '
        f'{n("q1.final_adj_f1.main", F3)} (the {n("q1.both")} that completed in both versions).',
        f'<b>Crashes.</b> The cycle step asks the model which link to remove, but its prompt never names the key the code then '
        f'reads. In this series {n("q1.cyc.main.entered")} runs reached the cycle step and {n("q1.cyc.main.keyerr")} of them '
        f'crashed there (a KeyError on <code>nodes</code>).'], 15),
    H2("What we changed"),
    ul([f'<b>Refinement v2</b> (fork branch <a href="{FORK}/compare/main...bld-06-refinement-v2">bld-06-refinement-v2</a>, '
        f'two files). It never deletes a link the algorithm found; it adds a link only if at least 90% of resamples have it; each '
        f'pair takes its commonest mark. The model is asked only about pairs the data leave without a direction, three '
        f'phrasings, used only if all three agree.',
        f'<b>Cycles.</b> Refinement v2 replaces the whole original sequence, cycle step included, so the crash cannot happen: '
        f'{n("q1.cyc.branch.entered")} runs entered the cycle step. The model may not set a direction that would close a cycle. '
        f'The data part has no such guard: {n("q1.cyc.branch.cyclic")} of {n("q1.cyc.branch.done")} delivered graphs contain a '
        f'directed cycle, a measured result, not a guarantee (checked after the series, not pre-registered).',
        f'<b>The original\'s cycle step, fixed</b> (branch <a href="{FORK}/compare/main...ext-03-cycle-step-key">'
        f'ext-03-cycle-step-key</a>): the prompt names the key, the reply is read defensively, and an unusable answer falls back '
        f'to a fixed choice. Tested on {n("q1.x03.runs")} offline runs with a stand-in model ({n("q1.x03.keyerr")} crashes); '
        f'not yet run live.'], 15),
    H2("One true link, both versions"),
    P(f'In a solder-reflow scenario the true link is entrained gas → voids. Both versions start from the algorithm\'s graph: '
      f'linked, direction open. {n("q1.q011.conn")} of 20 resamples link the pair.'),
    ul([f'<b>Unmodified:</b> the arrow gas → voids reappears in {n("q1.q011.main.true")} of 20 resamples, so the rule deletes the '
        f'link. The model, asked later, calls the relationship not clearly established, and the link stays deleted.',
        f'<b>Refinement v2:</b> keeps the link, but the commonest mark is the backward arrow ({n("q1.q011.br.back")} of 20, against '
        f'{n("q1.q011.br.oo")} for "linked, direction open"). A plurality, not a majority, decides; once the data set a direction '
        f'the model is never asked.'], 15),
    P(f'The full trace, with the run files it comes from: <a href="{Q1REPO}/blob/main/analysis/reports/run_trace/q011_gas_void.md">'
      f'the gas/void walkthrough</a>. One pair cannot set a threshold; it becomes a regression check for the next rule.', 15),
    H2("Not established yet"),
    ul(["Better arrows: the gain on directed F1 has an interval that includes zero.",
        "Breadth: one run per table and arm, one model, 10 scenarios from one benchmark.",
        "The cycle-step fix on its own: offline runs only."], 15),
    H2("Next"),
    P("A rule for when the evidence is strong enough to commit to an arrow, and otherwise to leave the direction open. It is "
      "developed on saved runs (no new spending), compared with the current rule on the same inputs, with wrong arrows, right "
      "arrows, open directions and links reported separately, and frozen before it sees new cases.", 15),
    H2("Check it yourself"),
    P(f'The public <a href="{Q1REPO}">Quarter 1 repository</a> recomputes the table above from the recorded runs with one command, '
      f'no API key: <code>python run.py reproduce</code>. Its <a href="{Q1REPO}/blob/main/docs/code_tour.md">code tour</a> and '
      f'<a href="{Q1REPO}/blob/main/docs/method.md">method notes</a> explain the controls and the metrics.', 15),
])
