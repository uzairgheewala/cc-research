# AUD-14: discovery wrappers (torch and time series), web demo, report generation

Baseline: a31aa7c (copy at `/home/claude/work/cc_src`). `externals/` (acceleration code, pyCausalFS, NTS-NOTEARS model) is **not** in the copy, except the vendored causal-learn at `/home/claude/work/ccr/Causal-Copilot/externals/causal-learn`. Claims about code in `externals/acceleration` are therefore marked "not verifiable here".
Labels: **[M]** measured (read in the code). **[R]** read in the paper. **[I]** interpretation. **[L]** prior ledger finding.
Repo graph convention: `M[i,j]==1` means j -> i (ledger F7). Codes: 2 undirected, 3 bidirected, 4 o->, 6 o-o, 7 associated.

---

## (a) Wrappers in `causal_discovery/wrappers`

### a.1 Package-level facts

- [M] `wrappers/__init__.py:1` imports `torch` unconditionally. Importing any wrapper, PC included, therefore needs PyTorch, and the CPU-only path is not torch-free.
- [M] `CALM` is listed in `score_based_algorithms` (__init__.py:44) but its import is commented out (__init__.py:25). `AcceleratedPC` is listed (__init__.py:43) but never imported. `TS-CDNOD` (ts_cdnod.py) is neither imported nor listed. [L] Matches F6 (27 names in `__all__`, 25 imported).
- [M] Selection can only pick algorithms that have a profile. Profiles exist for 20 algorithms in `causal_discovery/context/algos/` (rerank.py:44-47 opens `algos/{algo}.txt`), and filter candidates come from `tab_tagging.txt` / `ts_tagging.txt` (filter.py:53-59). `tab_tagging.txt` marks **HITONMB, CALM, CORL, NOTEARSNonlinear, ICALiNGAM, Hybrid as "Availability: Unavailable"** (tab_tagging.txt:300, 315, 330, 345, 360, 375). PCParallel has no tag entry.
- [M] `program.py` unpacks **three** values from every `fit` (program.py:23, 46, 53). There is no try/except, no timeout and no retry around `fit` (program.py:9-82). main.py:262-264 re-raises.

### a.2 Torch-based and GPU-capable wrappers

