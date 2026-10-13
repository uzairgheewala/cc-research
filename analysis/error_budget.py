"""Error budget for CausalArena's public scenarios: how much directed-edge F1 is lost to what.

For each scenario (true DAG known) this computes, with no data at all:
  ceiling_obs   expected directed-edge F1 of a method that knows the true Markov equivalence class (CPDAG) and, as the
                scoreboard's rule prescribes for PC and GIES, orients every undecided edge at random: (C + U/2) / E,
                where E = edges, C = edges whose direction is fixed in the class, U = E - C
  ceiling_int   the same after adding the released single-variable intervention targets (interventional essential
                graph: every edge touching a target is fixed, then Meek's rules R1-R4 are closed)
and, from the stored plain-PC runs (pc_rows_v2.jsonl; published configuration, n = 1,000):
  skeleton precision / recall, PC's own orientation accuracy on the true adjacencies it found, and two hypothetical
  systems (PC's skeleton with perfect orientation; perfect skeleton is the ceiling above).

Gate B1: the CPDAG computed here equals cc_graph.cpdag_of (itself checked against causal-learn's dag2cpdag) on every scenario.
Gate B2: every scenario's obs+int file marks at least one target, and every marked target is a variable of the graph.

  python error_budget.py --root external/causalarena --pc analysis/results/causalarena_calibration/pc_rows_v2.jsonl --out analysis/results/error_budget
"""
import argparse
import glob
import json
import os
import statistics as st
import sys
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
import cc_graph as G  # noqa: E402


