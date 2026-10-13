"""Build the LLM dependency inventory: static scan + hand classification + reconciliation with recorded runs.

  python llm_inventory_build.py SCAN_JSON RUNS_DIR OUT_DIR

Gates (exit 1 if any fails):
  G1  every textual `chat_completion(` / `completions.create(` occurrence is matched by an AST call site
  G2  every logical LLM point has a classification (no UNCLASSIFIED rows)
  G3  every caller recorded in any run maps to a statically found call site (same file and line)
  G4  for every observed site, recorded json_response and temperature agree with the static scan
"""
import csv
import glob
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

scan = json.load(open(sys.argv[1]))
runs_dir, out_dir = sys.argv[2], Path(sys.argv[3])
out_dir.mkdir(parents=True, exist_ok=True)

GENERIC = {"LLM_parse_query"}     # generic wrappers: their callers are the logical points, not the wrapper body
# (path, role, kind, effect on causal output, validation of the answer, where the answer is kept, basis)
#   basis: "read" = function read line by line; "prompt" = classified from prompt text and names only
R = {}


def rule(key, *vals):
    R[key] = vals


CLI, WEB, BOTH, INF, REP, TST = "CLI+web discovery", "web demo only", "CLI+web discovery", "inference (web demo)", "report", "benchmark/test"
rule(("global_setting/Initialize_state.py", "global_state_initialization"), BOTH, "extract user intent into 9 fields", "decision",
     "indirect: can fix linearity/Gaussianity (skipping the statistical tests), the algorithm, alpha, time-series flag",
     "none on values; missing key raises KeyError", "only the resulting fields; prompt and answer not kept (logging.query_conversation unused)", "read")
rule(("preprocess/dataset.py", "knowledge_info"), BOTH, "elicit domain knowledge as prose", "descriptive, reused as input",
     "indirect: pasted into the filter, rerank, hyperparameter and edge-review prompts", "none", "user_data.knowledge_docs / knowledge_docs_for_user", "read")
rule(("preprocess/stat_info_functions.py", "llm_select_dropped_features"), WEB, "choose which 30-50%-missing variables to keep", "decision",
     "indirect: changes the variable set", "none", "user_data.llm_drop_features", "read")
rule(("causal_discovery/filter.py", "Filter.forward"), BOTH, "shortlist 2 algorithms", "decision", "indirect: decides which algorithms can run",
     "none here; unknown names dropped later (rerank.py:58)", "algorithm.algorithm_candidates + logging.select_conversation", "read")
rule(("causal_discovery/rerank.py", "Reranker.select_algorithm"), BOTH, "pick the algorithm (LLM also does the 0.7/0.3 score arithmetic)", "decision",
     "indirect: decides the algorithm", "none; name must be a wrapper attribute or execution fails", "algorithm.algorithm_optimum + logging.select_conversation", "read")
rule(("causal_discovery/hyperparameter_selector.py", "HyperparameterSelector.select_hyperparameters"), BOTH, "choose hyperparameters", "decision",
     "indirect: test type, alpha, depth etc.", "keys filtered to primary parameters (drops background_knowledge); values not checked against allowed list",
     "algorithm.algorithm_arguments_json + logging.argument_conversation", "read")
rule(("causal_discovery/runtime_estimators/runtime_estimator.py", "RuntimeEstimator._query_llm"), BOTH, "guess a runtime model for an algorithm without one", "decision",
     "indirect: runtime text shown to the rerank prompt", "none", "written to a JSON file in the repo", "prompt")
rule(("postprocess/judge_functions.py", "call_llm_new"), BOTH, "edit the graph: A/B/C/D per variable pair", "decision",
     "direct: adds, orients and deletes edges", "none: any A/B/C applied; unparseable pairs silently skipped; D not recorded; unbounded retry on format error",
     "results.llm_errors (A/B/C with explanation)", "read")
rule(("postprocess/judge_functions.py", "LLM_remove_cycles"), BOTH, "choose which edge of a cycle to delete", "decision", "direct: deletes an edge",
     "none", "not kept", "read")