| Wrapper | Library called | GPU / CPU | Offline? | Defects and notes |
|---|---|---|---|---|
| CORL (corl.py) | gcastle `castle.algorithms.gradient.corl.torch.CORL` (corl.py:13) | `device_type` "auto" -> gpu if CUDA (corl.py:45-46) | [I] yes (local training) | [M] **`fit` returns 2 values** (corl.py:93), while program.py:53 unpacks 3, so selecting CORL crashes with ValueError. Tagged Unavailable. gcastle output is transposed to the repo convention (corl.py:84). |
| GOLEM (golem.py) | gcastle `GOLEM` (golem.py:14) | auto device (golem.py:33-38) | [I] yes | [M] Transposed to the repo convention (golem.py:73). Returns the matrix twice (golem.py:80). Tagged **Available**, 10-20 vars (tab_tagging.txt:114-122). |
| NOTEARSNonlinear (notears_nolinear.py) | gcastle `NotearsNonlinear` (notears_nolinear.py:12) | auto device (notears_nolinear.py:35-40) | [I] yes | [M] Tagged Unavailable. The hyperparameter file is named `NOTEARSNolinear.json` (context/hyperparameters), which does not match the class name `NOTEARSNonlinear`. |
| NTSNOTEARS (nts_notears.py) | `externals.notears.model` (nts_notears.py:16), not in this copy | auto device (nts_notears.py:32-37) | [I] yes if externals are present | [M] Builds `lag_matrix[lag, effect, cause]` (nts_notears.py:93-98), which is consistent with j->i. Prints `p` to stdout (nts_notears.py:65). It has no fitted runtime model (see DOM-12). |
| CALM (calm.py) | causal-learn `ScoreBased/CALM` (vendored, present) | auto `device` (calm.py:36-37) | [I] yes | [M] Not imported by the package (__init__.py:25), so it cannot be selected. The adjacency conversion matches the convention (calm.py:79-86). |
| Hybrid (hybrid.py) | PC/GES wrappers + causal-learn ANM / PNL (hybrid.py:19-25) | CPU (PNL in causal-learn uses torch) | [I] yes | [M] Tagged Unavailable. |
| PC (pc.py) | causal-learn `pc` (CPU) or `externals.acceleration.pc.accelerated_pc` (GPU, pc.py:29, 154) | GPU if CUDA **and** `'gpu'` in `indep_test` (pc.py:140-145) | [I] yes | [M] (1) **Import-time NameError on CUDA machines without the acceleration package.** `logger` is imported only inside `if not cuda_available` (pc.py:31-33), but used unconditionally at pc.py:34. The package import (`__init__.py:5`) would fail. (2) On CPU machines `'fisherz_gpu'` keeps its suffix: only `'_cpu'` is stripped (pc.py:144). The suffixed name then goes to causal-learn (pc.py:169). Avoiding GPU tests on CPU is left to prompt text (hyperparameter_selector.py:79; context/hyperparameters/PC.json:10-11). (3) The GPU path ignores background knowledge (pc.py:147-155). |
| CDNOD (cdnod.py) | causal-learn `cdnod` or `accelerated_cdnod` (cdnod.py:30, 148) | same rule as PC (cdnod.py:132-136) | [I] yes | [M] Same suffix handling. Its import fallback guards `logger` correctly (cdnod.py:31-33). |
| DirectLiNGAM (direct_lingam.py) | causal-learn DirectLiNGAM or `culingam` (direct_lingam.py:18, 26) | GPU if CUDA and `gpu=True`; default False (direct_lingam.py:40, 72) | [I] yes | [M] OK. |
| VARLiNGAM (var_lingam.py) | causal-learn VARLiNGAM or `culingam.varlingam` (var_lingam.py:17, 26) | default **`gpu: True`** (var_lingam.py:127) | [I] yes | [M] (1) A compatibility subclass `AcVarLiNGAMWrapper`, documented as fixing the `'original'` fit-parameter issue, is defined (var_lingam.py:35) but **never used**: `fit` instantiates the raw `AcVarLiNGAM` (var_lingam.py:160). (2) The subclass is defined whenever `cuda_available` (var_lingam.py:34). If CUDA is present but `culingam` is not installed, `AcVarLiNGAM` is undefined and the module raises NameError at import (the except branch at :29-32 only logs). |
| PCMCI (pcmci.py) | tigramite `run_pcmciplus` (pcmci.py:12, 175); GPDC on torch if CUDA (pcmci.py:142-147) | GPU only for `gpdc` | [I] yes | [M] (1) The adjacency is built from **p-values only**: `q_matrix <= pc_alpha` (pcmci.py:183). PCMCI+'s own oriented `graph` output is ignored, so contemporaneous links set both cells and become 2-cycles in the summary. (2) An unknown `indep_test` string (an LLM choice) leaves `cond_ind_test` unassigned, giving UnboundLocalError at pcmci.py:162. (3) Autoregressive links put 1s on the summary diagonal (pcmci.py:184, 195). |

### a.3 Time-series wrappers

