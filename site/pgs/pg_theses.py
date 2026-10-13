"""Page 8: theses and the claim ledger. Act III: what the project claims (six theses, three pillars), what it would build
(the claim ledger and its invariants), and the build order Uzair set on 13 Oct (reliability before features)."""
from pagekit import *  # noqa: F401,F403
import main as L1
import theses as L3

pillars_intro = P(f"Acts I and II leave three open questions, and the project splits into three {T('pillar', 'pillars')} to "
                  f"answer them. P1, measurement: where does each system's direction come from, and how far is it from the limit? "
                  f"P2, the {T('ledger', 'claim ledger')}: can a system use knowledge on purpose, say where every direction came "
                  f"from, and never fall below its data? P3, decisions: do better directions turn into better answers to 'what "
                  f"if we set X' and better choices of experiment?")

reliability = box(
    f"{H3('Build order: reliability before features')}"
    f"<p class='prose' style='margin: 0'>Decided on 13 Oct 2026: the audit product (page 9) is the more valuable one, but nothing is "
    f"built on top until the ledger itself is reliable. That means its {T('invariant', 'invariants')} hold by construction and are "
    f"tested, it never scores below its own data-only output, wrong knowledge does bounded harm, and {T('calib', 'calibration')} "
    f"and abstention are measured on held-out data before anyone is asked to trust them. In decisions as sensitive as these, "
    f"reliability is the product.</p>", tone="orange")

matrix = section(
    H2("The grid again, with what has been measured"),
    P("Page 3 showed the grid with limits and published numbers. Here it is with our measurements, the agent from page 6, and "
      "the pillar that owns each cell. The thick cell, orientation with declared knowledge, is where the ledger aims: no published "
      "method reports a number there."),
    f'<div style="display: flex; flex-wrap: wrap; gap: 16px">{L1.legend}</div>',
    L1.matrix)

BODY = "\n".join([
    question("What does this project claim, and what would it build?",
             before=f'Acts I and II: {link("scoring", "the limits")}, {link("scoreboard", "the scoreboard")}, '
                    f'{link("decisions", "decision value")}, {link("names", "the agents")} and {link("rca", "declared structure")}.'),
    P(f"Everything so far was measurement. This page states what the project claims and what it plans to build. Each claim is a "
      f"{T('thesis')}: it says what would refute it, written down before the evidence came in, and what the evidence says today. "
      f"Effects answered with an {T('ident', 'identification status')} rely on {T('ida', 'IDA')}, which lists every effect "
      f"consistent with the equivalence class. Each card names the {T('ticket', 'tickets')} that hold its evidence; the work "
      f"that tests it is organised in {T('bundle', 'bundles')}, and the decisions it feeds are taken at {T('gate', 'gates')}."),
    pillars_intro,
    reliability,
    P("Each card below gives the claim, what would refute it (written before the evidence), what the evidence says today, and "
      "the route from where it stands to the limit.", 15),
    delevel(L3.cols),
    delevel(L3.invariants),
    answer("Six theses, in three pillars. The measurement theses are mostly settled and have already corrected the plan; the "
           "system theses, a claim ledger that keeps every direction's source, abstains when unsure and never falls below its data, "
           "are where the distance to the limit is closed, and they come first in the build, before any product.",
           "Who would use such a system, and is there a market for it?"),
])
