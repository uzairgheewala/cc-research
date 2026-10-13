# Stability and name-versus-data report

Label `b1`. Runs directory `runs`. 45 runs included in 12 arms; 9 excluded.

## Excluded runs

| Run | Arm | Reason |
|---|---|---|
| 20261006T231745Z_b1_k13_r01_59427f | k13 | status FAILED |
| 20261006T233111Z_b1_k23_r01_51669a | k23 | status FAILED |
| 20261007T000047Z_b1_k43_r01_00df82 | k43 | status FAILED |
| 20261007T010127Z_b1_k33_r02_ce51b9 | k33 | status FAILED |
| 20261007T011030Z_b1_k11_r03_4e9a5e | k11 | status FAILED |
| 20261007T014315Z_b1_k31_r03_11d56f | k31 | status FAILED |
| 20261007T020711Z_b1_k11_r04_a25308 | k11 | status FAILED |
| 20261007T032700Z_b1_k43_r04_7b77db | k43 | status FAILED |
| 20261007T203354Z_b1_k43_r02_f14a7f | k43 | status FAILED |

## Arm `k11` (5 runs)

Family `abalone`, role `real`. Column labels: Age, Length, Shell weight, Diameter, Height, Whole weight, Shucked weight, Viscera weight. File path names the dataset: no.

**Choices.** Algorithm: FCI ×5. Hyperparameters passed to it: {"alpha": 0.05, "depth": 6, "indep_test": "rcit"} ×5. Proposed by the LLM but not passed: ["background_knowledge"] ×4; [] ×1. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 5 | 0 | 0 | 0 |
| 06b_rerank | 5 | 0 | 0 | 0 |
| 06c_hyperparameters | 5 | 0 | 0 | 0 |
| 07b_refinement | 40 | 0 | 0 | 0 |
| 08a_report_graph_text | 4 | 1 | 0 | 0 |
| 08b_report | 17 | 2 | 0 | 2 |
| 09_discussion_init | 5 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×10.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 6, "indep_test": "rcit"}: 5.

**Graph by stage.** 4 distinct algorithm outputs (S0) across 5 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 14.6 ± 0.5 | 0.90 | 0.50 |
| S1 after bootstrap edits | 5.0 ± 1.0 | 0.41 | 0.26 |
| S2 after LLM review | 19.6 ± 2.8 | 0.76 | 0.76 |
| S3 after KCI pruning | 19.6 ± 2.8 | 0.76 | 0.76 |
| S4 final (after cycle step) | 19.6 ± 2.8 | 0.76 | 0.76 |

**LLM review decisions.** 28 pairs. Same decision in every run: 14. Same edge/no-edge call in every run: 17. Mean share of runs agreeing with the commonest decision for a pair: 0.86. Letters over all runs: A 88, B 8, C 38, D 6.

**Final edges.** 25 distinct edges appear in at least one run; 13 appear in every run. Set by: llm 93, algorithm (unchanged) 5. Per run: LLM-set edges 18.6 ± 3.0; final edges between pairs the algorithm did not connect 10.2 ± 1.3; LLM additions where at least 90% of resamples had no edge 6.0 ± 2.0.

| Final edge | Runs (of 5) |
|---|---|
| Age->Length | 5 |
| Age->Shell weight | 5 |
| Age->Diameter | 5 |
| Age->Height | 5 |
| Age->Whole weight | 5 |
| Age->Shucked weight | 5 |
| Age->Viscera weight | 5 |
| Length->Diameter | 5 |
| Whole weight->Shell weight | 5 |
| Height->Whole weight | 5 |
| Height->Shucked weight | 5 |
| Whole weight->Shucked weight | 5 |
| Whole weight->Viscera weight | 5 |
| Height->Viscera weight | 4 |
| Length->Shell weight | 4 |
| Length->Height | 4 |
| Length->Whole weight | 4 |
| Length->Shucked weight | 4 |
| Length->Viscera weight | 4 |
| Height->Shell weight | 2 |
| Shucked weight->Shell weight | 2 |
| Diameter->Whole weight | 2 |
| Viscera weight->Shucked weight | 1 |
| Diameter->Height | 1 |
| Diameter->Shucked weight | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.21 ± 0.01 | 0.43 ± 0.00 | 0.28 ± 0.01 | 0.0 ± 0.0 | 1.0 ± 0.0 | 18.6 ± 0.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S1 after bootstrap edits | 0.24 ± 0.06 | 0.17 ± 0.06 | 0.20 ± 0.06 | 0.0 ± 0.0 | 1.0 ± 0.0 | 10.8 ± 0.8 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.36 ± 0.06 | 1.00 ± 0.00 | 0.53 ± 0.06 | 7.0 ± 0.0 | 0.0 ± 0.0 | 19.6 ± 2.8 | 0.36 ± 0.06 | 1.00 ± 0.00 | 0.53 ± 0.06 |
| S3 after KCI pruning | 0.36 ± 0.06 | 1.00 ± 0.00 | 0.53 ± 0.06 | 7.0 ± 0.0 | 0.0 ± 0.0 | 19.6 ± 2.8 | 0.36 ± 0.06 | 1.00 ± 0.00 | 0.53 ± 0.06 |
| S4 final (after cycle step) | 0.36 ± 0.06 | 1.00 ± 0.00 | 0.53 ± 0.06 | 7.0 ± 0.0 | 0.0 ± 0.0 | 19.6 ± 2.8 | 0.36 ± 0.06 | 1.00 ± 0.00 | 0.53 ± 0.06 |

## Arm `k12` (4 runs)

Family `abalone`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08. File path names the dataset: no.

**Choices.** Algorithm: FCI ×4. Hyperparameters passed to it: {"alpha": 0.05, "depth": 6, "indep_test": "fisherz"} ×2; {"alpha": 0.05, "depth": -1, "indep_test": "rcit"} ×1; {"alpha": 0.05, "depth": -1, "indep_test": "fisherz"} ×1. Proposed by the LLM but not passed: [] ×4. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 2 | 1 | 0 | 0 |
| 06b_rerank | 3 | 1 | 0 | 0 |
| 06c_hyperparameters | 2 | 1 | 0 | 0 |
| 07b_refinement | 16 | 8 | 5 | 0 |
| 08a_report_graph_text | 2 | 1 | 0 | 0 |
| 08b_report | 10 | 4 | 0 | 2 |
| 09_discussion_init | 4 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×3, 06b_rerank ×2, 08b_report ×1.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 6, "indep_test": "fisherz"}: 1; FCI {"alpha": 0.05, "depth": -1, "indep_test": "rcit"}: 1; FCI {"alpha": 0.05, "depth": -1, "indep_test": "fisherz"}: 1.

