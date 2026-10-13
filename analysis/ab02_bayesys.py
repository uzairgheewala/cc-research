"""AB-02 (AUD-34): the second scoreboard, Bayesys (Constantinou et al. 2021, IJAR 131:151-188; CC BY-SA 4.0).

  python analysis/ab02_bayesys.py --root external/bayesys --causal-learn PATH --out analysis/results/ab02 [--budget-s N]

Data: the six networks' Experiment1 ("N", no noise) training files at 0.1k, 1k and 10k rows, as released (discrete,
string-valued; columns coded to integers in order of first appearance). Truth: each network's GroundTruth.csv (a DAG).
Measured per network:
  layout   share of true edges running earlier column -> later column; Kendall tau of column index vs depth (P3)
  methods  PC (causal-learn 0.1.4.8, stable, G-squared test, alpha 0.05) with the default collider rule (uc_rule 0,
           priority 2) and maxP (uc_rule 1, priority 3); FCI (G-squared, alpha 0.05; skeleton and arrows scored as PAG
           marks: tail-arrowhead = committed, everything else undecided); GES with the BDeu score on networks with at
           most 40 variables (causal-learn local_score_BDeu)
  arms     released order, and 5 shuffled orders (seeds 1-5); every arm scores against the same truth
  scores   directed F1 under the expectation rule (undecided pairs at random, per-run seed) and under the "lower"
           rule (earlier column -> later column); S, c, q as in rescore_controls.py; Bayesys-style F1 (an arc with
           the wrong orientation or left undirected counts 0.5 TP; Constantinou et al. 2021, section 3.3, as reported
           second-hand in AU2 / AB-15) for comparison with the published tables once they are available
Resumable: one JSON line per (network, size, method, arm) in <out>/bayesys_runs.jsonl. No model calls.
Tickets: AUD-34, BEN-07
"""
import argparse, contextlib, csv, glob, io, json, os, signal, statistics as st, sys, time, zlib
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

HERE = Path(__file__).resolve().parent
NETS = ("ASIA", "SPORTS", "PROPERTY", "ALARM", "FORMED", "PATHFINDER")
SIZES = ("0.1k", "1k", "10k")
SEEDS = (1, 2, 3, 4, 5)


def load(root, net, size):
    f = glob.glob(os.path.join(root, net, "Experiment1", "*", "trainingData_%s_N_%s.csv" % (net, size)))[0]
    rows = list(csv.reader(open(f, encoding="utf-8")))
    cols, body = rows[0], rows[1:]
    X = np.zeros((len(body), len(cols)), dtype=int)
    for j in range(len(cols)):
        codes = {}
        for i, r in enumerate(body):
            X[i, j] = codes.setdefault(r[j], len(codes))
    gt = list(csv.DictReader(open(os.path.join(root, net, "Experiment1", "GroundTruth.csv"), encoding="utf-8")))
    pos = {c: i for i, c in enumerate(cols)}
    T = {(pos[r["from"]], pos[r["to"]]) for r in gt}
    return X, cols, T, f


def depth(d, T):
    par = {v: [a for a, b in T if b == v] for v in range(d)}
    memo = {}

    def dep(v):
        if v not in memo:
            memo[v] = 0 if not par[v] else 1 + max(dep(p) for p in par[v])
        return memo[v]
    return [dep(v) for v in range(d)]


def marks_to_sets(M):
    d = M.shape[0]
    D, U = set(), set()
    for i in range(d):
        for j in range(i + 1, d):
            a, b = int(M[i, j]), int(M[j, i])
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                D.add((i, j))
            elif a == 1 and b == -1:
                D.add((j, i))
            else:
                U.add((i, j))
    return D, U


