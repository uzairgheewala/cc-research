# Edge lineage: 20261006T141902Z_p4b_20241024_145159_Linear-Non-gaussian_id_0_nodes10_samples1000_r02_b4e2a1

Dataset `data/dataset/20241024_145159_Linear-Non-gaussian_id_0_nodes10_samples1000`, algorithm **XGES** {"alpha": 2}. 10 variables, 45 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 9 | 0.33 | 0.33 | 0.33 | 1 | 0 | 2 | 14 |
| S1 after bootstrap edits | 7 | 0.14 | 0.11 | 0.12 | 1 | 0 | 0 | 15 |
| S2 after LLM review | 7 | 0.14 | 0.11 | 0.12 | 1 | 0 | 0 | 15 |
| S3 after KCI pruning | 7 | 0.14 | 0.11 | 0.12 | 1 | 0 | 0 | 15 |
| S4 final (after cycle step) | 7 | 0.14 | 0.11 | 0.12 | 1 | 0 | 0 | 15 |

Scored against: ground truth loaded by the pipeline.

## What each step did

- Bootstrap step: added 0, deleted 2. Of the deleted, 2 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 10 calls, 45 distinct pairs answered out of 45, plus 10 self-pairs. Letters: {"D": 45}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 7 edges; set by {"algorithm (unchanged)": 7}; 7 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| X0->X3 | algorithm (unchanged) | yes | 0.00 |
| X0->X9 | algorithm (unchanged) | yes | 0.00 |
| X1->X6 | algorithm (unchanged) | yes | 0.00 |
| X2->X3 | algorithm (unchanged) | yes | 0.00 |
| X2->X6 | algorithm (unchanged) | yes | 0.00 |
| X3->X9 | algorithm (unchanged) | yes | 0.00 |
| X6->X8 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| X0, X4 | X0 --- X4 | X0   X4 (no edge) | X0   X4 (no edge) | X0   X4 (no edge) | X0   X4 (no edge) | X0 -> X4 | (X0, X4)=D |
| X2, X5 | X2 --- X5 | X2   X5 (no edge) | X2   X5 (no edge) | X2   X5 (no edge) | X2   X5 (no edge) | X2 -> X5 | (X2, X5)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
