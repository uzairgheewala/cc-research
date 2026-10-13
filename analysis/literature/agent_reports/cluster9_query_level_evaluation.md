**Where we are now:** the literature check is done. One July 2026 preprint (CausalDS) already covers most of the target benchmark design; the rest of the target is still open as far as this search reached.

Marks: **V** = I opened the primary page (arXiv, proceedings, GitHub). Most V reads went through a fetch tool that summarises the page, so numbers are as it reported them. The CausalDS scoring table, coverage figures and motif table I saw as raw PDF text. **A** = snippet, search-result title or memory.

## 1. Data-in, effect-question benchmarks

- **CausalDS** (Leban & Sun, arXiv 2607.08093, Jul 2026) is the closest match. V
  - Input: story, parquet tables and schema, in a sandbox. Ground truth: a hidden sampled SCM.
  - Tasks span rungs 1-3; effect tasks are "identification-gated". Labels come from DoWhy (ATE) and y0 ID*/IDC* (rung 3).
  - Non-identifiable score is 1 iff the agent answers null. Identifiable ATE intervals get a proper interval score, with coverage reported.
  - Scale: 953 scenes; the released exam is 100 tasks on small motifs (IV, confounding, front-door, chain, "grafted").
  - Results: pass rate 82.4% for Claude Opus 4.8 and GPT-5.5. Coverage of nominal-95% ATE intervals is 71.4% for Opus and 20-43% for the other five models.
  - Those coverage values look like multiples of 1/7, so the interval pool is probably about 7 items (my inference).
- **CausalReasoningBenchmark** (Sawarni, Tan, Syrgkanis, arXiv 2602.20571). V
  - 174 queries on 139 real datasets; input is question, CSV and metadata. Gold design spec plus reference estimate.
  - Identification and estimation are scored separately. No abstention cases; interval overlap is scored but not coverage.
  - Baseline: strategy correct 81%, full spec 38%.
- **CauSciBench** (Acharya et al., ICML 2026, PMLR 306). V
  - CSV plus question, built from replicated papers, textbooks and synthetic data. Metrics: method-selection accuracy and mean relative error.
  - The 2025 preprint says there is no abstention and no uncertainty scoring; o3 has 49% relative error on real data.
- **QRData** (Liu et al., Findings of ACL 2024, arXiv 2402.17644). V
  - 411 questions with data sheets, 269 causal (IHDP, Jobs, Sachs and others). Accuracy within ±3%.
  - GPT-4: 58% overall, at most 51% on causal. No non-identifiable option.
- **ORCA** (Chung et al., arXiv 2508.21304). V
  - A system paper with its own synthetic database. It reports CI coverage: 74.8% agentic, 89.9% with oracle SQL, 13% for GPT-4o-mini.
- **ACIC 2016** (Dorie et al., arXiv 1707.02641). V
  - Real covariates with simulated treatment and outcome, 77 settings. Metrics: bias, RMSE, coverage, interval length, PEHE.
  - Ignorability holds by construction, so abstention is never correct.
- **RealCause** (Neal et al., arXiv 2011.15007): generative-model ground truth. V (abstract only)
- **Text-only or not interventional:**
  - CLadder (NeurIPS 2023): 10K natural-language items from an oracle engine. V. CausalDS's comparison table says it has no tabular data and no non-identifiable abstention. V
  - CausalBench, Wang (SIGHAN 2024): text, math and code problems. V
  - CausalBench / CausalBN-Bench, Zhou et al. (arXiv 2404.06349): graph-level tasks. V
  - DiscoveryBench (arXiv 2407.01725): 264 real tasks, best score 25%. V
  - BLADE (arXiv 2408.09667): expert analysis decisions, not causal ground truth. V
  - CausalPitfalls (Du et al., arXiv 2505.13770): rubric plus LLM judge. V
  - InterveneBench (arXiv 2603.15542): study-design reasoning over 744 studies. V
  - EconCausal (arXiv 2510.07231): models recognise null effects only 13.8% of the time. V
- **Graph or mechanism-centred with interventions:**
  - CausalBench-GSK (Chevalley et al., arXiv 2210.17283): predicted edges scored on held-out perturbation data by mean Wasserstein distance and false-omission rate; effect sizes are not predicted. V
  - Causal Chambers (Gamella, Peters, Bühlmann, arXiv 2404.11341). V (abstract; no explicit effect-estimation task seen)
  - CausaLab (Yang et al., arXiv 2605.26029): observational-only GPT-5.2 reaches 92% task accuracy with edge F1 of 0.471. V
  - CausalGame (arXiv 2607.04293). V
- **Causal-Copilot** (Wang et al., arXiv 2504.13263): evaluated on graph F1 only, with no effect-error metric, identifiability check or abstention described. V
- **CAIS** (Acharya et al., ICML 2026 workshop): evaluated on CauSciBench. V

## 2. Partial identification and equivalence-class identification

- **autobounds** (Duarte, Finkelstein, Knox, Mummolo, Shpitser, arXiv 2109.13471). V
  - Returns sharp bounds via polynomial programming and is anytime-valid.
  - Observed variables must be discrete; the problem is NP-hard in general; the examples shown are small.
  - JASA 2024 citation: A.
