"""B0.1: the PC-maxP wrapper recovers the true equivalence class from a perfect independence oracle under every column
order, and the kernel's canonical ordering makes its input, hence its output, order-invariant.

  CC_CAUSAL_LEARN=PATH python -m engines.oracle_check [--dags 120 --perms 6 --out analysis/results/q2_b0/oracle_check.json]

Random DAGs: the AB-03 generator (analysis/engine_oracle_check.random_dags, seed 20261013): p in {6, 8, 10, 12},
expected degree 2-3. For each DAG and each of 6 column orders (identity, reversed, 4 seeded):
  exact      run_pc_maxp with the d-separation oracle on the permuted columns returns the true CPDAG (mapped back)
  rederived  kernel.derive re-derives the same graph from the engine's recorded tests
  invariant  with the kernel's canonical order (by variable identity), all 6 orders give the identical engine output
Pass (gate B0.1, plans/q2_build_prereg.json): 720/720 exact and 120/120 order-invariant. No data, no model calls.
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dags", type=int, default=120)
    ap.add_argument("--perms", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20261013)
    ap.add_argument("--out", default=str(ROOT / "analysis" / "results" / "q2_b0" / "oracle_check.json"))
    a = ap.parse_args()
    import networkx as nx
    import numpy as np
    from engine_oracle_check import perms, random_dags
    from engines import core
    from kernel import derive
    from score import graph
    dsep = getattr(nx, "is_d_separator", None) or nx.d_separated
    dags = random_dags(a.dags, a.seed)
    rows, exact, rederived, invariant = [], 0, 0, 0
    for di, d in enumerate(dags):
        p, edges = d["p"], [tuple(e) for e in d["edges"]]
        G = nx.DiGraph()
        G.add_nodes_from(range(p))
        G.add_edges_from(edges)
        Dt, Ut = graph.cpdag(edges, p)
        Ut = {tuple(sorted(u)) for u in Ut}
        outs = []
        for pi, perm in enumerate(perms(p, a.perms, 1000 + di)):
            ci = lambda i, j, S, perm=perm: 1.0 if dsep(G, {perm[i]}, {perm[j]}, {perm[s] for s in S}) else 0.0  # noqa: E731
            r = core.run_pc_maxp(None, ci=ci, p=p)
            ok = r.ok
            D, U = core.map_back(*core.marks_to_sets(r.marks), perm) if ok else (None, None)
            e_ok = ok and (D, U) == (Dt, Ut)
            der = derive.pc_maxp_from_tests(p, r.tests) if ok else None
            r_ok = ok and np.array_equal(der["final"], r.marks) and not der["missing_tests"]
            exact += e_ok
            rederived += r_ok
            # canonical order by variable identity: the label of the original variable in each column
            ids = ["var%03d" % perm[k] for k in range(p)]
            order = core.canonical_order(ids=ids)
            canon = [perm[k] for k in order]                       # original variable in each canonical column
            ci_c = lambda i, j, S, c=canon: 1.0 if dsep(G, {c[i]}, {c[j]}, {c[s] for s in S}) else 0.0  # noqa: E731
            rc = core.run_pc_maxp(None, ci=ci_c, p=p)
            outs.append(rc.marks.tolist() if rc.ok else None)
            rows.append({"dag": di, "perm": pi, "p": p, "exact": bool(e_ok), "rederived": bool(r_ok), "failure": r.failure})
        inv = all(o is not None and o == outs[0] for o in outs)
        invariant += inv
        rows.append({"dag": di, "invariant": bool(inv)})
    total = a.dags * a.perms
    res = {"tickets": ["CAP-05", "CAP-11", "BLD-02"], "gate": "B0.1", "engine": "causal-learn 0.1.4.8 pc maxP via engines.core.run_pc_maxp",
           "dags": a.dags, "perms": a.perms, "seed": a.seed, "exact": exact, "rederived": rederived, "runs": total,
           "order_invariant_dags": invariant, "pass": exact == total and invariant == a.dags and rederived == total, "rows": rows}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print("exact %d/%d; re-derived %d/%d; order-invariant %d/%d; %s" % (exact, total, rederived, total, invariant, a.dags, "PASS" if res["pass"] else "FAIL"))
    sys.exit(0 if res["pass"] else 1)


if __name__ == "__main__":
    main()