**Graph by stage.** 2 distinct algorithm outputs (S0) across 4 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 14.0 ± 0.0 | 0.82 | 0.54 |
| S1 after bootstrap edits | 3.8 ± 1.5 | 0.56 | 0.50 |
| S2 after LLM review | 3.8 ± 1.5 | 0.56 | 0.50 |
| S3 after KCI pruning | 3.8 ± 1.5 | 0.56 | 0.50 |
| S4 final (after cycle step) | 3.8 ± 1.5 | 0.56 | 0.50 |

**LLM review decisions.** 28 pairs. Same decision in every run: 28. Same edge/no-edge call in every run: 28. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 112.

**Final edges.** 9 distinct edges appear in at least one run; 0 appear in every run. Set by: algorithm (unchanged) 15. Per run: LLM-set edges 0.0 ± 0.0; final edges between pairs the algorithm did not connect 0.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

| Final edge | Runs (of 4) |
|---|---|
| V02->V07 | 3 |
| V08->V03 | 3 |
| V05 o-o V06 | 3 |
| V01 <-> V08 | 1 |
| V03 o-> V02 | 1 |
| V02 <-> V06 | 1 |
| V03 o-> V08 | 1 |
| V05 <-> V07 | 1 |
| V06->V07 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.16 ± 0.04 | 0.32 ± 0.07 | 0.21 ± 0.05 | 0.2 ± 0.5 | 0.0 ± 0.0 | 18.8 ± 0.5 | 0.08 ± 0.17 | 0.04 ± 0.07 | 0.05 ± 0.10 |
| S1 after bootstrap edits | 0.04 ± 0.08 | 0.04 ± 0.07 | 0.04 ± 0.08 | 0.0 ± 0.0 | 0.0 ± 0.0 | 10.5 ± 1.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.04 ± 0.08 | 0.04 ± 0.07 | 0.04 ± 0.08 | 0.0 ± 0.0 | 0.0 ± 0.0 | 10.5 ± 1.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S3 after KCI pruning | 0.04 ± 0.08 | 0.04 ± 0.07 | 0.04 ± 0.08 | 0.0 ± 0.0 | 0.0 ± 0.0 | 10.5 ± 1.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S4 final (after cycle step) | 0.04 ± 0.08 | 0.04 ± 0.07 | 0.04 ± 0.08 | 0.0 ± 0.0 | 0.0 ± 0.0 | 10.5 ± 1.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |

## Arm `k13` (3 runs)

Family `abalone`, role `swapped`. Column labels: Length, Age, Diameter, Shell weight, Whole weight, Height, Viscera weight, Shucked weight. File path names the dataset: no.

**Choices.** Algorithm: FCI ×3. Hyperparameters passed to it: {"alpha": 0.05, "depth": 6, "indep_test": "rcit"} ×3. Proposed by the LLM but not passed: ["background_knowledge"] ×2; [] ×1. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 3 | 0 | 0 | 0 |
| 06b_rerank | 3 | 0 | 0 | 0 |
| 06c_hyperparameters | 3 | 0 | 0 | 0 |
| 07b_refinement | 24 | 0 | 0 | 0 |
| 08a_report_graph_text | 3 | 0 | 0 | 0 |
| 08b_report | 11 | 2 | 0 | 2 |
| 09_discussion_init | 3 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×3.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 6, "indep_test": "rcit"}: 3.

**Graph by stage.** 3 distinct algorithm outputs (S0) across 3 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 15.0 ± 1.0 | 0.92 | 0.46 |
| S1 after bootstrap edits | 5.0 ± 1.7 | 0.43 | 0.37 |
| S2 after LLM review | 21.7 ± 0.6 | 0.94 | 0.94 |
| S3 after KCI pruning | 21.7 ± 0.6 | 0.94 | 0.94 |
| S4 final (after cycle step) | 21.7 ± 0.6 | 0.94 | 0.94 |

**LLM review decisions.** 28 pairs. Same decision in every run: 26. Same edge/no-edge call in every run: 26. Mean share of runs agreeing with the commonest decision for a pair: 0.98. Letters over all runs: A 34, B 31, C 17, D 2.

**Final edges.** 23 distinct edges appear in at least one run; 21 appear in every run. Set by: llm 60, algorithm (unchanged) 5. Per run: LLM-set edges 20.0 ± 1.0; final edges between pairs the algorithm did not connect 9.0 ± 1.0; LLM additions where at least 90% of resamples had no edge 5.7 ± 0.6.

| Final edge | Runs (of 3) |
|---|---|
| Age->Length | 3 |
| Length->Diameter | 3 |
| Shell weight->Length | 3 |
| Whole weight->Length | 3 |
| Length->Height | 3 |
| Viscera weight->Length | 3 |
| Shucked weight->Length | 3 |
| Age->Diameter | 3 |
| Age->Shell weight | 3 |
| Age->Whole weight | 3 |
| Age->Height | 3 |
| Age->Viscera weight | 3 |
| Age->Shucked weight | 3 |
| Shell weight->Diameter | 3 |
| Whole weight->Diameter | 3 |
| Viscera weight->Diameter | 3 |
| Shucked weight->Diameter | 3 |
| Whole weight->Shell weight | 3 |
| Whole weight->Viscera weight | 3 |
| Whole weight->Shucked weight | 3 |
| Viscera weight->Shucked weight | 3 |
| Diameter->Height | 1 |
| Shucked weight->Shell weight | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.20 ± 0.01 | 0.43 ± 0.00 | 0.27 ± 0.01 | 0.0 ± 0.0 | 1.0 ± 0.0 | 19.0 ± 1.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S1 after bootstrap edits | 0.22 ± 0.10 | 0.14 ± 0.00 | 0.17 ± 0.03 | 0.0 ± 0.0 | 1.0 ± 0.0 | 11.0 ± 1.7 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 | 2.0 ± 0.0 | 5.0 ± 0.0 | 21.7 ± 0.6 | 0.09 ± 0.00 | 0.29 ± 0.00 | 0.14 ± 0.00 |
| S3 after KCI pruning | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 | 2.0 ± 0.0 | 5.0 ± 0.0 | 21.7 ± 0.6 | 0.09 ± 0.00 | 0.29 ± 0.00 | 0.14 ± 0.00 |
| S4 final (after cycle step) | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 | 2.0 ± 0.0 | 5.0 ± 0.0 | 21.7 ± 0.6 | 0.09 ± 0.00 | 0.29 ± 0.00 | 0.14 ± 0.00 |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.22 ± 0.03 | 0.48 ± 0.08 | 0.30 ± 0.04 | 0.0 ± 0.0 | 0.0 ± 0.0 | 18.7 ± 0.6 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S1 after bootstrap edits | 0.33 ± 0.00 | 0.24 ± 0.08 | 0.27 ± 0.06 | 0.0 ± 0.0 | 0.0 ± 0.0 | 10.3 ± 1.2 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 | 7.0 ± 0.0 | 0.0 ± 0.0 | 21.7 ± 0.6 | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 |
| S3 after KCI pruning | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 | 7.0 ± 0.0 | 0.0 ± 0.0 | 21.7 ± 0.6 | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 |
| S4 final (after cycle step) | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 | 7.0 ± 0.0 | 0.0 ± 0.0 | 21.7 ± 0.6 | 0.32 ± 0.01 | 1.00 ± 0.00 | 0.49 ± 0.01 |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 18 |
| data only | 15 |
| both | 3 |
| neither | 24 |

