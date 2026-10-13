# Causal AI market map (commercial causal discovery / inference / "causal AI"), as of 2026-10-13

Scope note: this extends AU5_commercial.md (42 rows, 2026-10-12), AB11_vendor_claims.md (pricing signals) and AB15_positioning.md. AB15 covers academic prior work only, so nothing here overlaps it. Facts already in AU5/AB11 are not repeated unless this pass updates or corrects them; corrections are marked **[CORRECTS AU5]** or **[UPDATES AU5]**. All pages were fetched 2026-10-13 through a summarising fetch tool, so numbers should be spot-checked before they go into a deck.

Labels: **primary** means the company's own announcement, filing, blog or repo. **second-hand** means news, an aggregator (Seedtable, CB Insights, VCBacked, PrivateMarketView) or a competitor's blog. **vendor claim** means a performance or ROI statement made by the vendor about itself; these are never measurements. Analyst market-size numbers are the analyst firm's own claims, so they are labelled **primary (analyst claim)** when read on the firm's own page and **second-hand** when read on a reseller or wire page.

## 1. Who sells causal AI / causal inference / causal discovery (2024-2026), by segment

### Takeaway
The "causal AI" label covers six segments that barely overlap. Two pure-play enterprise "causal AI platforms" raised money in 2021-2022 and have since either repositioned to LLM agents (causaLens) or remain small (Geminos). Most of the new 2025-2026 money with a causal or root-cause pitch went to AI SRE agents: Resolve AI ($125M Series A at a $1B valuation, Feb 2026), Traversal ($48M, June 2025), NeuBird ($19.3M, Apr 2026) and Cleric ($9.8M seed). Experimentation and marketing measurement are where the large exits are.

### Cited Findings

