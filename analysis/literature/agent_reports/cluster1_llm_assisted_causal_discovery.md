# LLM-assisted causal discovery and LLM-derived causal priors: literature report (cluster 2)

## Where we are now

I located and checked 35 works in this session. Prior work already covers three of the four ideas in the proposed project, each separately: four-state per-edge fusion of LLM and data graphs, calibration measurement of LLM edge confidence, and the principle that provenance must be kept. I found no work that combines them into a persistent typed per-edge record, and none that fuses LLM judgements with PAG marks.

**Verification caveats**
- Page contents were read through a summarising fetch tool, so any quoted wording needs re-checking against the PDF before it is cited verbatim.
- Several arXiv abstract pages did not render metadata; for those I confirmed title and authors from the HTML or PDF version instead.
- Anything I could not confirm is marked "unverified".
- I did not re-research Causal-Copilot itself.

Each entry below uses the same six points: (1) problem, (2) representation, (3) what stays implicit, (4) guarantees, (5) evaluation, (6) relevance and what it leaves open.

---

## A. Foundations and the "imperfect expert" line

**1. Kıcıman, Ness, Sharma, Tan. "Causal Reasoning and Large Language Models: Opening a New Frontier for Causality." arXiv 2305.00050 (v1 Apr 2023, v3 Aug 2024); TMLR.** https://arxiv.org/abs/2305.00050
1. Tests whether GPT-3.5/4 can do pairwise and full-graph discovery from variable names alone.
2. Text answers to pairwise prompts, assembled into edges; no uncertainty representation.
3. Why an edge is asserted (recall or reasoning) is not recorded; no confidence.
4. None.
5. Tübingen pairs (97% for GPT-4), neuropathic pain, Arctic sea ice. A row-completion memorisation test found GPT-4 could reproduce about 61% of the remaining cells and 25% of full rows of Tübingen. The authors argue memorisation alone does not explain accuracy, and report similar results on datasets created after the training cutoff.
6. The canonical precedent for finding (d). It documents "unpredictable failure modes" and recommends hybrid use, but proposes no calibration or provenance.

**2. Long, Schuster, Piché. "Can Large Language Models Build Causal Graphs?" arXiv 2303.05279; NeurIPS 2022 workshop (venue from search listing).** https://arxiv.org/abs/2303.05279
1. Tests whether GPT-3 can score edges in medical DAGs.
2. Binary edge present/absent per ordered pair, from comparing two statement scores.
3. No uncertainty and no separation of knowledge sources.
4. None.
5. Four small medical DAGs (alcohol, cancer, diabetes, obesity); accuracy only. Shows strong sensitivity to prompt wording and persona.
6. Early evidence that an LLM edge judgement depends on the prompt, which motivates recording the prompt and context as part of an edge's provenance.

**3. Long, Piché, Zantedeschi, Schuster, Drouin. "Causal Discovery with Language Models as Imperfect Experts." arXiv 2307.02390; ICML 2023 SPIGM workshop.** https://arxiv.org/abs/2307.02390
1. Uses a fallible expert to orient the ambiguous edges of a Markov equivalence class (MEC).
2. Starts from the MEC and uses an "ε-expert" noise model, a Bayesian posterior over orientations, greedy query selection and Meek-rule propagation.
3. Assumes a constant, independent error rate; per-edge source is not stored in the output.
4. Returns a reduced class with p(true graph in class) ≥ 1 − η. This holds only under the ε-expert model.
5. bnlearn Asia, CHILD, ALARM, Insurance, starting from true MECs. GPT-3.5 was over-confident and poorly calibrated, and the true graph was excluded on ALARM. No memorisation control.
6. The closest formal ancestor of "LLM judgement as a bounded-risk prior that respects CPDAG ambiguity". The authors state the noise model does not fit LLMs, so the open part is a calibrated, non-constant, checkable noise model.

