Tickets: AUD-22, STR-06

Written 2026-10-12 by an audit agent; sources read on that date.

# AU5: Commercial applications of causal discovery and causal analysis

## Question

Who sells or buys causal discovery and causal analysis today, for which decisions, with what claimed guarantees, at what price model, and where does it fail in practice? Which guarantee (accuracy, calibrated uncertainty, abstention, provenance/audit trail, speed, cost) do buyers actually pay for?

## Method

- Desk research: 54 web searches (listed at the end) and about 75 pages opened. Two more searches were planned but not run because the shared search budget ran out. Every URL cited was opened on 2026-10-12. Anything not opened is listed under "Not read".
- Inclusion rule: (a) products or internal systems sold or used as "causal" analysis for a real decision; (b) buyer-side evidence such as purchases, acquisitions, surveys and regulator requirements; (c) independent evaluations of those product classes. Pure academic methods are left out unless they come from or are deployed in industry.
- Labels: `claim (vendor)` covers marketing, press releases, pricing pages and vendor-authored blogs. `reported` covers authors' own paper or table, including vendor-authored arXiv papers, which are flagged as self-evaluations. `second-hand` covers someone else's summary (analysts, news, price aggregators).
- Prior notes checked: cluster9 (section 5: causaLens homepage pivot, ShowWhy archived) and cluster2/5. This audit extends them. The cluster9 observation about causaLens was confirmed again today.
- Distinction kept throughout. **Discovery** means learning the graph from data. **Effect estimation** means estimating effects with a graph or design that is given (A/B tests, DiD, synthetic control, MMM, ANCOVA). **RCA** means ranking root causes over a graph, which in practice is almost always declared topology.

## Findings

### F1. Most of the money is in effect estimation with a design, not in discovery

