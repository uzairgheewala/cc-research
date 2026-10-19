"""K1 link recovery (kernel v3): a second look at every pair the ledger left unconnected, with tests the engines do not
use, so that links the Gaussian linear tests are blind to are recovered as typed "weak link" claims.

Why (docs/design/q2_kernel_v3_design.md section 2): on dev, the v2 skeleton misses about a third of true links; 65% of
semantic misses touch a column with <= 10 distinct values, 38-45% carry a nonlinear conditional signal, and about a third
show no signal under any test (the floor).

The battery, for one pair (x, y) and one conditioning set S, each a p-value for "x independent of y given S":
  T0 fisher_z   partial correlation of x and y given S, Fisher z (the engines' own test; the baseline)
  T1 rank_z     the same on rank-transformed columns (average ranks): monotone nonlinear and tied (discrete) columns
  T2 resid_chi2 x and y residualised on an additive cubic basis of S (one-hot for a discrete member of S); the residuals
                cut into quantile bins (a discrete x or y keeps its own levels, up to 10) and tested with a chi-square test
                of independence: non-monotone dependence, dependence in a discrete column's levels
combined as p = min(1, 3 * min(p0, p1, p2)) (Bonferroni over the battery).

Recovery rule for a pair the ledger left unconnected (fixed in plans/k1_prereg.json before any dev run):
  * conditioning sets: the empty set, every subset of size <= max_k (default 2) of adj(x) \ {y} and of adj(y) \ {x} in the
    ledger's graph, and the two full neighbourhoods; a pair is a candidate only if the combined test rejects for every
    one of them (p_pair = max over sets), the local version of PC's adjacency rule;
  * Benjamini-Hochberg at q = 0.05 over the candidate pairs of one table;
  * a recovered pair becomes a claim with relation "x~y" (weak link): connected, direction open, licence "recovered",
    evidence a "dependence_test" record per conditioning set tried. It never removes or reorients anything.
Deterministic (no random numbers); NumPy and SciPy only.
"""
from itertools import combinations

import numpy as np
from scipy import stats

DISCRETE_MAX = 10


def is_discrete(col):
    return len(np.unique(col)) <= DISCRETE_MAX


def _ranks(X):
    return np.column_stack([stats.rankdata(X[:, j]) for j in range(X.shape[1])])


def _partial_z(C, i, j, S, n):
    idx = [i, j] + list(S)
    sub = C[np.ix_(idx, idx)]
    try:
        P = np.linalg.inv(sub)
    except np.linalg.LinAlgError:
        P = np.linalg.pinv(sub)
    r = -P[0, 1] / np.sqrt(abs(P[0, 0] * P[1, 1]))
    r = float(np.clip(r, -0.999999, 0.999999))
    z = 0.5 * np.log((1 + r) / (1 - r)) * np.sqrt(max(n - len(S) - 3, 1))
    return float(2 * stats.norm.sf(abs(z))), r


def _basis(X, S, disc):
    cols = [np.ones(X.shape[0])]
    for s in S:
        v = X[:, s]
        if disc[s]:
            lv = np.unique(v)
            cols += [(v == l).astype(float) for l in lv[1:]]
        else:
            z = (v - v.mean()) / (v.std() or 1.0)
            cols += [z, z ** 2, z ** 3]
    return np.column_stack(cols)


def _resid(y, B):
    coef, *_ = np.linalg.lstsq(B, y, rcond=None)
    return y - B @ coef


def _bins(v, disc, k=5):
    if disc:
        _, inv = np.unique(v, return_inverse=True)
        return inv
    q = np.quantile(v, np.linspace(0, 1, k + 1)[1:-1])
    return np.searchsorted(q, v, side="right")


def _chi2(a, b):
    ka, kb = a.max() + 1, b.max() + 1
    if ka < 2 or kb < 2:
        return 1.0
    T = np.zeros((ka, kb))
    np.add.at(T, (a, b), 1)
    T = T[T.sum(1) > 0][:, T.sum(0) > 0]
    if T.shape[0] < 2 or T.shape[1] < 2:
        return 1.0
    E = T.sum(1, keepdims=True) * T.sum(0, keepdims=True) / T.sum()
    chi = float(((T - E) ** 2 / E).sum())
    return float(stats.chi2.sf(chi, (T.shape[0] - 1) * (T.shape[1] - 1)))