Direction among those: data: direction as in reference 6, data: reversed 9, labels: direction as in reference 18.
Distinct edges: both: Age->Length; data only: Length->Diameter, Length->Height, Shell weight->Length, Viscera weight->Length, Whole weight->Length; labels only: Age->Diameter, Age->Height, Age->Shell weight, Age->Shucked weight, Age->Viscera weight, Age->Whole weight; neither: Diameter->Height, Shell weight->Diameter, Shucked weight->Diameter, Shucked weight->Shell weight, Viscera weight->Diameter, Viscera weight->Shucked weight, Whole weight->Diameter, Whole weight->Shell weight, Whole weight->Shucked weight, Whole weight->Viscera weight.

## Arm `k21` (4 runs)

Family `autompg`, role `real`. Column labels: mpg, displacement, horsepower, weight, acceleration. File path names the dataset: no.

**Choices.** Algorithm: FCI ×4. Hyperparameters passed to it: {"alpha": 0.1, "depth": 6, "indep_test": "rcit"} ×4. Proposed by the LLM but not passed: ["background_knowledge"] ×4. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 4 | 0 | 0 | 0 |
| 06b_rerank | 4 | 0 | 0 | 0 |
| 06c_hyperparameters | 4 | 0 | 0 | 0 |
| 07b_refinement | 20 | 0 | 0 | 0 |
| 08a_report_graph_text | 4 | 0 | 0 | 0 |
| 08b_report | 14 | 2 | 0 | 2 |
| 09_discussion_init | 4 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×6.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.1, "depth": 6, "indep_test": "rcit"}: 4.

**Graph by stage.** 4 distinct algorithm outputs (S0) across 4 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 5.8 ± 1.0 | 0.65 | 0.13 |
| S1 after bootstrap edits | 3.0 ± 0.8 | 0.64 | 0.15 |
| S2 after LLM review | 3.5 ± 1.0 | 0.80 | 0.59 |
| S3 after KCI pruning | 3.5 ± 1.0 | 0.80 | 0.59 |
| S4 final (after cycle step) | 3.5 ± 1.0 | 0.80 | 0.59 |

**LLM review decisions.** 10 pairs. Same decision in every run: 6. Same edge/no-edge call in every run: 8. Mean share of runs agreeing with the commonest decision for a pair: 0.90. Letters over all runs: A 9, B 5, C 25, D 1.

**Final edges.** 6 distinct edges appear in at least one run; 2 appear in every run. Set by: llm 11, algorithm (unchanged) 3. Per run: LLM-set edges 2.8 ± 1.0; final edges between pairs the algorithm did not connect 1.0 ± 0.8; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

| Final edge | Runs (of 4) |
|---|---|
| displacement->horsepower | 4 |
| horsepower->acceleration | 4 |
| weight->mpg | 3 |
| horsepower->mpg | 1 |
| weight->displacement | 1 |
| mpg->weight | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.70 ± 0.13 | 0.80 ± 0.16 | 0.74 ± 0.14 | 1.0 ± 0.8 | 0.5 ± 0.6 | 6.8 ± 1.0 | 0.42 ± 0.29 | 0.20 ± 0.16 | 0.27 ± 0.21 |
| S1 after bootstrap edits | 0.85 ± 0.17 | 0.50 ± 0.12 | 0.62 ± 0.11 | 1.0 ± 0.8 | 0.0 ± 0.0 | 5.5 ± 0.6 | 0.75 ± 0.50 | 0.20 ± 0.16 | 0.31 ± 0.23 |
| S2 after LLM review | 1.00 ± 0.00 | 0.70 ± 0.20 | 0.81 ± 0.13 | 3.2 ± 1.3 | 0.2 ± 0.5 | 4.0 ± 0.8 | 0.92 ± 0.17 | 0.65 ± 0.25 | 0.75 ± 0.20 |
| S3 after KCI pruning | 1.00 ± 0.00 | 0.70 ± 0.20 | 0.81 ± 0.13 | 3.2 ± 1.3 | 0.2 ± 0.5 | 4.0 ± 0.8 | 0.92 ± 0.17 | 0.65 ± 0.25 | 0.75 ± 0.20 |
| S4 final (after cycle step) | 1.00 ± 0.00 | 0.70 ± 0.20 | 0.81 ± 0.13 | 3.2 ± 1.3 | 0.2 ± 0.5 | 4.0 ± 0.8 | 0.92 ± 0.17 | 0.65 ± 0.25 | 0.75 ± 0.20 |

## Arm `k22` (4 runs)

Family `autompg`, role `neutral`. Column labels: V01, V02, V03, V04, V05. File path names the dataset: no.

**Choices.** Algorithm: FCI ×4. Hyperparameters passed to it: {"alpha": 0.1, "depth": 6, "indep_test": "rcit"} ×4. Proposed by the LLM but not passed: [] ×4. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 2 | 2 |
| 06a_filter | 1 | 1 | 0 | 1 |
| 06b_rerank | 1 | 1 | 0 | 1 |
| 06c_hyperparameters | 1 | 1 | 0 | 1 |
| 07b_refinement | 20 | 0 | 0 | 0 |
| 08a_report_graph_text | 4 | 0 | 0 | 0 |
| 08b_report | 11 | 3 | 1 | 3 |
| 09_discussion_init | 4 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 08a_report_graph_text ×6.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.1, "depth": 6, "indep_test": "rcit"}: 4.

**Graph by stage.** 4 distinct algorithm outputs (S0) across 4 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 6.0 ± 0.8 | 0.72 | 0.26 |
| S1 after bootstrap edits | 2.5 ± 1.3 | 0.26 | 0.26 |
| S2 after LLM review | 2.5 ± 1.3 | 0.26 | 0.26 |
| S3 after KCI pruning | 2.5 ± 1.3 | 0.26 | 0.26 |
| S4 final (after cycle step) | 2.5 ± 1.3 | 0.26 | 0.26 |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 40.

**Final edges.** 6 distinct edges appear in at least one run; 0 appear in every run. Set by: algorithm (unchanged) 10. Per run: LLM-set edges 0.0 ± 0.0; final edges between pairs the algorithm did not connect 0.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

