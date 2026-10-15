# Edge lineage: 20261014T033650Z_ab06cc_q092_r01_06cc95

Dataset `/research/datasets/suite_q1s2/q092/q092.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 25 | 0.84 | 0.60 | 0.70 | 7 | 1 | 13 | 32 |
| S1 after bootstrap edits | 12 | 0.83 | 0.29 | 0.43 | 7 | 0 | 3 | 30 |
| S2 after LLM review | 14 | 0.71 | 0.29 | 0.41 | 6 | 1 | 3 | 33 |
| S3 after KCI pruning | 14 | 0.71 | 0.29 | 0.41 | 6 | 1 | 3 | 33 |
| S4 final (after cycle step) | 14 | 0.71 | 0.29 | 0.41 | 6 | 1 | 3 | 33 |

Scored against: reference graph s2_09_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 13. Of the deleted, 7 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 10, "C": 11, "D": 210}.
- LLM effect: added 2 (of which 2 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 2.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 14 edges; set by {"algorithm (unchanged)": 10, "llm": 4}; 10 identical to the algorithm's output; 2 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V01->V11 | algorithm (unchanged) | yes | 0.10 |
| V01->V12 | algorithm (unchanged) | yes | 0.60 |
| V01->V16 | algorithm (unchanged) | yes | 0.00 |
| V21 o-> V02 | algorithm (unchanged) | yes | 0.25 |
| V03->V17 | llm | yes | 0.35 |
| V04 o-> V17 | algorithm (unchanged) | yes | 0.00 |
| V05->V15 | algorithm (unchanged) | yes | 0.00 |
| V05->V19 | llm | no | 1.00 |
| V21 o-> V09 | algorithm (unchanged) | yes | 0.00 |
| V22 o-> V09 | algorithm (unchanged) | yes | 0.00 |
| V13->V17 | algorithm (unchanged) | yes | 0.00 |
| V15->V19 | llm | yes | 0.00 |
| V16->V19 | algorithm (unchanged) | yes | 0.10 |
| V17->V19 | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V13 | V01 o-o V13 | V01   V13 (no edge) | V01   V13 (no edge) | V01   V13 (no edge) | V01   V13 (no edge) | V01 -> V13 | (V01, V13)=D |
| V02, V09 | V02 o-o V09 | V02   V09 (no edge) | V02   V09 (no edge) | V02   V09 (no edge) | V02   V09 (no edge) | no edge | (V02, V09)=D |
| V02, V22 | V22 o-> V02 | V02   V22 (no edge) | V02   V22 (no edge) | V02   V22 (no edge) | V02   V22 (no edge) | V22 -> V02 | (V02, V22)=D |
| V03, V17 | V17->V03 | V17->V03 | V03->V17 | V03->V17 | V03->V17 | no edge | (V03, V17)=A |
| V04, V12 | V04 o-> V12 | V04   V12 (no edge) | V04   V12 (no edge) | V04   V12 (no edge) | V04   V12 (no edge) | V04 -> V12 | (V04, V12)=D |
| V05, V08 | V05 o-o V08 | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | V08 -> V05 | (V05, V08)=D |
| V05, V19 | V05   V19 (no edge) | V05   V19 (no edge) | V05->V19 | V05->V19 | V05->V19 | no edge | (V05, V19)=A |
| V06, V11 | V06 <-> V11 | V06   V11 (no edge) | V06   V11 (no edge) | V06   V11 (no edge) | V06   V11 (no edge) | V11 -> V06 | (V06, V11)=D |
| V06, V20 | V06->V20 | V06   V20 (no edge) | V06   V20 (no edge) | V06   V20 (no edge) | V06   V20 (no edge) | V20 -> V06 | (V06, V20)=D |
| V06, V21 | V21 o-> V06 | V06   V21 (no edge) | V06   V21 (no edge) | V06   V21 (no edge) | V06   V21 (no edge) | V06 -> V21 | (V06, V21)=D |
| V10, V15 | V10 o-> V15 | V10   V15 (no edge) | V10   V15 (no edge) | V10   V15 (no edge) | V10   V15 (no edge) | V10 -> V15 | (V10, V15)=D |
| V11, V20 | V11 <-> V20 | V11   V20 (no edge) | V11   V20 (no edge) | V11   V20 (no edge) | V11   V20 (no edge) | V20 -> V11 | (V11, V20)=C |
| V14, V19 | V14 o-> V19 | V14   V19 (no edge) | V14   V19 (no edge) | V14   V19 (no edge) | V14   V19 (no edge) | V14 -> V19 | (V14, V19)=D |
| V15, V19 | V19->V15 | V19->V15 | V15->V19 | V15->V19 | V15->V19 | V19 -> V15 | (V15, V19)=A |
| V16, V18 | V16 <-> V18 | V16   V18 (no edge) | V16   V18 (no edge) | V16   V18 (no edge) | V16   V18 (no edge) | V18 -> V16 | (V16, V18)=D |
| V17, V19 | V17   V19 (no edge) | V17   V19 (no edge) | V17->V19 | V17->V19 | V17->V19 | no edge | (V17, V19)=A |
| V18, V19 | V18 <-> V19 | V18   V19 (no edge) | V18   V19 (no edge) | V18   V19 (no edge) | V18   V19 (no edge) | no edge | (V18, V19)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