class Battery:
    """Precomputes what every test of one table shares (correlations, ranks, discreteness)."""

    def __init__(self, X):
        X = np.asarray(X, dtype=float)
        self.X, self.n = X, X.shape[0]
        sd = X.std(0)
        self.const = sd < 1e-12
        Xs = np.where(self.const, 0.0, (X - X.mean(0)) / np.where(self.const, 1.0, sd))
        self.C = np.corrcoef(Xs.T) if X.shape[1] > 1 else np.ones((1, 1))
        self.C = np.nan_to_num(self.C)
        np.fill_diagonal(self.C, 1.0)
        R = _ranks(X)
        self.Cr = np.nan_to_num(np.corrcoef(R.T))
        np.fill_diagonal(self.Cr, 1.0)
        self.disc = [bool(is_discrete(X[:, j])) for j in range(X.shape[1])]
        self.tests = 0

    def test(self, i, j, S):
        """-> dict(p0, p1, p2, p) for x_i independent of x_j given x_S."""
        self.tests += 1
        S = tuple(S)
        if self.const[i] or self.const[j]:
            return {"p0": 1.0, "p1": 1.0, "p2": 1.0, "p": 1.0}
        p0, r0 = _partial_z(self.C, i, j, S, self.n)
        p1, _ = _partial_z(self.Cr, i, j, S, self.n)
        B = _basis(self.X, S, self.disc)
        ri = self.X[:, i] if (self.disc[i] and not S) else _resid(self.X[:, i], B)
        rj = self.X[:, j] if (self.disc[j] and not S) else _resid(self.X[:, j], B)
        p2 = _chi2(_bins(ri, self.disc[i] and not S), _bins(rj, self.disc[j] and not S))
        return {"p0": p0, "p1": p1, "p2": p2, "p": min(1.0, 3 * min(p0, p1, p2)), "r": r0}


def conditioning_sets(i, j, adj, max_k=2, n_vars=None, full=False):
    """Empty set, subsets of size <= max_k of each neighbourhood, both full neighbourhoods; with full=True also every
    other variable (blocks a shadow path through a mediator the ledger has not connected; a co-parent pair is already
    excluded by the empty set, where it is independent)."""
    Ni = sorted(adj[i] - {j})
    Nj = sorted(adj[j] - {i})
    out, seen = [], set()
    for base in (Ni, Nj):
        for k in range(0, max_k + 1):
            for S in combinations(base, k):
                if S not in seen:
                    seen.add(S)
                    out.append(S)
    extra = [tuple(Ni), tuple(Nj)]
    if full and n_vars is not None:
        extra.append(tuple(v for v in range(n_vars) if v not in (i, j)))
    for S in extra:
        if S not in seen:
            seen.add(S)
            out.append(S)
    return out


def bh(ps, q):
    """Benjamini-Hochberg: indices of rejected hypotheses."""
    m = len(ps)
    if not m:
        return set()
    order = sorted(range(m), key=lambda k: ps[k])
    kmax = 0
    for r, k in enumerate(order, 1):
        if ps[k] <= q * r / m:
            kmax = r
    return set(order[:kmax])


def dependence_pool(bat, n_vars, alpha=0.05):
    """Pairs the battery finds marginally dependent (combined p <= alpha): the pool a separating set is drawn from when
    the ledger's own graph is missing the mediator (a missed X-M link hides the set that would separate X and Y)."""
    dep = {v: set() for v in range(n_vars)}
    for i, j in combinations(range(n_vars), 2):
        if bat.test(i, j, ())["p"] <= alpha:
            dep[i].add(j)
            dep[j].add(i)
    return dep


def recover(X, adj_pairs, n_vars, max_k=2, q=0.05, alpha_screen=0.05, full=False, pool="ledger", test="battery"):
    """X: the table in the ledger's index space; adj_pairs: set of frozenset pairs the ledger connects.
    -> dict(recovered=[(i, j, p_pair)], candidates=[...], records={(i, j): [tests]}, tests=int)."""
    bat = Battery(X)
    adj = {v: set() for v in range(n_vars)}
    for e in adj_pairs:
        a, b = tuple(e)
        adj[a].add(b)
        adj[b].add(a)
    cands, records = [], {}
    dep = dependence_pool(bat, n_vars, alpha_screen) if pool == "dependence" else None
    for i, j in combinations(range(n_vars), 2):
        if frozenset((i, j)) in adj_pairs:
            continue
        rec, pmax, alive = [], 0.0, True
        if dep is not None:
            if j not in dep[i]:
                continue
            common = (dep[i] & dep[j]) | adj[i] | adj[j]
            nb = {v: set() for v in range(n_vars)}
            nb[i] = (common - {j}) | (adj[i] - {j})
            nb[j] = (common - {i}) | (adj[j] - {i})
            sets = conditioning_sets(i, j, nb, max_k, n_vars, full)
        else:
            sets = conditioning_sets(i, j, adj, max_k, n_vars, full)
        for S in sets:
            t = bat.test(i, j, S) if test == "battery" else cell_test(bat.X, i, j, S)
            rec.append({"S": list(S), **t})
            pmax = max(pmax, t["p"])
            if pmax > alpha_screen:          # dependence not shown for this set: the pair cannot be recovered
                alive = False
                break
        if alive:
            cands.append((i, j, pmax))
            records[(i, j)] = rec
    keep = bh([p for _, _, p in cands], q)
    recovered = [cands[k] for k in sorted(keep)]
    return {"recovered": recovered, "candidates": cands, "records": {k: records[k] for k in records if any(k == (a, b) for a, b, _ in recovered)},
            "tests": bat.tests, "discrete": bat.disc}


