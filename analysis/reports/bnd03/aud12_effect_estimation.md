# AUD-12: audit of `causal_inference/` (effect estimation path)

Baseline: Causal-Copilot upstream commit a31aa7c (copy at `/home/claude/work/cc_src`, without data/, output/, asset/, externals/). Paper: arXiv 2504.13263v2.
Method: static read of every Python file under `causal_inference/`, the web-demo stages that call it, `llm/llm_client.py` and `report/inference_report_generation.py`. Two offline micro-tests, no LLM or network (scripts and outputs in `evidence/`).
Labels: **[M]** measured (read in the code; cited file:line). **[X]** measured by running repo functions offline. **[R]** read in the paper. **[I]** interpretation. **[L]** prior finding taken from the research ledger, not re-done here.

---

## 1. Entry points and whether the pipeline reaches them

| Entry | How it reaches `causal_inference` | Status |
|---|---|---|
| `main.py` (CLI) | It never imports `causal_inference` (imports at main.py:7-18; steps 1-8 at main.py:166-381). | [M] Not reached. The CLI does discovery, refinement, report and a Q&A discussion only. |
| `report/report_generation.py` | Imports `Inference_Report_generation` (report_generation.py:15). It is called only when `inference.task_index != -1` (report_generation.py:977-983). On the CLI `task_index` stays at its default. | [M] Reached for the report only, and only from the web demo. |
| `web_demo/demo.py` (Gradio) | Imports `Analysis` (demo.py:86) and runs stages `parse_task` -> `inference_info_collection_*` -> `method_selection` -> `analyze_causal_task` (demo.py:863-1125). | [M] **The only working route to effect estimation.** |
| `web_demo/demo_inf.py` | Same imports (demo_inf.py:83, 88) and the same stages (Analysis at demo_inf.py:982, 1052, 1105). It launches with `share=True` (demo_inf.py:1635). | [M] Alternative demo. |
| `causal_inference/main.py` | `main(global_state, args)` (main.py:13-45). | [M] **Broken in two independent ways.** (a) `LLM_parse_query` returns a plain dict (help_functions.py:175-182, llm_client.py:184-190), so `parsed_response.tasks` raises AttributeError (causal_inference/main.py:32). (b) `analysis.forward(task, desc, key_node)` passes 3 arguments, but the method needs 4 (inference.py:1329), and its result is unpacked into 2 names. |
| `causal_inference/inference.py __main__` | It needs a hard-coded pickle under `./demo_data/...` (inference.py:1546). | [M] Developer harness, not an entry point. |

[I] Effect estimation is a web-demo feature. Live runs of the CLI pipeline (ledger: 84 runs) never exercised it. The ledger's open question Q7 ("causal inference path mostly unread") is answered by this file.

## 2. Flow in the web demo (treatment effect task)

1. [M] The task list is parsed by an LLM (help_functions.py web_demo:831-857, schema `InfList`). Only `key_node_list[0]` is checked against the columns (demo.py:873). Other key nodes are not checked.
2. [M] Treatment: `parse_treatment` returns free LLM text (web_demo/help_functions.py:891-899). It is checked against the columns at demo.py:932. In the counterfactual path it is **not** checked (demo.py:901). In the binary re-ask path it is not checked either (demo.py:961).
3. [M] If the treatment is not binary, the demo binarizes it at the median **in place in `processed_data`** (demo.py:943-946). It also sets the column type to `'category'` in lower case, while every other consumer compares with `'Continuous'`/`'Category'`.
4. [M] Confounders: `Analysis._identify_confounders` (inference.py:222-252) reads `results.revised_graph`. The confounder list is then the union of "confounders" and "potential confounders" (demo.py:979-980). The user may add more names through an LLM parser (demo.py:994-1004).
5. [M] Heterogeneity variables `X_col` come from `LLM_select_hte_var` (help_functions.py:199-214; called at demo.py:1032). This call is made on every path, including when the user answers "no".
6. [M] Method choice is a fixed rule (demo.py:1047-1061): IV if `contains_iv` finds an instrument; otherwise CEM or PSM when there are 1-5 confounders (CEM if most confounders are discrete); otherwise DML if n > 2000, else DRL. The user may override the choice through an LLM parser (web_demo/help_functions.py:564-617).
7. [M] `Analysis.forward` (inference.py:1329-1474) runs the estimator. One LLM call then turns the numbers into prose (`causal_inference/analysis.py`). The demo stores `{'response': info, 'figs': figs}` (demo.py:1117-1118), and the report later reads it.