| Final edge | Runs (of 4) |
|---|---|
| V02->V01 | 3 |
| V04 o-> V02 | 3 |
| V04->V01 | 1 |
| V02 <-> V05 | 1 |
| V03 <-> V05 | 1 |
| V03->V02 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.66 ± 0.05 | 0.80 ± 0.16 | 0.72 ± 0.10 | 0.8 ± 1.0 | 0.8 ± 1.0 | 6.8 ± 0.5 | 0.25 ± 0.29 | 0.15 ± 0.19 | 0.18 ± 0.22 |
| S1 after bootstrap edits | 0.67 ± 0.24 | 0.30 ± 0.12 | 0.39 ± 0.10 | 0.2 ± 0.5 | 0.2 ± 0.5 | 5.8 ± 1.0 | 0.12 ± 0.25 | 0.05 ± 0.10 | 0.07 ± 0.14 |
| S2 after LLM review | 0.67 ± 0.24 | 0.30 ± 0.12 | 0.39 ± 0.10 | 0.2 ± 0.5 | 0.2 ± 0.5 | 5.8 ± 1.0 | 0.12 ± 0.25 | 0.05 ± 0.10 | 0.07 ± 0.14 |
| S3 after KCI pruning | 0.67 ± 0.24 | 0.30 ± 0.12 | 0.39 ± 0.10 | 0.2 ± 0.5 | 0.2 ± 0.5 | 5.8 ± 1.0 | 0.12 ± 0.25 | 0.05 ± 0.10 | 0.07 ± 0.14 |
| S4 final (after cycle step) | 0.67 ± 0.24 | 0.30 ± 0.12 | 0.39 ± 0.10 | 0.2 ± 0.5 | 0.2 ± 0.5 | 5.8 ± 1.0 | 0.12 ± 0.25 | 0.05 ± 0.10 | 0.07 ± 0.14 |

## Arm `k23` (3 runs)

Family `autompg`, role `swapped`. Column labels: displacement, weight, acceleration, horsepower, mpg. File path names the dataset: no.

**Choices.** Algorithm: FCI ×3. Hyperparameters passed to it: {"alpha": 0.1, "depth": 6, "indep_test": "rcit"} ×3. Proposed by the LLM but not passed: ["background_knowledge"] ×3. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 3 | 0 | 0 | 0 |
| 06b_rerank | 3 | 0 | 0 | 0 |
| 06c_hyperparameters | 3 | 0 | 0 | 0 |
| 07b_refinement | 15 | 0 | 0 | 0 |
| 08a_report_graph_text | 3 | 0 | 0 | 0 |
| 08b_report | 11 | 2 | 1 | 2 |
| 09_discussion_init | 3 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×3.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.1, "depth": 6, "indep_test": "rcit"}: 3.

**Graph by stage.** 3 distinct algorithm outputs (S0) across 3 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 5.7 ± 0.6 | 0.79 | 0.42 |
| S1 after bootstrap edits | 2.7 ± 0.6 | 0.61 | 0.61 |
| S2 after LLM review | 5.0 ± 0.0 | 1.00 | 1.00 |
| S3 after KCI pruning | 5.0 ± 0.0 | 1.00 | 1.00 |
| S4 final (after cycle step) | 5.0 ± 0.0 | 1.00 | 1.00 |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 9, B 6, C 15.

**Final edges.** 5 distinct edges appear in at least one run; 5 appear in every run. Set by: llm 12, algorithm (unchanged) 3. Per run: LLM-set edges 4.0 ± 0.0; final edges between pairs the algorithm did not connect 2.7 ± 0.6; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

| Final edge | Runs (of 3) |
|---|---|
| weight->displacement | 3 |
| displacement->horsepower | 3 |
| weight->mpg | 3 |
| horsepower->acceleration | 3 |
| horsepower->mpg | 3 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.59 ± 0.08 | 0.67 ± 0.12 | 0.62 ± 0.09 | 0.3 ± 0.6 | 1.3 ± 1.2 | 7.3 ± 0.6 | 0.17 ± 0.29 | 0.07 ± 0.12 | 0.10 ± 0.16 |
| S1 after bootstrap edits | 0.50 ± 0.17 | 0.27 ± 0.12 | 0.35 ± 0.14 | 0.0 ± 0.0 | 0.0 ± 0.0 | 6.3 ± 0.6 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.20 ± 0.00 | 0.20 ± 0.00 | 0.20 ± 0.00 | 0.0 ± 0.0 | 1.0 ± 0.0 | 9.0 ± 0.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S3 after KCI pruning | 0.20 ± 0.00 | 0.20 ± 0.00 | 0.20 ± 0.00 | 0.0 ± 0.0 | 1.0 ± 0.0 | 9.0 ± 0.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S4 final (after cycle step) | 0.20 ± 0.00 | 0.20 ± 0.00 | 0.20 ± 0.00 | 0.0 ± 0.0 | 1.0 ± 0.0 | 9.0 ± 0.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.41 ± 0.08 | 0.47 ± 0.12 | 0.44 ± 0.10 | 1.3 ± 0.6 | 0.0 ± 0.0 | 8.3 ± 0.6 | 0.44 ± 0.10 | 0.27 ± 0.12 | 0.33 ± 0.10 |
| S1 after bootstrap edits | 0.50 ± 0.17 | 0.27 ± 0.12 | 0.35 ± 0.14 | 1.0 ± 0.0 | 0.0 ± 0.0 | 6.3 ± 0.6 | 1.00 ± 0.00 | 0.20 ± 0.00 | 0.33 ± 0.00 |
| S2 after LLM review | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 5.0 ± 0.0 | 0.0 ± 0.0 | 3.0 ± 0.0 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| S3 after KCI pruning | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 5.0 ± 0.0 | 0.0 ± 0.0 | 3.0 ± 0.0 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| S4 final (after cycle step) | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 5.0 ± 0.0 | 0.0 ± 0.0 | 3.0 ± 0.0 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 9 |
| data only | 0 |
| both | 3 |
| neither | 0 |

Direction among those: labels: direction as in reference 9.
Distinct edges: both: displacement->horsepower; labels only: horsepower->acceleration, horsepower->mpg, weight->mpg.

## Arm `k31` (3 runs)

Family `concrete`, role `real`. Column labels: Cement, Blast furnace slag, Fly ash, Water, Superplasticizer, Coarse aggregate, Fine aggregate, Age, Compressive strength. File path names the dataset: no.

