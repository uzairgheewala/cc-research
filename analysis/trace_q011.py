"""The gas/void case (scenario q011, solder-reflow voids): one true link, followed through both arms of the BLD-06 live
comparison, from the algorithm's graph to the delivered graph. Writes a JSON of every fact and the walkthrough built from it.

Tickets: BLD-06, DLV-04

    python analysis/trace_q011.py      (needs runs/ for the two runs below; numpy only)

Outputs (committed): analysis/results/run_trace/q011_gas_void.json, analysis/reports/run_trace/q011_gas_void.md.
Reads: each run's final JSON state, its bootstrap capture (artifacts/00018_bootstrap.pkl: 20 resampled graphs, typed
frequencies), the unmodified arm's bootstrap_recommend and kci_pruning captures, the refinement v2 record, and llm_calls.jsonl.
Matrix convention (Causal-Copilot): M[i, j] = 1 means j -> i; 6 marks o-o (connected, no direction)."""
import glob
import hashlib
import json
import pickle
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUNS = {"branch (refinement v2)": "20261021T214822Z_f06_q011_r01_dadc44",
        "main (unmodified)": "20261022T021911Z_m06_q011_r01_e82c08"}
MAP = ROOT / "datasets" / "suite_q1s2" / "MAPPING.json"
A_NAME, B_NAME = "residual_entrained_gas_mg", "true_void_fraction"
OUT_JSON = ROOT / "analysis" / "results" / "run_trace" / "q011_gas_void.json"
OUT_MD = ROOT / "analysis" / "reports" / "run_trace" / "q011_gas_void.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def arr(x):
    if isinstance(x, dict) and x.get("__ndarray__"):
        return np.array(x["data"])
    return None if x is None else np.asarray(x)


def mark(M, a, b):
    """The pair's mark in plain words, with a = gas and b = void."""
    x, y = int(M[a, b]), int(M[b, a])
    if x == 0 and y == 0:
        return "no link"
    if y == 1 and x == 0:
        return "gas -> void"
    if x == 1 and y == 0:
        return "void -> gas"
    if {x, y} - {0} == {6}:
        return "linked, direction open (o-o)"
    return "other mark (%d, %d)" % (x, y)


def freqs(T, a, b):
    T = {k: np.asarray(v, dtype=float) for k, v in T.items()}
    f = {"gas -> void": T["certain_edges"][b, a], "void -> gas": T["certain_edges"][a, b],
         "undirected": T["uncertain_edges"][a, b], "bidirected": T["bi_edges"][a, b],
         "gas o-> void": T["half_certain_edges"][b, a], "void o-> gas": T["half_certain_edges"][a, b],
         "gas o- void": T["half_uncertain_edges"][b, a], "void o- gas": T["half_uncertain_edges"][a, b],
         "o-o": T["none_edges"][a, b]}
    return {k: int(round(20 * float(v))) for k, v in f.items() if v}, int(round(20 * (1 - float(T["none_existence"][a, b]))))


def review(run, a, b):
    """The unmodified review's calls that list the pair among the relationships to determine, and the model's line for it."""
    hits = []
    for line in open(run / "llm_calls.jsonl", encoding="utf-8"):
        c = json.loads(line)
        if not str(c.get("stage", "")).startswith("07"):
            continue
        p = (c.get("args") or {}).get("prompt") or ""
        task = p.split("**Your Task**", 1)[-1]
        if "%s and %s" % (A_NAME, B_NAME) in task or "%s and %s" % (B_NAME, A_NAME) in task:
            ans = c.get("result") if isinstance(c.get("result"), str) else json.dumps(c.get("result"))
            mine = [s.strip() for s in ans.split(";") if A_NAME in s and B_NAME in s]
            hits.append({"seq": c.get("seq"), "caller": (c.get("caller") or [None])[0], "answer_for_pair": mine[0][:400] if mine else None})
    return hits


