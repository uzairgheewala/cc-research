# Edge lineage: 20261014T011246Z_ab06cc_q052_r01_4d1722

Dataset `/research/datasets/suite_q1s2/q052/q052.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 20 variables, 190 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 18 | 0.83 | 0.39 | 0.54 | 2 | 0 | 13 | 39 |
| S1 after bootstrap edits | 4 | 0.75 | 0.08 | 0.14 | 1 | 0 | 2 | 38 |
| S2 after LLM review | 3 | 1.00 | 0.08 | 0.15 | 1 | 0 | 2 | 37 |
| S3 after KCI pruning | 3 | 1.00 | 0.08 | 0.15 | 1 | 0 | 2 | 37 |
| S4 final (after cycle step) | 3 | 1.00 | 0.08 | 0.15 | 1 | 0 | 2 | 37 |

Scored against: reference graph s2_05_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 14. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 20 calls, 190 distinct pairs answered out of 190, plus 20 self-pairs. Letters: {"A": 1, "C": 11, "D": 178}.
- LLM effect: added 0 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 3 edges; set by {"algorithm (unchanged)": 3}; 3 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V02 <-> V15 | algorithm (unchanged) | yes | 0.10 |
| V09->V11 | algorithm (unchanged) | yes | 0.50 |
| V10 ~~~ V18 | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V01, V02 | V01 <-> V02 | V01   V02 (no edge) | V01   V02 (no edge) | V01   V02 (no edge) | V01   V02 (no edge) | V01 -> V02 | (V01, V02)=D |
| V01, V03 | V01 <-> V03 | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | V01   V03 (no edge) | no edge | (V01, V03)=D |
| V03, V05 | V03 <-> V05 | V03   V05 (no edge) | V03   V05 (no edge) | V03   V05 (no edge) | V03   V05 (no edge) | V03 -> V05 | (V03, V05)=D |
| V03, V14 | V14 o-> V03 | V03   V14 (no edge) | V03   V14 (no edge) | V03   V14 (no edge) | V03   V14 (no edge) | V14 -> V03 | (V03, V14)=D |
| V04, V08 | V08 o-> V04 | V04   V08 (no edge) | V04   V08 (no edge) | V04   V08 (no edge) | V04   V08 (no edge) | V08 -> V04 | (V04, V08)=D |
| V04, V15 | V04 <-> V15 | V04   V15 (no edge) | V04   V15 (no edge) | V04   V15 (no edge) | V04   V15 (no edge) | V15 -> V04 | (V04, V15)=D |
| V04, V20 | V20->V04 | V04   V20 (no edge) | V04   V20 (no edge) | V04   V20 (no edge) | V04   V20 (no edge) | no edge | (V04, V20)=D |
| V05, V20 | V05 <-> V20 | V05   V20 (no edge) | V05   V20 (no edge) | V05   V20 (no edge) | V05   V20 (no edge) | V20 -> V05 | (V05, V20)=D |
| V06, V12 | V06 o-o V12 | V06   V12 (no edge) | V06   V12 (no edge) | V06   V12 (no edge) | V06   V12 (no edge) | V06 -> V12 | (V06, V12)=D |
| V06, V15 | V06->V15 | V06   V15 (no edge) | V06   V15 (no edge) | V06   V15 (no edge) | V06   V15 (no edge) | V06 -> V15 | (V06, V15)=D |
| V09, V10 | V10 o-> V09 | V10 o-> V09 | V09   V10 (no edge) | V09   V10 (no edge) | V09   V10 (no edge) | no edge | (V09, V10)=C |
| V09, V18 | V18 o-> V09 | V09   V18 (no edge) | V09   V18 (no edge) | V09   V18 (no edge) | V09   V18 (no edge) | V18 -> V09 | (V09, V18)=C |
| V09, V19 | V19 o-> V09 | V09   V19 (no edge) | V09   V19 (no edge) | V09   V19 (no edge) | V09   V19 (no edge) | V19 -> V09 | (V09, V19)=C |
| V11, V17 | V17 o-> V11 | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V11   V17 (no edge) | V17 -> V11 | (V11, V17)=D |
| V15, V20 | V15 <-> V20 | V15   V20 (no edge) | V15   V20 (no edge) | V15   V20 (no edge) | V15   V20 (no edge) | V20 -> V15 | (V15, V20)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
