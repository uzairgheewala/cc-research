# Edge lineage: 20261006T044214Z_golden_Linear_Gaussian_r01_b8b58c

Dataset `data/dataset/Linear_Gaussian`, algorithm **XGES** {"alpha": 2}. 5 variables, 10 pairs. 20 bootstrap resamples.

## Gates

- A_S0_equals_state_converted_graph: **PASS**
- B_rebuilt_S2_equals_graph_into_KCI: **PASS**
- C_rebuilt_S3_equals_graph_into_cycle_step: **PASS**
- D_cycle_output_equals_state_revised_graph: **PASS**
- E_every_change_covered_by_step_evidence: **PASS**
- F_all_llm_answers_name_dataset_variables: **PASS**

## Edges by stage

| Stage | Adjacent pairs | adj P | adj R | adj F1 | true edges directed correctly | reversed | present, not directed | SHD vs CPDAG |
|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 1 | 1.00 | 1.00 | 1.00 | 0 | 0 | 1 | 0 |
| S1 after bootstrap edits | 0 | n/a | 0.00 | 0.00 | 0 | 0 | 0 | 1 |
| S2 after LLM review | 0 | n/a | 0.00 | 0.00 | 0 | 0 | 0 | 1 |
| S3 after KCI pruning | 0 | n/a | 0.00 | 0.00 | 0 | 0 | 0 | 1 |
| S4 final (after cycle step) | 0 | n/a | 0.00 | 0.00 | 0 | 0 | 0 | 1 |

Scored against: ground truth loaded by the pipeline.

## What each step did

- Bootstrap step: added 0, deleted 1. Of the deleted, 1 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"D": 10}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 0 edges; set by {}; 0 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| X2, X4 | X2 --- X4 | X2   X4 (no edge) | X2   X4 (no edge) | X2   X4 (no edge) | X2   X4 (no edge) | X2 -> X4 | (X2, X4)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