**Choices.** Algorithm: FCI ×3. Hyperparameters passed to it: {"alpha": 0.05, "depth": 6, "indep_test": "rcit"} ×2; {"alpha": 0.05, "depth": -1, "indep_test": "fisherz"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×3. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 3 | 0 | 0 | 0 |
| 06b_rerank | 3 | 0 | 0 | 0 |
| 06c_hyperparameters | 3 | 0 | 0 | 0 |
| 07b_refinement | 27 | 0 | 0 | 0 |
| 08a_report_graph_text | 3 | 0 | 0 | 0 |
| 08b_report | 11 | 2 | 0 | 2 |
| 09_discussion_init | 3 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×3.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": -1, "indep_test": "fisherz"}: 1; FCI {"alpha": 0.05, "depth": 6, "indep_test": "rcit"}: 2.

**Graph by stage.** 3 distinct algorithm outputs (S0) across 3 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 16.0 ± 0.0 | 0.75 | 0.37 |
| S1 after bootstrap edits | 6.3 ± 1.5 | 0.34 | 0.16 |
| S2 after LLM review | 9.0 ± 1.0 | 0.81 | 0.81 |
| S3 after KCI pruning | 9.0 ± 1.0 | 0.81 | 0.81 |
| S4 final (after cycle step) | 9.0 ± 1.0 | 0.81 | 0.81 |

**LLM review decisions.** 36 pairs. Same decision in every run: 33. Same edge/no-edge call in every run: 36. Mean share of runs agreeing with the commonest decision for a pair: 0.97. Letters over all runs: A 24, C 81, D 3.

**Final edges.** 11 distinct edges appear in at least one run; 8 appear in every run. Set by: llm 24, algorithm (unchanged) 3. Per run: LLM-set edges 8.0 ± 0.0; final edges between pairs the algorithm did not connect 4.7 ± 0.6; LLM additions where at least 90% of resamples had no edge 4.0 ± 1.0.

| Final edge | Runs (of 3) |
|---|---|
| Cement->Compressive strength | 3 |
| Blast furnace slag->Compressive strength | 3 |
| Fly ash->Compressive strength | 3 |
| Water->Compressive strength | 3 |
| Superplasticizer->Compressive strength | 3 |
| Coarse aggregate->Compressive strength | 3 |
| Fine aggregate->Compressive strength | 3 |
| Age->Compressive strength | 3 |
| Blast furnace slag <-> Coarse aggregate | 1 |
| Blast furnace slag <-> Fine aggregate | 1 |
| Fly ash <-> Superplasticizer | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.21 ± 0.04 | 0.42 ± 0.07 | 0.28 ± 0.05 | 0.0 ± 0.0 | 0.0 ± 0.0 | 20.7 ± 0.6 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S1 after bootstrap edits | 0.07 ± 0.12 | 0.04 ± 0.07 | 0.05 ± 0.09 | 0.0 ± 0.0 | 0.0 ± 0.0 | 14.0 ± 2.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.90 ± 0.10 | 1.00 ± 0.00 | 0.94 ± 0.06 | 8.0 ± 0.0 | 0.0 ± 0.0 | 1.0 ± 1.0 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| S3 after KCI pruning | 0.90 ± 0.10 | 1.00 ± 0.00 | 0.94 ± 0.06 | 8.0 ± 0.0 | 0.0 ± 0.0 | 1.0 ± 1.0 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| S4 final (after cycle step) | 0.90 ± 0.10 | 1.00 ± 0.00 | 0.94 ± 0.06 | 8.0 ± 0.0 | 0.0 ± 0.0 | 1.0 ± 1.0 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |

## Arm `k32` (4 runs)

Family `concrete`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09. File path names the dataset: no.

**Choices.** Algorithm: FCI ×4. Hyperparameters passed to it: {"alpha": 0.05, "depth": 6, "indep_test": "rcit"} ×4. Proposed by the LLM but not passed: [] ×4. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 2 | 2 |
| 06a_filter | 1 | 1 | 0 | 1 |
| 06b_rerank | 2 | 2 | 0 | 0 |
| 06c_hyperparameters | 1 | 1 | 0 | 1 |
| 07b_refinement | 36 | 0 | 0 | 0 |
| 08a_report_graph_text | 4 | 0 | 0 | 0 |
| 08b_report | 11 | 3 | 1 | 3 |
| 09_discussion_init | 4 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06b_rerank ×4, 08a_report_graph_text ×2.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 6, "indep_test": "rcit"}: 4.

**Graph by stage.** 4 distinct algorithm outputs (S0) across 4 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 15.8 ± 1.0 | 0.82 | 0.31 |
| S1 after bootstrap edits | 6.0 ± 1.4 | 0.45 | 0.12 |
| S2 after LLM review | 6.0 ± 1.4 | 0.45 | 0.12 |
| S3 after KCI pruning | 6.0 ± 1.4 | 0.45 | 0.12 |
| S4 final (after cycle step) | 6.0 ± 1.4 | 0.45 | 0.12 |

**LLM review decisions.** 36 pairs. Same decision in every run: 35. Same edge/no-edge call in every run: 35. Mean share of runs agreeing with the commonest decision for a pair: 0.99. Letters over all runs: A 1, D 143.

**Final edges.** 18 distinct edges appear in at least one run; 0 appear in every run. Set by: algorithm (unchanged) 24. Per run: LLM-set edges 0.0 ± 0.0; final edges between pairs the algorithm did not connect 0.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

| Final edge | Runs (of 4) |
|---|---|
| V03->V01 | 3 |
| V02 <-> V07 | 2 |
| V05 o-> V03 | 2 |
| V05 o-> V04 | 2 |
| V03 <-> V05 | 2 |
| V02 o-> V01 | 1 |
| V03 o-> V01 | 1 |
| V06 o-> V01 | 1 |
| V01 <-> V07 | 1 |
| V06 o-> V07 | 1 |
| V02 <-> V06 | 1 |
| V04->V07 | 1 |
| V08 o-> V09 | 1 |
| V01 <-> V06 | 1 |
| V04->V05 | 1 |
| V01->V07 | 1 |
| V02->V06 | 1 |
| V05->V04 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.22 ± 0.04 | 0.44 ± 0.07 | 0.29 ± 0.05 | 0.5 ± 0.6 | 0.0 ± 0.0 | 19.8 ± 0.5 | 0.12 ± 0.11 | 0.06 ± 0.07 | 0.07 ± 0.09 |
| S1 after bootstrap edits | 0.04 ± 0.08 | 0.03 ± 0.06 | 0.04 ± 0.07 | 0.0 ± 0.0 | 0.0 ± 0.0 | 13.8 ± 1.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.04 ± 0.08 | 0.03 ± 0.06 | 0.04 ± 0.07 | 0.0 ± 0.0 | 0.0 ± 0.0 | 13.8 ± 1.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S3 after KCI pruning | 0.04 ± 0.08 | 0.03 ± 0.06 | 0.04 ± 0.07 | 0.0 ± 0.0 | 0.0 ± 0.0 | 13.8 ± 1.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S4 final (after cycle step) | 0.04 ± 0.08 | 0.03 ± 0.06 | 0.04 ± 0.07 | 0.0 ± 0.0 | 0.0 ± 0.0 | 13.8 ± 1.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |

## Arm `k33` (3 runs)

Family `concrete`, role `swapped`. Column labels: Blast furnace slag, Cement, Water, Fly ash, Coarse aggregate, Superplasticizer, Age, Compressive strength, Fine aggregate. File path names the dataset: no.

