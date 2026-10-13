# Edge lineage: 20261011T221746Z_s2_q072_r01_f38486

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
| S1 after bootstrap edits | 9 | 0.89 | 0.23 | 0.36 | 6 | 0 | 2 | 31 |
| S2 after LLM review | 9 | 0.89 | 0.23 | 0.36 | 6 | 0 | 2 | 31 |
| S3 after KCI pruning | 9 | 0.89 | 0.23 | 0.36 | 6 | 0 | 2 | 31 |
| S4 final (after cycle step) | 9 | 0.89 | 0.23 | 0.36 | 6 | 0 | 2 | 31 |

Scored against: reference graph s2_07_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 18. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"D": 231}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 9 edges; set by {"algorithm (unchanged)": 9}; 9 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02->V03 | algorithm (unchanged) | yes | 0.00 |
| V10->V03 | algorithm (unchanged) | yes | 0.00 |
| V19 o-> V03 | algorithm (unchanged) | yes | 0.65 |
| V08->V11 | algorithm (unchanged) | yes | 0.05 |
| V09->V14 | algorithm (unchanged) | yes | 0.00 |
| V11 <-> V21 | algorithm (unchanged) | yes | 0.05 |
| V12->V14 | algorithm (unchanged) | yes | 0.00 |
| V12 <-> V22 | algorithm (unchanged) | yes | 0.05 |
| V17->V22 | algorithm (unchanged) | yes | 0.10 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V20 | V01 o-o V20 | V01   V20 (no edge) | V01   V20 (no edge) | V01   V20 (no edge) | V01   V20 (no edge) | V01 -> V20 | (V01, V20)=D |
| V01, V21 | V01->V21 | V01   V21 (no edge) | V01   V21 (no edge) | V01   V21 (no edge) | V01   V21 (no edge) | V21 -> V01 | (V01, V21)=D |
| V02, V10 | V02 ~~~ V10 | V02   V10 (no edge) | V02   V10 (no edge) | V02   V10 (no edge) | V02   V10 (no edge) | V02 -> V10 | (V02, V10)=D |
| V02, V14 | V02 <-> V14 | V02   V14 (no edge) | V02   V14 (no edge) | V02   V14 (no edge) | V02   V14 (no edge) | V14 -> V02 | (V02, V14)=D |
| V02, V15 | V02 <-> V15 | V02   V15 (no edge) | V02   V15 (no edge) | V02   V15 (no edge) | V02   V15 (no edge) | no edge | (V02, V15)=D |
| V02, V16 | V02 <-> V16 | V02   V16 (no edge) | V02   V16 (no edge) | V02   V16 (no edge) | V02   V16 (no edge) | V16 -> V02 | (V02, V16)=D |
| V03, V13 | V13 o-> V03 | V03   V13 (no edge) | V03   V13 (no edge) | V03   V13 (no edge) | V03   V13 (no edge) | V13 -> V03 | (V03, V13)=D |
| V04, V14 | V04 o-> V14 | V04   V14 (no edge) | V04   V14 (no edge) | V04   V14 (no edge) | V04   V14 (no edge) | V04 -> V14 | (V04, V14)=D |
| V05, V21 | V05 o-> V21 | V05   V21 (no edge) | V05   V21 (no edge) | V05   V21 (no edge) | V05   V21 (no edge) | no edge | (V05, V21)=D |
| V08, V17 | V08 o-o V17 | V08   V17 (no edge) | V08   V17 (no edge) | V08   V17 (no edge) | V08   V17 (no edge) | V17 -> V08 | (V08, V17)=D |
| V09, V12 | V09 o-> V12 | V09   V12 (no edge) | V09   V12 (no edge) | V09   V12 (no edge) | V09   V12 (no edge) | V09 -> V12 | (V09, V12)=D |
| V10, V14 | V10 <-> V14 | V10   V14 (no edge) | V10   V14 (no edge) | V10   V14 (no edge) | V10   V14 (no edge) | no edge | (V10, V14)=D |
| V10, V15 | V10 <-> V15 | V10   V15 (no edge) | V10   V15 (no edge) | V10   V15 (no edge) | V10   V15 (no edge) | V10 -> V15 | (V10, V15)=D |
| V10, V16 | V10 <-> V16 | V10   V16 (no edge) | V10   V16 (no edge) | V10   V16 (no edge) | V10   V16 (no edge) | no edge | (V10, V16)=D |
| V11, V15 | V11 <-> V15 | V11   V15 (no edge) | V11   V15 (no edge) | V11   V15 (no edge) | V11   V15 (no edge) | V11 -> V15 | (V11, V15)=D |
| V11, V22 | V11 <-> V22 | V11   V22 (no edge) | V11   V22 (no edge) | V11   V22 (no edge) | V11   V22 (no edge) | V22 -> V11 | (V11, V22)=D |
| V13, V19 | V13 ~~~ V19 | V13   V19 (no edge) | V13   V19 (no edge) | V13   V19 (no edge) | V13   V19 (no edge) | V19 -> V13 | (V13, V19)=D |
| V16, V21 | V16 <-> V21 | V16   V21 (no edge) | V16   V21 (no edge) | V16   V21 (no edge) | V16   V21 (no edge) | no edge | (V16, V21)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
