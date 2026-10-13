"""Page 4: the scoreboard is not what it seems. Act II: AB-01 (controlled scoreboard), AB-02 (Bayesys), AB-03 (engines),
BND-06 (the vendored PC)."""
from pagekit import *  # noqa: F401,F403

channels = table(
    ["Channel", "What it does", "Size (CausalArena semantic, directed F1)", "Who it affects"],
    [[f"{T('indexrule', 'Index tie-break')}", "The scoring code orients every undecided pair from the earlier column to the later one.",
      f"FCI gains {n('ab01.fci.index.sem')}; PC with maxP {n('ab01.maxp.index.sem')}; GES {n('ab01.ges.index.sem')}",
      "every method that leaves pairs undecided"],
     [f"{T('conflict', 'Conflict rule')}", "PC's default way of settling two colliders that disagree depends on which column it visits first.",
      f"PC loses {n('ab01.pc.conflict.sem')} on the released order against shuffled columns; with maxP the gap is {n('ab01.maxp.conflict.sem')}",
      "PC with its default settings"],
     [f"{T('engine', 'Engine defect')}", "A bug in the library that runs the algorithm.",
      f"Causal-Copilot's bundled PC changes its skeleton with column order in {n('pc.order.changed')} of {n('pc.order.files')} files; "
      f"the current library release in {n('pc.order.changed.upstream')}",
      "anyone running that copy"]],
    caption="Source: AB-01 controlled scoreboard and BND-06; every number links to its file.")

corrected = table(
    ["Method", "Published", "Controlled (columns shuffled, undecided pairs at random)"],
    [["PC (semantic)", n("pub.sem.D.PC"), f"{n('ab01.sem.maxp.ctrl', bold=True)} with maxP, no other change"],
     ["PC (formula)", n("ab01.pub.for.pc"), f"{n('ab01.for.maxp.ctrl', bold=True)} with maxP"],
     ["PC (synthetic)", n("ab01.pub.syn.pc"), f"{n('ab01.syn.maxp.ctrl', bold=True)} with maxP"],
     ["GES (semantic)", n("pub.sem.D.GIES"), n("ab01.ges.ctrl.sem")],
     ["GIES with intervention targets (semantic, D+I)", n("pub.sem.DI.best"), n("ab01.gies.ctrl.sem")]],
    mono_cols=(1, 2),
    caption="GES is listed as GIES on the published board for regime D. Controlled numbers come from the files we could run "
            "(225-250 per row); published ones from all 100 scenarios.")

engines = table(
    ["Library", "Exact answers with perfect information (of 720)", "Same answer in every column order (of 120 graphs)", "Defect"],
    [["causal-learn (current release), PC and FCI", "720", "120", "none"],
     ["Causal-Copilot's bundled copy of causal-learn PC", n("ab03.vendored.exact"), n("ab03.vendored.inv"), "extra connections; order-dependent"],
     ["gCastle PC, original and stable variants", "456-460", "56", "extra connections; order-dependent"],
     ["dodiscover PC", f"{n('ab03.dodiscover.exact')} of {n('ab03.dodiscover.n')}", "88", "wrong or cyclic orientations"],
     ["pgmpy PC, tigramite PCMCI+", "720", "120", "none"]],
    caption="AB-03: 120 random graphs, 6 column orders each, with a perfect independence oracle. A correct engine returns the "
            "true CPDAG every time.")

BODY = "\n".join([
    question("Do published scores measure methods, or how the files happen to be laid out?",
             before=f'{link("scoring", "page 2")} (F1 = S × a, forced choice) and {link("space", "page 3")} (the cell the leaderboard covers).'),
    P(f"CausalArena's released files list their columns in causal order: causes come before their effects. That is a {T('leak')}. "
      f"A rule that ignores the data and just points every pair from the earlier column to the later one scores "
      f"{n('leak.released', bold=True)} directed F1 on the semantic family, more than every published method. With the "
      f"{T('shuffle', 'columns shuffled')}, the same rule scores {n('leak.shuffled')}."),
    P("A method does not have to read column positions on purpose to benefit. We found three channels through which the layout, "
      "or the software, moves a published number."),
    channels,
    H2("Corrected for layout, PC is a much better method than its published row"),
    P("Scoring every method we could run with shuffled columns and random tie-breaking removes the first two channels. PC with an "
      "order-free conflict rule, a configuration change and nothing else, rises to third place among the published methods "
      "on the semantic family, behind only FoundCause and GIES."),
    corrected,
    H2("The engines themselves"),
    P("Feeding each library a perfect-information oracle, where the right answer is known exactly, separates the method from its "
      "implementation. Two widely used Python libraries and Causal-Copilot's bundled copy fail."),
    engines,
    H2("A second benchmark: Bayesys"),
    P(f"Bayesys (Constantinou et al., 2021) is a second public benchmark with released files and published scores. Three of its "
      f"six networks are also released in topological column order. We first reproduced its published table: "
      f"{n('ab02.repro.cells')} of {n('ab02.repro.compared')} PC-Stable and FCI cells match within a pre-stated tolerance "
      f"(PC: {n('ab02.repro.pc')} of {n('ab02.repro.pc.n')})."),
    P(f"Then the twist. Bayesys scores with {T('halfcredit')}: a true connection with the wrong or no direction counts half. "
      f"Under that rule, shuffling the columns moves PC, maxP and FCI by at most {n('ab02.order.max.pc')}. An index tie-break "
      f"would be worth {n('ab02.index.lo')} to {n('ab02.index.hi')} F1 on those three networks, but Bayesys's scoring never uses one. Whether a benchmark's layout "
      f"inflates its leaderboard depends on its scoring rule. The engine channel shows up on both: causal-learn's GES scores "
      f"up to {n('ab02.ges.property')} lower on one network's released order than on shuffled ones."),
    answer(f"Partly the layout. On CausalArena, the scoring rule rewards an index tie-break and PC's default conflict rule punishes "
           f"the released order; controlled for both, PC rises from {t('pub.sem.D.PC')} to {t('ab01.sem.maxp.ctrl')}. Bayesys is "
           f"robust to its layout because of how it scores. Engine bugs move numbers on both.",
           "Leaving the scoreboard aside: is a learned graph worth acting on at all?"),
])
