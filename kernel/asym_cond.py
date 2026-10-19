"""Direction signals, round 2 (plans/dirsig2_prereg.json): the class fixes for round 1's two failure conditions.
NumPy only; kernel/asym.py (round 1, hashed) is unchanged and reused.

1. Applicability gate (observable, no truth): a pair is declined when either end has a mass point, i.e. at least
   MASS_GATE of its rows on one value (clamps, floors, zero inflation, categorical columns). Round 1: with a child mass
   point >= 20% every signal was confidently wrong.
2. Conditional signals: the other ledger neighbours of each end are regressed out with the pair, so a child's other
   parents stop acting as noise. For "x -> y" the model is y = f(x) + sum_k g_k(z_k) + e over z in Zy (y's ledger
   neighbours other than x and other than y's committed children); the score compares how much the residual still
   depends on the candidate cause in each direction (HSIC), or the regression error (RECI).
3. Mass-point side (lever D14, measured only): the end with the mass point is the child. A structural prior about how
   mechanisms clamp; generator-dependent, reported as such.
"""
import numpy as np

from kernel import asym

MASS_GATE = 0.01
MAX_COND = 6


def masspoint(v):
    _, c = np.unique(v, return_counts=True)
    return float(c.max() / len(v))


def gated(x, y):
    return masspoint(x) < MASS_GATE and masspoint(y) < MASS_GATE


def _additive_basis(cols):
    """Additive cubic-spline basis (no intercept duplication) over several inputs."""
    parts = [np.ones(len(cols[0]))]
    for u in cols:
        uu = np.unique(u)
        if len(uu) <= asym.DISCRETE_MAX:
            parts += [(u == a).astype(float) for a in uu[1:]]
            continue
        us = (u - u.mean()) / (u.std() or 1.0)
        knots = np.unique(np.quantile(us, np.linspace(0, 1, asym.KNOTS + 2)[1:-1]))
        parts += [us, us ** 2, us ** 3] + [np.clip(us - k, 0, None) ** 3 for k in knots]
    return np.column_stack(parts)


def _resid(target, inputs):
    B = _additive_basis(inputs)
    coef, *_ = np.linalg.lstsq(B, target, rcond=None)
    return target - B @ coef


def _cols(X, idx):
    return [asym._std(X[:, k]) for k in list(idx)[:MAX_COND]]


def cond_anm(X, a, b, Za, Zb, seed=0):
    """> 0 says a -> b. Residual of b on (a, Zb) vs residual of a on (b, Za); smaller dependence on the candidate cause wins."""
    xa, xb = asym._std(X[:, a]), asym._std(X[:, b])
    rb = _resid(xb, [xa] + _cols(X, Zb))
    ra = _resid(xa, [xb] + _cols(X, Za))
    i = asym._sub(len(xa), seed)
    return float(np.log(asym.hsic(xb[i], ra[i]) + 1e-12) - np.log(asym.hsic(xa[i], rb[i]) + 1e-12))


def cond_hnm(X, a, b, Za, Zb, seed=0):
    xa, xb = asym._std(X[:, a]), asym._std(X[:, b])

    def sr(t, ins):
        r = _resid(t, ins)
        g = np.sqrt(np.clip(_fit_sq(r, ins), 1e-6, None))      # fitted scale of the residual given the inputs
        return r / g
    rb = sr(xb, [xa] + _cols(X, Zb))
    ra = sr(xa, [xb] + _cols(X, Za))
    i = asym._sub(len(xa), seed)
    return float(np.log(asym.hsic(xb[i], ra[i]) + 1e-12) - np.log(asym.hsic(xa[i], rb[i]) + 1e-12))


def _fit_sq(r, ins):
    t = r ** 2
    return t - _resid(t, ins)


def cond_reci(X, a, b, Za, Zb):
    def mm(v):
        rr = v.max() - v.min()
        return (v - v.min()) / rr if rr > 0 else v * 0.0
    xa, xb = mm(X[:, a]), mm(X[:, b])
    e_ab = float(np.mean(_resid(xb, [xa] + [mm(X[:, k]) for k in list(Zb)[:MAX_COND]]) ** 2))
    e_ba = float(np.mean(_resid(xa, [xb] + [mm(X[:, k]) for k in list(Za)[:MAX_COND]]) ** 2))
    return e_ba - e_ab


def mass_side(x, y, hi=0.20, lo=MASS_GATE):
    """D14: > 0 says x -> y when y has a mass point (>= hi) and x does not (< lo); None otherwise."""
    mx, my = masspoint(x), masspoint(y)
    if my >= hi and mx < lo:
        return 1.0
    if mx >= hi and my < lo:
        return -1.0
    return None


COND = {"C5a_cond_anm": cond_anm, "C6_cond_hnm": cond_hnm, "C5b_cond_reci": lambda X, a, b, Za, Zb, s: cond_reci(X, a, b, Za, Zb)}


def all_cond(X, a, b, Za, Zb, seed=0):
    out = {}
    for k, f in COND.items():
        try:
            v = f(X, a, b, Za, Zb, seed)
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            v = None
        out[k] = None if v is None or not np.isfinite(v) else float(v)
    return out
