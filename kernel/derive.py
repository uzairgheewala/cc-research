"""Re-derive PC with maxP from its recorded CI tests (K7 checker core; NumPy only).

Index space: the canonical column order the engine saw (0..n-1). Marks follow causal-learn: M[i, j] is the mark at i
on the i-j edge (-1 tail, 1 arrowhead, 0 none); i -> j is M[i, j] = -1, M[j, i] = 1.

The procedures below mirror causal-learn 0.1.4.8 (SkeletonDiscovery stable, UCSepset.maxp priority 3, Meek.meek) step
for step, including the order in which candidate triples are listed and conflicts resolved, so that the re-derived graph
equals the engine's graph exactly. B1 rung R1 checks the equality on every dev file; any difference is reported, never
patched over.
  skeleton    a pair is non-adjacent iff some skeleton-phase test of it had p > alpha (stable PC removes an edge after
              every conditioning set of the current depth has been tried; the tests themselves are recorded)
  maxp        for each unshielded triple x - y - z (x < z): p_with = max p(x, z | S) over S in the powerset of
              adj(x) or of adj(z) containing y; p_without = the same over S not containing y. A collider candidate
              when p_without > p_with. Candidates applied in ascending p_with (ties in listing order); a candidate is
              applied only if neither y -> x nor y -> z is already oriented.
  meek        R1 over unshielded triples, R2 over triangles, R3 over kites, repeated to a fixed point; an orientation that
              would make a directed cycle is skipped (causal-learn's ancestor check).
"""
from itertools import chain, combinations, permutations

import numpy as np


def _powerset(xs):
    xs = list(xs)
    return chain.from_iterable(combinations(xs, r) for r in range(len(xs) + 1))


def skeleton(n, tests, alpha):
    """tests: iterable of (phase, i, j, S, p). -> adjacency matrix A (bool) after the skeleton phase."""
    A = np.ones((n, n), dtype=bool)
    np.fill_diagonal(A, False)
    for ph, i, j, S, p in tests:
        if ph == "skeleton" and p > alpha:
            A[i, j] = A[j, i] = False
    return A


def skeleton_marks(A):
    M = np.zeros(A.shape, dtype=int)
    M[A] = -1
    return M


def _adj_list(M):
    """causal-learn find_adj: find_tails() + find_arrow_heads(), each as (col, row) pairs in row-major order."""
    tails = np.where(M == -1)
    heads = np.where(M == 1)
    return list(zip(tails[1].tolist(), tails[0].tolist())) + list(zip(heads[1].tolist(), heads[0].tolist()))


def unshielded_triples(M):
    adj = _adj_list(M)
    return [(p0[0], p0[1], p1[1]) for p0, p1 in permutations(adj, 2)
            if p0[1] == p1[0] and p0[0] != p1[1] and M[p0[0], p1[1]] == 0]


def triangles(M):
    adj = _adj_list(M)
    aset = set(adj)
    return [(p0[0], p0[1], p1[1]) for p0, p1 in permutations(adj, 2)
            if p0[1] == p1[0] and p0[0] != p1[1] and (p0[0], p1[1]) in aset]


def kites(M):
    tri = triangles(M)
    return [(p0[0], p0[1], p1[1], p0[2]) for p0, p1 in permutations(tri, 2)
            if p0[0] == p1[0] and p0[2] == p1[2] and p0[1] < p1[1] and M[p0[1], p1[1]] == 0]


def _directed(M, i, j):
    return M[i, j] == -1 and M[j, i] == 1


def _undirected(M, i, j):
    return M[i, j] == -1 and M[j, i] == -1


def _orient(M, i, j):
    M[i, j], M[j, i] = -1, 1


def maxp(M_skel, pvalue, priority=3):
    """M_skel: skeleton marks. pvalue(x, z, S) -> recorded p. Returns (marks after maxP, collider records)."""
    M = M_skel.copy()
    nbr = lambda v: np.where(M_skel[v, :] != 0)[0].tolist()  # noqa: E731
    cands = []
    for (x, y, z) in [t for t in unshielded_triples(M_skel) if t[0] < t[2]]:
        sets = {tuple(sorted(S)) for S in chain(_powerset(nbr(x)), _powerset(nbr(z)))}
        sets = [S for S in sets if x not in S and z not in S]
        with_y = [pvalue(x, z, S) for S in sets if y in S]
        without_y = [pvalue(x, z, S) for S in sets if y not in S]
        p_with, p_without = max(with_y), max(without_y)
        cands.append({"x": x, "y": y, "z": z, "p_with": p_with, "p_without": p_without, "candidate": p_without > p_with,
                      "applied": False})
    order = sorted([c for c in cands if c["candidate"]], key=lambda c: c["p_with"])     # stable: ties keep listing order
    for c in order:
        x, y, z = c["x"], c["y"], c["z"]
        if not _directed(M, y, x) and not _directed(M, y, z):
            _orient(M, x, y)
            _orient(M, z, y)
            c["applied"] = True
    return M, cands


def _ancestor(M, a, b):
    """a is an ancestor of b through directed edges (a == b counts, as causal-learn's dpath diagonal)."""
    if a == b:
        return True
    n = M.shape[0]
    stack, seen = [a], {a}
    while stack:
        u = stack.pop()
        for v in range(n):
            if _directed(M, u, v) and v not in seen:
                if v == b:
                    return True
                seen.add(v)
                stack.append(v)
    return False


def meek(M_in):
    """-> (final marks, {(i, j): rule}) for every edge Meek oriented."""
    M = M_in.copy()
    UT, Tri, Kite = unshielded_triples(M), triangles(M), kites(M)
    labels = {}
    loop = True
    while loop:
        loop = False
        for (i, j, k) in UT:
            if _directed(M, i, j) and _undirected(M, j, k):
                if _ancestor(M, k, j):
                    continue
                _orient(M, j, k)
                labels[(j, k)] = "meek_r1"
                loop = True
        for (i, j, k) in Tri:
            if _directed(M, i, j) and _directed(M, j, k) and _undirected(M, i, k):
                if _ancestor(M, k, i):
                    continue
                _orient(M, i, k)
                labels[(i, k)] = "meek_r2"
                loop = True
        for (i, j, k, l) in Kite:
            if _undirected(M, i, j) and _undirected(M, i, k) and _directed(M, j, l) and _directed(M, k, l) and _undirected(M, i, l):
                if _ancestor(M, l, i):
                    continue
                _orient(M, i, l)
                labels[(i, l)] = "meek_r3"
                loop = True
    return M, labels


def pc_maxp_from_tests(n, tests, alpha=0.05):
    """Full re-derivation. Returns {"skeleton": marks, "after_maxp": marks, "final": marks, "colliders": [...],
    "meek_labels": {...}, "missing_tests": [...]} ; missing_tests lists (x, z, S) the maxP step needed but the records lack."""
    pv = {}
    for ph, i, j, S, p in tests:
        key = (min(i, j), max(i, j), tuple(sorted(S)))
        pv.setdefault(key, p)
    missing = []

    def pvalue(x, z, S):
        key = (min(x, z), max(x, z), tuple(sorted(S)))
        if key not in pv:
            missing.append(key)
            return -1.0
        return pv[key]
    A = skeleton(n, tests, alpha)
    Ms = skeleton_marks(A)
    Mm, cols = maxp(Ms, pvalue)
    Mf, labels = meek(Mm)
    return {"skeleton": Ms, "after_maxp": Mm, "final": Mf, "colliders": cols, "meek_labels": labels, "missing_tests": missing}