**Choices.** Algorithm: FCI ×3. Hyperparameters passed to it: {"alpha": 0.05, "depth": 6, "indep_test": "rcit"} ×3. Proposed by the LLM but not passed: ["background_knowledge"] ×3. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 3 | 0 | 0 | 0 |
| 06b_rerank | 3 | 0 | 0 | 0 |
| 06c_hyperparameters | 3 | 0 | 0 | 0 |
| 07b_refinement | 27 | 0 | 0 | 0 |
| 08a_report_graph_text | 3 | 0 | 0 | 0 |
| 08b_report | 11 | 2 | 1 | 2 |
| 09_discussion_init | 3 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×3.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 6, "indep_test": "rcit"}: 3.

**Graph by stage.** 3 distinct algorithm outputs (S0) across 3 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 14.7 ± 0.6 | 0.80 | 0.37 |
| S1 after bootstrap edits | 7.3 ± 1.5 | 0.63 | 0.19 |
| S2 after LLM review | 9.3 ± 1.2 | 0.81 | 0.70 |
| S3 after KCI pruning | 9.3 ± 1.2 | 0.81 | 0.70 |
| S4 final (after cycle step) | 9.3 ± 1.2 | 0.81 | 0.70 |

**LLM review decisions.** 36 pairs. Same decision in every run: 29. Same edge/no-edge call in every run: 33. Mean share of runs agreeing with the commonest decision for a pair: 0.94. Letters over all runs: A 24, B 1, C 77, D 6.

**Final edges.** 12 distinct edges appear in at least one run; 7 appear in every run. Set by: llm 25, algorithm (unchanged) 3. Per run: LLM-set edges 8.3 ± 1.2; final edges between pairs the algorithm did not connect 7.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 5.3 ± 0.6.

| Final edge | Runs (of 3) |
|---|---|
| Blast furnace slag->Compressive strength | 3 |
| Cement->Compressive strength | 3 |
| Water->Compressive strength | 3 |
| Fly ash->Compressive strength | 3 |
| Coarse aggregate->Compressive strength | 3 |
| Superplasticizer->Compressive strength | 3 |
| Age->Compressive strength | 3 |
| Blast furnace slag <-> Cement | 2 |
| Compressive strength->Fine aggregate | 2 |
| Blast furnace slag->Cement | 1 |
| Blast furnace slag <-> Water | 1 |
| Age->Fly ash | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.20 ± 0.07 | 0.38 ± 0.12 | 0.26 ± 0.09 | 0.0 ± 0.0 | 0.0 ± 0.0 | 19.7 ± 1.2 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S1 after bootstrap edits | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 15.3 ± 1.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.07 ± 0.06 | 0.08 ± 0.07 | 0.07 ± 0.06 | 0.7 ± 0.6 | 0.0 ± 0.0 | 16.0 ± 0.0 | 0.07 ± 0.06 | 0.08 ± 0.07 | 0.08 ± 0.07 |
| S3 after KCI pruning | 0.07 ± 0.06 | 0.08 ± 0.07 | 0.07 ± 0.06 | 0.7 ± 0.6 | 0.0 ± 0.0 | 16.0 ± 0.0 | 0.07 ± 0.06 | 0.08 ± 0.07 | 0.08 ± 0.07 |
| S4 final (after cycle step) | 0.07 ± 0.06 | 0.08 ± 0.07 | 0.07 ± 0.06 | 0.7 ± 0.6 | 0.0 ± 0.0 | 16.0 ± 0.0 | 0.07 ± 0.06 | 0.08 ± 0.07 | 0.08 ± 0.07 |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.07 ± 0.00 | 0.12 ± 0.00 | 0.09 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 21.7 ± 0.6 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S1 after bootstrap edits | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.0 ± 0.0 | 0.0 ± 0.0 | 15.3 ± 1.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.83 ± 0.04 | 0.96 ± 0.07 | 0.88 ± 0.01 | 7.0 ± 0.0 | 0.7 ± 0.6 | 2.7 ± 0.6 | 0.85 ± 0.13 | 0.88 ± 0.00 | 0.86 ± 0.06 |
| S3 after KCI pruning | 0.83 ± 0.04 | 0.96 ± 0.07 | 0.88 ± 0.01 | 7.0 ± 0.0 | 0.7 ± 0.6 | 2.7 ± 0.6 | 0.85 ± 0.13 | 0.88 ± 0.00 | 0.86 ± 0.06 |
| S4 final (after cycle step) | 0.83 ± 0.04 | 0.96 ± 0.07 | 0.88 ± 0.01 | 7.0 ± 0.0 | 0.7 ± 0.6 | 2.7 ± 0.6 | 0.85 ± 0.13 | 0.88 ± 0.00 | 0.86 ± 0.06 |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 21 |
| data only | 0 |
| both | 2 |
| neither | 2 |

Direction among those: labels: direction as in reference 21.
Distinct edges: both: Compressive strength->Fine aggregate; labels only: Age->Compressive strength, Blast furnace slag->Compressive strength, Cement->Compressive strength, Coarse aggregate->Compressive strength, Fly ash->Compressive strength, Superplasticizer->Compressive strength, Water->Compressive strength; neither: Age->Fly ash, Blast furnace slag->Cement.

## Arm `k41` (4 runs)

Family `dwd`, role `real`. Column labels: Altitude, Temperature, Precipitation, Longitude, Sunshine hours. File path names the dataset: no.

**Choices.** Algorithm: FCI ×4. Hyperparameters passed to it: {"alpha": 0.1, "depth": 6, "indep_test": "rcit"} ×4. Proposed by the LLM but not passed: ["background_knowledge"] ×4. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 4 | 0 | 0 | 0 |
| 06b_rerank | 4 | 0 | 0 | 0 |
| 06c_hyperparameters | 4 | 0 | 0 | 0 |
| 07b_refinement | 20 | 0 | 0 | 0 |
| 08a_report_graph_text | 4 | 0 | 0 | 0 |
| 08b_report | 14 | 2 | 0 | 2 |
| 09_discussion_init | 4 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×6.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.1, "depth": 6, "indep_test": "rcit"}: 4.

**Graph by stage.** 4 distinct algorithm outputs (S0) across 4 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 6.0 ± 0.8 | 0.76 | 0.19 |
| S1 after bootstrap edits | 1.2 ± 1.3 | 0.11 | 0.00 |
| S2 after LLM review | 3.2 ± 0.5 | 0.88 | 0.88 |
| S3 after KCI pruning | 3.2 ± 0.5 | 0.88 | 0.88 |
| S4 final (after cycle step) | 3.2 ± 0.5 | 0.88 | 0.88 |

**LLM review decisions.** 10 pairs. Same decision in every run: 9. Same edge/no-edge call in every run: 9. Mean share of runs agreeing with the commonest decision for a pair: 0.95. Letters over all runs: A 8, B 5, C 26, D 1.

**Final edges.** 4 distinct edges appear in at least one run; 3 appear in every run. Set by: llm 13. Per run: LLM-set edges 3.2 ± 0.5; final edges between pairs the algorithm did not connect 1.2 ± 0.5; LLM additions where at least 90% of resamples had no edge 0.5 ± 0.6.

