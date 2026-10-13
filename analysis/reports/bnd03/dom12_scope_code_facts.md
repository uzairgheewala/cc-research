# DOM-12: what the code offers for hidden confounders, time series and 100+ variables

Baseline: a31aa7c (`/home/claude/work/cc_src`; `externals/acceleration` not in the copy).
Labels: **[M]** measured (code read). **[X]** executed offline. **[L]** ledger. **[I]** interpretation (only in the last section).

## (i) Hidden common causes

| Fact | Location |
|---|---|
| [M] FCI is the only wrapper that emits PAG marks: 1 directed, 4 `o->`, 3 `<->`, 6 `o-o`. It never emits 5 (`o-`). | wrappers/fci.py:103-135, 137-160 |
| [M] PC, CDNOD, GRaSP and Hybrid can also emit code 3 when causal-learn leaves conflicting arrowheads; this is not a latent-variable claim. | wrappers/pc.py:194; cdnod.py:197; grasp.py:83; hybrid.py:230 |
| [M] Each symmetric mark is stored in one cell only; which cell depends on the wrapper. | fci.py:150-159; [L] F7 |
| [M] Whether hidden confounders are suspected is decided only by LLM prompts. The query parse has no key for it (9 keys). The knowledge prompt asks the LLM to list "Potential unmeasured variables". The rerank prompt asks "Are hidden confounders likely in THIS domain?". | Initialize_state.py:124-156; preprocess/dataset.py:102; context/algo_rerank_prompt.txt:66 |
| [M] Selector tags rate "Latent Variable Tolerance: Robust" for FCI and BAMB only. BAMB is a Markov-blanket method whose output (MB2CPDAG) carries no PAG marks. | context/algos/tab_tagging.txt:135, 274; wrappers/utils/tab_utils.py:44-86 |
| [M][L] Refinement keys on directed-edge bootstrap frequency only. Existing edges whose directed frequency is at most 0.1 are deleted, and that includes every consistently found PAG mark. | judge_functions.py:221-237; judge.py:78-84; [L] F23, offline survival of `o-o` 12%, `<->` 12%, `o->` 25% |
| [M] The LLM review can only add **directed** edges (code 1) or delete edges. It cannot write a PAG mark. | judge.py:103-110 |
| [M] KCI pruning and cycle handling treat every non-zero cell as an arrow. | judge_functions.py:473-483, 564-594; [L] F28b |
| [M] In the web demo, refinement is skipped when the LLM judges names "not meaningful". FCI's PAG marks then reach the user unchanged. | web_demo/demo.py:690-698 |
| [M][X] Effect estimation converts every non-zero mark to a directed edge and treats `<->` and `o->` as causal parents when choosing confounders. | causal_inference/help_functions.py:11-16; inference.py:242-246; evidence/mt_confounders_output.txt |
| [M] The scorer maps a predicted `<->` to a directed edge in the true direction. There is no PAG-aware metric. `GraphEvaluator(has_hidden_confounders=False)` is the default. | evaluation/evaluator.py:20, 183-190 |
| [M] Graph refutation keeps only code-1 edges. | postprocess/judge.py:185 |

## (ii) Time series

| Fact | Location |
|---|---|
| [M] Algorithms offered to the selector for time series: PCMCI, VARLiNGAM, DYNOTEARS, GrangerCausality, NTSNOTEARS. | context/algos/ts_tagging.txt:92-170; wrappers/__init__.py:49 |
| [M] Time-series mode is set **only by the LLM**: on the CLI from the query parse, default False "only if the user explicitly asks"; in the demo from a separate LLM parse of the user message. There is no data-driven detection. | Initialize_state.py:151-153, 185; web_demo/help_functions.py:331-378 |
| [M] The demo's time index and lag come from the LLM without a column or type check. | web_demo/help_functions.py:369-374; used at stat_info_functions.py:836-839 |
| [M] Lag estimation runs on at most 50 randomly sampled variables (stdlib `random`, which semopy seeds at import [L F8a]). | stat_info_functions.py:336-352, 905 |
| [M] Selection uses `ts_tagging.txt` and `algorithm_performance_analysis_ts.json`. | filter.py:53-56; rerank.py:31-34; hyperparameter_selector.py:53-56 |
| [M] Lagged output is stored in `results.lagged_graph` when the wrapper returns `info['lag_matrix']` (PCMCI, VARLiNGAM, DYNOTEARS, NTSNOTEARS). Granger returns none. | program.py:59-78; granger_causality.py:170-176 |
| [M] CLI with a lagged graph: no refinement and no Judge. The code then plots `revised_graph`, which is None, giving a crash (code trace, not executed). CLI without a lagged graph (e.g. Granger): the tabular branch runs Judge with `ts=False` bootstrap on time-series rows. | main.py:268-277, 287-298, 303-308; judge.py:58-59; state.py:91 |
| [M] Wrapper defects: Granger needs integer column names; PCMCI uses p-values only, so contemporaneous links become symmetric; VARLiNGAM's GPU subclass is unused; DYNOTEARS assumes an ordering of causalnex nodes; TS-CDNOD is dead code. | AUD-14 a.2-a.3 (granger_causality.py:93, 110, 118; pcmci.py:183-195; var_lingam.py:35, 160; dynotears.py:63-69; ts_cdnod.py:24) |
| [M] The scorer evaluates the summary graph with the diagonal excluded, and raises on symmetric pairs. | evaluator.py:47-52, 351-354 |
| [M] The effect-estimation path has no time-series handling (rows treated as i.i.d.). | causal_inference/inference.py (no lag or time-index use) |

