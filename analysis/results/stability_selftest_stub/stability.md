# Stability and name-versus-data report

Label `selftest` (STUB LLM: tool self-test, answers carry no meaning). Runs directory `/sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/ccr-dev/runs`. 6 runs included in 3 arms; 1 excluded.

## Excluded runs

| Run | Arm | Reason |
|---|---|---|
| 20261006T061556Z_selftest_20241024_145159_Linear-Non-gaussian_id_0_nodes10_samples1000_STUB_4e31d8 | 20241024_145159_Linear-Non-gaussian_id_0_nodes10_samples1000 | status FAILED |

## Arm `d02` (3 runs)

Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11. Path contains "sachs": no.

**Choices.** Algorithm: PC ×3. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×3. Proposed by the LLM but not passed: [] ×3. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 2 | 2 |
| 06a_filter | 1 | 1 | 1 | 1 |
| 06b_rerank | 1 | 1 | 1 | 1 |
| 06c_hyperparameters | 1 | 1 | 1 | 1 |
| 07b_refinement | 11 | 11 | 11 | 11 |
| 08a_report_graph_text | 1 | 1 | 1 | 1 |
| 08b_report | 5 | 5 | 5 | 5 |
| 09_discussion_init | 1 | 1 | 1 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): never (25 calls) ×3.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 3 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 8.0 ± 0.0 | 1.00 | 1.00 |
| S1 after bootstrap edits | 4.0 ± 0.0 | 1.00 | 1.00 |
| S2 after LLM review | 21.0 ± 0.0 | 1.00 | 1.00 |
| S3 after KCI pruning | 17.0 ± 0.0 | 1.00 | 1.00 |
| S4 final (after cycle step) | 17.0 ± 0.0 | 1.00 | 1.00 |

**LLM review decisions.** 55 pairs. Same decision in every run: 55. Same edge/no-edge call in every run: 55. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 42, B 18, C 39, D 66.

**Final edges.** 17 distinct edges appear in at least one run; 17 appear in every run. Set by: llm 48, algorithm (unchanged) 3. Per run: LLM-set edges 16.0 ± 0.0; final edges between pairs the algorithm did not connect 13.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 12.0 ± 0.0.

| Final edge | Runs (of 3) |
|---|---|
| V02->V01 | 3 |
| V01->V06 | 3 |
| V01->V10 | 3 |
| V01->V11 | 3 |
| V02->V04 | 3 |
| V02->V11 | 3 |
| V03->V04 | 3 |
| V05->V03 | 3 |
| V03->V06 | 3 |
| V04->V06 | 3 |
| V04->V08 | 3 |
| V05->V07 | 3 |
| V05->V11 | 3 |
| V06->V11 | 3 |
| V07->V08 | 3 |
| V08->V11 | 3 |
| V10->V09 | 3 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 1.00 ± 0.00 | 0.42 ± 0.00 | 0.59 ± 0.00 | 0.0 ± 0.0 | 2.0 ± 0.0 | 17.0 ± 0.0 |
| S1 after bootstrap edits | 1.00 ± 0.00 | 0.21 ± 0.00 | 0.35 ± 0.00 | 0.0 ± 0.0 | 2.0 ± 0.0 | 18.0 ± 0.0 |
| S2 after LLM review | 0.43 ± 0.00 | 0.47 ± 0.00 | 0.45 ± 0.00 | 5.0 ± 0.0 | 4.0 ± 0.0 | 30.0 ± 0.0 |
| S3 after KCI pruning | 0.41 ± 0.00 | 0.37 ± 0.00 | 0.39 ± 0.00 | 4.0 ± 0.0 | 3.0 ± 0.0 | 28.0 ± 0.0 |
| S4 final (after cycle step) | 0.41 ± 0.00 | 0.37 ± 0.00 | 0.39 ± 0.00 | 4.0 ± 0.0 | 3.0 ± 0.0 | 28.0 ± 0.0 |

## Arm `d03` (2 runs)

Column labels: Mek, Plcg, PIP2, Raf, PKA, P38, PIP3, Erk, Akt, Jnk, PKC. Path contains "sachs": no.

**Choices.** Algorithm: PC ×2. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×2. Proposed by the LLM but not passed: [] ×2. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 2 | 2 |
| 06a_filter | 1 | 1 | 1 | 1 |
| 06b_rerank | 1 | 1 | 1 | 1 |
| 06c_hyperparameters | 1 | 1 | 1 | 1 |
| 07b_refinement | 11 | 11 | 11 | 11 |
| 08a_report_graph_text | 1 | 1 | 1 | 1 |
| 08b_report | 5 | 5 | 5 | 5 |
| 09_discussion_init | 1 | 1 | 1 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): never (25 calls) ×1.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 2 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 8.0 ± 0.0 | 1.00 | 1.00 |
| S1 after bootstrap edits | 4.0 ± 0.0 | 1.00 | 1.00 |
| S2 after LLM review | 21.0 ± 0.0 | 1.00 | 1.00 |
| S3 after KCI pruning | 17.0 ± 0.0 | 1.00 | 1.00 |
| S4 final (after cycle step) | 17.0 ± 0.0 | 1.00 | 1.00 |

**LLM review decisions.** 55 pairs. Same decision in every run: 55. Same edge/no-edge call in every run: 55. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 28, B 12, C 26, D 44.

**Final edges.** 17 distinct edges appear in at least one run; 17 appear in every run. Set by: llm 32, algorithm (unchanged) 2. Per run: LLM-set edges 16.0 ± 0.0; final edges between pairs the algorithm did not connect 13.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 12.0 ± 0.0.

