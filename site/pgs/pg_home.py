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
    H2("Where this is heading"),
    box(f'<p class="prose" style="margin: 0">The evidence points to a product: an independent audit of the causal claims other '
        f'people\'s AI agents make, starting with incident root cause analysis. The desk research on that market is on '
        f'{link("market", "page 9")}. The build order is deliberate: the claim ledger is made reliable first (its invariants, '
        f'never below its data, bounded harm from wrong knowledge, calibration measured on held-out data) and only then is '
        f'anything built on top. {link("theses", "Page 8")} has the claims and the plan. The audit chapter closed on 14 Oct with '
        f'that decision (DEC-05): keep every measurement result, and build the claim ledger in gated steps, the checker for '
        f'other agents\' claims last.</p>', tone="blue"),
    latest_html,
])
