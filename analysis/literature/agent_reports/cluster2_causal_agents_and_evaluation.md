# Literature scan: causal analysis agents, causal AutoML, and how they are evaluated

## Where we are now

I located and read 26 works. The scan is incomplete in one specific way: the shared web-search budget ran out after about 25 queries, so the citing-works sweep for Causal-Copilot (Google Scholar / Semantic Scholar) was not finished.

Pages I could not read:
- `arxiv.org/html/2609.31675` (Active Causal Discovery Benchmark) — rate limited.
- `arxiv.org/abs/2504.13263v3` — rate limited, so Causal-Copilot's version history is confirmed only up to v2; whether v3 exists is unverified.
- The OpenReview PDF for Causal AI Scientist — 403.
- The Semantic Scholar API — 429.

Reliability caveat: details below come from an automated reader over each paper's HTML or PDF, not from my reading the PDFs line by line. Titles, authors and URLs are solid. Re-check every number against the PDF before quoting it; I flag the ones that look wrong.

## A. Agents, hybrid LLM+statistics pipelines, causal AutoML

### 1. CausalSteward (CaST)
Tagliapietra, Marchioni, Willig, Luettin, Halilaj, Kersting. "CausalSteward: An Agentic Divide-Conquer-Combine Copilot for Causal Discovery." arXiv:2607.01936, 2 July 2026. https://arxiv.org/abs/2607.01936 (tables read via https://www.alphaxiv.org/abs/2607.01936.md)
1. **Problem:** causal discovery on high-dimensional data where manual constraint specification is intractable.
2. **Architecture:** Explain, Divide, Conquer, Combine. LLM hypothesis and critic agents partition variables and propose local graphs; FCI/ICD run on each partition seeded with LLM edges; local graphs are merged by union. RAG and human-in-the-loop are optional.
3. **Implicit:** no per-edge provenance or audit trail is described. The ethics statement admits sensitivity to data leaks in retrieved content.
4. **Guarantees:** conditional only. If the partitioning is causally correct, the union of local graphs recovers the global graph; appendix error bounds cover imperfect partitions.
5. **Evaluation:**
   - Datasets: CausalMan Small (53 nodes) and Medium (186 nodes), Neuropathic Pain (222 nodes), CausalChambers.
   - Metrics: F1, precision, SHD; 5 seeds with mean and standard deviation.
   - Baselines: FCI, XGES, GranDAG, BOSS, LLM-BFS, LLM-Pairwise, and **Causal-Copilot**.
   - Ablations: RAG, human-in-the-loop, partition size, and critic agents. Removing critics drops Small from F1 0.42-0.48 to 0.29 and precision to 0.38.
   - No variable anonymisation or memorisation control.
6. **Relevance:** the only independent evaluation of Causal-Copilot I found.
   - Reported Causal-Copilot results: Small F1 0.078 / SHD 117.4; Medium F1 0.014 / precision 0.211 / SHD 547; Neuropathic F1 0.334.
   - The authors write: "CausalCopilot was steered towards XGES, as it often preferred intractable methods such as FCI."
   - On Medium, Causal-Copilot's row is identical to the XGES row. This is consistent with your finding that the scored graph is the raw algorithm output, but it is my inference, not their claim. On Small its numbers differ from the plain FCI row.
   - On Neuropathic Pain the LLM-heavy CaST scores F1 0.10-0.13, below XGES (0.309) and Causal-Copilot (0.334).
   - Left open: stage attribution inside Causal-Copilot, and memorisation.

### 2. Causal Ensemble Agent (CEA)
Li, Wang, Li, Zhou, Gao, Han, Liu, Zhang, Bondell, Gong. "Causal Ensemble Agent: Hierarchical Causal Discovery with LLM-guided Expert Reweighting." arXiv:2606.10607 (June 2026 by ID; exact date and venue unverified). https://arxiv.org/abs/2606.10607
1. **Problem:** discovery algorithms disagree, and directly asking an LLM for edges is unreliable.
2. **Architecture:** the LLM is a "meta-referee". Six algorithms (PC, FCI, GES, BOSS, GRaSP, ICA-LiNGAM) produce bootstrap support per relation. Only relations near the decision threshold trigger an LLM call, which returns 0-10 weights per algorithm. Three layers follow: skeleton, v-structures, orientation with Meek closure. Explicit state is the per-relation support scores, the dispute set and the weights.
3. **Implicit:** the LLM's rationale for its weights.
4. **Guarantees:** fused scores stay within the min/max of the expert estimates (convex-hull lemma).
5. **Evaluation:**
   - Datasets: bnlearn Alarm, Asia, Child, Insurance, Sachs at four sample sizes; Alzheimer, Arctic-Sea, Sangiovese.
   - Metrics: normalised-Hamming ratio and precision-recall AUC.
   - Ablations: LLM weights versus uniform weights (removing the LLM degrades the Hamming ratio by 41.9%); LLM as direct edge expert versus referee; prompt components. Standard deviations over 5 LLM runs.
   - Memorisation: not controlled by renaming. They note the direct-LLM baseline is perfect on Asia and call it a "potential benchmark-leakage signal".
