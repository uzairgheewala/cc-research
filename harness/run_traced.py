"""Run Causal-Copilot's CLI pipeline (main.py) once, unmodified, while recording everything.

Usage (inside the container, repo mounted at /app, this folder's parent at /research):
  python /research/harness/run_traced.py --dataset data/dataset/Linear_Gaussian --data-mode simulated
Options: --query "...", --label NAME, --stub-llm (dry run, no API calls), --allow-drift
"""
import argparse
import datetime
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import traceback
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from cc_common import (BASELINE_COMMIT, REPO, RESEARCH, Scrubber, dump_json, key_status,  # noqa: E402
                       to_jsonable, verify_tree)
from cc_trace import Recorder, Tee  # noqa: E402

DEFAULT_QUERY = "Do causal discovery on this dataset"   # main.py's own default
EDGE_CODES = {1: "directed", 2: "undirected", 3: "bidirected", 4: "o->", 5: "o-", 6: "o-o", 7: "associated"}


def parse():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True, help="path relative to the repo root (CSV file or dataset directory)")
    p.add_argument("--data-mode", choices=["real", "simulated"], required=True)
    p.add_argument("--query", default=None)
    p.add_argument("--label", default="run")
    p.add_argument("--stub-llm", action="store_true")
    p.add_argument("--allow-drift", action="store_true")
    p.add_argument("--run-id", default=None)
    return p.parse_args()


def edge_counts(mat):
    import numpy as np
    m = np.asarray(mat)
    out = {}
    for code, name in EDGE_CODES.items():
        n = int((m == code).sum())
        if n:
            out[name] = n
    out["nonzero_cells"] = int((m != 0).sum())
    return out


