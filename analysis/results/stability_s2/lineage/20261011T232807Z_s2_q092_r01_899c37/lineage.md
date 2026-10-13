# Edge lineage: 20261011T232807Z_s2_q092_r01_899c37

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
| S0 algorithm output | 23 | 0.91 | 0.60 | 0.72 | 7 | 2 | 12 | 30 |
| S1 after bootstrap edits | 15 | 0.87 | 0.37 | 0.52 | 7 | 1 | 5 | 30 |
| S2 after LLM review | 15 | 0.87 | 0.37 | 0.52 | 7 | 1 | 5 | 30 |
| S3 after KCI pruning | 15 | 0.87 | 0.37 | 0.52 | 7 | 1 | 5 | 30 |
| S4 final (after cycle step) | 15 | 0.87 | 0.37 | 0.52 | 7 | 1 | 5 | 30 |

Scored against: reference graph s2_09_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 8. Of the deleted, 6 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"D": 231}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 15 edges; set by {"algorithm (unchanged)": 15}; 15 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V01->V11 | algorithm (unchanged) | yes | 0.00 |
| V01->V12 | algorithm (unchanged) | yes | 0.45 |
| V01->V16 | algorithm (unchanged) | yes | 0.00 |
| V21 o-> V02 | algorithm (unchanged) | yes | 0.20 |
| V17->V03 | algorithm (unchanged) | yes | 0.30 |
| V04 o-> V17 | algorithm (unchanged) | yes | 0.05 |
| V05->V15 | algorithm (unchanged) | yes | 0.00 |
| V06->V20 | algorithm (unchanged) | yes | 0.00 |
| V21 o-> V09 | algorithm (unchanged) | yes | 0.00 |
| V22 o-> V09 | algorithm (unchanged) | yes | 0.00 |
| V11 <-> V20 | algorithm (unchanged) | yes | 0.00 |
| V13->V17 | algorithm (unchanged) | yes | 0.00 |
| V19->V15 | algorithm (unchanged) | yes | 0.00 |
| V18 o-> V16 | algorithm (unchanged) | yes | 0.00 |
| V16->V19 | algorithm (unchanged) | yes | 0.15 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V13 | V01 o-o V13 | V01   V13 (no edge) | V01   V13 (no edge) | V01   V13 (no edge) | V01   V13 (no edge) | V01 -> V13 | (V01, V13)=D |
| V02, V22 | V22 o-> V02 | V02   V22 (no edge) | V02   V22 (no edge) | V02   V22 (no edge) | V02   V22 (no edge) | V22 -> V02 | (V02, V22)=D |
| V04, V12 | V04 o-> V12 | V04   V12 (no edge) | V04   V12 (no edge) | V04   V12 (no edge) | V04   V12 (no edge) | V04 -> V12 | (V04, V12)=D |
| V05, V08 | V05 o-o V08 | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | V08 -> V05 | (V05, V08)=D |
| V06, V11 | V06 <-> V11 | V06   V11 (no edge) | V06   V11 (no edge) | V06   V11 (no edge) | V06   V11 (no edge) | V11 -> V06 | (V06, V11)=D |
| V06, V21 | V21 o-> V06 | V06   V21 (no edge) | V06   V21 (no edge) | V06   V21 (no edge) | V06   V21 (no edge) | V06 -> V21 | (V06, V21)=D |
| V10, V15 | V10 o-> V15 | V10   V15 (no edge) | V10   V15 (no edge) | V10   V15 (no edge) | V10   V15 (no edge) | V10 -> V15 | (V10, V15)=D |
| V14, V19 | V19->V14 | V14   V19 (no edge) | V14   V19 (no edge) | V14   V19 (no edge) | V14   V19 (no edge) | V14 -> V19 | (V14, V19)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