| Final edge | Runs (of 2) |
|---|---|
| Plcg->Mek | 2 |
| Mek->P38 | 2 |
| Mek->Jnk | 2 |
| Mek->PKC | 2 |
| Plcg->Raf | 2 |
| Plcg->PKC | 2 |
| PIP2->Raf | 2 |
| PKA->PIP2 | 2 |
| PIP2->P38 | 2 |
| Raf->P38 | 2 |
| Raf->Erk | 2 |
| PKA->PIP3 | 2 |
| PKA->PKC | 2 |
| P38->PKC | 2 |
| PIP3->Erk | 2 |
| Erk->PKC | 2 |
| Jnk->Akt | 2 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 1.00 ± 0.00 | 0.42 ± 0.00 | 0.59 ± 0.00 | 0.0 ± 0.0 | 2.0 ± 0.0 | 17.0 ± 0.0 |
| S1 after bootstrap edits | 1.00 ± 0.00 | 0.21 ± 0.00 | 0.35 ± 0.00 | 0.0 ± 0.0 | 2.0 ± 0.0 | 18.0 ± 0.0 |
| S2 after LLM review | 0.43 ± 0.00 | 0.47 ± 0.00 | 0.45 ± 0.00 | 5.0 ± 0.0 | 4.0 ± 0.0 | 30.0 ± 0.0 |
| S3 after KCI pruning | 0.41 ± 0.00 | 0.37 ± 0.00 | 0.39 ± 0.00 | 4.0 ± 0.0 | 3.0 ± 0.0 | 28.0 ± 0.0 |
| S4 final (after cycle step) | 0.41 ± 0.00 | 0.37 ± 0.00 | 0.39 ± 0.00 | 4.0 ± 0.0 | 3.0 ± 0.0 | 28.0 ± 0.0 |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 27.0 ± 0.0 |
| S1 after bootstrap edits | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 23.0 ± 0.0 |
| S2 after LLM review | 0.29 ± 0.00 | 0.32 ± 0.00 | 0.30 ± 0.00 | 1.0 ± 0.0 | 5.0 ± 0.0 | 34.0 ± 0.0 |
| S3 after KCI pruning | 0.24 ± 0.00 | 0.21 ± 0.00 | 0.22 ± 0.00 | 1.0 ± 0.0 | 3.0 ± 0.0 | 32.0 ± 0.0 |
| S4 final (after cycle step) | 0.24 ± 0.00 | 0.21 ± 0.00 | 0.22 ± 0.00 | 1.0 ± 0.0 | 3.0 ± 0.0 | 32.0 ± 0.0 |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 8 |
| data only | 12 |
| both | 0 |
| neither | 12 |

Direction among those: data: direction as in reference 8, data: reversed 4, labels: direction as in reference 2, labels: reversed 6.

## Arm `20241024_145159_Linear-Non-gaussian_id_0_nodes10_samples1000` (1 runs)

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 11 | 0 | 0 | 11 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 11.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 9.0 (1 run) | n/a | n/a |
| S2 after LLM review | 20.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 17.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 16.0 (1 run) | n/a | n/a |

**LLM review decisions.** 45 pairs. Same decision in every run: 45. Same edge/no-edge call in every run: 45. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 11, B 6, C 9, D 19.

**Final edges.** 16 distinct edges appear in at least one run; 16 appear in every run. Set by: llm 10, algorithm (unchanged) 6. Per run: LLM-set edges 10.0 (1 run); final edges between pairs the algorithm did not connect 10.0 (1 run); LLM additions where at least 90% of resamples had no edge 12.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| X0->X3 | 1 |
| X0->X5 | 1 |
| X2->X1 | 1 |
| X1->X7 | 1 |
| X1->X6 | 1 |
| X2->X3 | 1 |
| X2->X6 | 1 |
| X2->X8 | 1 |
| X7->X6 | 1 |
| X7->X9 | 1 |
| X4->X5 | 1 |
| X9->X4 | 1 |
| X3->X5 | 1 |
| X3 --- X9 | 1 |
| X8->X5 | 1 |
| X6->X8 | 1 |

**Accuracy by stage, scored against the ground truth** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 0.27 (1 run) | 0.33 (1 run) | 0.30 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 16.0 (1 run) |
| S1 after bootstrap edits | 0.11 (1 run) | 0.11 (1 run) | 0.11 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 17.0 (1 run) |
| S2 after LLM review | 0.10 (1 run) | 0.22 (1 run) | 0.14 (1 run) | 1.0 (1 run) | 1.0 (1 run) | 27.0 (1 run) |
| S3 after KCI pruning | 0.06 (1 run) | 0.11 (1 run) | 0.08 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 25.0 (1 run) |
| S4 final (after cycle step) | 0.06 (1 run) | 0.11 (1 run) | 0.08 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 24.0 (1 run) |

## Predictions fixed before the data

- **P1**: {"labels_only": 8, "data_only": 12, "share_following_labels": 0.4, "verdict": "REFUTED"}
- **P3**: {"distinct_outputs_counted": 2, "nondirected_edges_in_algorithm_output": 9, "of_which_still_adjacent_after_bootstrap_step": 3, "share": 0.3333333333333333, "directed_edges": 10, "directed_still_adjacent": 10, "verdict": "INCONCLUSIVE"}
- **P5**: {"arms": 3, "arms_with_more_than_one_algorithm": 0, "verdict": "exploratory"}

## Gates

- T1_no_arm_left_empty: **PASS**
- T2_min_runs_per_arm: **FAIL**
- T3_same_dataset_bytes: **PASS**
- T4_variable_names_match_arm: **PASS**
- T5_scores_recomputed_equal_lineage: **PASS**
- T6_one_model_snapshot_per_arm (report only): **PASS**

This is a STUB self-test: the numbers above show that the tool runs and its checks behave as expected. They say nothing about Causal-Copilot's behaviour with a real model.