rule(("postprocess/judge_functions.py", "get_json"), "dead code (no caller)", "-", "-", "-", "-", "-", "read")
rule(("postprocess/judge.py", "Judge.graph_refutation"), WEB, "summarise the falsification test", "descriptive", "none", "none", "results.refutation_analysis", "read")
rule(("user/discuss.py", "Discussion.__init__"), CLI, "strip LaTeX from the report", "descriptive", "none", "none", "not kept", "read")
rule(("user/discuss.py", "Discussion.interaction"), CLI, "answer follow-up questions (history is not sent)", "descriptive", "none", "none", "logging.final_discuss", "read")
rule(("data/simulator/simulation.py", "SimulationManager.generate_simulation_config"), "online simulation mode", "invent a simulation config", "decision",
     "defines the synthetic data", "none", "config", "prompt")
for f in ("causal_discovery/tests/selection_test.py", "causal_discovery/tests/user_simulation.py"):
    rule((f, None), TST, "benchmark helper", "-", "none in a pipeline run", "-", "-", "prompt")
for d in ("DML", "DRL", "IV", "MetaLearners", "Uplift"):
    rule(("causal_inference/%s/" % d, "filter"), INF, "choose the effect estimator", "decision", "effect estimate: estimator choice", "not examined", "inference.* fields", "prompt")
    rule(("causal_inference/%s/" % d, "params"), INF, "choose nuisance models / estimator parameters", "decision", "effect estimate: model choice", "not examined", "inference.* fields", "prompt")
for fn in ("get_title", "intro_prompt", "background_prompt", "graph_effect_prompts", "confidence_analysis_prompts", "comparision_prompt",
           "abstract_prompt", "keyword_prompt", "conclusion_prompt"):
    rule(("report/report_generation.py", "Report_generation." + fn), REP, "write report prose", "descriptive",
         "none on the graph; shapes the claims a reader sees", "none", "report text", "read" if fn in ("get_title", "intro_prompt", "background_prompt") else "prompt")
for fn in ("latex_convert", "latex_bug_checking"):
    rule(("report/report_generation.py", "Report_generation." + fn), REP, "reformat / repair LaTeX", "format", "none", "none", "report text", "read")
