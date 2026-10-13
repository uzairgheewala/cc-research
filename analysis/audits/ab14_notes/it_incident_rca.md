# IT incident analysis / root cause analysis (RCA) as a vertical for an auditable causal-claims layer (as of 13 Oct 2026)

Scope note. This file extends, and does not repeat, AU5 (F2, F3, F5) and AB11 (pricing signals), plus the AB-12 probe. AB-12 found that on PetShop, declared call graph + traversal scored AC@3 0.901 (0.932 on answered issues with abstention, coverage 0.917). A PC-learned graph scored 0.208, and ranked correlation scored 0.799. The abstention rule added only +0.031 on answered issues and nothing on the no-issue period, where 40-83% of latency windows still produced a fabricated root cause. The product idea is to attach a source and a calibrated confidence to each causal claim an incident agent makes, and to abstain when evidence is thin.

All pages were fetched on 2026-10-13 unless stated otherwise.

Labels:
- **[primary]**: a filing, the vendor's own pricing page or docs, or an original survey publisher.
- **[vendor claim]**: marketing or self-reported performance.
- **[second-hand]**: an aggregator, analyst excerpt quoted by a third party, or a competitor's write-up.
- **[estimate]**: my arithmetic, with its inputs shown.

---

## Q1. Market sizes for observability, AIOps and incident management (2024-2026)

### Takeaway
Published sizes conflict by up to about 5x for the same category. Gartner's observability figure (about USD 14.2B by 2028) and MarketsandMarkets' figure (USD 11.91B in 2026) are roughly consistent. The AIOps estimates range from USD 6.7B to USD 32.5B for 2025, which makes the category unusable as a TAM anchor without a definition check. Public-company revenue is a firmer top-down anchor: Datadog guides to USD 4.45-4.47B for 2026, Dynatrace has USD 2.05B ARR and PagerDuty USD 0.50B ARR.

