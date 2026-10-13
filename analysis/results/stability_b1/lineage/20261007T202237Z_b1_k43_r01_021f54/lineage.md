# Edge lineage: 20261007T202237Z_b1_k43_r01_021f54

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
| S0 algorithm output | 5 | 0.80 | 1.00 | 0.89 | 0 | 1 | 3 | 5 |
| S1 after bootstrap edits | 3 | 0.67 | 0.50 | 0.57 | 0 | 1 | 1 | 5 |
| S2 after LLM review | 5 | 0.40 | 0.50 | 0.44 | 0 | 1 | 1 | 7 |
| S3 after KCI pruning | 5 | 0.40 | 0.50 | 0.44 | 0 | 1 | 1 | 7 |
| S4 final (after cycle step) | 5 | 0.40 | 0.50 | 0.44 | 0 | 1 | 1 | 7 |

Scored against: reference graph dwd_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 2. Of the deleted, 1 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"A": 2, "B": 2, "C": 5, "D": 1}.
- LLM effect: added 4 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 5 edges; set by {"algorithm (unchanged)": 1, "llm": 4}; 1 identical to the algorithm's output; 3 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Precipitation <-> Sunshine hours | algorithm (unchanged) | yes | 0.00 |
| Altitude->Precipitation | llm | no | 0.80 |
| Temperature->Precipitation | llm | yes | 0.20 |
| Sunshine hours->Temperature | llm | no | 0.75 |
| Altitude->Temperature | llm | no | 0.25 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Precipitation, Longitude | Longitude->Precipitation | Longitude->Precipitation | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation -> Longitude | (Precipitation, Longitude)=C |
| Precipitation, Altitude | Precipitation   Altitude (no edge) | Precipitation   Altitude (no edge) | Altitude->Precipitation | Altitude->Precipitation | Altitude->Precipitation | no edge | (Precipitation, Altitude)=B |
| Precipitation, Temperature | Temperature o-> Precipitation | Precipitation   Temperature (no edge) | Temperature->Precipitation | Temperature->Precipitation | Temperature->Precipitation | Precipitation -> Temperature | (Precipitation, Temperature)=B |
| Longitude, Altitude | Longitude o-o Altitude | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Longitude   Altitude (no edge) | Altitude -> Longitude | (Longitude, Altitude)=C |
| Sunshine hours, Altitude | Altitude->Sunshine hours | Altitude->Sunshine hours | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | Sunshine hours   Altitude (no edge) | no edge | (Sunshine hours, Altitude)=C |
| Sunshine hours, Temperature | Sunshine hours   Temperature (no edge) | Sunshine hours   Temperature (no edge) | Sunshine hours->Temperature | Sunshine hours->Temperature | Sunshine hours->Temperature | no edge | (Sunshine hours, Temperature)=A |
| Altitude, Temperature | Altitude   Temperature (no edge) | Altitude   Temperature (no edge) | Altitude->Temperature | Altitude->Temperature | Altitude->Temperature | no edge | (Altitude, Temperature)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
