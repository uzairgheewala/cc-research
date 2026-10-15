# Edge lineage: 20261014T015338Z_ab06cc_q062_r01_84b6d7

Dataset `/research/datasets/suite_q1s2/q062/q062.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

Hyperparameters the LLM proposed that were not passed to the algorithm: ['background_knowledge']

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
| S0 algorithm output | 20 | 0.85 | 0.36 | 0.51 | 5 | 0 | 12 | 47 |
| S1 after bootstrap edits | 6 | 0.83 | 0.11 | 0.19 | 4 | 0 | 1 | 46 |
| S2 after LLM review | 13 | 0.38 | 0.11 | 0.17 | 5 | 0 | 0 | 52 |
| S3 after KCI pruning | 13 | 0.38 | 0.11 | 0.17 | 5 | 0 | 0 | 52 |
| S4 final (after cycle step) | 13 | 0.38 | 0.11 | 0.17 | 5 | 0 | 0 | 52 |

Scored against: reference graph s2_06_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 14. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 10, "B": 3, "C": 98, "D": 189}.
- LLM effect: added 9 (of which 7 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 13 edges; set by {"algorithm (unchanged)": 4, "llm": 9}; 4 identical to the algorithm's output; 8 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V04->V11 | algorithm (unchanged) | yes | 0.65 |
| V04->V18 | llm | no | 1.00 |
| V05->V11 | llm | no | 0.40 |
| V05->V18 | algorithm (unchanged) | yes | 0.70 |
| V06->V18 | llm | no | 1.00 |
| V08->V07 | algorithm (unchanged) | yes | 0.35 |
| V08->V11 | llm | yes | 0.00 |
| V08->V18 | llm | no | 1.00 |
| V08->V20 | algorithm (unchanged) | yes | 0.00 |
| V11->V18 | llm | no | 1.00 |
| V20->V11 | llm | no | 0.95 |
| V16->V20 | llm | no | 1.00 |
| V20->V18 | llm | no | 0.95 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V02, V14 | V02 o-> V14 | V02   V14 (no edge) | V02   V14 (no edge) | V02   V14 (no edge) | V02   V14 (no edge) | no edge | (V02, V14)=D |
| V02, V22 | V02 o-> V22 | V02   V22 (no edge) | V02   V22 (no edge) | V02   V22 (no edge) | V02   V22 (no edge) | V02 -> V22 | (V02, V22)=D |
| V03, V16 | V03 ~~~ V16 | V03   V16 (no edge) | V03   V16 (no edge) | V03   V16 (no edge) | V03   V16 (no edge) | V03 -> V16 | (V03, V16)=C |
| V03, V19 | V03 ~~~ V19 | V03   V19 (no edge) | V03   V19 (no edge) | V03   V19 (no edge) | V03   V19 (no edge) | V19 -> V03 | (V03, V19)=C |
| V04, V18 | V04   V18 (no edge) | V04   V18 (no edge) | V04->V18 | V04->V18 | V04->V18 | no edge | (V04, V18)=A |
| V04, V25 | V04 o-o V25 | V04 o-o V25 | V04   V25 (no edge) | V04   V25 (no edge) | V04   V25 (no edge) | V25 -> V04 | (V04, V25)=C |
| V05, V08 | V08->V05 | V08->V05 | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | V08 -> V05 | (V05, V08)=C |
| V05, V11 | V05   V11 (no edge) | V05   V11 (no edge) | V05->V11 | V05->V11 | V05->V11 | no edge | (V05, V11)=A |
| V06, V15 | V06 o-o V15 | V06   V15 (no edge) | V06   V15 (no edge) | V06   V15 (no edge) | V06   V15 (no edge) | V15 -> V06 | (V06, V15)=D |
| V06, V18 | V06   V18 (no edge) | V06   V18 (no edge) | V06->V18 | V06->V18 | V06->V18 | no edge | (V06, V18)=A |
| V07, V18 | V07 <-> V18 | V07   V18 (no edge) | V07   V18 (no edge) | V07   V18 (no edge) | V07   V18 (no edge) | V07 -> V18 | (V07, V18)=C |
| V08, V09 | V09 o-> V08 | V08   V09 (no edge) | V08   V09 (no edge) | V08   V09 (no edge) | V08   V09 (no edge) | V08 -> V09 | (V08, V09)=D |
| V08, V11 | V08 <-> V11 | V08   V11 (no edge) | V08->V11 | V08->V11 | V08->V11 | V08 -> V11 | (V08, V11)=A |
| V08, V18 | V08   V18 (no edge) | V08   V18 (no edge) | V08->V18 | V08->V18 | V08->V18 | no edge | (V08, V18)=A |
| V11, V18 | V11   V18 (no edge) | V11   V18 (no edge) | V11->V18 | V11->V18 | V11->V18 | no edge | (V11, V18)=A |
| V11, V20 | V11   V20 (no edge) | V11   V20 (no edge) | V20->V11 | V20->V11 | V20->V11 | no edge | (V11, V20)=B |
| V12, V21 | V12 o-> V21 | V12   V21 (no edge) | V12   V21 (no edge) | V12   V21 (no edge) | V12   V21 (no edge) | V12 -> V21 | (V12, V21)=D |
| V13, V18 | V13 o-> V18 | V13   V18 (no edge) | V13   V18 (no edge) | V13   V18 (no edge) | V13   V18 (no edge) | V13 -> V18 | (V13, V18)=D |
| V14, V18 | V18->V14 | V14   V18 (no edge) | V14   V18 (no edge) | V14   V18 (no edge) | V14   V18 (no edge) | V18 -> V14 | (V14, V18)=D |
| V14, V22 | V14 ~~~ V22 | V14   V22 (no edge) | V14   V22 (no edge) | V14   V22 (no edge) | V14   V22 (no edge) | V14 -> V22 | (V14, V22)=D |
| V16, V20 | V16   V20 (no edge) | V16   V20 (no edge) | V16->V20 | V16->V20 | V16->V20 | no edge | (V16, V20)=A |
| V18, V20 | V18   V20 (no edge) | V18   V20 (no edge) | V20->V18 | V20->V18 | V20->V18 | V20 -> V18 | (V18, V20)=B |
| V18, V22 | V18->V22 | V18   V22 (no edge) | V18   V22 (no edge) | V18   V22 (no edge) | V18   V22 (no edge) | no edge | (V18, V22)=C |
| V21, V23 | V23 o-> V21 | V21   V23 (no edge) | V21   V23 (no edge) | V21   V23 (no edge) | V21   V23 (no edge) | V23 -> V21 | (V21, V23)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