def audit(X, adj_pairs, n_vars, max_k=2, alpha_sep=0.05, bat=None):
    """The other direction (K1b, measured before it is adopted): for every pair the ledger connects, is there a local
    conditioning set (as in recover(), without the full set) under which the whole battery fails to reject
    independence (combined p > alpha_sep)? -> {(i, j): (S, p)} for the pairs that would be separated."""
    bat = bat or Battery(X)
    adj = {v: set() for v in range(n_vars)}
    for e in adj_pairs:
        a, b = tuple(e)
        adj[a].add(b)
        adj[b].add(a)
    out = {}
    for e in sorted(tuple(sorted(e)) for e in adj_pairs):
        i, j = e
        for S in conditioning_sets(i, j, adj, max_k):
            t = bat.test(i, j, S)
            if t["p"] > alpha_sep:
                out[e] = (list(S), t["p"])
                break
    return out


def flex_residual(X, target, cond, folds=2):
    """Cross-fitted gradient-boosting residual of column `target` on columns `cond` (deterministic: fixed folds by row
    parity, no subsampling, no early stopping)."""
    from sklearn.ensemble import HistGradientBoostingRegressor as HGB
    y = X[:, target]
    if not cond:
        return y - y.mean()
    Z = X[:, list(cond)]
    r = np.empty_like(y)
    idx = np.arange(len(y))
    for k in range(folds):
        te = idx % folds == k
        m = HGB(max_iter=100, max_leaf_nodes=15, learning_rate=0.1, early_stopping=False, random_state=0)
        m.fit(Z[~te], y[~te])
        r[te] = y[te] - m.predict(Z[te])
    return r


def flex_test(X, i, j, cond):
    """x_i independent of x_j given x_cond, with flexible (cross-fitted boosting) residualisation of both: p-value of
    the residuals' dependence, 2 * min(rank-correlation p, binned chi-square p)."""
    ri, rj = flex_residual(X, i, cond), flex_residual(X, j, cond)
    rho, p_rank = stats.spearmanr(ri, rj)
    p_chi = _chi2(_bins(ri, False), _bins(rj, False))
    return {"p_rank": float(p_rank), "p_chi2": float(p_chi), "p": min(1.0, 2 * min(float(p_rank), p_chi)), "rho": float(rho)}


def cell_residual(X, target, S, bins1=10, bins2=6):
    """Residual of column `target` after removing its mean within joint quantile cells of the conditioning columns
    (10 cells for one column, 6 x 6 for two; a discrete column keeps its levels). Nonparametric in S: it removes any
    dependence of the target on S up to the cell resolution, which a linear or rank partial correlation does not
    (a nonlinear mediator X -> M -> Y leaves linear partial dependence between X and Y given M)."""
    y = X[:, target].astype(float)
    if not S:
        return y - y.mean()
    if len(S) > 2:
        return _resid(y, _basis(X, S, [is_discrete(X[:, v]) for v in range(X.shape[1])]))
    k = bins1 if len(S) == 1 else bins2
    code = np.zeros(len(y), dtype=np.int64)
    for s in S:
        v = X[:, s]
        if is_discrete(v):
            _, c = np.unique(v, return_inverse=True)
        else:
            c = np.searchsorted(np.quantile(v, np.linspace(0, 1, k + 1)[1:-1]), v, side="right")
        code = code * 64 + c
    _, cell = np.unique(code, return_inverse=True)
    sums = np.bincount(cell, weights=y)
    cnt = np.bincount(cell)
    return y - (sums / cnt)[cell]


def cell_test(X, i, j, S):
    ri, rj = cell_residual(X, i, S), cell_residual(X, j, S)
    if ri.std() < 1e-12 or rj.std() < 1e-12:
        return {"p": 1.0, "p_rank": 1.0, "p_chi2": 1.0}
    _, p_rank = stats.spearmanr(ri, rj)
    p_chi = _chi2(_bins(ri, False), _bins(rj, False))
    p_rank = float(p_rank) if np.isfinite(p_rank) else 1.0
    return {"p": min(1.0, 2 * min(p_rank, p_chi)), "p_rank": p_rank, "p_chi2": p_chi}
