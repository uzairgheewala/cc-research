# Edge lineage: 20261007T003854Z_b1_k21_r02_7cc686

Dataset `/research/datasets/suite_b1/k21/k21.csv`, algorithm **FCI** {"alpha": 0.1, "indep_test": "rcit", "depth": 6}. 5 variables, 10 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 5 | 0.80 | 0.80 | 0.80 | 1 | 1 | 2 | 6 |
| S1 after bootstrap edits | 2 | 1.00 | 0.40 | 0.57 | 1 | 0 | 1 | 5 |
| S2 after LLM review | 5 | 1.00 | 1.00 | 1.00 | 5 | 0 | 0 | 3 |
| S3 after KCI pruning | 5 | 1.00 | 1.00 | 1.00 | 5 | 0 | 0 | 3 |
| S4 final (after cycle step) | 5 | 1.00 | 1.00 | 1.00 | 5 | 0 | 0 | 3 |

Scored against: reference graph autompg_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 3. Of the deleted, 1 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"A": 2, "B": 3, "C": 4, "D": 1}.
- LLM effect: added 3 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 1.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 5 edges; set by {"llm": 4, "algorithm (unchanged)": 1}; 1 identical to the algorithm's output; 1 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| horsepower->mpg | llm | yes | 0.00 |
| weight->mpg | llm | yes | 0.10 |
| displacement->horsepower | llm | no | 0.45 |
| weight->displacement | algorithm (unchanged) | yes | 0.00 |
| horsepower->acceleration | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| mpg, horsepower | mpg->horsepower | mpg   horsepower (no edge) | horsepower->mpg | horsepower->mpg | horsepower->mpg | horsepower -> mpg | (mpg, horsepower)=B |
| mpg, weight | mpg o-o weight | mpg   weight (no edge) | weight->mpg | weight->mpg | weight->mpg | weight -> mpg | (mpg, weight)=B |
| displacement, horsepower | displacement   horsepower (no edge) | displacement   horsepower (no edge) | displacement->horsepower | displacement->horsepower | displacement->horsepower | displacement -> horsepower | (displacement, horsepower)=A |
| displacement, acceleration | acceleration o-> displacement | displacement   acceleration (no edge) | displacement   acceleration (no edge) | displacement   acceleration (no edge) | displacement   acceleration (no edge) | no edge | (displacement, acceleration)=D |
| horsepower, acceleration | acceleration o-> horsepower | acceleration o-> horsepower | horsepower->acceleration | horsepower->acceleration | horsepower->acceleration | horsepower -> acceleration | (horsepower, acceleration)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