# wrapper (LLM_parse_query) callers
W = {
    "parse_drop_high_miss_query": (WEB, "parse a yes/no", "interpretation", "indirect: drop high-missing variables", "pydantic class, lenient", "statistics.drop_important_var"),
    "meaningful_feature_query": (WEB, "decide whether variable names are meaningful", "decision", "indirect: gates whether LLM edge review is offered", "none", "user_data.meaningful_feature"),
    "heterogeneity_query": (WEB, "extract the domain-index column", "interpretation", "indirect: heterogeneity handling", "pydantic class, lenient", "statistics.domain_index"),
    "parse_preliminary_feedback": (WEB, "parse a filled-in template", "interpretation", "indirect: variables, CPDAG acceptance, missing marker", "pydantic class, lenient", "several user_data/statistics fields"),
    "parse_reupload_query": (WEB, "parse a yes/no", "interpretation", "none", "pydantic class, lenient", "stage only"),
    "parse_var_selection_query": (WEB, "extract variable names", "interpretation", "indirect: variable set; also user-added confounders", "pydantic class, lenient", "selected features / confounders"),
    "LLM_var_selection": (WEB, "pick 10 variables when there are too many", "decision", "display only (visual_selected_features)", "none", "visual_selected_features"),
    "parse_ts_query": (WEB, "parse time-series settings", "interpretation", "indirect: time-series path and lag", "pydantic class, lenient", "statistics.time_series/time_lag"),
    "parse_sparsity_query": (WEB, "extract variables to drop", "interpretation", "indirect: variable set", "pydantic class, lenient", "user_data.user_drop_features"),
    "first_stage_sparsity_check": (WEB, "extract the missing-value marker", "interpretation", "indirect: imputation", "pydantic class, lenient", "user_data.nan_indicator"),
    "parse_algo_query": (WEB, "extract a user-chosen algorithm", "interpretation", "indirect: algorithm", "LLM told the allowed list; not re-checked", "algorithm.selected_algorithm"),
    "parse_algo_selection": (WEB, "extract a user-chosen algorithm", "interpretation", "indirect: algorithm", "LLM told the allowed list; not re-checked", "algorithm.selected_algorithm"),
    "parse_method_selection_query": (INF, "extract a user-chosen estimation method", "interpretation", "effect estimate: method", "LLM told the allowed list", "inference task info"),
    "prepare_hyperparameter_text": (WEB, "write a hint for the user", "descriptive", "none", "none", "chat only"),
    "parse_hyperparameter_query": (WEB, "parse AND validate user hyperparameters", "interpretation + validation by LLM", "indirect: hyperparameters", "the LLM itself is the validator", "algorithm.algorithm_arguments"),
    "parse_query": (WEB, "parse user edge edits (add / forbid / orient)", "interpretation", "direct: user edits applied to the graph", "pydantic class, lenient; names looked up afterwards", "not kept (only the edited graph)"),
    "parse_report_algo_query": (WEB, "extract which runs to report", "interpretation", "none", "pydantic class, lenient", "results.report_selected_index"),
    "parse_inference_query": (INF, "split a question into inference tasks", "decision", "effect estimate: which task, which target", "pydantic class, lenient", "inference.task_info"),
    "parse_inf_discuss_query": (INF, "answer a follow-up", "descriptive", "none", "none", "chat"),
    "parse_treatment": (INF, "identify the treatment variable", "decision", "effect estimate: treatment", "none", "inference.task_info"),
    "parse_shift_value": (INF, "extract an intervention value", "interpretation", "effect estimate: intervention size", "pydantic class, lenient", "inference.task_info"),
    "process_message": (WEB, "parse a yes/no or free-form feedback", "interpretation", "indirect: control flow (e.g. whether LLM pruning runs)", "pydantic class, lenient", "stage only"),
    "LLM_select_confounders": ("dead code (only call is commented out)", "pick confounders by name", "-", "-", "-", "-"),
    "LLM_select_hte_var": (INF, "pick effect-modifier variables", "decision", "effect estimate: heterogeneity variables", "none", "inference.task_info X_col"),
    "main": (INF, "split a question into inference tasks", "decision", "effect estimate: which task", "pydantic class, lenient", "local"),
    "fix_latex_itemize_LLM": (REP, "repair LaTeX", "format", "none", "none", "report text"),
    "Report_generation.background_prompt": (REP, "list 'possible causal relations' from background knowledge", "descriptive",
                                            "none on the graph; prints LLM-asserted relations in the report", "pydantic class, lenient", "report text"),
}
for k in ("generate_analysis_econml", "generate_analysis_matching", "generate_analysis_linear_regression", "generate_analysis_feature_importance",
          "generate_analysis_anormaly", "generate_analysis_anormaly_dist", "generate_conterfactual_estimation"):
    W[k] = (INF, "explain an estimate in prose", "descriptive", "none; shapes the claims a reader sees", "none", "chat / report")
for k in ("generate_proposal", "generate_feature_importance", "generate_attribution", "generate_counterfactual_estimation", "generate_discussion", "generate_next_step"):
    W["Inference_Report_generation." + k] = (REP, "write inference-report prose", "descriptive", "none on estimates", "none", "report text")


def contract(site):
    if site.get("response_format"):
        return "Pydantic class (parse falls back to an untyped object)"
    if site.get("json_response") is True:
        return "JSON mode, no schema"
    return "free text"


def classify_api(s):
    f, fn = s["file"], s["function"]
    if (f, fn) in R:
        return R[(f, fn)]
    if (f, None) in R:
        return R[(f, None)]
    for (pf, tag), v in R.items():
        if tag in ("filter", "params") and f.startswith(pf) and (("filter" in f) == (tag == "filter")):
            return v
    return None


rows = []
api = sorted(scan["api_sites"], key=lambda s: (s["file"], s["line"]))
for s in api:
    if s["file"].startswith("llm/"):
        continue
    if s["function"].split(".")[-1] in GENERIC:
        continue
    c = classify_api(s)
    rows.append({"layer": "direct call", "file": s["file"], "line": s["line"], "function": s["function"],
                 "output_contract": "line format `(X, Y): LETTER: text`, split on ':'" if s["function"] == "call_llm_new" else contract(s),
                 "temperature": s["temperature"], "cls": c})
generic_defs = {}
for s in api:
    if s["function"].split(".")[-1] in GENERIC:
        generic_defs.setdefault(s["file"], []).append(s)
