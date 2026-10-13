# Edge lineage: 20261011T193340Z_s2_q022_r01_13bcd2

Dataset `/research/datasets/suite_q1s2/q022/q022.csv`, algorithm **PC** {"alpha": 0.05, "indep_test": "rcit_cpu", "depth": 5}. 21 variables, 210 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 24 | 0.83 | 0.53 | 0.65 | 14 | 2 | 4 | 31 |
| S1 after bootstrap edits | 20 | 0.90 | 0.47 | 0.62 | 13 | 2 | 3 | 29 |
| S2 after LLM review | 20 | 0.90 | 0.47 | 0.62 | 13 | 2 | 3 | 29 |
| S3 after KCI pruning | 20 | 0.90 | 0.47 | 0.62 | 13 | 2 | 3 | 29 |
| S4 final (after cycle step) | 20 | 0.90 | 0.47 | 0.62 | 13 | 2 | 3 | 29 |

Scored against: reference graph s2_02_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 4. Of the deleted, 0 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 21 calls, 210 distinct pairs answered out of 210, plus 21 self-pairs. Letters: {"D": 210}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 20 edges; set by {"algorithm (unchanged)": 20}; 20 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V01 --- V02 | algorithm (unchanged) | yes | 0.00 |
| V01 --- V06 | algorithm (unchanged) | yes | 0.00 |
| V03->V09 | algorithm (unchanged) | yes | 0.00 |
| V03->V12 | algorithm (unchanged) | yes | 0.00 |
| V03->V14 | algorithm (unchanged) | yes | 0.00 |
| V04->V21 | algorithm (unchanged) | yes | 0.45 |
| V15->V05 | algorithm (unchanged) | yes | 0.00 |
| V05->V21 | algorithm (unchanged) | yes | 0.45 |
| V06->V09 | algorithm (unchanged) | yes | 0.00 |
| V06->V15 | algorithm (unchanged) | yes | 0.05 |
| V07 --- V13 | algorithm (unchanged) | yes | 0.00 |
| V08->V19 | algorithm (unchanged) | yes | 0.00 |
| V09->V21 | algorithm (unchanged) | yes | 0.45 |
| V10->V11 | algorithm (unchanged) | yes | 0.00 |
| V16->V11 | algorithm (unchanged) | yes | 0.00 |
| V16->V14 | algorithm (unchanged) | yes | 0.00 |
| V20->V15 | algorithm (unchanged) | yes | 0.00 |
| V16->V19 | algorithm (unchanged) | yes | 0.10 |
| V18->V19 | algorithm (unchanged) | yes | 0.00 |
| V20->V21 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V02, V06 | V02 --- V06 | V02   V06 (no edge) | V02   V06 (no edge) | V02   V06 (no edge) | V02   V06 (no edge) | no edge | (V02, V06)=D |
| V05, V12 | V05->V12 | V05   V12 (no edge) | V05   V12 (no edge) | V05   V12 (no edge) | V05   V12 (no edge) | V05 -> V12 | (V05, V12)=D |
| V07, V17 | V07 --- V17 | V07   V17 (no edge) | V07   V17 (no edge) | V07   V17 (no edge) | V07   V17 (no edge) | V07 -> V17 | (V07, V17)=D |
| V13, V17 | V13 --- V17 | V13   V17 (no edge) | V13   V17 (no edge) | V13   V17 (no edge) | V13   V17 (no edge) | no edge | (V13, V17)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
