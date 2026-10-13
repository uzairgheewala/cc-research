"""Page 5: do learned graphs help decisions? Act II: AB-04 (decision value), AB-09 (theory pack, bounded harm)."""
from pagekit import *  # noqa: F401,F403

dv_table = table(
    ["Benchmark", "Method", "Its precision", "'Nothing moves', same files", "True CPDAG (ceiling)"],
    [["CausalArena semantic", "GIES with targets", n("ab04.sem.gies.prec"), n("ab04.sem.empty"), "1.000"],
     ["CausalArena formula", "GIES with targets", n("ab04.for.gies.prec"), n("ab04.for.empty"), "1.000"],
     ["CausalArena synthetic", "PC (default)", n("ab04.syn.pc.prec"), n("ab04.syn.empty"), "1.000"],
     ["Causal Chambers (physical truth)", "GES", n("ab04.ch.ges.prec"), n("ab04.ch.empty"), "1.000"]],
    mono_cols=(2, 3, 4),
    caption="DV-1: precision of the committed answers to 'if I set T, does Y move?', on exactly the files each method finished. "
            "On synthetic, PC is worse than answering 'nothing moves' everywhere.")

value_table = table(
    ["Benchmark", "Share of the ceiling's value the best method captures (wrong action costs as much as a right one gains)"],
    [["CausalArena semantic", f"{n('ab04.share.sem')} (GIES with targets)"],
     ["CausalArena formula", f"{n('ab04.share.for')} (GIES with targets)"],
     ["CausalArena synthetic", f"{n('ab04.share.syn')}; GES and PC are below doing nothing"]],
    caption="A stylised two-outcome decision, not a cost model of any real user.")

BODY = "\n".join([
    question("If you act on a learned graph, are you better off than assuming nothing moves?",
             before=f'{link("scoreboard", "page 4")}: the leaderboard number mixes method, layout and engine.'),
    P(f"A leaderboard asks whether arrows match. A decision asks something narrower: <i>if I set T, does Y move?</i> We ask every "
      f"learned graph that question for every target with released interventional data, and score the answers it commits to. "
      f"That is {T('dv')}. Two reference points make the number readable: the {T('emptygraph')}, which answers 'nothing "
      f"moves' every time, and the true CPDAG, the best any method could do from data."),
    dv_table,
    P("On CausalArena, most learned graphs sit within a few points of 'nothing moves', while the ceiling is far above them. On "
      "Causal Chambers, the one benchmark with physical ground truth and real interventions, GES does clearly better, within "
      f"{n('ab04.ch.gap')} of the ceiling. So the finding is a CausalArena result with a physical contrast, not a law of the field."),
    H2("How much of the possible value is captured"),
    value_table,
    H2("Two facts that make a careful system possible"),
    grid([
        box(f"{H3('Committing only when right pays')}<p class='prose' style='margin: 0'>Page 2 showed that under forced choice a "
            f"direction is worth committing only when its accuracy is above one half. Declining to commit, {T('abstain', 'abstention')}, "
            f"is therefore not a loss of nerve: on pairs a method gets wrong more often than right, it raises the score. "
            f"Replicate agreement already separates good claims from bad ones: the most-agreed {n('ab04.rc.share')} of GES and GIES "
            f"claims are {n('ab04.rc.prec')} precise.</p>"),
        box(f"{H3('Wrong knowledge does bounded harm')}<p class='prose' style='margin: 0'>If knowledge is only allowed to orient "
            f"connections the data already found, never to add or remove one, then wrong knowledge can cost at most the directions "
            f"it decided ({T('harm')}). The exact bound was checked {n('ab09.t3.checks')} times on every public CausalArena file "
            f"with {n('ab09.t3.violations', '{:.0f}')} violations.</p>"),
    ], min_w=380),
    answer("On CausalArena, mostly not: learned graphs capture a third to a half of the available decision value at best, and on "
           "synthetic data some are worse than assuming nothing moves. Real physical data are kinder. Two facts point to a better "
           "design: commit only when confident, and let knowledge orient but never connect.",
           "LLM agents promise to supply exactly that knowledge from variable names. Where do their directions actually come from?"),
])
