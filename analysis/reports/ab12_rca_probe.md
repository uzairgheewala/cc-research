# AB-12 RCA vertical probe: declared topology vs learned graph vs no graph, with abstention (PetShop)

Tickets: AUD-43 (this bundle), STR-06. Written 2026-10-13. No LLM calls. One command reproduces every number:

```
cd /home/claude/work/kit && nice -n 10 /home/claude/work/engines/venv/bin/python -W ignore analysis/ab12_rca_probe.py
```

(about 100 s wall and 65 s CPU on the shared box). Outputs: `analysis/results/rca/rca_probe.json` (all numbers, per-issue
ranks and outcome classes, P15 verdict), `analysis/results/rca/CONTRACT.json`, and `analysis/results/rca/ab12_prereg.json`
(protocol frozen before any test result was computed, sha256 `5d5939da…88cb`, recorded in both outputs).

Labels: **measured** means computed by the script; **read** means read in the authors' code, notebook or paper;
**interpretation** is our reading.

## 0. Where we are now

AB-04 established that learned graphs carry little decision value on CausalArena. The audit synthesis (AU0) noted that
industrial RCA ranks causes over a *declared* topology. AB-12 tests that on the one public RCA benchmark that ships a
declared call graph: the AWS PetShop dataset (Hardt et al., CLeaR 2024; data CC BY 4.0, code Apache-2.0). P15 was
registered in the audit DAG before this bundle: *declared topology plus abstention beats learned-graph RCA on AC@3 by
at least 0.1; refuted if the gap is under 0.03.*

## 1. The dataset (read)

- **Layout.** There are four scenarios: `low_traffic`, `high_traffic`, `temporal_traffic1` and `temporal_traffic2`. Each has:
  - `graph.csv`: the declared call graph. It is a 41-44 node 0/1 adjacency matrix from AWS X-Ray, where row A, column B = 1 means A calls B. It is acyclic in all four scenarios.
  - `noissue/metrics.csv`: the normal period, with 589 five-minute rows (1652 in the temporal scenarios). Columns are a 3-level header: service x {latency, availability, requests} x {Average, Sum, p50, p90, p95, p99}.
  - `{train,test}/issue_k/metrics.csv`: 5 rows each.
  - `{train,test}/issue_k/target.json`: the SLO target node, metric and aggregate, plus the root-cause node. Its root-cause metric is always null.
- **The README does not describe `graph.csv`.** `rca_task.load_scenario` reads it with `nx.from_pandas_adjacency`.
- **Issues.** There are 68 in total.
  - Test has 48: low 18, high 18, temporal1 6, temporal2 6. It has 26 latency and 22 availability issues.
  - Train has 20. Every train root cause is `PetSearch_AWS::ECS::Fargate`.
  - The test root causes are four other services: payforadoption, petInfo DynamoDB table, lambdastatusupdater and petlistadoptions.
  - The paper says the split is "according to the microservice they originated from".
  - The target is always `PetSite` with the `Average` statistic.
- **Authors' evaluation protocol (code, `rca_task.evaluate`).**
  - `split=None` evaluates train and test pooled. Passing a split would crash, because `splits` is undefined.
  - The normal period is the whole `noissue` file.
  - Top-k recall: the true node is in the top k after sorting by score. Node-only matching applies, since the root-cause metric is null.
  - An empty output is a miss.
  - The notebook's issue counts confirm the pooling: 14+12 = 26 = 8 train + 18 test.
- **Anomaly detection (`data_preprocessing.py`).**
  - A dowhy `MedianDeviationScorer` is fitted per service on the normal period. Its scale is `statsmodels.robust.mad`, i.e. MAD/0.6745; we read this in the dowhy 0.9.1 wheel, sha256 `0e816b71…434f`.
  - A service is anomalous when its score exceeds 5.
  - Zero-variance services use |x - mean| with a threshold of 0. Services with fewer than 10 points get no detector.
  - The analysed row is the third row of the issue window, or the first later row where the target is anomalous. If the target is not anomalous, the output is empty.
- **Traversal (`baseline_anomaly_traversal.py`).**
  - The causal graph is the call graph reversed (callee -> caller).
  - Root-cause candidates are anomalous nodes with no anomalous parent.
  - Candidates are kept only if an all-anomalous path leads to the target. The score is the maximum over such paths of the sum of node scores.
