# Edge lineage: 20261014T064022Z_ab06cc_q042_r01_bca118

Dataset `/research/datasets/suite_q1s2/q042/q042.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 25 | 0.84 | 0.53 | 0.65 | 4 | 1 | 16 | 40 |
| S1 after bootstrap edits | 9 | 0.89 | 0.20 | 0.33 | 4 | 0 | 4 | 37 |
| S2 after LLM review | 10 | 0.70 | 0.17 | 0.28 | 3 | 1 | 3 | 40 |
| S3 after KCI pruning | 10 | 0.70 | 0.17 | 0.28 | 3 | 1 | 3 | 40 |
| S4 final (after cycle step) | 10 | 0.70 | 0.17 | 0.28 | 3 | 1 | 3 | 40 |

Scored against: reference graph s2_04_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 16. Of the deleted, 11 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 5, "B": 2, "C": 19, "D": 274}.
- LLM effect: added 2 (of which 2 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 1.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 10 edges; set by {"algorithm (unchanged)": 7, "llm": 3}; 7 identical to the algorithm's output; 2 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02 o-> V12 | algorithm (unchanged) | yes | 0.00 |
| V12->V04 | algorithm (unchanged) | yes | 0.00 |
| V04->V17 | algorithm (unchanged) | yes | 0.20 |
| V06 <-> V17 | algorithm (unchanged) | yes | 0.05 |
| V09->V14 | algorithm (unchanged) | yes | 0.00 |
| V14->V10 | algorithm (unchanged) | yes | 0.35 |
| V10->V15 | llm | no | 1.00 |
| V14->V15 | llm | no | 1.00 |
| V14 <-> V17 | algorithm (unchanged) | yes | 0.25 |
| V15->V23 | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V23 | V01 o-> V23 | V01   V23 (no edge) | V01   V23 (no edge) | V01   V23 (no edge) | V01   V23 (no edge) | V01 -> V23 | (V01, V23)=D |
| V03, V17 | V03 o-> V17 | V03   V17 (no edge) | V03   V17 (no edge) | V03   V17 (no edge) | V03   V17 (no edge) | V03 -> V17 | (V03, V17)=D |
| V05, V16 | V05 o-> V16 | V05   V16 (no edge) | V05   V16 (no edge) | V05   V16 (no edge) | V05   V16 (no edge) | V05 -> V16 | (V05, V16)=D |
| V06, V09 | V06->V09 | V06   V09 (no edge) | V06   V09 (no edge) | V06   V09 (no edge) | V06   V09 (no edge) | V09 -> V06 | (V06, V09)=D |
| V06, V19 | V19 o-> V06 | V06   V19 (no edge) | V06   V19 (no edge) | V06   V19 (no edge) | V06   V19 (no edge) | V19 -> V06 | (V06, V19)=D |
| V07, V12 | V07 o-> V12 | V07   V12 (no edge) | V07   V12 (no edge) | V07   V12 (no edge) | V07   V12 (no edge) | V07 -> V12 | (V07, V12)=D |
| V08, V10 | V08 <-> V10 | V08   V10 (no edge) | V08   V10 (no edge) | V08   V10 (no edge) | V08   V10 (no edge) | V08 -> V10 | (V08, V10)=D |
| V08, V14 | V08 <-> V14 | V08   V14 (no edge) | V08   V14 (no edge) | V08   V14 (no edge) | V08   V14 (no edge) | V08 -> V14 | (V08, V14)=D |
| V09, V17 | V09 <-> V17 | V09   V17 (no edge) | V09   V17 (no edge) | V09   V17 (no edge) | V09   V17 (no edge) | no edge | (V09, V17)=D |
| V09, V24 | V09 <-> V24 | V09   V24 (no edge) | V09   V24 (no edge) | V09   V24 (no edge) | V09   V24 (no edge) | V09 -> V24 | (V09, V24)=D |
| V10, V15 | V10   V15 (no edge) | V10   V15 (no edge) | V10->V15 | V10->V15 | V10->V15 | no edge | (V10, V15)=A |
| V10, V17 | V10 <-> V17 | V10 <-> V17 | V10   V17 (no edge) | V10   V17 (no edge) | V10   V17 (no edge) | V17 -> V10 | (V10, V17)=C |
| V11, V16 | V11 <-> V16 | V11   V16 (no edge) | V11   V16 (no edge) | V11   V16 (no edge) | V11   V16 (no edge) | V11 -> V16 | (V11, V16)=D |
| V11, V17 | V11 <-> V17 | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | no edge | (V11, V17)=D |
| V13, V24 | V13 o-> V24 | V13   V24 (no edge) | V13   V24 (no edge) | V13   V24 (no edge) | V13   V24 (no edge) | V13 -> V24 | (V13, V24)=D |
| V14, V15 | V14   V15 (no edge) | V14   V15 (no edge) | V14->V15 | V14->V15 | V14->V15 | no edge | (V14, V15)=A |
| V15, V16 | V15 <-> V16 | V15   V16 (no edge) | V15   V16 (no edge) | V15   V16 (no edge) | V15   V16 (no edge) | V16 -> V15 | (V15, V16)=D |
| V15, V23 | V23->V15 | V23->V15 | V15->V23 | V15->V23 | V15->V23 | V23 -> V15 | (V15, V23)=A |
| V16, V22 | V22 o-> V16 | V16   V22 (no edge) | V16   V22 (no edge) | V16   V22 (no edge) | V16   V22 (no edge) | no edge | (V16, V22)=D |
| V18, V23 | V18 o-> V23 | V18   V23 (no edge) | V18   V23 (no edge) | V18   V23 (no edge) | V18   V23 (no edge) | V18 -> V23 | (V18, V23)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
