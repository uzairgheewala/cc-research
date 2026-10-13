# Public demand signals for trustworthy, auditable causal claims from AI tools (as of 2026-10-13)

All evidence below is INDIRECT. None of it is an interview with the capstone's target users. It stands in for the planned 5-8 practitioner interviews.

Tag format for each finding: [evidence type | date | sector | hypothesis | direction].
- Evidence types: survey (n=…), primary, second-hand, vendor claim, anecdote. Vendor-run surveys are tagged "survey, vendor-run".
- Direction: + supports the hypothesis, − cuts against it, ~ mixed or neutral.
- Hypotheses:
  - H1: practitioners would use per-claim provenance and abstention.
  - H2: practitioners ask intervention or effect questions, not for full graphs.
  - H3: an audit of an LLM tool's reliance on names and semantics is worth paying for.

## Q1. Surveys (2023-2026): trust in AI analytics, explainability and audit requirements, hallucination concerns

### Takeaway
- The strongest direct H1 signal is insightsoftware's 2026 survey (n=114 data and analytics leaders, vendor-run):
  - 53% prioritise audit trails for AI-generated answers;
  - 51% prioritise verifiable or deterministic AI outputs;
  - 31% say they cannot verify AI results;
  - only 51% trust AI-generated insights.
- Large developer surveys (Stack Overflow 2025) show distrust of AI accuracy outweighing trust, 46% to 33%.
- No survey found asks about causal claims specifically.
- No survey found measures how often practitioners use causal inference.

