# AU7: value of accuracy

Tickets: AUD-24, TGT-08, EVL-03
Written 2026-10-12 by an audit agent; sources read on that date.

**Where we are now:** this is a desk audit. It extends the earlier notes cluster3, cluster4, cluster8, cluster9 and dom09 and does not redo them. It also lines up with AU4's R11-R13 (decision-level scoring). Typed table: 45 rows in `AU7_value_of_accuracy.json`, with a compact version in section 5.

Number labels:
- `reported`: from the authors' own page, read today.
- `second-hand`: from an earlier project note, not re-opened today; the note is named.
- `measured (ours)`: from audit_context.md or dom09, not re-verified here.
- `our derivation` / `inference`: our own reasoning, not from a source.

The web-search budget for this turn ran out after about 30 searches. One fetch (Emezue et al. HTML) was refused with HTTP 429. Both are listed at the end.

---

## 1. Question

How do errors in a learned causal graph turn into errors in the decisions the graph is used for? At what accuracy, or with what guarantee, does a causal-discovery tool become worth using?

Concretely, for this project: does moving directed-edge F1 on CausalArena semantic scenarios from 0.63 (best published, FoundCause) toward the 0.957 identifiability limit matter for downstream use? Or do reliability, calibrated confidence and abstention matter more?

## 2. Method

**Starting point.** The earlier project notes listed in audit_context.md, especially cluster3 (edge confidence), cluster4 (fallible experts), cluster9 (query-level evaluation), cluster8 (metrics) and dom09 (what-if computation).

**Searches.** About 30 web searches, listed in section 10. We opened about 40 primary pages: arXiv abs/HTML/PDF, PMLR and NeurIPS proceedings, Nature Methods, Scientific Reports, bioRxiv/medRxiv, and author-hosted PDFs.

**Inclusion rule.** A source was kept if it does at least one of these:
- relates a graph-level metric to a decision-level one (interventional prediction, effect estimate, regret, top-k root-cause accuracy, experimental hit rate);
- measures the downstream value of discovery in a real application;
- measures how accurate human or expert causal graphs are, or how accurate they need to be;
- states what practitioners need.

**Reading caveat.** Pages were read through a fetch tool that summarises them. Table numbers below are as the tool reported them; spot-check before quoting in a paper.

---

## 3. Findings

### 3.1 Graph metrics are not decision metrics, and the difference is structured

