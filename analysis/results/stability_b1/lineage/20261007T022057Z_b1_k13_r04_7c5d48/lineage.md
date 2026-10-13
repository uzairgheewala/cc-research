# Edge lineage: 20261007T022057Z_b1_k13_r04_7c5d48

Dataset `/research/datasets/suite_b1/k13/k13.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 6}. 8 variables, 28 pairs. 20 bootstrap resamples.

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
| S1 after bootstrap edits | 3 | 0.33 | 0.14 | 0.20 | 0 | 1 | 0 | 9 |
| S2 after LLM review | 22 | 0.32 | 1.00 | 0.48 | 2 | 5 | 0 | 22 |
| S3 after KCI pruning | 22 | 0.32 | 1.00 | 0.48 | 2 | 5 | 0 | 22 |
| S4 final (after cycle step) | 22 | 0.32 | 1.00 | 0.48 | 2 | 5 | 0 | 22 |

Scored against: reference graph abalone_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 11. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 8 calls, 28 distinct pairs answered out of 28, plus 8 self-pairs. Letters: {"A": 11, "B": 11, "C": 5, "D": 1}.
- LLM effect: added 19 (of which 6 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 1.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 22 edges; set by {"llm": 20, "algorithm (unchanged)": 2}; 2 identical to the algorithm's output; 9 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Age->Length | llm | no | 1.00 |
| Length->Diameter | llm | no | 1.00 |
| Shell weight->Length | llm | no | 0.70 |
| Whole weight->Length | llm | yes | 0.25 |
| Length->Height | llm | yes | 0.00 |
| Viscera weight->Length | llm | no | 0.85 |
| Shucked weight->Length | algorithm (unchanged) | yes | 0.00 |
| Age->Diameter | llm | yes | 0.00 |
| Age->Shell weight | llm | no | 1.00 |
| Age->Whole weight | llm | yes | 0.20 |
| Age->Height | llm | no | 0.85 |
| Age->Viscera weight | llm | yes | 0.10 |
| Age->Shucked weight | llm | no | 0.95 |
| Shell weight->Diameter | llm | no | 1.00 |
| Whole weight->Diameter | algorithm (unchanged) | yes | 0.15 |
| Viscera weight->Diameter | llm | no | 1.00 |
| Shucked weight->Diameter | llm | yes | 0.00 |
| Whole weight->Shell weight | llm | yes | 0.25 |
| Shucked weight->Shell weight | llm | yes | 0.00 |
| Whole weight->Viscera weight | llm | yes | 0.00 |
| Whole weight->Shucked weight | llm | yes | 0.00 |
| Viscera weight->Shucked weight | llm | yes | 0.05 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Length, Age | Length   Age (no edge) | Length   Age (no edge) | Age->Length | Age->Length | Age->Length | Length -> Age | (Length, Age)=B |
| Length, Diameter | Length   Diameter (no edge) | Length   Diameter (no edge) | Length->Diameter | Length->Diameter | Length->Diameter | Length -> Diameter | (Length, Diameter)=A |
| Length, Shell weight | Length   Shell weight (no edge) | Length   Shell weight (no edge) | Shell weight->Length | Shell weight->Length | Shell weight->Length | Length -> Shell weight | (Length, Shell weight)=B |
| Length, Whole weight | Length <-> Whole weight | Length   Whole weight (no edge) | Whole weight->Length | Whole weight->Length | Whole weight->Length | Length -> Whole weight | (Length, Whole weight)=B |
| Length, Height | Height o-> Length | Length   Height (no edge) | Length->Height | Length->Height | Length->Height | Length -> Height | (Length, Height)=A |
| Length, Viscera weight | Length   Viscera weight (no edge) | Length   Viscera weight (no edge) | Viscera weight->Length | Viscera weight->Length | Viscera weight->Length | Length -> Viscera weight | (Length, Viscera weight)=B |
| Age, Diameter | Age <-> Diameter | Age <-> Diameter | Age->Diameter | Age->Diameter | Age->Diameter | no edge | (Age, Diameter)=A |
| Age, Shell weight | Age   Shell weight (no edge) | Age   Shell weight (no edge) | Age->Shell weight | Age->Shell weight | Age->Shell weight | no edge | (Age, Shell weight)=A |
| Age, Whole weight | Age <-> Whole weight | Age   Whole weight (no edge) | Age->Whole weight | Age->Whole weight | Age->Whole weight | no edge | (Age, Whole weight)=A |
| Age, Height | Age   Height (no edge) | Age   Height (no edge) | Age->Height | Age->Height | Age->Height | no edge | (Age, Height)=A |
| Age, Viscera weight | Viscera weight o-> Age | Age   Viscera weight (no edge) | Age->Viscera weight | Age->Viscera weight | Age->Viscera weight | no edge | (Age, Viscera weight)=A |
| Age, Shucked weight | Age   Shucked weight (no edge) | Age   Shucked weight (no edge) | Age->Shucked weight | Age->Shucked weight | Age->Shucked weight | no edge | (Age, Shucked weight)=A |
| Diameter, Shell weight | Diameter   Shell weight (no edge) | Diameter   Shell weight (no edge) | Shell weight->Diameter | Shell weight->Diameter | Shell weight->Diameter | no edge | (Diameter, Shell weight)=B |
| Diameter, Viscera weight | Diameter   Viscera weight (no edge) | Diameter   Viscera weight (no edge) | Viscera weight->Diameter | Viscera weight->Diameter | Viscera weight->Diameter | no edge | (Diameter, Viscera weight)=B |
| Diameter, Shucked weight | Diameter <-> Shucked weight | Diameter   Shucked weight (no edge) | Shucked weight->Diameter | Shucked weight->Diameter | Shucked weight->Diameter | no edge | (Diameter, Shucked weight)=B |
| Shell weight, Whole weight | Shell weight o-> Whole weight | Shell weight   Whole weight (no edge) | Whole weight->Shell weight | Whole weight->Shell weight | Whole weight->Shell weight | no edge | (Shell weight, Whole weight)=B |
| Shell weight, Shucked weight | Shell weight o-> Shucked weight | Shell weight   Shucked weight (no edge) | Shucked weight->Shell weight | Shucked weight->Shell weight | Shucked weight->Shell weight | no edge | (Shell weight, Shucked weight)=B |
| Whole weight, Height | Height o-> Whole weight | Whole weight   Height (no edge) | Whole weight   Height (no edge) | Whole weight   Height (no edge) | Whole weight   Height (no edge) | no edge | (Whole weight, Height)=C |
| Whole weight, Viscera weight | Viscera weight o-> Whole weight | Whole weight   Viscera weight (no edge) | Whole weight->Viscera weight | Whole weight->Viscera weight | Whole weight->Viscera weight | no edge | (Whole weight, Viscera weight)=A |
| Whole weight, Shucked weight | Whole weight <-> Shucked weight | Whole weight   Shucked weight (no edge) | Whole weight->Shucked weight | Whole weight->Shucked weight | Whole weight->Shucked weight | no edge | (Whole weight, Shucked weight)=A |
| Viscera weight, Shucked weight | Viscera weight o-> Shucked weight | Viscera weight   Shucked weight (no edge) | Viscera weight->Shucked weight | Viscera weight->Shucked weight | Viscera weight->Shucked weight | no edge | (Viscera weight, Shucked weight)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