- **causaloptim** (Sachs et al., JCGS 2023): symbolic LP bounds for a restricted problem class. V
- **Zhang, Tian, Bareinboim** (ICML 2022): canonical SCMs, discrete domains, polynomial program with Monte Carlo approximation. V
- **Balazadeh, Syrgkanis, Krishnan** (NeurIPS 2022): continuous variables, general graphs, with a tightness proof only for linear SCMs. V
- **Padh et al.** (CLeaR 2023): A
- **"A-identifiability":** nothing found under that name. The nearest is ε-identifiability (Li, Mueller, Shu, Pearl, AISTATS 2026). V
- **Equivalence class:**
  - IDA (Maathuis, Kalisch, Bühlmann, arXiv 0810.4214): returns the multiset of effects across the class, with the minimum absolute value as a lower bound. V
  - Generalised adjustment (Perković et al., JMLR 2018): sound and complete for DAG, CPDAG, MAG and PAG; implemented in dagitty. V
  - Jaber et al. (ICML 2019; NeurIPS 2022): complete ID and conditional-ID algorithms on PAGs. V
- **Practical at 20-40 variables (my judgment, A):**
  - Graphical identification (ID, generalised adjustment, IDA, PAG algorithms) should be cheap.
  - Sharp bounding is practical only after projecting to a small discrete sub-problem.
  - Neural bounds run but give no certificate.
  - I did not verify PAG-ID implementations at this scale.

## 3. Calibration and selective prediction

- **Interval calibration against ground truth:** CausalDS, ORCA and ACIC 2016 (above).
- **Conformal ITE intervals:** Lei & Candès (arXiv 2006.06138). V
- **Uncertainty-flagged CATE:** Jesson et al. (NeurIPS 2020; ICML 2021 intervals under bounded hidden confounding). V (abstracts)
- **Structure:**
  - Wang, Kolar, Drton, "Confidence Sets for Causal Orderings" (arXiv 2305.14506). V
  - Karimi Mamaghan et al. (arXiv 2406.03209): common metrics for Bayesian discovery track posterior quality poorly. V
- **Decision gate:** CIVeX (Rovai, arXiv 2605.09168). V
  - Verdicts are EXECUTE / REJECT / EXPERIMENT / ABSTAIN, scored by false-execution rate.
  - It is a single-author preprint with its own synthetic benchmark.
- **Not found:** risk-coverage curves over an agent's per-claim causal conclusions, or conformal structure sets used in an agent benchmark.

## 4. Decision-grade evaluation

- Gentzel, Garant, Jensen (NeurIPS 2019): interventional measures on empirical data give different rankings from structural ones. V
- SID (Peters & Bühlmann, arXiv 1306.1043). V
- AID / gadjid (Henckel, Würtzen, Weichwald, arXiv 2402.08616): SID is a special case; much faster. V
- Eigenmann, Mukherjee, Maathuis (UAI 2020): causal risk. V
- Emezue et al. (arXiv 2307.04988): Bayesian discovery scored by downstream ATE. V
- Li & Kilbertus (arXiv 2510.25037): estimand-based graph distance with latents. V
- Scoring at both graph and intervention level: CausalDS, CausaLab, QRData, CausalBench-GSK and Emezue et al.

## 5. Practical systems

- **DoWhy:** backdoor, front-door, IV and the ID algorithm, with a `proceed_when_unidentifiable` flag. V (docs and source). The pages I read mention no bounds.
- **PyWhy-LLM:** self-described "experimental". V
- **ShowWhy:** archived 17 Dec 2025. V
- **causaLens:** the homepage now sells "Digital Workers"; decisionOS and identifiability are not mentioned. V
- **Causal-Copilot:** the GitHub page mentions bootstrap edge uncertainty and DoWhy integration; automatic refutation and abstention are not described. V
- **CATE-B** (Berrevoets et al., arXiv 2508.10581) and **CausalAgent** (Zhu, Chen, Cai, arXiv 2602.11527): V (abstracts)
- No system I read returns "not identifiable, here are bounds and the experiment that would resolve it".

## Ten most relevant works

| Work | Data in | Abstain scored | Intervals scored | Experiment scored |
|---|---|---|---|---|
| CausalDS 2026 | yes | yes | yes | no |
| CausalReasoningBenchmark 2026 | yes | no | overlap only | no |
| CauSciBench 2026 | yes | no | no | no |
| QRData 2024 | yes | no | no | no |
| CIVeX 2026 | yes | yes | lower bound | verdict only |
| CausaLab 2026 | interactive | no | no | implicit |
| BoxingGym (arXiv 2501.01540) | interactive | no | no | yes (information gain) |
| CausalBench-GSK | yes | no | no | no |
| Gentzel et al. 2019 | n/a | n/a | n/a | n/a |
| ACIC 2016 | yes | no | yes | no |

## What appears not to exist

I found no benchmark that combines all of the following:
- tabular data at 20-40 variables;
- per-query identifiability labels under an explicitly stated assumption set or a discovered equivalence class;
- credit for correct bounds;
- calibrated intervals;
- scoring of the experiment proposed to resolve non-identifiability.

CausalDS covers labels, abstention and interval scoring, but on small synthetic motifs and relative to one hidden "story-implied" graph. Its fetched text contrasts it with interactive environments and showed no experiment proposal or bounds answer. Experiment-choice scoring exists only in separate interactive benchmarks (BoxingGym, CausaLab, CausalGame, WhatWorkedBench arXiv 2609.27490), none tied to identifiability.

## Could not verify

- CausalDS: the share of non-identifiable tasks, per-model abstention numbers (its Table 12), and whether bounds are ever accepted.
- Whether CLadder filters to identifiable queries.
- Venue claims beyond arXiv for SID, AID, DiscoveryBench, CausalPitfalls and CausalBench-GSK.
- "causal-learn+" (not found).
- Anything behind OpenReview or paywalls.

**Where we're going:** read CausalDS in full (github.com/andleb/causalds) before fixing the design, and position against it on scale, stated assumption sets, bounds and experiment proposal. Worth saving to memory: CausalDS (arXiv 2607.08093) is the nearest prior art.
