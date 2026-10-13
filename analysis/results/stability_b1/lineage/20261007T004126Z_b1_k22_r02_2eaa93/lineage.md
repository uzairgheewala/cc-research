# Edge lineage: 20261007T004126Z_b1_k22_r02_2eaa93

Dataset `/research/datasets/suite_b1/k22/k22.csv`, algorithm **FCI** {"alpha": 0.1, "indep_test": "rcit", "depth": 6}. 5 variables, 10 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 6 | 0.67 | 0.80 | 0.73 | 1 | 0 | 3 | 7 |
| S1 after bootstrap edits | 4 | 0.50 | 0.40 | 0.44 | 0 | 0 | 2 | 7 |
| S2 after LLM review | 4 | 0.50 | 0.40 | 0.44 | 0 | 0 | 2 | 7 |
| S3 after KCI pruning | 4 | 0.50 | 0.40 | 0.44 | 0 | 0 | 2 | 7 |
| S4 final (after cycle step) | 4 | 0.50 | 0.40 | 0.44 | 0 | 0 | 2 | 7 |

Scored against: reference graph autompg_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 2. Of the deleted, 0 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"D": 10}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 4 edges; set by {"algorithm (unchanged)": 4}; 4 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02->V01 | algorithm (unchanged) | yes | 0.30 |
| V04 o-> V02 | algorithm (unchanged) | yes | 0.00 |
| V02 <-> V05 | algorithm (unchanged) | yes | 0.05 |
| V03 <-> V05 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V03 | V01 o-> V03 | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V03 -> V01 | (V01, V03)=D |
| V02, V03 | V02->V03 | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | V02 -> V03 | (V02, V03)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
