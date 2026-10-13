# Edge lineage: 20261007T020436Z_b1_k43_r03_5d2382

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
| S0 algorithm output | 6 | 0.67 | 1.00 | 0.80 | 1 | 1 | 2 | 5 |
| S1 after bootstrap edits | 1 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 5 |
| S2 after LLM review | 3 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 7 |
| S3 after KCI pruning | 3 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 7 |
| S4 final (after cycle step) | 3 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 7 |

Scored against: reference graph dwd_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 5. Of the deleted, 2 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"A": 3, "C": 5, "D": 2}.
- LLM effect: added 3 (of which 1 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 3 edges; set by {"llm": 3}; 0 identical to the algorithm's output; 2 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Precipitation->Altitude | llm | no | 0.90 |
| Sunshine hours->Temperature | llm | no | 0.70 |
| Altitude->Temperature | llm | yes | 0.20 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Precipitation, Longitude | Precipitation <-> Longitude | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation -> Longitude | (Precipitation, Longitude)=C |
| Precipitation, Sunshine hours | Precipitation <-> Sunshine hours | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation -> Sunshine hours | (Precipitation, Sunshine hours)=D |
| Precipitation, Altitude | Precipitation   Altitude (no edge) | Precipitation   Altitude (no edge) | Precipitation->Altitude | Precipitation->Altitude | Precipitation->Altitude | no edge | (Precipitation, Altitude)=A |
| Precipitation, Temperature | Temperature->Precipitation | Precipitation   Temperature (no edge) | Precipitation   Temperature (no edge) | Precipitation   Temperature (no edge) | Precipitation   Temperature (no edge) | Precipitation -> Temperature | (Precipitation, Temperature)=D |
| Longitude, Altitude | Altitude->Longitude | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Altitude -> Longitude | (Longitude, Altitude)=C |
| Sunshine hours, Altitude | Altitude->Sunshine hours | Altitude->Sunshine hours | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | no edge | (Sunshine hours, Altitude)=C |
| Sunshine hours, Temperature | Sunshine hours   Temperature (no edge) | Sunshine hours   Temperature (no edge) | Sunshine hours->Temperature | Sunshine hours->Temperature | Sunshine hours->Temperature | no edge | (Sunshine hours, Temperature)=A |
| Altitude, Temperature | Altitude o-o Temperature | Altitude   Temperature (no edge) | Altitude->Temperature | Altitude->Temperature | Altitude->Temperature | no edge | (Altitude, Temperature)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
