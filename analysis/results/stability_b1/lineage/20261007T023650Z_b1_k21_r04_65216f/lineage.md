# Edge lineage: 20261007T023650Z_b1_k21_r04_65216f

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
| S0 algorithm output | 6 | 0.83 | 1.00 | 0.91 | 2 | 1 | 2 | 6 |
| S1 after bootstrap edits | 3 | 1.00 | 0.60 | 0.75 | 2 | 0 | 1 | 5 |
| S2 after LLM review | 3 | 1.00 | 0.60 | 0.75 | 3 | 0 | 0 | 4 |
| S3 after KCI pruning | 3 | 1.00 | 0.60 | 0.75 | 3 | 0 | 0 | 4 |
| S4 final (after cycle step) | 3 | 1.00 | 0.60 | 0.75 | 3 | 0 | 0 | 4 |

Scored against: reference graph autompg_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 3. Of the deleted, 1 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 5 calls, 10 distinct pairs answered out of 10, plus 5 self-pairs. Letters: {"A": 2, "B": 1, "C": 7}.
- LLM effect: added 1 (of which 0 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 1.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 3 edges; set by {"llm": 2, "algorithm (unchanged)": 1}; 1 identical to the algorithm's output; 0 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| weight->mpg | llm | yes | 0.30 |
| displacement->horsepower | algorithm (unchanged) | yes | 0.40 |
| horsepower->acceleration | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| mpg, horsepower | mpg->horsepower | mpg   horsepower (no edge) | mpg   horsepower (no edge) | mpg   horsepower (no edge) | mpg   horsepower (no edge) | horsepower -> mpg | (mpg, horsepower)=C |
| mpg, weight | mpg o-o weight | mpg   weight (no edge) | weight->mpg | weight->mpg | weight->mpg | weight -> mpg | (mpg, weight)=B |
| displacement, weight | weight->displacement | weight->displacement | displacement   weight (no edge) | displacement   weight (no edge) | displacement   weight (no edge) | weight -> displacement | (displacement, weight)=C |
| displacement, acceleration | displacement <-> acceleration | displacement   acceleration (no edge) | displacement   acceleration (no edge) | displacement   acceleration (no edge) | displacement   acceleration (no edge) | no edge | (displacement, acceleration)=C |
| horsepower, acceleration | horsepower <-> acceleration | horsepower <-> acceleration | horsepower->acceleration | horsepower->acceleration | horsepower->acceleration | horsepower -> acceleration | (horsepower, acceleration)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