def main():
    spec = json.loads(MAP.read_text(encoding="utf-8"))["arms"]["q011"]
    cols = spec["column_labels"]
    a, b = cols.index(A_NAME), cols.index(B_NAME)
    ref = np.load(MAP.parent / spec["reference_by_data"])
    out = {"tickets": ["BLD-06", "DLV-04"], "scenario": "q011 (%s)" % spec["scenario_id"], "pair": {"gas": [a, A_NAME], "void": [b, B_NAME]},
           "truth": mark(ref, a, b), "sources": {}, "arms": {}}
    out["sources"][str(MAP.relative_to(ROOT))] = sha(MAP)
    for label, rid in RUNS.items():
        run = ROOT / "runs" / rid
        fin = sorted(glob.glob(str(run / "state" / "*99_final.json")))[-1]
        st = json.loads(Path(fin).read_text(encoding="utf-8"))
        res = st["results"]
        boot_p = run / "artifacts" / "00018_bootstrap.pkl"
        boot = pickle.load(open(boot_p, "rb"))["ret"][1]
        f, conn = freqs(boot, a, b)
        arm = {"run_id": rid, "algorithm_graph": mark(arr(res["converted_graph"]), a, b),
               "bootstrap_out_of_20": f, "connected_out_of_20": conn,
               "delivered_graph": mark(arr(res["revised_graph"]), a, b)}
        out["sources"]["runs/%s/state/%s" % (rid, Path(fin).name)] = sha(fin)
        out["sources"]["runs/%s/artifacts/00018_bootstrap.pkl" % rid] = sha(boot_p)
        if rid.split("_")[1] == "m06":
            rp = run / "artifacts" / "00039_bootstrap_recommend.pkl"
            rec = pickle.load(open(rp, "rb"))
            low = rec["ret"]["low_prob_edges"]["exist"]
            arm["bootstrap_recommend"] = {
                "rule": "at a31aa7c, postprocess/judge_functions.py:221-262 (bootstrap_recommend) puts every cell M[i, j] != 0 whose "
                        "directed (certain_edges) frequency is <= 0.1 in low_prob_edges.exist, and postprocess/judge.py:80-81 deletes "
                        "every cell in that list",
                "pair_cell_in_low_prob_exist": [int(x) for x in (b, a)] if (b, a) in [tuple(map(int, p)) for p in low] else None,
                "directed_frequency_read": float(np.asarray(rec["args_before"]["args"][1]["certain_edges"])[b, a])}
            kp = run / "artifacts" / "00087_kci_pruning.pkl"
            mid = rec["ret"].get("middle_prob_edges", {}).get("non-exist", [])
            arm["bootstrap_recommend"]["reverse_cell_in_middle_non_exist"] = [int(x) for x in (a, b)] if (a, b) in [tuple(map(int, p)) for p in mid] else None
            arm["model_review_of_pair"] = review(run, a, b)
            arm["graph_entering_kci_pruning"] = mark(np.asarray(pickle.load(open(kp, "rb"))["args_before"]["args"][1]), a, b)
            out["sources"]["runs/%s/artifacts/00039_bootstrap_recommend.pkl" % rid] = sha(rp)
            out["sources"]["runs/%s/artifacts/00087_kci_pruning.pkl" % rid] = sha(kp)
        else:
            v2 = res["llm_errors"]["refinement_v2"]
            arm["refinement_v2_source"] = next((s for s in v2["sources"] if s["pair"] == [a, b]), None)
            arm["refinement_v2_asked_model"] = any(r["pair"] == [a, b] for r in v2.get("names", []))
            arm["rule"] = ("postprocess/refinement_v2_dropin.py v2d on branch bld-06-refinement-v2 (55a490a): the pair keeps the "
                           "commonest typed bootstrap outcome; ties go to the algorithm's own type; only pairs left non-directed are asked")
        calls = [json.loads(l) for l in open(run / "llm_calls.jsonl", encoding="utf-8")]
        both = [c for c in calls if A_NAME in json.dumps(c.get("args")) and B_NAME in json.dumps(c.get("args"))]
        arm["model_calls"] = len(calls)
        arm["model_calls_naming_both"] = sorted({c.get("stage") for c in both})
        out["arms"][label] = arm
        out["sources"]["runs/%s/llm_calls.jsonl" % rid] = sha(run / "llm_calls.jsonl")
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(report(out), encoding="utf-8")
    print("q011: truth %s; branch %s; main %s" % (out["truth"], out["arms"]["branch (refinement v2)"]["delivered_graph"],
                                                 out["arms"]["main (unmodified)"]["delivered_graph"]))


