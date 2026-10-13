# Edge lineage: 20261007T015157Z_b1_k33_r03_3f6b3e

Dataset `/research/datasets/suite_b1/k33/k33.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 6}. 9 variables, 36 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 15 | 0.27 | 0.50 | 0.35 | 0 | 0 | 4 | 19 |
| S1 after bootstrap edits | 6 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 14 |
| S2 after LLM review | 10 | 0.10 | 0.12 | 0.11 | 1 | 0 | 0 | 16 |
| S3 after KCI pruning | 10 | 0.10 | 0.12 | 0.11 | 1 | 0 | 0 | 16 |
| S4 final (after cycle step) | 10 | 0.10 | 0.12 | 0.11 | 1 | 0 | 0 | 16 |

Scored against: reference graph concrete_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 9. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 9 calls, 36 distinct pairs answered out of 36, plus 9 self-pairs. Letters: {"A": 9, "C": 23, "D": 4}.
- LLM effect: added 9 (of which 5 where the resamples showed no edge at frequency >= 0.9), removed 5, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 10 edges; set by {"llm": 9, "algorithm (unchanged)": 1}; 1 identical to the algorithm's output; 7 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Blast furnace slag->Cement | llm | yes | 0.00 |
| Blast furnace slag <-> Water | algorithm (unchanged) | yes | 0.05 |
| Blast furnace slag->Compressive strength | llm | no | 1.00 |
| Cement->Compressive strength | llm | no | 1.00 |
| Water->Compressive strength | llm | no | 1.00 |
| Fly ash->Compressive strength | llm | no | 0.85 |
| Coarse aggregate->Compressive strength | llm | no | 0.85 |
| Superplasticizer->Compressive strength | llm | no | 1.00 |
| Age->Compressive strength | llm | no | 1.00 |
| Compressive strength->Fine aggregate | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Blast furnace slag, Cement | Blast furnace slag <-> Cement | Blast furnace slag   Cement (no edge) | Blast furnace slag->Cement | Blast furnace slag->Cement | Blast furnace slag->Cement | no edge | (Blast furnace slag, Cement)=A |
| Blast furnace slag, Superplasticizer | Blast furnace slag <-> Superplasticizer | Blast furnace slag   Superplasticizer (no edge) | Blast furnace slag   Superplasticizer (no edge) | Blast furnace slag   Superplasticizer (no edge) | Blast furnace slag   Superplasticizer (no edge) | no edge | (Blast furnace slag, Superplasticizer)=D |
| Blast furnace slag, Compressive strength | Blast furnace slag   Compressive strength (no edge) | Blast furnace slag   Compressive strength (no edge) | Blast furnace slag->Compressive strength | Blast furnace slag->Compressive strength | Blast furnace slag->Compressive strength | no edge | (Blast furnace slag, Compressive strength)=A |
| Blast furnace slag, Fine aggregate | Blast furnace slag <-> Fine aggregate | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag -> Fine aggregate | (Blast furnace slag, Fine aggregate)=C |
| Cement, Water | Cement <-> Water | Cement   Water (no edge) | Cement   Water (no edge) | Cement   Water (no edge) | Cement   Water (no edge) | no edge | (Cement, Water)=C |
| Cement, Superplasticizer | Cement <-> Superplasticizer | Cement <-> Superplasticizer | Cement   Superplasticizer (no edge) | Cement   Superplasticizer (no edge) | Cement   Superplasticizer (no edge) | no edge | (Cement, Superplasticizer)=C |
| Cement, Age | Cement <-> Age | Cement <-> Age | Cement   Age (no edge) | Cement   Age (no edge) | Cement   Age (no edge) | no edge | (Cement, Age)=C |
| Cement, Compressive strength | Cement   Compressive strength (no edge) | Cement   Compressive strength (no edge) | Cement->Compressive strength | Cement->Compressive strength | Cement->Compressive strength | no edge | (Cement, Compressive strength)=A |
| Water, Coarse aggregate | Coarse aggregate o-> Water | Coarse aggregate o-> Water | Water   Coarse aggregate (no edge) | Water   Coarse aggregate (no edge) | Water   Coarse aggregate (no edge) | no edge | (Water, Coarse aggregate)=C |
| Water, Compressive strength | Water   Compressive strength (no edge) | Water   Compressive strength (no edge) | Water->Compressive strength | Water->Compressive strength | Water->Compressive strength | no edge | (Water, Compressive strength)=A |
| Water, Fine aggregate | Water <-> Fine aggregate | Water   Fine aggregate (no edge) | Water   Fine aggregate (no edge) | Water   Fine aggregate (no edge) | Water   Fine aggregate (no edge) | Water -> Fine aggregate | (Water, Fine aggregate)=C |
| Fly ash, Coarse aggregate | Coarse aggregate o-> Fly ash | Coarse aggregate o-> Fly ash | Fly ash   Coarse aggregate (no edge) | Fly ash   Coarse aggregate (no edge) | Fly ash   Coarse aggregate (no edge) | no edge | (Fly ash, Coarse aggregate)=C |
| Fly ash, Superplasticizer | Fly ash <-> Superplasticizer | Fly ash   Superplasticizer (no edge) | Fly ash   Superplasticizer (no edge) | Fly ash   Superplasticizer (no edge) | Fly ash   Superplasticizer (no edge) | no edge | (Fly ash, Superplasticizer)=C |
| Fly ash, Age | Fly ash <-> Age | Fly ash   Age (no edge) | Fly ash   Age (no edge) | Fly ash   Age (no edge) | Fly ash   Age (no edge) | no edge | (Fly ash, Age)=C |
| Fly ash, Compressive strength | Fly ash   Compressive strength (no edge) | Fly ash   Compressive strength (no edge) | Fly ash->Compressive strength | Fly ash->Compressive strength | Fly ash->Compressive strength | no edge | (Fly ash, Compressive strength)=A |
| Fly ash, Fine aggregate | Fly ash <-> Fine aggregate | Fly ash   Fine aggregate (no edge) | Fly ash   Fine aggregate (no edge) | Fly ash   Fine aggregate (no edge) | Fly ash   Fine aggregate (no edge) | Fly ash -> Fine aggregate | (Fly ash, Fine aggregate)=C |
| Coarse aggregate, Compressive strength | Coarse aggregate   Compressive strength (no edge) | Coarse aggregate   Compressive strength (no edge) | Coarse aggregate->Compressive strength | Coarse aggregate->Compressive strength | Coarse aggregate->Compressive strength | no edge | (Coarse aggregate, Compressive strength)=A |
| Superplasticizer, Age | Superplasticizer->Age | Superplasticizer->Age | Superplasticizer   Age (no edge) | Superplasticizer   Age (no edge) | Superplasticizer   Age (no edge) | no edge | (Superplasticizer, Age)=C |
| Superplasticizer, Compressive strength | Superplasticizer   Compressive strength (no edge) | Superplasticizer   Compressive strength (no edge) | Superplasticizer->Compressive strength | Superplasticizer->Compressive strength | Superplasticizer->Compressive strength | no edge | (Superplasticizer, Compressive strength)=A |
| Age, Compressive strength | Age   Compressive strength (no edge) | Age   Compressive strength (no edge) | Age->Compressive strength | Age->Compressive strength | Age->Compressive strength | no edge | (Age, Compressive strength)=A |
| Compressive strength, Fine aggregate | Compressive strength o-> Fine aggregate | Compressive strength   Fine aggregate (no edge) | Compressive strength->Fine aggregate | Compressive strength->Fine aggregate | Compressive strength->Fine aggregate | Compressive strength -> Fine aggregate | (Compressive strength, Fine aggregate)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