- **Published numbers.**
  - Table 3 of the paper (top-3, arXiv 2311.04806v2 HTML) is reproduced in section 4.
  - The notebook outputs give traversal top-1/top-3 and specificity per scenario group and metric.
  - We could not read Table 8 (top-1 for all methods) or the paper's specificity tables. The HTML text stops in Appendix C.1, and the PMLR and arXiv PDFs are blocked by this session's proxy.

## 2. Protocol (frozen in `ab12_prereg.json` before test results)

- **Primary split: test (48 issues).** Train (20) is used only to tune the abstention threshold. Pooled train+test is
  reported only to compare with the authors' published numbers.
- **AC@k** is the expected top-k hit of the single true node under a uniform random order within score ties, written
  `clamp((k - a)/g, 0, 1)`. **Avg@5** is the mean of AC@1..5.
  - Ties are common: availability services with MAD 0 score infinity.
  - The authors break ties in Python set/hash order, which depends on `PYTHONHASHSEED` and so is not reproducible.
  - Our tie-aware metric uses neither names nor column order.
  - A name-ascending tie-break is used only to show per-issue ranks and in the reproduction check.
- **Methods.** All are reimplemented line by line from the authors' code; dowhy, PyRCA and javabridge are not installed.

| id | method | regime | what it uses |
|---|---|---|---|
| a | `ranked_correlation`: authors' defaults (Pearson on the 5 abnormal rows, rank by p-value, MAD>5 filter, top-3 output) | D | metrics only |
| a2 | `mad_rank`: anomalous services ranked by MAD score at the analysed row (robust z, BARO-like, **not** BARO) | D | metrics only |
| b | `learned_traversal`: authors' traversal on a PC graph (causal-learn 0.1.4.8, Fisher-z, alpha 0.05, stable, uc_rule 0, uc_priority 2) learned per scenario x target metric from the normal period. Undirected edges count both ways. Constant or sparse series are excluded from PC and become isolated nodes | D | metrics only |
| b_rand | as b, with undirected edges oriented at random (seeded) | D | sensitivity |
| b_lat | as b, but the latency-learned graph is used for availability issues too. **Post hoc**, added after seeing that 28-33 availability series are constant in the normal period | D | sensitivity |
| c | `declared_traversal`: authors' baseline on the reversed `graph.csv` | D+K | call graph |
| d | c + abstention | D+K | call graph |
| e | a + abstention, same rule shape | D | metrics only |
| b+abst | b + abstention (extra row) | D | metrics only |

**Abstention rule (fixed beforehand).** The method abstains if it has no candidate, or if it has 4 or more candidates and
the relative margin between the 3rd and 4th scores is at most tau. In other words, it abstains when the scores do not
determine the top-3 set. tau is chosen from {0, .01, .02, .05, .1, .2, .5} on train only, to maximise AC@3 on answered
issues subject to coverage >= 0.5, with the smallest tau winning ties. On train every tau gave the same result
(coverage 0.8, AC@3 answered 0.94 for d and 1.00 for e), so tau = 0 for every method. **In effect, the rule is
"abstain when the output is empty or the 3rd and 4th scores tie exactly."** Train cannot tune it any further, because
all 20 train issues share one root cause.

**P15 operationalisation (fixed beforehand).**
- **Primary:** AC@3 of d on answered test issues minus AC@3 of b over all test issues. This counts only if d's coverage is at least 0.5.
- **Strict:** the same, with d's abstentions counted as misses.
- **Thresholds:** a gap of 0.10 or more supports P15; under 0.03 refutes it.
- **Uncertainty:** a paired bootstrap over test issues (2000 resamples, seed 20261012).

## 3. Results on the test split (measured)

