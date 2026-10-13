# Stability and name-versus-data report

Label `b1self` (STUB LLM: tool self-test, answers carry no meaning). Runs directory `/sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/ccr-dev/runs`. 8 runs included in 8 arms; 0 excluded.

## Arm `k11` (1 runs)

Family `abalone`, role `real`. Column labels: Age, Length, Shell weight, Diameter, Height, Whole weight, Shucked weight, Viscera weight. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 24 | 0 | 0 | 24 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 16.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 15.0 (1 run) | n/a | n/a |
| S2 after LLM review | 18.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 18.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 15.0 (1 run) | n/a | n/a |

**LLM review decisions.** 28 pairs. Same decision in every run: 28. Same edge/no-edge call in every run: 28. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 8, B 4, C 5, D 11.

**Final edges.** 15 distinct edges appear in at least one run; 15 appear in every run. Set by: algorithm (unchanged) 9, llm 6. Per run: LLM-set edges 6.0 (1 run); final edges between pairs the algorithm did not connect 4.0 (1 run); LLM additions where at least 90% of resamples had no edge 2.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| Viscera weight->Age | 1 |
| Length->Diameter | 1 |
| Whole weight->Length | 1 |
| Length->Shucked weight | 1 |
| Length->Viscera weight | 1 |
| Shell weight->Diameter | 1 |
| Shell weight->Whole weight | 1 |
| Height->Diameter | 1 |
| Shucked weight->Diameter | 1 |
| Diameter->Viscera weight | 1 |
| Height->Whole weight | 1 |
| Height->Shucked weight | 1 |
| Whole weight->Shucked weight | 1 |
| Whole weight->Viscera weight | 1 |
| Shucked weight->Viscera weight | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.12 (1 run) | 0.29 (1 run) | 0.17 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 21.0 (1 run) | 0.15 (1 run) | 0.29 (1 run) | 0.20 (1 run) |
| S1 after bootstrap edits | 0.13 (1 run) | 0.29 (1 run) | 0.18 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 20.0 (1 run) | 0.15 (1 run) | 0.29 (1 run) | 0.20 (1 run) |
| S2 after LLM review | 0.17 (1 run) | 0.43 (1 run) | 0.24 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 22.0 (1 run) | 0.11 (1 run) | 0.29 (1 run) | 0.16 (1 run) |
| S3 after KCI pruning | 0.17 (1 run) | 0.43 (1 run) | 0.24 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 22.0 (1 run) | 0.11 (1 run) | 0.29 (1 run) | 0.16 (1 run) |
| S4 final (after cycle step) | 0.07 (1 run) | 0.14 (1 run) | 0.09 (1 run) | 0.0 (1 run) | 1.0 (1 run) | 21.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |

## Arm `k21` (1 runs)

Family `autompg`, role `real`. Column labels: mpg, displacement, horsepower, weight, acceleration. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 8 | 0 | 0 | 8 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 8.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 8.0 (1 run) | n/a | n/a |
| S2 after LLM review | 8.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 8.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 6.0 (1 run) | n/a | n/a |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 2, B 2, C 1, D 5.

**Final edges.** 6 distinct edges appear in at least one run; 6 appear in every run. Set by: algorithm (unchanged) 4, llm 2. Per run: LLM-set edges 2.0 (1 run); final edges between pairs the algorithm did not connect 1.0 (1 run); LLM additions where at least 90% of resamples had no edge 1.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| mpg->horsepower | 1 |
| weight->mpg | 1 |
| mpg->acceleration | 1 |
| horsepower->displacement | 1 |
| weight->displacement | 1 |
| acceleration->horsepower | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 1.0 (1 run) | 4.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S1 after bootstrap edits | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 1.0 (1 run) | 4.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S2 after LLM review | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 2.0 (1 run) | 3.0 (1 run) | 7.0 (1 run) | 0.25 (1 run) | 0.40 (1 run) | 0.31 (1 run) |
| S3 after KCI pruning | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 2.0 (1 run) | 3.0 (1 run) | 7.0 (1 run) | 0.25 (1 run) | 0.40 (1 run) | 0.31 (1 run) |
| S4 final (after cycle step) | 0.83 (1 run) | 1.00 (1 run) | 0.91 (1 run) | 2.0 (1 run) | 3.0 (1 run) | 5.0 (1 run) | 0.33 (1 run) | 0.40 (1 run) | 0.36 (1 run) |

