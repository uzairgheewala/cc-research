# Evidence fusion, uncertainty representation, background knowledge and provenance in causal structure learning

## Where we are now

- All 22 main works below were located this session and each has a working URL.
- arXiv abstract pages often returned no title or author metadata to the fetcher, so I confirmed bibliographic details from proceedings pages, HTML versions or PDFs. Anything I could not confirm is marked "unverified".
- PubMed and PMC pages were blocked by a CAPTCHA. For Oates et al. I confirmed only the bibliographic record, not the content.
- I found no reporting guideline specific to causal discovery studies.

**Short answers**
- **(ii)** No guarantee-backed standard exists. The cleanest published separation is bnlearn's arc "strength" plus "direction given presence" (Friedman et al. 1999; Scutari and Nagarajan 2013), which covers DAGs and CPDAGs only. For PAGs there are only per-pair edge-type frequency vectors (Tetrad; Jabbari et al.; Debeire et al.).
- **(iii)** ASP (Hyttinen et al.), Ancestral Causal Inference, argumentation (Bromberg and Margaritis; Causal ABA) and Bayesian priors each give one inspectable representation. None has calibrated weights for LLM statements, per-edge provenance in the output, or abstention.

---

## A. Resampling-based edge confidence

**1. Friedman, Goldszmidt, Wyner (1999). "Data Analysis with Bayesian Networks: A Bootstrap Approach." UAI 1999.** https://arxiv.org/abs/1301.6695
1. Problem: confidence in features of a learned network when data are too few for a single trustworthy structure.
2. Representation: per-feature bootstrap frequency. Features are defined on PDAGs, with "directed and undirected edges between pairs of variables as different features", plus Markov-blanket membership and ancestor/order relations. Both parametric and non-parametric bootstrap are used.
3. Implicit: dependence between features; where to set the threshold (they note it is domain-dependent, e.g. 0.8 vs 0.65); no rule for turning frequencies into one graph.
4. Guarantees: none formal. The empirical claim is that "features induced with high confidence are rarely false positives".
5. Evaluation: simulations from known networks (alarm, text-derived).
6. Relevance: the origin of the practice. It already treats "undirected in the PDAG" as a separate feature from "directed", so a directed-only rule is a regression from 1999. It leaves the aggregation rule open.

**2. Scutari and Nagarajan (2013). "Identifying significant edges in graphical models of molecular networks." Artificial Intelligence in Medicine 57(3):207-217.** https://pmc.ncbi.nlm.nih.gov/articles/PMC4070079 (arXiv 1104.0896)
- Companion software documentation, bnlearn `boot.strength` / `averaged.network`: https://www.bnlearn.com/documentation/man/arc.strength.html and https://www.bnlearn.com/documentation/man/bn.strength-class.html
1. Problem: replacing ad hoc thresholds on bootstrap arc frequencies with a data-driven one.
2. Representation: two numbers per pair.
   - bnlearn computes "the probability of each arc (modulo its direction) and the probabilities of each arc's directions conditional on the arc being present in the graph (in either direction)".
   - The `direction` column is "the probability of the arc's direction given its presence in the graph".
   - The threshold applies to strength only. It is the minimiser of the L1 distance between the empirical CDF of strengths and an ideal 0/1 step CDF.
   - With `cpdag=TRUE` the equivalence class is used; an averaged arc stays undirected "if and only if the probability of each of its directions is exactly 0.5".
3. Implicit: joint dependence between arcs; calibration of the frequencies; no PAG marks.
4. Guarantees: none formal. The authors note the threshold varies strongly across samples.
5. Evaluation: ALARM, HAILFINDER and INSURANCE at sample sizes 100 to 20,000 with three learners; two molecular datasets.
6. Relevance: the closest published answer to (ii) for CPDAGs. Under this scheme the edge that is undirected in 95% of resamples has strength 0.95 and direction 0.5, and is kept. Open: a direction threshold (anything short of exactly 0.5 gets oriented), and PAGs.

**3. Tetrad bootstrapping and edge-type ensembles (software documentation, not peer-reviewed).** https://tetrad-manual.readthedocs.io/en/latest/tetrad-interface/detail-callouts/detail-bootstrapping.html and https://www.phil.cmu.edu/tetrad-javadocs/7.6.5/edu/pitt/dbmi/algo/resampling/ResamplingEdgeEnsemble.html
1. Problem: summarising bootstrap runs of any Tetrad search, including CPDAG and PAG outputs.
2. Representation: per pair, "Edge Frequencies: How often an edge was present or absent" and "Orientation Frequencies: Frequencies for different edge types (e.g., →, ←, undirected, circle endpoints, bidirected)". Ensemble rules, quoted from the javadoc:
   - Preserved (the default): "Choose an edge iff there is an edge that its prob. is the highest and it's not nil otherwise choose nil".
   - Highest: "Choose an edge iff its prob. is the highest (even it's nil…)".
   - Majority: "Choose an edge iff its prob. > .5 even it's nil".
   - Threshold: user-defined.