def dataset_identity(path):
    """sha256 of the dataset file, or of every regular file directly inside the dataset directory.
    Recorded so that two runs can be shown to have read the same bytes."""
    import hashlib
    p = Path(path)
    files = [p] if p.is_file() else sorted(f for f in p.iterdir() if f.is_file()) if p.is_dir() else []
    out = {}
    for f in files:
        h = hashlib.sha256()
        with open(f, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        out[f.name] = {"sha256": h.hexdigest(), "bytes": f.stat().st_size}
    return {"path": str(path), "kind": "file" if p.is_file() else "directory" if p.is_dir() else "missing", "files": out}


def repo_frame(tb):
    """Deepest traceback frame that lives in the repo (file:line:function)."""
    best = None
    prefix = str(REPO) + os.sep
    for fr in traceback.extract_tb(tb):
        fn = os.path.realpath(fr.filename)
        if fn.startswith(prefix):
            best = "%s:%d:%s" % (fn[len(prefix):].replace(os.sep, "/"), fr.lineno, fr.name)
    return best


def main():
    a = parse()
    t_start = time.time()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ds_name = Path(a.dataset).name.replace(".csv", "")
    run_id = a.run_id or "%s_%s_%s%s_%s" % (stamp, a.label, ds_name, "_STUB" if a.stub_llm else "", uuid.uuid4().hex[:6])
    run_dir = RESEARCH / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    scrub = Scrubber()
    log_fh = open(run_dir / "console.log", "w", encoding="utf-8")
    sys.stdout = Tee(sys.stdout, log_fh, scrub)
    sys.stderr = Tee(sys.stderr, log_fh, scrub)
    print("[harness] run_id = %s" % run_id)
    print("[harness] run_dir = %s" % run_dir)

    meta = {"run_id": run_id, "label": a.label, "stub_llm": a.stub_llm, "started_utc": stamp,
            "dataset": a.dataset, "data_mode": a.data_mode, "query": a.query or DEFAULT_QUERY,
            "query_is_repo_default": a.query is None, "baseline_commit": BASELINE_COMMIT,
            "python": sys.version, "platform": platform.platform(), "repo": str(REPO)}
    summary = {"run_id": run_id, "status": "NOT_STARTED", "must_show": {}}

    def finish(code):
        meta["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        meta["wall_time_s"] = round(time.time() - t_start, 1)
        dump_json(run_dir / "meta.json", meta, scrub)
        dump_json(run_dir / "summary.json", summary, scrub)
        write_summary_text(run_dir, meta, summary)
        print("\n" + (run_dir / "SUMMARY.txt").read_text(encoding="utf-8"))
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(code)

    # ---- 1. code identity --------------------------------------------------
    if not (REPO / "main.py").is_file():
        summary["status"] = "ABORTED: repo not found at %s (set CC_REPO)" % REPO
        finish(2)
    print("[harness] checking code identity against baseline %s ..." % BASELINE_COMMIT)
    ident = verify_tree()
    meta["tree_identity"] = ident
    summary["must_show"]["1_code_identity"] = "OK" if ident["ok"] else "DRIFT"
    if not ident["ok"] and not a.allow_drift:
        summary["status"] = "ABORTED: repo differs from baseline (missing=%d changed=%d). Use --allow-drift to override." % (
            len(ident["missing"]), len(ident["changed"]))
        finish(2)
    pre_extra = set(ident["extra_unexpected"])

    # ---- 2. environment ----------------------------------------------------
    os.chdir(REPO)
    sys.path.insert(0, str(REPO))
    meta["dataset_identity"] = dataset_identity(a.dataset)
    env_before = {k: (k in os.environ) for k in ("OPENAI_API_KEY", "LLM_PROVIDER", "LLM_MODEL")}
    try:
        from dotenv import load_dotenv
        load_dotenv(REPO / ".env")           # same precedence as main.py: real env vars win over .env
    except Exception as e:
        print("[harness] could not load .env: %r" % (e,))
    if a.stub_llm:
        if key_status() != "set":
            os.environ["OPENAI_API_KEY"] = "stub-key-not-real"
        os.environ.setdefault("LLM_PROVIDER", "openai")
    scrub.refresh()
    meta["llm"] = {"provider": os.environ.get("LLM_PROVIDER"), "model": os.environ.get("LLM_MODEL"),
                   "openai_key": "stub" if a.stub_llm else key_status(),
                   "set_in_process_env_before_dotenv": env_before}
    if not a.stub_llm and (os.environ.get("LLM_PROVIDER", "openai").lower() == "openai") and key_status() != "set":
        summary["status"] = "ABORTED: OPENAI_API_KEY is %s. Put the key on the OPENAI_API_KEY line of Causal-Copilot/.env" % key_status()
        finish(2)
    try:
        meta["pip_freeze"] = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True,
                                            text=True, timeout=120).stdout.splitlines()
    except Exception as e:
        meta["pip_freeze"] = ["unavailable: %r" % (e,)]
    try:
        meta["container_images"] = json.loads((RESEARCH / "manifests" / "image_ids.json").read_text(encoding="utf-8-sig"))
    except Exception:
        meta["container_images"] = None
    dump_json(run_dir / "meta.json", meta, scrub)

    # ---- 3. hooks ----------------------------------------------------------
    rec = Recorder(run_dir, scrub)
    if a.stub_llm:
        import stub_llm
        stub_llm.install()
    rec.install_llm_hooks()
    rec.auto_answer_input("no")
    print("[harness] importing the pipeline (this can take a minute) ...")
    import main as cc_main
    import causal_discovery.filter as m_filter
    import causal_discovery.hyperparameter_selector as m_hp
    import causal_discovery.program as m_program
    import causal_discovery.rerank as m_rerank
    import postprocess.judge as m_judge
    import postprocess.judge_functions as jf
    import preprocess.eda_generation as m_eda
    import report.report_generation as m_report
    import user.discuss as m_discuss

    rec.wrap_stage(cc_main, "global_state_initialization", "01_init_query_parse")
    rec.wrap_stage(cc_main, "load_data", "02_load_data")
    rec.wrap_stage(cc_main, "stat_info_collection", "04a_statistics")
    rec.wrap_stage(cc_main, "knowledge_info", "04b_knowledge")
    rec.wrap_stage(m_eda.EDA, "generate_eda", "05_eda")
    rec.wrap_stage(m_filter.Filter, "forward", "06a_filter")
    rec.wrap_stage(m_rerank.Reranker, "forward", "06b_rerank")
    rec.wrap_stage(m_hp.HyperparameterSelector, "forward", "06c_hyperparameters")
    rec.wrap_stage(m_program.Programming, "forward", "07a_algorithm")
    rec.wrap_stage(m_judge.Judge, "forward", "07b_refinement")
    rec.wrap_stage(m_report.Report_generation, "graph_effect_prompts", "08a_report_graph_text", snapshot=False)
    rec.wrap_stage(m_report.Report_generation, "generation", "08b_report", snapshot=False)
    rec.wrap_stage(m_report.Report_generation, "save_report", "08c_report_compile", snapshot=False)
    rec.wrap_stage(m_discuss.Discussion, "__init__", "09_discussion_init", snapshot=False)

    for name in ("bootstrap_iteration", "bootstrap", "bootstrap_recommend", "llm_evaluation_new",
                 "call_llm_new", "kci_pruning", "check_cycle", "LLM_remove_cycles"):
        rec.wrap_capture(jf, name)
    rec.wrap_capture(m_judge.Judge, "quality_judge", drop_first=True)
    rec.wrap_capture(m_judge.Judge, "evaluation", drop_first=True)
    rec.record_rng_states()

    # ---- 4. run main.py's own main() ---------------------------------------
    argv = ["main.py", "--data-file", a.dataset, "--data_mode", a.data_mode]
    if a.query is not None:
        argv += ["--initial_query", a.query]
    meta["main_argv"] = argv
    sys.argv = argv
    status, failure, state = "COMPLETED", None, None
    t_pipe = time.time()
    try:
        args = cc_main.parse_args()
        meta["main_args"] = to_jsonable(vars(args))
        _report, state = cc_main.main(args)
    except SystemExit as e:
        status = "FAILED"
        failure = {"type": "SystemExit", "message": str(e.code), "repo_frame": None, "traceback": traceback.format_exc()}
    except BaseException as e:      # noqa: BLE001  (we want everything, including KeyboardInterrupt)
        status = "FAILED"
        failure = {"type": type(e).__name__, "message": str(e)[:4000], "repo_frame": repo_frame(e.__traceback__),
                   "stage": rec.stage_times[-1]["stage"] if rec.stage_times else None,
                   "traceback": traceback.format_exc()}
        traceback.print_exc()
    pipeline_s = round(time.time() - t_pipe, 1)
    state = state if state is not None else rec.last_state
    if state is not None:
        try:
            rec.snapshot("99_final" if status == "COMPLETED" else "99_at_failure", state)
        except Exception as e:
            print("[harness] final snapshot failed: %r" % (e,))

    # ---- 5. collect outputs + build the must-show summary -------------------
    out_dirs = []
    if state is not None:
        for attr in ("output_report_dir", "output_graph_dir"):
            d = getattr(state.user_data, attr, None)
            if d and (REPO / d).is_dir():
                out_dirs.append(d)
    for d in out_dirs:
        try:
            shutil.copytree(REPO / d, run_dir / "pipeline_output" / Path(d).name, dirs_exist_ok=True)
        except Exception as e:
            print("[harness] could not copy %s: %r" % (d, e))
    post = verify_tree(use_cache=True)
    meta["tree_identity_after"] = {k: post[k] for k in ("ok", "missing", "changed", "extra_allowed")}
    meta["new_unexpected_files_in_repo"] = sorted(set(post["extra_unexpected"]) - pre_extra)
    meta["stage_times"] = rec.stage_times
    meta["failure"] = failure

    ms = summary["must_show"]
    summary["status"] = status
    summary["pipeline_wall_time_s"] = pipeline_s
    ms["2_pipeline"] = "COMPLETED" if status == "COMPLETED" else "FAILED at %s (%s: %s)" % (
        failure.get("repo_frame"), failure.get("type"), (failure.get("message") or "")[:300])
    # LLM calls
    calls, usage, models, fps, by_stage, errors = 0, {"prompt_tokens": 0, "completion_tokens": 0}, set(), set(), {}, 0
    if rec.llm_path.is_file():
        for line in rec.llm_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            calls += 1
            by_stage[r.get("stage")] = by_stage.get(r.get("stage"), 0) + 1
            errors += 1 if r.get("error") else 0
            for api in r.get("api") or []:
                resp = api.get("response") or {}
                u = resp.get("usage") or {}
                usage["prompt_tokens"] += u.get("prompt_tokens") or 0
                usage["completion_tokens"] += u.get("completion_tokens") or 0
                if resp.get("model"):
                    models.add(resp["model"])
                if resp.get("system_fingerprint"):
                    fps.add(resp["system_fingerprint"])
    ms["3_llm_calls"] = {"count": calls, "errors": errors, "by_stage": by_stage, "tokens": usage,
                         "served_models": sorted(models), "system_fingerprints": sorted(fps)}
    ms["4_state_snapshots"] = [s["label"] for s in rec.snapshots]
    sel = {}
    if state is not None:
        sel = {"algorithm": getattr(state.algorithm, "selected_algorithm", None),
               "hyperparameters": to_jsonable(getattr(state.algorithm, "algorithm_arguments", None))}
    ms["5_selection"] = sel
    graphs = {}
    if state is not None:
        import numpy as np
        g0, g1 = getattr(state.results, "converted_graph", None), getattr(state.results, "revised_graph", None)
        if g0 is not None:
            graphs["initial"] = edge_counts(g0)
        if g1 is not None:
            graphs["revised"] = edge_counts(g1)
        if g0 is not None and g1 is not None and np.asarray(g0).shape == np.asarray(g1).shape:
            graphs["cells_changed_by_refinement"] = int((np.asarray(g0) != np.asarray(g1)).sum())
        graphs["ground_truth_loaded"] = getattr(state.user_data, "ground_truth", None) is not None
        graphs["metrics_initial"] = to_jsonable(getattr(state.results, "metrics", None))
        graphs["metrics_revised"] = to_jsonable(getattr(state.results, "revised_metrics", None))
    ms["6_graphs"] = graphs
    ms["7_refinement_captures"] = dict(rec.captures)
    ms["8_stage_times_s"] = {s["stage"]: s["duration_s"] for s in rec.stage_times}
    pdfs = [str(p.relative_to(run_dir)) for p in (run_dir / "pipeline_output").rglob("report.pdf")] \
        if (run_dir / "pipeline_output").is_dir() else []
    ms["9_report_pdf"] = pdfs or "not produced"
    ms["10_repo_after_run"] = {"baseline_files_intact": post["ok"],
                               "new_unexpected_files": meta["new_unexpected_files_in_repo"][:50]}
    summary["auto_answered_prompts"] = rec.auto_inputs
    finish(0 if status == "COMPLETED" else 1)


def write_summary_text(run_dir, meta, summary):
    ms = summary.get("must_show", {})
    L = ["=" * 78, "CAUSAL-COPILOT TRACED RUN SUMMARY%s" % ("   *** STUB LLM: plumbing test only ***" if meta.get("stub_llm") else ""),
         "=" * 78,
         "run_id   : %s" % meta.get("run_id"), "dataset  : %s (%s)" % (meta.get("dataset"), meta.get("data_mode")),
         "query    : %s" % meta.get("query"), "model    : %s" % (meta.get("llm") or {}).get("model"),
         "status   : %s" % summary.get("status"), "wall time: %s s" % meta.get("wall_time_s"), "-" * 78]
    for key in sorted(ms, key=lambda s: int(s.split("_")[0])):
        v = ms[key]
        if isinstance(v, (dict, list)):
            L.append("%s:" % key)
            for line in json.dumps(v, indent=2, default=repr).splitlines():
                L.append("    " + line)
        else:
            L.append("%s: %s" % (key, v))
    L += ["-" * 78, "Full record in: %s" % run_dir, "=" * 78]
    (run_dir / "SUMMARY.txt").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