| | method | regime | AC@1 | AC@3 | Avg@5 | coverage | AC@3, abstain = miss |
|---|---|---|---|---|---|---|---|
| a | ranked correlation (authors') | D | 0.653 | 0.799 | 0.761 | 1.00 | 0.799 |
| a2 | MAD-score ranking | D | 0.285 | 0.507 | 0.517 | 1.00 | 0.507 |
| b | **PC graph + traversal** | D | 0.208 | **0.208** | 0.208 | 1.00 (52% empty) | 0.208 |
| b_rand | PC, random orientation | D | 0.229 | 0.229 | 0.229 | 1.00 | 0.229 |
| b_lat | PC latency graph for both metrics (post hoc) | D | 0.396 | 0.396 | 0.396 | 1.00 | 0.396 |
| c | **declared call graph + traversal** | D+K | 0.689 | **0.901** | 0.848 | 1.00 | 0.901 |
| d | **c + abstention** | D+K | 0.735 | **0.932** | 0.877 | 0.917 (44/48) | 0.854 |
| e | a + abstention | D | 0.682 | 0.814 | 0.781 | 0.896 (43/48) | 0.729 |
| b+abst | b + abstention | D | 0.435 | 0.435 | 0.435 | 0.479 (23/48) | 0.208 |

For d, e and b+abst, AC@1, AC@3 and Avg@5 are on answered issues.

Test AC@3 by scenario group and metric (n per cell in brackets):

| | low lat (10) | low avail (8) | high lat (10) | high avail (8) | temporal lat (6) | temporal avail (6) |
|---|---|---|---|---|---|---|
| a ranked correlation | 0.60 | 0.96 | 0.90 | 0.96 | 0.67 | 0.67 |
| a2 MAD ranking | 0.70 | 1.00 | 0.00 | 0.25 | 0.67 | 0.56 |
| b PC traversal | 0.40 | 0.00 | 0.40 | 0.00 | 0.33 | 0.00 |
| b_lat (post hoc) | 0.40 | 0.25 | 0.40 | 0.62 | 0.33 | 0.33 |
| c declared traversal | 0.70 | 1.00 | 0.90 | 0.91 | 1.00 | 1.00 |

**Why each method misses (measured; test outcome classes, 48 issues each).**
- In every case the true root cause *was* flagged anomalous. The target was not anomalous in 1 issue (low_traffic issue_5), so every method returns nothing there.
- Misses therefore come from topology or ranking, never from detection.

| method | hit@3 | tie straddles rank 3 | true cause has an anomalous parent in the graph | no all-anomalous path to target | ranked below 3 |
|---|---|---|---|---|---|
| c declared | 41 | 3 | 3 | 0 | 0 |
| b PC | 10 | 0 | 11 | 26 | 0 |
| b_lat | 19 | 0 | 19 | 9 | 0 |
| a ranked correlation | 37 | 2 | n/a | n/a | 8 |

- **Availability is where the learned graph fails structurally.**
  - In the normal period, 28 of 41 (low), 32 of 39 (high) and 28 of 41 (temporal) availability series are constant.
  - PC cannot test a constant series, so those services are isolated in the learned graph and no path reaches PetSite. b scores 0.00 on all 22 availability issues.
  - The post hoc b_lat borrows the latency graph and recovers to 0.25-0.62 there. It is still far below the declared graph.

**Abstention on the no-issue period (measured; authors' `evaluate_specificity` windows).**
- Our declared traversal reproduces the notebook's specificity exactly: 0.167 / 1.000 / 0.333 / 1.000 / 0.600 / 1.000 for low lat, low avail, high lat, high avail, temporal lat and temporal avail.
- **The abstention rule adds nothing here.** The share of no-issue windows where d stays silent equals c's in every cell.
- All silence comes from the target-not-anomalous gate. On latency, 40-83% of windows still yield a fabricated root cause.

## 4. Reproduction of the authors' numbers (measured, train+test pooled as in their notebook)

| group, metric | traversal top-3, ours | Table 3 | traversal top-1, ours (name tie-break) | notebook top-1 | empty, ours / notebook | ranked correlation top-3, ours (name tie-break / tie-aware) | Table 3 |
|---|---|---|---|---|---|---|---|
| low, latency | 0.571 | 0.57 | 0.571 | 0.571 | 0.21 / 0.21 | 0.571 / 0.571 | 0.57 |
| low, availability | 1.000 | 1.00 | 0.833 | 0.833 | 0 / 0 | 0.917 / 0.972 | 0.92 |
| high, latency | 0.786 | 0.79 | 0.571 | 0.571 | 0.14 / 0.14 | 0.786 / 0.786 | 0.79 |
| high, availability | 1.000 | 1.00 | 0.667 | 0.667 | 0 / 0 | 0.917 / 0.972 | 0.92 |
| temporal, latency | 1.000 | 1.00 | 1.000 | 1.000 | 0 / 0 | 0.750 / 0.750 | 0.75 |
| temporal, availability | 1.000 | 1.00 | 0.750 | 0.750 | 0 / 0 | 0.750 / 0.750 | 0.75 |

**Both of the authors' methods we could run reproduce exactly in every cell.**
- This holds for traversal top-1, top-3, empty fraction and specificity, and for ranked correlation top-3 under the name tie-break.
- Under the tie-aware metric, traversal top-1 on availability is lower: 0.68 / 0.38 / 0.58 instead of 0.83 / 0.67 / 0.75. **The published top-1 availability numbers therefore depend on how ties are broken.** Several services score infinity, and the authors' order is hash-seeded.
- ε-diagnosis, CIRCA, RCD and counterfactual attribution were not rerun, because they need PyRCA, javabridge or dowhy. Their Table 3 numbers are listed in the JSON; for example, ε-diagnosis top-3 is 0.00-0.33.

## 5. P15 verdict (measured)

**SUPPORTED.**

| | d | b | gap | bootstrap 95% CI |
|---|---|---|---|---|
| primary: AC@3 of d on answered issues vs b | 0.932 (coverage 0.917) | 0.208 | **+0.723** | [0.55, 0.88] |
| strict: d with abstentions as misses vs b | 0.854 | 0.208 | **+0.646** | [0.46, 0.79] |

Both gaps clear 0.10 by a wide margin, and both CIs exclude 0.03.

**How the gap divides (interpretation of measured numbers).** Almost all of it comes from the topology, not the abstention:
- c - b = +0.693
- d (answered) - c = +0.031
- The strict d (0.854) is *below* c (0.901). The 3 tie abstentions give up partial credit that c's tie-aware score kept.

**The gap does not rest on the availability artefact alone.**
- On latency issues only, d answered 0.88 against b 0.38: gap +0.50.
- Against the post hoc b_lat, which avoids the artefact, the gap is +0.54 (primary) and +0.46 (strict).

**Declared topology also beats the best graph-free baseline, by less.** c 0.901 vs a 0.799 is +0.10. With abstention on both, d 0.932 vs e 0.814.

**The learned graph is the worst of the three families.** It loses to plain ranked correlation (0.208 vs 0.799). This is the same direction as RCAEval's PC-PageRank vs BARO result.

**The P15 wording overstates abstention's share.** The data support "declared topology beats a learned graph". They do not support "abstention adds 0.1"; abstention adds 0.03 on answered cases and nothing on the no-issue period.

## 6. Column order (task 3; measured)

One seeded permutation of metric columns per scenario (`default_rng([20261012, scenario_index])`), applied to the
normal and issue files alike:

| method | test AC@3, released order | test AC@3, shuffled | issues with a different candidate set or scores (of 68) | issues whose hits changed |
|---|---|---|---|---|
| a ranked correlation | 0.799 | 0.799 | 0 | 0 |
| c declared traversal | 0.901 | 0.901 | 0 | 0 |
| b PC traversal | 0.208 | 0.188 | 6 | 1 |
| b_rand | 0.229 | 0.208 | 5 | 1 |
| b_lat (post hoc) | 0.396 | 0.396 | 12 | 4 (they cancel) |

- **Declared-topology and graph-free RCA are invariant to column order by construction, and confirmed here.**
- **PC is not invariant.**
  - Stable PC gives the identical skeleton in all 8 graphs.
  - Orientations change. In temporal1 latency only 28 of 46 directed edges are shared between the two orders; in low latency 24 of 32 are, and 2 of 10 undirected edges.
  - This is the same PC orientation-order dependence we measured on CausalArena: same skeleton, different arrows.
  - The RCA effect is small here (one issue) only because the learned graph rarely connects the true cause to the target anyway.

**Names are not applicable to this probe.**
- No method here reads service names. The primary metric does not even use them to break ties.
- Name dependence matters only for LLM tools that read `payforadoption_AWS::ECS::Container` and similar names.
- AB-06 can test that on these same 68 incidents: real, neutral and swapped service names, with the declared graph and anomaly scores held fixed.

## 7. What a claim ledger adds in RCA (interpretation, grounded in the outcome classes above)

**Each ranked answer "X caused PetSite's SLO breach" is a conjunction of sub-claims with different sources.**

| sub-claim | source tag | what the ledger records |
|---|---|---|
| X is anomalous at the analysed row | **anomaly score** (D: MAD vs the normal period) | score and threshold. Infinite when the normal-period MAD is 0, which should itself be flagged as a weak test |
| no parent of X is anomalous | **topology declared** (K: X-Ray call graph) or **topology learned** (D: a PC edge, typed directed / undirected / orientation order-dependent) | which edge excluded or admitted X, and its provenance |
| an all-anomalous path X -> target exists | same as above | the path, edge by edge |
| rank | **anomaly score** (path sum) | the score and whether it ties across the top-k boundary |
| "cannot tell" | **abstention** | the reason, typed: target not anomalous / no candidate / top-3 not separated |

**What the ledger would have shown on this test set.**
- **b's 26 "no path" misses would carry a typed source.** 20 of them are availability issues and trace to edges that are *absent because the series was untestable*: constant in the normal period and excluded from PC. That is a typed gap ("not identifiable from normal-period data"), not a tested independence. Today the learned-graph pipeline reports the two identically, as an empty answer.
- **b's 11 "anomalous parent" misses trace to specific learned edges.** Some are undirected edges counted both ways; some are orientations that change when the columns are shuffled. Both are flaggable per claim.
- **c's 3 "anomalous parent" misses trace to one declared caller -> callee edge each.** A reviewer can check that edge against the architecture. A learned edge offers nothing comparable to check.
- **Abstention stated per claim makes the residual failure visible.** The current rule never fires on the no-issue period, so the 40-83% fabricated latency answers there are an open item, not a solved one. The ledger would show that every one of those answers rests on a single anomaly-score sub-claim with no corroborating path.

**For the product angle (C2):**
- In RCA the decision-relevant graph is declared, not learned.
- The value we can add is provenance per sub-claim plus typed abstention, not better structure learning.
- This matches what AU0 inferred from the vendor survey.

## 8. Deviations and limitations (stated plainly)

- **Reimplementation, not the authors' runtime.**
  - dowhy, PyRCA and javabridge are not installed. Anomaly scoring, traversal and ranked correlation are reimplemented from their code and the dowhy 0.9.1 source.
  - The match is exact on every published or notebook cell we can compare, under a name tie-break. Their own tie order is hash-seeded and not reproducible.
- **Tie handling.** The primary metric is tie-aware, which the authors did not use. On availability, top-1 differs materially from the published values (section 4).
- **Split.**
  - The authors pool train and test. We score test and tune on train.
  - Train has a single root-cause service, so the tau tuning was degenerate: every tau gave identical train results, and tau = 0 was taken by the tie rule.
- **Small n.**
  - There are 48 test issues, 4 distinct root-cause services, and one target (`PetSite`).
  - The CIs in section 5 are over issues and do not cover service-level variation.
- **The learned-graph arm is one reasonable pipeline, not the best possible.**
  - It uses PC on the normal period, one metric, and the authors' traversal.
  - We did not run PC on pooled normal and abnormal data, multi-metric graphs, PageRank or random-walk scoring, CIRCA, or RCD.
  - The availability collapse is partly a property of this pipeline. The post hoc b_lat row bounds that effect, and P15 holds against it.
- **Regime labels.**
  - "D+K" for the declared graph follows the project convention: topology is given to the method, not learned from these metrics.
  - The X-Ray graph is itself derived from trace data, so "declared" here means "from a different data source the operator already has".
  - The paper notes it is a service map, not a causal graph; reversing it is the authors' heuristic.
- **Acyclicity check skipped on learned graphs.** The authors' traversal raises an error when the anomalous subgraph is cyclic. On learned graphs we skip that check, because undirected edges counted both ways form 2-cycles; this was flagged on 62 learned-graph issue runs. On the declared graph the check is kept and never fired.
- **Paper tables not read.** Table 8 (top-1 for all methods) and the specificity tables were not readable from this session. Only Table 3 and the notebook outputs were compared.

## 9. Where we're going

- **AB-06** can reuse these 68 incidents for the names arm: real, neutral and swapped service names, with the declared graph and anomaly scores fixed. That isolates what an LLM RCA tool takes from names.
- **The abstention rule needs a second, normal-period-aware condition.** Candidates are a score floor on the target, or anomaly persistence over 2+ rows. It should be fixed on train plus the first half of `noissue` and scored on the rest. Today's rule is a typed gap: it does not reduce fabricated causes during normal operation.
- **RCAEval RE1-OB is the planned second slice** (AB02 scouting). It has a published PC-PageRank vs BARO comparison and needs its topology written from the Online Boutique architecture.
- **The claim-ledger fields in section 7** (source tag per sub-claim, typed abstention reason, untestable-edge flag) are the concrete schema input from this bundle to BLD and STR-06.