**SHD misses which errors matter.** Peters and Bühlmann, *Neural Computation* 27:771-799 (2015), [PDF](https://stat.ethz.ch/Manuscripts/buhlmann/SID-final.pdf), [arXiv](https://ar5iv.labs.arxiv.org/html/1306.1043). All `reported`.
- Two estimates with equal SHD can differ in SID, which counts the (i, j) pairs whose intervention distribution the estimate gets wrong.
- Any supergraph of the true DAG has SID 0 (Prop. 3).
- At p = 40, n = 100, PC is best on SHD and worst on SID.
- At p = 5, n = 100, a random graph scored below PC's SID upper bound in 77 of 100 runs. PC's CPDAG can be no better than random for intervention prediction even when it beats random on SHD.

**Adjustment identification distance (AID).** Henckel, Würtzen, Weichwald, [arXiv 2402.08616](https://arxiv.org/html/2402.08616). All `reported`.
- SID is the parent-adjustment special case. AID adds ancestor-based and optimal-set (O-set) variants and handles DAGs, CPDAGs and causal orders.
- **Ancestor-AID is zero iff the guess respects the true causal orders.**
- For 300 pairs of 30-node graphs that differ by one edge (SHD = 1), the mean distances are 2.0 (ancestor), 5.9 (O-set) and 11.2 (parent) mis-identified pairs.
- A fully connected guess against an empty truth has maximal SHD and AID 0.
- The three AIDs correlate with each other at only 0.09-0.73. The authors' conclusion is that the choice of distance matters in practice.
- Runtime: milliseconds at p = 1000, against hours for SID.

**Estimand-level distance with latents (FID).** Li and Kilbertus, [arXiv 2510.25037](https://arxiv.org/pdf/2510.25037v1). All `reported`.
- A single reversal costs on average about 2.6 times as much as a deleted directed edge (mean FID 0.336 vs 0.130).
- FID correlates with SHD at r = 0.82, with wide spread within each SHD bin.

**Empirical evaluation.** Gentzel, Garant, Jensen, NeurIPS 2019, [ar5iv 1910.05387](https://ar5iv.labs.arxiv.org/html/1910.05387). All `reported`.
- On synthetic data, SHD and SID are strongly correlated, but SHD and total-variation distance between interventional distributions are only very weakly correlated (qualitative; no coefficient given).
- Algorithm orderings on empirical software-system data (Postgres and others) differ from orderings on synthetic data.
- Only 6 of 91 surveyed papers (7%) used both empirical data and interventional measures.

**Field practice.** Brouillard et al., [arXiv 2412.01953v2](https://arxiv.org/html/2412.01953v2). All `reported`.
- Interventional metrics appear in 9.1% (simulated) and 7.5% (real) of reviewed studies.
- Where real datasets contain interventions, interventional metrics went unused 89% of the time.
- The authors call interventional metrics "closest to what most practitioners care about".
- Sachs results have "peaked at an SHD of around 12".

**Bayesian posterior metrics.** Karimi Mamaghan et al., ICML 2024, [PMLR v235](https://proceedings.mlr.press/v235/karimi-mamaghan24a.html), `reported`: many metrics for Bayesian discovery correlate poorly with the quality of the posterior approximation.

**Task accuracy can be decoupled from edge F1.**
- CausaLab: observational-only GPT-5.2 reached 92% task accuracy with edge F1 0.471. `second-hand`, cluster9 note.
- Effect-level validation on game telemetry (Dang, Pham, Nguyen, [arXiv 2602.08340](https://arxiv.org/html/2602.08340v1)), `reported`:
  - PC (SHD 15) and BOSS (SHD 33) gave the same identified effect, about 0.144.
  - CFCI had the lowest SHD (11) but identified the effect in only one configuration.
  - Their reference graph is a domain-admissible baseline, not ground truth.

**Reading (inference).** For any query about the effect of an intervention, a graph's errors are not exchangeable.
- Errors that change ancestral order (reversals, and missing edges that change ancestry) or that hide a confounder are costly.
- Extra edges among a node's predecessors cost only efficiency.
- F1 and SHD weight all of these equally. SID, AID and FID do not.

### 3.2 How graph error propagates into effect estimates

**Order is what adjustment needs under causal sufficiency.** Vashishtha et al., [arXiv 2310.15117](https://arxiv.org/html/2310.15117), `reported`:
- Prop. 3.2: the variables preceding X in any topological order form a valid adjustment set.
- Prop. 3.3: a correct order (D_top = 0) holds iff the order yields a valid adjustment set for every treatment-outcome pair.

So with no hidden confounders, effect identification depends on order, not on the edge set. This is the same statement as "ancestor-AID = 0 iff orders respected" (Henckel et al.).

**Typed error cases** (`our derivation`; standard graphical reasoning under causal sufficiency and linear effects, no source read today):

| Graph error near the pair (X, Y) | Parent-adjustment effect estimate | Order-adjustment effect estimate |
|---|---|---|
| Extra edge (supergraph) | valid; efficiency loss only (SID 0) | valid |
| Missing edge C→X, C a confounder | not adjusted → bias = γ·α·Var(C)/Var(X) (omitted-variable algebra for Y = βX + γC + e, X = αC + u) | valid if C is still placed before X |
| Reversed C→X, i.e. X→C | C treated as a descendant, not adjusted → same confounding bias | bias if the order puts C after X |
| Reversed X→M (mediator), i.e. M→X | M adjusted → only the direct effect is estimated (over-control) | same |
| Reversed X→Y | predicted effect 0 | predicted effect 0 |
| Edge left undirected (CPDAG) | IDA returns a multiset; the minimum absolute value is a lower bound | (n/a) |

**Equivalence-class tools.** These all exist and are cheap at 20-40 variables (dom09, `measured (ours)`: all 600 pairs in 0.06 s):
- IDA ([arXiv 0810.4214](https://arxiv.org/abs/0810.4214));
- generalised adjustment ([JMLR v18](https://jmlr.org/papers/v18/16-319.html));
- MPDAG adjustment with background knowledge. Perković, Kalisch, Maathuis, [arXiv 1707.02171](https://arxiv.org/abs/1707.02171), `reported` (qualitative only): effects become more identifiable as background knowledge grows.

**Measured on our benchmark (dom09, `measured (ours)`).** On one 25-variable semantic scenario, the true parent set of X was among PC's IDA candidates for only 7 of 25 variables. What-if accuracy there is bounded by skeleton recall (0.52), not by ambiguity within the class.

**Bounds instead of one graph.** Padh, Li, Casolo, Kilbertus, [arXiv 2502.17030](https://arxiv.org/html/2502.17030v2) (proceedings page lists editors Huang and Drton; [PMLR v275](https://proceedings.mlr.press/v275/padh25a.html)). `reported`:
- Bounds over all DAGs consistent with sure, forbidden and uncertain edges covered the true ATE 93-99% of the time in synthetic tests.
- On IHDP the bounds were wide: [2.4, 7.2] around a true 4.7.
- They warn that PC-derived edge sets may exclude the true graph.

### 3.3 Decision and regret studies

**Causal bandits.** Learning the graph is not the goal, and can conflict with the goal.
- Shahverdikondori, Etesami, Kiyavash, [arXiv 2510.16811](https://arxiv.org/abs/2510.16811), `reported`: learning the reward's parent set is suboptimal for regret, sometimes in direct conflict with it. Their near-optimal algorithms skip graph recovery.
- Elahi, Ghasemi, Kocaoglu, [arXiv 2411.04054](https://arxiv.org/html/2411.04054v1), `reported`: with latents, recovering the induced subgraph on the reward's ancestors plus a characterised set of confounders suffices for sublinear regret.

**Causal Bayesian optimisation.** Durand, Annadani, Bauer, Parbhoo, [arXiv 2503.19554](https://arxiv.org/html/2503.19554v1), `reported`:
- Standard CBO needs a fully and accurately specified graph.
- Under their assumptions only the target's direct parents matter. CBO-U, which learns a posterior over them, converges to the true-graph optimum.
- CBO with a wrong graph does worse on average.
- No numeric regret is given in the text read.

**Reading (inference).** For decisions about one outcome, the value lies in a small, local part of the graph: the outcome's parents or ancestors, and the confounders between them. Global F1 dilutes errors there with errors everywhere else.

### 3.4 Applications with measured downstream value

#### Root-cause analysis in IT operations

The decision is which component to investigate. The metric is top-k accuracy, AC@k or Avg@k.

**Pham et al., ASE 2024** ([arXiv 2408.13729](https://arxiv.org/html/2408.13729v1)), the closest "graph quality vs RCA" study. All `reported`.
- Nine discovery methods reached directed F1 of only about 0.1 to 0.54 on RCA synthetic graphs.
- PC-, FCI-, Granger- and LiNGAM-based RCA performed "similarly to Dummy" (random).
- BARO, a non-causal method, reached Avg@5 0.94 (Online Boutique CPU) and 0.81 (Train Ticket CPU).
- CausalRCA, the best causal method, scored 0.97 and 0.53 on those two, and 0.05 on CIRCA10 synthetic data.
- No correlation between graph F1 and RCA accuracy is reported. The best discovery methods were not the best RCA methods.

**RCAEval** (WWW 2025, [arXiv 2412.17015](https://arxiv.org/html/2412.17015v1)). All `reported`.
- 735 cases on Online Boutique, Sock Shop and Train Ticket; 15 baselines.
- Text says CIRCA and RCD are best (Avg@5 0.46 and 0.54).
- Table 6 shows BARO at about 0.80 and TraceRCA at 0.77. Text and table are inconsistent; re-read before citing.

**PetShop** (CLeaR 2024, [arXiv 2311.04806](https://arxiv.org/html/2311.04806v2), [PMLR](https://proceedings.mlr.press/v236/hardt24a.html)). All `reported`.
- 41 services, 68 injected issues.
- Methods given the X-Ray service map usually win; CIRCA reached top-3 recall of 0.86-1.00 in four of six settings.
- Without a graph, "none of the proposed approaches outperform the basic ranked correlations". Ranked correlation was best at top-1.

**CIRCA** (KDD 2022, [arXiv 2206.05871](https://arxiv.org/pdf/2206.05871)), `reported`.
- On 99 real Oracle database faults, CIRCA with a knowledge-built structural graph reached AC@5 0.763 (Avg@5 0.603).
- Random-walk methods on a PCTS-learned graph reached AC@5 0.449 (Avg@5 0.290) and were about 40 times slower.
- Caveat: the graph's effect is not isolated from the scoring method.

**RCD** (NeurIPS 2022, [PDF](https://par.nsf.gov/servlets/purl/10495798)), `reported`.
- Learns only the neighbourhood of the failure node.
- About 98% top-1 recall on synthetic data.
- Sock-shop top-1 recall is mixed: 0.11-0.71, and below ε-Diagnosis for some services.
- Full-graph Ψ-PC matched it on synthetic data but took more than 150 minutes at 500 nodes, against about 22 s.

**Deployed systems** (`reported`; both are authors' own claims about their own deployments):
- Groot, an event graph from rules ([arXiv 2108.00344](https://arxiv.org/abs/2108.00344)): 95% top-3 and 78% top-1 on 952 production incidents.
- AWS cloud-network RCA, a Granger-learned event graph ([arXiv 2606.13532](https://arxiv.org/pdf/2606.13532)): recall@3 85.7% and exact match 74.3% on 35 incidents, against 62.8% and 48.6% for the rule baseline.
  - Its learned graph has cycles and some edges that contradict domain knowledge, and still adds value over rules.

#### Experiment planning in molecular biology

The decision is which gene to perturb or test. The metric is the hit rate of validation experiments. All `reported`.
- **IDA** (Maathuis et al., *Nature Methods* 2010, [PDF](https://stat.ethz.ch/Manuscripts/buhlmann/maathuisetal2010.pdf)):
  - Yeast, from 63 observational profiles, scored against 234 knockouts.
  - Of IDA's top 50 predicted effects, 33 (66%) were in the true top 10%, against 10 (Lasso), 8 (elastic net) and 5 ± 2.1 (random).
- **ICP** (Meinshausen et al., *PNAS* 2016, [PMC4941490](https://pmc.ncbi.nlm.nih.gov/articles/PMC4941490)):
  - Its top 4 edges were all strong intervention effects, and 7 of its top 20, where random guessing expects 0.03.
  - The method issues confidence statements and makes few predictions.
- **CStaR** (Stekhoven et al., *Bioinformatics* 2012, [PDF](https://stat.ethz.ch/Manuscripts/buhlmann/cstar.pdf)): of 9 testable Arabidopsis mutants from top-ranked genes, 4 showed a flowering-time effect (unadjusted p < 0.05).
- **DREAM5** (Marbach et al., *Nature Methods* 2012, [nmeth.2016](https://www.nature.com/articles/nmeth.2016)):
  - 23 of 53 novel *E. coli* predictions were supported (43%).
  - The community networks have about 50% precision.
- **Counter-evidence:**
  - BEELINE ([bioRxiv 642926](https://www.biorxiv.org/content/10.1101/642926.full.pdf), preprint version read): many GRN methods have early precision near random on curated models.
  - CausalBench (Chevalley et al., [arXiv 2210.17283](https://arxiv.org/html/2210.17283v2)):
    - Interventional methods were no better than observational ones.
    - GRNBoost and sortnregress ranked at the top.
    - Methods sat at precision-recall extremes; NOTEARS-linear, for example, had precision 0.88 and recall about 0.

#### Medicine and epidemiology

`reported`:
- **Shen, Ma, Vemuri, Simon** (*Sci. Rep.* 2020, [s41598-020-59669-x](https://www.nature.com/articles/s41598-020-59669-x)). Alzheimer's, ADNI, 8-edge literature gold standard.
  - FGES precision and recall went from 0.44 / 0.60 to 0.71 / 0.68 with trivial background knowledge.
  - A single wrong independence test created a false collider that propagated through FCI's graph.
  - No downstream decision was measured.
- **Constantinou et al.** COVID-19 case study ([arXiv 2305.03859](https://arxiv.org/abs/2305.03859v1)).
  - 28 algorithms were run against an author-built "common knowledge" graph (17 variables, 37 edges).
  - The authors note the graph captures observational, not interventional, relations.
  - We could not reach its results section (see Not read).

#### Manufacturing

- Marazopoulou et al. ([arXiv 1605.04056](https://arxiv.org/abs/1605.04056v2)): assembly-line discovery was assessed only by standard metrics and expert review. No downstream yield or cost was measured. `reported`
- Vendor manufacturing case studies are AU5's scope and are not used here.

### 3.5 How accurate are humans and experts, and how accurate must they be?

**Hand-drawn DAGs in health research.** Tennant et al., *IJE* 2021, [PDF](https://eprints.whiterose.ac.uk/id/eprint/180527/1/dyaa213.pdf). All `reported`.
- 144 DAGs in 234 articles: median 12 nodes and 46% of possible arcs.
- No article tested its DAG against the data.
- 73% reported estimates from adjustment sets other than, or not clearly derived from, the DAG.
- Recommendation: assume arcs exist unless omission is justified. This is consistent with SID/AID treating extra edges as harmless for validity.

**DAG knowledge, attitudes and practice survey** ([medRxiv 2020.01.17.20017939](https://www.medrxiv.org/content/10.1101/2020.01.17.20017939.full.pdf); authors not captured by the fetch). All `reported`.
- About 60% of respondents use causal graphs.
- About 20% of users build them by a systematic process.
- About half know that omitting an arrow is the stronger assumption.

**Lay annotators.** Vashishtha et al. `reported`: 15 STEM annotators had SHD of 1.67-11.33 on 4-8 node BNLearn graphs with triplet prompts, with D_top mostly 0.

**Required expert accuracy** (`reported`):
- Ankan and Textor, UAI 2025 ([PMLR v286](https://proceedings.mlr.press/v286/ankan25a.html)): expert-in-the-loop refinement beats data-only learning once new-edge orientations are right in at least 2 of 3 cases.
- Kitson and Constantinou, Tabu-AL ([arXiv 2310.11154](https://arxiv.org/pdf/2310.11154v1)): querying on uncertain edges raises mean F1 by:

| Expert accuracy | Mean F1 gain |
|---|---|
| 1.0 | 0.207 |
| 0.9 | 0.138 |
| 0.8 | 0.096 |
| 0.67 | 0.063 |
| 0.5 | accuracy worsens |

**LLM experts** (`second-hand`, cluster4):
- LLMs are more reliable on orientation than on existence: 96% orientation accuracy against 60.3% edge recall (Kitson and Constantinou 2026).
- Verbalised confidence is not calibrated (Kumar et al. 2026).

### 3.6 What practitioners say they need

`reported`:
- **CAWS 2021 round table** (Kummerfeld et al., [PMLR v160](https://proceedings.mlr.press/v160/kummerfeld21a/kummerfeld21a.pdf); 61 participants, 15% from industry):
  - reliability on finite real data is "uncertain";
  - gold-standard datasets are scarce;
  - many scientists doubt causal analysis is possible.
- **Brouillard et al.:** practitioners use discovery "as an exploratory tool", not to derive an irrevocable causal truth.
- **KAP survey:** barriers are not knowing how to use graphs and choosing which arrows to include. Users asked for tools and pre-published graphs.

**Not found** by these searches: a survey of industry practitioners with a stated numeric accuracy requirement for causal discovery, or an industry talk with a stated graph-accuracy threshold. The only operational numbers are deployed RCA hit rates (78-95% top-1/top-3), which the authors reported for systems in use.

---

## 4. Answers to the four required questions

### 4.1 What score or guarantee makes a discovery tool invaluable? (per application)

| Application | Decision | What the evidence says matters | Evidenced numbers | Our inference (target) |
|---|---|---|---|---|
| **RCA (IT ops)** | which component to inspect first | Local structure upstream of the anomaly, timing, and a strong non-causal baseline. Globally learned graphs at F1 ≤ 0.54 gave RCA no better than random. Knowledge or topology graphs plus local scoring win. | BARO Avg@5 0.81-0.94; deployed 78% top-1 / 95% top-3 (Groot), 85.7% recall@3 (AWS); structural vs learned AC@5 0.763 vs 0.449 (CIRCA). | Worth using only if top-3 accuracy beats the best non-causal baseline (BARO, ranked correlation) on the same incidents, and it says "unknown" instead of ranking when evidence is weak. Global F1 is close to irrelevant; ancestor accuracy for the anomalous node is what counts. No paper gives a graph-F1 threshold. |
| **Policy / effect estimation** | sign and size of the effect of X on Y; whether to act | Correct ancestral order and no hidden confounder between X and Y. Extra edges are harmless for validity. One reversal near the pair can flip or null the estimate. Bounds over graph uncertainty cover the truth but are wide. Practice: hand-drawn DAGs are never tested against data. | AID: one edge costs 2-11 mis-identified pairs on average; Padh IHDP bounds [2.4, 7.2] vs 4.7; Tennant: 0 of 144 DAGs tested. | The valuable output is a per-query guarantee: "identified under assumptions A, interval with stated coverage", or "not identified: bounds, and the experiment that resolves it". Target: precision of committed effect-sign claims ≥ 0.9 at stated coverage, with ancestor-AID reported. No published threshold; this is our proposal. |
| **Experiment planning (biology, labs)** | which interventions to run | Precision of the top few ranked predictions against later experiments, relative to the base rate. Global graph accuracy can stay low. | IDA 66% vs 10% random in the top 50; ICP 7/20 vs 0.03 expected; CStaR 4/9; DREAM5 43%. | Invaluable when lift over the base rate is large at small q (5-50 experiments) and the ranking comes with error control (ICP-style). F1 is the wrong score. |
| **Model building with experts (epidemiology)** | which DAG to adopt for adjustment | Orientation accuracy of the expert above about 2/3 helps; data should flag missing or superfluous edges. | Ankan and Textor 2/3; Tabu-AL gain falls about 33% at 90% accuracy. | A tool that tests an expert DAG against data and reports which arcs the data contradict fills a documented gap: no article tested its DAG. |

### 4.2 Has precision at a stated coverage (abstaining on uncertain edges) been shown to improve downstream decisions?

**Partly.**

**Shown, for experiment planning.** Ranking and then committing to only the most confident predictions improved the hit rate of real validation experiments well above random and above non-causal baselines:
- IDA, top 50: 66% vs 20% (Lasso) and 10% (random);
- ICP's few predictions, which come with confidence statements;
- CStaR's stability ranking, which improved on plain IDA (shown in a plot only).

These are precision-at-small-coverage results with interventional ground truth, all `reported`. However, they are rankings, not calibrated per-edge abstention with a stated error rate. Only ICP comes with a formal error statement.

**Shown at graph level, not decision level.**
- Tabu-AL improves F1 when the algorithm asks on uncertain edges.
- Bootstrap edge confidence and stability selection control adjacency errors (cluster3).
- The one formal LLM-expert guarantee (Long et al.) failed in its own LLM test (cluster4).

**Not found:**
- a study showing that per-edge abstention or calibrated edge confidence improves effect-estimation or policy decisions on held-out interventions;
- a risk-coverage curve over causal claims scored against interventions;
- abstention in RCA.

Benchmarks that score abstention exist: CausalDS and CIVeX (cluster9). Neither reports real downstream decisions.

**This is an open, testable gap, and our data can test it** (section 4.3).

### 4.3 Proposal: scoring "decision value" on top of F1

**What the data offer** (`measured (ours)`, inspected today):
- **CausalArena semantic obs+int files:** 50 public scenarios with 800 observational and 200 interventional rows.
  - Interventions are single-target, with 3-7 targets per scenario (median 3) and 28-67 rows per target.
  - The semantics are `do_resampling_and_descendant_recomputation`: the target is redrawn from a distribution, not clamped.
- **Causal Chambers `lt_interventions_standard_v1`:**
  - single-target interventions on every manipulable light-tunnel variable at weak/mid/strong strength;
  - a `uniform_reference` experiment;
  - a validated ground-truth graph (Gamella, Peters, Bühlmann, *Nature Machine Intelligence* 2025, DOI 10.1038/s42256-024-00964-x, per the dataset README; [arXiv 2404.11341](https://arxiv.org/abs/2404.11341)).

**Metric DV-1: held-out interventional claim accuracy, with a risk-coverage curve.**

*Labels from data.* For every released target t and every other variable y, compare y's interventional rows with the observational rows:
- two-sided Mann-Whitney test with BH at q = 0.05;
- record the sign of the median shift;
- label each pair `up`, `down` or `none`.

Keep only targets whose own distribution shifts detectably. Under resampling semantics some targets barely move, and their pairs carry no label.

*Claims from the method.* Using only the observational rows and the method's output graph, each pair gets one claim:
- `not a descendant`;
- `descendant, sign +` or `descendant, sign −`, when every IDA / MPDAG value has that sign;
- `abstain`, for a possible descendant or a mixed-sign multiset.

A ledger supplies a confidence for each claim.

*Scores.*
- Precision of committed claims and coverage.
- AURC and precision at 50% and 80% coverage.
- Eigenmann et al.'s descendant-set Jaccard as a no-sign variant ([UAI 2020](https://proceedings.mlr.press/v124/eigenmann20a.html); [arXiv 2006.15387](https://arxiv.org/pdf/2006.15387)).

*Ceiling.* Report the same scores for the true graph plus observational rows. This separates graph error from finite-sample and mechanism error. It is the decision-level analogue of the 0.957 limit.

*Why this metric.* It is computable now. It directly tests 4.2, i.e. whether abstention raises decision precision. It applies unchanged to Causal Chambers, where actuator→sensor pairs at three strengths add a dose-monotonicity check.

**Metric DV-2: target-choice regret and experiment lift.**

*Regret.* For each scenario and each outcome y that at least one released target moves:
- the method picks the target with the largest predicted standardised effect on y, or abstains;
- regret = (largest observed standardised shift of y over the targets) − (observed shift under the chosen target);
- abstaining costs a fixed c, the price of running one experiment.

Report mean regret and the abstain rate as c varies.

*Lift.* Maathuis-style precision@q of the top-q ranked (t, y) claims against the data labels, divided by the base rate.

*Caveat.* With a median of 3 targets per scenario, regret on CausalArena is coarse. The replay sampler can generate held-out targets, but that is simulation, so label it as such. Causal Chambers has every manipulable variable intervened and gives the cleaner regret test.

**Graph-only companion (no data needed).** Report gadjid's ancestor-AID and O-set-AID next to F1 for every run, on CPDAG and forced-DAG outputs (AU4 R07 already proposes this).

**Required control.** Compute everything on column-shuffled inputs. A method that reads the released column order gets a correct causal order, and so ancestor-AID = 0 and valid adjustment for every pair, from layout alone (`inference`, from Prop. 3.3 plus our 0.680 order-leak finding). Decision metrics are more exposed to the order leak than F1 is.

### 4.4 What approaching the 0.957 limit would and would not give

**Would give** (`inference` grounded in 3.1-3.2):
- If 0.957 is reached by recovering the true CPDAG, every compelled orientation is right.
- Every pair is then either identified (amenable) or has a small IDA multiset that contains the truth. Under causal sufficiency, adjustment is valid wherever the class allows it.
- With the released interventions (≥ 0.974), the multisets shrink further.
- This is a large step from today's state. In dom09, PC's class contained the true parent set for only 7 of 25 variables (`measured (ours)`).

**Would not give:**
1. **F1 is blind to error type.** A forced-orientation output can reach high F1 while containing a few order inversions next to the pairs that matter. One reversal costs 2-11 mis-identified pairs on average (AID), and reversals are about 2.6 times as costly as deletions (FID). Two outputs with the same F1 can differ widely in decision value. The 0.714 result from true depth alone (`measured (ours)`) shows how much of the decision-relevant content is order, which F1 rewards only indirectly.
2. **No calibrated uncertainty or abstention.** A point graph at 0.957 carries no statement of which 4% is wrong. Decision users need that, as the ICP and IDA experiment-planning successes show.
3. **No effect magnitudes.** Finite-sample estimation and mechanism misfit remain; DV-1's true-graph ceiling measures them.
4. **No transfer to other worlds.** Hidden confounders, time series and real data are outside the limit. Rankings change between synthetic and empirical data (Gentzel et al.), and the RCA literature shows discovery that looks good on synthetic data being near-random in practice (Pham et al.).
5. **For local decisions, most of the gain is irrelevant.** RCA, bandits and CBO need only the target's ancestors or parents (Shahverdikondori; Elahi; Durand; RCD). A tool can be decision-perfect for one outcome at modest global F1.

**Bottom line** (`inference`): moving F1 toward 0.957 matters only insofar as it removes order errors and missed confounders near the queried pairs. For the uses evidenced in the literature, the published value came from three things:
- precision on a small set of confident claims, validated by intervention;
- local correctness around the target;
- explicit statements of what is identified.

Neither the reviewed literature nor our own measurements support a global F1 threshold at which a tool becomes "worth it".

---

## 5. Typed table (compact; full rows with sources in the JSON, ids V01-V45)

| Ids | Setting | Graph metric | Downstream metric | Relation (label) |
|---|---|---|---|---|
| V01-V04 | SID paper, synthetic | SHD | SID | equal SHD, different SID; supergraph SID 0; PC best SHD / worst SID at p=40; random < PC's SID upper bound 77/100 at p=5 (reported) |
| V05-V07 | AID, synthetic | SHD, order | parent/ancestor/O-set AID | SHD=1 -> 2.0/5.9/11.2 pairs; AIDs inter-correlate 0.09-0.73; ancestor-AID 0 iff order right (reported) |
| V08 | FID with latents | SHD | estimand distance | reversal 0.336 vs deletion 0.130; r=0.82 (reported) |
| V09 | Gentzel, software systems | SHD/SID | interventional TVD | very weak SHD-TVD correlation; synthetic != empirical ordering (reported) |
| V10-V11 | Brouillard; Karimi Mamaghan | structural | interventional / posterior | 7.5-9.1% use interventional; metrics track posterior poorly (reported) |
| V12 | Eigenmann, synthetic | (none) | causal risk from interventions | estimable from data; signs mostly right (reported) |
| V13-V14 | Vashishtha; Dang | D_top, SHD | valid adjustment; identified ATE | order <=> valid adjustment; SHD 15 vs 33 -> same ATE (reported) |
| V15-V16 | Padh; dom09 | edge uncertainty; skeleton recall | ATE bounds; IDA candidates | bounds cover truth but wide; true parents in 7/25 (reported; measured ours) |
| V17-V19 | CBO, bandits | parent/ancestor recovery | regret / optimum | parents or ancestors suffice; full graph not needed (reported) |
| V20-V26 | RCA benchmarks and deployments | F1 0.1-0.54; learned vs structural | AC@k, Avg@5 | learned-graph RCA ~ random; structural 0.763 vs learned 0.449; deployed 78-95% (reported) |
| V27-V32 | Biology | ranking / global | validation hit rate | 66% vs 10%; 7/20 vs 0.03; 4/9; 43%; near-random in BEELINE/CausalBench (reported) |
| V33-V34 | Medicine | precision/recall vs literature | none measured | 0.44 -> 0.71 with trivial knowledge; COVID results not read (reported) |
| V35-V40 | Experts and practitioners | expert accuracy / practice | F1 gain; adjustment practice | 2/3 orientation threshold; gain -33% at 90% accuracy; 0/144 DAGs tested (reported) |
| V41 | Manufacturing | expert review | none measured | no downstream value measured (reported) |
| V42-V45 | Second-hand rows | various | various | CausaLab 92% task acc at F1 0.471; LLM orientation vs existence; Long et al. guarantee broke; LLM calibration (second-hand) |

---

## 6. What this changes for the project

1. **Stop treating the 0.957 limit as the practical target.** Report it as the structural ceiling, and add a decision-level ceiling: DV-1 with the true graph plus observational rows. The claim ledger should be judged on decision precision at stated coverage, not on F1 alone. (TGT-08)
2. **Add DV-1 and DV-2 to the scorer** (EVL-03), plus ancestor-AID and O-set-AID via gadjid, all on column-shuffled inputs. DV-1 needs only the released obs+int files and runs in seconds per scenario.
3. **Test the open claim directly.** Does abstention by the ledger raise held-out interventional claim precision on CausalArena and Causal Chambers? The literature does not show this for effect decisions (4.2). A positive or negative answer is publishable either way.
4. **Rank the ledger's work by decision impact.** Order provenance and confounder detection near queried pairs come first, global edge count second. Our 0.714 true-depth result and Vashishtha's Prop. 3.3 point the same way.
5. **For any RCA or applied pitch (STR-06), compare against non-causal baselines** (BARO, ranked correlation). Claim value only as top-k lift on the same incidents.
6. **Phrase the guarantee per query:** identified or not, interval with coverage, abstain. This matches what the evidence rewards and the honest-capability framing.

## 7. Open questions

- What ancestor-AID and DV-1 precision do PC, GES and FoundCause-class outputs reach on shuffled CausalArena files, against their F1 of 0.33-0.63? This is the actual F1 → decision mapping for our benchmark. It is a compute task (AU9-type), not desk.
- With 28-67 interventional rows per target, what fraction of true descendant pairs are detectable? This sets the noise floor for DV-1 labels.
- Is there an industry survey with stated accuracy thresholds? Not found; the search budget ran out (see 10).
- Do Emezue et al. (Bayesian discovery scored by ATE) report a correlation between structure and ATE error? Only the abstract was read.
- The full Constantinou et al. COVID-19 results: how different were the effects implied by the 28 learned graphs?

## 8. Not read

| Source | Reason |
|---|---|
| Emezue et al., [arXiv 2307.04988](https://arxiv.org/html/2307.04988v1) full text | HTTP 429 from the fetch proxy; abstract page only |
| Constantinou et al., [arXiv 2305.03859](https://arxiv.org/pdf/2305.03859v1) results sections | Four fetches at different offsets returned methods and tables only |
| "Construction and Application of DAGs in Leading Medical Journals", [PMC12805448](https://pmc.ncbi.nlm.nih.gov/articles/PMC12805448) | reCAPTCHA page |
| Budhathoki et al., ICML 2022, full PDF | Abstract page only; graph-robustness experiments unknown |
| LeGIT ([arXiv 2503.01139](https://arxiv.org/abs/2503.01139)) human-vs-LLM numbers | Abstract only. The SHD numbers in cluster4 (17.40 vs 22.60 humans) are not re-verified |
| Graph-Agnostic CBO ([arXiv 2411.03028](https://arxiv.org/abs/2411.03028v1)) | Abstract had no numbers |
| BEELINE final *Nature Methods* version | Read the bioRxiv preprint PDF instead |
| Cinelli and Hazlett (omitted-variable bias) | Not opened. The bias formula in 3.2 is labelled our derivation |
| Vowels et al., "D'ya like DAGs?" | Abstract had nothing on evaluation; not used |
| Industry talks or practitioner surveys with numeric thresholds | Not located before the web-search budget was exhausted |

## 9. Sources read (date read 2026-10-12)

All URLs are in the JSON rows. Every row lists its URL(s) and `read_on`.

## 10. Searches run (2026-10-12)

1. Root Cause Analysis for Microservices based on Causal Inference: How Far Are We? causal discovery graph quality RCA accuracy
2. RCAEval benchmark root cause analysis microservice arXiv Pham
3. PetShop dataset root cause analysis causal discovery benchmark Hardt arXiv
4. Gentzel Garant Jensen "The Case for Evaluating Causal Models Using Interventional Measures and Empirical Data"
5. Ikram root cause analysis of failures in microservices through causal discovery NeurIPS 2022 RCD top-k
6. Peters Bühlmann structural intervention distance SID causal graphs arXiv 1306.1043
7. Eigenmann Mukherjee Maathuis "Evaluation of causal structure learning algorithms via risk estimation" UAI 2020
8. Maathuis Colombo Kalisch Bühlmann 2010 Nature Methods predicting causal effects ... IDA
9. Meinshausen Hauser Mooij Peters Versteeg Bühlmann "Methods for causal inference from gene perturbation experiments and validation"
10. Stekhoven ... causal stability ranking Arabidopsis flowering time validation mutants
11. CausalBench Chevalley large-scale benchmark ... Wasserstein false omission rate results
12. BEELINE Pratapa 2020 benchmarking gene regulatory network inference ... random predictor
13. Constantinou "Open problems in causal structure learning: A case study of COVID-19 in the UK"
14. inter-rater agreement directed acyclic graphs drawn by different researchers same research question epidemiology
15. Tennant 2021 "Use of directed acyclic graphs (DAGs) to identify confounders in applied health research"
16. causal Bayesian optimization misspecified causal graph regret unknown graph learned graph
17. "Your Assumed DAG is Wrong and Here's How To Deal With It" Padh Kilbertus
18. simulation study consequences of misspecified DAG for confounder adjustment bias missing arc reversed arc
19. causal discovery downstream effect estimation error correlation with SHD benchmark ... ATE
20. decision-focused evaluation causal discovery regret policy learned graph
21. "Effect-Level Validation for Causal Discovery" arXiv
22. interview study causal inference practitioners industry needs challenges causal discovery adoption survey
23. survey of practitioners causal discovery "practitioners" trust uncertainty requirements questionnaire 2024 2025
24. industry experience causal discovery deployed root cause analysis production lessons learned accuracy ... top-1 top-3
25. causal discovery manufacturing root cause analysis case study evaluation downstream value production line review
26. root cause analysis sensitivity to causal graph errors misspecified graph ... (**not performed: web-search budget for the turn exhausted**)

"Not found" statements in this note refer to searches 1-25 plus the earlier project notes.

---

**Where we're going:** wire DV-1 (interventional claim precision and coverage) and ancestor-AID into the scorer on shuffled CausalArena files and Causal Chambers. Then run PC, GES and the ledger through it, which turns "does 0.63 → 0.957 matter?" into a measured curve rather than an argument.
