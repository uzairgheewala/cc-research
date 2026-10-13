# Cluster report: fallible experts, human-in-the-loop, and active causal discovery

## Where we are now

I located 22 core works and about 25 supporting ones, each opened or surfaced in this session with a URL. The shared web-search budget ran out partway through, so a few leads could not be located and are listed as gaps at the end. Numbers below are as reported by the fetched pages (read through a summarising fetch tool, so spot-check any figure before quoting it in the capstone). "Unverified" marks details I could not confirm.

Short version of the findings:
- Only one located method gives the "true graph stays in the returned class with probability at least 1 − η" guarantee for LLM pairwise answers (Long et al. 2023), and its own LLM case study breaks it.
- One 2026 paper measures calibration of LLM direct-edge judgements head-on (Kumar et al., arXiv 2608.23660).
- No located system does what Causal-Copilot lacks: choosing between asking the LLM, asking a human, and running an experiment for an unresolved pair.

---

## Core works (six fields each)

### A. Fallible experts, calibration, abstention, error control

**1. Long, Piché, Zantedeschi, Schuster, Drouin (2023). "Causal Discovery with Language Models as Imperfect Experts." ICML 2023 workshop on Structured Probabilistic Inference & Generative Modeling.** https://arxiv.org/abs/2307.02390
1. Problem: orient the undirected edges of a Markov equivalence class (MEC) using an expert who may be wrong.
2. Representation: an "ε-expert" is wrong with constant probability ε, given the true orientation. A Bayesian posterior over orientations uses a uniform prior over graphs in the MEC. Two greedy strategies pick the next edge: S_size (smallest resulting class) and S_risk (lowest risk of excluding the truth). Meek rules propagate orientations.
3. Implicit: the MEC from data is correct; ε is known and constant; the expert only orients and never adds or deletes edges; there is no "no edge" or "don't know" answer.
4. Guarantee: minimise the class size subject to p(G* ∈ M) ≥ 1 − η, valid under the ε-expert model.
5. Evaluation: Asia, CHILD, Insurance, ALARM; simulated experts with ε ∈ {0.1, 0.3}; text-davinci-002 and -003 with 20 randomised causal verbs.
6. Relevance: the closest formal template for our case. Its failures: on ALARM the true graph was excluded "even for small tolerance η", and text-davinci-003 was "often over-confident", underestimating exclusion risk. Open: noise models that fit LLMs, and the answers C and D.

**2. Clivio, Mahajan, Taslakian, Magliacane, Mitliagkas, Zantedeschi, Drouin (2025). "Learning to Defer for Causal Discovery with Imperfect Experts" (L2D-CD).** Venue unverified. https://arxiv.org/abs/2502.13132
1. Problem: decide per pair whether to trust the LLM or the statistical method.
2. Representation: the expert gives a binary direction with no confidence. A deferral function (random forest on text embeddings of the metadata) is trained on pairs where expert and method disagree, to predict when the expert is right.
3. Implicit: needs labelled pairs for training; one expert only; direction only (an edge is assumed to exist).
4. Guarantee: H-consistency bound for the surrogate deferral loss. This is a learning-theoretic bound, not a per-graph one.
5. Evaluation: Tübingen pairs. With RECI and GPT-4o: method alone 65.4%, expert alone 75.1%, L2D-CD 77.3%. Deferral is "domain-consistent" (it picks the expert where the expert is strong).
6. Relevance: shows LLM reliability varies by domain and can be learned. Open: the extension to more than two variables is only sketched (rank aggregation), and it does not cover "no edge".

**3. Kumar, Zarabi, Trivedy, Chen, Zhang, Fu, Ji (2026). "From Causal Plausibility to Causal Reliability: Evaluating LLMs as Calibrated Direct Causal-Edge Classifiers."** arXiv 2608.23660 (the ID indicates August 2026; the page date was not confirmed). https://arxiv.org/html/2608.23660v1
1. Problem: are LLM pairwise direct-edge answers accurate and calibrated?
2. Representation: four confidence sources (verbalised 0–100, YES/NO logits, cross-prompt agreement, cross-model agreement). No data are combined.
3. Implicit: evaluation only; open-weight models from 4B to 72B.
4. Guarantee: none.
5. Evaluation: six graphs (AsiaM to Munin1), 12 models, 5 prompts.
   - Recall exceeded precision in 94.4% of model-dataset combinations.
   - Precision fell to 0.018 on Munin1.
   - False-positive rates: 40.0% on indirect pairs, 36.0% on reversed pairs, 28.2% on other non-edges.
   - 84.6% of reversed and 80.8% of indirect false positives carried confidence of 80–100.
   - Large models: verbalised confidence ECE 0.205, AUROC 0.448; cross-prompt agreement ECE 0.016, AUROC 0.772. Differences were not significant after Holm correction.
   - Temperature scaling fixed sharpness, not ranking.