**4. Ban, Chen, Lyu, Wang, Zhu, Tu, Chen. "Integrating Large Language Model for Improved Causal Discovery." arXiv 2306.16902 (v1 June 2023, v2 Aug 2025); IEEE Trans. on Artificial Intelligence, 2025.** https://arxiv.org/abs/2306.16902
1. Error-tolerant use of LLM causal statements in score-based structure learning.
2. LLM statements become ancestral constraints, applied either hard (pruning) or soft (a prior term in the score with a preset confidence).
3. One global confidence, not per-edge calibration; the final graph does not say which edges the prior forced.
4. None formal.
5. Eight bnlearn networks (Cancer, Asia, Child, Alarm, Insurance, Water, Mildew, Barley); F1 and SHD. No memorisation control on these well-known networks.
6. Establishes the "hard vs soft constraint" vocabulary. Leaves calibration and provenance open.
- The lead title "From query tools to causal architects" could not be confirmed; the current arXiv record carries the title above, and the v1 title is unverified.

**5. Ban, Chen, Lyu, Wang, Chen. "Causal Structure Learning Supervised by Large Language Model" (ILS-CSL). arXiv 2311.11689; venue unverified.** https://arxiv.org/abs/2311.11689
1. Reduces erroneous LLM constraints by having the LLM verify only edges the data-driven learner proposes, iteratively.
2. Edge-level required/forbidden constraints, hard or soft (prior probability 0.99999). The prompt includes an "uncertain" option.
3. Constraint origin is not carried in the output; abstentions are not accounted.
4. An empirical estimate that erroneous constraints fall by roughly O(N) versus full pairwise querying; no formal guarantee.
5. The same eight bnlearn networks; scaled SHD. No memorisation discussion.
6. Directly relevant to finding (c): its design never lets the LLM add an edge the data did not propose, because LLMs confuse indirect with direct causation (reported direct-edge accuracy about 0.96 versus 0.65 on indirect paths).

**6. Chen, Ban, Wang, Lyu, Chen. "Mitigating Prior Errors in Causal Structure Learning: Towards LLM driven Prior Knowledge." arXiv 2306.07032; venue unverified.** https://arxiv.org/abs/2306.07032
1. Detects wrong LLM edge priors without human input.
2. Hard edge priors; an error taxonomy (order-consistent, order-reversed, irrelevant); detection through "quasi-circles".
3. Cannot detect indirect or irrelevant priors; no confidence.
4. Lemmas under sufficient data and a consistent score: order-reversed priors necessarily create quasi-circles, and the other error types add at most one SHD.
5. Asia, Child, Alarm, Insurance plus synthetic graphs; SHD decomposition. Priors are simulated, so there is no memorisation issue.
6. Supplies a typed taxonomy of prior errors, a useful precedent for typed evidence. It needs a majority of priors to be correct.
- A later version is titled "…: A Resilient Approach via Bayesian Networks" (seen in a search listing).

