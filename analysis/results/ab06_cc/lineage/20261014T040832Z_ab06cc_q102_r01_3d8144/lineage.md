# Edge lineage: 20261014T040832Z_ab06cc_q102_r01_3d8144

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
| S0 algorithm output | 20 | 0.75 | 0.33 | 0.46 | 6 | 1 | 8 | 45 |
| S1 after bootstrap edits | 9 | 1.00 | 0.20 | 0.33 | 5 | 1 | 3 | 40 |
| S2 after LLM review | 10 | 0.90 | 0.20 | 0.33 | 5 | 1 | 3 | 41 |
| S3 after KCI pruning | 10 | 0.90 | 0.20 | 0.33 | 5 | 1 | 3 | 41 |
| S4 final (after cycle step) | 10 | 0.90 | 0.20 | 0.33 | 5 | 1 | 3 | 41 |

Scored against: reference graph s2_10_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 11. Of the deleted, 1 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 3, "B": 2, "D": 295}.
- LLM effect: added 1 (of which 1 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 10 edges; set by {"algorithm (unchanged)": 9, "llm": 1}; 9 identical to the algorithm's output; 1 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02 o-o V14 | algorithm (unchanged) | yes | 0.40 |
| V02->V24 | algorithm (unchanged) | yes | 0.10 |
| V04 o-o V20 | algorithm (unchanged) | yes | 0.00 |
| V05->V19 | algorithm (unchanged) | yes | 0.00 |
| V07->V06 | llm | no | 1.00 |
| V11->V06 | algorithm (unchanged) | yes | 0.00 |
| V20->V07 | algorithm (unchanged) | yes | 0.05 |
| V14->V11 | algorithm (unchanged) | yes | 0.00 |
| V16 o-o V20 | algorithm (unchanged) | yes | 0.35 |
| V23->V24 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V15 | V01 o-> V15 | V01   V15 (no edge) | V01   V15 (no edge) | V01   V15 (no edge) | V01   V15 (no edge) | no edge | (V01, V15)=D |
| V05, V09 | V05 <-> V09 | V05   V09 (no edge) | V05   V09 (no edge) | V05   V09 (no edge) | V05   V09 (no edge) | no edge | (V05, V09)=D |
| V05, V18 | V18 o-> V05 | V05   V18 (no edge) | V05   V18 (no edge) | V05   V18 (no edge) | V05   V18 (no edge) | V18 -> V05 | (V05, V18)=D |
| V06, V07 | V06   V07 (no edge) | V06   V07 (no edge) | V07->V06 | V07->V06 | V07->V06 | no edge | (V06, V07)=B |
| V06, V14 | V14->V06 | V06   V14 (no edge) | V06   V14 (no edge) | V06   V14 (no edge) | V06   V14 (no edge) | V14 -> V06 | (V06, V14)=D |
| V07, V15 | V07 <-> V15 | V07   V15 (no edge) | V07   V15 (no edge) | V07   V15 (no edge) | V07   V15 (no edge) | V15 -> V07 | (V07, V15)=D |
| V09, V19 | V09 <-> V19 | V09   V19 (no edge) | V09   V19 (no edge) | V09   V19 (no edge) | V09   V19 (no edge) | no edge | (V09, V19)=D |
| V09, V21 | V21->V09 | V09   V21 (no edge) | V09   V21 (no edge) | V09   V21 (no edge) | V09   V21 (no edge) | no edge | (V09, V21)=D |
| V10, V23 | V10 o-o V23 | V10   V23 (no edge) | V10   V23 (no edge) | V10   V23 (no edge) | V10   V23 (no edge) | V10 -> V23 | (V10, V23)=D |
| V11, V17 | V17 o-> V11 | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V17 -> V11 | (V11, V17)=D |
| V16, V21 | V16 o-o V21 | V16   V21 (no edge) | V16   V21 (no edge) | V16   V21 (no edge) | V16   V21 (no edge) | V16 -> V21 | (V16, V21)=D |
| V22, V24 | V22 o-> V24 | V22   V24 (no edge) | V22   V24 (no edge) | V22   V24 (no edge) | V22   V24 (no edge) | no edge | (V22, V24)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