6. Relevance: direct evidence that a one-shot A/B/C/D answer at temperature 0 is not a calibrated assertion. Open: no error-controlled decision rule; Sachs is not included.

**4. Cohrs, Varando, Diaz, Sitokonstantinou, Camps-Valls (2024). "Large Language Models for Constrained-Based Causal Discovery" (chatPC).** Venue unverified. https://arxiv.org/abs/2406.07378
1. Problem: use an LLM as the conditional-independence oracle inside PC.
2. Representation: YES / NO / UNCERTAIN plus stated confidence over n repeated queries (GPT-3.5-turbo, GPT-4). Aggregation is by majority vote, confidence-weighted vote, or a binomial test at α = 0.05 with a user-chosen null (p_no ≥ p_yes, or the reverse).
3. Implicit: the test controls error relative to the LLM's own response distribution, not relative to the truth.
4. Guarantee: PC is sound only with a perfect oracle; no guarantee with the LLM.
5. Evaluation: cancer, burglary, asia, sachs and three others. The paper reports "high degree of variability" and a tendency toward conservative answers. I did not see numeric tables.
6. Relevance: the nearest precedent for treating D as a first-class answer and choosing the default direction of error. Open: a link from vote statistics to true error.

**5. Vashishtha, Reddy, Kumar, Bachu, Balasubramanian, Sharma (2023). "Causal Order: The Key to Leveraging Imperfect Experts in Causal Inference."** Venue unverified (NeurIPS 2024 workshop and ICLR 2025 pages appeared in results but were not opened). https://arxiv.org/abs/2310.15117
1. Problem: pairwise expert answers conflate direct and indirect effects.
2. Representation: triplet prompts with majority voting yield a causal order. The order orients PC's undirected edges or acts as a level prior in CaMML.
3. Implicit: no latent confounders; variables known to the LLM.
4. Guarantee: Prop. 3.1 (a perfect expert's pairwise answers give a correct order but possibly a wrong graph); Prop. 4.1 (triplets reduce an ε-expert's error to ε/(2 − ε)).
5. Evaluation: on Child with GPT-3.5, pairwise prompting gave SHD 177 with thousands of cycles, and triplets gave SHD 28 with 0 cycles. Human annotators were also tested.
6. Relevance: explains why applying A answers as direct edges is structurally unsafe, and offers D_top as a metric. Open: an order does not say which edges exist.

**6. Baldo, Ferreira, Assaad (2024). "Retrieving Classes of Causal Orders with Inconsistent Knowledge Bases."** Venue unverified. https://arxiv.org/abs/2412.14019
1. Problem: repeated LLM pairwise answers contradict each other and form cycles.
2. Representation: a self-consistency score C(X→Y), the fraction of "yes" over n queries, builds a semi-complete partially directed graph. A weighted feedback-arc-set search returns all maximally consistent acyclic tournaments.
3. Implicit: consistency is treated as a proxy for correctness.
4. Guarantee: soundness, completeness and termination; the returned class contains the true order if the knowledge base is consistent.
5. Evaluation: 11 graphs, mostly epidemiology; lowest error on 7 of 11.
6. Relevance: returns a set rather than one graph, which is the right output shape for unresolved pairs. Open: nothing when the LLM is consistently wrong.

**7. Darvariu, Hailes, Musolesi (2024). "Large Language Models are Effective Priors for Causal Graph Discovery."** arXiv preprint. https://arxiv.org/abs/2405.13551
1. Problem: evaluate LLM judgements independently of the downstream algorithm, then use them as soft priors.
2. Representation: token probabilities of options (A), (B), (C), averaged over both query directions. They enter the simulation policy of a tree-search method through a temperature-controlled softmax, optionally multiplied by mutual information.
3. Implicit: the token probabilities are not calibrated; small open models only.
4. Guarantee: none.
5. Evaluation: Asia, Child, Insurance. Metrics: fraction of correct orientations (FCO), true-edge-to-reverse-edge and true-edge-to-negative-edge ratios (TERE, TENE), and level of disagreement (LOD). A 3-way prompt beat a 2-way prompt on every metric (for example FCO higher by 0.028–0.051).
6. Relevance: supports offering C explicitly and supplies ready-made judgement-quality metrics. Open: an abstain option; error control.