3. Implicit: no statistical justification of the rules; the ensemble graph need not be a valid CPDAG or PAG; the Preserved wording is ambiguous.
4. Guarantees: none. The manual says "Bootstrapping does not validate assumptions" and "Unstable edges are not necessarily false".
5. Evaluation: none in the documentation (see 4 and 5 below).
6. Relevance: the only place I found full typed edge-mark frequencies including circle marks. Under Highest or Preserved, a circle-circle edge at 80% is kept as circle-circle. Tetrad's separate StabilitySelection wrapper thresholds a frequency that includes orientation (https://tetrad-manual.readthedocs.io/en/latest/algorithms/stability-selection.html). That splits adjacency mass across edge types, which is the same family of failure we observed.

**4. Jabbari, Naeini, Cooper (2017). "Obtaining Accurate Probabilistic Causal Inference by Post-Processing Calibration." arXiv 1712.08626 (venue unverified).** https://arxiv.org/abs/1712.08626
1. Problem: bootstrap edge-type frequencies are not calibrated probabilities.
2. Representation: bootstrap RFCI (200 resamples) gives each pair a seven-way vector: no edge, A→B, B→A, A o→ B, B o→ A, A o–o B, A↔B. A shallow neural network maps this to calibrated probabilities using a small set of pairs with known status.
3. Implicit: where a calibration set comes from in practice; adjacency is not separated from orientation beyond the seven classes.
4. Guarantees: none formal.
5. Evaluation: simulated data; precision, recall, F1 and maximum calibration error.
6. Relevance: shows PAG edge-mark frequencies are raw scores needing calibration, so fixed cut-offs like 0.1 and 0.9 on them are unsupported. Open: calibration without ground truth.

**5. Kummerfeld and Rix (2019). "Simulations evaluating resampling methods for causal discovery: ensemble performance and calibration." arXiv 1910.02047 (published venue unverified).** https://arxiv.org/abs/1910.02047
- Follow-up: Banerjee, Andrews, Kummerfeld (2025), "An extensive simulation study evaluating the interaction of resampling techniques across multiple causal discovery contexts", arXiv 2503.15436. https://arxiv.org/abs/2503.15436
1. Problem: do bootstrap or subsample frequencies behave like probabilities?
2. Representation: a per-pair table of "the proportion of votes each relationship got"; an ensemble graph by highest vote (2019) or a 0.5 adjacency threshold (2025).
3. Implicit: the 2019 paper pools all edge relationships; the 2025 paper tracks adjacency only. Only score-based learners are tested (GES; fGES and BOSS). No PAGs.
4. Guarantees: none.
5. Evaluation: Brier score, reliability and expected calibration error on linear Gaussian simulations, Hepar2 and Child.
   - 2025 findings: "There is no resampling technique that is superior"; plain bootstrap shows "persistent miscalibration"; calibration interacts with the penalty parameter.
6. Relevance: 20 resamples with fixed cut-offs has no calibration backing. Orientation calibration is unstudied.

**6. Debeire, Runge, Gerhardus, Eyring (2024). "Bootstrap aggregation and confidence measures to improve time series causal discovery." CLeaR 2024, PMLR 236.** https://proceedings.mlr.press/v236/debeire24a.html
1. Problem: bagging and confidence for PCMCI+ time-series graphs.
2. Representation: per pair, "the relative frequency of each of the possible edge types" (no edge, →, ←, o–o, and x–x for conflicts). The bagged graph is a majority vote over types. Ties are broken conservatively: "no edge, ×–×, ∘–∘, and, at the same preference level, → and ←". Confidence is the frequency of the winning type.
3. Implicit: adjacency versus orientation is not disaggregated; edge-wise voting loses dependencies between edges.
4. Guarantees: none; the authors say convergence of the frequency error is unclear.
5. Evaluation: synthetic models. Link-frequency error is about 3% for lagged links and about 7% for contemporaneous links.
6. Relevance: the most recent peer-reviewed aggregation rule that treats unoriented and conflict marks as first-class outcomes. An o–o edge at 80% survives. Open: PAG marks and separate adjacency confidence.

