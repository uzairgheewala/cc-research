"""Link filters measured as candidate licences (lever-map rows L8 and L7; plans/linkfilt_prereg.json). NumPy only.

A filter proposes to withdraw ("cut") a found link. It never adds a link and never touches directions; a cut link
would be shown as "no claim", not as "independent".

  L8  shadow ordering (data-processing inequality, as in ARACNE, Margolin et al. 2006): in every ledger triangle
      a-b, a-m, m-b, a shadow a-b should be weaker than both links of the path it shadows. For each found link the
      statistic is dpi_ratio = min over triangles of s(a,b) / min(s(a,m), s(m,b)); a link with no triangle has none.
      Strength s is |Spearman| (L8a) or binned mutual information (L8b).
  L7  resampling stability: the share of bootstrap resamples whose ledger contains the link (computed by the
      measurement script from cached resample engines; nothing here).
"""
import numpy as np

BINS = 10
DISCRETE_MAX = 10


def _ranks(v):
    o = np.argsort(v, kind="stable")
    r = np.empty(len(v), dtype=float)
    r[o] = np.arange(len(v))
    # average ranks over ties
    u, inv, cnt = np.unique(v, return_inverse=True, return_counts=True)
    if len(u) < len(v):
        sums = np.bincount(inv, weights=r)
        r = (sums / cnt)[inv]
    return r


def spearman_matrix(X):
    R = np.column_stack([_ranks(X[:, j]) for j in range(X.shape[1])])
    C = np.corrcoef(R, rowvar=False)
    return np.nan_to_num(np.abs(C), nan=0.0)


def _codes(v):
    u = np.unique(v)
    if len(u) <= DISCRETE_MAX:
        return np.searchsorted(u, v)
    q = np.quantile(v, np.linspace(0, 1, BINS + 1)[1:-1])
    return np.searchsorted(q, v, side="right")


def mi_matrix(X):
    """Binned mutual information (nats), plug-in estimator with the Miller-Madow correction, floored at 0; discrete columns keep their values, others 10 quantile bins."""
    n, p = X.shape
    codes = [_codes(X[:, j]) for j in range(p)]
    M = np.zeros((p, p))
    for i in range(p):
        for j in range(i + 1, p):
            a, b = codes[i], codes[j]
            ka, kb = a.max() + 1, b.max() + 1
            joint = np.bincount(a * kb + b, minlength=ka * kb).reshape(ka, kb) / n
            pa, pb = joint.sum(1, keepdims=True), joint.sum(0, keepdims=True)
            nz = joint > 0
            plug = float(np.sum(joint[nz] * np.log(joint[nz] / (pa @ pb)[nz])))
            # Miller-Madow: the plug-in estimate is biased up by about (cells - rows - cols + 1) / 2n, which differs between
            # discrete and binned columns and would tilt triangle comparisons between link types
            bias = (nz.sum() - (pa > 0).sum() - (pb > 0).sum() + 1) / (2.0 * n)
            M[i, j] = M[j, i] = max(0.0, plug - bias)
    return M


def dpi_ratios(adj, S):
    """adj: set of frozenset pairs (the ledger's links); S: strength matrix.
    -> {frozenset(a, b): ratio or None}; ratio < 1 means a-b is the weakest link of some triangle."""
    nb = {}
    for e in adj:
        a, b = tuple(e)
        nb.setdefault(a, set()).add(b)
        nb.setdefault(b, set()).add(a)
    out = {}
    for e in adj:
        a, b = tuple(e)
        common = (nb[a] & nb[b]) - {a, b}
        if not common:
            out[e] = None
            continue
        best = None
        for m in common:
            den = min(S[a, m], S[m, b])
            r = S[a, b] / den if den > 0 else np.inf
            best = r if best is None else min(best, r)
        out[e] = float(best)
    return out