| Wrapper | Library | Output convention | Defects |
|---|---|---|---|
| PCMCI | tigramite | `lag_matrix[lag] = matrices[:, :, lag].T` (pcmci.py:184): effect row, cause column. Consistent. | See table a.2. |
| VARLiNGAM | causal-learn / culingam | LiNGAM `B[i,j]` = j->i. Consistent. `lag_matrix` holds **weights**, not 0/1 (var_lingam.py:162, 166). | See table a.2. |
| DYNOTEARS (dynotears.py) | causalnex `from_pandas_dynamic` (dynotears.py:15, 59) | `lagged_adj_matrix[lag, target, cause]` (ts_utils.py:21). Consistent. | [M] Node-name mapping assumes causalnex lists `sm.nodes` variable-major with exactly `max_lag+1` entries per variable (dynotears.py:63-69). [I] If that ordering assumption fails, edges would be attributed to the wrong variables silently; not executed. |
| GrangerCausality (granger_causality.py) | statsmodels VAR / `grangercausalitytests` (granger_causality.py:14-17) | `adj[r, c]=1` when c Granger-causes r (granger_causality.py:104-110). Consistent. | [M] **Works only when column names are integer strings.** It uses `int(e)`, `int(c)`, `int(r)` on column names (granger_causality.py:93, 110, 118), so any named column raises ValueError. pairwise mode sets every diagonal entry to 1 (granger_causality.py:116-118); mv mode initialises every parent set with the node itself (granger_causality.py:34). No `lag_matrix` is returned, so `results.lagged_graph = None` (program.py:77-78). |
| NTSNOTEARS | externals | consistent (see a.2) | - |
| TS-CDNOD (ts_cdnod.py) | causal-learn `cdnod` + `accelerated_cdnod`, imported unguarded at module level (ts_cdnod.py:24) | The comment says "variable i at any lag causes variable j at t=0" and the code stores `summary_adj[i, j] = 1` (ts_cdnod.py:131-136). Under causal-learn's encoding, `adj[i_lag, j_t0] == 1` marks an arrowhead at `i_lag`. | [M] Dead code: not imported anywhere. No temporal tiers are given to CDNOD. [I] The comment, causal-learn's encoding and the repo convention disagree. Edges from the present into the past are not excluded. |

### a.4 Other wrapper-level facts

- [M] Highly correlated features (|r| >= 0.99 by default, program.py:12) are removed before `fit` and re-attached afterwards as code **7** "associated" edges (wrappers/utils/tab_utils.py:515, 556). This is the source of code 7 in outputs. [L] Code 7 is dropped by the bootstrap tally and described to the LLM as an empty sentence (F23).
- [M] Algorithms with PAG/CPDAG marks: FCI emits 4/3/6 (fci.py:147, 152, 159). PC, CDNOD, GRaSP and Hybrid emit 3/2 (pc.py:194, 201; cdnod.py:197, 204; grasp.py:83, 90; hybrid.py:230, 237). GES, FGES, XGES and PCParallel emit 2 (ges.py:91; fges.py:82; x_ges.py:70; pc_parallel.py:104). Each mark is stored in one cell only.
- [M] No wrapper downloads anything. [I] All run offline once dependencies are installed. Remaining network uses are outside the wrappers: `install_packages`/`init_latex` in demo.py:8-56 (commented out at demo.py:57-61), and the runtime estimator's URL fetch for unregistered algorithms (runtime_estimators/runtime_estimator.py:330-336).
- [L] Pass 4a ran 18 algorithms offline. Torch wrappers (GOLEM, CORL, NOTEARS-nonlinear, Hybrid) were not run, and HITON-MB failed once with an index error (ledger Q5, pass4a section 6).

## (b) Web demo path

### b.1 Entry point and differences from `main.py`

- [M] Entry: `python web_demo/demo.py` (README.md:314). `demo.launch(server_name="0.0.0.0", server_port=7860, show_api=False)` (demo.py:2042) has **no `auth=` argument**. The alternative `demo_inf.py` uses `demo.launch(share=True)` (demo_inf.py:1635). [I] `share=True` opens a public Gradio tunnel, so it needs network and exposes the session, and the server's LLM key, to anyone holding the link.
- [M] Session state is a `gr.State` per browser session (demo.py:1672-1683). Global states are pickled to `output_graph_dir/<ALGO>_global_state.pkl` (demo.py:780, 824) and reloaded with `pickle.load` for report selection (demo.py:1158, 1209; report_generation.py:77-78). [I] These are files the app wrote itself, so this is not an external-input deserialization path unless the output directory is shared.