for w in sorted(scan["wrapper_sites"], key=lambda w: (w["file"], w["line"])):
    if w["calls"] not in GENERIC:
        continue
    key = w["function"].split(".")[-1] if w["function"].split(".")[-1] in W else w["function"]
    v = W.get(key) or W.get(w["function"].split(".")[-1])
    c = None
    if v:
        c = (v[0], v[1], v[2], v[3], v[4], v[5], "read" if v[0] in (WEB, "dead code (only call is commented out)") or "Report" in key else "prompt")
    rows.append({"layer": "via LLM_parse_query", "file": w["file"], "line": w["line"], "function": w["function"],
                 "output_contract": "Pydantic class or free text (per call)", "temperature": "default 0.0", "cls": c})

# ---- dynamic reconciliation
api_index = {(s["file"], s["line"]): s for s in api}
observed = defaultdict(lambda: {"calls": 0, "runs": set(), "prompt_tokens": 0, "completion_tokens": 0, "stub_calls": 0})
g3_unmapped, g4_mismatch, n_records = [], [], 0
for run in sorted(glob.glob(os.path.join(runs_dir, "*"))):
    p = os.path.join(run, "llm_calls.jsonl")
    if not os.path.isfile(p):
        continue
    stub = "_STUB" in os.path.basename(run)
    for line in open(p, encoding="utf-8"):
        r = json.loads(line)
        if r.get("level") != "client":
            continue
        n_records += 1
        caller = (r.get("caller") or [None])[0]
        if not caller:
            g3_unmapped.append((os.path.basename(run), r.get("seq"), "no caller"))
            continue
        f, ln, _fn = caller.rsplit(":", 2)
        key = (f, int(ln))
        if key not in api_index:
            g3_unmapped.append((os.path.basename(run), r.get("seq"), caller))
            continue
        s = api_index[key]
        o = observed[key]
        o["calls"] += 1
        o["runs"].add(os.path.basename(run))
        if stub:
            o["stub_calls"] += 1
        for a in r.get("api") or []:
            u = (a.get("response") or {}).get("usage") or {}
            o["prompt_tokens"] += u.get("prompt_tokens") or 0
            o["completion_tokens"] += u.get("completion_tokens") or 0
        args = r.get("args") or {}
        static_json = bool(s["json_response"]) or bool(s.get("response_format"))
        rec_json = bool(args.get("json_response")) or bool(r.get("response_format"))
        static_temp = 0.0 if str(s["temperature"]) in ("default 0.0", "0.0") else None
        if static_json != rec_json or (static_temp is not None and args.get("temperature") != static_temp):
            g4_mismatch.append((caller, s["json_response"], args.get("json_response"), s["temperature"], args.get("temperature")))

gates = {
    "G1_ast_matches_text": len(scan["text_hits_not_matched_by_ast"]) == 0 and not scan["unparseable"],
    "G2_all_points_classified": all(r["cls"] for r in rows),
    "G3_every_recorded_caller_is_a_known_site": len(g3_unmapped) == 0 and n_records > 0,
    "G4_recorded_flags_match_static": len(g4_mismatch) == 0,
}

# ---- outputs
fields = ["layer", "file", "line", "function", "path", "role", "kind", "effect_on_causal_output", "output_contract", "answer_validation",
          "answer_kept_in", "temperature", "basis", "observed_calls_real", "observed_calls_stub", "prompt_tokens_real", "completion_tokens_real"]
