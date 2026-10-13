# Scores through S3 for all runs that reached refinement (label b1)

Runs: 54. Reached: S3 8, S4 45, no refinement graph 1.

Gates: Q1_rebuilt_S2_S3_equal_recorded PASS; Q2_cycle_crashes_have_cycle_in_S3 PASS; Q3_all_runs_accounted PASS

Scores are against the by-data reference unless a column says by label. S3 is the graph handed to the cycle step.

| arm | family | role | runs | completed | with S3 | S3 cyclic by the pipeline's test | of which cyclic among committed directions | adjacency F1 S0 | S3 (completed) | S3 (all) | directed F1 S0 | S3 (completed) | S3 (all) | S3 all, by label: adjacency | directed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| k11 | abalone | real | 7 | 5 | 7 | 2 | 1 | 0.265 | 0.532 | 0.5 | 0.0 | 0.532 | 0.482 | 0.5 | 0.482 |
| k12 | abalone | neutral | 4 | 4 | 4 | 0 | 0 | 0.214 | 0.038 | 0.038 | 0.05 | 0.0 | 0.0 | None | None |
| k13 | abalone | swapped | 4 | 3 | 4 | 1 | 0 | 0.276 | 0.489 | 0.456 | 0.0 | 0.14 | 0.179 | 0.491 | 0.477 |
| k21 | autompg | real | 4 | 4 | 4 | 0 | 0 | 0.744 | 0.812 | 0.812 | 0.268 | 0.75 | 0.75 | 0.812 | 0.75 |
| k22 | autompg | neutral | 4 | 4 | 4 | 0 | 0 | 0.722 | 0.391 | 0.391 | 0.183 | 0.071 | 0.071 | None | None |
| k23 | autompg | swapped | 4 | 3 | 4 | 1 | 0 | 0.65 | 0.2 | 0.241 | 0.071 | 0.0 | 0.0 | 0.977 | 1.0 |
| k31 | concrete | real | 4 | 3 | 3 | 0 | 0 | 0.278 | 0.943 | 0.943 | 0.0 | 1.0 | 1.0 | 0.943 | 1.0 |
| k32 | concrete | neutral | 4 | 4 | 4 | 0 | 0 | 0.295 | 0.036 | 0.036 | 0.074 | 0.0 | 0.0 | None | None |
| k33 | concrete | swapped | 4 | 3 | 4 | 1 | 0 | 0.261 | 0.074 | 0.114 | 0.0 | 0.078 | 0.09 | 0.898 | 0.864 |
| k41 | dwd | real | 4 | 4 | 4 | 0 | 0 | 0.748 | 0.554 | 0.554 | 0.083 | 0.554 | 0.554 | 0.554 | 0.554 |
| k42 | dwd | neutral | 4 | 4 | 4 | 0 | 0 | 0.822 | 0.354 | 0.354 | 0.0 | 0.0 | 0.0 | None | None |
| k43 | dwd | swapped | 7 | 4 | 7 | 3 | 3 | 0.736 | 0.285 | 0.325 | 0.041 | 0.062 | 0.036 | 0.478 | 0.327 |

| role | with S3 | completed | S3 adjacency F1 below S0 (all) | adjacency F1 S0 | S3 (completed) | S3 (all) | directed F1 S0 | S3 (completed) | S3 (all) |
|---|---|---|---|---|---|---|---|---|---|
| real | 18 | 16 | 5 | 0.481 | 0.684 | 0.655 | 0.078 | 0.679 | 0.644 |
| neutral | 16 | 16 | 16 | 0.513 | 0.205 | 0.205 | 0.077 | 0.018 | 0.018 |
| swapped | 19 | 13 | 15 | 0.521 | 0.264 | 0.291 | 0.03 | 0.07 | 0.07 |

Cycle step: {"runs_cyclic_by_pipeline_test": 8, "of_which_cyclic_among_committed_directions": 4, "of_which_completed": 0, "by_role": {"real": 2, "neutral": 0, "swapped": 6}, "cycle_step_llm_calls": 8, "answer_keys": {"edge_to_remove": 4, "nodes_to_remove": 4}}