| Aspect | `main.py` | `web_demo/demo.py` |
|---|---|---|
| Effect estimation / attribution | absent | present (see AUD-12) |
| Meaningful-name check | none | LLM yes/no (web_demo/help_functions.py:104-121, substring `'yes' in response.lower()`) |
| LLM refinement (Judge) | always for non-time-series (main.py:298) | **skipped when the LLM says names are not meaningful**: `revised_graph = converted_graph` (demo.py:690-698); also skipped when the user declines (demo.py:708-719) |
| Judge failure | raises | **retries the identical call once**, with no change (demo.py:727-734) |
| Graph refutation | commented out (main.py:320) | `judge.graph_refutation` (demo.py:757; postprocess/judge.py:180-218) |
| User graph edits | none | `parse_user_postprocess` -> `judge.user_postprocess` (web_demo/help_functions.py:747-806; demo.py:796-802) |
| Constant-column removal | none | `remove_constant` (demo.py:261) |
| Missingness / scaling | `missingness=None`, so imputation and z-scoring always run (stat_info_functions.py:872-875, 469-470) | `missing_ratio_table` sets missingness (web_demo/help_functions.py:448; stat_info_functions.py:108-112), so scaling only runs when NaNs exist |
| Time-series flag | LLM query parse (Initialize_state.py:151-153, 185) | separate LLM parse of the user message (web_demo/help_functions.py:331-378) |
| Column names | as in file | spaces replaced by `_` (demo.py:213) |

- [M] `graph_refutation` uses only code-1 edges (judge.py:185) and calls `falsify_graph(..., n_permutations=10)` (judge.py:190). The LLM then writes the interpretation (judge.py:200-215). [I] With 10 permutations the smallest attainable permutation p-value is about 0.1, so the "0.05" decision described in the prompt (judge.py:208) cannot be resolved.

### b.2 LLM calls specific to the web demo (decision-relevant ones)

All go through `web_demo/help_functions.py:44-65`, which builds `LLMClient()` **without args**.

| Site | Decides | Check on the answer |
|---|---|---|
| meaningful_feature_query (:104-121) | whether LLM refinement runs and whether the report treats the data as "real" or "simulated" (report_generation.py:96-99) | [M] Substring "yes" only. |
| heterogeneity_query (:124-167) | domain index | [M] Checked against columns (:154). |
| parse_ts_query (:331-378) | time-series flag, `time_lag`, `time_index` | [M] `time_index` is **not** checked against columns (:372-374). Later `set_index(time_index)` (stat_info_functions.py:837) would raise KeyError. `time_lag` is not type-checked (:369-370). The code writes `user_data.heterogeneous` instead of `statistics.heterogeneous` (:369). |
| parse_var_selection_query (:266-305), LLM_var_selection (:314-329) | feature subsets | [M] partly checked (not analysed line by line) |
| parse_algo_query / parse_algo_selection (:471-560) | user override of the algorithm | [M] not examined in detail |
| parse_hyperparameter_query (:646-745) | user hyperparameters | [M] wrapped in try (:740) |
| parse_user_postprocess (:747-806) | **graph edits** (add/forbid/orient) | [M] Names are validated against `raw_data.columns`, with one retry (:789-799). The prompt contradicts the parser: it asks for tuples `(Age, Height)` (:768-776), but the code splits on `'->'` (:783-785). It also lists column names **with underscores removed** (:771) while validating against underscored names (:791). [I] Edits to any column containing `_` (all multi-word columns after demo.py:213) will tend to fail validation. |
| parse_report_algo_query (:808-829) | which run the report describes | [M] `algos.index(...)` raises ValueError on a name not in the list (:826). |
| LLM_prune indicator (demo.py:713) | continue to refinement or not | [M] bool field |
| Inference parsers | see AUD-12 section 4 | |

### b.3 Credentials handling (patterns only; no values reproduced)

