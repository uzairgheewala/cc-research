# Edge lineage: 20261013T213848Z_ab06cc_q022_r01_eda1bc

Dataset `/research/datasets/suite_q1s2/q022/q022.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 21 variables, 210 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 22 | 0.82 | 0.47 | 0.60 | 3 | 0 | 15 | 40 |
| S1 after bootstrap edits | 6 | 1.00 | 0.16 | 0.27 | 3 | 0 | 3 | 36 |
| S2 after LLM review | 7 | 0.86 | 0.16 | 0.27 | 2 | 1 | 3 | 38 |
| S3 after KCI pruning | 7 | 0.86 | 0.16 | 0.27 | 2 | 1 | 3 | 38 |
| S4 final (after cycle step) | 7 | 0.86 | 0.16 | 0.27 | 2 | 1 | 3 | 38 |

Scored against: reference graph s2_02_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 16. Of the deleted, 9 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 21 calls, 210 distinct pairs answered out of 210, plus 21 self-pairs. Letters: {"A": 3, "B": 1, "D": 206}.
- LLM effect: added 1 (of which 1 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 1.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 7 edges; set by {"algorithm (unchanged)": 5, "llm": 2}; 5 identical to the algorithm's output; 1 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V01 o-> V06 | algorithm (unchanged) | yes | 0.00 |
| V03 o-> V12 | algorithm (unchanged) | yes | 0.05 |
| V03 o-> V14 | algorithm (unchanged) | yes | 0.00 |
| V05->V06 | llm | no | 0.95 |
| V15->V05 | algorithm (unchanged) | yes | 0.00 |
| V06->V09 | algorithm (unchanged) | yes | 0.00 |
| V14->V16 | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V02 | V01 o-o V02 | V01   V02 (no edge) | V01   V02 (no edge) | V01   V02 (no edge) | V01   V02 (no edge) | V01 -> V02 | (V01, V02)=D |
| V02, V06 | V02 o-> V06 | V02   V06 (no edge) | V02   V06 (no edge) | V02   V06 (no edge) | V02   V06 (no edge) | no edge | (V02, V06)=D |
| V03, V09 | V03 o-> V09 | V03   V09 (no edge) | V03   V09 (no edge) | V03   V09 (no edge) | V03   V09 (no edge) | V03 -> V09 | (V03, V09)=D |
| V04, V21 | V04 o-> V21 | V04   V21 (no edge) | V04   V21 (no edge) | V04   V21 (no edge) | V04   V21 (no edge) | no edge | (V04, V21)=D |
| V05, V06 | V05   V06 (no edge) | V05   V06 (no edge) | V05->V06 | V05->V06 | V05->V06 | no edge | (V05, V06)=A |
| V05, V12 | V05 <-> V12 | V05   V12 (no edge) | V05   V12 (no edge) | V05   V12 (no edge) | V05   V12 (no edge) | V05 -> V12 | (V05, V12)=D |
| V06, V15 | V06 <-> V15 | V06   V15 (no edge) | V06   V15 (no edge) | V06   V15 (no edge) | V06   V15 (no edge) | V15 -> V06 | (V06, V15)=D |
| V07, V13 | V07 o-o V13 | V07   V13 (no edge) | V07   V13 (no edge) | V07   V13 (no edge) | V07   V13 (no edge) | V07 -> V13 | (V07, V13)=D |
| V07, V17 | V07 o-o V17 | V07   V17 (no edge) | V07   V17 (no edge) | V07   V17 (no edge) | V07   V17 (no edge) | V07 -> V17 | (V07, V17)=D |
| V08, V19 | V08 o-> V19 | V08   V19 (no edge) | V08   V19 (no edge) | V08   V19 (no edge) | V08   V19 (no edge) | V08 -> V19 | (V08, V19)=D |
| V10, V11 | V10 <-> V11 | V10   V11 (no edge) | V10   V11 (no edge) | V10   V11 (no edge) | V10   V11 (no edge) | V10 -> V11 | (V10, V11)=D |
| V10, V20 | V10 <-> V20 | V10   V20 (no edge) | V10   V20 (no edge) | V10   V20 (no edge) | V10   V20 (no edge) | no edge | (V10, V20)=D |
| V11, V16 | V11 <-> V16 | V11   V16 (no edge) | V11   V16 (no edge) | V11   V16 (no edge) | V11   V16 (no edge) | V16 -> V11 | (V11, V16)=D |
| V14, V16 | V16->V14 | V16->V14 | V14->V16 | V14->V16 | V14->V16 | V16 -> V14 | (V14, V16)=A |
| V15, V20 | V15 <-> V20 | V15   V20 (no edge) | V15   V20 (no edge) | V15   V20 (no edge) | V15   V20 (no edge) | V20 -> V15 | (V15, V20)=D |
| V16, V19 | V16 <-> V19 | V16   V19 (no edge) | V16   V19 (no edge) | V16   V19 (no edge) | V16   V19 (no edge) | V16 -> V19 | (V16, V19)=D |
| V18, V19 | V18 o-> V19 | V18   V19 (no edge) | V18   V19 (no edge) | V18   V19 (no edge) | V18   V19 (no edge) | V18 -> V19 | (V18, V19)=D |
| V20, V21 | V20 <-> V21 | V20   V21 (no edge) | V20   V21 (no edge) | V20   V21 (no edge) | V20   V21 (no edge) | no edge | (V20, V21)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
