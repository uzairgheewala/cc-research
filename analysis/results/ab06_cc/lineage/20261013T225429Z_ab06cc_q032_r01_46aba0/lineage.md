# Edge lineage: 20261013T225429Z_ab06cc_q032_r01_46aba0

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
| S0 algorithm output | 31 | 0.71 | 0.38 | 0.49 | 3 | 1 | 18 | 64 |
| S1 after bootstrap edits | 13 | 0.62 | 0.14 | 0.23 | 2 | 1 | 5 | 61 |
| S2 after LLM review | 13 | 0.62 | 0.14 | 0.23 | 2 | 1 | 5 | 61 |
| S3 after KCI pruning | 13 | 0.62 | 0.14 | 0.23 | 2 | 1 | 5 | 61 |
| S4 final (after cycle step) | 13 | 0.62 | 0.14 | 0.23 | 2 | 1 | 5 | 61 |

Scored against: reference graph s2_03_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 18. Of the deleted, 7 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 2, "B": 1, "C": 1, "D": 296}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 13 edges; set by {"algorithm (unchanged)": 13}; 13 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02 <-> V19 | algorithm (unchanged) | yes | 0.35 |
| V03 <-> V10 | algorithm (unchanged) | yes | 0.00 |
| V03 <-> V16 | algorithm (unchanged) | yes | 0.25 |
| V03->V23 | algorithm (unchanged) | yes | 0.15 |
| V09 o-> V07 | algorithm (unchanged) | yes | 0.15 |
| V17->V08 | algorithm (unchanged) | yes | 0.15 |
| V09 o-> V22 | algorithm (unchanged) | yes | 0.15 |
| V10 o-> V15 | algorithm (unchanged) | yes | 0.05 |
| V10->V18 | algorithm (unchanged) | yes | 0.10 |
| V22->V11 | algorithm (unchanged) | yes | 0.00 |
| V15->V16 | algorithm (unchanged) | yes | 0.25 |
| V18->V16 | algorithm (unchanged) | yes | 0.10 |
| V19 <-> V24 | algorithm (unchanged) | yes | 0.10 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V03 | V01 o-> V03 | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V01 -> V03 | (V01, V03)=D |
| V01, V07 | V01 o-> V07 | V01   V07 (no edge) | V01   V07 (no edge) | V01   V07 (no edge) | V01   V07 (no edge) | V01 -> V07 | (V01, V07)=D |
| V02, V08 | V02 <-> V08 | V02   V08 (no edge) | V02   V08 (no edge) | V02   V08 (no edge) | V02   V08 (no edge) | V08 -> V02 | (V02, V08)=D |
| V02, V24 | V02->V24 | V02   V24 (no edge) | V02   V24 (no edge) | V02   V24 (no edge) | V02   V24 (no edge) | V02 -> V24 | (V02, V24)=D |
| V03, V15 | V03 <-> V15 | V03   V15 (no edge) | V03   V15 (no edge) | V03   V15 (no edge) | V03   V15 (no edge) | V15 -> V03 | (V03, V15)=D |
| V03, V18 | V03 <-> V18 | V03   V18 (no edge) | V03   V18 (no edge) | V03   V18 (no edge) | V03   V18 (no edge) | no edge | (V03, V18)=D |
| V04, V17 | V04 o-o V17 | V04   V17 (no edge) | V04   V17 (no edge) | V04   V17 (no edge) | V04   V17 (no edge) | V17 -> V04 | (V04, V17)=D |
| V04, V25 | V04 o-o V25 | V04   V25 (no edge) | V04   V25 (no edge) | V04   V25 (no edge) | V04   V25 (no edge) | V25 -> V04 | (V04, V25)=D |
| V05, V07 | V05 o-> V07 | V05   V07 (no edge) | V05   V07 (no edge) | V05   V07 (no edge) | V05   V07 (no edge) | no edge | (V05, V07)=D |
| V10, V23 | V10 <-> V23 | V10   V23 (no edge) | V10   V23 (no edge) | V10   V23 (no edge) | V10   V23 (no edge) | no edge | (V10, V23)=D |
| V12, V22 | V12 o-> V22 | V12   V22 (no edge) | V12   V22 (no edge) | V12   V22 (no edge) | V12   V22 (no edge) | V12 -> V22 | (V12, V22)=D |
| V14, V19 | V14 o-> V19 | V14   V19 (no edge) | V14   V19 (no edge) | V14   V19 (no edge) | V14   V19 (no edge) | V14 -> V19 | (V14, V19)=D |
| V15, V18 | V18 o-> V15 | V15   V18 (no edge) | V15   V18 (no edge) | V15   V18 (no edge) | V15   V18 (no edge) | V15 -> V18 | (V15, V18)=D |
| V15, V23 | V15 <-> V23 | V15   V23 (no edge) | V15   V23 (no edge) | V15   V23 (no edge) | V15   V23 (no edge) | V15 -> V23 | (V15, V23)=D |
| V16, V23 | V16 <-> V23 | V16   V23 (no edge) | V16   V23 (no edge) | V16   V23 (no edge) | V16   V23 (no edge) | no edge | (V16, V23)=D |
| V19, V21 | V21 o-> V19 | V19   V21 (no edge) | V19   V21 (no edge) | V19   V21 (no edge) | V19   V21 (no edge) | V21 -> V19 | (V19, V21)=D |
| V20, V22 | V20 o-> V22 | V20   V22 (no edge) | V20   V22 (no edge) | V20   V22 (no edge) | V20   V22 (no edge) | V20 -> V22 | (V20, V22)=D |
| V22, V24 | V22 <-> V24 | V22   V24 (no edge) | V22   V24 (no edge) | V22   V24 (no edge) | V22   V24 (no edge) | V22 -> V24 | (V22, V24)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