| Final edge | Runs (of 4) |
|---|---|
| Altitude->Temperature | 4 |
| Altitude->Precipitation | 4 |
| Sunshine hours->Temperature | 4 |
| Precipitation->Temperature | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.63 ± 0.05 | 0.94 ± 0.12 | 0.75 ± 0.06 | 0.2 ± 0.5 | 0.2 ± 0.5 | 6.2 ± 0.5 | 0.25 ± 0.35 | 0.06 ± 0.12 | 0.08 ± 0.17 |
| S1 after bootstrap edits | 0.56 ± 0.51 | 0.19 ± 0.24 | 0.24 ± 0.29 | 0.0 ± 0.0 | 0.0 ± 0.0 | 4.5 ± 0.6 | n/a | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.62 ± 0.08 | 0.50 ± 0.00 | 0.55 ± 0.04 | 2.0 ± 0.0 | 0.0 ± 0.0 | 4.2 ± 0.5 | 0.62 ± 0.08 | 0.50 ± 0.00 | 0.55 ± 0.04 |
| S3 after KCI pruning | 0.62 ± 0.08 | 0.50 ± 0.00 | 0.55 ± 0.04 | 2.0 ± 0.0 | 0.0 ± 0.0 | 4.2 ± 0.5 | 0.62 ± 0.08 | 0.50 ± 0.00 | 0.55 ± 0.04 |
| S4 final (after cycle step) | 0.62 ± 0.08 | 0.50 ± 0.00 | 0.55 ± 0.04 | 2.0 ± 0.0 | 0.0 ± 0.0 | 4.2 ± 0.5 | 0.62 ± 0.08 | 0.50 ± 0.00 | 0.55 ± 0.04 |

## Arm `k42` (4 runs)

Family `dwd`, role `neutral`. Column labels: V01, V02, V03, V04, V05. File path names the dataset: no.

**Choices.** Algorithm: FCI ×4. Hyperparameters passed to it: {"alpha": 0.1, "depth": 6, "indep_test": "rcit"} ×4. Proposed by the LLM but not passed: [] ×4. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 4 | 0 | 0 | 0 |
| 06b_rerank | 4 | 0 | 0 | 0 |
| 06c_hyperparameters | 4 | 0 | 0 | 0 |
| 07b_refinement | 20 | 0 | 0 | 0 |
| 08a_report_graph_text | 4 | 0 | 0 | 0 |
| 08b_report | 13 | 3 | 1 | 2 |
| 09_discussion_init | 4 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×6.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.1, "depth": 6, "indep_test": "rcit"}: 4.

**Graph by stage.** 4 distinct algorithm outputs (S0) across 4 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 5.8 ± 0.5 | 0.92 | 0.37 |
| S1 after bootstrap edits | 2.2 ± 1.3 | 0.54 | 0.19 |
| S2 after LLM review | 2.2 ± 1.3 | 0.54 | 0.19 |
| S3 after KCI pruning | 2.2 ± 1.3 | 0.54 | 0.19 |
| S4 final (after cycle step) | 2.2 ± 1.3 | 0.54 | 0.19 |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 40.

**Final edges.** 6 distinct edges appear in at least one run; 0 appear in every run. Set by: algorithm (unchanged) 9. Per run: LLM-set edges 0.0 ± 0.0; final edges between pairs the algorithm did not connect 0.0 ± 0.0; LLM additions where at least 90% of resamples had no edge 0.0 ± 0.0.

| Final edge | Runs (of 4) |
|---|---|
| V04->V03 | 3 |
| V02 <-> V04 | 2 |
| V03 <-> V04 | 1 |
| V01 <-> V02 | 1 |
| V01 <-> V05 | 1 |
| V02 o-o V04 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.70 ± 0.07 | 1.00 ± 0.00 | 0.82 ± 0.04 | 0.0 ± 0.0 | 0.2 ± 0.5 | 5.8 ± 0.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S1 after bootstrap edits | 0.44 ± 0.31 | 0.31 ± 0.31 | 0.35 ± 0.31 | 0.0 ± 0.0 | 0.0 ± 0.0 | 5.0 ± 0.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.44 ± 0.31 | 0.31 ± 0.31 | 0.35 ± 0.31 | 0.0 ± 0.0 | 0.0 ± 0.0 | 5.0 ± 0.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S3 after KCI pruning | 0.44 ± 0.31 | 0.31 ± 0.31 | 0.35 ± 0.31 | 0.0 ± 0.0 | 0.0 ± 0.0 | 5.0 ± 0.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S4 final (after cycle step) | 0.44 ± 0.31 | 0.31 ± 0.31 | 0.35 ± 0.31 | 0.0 ± 0.0 | 0.0 ± 0.0 | 5.0 ± 0.0 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |

## Arm `k43` (4 runs)

Family `dwd`, role `swapped`. Column labels: Precipitation, Longitude, Sunshine hours, Altitude, Temperature. File path names the dataset: no.

**Choices.** Algorithm: FCI ×4. Hyperparameters passed to it: {"alpha": 0.1, "depth": 6, "indep_test": "rcit"} ×4. Proposed by the LLM but not passed: ["background_knowledge"] ×4. Served model: gpt-4o-2024-08-06.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 1 | 1 | 1 |
| 04b_knowledge | 2 | 2 | 0 | 2 |
| 06a_filter | 4 | 0 | 0 | 0 |
| 06b_rerank | 4 | 0 | 0 | 0 |
| 06c_hyperparameters | 4 | 0 | 0 | 0 |
| 07b_refinement | 20 | 0 | 0 | 0 |
| 08a_report_graph_text | 4 | 0 | 0 | 0 |
| 08b_report | 14 | 2 | 0 | 2 |
| 09_discussion_init | 4 | 0 | 0 | 0 |

First stage at which two runs stop sending identical requests (one count per pair of runs): 06a_filter ×6.

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.1, "depth": 6, "indep_test": "rcit"}: 4.

**Graph by stage.** 4 distinct algorithm outputs (S0) across 4 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 6.2 ± 1.3 | 0.71 | 0.09 |
| S1 after bootstrap edits | 2.0 ± 1.2 | 0.14 | 0.06 |
| S2 after LLM review | 4.2 ± 1.0 | 0.70 | 0.44 |
| S3 after KCI pruning | 4.2 ± 1.0 | 0.70 | 0.44 |
| S4 final (after cycle step) | 4.2 ± 1.0 | 0.70 | 0.44 |

**LLM review decisions.** 10 pairs. Same decision in every run: 5. Same edge/no-edge call in every run: 9. Mean share of runs agreeing with the commonest decision for a pair: 0.80. Letters over all runs: A 11, B 4, C 20, D 5.