**8. Takayama, Okuda, Pham, Ikenoue, Fukuma, Shimizu, Sannai (2024). "Integrating Large Language Models in Causal Discovery: A Statistical Causal Approach."** Venue unverified. https://arxiv.org/abs/2402.01454
1. Problem: feed statistical results into the prompt, then feed LLM knowledge back as constraints.
2. Representation: mean probability of "yes" over 5 runs from log-probabilities; below 0.05 becomes forbidden, 0.95 or above becomes forced, otherwise unknown. Used in PC, Exact Search and DirectLiNGAM.
3. Implicit: fixed thresholds, uncalibrated.
4. Guarantee: none.
5. Evaluation: benchmarks plus an unpublished health-screening dataset outside GPT-4's training data. A coefficient change from 1.25 to 1.30 in the prompt swung the confidence from 0.049 to 0.983.
6. Relevance: a three-zone rule with an explicit "unknown" band, and proof of prompt fragility. Open: nothing is done about pairs left unknown.

**9. Chen, Ban, Wang, Lyu, Chen (2023). "Mitigating Prior Errors in Causal Structure Learning: Towards LLM driven Prior Knowledge."** https://arxiv.org/abs/2306.07032
1. Problem: which wrong priors hurt, and can they be detected without ground truth?
2. Representation: hard edge priors in score-based search. Wrong priors are typed as irrelevant, indirect, reversed-indirect or reversed-direct. Order-reversing priors create "quasi-circles", which flag suspicious priors.
3. Implicit: enough data; faithfulness.
4. Guarantee: lemmas that reversed priors induce quasi-circles; order-consistent errors raise SHD by at most one.
5. Evaluation: Asia, Child, Alarm, Insurance; about 60% of wrong priors detected and about 90% of correct ones kept.
6. Relevance: an error taxonomy we can adopt, and a data-driven check on LLM edges. Open: indirect and irrelevant errors stay undetected.

**10. Li, Russo (2026). "Leveraging Large Language Models for Causal Discovery: a Constraint-based, Argumentation-driven Approach."** UAI 2026, PMLR 337:3631–3667. https://proceedings.mlr.press/v337/li26e.html (arXiv https://arxiv.org/abs/2602.16481)
1. Problem: let data overrule LLM constraints transparently.
2. Representation: required and forbidden arrows from 5 runs, keeping only the intersection. They enter an assumption-based argumentation solver, where a required arrow is dropped if a high-confidence independence test contradicts it.
3. Implicit: causal sufficiency; scales to about 15 nodes.
4. Guarantee: correspondence between accepted assumptions and the d-separations of the output graph; nothing about LLM error.
5. Evaluation: 54 synthetic graphs grounded in CauseNet to avoid memorisation. Consensus constraints reach precision of 0.95 or more when produced, but F1 of only 0.32–0.39 because recall is low.
6. Relevance: the cleanest published example of LLM answers being defeasible against statistical evidence. Open: no probability attached to constraints.

**11. Kitson, Constantinou (2026). "LLM-Augmented Causal Discovery: Probabilistic Fusion of Edge Existence and Orientation."** arXiv 2608.27472 (date unverified). https://arxiv.org/html/2608.27472v1
1. Problem: fuse LLM and data-driven graphs.
2. Representation: each pair gets four probabilities (forward, backward, undirected, absent). LLM and structure-learning graphs are averaged 50/50, then a greedy step extracts a DAG.
3. Implicit: the authors say the values are "empirical support", not calibrated posteriors; the weight has no principled choice.
4. Guarantee: none.
5. Evaluation: 26 networks with obfuscated variable names. Mean F1: data-driven 0.662, LLM 0.572, fusion 0.760. On Sachs: 0.606, 0.400, 0.727. LLM orientation accuracy was 96% but edge recall 60.3%.
6. Relevance: includes Sachs, and shows the LLM is good at direction and poor at existence, the opposite of how Causal-Copilot uses it. Open: calibration.

**12. Feng, Qu, Tandon, Li, Kang, Haffari (2024). "On the Reliability of Large Language Models for Causal Discovery."** Venue unverified. https://arxiv.org/abs/2407.19638
1. Problem: is LLM causal accuracy memorisation?
2. Representation: counts how often "X causes Y" appears in the open pretraining corpora of OLMo and BLOOM.
3. Implicit: frequency stands in for exposure.
4. Guarantee: none.
5. Evaluation: F1 of 0.88 in the most frequent bin versus 0.2 in the least frequent (Spearman 0.9). A supportive context raised the "yes" ratio to 0.83, and a negative one cut it to 0.33 (baseline 0.66).
6. Relevance: predicts weak performance on rarely written relations. Open: a usable reliability score per query.