## 3. Estimators and libraries

| Method key | Classes (file) | Library | Reachable? |
|---|---|---|---|
| `dml` | DML, LinearDML, SparseLinearDML, CausalForestDML (DML/wrappers/estimator.py:17-223) | econml.dml | [M] yes |
| `drl` | DRL, LinearDRL, SparseLinearDRL, ForestDRL (DRL/wrappers/estimator.py:20-241) | econml.dr | [M] yes |
| `iv` | DRIV, LinearDRIV, SparseLinearDRIV, ForestDRIV (IV/wrappers/estimator.py:17-207) | econml.iv.dr | [M] yes, when `contains_iv` finds an instrument (demo.py:1047-1051). If the user picks IV by hand, the demo refuses with "instrumental variable doesn't exist", whatever the graph shows (web_demo/help_functions.py:603-606). |
| `propensity_score` | `_propensity_score_matching` (inference.py:147-201) | sklearn LogisticRegression + 1-NN | [M] yes |
| `cem` | `_coarsened_exact_matching` (inference.py:203-220) | CEM_LinearInf | [M] yes |
| `linear_regression` | `estimate_effect_linear` (inference.py:1073-1125) | dowhy CausalModel | [M] No: the demo never sets this key. The branch is also broken: it uses the undefined global `args` (inference.py:1437) and the unassigned `figs` (inference.py:1439). |
| MetaLearners | SLearner, TLearner, XLearner, DomainAdaptationLearner (MetaLearners/wrappers/estimator.py) | econml.metalearners, xgboost | [M] Imported (inference.py:44-46) but never called ("TODO: Add MetaLearner Estimation", inference.py:1370). |
| Uplift | CausalML S/T/X/R learners, uplift trees (Uplift/wrappers/causalml_wrappers.py) | causalml | [M] Never imported outside its folder. The branch is commented out (inference.py:1393-1406). |
| Feature importance | `feature_importance` (inference.py:106-145) | shap + LinearRegression / RandomForest | [M] yes. SHAP is computed on **all other columns** (inference.py:110), not only the causal parents. |
| Anomaly attribution | `attribute_anomalies` (inference.py:350-528) | dowhy.gcm | [M] yes |
| "Counterfactual Estimation" | `simulate_intervention` (inference.py:1178-1294) | dowhy.gcm `interventional_samples` | [M] yes. It is an **interventional shift**. `counterfactual_estimation` (inference.py:1127-1176) is never called. |
| Distributional change | `attribute_distributional_changes` (inference.py:530-713) | dowhy.gcm | [M] Not offered by the task prompt (causal_inference/context/query_prompt.txt:6). The branch returns a 2-tuple while callers unpack 3 (inference.py:1462 vs demo.py:1105). |
| Sensitivity / refutation | `sensitivity_analysis` (inference.py:1297-1326) | dowhy refuters | [M] Defined but never called. |

## 4. Every LLM call on this path

`LLM_parse_query` in `causal_inference/help_functions.py:175-182` passes `json_response=bool(format)` but never passes `response_format`. [M] As a result the pydantic class is never applied: the client returns the raw parsed dict (llm_client.py:184-190), and invalid JSON raises ValueError (llm_client.py:203). The web-demo helper does pass `response_format` (web_demo/help_functions.py:50-56). Even so, a response that fails the schema falls back silently to a `DictAsObject` (llm_client.py:59-63), and a missing field then raises AttributeError.

