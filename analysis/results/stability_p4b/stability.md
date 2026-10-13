# Stability and name-versus-data report

Label `p4b`. Runs directory `/sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/mnt/DSC 180A/cc-research/runs`. 25 runs included in 6 arms; 3 excluded.

## Excluded runs

| Run | Arm | Reason |
|---|---|---|
| 20261006T134450Z_p4b_sachs_r01_feb9cc | sachs | status FAILED |
| 20261006T134554Z_p4b_d01_r01_f9955f | d01 | status FAILED |
| 20261006T140411Z_p4b_d01_r02_5f5104 | d01 | status FAILED |

## Arm `sachs` (4 runs)

Column labels: Raf, Mek, Plcg, PIP2, PIP3, Erk, Akt, PKA, PKC, P38, Jnk. Path contains "sachs": yes.

**Choices.** Algorithm: FCI ×4. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×4. Proposed by the LLM but not passed: ["background_knowledge"] ×4. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 0 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 4 | 0 | 0 | 0 |
| 06b_rerank | 4 | 0 | 0 | 0 |
| 06c_hyperparameters | 4 | 0 | 0 | 0 |
| 07b_refinement | 44 | 0 | 0 | 0 |
| 08a_report_graph_text | 3 | 1 | 0 | 0 |
| 08b_report | 14 | 2 | 1 | 2 |
| 09_discussion_init | 4 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×6.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 4.

**Graph by stage.** 3 distinct algorithm outputs (S0) across 4 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 9.5 ± 0.6 | 0.90 | 0.90 |
| S1 after bootstrap edits | 1.8 ± 0.5 | 0.53 | 0.53 |
| S2 after LLM review | 7.2 ± 1.0 | 0.67 | 0.67 |
| S3 after KCI pruning | 7.2 ± 1.0 | 0.67 | 0.67 |
| S4 final (after cycle step) | 7.2 ± 1.0 | 0.67 | 0.67 |

**LLM review decisions.** 55 pairs. Same decision in every run: 33. Same edge/no-edge call in every run: 50. Mean share of runs agreeing with the commonest decision for a pair: 0.84. Letters over all runs: A 27, C 140, D 53.

**Final edges.** 10 distinct edges appear in at least one run; 4 appear in every run. Set by: llm 27, algorithm (unchanged) 2. Per run: LLM-set edges 6.8 ± 0.5; final edges between pairs the algorithm did not connect 2.5 ± 0.6; LLM additions where at least 90% of resamples had no edge 2.2 ± 0.5.

| Final edge | Runs (of 4) |
|---|---|
| Raf->Mek | 4 |
| Mek->Erk | 4 |
| PIP2->PIP3 | 4 |
| PIP3->Akt | 4 |
| Plcg->PIP3 | 3 |
| PKC->P38 | 3 |
| PKC->Jnk | 3 |
| Erk o-o PKA | 2 |
| Raf->Erk | 1 |
| Plcg->PIP2 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 0.92 ± 0.05 | 0.46 ± 0.03 | 0.61 ± 0.03 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.8 ± 0.5 |
| S1 after bootstrap edits | 1.00 ± 0.00 | 0.09 ± 0.03 | 0.17 ± 0.05 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.0 ± 0.0 |
| S2 after LLM review | 0.96 ± 0.08 | 0.37 ± 0.07 | 0.53 ± 0.09 | 4.8 ± 0.5 | 1.8 ± 0.5 | 16.2 ± 0.5 |
| S3 after KCI pruning | 0.96 ± 0.08 | 0.37 ± 0.07 | 0.53 ± 0.09 | 4.8 ± 0.5 | 1.8 ± 0.5 | 16.2 ± 0.5 |
| S4 final (after cycle step) | 0.96 ± 0.08 | 0.37 ± 0.07 | 0.53 ± 0.09 | 4.8 ± 0.5 | 1.8 ± 0.5 | 16.2 ± 0.5 |

## Arm `d01` (3 runs)

Column labels: Raf, Mek, Plcg, PIP2, PIP3, Erk, Akt, PKA, PKC, P38, Jnk. Path contains "sachs": no.

