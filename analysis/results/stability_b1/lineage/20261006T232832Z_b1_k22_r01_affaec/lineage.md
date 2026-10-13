# Edge lineage: 20261006T232832Z_b1_k22_r01_affaec

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
| S0 algorithm output | 7 | 0.71 | 1.00 | 0.83 | 2 | 1 | 2 | 6 |
| S1 after bootstrap edits | 3 | 0.67 | 0.40 | 0.50 | 1 | 0 | 1 | 5 |
| S2 after LLM review | 3 | 0.67 | 0.40 | 0.50 | 1 | 0 | 1 | 5 |
| S3 after KCI pruning | 3 | 0.67 | 0.40 | 0.50 | 1 | 0 | 1 | 5 |
| S4 final (after cycle step) | 3 | 0.67 | 0.40 | 0.50 | 1 | 0 | 1 | 5 |

Scored against: reference graph autompg_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 4. Of the deleted, 2 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"D": 10}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 3 edges; set by {"algorithm (unchanged)": 3}; 3 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02->V01 | algorithm (unchanged) | yes | 0.35 |
| V04->V01 | algorithm (unchanged) | yes | 0.30 |
| V04 o-> V02 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V03 | V01->V03 | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V03 -> V01 | (V01, V03)=D |
| V02, V03 | V02->V03 | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | V02 -> V03 | (V02, V03)=D |
| V02, V05 | V02 <-> V05 | V02   V05 (no edge) | V02   V05 (no edge) | V02   V05 (no edge) | V02   V05 (no edge) | no edge | (V02, V05)=D |
| V03, V05 | V03 <-> V05 | V03   V05 (no edge) | V03   V05 (no edge) | V03   V05 (no edge) | V03   V05 (no edge) | V03 -> V05 | (V03, V05)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