**7. Vashishtha, Reddy, Kumar, Bachu, Balasubramanian, Sharma. "Causal Order: The Key to Leveraging Imperfect Experts in Causal Inference." arXiv 2310.15117; ICLR 2025 poster.** https://arxiv.org/abs/2310.15117
1. Pairwise LLM prompts cannot separate direct from indirect effects; the paper proposes causal order as the output interface.
2. A topological order from triplet prompts with voting, used to orient CPDAG edges from PC or as a prior in CaMML.
3. The order is treated as hard when orienting a CPDAG, and oriented edges are not marked as expert-derived.
4. A perfect expert's pairwise answers give a correct order; zero topological divergence gives a valid backdoor set; the triplet method lowers error for ε-experts.
5. bnlearn networks plus less-known graphs (Neuropathic, Alzheimer's, COVID-19), chosen explicitly because of memorisation concerns.
6. The fusion is type-aware in a limited sense: the LLM only resolves undirected CPDAG edges. Open: per-edge confidence and PAGs.
- An earlier version is titled "Causal Inference Using LLM-Guided Discovery".

**8. Abdulaal, Hadjivasiliou, Montaña-Brown, He, Ijishakin, Drobnjak, Castro, Alexander. "Causal Modelling Agents: Causal Graph Discovery through Synergising Metadata- and Data-driven Reasoning." ICLR 2024.** https://iclr.cc/virtual/2024/poster/17791
1. An agent loop in which the LLM proposes a graph, a deep structural causal model is fitted, and the LLM amends the graph.
2. A JSON DAG, extended to chain graphs for unmeasured confounding; data fit as likelihood; a text "memory" of changes.
3. The final graph does not distinguish LLM-proposed from data-supported edges.
4. None.
5. Arctic sea ice, Sangiovese, an Alzheimer's graph and ADNI data; normalised Hamming distance. No memorisation analysis.
6. The architectural precedent for Causal-Copilot-style refinement; it has the same collapse as findings (a) and (b).

**9. Jiralerspong, Chen, More, Shah, Bengio. "Efficient Causal Graph Discovery Using Large Language Models." arXiv 2402.01207; ICLR 2024 workshop (venue from search listing).** https://arxiv.org/abs/2402.01207
1. Full-graph discovery with a linear number of queries, using breadth-first prompting.
2. Deterministic edges; optional Pearson correlations pasted into the prompt.
3. Data evidence and LLM knowledge are merged inside the prompt and cannot be separated afterwards; no confidence.
4. Acyclicity only.
5. Asia, Child, Neuropathic. No memorisation analysis.
6. An example of evidence collapse at the prompt level.

**10. Darvariu, Hailes, Musolesi. "Large Language Models are Effective Priors for Causal Graph Discovery." arXiv 2405.13551 (May 2024).** https://arxiv.org/abs/2405.13551
1. Uses LLM judgements as soft priors and assesses them independently of the downstream algorithm.
2. Probabilistic expert judgements with a three-way prompt (forward, backward, no edge) that bias the search policy of a Monte Carlo tree search method (CD-UCT).
3. Calibration is not evaluated (as far as I could verify); provenance is not kept.
4. None.
5. Three common-sense benchmarks (names unverified). Finds LLMs help more with direction than with existence.
6. Supports treating existence and orientation as different evidence types.

**11. Takayama, Okuda, Pham, Ikenoue, Fukuma, Shimizu, Sannai. "Integrating Large Language Models in Causal Discovery: A Statistical Causal Approach." arXiv 2402.01454; TMLR 2025.** https://arxiv.org/abs/2402.01454
1. "Statistical causal prompting": run discovery, show the result to the LLM, turn its answer into prior knowledge, and rerun.
2. An LLM probability matrix thresholded into forbidden (<0.05), forced (>0.95) or unknown.
3. The LLM has seen the data result, so its "knowledge" is contaminated by it; forced edges are not labelled in the output.
4. None.
5. Auto MPG, DWD climate, Sachs, and an unpublished health-screening dataset used specifically to exclude memorisation; SHD plus model-fit indices (CFI, RMSEA, BIC).
6. The thresholded matrix is a de facto abstention band. The authors report unstable probabilities and hallucination risk. Open: calibrating the thresholds.

**12. Cohrs, Varando, Diaz, Sitokonstantinou, Camps-Valls. "Large Language Models for Constrained-Based Causal Discovery" (title as printed). arXiv 2406.07378; venue unverified.** https://arxiv.org/abs/2406.07378
1. Replaces PC's conditional-independence test with LLM answers ("chatPC").
2. Yes/no independence answers with self-reported confidence, aggregated by majority, weighted or hypothesis-test voting.
3. Verbalised confidence is not calibrated.
4. Heuristic false-positive control through the voting test; the CPDAG is correct only with a perfect oracle.
5. Cancer, burglary, Asia, Sachs and climate examples. No memorisation analysis. Finds high variability and conservative answers.
6. Keeps the CPDAG output type, but every edge is LLM-derived.

**13. Khatibi, Abbasian, Yang, Azimi, Rahmani. "ALCM: Autonomous LLM-Augmented Causal Discovery Framework." arXiv 2405.01744.** https://arxiv.org/abs/2405.01744
1. A pipeline of weighted-vote discovery (PC, LiNGAM, NOTEARS), a prompt wrapper, then an LLM refiner that validates, reorients, removes and adds edges.
2. A single graph edited in place; categorical LLM confidence labels.
3. No record of which edges came from the LLM.
4. None.
5. Seven well-known datasets including Asia, Sachs, Child and Insurance. No memorisation analysis.
6. Structurally the same failure pattern as Causal-Copilot. The authors themselves list missing uncertainty quantification as a limitation.

**14. Le, Xia, Chen. "Multi-Agent Causal Discovery Using Large Language Models" (MAC). arXiv 2407.15073; venue unverified.** https://arxiv.org/abs/2407.15073
1. Multi-agent debate over which statistical method to run, then debate to refine the graph.
2. A final DAG.
3. Edge provenance is not marked.
4. None.
5. Five datasets (names unverified).
6. Same collapse as findings (a) and (b).

**15. Liu, Chen, Liu, Gong, Cheng, Han, Zhang. "Discovery of the Hidden World with Large Language Models" (COAT). NeurIPS 2024; arXiv 2402.03941.** https://proceedings.neurips.cc/paper_files/paper/2024/hash/b99a07486702417d3b1bd64ec2cf74ad-Abstract.html
1. The LLM proposes and annotates high-level variables from unstructured data; FCI finds the relations.
2. A clean role split: the LLM never decides edges, and the output is a PAG from FCI.
3. LLM annotation noise enters the data silently.
4. Markov-blanket identification with a convergence rate depending on LLM "perception" and "capacity" scores.
5. AppleGastronome (synthetic), Neuropathic and case studies.
6. The best existing example of separation by construction. It sidesteps fusion and does not solve it.

**16. Zhang, Zhang, Gan, Yao, Wang. "Causal Graph Discovery with Retrieval-Augmented Generation based Large Language Models" (LACR). arXiv 2402.15301.** https://arxiv.org/abs/2402.15301
1. Grounds LLM edge decisions in retrieved papers.
2. Per-pair votes over documents (independent, direct, indirect, unknown), giving a skeleton and then orientation.
3. The documents behind each edge are not kept in the output graph.
4. A determinism proposition and a wisdom-of-crowds argument only.
5. Asia, Sachs, Coronary. Argues that published "ground truth" graphs (for example Asia) conflict with current literature.
6. Its evidence is of a citable type, which shows provenance is feasible. It also warns that benchmark truth is itself contestable.

## B. Critiques, memorisation and benchmarks

**17. Zečević, Willig, Dhami, Kersting. "Causal Parrots: Large Language Models May Talk Causality But Are Not Causal." TMLR 2023; arXiv 2308.13067.** https://openreview.net/forum?id=tv46tCzs83
1. Argues LLMs recite correlations between causal facts in their training text.
2. The "meta SCM" concept.
3. Not applicable.
4. A conceptual argument.
5. Small empirical probes.
6. The theoretical framing for finding (d).

**18. Jin et al. "Can Large Language Models Infer Causation from Correlation?" (Corr2Cause), ICLR 2024, and Jin et al. "CLadder: Assessing Causal Reasoning in Language Models," NeurIPS 2023 (arXiv 2312.04350).** https://iclr.cc/virtual/2024/poster/17518 and https://arxiv.org/abs/2312.04350
1. Benchmarks for formal causal reasoning without world knowledge.
2. Symbolic graphs rendered as text.
3. Not applicable.
4. Not applicable.
5. Near-random performance on Corr2Cause; fine-tuned models fail out of distribution; CLadder has 10K samples.
6. Evidence that LLM "judgement" is knowledge recall and not inference from statistics, which supports labelling it as a distinct evidence kind.

**19. Feng, Qu, Tandon, Li, Kang, Haffari. "On the Reliability of Large Language Models for Causal Discovery." arXiv 2407.19638; ACL 2025 (venue from search listing).** https://arxiv.org/abs/2407.19638
1. Tests whether memorisation drives LLM causal accuracy.
2. Counts each relation's occurrences in open pretraining corpora (OLMo/Dolma, BLOOM/ROOTS).
3. Not applicable.
4. None.
5. Accuracy correlates strongly with corpus frequency (Spearman about 0.9); F1 falls from about 0.9 to about 0.2–0.35 for rare relations; conflicting corpus statements lower confidence.
6. The strongest mechanistic evidence for finding (d). Limited to open models and mostly common-sense relations.

**20. Srivastava, Nagalapatti, Jajoo, Vashishtha, Krishnamurthy, Sharma. "Realizing LLMs' Causal Potential Requires Science-Grounded, Novel Benchmarks." arXiv 2510.16530 (Oct 2025).** https://arxiv.org/abs/2510.16530
1. Shows bnlearn benchmarks are memorised and proposes post-cutoff benchmarks.
2. Three reconstruction tests (complete the nodes, the edges, or the subgraph from the dataset name).
3. Not applicable.
4. None.
5. Near-perfect reconstruction of Asia and Cancer with no context given. Four graphs from recent papers (Alzheimer's, two COVID-19, Sweden transport) show near-zero memorisation and much lower LLM accuracy.
6. Finding (d) is therefore already published for bnlearn. Their hybrid uses LLM edges as hard priors that stop PC from removing an edge even when independence is detected, with no calibration or labelling; this is the same behaviour as finding (c), adopted as a design choice.

**21. Wu, Yu, Wu, Tan. "LLM Cannot Discover Causality, and Should Be Restricted to Non-Decisional Support in Causal Discovery." arXiv 2506.00844 (June 2025).** https://arxiv.org/abs/2506.00844
1. A position paper: LLM outputs, whether hard or soft, undermine the guarantees of discovery algorithms.
2. Not applicable.
3. Not applicable.
4. Arguments that soft LLM priors break score decomposability and local consistency.
5. Fourteen bnlearn networks; attributes reported gains to hand-curated prompts that leak ground truth.
6. Any project that keeps LLM priors must answer this objection. Calibrated, separately labelled priors are one answer.

**22. Zheng, Verma, Gill, Dai, Spirtes, Zhang. "Causal Discovery in the Era of Agents." arXiv 2606.23608 (22 June 2026).** https://arxiv.org/abs/2606.23608
1. A position paper with a platform (causal-learn+): agents should assist the workflow but must not supply edges, orientations, priors or constraints.
2. Agent suggestions, user choices, algorithm settings and graph outputs are kept as "distinct objects"; constraints enter only after user approval.
3. No formal provenance schema or per-edge record is specified; LLM judgement is excluded, not calibrated; no bootstrap or stability discussion.
4. None.
5. One case study (Big Five personality data); no quantitative evaluation; memorisation is not discussed.
6. States our findings (a) and (b) as a principle (extracted wording: "provenance is not bookkeeping; it is part of what a graph mark means"). Lists as future work "audit trails that separate data, assumptions, agent recommendations, user decisions and algorithmic outputs" and evaluating over-interpretation of partially identified graphs. This is both a threat (the idea is stated by a prominent group) and a licence (they say it is not yet built).

## C. Trust, deferral, calibration and fusion (2025–2026)

**23. Clivio, Mahajan, Taslakian, Magliacane, Mitliagkas, Zantedeschi, Drouin. "Learning to Defer for Causal Discovery with Imperfect Experts" (L2D-CD). arXiv 2502.13132 (Feb 2025).** https://arxiv.org/abs/2502.13132
1. Learns, per variable pair, whether to trust the data-driven method or the LLM.
2. A learned deferral function that selects one source and does not blend them.
3. Needs labelled pairs to train.
4. A consistency bound for the surrogate loss.
5. Tübingen pairs only, which Kıcıman et al. showed are partly memorised (entry 1); the paper does not discuss this.
6. A precedent for per-item source selection. Limited to bivariate cases; extension to graphs is left as future work.

**24. Lyu, Turcan, Zhang, Wilder. "Improving Constraint-Based Discovery with Robust Propagation and Reliable LLM Priors" (MosaCD). arXiv 2509.23570 (Sept 2025).** https://arxiv.org/abs/2509.23570
1. LLM orientation seeds for a PC skeleton, filtered for hallucination.
2. A CPDAG/PDAG; seeds kept only if consistent across shuffled answer orders and repeats, and discarded if they contradict the separating-set record or create cycles; low-confidence edges stay unoriented.
3. Seeds are not labelled in the output; the residual false-seed rate is not quantified.
4. A theorem that it returns the true CPDAG given a perfect independence oracle and consistent seeds.
5. Ten bnlearn networks; orientation F1. No explicit memorisation test.
6. Abstention plus a data veto over the LLM inside a CPDAG. The closest constraint-based realisation of "LLM as abstaining prior", without calibration or provenance.

**25. Tench, Demeester. "Dynamic Expert-Guided Model Averaging for Causal Discovery." arXiv 2601.16715 (Jan 2026).** https://arxiv.org/abs/2601.16715
1. Ensembles several algorithms and queries an expert only on edges where the algorithms disagree.
2. Edge frequency across models; existence and orientation treated separately; the expert is asked only in a mid-confidence band; inconsistent LLM answers fall back to the vote.
3. Edge source is not tracked after insertion.
4. Acyclicity only.
5. Bayesys networks plus SimSUM, clean and noisy. A memorisation probe found high memorisation of ASIA and little for the others.
6. Selective querying driven by algorithmic disagreement is close to "ask the LLM only where the data are ambiguous".

**26. Bonilla, Zhao, Steinberg. "Causal Preference Elicitation" (CaPE). arXiv 2602.01483 (Feb 2026); ICML 2026 poster (venue from search listing).** https://arxiv.org/abs/2602.01483
1. Bayesian expert-in-the-loop discovery with active queries.
2. A particle posterior over DAGs; a three-way noisy-expert likelihood (forward, backward, none) with reliability parameters; queries chosen by expected information gain.
3. DAGs only; tested with simulated experts, not LLMs.
4. Posterior convergence to the true DAG up to Markov equivalence, under a non-adversarial expert.
5. Synthetic graphs, Sachs and CausalBench.
6. A principled way to treat a judgement as likelihood evidence and not as a graph edit. Open: fitting the reliability parameters for LLMs.

**27. Li, Russo. "Leveraging Large Language Models for Causal Discovery: a Constraint-based, Argumentation-driven Approach." arXiv 2602.16481; UAI 2026 (PMLR v337).** https://arxiv.org/abs/2602.16481
1. LLM priors inside Causal Assumption-Based Argumentation.
2. LLM constraints kept only if all five runs agree, encoded as required/forbidden arrows; independence statements are weighted defeasible assumptions; a required arrow is dropped if the data removed that adjacency.
3. Argument-level tracing is claimed to be possible but not shown per edge; no calibration; assumes causal sufficiency.
4. The output DAG is consistent with a defensible subset of the input constraints (stable semantics).
5. bnlearn (including Sachs) plus a new memorisation-mitigating protocol: random DAGs mapped onto CauseNet subgraphs, giving 54 novel graphs.
6. The strongest symbolic provenance story, with a data veto over the LLM. Scales to about 15 nodes.

**28. Peng, Wu, Chen, Wang, Qiao, Lu. "CauTion: Knowing When to Trust LLMs for Ensemble Causal Discovery." arXiv 2606.03602 (June 2026).** https://arxiv.org/abs/2606.03602
1. Decides when to trust the LLM versus an ensemble of algorithms.
2. Four-category votes per algorithm (forward, reverse, undirected, none); existence and direction as separate tasks; LLM accuracy estimated on consensus edges used as pseudo-labels; trust weights; the LLM is queried only when the algorithmic margin is low.
3. Outputs a single DAG; no source labels; assumes LLM reliability on consensus edges transfers to disputed ones.
4. Acyclicity only.
5. Six benchmarks up to Win95pts (76 nodes); SHD, F1, SID. Memorisation is not discussed.
6. A direct competitor on "calibrated trust". Its reliability estimate breaks under finding (d), because consensus edges on famous benchmarks are exactly the ones the LLM has memorised.

**29. Kitson, Constantinou. "LLM-Augmented Causal Discovery: Probabilistic Fusion of Edge Existence and Orientation." arXiv 2608.27472 (19 Aug 2026).** https://arxiv.org/abs/2608.27472
1. Fuses structure-learning ensembles with LLM knowledge.
2. "Probabilistic Dependency Graphs": four probabilities per pair (none, forward, backward, undirected); DAG, CPDAG and PDAG inputs are converted and averaged with weights; the LLM returns existence and orientation confidences separately.
3. Source identity is lost after fusion; the authors state the values are "empirical support", not calibrated posteriors; no bidirected or circle state; no true abstention.
4. None; a greedy DAG extraction.
5. 26 networks (bnlearn, bnRep, Bayesys); fusion beats the better single source in 22 of 26. Variable names replaced by neutral aliases, plus a post-hoc leakage audit.
6. The nearest technical neighbour to "fusion rules that respect edge types". Open: calibration, provenance after fusion, PAG marks, real or noisy data.

**30. Kumar, Zarabi, Trivedy, Chen, Zhang, Fu, Ji. "From Causal Plausibility to Causal Reliability: Evaluating LLMs as Calibrated Direct Causal-Edge Classifiers." arXiv 2608.23660 (Aug 2026); venue unverified.** https://arxiv.org/abs/2608.23660
1. Asks whether LLM confidence in direct-edge judgements is trustworthy.
2. Four confidence sources (verbalised, logit, cross-prompt agreement, cross-model agreement); ECE, Brier, AUROC; temperature scaling.
3. No fusion with data, no abstention and no global constraints.
4. None.
5. 12 open models, six CausalGraphBench graphs, five prompt styles. Recall exceeds precision in 94.4% of cases. False positives concentrate on indirect and reversed pairs, with over 80% of them at 80% or higher stated confidence. Includes a two-stage benchmark-familiarity audit.
6. Supplies the measurement for finding (c) and recommends treating LLM judgements as "externally validated soft causal priors", but does not build that integration.

**31. Wan, Lu, Wu, Hu, Li. "Large Language Models for Causal Discovery: Current Landscape and Future Directions." IJCAI 2025, pp. 10687–10695, DOI 10.24963/ijcai.2025/1186; arXiv 2402.11068.** https://www.ijcai.org/proceedings/2025/1186
1. A survey of the field.
2. Its taxonomy has three roles: extracting relations from text, supplying domain knowledge to statistical methods, and refining structures.
3. Provenance is not treated as a topic; calibration is not analysed in depth (based on the arXiv version I read).
4. Not applicable.
5. Calls for out-of-distribution benchmarks.
6. Confirms the gap is not a named research line in the main survey.

**Also located (peripheral)**
- Du et al., "Causal Discovery through Synergizing Large Language Model and Data-Driven Reasoning" (LLM-CD), KDD 2025: LLM inside PC with evidential uncertainty; no latent confounders. https://www.cs.emory.edu/~jyang71/files/llmcd.pdf
- Peng, Chen, Xu, Lu, "CauScientist", arXiv 2601.13614: the LLM proposes edits and a BIC score accepts or rejects them, with a rejection memory. https://arxiv.org/abs/2601.13614
- Bazgir et al., "Causal MAS" survey, arXiv 2509.00987: multi-agent systems; no treatment of provenance or calibration. https://arxiv.org/abs/2509.00987
- Roy, Parbhoo, "Why LLMs Fail at Causal Discovery and How Interventional Agents Escape", arXiv 2605.27567: an impossibility argument plus an external Bayesian loop. https://arxiv.org/abs/2605.27567

---

## (i) Synthesis

**Solved or well established**
- LLMs are "imperfect experts" whose edge judgements are mostly recall (entries 1, 17, 19).
- Famous benchmarks are memorised (1, 20, 25), and memorisation-resistant evaluations exist (11, 20, 27, 29).
- LLM knowledge can enter discovery as hard or soft constraints, as a causal order, or as a noisy-expert likelihood (4–7, 10, 26).
- Hard LLM constraints are risky, and data should be able to veto them (5, 24, 27).
- Existence and orientation are different judgements, and LLMs are better at orientation (10, 28, 29).
- LLM confidence about direct edges is badly over-confident, with errors concentrated on indirect and reversed pairs (30).
- Selective querying, deferral and abstention heuristics exist (23–25, 28).
- A formal inclusion guarantee exists for orienting a Markov equivalence class, but only under a noise model LLMs violate (3).

**Open**
- No system I located emits a persistent per-edge record of why an edge exists. Fusion methods discard source after merging (28, 29); agent pipelines edit one matrix (8, 13, 14); the provenance principle has no schema (22); argumentation tracing is undemonstrated (27).
- No LLM-fusion work handles PAG marks (circle or bidirected endpoints). CPDAG undirected edges are handled in 3, 7, 24 and 29.
- Calibration is measured (30) but not connected to fusion, and there is no abstention accounting with a risk statement valid for real LLMs.
- Memorisation is audited after the fact but never used as a runtime signal to down-weight the LLM.
- I found no audit of a deployed agent such as Causal-Copilot, and no study of LLM judgements overriding bootstrap edge frequencies.

## (ii) Strongest threats to novelty

1. **Kitson & Constantinou (29).** A four-state per-edge representation with CPDAG-aware fusion and separate existence and orientation channels already exists. "Typed fusion" alone is not new; the project must differ on provenance after fusion, calibration, PAG marks and abstention.
2. **Zheng, …, Spirtes, Zhang (22).** The diagnosis in our findings (a) and (b) is already stated by a leading causal-discovery group, who conclude LLMs should supply no edges at all. A project that keeps LLM priors must justify that choice and should present itself as building the audit trail they call for.
3. **Kumar et al. (30).** Calibration evaluation of LLM edge judgements (ECE, Brier, temperature scaling, a familiarity audit) is done. Novelty has to be in using calibration inside fusion.
4. **CauTion (28) and Tench & Demeester (25).** "Knowing when to trust the LLM" through annotation-free reliability estimates and selective querying is done for DAG outputs.
5. **Li & Russo (27) and MosaCD (24).** Data veto over LLM constraints, abstention, traceable symbolic integration and CPDAG correctness theorems exist.
6. **Long et al. (3), Clivio et al. (23), Bonilla et al. (26).** Formal noisy-expert models with guarantees or posteriors exist; "LLM as bounded-error prior" is not new as a concept.
7. **Srivastava et al. (20) and Kıcıman et al. (1).** Finding (d) is published for bnlearn and Tübingen. Only the Sachs-specific observation inside a deployed agent, and its downstream effect on the final graph, would be new.
8. **Wu et al. (21).** A reviewer can cite this to argue the whole premise of LLM priors is unsound.

An honest position, given these: the contribution is an audit of an existing agent plus an integration of known pieces into one typed record, extended to PAG marks. It is not a new fusion principle.

## (iii) Terminology used in this literature

- **The LLM's role:** "imperfect expert", "ε-expert", "LLM as oracle", "knowledge-driven / metadata-based reasoning" versus "data-driven"; "knowledge-based causal inference" (Takayama); "non-decisional support" (Wu).
- **Form of knowledge:** "LLM-derived priors", "prior knowledge", "background knowledge"; "hard constraints" versus "soft constraints"; "required/forced" and "forbidden" edges; "ancestral constraints"; "edge-level priors"; "causal order"; "seeds".
- **Evidence types:** "edge existence" versus "orientation/direction"; "direct" versus "indirect" causation; "Markov equivalence class", "CPDAG", "PAG"; "partially identified graphs"; "Probabilistic Dependency Graph".
- **Errors in priors:** "prior errors" typed as "order-consistent / order-reversed / irrelevant"; "hallucination"; "positional bias".
- **Trust and uncertainty:** "error-tolerant", "learning to defer / deferral", "selective expert querying", "trust-calibrated arbitration", "consensus filtering", "reliability estimation", "verbalised confidence", "calibration" (ECE, Brier), "expected information gain", "noisy expert likelihood".
- **Memorisation:** "memorization", "dataset leakage", "benchmark familiarity audit", "causal parrots", "science-grounded / leakage-resistant benchmarks".
- **Provenance:** "provenance", "audit trail", "distinct objects" (Zheng et al.); "defeasible assumptions", "arguments" (Li & Russo). The phrases "typed evidence" and "evidence record" did not appear in any work I located.

## (iv) Closest works from 2025–2026

1. Kitson & Constantinou, arXiv 2608.27472 (Aug 2026): four-state per-edge probabilistic fusion.
2. Zheng et al., arXiv 2606.23608 (June 2026): the provenance and separation principle, and an explicit call for audit trails.
3. Kumar et al., arXiv 2608.23660 (Aug 2026): calibration of LLM direct-edge judgements.
4. Peng et al. (CauTion), arXiv 2606.03602 (June 2026): calibrated trust between an LLM and an algorithm ensemble.
5. Li & Russo, arXiv 2602.16481 (UAI 2026): argumentation-based integration with provenance and a memorisation-mitigating protocol.

Close runners-up: MosaCD (arXiv 2509.23570) and Srivastava et al. (arXiv 2510.16530).

## Where we're going

- **Read in full before fixing the design:** Kitson & Constantinou (29) and Zheng et al. (22). Between them they bound the claim from both sides.
- **Defensible gaps to build on:**
  - a per-edge typed provenance record that survives fusion;
  - PAG endpoint marks as first-class types;
  - calibration from Kumar-style measurement wired into fusion, with abstention accounting;
  - memorisation detection used as a runtime gate on the LLM's weight;
  - the Causal-Copilot audit itself, including LLM-versus-bootstrap overrides.
- **Still to verify:** the original title of Ban et al. v1; the venues of ILS-CSL, Chen et al., Cohrs et al., MAC and Kumar et al.; the dataset names in Darvariu et al. and MAC; all quoted wording.
- **Not covered in this cluster:** classical background-knowledge theory for PAGs (tiered knowledge, orientation-rule completeness) and bootstrap or stability-selection methods. Both bear on the "fusion rules respecting PAG marks" claim and need their own search.
- **A threat specific to CauTion-style designs:** on famous benchmarks, reliability estimated from consensus edges is inflated by memorisation. That is a testable experiment for the capstone.