def score(D, U, T, d, seed, perm_pos=None):
    """D, U, T in original indices. perm_pos maps original index -> column position the method saw (for 'lower')."""
    rng = np.random.default_rng(seed)
    tadj = {frozenset(e) for e in T}
    padj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    tp = len(tadj & padj)
    P = tp / len(padj) if padj else 0.0
    R = tp / len(tadj) if tadj else 0.0
    S = 2 * P * R / (P + R) if P + R else 0.0
    right = sum(1 for e in D if e in T)
    wrong = sum(1 for e in D if (e[1], e[0]) in T)
    out = {"S": S, "c": (right + wrong) / tp if tp else 0.0, "q": right / (right + wrong) if right + wrong else None}

    def f1(pred):
        t = len(pred & T)
        p = t / len(pred) if pred else 0.0
        r = t / len(T) if T else 0.0
        return 2 * p * r / (p + r) if p + r else 0.0
    rand = set(D) | {(a, b) if rng.integers(2) == 0 else (b, a) for a, b in sorted(U)}
    pp = perm_pos or {i: i for i in range(d)}
    low = set(D) | {(a, b) if pp[a] < pp[b] else (b, a) for a, b in U}
    out["F1_random"], out["F1_lower"] = f1(rand), f1(low)
    # Bayesys-style: correct arc 1, reversed or undirected on a true adjacency 0.5
    half = right + 0.5 * (wrong + sum(1 for u in U if frozenset(u) in tadj))
    npred = len(D) + len(U)
    bp = half / npred if npred else 0.0
    br = half / len(T) if T else 0.0
    out["F1_bayesys_half_credit"] = 2 * bp * br / (bp + br) if bp + br else 0.0
    return out


def run_method(method, X):
    with contextlib.redirect_stdout(io.StringIO()):
        if method in ("pc", "pc_maxp"):
            from causallearn.search.ConstraintBased.PC import pc
            r, p = (0, 2) if method == "pc" else (1, 3)
            return marks_to_sets(pc(X, 0.05, "gsq", stable=True, uc_rule=r, uc_priority=p, show_progress=False).G.graph)
        if method == "fci":
            from causallearn.search.ConstraintBased.FCI import fci
            G, _ = fci(X, independence_test_method="gsq", alpha=0.05, show_progress=False, verbose=False)
            return marks_to_sets(G.graph)
        if method == "ges":
            from causallearn.search.ScoreBased.GES import ges
            return marks_to_sets(ges(X, score_func="local_score_BDeu")["G"].graph)
    raise ValueError(method)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent / "external" / "bayesys"))
    ap.add_argument("--causal-learn", required=True)
    ap.add_argument("--out", default=str(HERE / "results" / "ab02"))
    ap.add_argument("--budget-s", type=float, default=0)
    ap.add_argument("--run-timeout-s", type=int, default=900)
    ap.add_argument("--nets", nargs="+", default=list(NETS))
    ap.add_argument("--sizes", nargs="+", default=list(SIZES))
    ap.add_argument("--methods", nargs="+", default=None, help="restrict to these methods (pc pc_maxp fci ges)")
    ap.add_argument("--arms", nargs="+", default=None, help="restrict to these arms (released shuffled_1 .. shuffled_5)")
    ap.add_argument("--summarise-only", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.causal_learn).resolve()))
    os.makedirs(a.out, exist_ok=True)
    runs_f = Path(a.out) / "bayesys_runs.jsonl"
    done = set()
    if runs_f.exists():
        for l in open(runs_f):
            r = json.loads(l)
            done.add((r["net"], r["size"], r["method"], r["arm"]))
    t0 = time.time()

    def _alarm(s, f):
        raise TimeoutError("run exceeded %d s" % a.run_timeout_s)
    signal.signal(signal.SIGALRM, _alarm)
    layout = {}
    for net in a.nets:
        X0, cols, T, src = load(a.root, net, "1k")
        d = len(cols)
        dep = depth(d, T)
        tau = kendalltau(range(d), dep)
        layout[net] = {"variables": d, "edges": len(T), "share_edges_earlier_to_later": round(sum(x < y for x, y in T) / len(T), 4),
                       "kendall_tau_index_vs_depth": round(float(tau.statistic), 4), "p": float(tau.pvalue)}
        if a.summarise_only:
            continue
        methods = ["pc", "pc_maxp", "fci"] + (["ges"] if d <= 40 else [])
        if a.methods:
            methods = [m for m in methods if m in a.methods]
        for size in a.sizes:
            X, cols, T, src = load(a.root, net, size)
            for method in methods:
                for arm in ["released"] + ["shuffled_%d" % s for s in SEEDS]:
                    if a.arms and arm not in a.arms:
                        continue
                    key = (net, size, method, arm)
                    if key in done:
                        continue
                    if a.budget_s and time.time() - t0 > a.budget_s:
                        print("budget reached")
                        return summarise(a, runs_f, layout)
                    perm = list(range(d)) if arm == "released" else [int(x) for x in np.random.default_rng(int(arm.split("_")[1]) * 1000 + zlib.crc32(net.encode())).permutation(d)]
                    pos = {v: i for i, v in enumerate(perm)}
                    rec = {"net": net, "size": size, "method": method, "arm": arm, "perm_seed": arm, "rows": int(X.shape[0])}
                    t = time.time()
                    try:
                        signal.alarm(a.run_timeout_s)
                        D, U = run_method(method, X[:, perm])
                        signal.alarm(0)
                        D = {(perm[i], perm[j]) for i, j in D}
                        U = {tuple(sorted((perm[i], perm[j]))) for i, j in U}
                        rec.update(score(D, U, T, d, seed=zlib.crc32(("%s|%s|%s|%s" % key).encode()), perm_pos=pos))
                        rec["failed"] = None
                    except Exception as e:  # noqa: BLE001
                        signal.alarm(0)
                        rec["failed"] = "%s: %s" % (type(e).__name__, str(e)[:160])
                    rec["seconds"] = round(time.time() - t, 2)
                    with open(runs_f, "a") as fh:
                        fh.write(json.dumps(rec) + "\n")
                    print("%-10s %-4s %-7s %-10s %s %.1fs" % (net, size, method, arm, "FAIL " + rec["failed"] if rec["failed"] else "F1r %.3f F1l %.3f q %s" % (rec["F1_random"], rec["F1_lower"], rec["q"]), rec["seconds"]), flush=True)
    return summarise(a, runs_f, layout)


