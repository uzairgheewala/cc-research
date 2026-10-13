# Edge lineage: 20261011T225512Z_s2_q082_r01_52b5f1

Dataset `/research/datasets/suite_q1s2/q082/q082.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 23 | 0.74 | 0.42 | 0.54 | 2 | 2 | 13 | 44 |
| S1 after bootstrap edits | 10 | 0.80 | 0.20 | 0.32 | 2 | 2 | 4 | 40 |
| S2 after LLM review | 10 | 0.80 | 0.20 | 0.32 | 2 | 2 | 4 | 40 |
| S3 after KCI pruning | 10 | 0.80 | 0.20 | 0.32 | 2 | 2 | 4 | 40 |
| S4 final (after cycle step) | 10 | 0.80 | 0.20 | 0.32 | 2 | 2 | 4 | 40 |

Scored against: reference graph s2_08_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 13. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 1, "D": 230}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 10 edges; set by {"algorithm (unchanged)": 10}; 10 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V07->V04 | algorithm (unchanged) | yes | 0.30 |
| V04->V08 | algorithm (unchanged) | yes | 0.00 |
| V20->V06 | algorithm (unchanged) | yes | 0.50 |
| V08 <-> V13 | algorithm (unchanged) | yes | 0.10 |
| V09 o-o V12 | algorithm (unchanged) | yes | 0.00 |
| V10->V14 | algorithm (unchanged) | yes | 0.45 |
| V12 o-o V22 | algorithm (unchanged) | yes | 0.00 |
| V21->V15 | algorithm (unchanged) | yes | 0.75 |
| V22->V16 | algorithm (unchanged) | yes | 0.00 |
| V20 o-o V21 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V03 | V01 o-o V03 | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V03 -> V01 | (V01, V03)=D |
| V01, V19 | V01 o-o V19 | V01   V19 (no edge) | V01   V19 (no edge) | V01   V19 (no edge) | V01   V19 (no edge) | no edge | (V01, V19)=D |
| V02, V05 | V02 o-> V05 | V02   V05 (no edge) | V02   V05 (no edge) | V02   V05 (no edge) | V02   V05 (no edge) | V05 -> V02 | (V02, V05)=D |
| V02, V17 | V02 o-o V17 | V02   V17 (no edge) | V02   V17 (no edge) | V02   V17 (no edge) | V02   V17 (no edge) | V17 -> V02 | (V02, V17)=D |
| V03, V10 | V03 o-o V10 | V03   V10 (no edge) | V03   V10 (no edge) | V03   V10 (no edge) | V03   V10 (no edge) | V03 -> V10 | (V03, V10)=D |
| V04, V13 | V04 <-> V13 | V04   V13 (no edge) | V04   V13 (no edge) | V04   V13 (no edge) | V04   V13 (no edge) | no edge | (V04, V13)=D |
| V05, V06 | V05 <-> V06 | V05   V06 (no edge) | V05   V06 (no edge) | V05   V06 (no edge) | V05   V06 (no edge) | no edge | (V05, V06)=D |
| V05, V17 | V17 o-> V05 | V05   V17 (no edge) | V05   V17 (no edge) | V05   V17 (no edge) | V05   V17 (no edge) | V17 -> V05 | (V05, V17)=D |
| V06, V16 | V06 <-> V16 | V06   V16 (no edge) | V06   V16 (no edge) | V06   V16 (no edge) | V06   V16 (no edge) | V16 -> V06 | (V06, V16)=D |
| V07, V19 | V07 o-o V19 | V07   V19 (no edge) | V07   V19 (no edge) | V07   V19 (no edge) | V07   V19 (no edge) | V07 -> V19 | (V07, V19)=D |
| V11, V13 | V11 o-> V13 | V11   V13 (no edge) | V11   V13 (no edge) | V11   V13 (no edge) | V11   V13 (no edge) | V13 -> V11 | (V11, V13)=D |
| V13, V14 | V13 <-> V14 | V13   V14 (no edge) | V13   V14 (no edge) | V13   V14 (no edge) | V13   V14 (no edge) | no edge | (V13, V14)=D |
| V14, V15 | V14 <-> V15 | V14   V15 (no edge) | V14   V15 (no edge) | V14   V15 (no edge) | V14   V15 (no edge) | V14 -> V15 | (V14, V15)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