6. **Relevance:** a clean template for ablating an LLM stage against a no-LLM version of the same pipeline, with the LLM-touched relations explicit. Causal-Copilot is not a baseline. No anonymised-name control.

### 3. LLM-Augmented Causal Discovery (probabilistic fusion)
Kitson, Constantinou. "LLM-Augmented Causal Discovery: Probabilistic Fusion of Edge Existence and Orientation." arXiv:2608.27472, 19 Aug 2026. https://arxiv.org/abs/2608.27472
1. **Problem:** combining unreliable LLM causal knowledge with structure learning.
2. **Architecture:** each edge carries a probability distribution over four states (forward, backward, undirected, absent), built separately per source. Sources are 18 LLM responses (3 models, 2 prompt levels, 3 repetitions) and FGES/Tabu/PC over data samples. They are fused 50/50 and a DAG is extracted greedily.
3. **Implicit:** probabilities are uncalibrated; no latent confounding.
4. **Guarantees:** none stated.
5. **Evaluation:**
   - 26 networks (8-70 variables) from bnlearn, bnRep and Bayesys; F1 and SHD.
   - **Variable-name obfuscation** against memorisation, plus a post-hoc audit of benchmark identifiability (correlation with improvement ρ = 0.14-0.18).
   - Fusion beats the better single source in 22 of 26 networks, mean F1 gain 0.056 (p < 0.001).
   - Structure learning has higher edge recall (80.2% vs 60.3%); the LLM has higher orientation accuracy (96% vs 77%).
   - Ablations over LLM models, algorithms, prompt detail and sample size.
6. **Relevance:** the closest published thing to per-edge, per-source state, and it controls memorisation. It is a fusion method, not an agent; there is no algorithm selection and data are clean and discrete.

### 4. Causal Discovery in the Era of Agents
Zheng, Verma, Gill, Dai, Spirtes, Zhang. "Causal Discovery in the Era of Agents." arXiv:2606.23608 (June 2026 by ID). https://arxiv.org/abs/2606.23608
1. **Problem:** a position-plus-system paper on what role agents should have.
2. **Architecture:** causal-learn+, where the agent coordinates tools and explains assumptions but "should not supply edges, orientations, priors, constraints or causal conclusions".
3. **Implicit:** the audit structure is advocated but not formally specified.
4. **Guarantees:** none new; causal claims rest on the underlying algorithms.
5. **Evaluation:** none systematic. It calls for "benchmarks that test whether agents improve data diagnosis, method selection and calibrated interpretation".
6. **Relevance:** it explicitly calls for "audit trails that separate data, assumptions, agent recommendations, user decisions and algorithmic outputs". That supports your provenance finding as an open problem. It does not mention Causal-Copilot in the text read.

