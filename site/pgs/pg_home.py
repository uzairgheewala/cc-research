"""Home: what the project is, three ways in, the headline findings, and where the product question stands. Leads with the
research and links the market/wedge (Uzair, 13 Oct). Exempt from the term scan: terms link to the glossary."""
from pagekit import *  # noqa: F401,F403
import common

SNAP = common.SNAP


def path_card(title, who, steps):
    links = " → ".join(steps)
    return box(f'{H3(title)}<p class="prose" style="margin: 0; color: #4E5751">{who}</p><p style="margin: 0; font-weight: 600">{links}</p>')


paths = grid([
    path_card("New here", "Start from zero: what causal discovery is, how it is scored, and where the hard problems are.",
              [link("primer", "1 Primer"), link("scoring", "2 Scoring"), link("space", "3 The space")]),
    path_card("Reviewing the work", "The findings, then the plan.",
              [link("scoreboard", "4 Scoreboard"), link("decisions", "5 Decisions"), link("names", "6 Agents"),
               link("rca", "7 Declared structure"), link("status", "10 Status")]),
    path_card("Back to recenter", "What moved, and where that leaves the plan. The team's day-to-day work is in the Slack lists.",
              [link("changes", "11 What changed"), link("status", "10 Status")]),
], min_w=300)

findings = ul([
    f"<b>The leaderboard mixes method with file layout.</b> CausalArena lists columns in causal order; a rule that only reads "
    f"column positions scores {n('leak.released')}, above every published method. Controlled for layout, PC rises from "
    f"{n('pub.sem.D.PC')} to {n('ab01.sem.maxp.ctrl')}. {link('scoreboard', 'Page 4')}",
    f"<b>Learned graphs rarely beat 'nothing moves'.</b> On CausalArena the best methods capture a third to a half of the "
    f"decision value the data allow; on physical data they do better. {link('decisions', 'Page 5')}",
    f"<b>LLM agents take directions from variable names.</b> With names swapped, three of the five systems audited lose "
    f"0.10 or more directed F1 (causaliq-knowledge {n('ab06.causaliq.nr', '{:.2f}')}, Causal-Copilot {n('ab06.cc4o.nr', '{:.2f}')}, "
    f"MATMCD {n('ab06.matmcd.nr', '{:.2f}')}), and MATMCD falls below its own data-only graph. The one that resists is the one "
    f"whose data decide the graph. {link('names', 'Page 6')}",
    f"<b>Stated structure plus abstention wins where it exists.</b> In incident root cause analysis a declared service map "
    f"scores {n('ab12.c.ac3')} top-3 accuracy against {n('ab12.b.ac3')} for a learned graph. {link('rca', 'Page 7')}",
])

build = ul([
    f"<b>The ledger never falls below its data, held out.</b> Against plain PC with maxP it gains {n('q2.erf.sem.f1', '{:+.3f}')} "
    f"(semantic) and {n('q2.erf.for.f1', '{:+.3f}')} (formula) directed F1 and its committed claims are more often right "
    f"({n('q2.erf.sem.dv', '{:+.3f}')} / {n('q2.erf.for.dv', '{:+.3f}')} DV-1 precision); it ties GES on F1 "
    f"({n('q2.ges.sem.f1', '{:+.3f}')} / {n('q2.ges.for.f1', '{:+.3f}')}). {link('status', 'Page 10')}",
    f"<b>Provenance holds on every held-out file.</b> Neutral names leave the ledger unchanged on {n('q2.b3.sem.neutral')}/{t('q2.b3.sem.files')} "
    f"and {n('q2.b3.for.neutral')}/{t('q2.b3.for.files')} files; wrong names cost at most the proven bound on every file; every claim "
    f"re-derives from its evidence. Real names add {n('q2.b3.sem.gain', '{:+.3f}')} / {n('q2.b3.for.gain', '{:+.3f}')}, below the bar of 0.03. "
    f"{link('theses', 'Page 8')}",
    f"<b>Calibrated confidence beats raw bootstrap shares.</b> In the first held-out read, calibration error was "
    f"{n('q2.b4.sem.ece', historic=True)} / {n('q2.b4.for.ece', historic=True)} against {n('q2.b4.sem.raw', historic=True)} / "
    f"{n('q2.b4.for.raw', historic=True)} for raw shares; the second read (kernel v3, below) is the one the landmarks use.",
    f"<b>Root cause analysis runs through the ledger.</b> Declared topology as knowledge reproduces the audit's number exactly: "
    f"AC@3 {n('q2.b5.ac3')} at coverage {n('q2.b5.cov')}, against {n('q2.b5.learned')} for the learned graph alone; {n('q2.b5.answered')} "
    f"issues keep the interval's lower end at {n('q2.b5.ac3.lo')}. {link('rca', 'Page 7')}",
    f"<b>Kernel v3 reads the same ledger more carefully.</b> Not acting on the weakest directions and scoring each answer from "
    f"the ledger's own features: formula answers are {n('q2v3.for.D.p')} precise at half coverage (lower end "
    f"{n('q2v3.for.D.lo')}, landmark met); semantic {n('q2v3.sem.D.p')}, capped by links the data cannot show "
    f"({n('q2v3.floor.sem', '{:.0%}')} of true links leave no usable signal). {link('status', 'Page 10')}",
])

latest = (SNAP.get("changes") or [{}])[0]
latest_html = (box(f'<span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: #1D5C99">'
                   f'Latest digest · {esc((latest.get("posted_utc") or "")[:10])}</span>'
                   f'<p class="prose" style="margin: 0">{esc(latest["points"][0])}</p>'
                   f'<p style="margin: 0">{link("changes", "All recent changes")}</p>') if latest.get("points") else "")

BODY = "\n".join([
    P("Causal discovery tries to recover cause and effect, which arrows point where, from data. This UCSD DSC 180 capstone "
      "audits how well the field's tools and benchmarks actually do it, starting with Causal-Copilot, an LLM agent, and CausalArena, "
      "a public leaderboard. The audits ask three things: what a published score really measures, whether a learned graph is "
      "worth acting on, and where an LLM agent's answers come from. The constructive goal is a system that keeps every causal "
      "claim's source, says how sure it is, declines when it should, and never does worse than its own data.", 18),
    paths,
    H2("What the audits found"),
    findings,
    H2("What the build showed (Q2, first pass)"),
    build,
    H2("Where this is heading"),
    box(f'<p class="prose" style="margin: 0">The evidence points to a product: an independent audit of the causal claims other '
        f'people\'s AI agents make, starting with incident root cause analysis. The desk research on that market is on '
        f'{link("market", "page 9")}. The claim ledger is now built and tested in gated steps: of the seven landmarks set in advance, the '
        f'floors, provenance and the physical-truth row are met; precision at half coverage, calibration, accuracy above GES and '
        f'root-cause accuracy at 0.90 are measured and not yet met ({t("q2.paper.met")} of 5 paper constraints, {t("q2.wedge.met")} of 5 '
        f'for the product). {link("status", "Page 10")} has the table; {link("theses", "Page 8")} the claims. A second version, '
        f'read once more held out, meets the precision landmark for formula but not semantic; the open choice is between more '
        f'scenarios to narrow every interval and a third version aimed at the links the search misses.</p>', tone="blue"),
    latest_html,
])
