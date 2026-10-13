"""AB-04 (AUD-36): the decision-value scoreboard on two benchmarks outside CausalArena.

  python analysis/dv_chambers_sachs.py --causal-learn PATH --chambers analysis/results/chambers/sample/obs_int_sample.npz \
      --sachs datasets/sachs/sachs.csv --out analysis/results/decision_value_v2

Causal Chambers (light tunnel, lt_interventions_standard_v1; physical ground truth graph('lt','standard'), 57 edges):
  the BEN-10 sample (1,000 observational rows + 100 rows for each of 52 single-target interventions, seed 20261012).
  Variables constant in the observational rows (fixed sensor parameters) cannot be learned from them and are dropped;
  targets are the intervened variables that remain. Truth for "T moves Y": Y is a descendant of T in the full 38-variable
  physical graph. Claims are also checked against the real interventional rows (Welch test, alpha 0.01): here the data are
  physical measurements, so this second check is meaningful (unlike CausalArena, BEN-09).
Sachs (853 observational rows, CD3/CD28; log-transformed): consensus graph of the bnlearn network as bundled in pgmpy
  1.1.2 (sachs.bif.gz, sha256 ed1830fb...; 17 arcs). Every variable is a target (no interventional rows in this file).
  The consensus graph is contested and has no v-structures, so its CPDAG commits no direction: the ceiling is low by
  construction. Reported as a weak benchmark.
Methods (no model calls): PC (upstream causal-learn, default rule and maxP), GES (BIC, `ges` 1.1.0), GIES with targets
(Chambers only, `gies` 0.0.3, jitter 1e-6 as in baseline_variants_run.py), DirectLiNGAM and NOTEARS (|w| >= 0.5) as in
causalarena_methods.py. Columns are given in a seeded random order (seed 20261010) and mapped back.
Tickets: AUD-36, TGT-15, CAP-15
"""
import argparse, contextlib, io, json, math, os, sys, zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from decision_value import reach  # noqa: E402
from decision_value_v2 import claims, threshold  # noqa: E402
from baseline_variants_run import marks_from_cpdag, to_graph  # noqa: E402

SACHS_ARCS = [("Erk", "Akt"), ("Mek", "Erk"), ("PIP3", "PIP2"), ("PKA", "Akt"), ("PKA", "Erk"), ("PKA", "Jnk"), ("PKA", "Mek"),
              ("PKA", "P38"), ("PKA", "Raf"), ("PKC", "Jnk"), ("PKC", "Mek"), ("PKC", "P38"), ("PKC", "PKA"), ("PKC", "Raf"),
              ("Plcg", "PIP2"), ("Plcg", "PIP3"), ("Raf", "Mek")]


def cl_graph_to_sets(M):
    d, u = to_graph(np.asarray(M))
    return d, {tuple(p) for p in u}


def learn(method, X, envs=None):
    """-> (directed set, undirected set) in X's column indices."""
    with contextlib.redirect_stdout(io.StringIO()):
        if method in ("pc", "pc_maxp"):
            from causallearn.search.ConstraintBased.PC import pc
            r, p = (0, 2) if method == "pc" else (1, 3)
            return cl_graph_to_sets(pc(X, 0.05, "fisherz", stable=True, uc_rule=r, uc_priority=p, show_progress=False).G.graph)
        if method == "ges":
            import ges
            if not hasattr(np, "Inf"):
                np.Inf = np.inf
            Z = (X - X.mean(0)) / X.std(0)
            C, _ = ges.fit_bic(Z)
            return cl_graph_to_sets(marks_from_cpdag((np.asarray(C) != 0).astype(int)))
        if method == "gies":
            import gies
            data = [e[0] for e in envs]
            C, _ = gies.fit_bic(data, [e[1] for e in envs])
            return cl_graph_to_sets(marks_from_cpdag((np.asarray(C) != 0).astype(int)))
        if method in ("lingam", "notears"):
            if method == "lingam":
                from causallearn.search.FCMBased.lingam import DirectLiNGAM
                m = DirectLiNGAM(random_state=0)
                m.fit(X)
                W = np.asarray(m.adjacency_matrix_).T
            else:
                from notears_linear import notears_linear
                Z = (X - X.mean(0)) / X.std(0)
                W = notears_linear(Z, lambda1=0.1, max_iter=100, h_tol=1e-8, w_threshold=0.0)
            B = (np.abs(W) >= 0.5)
            np.fill_diagonal(B, False)
            d = {(i, j) for i, j in zip(*np.where(B)) if not B[j, i]}
            u = {(min(i, j), max(i, j)) for i, j in zip(*np.where(B)) if B[j, i]}
            return {(int(a), int(b)) for a, b in d}, {(int(a), int(b)) for a, b in u}
    raise ValueError(method)