| # | Site | What it decides | Validated? | Malformed JSON / missing key |
|---|---|---|---|---|
| 1 | `parse_inference_query` (web_demo/help_functions.py:852) | task list, outcome per task | Only `key_node[0]` is checked against the columns (demo.py:873). Task names are not checked against the 4 allowed names. | AttributeError via DictAsObject. The stage has no local try block (only `analyze_causal_task` has one, demo.py:1104-1116). The error is caught by the outer handler (demo.py:186 / 1270-1279), which resets the whole session to `initial_process`, so the user must re-upload. |
| 2 | `parse_treatment` (web_demo/help_functions.py:891-899) | the treatment column | Checked at demo.py:932. Not checked at demo.py:901 or demo.py:961. | Free text, so no JSON. |
| 3 | `parse_shift_value` (web_demo/help_functions.py:901-906) | shift size for "counterfactual" | `float` field. None is handled (demo.py:914-925). | AttributeError if the field is missing. |
| 4 | `LLM_select_hte_var` (help_functions.py:199-214) | heterogeneity variables X | **No check** that the names are columns, nor that they differ from treatment, outcome or confounders. | `response['hte_variable']` KeyError (help_functions.py:214). An unknown name gives a KeyError later at `data[self.X_col]` (e.g. DML/wrappers/estimator.py:32) and at `data_type_column[var]` (help_functions.py:47). |
| 5 | `LLM_select_confounders` (help_functions.py:184-197) | confounders | none | Unused: its call is commented out in demo.py. |
| 6 | `parse_var_selection_query` (web_demo/help_functions.py:266-305), added confounders | extra W columns | Partly checked inside the helper (not analysed further). | not examined |
| 7 | `parse_method_selection_query` (web_demo/help_functions.py:564-617) | override of the method | Checked against `permitted_algo_list`. `iv` is always refused. | AttributeError via DictAsObject. |
| 8 | `HTE_Filter.forward`, DML/DRL/IV (DML/hte_filter.py:35-48, DRL/hte_filter.py:36-49, IV/hte_filter.py:35-49) | which econml estimator | **None.** The name goes straight to `getattr(wrappers, name)` (DML/hte_program.py:17; DRL/hte_program.py:19; IV/hte_program.py:18). The context files offer `metalearners` (DML/context/hte_algo.txt:9, DRL/context/hte_algo.txt:9), which has **no wrapper class**, so choosing it raises AttributeError. | Missing `name` gives KeyError (inference.py:829, 900). Invalid JSON gives ValueError. |
| 9 | `HTE_Param_Selector.forward`, outcome model (DML/hte_params.py:78-82; DRL :181-186; IV :186-190) | nuisance regressor or classifier | The name is resolved by `getattr` on sklearn modules (DML/hte_params.py:46-54). DRL/IV also require the name in a fixed defaults table (DRL/hte_params.py:60-157). There is no check that a classifier was chosen for a discrete target. | `while not json:` retries **without limit** on an empty answer (DML/hte_params.py:79, 85, 91). A missing `name` gives KeyError. An unknown model gives ValueError (DML/hte_params.py:54; DRL/hte_params.py:157). |
| 10 | same, treatment model / instrument model | model_t / model_propensity / model_z_xw | same | same (DML/hte_params.py:85-88; IV/hte_params.py:200-203) |
| 11 | same, final model (DML, DRL) | model_final | same. LinearDML, SparseLinearDML, CausalForestDML and ForestDRL then drop it with `params.pop('model_final')` (DML/wrappers/estimator.py:71, 123, 175; DRL/wrappers/estimator.py:168). | same |
| 12 | `check_cycle` -> `LLM_remove_cycles` (postprocess/judge_functions.py:551-562), called from `attribute_anomalies` (inference.py:373) and `attribute_distributional_changes` (inference.py:560) | which cycle edge to delete | none | `response['nodes']` KeyError: crash C1 [L, F28a: crashed 9 of 9 times when entered live]. |
| 13-20 | `generate_analysis_econml` (analysis.py:3-48, 2 calls), `_matching` (:50-85, 2 calls), `_linear_regression` (:87-102), `_feature_importance` (:140-152), `_anormaly` (:154-170), `_anormaly_dist` (:172-187), `generate_conterfactual_estimation` (:189-209) | user-facing prose about the result | none. The text is appended to the chat and stored as the task result. | Prose only, so no JSON. |
| 21 | `parse_inf_discuss_query` (web_demo/help_functions.py:860-889) | follow-up answers, stored in `task_info['result']['discussion']` | none | AttributeError via DictAsObject |

[M] Prompt-content defect: every nuisance-model prompt renders `regressor.txt`. This file ends with a section titled "Domain Knowledge about Algorithm Selection" that recommends **causal discovery algorithms** (PC, GES, FCI, NOTEARS, DirectLiNGAM; DML/context/regressor.txt:151-188, and the same in the DRL, IV and MetaLearners copies). [I] The selector of the effect-estimation nuisance model is therefore shown advice that does not apply to its task.

