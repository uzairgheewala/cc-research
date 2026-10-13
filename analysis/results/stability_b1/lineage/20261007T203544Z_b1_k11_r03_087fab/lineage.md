# Edge lineage: 20261007T203544Z_b1_k11_r03_087fab

Dataset `/research/datasets/suite_b1/k11/k11.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 6}. 8 variables, 28 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 14 | 0.21 | 0.43 | 0.29 | 0 | 1 | 2 | 18 |
| S1 after bootstrap edits | 6 | 0.33 | 0.29 | 0.31 | 0 | 1 | 1 | 11 |
| S2 after LLM review | 21 | 0.33 | 1.00 | 0.50 | 7 | 0 | 0 | 21 |
| S3 after KCI pruning | 21 | 0.33 | 1.00 | 0.50 | 7 | 0 | 0 | 21 |
| S4 final (after cycle step) | 21 | 0.33 | 1.00 | 0.50 | 7 | 0 | 0 | 21 |

Scored against: reference graph abalone_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 8. Of the deleted, 4 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 8 calls, 28 distinct pairs answered out of 28, plus 8 self-pairs. Letters: {"A": 18, "B": 2, "C": 5, "D": 3}.
- LLM effect: added 15 (of which 7 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 4.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 21 edges; set by {"llm": 19, "algorithm (unchanged)": 2}; 2 identical to the algorithm's output; 11 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Age->Length | llm | no | 1.00 |
| Age->Shell weight | llm | no | 1.00 |
| Age->Diameter | llm | no | 0.70 |
| Age->Height | llm | yes | 0.50 |
| Age->Whole weight | llm | yes | 0.00 |
| Age->Shucked weight | llm | no | 0.85 |
| Age->Viscera weight | llm | yes | 0.20 |
| Length->Shell weight | llm | yes | 0.00 |
| Length->Diameter | llm | no | 1.00 |
| Length->Height | llm | yes | 0.40 |
| Length->Whole weight | llm | no | 0.55 |
| Length->Shucked weight | llm | yes | 0.25 |
| Length->Viscera weight | llm | no | 1.00 |
| Height->Shell weight | algorithm (unchanged) | yes | 0.30 |
| Whole weight->Shell weight | llm | no | 1.00 |
| Shucked weight->Shell weight | llm | no | 1.00 |
| Height->Whole weight | llm | yes | 0.00 |
| Height->Shucked weight | algorithm (unchanged) | yes | 0.00 |
| Height->Viscera weight | llm | yes | 0.00 |
| Whole weight->Shucked weight | llm | no | 0.30 |
| Whole weight->Viscera weight | llm | no | 0.95 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Age, Length | Age   Length (no edge) | Age   Length (no edge) | Age->Length | Age->Length | Age->Length | Age -> Length | (Age, Length)=A |
| Age, Shell weight | Age   Shell weight (no edge) | Age   Shell weight (no edge) | Age->Shell weight | Age->Shell weight | Age->Shell weight | Age -> Shell weight | (Age, Shell weight)=A |
| Age, Diameter | Age   Diameter (no edge) | Age   Diameter (no edge) | Age->Diameter | Age->Diameter | Age->Diameter | Age -> Diameter | (Age, Diameter)=A |
| Age, Height | Age <-> Height | Age   Height (no edge) | Age->Height | Age->Height | Age->Height | Age -> Height | (Age, Height)=A |
| Age, Whole weight | Whole weight o-> Age | Whole weight o-> Age | Age->Whole weight | Age->Whole weight | Age->Whole weight | Age -> Whole weight | (Age, Whole weight)=A |
| Age, Shucked weight | Age   Shucked weight (no edge) | Age   Shucked weight (no edge) | Age->Shucked weight | Age->Shucked weight | Age->Shucked weight | Age -> Shucked weight | (Age, Shucked weight)=A |
| Age, Viscera weight | Viscera weight->Age | Viscera weight->Age | Age->Viscera weight | Age->Viscera weight | Age->Viscera weight | Age -> Viscera weight | (Age, Viscera weight)=A |
| Length, Shell weight | Length <-> Shell weight | Length <-> Shell weight | Length->Shell weight | Length->Shell weight | Length->Shell weight | no edge | (Length, Shell weight)=A |
| Length, Diameter | Length   Diameter (no edge) | Length   Diameter (no edge) | Length->Diameter | Length->Diameter | Length->Diameter | no edge | (Length, Diameter)=A |
| Length, Height | Length <-> Height | Length   Height (no edge) | Length->Height | Length->Height | Length->Height | no edge | (Length, Height)=A |
| Length, Whole weight | Length   Whole weight (no edge) | Length   Whole weight (no edge) | Length->Whole weight | Length->Whole weight | Length->Whole weight | no edge | (Length, Whole weight)=A |
| Length, Shucked weight | Length <-> Shucked weight | Length   Shucked weight (no edge) | Length->Shucked weight | Length->Shucked weight | Length->Shucked weight | no edge | (Length, Shucked weight)=A |
| Length, Viscera weight | Length   Viscera weight (no edge) | Length   Viscera weight (no edge) | Length->Viscera weight | Length->Viscera weight | Length->Viscera weight | no edge | (Length, Viscera weight)=A |
| Shell weight, Whole weight | Shell weight   Whole weight (no edge) | Shell weight   Whole weight (no edge) | Whole weight->Shell weight | Whole weight->Shell weight | Whole weight->Shell weight | no edge | (Shell weight, Whole weight)=B |
| Shell weight, Shucked weight | Shell weight   Shucked weight (no edge) | Shell weight   Shucked weight (no edge) | Shucked weight->Shell weight | Shucked weight->Shell weight | Shucked weight->Shell weight | no edge | (Shell weight, Shucked weight)=B |
| Shell weight, Viscera weight | Shell weight <-> Viscera weight | Shell weight   Viscera weight (no edge) | Shell weight   Viscera weight (no edge) | Shell weight   Viscera weight (no edge) | Shell weight   Viscera weight (no edge) | no edge | (Shell weight, Viscera weight)=D |
| Diameter, Height | Diameter o-> Height | Diameter   Height (no edge) | Diameter   Height (no edge) | Diameter   Height (no edge) | Diameter   Height (no edge) | no edge | (Diameter, Height)=C |
| Diameter, Viscera weight | Diameter o-> Viscera weight | Diameter   Viscera weight (no edge) | Diameter   Viscera weight (no edge) | Diameter   Viscera weight (no edge) | Diameter   Viscera weight (no edge) | no edge | (Diameter, Viscera weight)=C |
| Height, Whole weight | Whole weight o-> Height | Height   Whole weight (no edge) | Height->Whole weight | Height->Whole weight | Height->Whole weight | no edge | (Height, Whole weight)=A |
| Height, Viscera weight | Height <-> Viscera weight | Height <-> Viscera weight | Height->Viscera weight | Height->Viscera weight | Height->Viscera weight | no edge | (Height, Viscera weight)=A |
| Whole weight, Shucked weight | Whole weight   Shucked weight (no edge) | Whole weight   Shucked weight (no edge) | Whole weight->Shucked weight | Whole weight->Shucked weight | Whole weight->Shucked weight | no edge | (Whole weight, Shucked weight)=A |
| Whole weight, Viscera weight | Whole weight   Viscera weight (no edge) | Whole weight   Viscera weight (no edge) | Whole weight->Viscera weight | Whole weight->Viscera weight | Whole weight->Viscera weight | no edge | (Whole weight, Viscera weight)=A |
| Shucked weight, Viscera weight | Shucked weight <-> Viscera weight | Shucked weight   Viscera weight (no edge) | Shucked weight   Viscera weight (no edge) | Shucked weight   Viscera weight (no edge) | Shucked weight   Viscera weight (no edge) | no edge | (Shucked weight, Viscera weight)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