**13. Srivastava, Nagalapatti, Jajoo, Vashishtha, Krishnamurthy, Sharma (2025). "Realizing LLMs' Causal Potential Requires Science-Grounded, Novel Benchmarks."** https://arxiv.org/abs/2510.16530
1. Problem: benchmark leakage.
2. Representation: memorisation tests by graph completion; four graphs from science published after training cut-offs; a hybrid where PC may not remove an edge the LLM asserts.
3. Implicit: the hybrid trusts LLM edges over independence tests.
4. Guarantee: none.
5. Evaluation: an LLM breadth-first method scored F1 0.93 on Asia and 0.54 on the novel Alzheimer's graph. PC plus LLM beat both parts on three novel graphs (for example 0.71 on COVID-19 respiratory).
6. Relevance: quantifies the drop on unfamiliar graphs. Open: a principled combination.

**14. Kıcıman, Ness, Sharma, Tan (2023). "Causal Reasoning and Large Language Models: Opening a New Frontier for Causality."** Venue unverified. https://arxiv.org/abs/2305.00050
1. Problem: how good are LLMs at pairwise direction?
2. Representation: a single prompt choosing between two directions; no uncertainty.
3. Implicit: the benchmark is in the training data.
4. Guarantee: none.
5. Evaluation: GPT-4 scored 96% (97% weighted) on Tübingen pairs. In the memorisation test GPT-4 recalled 61% of dataset cells. The authors note "unpredictable failure modes" and strong prompt dependence.
6. Relevance: the origin of the optimism behind designs like Causal-Copilot's. Open: when to trust an individual answer.

**15. Constantinou, Guo, Kitson (2023). "The impact of prior knowledge on causal structure learning." Knowledge and Information Systems 65(8):3385–3434.** https://doi.org/10.1007/s10115-023-01858-x
1. Problem: how much does each kind of knowledge help structure learning?
2. Representation: ten constraint types (required, forbidden and undirected edges, temporal order, initial graph and others) in four algorithms.
3. Implicit: knowledge is assumed correct. The paper does not study wrong knowledge systematically.
4. Guarantee: none.
5. Evaluation: required directed edges help most; forbidden edges matter more with large samples; constraints that conflict with data can increase run time.
6. Relevance: the baseline for the value of correct knowledge. Open: the effect of errors (see items 9 and 18).

### B. Human-in-the-loop and interactive discovery

**16. da Silva, Bazaluk, de Souza da Silva, Góis, Heider, Kaski, Mesquita, Ribeiro (2023; v3 retitled "Expert-Aided Causal Discovery of Ancestral Graphs").** Venue unverified. https://arxiv.org/abs/2309.12032
1. Problem: discovery with latent confounding plus uncertain expert feedback.
2. Representation: a generative flow network samples ancestral graphs in proportion to a score. Noisy expert answers about a pair reweight the samples, with no retraining. The next query is chosen by optimal experimental design.
3. Implicit: expert reliability is assumed; linear Gaussian scores. The exact likelihood form was not confirmed.
4. Guarantee: sampling is proportional to the score; no convergence rate was seen.
5. Evaluation: synthetic data, Sachs, gene networks; simulated experts and GPT-4o as a surrogate expert.
6. Relevance: asks about the most informative pair instead of all 55. Open: calibrating the reliability parameter for an LLM.

**17. Bonilla, Zhao, Steinberg (2026). "Causal Preference Elicitation." ICML 2026 poster.** https://arxiv.org/abs/2602.01483
1. Problem: pick the expert queries that most shrink posterior uncertainty.
2. Representation: a three-way categorical likelihood over {i→j, j→i, no edge} with reliability hyperparameters. A particle posterior over DAGs is updated by sequential Monte Carlo. Queries maximise expected information gain.
3. Implicit: the expert is non-adversarial; causal sufficiency.
4. Guarantee: the posterior converges to the true graph up to Markov equivalence if ambiguous edges are queried infinitely often, with an exponential finite-time rate.
5. Evaluation: on Sachs (observational only), 40 queries cut Hamming distance by about 14 and raised orientation F1 by more than 0.38; also CausalBench with 50 genes.
6. Relevance: the best located formal account of asking an expert as an information-gain decision, and it models the "no edge" answer. Open: no "don't know" option, no LLM expert, no comparison with experiments.

