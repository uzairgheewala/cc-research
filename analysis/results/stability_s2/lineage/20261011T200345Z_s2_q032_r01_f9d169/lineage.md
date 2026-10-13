# Edge lineage: 20261011T200345Z_s2_q032_r01_f9d169

Dataset `/research/datasets/suite_q1s2/q032/q032.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 25 | 0.72 | 0.31 | 0.43 | 2 | 0 | 16 | 63 |
| S1 after bootstrap edits | 6 | 0.67 | 0.07 | 0.12 | 1 | 0 | 3 | 59 |
| S2 after LLM review | 6 | 0.67 | 0.07 | 0.12 | 1 | 0 | 3 | 59 |
| S3 after KCI pruning | 6 | 0.67 | 0.07 | 0.12 | 1 | 0 | 3 | 59 |
| S4 final (after cycle step) | 6 | 0.67 | 0.07 | 0.12 | 1 | 0 | 3 | 59 |

Scored against: reference graph s2_03_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 19. Of the deleted, 6 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"D": 300}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 6 edges; set by {"algorithm (unchanged)": 6}; 6 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02 o-> V24 | algorithm (unchanged) | yes | 0.00 |
| V10 o-> V03 | algorithm (unchanged) | yes | 0.00 |
| V08 o-o V17 | algorithm (unchanged) | yes | 0.15 |
| V09 o-> V22 | algorithm (unchanged) | yes | 0.15 |
| V16 o-o V18 | algorithm (unchanged) | yes | 0.35 |
| V24->V19 | algorithm (unchanged) | yes | 0.15 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V03 | V01 <-> V03 | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V01 -> V03 | (V01, V03)=D |
| V01, V07 | V01 <-> V07 | V01   V07 (no edge) | V01   V07 (no edge) | V01   V07 (no edge) | V01   V07 (no edge) | V01 -> V07 | (V01, V07)=D |
| V02, V19 | V02->V19 | V02   V19 (no edge) | V02   V19 (no edge) | V02   V19 (no edge) | V02   V19 (no edge) | V02 -> V19 | (V02, V19)=D |
| V03, V15 | V15 o-> V03 | V03   V15 (no edge) | V03   V15 (no edge) | V03   V15 (no edge) | V03   V15 (no edge) | V15 -> V03 | (V03, V15)=D |
| V03, V16 | V16 o-> V03 | V03   V16 (no edge) | V03   V16 (no edge) | V03   V16 (no edge) | V03   V16 (no edge) | no edge | (V03, V16)=D |
| V03, V18 | V18 o-> V03 | V03   V18 (no edge) | V03   V18 (no edge) | V03   V18 (no edge) | V03   V18 (no edge) | no edge | (V03, V18)=D |
| V03, V23 | V23 o-> V03 | V03   V23 (no edge) | V03   V23 (no edge) | V03   V23 (no edge) | V03   V23 (no edge) | no edge | (V03, V23)=D |
| V04, V17 | V04 o-o V17 | V04   V17 (no edge) | V04   V17 (no edge) | V04   V17 (no edge) | V04   V17 (no edge) | V17 -> V04 | (V04, V17)=D |
| V04, V25 | V04 o-o V25 | V04   V25 (no edge) | V04   V25 (no edge) | V04   V25 (no edge) | V04   V25 (no edge) | V25 -> V04 | (V04, V25)=D |
| V07, V09 | V09 o-> V07 | V07   V09 (no edge) | V07   V09 (no edge) | V07   V09 (no edge) | V07   V09 (no edge) | V09 -> V07 | (V07, V09)=D |
| V10, V18 | V10 o-o V18 | V10   V18 (no edge) | V10   V18 (no edge) | V10   V18 (no edge) | V10   V18 (no edge) | no edge | (V10, V18)=D |
| V10, V23 | V10 o-o V23 | V10   V23 (no edge) | V10   V23 (no edge) | V10   V23 (no edge) | V10   V23 (no edge) | no edge | (V10, V23)=D |
| V11, V22 | V11 o-> V22 | V11   V22 (no edge) | V11   V22 (no edge) | V11   V22 (no edge) | V11   V22 (no edge) | V22 -> V11 | (V11, V22)=D |
| V12, V22 | V12 o-> V22 | V12   V22 (no edge) | V12   V22 (no edge) | V12   V22 (no edge) | V12   V22 (no edge) | V12 -> V22 | (V12, V22)=D |
| V14, V19 | V14 o-> V19 | V14   V19 (no edge) | V14   V19 (no edge) | V14   V19 (no edge) | V14   V19 (no edge) | V14 -> V19 | (V14, V19)=D |
| V15, V16 | V15 o-o V16 | V15   V16 (no edge) | V15   V16 (no edge) | V15   V16 (no edge) | V15   V16 (no edge) | V15 -> V16 | (V15, V16)=D |
| V19, V21 | V21 o-> V19 | V19   V21 (no edge) | V19   V21 (no edge) | V19   V21 (no edge) | V19   V21 (no edge) | V21 -> V19 | (V19, V21)=D |
| V20, V22 | V20 o-> V22 | V20   V22 (no edge) | V20   V22 (no edge) | V20   V22 (no edge) | V20   V22 (no edge) | V20 -> V22 | (V20, V22)=D |
| V22, V24 | V22 <-> V24 | V22   V24 (no edge) | V22   V24 (no edge) | V22   V24 (no edge) | V22   V24 (no edge) | V22 -> V24 | (V22, V24)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
