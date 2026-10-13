# Edge lineage: 20261007T010807Z_b1_k43_r02_713a73

Dataset `/research/datasets/suite_b1/k43/k43.csv`, algorithm **FCI** {"alpha": 0.1, "indep_test": "rcit", "depth": 6}. 5 variables, 10 pairs. 20 bootstrap resamples.

Hyperparameters the LLM proposed that were not passed to the algorithm: ['background_knowledge']

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
| S0 algorithm output | 6 | 0.50 | 0.75 | 0.60 | 0 | 0 | 3 | 7 |
| S1 after bootstrap edits | 3 | 0.33 | 0.25 | 0.29 | 0 | 0 | 1 | 6 |
| S2 after LLM review | 5 | 0.40 | 0.50 | 0.44 | 1 | 0 | 1 | 7 |
| S3 after KCI pruning | 5 | 0.40 | 0.50 | 0.44 | 1 | 0 | 1 | 7 |
| S4 final (after cycle step) | 5 | 0.40 | 0.50 | 0.44 | 1 | 0 | 1 | 7 |

Scored against: reference graph dwd_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 3. Of the deleted, 2 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"A": 4, "C": 4, "D": 2}.
- LLM effect: added 4 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 5 edges; set by {"llm": 4, "algorithm (unchanged)": 1}; 1 identical to the algorithm's output; 3 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Precipitation->Altitude | llm | no | 0.80 |
| Precipitation->Temperature | llm | no | 0.10 |
| Longitude <-> Altitude | algorithm (unchanged) | yes | 0.00 |
| Sunshine hours->Temperature | llm | no | 0.80 |
| Altitude->Temperature | llm | yes | 0.10 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Precipitation, Longitude | Precipitation o-> Longitude | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation -> Longitude | (Precipitation, Longitude)=C |
| Precipitation, Sunshine hours | Precipitation o-> Sunshine hours | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation -> Sunshine hours | (Precipitation, Sunshine hours)=C |
| Precipitation, Altitude | Precipitation   Altitude (no edge) | Precipitation   Altitude (no edge) | Precipitation->Altitude | Precipitation->Altitude | Precipitation->Altitude | no edge | (Precipitation, Altitude)=A |
| Precipitation, Temperature | Precipitation   Temperature (no edge) | Precipitation   Temperature (no edge) | Precipitation->Temperature | Precipitation->Temperature | Precipitation->Temperature | Precipitation -> Temperature | (Precipitation, Temperature)=A |
| Longitude, Sunshine hours | Longitude o-o Sunshine hours | Longitude o-o Sunshine hours | Longitude   Sunshine hours (no edge) | Longitude   Sunshine hours (no edge) | Longitude   Sunshine hours (no edge) | no edge | (Longitude, Sunshine hours)=C |
| Sunshine hours, Altitude | Sunshine hours <-> Altitude | Sunshine hours <-> Altitude | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | no edge | (Sunshine hours, Altitude)=C |
| Sunshine hours, Temperature | Sunshine hours   Temperature (no edge) | Sunshine hours   Temperature (no edge) | Sunshine hours->Temperature | Sunshine hours->Temperature | Sunshine hours->Temperature | no edge | (Sunshine hours, Temperature)=A |
| Altitude, Temperature | Temperature o-> Altitude | Altitude   Temperature (no edge) | Altitude->Temperature | Altitude->Temperature | Altitude->Temperature | no edge | (Altitude, Temperature)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