**Choices.** Algorithm: FCI ×3. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×3. Proposed by the LLM but not passed: ["background_knowledge"] ×3. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 0 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 3 | 0 | 0 | 0 |
| 06b_rerank | 3 | 0 | 0 | 0 |
| 06c_hyperparameters | 3 | 0 | 0 | 0 |
| 07b_refinement | 33 | 0 | 0 | 0 |
| 08a_report_graph_text | 2 | 1 | 0 | 0 |
| 08b_report | 11 | 2 | 1 | 2 |
| 09_discussion_init | 3 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×3.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 3.

**Graph by stage.** 2 distinct algorithm outputs (S0) across 3 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 9.7 ± 0.6 | 0.93 | 0.72 |
| S1 after bootstrap edits | 2.0 ± 0.0 | 0.56 | 0.56 |
| S2 after LLM review | 6.7 ± 1.2 | 0.56 | 0.56 |
| S3 after KCI pruning | 6.7 ± 1.2 | 0.56 | 0.56 |
| S4 final (after cycle step) | 6.7 ± 1.2 | 0.56 | 0.56 |

**LLM review decisions.** 55 pairs. Same decision in every run: 35. Same edge/no-edge call in every run: 50. Mean share of runs agreeing with the commonest decision for a pair: 0.87. Letters over all runs: A 19, C 116, D 30.

**Final edges.** 10 distinct edges appear in at least one run; 4 appear in every run. Set by: llm 19, algorithm (unchanged) 1. Per run: LLM-set edges 6.3 ± 0.6; final edges between pairs the algorithm did not connect 3.3 ± 0.6; LLM additions where at least 90% of resamples had no edge 3.0 ± 1.0.

| Final edge | Runs (of 3) |
|---|---|
| Raf->Mek | 3 |
| Mek->Erk | 3 |
| Plcg->PIP2 | 3 |
| PIP3->Akt | 3 |
| PIP2->PIP3 | 2 |
| P38->Jnk | 2 |
| Erk->P38 | 1 |
| Plcg->PKC | 1 |
| PIP2->PKC | 1 |
| Erk ~~~ Akt | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 0.93 ± 0.06 | 0.47 ± 0.00 | 0.63 ± 0.01 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.7 ± 0.6 |
| S1 after bootstrap edits | 1.00 ± 0.00 | 0.11 ± 0.00 | 0.19 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.0 ± 0.0 |
| S2 after LLM review | 0.85 ± 0.02 | 0.30 ± 0.06 | 0.44 ± 0.07 | 4.7 ± 1.2 | 0.7 ± 0.6 | 17.0 ± 0.0 |
| S3 after KCI pruning | 0.85 ± 0.02 | 0.30 ± 0.06 | 0.44 ± 0.07 | 4.7 ± 1.2 | 0.7 ± 0.6 | 17.0 ± 0.0 |
| S4 final (after cycle step) | 0.85 ± 0.02 | 0.30 ± 0.06 | 0.44 ± 0.07 | 4.7 ± 1.2 | 0.7 ± 0.6 | 17.0 ± 0.0 |

## Arm `d02` (5 runs)

Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11. Path contains "sachs": no.

**Choices.** Algorithm: FCI ×5. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×5. Proposed by the LLM but not passed: [] ×5. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 1 | 2 |
| 06a_filter | 1 | 1 | 0 | 1 |
| 06b_rerank | 2 | 2 | 0 | 0 |
| 06c_hyperparameters | 1 | 1 | 0 | 1 |
| 07b_refinement | 44 | 11 | 4 | 0 |
| 08a_report_graph_text | 2 | 1 | 0 | 0 |
| 08b_report | 17 | 2 | 1 | 2 |
| 09_discussion_init | 5 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06b_rerank ×6, 07b_refinement ×2, 08a_report_graph_text ×2.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 5.

**Graph by stage.** 2 distinct algorithm outputs (S0) across 5 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 10.0 ± 0.0 | 0.93 | 0.77 |
| S1 after bootstrap edits | 1.0 ± 0.7 | 0.20 | 0.10 |
| S2 after LLM review | 1.0 ± 0.7 | 0.20 | 0.10 |
| S3 after KCI pruning | 1.0 ± 0.7 | 0.20 | 0.10 |
| S4 final (after cycle step) | 1.0 ± 0.7 | 0.20 | 0.10 |

