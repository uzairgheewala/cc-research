Tickets: TEAM-13, AUD-16

# Causal-Copilot code notes from the "Inside Causal-Copilot" pass (20 Oct 2026)

While writing the step pages of the code-explorer site (site/copilot/), every function on the command-line path was read at
upstream a31aa7c. These are the things that reading found that earlier passes had not recorded. Label for every item:
**partial** (read in the source line by line; not executed, not seen in a recorded run, unless the item says so). Each item
names the function so it can be checked; the step pages link the code.

## Setup, data and the question
1. The user's question is parsed by the model inside `global_setting/Initialize_state.py::global_state_initialization`
   (nine fields), not in main.py's step 3; `main.py::process_user_query` only splits `key: value` text, and its
   `selected_algorithm` key is printed but never stored.
2. If the query parse returns a `domain_index`, the initialiser reads `raw_data.columns` while `raw_data` is still None (the
   data are loaded in the next step): a crash on that path.
3. `--output-report-dir` and `--output-graph-dir` are parsed but not used; output folders come from the file name and a
   timestamp. In real-data mode the file is read twice, and a folder path fails unless `--data_mode` is simulated.

## Statistics
4. For tabular data the imputer runs and fills the table in place before the missing-value check, so `missingness` ends
   False and the statistics text says there are no missing values even when there were (a minimal pandas check of the
   in-place fill confirmed the mechanism; the pipeline itself was not run on data with missing values).

## Exploratory analysis
5. The EDA results reach no decision: nothing after EDA reads `results.eda` except the report's fixed text. The
   stationarity test is not inside a try block, so an unusual series ends the whole run.

## Choosing the algorithm
6. The reranker's filter of unknown algorithm names (`causal_discovery/rerank.py::Reranker.filter_algo_candidates`) works on
   a local copy; `create_prompt` still opens `algos/<name>.txt` for every shortlisted name, so an unknown name from the model
   stops the run rather than being dropped (pass 3 recorded it as dropped at rerank.py:58).
7. The shortlist's descriptions and the ranking reason are not passed on to later prompts; the model does the 0.7 / 0.3
   theoretical / empirical scoring itself and the code does not check the name it returns.
8. Hyperparameter selection writes its prompt into the repository on every run (`context/hp_rerank_prompt_test.txt`).
9. The runtime estimator's model call cannot fire with the shipped files.

## Running the algorithm
10. `wrappers/utils/tab_utils.py::restore_original_node_indices` returns the graph unchanged; `info["high_corr_features_removed"]`
    holds the columns that were kept, not those removed.
11. Only primary parameters survive hyperparameter selection, so PC's background knowledge can never reach it; the
    NOTEARSLinear settings file names `lambda_1` while the code expects `lambda1`, so that choice is dropped; PCParallel has
    no profile or settings file, so normal selection cannot pick it.
12. Graph encoding used by every wrapper: `M[i, j] = 1` means j -> i; codes 2 (undirected) and 3 (bidirected) are stored in
    one cell only (above the diagonal for PC); 7 marks the link added for a set-aside correlated column.

## Refinement, evaluation and the report
13. At S2 (the model's edge review), `results.bootstrap_probability` is still None, so the review prompt carries no bootstrap
    frequencies (a recorded prompt confirms it: seen in a recorded run).
14. A/B answers of the review are added to the shared edge list, so later prompts present the model's own edges as findings
    of the statistical algorithm.
15. `user_data.meaningful_feature` is never set on the command-line path, so the report always uses the "simulated"
    template: no background section, no record of the model's edits, no revised graph.
16. The follow-up discussion (`user/discuss.py`) does not send its history, so the model answers without the report;
    `check_cycle` prints each cycle against the causal direction.
