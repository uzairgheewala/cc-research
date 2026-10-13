# Edge lineage: 20261006T145515Z_p4b_d02_r04_fa23e3

Dataset `/research/datasets/d02/d02.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 11 variables, 55 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 10 | 0.90 | 0.47 | 0.62 | 0 | 0 | 9 | 20 |
| S1 after bootstrap edits | 2 | 1.00 | 0.11 | 0.19 | 0 | 0 | 2 | 19 |
| S2 after LLM review | 2 | 1.00 | 0.11 | 0.19 | 0 | 0 | 2 | 19 |
| S3 after KCI pruning | 2 | 1.00 | 0.11 | 0.19 | 0 | 0 | 2 | 19 |
| S4 final (after cycle step) | 2 | 1.00 | 0.11 | 0.19 | 0 | 0 | 2 | 19 |

Scored against: reference graph reference_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 8. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 11 calls, 55 distinct pairs answered out of 55, plus 11 self-pairs. Letters: {"D": 55}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 2 edges; set by {"algorithm (unchanged)": 2}; 2 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V03 o-> V05 | algorithm (unchanged) | yes | 0.00 |
| V04 o-> V05 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V02 | V02 o-> V01 | V01   V02 (no edge) | V01   V02 (no edge) | V01   V02 (no edge) | V01   V02 (no edge) | V01 -> V02 | (V01, V02)=D |
| V01, V05 | V01 <-> V05 | V01   V05 (no edge) | V01   V05 (no edge) | V01   V05 (no edge) | V01   V05 (no edge) | no edge | (V01, V05)=D |
| V03, V04 | V03 o-o V04 | V03   V04 (no edge) | V03   V04 (no edge) | V03   V04 (no edge) | V03   V04 (no edge) | V03 -> V04 | (V03, V04)=D |
| V06, V07 | V06 ~~~ V07 | V06   V07 (no edge) | V06   V07 (no edge) | V06   V07 (no edge) | V06   V07 (no edge) | V06 -> V07 | (V06, V07)=D |
| V06, V08 | V06 o-o V08 | V06   V08 (no edge) | V06   V08 (no edge) | V06   V08 (no edge) | V06   V08 (no edge) | V08 -> V06 | (V06, V08)=D |
| V07, V08 | V07 o-o V08 | V07   V08 (no edge) | V07   V08 (no edge) | V07   V08 (no edge) | V07   V08 (no edge) | V08 -> V07 | (V07, V08)=D |
| V09, V10 | V09 o-o V10 | V09   V10 (no edge) | V09   V10 (no edge) | V09   V10 (no edge) | V09   V10 (no edge) | V09 -> V10 | (V09, V10)=D |
| V09, V11 | V09 o-o V11 | V09   V11 (no edge) | V09   V11 (no edge) | V09   V11 (no edge) | V09   V11 (no edge) | V09 -> V11 | (V09, V11)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