**Final edges.** 8 distinct edges appear in at least one run; 2 appear in every run. Set by: llm 15, algorithm (unchanged) 2. Per run: LLM-set edges 3.8 ± 0.5; final edges between pairs the algorithm did not connect 2.2 ± 1.0; LLM additions where at least 90% of resamples had no edge 0.5 ± 0.6.

| Final edge | Runs (of 4) |
|---|---|
| Sunshine hours->Temperature | 4 |
| Altitude->Temperature | 4 |
| Precipitation->Altitude | 2 |
| Altitude->Precipitation | 2 |
| Temperature->Precipitation | 2 |
| Precipitation->Temperature | 1 |
| Longitude <-> Altitude | 1 |
| Precipitation <-> Sunshine hours | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.62 ± 0.15 | 0.94 ± 0.12 | 0.74 ± 0.13 | 0.2 ± 0.5 | 0.5 ± 0.6 | 6.2 ± 1.5 | 0.17 ± 0.24 | 0.06 ± 0.12 | 0.07 ± 0.14 |
| S1 after bootstrap edits | 0.25 ± 0.32 | 0.19 ± 0.24 | 0.21 ± 0.27 | 0.0 ± 0.0 | 0.2 ± 0.5 | 5.2 ± 0.5 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| S2 after LLM review | 0.26 ± 0.19 | 0.31 ± 0.24 | 0.28 ± 0.21 | 0.2 ± 0.5 | 0.5 ± 0.6 | 7.0 ± 0.0 | 0.06 ± 0.12 | 0.06 ± 0.12 | 0.06 ± 0.12 |
| S3 after KCI pruning | 0.26 ± 0.19 | 0.31 ± 0.24 | 0.28 ± 0.21 | 0.2 ± 0.5 | 0.5 ± 0.6 | 7.0 ± 0.0 | 0.06 ± 0.12 | 0.06 ± 0.12 | 0.06 ± 0.12 |
| S4 final (after cycle step) | 0.26 ± 0.19 | 0.31 ± 0.24 | 0.28 ± 0.21 | 0.2 ± 0.5 | 0.5 ± 0.6 | 7.0 ± 0.0 | 0.06 ± 0.12 | 0.06 ± 0.12 | 0.06 ± 0.12 |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.31 ± 0.08 | 0.50 ± 0.20 | 0.38 ± 0.12 | 0.5 ± 0.6 | 0.0 ± 0.0 | 8.2 ± 0.5 | 0.42 ± 0.12 | 0.12 ± 0.14 | 0.15 ± 0.18 |
| S1 after bootstrap edits | 0.67 ± 0.38 | 0.25 ± 0.00 | 0.34 ± 0.07 | 0.5 ± 0.6 | 0.0 ± 0.0 | 5.0 ± 1.2 | 0.75 ± 0.35 | 0.12 ± 0.14 | 0.18 ± 0.21 |
| S2 after LLM review | 0.49 ± 0.13 | 0.50 ± 0.00 | 0.49 ± 0.06 | 1.5 ± 0.6 | 0.5 ± 0.6 | 5.2 ± 1.0 | 0.40 ± 0.12 | 0.38 ± 0.14 | 0.38 ± 0.13 |
| S3 after KCI pruning | 0.49 ± 0.13 | 0.50 ± 0.00 | 0.49 ± 0.06 | 1.5 ± 0.6 | 0.5 ± 0.6 | 5.2 ± 1.0 | 0.40 ± 0.12 | 0.38 ± 0.14 | 0.38 ± 0.13 |
| S4 final (after cycle step) | 0.49 ± 0.13 | 0.50 ± 0.00 | 0.49 ± 0.06 | 1.5 ± 0.6 | 0.5 ± 0.6 | 5.2 ± 1.0 | 0.40 ± 0.12 | 0.38 ± 0.14 | 0.38 ± 0.13 |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 8 |
| data only | 3 |
| both | 0 |
| neither | 4 |

Direction among those: data: direction as in reference 1, data: reversed 2, labels: direction as in reference 6, labels: reversed 2.
Distinct edges: data only: Precipitation->Temperature, Temperature->Precipitation; labels only: Altitude->Precipitation, Altitude->Temperature, Precipitation->Altitude; neither: Sunshine hours->Temperature.

## Predictions fixed before the data

- **N1**: {"what": "swapped arms, distinct (family, edge): LLM-set final edges adjacent in exactly one reference", "labels_only": 19, "data_only": 7, "neither": 13, "share_following_labels": 0.7307692307692307, "verdict": "INCONCLUSIVE"}
- **N2**: {"what": "mean LLM-set final edges per run, neutral names at most half of real names, per family", "families": {"abalone": {"real": 18.6, "neutral": 0, "holds": true}, "autompg": {"real": 2.75, "neutral": 0, "holds": true}, "concrete": {"real": 8, "neutral": 0, "holds": true}, "dwd": {"real": 3.25, "neutral": 0, "holds": true}}, "testable_families": 4, "held_in": 4, "verdict": "SUPPORTED"}
- **N4**: {"what": "runs whose final graph has lower adjacency F1 than the algorithm's own output", "runs": 45, "below": 31, "share": 0.6888888888888889, "verdict": "INCONCLUSIVE"}
- **N5**: {"what": "exploratory: mean F1 by role over all runs, scored against the data-side reference or ground truth", "by_role": {"real": {"runs": 16, "directed_edge_f1_algorithm_output": 0.08779761904761905, "directed_edge_f1_final": 0.6794918443625341, "adjacency_f1_algorithm_output": 0.5120400432900433, "adjacency_f1_final": 0.6844959293298543}, "neutral": {"runs": 16, "directed_edge_f1_algorithm_output": 0.07667887667887668, "directed_edge_f1_final": 0.01785714285714286, "adjacency_f1_algorithm_output": 0.5132878866302779, "adjacency_f1_final": 0.20480387667887667}, "swapped": {"runs": 13, "directed_edge_f1_algorithm_output": 0.04395604395604396, "directed_edge_f1_final": 0.06953948688228608, "adjacency_f1_algorithm_output": 0.4955431042387564, "adjacency_f1_final": 0.26358679634541704}}, "verdict": "exploratory"}
- **P3**: {"distinct_outputs_counted": 43, "nondirected_edges_in_algorithm_output": 336, "of_which_still_adjacent_after_bootstrap_step": 100, "share": 0.2976190476190476, "directed_edges": 101, "directed_still_adjacent": 66, "verdict": "INCONCLUSIVE"}
- **P5**: {"arms": 12, "arms_with_more_than_one_algorithm": 0, "verdict": "exploratory"}

## Gates

- T1_no_arm_left_empty: **PASS**
- T2_min_runs_per_arm: **PASS**
- T3_same_dataset_bytes: **PASS**
- T4_variable_names_match_arm: **PASS**
- T5_scores_recomputed_equal_lineage: **PASS**
- T6_one_model_snapshot_per_arm (report only): **PASS**
