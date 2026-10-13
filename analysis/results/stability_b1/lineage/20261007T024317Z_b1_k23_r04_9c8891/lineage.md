# Edge lineage: 20261007T024317Z_b1_k23_r04_9c8891

Dataset `/research/datasets/suite_b1/k23/k23.csv`, algorithm **FCI** {"alpha": 0.1, "indep_test": "rcit", "depth": 6}. 5 variables, 10 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 6 | 0.50 | 0.60 | 0.55 | 0 | 2 | 1 | 8 |
| S1 after bootstrap edits | 3 | 0.33 | 0.20 | 0.25 | 0 | 0 | 1 | 7 |
| S2 after LLM review | 5 | 0.20 | 0.20 | 0.20 | 0 | 1 | 0 | 9 |
| S3 after KCI pruning | 5 | 0.20 | 0.20 | 0.20 | 0 | 1 | 0 | 9 |
| S4 final (after cycle step) | 5 | 0.20 | 0.20 | 0.20 | 0 | 1 | 0 | 9 |

Scored against: reference graph autompg_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 3. Of the deleted, 1 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"A": 3, "B": 2, "C": 5}.
- LLM effect: added 3 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 1.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 5 edges; set by {"algorithm (unchanged)": 1, "llm": 4}; 2 identical to the algorithm's output; 2 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| weight->displacement | algorithm (unchanged) | yes | 0.30 |
| displacement->horsepower | llm | no | 0.30 |
| weight->mpg | llm | yes | 0.00 |
| horsepower->acceleration | llm | yes | 0.30 |
| horsepower->mpg | llm | no | 0.60 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| displacement, acceleration | displacement->acceleration | displacement   acceleration (no edge) | displacement   acceleration (no edge) | displacement   acceleration (no edge) | displacement   acceleration (no edge) | acceleration -> displacement | (displacement, acceleration)=C |
| displacement, horsepower | displacement   horsepower (no edge) | displacement   horsepower (no edge) | displacement->horsepower | displacement->horsepower | displacement->horsepower | horsepower -> displacement | (displacement, horsepower)=A |
| weight, horsepower | horsepower o-> weight | horsepower o-> weight | weight   horsepower (no edge) | weight   horsepower (no edge) | weight   horsepower (no edge) | horsepower -> weight | (weight, horsepower)=C |
| weight, mpg | mpg o-> weight | mpg o-> weight | weight->mpg | weight->mpg | weight->mpg | no edge | (weight, mpg)=A |
| acceleration, horsepower | horsepower->acceleration | acceleration   horsepower (no edge) | horsepower->acceleration | horsepower->acceleration | horsepower->acceleration | no edge | (acceleration, horsepower)=B |
| acceleration, mpg | mpg->acceleration | acceleration   mpg (no edge) | acceleration   mpg (no edge) | acceleration   mpg (no edge) | acceleration   mpg (no edge) | acceleration -> mpg | (acceleration, mpg)=C |
| horsepower, mpg | horsepower   mpg (no edge) | horsepower   mpg (no edge) | horsepower->mpg | horsepower->mpg | horsepower->mpg | no edge | (horsepower, mpg)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
