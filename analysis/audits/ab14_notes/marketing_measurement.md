# Marketing measurement (MMM, incrementality/geo experiments, attribution) as a vertical for an auditable causal-claims layer — as of 13 Oct 2026

Scope note: extends AU5 (F1, F5, F6, rows C19–C26) and AB11 (pricing). Facts already established there are **not** re-researched; they are reused with the pointer "(AU5)" / "(AB11)". All web sources below were opened on 2026-10-13 unless marked "search snippet only".
Labels: **primary** = the originating organisation's own page/release/data; **second-hand** = news, aggregator, analyst summary, or a figure quoted by someone else; **vendor claim** = a measurement vendor's statement about itself or its own survey. Arithmetic is marked **(arith.)** and any number built on assumptions is marked **estimate**.

Carried over (not re-fetched):
- Haus median ACV USD 150k (range 132k–168k), redline ~USD 100k, no list price — second-hand (Vendr), AB11.
- Recast: no list price; costbench median USD 6k/yr from 3 reports, inconsistent with its own USD 5k–50k/month band — second-hand, AB11. Do not use for sizing.
- Lifesight: one annual subscription priced by "maturity"; Mutinex: demo only, no price — primary, AB11.
- Meridian and Robyn free/open source; Robyn calls itself "experimental" — AU5.
- MMM failure case: simulated paid-search ROAS 10.61x vs true 4.20x, 90% interval excluded truth; experiment-based estimate 4.14x — second-hand of arXiv 2608.21128, AU5 F6.
- Recast "95%+ holdout accuracy", weekly backtests visible to clients — vendor claim, AU5.

---

## Q1. Market size for MMM / marketing measurement / attribution software and services (2024–2026)

### Takeaway
Published sizings disagree by definition, not just by number: "MMM software" is sized at ~USD 2.0–2.2B globally for 2025–2026 (Mordor), "marketing attribution software" at USD 3.1B already in 2021 (Allied, a 2022 report), and "causal AI" at only USD 56M for 2024 (MarketsandMarkets, AU5). None of these methodologies was read; treat all as second-hand, order-of-magnitude anchors. The MMM slice is the one that maps to the product idea.