**18. Kitson, Constantinou (2023). "Causal discovery using dynamically requested knowledge" (Tabu-AL).** Venue unverified. https://arxiv.org/abs/2310.11154
1. Problem: let the algorithm ask for knowledge when it is unsure.
2. Representation: four triggers (equal-scoring orientations, small counts, unstable score across subsamples, small score gain). The simulated human has an "expertise" accuracy and a query limit.
3. Implicit: heuristic thresholds.
4. Guarantee: none.
5. Evaluation: 16 networks. Queries equal to half the number of variables improved mean F1 by 0.207. With 90% expertise the gain fell to 0.138.
6. Relevance: a concrete rule for when a pair is unresolved enough to ask. Open: a 10% error rate already erases a third of the benefit.

**19. Ankan, Textor (2025). "Expert-In-The-Loop Causal Discovery: Iterative Model Refinement Using Expert Knowledge." UAI 2025, PMLR 286:172–183.** https://proceedings.mlr.press/v286/ankan25a.html
1. Problem: help a researcher build a DAG iteratively.
2. Representation: independence tests find pairs where an edge is missing or superfluous, ranked by effect on model fit. The expert supplies only the orientation.
3. Implicit: the abstract does not describe an explicit expert-error model.
4. Guarantee: none stated in the abstract.
5. Evaluation: in simulation the approach beats purely data-driven learning once orientations are right "in at least two out of three cases". There is an LLM proof of concept (details not read; the PDF was unreadable).
6. Relevance: the inverse division of labour to Causal-Copilot (data decide existence, the expert decides direction), with a usable accuracy threshold. Open: abstention.

### C. Active discovery and experiment selection

**20. Choo, Gouleakis, Bhattacharyya (2023). "Active causal structure learning with advice." ICML 2023, PMLR 202:5838–5867.** https://proceedings.mlr.press/v202/choo23a.html
1. Problem: use an advised DAG, possibly wrong, to cut the number of interventions.
2. Representation: the advice is a full DAG. Its quality ψ is a distance to the truth and is not known in advance.
3. Implicit: noiseless interventions; causal sufficiency; known essential graph.
4. Guarantee: intervention cost at most O(max{1, log ψ}) times the verification cost, matching the no-advice bound in the worst case. Correctness never depends on the advice.
5. Evaluation: mainly theoretical (experiments unverified).
6. Relevance: the principled pattern, where the fallible expert steers which experiments to run and experiments decide the graph. Open: needs interventions, which Causal-Copilot lacks.

**21. Li, Chen, Liu, Cai, Liu, Han, Zhang, Xiong (2025). "Can Large Language Models Help Experimental Design for Causal Discovery?" (LeGIT). ICML 2025 workshop oral.** https://arxiv.org/abs/2503.01139
1. Problem: choose intervention targets when numerical signals are noisy early on.
2. Representation: GPT-4o proposes targets in about 5 early rounds of 33, with self-consistency voting. A gradient-based method then takes over.
3. Implicit: the LLM warm-up is assumed informative.
4. Guarantee: convergence to the true DAG as rounds go to infinity, conditional on that assumption.
5. Evaluation: SHD on Alarm of 17.40 against 19.60 for the numerical baseline and 22.60 for five humans.
6. Relevance: the LLM proposes experiments instead of asserting edges. Open: simulated interventions only.

**22. Wu, Yu, Wu, Tan (2025). "LLM Cannot Discover Causality, and Should Be Restricted to Non-Decisional Support in Causal Discovery."** https://arxiv.org/abs/2506.00844
1. Problem: a position paper on the legitimate role of LLMs.
2. Representation: argues that adding LLM priors to data scores causes scale mismatch (BIC grows with sample size, a prior does not) and breaks score consistency, and that altering test statistics breaks their null distribution.
3. Implicit: a strong normative stance.
4. Guarantee: none new; the aim is to preserve existing ones.
5. Evaluation: 14 bnlearn datasets; argues that reported gains come from prompt engineering that leaks ground truth.
6. Relevance: the published statement of our critique. Open: it offers no error-controlled way to use LLM answers at all.

---

## Supporting works located (compact)

**LLM as noisy oracle, with bounds**
- Ding, Ye-Hao, Wang, Zhang (2026), "Step-by-Step Causality: … Tree-Query and Adversarial Confidence Estimation". Correctness at least 1 − M·exp[−2m(0.5 − α)²], assuming independent experts with error below 0.5. No data are used. https://arxiv.org/abs/2601.10137
- Roy, Parbhoo (2026, by arXiv ID), "Why LLMs Fail at Causal Discovery and How Interventional Agents Escape". A frozen LLM answers binary interventional questions inside a Bayesian loop, with convergence under oracle noise η; synthetic text tasks only. https://arxiv.org/abs/2605.27567
- Singh et al. (2026), "CausalGuard: Conformal Inference under Graph Uncertainty". Conformal coverage for treatment-effect intervals over LLM-proposed graphs; the guarantee is not about the graph. https://arxiv.org/abs/2605.21928

