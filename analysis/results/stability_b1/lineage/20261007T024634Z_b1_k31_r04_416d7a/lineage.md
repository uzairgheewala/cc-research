# Edge lineage: 20261007T024634Z_b1_k31_r04_416d7a

Dataset `/research/datasets/suite_b1/k31/k31.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 6}. 9 variables, 36 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 16 | 0.19 | 0.38 | 0.25 | 0 | 0 | 3 | 21 |
| S1 after bootstrap edits | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 16 |
| S2 after LLM review | 8 | 1.00 | 1.00 | 1.00 | 8 | 0 | 0 | 0 |
| S3 after KCI pruning | 8 | 1.00 | 1.00 | 1.00 | 8 | 0 | 0 | 0 |
| S4 final (after cycle step) | 8 | 1.00 | 1.00 | 1.00 | 8 | 0 | 0 | 0 |

Scored against: reference graph concrete_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 8. Of the deleted, 6 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 9 calls, 36 distinct pairs answered out of 36, plus 9 self-pairs. Letters: {"A": 8, "C": 28}.
- LLM effect: added 8 (of which 4 where the resamples showed no edge at frequency >= 0.9), removed 8, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 8 edges; set by {"llm": 8}; 0 identical to the algorithm's output; 5 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Cement->Compressive strength | llm | yes | 0.00 |
| Blast furnace slag->Compressive strength | llm | no | 0.95 |
| Fly ash->Compressive strength | llm | no | 0.60 |
| Water->Compressive strength | llm | no | 0.20 |
| Superplasticizer->Compressive strength | llm | no | 0.90 |
| Coarse aggregate->Compressive strength | llm | no | 0.90 |
| Fine aggregate->Compressive strength | llm | yes | 1.00 |
| Age->Compressive strength | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Cement, Blast furnace slag | Cement <-> Blast furnace slag | Cement <-> Blast furnace slag | Cement   Blast furnace slag (no edge) | Cement   Blast furnace slag (no edge) | Cement   Blast furnace slag (no edge) | no edge | (Cement, Blast furnace slag)=C |
| Cement, Fly ash | Cement->Fly ash | Cement->Fly ash | Cement   Fly ash (no edge) | Cement   Fly ash (no edge) | Cement   Fly ash (no edge) | no edge | (Cement, Fly ash)=C |
| Cement, Superplasticizer | Superplasticizer->Cement | Superplasticizer->Cement | Cement   Superplasticizer (no edge) | Cement   Superplasticizer (no edge) | Cement   Superplasticizer (no edge) | no edge | (Cement, Superplasticizer)=C |
| Cement, Coarse aggregate | Cement <-> Coarse aggregate | Cement <-> Coarse aggregate | Cement   Coarse aggregate (no edge) | Cement   Coarse aggregate (no edge) | Cement   Coarse aggregate (no edge) | no edge | (Cement, Coarse aggregate)=C |
| Cement, Compressive strength | Cement <-> Compressive strength | Cement   Compressive strength (no edge) | Cement->Compressive strength | Cement->Compressive strength | Cement->Compressive strength | Cement -> Compressive strength | (Cement, Compressive strength)=A |
| Blast furnace slag, Fly ash | Blast furnace slag <-> Fly ash | Blast furnace slag   Fly ash (no edge) | Blast furnace slag   Fly ash (no edge) | Blast furnace slag   Fly ash (no edge) | Blast furnace slag   Fly ash (no edge) | no edge | (Blast furnace slag, Fly ash)=C |
| Blast furnace slag, Coarse aggregate | Blast furnace slag->Coarse aggregate | Blast furnace slag   Coarse aggregate (no edge) | Blast furnace slag   Coarse aggregate (no edge) | Blast furnace slag   Coarse aggregate (no edge) | Blast furnace slag   Coarse aggregate (no edge) | no edge | (Blast furnace slag, Coarse aggregate)=C |
| Blast furnace slag, Fine aggregate | Blast furnace slag <-> Fine aggregate | Blast furnace slag <-> Fine aggregate | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag   Fine aggregate (no edge) | Blast furnace slag   Fine aggregate (no edge) | no edge | (Blast furnace slag, Fine aggregate)=C |
| Blast furnace slag, Compressive strength | Blast furnace slag   Compressive strength (no edge) | Blast furnace slag   Compressive strength (no edge) | Blast furnace slag->Compressive strength | Blast furnace slag->Compressive strength | Blast furnace slag->Compressive strength | Blast furnace slag -> Compressive strength | (Blast furnace slag, Compressive strength)=A |
| Fly ash, Superplasticizer | Superplasticizer->Fly ash | Superplasticizer->Fly ash | Fly ash   Superplasticizer (no edge) | Fly ash   Superplasticizer (no edge) | Fly ash   Superplasticizer (no edge) | no edge | (Fly ash, Superplasticizer)=C |
| Fly ash, Compressive strength | Fly ash   Compressive strength (no edge) | Fly ash   Compressive strength (no edge) | Fly ash->Compressive strength | Fly ash->Compressive strength | Fly ash->Compressive strength | Fly ash -> Compressive strength | (Fly ash, Compressive strength)=A |
| Water, Superplasticizer | Water->Superplasticizer | Water->Superplasticizer | Water   Superplasticizer (no edge) | Water   Superplasticizer (no edge) | Water   Superplasticizer (no edge) | no edge | (Water, Superplasticizer)=C |
| Water, Coarse aggregate | Water <-> Coarse aggregate | Water   Coarse aggregate (no edge) | Water   Coarse aggregate (no edge) | Water   Coarse aggregate (no edge) | Water   Coarse aggregate (no edge) | no edge | (Water, Coarse aggregate)=C |
| Water, Fine aggregate | Water <-> Fine aggregate | Water   Fine aggregate (no edge) | Water   Fine aggregate (no edge) | Water   Fine aggregate (no edge) | Water   Fine aggregate (no edge) | no edge | (Water, Fine aggregate)=C |
| Water, Compressive strength | Water   Compressive strength (no edge) | Water   Compressive strength (no edge) | Water->Compressive strength | Water->Compressive strength | Water->Compressive strength | Water -> Compressive strength | (Water, Compressive strength)=A |
| Superplasticizer, Coarse aggregate | Superplasticizer <-> Coarse aggregate | Superplasticizer <-> Coarse aggregate | Superplasticizer   Coarse aggregate (no edge) | Superplasticizer   Coarse aggregate (no edge) | Superplasticizer   Coarse aggregate (no edge) | no edge | (Superplasticizer, Coarse aggregate)=C |
| Superplasticizer, Compressive strength | Superplasticizer   Compressive strength (no edge) | Superplasticizer   Compressive strength (no edge) | Superplasticizer->Compressive strength | Superplasticizer->Compressive strength | Superplasticizer->Compressive strength | Superplasticizer -> Compressive strength | (Superplasticizer, Compressive strength)=A |
| Coarse aggregate, Fine aggregate | Fine aggregate->Coarse aggregate | Coarse aggregate   Fine aggregate (no edge) | Coarse aggregate   Fine aggregate (no edge) | Coarse aggregate   Fine aggregate (no edge) | Coarse aggregate   Fine aggregate (no edge) | no edge | (Coarse aggregate, Fine aggregate)=C |
| Coarse aggregate, Compressive strength | Coarse aggregate   Compressive strength (no edge) | Coarse aggregate   Compressive strength (no edge) | Coarse aggregate->Compressive strength | Coarse aggregate->Compressive strength | Coarse aggregate->Compressive strength | Coarse aggregate -> Compressive strength | (Coarse aggregate, Compressive strength)=A |
| Fine aggregate, Compressive strength | Fine aggregate <-> Compressive strength | Fine aggregate   Compressive strength (no edge) | Fine aggregate->Compressive strength | Fine aggregate->Compressive strength | Fine aggregate->Compressive strength | Fine aggregate -> Compressive strength | (Fine aggregate, Compressive strength)=A |
| Age, Compressive strength | Age o-> Compressive strength | Age   Compressive strength (no edge) | Age->Compressive strength | Age->Compressive strength | Age->Compressive strength | Age -> Compressive strength | (Age, Compressive strength)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
