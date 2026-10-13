# Edge lineage: 20261006T234430Z_b1_k33_r01_c33d49

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
| S0 algorithm output | 15 | 0.13 | 0.25 | 0.17 | 0 | 0 | 2 | 21 |
| S1 after bootstrap edits | 7 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 15 |
| S2 after LLM review | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 16 |
| S3 after KCI pruning | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 16 |
| S4 final (after cycle step) | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 16 |

Scored against: reference graph concrete_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 8. Of the deleted, 6 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 9 calls, 36 distinct pairs answered out of 36, plus 9 self-pairs. Letters: {"A": 7, "C": 28, "D": 1}.
- LLM effect: added 7 (of which 6 where the resamples showed no edge at frequency >= 0.9), removed 6, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 8 edges; set by {"algorithm (unchanged)": 1, "llm": 7}; 1 identical to the algorithm's output; 7 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Blast furnace slag <-> Cement | algorithm (unchanged) | yes | 0.00 |
| Blast furnace slag->Compressive strength | llm | no | 1.00 |
| Cement->Compressive strength | llm | no | 1.00 |
| Water->Compressive strength | llm | no | 1.00 |
| Fly ash->Compressive strength | llm | no | 0.90 |
| Coarse aggregate->Compressive strength | llm | no | 0.75 |
| Superplasticizer->Compressive strength | llm | no | 1.00 |
| Age->Compressive strength | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Blast furnace slag, Water | Water->Blast furnace slag | Water->Blast furnace slag | Blast furnace slag   Water (no edge) | Blast furnace slag   Water (no edge) | Blast furnace slag   Water (no edge) | no edge | (Blast furnace slag, Water)=C |
| Blast furnace slag, Superplasticizer | Superplasticizer->Blast furnace slag | Superplasticizer->Blast furnace slag | Blast furnace slag   Superplasticizer (no edge) | Blast furnace slag   Superplasticizer (no edge) | Blast furnace slag   Superplasticizer (no edge) | no edge | (Blast furnace slag, Superplasticizer)=C |
| Blast furnace slag, Age | Blast furnace slag <-> Age | Blast furnace slag   Age (no edge) | Blast furnace slag   Age (no edge) | Blast furnace slag   Age (no edge) | Blast furnace slag   Age (no edge) | no edge | (Blast furnace slag, Age)=C |
| Blast furnace slag, Compressive strength | Blast furnace slag   Compressive strength (no edge) | Blast furnace slag   Compressive strength (no edge) | Blast furnace slag->Compressive strength | Blast furnace slag->Compressive strength | Blast furnace slag->Compressive strength | no edge | (Blast furnace slag, Compressive strength)=A |
| Blast furnace slag, Fine aggregate | Blast furnace slag <-> Fine aggregate | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag -> Fine aggregate | (Blast furnace slag, Fine aggregate)=C |
| Cement, Water | Cement <-> Water | Cement   Water (no edge) | Cement   Water (no edge) | Cement   Water (no edge) | Cement   Water (no edge) | no edge | (Cement, Water)=C |
| Cement, Superplasticizer | Superplasticizer->Cement | Superplasticizer->Cement | Cement   Superplasticizer (no edge) | Cement   Superplasticizer (no edge) | Cement   Superplasticizer (no edge) | no edge | (Cement, Superplasticizer)=C |
| Cement, Age | Age->Cement | Cement   Age (no edge) | Cement   Age (no edge) | Cement   Age (no edge) | Cement   Age (no edge) | no edge | (Cement, Age)=C |
| Cement, Compressive strength | Cement   Compressive strength (no edge) | Cement   Compressive strength (no edge) | Cement->Compressive strength | Cement->Compressive strength | Cement->Compressive strength | no edge | (Cement, Compressive strength)=A |
| Water, Coarse aggregate | Water <-> Coarse aggregate | Water <-> Coarse aggregate | Water   Coarse aggregate (no edge) | Water   Coarse aggregate (no edge) | Water   Coarse aggregate (no edge) | no edge | (Water, Coarse aggregate)=C |
| Water, Compressive strength | Water   Compressive strength (no edge) | Water   Compressive strength (no edge) | Water->Compressive strength | Water->Compressive strength | Water->Compressive strength | no edge | (Water, Compressive strength)=A |
| Fly ash, Coarse aggregate | Coarse aggregate->Fly ash | Coarse aggregate->Fly ash | Fly ash   Coarse aggregate (no edge) | Fly ash   Coarse aggregate (no edge) | Fly ash   Coarse aggregate (no edge) | no edge | (Fly ash, Coarse aggregate)=C |
| Fly ash, Superplasticizer | Fly ash <-> Superplasticizer | Fly ash   Superplasticizer (no edge) | Fly ash   Superplasticizer (no edge) | Fly ash   Superplasticizer (no edge) | Fly ash   Superplasticizer (no edge) | no edge | (Fly ash, Superplasticizer)=C |
| Fly ash, Age | Fly ash->Age | Fly ash->Age | Fly ash   Age (no edge) | Fly ash   Age (no edge) | Fly ash   Age (no edge) | no edge | (Fly ash, Age)=C |
| Fly ash, Compressive strength | Fly ash   Compressive strength (no edge) | Fly ash   Compressive strength (no edge) | Fly ash->Compressive strength | Fly ash->Compressive strength | Fly ash->Compressive strength | no edge | (Fly ash, Compressive strength)=A |
| Coarse aggregate, Superplasticizer | Coarse aggregate <-> Superplasticizer | Coarse aggregate   Superplasticizer (no edge) | Coarse aggregate   Superplasticizer (no edge) | Coarse aggregate   Superplasticizer (no edge) | Coarse aggregate   Superplasticizer (no edge) | no edge | (Coarse aggregate, Superplasticizer)=C |
| Coarse aggregate, Compressive strength | Coarse aggregate   Compressive strength (no edge) | Coarse aggregate   Compressive strength (no edge) | Coarse aggregate->Compressive strength | Coarse aggregate->Compressive strength | Coarse aggregate->Compressive strength | no edge | (Coarse aggregate, Compressive strength)=A |
| Superplasticizer, Age | Superplasticizer <-> Age | Superplasticizer   Age (no edge) | Superplasticizer   Age (no edge) | Superplasticizer   Age (no edge) | Superplasticizer   Age (no edge) | no edge | (Superplasticizer, Age)=C |
| Superplasticizer, Compressive strength | Superplasticizer   Compressive strength (no edge) | Superplasticizer   Compressive strength (no edge) | Superplasticizer->Compressive strength | Superplasticizer->Compressive strength | Superplasticizer->Compressive strength | no edge | (Superplasticizer, Compressive strength)=A |
| Age, Compressive strength | Age   Compressive strength (no edge) | Age   Compressive strength (no edge) | Age->Compressive strength | Age->Compressive strength | Age->Compressive strength | no edge | (Age, Compressive strength)=A |
| Compressive strength, Fine aggregate | Compressive strength o-> Fine aggregate | Compressive strength   Fine aggregate (no edge) | Compressive strength   Fine aggregate (no edge) | Compressive strength   Fine aggregate (no edge) | Compressive strength   Fine aggregate (no edge) | Compressive strength -> Fine aggregate | (Compressive strength, Fine aggregate)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