## Arm `k22` (1 runs)

Family `autompg`, role `neutral`. Column labels: V01, V02, V03, V04, V05. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 8 | 0 | 0 | 8 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 8.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 8.0 (1 run) | n/a | n/a |
| S2 after LLM review | 8.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 8.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 7.0 (1 run) | n/a | n/a |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 2, B 2, C 1, D 5.

**Final edges.** 7 distinct edges appear in at least one run; 7 appear in every run. Set by: algorithm (unchanged) 5, llm 2. Per run: LLM-set edges 2.0 (1 run); final edges between pairs the algorithm did not connect 1.0 (1 run); LLM additions where at least 90% of resamples had no edge 1.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01->V03 | 1 |
| V01->V05 | 1 |
| V03->V02 | 1 |
| V04->V02 | 1 |
| V03->V04 | 1 |
| V05->V03 | 1 |
| V05->V04 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 1.0 (1 run) | 4.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S1 after bootstrap edits | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 1.0 (1 run) | 4.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S2 after LLM review | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 2.0 (1 run) | 3.0 (1 run) | 7.0 (1 run) | 0.25 (1 run) | 0.40 (1 run) | 0.31 (1 run) |
| S3 after KCI pruning | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 2.0 (1 run) | 3.0 (1 run) | 7.0 (1 run) | 0.25 (1 run) | 0.40 (1 run) | 0.31 (1 run) |
| S4 final (after cycle step) | 0.57 (1 run) | 0.80 (1 run) | 0.67 (1 run) | 1.0 (1 run) | 3.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |

## Arm `k23` (1 runs)

Family `autompg`, role `swapped`. Column labels: displacement, weight, acceleration, horsepower, mpg. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 8 | 0 | 0 | 8 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 8.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 8.0 (1 run) | n/a | n/a |
| S2 after LLM review | 8.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 8.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 6.0 (1 run) | n/a | n/a |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 2, B 2, C 1, D 5.

**Final edges.** 6 distinct edges appear in at least one run; 6 appear in every run. Set by: algorithm (unchanged) 4, llm 2. Per run: LLM-set edges 2.0 (1 run); final edges between pairs the algorithm did not connect 1.0 (1 run); LLM additions where at least 90% of resamples had no edge 1.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| displacement->acceleration | 1 |
| horsepower->displacement | 1 |
| displacement->mpg | 1 |
| acceleration->weight | 1 |
| horsepower->weight | 1 |
| mpg->acceleration | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 1.0 (1 run) | 4.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S1 after bootstrap edits | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 1.0 (1 run) | 4.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S2 after LLM review | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 2.0 (1 run) | 3.0 (1 run) | 7.0 (1 run) | 0.25 (1 run) | 0.40 (1 run) | 0.31 (1 run) |
| S3 after KCI pruning | 0.62 (1 run) | 1.00 (1 run) | 0.77 (1 run) | 2.0 (1 run) | 3.0 (1 run) | 7.0 (1 run) | 0.25 (1 run) | 0.40 (1 run) | 0.31 (1 run) |
| S4 final (after cycle step) | 0.83 (1 run) | 1.00 (1 run) | 0.91 (1 run) | 2.0 (1 run) | 3.0 (1 run) | 5.0 (1 run) | 0.33 (1 run) | 0.40 (1 run) | 0.36 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.50 (1 run) | 0.80 (1 run) | 0.62 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S1 after bootstrap edits | 0.50 (1 run) | 0.80 (1 run) | 0.62 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S2 after LLM review | 0.38 (1 run) | 0.60 (1 run) | 0.46 (1 run) | 0.0 (1 run) | 3.0 (1 run) | 10.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S3 after KCI pruning | 0.38 (1 run) | 0.60 (1 run) | 0.46 (1 run) | 0.0 (1 run) | 3.0 (1 run) | 10.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S4 final (after cycle step) | 0.17 (1 run) | 0.20 (1 run) | 0.18 (1 run) | 0.0 (1 run) | 1.0 (1 run) | 10.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 0 |
| data only | 0 |
| both | 1 |
| neither | 1 |