**More expert-in-the-loop and LLM-plus-data systems**
- Tench, Demeester (2026, by ID), "Dynamic Expert-Guided Model Averaging for Causal Discovery". GPT-5-nano as expert scored 84.2% on ASIA and 58.1% on ALARM, strong on orientation and weak on existence. https://arxiv.org/abs/2601.16715
- Ban, Chen, Wang, Chen (2023), "From Query Tools to Causal Architects". GPT-4 causal statements were 100% correct on Asia but 60% on Water and 67% on Mildew. https://arxiv.org/abs/2306.16902
- KaPatel et al. (2026), "DMCD". LLM draft, then statistical verification with false-discovery-rate adjustment; F1 fell from 0.209 to 0.07 when variable descriptions were removed. https://arxiv.org/abs/2602.20333
- Peng et al. (2026), "CauScientist". The LLM proposes edits and a BIC check accepts or rejects them; 21–31% of proposals were accepted. https://arxiv.org/abs/2601.13614
- Zhang et al. (2025, by ID), "Bayesian Network Structure Discovery Using Large Language Models". https://arxiv.org/abs/2511.00574
- Amirkhani, Rahmati, Lucas, Hommersom (2017), "Exploiting Experts' Knowledge for Structure Learning of Bayesian Networks", IEEE TPAMI 39(11):2154–2170. Bibliographic record only; content not read. https://doi.org/10.1109/TPAMI.2016.2636828

**Robustness and memorisation**
- Jin et al. (2023), "Can Large Language Models Infer Causation from Correlation?". A fine-tuned model fell from 94.74 to 67.87 F1 when variables were renamed. https://arxiv.org/abs/2306.05836
- Zečević, Willig, Dhami, Kersting (2023), "Causal Parrots". https://arxiv.org/abs/2308.13067
- Lithgow-Serrano, Kanjirangat, Antonucci (2025), "Causal Understanding by LLMs: The Role of Uncertainty". Sentence-level causal classification; instruction-tuned models reached ECE up to 0.56. https://arxiv.org/abs/2509.20088

**Active-learning classics**
- Tong, Koller (2001), IJCAI, pp. 863–869. https://mlanthology.org/ijcai/2001/tong2001ijcai-active
- He, Geng (2008), JMLR 9:2523–2547. https://jmlr.org/papers/v9/he08a.html
- Hauser, Bühlmann, "Two optimal strategies for active learning of causal models from interventional data". https://arxiv.org/abs/1205.4174
- Agrawal, Squires, Yang, Shanmugam, Uhler (2019), "ABCD-Strategy", AISTATS, PMLR 89:3400–3409. https://proceedings.mlr.press/v89/agrawal19b.html
- Squires et al. (2020), "Active Structure Learning of Causal DAGs via Directed Clique Trees". https://arxiv.org/abs/2011.00641
- Tigas et al. (2022), "Interventions, Where and How?", NeurIPS. https://arxiv.org/abs/2203.02016
- "Active Bayesian Causal Inference" (Toth et al., NeurIPS 2022; author list not displayed in the fetched page). https://arxiv.org/abs/2206.02063
- Zhang, Li, Chen, Xie (2023), "Bayesian Active Causal Discovery with Multi-Fidelity Experiments", NeurIPS. The nearest located work to a cost-versus-information trade-off across evidence sources. https://proceedings.neurips.cc/paper_files/paper/2023/hash/c9d9659d1d960b53e8121469ef1f2df5-Abstract.html