### Cited Findings
- [survey, vendor-run, n=114 | 2026-06-10 | cross-industry data and analytics leaders | H1, H3 | +] insightsoftware 2026 AI survey. Source: [insightsoftware blog](https://www.insightsoftware.com/blog/why-dont-data-leaders-trust-ai-and-other-insights-from-our-2026-ai-survey/). Findings:
  - 51% trust AI-generated insights; 33% are concerned about hallucinations; 26% have had negative consequences from hallucinations or unreliable AI.
  - Governance priorities: audit trails for AI-generated answers 53%; verifiable or deterministic AI outputs 51%; user permission controls 43%.
  - Pilot-to-production blockers: security and governance 58%; inaccurate or inconsistent outputs 39%; lack of ability to verify results 31%.
  - Caveats: insightsoftware sells BI and analytics software. Fieldwork dates and methodology are not published, and a trust-factor chart has no figures in the text. The [landing page](https://insightsoftware.com/resources/key-findings-from-insightsoftwares-2026-ai-survey/) gates the full results behind a form.
- [survey, n≈49,000 implied by response counts | 2025 survey; page undated | software developers | H1 | +] Stack Overflow 2025 Developer Survey, AI section. Source: [survey.stackoverflow.co/2025/ai](https://survey.stackoverflow.co/2025/ai).
  - Trust in AI tool accuracy: highly trust 3.1%, somewhat trust 29.6%, somewhat distrust 26.1%, highly distrust 19.6%. That is about 46% distrust against 33% trust.
  - The most-cited frustration is "AI solutions that are almost right, but not quite" (66%). For H1 this suggests verification cost is the pain point.
  - 65.6% do not plan to use AI for predictive analytics.
  - There is no breakdown for data scientists.
- [survey, vendor-run, "over 2,000 data professionals", exact n not stated | report 2025; blog 2026-02-20 | data teams | H1 | ~] Hex's State of Data Teams 2025, as summarised by Hex. Source: [Hex blog](https://hex.tech/blog/ai-analytics-trust/).
  - 77% are excited about AI, but only 3% call it a main focus area. 84% rate data quality as a top focus.
  - Hex's own guidance (not measured) recommends: lineage so "a number can be traced to its source tables"; routing low-confidence and ambiguous questions to human review, which is abstention; and confidence indicators.
  - This is vendor guidance, not a measurement of demand.
- [survey, n=100 CIOs plus about 24 buyer conversations | 2025-06-10 | enterprise IT, 15 industries | H1, H3 | ~ / −] a16z, "How 100 Enterprise CIOs are building and buying Gen AI in 2025". Source: [a16z](https://a16z.com/ai-enterprise-2025/).
  - Security and cost "have gained ground on overall accuracy and reliability" as selection criteria. One quote: "all the models perform well enough now—so pricing has become a much more important factor."
  - Enterprises use internal benchmarks and golden datasets ("you still need to assess yourself"). This is demand for evaluation, read as + for evaluation in general.
  - Trust in model performance has increased, which is − for urgency.
  - The report does not mention hallucinations.
- [survey, n not stated | 2025-09-23; fieldwork July 2025 | enterprise software buyers | H1 | ~] Futurum's decision-maker survey. Source: [Futurum press release](https://futurumgroup.com/press-release/genai-features-are-the-top-criteria-for-future-enterprise-software-purchases/).
  - Top purchase criteria: GenAI capabilities 40.6%, features 39.6%, pricing 39.6%, agentic capabilities 37.8%.
  - Trust, accuracy and explainability do not appear among the reported criteria. Capability ranks above assurance here.
- [second-hand / headline only | date not shown (2026 footer) | enterprise | H1 | ~] "AI Analytics Hits a Trust Barrier" (BankInfoSecurity). The teaser reports "limited confidence" in AI analytics and says "most employees still rely on dashboards and manual requests". The full text and survey identity could not be retrieved; the fetch returned only the teaser. Source: [BankInfoSecurity](https://bankinfosecurity.com/ai-analytics-hits-trust-barrier-a-32632).

### Inferences
- The "audit trail" and "verifiable/deterministic outputs" items (53% and 51%) are the closest public proxy for H1. They support provenance demand at the level of data-to-answer lineage, not causal-edge provenance specifically.
- Every analytics-trust survey found is vendor-run (insightsoftware, Hex). This biases them toward finding a trust problem the vendor sells a fix for.
- No survey measured abstention preference directly. Hex's recommendation to escalate low-confidence answers to humans is vendor advice, not a measurement.

### Gaps
- No public survey asks about causal inference or causal discovery usage, or about trust in AI-produced causal claims.
- Kaggle ML and DS survey: I did not find a 2023-2026 edition. I believe it stopped after 2022, but did not verify this.
- Anaconda State of Data Science: only 2022 and 2023 editions surfaced; I did not fetch them.
- McKinsey State of AI, Gartner and Deloitte: their figures on inaccuracy risk were not retrieved. Search returned only aggregators or gated abstracts.
- dbt and Databricks state-of-data reports were not retrieved.

## Q2. Job-market signals for causal inference and causal ML

### Takeaway
- I found no public, methodologically stated count or trend of job postings mentioning "causal inference" or "causal ML".
- The strongest market-level signal about causal methods is capital flowing into experimentation platforms, which measure intervention effects:
  - Statsig: about $40M annualised revenue and a $1.1B valuation (May 2025), then acquired by OpenAI for a reported $1.1B (Sept 2025);
  - Eppo: acquired by Datadog for a reported $220M.

### Cited Findings
- [second-hand, Fortune | 2025-05-06 | experimentation / product analytics | H2 | +] Statsig raised a $100M Series C at a $1.1B valuation, led by ICONIQ. Source: [Fortune](https://www.fortune.com/2025/05/06/statsig-series-c-100-million-1-1-billion-eppo-datadog).
  - About $40M annualised revenue; customers include Notion and Rippling.
  - Datadog acquired competitor Eppo. Upstarts Media reported $220M; Datadog confirmed the deal but not the price.
- [second-hand | Sept 2025 | AI labs / experimentation | H2 | +] OpenAI acquired Statsig for a reported $1.1B and named CEO Vijaye Raji CTO of Applications. Sources: [AI Business](https://aibusiness.com/generative-ai/openai-acquires-startup-for-1-1b-hires-ceo); [etcentric](https://www.etcentric.org/openai-acquires-product-testing-firm-statsig-for-1-1-billion/). I did not fetch the full articles; the facts come from headlines and snippets.
- [aggregator listing | undated | various | H2 | ~] ZipRecruiter runs a "Causal Inference Jobs" listing page, but I found no count I could cite. Source: [ZipRecruiter](https://www.ziprecruiter.com/n/Causal-Inference-Jobs-Near-Me).
- [primary, job post | undated | marketing science | H2 | +] Open Data Science job board listing: "Data Scientist, Causal Inference and Experimental Design, Marketing Science R&D". This is one example of a titled causal-inference role. Source: [ODSC jobs](https://jobs.opendatascience.com/jobs/data-scientist-causal-inference-and-experimental-design-marketing-science-rd/). I did not fetch it.
- [negative result] The DoorDash Greenhouse link fetched a general listing (462 openings, mostly support and DashMart roles) with no causal-inference postings visible on the first page. Source: [DoorDash Greenhouse](https://job-boards.greenhouse.io/doordashusa/jobs/7095169).
- [negative result] Scott Cunningham's Mixtape piece (2022-02-09) on ML engineers and causal inference contained no posting counts in the visible, non-paywalled text. Source: [Mixtape Substack](https://causalinf.substack.com/p/the-role-of-machine-learning-engineers).

### Inferences
- Buyers pay a lot for tools that measure intervention effects through randomised experiments: a $1.1B exit and a $220M exit.
  - This is indirect support for H2, since the economic demand is for "what happens if we change X".
  - It cuts against any claim of demand for causal discovery or full graphs, since none of these companies sells graph discovery.

### Gaps
- No public job-posting counts or trends for "causal inference" or "causal ML". LinkedIn, Indeed Hiring Lab, Lightcast and similar sources were not found or are not public. A count would need a manual scrape, for example of company career pages or Indeed searches, which I did not do.
- Company-level hiring evidence for Netflix, Amazon, Meta and Airbnb causal teams was not retrieved in this pass; see Q3 for Uber.

## Q3. Practitioner writing: what questions practitioners actually ask (intervention effects versus full graphs; "which causes, how sure")

### Takeaway
- Industry engineering writing consistently frames causal work as estimating intervention and heterogeneous treatment effects (uplift, CATE, diff-in-diff, regression discontinuity), not learning full graphs.
- Where graphs appear, domain experts draw them to state assumptions; they are not discovered from data.
- This supports H2.
- Hard evidence that business users want "which causes, how sure" is thin: only vendor rhetoric and practitioner essays.

### Cited Findings
- [primary, engineering blog | 2019-06-19 | ride-hailing / marketplace | H2 | +] Uber, "Using Causal Inference to Improve the Uber User Experience". Source: [Uber blog](https://www.uber.com/blog/causal-inference-at-uber/).
  - Use cases are effects of interventions such as email campaigns and surge-pricing changes, using CUPED, CACE, diff-in-diff, interrupted time series, IV and regression discontinuity.
  - Uplift modelling for heterogeneous effects is "one popular approach at Uber", and Uber open-sourced it as CausalML ([arXiv 2002.11631](https://arxiv.org/pdf/2002.11631)).
  - Causal graphs are built "with domain expert input", not discovered.
- [primary, arXiv | 2020-07-21 | streaming (Netflix-affiliated author) | H2 | +] Jeffrey C. Wong, "Computational Causal Inference". The abstract frames the field as computing many causal effects on massive datasets. The abstract itself does not name Netflix; the affiliation comes from search-result context ("Computational Causal Inference at Netflix"). Sources: [arXiv 2007.10979](https://arxiv.org/abs/2007.10979); related Netflix-affiliated papers on HTE in large experiments, [arXiv 2111.01223](https://arxiv.org/pdf/2111.01223) and [arXiv 2206.04907](https://arxiv.org/pdf/2206.04907) (titles only, not fetched).
- [practitioner essay | 2024-01-17 | general industry DS | H2 | +] Zijing Zhu, Towards Data Science, "How is causal inference different in academia and industry". Source: [TDS](https://towardsdatascience.com/how-is-causal-inference-different-in-academia-and-industry-fb5afd12e2e7).
  - Industry prioritises speed ("time is money") and individual treatment effects for targeting decisions.
  - Success is judged by live KPIs.
  - Expert-specified causal structure and transparency about assumptions are needed in both settings.
- [vendor claim | 2024-09-12 | enterprise / telecom example | H2, H1 | +] causaLens and Google Cloud press release. Source: [BusinessWire](https://www.businesswire.com/news/home/20240912382958/en).
  - Pitches causal AI as a "grounding" layer for LLMs on three tasks: causal inference, counterfactual "what if", and interventions that recommend actions. The example: are outages or pricing driving churn, and what is the effect of improving reliability?
  - The CEO says it will "unlock trust in Generative AI".
  - The release reports no adoption data.

### Inferences
- The industrial causal stack that gets publicised (experimentation, uplift, CATE) answers H2-style questions. That supports positioning the audited tools' output as "effect of X, with confidence and evidence source" rather than "a DAG".
- The Uber and TDS pattern of expert-drawn graphs suggests practitioners already treat structure as an assumption to be justified. This is weakly consistent with H1: provenance per edge resembles "who asserted this assumption".

### Gaps
- No KDD or CLeaR industry-track paper was found that quantifies which questions business users ask. This is a gap, not a negative finding.
- No public study measures demand for "which causes, how sure". The interview-study search returned visualisation papers such as Causalvis ([arXiv 2303.00617](https://arxiv.org/pdf/2303.00617)), which I did not fetch.
- Amazon, Meta, Airbnb, DoorDash and Microsoft (EconML/DoWhy) causal blogs were not fetched in this pass.

## Q4. Willingness to pay for AI audit, assurance, evaluation and provenance

### Takeaway
- Buyers demonstrably pay for LLM evaluation and observability:
  - Braintrust raised $80M at an $800M valuation (Feb 2026);
  - Arize raised a $70M Series C (Feb 2025);
  - Langfuse was acquired by ClickHouse with a claimed 2,000+ paying customers (Jan 2026);
  - Patronus raised a $17M Series A (2024).
- The UK government estimates its AI assurance market at about £1.01bn across 524 firms, but describes demand as "below potential".
- The cost of missing provenance is visible: about 1,600 court cases worldwide involve AI-hallucinated citations, with sanctions.
- This supports H3 in general terms. No evidence was found of anyone paying specifically for causal-claim or name-reliance audits.

### Cited Findings
- [second-hand, Axios Pro | 2026-02-17 | AI evaluation / observability | H3 | +] Braintrust raised an $80M Series B at an $800M post-money valuation, led by Iconiq. The article does not state customers or revenue. Source: [Axios](https://www.axios.com/pro/enterprise-software-deals/2026/02/17/ai-observability-braintrust-80-million-800-million).
- [vendor claim / primary announcement | 2025-02-20 | AI observability | H3 | +] Arize AI raised a $70M Series C led by Adams Street, with M12, Datadog and PagerDuty participating. Source: [Arize blog](https://arize.com/blog/arize-ai-raises-70m-series-c/).
  - Self-described as "the largest-ever investment in AI observability".
  - Claims Phoenix OSS has more than 2 million monthly downloads. Both are vendor claims.
- [primary announcement / vendor claim | 2026-01-26 | LLM observability | H3 | +] Langfuse was acquired by ClickHouse; terms undisclosed. Source: [Orrick](https://www.orrick.com/en/news/2026/01/open-source-llm-observability-langfuse-acquired-by-clickhouse-inc).
  - Claims: more than 2,000 paying customers, more than 26M SDK installs per month, and use by 19 of the Fortune 50. All are vendor claims.
  - A HackerNoon piece frames the space as "two acquisitions deep, two still standing" ([HackerNoon](https://hackernoon.com/two-acquisitions-deep-two-still-standing-whats-really-happening-to-open-source-llm-observability)); not fetched.
- [primary announcement | 2024 | LLM evaluation / hallucination detection | H3 | +] Patronus AI raised a $17M Series A led by Notable Capital, with Lightspeed and Datadog. Source: [Patronus blog](https://patronus.ai/blog/announcing-our-17-million-series-a).
- [primary government report, via law-firm summary | DSIT report Nov 2024; summary 2024-11-22 | AI assurance, UK | H3 | + / ~] UK AI assurance market, from DSIT's "Assuring a Responsible Future for AI". Sources: [Burges Salmon summary](https://www.burges-salmon.com/articles/102jph1/ai-assurance-the-uk-market-and-government-actions-dsit-report/); [primary PDF](https://assets.publishing.service.gov.uk/media/672a2ca440f7da695c921b7c/Assuring_a_Responsible_Future_for_AI.pdf) (not fetched directly).
  - 524 firms, 84 of them specialised (up from 17 in 2023); about £1.01bn; 12,572 employees; potential above £6.53bn by 2035.
  - Demand-side barriers: buyers' limited understanding of AI risks and of the value of assurance; demand and supply "below their potential"; unclear tool quality.
- [primary journalism plus crowd-sourced database | 2026-06-16 | legal | H1 | +] Damien Charlotin's database counts about 1,600 court cases in 35 countries involving AI-hallucinated citations (US 1,116), roughly eight times the previous year. Sanctions include a US$8,000 fine and a two-year bar in Mississippi in June 2026. Source: [Malay Mail](https://www.malaymail.com/news/tech-gadgets/2026/06/16/do-your-job-global-courts-face-rising-tide-of-ai-generated-fake-cases-and-quotes/223865).
  - This is evidence of the cost of unverified claims, not of willingness to pay for provenance.
- [survey, n=100 CIOs | 2025-06-10 | enterprise | H3 | ~] a16z: enterprise LLM budgets are expected to grow about 75%, and spending has moved from innovation budgets (25% down to 7%) into core budgets. CIOs are wary of outcome-based pricing. Source: [a16z](https://a16z.com/ai-enterprise-2025/).

### Inferences
- There is a funded, growing category for "evaluate the LLM before trusting it": hundreds of millions of dollars in rounds, and two exits in 2025-26 if Statsig, as an adjacent experimentation tool, is counted.
- A name-reliance or semantic-dependence audit for causal tools would sit inside this category as a specialised evaluation. H3 is plausible by analogy but unproven. The UK report's "demand below potential" warns that assurance buyers often do not yet understand what they would be buying.
- Legal-sector hallucination sanctions are the clearest case where missing per-claim provenance carries a measurable penalty. That is a cross-sector analogue for H1.

### Gaps
- No public evidence of buyers paying a premium specifically for citations or provenance in AI answers, for example a pricing tier gated on citations.
- No global AI-assurance market size from a non-vendor source. Market-research-firm numbers were not pursued because they are typically paywalled and unverifiable.
- Galileo funding and model-risk-management (SR 11-7) spend figures were not retrieved.

## Q5. Counter-evidence: buyers not caring about provenance or abstention, preferring speed, or causal-AI products failing

### Takeaway
- Several signals cut against the hypotheses:
  - Microsoft archived ShowWhy, its no-code causal-analysis tool, in Dec 2025 as "research efforts that are no longer active".
  - causaLens, the best-known causal-AI vendor, now describes itself in boilerplate as a "Digital Workers" (agentic) company. "Causal reasoning" is demoted to a feature.
  - Enterprise buyers rank capability and price above accuracy when choosing models.
  - Practitioners emphasise speed.

### Cited Findings
- [primary | archived 2025-12-17 | causal analysis tooling (Microsoft Research) | H2, H3 | −] The microsoft/showwhy repository was archived on Dec 17, 2025. The README says: "the result of research efforts that are no longer active", "no longer maintained or accepting contributions". It does not state why. Source: [GitHub microsoft/showwhy](https://github.com/microsoft/showwhy).
- [vendor claim / primary press release | 2026-05-06 (from URL date) | biopharma commercialisation | H2, H3 | −] causaLens and Syneos Health. Source: [BusinessWire](https://businesswire.com/news/home/20260506514597/en/causaLens-Expands-Strategic-Partnership-with-Syneos-Health-to-Scale-Agentic-AI-in-Biopharma-Commercialization).
  - The boilerplate reads "causaLens delivers Digital Workers that enterprises can rely on", with no "causal AI" label.
  - The body still claims "causal reasoning, a field we pioneered".
  - Reports over $50M raised; no customer metrics.
  - Its 2023 launch called its product "the first operating system for decision making powered by Causal AI" ([causaLens blog](https://causalai.causalens.com/resources/blog/causalens-launches-the-first-operating-system-for-decision-making-powered-by-causal-ai/)). That is a repositioning over about three years.
- [secondary, Wikipedia citing Gartner and VentureBeat | 2022 | general | H3 | ~] Gartner first included causal AI in its 2022 Hype Cycle for Emerging Technologies. Its later phase was not retrieved; the Gartner hype-cycle documents are gated abstracts. Source: [Wikipedia, Causal AI](https://en.wikipedia.org/wiki/Causal_AI).
- [survey, n=100 | 2025-06-10 | enterprise | H1 | −] a16z: "for most tasks, all the models perform well enough now—so pricing has become a much more important factor". Security and cost gained ground on accuracy and reliability. Source: [a16z](https://a16z.com/ai-enterprise-2025/).
- [survey, n not stated | 2025-09-23 | enterprise software buyers | H1 | −] Futurum: the top purchase criteria are capabilities, features and pricing. Trust, explainability and governance do not appear in the reported criteria. Source: [Futurum](https://futurumgroup.com/press-release/genai-features-are-the-top-criteria-for-future-enterprise-software-purchases/).
- [practitioner essay | 2024-01-17 | industry DS | H1 | −] "Time is money": industry wants a quick benchmark model, refined later. Source: [TDS](https://towardsdatascience.com/how-is-causal-inference-different-in-academia-and-industry-fb5afd12e2e7).
- [primary government report summary | 2024-11 | UK assurance | H3 | −] Buyers have limited understanding of the value of AI assurance, and demand is "below potential". Source: [Burges Salmon](https://www.burges-salmon.com/articles/102jph1/ai-assurance-the-uk-market-and-government-actions-dsit-report/).
- [survey, vendor-run, n=114 | 2026-06 | data leaders | H1 | ~] insightsoftware: 19% report no issues with AI, and the top barrier is security and governance, not accuracy. Source: [insightsoftware](https://www.insightsoftware.com/blog/why-dont-data-leaders-trust-ai-and-other-insights-from-our-2026-ai-survey/).

### Inferences
- "Causal AI" as a standalone product category shows signs of weak demand: one big-tech tool archived, and the flagship vendor rebranded toward agents.
  - That cuts against selling causal discovery itself.
  - It does not directly cut against H3, which is about auditing LLM tools; that category is funded (Q4).
- The most defensible framing is "evaluation and assurance for LLM causal claims", which rides the funded evaluation market, rather than "a better causal-AI product".

### Gaps
- No public post-mortem or stated reason for ShowWhy's archival.
- I did not find funding-round data, layoffs or revenue for causaLens after 2024. Over $50M raised is self-reported.
- Other causal-AI vendors (Geminos, Howso, cStructure and others) were not checked.

## Q6. Community discussion (Reddit, HN, LinkedIn) on LLMs doing causal analysis — ANECDOTE ONLY

### Takeaway
- Community discussion found in this pass is low-volume.
- An HN Algolia search for "LLM causal discovery" returned only 4 stories, none about trust in LLM causal analysis.
- The only large-scale evidence is an academic analysis of 230,576 Reddit posts (2022-2025) on generative AI trust in general. It finds trust and distrust nearly balanced, driven mainly by technical performance and personal experience. It is not specific to causal analysis.

### Cited Findings
- [anecdote volume / primary data pull | queried 2026-10-13 | HN | H1-H3 | ~] HN Algolia "LLM causal discovery", stories only: 4 hits, none on the topic. The top hit was "Launch HN: Undermind" (292 points, 2024-07-25), about scientific-paper discovery. Source: [HN Algolia API](https://hn.algolia.com/api/v1/search?query=LLM%20causal%20discovery&tags=story&hitsPerPage=20).
  - This is a low-volume result for this exact phrasing only. Broader queries such as "causal inference" and "correlation causation LLM" were not run on HN.
- [primary academic analysis of community data | 2025-10-17; v2 2026-03-23 | general public and experts on Reddit | H1 | ~] Pessianzadeh et al., "In Generative AI We (Dis)Trust?". Source: [arXiv 2510.16173](https://arxiv.org/abs/2510.16173).
  - Dataset: 230,576 posts, 39 subreddits, 2022-2025.
  - Trust and distrust are nearly balanced, with trust modestly ahead, and shift around model releases.
  - Technical performance and usability dominate; personal experience is the most frequent reason.
- [academic, not demand | various | research | context only] Academic work on LLM causal unreliability, which community threads tend to cite:
  - "Can LLMs Infer Causation from Correlation?" ([arXiv 2306.05836](https://arxiv.org/pdf/2306.05836));
  - "On the Reliability of LLMs for Causal Discovery" ([arXiv 2407.19638](https://arxiv.org/html/2407.19638v2));
  - "LLM Cannot Discover Causality…" ([arXiv 2506.00844](https://arxiv.org/html/2506.00844v1)).
  - These support the capstone's technical finding. They are not demand evidence.

### Inferences
- The scarcity of public practitioner chatter on "LLMs doing causal discovery" is itself a weak signal. The use case is niche among practitioners, consistent with H2: people ask effect questions, not discovery questions.
- No anecdote was found that supports or contradicts name reliance specifically.

### Gaps
- Reddit (r/datascience, r/statistics, r/CausalInference) was not searched directly. Search engines surfaced academic papers instead of threads, and Reddit pages were not fetched.
- LinkedIn content is not publicly fetchable.
- No anecdote quotes are included, because no qualifying thread was retrieved. Quoting from memory would risk fabrication.