with open(out_dir / "llm_inventory.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    for r in rows:
        c = r["cls"] or ("UNCLASSIFIED",) * 7
        o = observed.get((r["file"], r["line"]))
        w.writerow({"layer": r["layer"], "file": r["file"], "line": r["line"], "function": r["function"], "path": c[0], "role": c[1], "kind": c[2],
                    "effect_on_causal_output": c[3], "output_contract": r["output_contract"], "answer_validation": c[4], "answer_kept_in": c[5],
                    "temperature": r["temperature"], "basis": c[6],
                    "observed_calls_real": (o["calls"] - o["stub_calls"]) if o else 0, "observed_calls_stub": o["stub_calls"] if o else 0,
                    "prompt_tokens_real": o["prompt_tokens"] if o else 0, "completion_tokens_real": o["completion_tokens"] if o else 0})

cls_rows = [r for r in rows if r["cls"]]
by_path = Counter(r["cls"][0] for r in cls_rows)
by_kind = Counter(r["cls"][2] for r in cls_rows)
direct_graph = [r for r in cls_rows if r["cls"][3].startswith("direct")]
unvalidated_decisions = [r for r in cls_rows if r["cls"][2].startswith("decision") and (r["cls"][4].startswith("none") or "not examined" in r["cls"][4])]
L = ["# LLM dependency inventory (pass 3)", "",
     "Static scan of the tree at baseline a31aa7c, classified by hand, reconciled with %d recorded LLM calls from the runs in `runs/`." % n_records, "",
     "## Gates", ""] + ["- %s: **%s**" % (k, "PASS" if v else "FAIL") for k, v in gates.items()]
L += ["", "## Counts", "",
      "- Call sites that issue a request (AST): %d, of which %d are outside `llm/`. Textual occurrences: %d." % (
          len(api), len([s for s in api if not s["file"].startswith("llm/")]), scan["text_hits"]),
      "- Logical LLM points (direct sites that are not generic wrappers, plus each caller of `LLM_parse_query`): **%d**." % len(rows),
      "- By path: %s." % "; ".join("%s %d" % kv for kv in by_path.most_common()),
      "- By kind: %s." % "; ".join("%s %d" % kv for kv in by_kind.most_common()),
      "- Points that edit the causal graph directly: %d (%s)." % (len(direct_graph), ", ".join("`%s:%d`" % (r["file"], r["line"]) for r in direct_graph)),
      "- Decision points whose answer has no check before use (or was not examined): %d of %d decisions." % (
          len(unvalidated_decisions), sum(1 for r in cls_rows if r["cls"][2].startswith("decision"))),
      "- Classification basis: %s." % "; ".join("%s %d" % kv for kv in Counter(r["cls"][6] for r in cls_rows).most_common()), ""]
L += ["## Sites observed in recorded runs", "", "| Site | Role | Real calls | Stub calls | Prompt tokens (real) | Completion tokens (real) |", "|---|---|---|---|---|---|"]
for key, o in sorted(observed.items()):
    r = next((x for x in rows if (x["file"], x["line"]) == key), None)
    L.append("| `%s:%d` | %s | %d | %d | %d | %d |" % (key[0], key[1], r["cls"][1] if r and r["cls"] else "?", o["calls"] - o["stub_calls"], o["stub_calls"],
                                                    o["prompt_tokens"], o["completion_tokens"]))
never = [r for r in cls_rows if r["layer"] == "direct call" and r["cls"][0] in (CLI, BOTH, REP) and (r["file"], r["line"]) not in observed]
L += ["", "## CLI-path and report sites never exercised by the recorded runs", ""] + ["- `%s:%d` %s (%s)" % (r["file"], r["line"], r["function"], r["cls"][1]) for r in never]
L += ["", "## Decision points on the discovery path", "", "| Site | Decides | Effect on the causal output | Check on the answer | Kept in |", "|---|---|---|---|---|"]
for r in cls_rows:
    if r["cls"][0] in (BOTH, WEB, CLI) and (r["cls"][2].startswith("decision") or r["cls"][3].startswith("direct") or "interpretation +" in r["cls"][2]):
        L.append("| `%s:%d` | %s | %s | %s | %s |" % (r["file"], r["line"], r["cls"][1], r["cls"][3], r["cls"][4], r["cls"][5]))
L += ["", "The full table (all %d points, every field) is `llm_inventory.csv`." % len(rows), ""]
if g3_unmapped:
    L += ["## G3 failures", ""] + ["- %s" % (x,) for x in g3_unmapped[:40]]
if g4_mismatch:
    L += ["## G4 failures", ""] + ["- %s" % (x,) for x in g4_mismatch[:40]]
(out_dir / "llm_inventory.md").write_text("\n".join(L), encoding="utf-8")
print("\n".join(L[:60]))
print("UNCLASSIFIED:", [(r["file"], r["line"], r["function"]) for r in rows if not r["cls"]])
sys.exit(0 if all(gates.values()) else 1)