**LLM review decisions.** 55 pairs. Same decision in every run: 55. Same edge/no-edge call in every run: 55. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 275.

**Final edges.** 4 distinct edges appear in at least one run; 0 appear in every run. Set by: algorithm (unchanged) 5. Per run: LLM-set edges 0.0 ± 0.0; final edges between pairs the algorithm did not connect 0.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

| Final edge | Runs (of 5) |
|---|---|
| V04 o-o V05 | 2 |
| V03 o-> V05 | 1 |
| V04 o-> V05 | 1 |
| V07 o-o V08 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 0.90 ± 0.00 | 0.47 ± 0.00 | 0.62 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 20.0 ± 0.0 |
| S1 after bootstrap edits | 1.00 ± 0.00 | 0.05 ± 0.04 | 0.10 ± 0.07 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.0 ± 0.0 |
| S2 after LLM review | 1.00 ± 0.00 | 0.05 ± 0.04 | 0.10 ± 0.07 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.0 ± 0.0 |
| S3 after KCI pruning | 1.00 ± 0.00 | 0.05 ± 0.04 | 0.10 ± 0.07 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.0 ± 0.0 |
| S4 final (after cycle step) | 1.00 ± 0.00 | 0.05 ± 0.04 | 0.10 ± 0.07 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.0 ± 0.0 |

## Arm `d03` (5 runs)

Column labels: Mek, Plcg, PIP2, Raf, PKA, P38, PIP3, Erk, Akt, Jnk, PKC. Path contains "sachs": no.

**Choices.** Algorithm: FCI ×5. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×5. Proposed by the LLM but not passed: ["background_knowledge"] ×5. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 5 | 0 | 0 | 0 |
| 06b_rerank | 5 | 0 | 0 | 0 |
| 06c_hyperparameters | 5 | 0 | 0 | 0 |
| 07b_refinement | 55 | 0 | 0 | 0 |
| 08a_report_graph_text | 3 | 1 | 0 | 0 |
| 08b_report | 17 | 2 | 1 | 2 |
| 09_discussion_init | 5 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×10.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 5.

**Graph by stage.** 3 distinct algorithm outputs (S0) across 5 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 9.8 ± 1.1 | 0.89 | 0.73 |
| S1 after bootstrap edits | 1.2 ± 1.1 | 0.13 | 0.13 |
| S2 after LLM review | 8.2 ± 0.4 | 0.96 | 0.83 |
| S3 after KCI pruning | 7.6 ± 0.9 | 0.88 | 0.88 |
| S4 final (after cycle step) | 7.6 ± 0.9 | 0.88 | 0.88 |

**LLM review decisions.** 55 pairs. Same decision in every run: 41. Same edge/no-edge call in every run: 55. Mean share of runs agreeing with the commonest decision for a pair: 0.92. Letters over all runs: A 32, B 8, C 169, D 66.

**Final edges.** 9 distinct edges appear in at least one run; 7 appear in every run. Set by: llm 37, algorithm (unchanged) 1. Per run: LLM-set edges 7.4 ± 0.5; final edges between pairs the algorithm did not connect 7.2 ± 0.4; LLM additions where at least 90% of resamples had no edge 6.2 ± 0.4.

