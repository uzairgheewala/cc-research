# Edge lineage: 20261011T213825Z_s2_q062_r01_e40c58

Dataset `/research/datasets/suite_q1s2/q062/q062.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 18 | 0.83 | 0.32 | 0.46 | 3 | 0 | 12 | 49 |
| S1 after bootstrap edits | 4 | 0.75 | 0.06 | 0.12 | 3 | 0 | 0 | 47 |
| S2 after LLM review | 4 | 0.75 | 0.06 | 0.12 | 3 | 0 | 0 | 47 |
| S3 after KCI pruning | 4 | 0.75 | 0.06 | 0.12 | 3 | 0 | 0 | 47 |
| S4 final (after cycle step) | 4 | 0.75 | 0.06 | 0.12 | 3 | 0 | 0 | 47 |

Scored against: reference graph s2_06_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 1, deleted 14. Of the deleted, 6 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"D": 300}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 4 edges; set by {"algorithm (unchanged)": 4}; 4 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V05 o-o V09 | algorithm (unchanged) | yes | 0.50 |
| V08->V07 | algorithm (unchanged) | yes | 0.35 |
| V08->V20 | algorithm (unchanged) | yes | 0.00 |
| V18->V14 | algorithm (unchanged) | yes | 0.80 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V03, V16 | V03 ~~~ V16 | V03   V16 (no edge) | V03   V16 (no edge) | V03   V16 (no edge) | V03   V16 (no edge) | V03 -> V16 | (V03, V16)=D |
| V03, V19 | V03 ~~~ V19 | V03   V19 (no edge) | V03   V19 (no edge) | V03   V19 (no edge) | V03   V19 (no edge) | V19 -> V03 | (V03, V19)=D |
| V04, V25 | V04 o-o V25 | V04   V25 (no edge) | V04   V25 (no edge) | V04   V25 (no edge) | V04   V25 (no edge) | V25 -> V04 | (V04, V25)=D |
| V05, V08 | V05 o-> V08 | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | V08 -> V05 | (V05, V08)=D |
| V05, V11 | V05 o-o V11 | V05   V11 (no edge) | V05   V11 (no edge) | V05   V11 (no edge) | V05   V11 (no edge) | no edge | (V05, V11)=D |
| V06, V15 | V06 o-o V15 | V06   V15 (no edge) | V06   V15 (no edge) | V06   V15 (no edge) | V06   V15 (no edge) | V15 -> V06 | (V06, V15)=D |
| V07, V18 | V07 <-> V18 | V07   V18 (no edge) | V07   V18 (no edge) | V07   V18 (no edge) | V07   V18 (no edge) | V07 -> V18 | (V07, V18)=D |
| V08, V09 | V09 o-> V08 | V08   V09 (no edge) | V08   V09 (no edge) | V08   V09 (no edge) | V08   V09 (no edge) | V08 -> V09 | (V08, V09)=D |
| V08, V11 | V11 o-> V08 | V08   V11 (no edge) | V08   V11 (no edge) | V08   V11 (no edge) | V08   V11 (no edge) | V08 -> V11 | (V08, V11)=D |
| V12, V21 | V12 o-> V21 | V12   V21 (no edge) | V12   V21 (no edge) | V12   V21 (no edge) | V12   V21 (no edge) | V12 -> V21 | (V12, V21)=D |
| V13, V18 | V13 o-> V18 | V13   V18 (no edge) | V13   V18 (no edge) | V13   V18 (no edge) | V13   V18 (no edge) | V13 -> V18 | (V13, V18)=D |
| V14, V22 | V14 ~~~ V22 | V14   V22 (no edge) | V14   V22 (no edge) | V14   V22 (no edge) | V14   V22 (no edge) | V14 -> V22 | (V14, V22)=D |
| V18, V22 | V18->V22 | V18   V22 (no edge) | V18   V22 (no edge) | V18   V22 (no edge) | V18   V22 (no edge) | no edge | (V18, V22)=D |
| V21, V23 | V23 o-> V21 | V21   V23 (no edge) | V21   V23 (no edge) | V21   V23 (no edge) | V21   V23 (no edge) | V23 -> V21 | (V21, V23)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