def essential(d, edges, fixed_pairs=()):
    """Compelled directions of the equivalence class of DAG `edges` (set of (cause, effect)), optionally with every
    edge in `fixed_pairs` (unordered) known. Returns the set of compelled (cause, effect)."""
    adj = {frozenset(e) for e in edges}
    par = {v: set() for v in range(d)}
    for c, e in edges:
        par[e].add(c)
    und = set(adj)                                   # unordered pairs not yet oriented
    ori = set()                                      # compelled (cause, effect)

    def orient(c, e):
        pr = frozenset((c, e))
        if pr in und:
            und.discard(pr)
            ori.add((c, e))
            return True
        return False

    for v in range(d):                               # unshielded colliders a -> v <- b
        ps = sorted(par[v])
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                if frozenset((ps[i], ps[j])) not in adj:
                    orient(ps[i], v)
                    orient(ps[j], v)
    for pr in fixed_pairs:
        a, b = tuple(pr)
        if (a, b) in edges:
            orient(a, b)
        elif (b, a) in edges:
            orient(b, a)
    nb = {v: set() for v in range(d)}
    for pr in adj:
        a, b = tuple(pr)
        nb[a].add(b)
        nb[b].add(a)
    changed = True
    while changed:                                   # Meek R1-R4
        changed = False
        into = {v: {c for c, e in ori if e == v} for v in range(d)}
        for pr in list(und):
            a, b = tuple(pr)
            for x, y in ((a, b), (b, a)):            # try to orient x -> y
                r1 = any(frozenset((c, y)) not in adj for c in into[x])
                r2 = any((x, m) in ori and (m, y) in ori for m in nb[x] & nb[y])
                cand = [m for m in nb[x] & nb[y] if frozenset((x, m)) in und and (m, y) in ori]
                r3 = any(frozenset((cand[i], cand[j])) not in adj for i in range(len(cand)) for j in range(i + 1, len(cand)))
                r4 = any(frozenset((x, k)) in und and (k, m) in ori and (m, y) in ori and frozenset((k, y)) not in adj
                         and frozenset((x, m)) in adj
                         for k in nb[x] for m in nb[x] & nb[y])
                if r1 or r2 or r3 or r4:
                    if orient(x, y):
                        changed = True
                    break
    assert ori <= set(edges), "a rule oriented an edge against the true DAG"
    return ori


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--pc", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = {"families": {}, "gates": {}}
    b1_bad, b2_bad = [], []
    for fam in ("semantic", "formula"):
        rows = []
        for f in sorted(glob.glob(os.path.join(a.root, "scm", fam, "data", "*obs_only*", "*rep000.npz"))):
            s = CA.load(f)
            d = len(s["node_ids"])
            E = CA.true_edges(s["g"])
            comp = essential(d, E)
            ref = G.cpdag_of({(c, e) for c, e in E}, d)          # repo convention: M[e, c] == 1 means c -> e
            ref_dir = {(int(j), int(i)) for i, j in np.argwhere(ref == 1) if ref[j, i] == 0}
            if ref_dir != comp:
                b1_bad.append(os.path.basename(f))
            fi = f.replace("obs_only", "obs_int")
            si = CA.load(fi) if os.path.exists(fi) else None
            targets = sorted(int(j) for j in np.where(si["intervened"].sum(0) > 0)[0]) if si is not None else []
            if not targets:
                b2_bad.append(os.path.basename(f))
            fixed = {frozenset(e) for e in E if e[0] in targets or e[1] in targets}
            comp_i = essential(d, E, fixed)
            has_parent = {e for _, e in E}
            rows.append({"scenario": s["meta"].get("scenario_id", os.path.basename(f)), "file": os.path.basename(f), "d": d,
                         "edges": len(E), "compelled_obs": len(comp), "compelled_int": len(comp_i),
                         "targets": len(targets), "targets_that_are_roots": sum(1 for t in targets if t not in has_parent),
                         "rows_per_target": (int(si["intervened"].sum()) / len(targets)) if targets else None,
                         "ceiling_obs": (len(comp) + (len(E) - len(comp)) / 2) / len(E),
                         "ceiling_int": (len(comp_i) + (len(E) - len(comp_i)) / 2) / len(E)})
        m = lambda k: round(st.mean(r[k] for r in rows), 3)
        res = {"scenarios": len(rows), "mean_edges": m("edges"), "share_compelled_obs": round(sum(r["compelled_obs"] for r in rows) / sum(r["edges"] for r in rows), 3),
               "share_compelled_int": round(sum(r["compelled_int"] for r in rows) / sum(r["edges"] for r in rows), 3),
               "ceiling_obs_mean": m("ceiling_obs"), "ceiling_obs_min": round(min(r["ceiling_obs"] for r in rows), 3),
               "ceiling_int_mean": m("ceiling_int"), "ceiling_int_min": round(min(r["ceiling_int"] for r in rows), 3),
               "scenarios_fully_identified_obs": sum(1 for r in rows if r["compelled_obs"] == r["edges"]),
               "scenarios_fully_identified_int": sum(1 for r in rows if r["compelled_int"] == r["edges"]),
               "targets_mean": m("targets"), "targets_that_are_roots": sum(r["targets_that_are_roots"] for r in rows),
               "targets_total": sum(r["targets"] for r in rows), "rows": rows}
        out["families"][fam] = res
    if a.pc and os.path.exists(a.pc):
        truth = {}
        for f in glob.glob(os.path.join(a.root, "scm", "semantic", "data", "semantic_obs_only", "*.npz")):
            truth[os.path.basename(f)] = CA.true_edges(np.load(f)["g"])
        per = {}
        for line in open(a.pc, encoding="utf-8"):
            r = json.loads(line)
            if r["alpha"] != 0.05:
                continue
            E = truth[r["file"]]
            tadj = {frozenset(e) for e in E}
            dire = {tuple(e) for e in r["directed_edges"]}
            und = {frozenset(e) for e in r["undirected_pairs"]}
            padj = {frozenset(e) for e in dire} | und
            tp = len(padj & tadj)
            P, R = tp / len(padj) if padj else 0.0, tp / len(tadj)
            right = sum(1 for e in dire if e in E)
            wrong = sum(1 for e in dire if (e[1], e[0]) in E)
            undec = len(und & tadj)
            per.setdefault(r["scenario"], []).append({
                "skel_precision": P, "skel_recall": R, "skel_f1": 2 * P * R / (P + R) if P + R else 0.0,
                "found_true_adjacencies": tp, "directed_right": right, "directed_wrong": wrong, "left_undirected": undec,
                "f1_official": r["random"]["f1"]})
        mm = lambda k: round(st.mean(st.mean(x[k] for x in v) for v in per.values()), 3)
        tot = {k: sum(x[k] for v in per.values() for x in v) for k in ("found_true_adjacencies", "directed_right", "directed_wrong", "left_undirected")}
        out["pc_semantic_n1000"] = {
            "scenarios": len(per), "skeleton_precision": mm("skel_precision"), "skeleton_recall": mm("skel_recall"),
            "pc_skeleton_with_perfect_orientation_f1": mm("skel_f1"), "pc_as_scored_f1": mm("f1_official"),
            "of_true_adjacencies_found": {"directed_right": round(tot["directed_right"] / tot["found_true_adjacencies"], 3),
                                          "directed_wrong": round(tot["directed_wrong"] / tot["found_true_adjacencies"], 3),
                                          "left_undirected": round(tot["left_undirected"] / tot["found_true_adjacencies"], 3)},
            "accuracy_of_committed_directions": round(tot["directed_right"] / (tot["directed_right"] + tot["directed_wrong"]), 3)}
    out["gates"] = {"B1_cpdag_equals_cc_graph": not b1_bad, "B2_targets_found_in_every_obs_int_file": not b2_bad}
    out["b1_bad"], out["b2_bad"] = b1_bad[:10], b2_bad[:10]
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "error_budget.json"), "w", encoding="utf-8"), indent=1)
    for fam, res in out["families"].items():
        print(fam, json.dumps({k: v for k, v in res.items() if k != "rows"}))
    print("pc", json.dumps(out.get("pc_semantic_n1000")))
    print("gates", out["gates"], out["b1_bad"], out["b2_bad"])
    sys.exit(0 if all(out["gates"].values()) else 1)


if __name__ == "__main__":
    main()