| Final edge | Runs (of 5) |
|---|---|
| Raf->Mek | 5 |
| Mek->Erk | 5 |
| Plcg->PIP2 | 5 |
| PIP2->PKC | 5 |
| Raf->Erk | 5 |
| P38->Jnk | 5 |
| PIP3->Akt | 5 |
| PIP2->PIP3 | 2 |
| PIP2 o-> Raf | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 0.88 ± 0.04 | 0.45 ± 0.05 | 0.60 ± 0.04 | 0.0 ± 0.0 | 0.0 ± 0.0 | 20.2 ± 0.4 |
| S1 after bootstrap edits | 1.00 ± 0.00 | 0.06 ± 0.06 | 0.11 ± 0.10 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.0 ± 0.0 |
| S2 after LLM review | 0.02 ± 0.05 | 0.01 ± 0.02 | 0.01 ± 0.03 | 0.0 ± 0.0 | 0.0 ± 0.0 | 27.0 ± 0.0 |
| S3 after KCI pruning | 0.02 ± 0.05 | 0.01 ± 0.02 | 0.01 ± 0.03 | 0.0 ± 0.0 | 0.0 ± 0.0 | 26.4 ± 0.5 |
| S4 final (after cycle step) | 0.02 ± 0.05 | 0.01 ± 0.02 | 0.01 ± 0.03 | 0.0 ± 0.0 | 0.0 ± 0.0 | 26.4 ± 0.5 |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 0.12 ± 0.04 | 0.06 ± 0.02 | 0.08 ± 0.03 | 0.0 ± 0.0 | 0.0 ± 0.0 | 27.6 ± 0.9 |
| S1 after bootstrap edits | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 20.2 ± 1.1 |
| S2 after LLM review | 0.73 ± 0.04 | 0.32 ± 0.00 | 0.44 ± 0.01 | 5.6 ± 0.5 | 0.4 ± 0.5 | 18.2 ± 0.4 |
| S3 after KCI pruning | 0.71 ± 0.03 | 0.28 ± 0.03 | 0.41 ± 0.03 | 5.0 ± 0.0 | 0.4 ± 0.5 | 18.2 ± 0.4 |
| S4 final (after cycle step) | 0.71 ± 0.03 | 0.28 ± 0.03 | 0.41 ± 0.03 | 5.0 ± 0.0 | 0.4 ± 0.5 | 18.2 ± 0.4 |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 27 |
| data only | 0 |
| both | 0 |
| neither | 10 |

Direction among those: labels: direction as in reference 25, labels: reversed 2.

## Arm `20241024_145159_Linear-Non-gaussian_id_0_nodes10_samples1000` (3 runs)

**Choices.** Algorithm: XGES ×3. Hyperparameters passed to it: {"alpha": 2} ×3. Proposed by the LLM but not passed: [] ×3. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 2 | 2 |
| 06a_filter | 1 | 1 | 0 | 1 |
| 06b_rerank | 2 | 1 | 0 | 0 |
| 06c_hyperparameters | 2 | 1 | 0 | 0 |
| 07b_refinement | 10 | 10 | 2 | 10 |
| 08a_report_graph_text | 1 | 1 | 0 | 1 |
| 08b_report | 7 | 4 | 0 | 4 |
| 09_discussion_init | 3 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06b_rerank ×2, 06c_hyperparameters ×1.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: XGES {"alpha": 2}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 3 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 9.0 ± 0.0 | 1.00 | 1.00 |
| S1 after bootstrap edits | 7.0 ± 0.0 | 1.00 | 1.00 |
| S2 after LLM review | 7.0 ± 0.0 | 1.00 | 1.00 |
| S3 after KCI pruning | 7.0 ± 0.0 | 1.00 | 1.00 |
| S4 final (after cycle step) | 7.0 ± 0.0 | 1.00 | 1.00 |

**LLM review decisions.** 45 pairs. Same decision in every run: 45. Same edge/no-edge call in every run: 45. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 135.

**Final edges.** 7 distinct edges appear in at least one run; 7 appear in every run. Set by: algorithm (unchanged) 21. Per run: LLM-set edges 0.0 ± 0.0; final edges between pairs the algorithm did not connect 0.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

| Final edge | Runs (of 3) |
|---|---|
| X0->X3 | 3 |
| X0->X9 | 3 |
| X1->X6 | 3 |
| X2->X3 | 3 |
| X2->X6 | 3 |
| X3->X9 | 3 |
| X6->X8 | 3 |

