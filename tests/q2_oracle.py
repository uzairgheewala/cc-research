"""Test helper (not a test module): a d-separation oracle and a stable-PC test log built from it, so the kernel's
re-derivation, ledger, checker and verifier can be exercised in CI without causal-learn.

The log follows stable PC (causal-learn SkeletonDiscovery, stable=True): depth by depth, for every ordered pair (x, y)
adjacent at the start of the depth, every subset S of adj(x) minus y of size depth is tested; removals happen at the end
of the depth. Then every test maxP needs (powersets of both endpoints' neighbours, for each unshielded triple) is logged
in phase 'maxp'. p = 1.0 when d-separated, 0.0 otherwise.
"""
import random
from itertools import chain, combinations

import networkx as nx
import numpy as np


def random_dag(p, seed, degree=2.5):
    rng = random.Random(seed)
    order = list(range(p))
    rng.shuffle(order)
    prob = degree / (p - 1)
    return sorted((order[i], order[j]) for i in range(p) for j in range(i + 1, p) if rng.random() < prob)


def oracle(edges, p):
    G = nx.DiGraph()
    G.add_nodes_from(range(p))
    G.add_edges_from(edges)
    dsep = getattr(nx, "is_d_separator", None) or nx.d_separated

    def ci(i, j, S):
        return 1.0 if dsep(G, {i}, {j}, set(S)) else 0.0
    return ci


def pc_log(p, ci, alpha=0.05):
    A = np.ones((p, p), dtype=bool)
    np.fill_diagonal(A, False)
    log = []
    depth = -1
    while A.sum(1).max() - 1 > depth:
        depth += 1
        removal = set()
        for x in range(p):
            nx_ = np.where(A[x])[0].tolist()
            if len(nx_) < depth - 1:
                continue
            for y in nx_:
                rest = [v for v in nx_ if v != y]
                for S in combinations(rest, depth):
                    S = tuple(sorted(S))
                    pv = ci(min(x, y), max(x, y), S)
                    log.append(("skeleton", min(x, y), max(x, y), S, pv))
                    if pv > alpha:
                        removal |= {(x, y), (y, x)}
        for x, y in removal:
            A[x, y] = False
    for x in range(p):
        for z in range(x + 1, p):
            if A[x, z]:
                continue
            for y in range(p):
                if A[x, y] and A[y, z]:
                    nb = lambda v: np.where(A[v])[0].tolist()  # noqa: E731
                    ps = chain.from_iterable(combinations(nb(v), r) for v in (x, z) for r in range(len(nb(v)) + 1))
                    for S in {tuple(sorted(s)) for s in ps}:
                        log.append(("maxp", x, z, S, ci(x, z, S)))
    return log


def true_cpdag(edges, p):
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from score import graph
    return graph.cpdag(edges, p)


def fake_engines(X, names, log=None):
    """An engines dict for kernel.build.build(eng=...): PC result built from an oracle log over the canonical columns."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from engines import core
    from kernel import derive
    from kernel import build as B
    X = np.asarray(X, dtype=float)
    _, order = B.variables(X, [str(n) for n in names])
    p = X.shape[1]
    der = derive.pc_maxp_from_tests(p, log)
    pc = core.EngineResult("pc_maxp", True, marks=der["final"], stages={"skeleton": der["skeleton"], "after_maxp": der["after_maxp"]},
                           tests=log, seconds=0.0)
    import hashlib
    return {"order": order, "Xc": X[:, order], "data_sha": hashlib.sha256(np.ascontiguousarray(X[:, order], dtype="<f8").tobytes()).hexdigest(),
            "pc": pc, "ges": None, "jittered": False, "deviations": []}