- [M] `LLMClient` reads the provider, model and keys **only from environment variables** (`LLM_PROVIDER`, `LLM_MODEL`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`; llm/llm_client.py:77-95). Its `args` parameter is documented (llm_client.py:70-75) but ignored.
- [M] `.env` is loaded at import by demo.py:5-6, demo_config.py:7 and causal_inference/help_functions.py:8-9 (relative path `.env`).
- [M] `DemoConfig` copies `OPENAI_API_KEY` into a dataclass field `apikey` (demo_config.py:26). `process_message` then copies every config field onto the Gradio `args` object (demo.py:194-198). [I] The key therefore lives in per-session Gradio state as well as in the environment. Its defaults (`LLM_PROVIDER` "ollama", model "llama3.2", demo_config.py:24-25) differ from `LLMClient`'s defaults ("openai", "gpt-4o-mini", llm_client.py:77-87). The config values are never used by `LLMClient`, so the demo's effective provider is decided by the environment alone.
- [M] Hard-coded OpenAI **organization and project identifier** defaults appear in `argparse` blocks under `__main__` in user/discuss.py:100-113, report/report_generation.py:1114-1126, report/inference_report_generation.py:359-371, causal_inference/main.py:78-90, and in a commented-out block at preprocess/dataset.py:253-265 (values not reproduced here). No API key literal was searched for (instruction). `--apikey` defaults are `None` where present.
- [M] demo.py:8-56 contains shell `subprocess.run(..., shell=True)` installers (apt-get, wget | sh, pip). They are not called (demo.py:57-61).

## (c) Report generation (`report/`)

### c.1 What the LLM writes and what the code writes

| Report part | Source | Label |
|---|---|---|
| Title / dataset name | LLM guesses the name from `self.data_file` = `output_graph_dir` (report_generation.py:102, 131-140) | [M] LLM |
| Introduction | LLM from the elicited knowledge prose (report_generation.py:142-159) | [M] LLM |
| Background (sections 1, 2) and the "graph suggested by LLM" figure | LLM summary plus an LLM-extracted causal-relation list, plotted as `potential_relation.pdf` (report_generation.py:161-290) | [M] LLM. Pairs are filtered to real column names (:250-253). |
| Data preview | `df.head().to_latex()` of `processed_data`, i.e. scaled values on the CLI (report_generation.py:930-942) | [M] data. With more than 20 columns, 10 columns are chosen with **unseeded** `np.random.choice` (:933). |
| Data property table | `statistics` fields (report_generation.py:292-311) | [M] data/code. Linearity and Gaussianity may come from the LLM query parse (see DOM-12 / REP-04 D15). |
| EDA | code-generated tables and plots (report_generation.py:338-416) | [M] data |
| Procedure section | fixed template text (report_generation.py:462-505) | [M] **Hard-coded claims**: "top three chosen algorithms" (:476), while `TOP_K = 2` (filter.py:10); ">90% added, <10% removed, moderate to LLM" (:492-494); "we employed a voting mechanism" and "LLM recommendations were not allowed to override high-confidence decisions" (:502). The CLI and demo call Judge with `voting_num=1` (main.py:298; demo.py:729), which takes the single-call path (judge_functions.py:421). [L] `fixed_pairs` is empty (F10, D1). |
| Graph result analysis | LLM prose from the edge list of `converted_graph`, i.e. the **initial** graph (main.py:338; report_generation.py:549-585) | [M] LLM |
| Revision section | Bootstrap and LLM records, first 10 LLM directions (report_generation.py:587-665) | [M] code. The "only a part" branch is dead: the code tests `len > 10` after truncating to 10 (:626-628). |
| Reliability analysis | The LLM is given bootstrap probabilities and asked to sort edges into high/moderate/low **itself** and "Do Not include Numerical Numbers" (report_generation.py:743-789, :763) | [M] LLM performs the classification. There is no code check that its buckets match the numbers. |
| Refutation | LLM paragraph (judge.py:200-218) | [M] LLM |
| Algorithm comparison | LLM (report_generation.py:806-855) | [M] LLM |
| Abstract | **LLM prompt with no content at all**: "Write an abstract for a causal discovery report. Summarize the dataset, methodology, and key findings" (report_generation.py:857-867), with no data, results or prior sections passed | [M] LLM, ungrounded. [I] Any dataset name, method or finding in the abstract is invented by the model. |
| Keywords, conclusion | LLM from earlier LLM sections (report_generation.py:869-890) | [M] LLM |
| Inference sections | LLM prose, re-processed by a second LLM call (`fix_latex_itemize_LLM`, report/help_functions.py:54-62) | [M] see AUD-12 section 7 |

### c.2 Failure handling

- [M] LaTeX compile errors return False without raising (report_generation.py:21-64). `main.py` regenerates the **whole report** up to 2 more times while `report.pdf` is missing (main.py:350-357). Each regeneration repeats every LLM call.
- [M] `latex_bug_checking` (an LLM repair of LaTeX) exists (report_generation.py:1036-1063) but its call is commented out (:1074-1076).
- [M] The background parser uses a schema (`response_format=CausalRelation`, report_generation.py:235 via report/help_functions.py:168-184). If validation fails, `DictAsObject` is returned (llm_client.py:59-63), and `rel.cause` on a dict item raises AttributeError (report_generation.py:236-238). There is no try block.
- [M] `report/report_generation.py:9` imports `plumbum.cmd.latexmk` at import time. [L] Matches F22: the module fails to import without latexmk.

## Findings

- F1 [M] CORL `fit` returns 2 values, but `program.py` unpacks 3, so selecting CORL crashes (wrappers/corl.py:93; program.py:53).
- F2 [M] Granger causality calls `int()` on column names, so it fails on any dataset with named columns (wrappers/granger_causality.py:93, 110, 118).
- F3 [M] pc.py uses `logger` outside the branch that imports it. On a CUDA machine without `externals.acceleration`, importing the wrappers package fails (wrappers/pc.py:30-34).
- F4 [M] var_lingam.py defines its GPU fix-up subclass but never uses it. With CUDA and no `culingam`, the module fails at import (wrappers/var_lingam.py:34-35, 160).
- F5 [M] On CPU machines the PC/CDNOD `*_gpu` test names are passed unchanged to causal-learn; GPU avoidance relies on prompt text (wrappers/pc.py:140-145; cdnod.py:132-136).
- F6 [M] PCMCI's adjacency comes from p-value thresholds only. PCMCI+ orientations are discarded, contemporaneous links become symmetric, and an unknown `indep_test` raises UnboundLocalError (wrappers/pcmci.py:136-162, 183-195).
- F7 [M] `wrappers/__init__.py:1` imports torch unconditionally. CALM is listed but not imported (:25, :44). Six profiled algorithms are tagged Unavailable (context/algos/tab_tagging.txt:300-375).
- F8 [M] TS-CDNOD is dead code with an unguarded import of the acceleration module, and its comment and code disagree on edge orientation (wrappers/ts_cdnod.py:24, 131-136).
- F9 [M] The web demo skips all LLM refinement when an LLM judges the column names "not meaningful" (web_demo/demo.py:690-698; web_demo/help_functions.py:110-114).
- F10 [M] The web demo retries a failed Judge call once, identically (web_demo/demo.py:727-734).
- F11 [M] `demo_inf.py` launches with `share=True`, and `demo.py` binds 0.0.0.0 without auth (web_demo/demo_inf.py:1635; web_demo/demo.py:2042).
- F12 [M] `LLMClient` ignores `args` and the demo config; provider, model and key come only from environment variables (llm/llm_client.py:66-99; web_demo/demo_config.py:24-26).
- F13 [M] Graph-edit parsing has a self-contradictory prompt (tuples vs `->`, underscores stripped vs validated) (web_demo/help_functions.py:768-791).
- F14 [M] The time index chosen by the LLM is not checked against the columns (web_demo/help_functions.py:372-374).
- F15 [M] The report abstract is generated from a prompt with no data or results (report/report_generation.py:857-867).
- F16 [M] The report's procedure section hard-codes behaviour the code does not perform: voting, non-override of bootstrap, "top three" (report/report_generation.py:476, 490-503 vs main.py:298, filter.py:10).
- F17 [M] Edge-confidence tiers in the report are assigned by the LLM, not by code, and the LLM is told to omit numbers (report/report_generation.py:743-789).
- F18 [M] Graph refutation uses 10 permutations against a 0.05 decision rule and only code-1 edges (postprocess/judge.py:185-190).
- F19 [M] Report title and dataset name are LLM guesses from the output directory path (report/report_generation.py:102, 131-140).
- F20 [M] With more than 20 columns, the data preview selects columns with unseeded randomness (report/report_generation.py:933).
