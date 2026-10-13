Tickets: AUD-19, BEN-07, STR-02
Written 2026-10-12 by an audit agent; sources read on that date.

# AU2 Benchmarks and datasets for causal discovery and causal reasoning

**Where we are now:** 69 benchmarks and dataset collections are typed in `AU2_benchmarks.json`. Each row records where the ground truth comes from, what is scored, and how the benchmark can leak. Most of the 2024-2026 field was checked against primary pages today. Facts carried over from earlier project notes are marked `prior-note:` in the JSON sources and were not re-opened today.

## Question

Which benchmarks and datasets exist for causal discovery and causal reasoning? For each one: where does its ground truth come from, what does it score, and how can it leak? Leak channels considered: variable names, column order, varsortability / R2-sortability, standardisation artefacts, LLM memorisation of famous graphs, and LLM-written graphs.

## Method

- **Sources:** primary pages only: arXiv abstract or HTML, proceedings, the dataset's own page (Hugging Face, Zenodo, CRAN, project site) and the GitHub README. All were read on 2026-10-12 through a fetch tool that summarises pages, so exact numbers should be re-checked before quoting.
- **Builds on:** prior notes cluster1, 2, 7, 8 and 9, bnd02/rep12, and the project doc `claude/benchmark-targets.md`.
- **Inclusion rule:** a fixed, released dataset, generator suite or scored protocol that is used to evaluate:
  - causal structure,
  - effects or root causes,
  - causal reasoning by language models, or
  - causal analysis by agents.
- **Excluded:** pure methods and survey papers. Leak studies (Reisach, Ormaniec, Kitson & Constantinou, Srivastava, CARE) are cited as evidence, not given rows. CARE and Feng et al. are the exception: they get rows because they define reusable probe protocols.
- **Number labels:**
  - `reported`: from the authors' own page.
  - `measured (project)`: our own measurements on CausalArena.
  - `second-hand`: taken from a prior note that read the primary source.
  - `inference`: my reasoning, not stated anywhere.
- **Memorisation risk:** an audit judgment with a stated reason. It was not measured.

## Findings

### F1. Where ground truth comes from

There are five kinds of origin. Each has its own way of failing.