def cpdag_sets(edges, n):
    import cc_graph as G
    C = G.cpdag_of(set(edges), n)
    cd, cu = set(), set()
    for x in range(n):
        for y in range(x + 1, n):
            tp = G.pair_type(C, x, y)
            if tp == "a->b":
                cd.add((x, y))
            elif tp == "b->a":
                cd.add((y, x))
            elif tp != "none":
                cu.add((x, y))
    return cd, cu


def score(cl, desc, data_moves=None):
    yes = [k for k, v in cl.items() if v]
    no = [k for k, v in cl.items() if not v]
    out = {"claims": len(cl), "yes": len(yes), "no": len(no),
           "precision_committed": round((sum(1 for t, y in yes if y in desc[t]) + sum(1 for t, y in no if y not in desc[t])) / len(cl), 4) if cl else None,
           "precision_yes": round(sum(1 for t, y in yes if y in desc[t]) / len(yes), 4) if yes else None}
    if data_moves is not None:
        chk = [k for k in cl if k[0] in data_moves]
        out["agreement_with_interventional_data"] = round(sum(1 for t, y in chk if (y in data_moves[t]) == cl[(t, y)]) / len(chk), 4) if chk else None
    return out


def run_benchmark(name, X, names, true_edges, targets, envs_fn, methods, data_moves=None, seed=20261010):
    n = X.shape[1]
    desc = reach(n, set(true_edges))
    pairs = len(targets) * (n - 1)
    rng = np.random.default_rng(seed + zlib.crc32(name.encode()))
    perm = [int(i) for i in rng.permutation(n)]
    pos = {v: i for i, v in enumerate(perm)}
    res = {"variables": n, "targets": len(targets), "pairs": pairs, "true_edges": len(true_edges), "methods": {}}
    refs = {"true DAG": (set(true_edges), set()), "true CPDAG": cpdag_sets(true_edges, n), "empty graph (nothing moves)": (set(), set())}
    for lab, (d, u) in refs.items():
        cl = claims(n, d, u, targets)
        res["methods"][lab] = {"coverage": round(len(cl) / pairs, 4), **score(cl, desc, data_moves)}
    for m in methods:
        Xp = X[:, perm]
        envs = None
        if m == "gies":
            envs = [(e[0][:, perm], [pos[t] for t in e[1]]) for e in envs_fn()]
        try:
            d, u = learn(m, Xp, envs)
        except Exception as e:  # noqa: BLE001
            res["methods"][m] = {"failed": "%s: %s" % (type(e).__name__, str(e)[:200])}
            continue
        d = {(perm[a], perm[b]) for a, b in d}
        u = {tuple(sorted((perm[a], perm[b]))) for a, b in u}
        cl = claims(n, d, u, targets)
        rec = {"coverage": round(len(cl) / pairs, 4), **score(cl, desc, data_moves), "edges_directed": len(d), "edges_undirected": len(u)}
        e = res["methods"]["empty graph (nothing moves)"]["precision_committed"]
        rec["lift_over_empty_graph"] = round(rec["precision_committed"] - e, 4) if rec["precision_committed"] is not None else None
        rec["threshold"] = threshold({"precision_yes": rec["precision_yes"], "yes_rate": rec["yes"] / pairs})
        res["methods"][m] = rec
        print("%-9s %-8s cov %.3f prec %s yes-prec %s lift %s data-agree %s" % (name, m, rec["coverage"], rec["precision_committed"],
              rec["precision_yes"], rec["lift_over_empty_graph"], rec.get("agreement_with_interventional_data")), flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--causal-learn", required=True)
    ap.add_argument("--chambers", required=True)
    ap.add_argument("--sachs", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.causal_learn).resolve()))
    out = {"tickets": ["AUD-36", "TGT-15", "CAP-15"], "benchmarks": {}}

    z = np.load(a.chambers, allow_pickle=True)
    X, reg, var, tg, A = z["X"].astype(float), z["regime"], [str(v) for v in z["variables"]], [str(t) for t in z["targets"]], z["true_adjacency"]
    obs = X[reg == 0]
    keep = [j for j in range(X.shape[1]) if obs[:, j].std() > 1e-9]
    idx = {j: k for k, j in enumerate(keep)}
    full_desc = reach(len(var), {(int(i), int(j)) for i, j in zip(*np.where(A != 0))})
    true_sub = [(idx[i], idx[j]) for i, j in zip(*np.where(A != 0)) if i in idx and j in idx]
    # descendants in the full physical graph, restricted to kept variables (paths through dropped variables count)
    target_vars = sorted({var.index(t) for t in tg if t and var.index(t) in idx})
    targets = [idx[t] for t in target_vars]
    rng = np.random.default_rng(1)
    jitter = lambda M: M + 1e-6 * rng.standard_normal(M.shape)

    def envs():
        e = [(jitter(obs[:, keep]), [])]
        for r, t in enumerate(tg):
            if t and var.index(t) in idx:
                e.append((jitter(X[reg == r][:, keep]), [idx[var.index(t)]]))
        return e
    # data check: does setting T shift Y (Welch, alpha 0.01, intervention rows of T vs observational rows)
    moves = {}
    for r, t in enumerate(tg):
        if not t or var.index(t) not in idx:
            continue
        T = idx[var.index(t)]
        rows = X[reg == r][:, keep]
        s = moves.setdefault(T, set())
        for y in range(len(keep)):
            if y == T:
                continue
            va, vb = rows[:, y].var(ddof=1) / len(rows), obs[:, keep][:, y].var(ddof=1) / len(obs)
            if va + vb > 0 and math.erfc(abs(rows[:, y].mean() - obs[:, keep][:, y].mean()) / math.sqrt(va + vb) / math.sqrt(2)) < 0.01:
                s.add(y)
    true_sub_desc_edges = set(true_sub)
    # replace the restricted-graph reachability by the full-graph one, re-indexed
    res = run_benchmark("chambers", obs[:, keep], [var[j] for j in keep], sorted(true_sub_desc_edges), targets, envs,
                        ["pc", "pc_maxp", "ges", "gies", "lingam", "notears"], data_moves=moves)
    full_vs_sub = sum(1 for T in targets for y in range(len(keep)) if y != T and (keep[y] in full_desc[keep[T]]) != (y in reach(len(keep), true_sub_desc_edges)[T]))
    res.update({"variables_kept": [var[j] for j in keep], "variables_dropped_constant_in_observational_rows": [var[j] for j in range(len(var)) if j not in idx],
                "pairs_where_full_graph_reachability_differs_from_kept_subgraph": full_vs_sub, "truth": "causalchamber graph('lt','standard') (true_adjacency in the sample)",
                "share_of_target_pairs_moved_in_data": round(sum(len(v) for v in moves.values()) / max(1, sum(len(keep) - 1 for _ in moves)), 4)})
    out["benchmarks"]["causal_chambers_lt"] = res

    import csv
    rows = list(csv.reader(open(a.sachs)))
    names, data = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
    Xs = np.log(np.clip(data, 1e-3, None))
    E = [(names.index(u), names.index(v)) for u, v in SACHS_ARCS]
    res = run_benchmark("sachs", Xs, names, E, list(range(len(names))), None, ["pc", "pc_maxp", "ges", "lingam", "notears"])
    res.update({"truth": "bnlearn sachs consensus (pgmpy 1.1.2 sachs.bif.gz sha256 ed1830fbde10...)", "rows": int(Xs.shape[0]),
                "transform": "natural log of values clipped at 1e-3"})
    out["benchmarks"]["sachs"] = res
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "dv_chambers_sachs.json"), "w"), indent=1)
    print("wrote", os.path.join(a.out, "dv_chambers_sachs.json"))


if __name__ == "__main__":
    main()
