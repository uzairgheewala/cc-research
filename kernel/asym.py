"""Pairwise direction signals that do not depend on collider patterns (lever-map rows D4, D5, D6, D10). NumPy only.

Every signal takes two 1-D arrays x, y (the two ends of a found link) and returns a signed score:
  score > 0  ->  the signal says x -> y
  score < 0  ->  the signal says y -> x
  None       ->  not applicable to this pair (see each function)
|score| is the signal's own strength; scales differ between signals and are compared only within a signal.

  entropy_lingam  D4   linear non-Gaussian likelihood ratio, entropies by m-spacing (Hyvarinen & Smith 2013, eq. form
                       L(x->y) - L(y->x) = H(y) + H(r_x) - H(x) - H(r_y) on standardised data). Continuous pairs only.
  anm_hsic        D5a  additive-noise model: regress each way with a cubic spline; the direction whose residual is less
                       dependent on its input (HSIC, Gaussian kernels, median bandwidth) wins.
  reci            D5b  regression error (Bloebaum et al. 2018): after min-max scaling, the causal direction has the
                       smaller regression error.
  igci_slope      D5c  information-geometric (Daniusis et al. 2010), slope estimator, uniform reference measure.
                       Continuous pairs only.
  hnm_hsic        D6   heteroscedastic noise: as D5a but the residual is divided by a fitted scale g(input) first.
  cds             D10  conditional distribution similarity (Fonollosa 2016): the causal direction's conditional
                       distributions, centred, look alike across cause values. Any pair (continuous columns binned).
"""
import numpy as np

DISCRETE_MAX = 10       # a column with at most this many distinct values is discrete (as in q2_missed_links_study)
HSIC_N = 500            # HSIC on a fixed subsample (O(n^2))
KNOTS = 8               # interior knots of the regression spline


def is_discrete(v):
    return len(np.unique(v)) <= DISCRETE_MAX


def _std(v):
    s = v.std()
    return (v - v.mean()) / s if s > 0 else v - v.mean()


def _rng(seed):
    return np.random.default_rng(seed)


# ---------------------------------------------------------------- regression (cubic regression spline, least squares)
def _basis(u, knots):
    cols = [np.ones_like(u), u, u ** 2, u ** 3] + [np.clip(u - k, 0, None) ** 3 for k in knots]
    return np.column_stack(cols)


def spline_fit(u, v):
    """Fitted values of v on a cubic regression spline of u (knots at quantiles of u; discrete u -> group means)."""
    uu = np.unique(u)
    if len(uu) <= DISCRETE_MAX:
        out = np.empty_like(v, dtype=float)
        for a in uu:
            m = u == a
            out[m] = v[m].mean()
        return out
    us = (u - u.mean()) / (u.std() or 1.0)
    knots = np.unique(np.quantile(us, np.linspace(0, 1, KNOTS + 2)[1:-1]))
    B = _basis(us, knots)
    coef, *_ = np.linalg.lstsq(B, v, rcond=None)
    return B @ coef


# ---------------------------------------------------------------- entropy (m-spacing, Vasicek), for D4
def entropy_mspacing(v):
    n = len(v)
    s = np.sort(v)
    m = max(1, int(round(np.sqrt(n))))
    d = s[m:] - s[:-m]
    floor = 1e-6 * (s[-1] - s[0] if s[-1] > s[0] else 1.0)
    return float(np.mean(np.log(np.maximum(d, floor) * (n + 1) / m)))


def entropy_lingam(x, y):
    if is_discrete(x) or is_discrete(y):
        return None
    x, y = _std(x), _std(y)
    rho = float(np.mean(x * y))
    rx = (x - rho * y) / np.sqrt(max(1e-12, 1 - rho ** 2))     # x's residual given y, standardised
    ry = (y - rho * x) / np.sqrt(max(1e-12, 1 - rho ** 2))
    return entropy_mspacing(y) + entropy_mspacing(rx) - entropy_mspacing(x) - entropy_mspacing(ry)


# ---------------------------------------------------------------- HSIC, for D5a and D6
def _gram(v):
    d = (v[:, None] - v[None, :]) ** 2
    med = np.median(d[d > 0]) if np.any(d > 0) else 1.0
    return np.exp(-d / med)


