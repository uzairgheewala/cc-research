"""Inside Causal-Copilot (C4): export one recorded scenario, run under three name arms, for the replay page.

    python site/copilot/export_replay.py RUN_REAL RUN_NEUTRAL RUN_SWAPPED

runs/ stays outside git; this writes the small, allowlisted file site/copilot/replay.json (committed): per arm, the state
at each recorded stage (only the fields listed in FIELDS), the model calls with the head of each prompt and answer, and the
edges after the algorithm and after refinement. Nothing else from the run is copied (no environment, no pip freeze, no
paths outside the run's own output folders)."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HEAD = 700
STAGE_TITLES = {"01_init_query_parse": "Reading the question", "02_load_data": "Loading the data", "04a_statistics": "Statistics",
                "04b_knowledge": "Domain knowledge", "05_eda": "Exploratory analysis", "06a_filter": "Shortlisting algorithms",
                "06b_rerank": "Ranking them", "06c_hyperparameters": "Setting hyperparameters", "07a_algorithm": "Running the algorithm",
                "07b_refinement": "Refining the graph", "99_final": "Final state", "08a_report_graph_text": "Report text"}


def edges(d):
    if not isinstance(d, dict):
        return {}
    return {k: [list(e) for e in v] for k, v in d.items() if isinstance(v, list)}


def arm(run_dir, label):
    run = ROOT / run_dir
    meta = json.load(open(run / "meta.json", encoding="utf-8"))
    summ = json.load(open(run / "summary.json", encoding="utf-8"))
    stages = []
    for f in sorted((run / "state").glob("*.json")):
        key = f.stem.split("_", 1)[1]
        s = json.load(open(f, encoding="utf-8"))
        st, al, ud = s.get("statistics", {}), s.get("algorithm", {}), s.get("user_data", {})
        stages.append({
            "stage": key, "title": STAGE_TITLES.get(key.replace("__FAILED", ""), key),
            "columns": ((ud.get("processed_data") or {}).get("columns") or (ud.get("raw_data") or {}).get("columns") or []) if key.startswith("02") else None,
            "statistics": {k: st.get(k) for k in ("data_type", "linearity", "gaussian_error", "missingness", "sample_size",
                                                   "feature_number", "time_series", "boot_num", "alpha")} if key >= "04" else None,
            "knowledge_head": (" ".join(map(str, ud.get("knowledge_docs") or []))[:HEAD] if key.startswith("04b") else None),
            "candidates": sorted((al.get("algorithm_candidates") or {}).keys()) if key >= "06a" else None,
            "selected": al.get("selected_algorithm") if key >= "06b" else None,
            "selected_reason": ((al.get("algorithm_optimum") or {}).get("reason") or "")[:HEAD] if key >= "06b" else None,
            "arguments": al.get("algorithm_arguments") if key >= "06c" else None,
        })
    final = json.load(open(sorted((run / "state").glob("*final*.json"))[-1], encoding="utf-8"))
    res = final.get("results", {})
    calls = []
    for line in open(run / "llm_calls.jsonl", encoding="utf-8"):
        c = json.loads(line)
        args = c.get("args") or {}
        prompt = args.get("prompt") if isinstance(args, dict) else str(args)
        system = args.get("system_prompt") if isinstance(args, dict) else None
        calls.append({"seq": c.get("seq"), "stage": c.get("stage"), "caller": (c.get("caller") or [None])[0],
                      "system_head": (system or "")[:HEAD], "prompt_head": (prompt or "")[:HEAD],
                      "answer_head": json.dumps(c.get("result"), ensure_ascii=False)[:HEAD] if not isinstance(c.get("result"), str) else c["result"][:HEAD],
                      "duration_s": c.get("duration_s"), "error": c.get("error")})
    direct = (res.get("llm_errors") or {}).get("direct_record") or {}
    forbid = (res.get("llm_errors") or {}).get("forbid_record") or {}
    return {"label": label, "run_id": meta["run_id"], "status": summ.get("status"), "model": (meta.get("llm") or {}).get("model", "gpt-4o"),
            "dataset_sha256": (meta.get("dataset_identity") or {}).get("sha256"), "wall_time_s": meta.get("wall_time_s"),
            "failure": meta.get("failure"), "stages": stages, "llm_calls": calls,
            "edges_after_algorithm": edges(res.get("raw_edges")), "edges_after_refinement": edges(res.get("revised_edges")),
            "llm_set_direction": [{"pair": v[0], "why": v[1][:300]} for v in direct.values()][:60],
            "llm_forbade": [{"pair": v[0], "why": v[1][:300]} for v in forbid.values()][:60]}


def main():
    runs = sys.argv[1:4]
    arms = [arm(r, l) for r, l in zip(runs, ("real names", "neutral names", "names moved to other columns"))]
    out = {"about": "One CausalArena scenario (BND-08 suite, q02) run by unmodified Causal-Copilot a31aa7c with gpt-4o under three "
                    "name arms, columns shuffled. Exported by site/copilot/export_replay.py from runs/ (outside git).",
           "tickets": ["TEAM-13", "AUD-17"], "scenario": "q02", "arms": arms}
    text = json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True, default=str) + "\n"
    (ROOT / "site" / "copilot" / "replay.json").write_text(text, encoding="utf-8")
    print("replay.json: %d bytes, sha256 %s" % (len(text.encode()), hashlib.sha256(text.encode()).hexdigest()[:12]))


if __name__ == "__main__":
    main()