def report(o):
    br, mn = o["arms"]["branch (refinement v2)"], o["arms"]["main (unmodified)"]
    fb = ", ".join("%s %d" % kv for kv in sorted(br["bootstrap_out_of_20"].items(), key=lambda kv: -kv[1]))
    fm = ", ".join("%s %d" % kv for kv in sorted(mn["bootstrap_out_of_20"].items(), key=lambda kv: -kv[1]))
    return "\n".join([
        "# The gas/void case: one true link through both arms (scenario q011)", "",
        "Tickets: BLD-06, DLV-04. Generated by `analysis/trace_q011.py` from `analysis/results/run_trace/q011_gas_void.json`;",
        "every fact below is in that file, with the sha256 of the run file it came from.", "",
        "The scenario is a solder-reflow process. The true link is **%s** (`%s` causes `%s`)." % (o["truth"], o["pair"]["gas"][1], o["pair"]["void"][1]),
        "", "| Step | Unmodified (main) | Refinement v2 (branch) |", "|---|---|---|",
        "| Algorithm's graph | %s | %s |" % (mn["algorithm_graph"], br["algorithm_graph"]),
        "| Resamples that link the pair | %d of 20 | %d of 20 |" % (mn["connected_out_of_20"], br["connected_out_of_20"]),
        "| Resamples by mark | %s | %s |" % (fm, fb),
        "| What the refinement does | deletes the link (bootstrap rule, below) | keeps the link, takes the commonest mark |",
        "| Delivered graph | %s | %s |" % (mn["delivered_graph"], br["delivered_graph"]),
        "| Model asked about this pair in refinement | %s | %s |" % (
            ("yes, in %d call(s) (seq %s), after the deletion" % (len(mn["model_review_of_pair"]), ", ".join(str(h["seq"]) for h in mn["model_review_of_pair"])))
            if mn["model_review_of_pair"] else "no",
            "yes" if br["refinement_v2_asked_model"] else "no (a direction was already set by the data, so the pair was not askable)"),
        "", "## Why the unmodified pipeline deletes it", "",
        "- %s." % mn["bootstrap_recommend"]["rule"],
        "- For this pair the directed frequency it reads is %.2f (gas -> void in 1 of 20 resamples), so the cell lands in that list,"
        " although the pair is linked in all %d resamples." % (mn["bootstrap_recommend"]["directed_frequency_read"], mn["connected_out_of_20"]),
        "- The graph entering the later KCI pruning already has: %s. The deletion happened at the bootstrap rule, not later." % mn["graph_entering_kci_pruning"],
        "- The reverse cell (void -> gas, %d of 20) is neither high nor low, so the rule sends it to the model as a missing link that "
        "might be added%s. The model's line for the pair: \"%s\" The link is not restored." % (
            mn["bootstrap_out_of_20"].get("void -> gas", 0),
            "" if mn["bootstrap_recommend"]["reverse_cell_in_middle_non_exist"] else " (not found in middle_prob_edges.non-exist; check)",
            (mn["model_review_of_pair"][0]["answer_for_pair"] if mn["model_review_of_pair"] else "none")),
        "", "## Why refinement v2 keeps it, and gets the direction wrong", "",
        "- %s." % br["rule"],
        "- Record for the pair: `%s`." % json.dumps(br["refinement_v2_source"]),
        "- The commonest mark is void -> gas (%d of 20): a plurality, not a majority. The marks that point the true way (gas -> void, gas o-> void) "
        "add up to %d." % (br["bootstrap_out_of_20"].get("void -> gas", 0), br["bootstrap_out_of_20"].get("gas -> void", 0) + br["bootstrap_out_of_20"].get("gas o-> void", 0)),
        "- Once the data set a direction, the pair is no longer askable, so the model's reading of the names never reaches it.",
        "", "## What it shows, and what it does not", "",
        "- It shows a specific defect in each arm: the unmodified rule treats a linked pair with no settled direction as a weak link; "
        "refinement v2 commits to a direction on a plurality of 8 in 20.",
        "- It is one pair in one run. It motivates the next rule (when to commit to a direction and when to leave it open) and becomes a "
        "regression check for that rule; it cannot set a threshold or show that the rule generalises.",
        ""])


if __name__ == "__main__":
    main()
