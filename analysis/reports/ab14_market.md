Ticket: AUD-45 (AB-14). Written 2026-10-13. Desk research only; no model calls. Research notes: `analysis/audits/ab14_notes/`.

# Sell the audit, not the causal graph

## Where we are now

The market labelled "causal AI" is small, and public data cannot size it. Eight published estimates for 2023-2025 run from **$28.9M** (Global Market Insights) to **$59.22B** (The Insight Partners), a spread of about 1,000x, and none has a reproducible method (all analyst claims, §1). The money that actually pays for causal answers is in segments that rarely call themselves causal AI:

- experimentation exits: Statsig **$1.1B** to OpenAI and Eppo **~$220M** reported to Datadog (second-hand);
- AI SRE agents that sell "root cause": about **$285M** in disclosed 2025-2026 rounds (estimate, §1);
- marketing-mix modelling (MMM) software: **~$2.2B** in 2026 (analyst claim);
- pharma real-world evidence (RWE): **$2.0-2.6B** in 2024-2025 (analyst claims).

Standalone causal-discovery products are being retired. Microsoft ShowWhy was archived in December 2025, McKinsey's CausalNex reached end of life in June 2026, and causaLens has dropped decisionOS in favour of LLM "Digital Workers" (all primary).

On public evidence, the auditable causal-claims product should start in **IT incident root cause analysis (RCA)**, as a vendor-neutral audit of AI SRE agents' root-cause claims, for four reasons:

- the project already has a measured result there (AB-12);
- LLM agents read service names, so the name-reliance audit applies;
- prices are public;
- no vendor publishes precision, recall or an abstention rate.

Marketing measurement is a close second and has the most direct stated pain. Pharma RWE has the strongest regulatory hooks, but its must-have core is small and sales are slow.

All of the following bottom-up figures are estimates, with every input shown in §2:

| Vertical | Estimate |
|---|---|
| RCA claim audit | $1.8-9.0M ARR obtainable within three years |
| Marketing | $3-67.5M obtainable at maturity |
| Pharma | $2.8-11M a year for the regulatory core; $20-100M a year across all registered RWE studies |

The public evidence on the three interview hypotheses is lopsided:

- **H2** has the strongest support.
- **H1** has support for "show your work", but none for abstention specifically.
- **H3** has support only by analogy. Buyers fund LLM evaluation, but nobody was found paying for a causal-claim or name-reliance audit.

None of this replaces the AB-10 interviews. The pre-registered P13 kill criterion can only be decided by them.

This is the project's AB-14 deliverable (ticket AUD-45). Its gate is "no number without its inputs". It synthesises five research notes compiled on 2026-10-13. It builds on, and in places corrects, `AU5_commercial.md`, `AB11_vendor_claims.md`, `AB13_regulation_map.md` and the AB-12 RCA probe (`ab12_rca_probe.md`); §5 lists the corrections. Web pages were read through a summarising fetch tool, so numbers should be spot-checked before they go into a deck; five were re-checked against their primary pages on 13 Oct (see the last section).

Every figure carries one of these labels:

| Label | Meaning |
|---|---|
| **primary** | The issuer's own filing, release, pricing page, repository or regulator table |
| **second-hand** | News, aggregators, competitors' pages, or one firm quoting another |
| **vendor claim** | A company's statement about its own performance, scale or customers. These are never measurements. |
| **analyst claim** | A paid market-research figure |
| **survey (n=…)** | "Vendor-run" is added when the sponsor sells a fix for the problem the survey finds |
| **anecdote** | Essays, conference abstracts and blog opinions |
| **estimate** | My arithmetic, with inputs shown. Unsourced inputs inside an estimate are marked **assumption**. |
| **project measurement** | The project's own measured results (for example AB-12) |

## Six segments carry the "causal" label, and the money sits in the ones that avoid it

### The segments barely overlap