**Calibration, abstention and error-rate toolkit**
- Xiong et al., "Can LLMs Express Their Uncertainty?" (ICLR 2024 poster page seen). https://arxiv.org/abs/2306.13063
- Lin, Hilton, Evans, "Teaching models to express their uncertainty in words". https://arxiv.org/abs/2205.14334
- Kadavath et al., "Language Models (Mostly) Know What They Know". https://arxiv.org/abs/2207.05221
- Kuhn, Gal, Farquhar, "Semantic Uncertainty". https://arxiv.org/abs/2302.09664
- Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models". https://arxiv.org/abs/2203.11171
- Quach et al., "Conformal Language Modeling". https://arxiv.org/abs/2306.10193
- Mohri, Hashimoto, "Language Models with Conformal Factuality Guarantees", ICML 2024. https://proceedings.mlr.press/v235/mohri24a.html
- Abbasi-Yadkori et al., "Mitigating LLM Hallucinations via Conformal Abstention". https://arxiv.org/abs/2405.01563
- Geifman, El-Yaniv, "Selective Classification for Deep Neural Networks". https://arxiv.org/abs/1705.08500
- Wen et al., "Know Your Limits: A Survey of Abstention in Large Language Models" (TACL 2025 page seen). https://arxiv.org/abs/2407.18418
- Li, Wang (2009), "Controlling the False Discovery Rate of the Association/Causality Structure Learned with the PC Algorithm", JMLR 10:475–514. https://www.jmlr.org/papers/v10/li09a.html
- Strobl, Spirtes, Visweswaran, "Estimating and Controlling the False Discovery Rate of the PC Algorithm Using Edge-Specific P-Values". https://arxiv.org/abs/1607.03975

---

## (i) Synthesis

The literature treats a fallible expert in four ways.

- **Noise-model methods.** The expert has an error rate, a posterior over graphs is kept, and the true graph is promised to survive with stated probability (Long et al.; Bonilla et al.; da Silva et al.). The guarantees are conditional on the noise model, and the one LLM test of such a guarantee failed through overconfidence.
- **Defeasible-constraint methods.** LLM statements can be overruled by data (Li and Russo; Chen et al.; Takayama et al.; Kitson and Constantinou). These are safer in practice but carry no error rate.
- **Selective methods.** A rule decides when to trust the expert at all (Clivio et al.; Cohrs et al.). They need labelled calibration pairs or control only self-agreement.
- **Advice-for-experiments methods.** The expert only steers which interventions to run and can never corrupt the answer (Choo et al.; LeGIT).

Measurement work agrees on three points. LLM pairwise answers over-assert edges, confusing indirect and reversed relations with direct ones at high stated confidence (Kumar et al.; Vashishtha et al.). Accuracy tracks familiarity with the domain (Feng et al.; Srivastava et al.; Ban et al.). Agreement across prompts is a better confidence signal than verbalised confidence. LLMs are more reliable on orientation than on edge existence (Kitson and Constantinou; Tench and Demeester).

Causal-Copilot does the opposite of every safeguard here. It lets one uncalibrated answer add or delete edges, ignores the data's verdict, and has no step for unresolved pairs. No located work gives a distribution-free error guarantee for LLM pairwise answers, nor a rule that weighs asking the LLM, asking a human, and experimenting.

## (ii) Best published method with a formal error guarantee

**Long et al. (2023)** is the only located method with a guarantee of the form "the true graph remains in the returned equivalence class with probability at least 1 − η".

It assumes:
- the MEC learned from data is correct;
- the expert only orients undirected edges within that class;
- errors occur with a constant, known probability ε, depending only on that edge's true orientation;
- a uniform prior over graphs in the class.

Its known failure cases, from the paper itself:
- On ALARM the true graph was excluded even at small η, attributed to ambiguous variable metadata.
- text-davinci-003 was over-confident, so the computed risk understated the real risk and wrong orientations were accepted.
- The authors call for noise models better suited to LLMs.

Structural limits visible from the method: it cannot represent "no relationship" or "don't know", and it does nothing about skeleton errors. It therefore does not cover the 28 C and 21 D answers in the Sachs run.

Weaker alternatives:
- L2D-CD: a consistency bound on a learned deferral rule; needs labelled pairs; two variables only.
- CaPE: posterior convergence under a non-adversarial expert; not tested with an LLM.
- Tree-Query: a Hoeffding-style bound that assumes independent experts with error below 0.5.
- Conformal methods for LLM outputs (Mohri and Hashimoto; Abbasi-Yadkori et al.): these give exactly the kind of guarantee we want, but need an exchangeable labelled calibration set, and I found no application to pairwise causal answers.

## (iii) Has calibration of LLM pairwise causal judgements been measured?

**Yes, directly, by Kumar et al. (2026).**
- Verbalised confidence: ECE about 0.21–0.23, AUROC 0.36–0.45 (worse than chance at separating right from wrong).
- Logit confidence: ECE about 0.22.
- Cross-prompt or cross-model agreement: ECE about 0.02–0.04, AUROC up to 0.772.
- Over 80% of false positives on reversed and indirect pairs carried confidence of 80 or more.

Other evidence:
- Long et al. report text-davinci-003 as poorly calibrated, qualitatively.
- Takayama et al. show one probability swinging from 0.049 to 0.983 after a small prompt change.