| Origin | Examples (row numbers in the table) | Characteristic failure |
|---|---|---|
| Synthetic generator | CausalArena synthetic (1), Causal-Copilot suite (3), cdt/gCastle/CSuite/CausalPlayground (11-15), CausalDynamics, NetSim, ACDB, CausaLab, ReplaySCM | Varsortability and R2-sortability. Topological column order if files are written in generation order. Truth is only as realistic as the generator. |
| Generator fitted to real data | CausalTime (31), causalAssembly (19), DREAM4 (27) | Truth is defined by the fitted model. In causalAssembly the cross-process edges were learned from the same plant data by SpAM pruning (reported), so part of the "truth" is a learner's output. |
| LLM-written, human-reviewed | CausalArena semantic and formula families (1) | Directions an LLM finds plausible are built in, so a name-reading LLM recovers them without data. CausalVerify reports that on its newest pairs the gain appeared only for models from the family that built the references (reported, [2609.07944](https://arxiv.org/abs/2609.07944)). |
| Expert-elicited or literature-curated | bnlearn (4-5), Sachs consensus (6), bnRep, Bayesys, Tübingen (9), Arctic sea ice, neuropathic, CausalGraphBench, BEELINE experimental sets, DREAM5 real organisms, all real-paper agent benchmarks | Memorised by LLMs (Srivastava et al.: near-perfect BNLearn completion at 0% context; LLM-BFS F1 0.93 on Asia vs 0.56 on a post-cutoff graph, reported). The truth itself is contested: Sachs is "not definitive" and results have peaked near SHD 12 (second-hand, Brouillard et al.); literature-inconsistency rates are Asia 57.9%, Child 54.0%, Sachs 26.7% (second-hand). |
| Physical or experimental | Causal Chambers (18), CausalRivers (32), CausalBench-GSK (26), PetShop (37), RCAEval (38), Sachs interventions (data only) | The cleanest truth, but narrow. The Mk1 chamber graphs are depth 1, with every parent a manipulable actuator (second-hand, computed from the package). The river graph follows elevation. GSK has no graph and scores held-out interventions. PetShop and RCAEval score root causes, not graphs. |

### F2. How each leak channel shows up

- **Column order.**
  - **CausalArena:** this is the one public benchmark where released files were measured to list columns in causal order. All 2,068 semantic, 1,714 formula and 50,421 synthetic true edges point forward. An order-reading regression scores 0.680 (0.269 shuffled) against the best published 0.634 (measured, project). The paper does not mention column order ([2609.11897 HTML](https://arxiv.org/html/2609.11897)).
  - **bnlearn files:** alphabetical, i.e. arbitrary. Hill-climbing F1 still swings by 0.412 with file order (second-hand, Kitson & Constantinou).
  - **Benchmarks that guard against it:**
    - ACDB permutes node indices (second-hand).
    - ReplaySCM varies order disclosure as a factor: Ordered / Block-order / Hidden-order / Hidden-roots. Held-out replay drops sharply when order is hidden (reported, [2605.08197](https://arxiv.org/abs/2605.08197)). It is the only benchmark found that treats order disclosure as an experimental factor.
- **Variable names.**
  - **Named:** CausalArena semantic and formula, bnlearn, Sachs, bnRep, Bayesys, Tübingen, Causal Chambers, CausalRivers (river names and elevation in metadata), neuropathic, Arctic sea ice, CausalBench-GSK genes, BEELINE experimental genes, and all real-paper agent benchmarks.
  - **Anonymised or abstract:** CausalArena synthetic, Corr2Cause (letters A-D), DREAM4 (gene IDs; not verified today), CausaLab (crystal entities), ReplaySCM, ACDB, CARE's random arm, and Feng et al.'s fictitious terms.
  - **Evidence of reliance:**
    - CausalBench-LLM (Zhou et al.) concludes that LLMs work through "semantic associations with named entities" (reported).
    - CARE's Asia score collapses from 1.000 to 0.00-0.08 with random names (second-hand).
    - On CausalArena, Causal-Copilot scores 0.306 with real names, 0.232 with neutral names and 0.142 with swapped names (measured, project).
- **Metadata as a side channel.** The CausalRivers kit ships elevation, coordinates and river name per station ([README](https://github.com/causalrivers/benchmark), reported). Because water flows downhill, metadata alone orients most edges (inference). This is a K channel that is neither a name nor column order.
- **Varsortability and R2-sortability.**
  - The general evidence (Reisach 2021 and 2023; Ormaniec iSCM) applies to every additive-noise generator row.
  - Values have been published for Sachs (R2-sortability 0.82, second-hand), but for none of the 2024-2026 suites in the table.
  - CausalArena cites UUMC as a remedy but does not report its own sortability (reported).
  - Varsortability is removed by standardisation; R2-sortability is not (reported, [2303.18211](https://arxiv.org/abs/2303.18211)).
  - CausalMan ships unnormalised data (second-hand), so scale cues there are unmeasured.
- **Memorisation of famous graphs.** Established for bnlearn (Srivastava; CARE) and Tübingen (GPT-4 row completion 61% of cells, second-hand). Feng et al. (ACL 2025) give the cleanest dose-response: OLMo F1 falls from 0.88 to 0.2 from the highest to the lowest pretraining-occurrence bin (reported, [ACL 2025](https://aclanthology.org/2025.acl-long.471.pdf)).
- **Scoring artefacts.**
  - CausalMan stores bidirected edges as two directed edges, so directed-F1 scorers double-count them (second-hand).
  - The cdt Tübingen loader labels every pair "A causes B", so a constant predictor scores perfectly unless pairs are flipped (reported, [cdt docs](https://fentechsolutions.github.io/CausalDiscoveryToolbox/html/data.html)).
  - CausalArena orients undirected PC/GIES edges at random (project).

### F3. Name collisions

At least four projects are called CausalBench. They are separate rows:

- GSK single-cell perturbation ([2210.17283](https://arxiv.org/abs/2210.17283)).
- Zhou et al. LLM causal learning, retitled CausalBN-Bench in v3 ([2404.06349](https://arxiv.org/abs/2404.06349)).
- Zeyu Wang, SIGHAN 2024 ([ACL Anthology](https://aclanthology.org/2024.sighan-1.17)).
- The ASU platform of Kapkiç et al. ([2409.08419](https://arxiv.org/abs/2409.08419)).

The abstract page for arXiv 2405.20318 now titles that work *Quriosity*. I believe it was earlier called CausalQuest, but that rests on my memory of the arXiv ID.

### F4. Maintenance

- **Archived:** CSuite (archived 2026-06-15) and PetShop (archived 2025-11-11).
- **Static for years:** the bnlearn repository page (last updated 2022-11-29) and the Tübingen pairs (v1.0 released 2015-12-21; the page now lists 108 pairs).
- **Active:** CausalArena (v1 Sept 2026, held-out half reserved), the CausalRivers leaderboard, Causal Chambers (Remote Lab offered in 2026), bnRep (0.0.6, 2025-10-26).

## Typed table

Full typed records, with the leak evidence and URLs for every row, are in `AU2_benchmarks.json`. Compact view (n/s = not stated on the pages read):

| # | Name | Category | Ground truth origin | Vars | I data | Hidden conf. | TS | Names (K) | Memorisation |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CausalArena (generated families: synthetic, semantic, formula) | structure | synthetic generator (synthetic family); LLM-written with human review (semantic and for... | semantic 17-25 vars, 25-67 edges (paper); ... | yes | no | no | semantic and formula: named (node_id like ... | medium-high |
| 2 | CausalArena real-data slice | structure | literature-curated / expert ('expert-specified or experimentally motivated in the sourc... | small (Auto MPG 4 vars per project) to ~40... | yes | n/s | no | named (Sachs proteins, PetShop services, c... | high |
| 3 | Causal-Copilot internal synthetic suite | structure | synthetic generator | tabular p=10 default up to 1000; time seri... | no | n/s | yes | not stated (no anonymisation described) | low |
| 4 | bnlearn repository: small discrete (Asia, Cancer, Earthquake, Survey, Sachs-discretised) | structure | expert-elicited (textbook and expert Bayesian networks; repository page cites Hebrew U ... | 5-11 | no | no | no | named (e.g. SMOKING, TUBERCULOSIS) | high |
| 5 | bnlearn repository: medium to massive discrete, Gaussian and CLG (Alarm, Child, Insurance, Water, Hepar2, Win95pts, Andes, Munin, ecoli70, magic-niab, arth150, Sangiovese, Mehra, ...) | structure | expert-elicited (discrete) and fitted to domain data in the source papers (Gaussian/CLG) | 20-1,041 (discrete); 44-107 (Gaussian); 7-... | no | no | no | named | high (named medium networks); medium (large/massive with cryptic node names) |
| 6 | Sachs flow cytometry (Sachs et al., Science 2005) | structure | literature-curated consensus network over an experimental (perturbation) dataset; the p... | 11 | yes | n/s | no | named (Raf, Mek, PKC, ...) | high |
| 7 | bnRep (Bayesian networks from the academic literature) | structure | literature-curated (BNs published in recent papers) | not stated on CRAN page | no | no | no | named | medium |
| 8 | Bayesys data and BN repository | structure | mixed: knowledge-based graphs (COVID-19 explicitly 'knowledge-based'); textbook BNs (As... | 8-109 | n/s | yes | no | named | medium |
| 9 | Tübingen cause-effect pairs (Mooij et al., JMLR 2016) | structure | literature-curated / domain knowledge (authors 'motivate' each direction); pairs 1-41 f... | 2 per pair (a few multivariate) | no | n/s | no | named (pairmeta/README descriptions) | high |
| 10 | ChaLearn cause-effect pairs challenges (2013; Fast Causation Coefficient 2014) | structure | mixed real and artificial pairs (data description not on page read) | 2 per pair | no | n/s | no | not read | medium |
| 11 | Causal Discovery Toolbox (cdt) datasets and generators | structure | mixed: Sachs (literature), Dream4 (GeneNetWeaver simulation), Tübingen (curated), plus ... | Sachs 11; Dream4 100; generator default 20 | no | no | no | Sachs named; Dream4 gene IDs; synthetic an... | mixed |
| 12 | gCastle datasets and simulators (Huawei) | structure | synthetic generator plus three real telecom datasets (ground-truth origin not read) | not read | n/s | n/s | yes | synthetic anonymous; telecom not read | low |
| 13 | Benchpress (Snakemake benchmarking workflow) | structure | user-chosen: bnlearn-style networks, random graphs, user models | user-chosen | no | n/s | no | depends on source | inherits from data source |
| 14 | CausalPlayground | simulator | synthetic generator | user-chosen | yes | n/s | no | anonymous by default (inference) | low |
| 15 | CSuite (Microsoft) | structure | synthetic generator (hand-designed small SCMs) | 2-12 nodes, 1-15 edges | yes | partly (see JSON) | no | anonymous/synthetic | low |
| 16 | OCDB (Open Causal Discovery Benchmark) | structure | real datasets (names and GT origin not in text read) | not read | n/s | n/s | n/s | not read | unknown |
| 17 | CausalBench (ASU platform; Kapkiç et al.) | platform | user-contributed datasets | varies | n/s | n/s | n/s | varies | unknown |
| 18 | Causal Chambers (light tunnel, wind tunnel) | structure | physical system: edges from physics knowledge, each validated by randomised two-level e... | Mk1 light tunnel 38 vars / 57 edges; wind ... | yes | partly (see JSON) | partly (see JSON) | named physical quantities (actuators, sens... | low-medium |
| 19 | causalAssembly (Bosch production line) | structure | mixed: within-process edges from expert physics knowledge; cross-process edges estimate... | 98 (5 stations: 6/34/16/26/16) | yes | no | no | not checked | low |
| 20 | CausalMan (Bosch physics-based simulator) | structure | simulator built with domain experts (physics of press-fitting) | observed 53 (Small) and 186 (Medium); full... | yes | yes | no | named manufacturing variables (inference f... | low |
| 21 | Neuropathic pain diagnosis simulator (Tu et al., NeurIPS 2019) | structure | expert-elicited medical causal graph with parameters fitted to real patient records | 222 nodes (prior note) | no | partly (see JSON) | no | named symptoms and diagnoses | medium |
| 22 | Arctic sea ice / atmosphere (Huang et al., Frontiers in Big Data 2021) | structure | literature-curated domain-knowledge graph (textbooks and papers) | 12 (11 ERA-5 variables + sea ice extent); ... | no | n/s | yes | named climate variables | medium |
| 23 | Science-grounded post-cutoff graphs (Srivastava et al. 2025: Alzheimer's, COVID-19 respiratory, COVID-19 complications, Sweden transport) | structure | expert-elicited graphs from recent papers (Alzheimer's from Causal Modelling Agents, IC... | 11-63 nodes, 10-138 edges | no | n/s | no | named | low now, rising |
| 24 | CausalGraphBench (Babakov et al., ACL SRW 2025) | structure | literature-curated: 35 graphs from public repositories and papers | not stated | no | n/s | no | named | high |
| 25 | Small real tables used in LLM/agent papers (UCI/Kaggle-style: Auto MPG, Abalone, Concrete, DWD climate, Ozone, Arrhythmia, Sangiovese, earthquake) | structure | literature-curated or author-asserted graphs | 4-~15 | no | n/s | partly (see JSON) | named | high |
| 26 | CausalBench (GSK; Chevalley et al.) single-cell perturbation | structure | experimental: no ground-truth graph; scored on held-out perturbation data plus literatu... | hundreds to thousands of genes (622 and 38... | yes | yes | no | named genes | medium |
| 27 | DREAM4 in silico network challenge | structure | synthetic generator (GeneNetWeaver) on subnetworks of E. coli and yeast regulatory netw... | 10 and 100 genes (5 networks each) | yes | n/s | partly (see JSON) | gene IDs (anonymised labels; not verified ... | low-medium |
| 28 | DREAM5 network inference | structure | in silico plus literature/ChIP gold standards for E. coli (RegulonDB) and yeast; S. aur... | thousands of genes | yes | yes | no | named genes in real organisms | medium |
| 29 | BEELINE (Pratapa et al., Nature Methods 2020) | structure | mixed: synthetic (BoolODE), four literature-curated Boolean models, and five experiment... | small synthetic to thousands of genes | no | n/s | partly (see JSON) | named genes in experimental sets | medium |
| 30 | SynTReN (Van den Bulcke et al., BMC Bioinformatics 2006) | simulator | synthetic generator on subgraphs of published E. coli / yeast networks with Michaelis-M... | user-set | no | n/s | no | gene names from source networks (inference) | low |
| 31 | CausalTime (Cheng et al.) | time series | synthetic generator fitted to real data: hypothesised graph from importance analysis of... | AQI 36, Traffic 20, Medical 20 | no | partly (see JSON) | yes | station/sensor IDs (not semantic, inference) | low |
| 32 | CausalRivers | time series | physical system: river network topology from agency metadata, HydroSHEDS, Wikipedia and... | East Germany 666 nodes / 651 edges; Bavari... | no | partly (see JSON) | yes | station IDs plus metadata (river name, coo... | low |
| 33 | CauseMe (Runge et al.) | time series | synthetic generators plus real data whose structure is 'known with high confidence' | varies | no | n/s | yes | not read | low |
| 34 | CausalDynamics (Herdeanu et al.) | time series | synthetic generator: coupled ODE/SDE systems and two idealised climate models | not stated in abstract | no | partly (see JSON) | yes | anonymous (inference) | low |
| 35 | NetSim (Smith et al., NeuroImage 2011) | time series | synthetic generator (simulated BOLD with ground-truth networks) | Nnodes varies by simulation | no | n/s | yes | anonymous nodes | low |
| 36 | CIPCaD-Bench (Menegozzo et al.) | time series | process knowledge for Tennessee Eastman simulator and a food plant ('multiple ground tr... | not stated in abstract | n/s | n/s | yes | named process variables (inference) | medium |
| 37 | PetShop (Hardt et al., CLeaR 2024) | root cause | experimental: 68 injected performance issues in a real microservice deployment | 41 components (metrics count not stated) | yes | n/s | yes | named services | low |
| 38 | RCAEval (Pham et al.) | root cause | experimental: injected failures in three microservice systems | not stated | yes | n/s | yes | named services (inference) | low |
| 39 | CausalVerse (Chen et al.) | representation | synthetic high-fidelity simulation (configurable) | not stated | yes | n/s | yes | n/a (images) | low |
| 40 | Corr2Cause (Jin et al.) | LLM reasoning | synthetic generator (graph enumeration; label by causal discovery logic) | 4-6 variables named A-D... | no | n/s | no | anonymous letters | medium |
| 41 | CLadder (Jin et al.) | LLM reasoning | synthetic generator ('oracle causal inference engine') then verbalised | small graphs | no | n/s | no | commonsense / anti-commonsense / nonsensic... | medium |
| 42 | CausalProbe-2024 (Chi et al.) | LLM reasoning | built from corpora 'fresh and nearly unseen' for studied LLMs | n/a | no | n/s | no | named (natural text) | low then rising |
| 43 | CausalBench / CausalBN-Bench (Zhou et al., LLM causal learning) | LLM reasoning | literature-curated (community datasets; graphs not listed on page) | up to >50 nodes | no | n/s | no | named | high |
| 44 | CausalBench (Zeyu Wang, SIGHAN 2024) | LLM reasoning | not stated on page | n/a | no | n/s | no | named | medium |
| 45 | CRAB (Romanou et al., EMNLP 2023) | LLM reasoning | expert/annotator-labelled (method not stated on page) | events | no | n/s | no | named events (news) | high |
| 46 | e-CARE (Du et al., ACL 2022) | LLM reasoning | human-annotated | n/a | no | n/s | no | natural text | high |
| 47 | COPA (Roemmele, Bejan, Gordon 2011) | LLM reasoning | expert-written (creation details not on page) | n/a | no | n/s | no | natural text | high |
| 48 | Kıcıman et al. LLM causal evaluations (Tübingen-LLM, neuropathic, counterfactual, actual causality) | LLM reasoning | reuses Tübingen pairs, neuropathic simulator, CRASS-type vignettes | pairs | no | n/s | no | named | high |
| 49 | CausalQuest / Quriosity (Ceraolo et al.) | LLM reasoning | naturally occurring questions; labelling method not stated | n/a | no | n/s | no | natural text | medium |
| 50 | CaLM (Chen et al.) | LLM reasoning | curated mix (construction not stated on page) | n/a | no | n/s | no | mixed | medium |
| 51 | CLEAR (Chen et al.) | LLM reasoning | synthetic graph tasks (construction not detailed) | small graphs | no | n/s | no | not stated | low-medium |
| 52 | CausalGraph2LLM (Sheth et al.) | LLM reasoning | graphs not listed on page | not stated | no | n/s | no | not stated | medium |
| 53 | CRASS (Frohberg & Binder) | LLM reasoning | hand-built with crowd-validated human baseline | n/a | no | n/s | no | natural text | high |
| 54 | Feng et al. 2025 occurrence-controlled probes (ConceptNet, CauseNet pairs; fictitious-term relations) | LLM reasoning | literature/knowledge-base pairs plus synthetic fictitious relations injected into Dolma... | pairs; graphs 12-27 vars | no | n/s | no | named; fictitious names for the control | controlled |
| 55 | CARE probe protocol (Dong et al.) on bnlearn | LLM reasoning | expert-elicited bnlearn graphs (Asia, Survey, Earthquake, Alarm) | 5-37 | no | no | no | original, anonymised and permuted arms | measured |
| 56 | CausalDS (Leban & Sun) | agentic | synthetic generator (hidden sampled SCM) with a synthetic story; optional grounding in ... | small motifs (IV, confounding, front-door,... | no | partly (see JSON) | no | named via story | low |
| 57 | CauSciBench (Acharya et al., ICML 2026) | agentic | literature-curated (replicated papers, textbooks) plus synthetic | real datasets | no | partly (see JSON) | no | named | medium |
| 58 | CausalReasoningBenchmark (Sawarni, Tan, Syrgkanis) | agentic | literature-curated from 73 papers and 3 textbooks | real datasets | no | n/s | no | named | medium |
| 59 | CausalVerify (Zhang et al.) | agentic | mixed: 259 real-paper contexts, 100 synthetic scenarios with executable references, pap... | n/a | no | n/s | no | named | medium |
| 60 | QRData (Liu et al., Findings ACL 2024) | agentic | literature-curated (textbooks, course material, papers) | varies | no | n/s | no | named | medium |
| 61 | DiscoveryBench (Majumder et al.) | agentic | literature-curated workflows from papers (real) plus synthetic | varies | no | n/s | no | named | medium |
| 62 | CausalPitfalls (Du et al.) | agentic | authored challenges with rubrics | small | no | n/s | no | named | medium |
| 63 | InterveneBench (Shi et al.) | agentic | literature-curated (744 social-science studies) | n/a | no | n/s | no | named | medium |
| 64 | Active Causal Discovery Benchmark (ACDB; Deb, Shah, Krishnan) | agentic | synthetic generator (linear-Gaussian) | 4-7 nodes (prior note) | yes | no | no | node indices permuted 'so names do not lea... | low |
| 65 | CausaLab (Yang et al.) | agentic | synthetic generator (randomly sampled hidden SCM) | 3-7 nodes (prior note) | yes | n/s | no | abstract lab entities | low |
| 66 | CausalGame (Chen et al.) | agentic | synthetic SCM-driven game | 14 scenarios | yes | yes | no | game semantics | low |
| 67 | BoxingGym (Gandhi et al.) | agentic | probabilistic models from science | 10 environments | yes | n/s | no | named scientific settings | medium |
| 68 | Auto-Discovery-Bench (Chen et al.) | agentic | synthetic oracle | small, degrading with size | yes | n/s | no | not stated | low |
| 69 | ReplaySCM (Batzoglou) | agentic | synthetic generator (Boolean SCMs) | 6-10 (prior note) | yes | no | no | order disclosure varied: Ordered / Block-o... | low |

## Explicit answers

### (1) Which benchmarks have physical or experimental ground truth rather than generated or expert graphs?

- **Graph validated by experiment:**
  - **Causal Chambers** is the only one. Each edge is validated by a randomised two-level experiment ([2404.11341](https://arxiv.org/abs/2404.11341); second-hand detail from prior note cluster7).
  - Caveat: the Mk1 graphs are depth 1 (actuator to sensor). That makes them a test of power and nonlinearity, not of orientation.
- **Graph from physical structure, not experiment:**
  - **CausalRivers.** River topology was built from agency metadata, HydroSHEDS, Wikipedia and elevation, and every edge was hand-checked ([HTML](https://arxiv.org/html/2503.17452)).
- **Experimental outcomes but no graph:**
  - **CausalBench-GSK:** Perturb-seq, scored on held-out interventions ([2210.17283](https://arxiv.org/abs/2210.17283)).
  - **PetShop:** 68 injected issues ([PMLR](https://proceedings.mlr.press/v236/hardt24a.html)).
  - **RCAEval:** 735 failure cases ([2412.17015](https://arxiv.org/abs/2412.17015)).
  - These score root causes or intervention effects, not edges.
- **Experimental data, literature graph:**
  - **Sachs:** perturbations are real, but the reference network is a contested consensus.
  - **DREAM5 real organisms:** literature and ChIP gold standards; 43% of tested novel predictions were supported.
  - **BEELINE experimental sets:** database networks.
- **Physics simulators** (truth is the simulator, not the world): CausalMan, causalAssembly (within-process edges), CIPCaD (Tennessee Eastman), CausalVerse.

### (2) Which expose meaningful variable names, and which shuffle or anonymise?

- **Names meaningful:**
  - Structure benchmarks: CausalArena semantic and formula, CausalArena real slice, bnlearn, Sachs, bnRep, Bayesys, Tübingen, Causal Chambers, CausalMan, neuropathic, Arctic sea ice, the Srivastava post-cutoff graphs, CausalGraphBench.
  - Biology: CausalBench-GSK genes, BEELINE and DREAM5 real genes.
  - Root cause: PetShop and RCAEval services.
  - Agent benchmarks on real papers: CausalDS stories, CauSciBench, CausalReasoningBenchmark, CausalVerify, QRData, DiscoveryBench, InterveneBench.
  - All the commonsense text benchmarks: COPA, e-CARE, CRAB, CRASS, CausalProbe.
- **Names carry metadata beyond the label:** CausalRivers. Station metadata includes elevation and coordinates, which orient edges.
- **Anonymised or abstract:**
  - Benchmarks: CausalArena synthetic, Corr2Cause (letters), CLadder nonsensical variant (from memory, not verified today), DREAM4 (gene IDs, not verified today), NetSim, CausalTime (station IDs), CausaLab, ReplaySCM, ACDB, CSuite.
  - Generators: cdt, gCastle, CausalPlayground, CausalDynamics.
- **Shuffle column order or node indices:**
  - ACDB permutes node indices (second-hand).
  - ReplaySCM varies how much of the order is disclosed.
  - CARE applies column reordering as augmentation only (second-hand).
  - No public structure benchmark with semantic names was found that releases files in shuffled order and documents doing so.
  - CausalArena does not shuffle (measured, project).
- **Name-control arms built into the benchmark:**
  - CARE: original / random / permuted.
  - Feng et al.: fictitious terms.
  - Kitson & Constantinou 2026: obfuscation (per prior note; not visible on today's abstract page).
  - Srivastava et al.: post-cutoff graphs.
  - None of them crosses names with column order.

### (3) Which support interventional data and experiment design?

- **Interventional data released** (targets fixed by the benchmark):
  - CausalArena: 800 observational + 200 interventional rows; replay sampler round-robin over declared targets.
  - Causal Chambers datasets.
  - CausalBench-GSK and Sachs.
  - DREAM4: knockouts, knockdowns, multifactorial.
  - CSuite: interventional test sets.
  - CausalMan: hard and soft interventions, including on latents.
  - causalAssembly: the README now supports hard and soft interventions; the paper said none were in the release.
  - PetShop and RCAEval: fault injections.
  - CausalVerse.
- **Experiment design (the agent chooses interventions):**
  - Causal Chambers Remote Lab: real hardware, real-time set/measure; subscription access.
  - CausalPlayground: Gymnasium environment.
  - ACDB: budgeted hard interventions on 4-7-node linear-Gaussian SCMs; random-DAG floor 23.6%; PC+greedy beats LLMs.
  - CausaLab, CausalGame, BoxingGym (expected-information-gain scoring), Auto-Discovery-Bench.
  - ReplaySCM gives interventions; it does not let the agent choose them.
  - Protocols such as LeGIT and IGDA simulate interventions on bnlearn graphs (second-hand).
- **Not found:**
  - An experiment-design benchmark at 20-40 variables with named variables that scores the choice of experiment against identifiability.
  - An interactive version of CausalArena (consistent with prior note cluster7).

### (4) The three biggest gaps a new benchmark could fill (feeds AU4)

1. **No benchmark measures where an answer's edge directions come from.**
   - Nothing found releases the same SCMs under crossed arms:
     - names: real, neutral, swapped;
     - layout: shuffled and documented;
     - scale: raw vs standardised vs iSCM-style (R2-sortability reported);
     - evidence regimes: D, D+I, D+K declared.
   - Nothing scores each edge by its evidence source.
   - CARE crosses names with data size on small bnlearn graphs only. ReplaySCM varies order disclosure on Boolean SCMs only. ACDB anonymises but has no names arm.
   - CausalArena, which has semantic names, ships files in causal order. Whoever adds the controls defines the field's first provenance-aware score.
2. **No mid-size benchmark has validated truth, depth, and choosable experiments together.**
   - Causal Chambers has validated truth and choosable experiments, but its Mk1 graphs are depth 1.
   - CausalMan and causalAssembly have depth and latents but are simulators with no experiment API scored against identifiability.
   - Agent experiment-design benchmarks stop at 3-10 nodes with abstract names.
   - Missing: 20-100 variables, deep graphs, hidden confounders, named variables with a declared knowledge tier, and an intervention budget scored against the identifiability limit (the gap between the CPDAG and what the chosen experiments resolve).
3. **No graph-level, decision-grade scoring that accepts honest abstention.**
   - Structure benchmarks score directed F1 against one DAG, with random orientation for undirected edges (CausalArena), so a correct CPDAG answer is penalised.
   - Interventional metrics appear in fewer than 5% of studies (second-hand, Brouillard et al.).
   - Abstention and interval scoring exist only for effect queries on small motifs (CausalDS) or in a single-author gate (CIVeX, prior note).
   - Missing: an MEC/PAG-aware score, per-edge calibration (risk-coverage), effect error on unseen interventions, and experiment cost, all on the same graphs.
   - A related and cheaper gap is freshness. LLM-written semantic graphs and post-cutoff curated graphs both age into pretraining data. No benchmark regenerates its named scenarios per release with an audit of whether the generating model favours itself.

### (5) Benchmarks for "agentic" causal analysis end to end

- **Effect estimation and analysis, data in, answer out:**
  - CausalDS: sandbox, rungs 1-3, abstention scored, intervals with coverage.
  - CauSciBench (ICML 2026).
  - CausalReasoningBenchmark: identification scored separately from estimation.
  - CausalVerify: four layers from method recognition to estimand recovery. 15.5% of runnable workflows still failed verification.
  - QRData, DiscoveryBench, CausalPitfalls, InterveneBench (study design without data).
- **Interactive discovery:** ACDB, CausaLab, CausalGame, BoxingGym, Auto-Discovery-Bench, ReplaySCM.
- **End-to-end causal-discovery agents of the Causal-Copilot type** (tabular data in, graph plus report out, scored as a pipeline):
  - No dedicated benchmark was found.
  - Causal-Copilot evaluates on its own synthetic suite.
  - CausalSteward scores it on CausalMan (F1 0.078 at 53 nodes, second-hand).
  - CausalArena has no agent entries (prior note).
  - This is the open slot for this project's public agent track (E2).

## What this changes for the project

1. **Keep CausalArena as the primary scoreboard, but report under controls.** Every CausalArena number we publish states the column-order and name arms. Order-reading (0.680) and name-reading effects are larger than the gaps between published methods. Whether to notify the maintainers stays Uzair's decision.
2. **Add a sortability audit to BEN-07 before any synthetic comparison.** Compute varsortability and R2-sortability on the CausalArena public families and on any generator we use; this is a cheap script. No 2024-2026 suite in the table reports it.
3. **Make the arms crossed: names x layout x scale.** CARE's design is names-only and ReplaySCM's is order-only. Crossing them on CausalArena's named SCMs is the smallest contribution with no precedent found.
4. **Treat LLM-written semantic graphs as their own leak channel.** Report Causal-Copilot's real-names advantage (0.306 vs 0.232 neutral) as measured against LLM-drafted graphs. Where possible, add one non-LLM-authored named benchmark as a check: Causal Chambers or CausalMan. CausalVerify's same-family finding is the closest published support.
5. **Use Causal Chambers as the physical-truth check, not as an orientation test.** Its Mk1 graphs are depth 1, so orientation is trivial once actuator columns are known. Use it to test power and nonlinearity, and for the interventional path.
6. **Use the post-cutoff and fictitious-name designs for the knowledge-elicitation runs (AU10).** These are the Srivastava graphs and the Feng et al. design. Avoid bnlearn, Sachs and Tübingen except as positive memorisation controls.
7. **For AU4:** the three gaps above are the requirements list. CausalDS (effects) and ACDB (active discovery) are the nearest prior art to position against.

## Open questions

- CausalArena's CD-CSG source (reference [44]) and Appendices B and C were not in the fetched text. Is any CausalArena real table derived from the Tübingen pair sources?
- Does CausalArena's semantic workflow record which LLM drafted each graph? That is needed to test a same-family advantage.
- What are the measured varsortability and R2-sortability of CausalArena, CausalMan and the Causal-Copilot suite? (Computable locally.)
- Does CLadder still ship its nonsensical/anti-commonsense variants in v1.5, and are DREAM4 labels anonymous? (Not verified today.)
- CausalBench-GSK and Benchpress maintenance status (no commit dates visible).
- Is the Srivastava novel-graph set released beyond the anonymous review repository?

## Not read

| Source | Reason |
|---|---|
| https://www.pnas.org/doi/10.1073/pnas.0913357107 (DREAM PNAS 2010) | fetch error |
| https://www.science.org/doi/10.1126/science.1105809 (Sachs 2005) | fetch error; PubMed abstract read instead |
| https://openreview.net/forum?id=pAoqRlTBtY (Causal Modelling Agents) | browser-verification wall |
| https://www.sciencedirect.com/science/article/pii/S2405471220302878 (SERGIO) | robots.txt; SERGIO has no row |
| https://github.com/huawei-noah/trustworthyAI/tree/master/datasets | robots.txt; gCastle dataset contents unknown |
| https://github.com/cbg-ethz/Benchpress | fetch error |
| https://arxiv.org/abs/2606.01789 | HTTP 429; inconsistency rates from prior note cluster8 |
| https://www.nature.com/articles/s41592-024-02443-2 | fetch error; identity unknown, unused |
| CausalArena reference list, Appendices B/C | not in fetched HTML |
| https://arxiv.org/abs/2409.19158 (bnRep paper), https://arxiv.org/abs/2308.15395 (GSK challenge) | not opened; CRAN page and project note used |
| Venue pages for CausalTime (ICLR 2024), CausalProbe (NeurIPS 2024), CausalVerse and CausalDynamics (NeurIPS 2025 D&B), CausalGraph2LLM (NAACL Findings 2025) | venue taken from search-result listings only |

## Searches run

Web searches (all 2026-10-12):

- CIPCaD-Bench continuous industrial process datasets benchmarking causal discovery
- CausalVerse benchmark causal representation learning simulation arXiv
- CausalPlayground python library structural causal models arXiv
- OCDB open causal discovery benchmark LLM arXiv 2024
- CausalBench causal learning benchmark platform Arizona State Kapkiç Wang causalbench.org
- DREAM4 in silico network challenge GeneNetWeaver gold standard knockouts time series 10 100 genes
- CausalDynamics benchmark large-scale time series causal discovery climate arXiv 2025
- PetShop dataset root cause analysis microservices causal arXiv
- RCAEval benchmark root cause analysis microservice systems arXiv 2412.17015
- CSuite causal discovery inference benchmark datasets Microsoft Geffner deep end-to-end causal inference
- neuropathic pain diagnosis simulator causal discovery Tu Zhang Kjellström NeurIPS 2019 222 nodes
- bnRep repository Bayesian networks from the literature Leonelli R package
- CausalProbe 2024 "Unveiling Causal Reasoning in Large Language Models: Reality or Mirage" arXiv
- CRAB benchmark causal relationships real-world events strength Romanou EMNLP 2023 arXiv
- CausalBench Zeyu Wang SIGHAN 2024 comprehensive benchmark evaluating causal reasoning capabilities of LLMs
- gCastle real telecom alarm dataset topology PCIC 2021 causal discovery competition ground truth
- Mooij Joint Causal Inference Sachs flow cytometry ground truth consensus network disagreement
- new benchmark causal discovery 2026 arXiv real-world ground truth dataset (extended)
- benchmark LLM causal discovery memorization anonymized variable names novel graphs 2025 2026 (extended)
- NetSim Smith 2011 network modelling methods for FMRI simulated BOLD 28 simulations benchmark causal
- ChaLearn cause-effect pairs challenge Guyon 2013 Kaggle dataset
- "CausalTime" Cheng ICLR 2024 realistically generated time-series benchmark causal discovery openreview

Direct page reads (about 75): the arXiv abstract or HTML pages, proceedings pages, Hugging Face cards, GitHub READMEs and project sites listed in each JSON row's `sources`. The arXiv export API was blocked by the proxy (403), so every arXiv read went through the web page.

"Not found" statements above refer only to these searches and reads.

**Where we're going:** AU4 can take the three gaps as its requirements. BEN-07 should first add the sortability audit and the crossed name x layout arms on CausalArena's public semantic files. Both run locally with no API cost.