"Causal AI" covers six commercial segments with different buyers, products and economics. StartUs Insights claims to track **733 "causal AI startups"** but gives no funding figures (second-hand; [StartUs Insights](https://www.startus-insights.com/innovators-guide/causal-ai-companies/)). Analyst vendor lists show how loose the boundary is. MarketsandMarkets lists real causal vendors (causaLens, Causaly, Aitia, Parabole.AI, Howso) next to IBM, Microsoft and Google ([MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/causal-ai-market-162494083.html)). GMI's "key players" include Dropbox, Pinterest and Snap, none of which sells a causal product ([GMI](https://gminsights.com/industry-analysis/causal-ai-market)).

| Segment | What is sold | Representative vendors | Freshest money signal (label; source) | Status, Oct 2026 |
|---|---|---|---|---|
| A. Horizontal enterprise causal-AI platforms | Causal modelling or discovery platforms, now mostly LLM agents | causaLens, Geminos, Kausable, Causa/CausaDB, Howso, Xplain Data | Kausable seed, 9 Jul 2026, €12M or $13.8M (the source conflicts with itself) (second-hand; [Nordic9](https://nordic9.com/news/kausable-raises-12-million-in-a-seed-funding/)) | Stalled. causaLens has had no visible round since its $45M Series A (~Jan 2022, primary; [causaLens](https://causalens.com/causal-ai/startup-series-a-funding-round-45-million)) and has rebranded to agents. |
| B. Observability, AIOps and AI SRE with root-cause reasoning | Autonomous incident investigation; RCA over topology | Datadog, Dynatrace, PagerDuty, AWS, New Relic, IBM Instana; Resolve AI, Traversal, Cleric, NeuBird, Ciroos, incident.io, Rootly; Causely | Resolve AI $125M Series A at a $1B valuation, 2 Feb 2026 (primary; [Resolve](https://resolve.ai/blog/series-a-funding)) | The most heavily funded segment in 2025-2026 |
| C. Marketing measurement | MMM, geo and incrementality experiments, "causal attribution" | Haus, Recast, Measured, Mutinex, Lifesight, Prescient, Northbeam, Analytic Partners, Nielsen; free Google Meridian and Meta Robyn | Haus $20M, 30 Jul 2024 (primary; [Haus](https://haus.io/blog/haus-announces-20m-raise-led-by-01-advisors)) | Mid-sized and services-heavy; the model itself is commoditising |
| D. Life sciences | RWE platforms; causal literature graphs; target discovery; RCT design | Aetion (Datavant), IQVIA, Flatiron, TriNetX, Truveta, Komodo, Atropos; Causaly, Aitia, Unlearn | Truveta $320M at more than $1B, 16 Jan 2025 (second-hand; [Pulse 2.0](https://pulse2.com/truveta-ehr-data-company-raises-320-million-at-over-1-billion-valuation)) | Consolidating around data networks |
| E. Experimentation platforms | A/B testing and feature-flag experiments | Statsig, Eppo, Split, VWO/AB Tasty, Optimizely, SiteSpect | Statsig $1.1B exit (second-hand; see M&A) | Consolidating into larger platforms |
| F. Open source with corporate backers | Libraries | DoWhy/PyWhy (AWS and Microsoft), EconML, CausalML (Uber), Tetrad (CMU) | DoWhy 8.3k stars, 1.1k forks; the README names no commercial backer (primary; [GitHub](https://github.com/py-why/dowhy)) | Libraries survive; no-code UIs died (see churn) |

### AI SRE has out-raised every company that sells itself as causal

In 2025-2026 the money with a causal or root-cause pitch went to LLM-agent companies that say "root cause" or "reasons over evidence", not to graph-discovery platforms. Resolve AI's latest round alone is larger than the disclosed total of any company that sells itself mainly as causal: causaLens at least $45M, Causaly $83M, Aitia $65.25M, Causely about $11M.

**Disclosed 2025-2026 AI SRE rounds total about $285M (estimate):**

| Company | Round (USD) |
|---|---|
| Resolve | $125M |
| incident.io | $62M |
| Traversal | $48M |
| Ciroos | $21M |
| NeuBird | $19.3M |
| Cleric | $9.8M |
| **Total** | **$285.1M** |

Two caveats apply. Cleric's $9.8M is a total seed that may include an earlier $4.3M tranche. Amex Ventures' strategic investment in Traversal was undisclosed and is excluded. None of the funded AI SRE firms publishes a precision or recall method. Traversal's ">90% accuracy on hundreds of high-impact incidents" has no method (vendor claim; [Traversal](https://traversal.com/blog/launch-announcement)).

| Company | Segment | Last known round | Total raised; conflicts | Label; source |
|---|---|---|---|---|
| Resolve AI | AI SRE | Series A, $125M, $1B valuation, led by Lightspeed. Dated 2 Feb 2026 (primary) or 4 Feb 2026 (second-hand). | More than $150M (primary) vs $160M including a $35M Oct 2024 seed (second-hand). TechCrunch sources suggested tranches priced below $1B; the company denied it. | primary, [Resolve](https://resolve.ai/blog/series-a-funding); second-hand, [Seedtable](https://seedtable.com/companies/resolveai/funding-rounds/series-a-2026-02), [TechCrunch](https://techcrunch.com/2026/02/04/ai-sre-resolve-ai-confirms-125m-raise-unicorn-valuation/) |
| incident.io | Incident management with AI | Series B, $62M, 10 Apr 2025, led by Insight | $100.7M (second-hand) vs "over $96M" (lead investor's release) | [CB Insights](https://www.cbinsights.com/company/incidentio/financials); [Insight Partners](https://www.insightpartners.com/ideas/incident-io-raises-62m-to-build-ai-agents-that-resolve-incidents-with-you/) |
| Traversal | AI SRE ("causal ML") | Seed + Series A, $48M, ~June 2025, Sequoia and Kleiner Perkins; Amex Ventures strategic investment, Mar 2026, amount undisclosed | $48M (primary) vs $53M, with an unsourced $309.5M valuation (second-hand, low reliability) | primary, [Traversal](https://traversal.com/blog/launch-announcement); second-hand, [PrivateMarketView](https://privatemarketview.com/companies/traversal/funding-rounds), [Pulse 2.0](https://pulse2.com/traversal-ai-site-reliability-engineering-platform-receives-strategic-investment-from-amex-ventures/amp/) |
| NeuBird | AI SRE | $19.3M, ~6 Apr 2026, led by Xora | At least $63.8M (estimate: $22M seed in Apr 2024 + $22.5M in Dec 2024 + $19.3M) | primary, [Business Wire](https://www.businesswire.com/news/home/20260406552258/en); second-hand, [TechCrunch](https://techcrunch.com/2024/12/11/microsofts-m12-invests-another-22-5m-into-nuebird-months-after-its-22m-seed-round/) |
| Ciroos | AI SRE | Seed, $21M, 3 Jun 2025 | — | second-hand, [Seedtable](https://seedtable.com/companies/ciroos) |
| Cleric | AI SRE | Seed total $9.8M, led by Vertex Ventures US, ~9 Dec 2025 | Earlier $4.3M reported (headline only) | primary, [Business Wire](https://businesswire.com/news/home/20251209625361/en/Cleric-Launches-the-First-Self-Learning-AI-SRE) |
| Causely | Causal RCA | Seed, $8.8M, 29 Jun 2023, led by 645 Ventures | More than $11M (primary) vs $10.8M (second-hand) | [Causely](https://www.causely.ai/blog/causely-raises-8-8m-in-seed-funding-to-deliver-it-industrys-first-causal-ai-platform); [VCBacked](https://www.vcbacked.co/company/causely) |
| causaLens | Enterprise causal AI, now agents | Series A, $45M, ~Jan 2022 | At least $45M (primary) vs "over $50M" (vendor claim, May 2026) | [causaLens](https://causalens.com/causal-ai/startup-series-a-funding-round-45-million); [Business Wire](https://businesswire.com/news/home/20260506514597/en/causaLens-Expands-Strategic-Partnership-with-Syneos-Health-to-Scale-Agentic-AI-in-Biopharma-Commercialization) |
| Geminos | Enterprise causal AI | Incubator round (Deere), 24 Jan 2024, amount undisclosed | Not disclosed | second-hand, [CB Insights](https://www.cbinsights.com/company/geminos-software/financials) |
| Kausable | Causal-structure AI | Seed, 9 Jul 2026 | €12M (headline) vs $13.8M (body of the same article) | second-hand, [Nordic9](https://nordic9.com/news/kausable-raises-12-million-in-a-seed-funding/) |
| Causaly | Life-science literature graph | Series B, $60M, 13 Jul 2023, led by EBRD VC | $83M | second-hand, [Seedtable](https://seedtable.com/companies/causaly/funding-rounds/series-b-2023-07) |
| Aitia (GNS) | Life-science discovery | Corporate minority round, Charles River Labs, 13 Nov 2023, amount undisclosed | $65.25M over 12 rounds | second-hand, [CB Insights](https://www.cbinsights.com/company/gns-healthcare/financials) |
| Unlearn | RCT design (digital twins) | Series C, $50M, 29 Feb 2024, led by Altimeter | More than $130M | primary (investor release), [DCVC](https://www.dcvc.com/press-releases/unlearn-raises-50-million-series-c-to-optimize-clinical-research-with-ai-powered-digital-twin-technology) |
| Atropos Health | AI for RWE | Series B, $33M, 23 May 2024; Merck GHI, Cencora and McKesson as strategic investors | $53.8M | second-hand, [Fierce Healthcare](https://www.fiercehealthcare.com/health-tech/atropos-health-lands-33m-scale-ai-powered-real-world-evidence-build-out-pharma) |
| Haus | Marketing incrementality | $20M, led by 01 Advisors. Dated 30 Jul 2024 (primary) vs Oct 2024 (law-firm snippet). | At least $37M if the $17M Series A is counted (primary) vs $61.65M over 6 rounds with a $435.72M valuation as of Apr 2025 (second-hand) | [Haus](https://haus.io/blog/haus-announces-20m-raise-led-by-01-advisors); [StockAnalysis](https://stockanalysis.com/private/haus/) |
| Measured | Incrementality + MMM | $21M, May 2022, Telescope Partners | — | second-hand, [Pulse 2.0](https://pulse2.com/media-investment-measurement-platform-company-measured-raises-21-million/amp/) |
| Prescient AI | MMM | Series A, $10M, 12 Mar 2024 | $18M | second-hand, [Refresh Miami](https://refreshmiami.com/news/prescient-ai-raises-10m-series-a-to-help-ecommerce-brands-optimize-their-ad-spend/) |
| Mutinex | MMM | $17.5M at a $132.5M valuation, 10 Oct 2024 (currency not stated, probably AUD) | — | second-hand, [Business News Australia](https://direct.businessnewsaustralia.com/articles/marketing-analytics-scale-up-mutinex-raises--17-5m--boosting-valuation-to--132-5m.html) |
| Recast | MMM | Seed, $3.4M, ~Dec 2022 | $4.5M; no later round found | second-hand, [AlleyWatch](https://alleywatch.com/2022/12/recast-marketing-mix-modeling-analytics-forecasting-platform-omnichannel-holistic-ad-spend-data-science-michael-kaminsky/) |

### Every priced exit is in experimentation or decisioning

No company that sells itself as causal AI has been acquired at a disclosed price (absence not exhaustively verified). The acquirers are infrastructure platforms folding measurement into a larger stack: OpenAI, Datadog, Harness, Braze, DoubleVerify and Datavant. That pattern suggests a causal-claims layer is more likely to end up as a feature of an observability, experimentation or RWE platform than as a standalone company. The Statsig sequence also shows a frontier-lab buyer wanting the team and internal tooling, not the external customer business. Note that several rows rely on Convert, an A/B-testing vendor that competes with the companies it reports on.

| Target → acquirer | Date | Price | Label; source |
|---|---|---|---|
| Statsig → OpenAI | Announced 2 Sep 2025 | $1.1B, all stock | second-hand; [AI Business](https://aibusiness.com/generative-ai/openai-acquires-startup-for-1-1b-hires-ceo) |
| ↳ Statsig brand and customers → Amplitude | Announced 5 May 2026 | Not reported. OpenAI's promise that Statsig would "continue operating independently" was retired. | second-hand (competitor blog); [Convert](https://convert.com/blog/a-b-testing/statsig-moves-to-amplitude/) |
| OfferFit → Braze | 2025 | $325M | second-hand (competitor blog); [Convert](https://www.convert.com/blog/a-b-testing/state-of-ab-testing-tools-2026/) |
| Eppo → Datadog | May 2025 | ~$220M reported; Datadog confirmed the deal but not the price | second-hand; [AIM Research](https://aimresearch.co/market-industry/datadog-enters-the-experimentation-space-with-220-million-eppo-deal); [Fortune](https://www.fortune.com/2025/05/06/statsig-series-c-100-million-1-1-billion-eppo-datadog) |
| Wingify (VWO), majority stake → Everstone | 2025 | ~$200M | second-hand; [Convert](https://www.convert.com/blog/a-b-testing/state-of-ab-testing-tools-2026/) |
| VWO + AB Tasty merger | 2026 | Not reported; combined ARR above $100M | second-hand; same source |
| Rockerbox → DoubleVerify | Announced 26 Feb 2025 | $85M cash | second-hand; [Axios](https://www.axios.com/2025/02/26/doubleverify-acquire-rockerbox-85-million) |
| Aetion → Datavant | Announced 15 May 2025; completed July 2025 | Undisclosed | second-hand, [Healthcare IT Today](https://www.healthcareittoday.com/2025/06/16/datavant-to-acquire-aetion-empowering-healthcare-and-life-sciences-organizations-to-generate-high-quality-scalable-real-world-evidence-from-connected-privacy-protected-data/); vendor release, [Datavant](https://www.datavant.com/press-release/datavant-completes-acquisition-of-aetion) |
| Split → Harness | Agreement 29 May 2024 | Undisclosed (Split had raised more than $110M) | primary; [Harness](https://harness.io/press-and-news/harness-acquires-split-software-to-enable-feature-flag-experimentation-in-software-workflows) |
| Analyx → Analytic Partners | Closed 9 Jan 2025 | Undisclosed | vendor claim; [Analytic Partners](https://analyticpartners.com/newsroom/analytic-partners-acquires-analyx/) |
| Intellimize → Webflow; SiteSpect → Monetate | 2024; 2025 | "Eight figures" reported; not reported | second-hand; [Convert](https://www.convert.com/blog/a-b-testing/state-of-ab-testing-tools-2026/) |

### Market-size estimates span three orders of magnitude

The published sizings cannot be reconciled. Four conflicts stand out:

- **The bases differ about 1,000-fold.** MarketsandMarkets puts 2024 at $56.24M; The Insight Partners puts 2025 at $59.22B.
- **MarketsandMarkets revised its own 2023 base fivefold, from $8.01M to $41.34M, between editions.** It stated no restatement.
- **Growth rates cluster at 38-47% even though the bases differ by orders of magnitude.** Emergen's 21.3% is the only exception.
- **No firm's definition includes experimentation or MMM spend.** Statsig's single exit is worth more than every forecast at the low end of the range.

The billion-dollar figures must therefore count AI spending that merely carries a causal label. The only range near a defensible bottom-up check is the tens-of-millions cluster. That is the same order as a handful of vendors at the ~$100k-£240k contract values recorded in AB11. For citation, the defensible wording is "about $30-60M in 2023-2025 per MarketsandMarkets, GMI and Roots, methods paywalled". It should be stated plainly that the $1B+ figures are not comparable.

| Firm (edition) | Base | Forecast | CAGR | Method stated | Label; source |
|---|---|---|---|---|---|
| MarketsandMarkets (17 May 2023) | $8.01M (2023) | $119.5M (2030) | 47.1% | Not in the press release | analyst claim, via a reposted press release; [jotup](https://jotup.co/node/2403603) |
| MarketsandMarkets (Dec 2024) | $41.34M (2023); $56.24M (2024) | $456.88M (2030) | 41.8% | Top-down + bottom-up, interviews (count not stated); BFSI the largest vertical | analyst claim; [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/causal-ai-market-162494083.html) |
| Global Market Insights (Jul 2024) | $28.9M (2023) | ~$600M (2032) | ~41% | Claims ~80% primary interviews and a revenue build | analyst claim; [GMI](https://gminsights.com/industry-analysis/causal-ai-market) |
| Roots Analysis (May 2025) | $63.37M (2025) | $1,628.43M (2035) | 38.35% | Generic | analyst claim; [Roots](https://www.rootsanalysis.com/causal-ai-market) |
| theCUBE Research (15 Mar 2025) | — | More than $1B (2030) | 41% | Not read | analyst claim, second-hand via `AU5_commercial.md` |
| Emergen (Oct 2025; modified May 2026) | $1.8B (2024) | $12.4B (2034) | 21.3% | Generic; the page's meta description contradicts its body | analyst claim; [Emergen](https://www.emergenresearch.com/industry-report/causal-ai-market) |
| SkyQuest (via reseller, 2026) | $1.15B (2024); $1.59B (2025) | $21.4B (2033) | 38.4% | Top-down + bottom-up | analyst claim, read on a reseller page; [GII Korea](https://www.giikorea.co.kr/report/sky2026331-causal-ai-market-size-share-growth-analysis-by.html) |
| The Insight Partners (28 Jul 2026) | **$59.22B (2025)** | $1,069.71B (2034) | 37.93% | "Proprietary research"; the table of contents confirms the units are US$ billions | analyst claim; [Insight Partners](https://www.theinsightpartners.com/reports/causal-ai-market), [TOC](https://www.theinsightpartners.com/reports/toc/causal-ai-market) |

The adjacent markets where causal answers are actually bought are larger and better anchored, but they have their own definition conflicts:

| Adjacent market | Estimates | Conflict | Label; source |
|---|---|---|---|
| Observability | $11.91B (2026) → $22.99B (2031), MarketsandMarkets; ~$14.2B by 2028, Gartner | MarketsandMarkets' page quotes a 2023-2028 CAGR that does not match its own window | analyst claims; [MarketsandMarkets](https://www.marketsandmarkets.com/ResearchInsight/size-and-share-of-observability-tools-and-platforms-market.asp); Gartner via a reseller excerpt, [Spotlight AR](https://research.oz.spotlightar.com/reports/magic-quadrant-observability-platforms-2025/market-definition) |
| Revenue cross-check for observability | Datadog FY2026 guidance $4.45-4.47B; Dynatrace ARR $2.054B; Elastic $1.739B (includes search and security); PagerDuty $492.5M; New Relic ~$1B | Mixed fiscal years | primary filings: [Datadog](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-second-quarter-2026-financial-results), [Dynatrace](https://www.sec.gov/Archives/edgar/data/0001773383/000177338326000011/fy26q4-earningsreleaseex99.htm), [Elastic](https://businesswire.com/news/home/20260527847546/en/Elastic-Reports-Fourth-Quarter-and-Fiscal-2026-Financial-Results), [PagerDuty](https://investor.pagerduty.com/news/news-details/2026/PagerDuty-Announces-Fourth-Quarter-and-Full-Year-Fiscal-2026-Financial-Results/). New Relic's ~$1B is second-hand (Wikipedia). Sum ≈ $9.7B (estimate: 4.46 + 2.02 + 1.74 + 0.49 + 1.0). |
| AIOps | $6.7B (2025), GMI vs $32.5B (2025), IMARC | About 5x apart. IMARC's figure is larger than total observability, so the category is undefined. | analyst claims; [GMI](https://www.gminsights.com/industry-analysis/aiops-market); [IMARC](https://www.imarcgroup.com/global-aiops-market) |
| MMM software | $1.96B (2025); $2.23B (2026); $4.22B (2031) | Broader "attribution software" was already $3.1B in 2021 (Allied, 2022 report) | analyst claims; [Mordor](https://www.mordorintelligence.com/industry-reports/marketing-mix-modeling-software-market); [Allied](https://alliedmarketresearch.com/press-release/marketing-attribution-software-market.html) |
| RWE solutions | $2.0B (2024) → $4.5B (2029), MarketsandMarkets; $2.3B (2024), $2.6B (2025), $3.1B (2026), GMI | GMI's ">17% share" for IQVIA implies ~$0.44B (estimate: 0.17 × $2.6B), but IQVIA booked **$674M** from only part of its real-world offerings (primary) | analyst claims; [MarketsandMarkets](https://prnewswire.co.uk/news-releases/real-world-evidence-solutions-market-worth-4-5-billion--marketsandmarkets-302064016.html); [GMI](https://www.gminsights.com/industry-analysis/real-world-evidence-solutions-market); [IQVIA](https://www.iqvia.com/newsroom/2026/02/iqvia-reports-fourth-quarter-and-full-year-2025-results-issues-full-year-2026-guidance) |

Gartner's position on causal AI is also contested.

- causaLens says causal AI entered Gartner's **2023** Hype Cycle for Emerging Technologies (vendor claim, undated; [causaLens](https://causalens.com/resources/blog/gartner-lists-causal-ai-as-a-flagship-emerging-technology)).
- Wikipedia, citing Gartner, says it was first included in **2022** (second-hand; [Wikipedia](https://en.wikipedia.org/wiki/Causal_AI)).
- A summary of the 2025 Hype Cycle for AI does not mention causal AI (second-hand; [Security World Market](https://www.securityworldmarket.com/int/News/Business-News/the-hype-cycle-for-ai-now-goes-beyond-gen-ai)).
- Its current position is paywalled.

### The discovery tools died, and the survivors attached "causal" to agents

Since late 2025, the best-known general-purpose causal-discovery and causal-modelling tools from large sponsors have exited or pivoted:

- **Microsoft ShowWhy** was archived on 17 December 2025 as "the result of research efforts that are no longer active". No successor was named (primary; [GitHub](https://github.com/microsoft/showwhy)).
- **CausalNex** reached end of life on 24 June 2026, with no further fixes or security patches (primary; [GitHub](https://github.com/mckinsey/causalnex)).
- **causaLens** has removed the decisionOS name from its homepage and now sells LLM "Digital Workers", with a "5x ROI in year one" claim (vendor claim; [causaLens](https://causalens.com/)). In 2023 it called its product "the first operating system for decision making powered by Causal AI" ([causaLens blog](https://causalai.causalens.com/resources/blog/causalens-launches-the-first-operating-system-for-decision-making-powered-by-causal-ai/)). Its May 2026 press boilerplate drops the "causal AI" label entirely (primary; [Business Wire](https://businesswire.com/news/home/20260506514597/en/causaLens-Expands-Strategic-Partnership-with-Syneos-Health-to-Scale-Agentic-AI-in-Biopharma-Commercialization)).
- **Causely** kept its "causal reasoning engine" but repackaged it as context for other companies' agents (primary; [Causely blog](https://www.causely.ai/blog)): an MCP server (Nov 2025), Datadog, Dynatrace and IBM Instana integrations, a Cursor plugin (May 2026), and A2A/AAIF membership (Aug 2026).

The stated reasons are thin. ShowWhy's is "research no longer active"; CausalNex's end of life is unexplained. Reading this as "lack of demand" is therefore inference, not a sourced fact. The commercial lesson is still clear: graph discovery on its own has no surviving commercial home among the tools checked, while "causal" survives as a reasoning claim attached to agents. **Causely is the closest comparable, because it now occupies the "causal context supplier to agents" slot an auditable claims layer would take.** In experimentation, churn takes the form of consolidation rather than shutdowns: Statsig to OpenAI to Amplitude, VWO with AB Tasty, and Google Optimize closed in 2023 (second-hand; [Convert](https://www.convert.com/blog/a-b-testing/state-of-ab-testing-tools-2026/)).

### SRE teams and pharma appear most often in public case studies

Named customer logos rank the buyer types roughly as follows: tech-platform SRE teams ≥ pharma R&D and RWE > consumer and DTC marketing > financial services.

- **SRE teams.** Resolve names Coinbase, DoorDash, MongoDB, MSCI, Salesforce and Zscaler (primary; [Resolve](https://resolve.ai/blog/series-a-funding)). Traversal names DigitalOcean, Eventbrite, Cloudways and unnamed Fortune 100 financial institutions (primary; [Traversal](https://traversal.com/blog/launch-announcement)). Cleric names BlaBlaCar (primary).
- **Pharma.** causaLens' 2026 testimonials include J&J and Syneos Health (primary; [causaLens](https://causalens.com/)). Aetion sells to biopharma, device makers, payers and regulators (second-hand).
- **Consumer and DTC brands.** Haus names StockX and OluKai (primary; [Haus](https://haus.io/blog/haus-announces-20m-raise-led-by-01-advisors)).

MarketsandMarkets calls BFSI the largest vertical (analyst claim). Recent logos do not reflect that: apart from MSCI, Coinbase and unnamed banks, finance appears mainly as causaLens' 2022 customers, Aviva and TIAA (primary). Logos are a biased sample chosen by vendors, and no independent survey of buyers by segment exists.

## Three vertical briefs: who would buy a claim audit, from which budget, at what price

Each brief below follows the same frame. It gives the buyer, budget line, purchase channel, price points, competitors and drivers in one table. A bottom-up estimate follows, with every input shown, then the strongest demand signals. The product in all three is the same: each causal claim carries a typed evidence source and a calibrated confidence, the tool abstains when evidence is thin, and it is paired with an audit of how much the LLM tool relies on variable names and column order.

### Brief 1: IT incident RCA, where downtime makes detection valuable but per-investigation prices leave thin margins

| Item | What the public record shows | Label; source |
|---|---|---|
| Buyer | VP Engineering or Head of SRE, Platform or Infrastructure, who owns the observability bill. Risk and compliance may co-sign where agents act in production. No source names the signing title. | inference |
| Budget line | Observability and incident-management budgets, usually drawn down from committed spend: Dynatrace's minimum annual platform commitment, Datadog AI credits, PagerDuty credit packs that expire annually, and AWS DevOps Agent credits worth 30-100% of the prior month's AWS Support charge | primary; [Dynatrace 10-K](https://www.sec.gov/Archives/edgar/data/0001773383/000177338326000019/dt-20260331.htm), [PagerDuty](https://www.pagerduty.com/pricing/), [AWS](https://aws.amazon.com/devops-agent/pricing/) |
| Purchase channel | Cloud-marketplace private offers. Resolve sells "AI SRE" on AWS Marketplace as a non-cancellable 12-month custom private offer sized on "monthly alert volume and incident counts". AWS Marketplace opened an "AI Agents & Tools" category with MCP and A2A listings on 16 Jul 2025. Integrations into incumbents are a second route (Causely's model). | primary; [AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/prodview-76q4p3nhuqgj4); [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/07/ai-agents-tools-aws-marketplace) |
| Price points (per investigation) | AWS DevOps Agent $0.0083 per agent-second; its own example of 10 investigations × 8 minutes = $39.84, i.e. **$3.98 each** | primary; [AWS](https://aws.amazon.com/devops-agent/pricing/) |
| | Datadog: ~6.5 credits per autonomous investigation at $1.00-1.30 a credit = **$6.50-8.45** | estimate from the primary price list; [Datadog](https://www.datadoghq.com/pricing/list/) |
| | Competitors instead quote Datadog at "$500 per 20 investigations", ≈ **$25 each** | second-hand; [Better Stack](https://betterstack.com/community/comparisons/bits-ai-sre-alternatives/), [Middleware](https://middleware.io/blog/ai-sre-tools/) |
| | Dynatrace AI units cost $0.10 each; ~30 units per investigation ≈ $3.00 is recorded in AB11 but not on today's rate card | primary rate card; units unconfirmed; [Dynatrace](https://www.dynatrace.com/pricing/rate-card/) |
| | Cost floor for a do-it-yourself LLM investigation: $0.10 to nearly $6 | second-hand; [InfoQ](https://infoq.com/news/2025/09/clickhouse-llm-sre-report) |
| Price points (flat) | Causely Professional $2,000/month for up to 500 services ($24k/yr) | primary; [Causely](https://www.causely.ai/pricing) |
| | PagerDuty platform fees $2,800, $12,000 or $48,000 a year | primary; [PagerDuty](https://www.pagerduty.com/pricing/) |
| | Incident-management seats $15-45 per user per month | primary; [incident.io](https://incident.io/pricing) |
| | Resolve "reportedly $1M+/yr for large deployments" | unsourced, on a competitor's page |
| Competitors | Incumbents: Datadog Bits AI SRE, Dynatrace, AWS DevOps Agent, PagerDuty's "Paige" agent, New Relic, IBM Instana. Startups: Resolve, Traversal, Cleric, NeuBird, Ciroos, incident.io, Rootly. Causal RCA: Causely. Several already sell trust features: Cleric's "confidence scores" and "links to relevant evidence", Datadog's "transparent, verifiable investigations", Deeptrace's root causes "with citations", NeuBird's escalation to a human. | vendor claims; [Cleric](https://businesswire.com/news/home/20251209625361/en/Cleric-Launches-the-First-Self-Learning-AI-SRE), [Datadog](https://www.datadoghq.com/product/ai/bits-investigation/), [Better Stack](https://betterstack.com/community/comparisons/bits-ai-sre-alternatives/) |
| Drivers | Gartner assumes AI SRE tooling use rises from under 5% of enterprises (2025) to 85% (2029) | second-hand, quoted by a listed vendor; [Cast AI](https://cast.ai/gartner-market-guide-for-ai-sre-tooling/) |
| | Buyers have "strong cost fatigue" | second-hand Gartner excerpt; [Spotlight AR](https://research.oz.spotlightar.com/reports/magic-quadrant-observability-platforms-2025/market-definition) |
| | PagerDuty's ARR grew 1% and its net retention fell to 98%, consistent with seat revenue saturating | primary; [PagerDuty](https://investor.pagerduty.com/news/news-details/2026/PagerDuty-Announces-Fourth-Quarter-and-Full-Year-Fiscal-2026-Financial-Results/) |
| | Downtime costs (see the value row below) | |

**Bottom-up estimate (every number below is an estimate).** Three facts frame it. The buyer pool is organisations spending at least $100k a year with a public observability vendor. Agent prices are public. The input that moves the result most is how "investigation" is defined, which varies about 50-fold.

| Input | Low | Mid | High | Basis and label |
|---|---|---|---|---|
| N, buyer organisations | 4,720 | 7,500 | 11,401 | Low: Datadog customers with ARR ≥ $100k at 30 Jun 2026 (primary; [Datadog](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-second-quarter-2026-financial-results)). Mid: judgement for overlap between vendor lists (assumption). High: Datadog 4,720 + Dynatrace 4,100 total customers + Elastic 1,720 at ≥ $100k ACV + PagerDuty 861 at ≥ $100k ARR, not de-duplicated (estimate from primary counts; [Dynatrace 10-K](https://www.sec.gov/Archives/edgar/data/0001773383/000177338326000019/dt-20260331.htm), [Elastic](https://businesswire.com/news/home/20260527847546/en/Elastic-Reports-Fourth-Quarter-and-Fiscal-2026-Financial-Results), [PagerDuty](https://investor.pagerduty.com/news/news-details/2026/PagerDuty-Announces-Fourth-Quarter-and-Full-Year-Fiscal-2026-Financial-Results/)) |
| I, agent investigations per org per month | 20 | 100 | 1,000 | Low: Datadog's quoted entry bundle (second-hand) and FireHydrant's 10-49 declared incidents a month (primary vendor dataset, 53,034 incidents; [FireHydrant](https://firehydrant.com/reports/incident-benchmarks)). Mid: assumption. High: ≈30% (assumption) of BigPanda's median 110 actioned incidents a day ≈ 3,300 a month (primary vendor dataset, n=125 organisations; [BigPanda](https://www.bigpanda.io/report/tool-effectiveness-for-it-event-management/detection-benchmarks/actioned-incidents)) |
| P_agent, price per investigation | $3.00 | $6.50 | $8.45 | Dynatrace (AB11, unconfirmed); Datadog annual and on-demand credits (estimate from primary prices) |
| s, audit price as a share of the agent price | 10% | 15% | 25% | assumption |
| ACV for a flat add-on | $8,388 | $24,000 | $48,000 | PagerDuty AIOps $699 × 12 (vendor claim via AB11; not on today's page); Causely list price (primary); PagerDuty Plus (primary) |

| Output | Formula | Low | Mid | High |
|---|---|---|---|---|
| A. Agent-investigation spend pool | N × I × 12 × P_agent | 4,720 × 20 × 12 × 3.00 = **$3.4M** | 7,500 × 100 × 12 × 6.50 = **$58.5M** | 11,401 × 1,000 × 12 × 8.45 = **$1.156B** |
| B. Per-investigation audit layer | A × s | **$0.34M** | **$8.8M** | **$289M** |
| C. Flat platform add-on | N × ACV | 4,720 × 8,388 = **$39.6M** | 7,500 × 24,000 = **$180M** | 11,401 × 48,000 = **$547M** |
| D. Obtainable in ~3 years | 1-5% of mid N (75-375 orgs) × $24k | | **$1.8M-9.0M ARR** | |
| E. Sanity check | C (mid) ÷ observability spend | $180M ÷ $11.91B = 1.5%; ÷ $14.2B = 1.3%. Plausible as a total market, aggressive as a serviceable one. B (high) would be 2.4% of 2026 observability spend, which is implausible near term. | | |
| F. Value per customer | One avoided 15-minute wrong-root-cause detour | 15 × $4,537/min = **$68k** (PagerDuty basis) | 0.25 h × $2M/h = **$500k** (New Relic basis) | Four avoided detours a year: **$272k-2M** |

The downtime inputs in row F come from two vendor-run surveys that measure different things:

- **PagerDuty: $4,537 per minute** (≈ $272k per hour, estimate ×60) and 25 high-priority incidents a year. This is an average over priority incidents (survey, vendor-run, n=500; [PagerDuty](https://pagerduty.com/newsroom/study-cost-of-incidents)).
- **New Relic: $2M per hour.** This is a median for high-impact outages (survey, vendor-run, n=1,700; [New Relic via Business Wire](https://www.businesswire.com/news/home/20250917981661/en/New-Relic-Study-Reveals-Businesses-Face-an-Annual-Median-Cost-of-$76-Million-from-High-Impact-IT-Outages)).

The two differ about 7x; the range should be reported with the definitions attached. Gartner's assumption of under 5% adoption in 2025 places the realised pool near the low-to-mid end today.

The arithmetic leads to one conclusion. Platform agents charge $3-8.45 per investigation, close to raw LLM cost, so a separately billed verification fee has to sit near **$0.30-2** (10-25% of the agent price), or be sold as a flat fee in the $8k-48k band. But the value of catching one wrong root cause ($68k-500k) dwarfs every price point. **The binding constraint is proof that the layer detects wrong answers, not willingness to pay.**

A conflict-of-interest argument favours a third-party auditor. Better Stack reports that Datadog bills only conclusive investigations ("inconclusive investigations are free"; second-hand, not confirmed on Datadog's own pages). If that is true, the agent vendor earns more when it does not abstain.

**Strongest demand signals.** Practitioners say they want reasoning shown, and almost nobody publishes accuracy:

- **95%** of respondents to Grafana's 2026 survey say it is important for AI to show its reasoning, though only **48.2%** say "very important" or "critical". **91%** say root-cause assistance would be valuable. Scepticism rises from 4-5% for assistance to 15% for autonomous action (survey, vendor-run, n>1,300; [Grafana](https://www.grafana.com/blog/observability-survey-AI-2026)).
- A competitor's critique notes that neither Rootly nor incident.io itself publishes production precision or recall. It tells buyers to demand those numbers and "confidence signaling" (second-hand, competitor-written; [incident.io](https://incident.io/blog/rootly-ai-accuracy-vs-competitors)).
- Datadog's engineering blog admits an early Bits version found the true cause in one of 12 tool calls but "still named the wrong one" (primary vendor; [Datadog](https://datadoghq.com/blog/building-bits-ai-sre/)).
- A 2026 conference abstract is titled "Your AI Root-Cause Is Wrong 23% of the Time" and argues "detectability, not accuracy, is the safety property" (anecdote, method not stated; [HighLoad++](https://highload.ru/moscow/2026/abstracts/19223)).

The counter-signal is just as clear. In the same Grafana survey, **only 15%** call AI capabilities an important selection criterion; cost dominates. That matches the project's own open item. In AB-12, declared topology reached AC@3 **0.901** against **0.208** for a learned PC graph, but the abstention rule added only **+0.031** on answered issues. On the no-issue period, **40-83%** of latency windows still produced a fabricated root cause (project measurement; `ab12_rca_probe.md`). The pitch has to be "we measure and reduce fabricated root causes", and the product cannot yet show that it does.

### Brief 2: marketing measurement, where the pain is credibility with finance and experiments are the currency

| Item | What the public record shows | Label; source |
|---|---|---|
| Buyer | The marketing science lead evaluates; the CMO or VP Growth buys; finance reads the audit trail (inference). | inference |
| | Haus's 2026 survey frame explicitly included finance decision-makers | vendor-run survey frame; [EMARKETER](https://www.emarketer.com/content/incrementality-testing-earns-marketers--top-trust) |
| | 36% are sole decision-makers, 50% decide with staff input, 14% decide by committee | survey, n=167, second-hand; [MarketScale](https://www.marketscale.com/industries/marketing-tech/only-22-of-marketers-feel-sure-they-can-justify-spend-to-the-cfo.md) |
| | The share of Fortune 500 firms with a CMO fell from 71% (2023) to 66% (2024) | second-hand, Spencer Stuart; same source |
| Budget line | Measurement, martech, or agency analytics services (inference; no source quantifies it) | inference |
| | Marketing budgets are 7.8% of revenue in 2026; 15.3% of marketing budgets go to AI; 56% of CMOs lack budget for their strategy | survey, n=401, primary; [Gartner](https://gartner.com/en/newsroom/press-releases/2026-05-11-gartner-2026-cmo-spend-survey-finds-cmos-allocate-15-point-3-percent-of-marketing-budgets-to-ai-but-only-30-percent-are-ready-to-scale-ai-capabilities) |
| Purchase channel | 51 Google Meridian certified partners: holding-company units (Publicis, Omnicom's Annalect, dentsu, Merkle), consultancies (Accenture, ZS, Ekimetrics, Artefact, Brainlabs) and data firms (NIQ, Circana). Four of them (Adswerve, Jellyfish, NIQ, Circana) are also certified for GeoX geo experiments. | primary, undated directory; [Google](https://developers.google.com/meridian/partners) |
| Price points | Northbeam Starter from $1,500/month and Professional from $3,500/month, i.e. **$18-42k/yr**; Growth and Enterprise tiers custom | primary; [Northbeam](https://www.northbeam.io/pricing) |
| | Haus median ACV **$150k** (range $132-168k; redline ~$100k) | second-hand (Vendr, sample size unstated), via `AB11_vendor_claims.md` |
| | Meridian and Robyn are free | primary, via AU5 |
| | Google cut the minimum for Conversion Lift experiments from "approaching $100,000" to **$5,000** (Nov 2025) | second-hand; [PPC Land](https://ppc.land/google-lowers-incrementality-testing-threshold-to-5-000-for-advertisers/) |
| | Recast's aggregator price is internally inconsistent and should not be used | second-hand, via AB11 |
| Competitors | Experiment-first: Haus, Measured. Bayesian MMM SaaS: Recast, Mutinex, Prescient, Lifesight. Econometrics firms and data owners: Analytic Partners, Nielsen, Ipsos MMA, TransUnion, Circana, NIQ, Kantar. Attribution-first: Northbeam, Rockerbox (now DoubleVerify). LLM front-ends: Lifesight's MCP connector, Adverity's "MMM Agent for Google Meridian", Northbeam MCP. | vendor claims and second-hand; [Mordor](https://www.mordorintelligence.com/industry-reports/marketing-mix-modeling-software-market), [PPC Land](https://ppc.land/lifesight-mcp-puts-live-marketing-measurement-inside-claude-and-chatgpt/) |
| Drivers | Gartner has a Magic Quadrant for MMM (2024 and 2025 editions), a sign that enterprises run RFPs for it | vendor claims of placement; [TransUnion via The Wise Marketer](https://thewisemarketer.com/transunion-named-a-leader-in-the-2025-gartner-magic-quadrant-for-marketing-mix-modeling-solutions/) |
| | Apple ATT opt-in stays at ~35% | vendor data; [Adjust](https://www.adjust.com/blog/att-opt-in-rates-2025) |
| | Google retired the Privacy Sandbox Attribution Reporting API (~Oct 2025) even though Chrome kept third-party cookies (Apr 2025) | second-hand; [MarTech](https://martech.org/googles-privacy-sandbox-what-you-need-to-know/) |
| | 86% of buyers expect to change how they measure because of AI-driven journeys | IAB survey release; sample stated for the outlook study as more than 200 decision-makers; [IAB](https://www.iab.com/news/iab-raises-2026-u-s-ad-spend-forecast/) |

**Bottom-up estimate (every number below is an estimate).** No public source counts US advertisers by annual media spend (MediaRadar/Vivvix and Pathmatics hold that data behind paywalls). The buyer count is therefore an assumption triangulated from proxies, and this is the weakest of the three bottom-ups on N.

| Input or check | Value | Basis and label |
|---|---|---|
| North American MMM spend (top-down anchor) | 2.23 × 0.3461 = **$0.772B** | $2.23B global MMM software in 2026 times North America's 34.61% share (analyst claims; [Mordor](https://www.mordorintelligence.com/industry-reports/marketing-mix-modeling-software-market)). Applying the 2025 regional share to 2026 is an assumption. |
| Contract-equivalents implied | 0.772B ÷ 0.15M ≈ **5,100** | Divides by Haus's median ACV (second-hand). It overstates enterprise buyers, because services and cheaper tools are mixed in. |
| Average spend per measured brand | $4B ÷ 500 ≈ **$8M** | Lifesight: 500+ brands managing more than $4B (vendor claim; [PPC Land](https://ppc.land/lifesight-mcp-puts-live-marketing-measurement-inside-claude-and-chatgpt/)). This places MMM buyers in the $1-50M media band, not only the Fortune 500. |
| Implied Haus customer count | $36.6M ÷ $150k ≈ **240** | GetLatka's estimated ARR as of Sept 2025 (second-hand estimate; [GetLatka](https://getlatka.com/companies/haus.io)) |
| Measurement as a share of ad spend | **~0.2-1.4%** | $2.23B ÷ $445.4B global digital and social, 2026 (primary; [WPP Media](https://www.wppmedia.com/news/campaigns-report-this-year-next-year-december-2025)) = 0.50%. $0.772B ÷ $385.47B US digital, from a stale 2022 forecast (second-hand; [EMARKETER](https://www.emarketer.com/content/digital-us-media-ad-spend)) = 0.20%. $150k ÷ $11M minimum media in Haus's survey frame = 1.36%. |
| N, US advertisers running MMM plus at least one experiment a year | 2,000-6,000 | assumption, triangulated from ~5,100 contract-equivalents and Google's statement that most advertisers run 1-2 incrementality studies a year (second-hand; [PPC Land](https://ppc.land/google-lowers-incrementality-testing-threshold-to-5-000-for-advertisers/)) |
| Price | $30-75k/yr | assumption: 20-50% of Haus's $150k ACV, as an add-on. Northbeam's $18-42k sets the floor. |
| Adoption at maturity | 5-15% | assumption |

| Output | Formula | Low | High |
|---|---|---|---|
| Serviceable market | N × price | 2,000 × $30k = **$60M** | 6,000 × $75k = **$450M** |
| Obtainable at maturity | N × adoption × price | 2,000 × 5% × $30k = **$3M** | 6,000 × 15% × $75k = **$67.5M** |
| Realistic serviceable ceiling | 10-20% of the MMM spend it audits | 0.10 × $0.772B = **$77M** | 0.20 × $0.772B = **$154M** |
| Partner-channel reach | 51 partners × 10-40 clients each (clients per partner is an assumption) | **~510** advertisers | **~2,040** advertisers |

The high serviceable figure ($450M) would be 58% of North American MMM spend, which is not credible for an add-on. The realistic ceiling is the $77-154M row.

**Strongest demand signals.** This vertical has the most direct statements of the pain the product addresses, though nearly every survey is run by a vendor that sells a fix:

- In Haus's 2026 index, **60%** trust independent incrementality testing most, against 40% for MMM and 37% for in-platform reporting. **78%** believe at least 10% of spend is wasted through poor measurement (survey, vendor-run, n=500; [EMARKETER](https://www.emarketer.com/content/incrementality-testing-earns-marketers--top-trust)).
- In an EMARKETER/TransUnion study (TransUnion sells MMM), **60%** say internal stakeholders question their metrics at least sometimes. About **29%** had up to 20% of the budget reallocated or put at risk over measurement doubts (survey, vendor-run, n=196; [TransUnion](https://newsroom.transunion.com/new-transunion-research-reveals-marketers-confidence-in-measurement-has-stalled/)).
- Only **22%** strongly feel they have the data to prove marketing's value to finance (survey, n=167, second-hand; [MarketScale](https://www.marketscale.com/industries/marketing-tech/only-22-of-marketers-feel-sure-they-can-justify-spend-to-the-cfo.md)).
- **75%** of US buy-side leaders say attribution, incrementality and MMM are underperforming (IAB/BWG survey, n not retrieved because the PDF failed to load; second-hand via [EMARKETER](https://www.emarketer.com/content/incrementality-testing-earns-marketers--top-trust)).

Experiments are doubted too, which sharpens the product:

- **44%** question the reliability of incrementality results (Skai/Path to Purchase Institute survey, n not stated, second-hand; [EMARKETER FAQ](https://www.emarketer.com/content/faq-on-incrementality-how-prove-your-ads-actually-work-2026)).
- Recast calls conflicting lift tests on the same channel "very common" (vendor claim; [Recast](https://getrecast.com/how-do-lift-tests-fit-in-with-mmm)).
- Sellforte documents a 2020 Meta conversion-lift issue that undercounted conversions for about a year (vendor claim; [Sellforte](https://sellforte.com/blog/asked-by-marketers/trust-meta-conversion-lift-tests)).

The evidence tags therefore need sub-fields, not just "experiment vs model": the scope of each test (channel, geo, window), its interval, its independence from other studies, and who ran the randomisation. LLM front-ends also create a new need for claim-level grading. Lifesight's MCP connector logs every query in an audit trail and ships "Board Briefing" and "P&L Translator" skills, but it grades no answer's evidence and made no accuracy claims at launch (second-hand of a vendor launch; [PPC Land](https://ppc.land/lifesight-mcp-puts-live-marketing-measurement-inside-claude-and-chatgpt/)).

### Brief 3: pharma RWE, where regulators reject packages over pre-specification but the must-have core is small

| Item | What the public record shows | Label; source |
|---|---|---|
| Buyer | Head of RWE or Epidemiology at the sponsor, with Regulatory Affairs and Biostatistics co-signing; CRO RWE practice leads as resellers (inference) | inference |
| | ICH M14 calls for a multidisciplinary team with epidemiology and biostatistics expertise | second-hand; [RAPS](https://www.raps.org/resource/ich-adopts-the-m14-guideline-on-observational-stud.html) |
| Budget line | Per-study line items in regulatory RWE, clinical-development and safety (PMR) budgets (inference) | inference |
| | IQVIA moved "Real-World Late Phase and certain other Real-World offerings" (**$674M** of 2025 revenue) into its R&D segment from 1 Jan 2026 | primary; [IQVIA](https://www.iqvia.com/newsroom/2026/02/iqvia-reports-fourth-quarter-and-full-year-2025-results-issues-full-year-2026-guidance) |
| | Services are 58.4% of RWE-solutions spend | analyst claim; [GMI](https://www.gminsights.com/industry-analysis/real-world-evidence-solutions-market) |
| Purchase channel | CRO partnerships; bundles with data vendors (Datavant-Aetion with 300+ data partners, TriNetX, Truveta); direct sales to top-20 pharma teams running externally controlled trials (inference) | inference |
| | Pharma and distributors already invest strategically: Merck GHI, Cencora and McKesson in Atropos | second-hand; [Fierce Healthcare](https://www.fiercehealthcare.com/health-tech/atropos-health-lands-33m-scale-ai-powered-real-world-evidence-build-out-pharma) |
| Price points | **No public price for any RWE platform or data licence was found** (Aetion, Flatiron, TriNetX, Truveta, Komodo, Optum, IQVIA E360) | gap |
| | causaLens decisionOS was listed at ~£240k per licence per year on UK G-Cloud (a non-pharma anchor) | vendor claim, via AU5 |
| | FDA bought two BayesiaLab licences for expert causal diagrams | via AU5 |
| | Oncology trial cost per patient "frequently exceeds $150,000"; synthetic control arms could save **$10-20M per trial** | second-hand consultant estimate, 2021; [BCG](https://www.bcg.com/publications/2021/synthetic-control-arms-changing-clinical-trials) |
| Competitors | Aetion (now Datavant; "advanced causal inference"), IQVIA, Flatiron (Roche; five-year FDA research collaboration), TriNetX (Carlyle majority), Truveta ($320M at more than $1B), Komodo (its Marmot platform is marketed as "reproducible, traceable, and governed"), Atropos (ChatRWD, an "Evidence Agent" from Mar 2026), Optum, Unlearn (PROCOVA) | vendor claims and second-hand; [Datavant](https://www.datavant.com/press-release/datavant-completes-acquisition-of-aetion), [Komodo](https://www.komodohealth.com/perspectives/ai-in-heor-what-ispor-2026-revealed/), [Atropos](https://www.businesswire.com/news/home/20260309966082/en) |
| Regulatory drivers | **ICH M14** reached Step 4 in Sep 2025; FDA finalised it on **4 Mar 2026**. Protocols must describe data sources and fitness for use and address bias and confounding. | primary; [FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m14-general-principles-planning-designing-analyzing-and-reporting-non-interventional-studies-utilize) |
| | FDA's device RWE final guidance (18 Dec 2025) requires causal diagrams in protocols and time-stamped revisions | primary, via `AB13_regulation_map.md` |
| | EMA adopted its RWD reflection paper on 17 Mar 2025 | second-hand; [RAPS](https://www.raps.org/resource/ema-adopts-reflection-paper-on-rwe-from-noninterve.html) |
| | The FDA AI credibility guidance is **still a draft** (7 Jan 2025) | primary; [FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological) |
| | The EU AI Act's high-risk duties are postponed to Dec 2027 / Aug 2028, and drug RWE is largely outside them | primary, via AB13 |

**Bottom-up estimate (every number below is an estimate).** Regulator-counted RWE is small but growing fast. CDER protocols with RWE went from 10 to 11 to **31** over FY2023-2025 (primary; [FDA CDER](https://www.fda.gov/science-research/real-world-evidence/real-world-evidence-submissions-center-drug-evaluation-and-research)). FDA's tables cover only submissions that meet PDUFA reporting criteria.

| Model | Inputs | Arithmetic | Result |
|---|---|---|---|
| A. Regulatory core: one assumption ledger per regulator-reported RWE study | CDER FY2025: 31 protocols + 10 NDA/BLAs + 6 final reports = 47 (primary). CBER FY2025: 8 + 0 + 1 = 9 (second-hand summary of FDA; [Becaris](https://becarispublishing.com/digital-content/blog-post/fda-releases-latest-figures-real-world-evidence-use-regulatory-submissions)). EMA-side submissions assumed equal to FDA's (assumption). Price $25-100k per study (assumption). | (47 + 9) × 2 = 112; 112 × $25k to 112 × $100k | **$2.8M-11.2M a year** |
| B. All registered RWE and observational studies | 927 RWE-labelled ClinicalTrials.gov registrations starting in 2022, a keyword undercount (second-hand; [ISPOR 2023 poster](https://www.ispor.org/heor-resources/presentations-database/presentation/intl2023-3666/127420)). EU sponsor studies assumed equal to that (assumption). ~180 EMA studies a year around 2025 (primary; [EMA](https://www.ema.europa.eu/system/files/documents/leaflet/infosheet-ema-review-real-world-data-studies_en.pdf)). Price $10-50k per study (assumption). | 927 + 927 + 180 = 2,034; × $10k to × $50k | **$20.3M-101.7M a year** |
| Top-down cross-check | 1-3% (assumption) of the 2025 RWE-solutions market, $2.6B (analyst claim; [GMI](https://www.gminsights.com/industry-analysis/real-world-evidence-solutions-market)) | 0.01-0.03 × $2.6B | **$26M-78M a year** |
| Seat-based cross-check | ~18,000 ISPOR members (primary, undated; [ISPOR](https://ispor.org/about/our-members)) × 30% at sponsors and CROs (assumption) × 10% adopting (assumption) × $10k per seat (assumption) | 540 seats × $10k | **$5.4M a year**, showing that per-seat pricing is weaker than per-study pricing |
| Value anchor | CDER FY2025 had 5 externally controlled trial (ECT) protocols and 4 NDA/BLAs built on ECTs (primary); one ECT saves $10-20M per trial (second-hand) | — | The highest-value niche. A ledger could be priced as insurance on a large ticket rather than as an analytics fee. |

**Strongest demand signals.** This vertical has the clearest public record of causal claims failing review for exactly the defects a ledger records:

- Of FDA CDER's 10 FY2025 NDA/BLAs with RWE, there were 4 approvals where RWE contributed, 1 approval where it did not, **4 complete response letters (CRLs) and 1 refuse-to-file** (primary; [FDA CDER](https://www.fda.gov/science-research/real-world-evidence/real-world-evidence-submissions-center-drug-evaluation-and-research)).
- Biohaven's troriluzole CRL (4 Nov 2025) cited "potential bias, design flaws, **lack of pre-specification** and unmeasured confounding factors" (primary company release; [Biohaven](https://ir.biohaven.com/news-releases/news-release-details/fda-issues-complete-response-letter-biohavens-vyglxia)).
- EMA judged **7 of 21 (33%)** RWD external controls inadequate in 2015-2023 (second-hand poster; [ISPOR Europe 2025](https://www.ispor.org/heor-resources/presentations-database/presentation-cti/ispor-europe-2025/poster-session-2-2/real-world-data-for-external-controls-insights-from-ema-regulatory-submissions)).
- Komodo's ISPOR 2026 recap says there is "no consensus" on validating LLM-assisted evidence, and that reviewers may not know which steps were human-specified and which were model-generated (vendor-authored commentary; [Komodo](https://www.komodohealth.com/perspectives/ai-in-heor-what-ispor-2026-revealed/)). That maps directly onto per-claim source typing.

The counter-evidence comes from buyer surveys, where auditability does not appear as a top barrier:

- Deloitte's barriers are data privacy (27%), shortage of combined RWE and AI expertise (25%) and regulatory uncertainty (23%) (survey, n=25, second-hand; [Becaris](https://becarispublishing.com/digital-content/blog-post/deloitte-s-latest-rwe-benchmarking-survey-highlights-biopharma-s-next-steps-real-world)).
- TriNetX's top barrier is data compatibility (survey, vendor-run, n=150; [TriNetX](https://trinetx.com/blog/ai-real-world-data-and-inclusion-in-pharma-2025-industry-survey-report/)).

A conflict in counts also needs flagging. An ISPOR 2025 poster says RWE was "central to nearly half" of 2024 novel approvals (second-hand; [ISPOR](https://www.ispor.org/heor-resources/presentations-database/presentation-cti/ispor-2025/poster-session-3/summary-of-evolving-role-and-impact-of-real-world-evidence-rwe-in-us-fda-regulatory-approvals-2020-2024)), while CDER counts 1 RWE NDA/BLA in FY2024. The definitions differ, and the two must not be mixed in one funnel.

## The public evidence on H1-H3 is indirect and lopsided

Everything in this section is **indirect evidence**. None of it is an interview with the capstone's target users. It stands in for the planned 5-8 practitioner interviews (AB-10) only in the sense of setting priors. The audit DAG pre-registered P13: half of interviewees name a decision where "which causes, how sure" matters more than the graph, refuted if fewer than a quarter do. Its kill rule says the product angle is shelved if no interviewee values provenance or abstention (`claude/audit-dag.md`). Public evidence can neither trigger nor clear that criterion. Every analytics-trust survey found is vendor-run, and no public survey asks about causal claims specifically.

### H1: per-claim provenance and abstention would be used

| Evidence | Label | Sector | Direction | Source |
|---|---|---|---|---|
| 53% prioritise audit trails for AI-generated answers; 51% want verifiable or deterministic outputs; 31% cannot verify AI results; only 51% trust AI insights | survey, vendor-run, n=114; fieldwork dates unpublished | cross-industry data leaders | + (answer-level lineage, not causal edges) | [insightsoftware](https://www.insightsoftware.com/blog/why-dont-data-leaders-trust-ai-and-other-insights-from-our-2026-ai-survey/) |
| 95% say AI showing its reasoning is important (48.2% "very important" or "critical") | survey, vendor-run, n>1,300 | observability | + | [Grafana](https://www.grafana.com/blog/observability-survey-AI-2026) |
| 46% distrust AI accuracy vs 33% who trust it; 66% cite answers that are "almost right, but not quite" | survey, n≈49,000 (implied by response counts) | developers | + (verification is the cost) | [Stack Overflow](https://survey.stackoverflow.co/2025/ai) |
| 60% say stakeholders question their metrics; 22% strongly feel they can prove value to finance | surveys: n=196 (vendor-run) and n=167 (second-hand) | marketing | + | [TransUnion](https://newsroom.transunion.com/new-transunion-research-reveals-marketers-confidence-in-measurement-has-stalled/); [MarketScale](https://www.marketscale.com/industries/marketing-tech/only-22-of-marketers-feel-sure-they-can-justify-spend-to-the-cfo.md) |
| 4 CRLs + 1 refuse-to-file among 10 RWE NDA/BLAs; Biohaven cites "lack of pre-specification" | primary | pharma | + (missing provenance carries a measurable penalty) | [FDA CDER](https://www.fda.gov/science-research/real-world-evidence/real-world-evidence-submissions-center-drug-evaluation-and-research); [Biohaven](https://ir.biohaven.com/news-releases/news-release-details/fda-issues-complete-response-letter-biohavens-vyglxia) |
| ~1,600 court cases in 35 countries involve AI-hallucinated citations, with sanctions | second-hand (journalism citing a crowd-sourced database) | legal (analogue) | + (cost of unverified claims, not willingness to pay) | [Malay Mail](https://www.malaymail.com/news/tech-gadgets/2026/06/16/do-your-job-global-courts-face-rising-tide-of-ai-generated-fake-cases-and-quotes/223865) |
| Vendors already sell confidence scores, evidence links, "verifiable" investigations and citations | vendor claims | IT | + for demand; − for differentiation | [Cleric](https://businesswire.com/news/home/20251209625361/en/Cleric-Launches-the-First-Self-Learning-AI-SRE); [Datadog](https://www.datadoghq.com/product/ai/bits-investigation/) |
| Security and cost have gained ground on accuracy: "all the models perform well enough now" | survey, n=100 CIOs | enterprise | − | [a16z](https://a16z.com/ai-enterprise-2025/) |
| Trust and explainability do not appear among top purchase criteria (GenAI capabilities 40.6%, features 39.6%, pricing 39.6%) | survey, n not stated | enterprise software buyers | − | [Futurum](https://futurumgroup.com/press-release/genai-features-are-the-top-criteria-for-future-enterprise-software-purchases/) |
| Only 15% call AI capabilities an important selection criterion | survey, vendor-run, n>1,300 | observability | − | [Grafana](https://www.grafana.com/blog/observability-survey-AI-2026) |
| Abstention specifically: no survey measures it. Only behaviours exist: Datadog "inconclusive" outcomes (via AB11), NeuBird escalating to a human, and one essay endorsing explicit partial answers. | vendor claims; anecdote | IT | ~ | [TechCrunch](https://techcrunch.com/2024/12/11/microsofts-m12-invests-another-22-5m-into-nuebird-months-after-its-22m-seed-round/); [HackerNoon](https://hackernoon.com/when-your-ai-sre-runs-out-of-telemetry-the-missing-evidence-problem-in-production-debugging) |
| AB-12: abstention adds +0.031 AC@3 on answered issues and nothing on no-issue windows | project measurement | IT | ~ (the feature does not yet deliver) | `ab12_rca_probe.md` |

**Verdict: supported for provenance as a stated preference, unsupported for abstention, and unproven as a purchase.** Across three verticals, people say they want AI to show its work. The pharma record shows that missing pre-specification and provenance have a measurable cost. But every survey that asks how buyers choose tools ranks capability and price above trust. "Citations" and "verifiable" are already marketing words. The defensible differentiator is therefore narrower than "provenance": a typed source per sub-claim, calibration measured against labelled cases, and an abstention rate that is reported rather than hidden. Nothing public measures whether practitioners would accept an abstaining tool.

### H2: practitioners ask intervention questions, not for full graphs

| Evidence | Label | Sector | Direction | Source |
|---|---|---|---|---|
| Statsig: $1.1B exit and ~$40M annualised revenue; Eppo: ~$220M. Both measure intervention effects; neither sells graph discovery. | second-hand | experimentation | + | [Fortune](https://www.fortune.com/2025/05/06/statsig-series-c-100-million-1-1-billion-eppo-datadog); [AI Business](https://aibusiness.com/generative-ai/openai-acquires-startup-for-1-1b-hires-ceo) |
| Uber's causal work estimates effects of interventions (email campaigns, surge pricing) with CUPED, diff-in-diff, IV and regression discontinuity; graphs are built "with domain expert input" | primary (engineering blog, 2019) | marketplace | + | [Uber](https://www.uber.com/blog/causal-inference-at-uber/) |
| "Computational Causal Inference" frames the field as computing many causal effects on massive data (Netflix affiliation from search context) | primary (arXiv abstract) | streaming | + | [arXiv 2007.10979](https://arxiv.org/abs/2007.10979) |
| Industry prioritises speed and individual treatment effects; success is judged on live KPIs | anecdote (practitioner essay) | general data science | + | [TDS](https://towardsdatascience.com/how-is-causal-inference-different-in-academia-and-industry-fb5afd12e2e7) |
| 60% trust incrementality experiments most, vs 40% MMM | survey, vendor-run, n=500 | marketing | + | [EMARKETER](https://www.emarketer.com/content/incrementality-testing-earns-marketers--top-trust) |
| Commercial RCA ranks causes over a declared topology (Dynatrace, New Relic, Instana, Causely); 91% value root-cause assistance | vendor docs via AU5 F2; survey, vendor-run, n>1,300 | IT | + ("which cause" over a given graph) | `AU5_commercial.md`; [Grafana](https://www.grafana.com/blog/observability-survey-AI-2026) |
| FDA's device RWE guidance asks for a causal diagram in the protocol | primary, via AB13 | pharma | ~ (a graph is wanted, but as a declared assumption, not a discovered one) | `AB13_regulation_map.md` |
| ShowWhy archived; CausalNex end of life; an HN search for "LLM causal discovery" returned 4 stories, none on the topic | primary; anecdote (volume) | tooling | + for H2; − for selling graphs | [GitHub](https://github.com/microsoft/showwhy); [HN Algolia](https://hn.algolia.com/api/v1/search?query=LLM%20causal%20discovery&tags=story&hitsPerPage=20) |
| Some buyers do rely on learned graphs: Amazon supply-chain KPI attribution (PC + DoWhy GCM), Xplain Data at Schaeffler and TRUMPF, Aitia target discovery | reported / second-hand, via AU5 F4 | supply chain; manufacturing; pharma R&D | − | `AU5_commercial.md` |

**Verdict: the strongest of the three, with a scope caveat.** The money and the published practice both point at "what happens if we change X", and at "which of these causes, given a graph we already trust". Learned graphs on their own are being abandoned as products. Where graphs are demanded, by regulators and by Uber's teams, they are expert-drawn statements of assumption. That is consistent with treating structure as something a ledger records the source of, not something it discovers. The caveat is that this evidence describes large tech firms' internal practice and the companies acquirers paid for. It does not say what users of LLM causal tools ask, which is what P13 tests. The few documented cases where discovery is relied on (supply chain, manufacturing, target discovery) are also the cases with no published graph accuracy.

### H3: an audit of name and semantic reliance is worth paying for

| Evidence | Label | Sector | Direction | Source |
|---|---|---|---|---|
| Braintrust raised $80M at an $800M post-money valuation (Feb 2026) | second-hand | LLM evaluation | + | [Axios](https://www.axios.com/pro/enterprise-software-deals/2026/02/17/ai-observability-braintrust-80-million-800-million) |
| Arize raised a $70M Series C with Datadog and PagerDuty participating (Feb 2025) | primary announcement; "largest-ever" is a vendor claim | AI observability | + | [Arize](https://arize.com/blog/arize-ai-raises-70m-series-c/) |
| Langfuse acquired by ClickHouse (Jan 2026), with 2,000+ paying customers claimed | vendor claim (counsel's announcement) | LLM observability | + | [Orrick](https://www.orrick.com/en/news/2026/01/open-source-llm-observability-langfuse-acquired-by-clickhouse-inc) |
| Patronus raised a $17M Series A (2024) for hallucination detection | primary | LLM evaluation | + | [Patronus](https://patronus.ai/blog/announcing-our-17-million-series-a) |
| UK AI assurance: 524 firms (84 specialised, up from 17 in 2023), ~£1.01bn; demand "below potential", and buyers have limited understanding of what assurance is worth | primary government report, via a law-firm summary | AI assurance | + and − | [Burges Salmon](https://www.burges-salmon.com/articles/102jph1/ai-assurance-the-uk-market-and-government-actions-dsit-report/) |
| No AI SRE vendor publishes production precision or recall; a competitor tells buyers to demand them | second-hand (competitor-written) | IT | + (the evaluation gap exists) | [incident.io](https://incident.io/blog/rootly-ai-accuracy-vs-competitors) |
| Datadog reportedly bills only conclusive investigations | second-hand, unverified | IT | + for a third-party auditor, if true | [Better Stack](https://betterstack.com/community/comparisons/bits-ai-sre-alternatives/) |
| The defect exists. EvoCause loses 6.12 Node F1 when alarm titles are anonymised (reported, arXiv 2607.27290, via AU5). CARE drops 0.858 → 0.137 under permuted names (via AB15). Causal-Copilot falls 0.306 → 0.232 → 0.142 (project measurement, via AU5). | reported; project measurement | technical, not demand | ~ (nobody is shown paying to find the defect) | `AU5_commercial.md`; `AB15_positioning.md` |
| Enterprises build their own golden datasets: "you still need to assess yourself" | survey, n=100 CIOs | enterprise | ~ (evaluation is demanded, but done in-house) | [a16z](https://a16z.com/ai-enterprise-2025/) |
| No evidence found of anyone paying for a causal-claim or name-reliance audit specifically | negative search result | all | − | `demand_signals.md` notes, Q4 gaps |

**Verdict: plausible by analogy, unproven in fact.** A funded category exists for "evaluate the LLM before trusting it": hundreds of millions of dollars in rounds and at least one exit. A name-reliance audit would sit inside it as a specialised evaluation. The UK government's own finding that assurance demand is "below potential" warns that buyers often do not understand what they would be buying. The most natural first payers are the AI SRE vendors themselves, who need proof for enterprise buyers, and those enterprise buyers comparing agents. That is the one setting where an LLM agent visibly reads names such as `payforadoption_AWS::ECS::Container`. No public evidence shows that commercial RCA agents rely on names. That is a measurement the project can make itself (a names arm on PetShop), and it should be made before anyone is asked to pay.

## IT incident RCA should go first, with marketing a close second

The ranking below answers a narrower question than AU5's. AU5 ranked product angles by demand evidence alone and put marketing first. This report asks where a student team with this project's results should *start*. That weights fit with what has been measured, the ability to prove the product on public data before any customer, and whether H3 can be tested in the vertical. On demand evidence alone, marketing still leads.

| Criterion | IT incident RCA | Marketing measurement | Pharma RWE |
|---|---|---|---|
| Directness of public demand evidence | Medium: 95% want reasoning shown (vendor-run); competitor and practitioner critiques; no paid evidence | **High**: credibility pain, budgets reallocated over doubt (vendor-run surveys) | Medium: 4 CRLs + 1 refuse-to-file of 10 (primary); audit not a top barrier in surveys |
| Fit with what the project has measured | **High**: AB-12 declared topology 0.901 vs learned 0.208; sub-claim ledger schema exists | Low to moderate: effect estimation, not discovery; intervention-sourced claims as a ledger tier | Moderate: AB13 maps ledger fields to 50 requirement rows; regulators want declared designs, not discovery |
| Can H3 (name reliance) be tested here | **Yes**: LLM agents read service names; 68 PetShop incidents ready for a names arm | Weak: channel names are few and standardised | Possible, but no public data with ground truth |
| Price transparency | **High**: public per-investigation and flat prices | Medium: Northbeam public; Haus second-hand | None |
| Bottom-up size (estimate) | Obtainable $1.8-9.0M ARR in 3 years; serviceable $0.34-289M per investigation or $40-547M flat | **Obtainable $3-67.5M; realistic serviceable ceiling $77-154M** | Core $2.8-11.2M/yr; broad $20.3-101.7M/yr |
| Channel open to a small team | Medium-high: AWS Marketplace AI Agents & Tools, MCP integrations | Medium: 51 Meridian partners, 4 also GeoX-certified | Low: CRO and data-vendor partnerships, regulated validation |
| Incumbent bundling and conflicts | High bundling risk (Datadog "verifiable", Cleric confidence scores), but vendors have an incentive not to abstain, which favours a third party | High: Haus and Lifesight bundle experiments and would themselves be audited | Medium: Aetion and Komodo already use "traceable" language |
| Time to a credible proof | **Short**: public benchmarks (PetShop, RCAEval) | Medium: simulation plus lift-test data needed | Long: patient-level data and regulatory acceptance |
| **Rank** | **1** | **2** | **3** |

**IT incident RCA ranks first.** It is the only vertical where the project already holds a measured, reproducible result, where the name-reliance audit applies to a real product class, and where both the buyer pool and prices can be read from filings and pricing pages. Its weakness is the one that matters most: the abstention the product promises does not yet work on no-issue windows, and buyers do not choose tools on AI features.

**Marketing ranks second, on the strongest stated pain and the healthiest price ladder.** The ladder runs from $18-42k a year at Northbeam to ~$150k at Haus, and an add-on at $30-75k fits between them. Its fit with the project's assets is weaker. The incumbents it would audit also bundle the experiments, and the evidence tags would have to grade the experiments themselves.

**Pharma ranks third.** It has the strongest regulatory hooks and the highest value per decision, but a small must-have core, no price data, slow sales, and a credibility bar a capstone cannot clear alone. It is best approached later, through a CRO or data-vendor partner.

| New evidence | Effect on the ranking |
|---|---|
| A PetShop names arm finds that LLM RCA agents keep their accuracy when service names are neutralised or swapped | H3 loses its RCA hook; marketing moves to first |
| A normal-period-aware abstention rule fails to cut the 40-83% of fabricated root causes on no-issue latency windows | The RCA product cannot show its core feature; marketing moves to first |
| Datadog, Dynatrace or AWS ship typed per-claim sources with calibration and a reported abstention rate | The gap closes; RCA drops, possibly below marketing |
| Datadog confirms on its own pages that only conclusive investigations are billed | The third-party case strengthens; RCA holds first |
| SRE interviewees price verification below ~$0.30 per investigation, or say they would not pay for it separately | RCA survives only as a flat fee, or drops |
| A Meridian or GeoX partner, or a marketing-science lead, agrees to pilot evidence grading | Marketing moves to first |
| A MediaRadar/Vivvix export or ANA count puts US advertisers running MMM well above 6,000 | Marketing's size rises; its rank may follow |
| FDA finalises the AI credibility or ECT guidance with claim-level traceability, or a CRO asks to partner | Pharma rises, at least above marketing as a long-term track |
| FDA's CRL publication initiative shows pre-specification is a common reason RWE submissions fail | Pharma's demand case strengthens |

## Ten corrections to AU5, AB11 and AB13

The notes confirm AB-12 rather than correct it. They also find that AB-12's open item, fabricated root causes on no-issue windows, matches the most common public practitioner complaint about AI SRE tools. The ten corrections below apply to the three desk files.

| Earlier file said | The notes show | Label; source |
|---|---|---|
| AU5/AB11: Haus's "$20M raise" was used as a current investor signal | It is dated 30 Jul 2024 by Haus itself; a law-firm snippet says Oct 2024. An aggregator puts the total at $61.65M with a $435.72M valuation. | primary, [Haus](https://haus.io/blog/haus-announces-20m-raise-led-by-01-advisors); second-hand, [StockAnalysis](https://stockanalysis.com/private/haus/) |
| AU5: Statsig was acquired by OpenAI | Amplitude is taking over Statsig's brand and customers (announced 5 May 2026); OpenAI's independence promise was retired | second-hand; [Convert](https://convert.com/blog/a-b-testing/statsig-moves-to-amplitude/) |
| AU5: Aetion was acquired by Datavant in May 2025 | Announced 15 May 2025, completed July 2025 | vendor release; [Datavant](https://www.datavant.com/press-release/datavant-completes-acquisition-of-aetion) |
| AU5: causal AI is $56.2M (MarketsandMarkets) and more than $1B (theCUBE) | Eight sizings span $28.9M to $59.22B; MarketsandMarkets revised its own 2023 base fivefold | analyst claims; §1 table |
| AB11: Dynatrace is ~30 AI units (≈ $3) per investigation | Not on the rate card read 13 Oct 2026; unconfirmed | primary; [Dynatrace](https://www.dynatrace.com/pricing/rate-card/) |
| AU5/AB11: Datadog is $6.50-8.45 per investigation | Competitors quote $500 per 20 (≈ $25). Datadog's CEO says an AI-credit model is being rolled out. Unresolved. | second-hand, [Better Stack](https://betterstack.com/community/comparisons/bits-ai-sre-alternatives/); primary transcript, [DDOG 2Q26](https://transcripts.platformaeronaut.com/transcripts/DDOG-2Q26-transcript) |
| AB11: PagerDuty AIOps from $699/month | The current page shows platform fees of $2,800, $12,000 and $48,000 a year and an AIOps SKU with no price | primary; [PagerDuty](https://www.pagerduty.com/pricing/) |
| AB13: no ICH M14 row | ICH M14 reached Step 4 in Sep 2025 and FDA finalised it on 4 Mar 2026; it should be added as a requirement row | primary; [FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m14-general-principles-planning-designing-analyzing-and-reporting-non-interventional-studies-utilize) |
| AU5: CausalNex absent from the churn list | End of life 24 Jun 2026 (AB11 already had this) | primary; [GitHub](https://github.com/mckinsey/causalnex) |
| AU5: cites a Gartner "Cool Vendor" category for RCA | Gartner now has a Market Guide for AI SRE Tooling (26 Jan 2026) that assumes adoption rises from under 5% to 85% by 2029 | second-hand; [Cast AI](https://cast.ai/gartner-market-guide-for-ai-sre-tooling/) |

## Where we're going

The commercial track now has public priors but no primary demand evidence. The next moves should turn the RCA ranking into something testable before the AB-16 wedge decision:

1. **Add a names arm on PetShop's 68 incidents**: an LLM root-cause agent (a small live run, still to be planned; AB-06 itself covers causal-discovery agents, not RCA agents) given real, neutral and swapped service names and the declared graph and anomaly scores held fixed. This gives H3 a measured basis in the starting vertical.
2. **Fix the abstention rule** with the normal-period-aware condition AB-12 already specified: a score floor on the target, or anomaly persistence over two or more rows. The RCA pitch depends on cutting the 40-83% of fabricated answers, not on the +0.031 gain on answered issues.
3. **Verify Datadog's billing rule** for inconclusive investigations from Datadog's own documentation, since the third-party argument partly rests on it.
4. **Spot-check every market-size figure** in the §1 tables against the original page before any of them reaches the AB-16 discussion or a mentor deck. Spot-checked so far (13 Oct): FDA CDER RWE counts, Datadog's ≥$100k customer count and guidance, Resolve's round, CausalNex's end of life, and ICH M14's final status all match their primary pages.
5. **Keep the AB-10 interview guide ready for whenever a chance arises**, built around the inputs this report could not source (interviews may never happen, so nothing above waits on them; confirm with course staff whether informal interviews need human-subjects review before any are run). The inputs to ask about:
   - investigations per month (I);
   - what share of the agent price a verifier could take (s);
   - the signing title;
   - whether abstention would be accepted or switched off.

   The interview mix should favour 3 SREs, 2 marketing-science leads drawn from the four GeoX-certified Meridian partners, and 1 RWE epidemiologist.

Several gaps cannot be closed by public research at all. Willingness to pay for calibrated confidence and abstention, separately from the agent, can only come from interviews or a pilot; so can the identity of the economic buyer and P13 itself. Three other gaps are commercial data that sits behind paywalls or inside companies:

- investigation volumes per organisation for AI agents;
- de-duplicated counts of buyers across vendor customer lists;
- US advertiser counts by spend band, which a MediaRadar/Vivvix export or ANA count could close.

RWE platform and study prices are negotiated privately, and the reasons for individual CRLs remain largely unpublished. Whether incumbents will bundle verification for free can only be watched, not researched.

What has changed is the frame. The causal-AI category is not where the money is, and the project should not pitch itself as one more causal-AI platform. The defensible offer is a **vendor-neutral audit of causal claims made by other people's agents**: typed source per sub-claim, measured calibration, reported abstention, and a name-reliance test. The binding constraint in every vertical is proof that the audit catches wrong answers, not proof that buyers have budget. The project's next measurements, AB-06 and the abstention fix, are therefore also its next commercial evidence.