## (iii) 100+ variables

| Fact | Location |
|---|---|
| [M] Tags give "Scalability >100 vars" to PC, CDNOD and FGES; 50-100 to XGES and DirectLiNGAM. The selection priority switches to scalability first at 50 or more and at 100 or more variables. | tab_tagging.txt:24-28, 91, 168, 182, 199, 245 |
| [M] GPU paths: PC and CDNOD switch to `externals.acceleration` when `indep_test` contains "gpu" and CUDA is present; DirectLiNGAM and VARLiNGAM use `culingam`; GOLEM, NOTEARSNonlinear, NTSNOTEARS, CORL and CALM run on torch devices. The acceleration code is not in this copy (not verifiable here). | pc.py:140-155; cdnod.py:132-148; direct_lingam.py:72; var_lingam.py:159-162; golem.py:33-38 |
| [M] The prompts tell the LLM to choose GPU tests "for large datasets (variable size > 150)". On CPU, a `_gpu` test name is passed through unchanged. | context/hyperparameters/PC.json:10-11; pc.py:140-145 |
| [M] Other scaling aids: correlated-feature collapsing (|r| >= 0.99) before `fit`, re-attached as code 7 afterwards; FGES from `externals.acceleration.fges`; PCParallel (gcastle), which is not in the tags and so cannot be selected. | program.py:11-42; tab_utils.py:515, 556; fges.py:13; pc_parallel.py:14 |
| [M] There is no execution timeout in the pipeline. The user's wait time (default 1440 min) is only text in prompts. | program.py:9-82; state.py:78; filter.py:77; rerank.py:66 |
| [M] Runtime estimator: a per-algorithm formula (`complexity_terms.json`) with coefficients from `context/benchmarking/acceleration_fit.json`, fed only `samples` and `variables`. Density is fixed at 0.2. The floor is `min_runtime` = 60 s. | rerank.py:100, 121-142; runtime_estimator.py:91-110, 221-240; complexity_terms.json |
| [M] Coverage: `acceleration_fit.json` has 20 algorithms. **NTSNOTEARS and PCParallel have no fit.** For those the estimator opens `merged_results.json`, which is absent, the exception is caught, and the runtime becomes `inf`. | runtime_estimator.py:40-55; rerank.py:131-134 |
| [M] Unregistered algorithms: the estimator asks an LLM for complexity terms (it may fetch code by URL), **writes them back to `complexity_terms.json`**, and evaluates them with `eval` (restricted builtins). | runtime_estimator.py:305-367, 127, 139-159 |
| [M] Refinement cost grows with p: the bootstrap re-runs the algorithm 20 times; the LLM is asked about every pair and self-pair; KCI runs one unconditional test per pair on the full data **before** checking whether an edge exists. | state.py:43; judge_functions.py:236, 477-480; [L] F8, F9 |
| [M] Presentation limits: the EDA caps the plotted features; the demo asks for "important features" above 20 columns (visualisation only); the report preview samples 10 columns above 20 (unseeded). | eda_generation.py:63; demo.py:216; report_generation.py:931-933 |
| [M] Effect estimation: anomaly and distribution attribution cut the graph to at most 10 nodes. | inference.py:413-424, 606-612 |

## Quarter 1 vs Quarter 2 (interpretation)

- [I] Quarter 1 can cover hidden confounders at the level of **measuring what happens to PAG marks**: the FCI wrapper is runnable on CPU, and our refinement measurements (bootstrap deletion of `o-o`/`<->`, LLM writing only `->`) already form a complete Q1 result. A PAG-preserving refinement or a PAG-aware scorer is Q2 work.
- [I] Time series should move to Quarter 2. The CLI path is broken after discovery (main.py:307), Granger fails on named columns, time-series mode depends on an LLM flag, and none of these wrappers have been run by us (ledger Q5). In Q1 at most a static note and one offline smoke run of PCMCI/VARLiNGAM/DYNOTEARS with patched names.
- [I] 100+ variables: the scaling path depends on CUDA and on `externals/acceleration` (which we have not read). Refinement cost is O(p^2) LLM questions plus O(p^2) unconditional KCI tests. This belongs in Quarter 2. In Q1 we can measure the CPU paths (FGES, PC with Fisher-z, XGES) offline at 50-100 variables without the LLM.
- [I] Across all three, the scorer's oracle orientation (evaluator.py:154-215) must be replaced before any Q2 comparison with the paper's numbers.
