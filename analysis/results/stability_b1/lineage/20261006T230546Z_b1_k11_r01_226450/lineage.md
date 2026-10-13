# Edge lineage: 20261006T230546Z_b1_k11_r01_226450

Dataset `/research/datasets/suite_b1/k11/k11.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 6}. 8 variables, 28 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 15 | 0.20 | 0.43 | 0.27 | 0 | 1 | 2 | 19 |
| S1 after bootstrap edits | 6 | 0.17 | 0.14 | 0.15 | 0 | 1 | 0 | 12 |
| S2 after LLM review | 15 | 0.47 | 1.00 | 0.64 | 7 | 0 | 0 | 15 |
| S3 after KCI pruning | 15 | 0.47 | 1.00 | 0.64 | 7 | 0 | 0 | 15 |
| S4 final (after cycle step) | 15 | 0.47 | 1.00 | 0.64 | 7 | 0 | 0 | 15 |

Scored against: reference graph abalone_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 9. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 8 calls, 28 distinct pairs answered out of 28, plus 8 self-pairs. Letters: {"A": 13, "B": 2, "C": 13}.
- LLM effect: added 12 (of which 3 where the resamples showed no edge at frequency >= 0.9), removed 3, re-oriented 2.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 15 edges; set by {"llm": 14, "algorithm (unchanged)": 1}; 1 identical to the algorithm's output; 8 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Age->Length | llm | no | 0.95 |
| Age->Shell weight | llm | no | 1.00 |
| Age->Diameter | llm | no | 0.80 |
| Age->Height | llm | yes | 0.45 |
| Age->Whole weight | llm | yes | 0.00 |
| Age->Shucked weight | llm | no | 0.75 |
| Age->Viscera weight | llm | yes | 0.15 |
| Length->Diameter | llm | no | 0.90 |
| Whole weight->Shell weight | llm | no | 0.85 |
| Height->Whole weight | llm | yes | 0.00 |
| Height->Shucked weight | algorithm (unchanged) | yes | 0.00 |
| Height->Viscera weight | llm | yes | 0.00 |
| Whole weight->Shucked weight | llm | no | 0.30 |
| Whole weight->Viscera weight | llm | no | 0.85 |
| Viscera weight->Shucked weight | llm | yes | 0.10 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Age, Length | Age   Length (no edge) | Age   Length (no edge) | Age->Length | Age->Length | Age->Length | Age -> Length | (Age, Length)=A |
| Age, Shell weight | Age   Shell weight (no edge) | Age   Shell weight (no edge) | Age->Shell weight | Age->Shell weight | Age->Shell weight | Age -> Shell weight | (Age, Shell weight)=A |
| Age, Diameter | Age   Diameter (no edge) | Age   Diameter (no edge) | Age->Diameter | Age->Diameter | Age->Diameter | Age -> Diameter | (Age, Diameter)=A |
| Age, Height | Age <-> Height | Age   Height (no edge) | Age->Height | Age->Height | Age->Height | Age -> Height | (Age, Height)=A |
| Age, Whole weight | Age <-> Whole weight | Age   Whole weight (no edge) | Age->Whole weight | Age->Whole weight | Age->Whole weight | Age -> Whole weight | (Age, Whole weight)=A |
| Age, Shucked weight | Age   Shucked weight (no edge) | Age   Shucked weight (no edge) | Age->Shucked weight | Age->Shucked weight | Age->Shucked weight | Age -> Shucked weight | (Age, Shucked weight)=A |
| Age, Viscera weight | Viscera weight->Age | Viscera weight->Age | Age->Viscera weight | Age->Viscera weight | Age->Viscera weight | Age -> Viscera weight | (Age, Viscera weight)=A |
| Length, Shell weight | Shell weight o-> Length | Shell weight o-> Length | Length   Shell weight (no edge) | Length   Shell weight (no edge) | Length   Shell weight (no edge) | no edge | (Length, Shell weight)=C |
| Length, Diameter | Length   Diameter (no edge) | Length   Diameter (no edge) | Length->Diameter | Length->Diameter | Length->Diameter | no edge | (Length, Diameter)=A |
| Length, Height | Length <-> Height | Length <-> Height | Length   Height (no edge) | Length   Height (no edge) | Length   Height (no edge) | no edge | (Length, Height)=C |
| Length, Whole weight | Length <-> Whole weight | Length   Whole weight (no edge) | Length   Whole weight (no edge) | Length   Whole weight (no edge) | Length   Whole weight (no edge) | no edge | (Length, Whole weight)=C |
| Length, Shucked weight | Length <-> Shucked weight | Length   Shucked weight (no edge) | Length   Shucked weight (no edge) | Length   Shucked weight (no edge) | Length   Shucked weight (no edge) | no edge | (Length, Shucked weight)=C |
| Shell weight, Height | Shell weight o-> Height | Shell weight   Height (no edge) | Shell weight   Height (no edge) | Shell weight   Height (no edge) | Shell weight   Height (no edge) | no edge | (Shell weight, Height)=C |
| Shell weight, Whole weight | Shell weight   Whole weight (no edge) | Shell weight   Whole weight (no edge) | Whole weight->Shell weight | Whole weight->Shell weight | Whole weight->Shell weight | no edge | (Shell weight, Whole weight)=B |
| Shell weight, Viscera weight | Shell weight o-> Viscera weight | Shell weight o-> Viscera weight | Shell weight   Viscera weight (no edge) | Shell weight   Viscera weight (no edge) | Shell weight   Viscera weight (no edge) | no edge | (Shell weight, Viscera weight)=C |
| Diameter, Height | Diameter o-> Height | Diameter   Height (no edge) | Diameter   Height (no edge) | Diameter   Height (no edge) | Diameter   Height (no edge) | no edge | (Diameter, Height)=C |
| Diameter, Viscera weight | Diameter o-> Viscera weight | Diameter   Viscera weight (no edge) | Diameter   Viscera weight (no edge) | Diameter   Viscera weight (no edge) | Diameter   Viscera weight (no edge) | no edge | (Diameter, Viscera weight)=C |
| Height, Whole weight | Whole weight o-> Height | Height   Whole weight (no edge) | Height->Whole weight | Height->Whole weight | Height->Whole weight | no edge | (Height, Whole weight)=A |
| Height, Viscera weight | Height <-> Viscera weight | Height <-> Viscera weight | Height->Viscera weight | Height->Viscera weight | Height->Viscera weight | no edge | (Height, Viscera weight)=A |
| Whole weight, Shucked weight | Whole weight   Shucked weight (no edge) | Whole weight   Shucked weight (no edge) | Whole weight->Shucked weight | Whole weight->Shucked weight | Whole weight->Shucked weight | no edge | (Whole weight, Shucked weight)=A |
| Whole weight, Viscera weight | Whole weight   Viscera weight (no edge) | Whole weight   Viscera weight (no edge) | Whole weight->Viscera weight | Whole weight->Viscera weight | Whole weight->Viscera weight | no edge | (Whole weight, Viscera weight)=A |
| Shucked weight, Viscera weight | Shucked weight <-> Viscera weight | Shucked weight   Viscera weight (no edge) | Viscera weight->Shucked weight | Viscera weight->Shucked weight | Viscera weight->Shucked weight | no edge | (Shucked weight, Viscera weight)=B |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