**On anonymised names and obscure data, the evidence is indirect.**
- Familiar versus novel graph: F1 0.93 on Asia versus 0.54 on a post-cut-off Alzheimer's graph (Srivastava et al.).
- Frequency in training text: F1 0.88 versus 0.2 between the most and least frequent relations (Feng et al.).
- By dataset: GPT-4 statement accuracy of 100% on Asia versus 60% on Water (Ban et al.); 84.2% on ASIA versus 58.1% on ALARM (Tench and Demeester).
- Obfuscated names: mean LLM F1 0.572 over 26 networks, and 0.400 on Sachs (Kitson and Constantinou).
- Renaming variables: 94.74 to 67.87 F1 for a fine-tuned model on a formal task (Jin et al.).
- Removing descriptions: 0.209 to 0.07 (DMCD).

I did not locate a study that anonymises names to X1, X2 in pairwise prompts and reports accuracy with calibration, nor one that measures calibration of the "don't know" option.

## (iv) Candidate metrics

**False causal assertion rate**
- False discovery proportion among asserted edges: wrong assertions divided by all assertions (Li and Wang 2009; Strobl et al.).
- The same rate split by what the pair truly is: reversed, indirect, or unrelated (Kumar et al.; Chen et al.'s four error types).
- High-confidence false-positive rate, at confidence of 80 or more (Kumar et al.).
- Empirical rate at which the true graph is excluded, compared with the nominal η (Long et al.).
- Order-level error D_top and cycle count (Vashishtha et al.); level of disagreement (Darvariu et al.).

**Abstention quality**
- Coverage and selective risk, the risk-coverage curve, and a selective-risk bound at confidence 1 − δ (Geifman and El-Yaniv).
- Reliable accuracy, abstention accuracy, Abstain ECE, and areas under the rejection curves (Wen et al.).
- Expected error at most α after conformal thresholding (Abbasi-Yadkori et al.).
- Domain consistency of deferral (Clivio et al.).
- Illustration, my arithmetic from the stated Sachs run: 21 D answers of 55 gives coverage of 34/55, about 62%. The open question is whether errors concentrate in the abstained pairs.

**Calibration**
- ECE, Brier score, AUROC and AUPRC of confidence against correctness (Xiong et al.; Kumar et al.).
- Adaptive calibration error (Lithgow-Serrano et al.).
- Mean squared error and mean absolute deviation of verbalised probability (Lin et al.).
- Agreement-based confidence across samples, prompts or models (Wang et al.; Kumar et al.).
- True-edge-to-reverse and true-edge-to-negative probability ratios (Darvariu et al.).

## (v) Closest works, 2024–2026

1. Kumar et al. (2026), arXiv 2608.23660: calibration of LLM direct-edge judgements.
2. Clivio et al. (2025), arXiv 2502.13132: learning when to defer to the LLM.
3. Bonilla, Zhao, Steinberg (ICML 2026), arXiv 2602.01483: information-gain expert queries with a noise model, tested on Sachs.
4. Li and Russo (UAI 2026), arXiv 2602.16481: LLM constraints that data can overrule.
5. Kitson and Constantinou (2026), arXiv 2608.27472: probabilistic fusion with obfuscated names, including Sachs.

Runner-up: Srivastava et al. (2025), arXiv 2510.16530.

---

## Gaps, typed

- **Not located** (search budget exhausted): Murphy 2001; Kumar et al. on conformal prediction for multiple-choice answers; any explicit value-of-information treatment of expert query versus experiment; any learning-to-defer work on full graphs.
- **Not reachable**: O'Hagan on elicitation (the DOI returned 403).
- **Bibliographic only**: Amirkhani et al. 2017 (abstract not read).
- **Details unread**: Ankan and Textor's LLM experiment; Cohrs et al.'s numeric tables; the exact expert likelihood in da Silva et al.
- **Dates and venues marked unverified** in the entries above: arXiv abstract pages returned only abstract text through the fetch tool, so several dates rest on the arXiv ID.

## Where we're going

Three steps follow from this.
1. Score the recorded Sachs run with the metrics in (iv), starting with the false discovery proportion among the 6 asserted edges and the risk-coverage picture for the 21 abstentions.
2. Rerun the 55 pairs with cross-prompt agreement and anonymised names, to obtain the calibration and anonymisation numbers that the literature lacks.
3. Position the capstone's contribution as the missing piece: an error-controlled rule that keeps data as the arbiter of edge existence, uses the LLM for orientation only above a calibrated threshold, and routes the remaining pairs to a human query or an experiment by expected information gain.

A follow-up search pass could close the "not located" gaps if the caller wants them.