**A. Enterprise causal-AI platforms (horizontal)**
- causaLens (London): $45M Series A, first close. Leads were Dorilton Ventures and Molten Ventures (formerly Draper Esprit); existing investors Generation Ventures and IQ Capital and new investor GP Bullhound also joined. Named customers were Aviva and TIAA. The page has no visible date; the text says funds will double the team "in 2022". (primary) — [causaLens](https://causalens.com/causal-ai/startup-series-a-funding-round-45-million). The press coverage that dates it to Jan 2022 was found but not opened: [VC Journal](https://www.venturecapitaljournal.com/causalens-scores-45m-series-a/), [Business Wire via ANSA, 2022-01-28](https://embed.ansa.it/sito/notizie/economia/business_wire/news/2022-01-28_128285552.html). No later round was found in the searches run.
- causaLens product, as of 2026-10-13: the homepage sells "Digital Workers", multi-agent LLM systems ("Blueprints", "Factory", "System of Work"). It claims "5x ROI in year one" (vendor claim). The name "decisionOS" no longer appears, and causal reasoning is now a feature claim ("Our Digital workers reason via causation"). Named testimonials: Johnson & Johnson, McCann Worldgroup, DANA Indonesia, Syneos Health, Cisco, Croud. No pricing. (primary) — [causalens.com](https://causalens.com/)
- Geminos Software: CB Insights shows only one round, a Jan 24, 2024 incubator/accelerator round with Deere Startup Collaborator, amount undisclosed, with no total funding disclosed (second-hand) — [CB Insights](https://www.cbinsights.com/company/geminos-software/financials). No priced round was found.
- Kausable (Germany, new 2026 entrant): seed round on 9 July 2026, led by UVC Partners and Entourage with HTGF and Mätch VC. It builds "reasoning-first" AI that learns causal structure. The amount conflicts within the source (€12M in the headline vs $13.8M / €13.8M in the body) (second-hand) — [Nordic9](https://nordic9.com/news/kausable-raises-12-million-in-a-seed-funding/). The InforCapital page could not be fetched (client error).
- Causa / CausaDB (York, UK): six-figure pre-seed, Feb 2024 (second-hand, headline only, not opened) — [Tech.eu](https://tech.eu/2024/02/09/causadb-the-new-cloud-native-platform-for-causal-ai-deployment-raises-pre-seed-funding/)
- StartUs Insights says it tracks 733 "causal AI startups". Its top hubs are SF, NYC, London, Bangalore and Toronto. Companies it names include Allos, Causa, Senzai AI, Black Forest AI, Cogxta, The PI, benshi.ai, Senser (eBPF RCA), Vedrai and Seeda (MMM). It gives no funding figures (second-hand, published 2025-02-20) — [StartUs Insights](https://www.startus-insights.com/innovators-guide/causal-ai-companies/)
- Analyst vendor lists show the category boundary is fuzzy:
  - MarketsandMarkets key players: IBM, causaLens, Microsoft, Dynatrace, Causality Link, Cognizant, Logility, DataRobot, Google, Aitia, Causaly, Data Poem, Lifesight, Parabole.AI. Highlighted startups: Parabole.AI, Howso, Incrmntal — [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/causal-ai-market-162494083.html)
  - GMI's "key players" are mostly big tech with no causal product (Dropbox, Pinterest, Snap, Reddit, Xiaomi) — [GMI](https://gminsights.com/industry-analysis/causal-ai-market)

**B. Observability / AIOps / AI SRE with "causal" or root-cause reasoning** (incumbents' RCA products are already in AU5 F2 and AB11 pricing)
- Causely (causal RCA): $8.8M seed on 2023-06-29, led by 645 Ventures, with Amity Ventures, Glasswing Ventures and Tau Ventures. "Over $11 million" raised since its 2022 founding (primary) — [Causely blog](https://www.causely.ai/blog/causely-raises-8-8m-in-seed-funding-to-deliver-it-industrys-first-causal-ai-platform). VCBacked instead says $10.8M total, adds Cervin Ventures, and dates its data to 2023-06-29 (second-hand; conflicts with primary) — [VCBacked](https://www.vcbacked.co/company/causely). No priced round after 2023 was found.
- Causely, 2025-2026 activity: no funding posts. It shifted to being a "causal reasoning engine" that feeds other agents: an MCP Server (Nov 2025), a Gemini pairing (2025-10-29), Datadog, IBM Instana and Dynatrace integrations (2025-12-22, 2025-10-23, 2026-07-24), a Cursor plugin (2026-05-12), MCP Skills (2026-06-03), and joining AAIF with A2A (2026-08-17) (primary) — [Causely blog index](https://www.causely.ai/blog)
- Resolve AI: $125M Series A on 2026-02-02 at a $1B valuation, led by Lightspeed, with Greylock, Unusual Ventures, Artisanal and A*. Total raised is more than $150M. Named customers: Coinbase, DoorDash, MongoDB, MSCI, Salesforce, Zscaler. Coinbase "72% reduction in time to investigate" and Zscaler "30% fewer engineers per incident" are vendor claims with no method. No root-cause accuracy figure is given (primary) — [Resolve blog](https://resolve.ai/blog/series-a-funding)
  - Seedtable dates the Series A to 2026-02-04 (citing TechCrunch and PR Newswire) and lists a $35M seed in Oct 2024 led by Greylock, for $160M total (second-hand; the date is 2 days off the primary) — [Seedtable](https://seedtable.com/companies/resolveai/funding-rounds/series-a-2026-02)
- Traversal: $48M across seed and Series A combined, led by Sequoia and Kleiner Perkins, with NFDG and Hanabi. It says it combines agents with "causal machine learning" research. Accuracy claim: ">90% accuracy on hundreds of high-impact incidents" (vendor claim, no method). Customers: DigitalOcean, Eventbrite, Cloudways and unnamed "largest financial institutions in the Fortune 100" (primary; the page has no date) — [Traversal](https://traversal.com/blog/launch-announcement). The round is dated June 2025 by second-hand sources — [Built In NYC, 2025-06-20](https://www.builtinnyc.com/articles/traversal-raises-48m-to-launch-ai-sre-20250620)
  - PrivateMarketView shows $53.0M total and a "last reported valuation" of $309.5M dated Oct 2026, with no rounds recorded and no source for the valuation (second-hand, low reliability) — [PrivateMarketView](https://privatemarketview.com/companies/traversal/funding-rounds)
- Cleric: $9.8M total seed, led by Vertex Ventures US, with Zetta Venture Partners (the initial seed investor). Launched as a "self-learning AI SRE" on ~2025-12-09 (date from the URL). Customer: BlaBlaCar (in production since early 2025). It attaches confidence scores to findings; the claim of 20-30% of engineering capacity freed is a vendor claim. No accuracy metrics (primary) — [Business Wire](https://businesswire.com/news/home/20251209625361/en/Cleric-Launches-the-First-Self-Learning-AI-SRE). An earlier $4.3M raise was reported (second-hand, headline only, not opened) — [Pulse 2.0](https://pulse2.com/cleric-4-3-million-raised-and-autonomous-ai-site-reliability-engineer-unveiled)
- NeuBird AI: $19.3M oversubscribed round on ~2026-04-06 (date from the URL), led by Xora Innovation, with Mayfield, StepStone, Prosperity7 and M12 (Microsoft). Claims RCA "in real time" and "up to 90% reduction in MTTR" (vendor claims) (primary) — [Business Wire](https://www.businesswire.com/news/home/20260406552258/en)
- incident.io (incident management, with AI investigation; also the author of the critique cited in AU5): $62M Series B on 2025-04-10 from Insight Partners, Index Ventures and Point Nine; $100.7M total; Series A valuation $350M (July 2022) (second-hand) — [CB Insights](https://www.cbinsights.com/company/incidentio/financials)

**C. Marketing measurement (incrementality / MMM / "causal attribution")**
- Haus: $20M "additional investment" on 2024-07-30, led by 01 Advisors (David Fischer, Dick Costolo, Adam Bain), with Rahul Mehta, Gokul Rajaram, Insight Partners (increased), Baseline, Haystack, Octave and Mantis. It launched a "Causal Attribution" product calibrated with GeoLift experiments. An earlier $17M Series A led by Insight Partners is referenced by a link slug only (primary) — [Haus blog](https://haus.io/blog/haus-announces-20m-raise-led-by-01-advisors). **[UPDATES AU5/AB11: the "USD 20M raise" is dated July 2024.]** No 2025-2026 round was found in the searches run.
- Mutinex (Australia, GrowthOS MMM): $17.5M on 2024-10-10, led by Marbruck Investments with EVP and Archangel Ventures. Valuation $132.5M, up from $75M. Claims more than $2B of marketing spend under management (second-hand) — [Business News Australia](https://direct.businessnewsaustralia.com/articles/marketing-analytics-scale-up-mutinex-raises--17-5m--boosting-valuation-to--132-5m.html)
- Recast: $3.4M raise (second-hand, headline only; date not confirmed) — [citybiz](https://www.citybiz.co/?p=360336)
- Braze acquired OfferFit (AI decisioning that replaces manual A/B tests) for $325M in 2025 (second-hand, competitor blog) — [Convert, 2026-03-25](https://www.convert.com/blog/a-b-testing/state-of-ab-testing-tools-2026/)

**D. Life sciences**
- Causaly (biomedical literature causal-relation graph): $60M Series B announced 2023-07-13, led by EBRD Venture Capital, with Index, ICONIQ, Pentech, Marathon, Visionaries Club, Emerge, and angels including Olivier Pomel (Datadog CEO). $83M total. Earlier rounds: Series A $17M (May 2021), $4.8M (Nov 2019), seed $1.2M (Jul 2018). Form D shows $52,999,948 of $60M sold, filed 2023-07-18 (second-hand aggregator citing Business Wire, VentureBeat and SEC EDGAR) — [Seedtable](https://seedtable.com/companies/causaly/funding-rounds/series-b-2023-07). No later round was found.
- Aitia (formerly GNS Healthcare): $65.25M total over 12 rounds. Latest is a corporate-minority round from Charles River Laboratories on 2023-11-13 (amount hidden). Earlier: MSD Global Health Innovation Fund (Series D-II, 2020-01-07), Celgene, Alexandria (second-hand) — [CB Insights](https://www.cbinsights.com/company/gns-healthcare/financials). Ono deal on 2 Sept 2026 is in AU5.
- Unlearn (digital twins / PROCOVA): $50M Series C on 2024-02-29, led by Altimeter, with Radical, Wittington, Mubadala, Epic, Necessary, Insight Partners, 8VC, DCVC and DCVC Bio. More than $130M raised in total. Customers are unnamed "leading global pharmaceutical companies" (primary, investor press release) — [DCVC](https://www.dcvc.com/press-releases/unlearn-raises-50-million-series-c-to-optimize-clinical-research-with-ai-powered-digital-twin-technology)
- Aetion: see M&A (section 3).

**E. Experimentation platforms** (all see M&A, section 3): Statsig, Eppo, Split, VWO/AB Tasty, SiteSpect, Optimizely, Intellimize.

**F. Open source with corporate backers**
- PyWhy: a GitHub organisation set up jointly by AWS and Microsoft, announced ~2022-06-28. DoWhy moved under it, and AWS contributed the GCM algorithms (second-hand) — [InfoQ](https://www.infoq.com/news/2022/06/dowhy-pywhy-aws-microsoft/); primary announcement found but not opened — [Microsoft Research blog](https://microsoft.com/research/blog/dowhy-evolves-to-independent-pywhy-model-to-help-causal-inference-grow)
- DoWhy as of 2026-10-13: 8.3k stars, 1.1k forks. The README names no commercial backer and does not mention the Linux Foundation (primary) — [GitHub](https://github.com/py-why/dowhy)
- CausalNex (McKinsey / QuantumBlack): **discontinued**. "As of 24th June 2026, CausalNex has reached end of life", with no further fixes or security patches; 2.5k stars (primary) — [GitHub](https://github.com/mckinsey/causalnex). **[NEW vs AU5]**
- Microsoft ShowWhy: archived 2025-12-17, "the result of research efforts that are no longer active". No successor named; 221 stars (primary) — [GitHub](https://github.com/microsoft/showwhy). Confirms AU5.
- Tetrad (CMU): no commercial backer was found in this pass. Not researched further (see Gaps).

### Inferences
- Unlike 2021-2022, the 2025-2026 money with a causal pitch went to LLM-agent companies that say "root cause" or "reasons over evidence", not to graph-discovery platforms. None of the funded AI SRE firms publishes a precision or recall method (Traversal's ">90%" has no method). This supports AU5 F3.
- The horizontal "causal AI platform" segment looks stalled. causaLens has no visible round since 2022 and has rebranded to agents; Geminos has no priced round; CausalNex and ShowWhy are dead. New entrants (Kausable, Causa) are seed or pre-seed.
- Causely's 2025-2026 moves (MCP server, Cursor plugin, A2A) turn it into a "causal context" supplier to other agents. That is the same slot an auditable causal-claims layer would occupy, so Causely is the most direct comparable.

### Gaps
- causaLens total funding and any post-2022 round: not found. Crunchbase and PitchBook were not fetched.
- Geminos, Xplain Data, Howso, Parabole.ai, Causality Link, Data Poem, Lifesight, INCRMNTAL, Recast: no reliable funding figures found in this pass. Searches returned only aggregator stubs.
- Haus: whether it raised in 2025-2026 is unverified.
- Tetrad funding (NIH / CMU grants) and EconML and CausalML stewardship were not checked.
- Kausable: the amount conflicts in the one source read.

## 2. Funding table (startups, latest known)

### Takeaway
Since 2024, AI SRE has far outraised pure causal AI. Resolve alone ($160M) exceeds every pure-play causal company's total. Among pure-play causal firms, the last priced rounds are causaLens $45M (2022), Causaly $60M (2023) and Causely $8.8M (2023).

### Cited Findings
| Company | Segment | Total raised | Last round (date, amount, lead) | Label / source |
|---|---|---|---|---|
| Resolve AI | AI SRE | >$150M (primary) / $160M (second-hand) | Series A, 2026-02-02, $125M, Lightspeed, $1B valuation | primary, [Resolve](https://resolve.ai/blog/series-a-funding) |
| incident.io | incident mgmt + AI | $100.7M | Series B, 2025-04-10, $62M, Insight/Index/Point Nine | second-hand, [CB Insights](https://www.cbinsights.com/company/incidentio/financials) |
| Causaly | life sci (literature K) | $83M | Series B, 2023-07-13, $60M, EBRD VC | second-hand, [Seedtable](https://seedtable.com/companies/causaly/funding-rounds/series-b-2023-07) |
| Aitia (GNS) | life sci (discovery) | $65.25M | corporate minority, 2023-11-13, undisclosed, Charles River Labs | second-hand, [CB Insights](https://www.cbinsights.com/company/gns-healthcare/financials) |
| Traversal | AI SRE ("causal ML") | $48M (primary) / $53M (second-hand) | Seed + A, ~June 2025, Sequoia + Kleiner Perkins | primary, [Traversal](https://traversal.com/blog/launch-announcement) |
| causaLens | enterprise causal AI → agents | ≥$45M (no total found) | Series A, ~Jan 2022, $45M, Dorilton + Molten | primary, [causaLens](https://causalens.com/causal-ai/startup-series-a-funding-round-45-million) |
| Unlearn | life sci (RCT design) | >$130M | Series C, 2024-02-29, $50M, Altimeter | primary, [DCVC](https://www.dcvc.com/press-releases/unlearn-raises-50-million-series-c-to-optimize-clinical-research-with-ai-powered-digital-twin-technology) |
| Haus | marketing incrementality | not stated (≥$37M if the $17M A is counted) | 2024-07-30, $20M, 01 Advisors | primary, [Haus](https://haus.io/blog/haus-announces-20m-raise-led-by-01-advisors) |
| NeuBird | AI SRE | not disclosed | ~2026-04-06, $19.3M, Xora Innovation | primary, [Business Wire](https://www.businesswire.com/news/home/20260406552258/en) |
| Mutinex | MMM | not stated | 2024-10-10, $17.5M, Marbruck, $132.5M valuation | second-hand, [BNA](https://direct.businessnewsaustralia.com/articles/marketing-analytics-scale-up-mutinex-raises--17-5m--boosting-valuation-to--132-5m.html) |
| Kausable | causal-structure AI | — | Seed, 2026-07-09, €12M or $13.8M (conflict), UVC + Entourage | second-hand, [Nordic9](https://nordic9.com/news/kausable-raises-12-million-in-a-seed-funding/) |
| Causely | causal RCA | >$11M (primary) / $10.8M (second-hand) | Seed, 2023-06-29, $8.8M, 645 Ventures | primary, [Causely](https://www.causely.ai/blog/causely-raises-8-8m-in-seed-funding-to-deliver-it-industrys-first-causal-ai-platform) |
| Cleric | AI SRE | $9.8M | Seed (Vertex Ventures US lead), announced ~2025-12-09 | primary, [Business Wire](https://businesswire.com/news/home/20251209625361/en/Cleric-Launches-the-First-Self-Learning-AI-SRE) |
| Geminos | enterprise causal AI | not disclosed | Incubator (Deere), 2024-01-24 | second-hand, [CB Insights](https://www.cbinsights.com/company/geminos-software/financials) |

### Inferences
- The AU5/AB11 "Haus $20M" investor signal belongs to mid-2024. The freshest causal-adjacent capital signals in 2026 are Resolve (Feb), NeuBird (Apr) and Kausable (Jul).

### Gaps
- Exact funding totals for causaLens, Haus, Traversal and NeuBird are not published in the sources read.
- Crunchbase and PitchBook were not fetched in this pass. CB Insights pages hide some rounds behind a paywall.

## 3. M&A since 2023 (with prices where reported)

### Takeaway
Every priced exit is in experimentation or decisioning, not "causal AI". Disclosed or reported prices: Statsig $1.1B (all-stock), OfferFit $325M, Eppo ~$220M (reported, unconfirmed), VWO ~$200M (PE majority stake). No pure-play causal-AI company has been acquired at a disclosed price. The biggest 2026 change is that Statsig's external product moved to Amplitude in May 2026, eight months after OpenAI bought it.

### Cited Findings
- **OpenAI acquired Statsig.** Announced 2025-09-02, all-stock, $1.1B. Founder Vijaye Raji became OpenAI's CTO of Applications, and Statsig was promised it would "continue operating independently". **On 2026-05-05 Amplitude announced it would take on Statsig's brand and customers**, keep the platform running, and reset pricing at each customer's renewal; the team stays at OpenAI (second-hand, competitor blog by Convert) — [Convert](https://convert.com/blog/a-b-testing/statsig-moves-to-amplitude/). **[UPDATES AU5]** The Amplitude press release itself was not opened.
- **Datadog acquired Eppo** for ~$220M, first reported by journalist Alex Konrad on X on 2025-05-01. The article does not say Datadog confirmed the price (second-hand) — [AIM Research](https://aimresearch.co/market-industry/datadog-enters-the-experimentation-space-with-220-million-eppo-deal); also [Seeking Alpha, headline only](https://seekingalpha.com/news/4439188-datadog-buying-startup-eppo-for-220m-report)
- **Datavant acquired Aetion.** Originally announced 2025-05-15; a re-run of the release is dated 2025-06-16; reported complete by 2025-07-13. Price and terms not disclosed (second-hand) — [Healthcare IT Today](https://www.healthcareittoday.com/2025/06/16/datavant-to-acquire-aetion-empowering-healthcare-and-life-sciences-organizations-to-generate-high-quality-scalable-real-world-evidence-from-connected-privacy-protected-data/); [Pulse 2.0](https://pulse2.com/datavant-acquisition-of-aetion-completed/). Aetion now sits in Datavant's Life Sciences division. **[UPDATES AU5 with the closing date]**
- **Harness acquired Split Software** (feature flags and experimentation). Definitive agreement announced 2024-05-29; price not disclosed. Split had raised more than $110M, including a $50M Series D in Aug 2021 (primary) — [Harness](https://harness.io/press-and-news/harness-acquires-split-software-to-enable-feature-flag-experimentation-in-software-workflows)
- **Braze acquired OfferFit** in 2025 for $325M ("autonomous decisioning in place of manual A/B tests") (second-hand, competitor) — [Convert](https://www.convert.com/blog/a-b-testing/state-of-ab-testing-tools-2026/)
- **Everstone Capital took a majority stake in Wingify (VWO)** in 2025 at ~$200M (second-hand). **VWO and AB Tasty merged in 2026** to form a company with more than $100M ARR; price not reported (second-hand) — [Convert](https://www.convert.com/blog/a-b-testing/state-of-ab-testing-tools-2026/)
- **Monetate acquired SiteSpect** in 2025 (a "$75M loan" is reported; signals of SiteSpect being deprecated are unconfirmed) (second-hand) — same source
- **Webflow acquired Intellimize** in 2024 for a reported "eight figures" (second-hand) — same source
- Caveat on the Convert source: Convert is an A/B-testing vendor competing with several of the companies listed.

### Inferences
- Acquirers are infrastructure platforms (OpenAI, Datadog, Harness, Braze, Amplitude, Datavant) folding causal or experimental measurement into a broader data or observability stack. Standalone measurement tools get absorbed rather than growing into large independent "causal" companies. A causal-claims layer is more likely to exit as a feature of an observability, experimentation or RWE platform than as a standalone company.
- The Statsig to Amplitude handoff shows a frontier-lab acquirer wanted the team and internal tooling, not the external customer business.

### Gaps
- Amplitude's own 2026-05-05 release, Statsig's prior funding, and the Eppo price confirmation in Datadog filings were not read.
- No disclosed acquisitions of causaLens, Geminos, Causely, Causaly or Xplain Data were found. Absence was not exhaustively verified.

## 4. Market-size reports for "causal AI"

### Takeaway
Published "causal AI" market sizes span three orders of magnitude for the same year: about $29M-63M (GMI, MarketsandMarkets 2024 edition, Roots/ResearchAndMarkets), $1.15B-1.8B (SkyQuest, Emergen) and $59B (Insight Partners). MarketsandMarkets revised its own 2023 base fivefold between editions ($8.0M to $41.3M). None publishes a reproducible method, a vendor list it sums over, or a definition that includes experimentation or MMM spend.

### Cited Findings
| Firm (published) | Base value | Forecast | CAGR | Method stated? | Label / source |
|---|---|---|---|---|---|
| MarketsandMarkets (2023-05-17 PR) | $8.01M (2023) | $119.5M (2030) | 47.1% | not in PR | second-hand (PR repost), [jotup](https://jotup.co/node/2403603) |
| MarketsandMarkets (Dec 2024) | $41.34M (2023); $56.24M (2024) | $456.88M (2030) | 41.8% (2024-30) | top-down + bottom-up, triangulation, supply- and demand-side interviews (number of interviews not stated). BFSI is the largest vertical, financial management the largest application, North America 38.92% | primary (analyst claim), [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/causal-ai-market-162494083.html) |
| Global Market Insights (Jul 2024, GMI10231) | $28.9M (2023) | ~$600M (2032) | "over 40%" / 41% (2024-32) | claims ~80% primary interviews and a bottom-up build from company revenue; healthcare fastest-growing (>44%); NA >35% | primary (analyst claim), [GMI](https://gminsights.com/industry-analysis/causal-ai-market) |
| Roots Analysis (updated May 2025); resold by ResearchAndMarkets (~2025-10-10) | $63.37M (2025) | $1,628.43M (2035) | 38.35% | generic "systematic methodology", three scenarios | primary (analyst claim), [Roots](https://www.rootsanalysis.com/causal-ai-market); second-hand, [Business Wire](https://www.businesswire.com/news/home/20251010801077/en) |
| theCUBE Research (2025-03-15) | — | >$1B (2030) | 41% | not read | second-hand, already in AU5 |
| Emergen Research (2025-10-03, modified 2026-05-13) | $1.8B (2024) | $12.4B (2034) | 21.3% | generic only; the meta description contradicts the body ("$12.4B in 2024") | primary (analyst claim), [Emergen](https://www.emergenresearch.com/industry-report/causal-ai-market) |
| SkyQuest (via GII Korea; no date, stamp "26.05.11") | $1.15B (2024); $1.59B (2025) | $21.4B (2033) | 38.4% (2026-33) | top-down + bottom-up, interviews | second-hand (reseller), [GII Korea](https://www.giikorea.co.kr/report/sky2026331-causal-ai-market-size-share-growth-analysis-by.html) |
| The Insight Partners (2026-07-28) | **US$59.22 billion (2025)** | **US$1,069.71B (2034)** | 37.93% (2026-34) | "proprietary research, government publications, company annual reports", interviews. The TOC confirms units are "US$ Billion" | primary (analyst claim), [Insight Partners](https://www.theinsightpartners.com/reports/causal-ai-market); [TOC](https://www.theinsightpartners.com/reports/toc/causal-ai-market) |

- Gartner: causaLens says causal AI was included in Gartner's **2023 Hype Cycle for Emerging Technologies**, with an accompanying deep-dive report. Phase and time-to-plateau are not stated on that page (vendor claim, undated blog) — [causaLens](https://causalens.com/resources/blog/gartner-lists-causal-ai-as-a-flagship-emerging-technology). A 2025-08-01 news summary of the **2025 Hype Cycle for AI** does not mention causal AI (second-hand) — [Security World Market](https://www.securityworldmarket.com/int/News/Business-News/the-hype-cycle-for-ai-now-goes-beyond-gen-ai). Gartner's 2025 China D&A Hype Cycle abstract is paywalled, and causal AI's position there is unknown — [Gartner](https://www.gartner.com/en/documents/6654634)

### Inferences
- **Conflicts:**
  - (a) 2024-2025 base values differ by about 1,000x ($56M MarketsandMarkets vs $59B Insight Partners).
  - (b) MarketsandMarkets' own 2023 base moved from $8.0M (2023 edition) to $41.3M (2024 edition) with no stated restatement.
  - (c) CAGRs cluster suspiciously at 38-47% across firms whose bases differ by orders of magnitude, except Emergen at 21%.
  - (d) "Key player" lists range from real vendors (MarketsandMarkets, Roots) to generic big tech with no causal product (GMI: Dropbox, Pinterest, Snap). The billion-dollar figures must therefore count AI spend that is merely labelled causal.
- The only estimate that comes near a defensible bottom-up check is the MarketsandMarkets/GMI/Roots tens-of-millions range. It is in the same order as a handful of vendors with ~$100k-£240k ACVs (AB11). For a capstone, cite it as "~$30-60M in 2023-2025, per MarketsandMarkets / GMI / Roots, methods paywalled" and state that the $1B+ figures are not comparable.
- All definitions exclude experimentation (Statsig $1.1B alone) and MMM/incrementality. The money paying for "causal" answers is therefore mostly outside the "causal AI market" as sized.

### Gaps
- No full methodology section was read; all reports are paywalled.
- Fortune Business Insights, Precedence, Market.us, MarketIntelo and Mordor were not opened. MarketIntelo appeared in search but was not fetched.
- Gartner's current (2025/2026) Hype Cycle position for causal AI could not be verified (paywalled).

## 5. Platform churn: shut down, archived, repositioned

### Takeaway
Since late 2025, the three best-known general-purpose causal-discovery or causal-modelling tools from large sponsors have all exited or pivoted: ShowWhy archived (Dec 2025), CausalNex end-of-life (Jun 2026), causaLens decisionOS dropped for LLM "Digital Workers". In experimentation, churn takes the form of consolidation (Statsig to OpenAI to Amplitude; VWO + AB Tasty) rather than shutdowns.

### Cited Findings
- Microsoft ShowWhy: archived 2025-12-17. "Research efforts that are no longer active"; no reason given beyond that and no successor (primary) — [GitHub](https://github.com/microsoft/showwhy)
- McKinsey/QuantumBlack CausalNex: end of life 2026-06-24. No updates, fixes or security patches; issues and PRs no longer monitored. No reason stated (primary) — [GitHub](https://github.com/mckinsey/causalnex)
- causaLens: the decisionOS name is absent from the homepage on 2026-10-13. The product is now LLM "Digital Workers" with a "System of Work" governance layer that has audit trails and evaluation, and causality is kept only as a reasoning claim (primary) — [causalens.com](https://causalens.com/). No public statement explaining the pivot was found.
- Causely: kept "causal reasoning engine" but repackaged it as context for third-party agents (MCP, Cursor, A2A, 2025-2026) (primary) — [Causely blog](https://www.causely.ai/blog)
- Statsig: OpenAI's Sept 2025 promise of independent operation was "retired"; customers moved to Amplitude (announced 2026-05-05) (second-hand) — [Convert](https://convert.com/blog/a-b-testing/statsig-moves-to-amplitude/)
- Google Optimize (experimentation) was shut down in 2023 with no replacement (second-hand) — [Convert](https://www.convert.com/blog/a-b-testing/state-of-ab-testing-tools-2026/)

### Inferences
- Common pattern: standalone causal-discovery UIs or libraries with no revenue owner are being retired, while survivors attach "causal" to LLM agents (causaLens, Causely, Traversal). A product pitched as "auditable causal claims for LLM agents" fits where the survivors are heading. Graph discovery alone has no surviving commercial home among the tools checked.
- "Why" is mostly unstated. The only stated reasons are "research efforts no longer active" (ShowWhy) and unexplained EOL (CausalNex). Any "lack of demand" explanation is inference, not a sourced fact.

### Gaps
- No primary statement from causaLens explaining the move from decisionOS to Digital Workers was found.
- Whether Microsoft's Causica, EconML or Uber CausalML changed status in 2026 was not checked in this pass. AU5 notes Causica had "no releases".

## 6. Which buyer types appear most in public case studies

### Takeaway
In the named-customer evidence gathered here, the most common buyers are tech-native platform and SRE teams (AI SRE vendors), then pharma or biotech R&D and RWE (Causaly, Aitia, Unlearn, Aetion), then DTC and consumer brands and agencies (Haus, causaLens 2026). Financial services appears as named early causaLens customers (Aviva, TIAA, 2022) and as MarketsandMarkets' "largest vertical", but not among the 2025-2026 AI SRE logos except MSCI, Coinbase and unnamed Fortune 100 banks.

### Cited Findings
- AI SRE customer logos:
  - Resolve: Coinbase, DoorDash, MongoDB, MSCI, Salesforce, Zscaler — [Resolve](https://resolve.ai/blog/series-a-funding)
  - Traversal: DigitalOcean, Eventbrite, Cloudways, plus Fortune 100 financial institutions — [Traversal](https://traversal.com/blog/launch-announcement)
  - Cleric: BlaBlaCar — [Business Wire](https://businesswire.com/news/home/20251209625361/en/Cleric-Launches-the-First-Self-Learning-AI-SRE)
  - All primary
- causaLens: Aviva and TIAA in 2022, all financial — [causaLens](https://causalens.com/causal-ai/startup-series-a-funding-round-45-million). In 2026: J&J, Syneos Health (life sciences), McCann Worldgroup and Croud (marketing agencies), Cisco, DANA Indonesia (fintech) — [causalens.com](https://causalens.com/). Primary.
- Haus: StockX and OluKai (consumer/DTC) (primary) — [Haus](https://haus.io/blog/haus-announces-20m-raise-led-by-01-advisors)
- Life sciences: Unlearn serves pharma sponsors, biotechs and academia — [DCVC](https://www.dcvc.com/press-releases/unlearn-raises-50-million-series-c-to-optimize-clinical-research-with-ai-powered-digital-twin-technology). Aetion serves biopharma, device makers, payers and regulators — [Healthcare IT Today](https://www.healthcareittoday.com/2025/06/16/datavant-to-acquire-aetion-empowering-healthcare-and-life-sciences-organizations-to-generate-high-quality-scalable-real-world-evidence-from-connected-privacy-protected-data/)
- Analyst view: MarketsandMarkets names BFSI as the largest vertical and marketing & pricing as the fastest-growing application (analyst claim) — [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/causal-ai-market-162494083.html). GMI names healthcare as fastest-growing (analyst claim) — [GMI](https://gminsights.com/industry-analysis/causal-ai-market)

### Inferences
- Buyer frequency in public logos: tech-platform SRE ≥ pharma/RWE > consumer marketing > finance. The analyst "BFSI largest" claim is not reflected in recent public logos. It may reflect causaLens's early hedge-fund and asset-manager focus ([Hedgeweek headline, not opened](https://hedgeweek.com/prominent-hedge-funds-among-finance-leaders-deploy-causalens-causal-ai-platform)).
- The two buyer types with both recent money and logos (SRE teams at tech companies, pharma R&D/RWE) map to AU5's angles #2 and #3. For a name-reliance audit service, the natural first customers are the AI SRE vendors themselves (Resolve, Traversal, Cleric, NeuBird, Causely) and the buyers comparing them. None publishes method-backed accuracy, and AU5 F3 already found no vendor publishes precision or recall.

### Gaps
- Logos are a biased sample (vendors choose them). No independent customer survey by segment was found.
- No case studies were read for Geminos, Xplain Data or Parabole in this pass. AU5 has rail (Geminos) and manufacturing (Xplain: Schaeffler, TRUMPF) second-hand.