Direction among those: n/a.
Distinct edges: both: horsepower->displacement; neither: displacement->mpg.

## Arm `k31` (1 runs)

Family `concrete`, role `real`. Column labels: Cement, Blast furnace slag, Fly ash, Water, Superplasticizer, Coarse aggregate, Fine aggregate, Age, Compressive strength. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 48 | 0 | 0 | 48 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 17.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 17.0 (1 run) | n/a | n/a |
| S2 after LLM review | 22.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 22.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 16.0 (1 run) | n/a | n/a |

**LLM review decisions.** 36 pairs. Same decision in every run: 36. Same edge/no-edge call in every run: 36. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 10, B 6, C 6, D 14.

**Final edges.** 16 distinct edges appear in at least one run; 16 appear in every run. Set by: llm 9, algorithm (unchanged) 7. Per run: LLM-set edges 9.0 (1 run); final edges between pairs the algorithm did not connect 6.0 (1 run); LLM additions where at least 90% of resamples had no edge 7.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| Blast furnace slag->Cement | 1 |
| Cement->Fine aggregate | 1 |
| Blast furnace slag->Water | 1 |
| Blast furnace slag->Superplasticizer | 1 |
| Coarse aggregate->Blast furnace slag | 1 |
| Blast furnace slag->Fine aggregate | 1 |
| Fly ash->Coarse aggregate | 1 |
| Fly ash->Fine aggregate | 1 |
| Superplasticizer->Water | 1 |
| Coarse aggregate->Water | 1 |
| Fine aggregate->Water | 1 |
| Water->Age | 1 |
| Compressive strength->Water | 1 |
| Coarse aggregate->Fine aggregate | 1 |
| Compressive strength->Coarse aggregate | 1 |
| Fine aggregate->Age | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.24 (1 run) | 0.50 (1 run) | 0.32 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 19.0 (1 run) | 0.12 (1 run) | 0.25 (1 run) | 0.16 (1 run) |
| S1 after bootstrap edits | 0.24 (1 run) | 0.50 (1 run) | 0.32 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 19.0 (1 run) | 0.12 (1 run) | 0.25 (1 run) | 0.16 (1 run) |
| S2 after LLM review | 0.14 (1 run) | 0.38 (1 run) | 0.20 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 26.0 (1 run) | 0.05 (1 run) | 0.12 (1 run) | 0.07 (1 run) |
| S3 after KCI pruning | 0.14 (1 run) | 0.38 (1 run) | 0.20 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 26.0 (1 run) | 0.05 (1 run) | 0.12 (1 run) | 0.07 (1 run) |
| S4 final (after cycle step) | 0.12 (1 run) | 0.25 (1 run) | 0.17 (1 run) | 0.0 (1 run) | 2.0 (1 run) | 22.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |

## Arm `k41` (1 runs)

Family `dwd`, role `real`. Column labels: Altitude, Temperature, Precipitation, Longitude, Sunshine hours. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 7 | 0 | 0 | 7 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 6.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 7.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 7.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 5.0 (1 run) | n/a | n/a |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 2, B 2, C 1, D 5.