## 5. Assumptions: checked or not

| Assumption | Code | Status |
|---|---|---|
| Graph used for adjustment | `convert_adj_mat` keeps every non-zero code as a directed edge j->i (help_functions.py:11-16). Its comment says "ignore all undirected edges", but `mat > 0` keeps them all. | [M] Comment and code disagree. [X] `evidence/mt_cycle_output.txt` case 1: an undirected edge (code 2) became a directed edge whose direction depends only on which cell the wrapper used. |
| Confounder set | Only common **direct parents** of T and Y (inference.py:239-251). Codes 1, 3 and 4 count as "influence". Code 3 (bidirected, which means a latent common cause) is treated as a causal parent (inference.py:242, 245). Codes 3/4 are looked up in one cell only, while code 2 is looked up in both cells (inference.py:243, 246). | [M] There is no back-door criterion, no ancestors beyond the parents, and no exclusion of descendants or mediators. [X] `evidence/mt_confounders_output.txt`: with Z<->T and Z<->Y, Z is returned as a confounder and becomes edges Z->T and Z->Y. |
| Post-treatment variables | User-added confounders (demo.py:994-1004) and LLM-chosen X (demo.py:1032) are not checked against the descendants of T. | [M] Not checked. |
| Positivity / overlap | No propensity trimming, overlap plot or common-support check. A search for overlap, positivity, trim or clip finds nothing in `causal_inference/`. PSM matches 1-NN with replacement and no caliper (inference.py:194-198). | [M] Not checked. |
| Balance | Density plots of at most 3 confounders (help_functions.py:110). No standardized mean differences and no pass/fail rule. | [M] Visual only. |
| IV validity | `contains_iv` (inference.py:959-1011) checks three things: a direct edge Z->T; no **direct** edge Z->Y (cutoff=1, inference.py:997); no parents of Z. Paths Z->M->Y via M != T pass the check. There is no first-stage strength test. The first qualifying node is returned. In the demo, `contains_iv` receives `key_node` as a **list** (demo.py:1044-1047), while `forward` passes a string (inference.py:1373). | [M] Partial structural check only. [I] The exclusion restriction is not tested. |
| Treatment coding | `prepare_treatment_column` (inference.py:755-815): categorical -> first two sorted values; numeric with 10 or fewer levels -> the two lowest; continuous -> 10th vs 90th percentile; CausalForestDML -> tertiles via `qcut` with T0/T1 set to tertile 0 vs 2 (inference.py:771-778), then **overridden** to values[0], values[1] = tertile 0 vs 1 (inference.py:858-866). | [M] The contrast changes silently between steps. |
| Scale of variables | On the CLI, `stat_info_collection` always z-scores **all** columns, category codes included, because `missingness` defaults to None (state.py:40; stat_info_functions.py:872-875, 469-470). In the web demo, the z-scoring runs when the data has missing values (missingness is set by web_demo/help_functions.py:448 -> stat_info_functions.py:108-112). | [M] When scaled, a 0/1 treatment no longer equals 0/1. PSM (`==1`/`==0`, inference.py:190-191), the balance plots (help_functions.py:121-153) and matched CATE (`==0`, inference.py:283) then select empty groups. [I] The likely result is a crash in `NearestNeighbors.fit` on an empty control set, or NaN CATE. Not executed. |
| No unobserved confounding (DML/DRL) | Assumed. `sensitivity_analysis` (causal_inference/inference.py:1297) is defined but never called (no other occurrence in the tree; checked 2026-10-10). | [M] Not checked. |

## 6. Failure modes and crash risks

