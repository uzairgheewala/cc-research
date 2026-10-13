# Edge lineage: 20261006T233618Z_b1_k32_r01_65a2c4

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
| S0 algorithm output | 15 | 0.20 | 0.38 | 0.26 | 0 | 0 | 3 | 20 |
| S1 after bootstrap edits | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 16 |
| S2 after LLM review | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 16 |
| S3 after KCI pruning | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 16 |
| S4 final (after cycle step) | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 16 |

Scored against: reference graph concrete_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 7. Of the deleted, 4 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 9 calls, 36 distinct pairs answered out of 36, plus 9 self-pairs. Letters: {"D": 36}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 8 edges; set by {"algorithm (unchanged)": 8}; 8 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02 o-> V01 | algorithm (unchanged) | yes | 0.00 |
| V03 o-> V01 | algorithm (unchanged) | yes | 0.00 |
| V06 o-> V01 | algorithm (unchanged) | yes | 0.40 |
| V01 <-> V07 | algorithm (unchanged) | yes | 0.05 |
| V02 <-> V07 | algorithm (unchanged) | yes | 0.00 |
| V05 o-> V03 | algorithm (unchanged) | yes | 0.00 |
| V05 o-> V04 | algorithm (unchanged) | yes | 0.00 |
| V06 o-> V07 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V05 | V05 o-> V01 | V01   V05 (no edge) | V01   V05 (no edge) | V01   V05 (no edge) | V01   V05 (no edge) | no edge | (V01, V05)=D |
| V01, V09 | V01 <-> V09 | V01   V09 (no edge) | V01   V09 (no edge) | V01   V09 (no edge) | V01   V09 (no edge) | V01 -> V09 | (V01, V09)=D |
| V02, V03 | V02 <-> V03 | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | V02   V03 (no edge) | no edge | (V02, V03)=D |
| V04, V06 | V06 o-> V04 | V04   V06 (no edge) | V04   V06 (no edge) | V04   V06 (no edge) | V04   V06 (no edge) | no edge | (V04, V06)=D |
| V04, V07 | V04 <-> V07 | V04   V07 (no edge) | V04   V07 (no edge) | V04   V07 (no edge) | V04   V07 (no edge) | no edge | (V04, V07)=D |
| V04, V09 | V04 <-> V09 | V04   V09 (no edge) | V04   V09 (no edge) | V04   V09 (no edge) | V04   V09 (no edge) | V04 -> V09 | (V04, V09)=D |
| V08, V09 | V08 o-> V09 | V08   V09 (no edge) | V08   V09 (no edge) | V08   V09 (no edge) | V08   V09 (no edge) | V08 -> V09 | (V08, V09)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
