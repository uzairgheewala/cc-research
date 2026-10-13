# Edge lineage: 20261011T235711Z_s2_q102_r01_3f4438

Dataset `/research/datasets/suite_q1s2/q102/q102.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 23 | 0.74 | 0.38 | 0.50 | 5 | 2 | 10 | 47 |
| S1 after bootstrap edits | 9 | 1.00 | 0.20 | 0.33 | 5 | 1 | 3 | 41 |
| S2 after LLM review | 9 | 1.00 | 0.20 | 0.33 | 5 | 1 | 3 | 41 |
| S3 after KCI pruning | 9 | 1.00 | 0.20 | 0.33 | 5 | 1 | 3 | 41 |
| S4 final (after cycle step) | 9 | 1.00 | 0.20 | 0.33 | 5 | 1 | 3 | 41 |

Scored against: reference graph s2_10_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 14. Of the deleted, 2 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"D": 300}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 9 edges; set by {"algorithm (unchanged)": 9}; 9 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V14->V02 | algorithm (unchanged) | yes | 0.20 |
| V02->V24 | algorithm (unchanged) | yes | 0.10 |
| V20->V04 | algorithm (unchanged) | yes | 0.00 |
| V05->V19 | algorithm (unchanged) | yes | 0.00 |
| V15 o-> V07 | algorithm (unchanged) | yes | 0.00 |
| V07 <-> V20 | algorithm (unchanged) | yes | 0.00 |
| V14 o-> V11 | algorithm (unchanged) | yes | 0.00 |
| V20->V16 | algorithm (unchanged) | yes | 0.10 |
| V23->V24 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V02, V11 | V11->V02 | V02   V11 (no edge) | V02   V11 (no edge) | V02   V11 (no edge) | V02   V11 (no edge) | no edge | (V02, V11)=D |
| V04, V07 | V04 <-> V07 | V04   V07 (no edge) | V04   V07 (no edge) | V04   V07 (no edge) | V04   V07 (no edge) | V04 -> V07 | (V04, V07)=D |
| V05, V09 | V05 <-> V09 | V05   V09 (no edge) | V05   V09 (no edge) | V05   V09 (no edge) | V05   V09 (no edge) | no edge | (V05, V09)=D |
| V05, V16 | V05 <-> V16 | V05   V16 (no edge) | V05   V16 (no edge) | V05   V16 (no edge) | V05   V16 (no edge) | V16 -> V05 | (V05, V16)=D |
| V05, V18 | V18 o-> V05 | V05   V18 (no edge) | V05   V18 (no edge) | V05   V18 (no edge) | V05   V18 (no edge) | V18 -> V05 | (V05, V18)=D |
| V06, V11 | V06 o-> V11 | V06   V11 (no edge) | V06   V11 (no edge) | V06   V11 (no edge) | V06   V11 (no edge) | V06 -> V11 | (V06, V11)=D |
| V06, V14 | V06 o-o V14 | V06   V14 (no edge) | V06   V14 (no edge) | V06   V14 (no edge) | V06   V14 (no edge) | V14 -> V06 | (V06, V14)=D |
| V09, V19 | V09 <-> V19 | V09   V19 (no edge) | V09   V19 (no edge) | V09   V19 (no edge) | V09   V19 (no edge) | no edge | (V09, V19)=D |
| V10, V23 | V10 o-o V23 | V10   V23 (no edge) | V10   V23 (no edge) | V10   V23 (no edge) | V10   V23 (no edge) | V10 -> V23 | (V10, V23)=D |
| V11, V17 | V17 o-> V11 | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V17 -> V11 | (V11, V17)=D |
| V12, V22 | V12 o-> V22 | V12   V22 (no edge) | V12   V22 (no edge) | V12   V22 (no edge) | V12   V22 (no edge) | no edge | (V12, V22)=D |
| V16, V21 | V21->V16 | V16   V21 (no edge) | V16   V21 (no edge) | V16   V21 (no edge) | V16   V21 (no edge) | V16 -> V21 | (V16, V21)=D |
| V20, V21 | V21 o-> V20 | V20   V21 (no edge) | V20   V21 (no edge) | V20   V21 (no edge) | V20   V21 (no edge) | no edge | (V20, V21)=D |
| V22, V24 | V22 <-> V24 | V22   V24 (no edge) | V22   V24 (no edge) | V22   V24 (no edge) | V22   V24 (no edge) | no edge | (V22, V24)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