**Final edges.** 5 distinct edges appear in at least one run; 5 appear in every run. Set by: algorithm (unchanged) 3, llm 2. Per run: LLM-set edges 2.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 1.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| Precipitation->Altitude | 1 |
| Altitude->Sunshine hours | 1 |
| Longitude->Temperature | 1 |
| Precipitation->Longitude | 1 |
| Sunshine hours->Longitude | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.67 (1 run) | 1.00 (1 run) | 0.80 (1 run) | 0.0 (1 run) | 4.0 (1 run) | 6.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.67 (1 run) | 1.00 (1 run) | 0.80 (1 run) | 0.0 (1 run) | 4.0 (1 run) | 6.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.57 (1 run) | 1.00 (1 run) | 0.73 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 6.0 (1 run) | 0.29 (1 run) | 0.50 (1 run) | 0.36 (1 run) |
| S3 after KCI pruning | 0.57 (1 run) | 1.00 (1 run) | 0.73 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 6.0 (1 run) | 0.29 (1 run) | 0.50 (1 run) | 0.36 (1 run) |
| S4 final (after cycle step) | 0.60 (1 run) | 0.75 (1 run) | 0.67 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 5.0 (1 run) | 0.40 (1 run) | 0.50 (1 run) | 0.44 (1 run) |

## Arm `k42` (1 runs)

Family `dwd`, role `neutral`. Column labels: V01, V02, V03, V04, V05. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 7 | 0 | 0 | 7 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 6.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 7.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 7.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 5.0 (1 run) | n/a | n/a |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 2, B 2, C 1, D 5.

**Final edges.** 5 distinct edges appear in at least one run; 5 appear in every run. Set by: algorithm (unchanged) 4, llm 1. Per run: LLM-set edges 1.0 (1 run); final edges between pairs the algorithm did not connect 1.0 (1 run); LLM additions where at least 90% of resamples had no edge 1.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V02->V01 | 1 |
| V03->V01 | 1 |
| V04->V01 | 1 |
| V03->V04 | 1 |
| V05->V04 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.67 (1 run) | 1.00 (1 run) | 0.80 (1 run) | 0.0 (1 run) | 4.0 (1 run) | 6.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.67 (1 run) | 1.00 (1 run) | 0.80 (1 run) | 0.0 (1 run) | 4.0 (1 run) | 6.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.57 (1 run) | 1.00 (1 run) | 0.73 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 6.0 (1 run) | 0.29 (1 run) | 0.50 (1 run) | 0.36 (1 run) |
| S3 after KCI pruning | 0.57 (1 run) | 1.00 (1 run) | 0.73 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 6.0 (1 run) | 0.29 (1 run) | 0.50 (1 run) | 0.36 (1 run) |
| S4 final (after cycle step) | 0.40 (1 run) | 0.50 (1 run) | 0.44 (1 run) | 0.0 (1 run) | 2.0 (1 run) | 7.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |

## Arm `k43` (1 runs)

Family `dwd`, role `swapped`. Column labels: Precipitation, Longitude, Sunshine hours, Altitude, Temperature. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: stub-llm.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 7 | 0 | 0 | 7 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": -1, "indep_test": "fisherz_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 6.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 7.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 7.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 5.0 (1 run) | n/a | n/a |

**LLM review decisions.** 10 pairs. Same decision in every run: 10. Same edge/no-edge call in every run: 10. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 2, B 2, C 1, D 5.

