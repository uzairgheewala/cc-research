"""B4: the isotonic calibration map (NumPy only) is monotone, reproduces pooled rates, and is applied as a step."""
import sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kernel import confidence as C  # noqa: E402


class Isotonic(unittest.TestCase):
    def test_monotone_and_pooled(self):
        rng = np.random.default_rng(0)
        x = rng.random(500)
        y = (rng.random(500) < x).astype(float)
        m = C.isotonic_fit(x, y)
        self.assertTrue(all(a <= b + 1e-12 for a, b in zip(m["y"], m["y"][1:])))
        self.assertAlmostEqual(float(np.mean(C.isotonic_apply(m, x))), float(y.mean()), places=9)

    def test_violators_pooled(self):
        m = C.isotonic_fit([0.1, 0.2, 0.3], [1, 0, 1])
        self.assertEqual(m["y"], [0.5, 0.5, 1.0])
        self.assertEqual(list(C.isotonic_apply(m, [0.0, 0.15, 0.25, 0.9])), [0.5, 0.5, 0.5, 1.0])


if __name__ == "__main__":
    unittest.main()
