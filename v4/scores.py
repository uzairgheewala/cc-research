"""Decomposable GES scores for kernel v4 candidates (BLD-18; plans/v4_prereg.json). NumPy only; data are column z-scores.

Every score is a penalised Gaussian log-likelihood of a regression of the child on a design built from its parents:

    local(x, pa) = -n/2 * (1 + log(RSS / n)) - lam * log(n) / 2 * (df + 1)

which is GaussObsL0Pen's local score when the design is the parents' linear terms (df = |pa|). The candidates differ only
in the design (binding time: the knob is fixed in the pre-registration before any dev number exists):

  gauss       linear terms; the v3 engine's score (ges 1.1.0 GaussObsL0Pen), re-implemented for the equality test
  additive    per parent: indicators (k - 1 columns) when the parent is discrete (<= MAX_LEVELS distinct values), else
              a hinge basis z, (z - q25)+, (z - q50)+, (z - q75)+ with the knots at the parent's quartiles; df = columns
  rff         linear terms plus D = min(80, 20 |pa|) random Fourier features of the parents jointly (Gaussian kernel,
              bandwidth sqrt(|pa|), seeded by (x, sorted pa)), fitted by ridge (alpha = 1); df = trace of the hat matrix
lam is the penalty scale (1 = BIC). The child is always modelled as continuous (Gaussian residual), discrete or not.
"""
import zlib

import numpy as np

MAX_LEVELS = 10
DESIGNS = ("gauss", "additive", "rff")


def is_discrete(col):
    return len(np.unique(col)) <= MAX_LEVELS


class DesignScore:
    """A decomposable score for ges.fit (attributes p and local_score; full_score sums local scores)."""

    def __init__(self, Z, design="additive", lam=1.0, ridge=1.0):
        if design not in DESIGNS:
            raise ValueError("unknown design %r" % design)
        self.Z = np.asarray(Z, dtype=float)
        self.n, self.p = self.Z.shape
        self.design, self.lam, self.ridge = design, float(lam), float(ridge)
        self._cache = {}
        self._basis = {}
        self.discrete = [is_discrete(self.Z[:, j]) for j in range(self.p)]

    # ------------------------------------------------------------------ designs
    def parent_basis(self, j):
        if j in self._basis:
            return self._basis[j]
        z = self.Z[:, j]
        if self.discrete[j]:
            levels = np.unique(z)
            B = np.stack([(z == v).astype(float) for v in levels[1:]], axis=1) if len(levels) > 1 else np.zeros((self.n, 0))
        else:
            q = np.quantile(z, [0.25, 0.5, 0.75])
            B = np.stack([z] + [np.maximum(z - k, 0.0) for k in q], axis=1)
        self._basis[j] = B
        return B

    def design_matrix(self, x, pa):
        pa = sorted(pa)
        if not pa:
            return np.zeros((self.n, 0)), 0.0
        if self.design == "gauss":
            return self.Z[:, pa], float(len(pa))
        if self.design == "additive":
            B = np.concatenate([self.parent_basis(j) for j in pa], axis=1)
            return B, float(B.shape[1])
        P = self.Z[:, pa]
        D = min(80, 20 * len(pa))
        rng = np.random.default_rng(zlib.crc32(("%d|%s" % (x, ",".join(map(str, pa)))).encode()))
        W = rng.standard_normal((len(pa), D)) / np.sqrt(len(pa))
        b = rng.uniform(0, 2 * np.pi, D)
        F = np.sqrt(2.0 / D) * np.cos(P @ W + b)
        return np.concatenate([P, F], axis=1), None

    # ------------------------------------------------------------------ scores
    def rss_df(self, x, pa):
        y = self.Z[:, x]
        A, df = self.design_matrix(x, pa)
        A = np.concatenate([np.ones((self.n, 1)), A], axis=1)
        if self.design == "rff" and pa:
            Ac = A[:, 1:] - A[:, 1:].mean(0)
            yc = y - y.mean()
            U, s, Vt = np.linalg.svd(Ac, full_matrices=False)
            shrink = s ** 2 / (s ** 2 + self.ridge)
            fit = U @ (shrink * (U.T @ yc))
            return float(np.sum((yc - fit) ** 2)), float(np.sum(shrink))
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        r = y - A @ coef
        return float(r @ r), df

    def local_score(self, x, pa):
        key = (x, tuple(sorted(pa)))
        if key not in self._cache:
            rss, df = self.rss_df(x, pa)
            sigma2 = max(rss / self.n, 1e-300)
            self._cache[key] = -0.5 * self.n * (1 + np.log(sigma2)) - self.lam * 0.5 * np.log(self.n) * (df + 1)
        return self._cache[key]

    def full_score(self, A):
        A = np.asarray(A)
        return float(sum(self.local_score(j, set(np.flatnonzero(A[:, j]))) for j in range(self.p)))