**Final edges.** 5 distinct edges appear in at least one run; 5 appear in every run. Set by: algorithm (unchanged) 3, llm 2. Per run: LLM-set edges 2.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 1.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| Sunshine hours->Precipitation | 1 |
| Precipitation->Temperature | 1 |
| Altitude->Longitude | 1 |
| Sunshine hours->Altitude | 1 |
| Temperature->Altitude | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.67 (1 run) | 1.00 (1 run) | 0.80 (1 run) | 0.0 (1 run) | 4.0 (1 run) | 6.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.67 (1 run) | 1.00 (1 run) | 0.80 (1 run) | 0.0 (1 run) | 4.0 (1 run) | 6.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.57 (1 run) | 1.00 (1 run) | 0.73 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 6.0 (1 run) | 0.29 (1 run) | 0.50 (1 run) | 0.36 (1 run) |
| S3 after KCI pruning | 0.57 (1 run) | 1.00 (1 run) | 0.73 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 6.0 (1 run) | 0.29 (1 run) | 0.50 (1 run) | 0.36 (1 run) |
| S4 final (after cycle step) | 0.60 (1 run) | 0.75 (1 run) | 0.67 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 5.0 (1 run) | 0.40 (1 run) | 0.50 (1 run) | 0.44 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.33 (1 run) | 0.50 (1 run) | 0.40 (1 run) | 0.0 (1 run) | 2.0 (1 run) | 8.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.33 (1 run) | 0.50 (1 run) | 0.40 (1 run) | 0.0 (1 run) | 2.0 (1 run) | 8.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.43 (1 run) | 0.75 (1 run) | 0.55 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.25 (1 run) | 0.18 (1 run) |
| S3 after KCI pruning | 0.43 (1 run) | 0.75 (1 run) | 0.55 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 8.0 (1 run) | 0.14 (1 run) | 0.25 (1 run) | 0.18 (1 run) |
| S4 final (after cycle step) | 0.40 (1 run) | 0.50 (1 run) | 0.44 (1 run) | 0.0 (1 run) | 2.0 (1 run) | 7.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 0 |
| data only | 2 |
| both | 0 |
| neither | 0 |

Direction among those: data: direction as in reference 2.
Distinct edges: data only: Altitude->Longitude, Precipitation->Temperature.

## Predictions fixed before the data

- **N1**: {"what": "swapped arms, distinct (family, edge): LLM-set final edges adjacent in exactly one reference", "labels_only": 0, "data_only": 2, "neither": 1, "share_following_labels": 0.0, "verdict": "INCONCLUSIVE"}
- **N2**: {"what": "mean LLM-set final edges per run, neutral names at most half of real names, per family", "families": {"autompg": {"real": 2, "neutral": 2, "holds": false}, "dwd": {"real": 2, "neutral": 1, "holds": true}}, "testable_families": 2, "held_in": 1, "verdict": "REFUTED"}
- **N4**: {"what": "runs whose final graph has lower adjacency F1 than the algorithm's own output", "runs": 8, "below": 6, "share": 0.75, "verdict": "INCONCLUSIVE"}
- **N5**: {"what": "exploratory: mean F1 by role over all runs, scored against the data-side reference or ground truth", "by_role": {"real": {"runs": 4, "directed_edge_f1_algorithm_output": 0.13166666666666665, "directed_edge_f1_final": 0.20202020202020202, "adjacency_f1_algorithm_output": 0.5157859531772575, "adjacency_f1_final": 0.45833333333333326}, "neutral": {"runs": 2, "directed_edge_f1_algorithm_output": 0.08333333333333333, "directed_edge_f1_final": 0.08333333333333333, "adjacency_f1_algorithm_output": 0.7846153846153847, "adjacency_f1_final": 0.5555555555555556}, "swapped": {"runs": 2, "directed_edge_f1_algorithm_output": 0.08333333333333333, "directed_edge_f1_final": 0.40404040404040403, "adjacency_f1_algorithm_output": 0.7846153846153847, "adjacency_f1_final": 0.7878787878787878}}, "verdict": "exploratory"}
- **P3**: {"distinct_outputs_counted": 4, "nondirected_edges_in_algorithm_output": 4, "of_which_still_adjacent_after_bootstrap_step": 3, "share": 0.75, "directed_edges": 43, "directed_still_adjacent": 43, "verdict": "INCONCLUSIVE"}
- **P5**: {"arms": 8, "arms_with_more_than_one_algorithm": 0, "verdict": "exploratory"}

## Gates

- T1_no_arm_left_empty: **PASS**
- T2_min_runs_per_arm: **PASS**
- T3_same_dataset_bytes: **PASS**
- T4_variable_names_match_arm: **PASS**
- T5_scores_recomputed_equal_lineage: **PASS**
- T6_one_model_snapshot_per_arm (report only): **PASS**

This is a STUB self-test: the numbers above show that the tool runs and its checks behave as expected. They say nothing about Causal-Copilot's behaviour with a real model.