### 5. Causal Modelling Agents (CMA)
Abdulaal, Hadjivasiliou, Montana-Brown, He, Ijishakin, Drobnjak, Castro, Alexander. "Causal Modelling Agents: Causal Graph Discovery through Synergising Metadata- and Data-driven Reasoning." ICLR 2024. https://openreview.net/forum?id=pAoqRlTBtY (metadata: https://mlanthology.org/iclr/2024/abdulaal2024iclr-causal)
1. **Problem:** combining LLM metadata reasoning with data-driven deep structural causal models.
2. **Architecture:** a loop of LLM hypothesis (JSON graph via function calling), model fit (likelihood), a memory of graph changes and likelihood shifts, and global then local edge amendment with keep/remove/reverse/add.
3. **Implicit:** the memory rationales are LLM text; edge-edit history is not exposed as provenance.
4. **Guarantees:** the fit signal is valid only up to the Markov equivalence class.
5. **Evaluation:**
   - Arctic sea ice, Sangiovese, an expert-consensus Alzheimer's graph (11 nodes) and an ADNI case study; normalised-Hamming ratio.
   - Compares LLM-only, data-only (NOTEARS, DAG-GNN) and combined; combined is best (Alzheimer's ratio 0.21 vs 0.27 for GPT-4).
   - No component ablation, no memorisation control, benchmark results appear to be single runs.
6. **Relevance:** the early template for iterative LLM graph amendment. Whether amendment helps beyond the LLM prior is shown only by aggregate comparison.

### 6. MATMCD
Shen, Chen, Luo, Xu, Chen, Ni. "Exploring Multi-Modal Integration with Tool-Augmented LLM Agents for Precise Causal Discovery." arXiv:2412.13667; a Findings of ACL 2025 entry exists (2025.findings-acl.36; I did not open that page). https://arxiv.org/abs/2412.13667
1. **Problem:** refining a statistical causal graph with retrieved textual knowledge.
2. **Architecture:** an initial graph from PC, Exact Search or DirectLiNGAM. A data-augmentation agent retrieves web and log context; a constraint agent emits yes/no edge constraints; the algorithm is rerun under them. Constraint matrices are explicit.
3. **Implicit:** which retrieved document drove which constraint.
4. **Guarantees:** none.
5. **Evaluation:**
   - AutoMPG, DWDClimate, Sachs, Asia, Child, and two AIOps systems.
   - Raw PC versus refined: AutoMPG normalised Hamming 0.32 to 0.04; Sachs 0.19 to 0.14; Asia SHD unchanged at 6.
   - Ablations on search rounds, base algorithm and LLM. Retrieval was screened for ground-truth leakage. No name anonymisation; MATMCD results appear single-run.
6. **Relevance:** a before/after refinement comparison exists here, but only on famous named benchmarks.

### 7. ALCM
Khatibi, Abbasian, Yang, Azimi, Rahmani. "ALCM: Autonomous LLM-Augmented Causal Discovery Framework." arXiv:2405.01744 (2024; venue unverified). https://arxiv.org/abs/2405.01744
1. **Problem:** automating graph refinement with an LLM.
2. **Architecture:** PC/LiNGAM/NOTEARS voting, a prompt-building "causal wrapper", and a GPT-4 refiner that validates, adds and reorients edges and assigns confidences.
3. **Implicit:** no record of which edges the LLM changed.
4. **Guarantees:** none.
5. **Evaluation:** Asia, Cancer, Child, Insurance, Neuropathic, Sachs, Sangiovese. It reports PC versus ALCM-PC versus ALCM-Hybrid, with refinement always better (for example Asia normalised Hamming 0.143 to 0.089). No variance, no memorisation control, no component ablation. The dataset sizes my reader extracted (Asia "11 nodes, 18 edges") look wrong; check the PDF.
6. **Relevance:** the architecture most similar to Causal-Copilot's LLM refiner. It claims uniform improvement, but under exactly the conditions (bnlearn names, single runs) your findings call into question.

### 8. CauScientist
Peng, Chen, Xu, Lu. "CauScientist: Teaching LLMs to Respect Data for Causal Discovery." arXiv:2601.13614 (Jan 2026 by ID). https://arxiv.org/abs/2601.13614
1. **Problem:** LLM proposals that contradict the statistics.
2. **Architecture:** start from the better of an FCI/AVICI graph and an LLM graph (chosen by an intervention-aware BIC). The LLM proposes atomic ADD/DEL/REV edits; each is accepted only if valid and BIC-improving; rejected edits go to an error memory.
3. **Implicit:** nothing obvious beyond the LLM's reasons for each proposal.
4. **Guarantees:** every accepted edit is BIC-improving and acyclic.
5. **Evaluation:** Cancer, Asia, Child, Alarm; F1 and SHD; 5 repeats averaged with no variance tables. No anonymisation and no component ablation.
6. **Relevance:** a design where each LLM edit is individually gated and logged, a natural contrast to an ungated refinement stage.

### 9. DMCD
KaPatel, Nikiforova, Saggese, Smith (Causify AI). "DMCD: Semantic-Statistical Framework for Causal Discovery." arXiv:2602.20333 (Feb 2026 by ID). https://arxiv.org/abs/2602.20333
1. **Problem:** using variable metadata as a prior, then verifying with data.
2. **Architecture:** the LLM drafts a DAG from metadata; conditional-independence tests with FDR control flag missing and spurious edges for revision.
3. **Implicit:** which draft edges survived for which reason.
4. **Guarantees:** none.
5. **Evaluation:**
   - Tennessee Eastman, Fluxnet2015, IT monitoring; 10 runs with standard deviations.
   - Explicit memorisation probes: sentence completion and dataset identification.
   - Renaming variables to X1..Xn with rephrased descriptions kept F1 high (Fluxnet 0.79).
   - Removing descriptions on Tennessee Eastman dropped F1 from 0.209 to 0.07.
   - Notes that temperature 0 does not give determinism.
6. **Relevance:** a reusable memorisation-probe protocol. Company-authored; not an agent with algorithm selection.

### 10. ABAPC-LLM
Li, Russo. "Leveraging Large Language Models for Causal Discovery: a Constraint-based, Argumentation-driven Approach." arXiv:2602.16481 (Feb 2026 by ID; venue unverified). https://arxiv.org/abs/2602.16481
1. **Problem:** using LLM priors rigorously while separating memorisation from generalisation.
2. **Architecture:** LLM constraints are kept only if unanimous across 5 queries, then enter a causal assumption-based argumentation solver alongside weighted independence statements.
3. **Implicit:** nothing notable; constraints are structured.
4. **Guarantees:** the output is a stable extension of the argumentation framework.
5. **Evaluation:**
   - bnlearn plus a new protocol: random DAGs mapped by subgraph isomorphism onto the CauseNet knowledge graph, so names are meaningful but the whole graph is unseen.
   - 54 such DAGs, 50 repetitions; SHD, SID, F1.
   - LLM-BFS reaches 100% recall on Asia and Sachs, flagged as a memorisation concern.
6. **Relevance:** the best synthetic-with-semantics generator I found for your memorisation control.

### 11. Multi-Agent Causal Discovery (MAC)
Le, Xia, Chen. "Multi-Agent Causal Discovery Using Large Language Models." arXiv:2407.15073 (venue unverified). https://arxiv.org/abs/2407.15073
- LLM agents debate to select a statistical algorithm; an affirmative/negative/judge debate then refines the graph.
- It is evaluated on five datasets against PC, FCI, GES, DirectLiNGAM and LLM baselines. Dataset names, numbers, ablations and controls were not in the text I could read: unverified.
- **Relevance:** another system with both LLM algorithm selection and LLM refinement.

### 12. Causal Agent
Han, Kuang, Zhao, Ye, Wu. "Causal Agent based on Large Language Model." arXiv:2408.06849 (2024; venue unverified). https://arxiv.org/abs/2408.06849
1. **Problem:** LLMs cannot reason causally over tabular data unaided.
2. **Architecture:** a ReAct loop over causal-learn and EconML tools. Memory holds causal graphs as Python objects, not text.
3. **Implicit:** algorithm and hyperparameter choice (PC and LinearDML are effectively fixed).
4. **Guarantees:** none.
5. **Evaluation:** a synthetic question-answering benchmark of about 1.4K questions with variable names randomly drawn from a 311-word pool, so names carry no causal signal. Accuracy at four levels (for example whole-graph 81.8%). No ablations and no variance.
6. **Relevance:** random variable naming is a simple memorisation control. It scores question answering, not graph recovery.

### 13. LLM4Causal
Jiang, Ge, Gao, Wang, Song. "LLM4Causal: Democratized Causal Tools for Everyone via Large Language Model" (later versions titled "LLM4Causal: Large Language Model for Causal Decision Making"). arXiv:2312.17122. https://arxiv.org/abs/2312.17122
1. **Problem:** routing lay causal questions to the right tool.
2. **Architecture:** a fine-tuned Llama-2 turns the query into a JSON task specification, runs the tool, and interprets the output.
3. **Implicit:** uncertainty in the estimates.
4. **Guarantees:** none.
5. **Evaluation:** synthetic data; pass, relevance and win rates against GPT-4 with function calling. Stage-wise variants (retrieve-only, interpret-only) are tested. Standard deviations are reported.
6. **Relevance:** an early example of stage-separated metrics for a causal pipeline.

### 14. Causal AI Scientist (CAIS)
Verma, Acharya, Bhardwaj, Simko, Yang, Haghighat, Janzing, Sachan, Schölkopf, Jin. "Causal AI Scientist: Facilitating Causal Data Science with Large Language Models." NeurIPS 2025 workshop (CauScien). https://neurips.cc/virtual/2025/124113 (a later version, "Towards End-to-End Causal Inference with Large Language Models", is an ICML 2026 workshop poster: https://icml.cc/virtual/2026/74805)
- An effect-estimation agent: the LLM identifies variables, a decision tree selects the method, and a validation loop tests assumptions.
- The project documentation describes a state manager and recorded decision paths (https://causal-agent.readthedocs.io/en/latest/theory/agent_architecture.html).
- I could not read the paper PDF, so evaluation details are unverified beyond the abstract (textbook, synthetic and real queries; CauSciBench in the later version).
- **Relevance:** method selection is a deterministic tree rather than LLM free text, a design contrast to Causal-Copilot's knowledge-memory selection.

### 15. CATE-B
Berrevoets, Piskorz, Davis, Amad, Weatherall, van der Schaar. "Technical Report: Facilitating the Adoption of Causal Inference Methods Through LLM-Empowered Co-Pilot." arXiv:2508.10581. https://arxiv.org/abs/2508.10581
- A treatment-effect copilot: discovery algorithm, then RAG-based LLM edge orientation, then a "minimum uncertainty adjustment set", then estimation.
- A central "state bank" stores intermediate artefacts and the front end logs decisions.
- Evaluated on two small datasets with 10 runs; no memorisation control.
- **Relevance:** explicit intermediate state in a causal copilot, without per-edge provenance evaluation.

### 16. CausalAgent (demo)
Zhu, Chen, Cai. "CausalAgent: A Conversational Multi-Agent System for End-to-End Causal Inference." arXiv:2602.11527 (IUI Companion 2026). https://arxiv.org/abs/2602.11527
- A three-agent demonstration with RAG and MCP. Its only case study is Sachs, with no quantitative evaluation.
- **Relevance:** an example of the unevaluated-agent pattern, demonstrated on a memorisable benchmark.

### 17. AutoCD (Bayesian optimisation)
Chan, Claassen, Hoos, Heskes, Baratchi. "AutoCD: Automated Machine Learning for Causal Discovery Algorithms." PGM 2024, PMLR 246:106-132. https://proceedings.mlr.press/v246/chan24a.html
- Non-LLM algorithm and hyperparameter search by Bayesian optimisation, comparing two label-free loss functions and post-hoc corrections.
- Evaluated on data simulated from 45 graphical models by average rank: the PC-warm-started variant ranks 3.69, versus 5.21 for the best tuning baseline and 4.36 for the best tuned single algorithm.
- **Relevance:** the non-LLM baseline an LLM selector should be compared against.

### 18. AutoCD (Tsamardinos group), OCT and ETIA
- Biza, Ntroumpogiannis, Triantafillou, Tsamardinos. "Towards Automated Causal Discovery: a case study on 5G telecommunication data." arXiv:2402.14481. https://arxiv.org/abs/2402.14481
- Biza, Tsamardinos, Triantafillou. "Tuning Causal Discovery Algorithms." PGM 2020, PMLR 138:17-28. https://proceedings.mlr.press/v138/biza20a.html
- ETIA library: https://etia.readthedocs.io/en/latest/ (authors not stated on the page).
- No LLM. Three modules: feature selection, causal learning tuned by out-of-sample causal tuning (each node predicted from its Markov boundary under cross-validation), and reasoning/visualisation.
- Per edge it records bootstrap edge confidence and "edge consistency frequency", and evaluates those confidences by AUC against truth.
- **Relevance:** it evaluates the bootstrap-confidence stage directly, which Causal-Copilot's benchmark does not.

### 19. Hyperparameter robustness
Machlanski, Samothrakis, Clarke. "Robustness of Algorithms for Causal Structure Learning to Hyperparameter Choice." CLeaR 2024, PMLR 236:703-739. https://proceedings.mlr.press/v236/machlanski24a.html
- Grid search over the hyperparameters of PC, FCI, FGES, NOTEARS, NOTEARS-MLP, LiNGAM, ANM and CAM.
- Data: Erdős-Rényi and scale-free graphs, 10/20/50 nodes, two densities, three sample sizes, linear non-Gaussian and nonlinear, plus Sachs and SynTReN.
- Compares BEST (oracle), WORST, DEFAULT and simulation-tuned settings. The winning algorithm changes with hyperparameter quality.
- **Relevance:** gives you an oracle-regret framing for scoring LLM hyperparameter choices.

### 20. PyWhy-LLM
https://github.com/py-why/pywhy-llm — an experimental library of LLM "suggesters" for modelling, identification and validation, with a CauseNet RAG variant. The repository page reports no benchmark. It is a library, not a paper.

## B. Evaluation, pitfalls, memorisation, agent reliability

### 21. Science-grounded novel benchmarks
Srivastava, Nagalapatti, Jajoo, Vashishtha, Krishnamurthy, Sharma. "Realizing LLMs' Causal Potential Requires Science-Grounded, Novel Benchmarks." arXiv:2510.16530, 18 Oct 2025. https://arxiv.org/abs/2510.16530
- Three memorisation tests: node completion, edge completion and subgraph completion from partial context.
- GPT-4 reconstructs bnlearn graphs (Asia near-perfect with zero context) but scores about 0 on four graphs taken from post-cutoff papers (Alzheimer's, two COVID-19 graphs, Sweden transport).
- On the novel graphs, PC seeded with an LLM prior beats both parts (Alzheimer's F1: PC 0.51, LLM 0.56, hybrid 0.73). The LLM alone is below PC on Sweden transport (0.31 vs 0.57).
- **Relevance:** the direct published precedent for your Sachs-recognition finding, at the level of the bare LLM rather than an agent. No anonymisation arm.

### 22. LLM cannot discover causality (position)
Wu, Yu, Wu, Tan. "LLM Cannot Discover Causality, and Should Be Restricted to Non-Decisional Support in Causal Discovery." arXiv:2506.00844, 1 June 2025. https://arxiv.org/abs/2506.00844
- Argues LLM outputs should never determine edge existence or direction.
- Claims prior positive results on bnlearn come partly from prompts that leak ground truth. Experiments use 14 bnlearn datasets with high- versus low-quality prompts.
- **Relevance:** theoretical backing for auditing an LLM refinement stage. It does not test an agent's refinement stage.

### 23. Kıcıman et al.
Kıcıman, Ness, Sharma, Tan. "Causal Reasoning and Large Language Models: Opening a New Frontier for Causality." arXiv:2305.00050 (TMLR per the OpenReview link; year unverified). https://arxiv.org/abs/2305.00050
- A row-completion memorisation test on the Tübingen pairs: GPT-4 recalls 61% of cells and 25% of complete rows.
- Partial memorisation of the neuropathic dataset by GPT-3.5; none for Arctic sea ice.
- Includes a post-cutoff set of 67 new pairs.

### 24. Varsortability
Reisach, Seiler, Weichwald. "Beware of the Simulated DAG! Causal Discovery Benchmarks May Be Easy To Game." NeurIPS 2021. https://arxiv.org/abs/2102.13647
- In common simulated additive-noise settings, marginal variance increases along the causal order (varsortability above 0.94 on average for linear models).
- A trivial "sort by variance and regress" baseline matches the state of the art; NOTEARS-type methods fail on standardised data.
- **Relevance:** your synthetic generator and Causal-Copilot's must be checked for this before any F1 comparison means anything.

### 25. Landscape of causal discovery data
Brouillard, Squires, Wahl, Körding, Sachs, Drouin, Sridhar. "The Landscape of Causal Discovery Data: Grounding Causal Discovery in Real-World Applications." arXiv:2412.01953. https://arxiv.org/abs/2412.01953
- Argues the field relies on synthetic data and a narrow set of real datasets, with "inadequate metrics".
- It has an appendix on the Sachs dataset, but that text was not in the HTML I could read, so its specific Sachs criticisms are unverified. I found no other dedicated Sachs critique before the search budget ran out.

### 26. Stage-separated causal-inference benchmarks
- **CauSciBench.** Acharya et al. "CauSciBench: Can LLMs Automate Causal Inference in Real-World Scientific Research?" ICML 2026, PMLR 306:332-384. https://proceedings.mlr.press/v306/acharya26a.html
  - Scores method selection accuracy separately from the relative error of the estimate.
  - The preprint reports the best model at 77% method accuracy but 49% relative error on real papers, with single attempts per task. It states that specialised causal agents such as Causal-Copilot are not evaluated.
- **CausalReasoningBenchmark.** Sawarni, Tan, Syrgkanis. arXiv:2602.20571. https://arxiv.org/abs/2602.20571
  - Requires a structured JSON identification specification scored field by field, separately from the estimate.
  - The evaluated model gets the strategy right 79.2% of the time but the full specification only 34.1%.
- **CausalVerify.** Zhang, Correia, Parra, Xie. arXiv:2609.07944, 7 Sept 2026. https://arxiv.org/abs/2609.07944
  - Layered scoring from "output exists" to "executed estimate matches the canonical estimate". 15.5% of executable workflows return wrong estimates.
  - Fixed-seed synthetic data with anonymised variables. Retrospective self-confidence does not separate right from wrong. Prompts with hashes and scorer decision records are released.
- **CausalDS.** Leban, Sun. arXiv:2607.08093, 9 July 2026. https://arxiv.org/abs/2607.08093
  - 953 fully synthetic scenes with hidden structural causal models.
  - A "verbalisation-swap" ablation holds graph and data fixed while changing only names and story. Reports pass@k and run-to-run stability.
- **DiscoveryBench.** Majumder et al. arXiv:2407.01725 (ICLR 2025 per ML Anthology). https://arxiv.org/abs/2407.01725 — final-hypothesis scoring only; intermediate steps are not evaluated.
- **ScienceAgentBench.** Chen et al. arXiv:2410.05080 (ICLR 2025 per ML Anthology). https://arxiv.org/abs/2410.05080 — three independent runs per task, five-stage rubrics, and dataset perturbations against contamination.

### 27. Run-to-run variance
- Mehta. "When Agents Disagree With Themselves: Behavioral Consistency as an Uncertainty Signal for LLM Agents." arXiv:2602.11619. https://arxiv.org/abs/2602.11619
  - 10 runs per task. Tasks with at most 2 distinct action sequences reach 82-87% accuracy; those with 4 or more reach 41-65%.
  - Single-run evaluations misrank models 29.3% of the time. It measures the step at which runs first diverge.
- Alvarado Gonzalez et al. "Do Repetitions Matter? Strengthening Reliability in LLM Evaluations." arXiv:2509.24086. https://arxiv.org/abs/2509.24086
  - Single-run leaderboards invert at least one pairwise rank in 10 of 12 slices; two runs remove about 83% of inversions.

### Leads named in the brief that I did not verify
Not located in this session (so no details given): StARS, CLadder, Corr2Cause, "Causal parrots", CausalBench (Zhou et al.), MLAgentBench, Long et al. "Causal Discovery with Language Models as Imperfect Experts" (arXiv:2307.02390; abstract only partly read), Jiralerspong et al. (LLM-BFS).

Titles seen but pages not read:
- Active Causal Discovery Benchmark (arXiv:2609.31675)
- CausalSmith (arXiv:2607.22511)
- Causal MAS survey (arXiv:2509.00987) — read; it lists Causal-Copilot descriptively and says standard benchmarks for causal multi-agent systems "are still lacking"

## (i) Synthesis

Systems that put an LLM into causal discovery fall into three designs:
- **LLM as post-hoc refiner** of an algorithm's graph: ALCM, MATMCD, MAC, Causal-Copilot.
- **LLM as prior or constraint source** gated by statistics: CMA, CauScientist, DMCD, ABAPC-LLM, Kitson and Constantinou.
- **LLM kept out of edge decisions:** CEA's referee role, and the positions of Zheng et al. and Wu et al.

The field moved toward the second and third designs during 2025-2026, driven by memorisation evidence. Srivastava et al. show GPT-4 reconstructs bnlearn graphs from their names but fails on post-cutoff graphs; CEA and ABAPC-LLM both flag perfect LLM scores on Asia or Sachs as leakage.

Evaluation practice lags. Most refiner papers report gains only on famous named benchmarks, single runs, with no renaming control. The exceptions are Kitson and Constantinou (name obfuscation), DMCD (renaming plus probes), ABAPC-LLM (CauseNet-grounded random DAGs) and CausalDS (verbalisation swap).

On the effect-estimation side, benchmarks now score stages separately (CausalReasoningBenchmark, CausalVerify, CauSciBench) and show that plausible intermediate choices and runnable code often yield wrong estimates. No equivalent stage-separated benchmark exists for discovery agents.

Causal AutoML without LLMs (both AutoCD systems, OCT, Machlanski et al.) supplies label-free selection baselines and an oracle-regret framing that LLM selectors have not been measured against.

Agent-reliability work shows single-run rankings are unstable, yet most causal-agent papers report single runs.

## (ii) The two specific questions

**Has anyone ablated an LLM refinement stage against ground truth?** Partly.
- Before/after or with/without-LLM comparisons exist for hybrid methods: MATMCD and ALCM (PC versus refined), CEA (LLM versus uniform weights), CausalSteward (critic agents removed), Kitson and Constantinou (fusion versus either source), Srivastava et al. (PC versus PC plus LLM prior), CMA (aggregate only).
- All report that the LLM component helps on average. The only cases I found where it does not: 4 of 26 networks in Kitson and Constantinou, and Asia SHD unchanged in MATMCD.
- I found no published ablation of the bootstrap-plus-LLM refinement stage of Causal-Copilot or of any end-to-end agent with LLM algorithm selection, and no paper reporting that such a stage hurts.
- Of the positive results, only Kitson and Constantinou control memorisation by renaming.
- This is "not found in a search that was cut short", not proof of absence.

**Has anyone published per-stage provenance or audit trails for a causal agent?** Not as an evaluated artefact.
- Zheng et al. call for it.
- CATE-B and CAIS describe state stores and decision-path logging.
- ETIA records per-edge bootstrap confidence.
- Kitson and Constantinou keep per-edge, per-source probabilities.
- CEA makes the set of LLM-adjudicated relations explicit.
- CausalVerify releases scorer decision records at benchmark level.
- None records, per final edge, which stage introduced, removed or reoriented it.

## (iii) Evaluation designs to reuse

**Metrics**
- Adjacency and orientation scored separately (Kitson and Constantinou's edge recall versus orientation accuracy); F1, SHD and SID.
- Normalised-Hamming ratio against a random baseline (CMA, CEA).
- Precision-recall AUC of edge confidences against truth (CEA, Biza et al.), to test whether bootstrap frequencies are informative.
- Oracle regret for algorithm and hyperparameter choice (Machlanski's BEST/DEFAULT/WORST) and average rank (Chan et al.).

**Stage separation**
- Score the raw algorithm graph, the bootstrap-filtered graph and the LLM-reviewed graph as separate layers, as CausalVerify and CausalReasoningBenchmark do for estimation.
- Mirror CEA's LLM-versus-uniform ablation.

**Synthetic generators**
- Machlanski's grid (two graph families, three sizes, two densities, three sample sizes, linear non-Gaussian and nonlinear).
- Report varsortability, standardise, and include the sort-by-variance baseline (Reisach et al.).
- CauseNet-grounded random DAGs when names must be meaningful (Li and Russo).

**Memorisation controls**
- Same data under original, obfuscated and swapped names (Kitson and Constantinou; DMCD; CausalDS).
- Node, edge and subgraph completion probes (Srivastava et al.) and row completion (Kıcıman et al.).
- Post-cutoff graphs.
- Random-word names (Han et al.).

**Repetition**
- At least 5 seeds with standard deviations (CausalSteward, CEA) and 10 where affordable (DMCD).
- Report answer consistency, action-sequence diversity and first divergence step (Mehta).

## (iv) Closest works, 2025-2026

1. **CausalSteward** (July 2026) — the only external evaluation using Causal-Copilot as a baseline; it has a critic-stage ablation.
2. **Causal Ensemble Agent** (June 2026) — bootstrap support plus LLM adjudication with a with/without-LLM ablation and a leakage flag.
3. **Kitson and Constantinou** (Aug 2026) — per-edge, per-source fusion with name obfuscation.
4. **Zheng et al.** (June 2026) — the position that agents must not decide edges, with an explicit call for audit trails.
5. **Srivastava et al.** (Oct 2025) — memorisation tests showing bnlearn results do not transfer to novel graphs.

Runner-up: Li and Russo (Feb 2026), for the CauseNet-grounded protocol.

## Where we're going

- **Finish the citing-works sweep** for Causal-Copilot and confirm whether an arXiv v3 exists; this needs a fresh search budget.
- **Open the CausalSteward PDF** to confirm the Causal-Copilot baseline rows, and check whether they scored its raw or refined graph.
- **Re-check every number quoted above against the PDFs** before it enters the capstone.
- **Read the unread pages:** Active Causal Discovery Benchmark, the CAIS paper, and the Sachs appendix in Brouillard et al.
- The design the literature most clearly leaves open is a three-layer score (raw, bootstrap-filtered, LLM-reviewed) under original versus obfuscated names with at least 5 seeds.