| # | Where | Trigger | Effect |
|---|---|---|---|
| 1 | DML/hte_program.py:25-43 (DRL :30/37/44, IV :28/36/43) | Any exception inside `ate`/`att`/`hte` | [M] Bare `except:` returns (None, None, None) with only a print. |
| 2 | inference.py:875, 947, 1060 | HTE returned None (row 1) | [M] `hte.flatten()` AttributeError. If only ATE/ATT failed, "None" goes into the LLM prompt (analysis.py:19-20). |
| 3 | DML/hte_program.py:17 | LLM picks `metalearners` or any name that is not a class | [M] AttributeError |
| 4 | DML/hte_params.py:79-91 | LLM returns `{}` repeatedly | [M] Unbounded loop. [L] The ledger saw `{}` answers to a byte-identical request (F29). |
| 5 | DRL/wrappers/estimator.py:172-185 | ForestDRL | [M] `T_vals` is never passed, so the empty `value_counts().min()` makes the `>= 3` test false. The code always uses `KFold(2)` (non-stratified). An LLM-chosen regressor propensity model is silently replaced by RandomForestClassifier (:189-192). |
| 6 | DML/hte_params.py:46-52 | LLM picks `SVC` or `SGDClassifier` for a discrete treatment | [M] Built with defaults, i.e. no `probability=True`, hinge loss. [I] econml discrete-treatment nuisance models need `predict_proba`, so the fit is likely to fail. Not executed. |
| 7 | inference.py:378-380 via check_cycle | Revised graph has any 2-cycle, e.g. from an undirected or bidirected mark | [X] `check_cycle` returns the original matrix with the symmetric pair intact (`evidence/mt_cycle_output.txt` case 2: "is DAG after check_cycle: False"). The caller then raises "Cycle removal was unsuccessful". This is the inference-side twin of ledger F28b. |
| 8 | inference.py:373, 560 | Real directed cycle | [L] LLM cycle helper, crash C1 (`'nodes'`). |
| 9 | inference.py:208-219 | CEM fails | [M] A bare `except` drops the **last** confounder and retries, twice, with no record of which confounder was dropped. |
| 10 | inference.py:818-822 (also :889-893, :1017-1021) | No confounders | [M] Adds a zero column `W` to `self.data` **and to `global_state.user_data.processed_data`**. The added column persists into later tasks and the report data. |
| 11 | inference.py:1437-1439 | `linear_regression` | [M] NameError (`args`), then UnboundLocalError (`figs`). Unreachable today. |
| 12 | inference.py:1441-1446 | Anomaly task | [M] `anomaly_samples=self.data`, i.e. **every row** is treated as an anomaly. The parent check runs after the expensive fit. |
| 13 | inference.py:1453-1462 | Distributional change | [M] Splits rows into halves by order ("For demonstration"). Returns a 2-tuple to a 3-tuple caller. |
| 14 | report/inference_report_generation.py:295 vs query_prompt.txt:6 | Report for the anomaly task | [M] Checks `'Abnormality Attribution'`, while tasks are named `'Anormaly Attribution'`, so the section is never generated. `generate_attribution` would read the **Feature Importance** results anyway (inference_report_generation.py:182-183). |
| 15 | report/inference_report_generation.py:78-127 | Method `iv` | [M] Only cem/psm and dml/drl have a template. For IV, `analysis` is an empty string, so IV results never reach the report. |
| 16 | causal_inference/main.py:32, :39 | Using the module entry | [M] AttributeError, then TypeError (section 1). |
| 17 | demo.py:1104-1116 | Any exception in `analysis.forward` | [M] Caught. The task index and **all** task_info are reset (demo.py:1113-1114), so earlier completed tasks are lost from the report. |

## 7. LLM output written into results without a data check

- [M] ATE/ATT/HTE prose: the numbers, possibly None or NaN, go into the prompt (analysis.py:19-20). The LLM text is stored as the task result (demo.py:1117-1118). The report then passes it **through a second LLM rewrite**, `fix_latex_itemize_LLM` (report/inference_report_generation.py:72). The report template has **no numeric placeholder** for effects (report/context/inference/treatment_effect.tex: only variable names, method and `[ANALYSIS]`). [I] Every effect number a reader sees has passed through two unchecked LLM generations.
- [M] Counterfactual prose tells the LLM the method is "shifting the observed samples in the direction of the identified confounders" (analysis.py:205). The code shifts the treatment by a constant (inference.py:1233-1235). The prompt therefore misdescribes the method.
- [M] Heterogeneity variables chosen by the LLM become estimator inputs and report text (`[HTE_VAR]`, inference_report_generation.py:131), with no column check.
- [M] Method justification in the report is a fixed JSON text per method (report/context/inference/hte_method_reason.json, read at inference_report_generation.py:63-64), not derived from the data.
- [M] The discussion answers (web_demo/help_functions.py:879-881) are stored and summarised into the report (inference_report_generation.py:226-252).