### Cited Findings
**Observability**
- Gartner (Magic Quadrant for Observability Platforms, 7 Jul 2025): the observability products market reaches about **USD 14.2B by 2028**, at an **11.1% CAGR for 2021-2028**. No base-year value is given. Gartner notes "strong cost fatigue" and buyers wanting clearer cost-to-value. [second-hand: excerpt of the Gartner MQ on a reseller research site] — [Spotlight AR excerpt](https://research.oz.spotlightar.com/reports/magic-quadrant-observability-platforms-2025/market-definition)
- MarketsandMarkets (published July 2026): observability tools and platforms at **USD 11.91B in 2026, rising to USD 22.99B by 2031**. The page quotes a "14.1% CAGR between 2023 and 2028", which does not match its own 2026-2031 window, so the page is internally inconsistent. [second-hand, paid report summary] — [MarketsandMarkets](https://www.marketsandmarkets.com/ResearchInsight/size-and-share-of-observability-tools-and-platforms-market.asp)

**AIOps**
- IMARC (27 Nov 2025): **USD 32.5B in 2025, rising to USD 132.2B by 2034**, CAGR 16.9% for 2026-2034. [second-hand, paid report summary] — [IMARC](https://www.imarcgroup.com/global-aiops-market)
- Global Market Insights (May 2025): **USD 6.7B in 2025, rising to USD 44.1B by 2034**, CAGR 22.1%. The page's meta description instead says USD 5.3B in 2024 with a 22.4% CAGR, so it is internally inconsistent. [second-hand] — [GMI](https://www.gminsights.com/industry-analysis/aiops-market)
- **Conflict.** IMARC's 2025 AIOps figure (USD 32.5B) is about 5x GMI's (USD 6.7B). It is also larger than both observability estimates, although AIOps is usually treated as a subset of IT operations tooling. The definitions clearly differ, and neither methodology was read.

**Incident management**
- DataHorizzon (18 Jan 2025): incident management software at **USD 8.5B in 2024, rising to USD 28.7B by 2033** (CAGR 12.9%). The page does not separate IT incidents from emergency incidents, and its regional values add up to USD 9.5B, not 8.5B. [second-hand, low quality] — [DataHorizzon](https://datahorizzonresearch.com/incident-management-software-market-39257)
- Do not use the "incident and emergency management" figures (USD 156B-255B). They cover public-safety and disaster-recovery spend, not IT ops. — [MarketsandMarkets via PR Newswire](https://prnewswire.com/news-releases/incident-and-emergency-management-market-worth-156-1-billion-by-2025--exclusive-report-by-marketsandmarkets-301080912.html)

**Revenue anchors from filings** [primary]
- Datadog: FY2025 revenue **USD 3.43B** (+28%) — [Datadog Q4 FY25 release, 10 Feb 2026](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-fourth-quarter-and-fiscal-year-2025-financial).
- Datadog: Q2 2026 revenue **USD 1.12B** (+36%); FY2026 guidance **USD 4.45-4.47B** — [Datadog Q2 2026 release, 6 Aug 2026](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-second-quarter-2026-financial-results).
- Dynatrace (FY ended 31 Mar 2026): revenue **USD 2.018B** (+19%), total ARR **USD 2.054B** (+18%) — [Dynatrace 8-K, 13 May 2026](https://www.sec.gov/Archives/edgar/data/0001773383/000177338326000011/fy26q4-earningsreleaseex99.htm).
- PagerDuty (FY ended 31 Jan 2026): revenue **USD 492.5M** (+5.4%), ARR **USD 498.7M** (+1%), dollar-based net retention **98%**, down from 106% — [PagerDuty FY26 release, 12 Mar 2026](https://investor.pagerduty.com/news/news-details/2026/PagerDuty-Announces-Fourth-Quarter-and-Full-Year-Fiscal-2026-Financial-Results/).
- Elastic (FY ended 30 Apr 2026): revenue **USD 1.739B** (+17%). This includes search and security, not only observability — [Elastic FY26 release](https://businesswire.com/news/home/20260527847546/en/Elastic-Reports-Fourth-Quarter-and-Fiscal-2026-Financial-Results).
- New Relic was taken private by Francisco Partners and TPG for about USD 6.5B (closed Nov 2023). It reports about USD 1B revenue (2025 milestone, period unspecified). [second-hand, Wikipedia] — [Wikipedia](https://en.wikipedia.org/wiki/New_Relic)
- Context: the "causal AI" category was sized at USD 56.2M in 2024 (AU5 F1, second-hand).

### Inferences
- Datadog, Dynatrace, Elastic, PagerDuty and New Relic together have about **USD 9-10B** of annual revenue. That is in the same range as the MarketsandMarkets and Gartner observability totals, so "observability ≈ USD 12-14B (2026-2028)" is a defensible top-down anchor.
  - [estimate] 4.46 + 2.02 + 1.74 + 0.49 + ~1.0 = **~USD 9.7B**. This is mixed fiscal years and includes Elastic's non-observability revenue.
- Do not anchor the brief on AIOps market reports. The ~5x spread shows the category is undefined.
- PagerDuty's flat ARR and 98% NRR (FY26) suggest that incident-management seat revenue is saturating. This is consistent with incumbents moving to consumption and AI-agent pricing (see Q3).

### Gaps
- IDC observability and AIOps figures were not found in open sources.
- Gartner's own AIOps and observability spend tables are paywalled. The Gartner figure above comes from a third-party excerpt.
- No AI-SRE-specific market size from an analyst was found. Only the Gartner adoption assumption is available (Q6).

---

## Q2. Bottom-up inputs: buyer counts, incident volumes, cost of downtime

### Takeaway
- **Buyer pool.** About 4,700-11,400 organisations spend at least USD 100k a year with one of the four public observability or incident vendors. This counts each vendor's list separately, with no de-duplication. Datadog alone has about 32,700 customers.
- **Incident volumes** span three orders of magnitude depending on definition:
  - about 25 high-priority incidents per year (PagerDuty survey);
  - 10-49 declared incidents per month (FireHydrant);
  - a median of 110 "actioned" alert-incidents per day (BigPanda).
- **Downtime.** Sourced hourly costs run from about USD 0.27M (PagerDuty 2024 average) to USD 2M (New Relic 2025, high-impact median).

### Cited Findings
**Buyer counts** [primary unless noted]
- Datadog: "approximately **32,700 customers** in over 160 countries" (31 Dec 2025, 10-K) — [Datadog 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm).
- Datadog: about **4,310** customers with ARR ≥ USD 100k and **603** ≥ USD 1M (31 Dec 2025) — [Q4 FY25 release](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-fourth-quarter-and-fiscal-year-2025-financial).
- Datadog: about **4,720** ≥ USD 100k (30 Jun 2026, +23% YoY) — [Q2 2026 release](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-second-quarter-2026-financial-results).
- Datadog Q2 2026 call: "over 750 AI customers"; 31 spend > USD 1M a year and 8 spend > USD 10M. [primary transcript, third-party host] — [DDOG 2Q26 transcript](https://transcripts.platformaeronaut.com/transcripts/DDOG-2Q26-transcript)
- Dynatrace: "approximately **4,100 customers** in over 110 countries" (31 Mar 2026). Its direct sales targets "the largest 15,000 companies globally" — [Dynatrace 10-K FY2026](https://www.sec.gov/Archives/edgar/data/0001773383/000177338326000019/dt-20260331.htm).
  - [estimate] Average ARR per customer is about USD 2.054B / 4,100 ≈ **USD 501k**.
- PagerDuty: **15,351** paid customers, of which **861** have ARR > USD 100k (31 Jan 2026) — [PagerDuty FY26 release](https://investor.pagerduty.com/news/news-details/2026/PagerDuty-Announces-Fourth-Quarter-and-Full-Year-Fiscal-2026-Financial-Results/).
- Elastic: "over **1,720**" customers with ACV > USD 100k (Q4 FY26, Apr 2026). This includes search and security customers — [Elastic FY26 release](https://businesswire.com/news/home/20260527847546/en/Elastic-Reports-Fourth-Quarter-and-Fiscal-2026-Financial-Results).
- incident.io had "powered over 250,000 incidents" by Apr 2025. Named customers: Netflix, Linear, Ramp, Etsy. No customer count was given. [vendor claim] — [Insight Partners, 10 Apr 2025](https://www.insightpartners.com/ideas/incident-io-raises-62m-to-build-ai-agents-that-resolve-incidents-with-you/)

**Incident and investigation volumes**
- PagerDuty/Censuswide survey (n = 500 IT leaders at companies with >1,000 employees; US, UK, AU; fieldwork 31 May-6 Jun 2024; released 27 Jun 2024). Vendor-sponsored survey:
  - an average of **25 high-priority incidents per year** per organisation;
  - **175 minutes** average to resolve;
  - **USD 4,537 per minute**;
  - **USD 794k per incident**;
  - "just under USD 20M a year";
  - incidents up an average of 43% for the 59% of firms reporting an increase.
  - Source: [PagerDuty newsroom](https://pagerduty.com/newsroom/study-cost-of-incidents)
- PagerDuty State of Digital Operations (n = 350, 7 Feb 2024): customer-facing incidents up **13% YoY**; enterprises up 16%, mid-market up 8%. No absolute counts. [primary vendor survey] — [PagerDuty](https://www.pagerduty.com/newsroom/2024-state-of-digital-operations-study/)
- FireHydrant Incident Benchmark Report covers 53,034 incidents resolved in 2019-2022 (report date not stated; likely early 2023). Declared incidents per month by company size:

  | Employees | Incidents per month |
  |---|---|
  | 0-599 | 10 |
  | 600-2,499 | 22 |
  | 2,500-6,000 | 49 |
  | 6,000+ | 37 |

  - Severity mix: 27% Sev1/Sev2.
  - MTTR "just over 24 hours".
  - [primary vendor dataset; dated] — [FireHydrant](https://firehydrant.com/reports/incident-benchmarks)
- BigPanda (2024 data, n = 125 organisations, page modified 11 Jul 2025): **median 34,232 actioned incidents per year per organisation**, or about 110 a day.
  - Median actionability rate: 18%.
  - By industry: financial services 86,034; technology 46,856.
  - These are AIOps-correlated alert incidents, not declared incidents. [primary vendor dataset] — [BigPanda](https://www.bigpanda.io/report/tool-effectiveness-for-it-event-management/detection-benchmarks/actioned-incidents)
- AWS DevOps Agent's pricing example: **10 investigations a month** averaging 8 minutes, costing USD 39.84 in total. This is an illustration, not usage data. [primary] — [AWS DevOps Agent pricing](https://aws.amazon.com/devops-agent/pricing/)
- New Relic 2025 Observability Forecast: 23% of teams with full-stack observability see high-impact outages at least weekly, against 40% without. Engineers spend 33% of their time on disruptions. [primary vendor survey] — [New Relic via BusinessWire, 17 Sep 2025](https://www.businesswire.com/news/home/20250917981661/en/New-Relic-Study-Reveals-Businesses-Face-an-Annual-Median-Cost-of-$76-Million-from-High-Impact-IT-Outages)

**Cost of downtime**
- New Relic 2025 Observability Forecast (n = 1,700, 23 countries, Apr-May 2025):
  - median **USD 2M per hour** for high-impact outages;
  - **USD 76M a year** median;
  - USD 1M per hour with full-stack observability.
  - [primary vendor survey] — [BusinessWire](https://www.businesswire.com/news/home/20250917981661/en/New-Relic-Study-Reveals-Businesses-Face-an-Annual-Median-Cost-of-$76-Million-from-High-Impact-IT-Outages)
- PagerDuty 2024: **USD 4,537 per minute**, about **USD 272k per hour** ([estimate] ×60) — [PagerDuty](https://pagerduty.com/newsroom/study-cost-of-incidents).
- PagerDuty, 17 Mar 2026 (n = 1,000 across US, UK/IE, JP, DE, ANZ, FR, Nordics). [primary vendor survey] — [Barchart/BusinessWire](https://www.barchart.com/story/news/803667/pagerduty-report-reveals-some-organizations-lose-more-than-1-million-per-hour-during-unplanned-disruptions)
  - 8% lose > USD 1M per hour;
  - 34% lose ≥ USD 500k per hour;
  - 68% lose > USD 300k per hour;
  - 77% plan to raise resilience budgets.
- Splunk with Oxford Economics (n = 2,000 executives, 12 Jun 2024): downtime costs the Global 2000 **USD 400B a year**, about **USD 200M per company** or about 9% of profits. [primary vendor-commissioned] — [Splunk](https://www.splunk.com/en_us/blog/cio-office/uncovering-downtime.html)
- **Conflict.** New Relic's USD 2M per hour is about 7x PagerDuty's USD 272k per hour. New Relic reports a median for "high-impact" outages; PagerDuty reports an average across priority incidents. Use them as a range and state the definitions.

### Inferences
- "Investigation" needs a definition in the brief. Agent vendors bill on alert investigations (Datadog, AWS, and Resolve's AWS Marketplace offer sized by "monthly alert volume and incident counts"). That volume sits between FireHydrant's tens of declared incidents a month and BigPanda's thousands of actioned alerts a month.
- The ≥ USD 100k customer lists overlap heavily. 4,720 (Datadog alone) is a floor; 11,401 (Datadog + Dynatrace + Elastic + PagerDuty) is an un-deduplicated ceiling.
  - [estimate] 4,720 + 4,100 + 1,720 + 861 = 11,401.

### Gaps
- No primary source counts organisations with SRE or platform teams. The vendor customer counts above are the proxy.
- Datadog does not disclose its share of ARR from ≥ USD 100k customers in the pages read. The 10-K was truncated at 100k characters.
- No 2025-2026 incident.io or Atlassian "State of Incident Management" report with per-organisation volumes was found.
- New Relic's customer count since going private was not found.
- No agent vendor discloses Bits or AI SRE adoption counts. Datadog's Q2 2026 call gives none.

---

## Q3. Pricing of AI SRE / AI investigation products (2025-2026)

### Takeaway
Autonomous investigations are priced openly by the large platforms, at about **USD 3-8.45 per investigation** in consumption units. Datadog appears to have moved from per-investigation bundles to AI credits in 2026; third-party pages still quote USD 500 per 20 investigations, which is USD 25 each. Startups (Resolve, Traversal, Cleric, Rootly AI SRE, incident.io AI SRE) do not publish prices and sell through sales-led or private offers. Incident-management seats cost USD 15-45 per user per month.

### Cited Findings
| Vendor / product | Price point (as read 13 Oct 2026) | Label | Source |
|---|---|---|---|
| **Datadog Bits AI SRE / Bits Investigation** | AI Credits: USD 500 per 500-credit bundle per month (annual), USD 600 month-to-month, USD 650 on demand; USD 1.30 per credit on demand. "Bits Investigate — Autonomous Investigation ~6.5 credits" | primary pricing page | [Datadog pricing list](https://www.datadoghq.com/pricing/list/); [pricing](https://www.datadoghq.com/pricing/?product=bits-ai-sre) |
| ↳ per-investigation arithmetic | 6.5 × USD 1.00 = **USD 6.50** (annual bundle) to 6.5 × 1.30 = **USD 8.45** (on demand) | estimate | as above |
| ↳ conflicting third-party quote | "USD 500/month for 20 investigations on an annual plan, or USD 600 month-to-month. Inconclusive investigations are free"; "Prices start at USD 500 per 20 investigations/month" (≈ **USD 25 per investigation**) | second-hand (competitors' pages, 19 Mar 2026 and 19 Aug 2026) | [Better Stack](https://betterstack.com/community/comparisons/bits-ai-sre-alternatives/); [Middleware](https://middleware.io/blog/ai-sre-tools/) |
| ↳ Datadog's own statement | CEO Q2 2026: "We have a new model with AI credits that we're rolling out" | primary transcript | [DDOG 2Q26](https://transcripts.platformaeronaut.com/transcripts/DDOG-2Q26-transcript) |
| **AWS DevOps Agent** (successor surface to CloudWatch investigations) | USD 0.0083 per agent-second; the example of 10 investigations × 8 min = USD 39.84/month, i.e. **USD 3.98 per investigation**; free tier with a 2-month trial (20 investigation-hours/month); monthly credits = 100% (Unified Ops) / 75% (Enterprise) / 30% (Business Support+) of the prior month's Support charge | primary | [AWS DevOps Agent pricing](https://aws.amazon.com/devops-agent/pricing/) |
| AWS CloudWatch investigations | no per-investigation price; quota of 150 enhanced investigations per account per month | primary (AB11) | AB11 |
| **Dynatrace** | Full-Stack USD 0.01 per memory-GiB-hour (≈ USD 58/month for an 8 GiB host, estimate); Infrastructure USD 0.04 per host-hour; **AI Units USD 0.10 per unit** (Agentic AppEngine) | primary rate card | [Dynatrace rate card](https://www.dynatrace.com/pricing/rate-card/) |
| ↳ units per investigation | AB11 recorded ~30 AI units per autonomous investigation (≈ USD 3.00). **Not stated on the rate-card page read today**; treat as unconfirmed | AB11 / unverified | — |
| ↳ DPS | "minimum annual spend commitment at the platform level", consumed by usage; overage at the same rates; larger commitment earns a deeper discount | primary 10-K | [Dynatrace 10-K FY26](https://www.sec.gov/Archives/edgar/data/0001773383/000177338326000019/dt-20260331.htm) |
| **PagerDuty** | Incident Mgmt Professional USD 21/user/month annual (USD 25 monthly); PD Reliability Platform fee **USD 2,800 / 12,000 / 48,000 per year** (Starter / Essential / Plus), Ultimate custom; "Paige, SRE Agent" an add-on in Incident Mgmt and included in Platform tiers; AI actions and events in included amounts plus **credit packs that expire annually**; AIOps SKU "will continue to exist" (no price shown) | primary pricing page | [PagerDuty pricing](https://www.pagerduty.com/pricing/) |
| ↳ PagerDuty AIOps | from USD 699/month (AB11, earlier read) | vendor claim (AB11) | AB11 |
| **incident.io** | Team USD 15 (annual) / 19; Pro USD 25 per user per month; On-call +USD 10 / +USD 20 per user; Enterprise custom; AI SRE ("Investigations", "autonomous agent") **no public price** | primary | [incident.io pricing](https://incident.io/pricing) |
| **Rootly** | Incident Response USD 20/user/month + On-Call USD 20/user/month (additive); **AI SRE "contact sales"**, now requires Incident Response (packaging change week 42, 12 Oct 2026) | second-hand (PricingSaaS tracker) | [PricingSaaS Rootly](https://pricingsaas.com/companies/rootly) |
| **Resolve AI** | no public price; "reportedly reaches USD 1M+/year for large deployments" (unsourced claim on a competitor's page); AWS Marketplace listing is a **12-month custom private offer**, sized on "monthly alert volume and incident counts" | second-hand / primary listing | [Better Stack](https://betterstack.com/community/comparisons/bits-ai-sre-alternatives/); [AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/prodview-76q4p3nhuqgj4) |
| **Traversal** | no public price found | — | — |
| **Cleric** | no public price found | — | — |
| **Causely** | Professional **USD 2,000/month for up to 500 services** (30-day retention, hybrid deploy); Enterprise custom (on-prem / air-gapped); 30-day trial | primary | [Causely pricing](https://www.causely.ai/pricing) |
| Others | Sentry Seer USD 40 per active contributor per month; Dash0 Agent0 from ~USD 50/month; Better Stack on-call from USD 29/responder/month | second-hand | [Better Stack](https://betterstack.com/community/comparisons/bits-ai-sre-alternatives/) |
| Cost floor (DIY LLM) | ClickHouse experiment: USD 0.10 to nearly USD 6 per LLM RCA investigation, taking 1 to 45 minutes | second-hand (InfoQ, 27 Sep 2025) | [InfoQ](https://infoq.com/news/2025/09/clickhouse-llm-sre-report) |

### Inferences
- Platform investigation prices cluster at **USD 3-8.45**: Dynatrace about 3 (unconfirmed), AWS 3.98, Datadog 6.50-8.45. That is close to raw LLM cost (USD 0.10-6, ClickHouse), so there is little margin for a separately billed per-investigation verification fee.
  - A verification layer priced per investigation probably has to sit at **≤ 10-25% of the agent price, about USD 0.30-2**.
  - Alternatively it could be a flat platform fee in the band PagerDuty and Causely occupy (USD 8.4k-48k a year).
- Better Stack reports that Datadog bills only conclusive investigations ("inconclusive investigations are free"; second-hand, not confirmed on Datadog's pages). If true, the vendor's revenue rises with conclusive answers, which gives the agent vendor a structural reason not to abstain.
  - This is an argument for a **third-party** claim auditor, which would carry no such conflict.
  - The billing claim must be verified before the brief uses it.

### Gaps
- No public pricing for Traversal, Cleric, NeuBird, Ciroos, or the incident.io and Rootly AI SRE tiers.
- PagerDuty credit-pack prices are not shown.
- Datadog's exact Bits AI SRE billing rule (conclusive only, or every run) was not found on Datadog's own pages. The docs pages read say nothing on billing.
- Dynatrace AI units per investigation are not confirmed.

---

## Q4. Funding of AI SRE startups (2025-2026)

### Takeaway
Rounds that could be confirmed for AI SRE and incident agents add up to about **USD 266M across five companies in 2025-2026**. Resolve AI holds the only unicorn valuation. Investors are top-tier (Lightspeed, Sequoia, Kleiner, Insight), and a strategic (Amex Ventures) has appeared. Several startups pitch "causal" or "evidence" language.

### Cited Findings
- **Resolve AI.** USD 125M Series A at a USD 1B valuation. Lightspeed led; Greylock, Unusual and others participated. Announced 4 Feb 2026.
  - TechCrunch sources suggested tranches at different prices, which would put the blended valuation below USD 1B. The company denied this ("100% of the equity was purchased at a valuation of USD 1 billion").
  - Founded early 2024 by ex-Splunk executives.
  - [second-hand news] — [TechCrunch, 4 Feb 2026](https://techcrunch.com/2026/02/04/ai-sre-resolve-ai-confirms-125m-raise-unicorn-valuation/); earlier report: [TechCrunch, 19 Dec 2025](https://techcrunch.com/2025/12/19/ex-splunk-execs-startup-resolve-ai-hits-1-billion-valuation-with-series-a)
- **Traversal.** USD 48M seed plus Series A, led by Sequoia and Kleiner Perkins, 18 Jun 2025 [vendor announcement] — [Traversal](https://www.traversal.com/post/fortune).
  - Amex Ventures made a strategic investment (amount undisclosed) on 5 Mar 2026.
  - Its "Causal Search Engine" "investigates incidents by testing hypotheses against system topology and operational data".
  - It claims a 40% average MTTR reduction [vendor claim].
  - [second-hand] — [Pulse 2.0](https://pulse2.com/traversal-ai-site-reliability-engineering-platform-receives-strategic-investment-from-amex-ventures/amp/)
- **incident.io.** USD 62M Series B, led by Insight Partners, 10 Apr 2025; total raised over USD 96M. The round funds AI agents that investigate and resolve incidents. — [Insight Partners](https://www.insightpartners.com/ideas/incident-io-raises-62m-to-build-ai-agents-that-resolve-incidents-with-you/)
- **Cleric.** USD 9.8M total seed, led by Vertex Ventures US with Zetta. The URL dates it to about 9 Dec 2025.
  - Claims "confidence scores", findings "with links to relevant evidence", and "20-30% of engineering capacity" freed [vendor claim].
  - Customer: BlaBlaCar. — [BusinessWire](https://businesswire.com/news/home/20251209625361/en/Cleric-Launches-the-First-Self-Learning-AI-SRE)
- **Ciroos.** USD 21M seed, led by Energy Impact Partners, 3 Jun 2025. Product: a "multi-agent AI SRE Teammate". [second-hand, Seedtable] — [Seedtable](https://seedtable.com/companies/ciroos)
- **NeuBird** (2024, for context). USD 22M seed in Apr 2024 at a USD 100M valuation (PitchBook via TechCrunch). A further USD 22.5M led by M12 on 11 Dec 2024. Its Hawkeye agent escalates to a human when it cannot resolve an issue. — [TechCrunch](https://techcrunch.com/2024/12/11/microsofts-m12-invests-another-22-5m-into-nuebird-months-after-its-22m-seed-round/)
- **Causely.** USD 8.8M seed (29 Jun 2023, per the BusinessWire headline; page not opened) — [BusinessWire](https://www.businesswire.com/news/home/20230629773124/en/Causely-Raises-8.8M-in-Seed-Funding-to-Deliver-IT-Industry%E2%80%99s-First-Causal-AI-Platform). No 2025-2026 round was found.
- **Rootly.** A USD 12M Series A post exists, but it was not opened and its date is unknown — [Rootly blog](https://rootly.com/blog/rootly-raises-12-million-from-renegade-partners-google-gradient-ventures-xyz-ventures.md).
- **Datadog** acquired Eppo (May 2025, ~USD 220M reported; AU5). This is the incumbent buying causal-adjacent (experimentation) capability.

### Inferences
- [estimate] Confirmed 2025-2026 AI SRE rounds: 125 + 48 + 62 + 9.8 + 21 = **USD 265.8M**. This excludes Amex's undisclosed amount and rounds that were not found.
- Traversal ("causal search", topology-tested hypotheses) and Causely ("causal reasoning") already occupy "causal" positioning. The claims layer should be pitched as **a vendor-neutral audit of any agent's claims**, not as another causal RCA engine. This matches AB-12's result that the value lies in provenance and abstention, not structure learning.

### Gaps
- No 2026 rounds found for Cleric, Traversal (beyond Amex), Rootly or Causely. Not checked: Deductive, Wild Moose, Parity, Komodor (Klaudia), Sherlocks AI (a USD 900k round appears in search results only).
- Startups' ARR and customer counts are undisclosed.

---

## Q5. Buyer, budget line, and purchase channel

### Takeaway
- **Budget.** The purchase rides on the observability and incident-management budget, mostly as consumption drawn from pre-committed spend. Mechanisms: Dynatrace DPS commitment, Datadog AI credits, PagerDuty credit packs, AWS Support-plan credits, and private offers on AWS Marketplace.
- **The "10-30% of cloud spend" figure.** Its best public source is a practitioner rule of thumb (15-25%, Honeycomb 2025), not a survey.
- **Who signs.** No primary source names the signing title.

### Cited Findings
**Budget line**
- Charity Majors (Honeycomb CTO), 16 Apr 2025 (updated 20 May 2025): observability spend is "around 15-25% of your infra bill".
  - The 2018 version said "~20-30%", "based on absolutely no data, only my own experiences".
  - Analysts told her about 10% "should be achievable" for large enterprises.
  - A Gartner webinar gave no percentage.
  - [vendor-authored anecdote] — [Honeycomb blog](https://honeycomb.io/blog/how-much-should-i-spend-on-observability-pt1)
- Gartner MQ 2025: buyers face "strong cost fatigue" and want clearer cost-to-value. [second-hand excerpt] — [Spotlight AR](https://research.oz.spotlightar.com/reports/magic-quadrant-observability-platforms-2025/market-definition)
- Grafana Observability Survey 2026 (n > 1,300, 76 countries, fieldwork Oct-Jan, published 18 Mar 2026):
  - cost is "universally cited as the top tool selection criteria";
  - only **15%** call AI capabilities an important selection criterion.
  - [primary vendor survey] — [Grafana](https://www.grafana.com/blog/observability-survey-AI-2026)
- PagerDuty, Mar 2026: 77% plan to increase resilience budgets over the next 12 months. [primary vendor survey] — [Barchart](https://www.barchart.com/story/news/803667/pagerduty-report-reveals-some-organizations-lose-more-than-1-million-per-hour-during-unplanned-disruptions)

**Purchase channel**
- Dynatrace DPS: a minimum annual platform commitment, drawn down by usage, including AI units at USD 0.10. Direct sales target the 15,000 largest companies. [primary] — [10-K](https://www.sec.gov/Archives/edgar/data/0001773383/000177338326000019/dt-20260331.htm); [rate card](https://www.dynatrace.com/pricing/rate-card/)
- Datadog: AI credits are an annual bundle or on demand. Its 10-K cites "the pricing of subscriptions from customers in our cloud-provider marketplaces" as a factor affecting results. No share of revenue is given. [primary] — [10-K FY2025](https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm)
- PagerDuty: annual platform fees, with AI actions in included amounts plus credit packs that expire annually. [primary] — [pricing](https://www.pagerduty.com/pricing/)
- AWS DevOps Agent is paid partly by credits worth 30-100% of the prior month's AWS Support charge. AI agents are therefore effectively bundled into an existing support budget line. [primary] — [AWS](https://aws.amazon.com/devops-agent/pricing/)
- AWS Marketplace launched an "AI Agents & Tools" category with MCP/A2A listings on 16 Jul 2025. [primary] — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/07/ai-agents-tools-aws-marketplace)
- Resolve AI sells "AI SRE" on AWS Marketplace as a 12-month custom private offer, non-cancellable. [primary listing] — [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-76q4p3nhuqgj4)
- The only adoption figure is Gartner's assumption that AI SRE tooling use rises from **<5% of enterprises in 2025 to 85% by 2029**. It comes from the Market Guide for AI SRE Tooling (26 Jan 2026) as quoted by a listed vendor. [second-hand] — [Cast AI](https://cast.ai/gartner-market-guide-for-ai-sre-tooling/). PagerDuty also cites being named in this guide. — [PagerDuty FY26 release](https://investor.pagerduty.com/news/news-details/2026/PagerDuty-Announces-Fourth-Quarter-and-Full-Year-Fiscal-2026-Financial-Results/)

### Inferences
- The likely path is a **marketplace private offer or integration that draws on committed cloud or observability spend**, not a new budget line.
  - Buyers already burn down DPS, AI credits or AWS credits.
  - A standalone tool must justify new spend against "cost fatigue".
  - Practical channels: an MCP-compatible tool listed in AWS Marketplace's AI Agents & Tools category, or a Datadog/Dynatrace/PagerDuty integration.
- Signer (inference, not sourced): VP Engineering, or Head of SRE/Platform/Infrastructure, who owns the observability bill. Risk, compliance and audit may co-sign where agents act in production (see Q6, "audit trails").
- Grafana's 15% "AI is an important criterion" warns that an AI-verification layer is unlikely to be bought on its own feature merits. It has to be framed as a risk or cost reduction: wrong-root-cause detours, MTTR, and audit evidence.

### Gaps
- No survey or job-posting source names the economic buyer for AI SRE tools.
- No independent survey gives observability as a % of cloud spend.
- No marketplace share-of-revenue figure for Datadog, Dynatrace or PagerDuty was found.
- Whether Causely, Traversal and Cleric are on cloud marketplaces was not confirmed. The Causely FAQ entry has no visible answer.

---

## Q6. Public demand signals for trust and verification of AI incident agents

### Takeaway
- Demand for "show your work" is broad. In Grafana's 2026 survey, 95% say it is important for AI to show its reasoning.
- No vendor publishes production precision or recall for AI RCA.
- Practitioners are starting to say publicly that AI root causes are wrong a material share of the time (one conference abstract says 23%), and that "detectability" matters more than accuracy.
- Vendors already sell "evidence-backed", "verifiable", "confidence scores" and "citations". Per-claim provenance is becoming table stakes, so the differentiator must be **typed source plus calibration plus abstention, checked independently**.

### Cited Findings
**Survey evidence**
- Grafana 2026: 95% say it is important for AI to show its reasoning:

  | Answer | Share |
  |---|---|
  | Important | 29.5% |
  | Very important | 26.6% |
  | It is critical | 21.6% |
  | Somewhat important | 17.2% |
  | Not important | 5.1% |

  - 91% say root-cause and correlation assistance would be valuable.
  - Skepticism rises from 4-5% for assistance to 15% for autonomous action.
  - Only 49% rate autonomous action "very valuable" or "critical".
  - [primary vendor survey] — [Grafana](https://www.grafana.com/blog/observability-survey-AI-2026)

**Competitor critiques and evaluations**
- incident.io, "Rootly AI RCA accuracy: verified claims vs. reality" (14 Apr 2026, competitor-written):
  - "no published precision or recall metrics for root cause analysis in production environments" for Rootly;
  - incident.io itself publishes none either;
  - it proposes asking vendors for precision, recall, false-positive rate, time to hypothesis and **confidence signaling**: "If a vendor cannot answer questions 1 and 2 with documented numbers, the AI RCA capability is unverified."
  - [second-hand, competitor] — [incident.io](https://incident.io/blog/rootly-ai-accuracy-vs-competitors)
- ClickHouse experiment (InfoQ, 27 Sep 2025): Claude Sonnet 4, o3, GPT-4.1 and Gemini 2.5 Pro on 4 OpenTelemetry-demo scenarios.
  - "Autonomous RCA is not there yet."
  - Gemini "formed an unsupported cause and tried to prove it".
  - [second-hand of vendor experiment] — [InfoQ](https://infoq.com/news/2025/09/clickhouse-llm-sre-report)
- Datadog engineering blog (12 Jan 2026): an early Bits version found the true cause in one of 12 tool calls but "still named the wrong one" in the summary. The fix tied each hypothesis to specific telemetry ("causal relationship between the monitor alert and specific telemetry data").
  - Evaluation uses human-labelled real incidents and an LLM judge aligned to human scores; no accuracy number is published.
  - [primary vendor] — [Datadog blog](https://datadoghq.com/blog/building-bits-ai-sre/)
- HighLoad++ 2026 (Moscow) abstract, "Your AI Root-Cause Is Wrong 23% of the Time" (N. Pandey):
  - the causal-reasoning engine was "wrong 23% of the time", the number "nobody puts on a slide";
  - the 22-to-4-minute median time-to-root-cause is "survivorship-contaminated";
  - "detectability, not accuracy, is the safety property to design for."
  - Method and sample are not stated. [anecdote / conference abstract] — [HighLoad++](https://highload.ru/moscow/2026/abstracts/19223)

**Practitioner opinion**
- CSO Online, 11 Jun 2026 (opinion by a StackGen developer advocate): "SRE teams will not trust an agent that gives answers without showing its work". Teams want audit trails and rollback paths, and "Explainability over magic". [anecdote, vendor-affiliated author] — [CSO Online](https://www.csoonline.com/article/4183666/what-sre-teams-need-before-they-trust-ai-agents.html)
- HackerNoon, 30 Sep 2026 (Middleware marketer):
  - "LLMs are very good at constructing coherent explanations from incomplete information … It becomes dangerous when you present a plausible explanation as a verified root cause".
  - It endorses explicit partial answers: "I have enough evidence to identify the suspicious code path, but not enough evidence to confirm the root cause … That is not a failure."
  - [anecdote, vendor-affiliated] — [HackerNoon](https://hackernoon.com/when-your-ai-sre-runs-out-of-telemetry-the-missing-evidence-problem-in-production-debugging)
- Substack "Why AI SRE tools are getting it wrong" (S. Economakis, 21 Jun 2026, promotes NOFire): a display "must not claim more than its data supports". [anecdote, vendor-affiliated] — [Substack](https://thereliabilityengineering.substack.com/p/why-ai-sre-tools-are-getting-it-wrong)

**Vendors selling evidence, explainability or confidence as features** [vendor claims]
- Datadog Bits Investigation: "transparent, verifiable investigations"; "90% faster"; "grounded in thousands of real-world incidents". No confidence scores or inconclusive handling on the product page — [Datadog](https://www.datadoghq.com/product/ai/bits-investigation/). AB11 recorded the docs' "evidence-backed" vs "inconclusive" outcomes.
- Cleric: "confidence scores", "links to relevant evidence" — [BusinessWire](https://businesswire.com/news/home/20251209625361/en/Cleric-Launches-the-First-Self-Learning-AI-SRE).
- Traversal: "testing hypotheses against system topology and operational data" — [Pulse 2.0](https://pulse2.com/traversal-ai-site-reliability-engineering-platform-receives-strategic-investment-from-amex-ventures/amp/). It also has a "How should you evaluate an AI SRE product?" post (not opened) — [Traversal](https://www.traversal.com/blog/how-should-you-evaluate-an-ai-sre-product).
- Deeptrace: "70%+ root cause identification accuracy", root causes "with citations"; Better Stack: every agent query visible; Rootly: "transparent reasoning". [second-hand via a competitor] — [Better Stack](https://betterstack.com/community/comparisons/bits-ai-sre-alternatives/)
- NeuBird Hawkeye escalates to a human when it cannot resolve an issue, an escalation-style abstention — [TechCrunch](https://techcrunch.com/2024/12/11/microsofts-m12-invests-another-22-5m-into-nuebird-months-after-its-22m-seed-round/).
- From AU5/AB11: IBM Instana reports low confidence on sparse telemetry, and Dynatrace claims "deterministic, causation-based analysis".

### Inferences
- **Demand is stated, but not yet paid for.** The signals are surveys (95% want reasoning shown), competitor critiques and practitioner essays. No buyer paying specifically for calibrated confidence or abstention was found, so AU5's "unvalidated demand" still holds.
- **"Citations" and "verifiable" are becoming standard claims**, from Datadog, Deeptrace, Cleric and Better Stack. A ledger that only attaches evidence links is not differentiated. Three things are not offered by anyone in the sources read:
  1. a typed source per sub-claim: topology declared vs learned vs anomaly score vs change event, as in AB-12 §7;
  2. calibration measured against labelled incidents;
  3. abstention whose rate is reported.
- **AB-12's open item matches the strongest practitioner complaint.**
  - AB-12 found 40-83% fabricated latency answers on no-issue windows.
  - The practitioner complaint is plausible explanations presented as verified root causes; the "23% wrong" talk makes the same point.
  - The brief should present no-issue-period specificity as the measurable feature buyers lack. It should not claim AB-12's abstention already solves it.

### Gaps
- No Hacker News or Reddit thread with direct user complaints about a named AI SRE product's hallucinated root cause was retrieved. Searches returned blogs, not HN threads.
- No independent (non-vendor) benchmark of commercial AI SRE agents was found.
- The method behind the HighLoad "23%" figure is not described.

---

## Q7. Bottom-up market estimate for a claim-audit layer (synthesis of Q2-Q3; all arithmetic is an estimate)

### Takeaway
[estimate] The serviceable market for an independent claim-verification layer is about **USD 9M (mid) per year**, within a wide **USD 0.3M-290M** band, if priced per investigation. If priced as a flat platform add-on at incumbent price points, it is **USD 40M-550M** (mid USD 180M). A realistic 3-year obtainable slice is **USD 2-9M ARR**. The width comes almost entirely from the definition of "investigation". The value case (USD 0.27M-2M per downtime hour) is far larger than any price point.

### Cited Findings
The inputs are cited in Q2 and Q3:
- buyer counts: Datadog ≥ USD 100k 4,720; Dynatrace 4,100; Elastic 1,720; PagerDuty 861;
- volumes: FireHydrant 10-49 incidents a month; BigPanda 110 actioned a day; PagerDuty 25 high-priority a year;
- agent prices: USD 3 / 3.98 / 6.50-8.45 per investigation;
- flat fees: PagerDuty AIOps USD 699/month (AB11), PagerDuty Essential USD 12k/yr, Causely USD 24k/yr, PagerDuty Plus USD 48k/yr;
- downtime: PagerDuty USD 4,537/min, New Relic USD 2M/hr.

### Inferences
**Inputs [estimate]**

| Input | Low | Mid | High |
|---|---|---|---|
| N, buyer organisations | 4,720 (Datadog ≥ 100k only) | 7,500 (judgement, de-duplicated overlap) | 11,401 (four vendor lists summed, not de-duplicated) |
| I, agent investigations per org per month | 20 (Datadog entry bundle; FireHydrant 10-49 declared incidents) | 100 | 1,000 (≈ 30% of BigPanda's median 110 actioned a day ≈ 3,300 a month) |
| P_agent, price per investigation | USD 3.00 (Dynatrace, AB11) | USD 6.50 (Datadog annual credits) | USD 8.45 (Datadog on demand) |
| s, audit-layer price as a share of agent price | 10% | 15% | 25% |

**A. Agent-investigation spend pool = N × I × 12 × P_agent [estimate]**
- Low: 4,720 × 20 × 12 × 3.00 = **USD 3.4M per year**
- Mid: 7,500 × 100 × 12 × 6.50 = **USD 58.5M per year**
- High: 11,401 × 1,000 × 12 × 8.45 = **USD 1.156B per year**
- Cross-check, Gartner adoption: 2025 adoption under 5% puts the realised 2025-2026 pool near the low-to-mid end. The 85%-by-2029 assumption (second-hand) would push it toward mid-to-high.

**B. Per-investigation audit layer = A × s [estimate]**
- Low: 3.4M × 10% = **USD 0.34M**
- Mid: 58.5M × 15% = **USD 8.8M**
- High: 1.156B × 25% = **USD 289M**

**C. Flat platform add-on = N × ACV [estimate]**
- Low: 4,720 × USD 8,388 (PagerDuty AIOps USD 699 × 12) = **USD 39.6M**
- Mid: 7,500 × USD 24,000 (Causely list) = **USD 180M**
- High: 11,401 × USD 48,000 (PagerDuty Plus) = **USD 547M**

**D. Obtainable in about 3 years [estimate]**
- 1-5% penetration of mid N (75-375 organisations) at USD 24k = **USD 1.8M-9.0M ARR**.

**E. Top-down sanity check [estimate]**
- 1% of observability spend: USD 11.91B (M&M 2026) → USD 119M; USD 14.2B (Gartner 2028) → USD 142M.
- So mid C (USD 180M) is about 1.3-1.5% of observability spend: plausible as a TAM, aggressive as a SAM.
- High B (USD 289M) is about 2.4% of 2026 observability spend: implausible near term.

**F. Value per customer (illustrative) [estimate]**
- One avoided 15-minute wrong-root-cause detour on a high-priority incident: 15 × USD 4,537 = **USD 68k** (PagerDuty basis), or 0.25 h × USD 2M = **USD 500k** (New Relic high-impact basis).
- Four such avoided detours a year, out of PagerDuty's 25 high-priority incidents, is worth USD 272k-2M. That exceeds every price point above.
- The binding constraint is therefore proof that the layer detects wrong answers (the HighLoad "detectability" framing), not willingness to pay.

**Assumptions that move the estimate most**
- The definition of an investigation: declared incidents vs alert triage. This drives about 50x of the range.
- Whether incumbents bundle verification for free. Datadog's "verifiable investigations" and Cleric's confidence scores suggest they will try.

### Gaps
- No primary source gives investigations per organisation for AI agents. I is the least-grounded input.
- No data on willingness to pay for verification separately from the agent.
- De-duplication of the vendor customer lists is judgement, not data.
- Practitioner interviews (AU5 recommendation 6) are still needed to validate s and the buyer title.
