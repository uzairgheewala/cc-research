"""Page 9: who would use it. Act III: AB-14 (market map, three vertical briefs, public demand evidence). Every $ figure
carries its evidence label (build check)."""
from pagekit import *  # noqa: F401,F403

where_money = ul([
    f"Experimentation platforms, which measure the effect of a change: Statsig sold for {n('ab14.statsig')} {label('second-hand')}, "
    f"Eppo for a reported {n('ab14.eppo')} {label('second-hand')}.",
    f"AI agents that investigate IT incidents and name a root cause: about {n('ab14.sre')} raised in 2025-2026 "
    f"{label('estimate, sum of six rounds')}, led by Resolve AI's {n('ab14.resolve')} round {label('primary')}.",
    f"Marketing-mix modelling software: about {n('ab14.mmm')} in 2026 {label('analyst claim')}.",
    f"Pharma real-world-evidence platforms and services: {n('ab14.rwe')} {label('analyst claims')}.",
])

ranking = table(
    ["Where to start", "Who buys", "Bottom-up estimate", "Why this rank"],
    [[f"<b>1. IT incident {T('rca', 'root cause analysis')}</b>: audit the root-cause claims of AI incident agents",
      "Head of SRE or platform, from observability budgets",
      f"{n('ab14.est.rca')} ARR obtainable in about three years {label('estimate')}",
      "the project already has a measured result here (page 7); agents read service names, so the name test applies; prices are public"],
     ["<b>2. Marketing measurement</b>: grade the evidence behind each channel-effect claim",
      "Marketing-science lead and CMO, with finance as the audience",
      f"{n('ab14.est.mkt')} obtainable at maturity {label('estimate')}",
      "the most direct stated pain: credibility with finance; but experiments themselves are doubted, so the grading must go deeper"],
     ["<b>3. Pharma real-world evidence</b>: an assumption ledger per study",
      "Head of RWE or epidemiology, with regulatory affairs",
      f"{n('ab14.est.pharma')} a year for the regulatory core {label('estimate')}",
      "the strongest regulatory hooks (pre-specification failures cost approvals), but a small core and slow sales"]],
    caption="Every estimate in the report shows its inputs and arithmetic; ranges are wide because public data cannot pin the "
            "number of buyers or how often they would use an audit.")

hyp = table(
    ["Interview hypothesis", "What public evidence says", "Strength"],
    [["H1: people would use a source on every claim, and a tool that can decline to answer",
      "Broad stated demand for AI that shows its work; nothing measures whether people would accept abstention; buyers rank price "
      "and features above trust", "supported for provenance only"],
     ["H2: people ask 'what happens if we change X?', not for whole graphs",
      "The money and published practice are in effect estimation and experiments; graph-discovery products are being retired",
      "best supported"],
     ["H3: an audit of how much an LLM tool relies on names is worth paying for",
      "LLM evaluation is a funded category; nobody was found paying for a causal-claim audit", "by analogy only"]],
    caption="All indirect: surveys, filings and published practice standing in for practitioner interviews. The interviews remain "
            "the only way to settle the pre-registered prediction about them.")

BODY = "\n".join([
    question("Who would pay for an audited causal claim, and where should it start?",
             before=f'{link("theses", "page 8")} (the claim ledger) and {link("rca", "page 7")} (where declared structure wins).'),
    P(f"This page summarises the project's desk research on the market (AB-14). Every figure carries an {T('evlabel')}: what kind "
      f"of evidence it is. A vendor's statement about itself is a claim, not a measurement; an estimate shows its inputs in the "
      f"report."),
    H2("The 'causal AI' category cannot be sized"),
    P(f"Eight published sizings of 'causal AI' run from {n('ab14.size.lo')} {label('analyst claim')} to {n('ab14.size.hi')} "
      f"{label('analyst claim')}, a spread of about a thousand times, and none has a reproducible method. The money that pays for "
      f"causal answers sits in segments that rarely use the word:"),
    where_money,
    P("Meanwhile the general-purpose causal-discovery tools from large sponsors have been retired or repositioned: Microsoft's "
      "ShowWhy was archived in December 2025, McKinsey's CausalNex reached end of life in June 2026, and causaLens now sells "
      "LLM agents. Graph discovery on its own has no surviving commercial home among the tools checked."),
    H2(f"Three {T('vertical', 'verticals')}, ranked for where to start"),
    ranking,
    P(f"The pharma figure has a broader form too: {n('ab14.est.pharma.broad')} a year across all registered real-world-evidence "
      f"studies {label('estimate')}."),
    H2("Is there demand? The public evidence, in place of interviews"),
    hyp,
    H2("What this means, and what it does not"),
    box("<p class='prose' style='margin: 0'><b>Sell the audit, not the causal graph.</b> The defensible offer is a vendor-neutral "
        "audit of the causal claims other people's agents make: a typed source for each claim, measured calibration, a reported "
        "abstention rate, and a name-reliance test. No vendor found publishes those today.</p>"
        "<p class='prose' style='margin: 0'><b>Reliability comes first.</b> An audit is only worth buying if it is itself "
        "reliable, and in decisions this sensitive that bar is high. So the build order is the one on page 8: the ledger's "
        "invariants, never falling below the data, bounded harm from wrong knowledge, and calibration measured on held-out data, "
        "before any product is built on top.</p>", tone="blue"),
    answer("Buyers already pay for root-cause answers, marketing measurement and real-world evidence, and none of the tools they "
           "buy publishes where each claim came from or how often it is right. The best place to start is incident root cause "
           "analysis, where this project already has a measured result. Whether practitioners would accept a tool that sometimes "
           "declines to answer is the one thing public evidence cannot tell.",
           "Where does the work stand right now?"),
])
