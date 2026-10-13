# Edge lineage: 20261006T235454Z_b1_k41_r01_d0fac0

Dataset `/research/datasets/suite_b1/k41/k41.csv`, algorithm **FCI** {"alpha": 0.1, "indep_test": "rcit", "depth": 6}. 5 variables, 10 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 7 | 0.57 | 1.00 | 0.73 | 0 | 0 | 4 | 7 |
| S1 after bootstrap edits | 1 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 5 |
| S2 after LLM review | 3 | 0.67 | 0.50 | 0.57 | 2 | 0 | 0 | 4 |
| S3 after KCI pruning | 3 | 0.67 | 0.50 | 0.57 | 2 | 0 | 0 | 4 |
| S4 final (after cycle step) | 3 | 0.67 | 0.50 | 0.57 | 2 | 0 | 0 | 4 |

Scored against: reference graph dwd_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 6. Of the deleted, 2 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"A": 2, "B": 1, "C": 6, "D": 1}.
- LLM effect: added 3 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 3 edges; set by {"llm": 3}; 0 identical to the algorithm's output; 1 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Altitude->Temperature | llm | yes | 0.05 |
| Altitude->Precipitation | llm | yes | 0.05 |
| Sunshine hours->Temperature | llm | no | 0.80 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Altitude, Temperature | Temperature o-> Altitude | Altitude   Temperature (no edge) | Altitude->Temperature | Altitude->Temperature | Altitude->Temperature | Altitude -> Temperature | (Altitude, Temperature)=A |
| Altitude, Precipitation | Altitude <-> Precipitation | Altitude   Precipitation (no edge) | Altitude->Precipitation | Altitude->Precipitation | Altitude->Precipitation | Altitude -> Precipitation | (Altitude, Precipitation)=A |
| Altitude, Sunshine hours | Sunshine hours o-> Altitude | Altitude   Sunshine hours (no edge) | Altitude   Sunshine hours (no edge) | Altitude   Sunshine hours (no edge) | Altitude   Sunshine hours (no edge) | Altitude -> Sunshine hours | (Altitude, Sunshine hours)=C |
| Temperature, Precipitation | Temperature o-> Precipitation | Temperature   Precipitation (no edge) | Temperature   Precipitation (no edge) | Temperature   Precipitation (no edge) | Temperature   Precipitation (no edge) | no edge | (Temperature, Precipitation)=D |
| Temperature, Longitude | Temperature o-> Longitude | Temperature   Longitude (no edge) | Temperature   Longitude (no edge) | Temperature   Longitude (no edge) | Temperature   Longitude (no edge) | Longitude -> Temperature | (Temperature, Longitude)=C |
| Temperature, Sunshine hours | Temperature   Sunshine hours (no edge) | Temperature   Sunshine hours (no edge) | Sunshine hours->Temperature | Sunshine hours->Temperature | Sunshine hours->Temperature | no edge | (Temperature, Sunshine hours)=B |
| Precipitation, Longitude | Precipitation <-> Longitude | Precipitation <-> Longitude | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | Precipitation   Longitude (no edge) | no edge | (Precipitation, Longitude)=C |
| Longitude, Sunshine hours | Sunshine hours o-> Longitude | Longitude   Sunshine hours (no edge) | Longitude   Sunshine hours (no edge) | Longitude   Sunshine hours (no edge) | Longitude   Sunshine hours (no edge) | no edge | (Longitude, Sunshine hours)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
