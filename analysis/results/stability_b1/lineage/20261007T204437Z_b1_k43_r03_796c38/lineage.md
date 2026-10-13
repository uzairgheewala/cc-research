# Edge lineage: 20261007T204437Z_b1_k43_r03_796c38

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
| S0 algorithm output | 8 | 0.50 | 1.00 | 0.67 | 0 | 0 | 4 | 8 |
| S1 after bootstrap edits | 1 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 5 |
| S2 after LLM review | 4 | 0.25 | 0.25 | 0.25 | 0 | 1 | 0 | 7 |
| S3 after KCI pruning | 4 | 0.25 | 0.25 | 0.25 | 0 | 1 | 0 | 7 |
| S4 final (after cycle step) | 4 | 0.25 | 0.25 | 0.25 | 0 | 1 | 0 | 7 |

Scored against: reference graph dwd_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 7. Of the deleted, 3 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"A": 2, "B": 2, "C": 6}.
- LLM effect: added 3 (of which 1 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 1.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 4 edges; set by {"llm": 4}; 0 identical to the algorithm's output; 1 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Altitude->Precipitation | llm | yes | 1.00 |
| Temperature->Precipitation | llm | yes | 0.15 |
| Sunshine hours->Temperature | llm | no | 0.75 |
| Altitude->Temperature | llm | yes | 0.10 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Precipitation, Longitude | Longitude o-> Precipitation | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation -> Longitude | (Precipitation, Longitude)=C |
| Precipitation, Sunshine hours | Sunshine hours o-> Precipitation | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation   Sunshine hours (no edge) | Precipitation -> Sunshine hours | (Precipitation, Sunshine hours)=C |
| Precipitation, Altitude | Altitude o-> Precipitation | Precipitation   Altitude (no edge) | Altitude->Precipitation | Altitude->Precipitation | Altitude->Precipitation | no edge | (Precipitation, Altitude)=B |
| Precipitation, Temperature | Temperature o-> Precipitation | Precipitation   Temperature (no edge) | Temperature->Precipitation | Temperature->Precipitation | Temperature->Precipitation | Precipitation -> Temperature | (Precipitation, Temperature)=B |
| Longitude, Sunshine hours | Longitude o-o Sunshine hours | Longitude   Sunshine hours (no edge) | Longitude   Sunshine hours (no edge) | Longitude   Sunshine hours (no edge) | Longitude   Sunshine hours (no edge) | no edge | (Longitude, Sunshine hours)=C |
| Longitude, Altitude | Longitude o-o Altitude | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Altitude -> Longitude | (Longitude, Altitude)=C |
| Sunshine hours, Altitude | Sunshine hours o-o Altitude | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | no edge | (Sunshine hours, Altitude)=C |
| Sunshine hours, Temperature | Sunshine hours   Temperature (no edge) | Sunshine hours   Temperature (no edge) | Sunshine hours->Temperature | Sunshine hours->Temperature | Sunshine hours->Temperature | no edge | (Sunshine hours, Temperature)=A |
| Altitude, Temperature | Altitude o-o Temperature | Altitude o-o Temperature | Altitude->Temperature | Altitude->Temperature | Altitude->Temperature | no edge | (Altitude, Temperature)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