def summarise(a, runs_f, layout):
    rows = [json.loads(l) for l in open(runs_f)] if runs_f.exists() else []
    out = {"tickets": ["AUD-34", "BEN-07"], "source": "Bayesys repository, Experiment1 (N), sizes 0.1k/1k/10k", "layout": layout, "cells": {}}
    keys = sorted({(r["net"], r["size"], r["method"]) for r in rows})
    for net, size, method in keys:
        rr = [r for r in rows if (r["net"], r["size"], r["method"]) == (net, size, method) and not r.get("failed")]
        rel = [r for r in rr if r["arm"] == "released"]
        sh = [r for r in rr if r["arm"].startswith("shuffled")]
        if not rel or not sh:
            continue
        m = lambda xs, k: round(st.mean([x[k] for x in xs if x[k] is not None]), 4) if [x for x in xs if x[k] is not None] else None
        cell = {"released": {k: rel[0][k] for k in ("S", "c", "q", "F1_random", "F1_lower", "F1_bayesys_half_credit")},
                "shuffled_mean": {k: m(sh, k) for k in ("S", "c", "q", "F1_random", "F1_lower", "F1_bayesys_half_credit")},
                "shuffled_runs": len(sh),
                "shuffled_F1_random_range": [round(min(x["F1_random"] for x in sh), 4), round(max(x["F1_random"] for x in sh), 4)]}
        cell["authors_style_gain"] = round(cell["released"]["F1_lower"] - cell["shuffled_mean"]["F1_random"], 4)
        cell["order_effect_expectation"] = round(cell["released"]["F1_random"] - cell["shuffled_mean"]["F1_random"], 4)
        cell["q_gap_shuffled_minus_released"] = round((cell["shuffled_mean"]["q"] or 0) - (cell["released"]["q"] or 0), 4) if cell["released"]["q"] is not None else None
        out["cells"]["%s|%s|%s" % (net, size, method)] = cell
    causal_order = [n for n, v in layout.items() if v["share_edges_earlier_to_later"] >= 0.85]
    out["P3"] = {"networks_in_causal_order (share >= 0.85)": causal_order,
                 "verdict": "supported" if any(v["kendall_tau_index_vs_depth"] > 0.3 for v in layout.values()) else ("refuted" if all(v["kendall_tau_index_vs_depth"] < 0.1 for v in layout.values()) else "inconclusive")}
    gaps = {k: v["q_gap_shuffled_minus_released"] for k, v in out["cells"].items() if k.split("|")[2] == "pc" and k.split("|")[0] in causal_order and v["q_gap_shuffled_minus_released"] is not None}
    # P4 as worded in plans/audit_dag.json: the effect "appears wherever columns follow causal order" (refuted: |delta q|
    # < 0.03 there). Operationalised per network (2026-10-13, after the first summary; the first version averaged all
    # cells and said "supported" on one 8-variable cell): a network shows the effect if any size has |gap| >= 0.03.
    per_net = {}
    for k, g in gaps.items():
        per_net.setdefault(k.split("|")[0], []).append(g)
    shows = {n: any(abs(g) >= 0.03 for g in v) for n, v in per_net.items()}
    out["P4"] = {"pc_default_q_gap_on_causal_order_networks": gaps,
                 "networks_showing_effect": sorted(n for n, v in shows.items() if v),
                 "networks_without_effect": sorted(n for n, v in shows.items() if not v),
                 "first_version_mean_rule": None if not gaps else round(st.mean(gaps.values()), 4),
                 "verdict": None if not gaps else ("refuted" if not any(shows.values()) else "supported" if all(shows.values())
                                                   else "inconclusive (%d of %d networks)" % (sum(shows.values()), len(shows)))}
    # Layout dose-response (descriptive): what an "earlier column -> later column" rule for undecided pairs is worth,
    # per network, against the share of true edges that run earlier -> later.
    dr = {}
    for net, v in layout.items():
        g = [c["authors_style_gain"] for k, c in out["cells"].items() if k.startswith(net + "|")]
        if g:
            dr[net] = {"share_edges_earlier_to_later": v["share_edges_earlier_to_later"], "cells": len(g),
                       "mean_authors_style_gain": round(st.mean(g), 4), "min": round(min(g), 4), "max": round(max(g), 4)}
    if len(dr) >= 3:
        from scipy.stats import spearmanr
        r = spearmanr([x["share_edges_earlier_to_later"] for x in dr.values()], [x["mean_authors_style_gain"] for x in dr.values()])
        out["layout_dose_response"] = {"per_network": dr, "spearman_share_vs_gain": round(float(r.statistic), 4), "p": round(float(r.pvalue), 4),
                                       "note": "descriptive; six networks"}
    json.dump(out, open(Path(a.out) / "bayesys.json", "w"), indent=1)
    write_contract(Path(a.out))
    print(json.dumps({"layout": layout, "P3": out["P3"], "P4": out["P4"], "layout_dose_response": out.get("layout_dose_response")}, indent=1))
    return out