### Cited Findings
- **MMM software, global (Mordor Intelligence; page last updated 11 Sep 2026; second-hand, paid report, methodology not read):** USD 1.96B (2025), USD 2.23B (2026), USD 4.22B (2031), CAGR 13.61% 2026–2031. 2025 splits: software 76.18% (services growing faster, 15.77% CAGR); cloud 79.61%; large enterprises 68.43%; North America 34.61%; CPG the largest end-user at 24.65%. Named players: Nielsen, Kantar, Circana, Analytic Partners, Measured. Definition: "data analytics solutions that help enterprises measure the impact of marketing activities". — [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/marketing-mix-modeling-software-market)
- **Marketing attribution software, global (Allied Market Research; report year shown as 2022; second-hand):** USD 3.1B in 2021, forecast USD 12.9B by 2031, CAGR 15.5% (2022–2031). Key players listed are Adobe, Alphabet, HubSpot, Merkle, Oracle, SAP, Nielsen, Ruler Analytics, Windsor.ai, Wizaly. These are mostly general martech, so the definition is broad. — [Allied Market Research](https://alliedmarketresearch.com/press-release/marketing-attribution-software-market.html)
- **Causal AI category (MarketsandMarkets, Dec 2024; second-hand):** USD 56.2M (2024) → USD 456.8M (2030). It excludes experimentation and MMM. — AU5 §(3)
- **Conflict/definition note.** The attribution figure (2021) exceeds the MMM figure (2025) even though MMM spending has grown since. This is consistent with "attribution" sizings including web-analytics and martech suites. The figures cannot be summed, since the categories overlap (vendors such as Northbeam, Lifesight, Haus and Rockerbox sell MTA, MMM and experiments together). — inference from the two pages above.
- **Gartner treats MMM as its own category.** Gartner published a "Magic Quadrant for Marketing Mix Modeling Solutions" in 2025. TransUnion's release says it was named a Leader "for the second consecutive year", so the first edition was 2024. Analytic Partners and Ipsos MMA also announced Leader placements. Number of vendors evaluated: not stated in the releases read. — [TransUnion via The Wise Marketer, 19 Nov 2025 (vendor claim)](https://thewisemarketer.com/transunion-named-a-leader-in-the-2025-gartner-magic-quadrant-for-marketing-mix-modeling-solutions/); [Analytic Partners newsroom (vendor claim)](https://analyticpartners.com/knowledge-hub/newsroom/analytic-partners-leader-in-2025-gartner-magic-quadrant-for-marketing-mix-modeling/); [Ipsos MMA (search snippet only)](https://technologymagazine.com/globenewswire/3185714)
- **Forrester Wave.** Analytic Partners states it was recognised in "The Forrester Wave™ for Q1 2026" (category name not given on the page read). — [Analytic Partners, Analyx release (vendor claim)](https://analyticpartners.com/newsroom/analytic-partners-acquires-analyx/)
- **Deal-value anchors in adjacent measurement:**
  - DoubleVerify agreed to acquire Rockerbox (multi-touch attribution) for USD 85M all-cash, announced 26 Feb 2025; Rockerbox had ~50 employees and was "relatively bootstrapped". — [Axios, 26 Feb 2025 (second-hand)](https://www.axios.com/2025/02/26/doubleverify-acquire-rockerbox-85-million)
  - Experimentation platforms: Statsig (USD 1.1B, OpenAI, Sept 2025) and Eppo (~USD 220M reported, Datadog, May 2025). — AU5 F1

### Inferences
- For a one-page brief, the defensible top-down anchor is: **"MMM software and services ≈ USD 2.2B globally in 2026, about USD 0.77B of it in North America"** (estimate: 2.23 × 0.3461 = 0.772, arith.; both inputs from a second-hand paid report). Attribution-software figures should be cited only as an upper, definitionally broader bound.
- A Gartner MQ for MMM (2024, 2025) is itself a demand signal: Gartner creates MQs where enterprise buyers run RFPs. Use it as a procurement-category signal, not as a size.

### Gaps
- Methodologies of Mordor and Allied were not read (paywalled). Marketintelo, TrendX and GII MMM reports appeared in search results but were **not opened**.
- No US-only figure for MMM services (econometrics consultancies such as Nielsen, Ipsos MMA, Analytic Partners) separate from software.
- No 2024 Mordor figure on the page read.
- Gartner MQ 2025 full text (vendor list, market definition, adoption predictions) is paywalled and was not read.

---

## Q2. Bottom-up inputs: buyer counts, measurement share of ad spend, ad-spend totals

### Takeaway
No public source counts US advertisers by annual media-spend band (USD 1M / 10M / 50M). The bottom-up therefore has to be built from proxies: firm counts by revenue, Gartner's marketing-to-revenue ratio, vendor survey sampling frames, and the top-down MMM figure. On those proxies, the US serviceable buyer pool for an MMM-plus-experiments audit layer is plausibly **low thousands of advertisers** (estimate), and measurement software is roughly **0.2–0.5% of digital ad spend** (estimate, cross-source).

### Cited Findings
**Ad-spend totals**
- **US 2026 growth (IAB, 2026 Outlook Study September Update, 10 Sep 2026; primary):** US ad spend forecast +12.3% YoY, raised from +9.5% in January. By channel: social +16.5%, CTV +15.6%, commerce media +13.6%, digital video excl. CTV +9.4%, podcasts +8.7%, paid search +8.1%, DOOH +7.0%, linear TV −1.5%. Based on "more than 200 brand and agency ad investment decision-makers". No dollar total on the page. — [IAB](https://www.iab.com/news/iab-raises-2026-u-s-ad-spend-forecast/)
- **US digital ad spend, dollar figure (EMARKETER, 7 Nov 2022 forecast; second-hand and stale):** "In 2026, digital ad spending will reach $385.47 billion and make up 80.9% of total media ad spend." This is a 2022 forecast and has not been checked against EMARKETER's current forecast (paywalled). — [EMARKETER](https://www.emarketer.com/content/digital-us-media-ad-spend)
- **US 2026 growth rates (EMARKETER, 16 Jan 2026; second-hand):** EMARKETER forecasts US digital ad spend +7.9% in 2026. Winterberry projects US "advertising, marketing, and data spending" at USD 664.2B in 2026 (+9.4%), with online marketing at 65.1% of total spend in 2025. — [EMARKETER](https://www.emarketer.com/content/us-ad-spending-growth-normalizes-digital-maturity-sets)
- **Global (WPP Media "This Year Next Year", 10 Dec 2025; primary):** global ad revenue USD 1.14T in 2025 (+8.8% excl. US political); +7.1% forecast for 2026. "Social and digital platforms" USD 413.0B (2025) → USD 445.4B (2026). "Intelligence (mostly search)" USD 244.9B (21.4%). — [WPP Media](https://www.wppmedia.com/news/campaigns-report-this-year-next-year-december-2025)
- **Conflict.** The IAB (+12.3%) and EMARKETER (+7.9% digital) 2026 US growth figures differ in scope (IAB covers all media and was updated Sept 2026; EMARKETER covers digital and dates from Jan 2026). EMARKETER's own coverage of the IAB update is titled "IAB raises ad spending forecast for 2026, but marketers should brace for 2027 slowdown" (search snippet only, not opened). — [EMARKETER](https://www.emarketer.com/content/iab-raises-ad-spending-forecast-2026-marketers-should-brace-2027-slowdown)

**Budget ratios**
- **Gartner 2026 CMO Spend Survey (11 May 2026; primary):** marketing budgets 7.8% of company revenue in 2026, up from 7.7% in 2025. Fielded Jan–Mar 2026; n = 401 CMOs in North America, UK and Europe, "vast majority" above USD 1B revenue. 15.3% of marketing budget goes to AI; 56% of CMOs lack the budget to deliver their 2026 strategy. The release gives no split by paid media, martech or agencies. — [Gartner](https://gartner.com/en/newsroom/press-releases/2026-05-11-gartner-2026-cmo-spend-survey-finds-cmos-allocate-15-point-3-percent-of-marketing-budgets-to-ai-but-only-30-percent-are-ready-to-scale-ai-capabilities)

**Firm counts and sampling frames (proxies for advertiser counts)**
- **Middle market (NCMM, Mid-Year 2025 Middle Market Indicator, via ABF Journal 6 Aug 2026; second-hand):** "nearly 200,000 U.S. middle market businesses" with annual revenue of USD 10M–1B. No count of firms above USD 1B was on the page. — [ABF Journal](https://www.abfjournal.com/the-200000-company-landscape-where-institutional-capital-still-falls-short-in-the-u-s-middle-market/)
- **Survey frames that define the buyer:**
  - Haus's 2026 index sampled decision-makers at organisations with **≥ USD 11M paid media budget**. — [EMARKETER on Haus index, 19 May 2026](https://www.emarketer.com/content/incrementality-testing-earns-marketers--top-trust)
  - Perion / Advertiser Perceptions sampled organisations spending **≥ USD 1M/yr on advertising**. — [MarketScale summary of Marketing Dive, Nov 2025](https://www.marketscale.com/industries/marketing-tech/only-22-of-marketers-feel-sure-they-can-justify-spend-to-the-cfo.md)
  - A Jan 2025 Google-cited survey used **> USD 500k annual ad spend**. — [PPC Land, 13 Nov 2025](https://ppc.land/google-lowers-incrementality-testing-threshold-to-5-000-for-advertisers/)

**Spend under measurement (vendor claims)**
- Lifesight: 500+ brands managing over USD 4B in marketing spend (June 2026). — [PPC Land](https://ppc.land/lifesight-mcp-puts-live-marketing-measurement-inside-claude-and-chatgpt/)
- Mutinex GrowthOS: manages more than USD 2B of marketing investment (Oct 2024). — [Business News Australia](https://www.businessnewsaustralia.com/articles/marketing-analytics-scale-up-mutinex-raises--17-5m--boosting-valuation-to--132-5m.html)
- Analyx (now Analytic Partners): customers analysed USD 5B of spend in the 12 months before Jan 2025. — [Analytic Partners](https://analyticpartners.com/newsroom/analytic-partners-acquires-analyx/)
- Measured: over 120 DTC brands and USD 4.14B ad spend tested (May 2022). — [Pulse 2.0](https://pulse2.com/media-investment-measurement-platform-company-measured-raises-21-million/amp/)

**Experiment frequency and cost**
- Google cut the minimum budget for Conversion Lift incrementality experiments from thresholds "approaching $100,000" to USD 5,000 (announced 11 Nov 2025). Per Google's historical data, "most advertisers conduct approximately one to two incrementality studies annually". — [PPC Land, 13 Nov 2025 (second-hand of Google)](https://ppc.land/google-lowers-incrementality-testing-threshold-to-5-000-for-advertisers/)
- Recast likewise says lift tests are expensive, so brands run only "one or two tests a year". — [Recast blog, 23 Aug 2023 (vendor claim)](https://getrecast.com/how-do-lift-tests-fit-in-with-mmm)

### Inferences (all **estimate**; inputs shown)
1. **Average spend per measured brand.** Lifesight USD 4B ÷ 500 brands ≈ **USD 8M per brand** (arith., vendor inputs). Mid-market MMM buyers are therefore in the USD 1–50M media band, not only the Fortune 500.
2. **Revenue threshold for a USD 10M marketing budget.** At 7.8% of revenue (Gartner), a USD 10M budget implies ≈ USD 128M revenue (10 / 0.078, arith.). Gartner's sample is mostly >USD 1B, so the ratio may not hold mid-market. Paid media is only part of the marketing budget, and no sourced paid-media share was found, so USD 10M of **media** implies a higher revenue threshold.
3. **Top-down-implied buyer count.** North America MMM ≈ USD 0.772B (Q1) ÷ Haus median ACV USD 0.15M ≈ **~5,100 contract-equivalents** (arith.). This overstates enterprise buyers, because services, cheaper tools and multi-vendor buyers are mixed in. Use it as a ceiling-type check.
4. **Implied Haus customer count.** GetLatka's USD 36.6M estimated ARR (Sept 2025, see Q3) ÷ USD 150k ≈ **~240 customers** (arith.). Both inputs are second-hand estimates.
5. **Measurement share of ad spend (no direct source found).**
   - Global: MMM software USD 2.23B ÷ WPP "social and digital platforms" USD 445.4B (2026) ≈ **0.50%**.
   - North America: USD 0.772B ÷ EMARKETER's (stale) US digital USD 385.47B (2026) ≈ **0.20%**.
   - Per customer: Haus USD 150k ACV ÷ USD 11M minimum media in Haus's survey frame ≈ **≤1.4%** of media for a measurement contract at the frame's floor.
   - All three mix sources and definitions; report as a range, **~0.2–1.4%** (estimate).
6. **Bottom-up for the audit layer** (structure plus two scenarios; counts are assumptions, not sourced):
   - Formula: revenue = N (US advertisers running MMM plus ≥1 experiment/yr) × adoption × price.
   - **N = 2,000–6,000.** Assumption, triangulated from point 3 (~5,100 contract-equivalents) and from Google's statement that experimenters run 1–2 studies/yr. Not a sourced count.
   - **Price = USD 30k–75k/yr.** Assumption: 20–50% of Haus's USD 150k median ACV, i.e. an add-on rather than a replacement. Northbeam's public attribution pricing (USD 18k–42k/yr starting rates, Q3) sets the floor.
   - **Adoption at maturity = 5–15%.** Assumption.
   - Serviceable market, N × price = **USD 60M** (2,000 × 30k) to **USD 450M** (6,000 × 75k). Estimate.
   - Obtainable market, N × adoption × price = **USD 3M** (2,000 × 5% × 30k) to **USD 67.5M** (6,000 × 15% × 75k). Estimate.
   - Cross-check: USD 450M is 58% of the USD 0.77B North American MMM market, so the high scenario is aggressive for an add-on. A realistic serviceable ceiling is probably **≤ 10–20% of the MMM spend it audits, i.e. ~USD 75–155M in North America** (0.1–0.2 × 0.772B; estimate).
7. **Channel multiplier.** 51 Meridian partners (Q4) × an assumed 10–40 Meridian clients each ≈ **~500–2,000 advertisers** reachable through one certified-partner channel (estimate; clients per partner is an assumption).

### Gaps
- **No source found for counts of US advertisers above USD 1M / 10M / 50M of annual media spend.** MediaRadar/Vivvix, Pathmatics and Winmo hold this data behind paywalls; nothing public was found. This is the biggest hole in the bottom-up. The best fix is a MediaRadar/Vivvix export or an ANA membership count.
- No count of US firms above USD 1B revenue was sourced in this pass.
- No source states the share of ad spend or marketing budget that goes to measurement or analytics. Gartner's release does not split martech; the full CMO Spend Survey report is paywalled.
- EMARKETER's current (2026) dollar forecast for US and global digital ad spend is paywalled. Only the stale Nov 2022 forecast and growth rates were available. IAB's September 2026 release gives growth only, not dollars.

---

## Q3. Vendor landscape and pricing, 2025–2026

### Takeaway
The category splits into four groups:
1. Experiment-first startups (Haus, Measured) priced at ~USD 100–170k ACV (Haus, second-hand).
2. Bayesian-MMM SaaS (Recast, Mutinex, Prescient, Lifesight) with no public prices.
3. Legacy econometrics consultancies and data owners (Nielsen, Analytic Partners, Ipsos MMA, TransUnion, Circana, NIQ, Kantar) that lead the Gartner MQ.
4. Attribution-first DTC tools (Northbeam, Rockerbox → DoubleVerify) with public mid-market prices of USD 1.5–3.5k/month.

Free Meridian and Robyn set a zero-price floor for the model itself, so vendors monetise data plumbing, experiments and services. Disclosed funding is modest: Haus ~USD 62M total (aggregator) is the largest disclosed among the startups.

### Cited Findings
| Vendor | Positioning | Price points (label, date) | Funding (label, date) | Customers / scale (label) |
|---|---|---|---|---|
| **Haus** | Geo experiments + "Causal MMM"/Causal Attribution | Median ACV USD 150k (132–168k), redline ~100k (second-hand, Vendr; AB11) | Series A USD 17M led by Insight Partners, 3 Aug 2023; USD 20M led by 01 Advisors (Oct 2024, MoFo release dated 24-10-24, search snippet); aggregator total **USD 61.65M over 6 rounds**, latest "Series A-3 USD 18.3M" (undated); valuation **USD 435.72M as of 18 Apr 2025** (second-hand, [StockAnalysis](https://stockanalysis.com/private/haus/)) | Named: Sonos, Paramount, Intuit, Dr. Squatch ([StockAnalysis](https://stockanalysis.com/private/haus/)); **est. ARR USD 36.6M, 283 employees (Sept 2025)** (second-hand estimate, [GetLatka](https://getlatka.com/companies/haus.io)) |
| **Recast** (getrecast.com) | Bayesian MMM, lift tests as time-local priors | No list price; costbench inconsistent (AB11) | Seed **USD 3.4M led by Lerer Hippeau**, total USD 4.5M ([AlleyWatch, ~Dec 2022, second-hand](https://alleywatch.com/2022/12/recast-marketing-mix-modeling-analytics-forecasting-platform-omnichannel-holistic-ad-spend-data-science-michael-kaminsky/)); later rounds not found | Named: Away, Harry's, Masterclass, Rocket Money (2022). SaaS subscription |
| **Measured** | Incrementality experiments + MMM | Not public | **USD 21M from Telescope Partners, May 2022** ([Pulse 2.0, second-hand](https://pulse2.com/media-investment-measurement-platform-company-measured-raises-21-million/amp/)) | 120+ DTC brands, USD 4.14B spend tested (2022, vendor claim); Mordor lists it as a key player |
| **Mutinex** (Sydney) | GrowthOS MMM SaaS | Demo only (AB11) | **USD 17.5M led by Marbruck, valuation USD 132.5M, 10 Oct 2024** (currency unstated, likely AUD) ([Business News Australia](https://www.businessnewsaustralia.com/articles/marketing-analytics-scale-up-mutinex-raises--17-5m--boosting-valuation-to--132-5m.html)); EVP invested ~USD 19M over two years | GrowthOS manages >USD 2B of marketing investment (vendor claim); US expansion |
| **Lifesight** | Unified MMM + geo incrementality + incrementality-adjusted attribution; MCP connector | Annual subscription by "maturity" (AB11) | CB Insights shows only a **USD 1.5M seed, 25 May 2018** (Provident Capital Partners) ([CB Insights, second-hand](https://www.cbinsights.com/company/lifesight/financials)); may be incomplete | **500+ brands, >USD 4B spend** (vendor claim, 2 Jun 2026) |
| **Prescient AI** | ML MMM for DTC/Amazon brands | Not found | **USD 10M Series A led by Headline and CEAS, 12 Mar 2024; USD 18M total** ([Refresh Miami, second-hand](https://refreshmiami.com/news/prescient-ai-raises-10m-series-a-to-help-ecommerce-brands-optimize-their-ad-spend/)) | Named: Good American, Eight Sleep, Cozy Earth; team 12 → 30 planned |
| **Northbeam** | MTA-first; MMM Plus and incrementality as add-ons; MCP on Growth tier | **Starter from USD 1,500/mo (<USD 1.5M/yr spend); Professional from USD 3,500/mo (up to USD 500k/mo spend); Growth and Enterprise custom; MMM Plus is an Enterprise add-on** (primary, [northbeam.io/pricing](https://www.northbeam.io/pricing), read 13 Oct 2026). Page conflict: Enterprise "more than $500k a month" on cards vs ">$250,000" in the FAQ. Costbench's "$5K/user/month, Feb 2026" is **not** supported by the vendor page ([costbench](https://costbench.com/changelog/northbeam-price-increase-2026-02/)) | USD 15M Series A, Aug 2022 ([BusinessWire, search snippet only](https://www.businesswire.com/news/home/20220816005159/en/Marketing-Intelligence-Platform-Northbeam-Raises-%2415-Million-Series-A-Funding)) | — |
| **Rockerbox** | MTA (+MMM, testing) | — | **Acquired by DoubleVerify for USD 85M cash, announced 26 Feb 2025**; previously "relatively bootstrapped" ([Axios](https://www.axios.com/2025/02/26/doubleverify-acquire-rockerbox-85-million)) | ~50 employees |
| **Analytic Partners** | Econometric "commercial analytics" (GPS-Enterprise) | Not public | Acquired **Analyx** (closed, 9 Jan 2025) and Magic Numbers (UK, 2024) ([Analytic Partners](https://analyticpartners.com/newsroom/analytic-partners-acquires-analyx/)) | "Fortune 500 brands"; Gartner MQ MMM Leader 2025; Forrester Wave Q1 2026 (vendor claims) |
| **Keen Decision Systems** | MMM/planning SaaS (CPG) | Not found | Series B, **undisclosed**, led by Ballast Point Ventures IV, 18 Aug 2022 ([PrivSource, second-hand](https://www.privsource.com/acquisitions/deal/0oSwAE)) | Not found |
| **Nielsen** | Legacy MMM / Nielsen ONE | Not found | Public-to-private (2022), not re-researched | Mordor key player |
| **TransUnion, Ipsos MMA** | MMM inside data companies | Not found | — | Gartner MQ MMM Leaders 2025 (vendor claims) |
| **Google Meridian** | Open-source Bayesian MMM; experiment results as priors; reach & frequency | Free | — | GA **29 Jan 2025**; "over 20" certified partners at launch; tested with "hundreds of brands" ([Google blog, primary](https://blog.google/products/ads-commerce/meridian-marketing-mix-model-open-to-everyone/?authuser=0)). Partner directory now lists **51** ([developers.google.com/meridian/partners](https://developers.google.com/meridian/partners), primary, undated) |
| **Meta Robyn** | Open-source MMM (R; Python port) | Free | — | "Experimental" (AU5). One 2026 page claims 4,200+ brands and 300+ contributors ([Presenc AI, May 2026](https://presenc.ai/research/open-source-mmm-frameworks-2026)) — **low reliability**: unsourced, and it describes Google's LightweightMMM as active without mentioning Meridian. Do not cite |

- **Other LLM / agent entrants in measurement** (named in June 2026 coverage): Adverity "MMM Agent for Google Meridian", Newton Research (with Snowflake), LiveRamp with Akkio, AppsFlyer, and Google, Amazon and Meta AI connectors. — [PPC Land, Jun 2026 (second-hand)](https://ppc.land/lifesight-mcp-puts-live-marketing-measurement-inside-claude-and-chatgpt/)
- **Google's own lift tests are now cheap.** The Conversion Lift minimum fell to USD 5k (Nov 2025). Platform-run experiments are therefore a growing, free evidence source next to paid geo tests. — [PPC Land](https://ppc.land/google-lowers-incrementality-testing-threshold-to-5-000-for-advertisers/)

### Inferences
- **Price ladder (estimate, from labelled points):** self-serve attribution USD 18–42k/yr (Northbeam, primary) → experiment/MMM platforms ~USD 100–170k/yr (Haus, second-hand) → consultancy MMM (Analytic Partners, Nielsen, Ipsos: unknown, likely higher, no source). An audit layer priced at USD 30–75k sits between the first two rungs.
- **Consolidation pressure.** Free Meridian/Robyn models, Google's USD 5k lift tests, a strategic exit for an attribution tool at USD 85M (Rockerbox), and roll-ups by Analytic Partners (Analyx, Magic Numbers) together suggest the model itself is commoditising. Value is moving to evidence (experiments), data plumbing and decision workflow. That favours a vendor-neutral evidence and audit layer, but the incumbents (Haus, Lifesight) already bundle the experiments.
- **Disclosed funding totals are small.** About USD 62M Haus, 18M Prescient, ≥21M Measured, ~4.5M Recast, ~17.5M Mutinex in the latest round. This is a services-heavy, mid-sized category, not a venture mega-category.

### Gaps
- No public or second-hand prices found for Nielsen, Analytic Partners, Keen, Measured, Prescient, Mutinex or Lifesight. Vendr pages for vendors other than Haus were not searched in this pass.
- Recast's post-2022 funding was not found. The search surfaced a different "Recast" (sports content, GBP 5.9M Series A), which must not be conflated.
- Measured's post-2022 status (later rounds or acquisition) was not verified.
- The Haus Oct 2024 round date comes from the MoFo URL slug (search snippet); haus.io/blog was not opened in this pass. Customer counts are not stated by any of these vendors except Lifesight (500+) and Measured (120+, 2022).
- The Meridian partner page shows no certification criteria and no date.

---

## Q4. Buyer and channel: who buys, from which budget line, and via whom

### Takeaway
The economic buyer is the senior marketing leader (CMO / VP Growth / Head of Performance). Marketing science and analytics leads are the technical evaluators, and finance is increasingly a co-signer or the audience. Measurement usually comes out of the marketing budget (martech, or agency/analytics services). Agencies and the 51 Meridian-certified partners (agency holding companies and specialist consultancies) are a primary route to market, because Meridian is free and someone has to run it.

### Cited Findings
- **Survey frames show who decides.**
  - Haus's 2026 index surveyed "US senior marketing, finance, and executive decision-makers" responsible for paid marketing at organisations with ≥ USD 11M paid media. Finance was explicitly part of the buyer frame. — [EMARKETER, 19 May 2026](https://www.emarketer.com/content/incrementality-testing-earns-marketers--top-trust) (vendor survey, second-hand)
  - In the Perion / Advertiser Perceptions study (fielded 28 Aug–10 Sep 2025, n = 167, ≥ USD 1M ad spend, 46% VP+), 36% were sole decision-makers, 50% decided with staff input, and 14% decided by committee. — [MarketScale summary](https://www.marketscale.com/industries/marketing-tech/only-22-of-marketers-feel-sure-they-can-justify-spend-to-the-cfo.md) (second-hand)
- **CMO role erosion moves the buyer.** The share of Fortune 500 firms with a CMO fell from 71% (2023) to 66% (2024) (Spencer Stuart via Fortune, June 2025). Buying authority is shifting to growth and revenue executives. — [same MarketScale summary](https://www.marketscale.com/industries/marketing-tech/only-22-of-marketers-feel-sure-they-can-justify-spend-to-the-cfo.md) (second-hand)
- **The budget is flat, which forces reallocation.** Marketing is 7.8% of revenue in 2026 (7.7% in 2025), and 56% of CMOs lack the budget for their strategy (Gartner, May 2026, primary). New tools must displace spend or prove savings. — [Gartner](https://gartner.com/en/newsroom/press-releases/2026-05-11-gartner-2026-cmo-spend-survey-finds-cmos-allocate-15-point-3-percent-of-marketing-budgets-to-ai-but-only-30-percent-are-ready-to-scale-ai-capabilities)
- **Agency and partner channel (Meridian directory, 51 partners; primary, undated):**
  - holding-company units: Publicis Media, YOTTA by Publicis, Digitas, Annalect (Omnicom), dentsu, Dentsu Digital, Merkle, KINESSO, GroupM Italy, Choreograph, Almap BBDO, CSA/Havas, Hakuhodo DY ONE
  - consultancies: Accenture, ZS, Ekimetrics, Artefact, fifty-five, Converteo, Analytic Edge, Monks, Brainlabs, Jellyfish, Tinuiti, Wpromote, Adswerve, Incubeta
  - data companies: NIQ, Circana
  - Four partners (Adswerve, Jellyfish, NIQ, Circana) are also listed for **GeoX** (Google geo experiments). — [Google Meridian partners](https://developers.google.com/meridian/partners)
- **Data-company MMM.** TransUnion (TruAudience) sells "unified, SaaS-based tools for advanced MMM, attribution, and experimentation" and stresses in-housing support. MMM is also bought as part of identity and data contracts. — [The Wise Marketer, Nov 2025](https://thewisemarketer.com/transunion-named-a-leader-in-the-2025-gartner-magic-quadrant-for-marketing-mix-modeling-solutions/) (vendor claim)
- **Mordor segment shares (2025, second-hand):** large enterprises hold 68.43% of MMM software spend; CPG is the largest vertical (24.65%); retail/e-commerce is fastest-growing (16.83% CAGR). — [Mordor](https://www.mordorintelligence.com/industry-reports/marketing-mix-modeling-software-market)
- **LLM front-ends widen the user base.** Lifesight's MCP "Skills Library" ships "Board Briefing" and "P&L Translator" workflows: outputs aimed at executives and finance, not analysts. — [PPC Land, Jun 2026](https://ppc.land/lifesight-mcp-puts-live-marketing-measurement-inside-claude-and-chatgpt/) (second-hand of vendor launch)

### Inferences
- **Who buys an audit layer.** It is a product for the **marketing science lead** (who owns MMM–experiment reconciliation), sold to the **CMO/VP Growth**, whose problem is credibility with **finance**. The CFO is the "reader" of the audit trail, not the budget holder. Its budget line would be measurement/martech (or analytics services, if delivered via an agency).
- **Fastest channel.** Meridian-certified partners and agencies, as a white-label "evidence grade" for the Meridian models they already deliver. Meridian accepts experiment priors natively, so tagging each channel's estimate as experiment-backed, prior-only or observational fit is a thin layer over an existing artefact. The 4 GeoX-certified partners are the natural first targets because they produce both kinds of evidence.
- **Secondary channel.** An integration or partnership with experiment vendors (Haus, Measured, Lifesight). This carries conflict-of-interest risk: they are the vendors whose claims the layer audits.

### Gaps
- No source quantifies who signs measurement contracts (marketing vs finance vs analytics) or which budget line they sit in. Gartner's full CMO spend breakdown (martech share) is paywalled.
- Meridian partners' client counts are not public. The "10–40 clients per partner" in Q2 is an assumption.
- Nothing was found on whether procurement or finance sign-off is required for MMM contracts.

---

## Q5. Demand signals for evidence, audit and calibration

### Takeaway
The demand evidence is unusually direct:
- Buyers trust experiments over MMM (60% vs 40%, vendor survey).
- Three in four buy-side leaders say measurement is underperforming (IAB 2026).
- 60% say internal stakeholders question their metrics.
- Only 22% strongly feel they can prove value to finance.
- Practitioners describe MMM–experiment conflicts, and also unreliable experiments, as routine.

Privacy pressure on attribution persists even though Chrome kept third-party cookies (April 2025) and Google retired the Privacy Sandbox APIs (Oct 2025). LLM front-ends (Lifesight MCP, Adverity's Meridian agent) are shipping with query audit logs but no claim-level evidence grading, and that is the gap.

### Cited Findings
**Trust in MMM vs experiments**
- **Haus 2026 Marketing Decision Confidence Index** (fielded Jan 2026, n = 500 US senior decision-makers with ≥ USD 11M paid media; vendor survey, reported by EMARKETER 19 May 2026):
  - 60% trust independent incrementality testing most, vs 40% MMM and 37% in-platform reporting.
  - 78% believe at least 10% of marketing spend is wasted through insufficient measurement; 7% put it at ≥30%.
  - — [EMARKETER](https://www.emarketer.com/content/incrementality-testing-earns-marketers--top-trust)
- **IAB & BWG Global, State of Data 2026 (2 Feb 2026):** 75% of US buy-side leaders say core measurement methods (attribution, incrementality tests, MMM) are underperforming, i.e. "not delivering the speed, accuracy, or trust they need". Second-hand via EMARKETER: the IAB PDF **failed to fetch** and the IAB landing page is a teaser. — [EMARKETER, 19 May 2026](https://www.emarketer.com/content/incrementality-testing-earns-marketers--top-trust); [EMARKETER FAQ, 3 Apr 2026](https://www.emarketer.com/content/faq-on-incrementality-how-prove-your-ads-actually-work-2026); [IAB teaser](https://iab.com/insights/2026-state-of-data-report/)
- **EMARKETER / TransUnion** (fielded July 2025, n = 196 US marketers; TransUnion release 21 Oct 2025, primary for the release; TransUnion sells MMM):
  - 47% plan to increase MMM spend.
  - 62% have "some confidence" in their metrics; 54% report no change in confidence YoY; 14% report a decline.
  - **60% say internal stakeholders question the validity of their metrics at least sometimes.**
  - For ~29% of respondents, up to 20% of the marketing budget was reallocated or put at risk over doubts about measurement accuracy.
  - 49% cite siloed or incomplete data as a top barrier.
  - — [TransUnion newsroom](https://newsroom.transunion.com/new-transunion-research-reveals-marketers-confidence-in-measurement-has-stalled/)
- **Same EMARKETER/TransUnion survey, as reported in EMARKETER's Apr 2026 FAQ:**
  - 52% use incrementality testing.
  - 27.6% rate MMM the most reliable methodology (vs MTA 19.4%, unified 18.9%).
  - 36.2% plan to increase incrementality spend.
  - EMARKETER uses 27.6% twice for different questions; verify before citing.
  - — [EMARKETER FAQ](https://www.emarketer.com/content/faq-on-incrementality-how-prove-your-ads-actually-work-2026)
- **Experiments are doubted too.** 44% question the reliability of incrementality results, the top barrier (Skai / Path to Purchase Institute, State of Retail Media, via EMARKETER). — [EMARKETER FAQ](https://www.emarketer.com/content/faq-on-incrementality-how-prove-your-ads-actually-work-2026) (second-hand)

**CFO / finance pressure**
- Only **22%** "strongly feel they have the data to prove marketing's value to finance" (Perion / Advertiser Perceptions, n = 167, Aug–Sep 2025; reported by Marketing Dive, Nov 2025). — [MarketScale summary](https://www.marketscale.com/industries/marketing-tech/only-22-of-marketers-feel-sure-they-can-justify-spend-to-the-cfo.md) (second-hand; the primary Perion report was not read)
- Flat budgets (7.8% of revenue) and 56% of CMOs short of budget (Gartner, May 2026). — [Gartner](https://gartner.com/en/newsroom/press-releases/2026-05-11-gartner-2026-cmo-spend-survey-finds-cmos-allocate-15-point-3-percent-of-marketing-budgets-to-ai-but-only-30-percent-are-ready-to-scale-ai-capabilities)

**MMM vs lift-test conflict (practitioner and vendor statements, labelled anecdotes)**
- Recast (vendor blog, 23 Aug 2023):
  - "when an MMM and a well-run experiment disagree… it's normally the MMM that's wrong".
  - Two lift tests on the same channel conflicting is "very common because channel performance changes over time".
  - Recast applies each test as a prior only for the window in which it ran. No conflict frequency is quantified.
  - — [Recast](https://getrecast.com/how-do-lift-tests-fit-in-with-mmm)
- Sellforte (vendor blog, 31 Aug 2026):
  - A Meta Conversion Lift test is credible only "for the audience, campaigns, conversion definition, and period it measured".
  - "A study of Meta sales campaigns should not silently become a precise prior for all paid social."
  - Overlapping studies should not be treated as "two fully independent observations".
  - The experiment's interval should become prior uncertainty rather than disappear.
  - A 2020 Meta conversion-lift issue "had affected some studies for about a year by undercounting reached conversions".
  - Advertisers cannot independently audit Meta's assignment.
  - — [Sellforte](https://sellforte.com/blog/asked-by-marketers/trust-meta-conversion-lift-tests)
- Haus's TikTok experiments found an extra 68% lift in the primary KPI that standard attribution missed (vendor claim via EMARKETER). Kroger Precision Marketing notes incremental ROAS runs below traditional ROAS. — [EMARKETER FAQ](https://www.emarketer.com/content/faq-on-incrementality-how-prove-your-ads-actually-work-2026)

**Privacy and signal loss**
- **Chrome.** On 22 Apr 2025 Google said it would keep third-party cookies in Chrome (no deprecation). It later confirmed the retirement of the remaining Privacy Sandbox APIs, including **Attribution Reporting**, Topics and Protected Audience (blog post around 17 Oct 2025; exact date inferred by the source). — [MarTech](https://martech.org/googles-privacy-sandbox-what-you-need-to-know/) (second-hand)
- **Apple ATT.** Industry-wide opt-in among users shown the prompt was 35% in Q2 2025 (34.5% Q2 2024; 34% Q2 2023). — [Adjust, 15 Jul 2025](https://www.adjust.com/blog/att-opt-in-rates-2025) (vendor data, primary for Adjust)
- **AI-driven journeys are a new measurement gap** (IAB, Sept 2026, primary):
  - 86% of buyers are changing, or expect to change, how they measure media within 12 months because of conversational AI and agents.
  - 45% cite difficulty comparing AI-driven and traditional journeys as their top challenge.
  - "increasing incrementality testing" is among the named responses.
  - — [IAB](https://www.iab.com/news/iab-raises-2026-u-s-ad-spend-forecast/)

**LLM front-ends and audit trails**
- **Lifesight MCP** (launched 2 Jun 2026): read-only MCP into Claude Desktop and ChatGPT, using OAuth with existing workspace permissions. **"Every request made through the connector is recorded in the customer's Lifesight audit trail."** It ships six prebuilt skills (Board Briefing, P&L Translator, Scenario Planner, Q4 Reallocation Stress Test, Channel Deep-Dive, Anomaly Triage). Future actions will require "explicit human approval". **No accuracy or uncertainty claims** were made at launch. — [PPC Land](https://ppc.land/lifesight-mcp-puts-live-marketing-measurement-inside-claude-and-chatgpt/) (second-hand of vendor launch)
- Adverity offers an "MMM Agent for Google Meridian". Northbeam lists MCP on its Growth tier. — [PPC Land](https://ppc.land/lifesight-mcp-puts-live-marketing-measurement-inside-claude-and-chatgpt/); [Northbeam pricing](https://www.northbeam.io/pricing)
- 60.9% of US marketers name generative insight summaries as their top AI enhancement for next-generation MMM (EMARKETER / Rakuten, Oct 2025, via EMARKETER). — [EMARKETER FAQ](https://www.emarketer.com/content/faq-on-incrementality-how-prove-your-ads-actually-work-2026)

### Inferences
- **The pain is credibility, not modelling.**
  - 60% of stakeholders question metrics, only 22% are confident with finance, and 75% say methods underperform.
  - Budget is being reallocated on doubt (29% of respondents risk up to 20%).
  - A claim-level evidence tag ("this channel ROI is experiment-backed in window W; this one is prior-only; this one is observational fit") speaks to exactly that doubt.
- **The layer must grade experiments too, not treat them as ground truth.** 44% doubt incrementality results; Sellforte documents scope mismatch, double-counting and a year-long Meta lift bug; Recast says conflicting tests on the same channel are "very common". The product's evidence tags therefore need sub-fields: scope (channel/campaign/geo/window), power or interval, independence from other studies, and who ran the randomisation (platform-run vs independent). This is a sharper differentiator than "experiment vs not".
- **The LLM-front-end wave creates the audit need.** Lifesight logs *queries*, not the *evidence status of each answer*. Once executives ask Claude or ChatGPT for a "Board Briefing", each sentence needs an evidence grade or an abstention. This is the claim-level gap, and no vendor read documents it (consistent with AU5 F5 and AB11).
- **Signal loss continues despite cookies surviving.** Chrome's reversal weakens the "cookieless" narrative, but ATT opt-in stays ~35%, Attribution Reporting is retired, and AI-assistant journeys are untracked. Demand for MMM plus experiments is sustained by these and by finance pressure, not by Chrome deprecation. Pitch accordingly.

### Gaps
- The full IAB State of Data 2026 PDF could not be fetched (fetch error); its sample size and method are unknown here.
- No independent (non-vendor) survey quantifies **how often** MMM estimates conflict with lift tests, or how long teams spend reconciling them. All conflict evidence found is vendor-blog or anecdotal.
- No CFO-side survey (e.g. Deloitte CFO Signals, Gartner for finance) on marketing ROI scrutiny was found in this pass; all finance-pressure figures are from marketers' self-reports.
- No LinkedIn or practitioner posts were read in this pass (budget). Anecdotes come only from vendor blogs (Recast, Sellforte).
- Not opened (search results only): Haus "Trust In, Trust Out" blog; LiftLab "Experiments validate MMM"; EMARKETER "MMM undervalues affiliate marketing"; Duke Fuqua CMO Survey "scrutiny" piece; cxtoday "flat budgets ROI pressure".
- Robyn's 2025–2026 maintenance status and adoption were not verified from a primary source (the only page found is unreliable).