- **Experimentation platforms.** These are the largest priced deals found:
  - Statsig was acquired by OpenAI for $1.1B, announced Sept 2025 (second-hand, AI Business).
  - Eppo was acquired by Datadog in May 2025 at a reported ~$220M (second-hand; a competitor's blog notes that no price was confirmed).
- **Marketing incrementality and MMM.**
  - Vendr data puts Haus's median annual contract at $150,000, range $132k–168k (second-hand).
  - Google Meridian and Meta Robyn are free and open source.
  - Survey: 46.9% of US marketers plan more MMM investment, and 52% already run incrementality tests (second-hand, EMARKETER/TransUnion, July 2025).
- **Pharma real-world evidence.**
  - Aetion was acquired by Datavant (May 2025, price not stated).
  - Unlearn's PROCOVA is a covariate-adjusted RCT design that EMA qualified in Sept 2022.
- **Market size.** The "causal AI" category is sized at USD 56.2M in 2024, rising to 456.8M by 2030 (second-hand, MarketsandMarkets, Dec 2024). That is small next to the experimentation exits above. The category as defined leaves out experimentation and MMM.

### F2. Commercial "causal AI" for root cause analysis runs on declared topology, not learned graphs

- **Dynatrace.** Davis runs fault-tree analysis over Smartscape, a real-time dependency graph (docs).
- **New Relic.** iRCA uses a "topology graph" plus path ranking (vendor blog, Feb 2026).
- **IBM Instana.** RCI runs a Beta-Binomial health model over traces and dependency topology (reported, arXiv 2502.18240).
- **Causely.** Maps "known failure paths" (claim (vendor)).
- **Groot.** The e-commerce RCA system uses SRE-written rules (reported: 78% top-1, 95% top-3 on 952 incidents).
- **Industrial vendors.** Parabole.ai builds graphs from manuals and interviews. Ethon encodes process structure (second-hand, ARC).

In the project's space this is R = K (declared knowledge): the graph is supplied and only ranking or attribution is computed. It matches our own result that a few bits of order knowledge (0.714) beat every published data-only method on CausalArena.

### F3. Independent evaluations of data-driven causal RCA are poor, and vendors publish no precision or recall

- **RCAEval (WWW 2025, preliminary table, reported).** Metric-based causal-discovery RCA methods score AC@1 0.09–0.32. The non-causal baseline BARO scores 0.67.
- **"How far are we?" (arXiv 2408.13729).** Covers 9 discovery and 21 RCA methods; no method is best overall.
- **Vendor accuracy figures:**
  - Causely's "100% fault accuracy" comes from its own benchmark: one 24-service demo app with injected faults (75% → 100% with Causely, arXiv 2605.18327).
  - Datadog and New Relic publish no accuracy rate.
  - A competitor critique found no production precision or recall published by AI incident-response vendors, including its own author's firm (second-hand, incident.io).
- **What is quoted instead:**
  - Speed: "minutes not hours", −63% time-to-diagnosis, "up to 95%" faster resolution.
  - Token or cost reduction: −48% to −60% tokens.

### F4. Graph discovery itself is relied on in only a few documented places, and none publishes graph accuracy

- **Amazon supply chain.** PC on observational data, then DoWhy GCM SCMs for KPI attribution (reported, KDD 2025 AI4SC workshop abstract). Graphs are checked with falsification tests and compared to a DAG from business definitions or an LLM. No graph accuracy figure is given.
- **Xplain Data "Causal DiscoveryBot".** Runs autonomous discovery over production data. Customers are Schaeffler and TRUMPF (second-hand, ARC). Claimed time-to-root-cause falls from weeks to under 2 h (second-hand). No metrics.
- **Aitia REFS / Gemini Digital Twins.** Causal models learned from omics and clinical data for target discovery (Ono deal, 2 Sept 2026, terms undisclosed). Claim (vendor): "true disease mechanisms". No validation stated.
- **causaLens decisionOS.** Offered "human-guided causal discovery" (G-Cloud 14 listing). The only contractual guarantee was 99% uptime, with no accuracy guarantee. The vendor has since repositioned to LLM "Digital Workers" (homepage).
- **Telecom alarm RCA (research for industry).** HPCI learns alarm graphs with Hawkes processes and CI tests. EvoCause has an LLM edit a PC graph using past expert diagnoses. **Replacing alarm titles with anonymous IDs lowers EvoCause Node F1 by 6.12 points** (reported, arXiv 2607.27290). This is the same name dependence we measured in Causal-Copilot (0.306 → 0.232 → 0.142).
- **Manufacturing research.** Seagate wafer data and assembly-line studies use temporal and domain constraints (tiers). Validation is engineers' agreement, not ground truth (reported).

Wherever discovery is used, the "guarantee" is expert sign-off or falsification tests, and the speed or value claims are vendor-reported. No buyer-facing graph-accuracy claim was found.

### F5. What buyers pay for differs by sector

| Sector | What is priced or demanded | Evidence |
|---|---|---|
| IT / SRE | **Speed and cost per investigation**, plus "deterministic / no hallucination" | Datadog Bits Investigation at ~6.5 AI credits each (≈$6.50–8.45, claim (vendor)); Causely $2,000/month for up to 500 services (claim (vendor)); claims are framed as time and tokens |
| Marketing | **Accuracy validated against experiments** (experiments as ground truth; calibration of MMM with lift tests; published out-of-sample forecast accuracy) | Haus, Meridian (experiments as priors), Recast ("95%+" holdout accuracy, weekly backtests visible to clients, claim (vendor)); ~$150k ACV (second-hand) |
| Pharma / regulators | **Provenance, pre-specification, audit trail, and guarantees that survive model error** | FDA ECT draft (protocol before analysis, audit trails, all data sources documented); EMA RWD paper (TTE, pre-specified sensitivity analyses, public code); PROCOVA admitted because it stays an unbiased ANCOVA whatever the ML model's quality |
| Banking | **Documentation, effective challenge, outcomes analysis** | SR 26-2 (17 Apr 2026) supersedes SR 11-7, but footnote 3 puts generative and agentic AI out of scope |
| Enterprise "causal AI" platforms | **Audit-readiness and ROI** language replaces accuracy | causaLens Digital Workers: "audit-ready reliability", "Always Accurate", "5x ROI" (claim (vendor), no evidence) |

**Calibrated uncertainty and abstention are almost never sold as features.** Only two abstention-like behaviours were found:
- IBM Instana reports low confidence when telemetry is sparse instead of guessing (reported).
- Causaly says its retrieval system recognises no-answer cases (claim (vendor)).

Lifesight's MCP into Claude and ChatGPT logs every query in an audit trail (claim (vendor), June 2026). It is the clearest sign that LLM front-ends are being sold with provenance attached.

### F6. Failure modes documented in practice

- **MMM.** In a simulation, a standard MMM put paid-search ROAS at 10.61x against a true 4.20x, and its 90% interval excluded the truth. Experiment-based structural estimation recovered 4.14x (second-hand report of arXiv 2608.21128; the abstract itself has no numbers). Recast's own post says no MMM can guarantee being right.
- **RWE.** RCT-DUPLICATE found database estimates tracked RCT estimates at r = 0.82 overall, 0.93 where the design could be closely emulated, and 0.53 otherwise (second-hand of Wang et al., JAMA 2023). Failure concentrates where design elements cannot be emulated.
- **RCA:**
  - Dynatrace docs admit duplicate problems and fixed merge windows.
  - Datadog admits earlier agents were distracted by suspicious signals and stopped at surface causes.
  - An Omdia analyst says Dynatrace's causal claims need customer proof.
- **Platform churn.** Microsoft ShowWhy, the only big-vendor no-code discovery UI, was archived on 17 Dec 2025. causaLens repositioned away from decisionOS. Robyn calls itself "experimental".

## Typed table

The full typed rows (42, all fields, sources) are in `AU5_commercial.json`. Compressed view:

| id | name | vendor | method_family | uses_llm | headline claim (label) | pricing | main criticism |
|---|---|---|---|---|---|---|---|
| C01 | decisionOS | causaLens | both | yes | 3–10x faster to value (claim (vendor)); uptime-only SLA | £240k/licence/yr (claim (vendor)) | no accuracy guarantee; product de-emphasised |
| C02 | Digital Workers | causaLens | unknown | yes | "Always Accurate", 5x ROI (claim (vendor)) | not public | no evidence |
| C03 | Manufacturing RCA case | causaLens | both | no | $15M downtime saved (claim (vendor)) | n/a | no metrics |
| C04 | CauseWay / PathWay Rail | Geminos | both (LLM-assisted) | yes | 40% of delay scenarios at launch (claim (vendor)) | not public | interview-based |
| C05 | Causely | Causely | RCA (known failure paths) | context for agents | 100% fault accuracy; 75→100% (reported, self) | $2,000/mo ≤500 services | self-benchmark, one demo app |
| C06 | Davis / RCA | Dynatrace | RCA over topology | no | "answers, not guesses" (claim (vendor)) | not read | duplicates; needs proof (analyst) |
| C07 | Watchdog RCA | Datadog | RCA | no | minutes not hours (claim (vendor)) | bundled | none independent |
| C08 | Bits AI SRE | Datadog | RCA (LLM hypothesis loop) | yes | up to 95% faster TTR (claim (vendor)) | ~6.5 credits/investigation | early wrong root causes admitted |
| C09 | iRCA | New Relic | RCA over topology | no | "high-accuracy" (claim (vendor)) | not read | no numbers |
| C10 | Instana RCI | IBM | RCA (Bayesian, topology) | no | ~90% identified; reports low confidence (reported) | not read | internal only |
| C11 | Groot | e-commerce firm | RCA (rules) | no | 78% top-1, 95% top-3 (reported) | internal | rule upkeep |
| C12 | Telecom alarm RCA / EvoCause | authors (Huawei-linked, unconfirmed) | discovery + RCA | EvoCause yes | name anonymisation −6.12 Node F1 (reported) | n/a | name dependence |
| C13 | Model-monitoring RCA | Fiddler | not causal | no | — | not read | attribution, not causal |
| C14 | DoWhy gcm RCA | Amazon/PyWhy | both | no | internal use (claim (vendor)) | free | graph source unstated |
| C15 | Supply-chain attribution | Amazon | discovery (PC) + SCM | partly | falsification-tested DAG (reported) | internal | no numbers |
| C16 | Azure RAI causal analysis | Microsoft | effect est. (DML) | no | CIs under no hidden confounding (claim (vendor)) | Azure ML | assumes observed confounders |
| C17 | ShowWhy | Microsoft | both | no | — | free | archived Dec 2025 |
| C18 | Causica | Microsoft | both | no | — | free | refactor, no releases |
| C19 | CausalImpact | Google | effect est. (BSTS) | no | posterior intervals (reported) | free | design assumptions |
| C20 | Meridian | Google | effect est. (Bayesian MMM) | no | experiment-calibrated (claim (vendor)) | free | no independent validation |
| C21 | Robyn | Meta | effect est. (MMM) | port via LLM | "experimental" | free | beta Python port |
| C22 | CausalML | Uber | effect est. (uplift) | no | — | free | — |
| C23 | Haus | Haus | effect est. (geo exp., synth. control) | yes | 4x more precise (claim (vendor)) | ~$150k ACV (second-hand) | none independent |
| C24 | Recast | Recast | effect est. (MMM + lift) | no | 95%+ holdout accuracy (claim (vendor)) | not public; est. (second-hand) | "no MMM can guarantee" (vendor) |
| C25 | Lifesight + MCP | Lifesight | effect est. | yes | audit-trail logging (claim (vendor)) | not public | no accuracy evidence |
| C26 | MMM in practice | many | effect est. | varies | 10.61x vs true 4.20x ROAS (second-hand, simulation) | — | overstatement, wrong intervals |
| C27 | Statsig | OpenAI | effect est. (A/B) | no | — | — | — |
| C28 | Eppo | Datadog | effect est. (A/B) | no | — | — | — |
| C29 | REFS / Gemini Digital Twins | Aitia | discovery | n/s | "true disease mechanisms" (claim (vendor)) | undisclosed | no validation stated |
| C30 | Aetion | Datavant | effect est. (RWE) | some AI | regulator-accepted RWE (claim (vendor)) | not public | — |
| C31 | RCT-DUPLICATE | academic/FDA | effect est. (TTE) | no | r 0.82 / 0.93 / 0.53 (second-hand) | — | weak where not emulable |
| C32 | PROCOVA | Unlearn | effect est. (ANCOVA + ML) | no | EMA-qualified; unbiased (regulator / claim (vendor)) | not public | optimistic power possible |
| C33 | Bio Graph | Causaly | literature K graph | yes | 70M directional relations; cited answers (claim (vendor)) | not public | no extraction accuracy |
| C34 | FDA buys BayesiaLab | FDA (buyer) | both (BN) | no | expert causal diagrams (buyer req.) | 2 licences | — |
| C35 | Causal DiscoveryBot | Xplain Data | discovery | no | weeks → <2 h (second-hand) | not read | no metrics |
| C36 | Parabole.ai, Ethon | — | RCA from K | unknown | >$10M at Siemens (second-hand) | not read | promotional |
| C37 | Wafer / assembly-line SL | Seagate data, academics | discovery + tiers | no | engineer-validated (reported) | n/a | no ground truth |
| C38 | RCAEval / How far are we | academic | evaluation | no | causal AC@1 0.09–0.32 vs BARO 0.67 (reported) | — | causal RCA underperforms |
| C39 | Incident-AI claims critique | incident.io | RCA (LLM) | yes | no precision/recall published (second-hand) | per user | competitor-written |
| C40 | Event attribution (WWA) | WWA | effect est. (probability ratio) | no | 8-step protocol, bootstrap CIs (reported) | non-profit | — |
| C41 | Earth-science discovery | academic | discovery (time series) | no | review (reported) | — | — |
| C42 | Market size | MarketsandMarkets, theCUBE | — | — | $56.2M→$456.8M; >$1B 2030 (second-hand) | — | paid reports, method unread |

## Requested sections

### (1) Where graph discovery itself is what customers rely on, and what is claimed

Graph discovery is relied on only in rows C12, C15, C29, C35 and C37, plus C01 historically:
- supply-chain KPI attribution at Amazon
- manufacturing quality drivers (Xplain Data, wafer and assembly-line studies)
- telecom alarm graphs
- pharma target discovery (Aitia)
- causaLens's "human-guided discovery"

In every case the claimed guarantee is one of three things:
- validation by experts or falsification tests (Amazon, Seagate)
- a speed or value number (Xplain Data weeks → <2 h; causaLens $15M)
- a mechanism claim with no evidence (Aitia)

**No vendor or deployed system publishes edge-level accuracy, calibration, or abstention for the learned graph.** Where graphs drive automated decisions at scale (IT RCA), vendors replaced discovery with declared topology or rules. Where discovery has been benchmarked independently (RCAEval), it loses to a simple non-causal baseline.

### (2) What an "auditable causal analyst" would replace or complement, and for whom

Here an auditable causal analyst means: every claim has an evidence source; claims are calibrated; the analyst can abstain.

- **Complement, not replace, the IT RCA incumbents.**
  - Incumbents own the topology (K) and the telemetry. An auditable layer adds per-claim provenance and abstention to LLM investigation agents (Datadog Bits, Causely MCP context).
  - Buyers there are quoted speed and tokens, so the layer must not slow investigations down.
  - Who: SRE platform teams already paying per investigation.
- **Complement marketing measurement.**
  - Tag each channel-effect claim as one of: experiment-backed, prior-only, or observational fit.
  - Abstain or flag where no experiment supports the claim.
  - This makes the Haus, Recast and Meridian "calibrate with experiments" practice explicit at claim level. The MMM-overstatement result (C26) is the failure it targets.
  - Who: growth and finance teams reconciling MMM against lift tests, and agencies certified on Meridian.
- **Complement regulated RWE and model validation.**
  - Generate the pre-specified assumption ledger, the data-source log and the bias-analysis record that FDA's ECT draft, FDA's AI credibility report and EMA's RWD paper ask for. It does not replace the epidemiologist's design.
  - Who: RWE teams at sponsors and CROs, and model-validation teams.
  - Caveat: under SR 26-2, LLM agents are outside model-risk guidance and fall to "broader risk governance". An LLM analyst sold to banks therefore has no ready-made validation route.
- **Replace little.** The only "replace" candidates are the no-code causal-discovery UIs that have been abandoned (ShowWhy) or repositioned (decisionOS). Their demise is weak evidence of demand for discovery alone.

### (3) Market-size statements (all second-hand)

- MarketsandMarkets (press release, 13 Dec 2024): causal AI at USD 56.2M in 2024, rising to USD 456.8M by 2030 (CAGR 41.8%). BFSI is named the largest vertical.
- theCUBE Research (15 Mar 2025): over $1B by 2030 at 41% CAGR.
- Dataiku/Databricks survey (June 2023, n = 400 senior AI professionals at >$3B companies): a chart lists "Causal AI" at 59% for "AI Pioneers" versus 32% for others. The metric label is unclear in the PDF read. The "16% use / 33% experimenting" figures quoted by theCUBE were not found in that PDF.
- Methodologies were not read. Note that these definitions exclude experimentation and MMM spend, where the deal values seen in F1 are larger.

### (4) Regulatory hooks that reward provenance and uncertainty

- **FDA draft guidance, Externally Controlled Trials (Feb 2023).**
  - Protocol and SAP must be final before analysis; changes must be date-stamped and justified.
  - Every data source considered must be documented, along with why it was chosen.
  - Audit trails of data access and analyses are recommended.
  - Quantitative bias analysis; patient-level data goes to FDA.
  - This is the closest regulatory analogue to a claim ledger.
- **FDA final guidance, RWD from EHR and claims (July 2024).** Fitness-for-use of RWD. Full PDF not read.
- **FDA draft guidance on AI for drug and biologic regulatory decisions (7 Jan 2025).**
  - Context of use; model risk = model influence × decision consequence.
  - A credibility plan and a credibility assessment report are required.
  - Data must be traceable. FDA notes the uncertainty of model outputs is hard to quantify.
  - A causal analyst's "model influence" can be lowered by design if it abstains.
- **EMA reflection paper on RWD in non-interventional studies.**
  - The PDF read is the 15 Apr 2024 consultation draft; RAPS reports adoption on 17 March (article dated 8 Apr 2025).
  - It recommends target-trial emulation, pre-specified sensitivity and bias analyses, negative controls, public analysis code and study registration.
- **EMA PROCOVA qualification (Sept 2022), with FDA comment (vendor post, Jan 2024).** ML is admitted when the inferential guarantee holds whatever the ML quality, because PROCOVA remains an ANCOVA.
- **EU AI Act.**
  - Art. 12 requires automatic logs over the system's lifetime.
  - Art. 13 requires declared accuracy levels and metrics, the known circumstances that affect accuracy, and output deployers can interpret.
  - A provisional Digital Omnibus deal (reported May 2026) moves Annex III high-risk obligations to 2 Dec 2027 and Annex I to 2 Aug 2028. Final adoption was not verified.
- **US banking: SR 26-2 (17 Apr 2026, Fed/OCC/FDIC).**
  - It supersedes SR 11-7 and SR 21-8.
  - It keeps documentation, effective challenge, outcomes analysis and back-testing, and validation of vendor models.
  - **Generative and agentic AI are explicitly out of scope (footnote 3).** A vendor explainer (Openlayer) says the opposite; the primary text wins.

### (5) Three candidate product angles, ranked by evidence of demand

1. **Claim-level evidence ledger for marketing measurement.** Each channel-effect claim carries its source (geo experiment, MMM prior, or observational fit), with calibrated intervals and abstention when it is not experiment-backed.
   - Demand evidence:
     - ~$150k ACV at Haus (second-hand)
     - Statsig at $1.1B and Eppo at ~$220M (second-hand)
     - 46.9% of marketers plan more MMM spend (second-hand)
     - vendors already sell "validation" (Recast) and "experiments as ground truth" (Haus)
     - documented MMM overstatement (C26)
     - LLM front-ends with audit trails already exist (Lifesight MCP)
   - Fit to our work: moderate. This is effect estimation, not discovery.
   - Risk: incumbents already do coarse versions.
2. **Provenance and abstention layer for LLM SRE investigation agents.** Each root-cause claim is tagged as topology (K), telemetry pattern (D) or intervention (I, e.g. a rollback or feature flag), with an "insufficient evidence" output.
   - Demand evidence:
     - per-investigation pricing (Datadog)
     - Causely's $2k/month and its pitch of "deterministic context" for agents
     - Gartner Cool Vendor category
     - Dynatrace, New Relic and IBM all investing
   - Fit: high. It maps directly onto the D/I/K ledger.
   - Risk: incumbents own topology and data; buyers are quoted speed, not calibration; no buyer was found paying for abstention.
3. **Assumption and provenance ledger for regulated causal studies.** Pre-specification records, a data-source log, bias-analysis records, and an FDA-style credibility report for any AI component.
   - Demand evidence:
     - strongest regulatory hooks (FDA ECT, FDA AI credibility, EMA RWD paper, EU AI Act Art. 12–13)
     - Aetion acquisition
     - PROCOVA precedent
   - Fit: good on provenance, weak on discovery; regulators want pre-specified designs, not learned graphs.
   - Risk: slow sales; generative and agentic AI are outside SR 26-2 in banking.

## What this changes for the project

1. **Positioning (STR-06).** Pitch the claim ledger as an evidence and audit layer for causal claims. Do not pitch it as a better discovery engine. No commercial buyer was found paying for graph accuracy, and no vendor publishes it. Add one sentence to the scope note saying so, citing F4.
2. **Headline guarantee.** Frame "never below its data-only output" in the PROCOVA way: the guarantee holds whatever the LLM or knowledge source does. This is the property regulators have already accepted for ML (EMA qualification; FDA's "special case of ANCOVA"). Add it to the design doc as the safety property, with the regulatory precedent cited.
3. **The Atlas should state that industry RCA is R = K.** Commercial "causal AI" for RCA mostly ranks over declared topology (Dynatrace, New Relic, Instana, Causely, Groot). This mirrors our 0.714 order-knowledge result. Add it to the Atlas value layer (AU5 slab): "declared knowledge is the industrial norm; the open problem is auditing it".
4. **Name-swap audit as a portable product test (AUD-22).** EvoCause loses 6.12 Node F1 when alarm names are anonymised. This is industrial evidence of the name dependence we measured in Causal-Copilot. Propose AUD-22 as a vendor-neutral "semantic dependence audit": real names, neutral names, swapped names, applied to any LLM-assisted causal tool.
5. **Add cost and latency to our metrics.** IT buyers are quoted time-to-answer and tokens (Causely −48% to −60% tokens; Datadog prices per investigation). Report tokens and wall-clock per scenario next to F1 and calibration for Causal-Copilot and the ledger.
6. **Abstention is a differentiator, but unvalidated demand.** Only Instana's low-confidence output and Causaly's no-answer detection were found. Treat "buyers pay for abstention" as a hypothesis. Test it with 3–5 practitioner interviews (SRE, marketing science, RWE) before building UI for it.
7. **Fix regulatory citations.** Any project text citing SR 11-7 as current must cite SR 26-2 (17 Apr 2026) instead. It must also note that generative and agentic AI are out of its scope. EU AI Act high-risk dates are likely Dec 2027 / Aug 2028, not Aug 2026 (provisional).
8. **Intervention-backed claims are the currency.** Marketing buyers trust experiments over models. Our CausalArena interventional identifiability (≥ 0.974) supports making I-sourced claims a first-class, separately reported tier in the ledger output.

## Open questions

- Does any vendor (causaLens, Xplain Data, Aitia, Geminos) measure edge-level graph accuracy internally? Nothing public was found.
- Prices for Dynatrace RCA, causaLens Digital Workers and Xplain Data; Haus's ACV comes from a small second-hand sample.
- Whether buyers would pay extra for calibrated intervals or abstention, as opposed to speed. No direct evidence either way.
- Exact RCT-DUPLICATE agreement metrics (primary paper behind a captcha); exact numbers in Heusch's MMM preprint (abstract only).
- Final adoption status of the EU AI Act Digital Omnibus as of Oct 2026.
- Affiliations behind EvoCause and HPCI. The Huawei link is inferred from author overlap and is not confirmed on the pages read.
- Gartner's current Hype Cycle position for causal AI (paywalled).

## Not read

- RCT-DUPLICATE paper on PMC: reCAPTCHA. Numbers are second-hand via Becaris and Cytel.
- Aetion RCT-DUPLICATE news: redirects to the Datavant newsroom; not followed.
- Robyn CRAN manual: robots-disallowed. GitHub README read instead. Calibration with lift tests was not confirmed from the pages read.
- IBM Instana RCA docs: fetch error. IBM arXiv paper read instead.
- FDA RWD EHR/claims guidance full PDF: landing page only.
- Heusch arXiv 2608.21128 full text: abstract only. ROAS numbers are second-hand.
- Pham et al. 2408.13729 full PDF; later RCAEval versions.
- Causely benchmark page and full arXiv 2605.18327 (affiliations not on the abs page).
- Gartner Hype Cycle documents: paywalled.
- gCastle (arXiv 2111.15155) and Structural Hawkes Processes (arXiv 2305.05986): found, not opened.
- Unlearn EMA qualification opinion PDF: vendor summary read instead.
- Kellogg MMM PDF, Nielsen MMM best-practices PDF, Sellforte blog: found, not opened.
- Openlayer SR 26-2 explainer: read but contradicted by primary text; not used for claims.

## Searches run

See `searches` in `AU5_commercial.json` (54 run). Two further searches were not run because the shared web-search budget was exhausted:
- causaLens discovery-with-constraints limitations
- causal-AI observability criticism

Main families:
- vendors: causaLens, Causely, Dynatrace, Datadog, New Relic, IBM, Fiddler, Geminos, Xplain Data, Aitia, Causaly, Aetion, Unlearn, Haus, Recast, Lifesight, Statsig/Eppo
- big-tech libraries: DoWhy/GCM, Amazon supply chain, Meridian, Robyn, CausalImpact, CausalML, Azure RAI, ShowWhy, Causica
- regulation: FDA RWE, ECT, AI credibility; EMA RWD; EU AI Act Art. 12/13 and Omnibus; SR 11-7 and SR 26-2
- evaluations: RCAEval, RCT-DUPLICATE, MMM criticism
- market size and surveys
- climate attribution and earth-science discovery
- manufacturing and telecom discovery