## 8. Paper vs code for this module (detail in REP-04)

- [R] p.11-12 lists DML (Linear/Sparse/CausalForest), DRL (Linear/Sparse/Forest), DRIV family, PSM/CEM and DoWhy counterfactuals. [M] The classes exist. The selection rule differs (D14); the "counterfactual" is an interventional shift (D12).
- [R] p.12: "CEM is used when the number of discrete variables is greater". [M] demo.py:1052-1056 counts confounders only, and only when there are 1-5 of them.

## Findings

- F1 [M] Effect estimation runs only from the web demo. `main.py` never imports `causal_inference`, and `causal_inference/main.py` is broken (causal_inference/main.py:32, :39; inference.py:1329).
- F2 [M] `causal_inference.help_functions.LLM_parse_query` never passes `response_format`, so no schema is applied to inference-side LLM answers (help_functions.py:175-182).
- F3 [M] The LLM can choose `metalearners`, which has no wrapper class, giving an AttributeError crash (DML/context/hte_algo.txt:9; DML/hte_program.py:17).
- F4 [M] Nuisance-model selectors retry without limit on empty JSON (DML/hte_params.py:79, 85, 91; DRL/hte_params.py:182-196; IV/hte_params.py:186-201).
- F5 [M] Bare `except` turns estimator failures into None, which then crashes at `hte.flatten()` or reaches the LLM prompt as "None" (DML/hte_program.py:25-43; inference.py:875; analysis.py:19).
- F6 [M][X] The confounder set is the common direct parents of T and Y, and bidirected/o-> marks count as causal parents (inference.py:242-246; evidence/mt_confounders_output.txt).
- F7 [M][X] `convert_adj_mat` turns every non-zero mark into a directed edge, contradicting its own comment (causal_inference/help_functions.py:12-15; evidence/mt_cycle_output.txt).
- F8 [M] No positivity/overlap, balance threshold, IV-strength or sensitivity check is run. `sensitivity_analysis` is never called (inference.py:147-201, 959-1011, 1297).
- F9 [M] `contains_iv` checks exclusion only for a direct Z->Y edge (inference.py:997-1003).
- F10 [M] Matching code hard-codes treatment values 0/1 (inference.py:190-191, 283; help_functions.py:121-153), while preprocessing z-scores all columns (stat_info_functions.py:469-470; always on the CLI, in the demo when data has NaNs).
- F11 [M] CausalForestDML's contrast is set to tertile 0 vs 2, then overridden to 0 vs 1 (inference.py:777-778 vs 858-866).
- F12 [M] "Counterfactual Estimation" is an interventional shift (inference.py:1464-1467, 1231-1235). The real counterfactual method is never called (inference.py:1127). The LLM prompt misdescribes the method (analysis.py:205).
- F13 [M] Anomaly attribution treats all rows as anomalies (inference.py:1442). Its report section never renders, because of a task-name mismatch (inference_report_generation.py:295) and a copy-paste key (:182-183).
- F14 [M] IV results are silently dropped from the report (inference_report_generation.py:104-127). Effect numbers reach the report only through LLM prose, which is rewritten a second time (inference_report_generation.py:72).
- F15 [M] An empty confounder set injects a zero column `W` into the shared `processed_data` (inference.py:818-822).
- F16 [M][X] Inference-side `check_cycle` leaves symmetric pairs, so `attribute_anomalies` raises on any undirected or bidirected pair (inference.py:373-380; postprocess/judge_functions.py:564-594; evidence/mt_cycle_output.txt).
- F17 [M] ForestDRL always uses non-stratified 2-fold CV and silently overrides the LLM's propensity model (DRL/wrappers/estimator.py:172-192).
- F18 [M] Nuisance-model prompts carry unrelated causal-discovery selection advice (DML/context/regressor.txt:151-188).
- F19 [M] MetaLearners and Uplift are dead code (inference.py:44-46, 1370, 1393-1406).
- F20 [M] The demo binarizes a non-binary treatment at the median inside the shared `processed_data` (demo.py:943-946).
- F21 [M] One analysis exception wipes all task_info, including tasks already completed (demo.py:1106-1114).