**7. Meinshausen and Bühlmann (2010). "Stability selection." JRSS-B 72(4):417-473.** https://arxiv.org/abs/0809.2932
- Also: Liu, Roeder, Wasserman (2010), "StARS", NIPS 2010. https://proceedings.neurips.cc/paper/2010/hash/301ad0e3bd5cb1627a2044908a42fdc2-Abstract.html
- Also: Stekhoven et al. (2012), "Causal stability ranking", Bioinformatics 28(21):2819-23. https://www.yeastgenome.org/reference/22945788
1. Problem: error-controlled selection (stability selection), regularisation choice (StARS), ranking causal effects (CStaR).
2. Representation: selection probability per feature over subsamples of size n/2, with a threshold π_thr. StARS uses edge instability across subsamples. CStaR gives a stable ranking of lower bounds on causal effects.
3. Implicit: the feature is an undirected edge or a variable; orientation marks are not addressed.
4. Guarantees:
   - Stability selection bounds the expected number of false selections under exchangeability-type assumptions (recalled from the paper; the theorem text was truncated in my fetch).
   - StARS has "partial sparsistency".
5. Evaluation: simulations and gene-expression data; Arabidopsis and yeast validation for CStaR.
6. Relevance: the only resampling results with finite-sample error control, and they cover adjacency-type features only. Nothing equivalent exists for marks.

## B. Marking uncertainty inside constraint-based search

**8. Ramsey, Zhang, Spirtes (2006). "Adjacency-Faithfulness and Conservative Causal Inference." UAI 2006.** https://arxiv.org/abs/1206.6843
- Also: Colombo and Maathuis (2014), "Order-Independent Constraint-Based Causal Structure Learning", JMLR 15:3921-3962. https://jmlr.org/papers/v15/colombo14a.html
1. Problem: unreliable collider orientation (conservative PC) and order dependence (PC-stable, with conservative and majority-rule variants in pcalg).
2. Representation: faithfulness is split into adjacency-faithfulness and orientation-faithfulness. Triples whose separating sets disagree are marked rather than oriented (the "ambiguous triple" term is the pcalg convention; not re-read this session).
3. Implicit: the mark is binary, with no strength attached.
4. Guarantees: CPC is correct under adjacency-faithfulness alone and matches PC asymptotically under full faithfulness. PC-stable removes order dependence in the skeleton and keeps consistency.
5. Evaluation: simulations; yeast expression data.
6. Relevance: the theoretical basis for treating adjacency evidence and orientation evidence as different kinds of claim.

**9. Claassen and Heskes (2012). "A Bayesian Approach to Constraint Based Causal Inference" (BCCD). UAI 2012.** https://arxiv.org/abs/1210.4866
1. Problem: constraint-based search makes hard, unranked decisions.
2. Representation: a posterior probability for each logical causal statement, p(L|D) ∝ Σ over structures entailing L. Statements are processed in decreasing reliability with a threshold (default 0.5). Output is a PAG.
3. Implicit: the final PAG does not carry the probabilities on its marks; the BD score assumes discrete data; structure priors.
4. Guarantees: soundness of the inference rules under the Markov and faithfulness assumptions.
5. Evaluation: random graphs with latent variables; 1-4% better than FCI and conservative FCI.
6. Relevance: reliability attaches to typed statements about presence or absence of causal relations, not to a "directed edge" count.

## C. Explicit weighted-evidence and argumentation frameworks

**10. Hyttinen, Eberhardt, Järvisalo (2014). "Constraint-based Causal Discovery: Conflict Resolution with Answer Set Programming." UAI 2014.** https://www.auai.org/uai2014/proceedings/individuals/87.pdf
1. Problem: conflicting independence and dependence results in finite samples, allowing cycles and latent variables.
2. Representation: every (in)dependence statement is a weighted constraint. The solver finds the graph minimising the summed weight of unsatisfied constraints. Three weightings: constant, hard dependencies, and Bayesian log-odds.
3. Implicit: which constraints the optimum violated is not part of the reported graph; weights assume independent errors.
4. Guarantees: any optimal ASP solution minimises the stated objective; completeness in the infinite-sample limit.
5. Evaluation: 200 random six-variable models at n=500; better than PC, cPC, FCI and cFCI. Scales to about seven variables.
6. Relevance: the canonical single objective for mixed evidence. Open: scale, and no per-edge support record.

