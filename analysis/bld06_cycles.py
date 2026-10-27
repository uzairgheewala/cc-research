"""BLD-06 live series: how each arm handled directed cycles (an ad-hoc check, not part of the pre-registration).

Tickets: BLD-06, EXT-03

    python analysis/bld06_cycles.py   -> analysis/results/fork/bld06_cycles.json

Per arm (refinement v2 branch, unmodified main): runs that crashed and where (meta.json failure), the cycle step's
KeyError count, completed final graphs that contain a directed cycle, and whether the cycle step ran at all
(llm_calls.jsonl has a call from postprocess/judge_functions.py LLM_remove_cycles). Matrix convention: M[i, j] = 1 and
M[j, i] = 0 means j -> i."""
import glob
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SERIES = {"branch": "plans/results/fork_bld06_live.capped.json", "main": "plans/results/fork_bld06_live_main.capped.json"}
OUT = ROOT / "analysis" / "results" / "fork" / "bld06_cycles.json"


def arr(x):
    return np.array(x["data"]) if isinstance(x, dict) and x.get("__ndarray__") else np.asarray(x)


def has_cycle(M):
    p = M.shape[0]
    ch = {}
    for i in range(p):
        for j in range(p):
            if M[i, j] == 1 and M[j, i] == 0:
                ch.setdefault(j, []).append(i)
    colour = {}

    def visit(u):
        colour[u] = 1
        for v in ch.get(u, ()):
            if colour.get(v) == 1 or (colour.get(v) is None and visit(v)):
                return True
        colour[u] = 2
        return False
    return any(colour.get(u) is None and visit(u) for u in range(p))


def main():
    out = {"tickets": ["BLD-06", "EXT-03"], "note": "ad hoc (27 Oct), not pre-registered", "arms": {}}
    for arm, path in SERIES.items():
        runs = json.loads((ROOT / path).read_text(encoding="utf-8"))["runs"].values()
        a = {"runs": 0, "completed": 0, "crashed": 0, "crash_sites": {}, "cycle_step_keyerrors": 0,
             "runs_entering_cycle_step": 0, "final_graphs_with_directed_cycle": 0}
        for r in runs:
            rid = r["run_id"]
            run = ROOT / "runs" / rid
            a["runs"] += 1
            calls = [json.loads(l) for l in open(run / "llm_calls.jsonl", encoding="utf-8")]
            if any("LLM_remove_cycles" in ((c.get("caller") or [""])[0] or "") for c in calls):
                a["runs_entering_cycle_step"] += 1
            fin = sorted(glob.glob(str(run / "state" / "*99_final.json")))
            if fin:
                a["completed"] += 1
                M = arr(json.loads(Path(fin[-1]).read_text(encoding="utf-8"))["results"]["revised_graph"])
                a["final_graphs_with_directed_cycle"] += bool(has_cycle(M))
            else:
                a["crashed"] += 1
                f = (json.loads((run / "meta.json").read_text(encoding="utf-8")).get("failure") or {})
                site = "%s %s" % (f.get("type"), f.get("repo_frame"))
                a["crash_sites"][site] = a["crash_sites"].get(site, 0) + 1
                if f.get("type") == "KeyError" and "LLM_remove_cycles" in (f.get("repo_frame") or ""):
                    a["cycle_step_keyerrors"] += 1
        out["arms"][arm] = a
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out["arms"], indent=1))


if __name__ == "__main__":
    main()
