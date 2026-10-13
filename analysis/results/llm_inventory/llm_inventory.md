# LLM dependency inventory (pass 3)

Static scan of the tree at baseline a31aa7c, classified by hand, reconciled with 107 recorded LLM calls from the runs in `runs/`.

## Gates

- G1_ast_matches_text: **PASS**
- G2_all_points_classified: **PASS**
- G3_every_recorded_caller_is_a_known_site: **PASS**
- G4_recorded_flags_match_static: **PASS**

## Counts

- Call sites that issue a request (AST): 51, of which 47 are outside `llm/`. Textual occurrences: 51.
- Logical LLM points (direct sites that are not generic wrappers, plus each caller of `LLM_parse_query`): **88**.
- By path: inference (web demo) 30; web demo only 23; report 19; CLI+web discovery 11; benchmark/test 2; online simulation mode 1; dead code (no caller) 1; dead code (only call is commented out) 1.
- By kind: descriptive 30; decision 29; interpretation 19; - 4; format 3; descriptive, reused as input 2; interpretation + validation by LLM 1.
- Points that edit the causal graph directly: 3 (`postprocess/judge_functions.py:288`, `postprocess/judge_functions.py:556`, `web_demo/help_functions.py:780`).
- Decision points whose answer has no check before use (or was not examined): 26 of 29 decisions.
- Classification basis: read 47; prompt 41.

## Sites observed in recorded runs

| Site | Role | Real calls | Stub calls | Prompt tokens (real) | Completion tokens (real) |
|---|---|---|---|---|---|
| `causal_discovery/filter.py:33` | shortlist 2 algorithms | 2 | 3 | 9303 | 1042 |
| `causal_discovery/hyperparameter_selector.py:104` | choose hyperparameters | 2 | 3 | 11990 | 716 |
| `causal_discovery/rerank.py:103` | pick the algorithm (LLM also does the 0.7/0.3 score arithmetic) | 2 | 3 | 23347 | 978 |
| `global_setting/Initialize_state.py:158` | extract user intent into 9 fields | 2 | 3 | 1222 | 134 |
| `postprocess/judge_functions.py:288` | edit the graph: A/B/C/D per variable pair | 16 | 21 | 36296 | 2478 |
| `preprocess/dataset.py:121` | elicit domain knowledge as prose | 2 | 3 | 1088 | 868 |
| `preprocess/dataset.py:138` | elicit domain knowledge as prose | 2 | 3 | 380 | 1075 |
| `report/report_generation.py:132` | write report prose | 2 | 3 | 182 | 6 |
| `report/report_generation.py:152` | write report prose | 2 | 3 | 1302 | 353 |
| `report/report_generation.py:578` | write report prose | 4 | 6 | 1214 | 1302 |
| `report/report_generation.py:778` | write report prose | 2 | 3 | 1025 | 281 |
| `report/report_generation.py:858` | write report prose | 2 | 3 | 142 | 248 |
| `report/report_generation.py:881` | write report prose | 2 | 3 | 3466 | 508 |
| `user/discuss.py:10` | strip LaTeX from the report | 2 | 3 | 8265 | 2970 |

## CLI-path and report sites never exercised by the recorded runs

- `causal_discovery/runtime_estimators/runtime_estimator.py:380` RuntimeEstimator._query_llm (guess a runtime model for an algorithm without one)
- `postprocess/judge_functions.py:556` LLM_remove_cycles (choose which edge of a cycle to delete)
- `report/report_generation.py:176` Report_generation.background_prompt (write report prose)
- `report/report_generation.py:847` Report_generation.comparision_prompt (write report prose)
- `report/report_generation.py:870` Report_generation.keyword_prompt (write report prose)
- `report/report_generation.py:908` Report_generation.latex_convert (reformat / repair LaTeX)
- `report/report_generation.py:1046` Report_generation.latex_bug_checking (reformat / repair LaTeX)
- `user/discuss.py:21` Discussion.interaction (answer follow-up questions (history is not sent))

## Decision points on the discovery path

| Site | Decides | Effect on the causal output | Check on the answer | Kept in |
|---|---|---|---|---|
| `causal_discovery/filter.py:33` | shortlist 2 algorithms | indirect: decides which algorithms can run | none here; unknown names dropped later (rerank.py:58) | algorithm.algorithm_candidates + logging.select_conversation |
| `causal_discovery/hyperparameter_selector.py:104` | choose hyperparameters | indirect: test type, alpha, depth etc. | keys filtered to primary parameters (drops background_knowledge); values not checked against allowed list | algorithm.algorithm_arguments_json + logging.argument_conversation |
| `causal_discovery/rerank.py:103` | pick the algorithm (LLM also does the 0.7/0.3 score arithmetic) | indirect: decides the algorithm | none; name must be a wrapper attribute or execution fails | algorithm.algorithm_optimum + logging.select_conversation |
| `causal_discovery/runtime_estimators/runtime_estimator.py:380` | guess a runtime model for an algorithm without one | indirect: runtime text shown to the rerank prompt | none | written to a JSON file in the repo |
| `global_setting/Initialize_state.py:158` | extract user intent into 9 fields | indirect: can fix linearity/Gaussianity (skipping the statistical tests), the algorithm, alpha, time-series flag | none on values; missing key raises KeyError | only the resulting fields; prompt and answer not kept (logging.query_conversation unused) |
| `postprocess/judge_functions.py:288` | edit the graph: A/B/C/D per variable pair | direct: adds, orients and deletes edges | none: any A/B/C applied; unparseable pairs silently skipped; D not recorded; unbounded retry on format error | results.llm_errors (A/B/C with explanation) |
| `postprocess/judge_functions.py:556` | choose which edge of a cycle to delete | direct: deletes an edge | none | not kept |
| `preprocess/stat_info_functions.py:140` | choose which 30-50%-missing variables to keep | indirect: changes the variable set | none | user_data.llm_drop_features |
| `web_demo/help_functions.py:110` | decide whether variable names are meaningful | indirect: gates whether LLM edge review is offered | none | user_data.meaningful_feature |
| `web_demo/help_functions.py:323` | pick 10 variables when there are too many | display only (visual_selected_features) | none | visual_selected_features |
| `web_demo/help_functions.py:709` | parse AND validate user hyperparameters | indirect: hyperparameters | the LLM itself is the validator | algorithm.algorithm_arguments |
| `web_demo/help_functions.py:780` | parse user edge edits (add / forbid / orient) | direct: user edits applied to the graph | pydantic class, lenient; names looked up afterwards | not kept (only the edited graph) |

The full table (all 88 points, every field) is `llm_inventory.csv`.