**11. Magliacane, Claassen, Mooij (2016). "Ancestral Causal Inference." NIPS 2016.** https://arxiv.org/abs/1606.07035
1. Problem: the same conflict problem, made tractable by reasoning over ancestral relations.
2. Representation: weighted inputs, either frequentist (w = |log p − log α|) or Bayesian log-odds. Loss is the sum of weights of violated inputs. Confidence per predicted feature is C(f) = min loss with ¬f forced − min loss with f forced. Interventions and background knowledge enter as weighted ancestral statements.
3. Implicit: only ancestral relations, no adjacencies or marks; the weights are not calibrated across sources.
4. Guarantees: soundness with oracle inputs and asymptotic consistency of C(f). It tends to ∞ for identifiably true features, −∞ for identifiably false ones, and 0 otherwise.
5. Evaluation: synthetic graphs with 6-9 variables against bootstrapped FCI/CFCI and Hyttinen et al.; flow-cytometry protein data.
6. Relevance: a published per-claim confidence with a three-way outcome, where 0 is a formal "undetermined". Open: mapping it to edge marks.

**12. Bromberg and Margaritis (2009). "Improving the Reliability of Causal Discovery from Small Data Sets Using Argumentation." JMLR 10:301-340.** https://jmlr.org/papers/v10/bromberg09a.html
1. Problem: unreliable independence tests on small samples.
2. Representation: a preference-based argumentation framework ⟨A, R, Π⟩. Propositions are test outcomes with a preference equal to an estimated probability of being correct. Pearl's independence axioms are the rules.
3. Implicit: the preference for "independent" uses a heuristic type-II error approximation; no expert input.
4. Guarantees: termination; exactly one of independence or dependence is accepted; no argument is left in abeyance under a strict preference order.
5. Evaluation: 8-variable networks with 6-13% accuracy gains; an approximate version up to 24 variables.
6. Relevance: defeat relations make it inspectable why a test result was overridden. Its forced binary decision is the opposite of abstention.

**13. Russo, Rapberger, Toni (2024). "Argumentative Causal Discovery." KR 2024.** https://arxiv.org/abs/2405.11250 (proceedings: https://proceedings.kr.org/2024/88/)
1. Problem: a symbolic, explainable resolution of inconsistent tests.
2. Representation: assumption-based argumentation. Assumptions are edges, non-edges and independencies; rules encode d-separation. Tests enter as weighted facts, and the weakest are dropped until a stable extension exists. Background knowledge is added as bodyless rules, i.e. hard.
3. Implicit: how weights should be calibrated; expert facts have no weight.
4. Guarantees: stable extensions correspond one-to-one with DAGs; the method recovers the true graph under stated conditions.
5. Evaluation: Asia, Cancer, Earthquake and Survey from bnlearn against Majority-PC and others. Scale is about 10 variables (per the fetched summary).
6. Relevance: every edge is derivable from named assumptions, so provenance exists in principle. Open: DAGs only, so no CPDAG or PAG marks.

**14. Li and Russo (2026). "Leveraging Large Language Models for Causal Discovery: a Constraint-based, Argumentation-driven Approach." UAI 2026, PMLR 337:3631-3667.** https://proceedings.mlr.press/v337/li26e.html (arXiv 2602.16481)
1. Problem: adding LLM-derived structural priors to Causal ABA.
2. Representation: the LLM gives required and forbidden arrows. Only arrows in the intersection of five independent queries are kept, and they enter as hard facts. A required arrow is enforced "only if the edge … was not already removed" by high-confidence tests. Remaining tests are weighted soft constraints.
3. Implicit: no confidence, calibration or abstention for individual LLM statements. The authors say "Consensus does not guarantee correctness; it is a pragmatic variance-reduction step".
4. Guarantees: those of Causal ABA; none about LLM correctness.
5. Evaluation: bnlearn benchmarks plus 54 synthetic DAGs grounded in CauseNet to resist memorisation. Best normalised SHD and F1; practical up to 15 nodes.
6. Relevance: the closest published design to an LLM-refinement stage with explicit evidence precedence (strong data beats the LLM). Open: weighted LLM evidence, PAGs, scale.

## D. Background knowledge with guarantees (hard knowledge)

**15. Meek (1995). "Causal Inference and Causal Explanation with Background Knowledge." UAI 1995.** https://arxiv.org/abs/1302.4972
- Also: Perković, Kalisch, Maathuis (2017), "Interpreting and using CPDAGs with background knowledge", UAI 2017. https://arxiv.org/abs/1707.02171
1. Problem: which orientations are common to all DAGs consistent with the independence facts and background knowledge (Meek); how to interpret and use the resulting maximally oriented PDAGs, or MPDAGs (Perković et al.).
2. Representation: required or forbidden directed edges as hard constraints; the output keeps an explicit undirected mark for "not determined".
3. Implicit: knowledge is assumed correct, with no weights or source.
4. Guarantees: Meek gives orientation rules for this setting (abstract only read; rule details not re-read). Perković et al. give ancestral-relation reading, an adjustment criterion and IDA variants for MPDAGs.
5. Evaluation: Perković et al. show effect identifiability improves with more knowledge in simulation. Meek's evaluation was not checked.
6. Relevance: an undirected edge is a legitimate final answer, and adding orientation knowledge never deletes an adjacency. Open: wrong knowledge.