def hsic(a, b):
    n = len(a)
    K, L = _gram(_std(a)), _gram(_std(b))
    Kc = K - K.mean(0)[None, :] - K.mean(1)[:, None] + K.mean()      # H K H; trace(K H L H) = sum(HKH * L)
    return float(np.sum(Kc * L)) / (n - 1) ** 2


def _sub(n, seed):
    if n <= HSIC_N:
        return np.arange(n)
    return np.sort(_rng(seed).choice(n, HSIC_N, replace=False))


def anm_hsic(x, y, seed=0):
    x, y = _std(x), _std(y)
    ry, rx = y - spline_fit(x, y), x - spline_fit(y, x)
    i = _sub(len(x), seed)
    return float(np.log(hsic(y[i], rx[i]) + 1e-12) - np.log(hsic(x[i], ry[i]) + 1e-12))


def hnm_hsic(x, y, seed=0):
    x, y = _std(x), _std(y)

    def scaled_resid(u, v):
        r = v - spline_fit(u, v)
        g = np.sqrt(np.clip(spline_fit(u, r ** 2), 1e-6, None))
        return r / g
    ry, rx = scaled_resid(x, y), scaled_resid(y, x)
    i = _sub(len(x), seed)
    return float(np.log(hsic(y[i], rx[i]) + 1e-12) - np.log(hsic(x[i], ry[i]) + 1e-12))


# ---------------------------------------------------------------- RECI, D5b
def reci(x, y):
    def mm(v):
        r = v.max() - v.min()
        return (v - v.min()) / r if r > 0 else v * 0.0
    x, y = mm(x), mm(y)
    e_xy = float(np.mean((y - spline_fit(x, y)) ** 2))       # error of the model x -> y
    e_yx = float(np.mean((x - spline_fit(y, x)) ** 2))
    return e_yx - e_xy


# ---------------------------------------------------------------- IGCI slope, D5c
def _igci_c(u, v):
    o = np.argsort(u, kind="stable")
    du, dv = np.diff(u[o]), np.diff(v[o])
    m = (du != 0) & (dv != 0)
    if m.sum() < 10:
        return None
    return float(np.mean(np.log(np.abs(dv[m] / du[m]))))


def igci_slope(x, y):
    if is_discrete(x) or is_discrete(y):
        return None

    def mm(v):
        r = v.max() - v.min()
        return (v - v.min()) / r if r > 0 else v * 0.0
    x, y = mm(x), mm(y)
    cxy, cyx = _igci_c(x, y), _igci_c(y, x)
    if cxy is None or cyx is None:
        return None
    return cyx - cxy


# ---------------------------------------------------------------- CDS, D10
def _levels(v, bins=DISCRETE_MAX):
    u = np.unique(v)
    if len(u) <= bins:
        return np.searchsorted(u, v)
    q = np.quantile(v, np.linspace(0, 1, bins + 1)[1:-1])
    return np.searchsorted(q, v, side="right")


def _cds(cause, effect, min_group=20):
    """Spread, across cause levels, of the centred conditional distribution of effect (lower = more alike)."""
    c, e = _levels(cause), _std(effect)
    edges = np.quantile(e, np.linspace(0, 1, 11))
    hists = []
    for a in np.unique(c):
        m = c == a
        if m.sum() < min_group:
            continue
        z = e[m] - np.median(e[m])
        h, _ = np.histogram(np.clip(z, edges[0] - edges[-1], edges[-1] - edges[0]), bins=10,
                            range=(edges[0] - edges[-1], edges[-1] - edges[0]))
        hists.append(h / h.sum())
    if len(hists) < 2:
        return None
    return float(np.mean(np.std(np.array(hists), axis=0)))


def cds(x, y):
    a, b = _cds(x, y), _cds(y, x)
    if a is None or b is None:
        return None
    return b - a


SIGNALS = {"D4_entropy_lingam": lambda x, y, s: entropy_lingam(x, y),
           "D5a_anm_hsic": anm_hsic,
           "D5b_reci": lambda x, y, s: reci(x, y),
           "D5c_igci": lambda x, y, s: igci_slope(x, y),
           "D6_hnm_hsic": hnm_hsic,
           "D10_cds": lambda x, y, s: cds(x, y)}


def all_signals(x, y, seed=0):
    out = {}
    for k, f in SIGNALS.items():
        try:
            v = f(x, y, seed)
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            v = None
        out[k] = None if v is None or not np.isfinite(v) else float(v)
    return out
