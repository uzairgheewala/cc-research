# Edge lineage: 20261007T011831Z_b1_k12_r03_9f711f

Dataset `/research/datasets/suite_b1/k12/k12.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": -1}. 8 variables, 28 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 14 | 0.21 | 0.43 | 0.29 | 1 | 0 | 2 | 18 |
| S1 after bootstrap edits | 6 | 0.17 | 0.14 | 0.15 | 0 | 0 | 1 | 12 |
| S2 after LLM review | 6 | 0.17 | 0.14 | 0.15 | 0 | 0 | 1 | 12 |
| S3 after KCI pruning | 6 | 0.17 | 0.14 | 0.15 | 0 | 0 | 1 | 12 |
| S4 final (after cycle step) | 6 | 0.17 | 0.14 | 0.15 | 0 | 0 | 1 | 12 |

Scored against: reference graph abalone_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 8. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 8 calls, 28 distinct pairs answered out of 28, plus 8 self-pairs. Letters: {"D": 28}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 6 edges; set by {"algorithm (unchanged)": 6}; 6 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V01 <-> V08 | algorithm (unchanged) | yes | 0.10 |
| V03 o-> V02 | algorithm (unchanged) | yes | 0.00 |
| V02 <-> V06 | algorithm (unchanged) | yes | 0.60 |
| V03 o-> V08 | algorithm (unchanged) | yes | 0.00 |
| V05 <-> V07 | algorithm (unchanged) | yes | 0.00 |
| V06->V07 | algorithm (unchanged) | yes | 0.40 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V04 | V01->V04 | V01   V04 (no edge) | V01   V04 (no edge) | V01   V04 (no edge) | V01   V04 (no edge) | V01 -> V04 | (V01, V04)=D |
| V01, V06 | V01 <-> V06 | V01   V06 (no edge) | V01   V06 (no edge) | V01   V06 (no edge) | V01   V06 (no edge) | V01 -> V06 | (V01, V06)=D |
| V02, V05 | V02->V05 | V02   V05 (no edge) | V02   V05 (no edge) | V02   V05 (no edge) | V02   V05 (no edge) | no edge | (V02, V05)=D |
| V02, V07 | V02 <-> V07 | V02   V07 (no edge) | V02   V07 (no edge) | V02   V07 (no edge) | V02   V07 (no edge) | no edge | (V02, V07)=D |
| V04, V08 | V04 <-> V08 | V04   V08 (no edge) | V04   V08 (no edge) | V04   V08 (no edge) | V04   V08 (no edge) | no edge | (V04, V08)=D |
| V05, V06 | V05 <-> V06 | V05   V06 (no edge) | V05   V06 (no edge) | V05   V06 (no edge) | V05   V06 (no edge) | no edge | (V05, V06)=D |
| V05, V08 | V05 <-> V08 | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | V05   V08 (no edge) | no edge | (V05, V08)=D |
| V07, V08 | V07 <-> V08 | V07   V08 (no edge) | V07   V08 (no edge) | V07   V08 (no edge) | V07   V08 (no edge) | no edge | (V07, V08)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