**Accuracy by stage, scored against the ground truth** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 0.33 ± 0.00 | 0.33 ± 0.00 | 0.33 ± 0.00 | 1.0 ± 0.0 | 0.0 ± 0.0 | 14.0 ± 0.0 |
| S1 after bootstrap edits | 0.14 ± 0.00 | 0.11 ± 0.00 | 0.12 ± 0.00 | 1.0 ± 0.0 | 0.0 ± 0.0 | 15.0 ± 0.0 |
| S2 after LLM review | 0.14 ± 0.00 | 0.11 ± 0.00 | 0.12 ± 0.00 | 1.0 ± 0.0 | 0.0 ± 0.0 | 15.0 ± 0.0 |
| S3 after KCI pruning | 0.14 ± 0.00 | 0.11 ± 0.00 | 0.12 ± 0.00 | 1.0 ± 0.0 | 0.0 ± 0.0 | 15.0 ± 0.0 |
| S4 final (after cycle step) | 0.14 ± 0.00 | 0.11 ± 0.00 | 0.12 ± 0.00 | 1.0 ± 0.0 | 0.0 ± 0.0 | 15.0 ± 0.0 |

## Arm `Linear_Gaussian` (5 runs)

**Choices.** Algorithm: XGES ×5. Hyperparameters passed to it: {"alpha": 2} ×5. Proposed by the LLM but not passed: [] ×5. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 2 | 2 |
| 06a_filter | 1 | 1 | 0 | 1 |
| 06b_rerank | 3 | 1 | 0 | 0 |
| 06c_hyperparameters | 2 | 2 | 0 | 0 |
| 07b_refinement | 5 | 5 | 0 | 5 |
| 08a_report_graph_text | 1 | 1 | 0 | 1 |
| 08b_report | 9 | 4 | 2 | 4 |
| 09_discussion_init | 5 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06b_rerank ×7, 06c_hyperparameters ×2, 08b_report ×1.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: XGES {"alpha": 2}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 5 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 1.0 ± 0.0 | 1.00 | 1.00 |
| S1 after bootstrap edits | 0.0 ± 0.0 | 1.00 | 1.00 |
| S2 after LLM review | 0.0 ± 0.0 | 1.00 | 1.00 |
| S3 after KCI pruning | 0.0 ± 0.0 | 1.00 | 1.00 |
| S4 final (after cycle step) | 0.0 ± 0.0 | 1.00 | 1.00 |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 50.

**Final edges.** 0 distinct edges appear in at least one run; 0 appear in every run. Set by: none. Per run: LLM-set edges 0.0 ± 0.0; final edges between pairs the algorithm did not connect 0.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

**Accuracy by stage, scored against the ground truth** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG |
|---|---|---|---|---|---|---|
| S0 algorithm output | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| S1 after bootstrap edits | n/a | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 1.0 ± 0.0 |
| S2 after LLM review | n/a | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 1.0 ± 0.0 |
| S3 after KCI pruning | n/a | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 1.0 ± 0.0 |
| S4 final (after cycle step) | n/a | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 1.0 ± 0.0 |

## Predictions fixed before the data

- **P1**: {"labels_only": 27, "data_only": 0, "share_following_labels": 1.0, "verdict": "SUPPORTED"}
- **P2**: {"d01_mean_llm_set_edges": 6.333333333333333, "d02_mean_llm_set_edges": 0, "verdict": "SUPPORTED"}
- **P3**: {"distinct_outputs_counted": 14, "nondirected_edges_in_algorithm_output": 119, "of_which_still_adjacent_after_bootstrap_step": 18, "share": 0.15126050420168066, "directed_edges": 7, "directed_still_adjacent": 7, "verdict": "SUPPORTED"}
- **P4**: {"sachs_mean_final_adj_f1": 0.5309116809116808, "d01_mean_final_adj_f1": 0.43950617283950616, "difference": 0.09140550807217468, "verdict": "exploratory"}
- **P5**: {"arms": 6, "arms_with_more_than_one_algorithm": 0, "verdict": "exploratory"}

## Gates

- T1_no_arm_left_empty: **PASS**
- T2_min_runs_per_arm: **PASS**
- T3_same_dataset_bytes: **PASS**
- T4_variable_names_match_arm: **PASS**
- T5_scores_recomputed_equal_lineage: **PASS**
- T6_one_model_snapshot_per_arm (report only): **PASS**
