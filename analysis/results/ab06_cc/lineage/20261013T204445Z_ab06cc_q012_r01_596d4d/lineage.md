# Edge lineage: 20261013T204445Z_ab06cc_q012_r01_596d4d

Dataset `/research/datasets/suite_q1s2/q012/q012.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 23 variables, 253 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 27 | 0.78 | 0.54 | 0.64 | 3 | 2 | 16 | 43 |
| S1 after bootstrap edits | 10 | 1.00 | 0.26 | 0.41 | 2 | 2 | 6 | 38 |
| S2 after LLM review | 9 | 1.00 | 0.23 | 0.38 | 3 | 1 | 5 | 37 |
| S3 after KCI pruning | 9 | 1.00 | 0.23 | 0.38 | 3 | 1 | 5 | 37 |
| S4 final (after cycle step) | 9 | 1.00 | 0.23 | 0.38 | 3 | 1 | 5 | 37 |

Scored against: reference graph s2_01_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 17. Of the deleted, 9 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 23 calls, 253 distinct pairs answered out of 253, plus 23 self-pairs. Letters: {"A": 3, "C": 30, "D": 220}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 3.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 9 edges; set by {"algorithm (unchanged)": 6, "llm": 3}; 6 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V01 o-> V04 | algorithm (unchanged) | yes | 0.00 |
| V01 o-> V18 | algorithm (unchanged) | yes | 0.00 |
| V03 ~~~ V16 | algorithm (unchanged) | yes | 0.00 |
| V05->V08 | llm | yes | 0.00 |
| V10->V15 | llm | yes | 0.45 |
| V10->V19 | llm | yes | 0.05 |
| V12 <-> V13 | algorithm (unchanged) | yes | 0.15 |
| V22->V13 | algorithm (unchanged) | yes | 0.00 |
| V16 o-> V20 | algorithm (unchanged) | yes | 0.25 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V02, V06 | V02 <-> V06 | V02   V06 (no edge) | V02   V06 (no edge) | V02   V06 (no edge) | V02   V06 (no edge) | V02 -> V06 | (V02, V06)=D |
| V02, V18 | V02 <-> V18 | V02   V18 (no edge) | V02   V18 (no edge) | V02   V18 (no edge) | V02   V18 (no edge) | no edge | (V02, V18)=D |
| V03, V15 | V03 o-o V15 | V03   V15 (no edge) | V03   V15 (no edge) | V03   V15 (no edge) | V03   V15 (no edge) | no edge | (V03, V15)=D |
| V03, V20 | V03 o-> V20 | V03   V20 (no edge) | V03   V20 (no edge) | V03   V20 (no edge) | V03   V20 (no edge) | no edge | (V03, V20)=D |
| V04, V17 | V04 <-> V17 | V04   V17 (no edge) | V04   V17 (no edge) | V04   V17 (no edge) | V04   V17 (no edge) | V17 -> V04 | (V04, V17)=D |
| V04, V23 | V23 o-> V04 | V04   V23 (no edge) | V04   V23 (no edge) | V04   V23 (no edge) | V04   V23 (no edge) | V23 -> V04 | (V04, V23)=D |
| V05, V08 | V08->V05 | V08->V05 | V05->V08 | V05->V08 | V05->V08 | V05 -> V08 | (V05, V08)=A |
| V05, V17 | V05 <-> V17 | V05   V17 (no edge) | V05   V17 (no edge) | V05   V17 (no edge) | V05   V17 (no edge) | V17 -> V05 | (V05, V17)=D |
| V06, V09 | V06 <-> V09 | V06   V09 (no edge) | V06   V09 (no edge) | V06   V09 (no edge) | V06   V09 (no edge) | V09 -> V06 | (V06, V09)=D |
| V07, V10 | V07->V10 | V07   V10 (no edge) | V07   V10 (no edge) | V07   V10 (no edge) | V07   V10 (no edge) | V07 -> V10 | (V07, V10)=D |
| V07, V22 | V07 o-o V22 | V07   V22 (no edge) | V07   V22 (no edge) | V07   V22 (no edge) | V07   V22 (no edge) | V22 -> V07 | (V07, V22)=D |
| V08, V19 | V08 o-o V19 | V08 o-o V19 | V08   V19 (no edge) | V08   V19 (no edge) | V08   V19 (no edge) | V19 -> V08 | (V08, V19)=C |
| V09, V18 | V09 <-> V18 | V09   V18 (no edge) | V09   V18 (no edge) | V09   V18 (no edge) | V09   V18 (no edge) | no edge | (V09, V18)=D |
| V10, V15 | V15->V10 | V15->V10 | V10->V15 | V10->V15 | V10->V15 | V10 -> V15 | (V10, V15)=A |
| V10, V19 | V19->V10 | V19->V10 | V10->V19 | V10->V19 | V10->V19 | V19 -> V10 | (V10, V19)=A |
| V11, V17 | V11 o-> V17 | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V17 -> V11 | (V11, V17)=D |
| V12, V20 | V12 <-> V20 | V12   V20 (no edge) | V12   V20 (no edge) | V12   V20 (no edge) | V12   V20 (no edge) | no edge | (V12, V20)=D |
| V14, V18 | V14 o-> V18 | V14   V18 (no edge) | V14   V18 (no edge) | V14   V18 (no edge) | V14   V18 (no edge) | V18 -> V14 | (V14, V18)=D |
| V15, V16 | V15 o-o V16 | V15   V16 (no edge) | V15   V16 (no edge) | V15   V16 (no edge) | V15   V16 (no edge) | V15 -> V16 | (V15, V16)=D |
| V15, V20 | V15 o-> V20 | V15   V20 (no edge) | V15   V20 (no edge) | V15   V20 (no edge) | V15   V20 (no edge) | no edge | (V15, V20)=D |
| V19, V21 | V19 o-o V21 | V19   V21 (no edge) | V19   V21 (no edge) | V19   V21 (no edge) | V19   V21 (no edge) | V21 -> V19 | (V19, V21)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
