"""L16 and L5 measurement helpers (analysis/q2_l16.py, analysis/q2_l5.py). NumPy only.

L16: Storey's 1 - pi0 is about 0 for uniform p-values and about 1 when every p-value is tiny; triangles are listed once;
G3's weakest-link test reads a shadow (a -> m -> b, a-b found) as independent given m and a real triangle as dependent.
L5: under do(t), the residual shift of y given the mediator vanishes for a shadow t -> m -> y and stays for a direct
link t -> y, while the marginal shift is present in both. The direct effect here is strong (1.5): with a weaker one
(0.8) the observational regression of y on m absorbs part of it into m's coefficient (m and t are correlated), and the
residual shift can miss it at 40 rows (seen while writing this test, 19 Oct; a failure mode for rule S)."""
import sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))
import q2_l16 as L16  # noqa: E402
import q2_l5 as L5  # noqa: E402
from kernel import interventions as IV  # noqa: E402
from kernel import linkfilt as F  # noqa: E402


class Storey(unittest.TestCase):
    def test_uniform_and_tiny(self):
        r = np.random.default_rng(0)
        self.assertLess(L16.storey_pi1(list(r.uniform(size=4000))), 0.06)
        self.assertGreater(L16.storey_pi1([1e-6] * 100), 0.99)
        self.assertIsNone(L16.storey_pi1([]))


class Triangles(unittest.TestCase):
    def test_listed_once(self):
        adj = {frozenset(e) for e in [(0, 1), (1, 2), (0, 2), (2, 3), (1, 3)]}
        self.assertEqual(L16.triangles(adj), [(0, 1, 2), (1, 2, 3)])


def _signed_spearman(X):
    R = np.column_stack([F._ranks(X[:, j]) for j in range(X.shape[1])])
    return np.corrcoef(R, rowvar=False)


class G3Test(unittest.TestCase):
    def test_shadow_vs_real_triangle(self):
        r = np.random.default_rng(1)
        n = 3000
        a = r.normal(size=n)
        m = a + 0.6 * r.normal(size=n)
        b_shadow = m + 0.6 * r.normal(size=n)
        b_real = m + 0.6 * a + 0.6 * r.normal(size=n)
        for b, small in ((b_shadow, False), (b_real, True)):
            X = np.column_stack([a, m, b])
            p = L16.g3_pvalues(_signed_spearman(X), [(0, 1, 2)], n)[0]
            if small:
                self.assertLess(p, 1e-3)
            else:
                self.assertGreater(p, 1e-3)


class ResidualShift(unittest.TestCase):
    def _data(self, direct, seed):
        r = np.random.default_rng(seed)
        def gen(n, t=None):
            tt = r.normal(size=n) if t is None else np.full(n, t) + 0.1 * r.normal(size=n)
            m = tt + 0.5 * r.normal(size=n)
            y = m + (1.5 * tt if direct else 0.0) + 0.5 * r.normal(size=n)
            return np.column_stack([tt, m, y])
        return gen(800), gen(40, t=2.0)

    def test_shadow_vanishes_direct_stays(self):
        for seed in range(5):
            obs, rows = self._data(False, seed)
            self.assertLess(IV.welch(rows[:, 2], obs[:, 2])[1], 0.01)          # marginal shift present
            self.assertGreater(L5._resid_shift(obs, rows, 2, [1]), 0.01)      # gone given the mediator
            obs, rows = self._data(True, seed)
            self.assertLess(L5._resid_shift(obs, rows, 2, [1]), 0.01)         # stays for a direct link


if __name__ == "__main__":
    unittest.main()