**16. Andrews, Spirtes, Cooper (2020). "On the Completeness of Causal Discovery in the Presence of Latent Confounding with Tiered Background Knowledge." AISTATS 2020, PMLR 108:4002-4011.** https://proceedings.mlr.press/v108/andrews20a.html
1. Problem: whether FCI stays sound and complete with background knowledge.
2. Representation: tiers (a partial temporal order) over variables.
3. Implicit: knowledge correctness; non-tiered knowledge.
4. Guarantees: FCI with tiered knowledge is sound and complete.
5. Evaluation: theoretical (experiments not checked).
6. Relevance: tiered knowledge is the form of expert or LLM knowledge that provably keeps PAG semantics intact. Pairwise add/remove/orient edits on a PAG have no such result. Wang, Qin and Zhou (NeurIPS 2022, https://proceedings.neurips.cc/paper_files/paper/2022/hash/4334031bd9d518af18a6aba32ad70c8e-Abstract.html) extend completeness to local background knowledge.

## E. Bayesian priors and soft or erroneous expert knowledge

**17. Heckerman, Geiger, Chickering (1994/1995). "Learning Bayesian Networks: The Combination of Knowledge and Statistical Data."** https://arxiv.org/abs/1302.6815 (UAI 1994 version located; the 1995 Machine Learning journal version was not fetched)
- Also: Castelo and Siebes (1998), "Priors on network structures: biasing the search for Bayesian networks", CWI report INS-R9816. https://ir.cwi.nl/pub/4603 (the 2000 journal version is unverified)
1. Problem: combining expert knowledge with data in score-based learning.
2. Representation: Heckerman et al. use a prior network, an equivalent sample size, and a structure prior p(B) = c·κ^δ that penalises arc differences from the prior network. Castelo and Siebes expand partial pairwise beliefs into a prior over all structures.
3. Implicit: where κ or the pairwise probabilities come from; posterior edge marginals are not the reported output.
4. Guarantees: score equivalence of the BDe metric.
5. Evaluation: the Alarm network with noisy prior networks.
6. Relevance: the standard soft-prior representation. Open: priors on equivalence-class marks.

**18. Borboudakis and Tsamardinos (2012/2013). "Scoring and Searching over Bayesian Networks with Causal and Associative Priors." arXiv 1209.6561 (venue unverified).** https://arxiv.org/abs/1209.6561
1. Problem: experts state path-level beliefs, not edge-level ones.
2. Representation: per pair, a probability distribution over four typed relations (X causes Y, Y causes X, associated without direction, independent). Dependent or incoherent beliefs are reconciled into a joint prior and added to the score.
3. Implicit: how the belief probabilities are calibrated.
4. Guarantees: none stated in what I read.
5. Evaluation: simulated networks, ALARM and INSURANCE.
6. Relevance: the closest prior-side analogue of typed evidence. "Associated but direction unknown" is a first-class category that expert or LLM input can express.

**19. Amirkhani, Rahmati, Lucas, Hommersom (2017). "Exploiting Experts' Knowledge for Structure Learning of Bayesian Networks." IEEE TPAMI 39(11):2154-2170.** https://research.ou.nl/en/publications/exploiting-experts-knowledge-for-structure-learning-of-bayesian-n/ (DOI 10.1109/TPAMI.2016.2636828)
1. Problem: multiple fallible experts.
2. Representation: a score that marginalises over experts' accuracy (per the repository summary; the full text was not read this session).
3. to 5. Unverified beyond the summary.
6. Relevance: the published precedent for modelling source reliability as an explicit parameter, which is what an LLM source would need.

**20. Constantinou, Guo, Kitson (2023). "The impact of prior knowledge on causal structure learning." Knowledge and Information Systems 65:3385-3434.** https://link.springer.com/article/10.1007/s10115-023-01858-x
- Also: Chen, Ban, Wang, Lyu, Chen (2023), "Mitigating Prior Errors in Causal Structure Learning: Towards LLM driven Prior Knowledge", arXiv 2306.07032. https://arxiv.org/abs/2306.07032
- Also: Oates, Kasza, Simpson, Forbes (2017), "Repair of Partly Misspecified Causal Diagrams", Epidemiology 28(4):548-552, DOI 10.1097/EDE.0000000000000659. https://eprints.ncl.ac.uk/237964 (bibliographic record only; content unverified)
1. Problem: how much different kinds of knowledge help, and what wrong knowledge does.
2. Representation:
   - Constantinou et al. test ten knowledge types (directed, undirected and forbidden edges, temporal tiers, initial graph and others), split into hard and soft.
   - Chen et al. type the prior errors as irrelevant, indirect, reversed-indirect and reversed-direct, and detect order-reversed priors through "quasi-circles".
3. Implicit: Constantinou et al. sample all constraints from the ground truth, so erroneous knowledge is not studied there, contrary to what the lead suggested.
4. Guarantees: Chen et al. prove lemmas, under sufficient data, that order-reversed priors induce quasi-circles.
5. Evaluation:
   - Constantinou et al.: benchmark networks. Directed-edge knowledge is most useful; forbidden edges are "many times less effective".
   - Chen et al.: Asia, Child, Alarm and Insurance. About 60% of prior errors are detected while 90% of correct priors are retained.
6. Relevance: a typed taxonomy of knowledge and of knowledge errors exists. Open: constraint-based and PAG settings.

## F. Confidence sets and provenance models

**21. Strieder and Drton (2023). "Confidence in Causal Inference under Structure Uncertainty in Linear Causal Models with Equal Variances." Journal of Causal Inference.** https://www.degruyterbrill.com/document/doi/10.1515/jci-2023-0030/html (arXiv 2309.04298)
- Also: Wang, Kolar, Drton, "Confidence Sets for Causal Orderings", arXiv 2305.14506. https://arxiv.org/abs/2305.14506 (journal venue unverified)
1. Problem: frequentist uncertainty that includes structure uncertainty.
2. Representation: confidence regions for total effects by test inversion over all structures; a confidence set of causal orderings ("all orderings that the data do not rule out").
3. Implicit: strong model classes (linear Gaussian with equal variances; identifiable additive-noise models).
4. Guarantees: asymptotic (1−α) coverage. Strieder and Drton show the naive bootstrap fails here because of non-smoothness.
5. Evaluation: simulations (up to about 12 variables); a stock-portfolio example.
6. Relevance: the only coverage-guaranteed structure uncertainty I located. It is set-valued, not per-edge marks, and does not cover CPDAG or PAG output.

**22. Moreau and Missier (eds.) (2013). "PROV-DM: The PROV Data Model." W3C Recommendation, 30 April 2013.** https://www.w3.org/TR/prov-dm/
- Also: Groth, Gibson, Velterop (2010), "The anatomy of a nanopublication", Information Services and Use 30(1-2):51-56. https://www.doi.org/10.3233/ISU-2010-0613
1. Problem: a domain-neutral record of how a piece of data or a claim was produced.
2. Representation:
   - PROV has Entity, Activity and Agent, with wasGeneratedBy, used, wasDerivedFrom, wasAttributedTo, wasAssociatedWith and actedOnBehalfOf. Bundles give provenance of provenance.
   - A nanopublication is a core statement plus its context (the assertion / provenance / publication-info three-graph layout is the standard description, not re-read this session).
3. Implicit: no notion of evidential strength or conflict; nothing specific to causal graphs.
4. Guarantees: none statistical. PROV defines provenance as information usable "to form assessments about its quality, reliability or trustworthiness".
5. Evaluation: not applicable (a standard).
6. Relevance: each edge mark could be an Entity derived from named activities (test, bootstrap, LLM query, pruning) with agents attached. I found no published application to causal discovery output.

**Also located and relevant (not written up in full)**
- Faltenbacher, Wahl, Herman, Runge (2026), "How PC-based Methods Err: Towards Better Reporting of Assumption Violations and Small Sample Errors", UAI 2026, PMLR 337:1498-1519. https://proceedings.mlr.press/v337/faltenbacher26a.html. Coherency scores between ASP-style global checks and local conflict marks.
- Hiremath et al. (2025), "From Guess2Graph", arXiv 2510.14488. https://arxiv.org/abs/2510.14488. Expert or LLM input only reorders tests, so correctness never depends on it.
- Clivio et al. (2025), "Learning to Defer for Causal Discovery with Imperfect Experts", arXiv 2502.13132. https://arxiv.org/abs/2502.13132. Learned deferral between data and LLM; pairwise only.
- Verma et al. (2025), "Sequential Causal Discovery with Noisy Language Model Priors", arXiv 2506.16234. https://arxiv.org/abs/2506.16234. LLM samples aggregated into histograms over PAG edge types.
- Darvariu, Hailes, Musolesi (2024), "Large Language Models are Effective Priors for Causal Graph Discovery", arXiv 2405.13551. https://arxiv.org/abs/2405.13551. Soft priors with a three-way prompt.
- Wang, Lin, He, Gao, "Robust Causal Discovery under Imperfect Structural Constraints", arXiv 2511.06790. https://arxiv.org/abs/2511.06790
- Faller et al. (2024), "Self-Compatibility: Evaluating Causal Discovery without Ground Truth", AISTATS 2024. https://arxiv.org/abs/2307.09552
- Padh, Li, Casolo, Kilbertus, "Your Assumed DAG is Wrong and Here's How To Deal With It", UAI (year unverified). https://arxiv.org/abs/2502.17030. Sure, forbidden and uncertain edge sets.
- Lorch et al. (2021), DiBS, NeurIPS 2021. https://papers.nips.cc/paper/2021/hash/ca6ab34959489659f8c3776aaf1f8efd-Abstract.html
- Deleu et al. (2022), DAG-GFlowNet, UAI 2022. https://mlanthology.org/uai/2022/deleu2022uai-bayesian. Both give posteriors over DAGs, from which edge marginals follow.
- "Causal Discovery in Observational Medical Research: Scoping Review", https://pmc.ncbi.nlm.nih.gov/articles/PMC13032097/. Title from search only; the page was blocked, so content is unverified.

---

## (i) Synthesis

The literature keeps three kinds of evidence largely apart.

- **Resampling evidence** is a per-pair frequency. Since Friedman et al. (1999) the features have been typed: directed and undirected PDAG edges are different features. Mature tooling stores either strength plus direction-given-presence (bnlearn) or a full edge-type vector including "no edge" and circle marks (Tetrad; Jabbari et al.; Debeire et al.). Error control exists only for adjacency-like features (stability selection). Calibration studies show the frequencies are not probabilities and depend on the resampling scheme and tuning.
- **Test evidence** is combined explicitly in ASP (Hyttinen et al.), Ancestral Causal Inference, BCCD and argumentation (Bromberg and Margaritis; Causal ABA). These attach weights or probabilities to independence statements or ancestral claims and optimise one objective, with soundness or consistency results. They are limited to roughly 7-15 variables.
- **Background knowledge** is either hard with completeness guarantees (Meek; MPDAGs; tiered FCI) or a soft Bayesian prior (Heckerman et al.; Castelo and Siebes; Borboudakis and Tsamardinos; Amirkhani et al.). Errors in knowledge are studied mainly for score-based DAG learning.

Three things are missing. No published rule with guarantees maps bootstrap output over CPDAGs or PAGs to per-mark decisions. No framework's output graph carries a per-edge record of supporting evidence types, even where one is derivable (ABA, ASP). LLM-derived statements have no calibrated weight in any of these frameworks. A rule that consults only the directed-edge frequency contradicts every representation above: each would retain an edge that is stably present but unoriented.

## (ii) Is there an accepted, published way to turn bootstrap results over CPDAGs or PAGs into per-edge decisions that keeps adjacency confidence separate from orientation confidence?

**For DAGs and CPDAGs: yes as established practice, without formal guarantees.**
- Friedman, Goldszmidt, Wyner (1999) define confidence on PDAG features, with directed and undirected edges as distinct features.
- bnlearn's `boot.strength` (documented, and tied to Scutari and Nagarajan 2013) reports the arc's probability "modulo its direction" and, separately, each direction's probability "conditional on the arc being present".
- The inclusion threshold applies to strength only. Direction is settled afterwards, and the arc stays undirected when the directions are balanced.
- Scutari and Nagarajan (2013) supply the threshold estimator and state that it is unstable across samples.

**For PAGs: no accepted peer-reviewed rule.** What exists:
- Tetrad's per-pair edge-type distributions and the Preserved / Highest / Majority / Threshold ensembles. This is software documentation.
- Jabbari, Naeini, Cooper (2017): seven-way edge-type frequencies from bootstrap RFCI, which need post-hoc calibration.
- Debeire et al. (2024): majority vote over link types with conservative tie-breaking, for PCMCI+ graphs. Their confidence is explicitly not split into adjacency and orientation.

None of these comes with error control. The only finite-sample control (Meinshausen and Bühlmann 2010) covers adjacency-type selection.

## (iii) Which frameworks already combine tests, background knowledge and soft priors in one inspectable representation, and what do they lack for LLM-derived knowledge?

| Framework | Representation | Background knowledge |
|---|---|---|
| Hyttinen et al. 2014 (ASP) | Weighted (in)dependence constraints; minimise violated weight | Hard constraints |
| Magliacane et al. 2016 (ACI) | Weighted ancestral and independence statements; per-claim confidence C(f) | Weighted, including interventions |
| Bromberg and Margaritis 2009 | Preference-based argumentation over test outcomes | None |
| Russo et al. 2024; Li and Russo 2026 (Causal ABA) | Assumptions, d-separation rules, weighted test facts | Hard facts; LLM arrows gated by five-query consensus |
| Claassen and Heskes 2012 (BCCD) | Posterior probability per causal statement | Structure prior |
| Heckerman et al.; Castelo and Siebes; Borboudakis and Tsamardinos; Amirkhani et al. | Bayesian structure priors; typed path beliefs; expert-accuracy parameter | Soft |

What they lack for LLM-derived knowledge:
- **Calibration.** Weights are p-value transforms or Bayes factors. No published mapping turns LLM answers into commensurable weights. Li and Russo use an intersection of five queries and say it "does not guarantee correctness". Jabbari et al. need known edges to calibrate.
- **Error dependence.** All assume roughly independent evidence items. LLM errors are correlated across pairs and confounded by benchmark memorisation, which Li and Russo address only at evaluation time.
- **Provenance.** Support is recoverable from extensions or optimal solutions but is not exported as a per-edge, per-mark record. No work connects to PROV or nanopublication-style models.
- **Abstention.** ACI's C(f) = 0 and the undirected or circle marks are abstentions for data evidence. For the LLM source, only Clivio et al. learn when to defer (pairwise only). Hiremath et al. avoid the question by letting the expert reorder tests but never decide them.
- **Mark-level typing and scale.** Evidence attaches to independence or ancestral statements, not to CPDAG or PAG marks. Solvers stop at about 7-15 variables.

## (iv) Terminology used in this literature

- Resampling: bootstrap confidence; arc strength / edge intensity; direction probability (conditional on presence); edge-type probability; link frequency; selection probability; stability selection; bagging / bootstrap aggregation / ensemble graph (Preserved, Highest, Majority); model averaging; averaged network; inclusion threshold; calibration (Brier score, reliability, ECE, MCE).
- Graph semantics: adjacency vs orientation; skeleton; edge mark / endpoint (tail, arrowhead, circle); CPDAG / PDAG / MPDAG (maximally oriented PDAG); PAG / MAG; ambiguous (unfaithful) triple; conflict mark (x–x); adjacency-faithfulness vs orientation-faithfulness; conservative and majority-rule orientation; order-independence.
- Knowledge: background knowledge; required / forbidden edges; tiered (temporal) knowledge; local background knowledge; hard vs soft constraints; structure prior; prior network; equivalent sample size; path beliefs; imperfect experts; prior errors (reversed, indirect, irrelevant).
- Evidence combination: weighted constraints; conflict resolution; answer set programming; ancestral relations; confidence score; assumption-based argumentation; stable extension; attack / defeat; preference-based argumentation; learning to defer; coherency score; self-compatibility.
- Uncertainty and provenance: confidence set / region; test inversion; posterior edge marginal; provenance (entity, activity, agent, derivation, bundle); nanopublication (assertion, provenance).

## (v) Closest works from 2024-2026

1. Li and Russo (2026), UAI, PMLR 337. LLM priors inside Causal ABA with data-over-LLM precedence. https://proceedings.mlr.press/v337/li26e.html
2. Debeire, Runge, Gerhardus, Eyring (2024), CLeaR. Typed link-frequency bagging with a conservative tie order. https://proceedings.mlr.press/v236/debeire24a.html
3. Russo, Rapberger, Toni (2024), KR. Argumentative causal discovery. https://arxiv.org/abs/2405.11250
4. Faltenbacher, Wahl, Herman, Runge (2026), UAI, PMLR 337. Coherency scores and better reporting of PC errors. https://proceedings.mlr.press/v337/faltenbacher26a.html
5. Hiremath et al. (2025), arXiv 2510.14488. Unreliable experts guide tests without deciding them. https://arxiv.org/abs/2510.14488 (Runner-up for the bootstrap side: Banerjee, Andrews, Kummerfeld 2025, arXiv 2503.15436.)

## Where we're going

- The gap that looks defensible from this search is narrow: a typed per-edge evidence record (adjacency frequency, mark-type frequencies, test support, LLM assertion and its consistency, pruning decisions) with a decision rule that separates adjacency from orientation. It would be bnlearn's strength/direction split extended to circle marks, with PROV-style derivations.
- Before claiming novelty, three checks remain:
  - read the Tetrad `GraphSampling` source to pin down the exact semantics of the "Preserved" ensemble, since the javadoc wording is ambiguous;
  - read the blocked scoping review (PMC13032097) and Oates et al. for any reporting recommendations;
  - check Causal-Copilot's own code and paper for whether the 0.1 / 0.9 cut-offs cite any of the above.