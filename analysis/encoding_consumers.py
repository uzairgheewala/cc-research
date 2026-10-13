"""Pass 5 micro-tests: how does each downstream consumer treat each edge code?

Calls the repo's own functions on tiny crafted graphs (3 variables, one marked pair) and records
what happens. No LLM is contacted: the cycle step's LLM helper is replaced by a recorder.

  python encoding_consumers.py OUT_DIR        (needs the repo importable: $CC_REPO or ~/cc)
"""
import contextlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

repo = os.environ.get("CC_REPO", os.path.expanduser("~/cc"))
os.chdir(repo)
sys.path[:0] = [repo, os.path.join(repo, "externals", "causal-learn"), str(Path(__file__).resolve().parent)]
import cc_graph as G  # noqa: E402
from lineage import step_bootstrap  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    import postprocess.judge_functions as jf
    from postprocess.visualization import convert_to_edges

out_dir = Path(sys.argv[1])
out_dir.mkdir(parents=True, exist_ok=True)
cols = pd.Index(["A", "B", "C"])
rng = np.random.default_rng(0)
indep = pd.DataFrame(rng.normal(size=(300, 3)), columns=cols)      # A, B, C mutually independent
PROB_ORDER = ["certain_edges", "uncertain_edges", "bi_edges", "half_certain_edges", "half_uncertain_edges", "none_edges", "none_existence"]
rows = []
for code in (1, 2, 3, 4, 5, 6, 7):
    for cell, (i, j) in (("upper [A,B]", (0, 1)), ("lower [B,A]", (1, 0))):
        M = np.zeros((3, 3))
        M[i, j] = code
        rec = {"code": code, "name": G.CODE_NAMES[code], "cell": cell}
        # (a) convert_to_edges
        ed = convert_to_edges("X", cols, M)
        rec["convert_to_edges"] = {k: v for k, v in ed.items() if v and k != "all_edges"}
        # (b) the sentence the LLM would read
        try:
            _d, text = jf.edges_to_relationship(indep, ed, None)
            rec["sentence_for_llm"] = " ".join(text.split())
        except Exception as e:
            rec["sentence_for_llm"] = "ERROR %r" % (e,)
        # (c) bootstrap bookkeeping when every resample returns exactly this graph
        probs = jf.bootstrap_probability(np.stack([M] * 20), "X")
        hit = {PROB_ORDER[k]: [(int(a), int(b)) for a, b in np.argwhere(probs[k] == 1.0) if a != b] for k in range(7)}
        rec["bootstrap_layer_with_frequency_1"] = {k: v for k, v in hit.items() if v and k != "none_existence"}
        boot = {PROB_ORDER[k]: probs[k] for k in range(7)}
        # (d) bootstrap step decision for an edge found in 100% of resamples
        buckets = jf.bootstrap_recommend(M, boot)
        S1, added, deleted = step_bootstrap(M, buckets)
        rec["survives_bootstrap_step_when_found_in_all_resamples"] = bool(G.is_adjacent(S1, 0, 1))
        # (e) KCI step: A and B are independent in the data, so the edge is removed iff it is examined
        with contextlib.redirect_stdout(io.StringIO()):
            removed = jf.kci_pruning(indep, M.copy())
        rec["kci_step_examines_it"] = bool(len(removed) > 0)
        rows.append(rec)

# (f) cycle step on unoriented triangles
calls = []
jf.LLM_remove_cycles = lambda args, message: (calls.append(message), message.split(" -> ")[:2])[1]
cyc = []
for label, cells in (("three undirected edges, all stored in the upper triangle", [(0, 1), (1, 2), (0, 2)]),
                     ("three undirected edges, stored A-B upper, B-C upper, A-C lower", [(0, 1), (1, 2), (2, 0)])):
    M = np.zeros((3, 3))
    for (i, j) in cells:
        M[i, j] = 2
    calls.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        out = jf.check_cycle(None, indep, M.copy())
    cyc.append({"graph": label, "llm_cycle_helper_called": len(calls), "edges_before": int((M != 0).sum()), "edges_after": int((out != 0).sum()),
                "prompt": calls[0] if calls else None})

json.dump({"per_code": rows, "cycle_step": cyc}, open(out_dir / "encoding_consumers.json", "w"), indent=1, default=str)
L = ["# How downstream steps treat each edge code (pass 5 micro-tests)", "",
     "Each row is one crafted 3-variable graph with a single mark between A and B, pushed through the repo's own functions.", "",
     "| Code | Meaning | Stored in | Listed by `convert_to_edges` as | Counted by the bootstrap tally as | Survives the bootstrap step if found in 100% of resamples | KCI step looks at it |",
     "|---|---|---|---|---|---|---|"]
for r in rows:
    ce = "; ".join("%s %s" % (k.replace("_edges", ""), v) for k, v in r["convert_to_edges"].items()) or "nothing"
    bl = "; ".join("%s at %s" % (k.replace("_edges", ""), v) for k, v in r["bootstrap_layer_with_frequency_1"].items()) or "no layer (not counted)"
    L.append("| %d | %s | %s | %s | %s | %s | %s |" % (r["code"], r["name"], r["cell"], ce, bl,
                                                    "yes" if r["survives_bootstrap_step_when_found_in_all_resamples"] else "**no**",
                                                    "yes" if r["kci_step_examines_it"] else "**no**"))
L += ["", "## Sentence shown to the LLM for each code", ""]
seen = set()
for r in rows:
    key = (r["code"], r["sentence_for_llm"])
    if key in seen:
        continue
    seen.add(key)
    L.append("- code %d (%s), %s: \"%s\"" % (r["code"], r["name"], r["cell"], r["sentence_for_llm"]))
L += ["", "## Cycle step on a triangle of undirected edges", ""]
for c in cyc:
    L.append("- %s: LLM cycle helper called %d time(s); edges %d -> %d.%s" % (c["graph"], c["llm_cycle_helper_called"], c["edges_before"], c["edges_after"],
                                                                         (" Prompt: \"%s\"" % c["prompt"]) if c["prompt"] else ""))
(out_dir / "encoding_consumers.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
