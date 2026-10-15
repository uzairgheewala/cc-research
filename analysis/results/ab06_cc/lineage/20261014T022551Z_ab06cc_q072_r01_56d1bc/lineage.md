# Edge lineage: 20261014T022551Z_ab06cc_q072_r01_56d1bc

Dataset `/research/datasets/suite_q1s2/q072/q072.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 27 | 0.78 | 0.60 | 0.68 | 6 | 1 | 14 | 36 |
| S1 after bootstrap edits | 11 | 1.00 | 0.31 | 0.48 | 5 | 1 | 5 | 31 |
| S2 after LLM review | 10 | 1.00 | 0.29 | 0.44 | 6 | 0 | 4 | 30 |
| S3 after KCI pruning | 10 | 1.00 | 0.29 | 0.44 | 6 | 0 | 4 | 30 |
| S4 final (after cycle step) | 10 | 1.00 | 0.29 | 0.44 | 6 | 0 | 4 | 30 |

Scored against: reference graph s2_07_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 16. Of the deleted, 4 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 5, "C": 3, "D": 223}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 1.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 10 edges; set by {"algorithm (unchanged)": 9, "llm": 1}; 9 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V01 o-o V21 | algorithm (unchanged) | yes | 0.00 |
| V02 ~~~ V10 | algorithm (unchanged) | yes | 0.00 |
| V10->V03 | algorithm (unchanged) | yes | 0.00 |
| V13 o-> V03 | algorithm (unchanged) | yes | 0.75 |
| V08->V11 | algorithm (unchanged) | yes | 0.00 |
| V09 o-> V12 | algorithm (unchanged) | yes | 0.00 |
| V09->V14 | algorithm (unchanged) | yes | 0.00 |
| V11->V21 | llm | yes | 0.00 |
| V12->V14 | algorithm (unchanged) | yes | 0.00 |
| V17->V22 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V20 | V01 o-o V20 | V01   V20 (no edge) | V01   V20 (no edge) | V01   V20 (no edge) | V01   V20 (no edge) | V01 -> V20 | (V01, V20)=D |
| V02, V03 | V02->V03 | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | V02 -> V03 | (V02, V03)=D |
| V02, V14 | V02 <-> V14 | V02   V14 (no edge) | V02   V14 (no edge) | V02   V14 (no edge) | V02   V14 (no edge) | V14 -> V02 | (V02, V14)=D |
| V02, V15 | V02 <-> V15 | V02   V15 (no edge) | V02   V15 (no edge) | V02   V15 (no edge) | V02   V15 (no edge) | no edge | (V02, V15)=D |
| V02, V16 | V16 o-> V02 | V02   V16 (no edge) | V02   V16 (no edge) | V02   V16 (no edge) | V02   V16 (no edge) | V16 -> V02 | (V02, V16)=D |
| V03, V19 | V19 o-> V03 | V03   V19 (no edge) | V03   V19 (no edge) | V03   V19 (no edge) | V03   V19 (no edge) | no edge | (V03, V19)=D |
| V04, V14 | V04 o-> V14 | V04   V14 (no edge) | V04   V14 (no edge) | V04   V14 (no edge) | V04   V14 (no edge) | V04 -> V14 | (V04, V14)=D |
| V06, V20 | V06 o-o V20 | V06   V20 (no edge) | V06   V20 (no edge) | V06   V20 (no edge) | V06   V20 (no edge) | no edge | (V06, V20)=D |
| V07, V11 | V07 o-> V11 | V07   V11 (no edge) | V07   V11 (no edge) | V07   V11 (no edge) | V07   V11 (no edge) | no edge | (V07, V11)=D |
| V08, V17 | V08 o-o V17 | V08   V17 (no edge) | V08   V17 (no edge) | V08   V17 (no edge) | V08   V17 (no edge) | V17 -> V08 | (V08, V17)=D |
| V10, V14 | V10 <-> V14 | V10   V14 (no edge) | V10   V14 (no edge) | V10   V14 (no edge) | V10   V14 (no edge) | no edge | (V10, V14)=D |
| V10, V15 | V10 <-> V15 | V10   V15 (no edge) | V10   V15 (no edge) | V10   V15 (no edge) | V10   V15 (no edge) | V10 -> V15 | (V10, V15)=D |
| V10, V16 | V16 o-> V10 | V10   V16 (no edge) | V10   V16 (no edge) | V10   V16 (no edge) | V10   V16 (no edge) | no edge | (V10, V16)=D |
| V11, V15 | V11 <-> V15 | V11   V15 (no edge) | V11   V15 (no edge) | V11   V15 (no edge) | V11   V15 (no edge) | V11 -> V15 | (V11, V15)=D |
| V11, V21 | V21->V11 | V21->V11 | V11->V21 | V11->V21 | V11->V21 | V11 -> V21 | (V11, V21)=A |
| V11, V22 | V11 <-> V22 | V11   V22 (no edge) | V11   V22 (no edge) | V11   V22 (no edge) | V11   V22 (no edge) | V22 -> V11 | (V11, V22)=D |
| V12, V22 | V12 <-> V22 | V12 <-> V22 | V12   V22 (no edge) | V12   V22 (no edge) | V12   V22 (no edge) | V22 -> V12 | (V12, V22)=C |
| V13, V19 | V13 ~~~ V19 | V13   V19 (no edge) | V13   V19 (no edge) | V13   V19 (no edge) | V13   V19 (no edge) | V19 -> V13 | (V13, V19)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
