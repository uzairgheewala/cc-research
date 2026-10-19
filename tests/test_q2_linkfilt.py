"""Link filters (kernel/linkfilt.py): on a chain a -> m -> b whose search also returned the shadow a-b, the shadow is the
weakest link of the triangle (ratio < 1) under both strengths, and the two real links are not; a link with no triangle
has no ratio; mutual information is zero-ish for independent columns and positive for dependent ones. NumPy only."""
import sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kernel import linkfilt as F  # noqa: E402


def chain(seed, n=2000):
    r = np.random.default_rng(seed)
    a = r.normal(size=n)
    m = np.tanh(a) + 0.5 * r.normal(size=n)
    b = m ** 3 + 0.5 * r.normal(size=n)
    c = r.normal(size=n)                       # an unrelated column, linked to a only
    return np.column_stack([a, m, b, c])


class DPI(unittest.TestCase):
    def test_shadow_is_weakest_in_its_triangle(self):
        adj = {frozenset(e) for e in [(0, 1), (1, 2), (0, 2), (0, 3)]}
        for seed in range(5):
            X = chain(seed)
            for S in (F.spearman_matrix(X), F.mi_matrix(X)):
                r = F.dpi_ratios(adj, S)
                self.assertLess(r[frozenset((0, 2))], 1.0)
                self.assertGreater(r[frozenset((0, 1))], 1.0)
                self.assertGreater(r[frozenset((1, 2))], 1.0)
                self.assertIsNone(r[frozenset((0, 3))])

    def test_mutual_information_orders_dependence(self):
        X = chain(1)
        M = F.mi_matrix(X)
        self.assertLess(M[0, 3], 0.005)          # bias-corrected: the plug-in estimate alone is ~0.02 here
        self.assertGreater(M[0, 1], 0.1)
        self.assertTrue(np.allclose(M, M.T))


if __name__ == "__main__":
    unittest.main()
