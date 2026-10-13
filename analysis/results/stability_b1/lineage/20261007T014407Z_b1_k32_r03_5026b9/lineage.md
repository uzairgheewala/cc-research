# Edge lineage: 20261007T014407Z_b1_k32_r03_5026b9

Dataset `/research/datasets/suite_b1/k32/k32.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 6}. 9 variables, 36 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 17 | 0.24 | 0.50 | 0.32 | 1 | 0 | 3 | 20 |
| S1 after bootstrap edits | 5 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 13 |
| S2 after LLM review | 5 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 13 |
| S3 after KCI pruning | 5 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 13 |
| S4 final (after cycle step) | 5 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 13 |

Scored against: reference graph concrete_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 12. Of the deleted, 7 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 9 calls, 36 distinct pairs answered out of 36, plus 9 self-pairs. Letters: {"D": 36}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 5 edges; set by {"algorithm (unchanged)": 5}; 5 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V03->V01 | algorithm (unchanged) | yes | 0.05 |
| V01 <-> V06 | algorithm (unchanged) | yes | 0.40 |
| V02 <-> V07 | algorithm (unchanged) | yes | 0.00 |
| V03 <-> V05 | algorithm (unchanged) | yes | 0.00 |
| V04->V05 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V02 | V01 <-> V02 | V01   V02 (no edge) | V01   V02 (no edge) | V01   V02 (no edge) | V01   V02 (no edge) | no edge | (V01, V02)=D |
| V01, V07 | V01 <-> V07 | V01   V07 (no edge) | V01   V07 (no edge) | V01   V07 (no edge) | V01   V07 (no edge) | no edge | (V01, V07)=D |
| V01, V09 | V01 <-> V09 | V01   V09 (no edge) | V01   V09 (no edge) | V01   V09 (no edge) | V01   V09 (no edge) | V01 -> V09 | (V01, V09)=D |
| V02, V03 | V02 <-> V03 | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | no edge | (V02, V03)=D |
| V02, V06 | V02->V06 | V02   V06 (no edge) | V02   V06 (no edge) | V02   V06 (no edge) | V02   V06 (no edge) | no edge | (V02, V06)=D |
| V03, V09 | V03->V09 | V03   V09 (no edge) | V03   V09 (no edge) | V03   V09 (no edge) | V03   V09 (no edge) | V03 -> V09 | (V03, V09)=D |
| V04, V06 | V04 <-> V06 | V04   V06 (no edge) | V04   V06 (no edge) | V04   V06 (no edge) | V04   V06 (no edge) | no edge | (V04, V06)=D |
| V04, V07 | V04 <-> V07 | V04   V07 (no edge) | V04   V07 (no edge) | V04   V07 (no edge) | V04   V07 (no edge) | no edge | (V04, V07)=D |
| V04, V09 | V04 <-> V09 | V04   V09 (no edge) | V04   V09 (no edge) | V04   V09 (no edge) | V04   V09 (no edge) | V04 -> V09 | (V04, V09)=D |
| V05, V06 | V05 <-> V06 | V05   V06 (no edge) | V05   V06 (no edge) | V05   V06 (no edge) | V05   V06 (no edge) | no edge | (V05, V06)=D |
| V06, V07 | V07->V06 | V06   V07 (no edge) | V06   V07 (no edge) | V06   V07 (no edge) | V06   V07 (no edge) | no edge | (V06, V07)=D |
| V08, V09 | V08 o-> V09 | V08   V09 (no edge) | V08   V09 (no edge) | V08   V09 (no edge) | V08   V09 (no edge) | V08 -> V09 | (V08, V09)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