def write_contract(out_dir):
    """The ab02 folder holds two producers' files: declared per file (score_record.check_contract)."""
    c = {"tickets": ["AUD-34", "BEN-07"], "producer": "analysis/ab02_bayesys.py", "score_bearing": False, "per_file": {
        "alarm_order.json": {"producer": "analysis/ab02_alarm_order.py", "score_bearing": False},
        "bayesys.json": {
            "producer": "analysis/ab02_bayesys.py", "score_bearing": True, "regime": "D",
            "split": "all-public (measurement, no tuning)",
            "controls": {"columns_shuffled": "per-row (arm: released order or shuffled seeds 1-5)", "names": "not applicable",
                         "supplier": "causal-learn 0.1.4.8 (PC, FCI, GES-BDeu)"},
            "orientation_rule": "F1_random: undecided pairs at random (per-run seed); F1_lower: earlier column -> later column",
            "metric_defs": {"F1_random": "directed F1, undecided pairs oriented at random",
                            "F1_lower": "directed F1, undecided pairs oriented earlier column -> later column (the authors' index rule)",
                            "F1_bayesys_half_credit": "Bayesys-style F1: a true adjacency with the wrong or no orientation counts 0.5 TP",
                            "S": "skeleton (adjacency) F1", "c": "share of found true adjacencies with a committed arrow",
                            "q": "share of committed arrows on true adjacencies that point the right way"}}}}
    json.dump(c, open(out_dir / "CONTRACT.json", "w"), indent=1)


if __name__ == "__main__":
    main()
