"""Sign conventions of the pairwise direction signals (kernel/asym.py): on textbook cases where each signal's assumption
holds, it must say x -> y (score > 0), and every signal is antisymmetric (swapping x and y flips the sign exactly).
A sign error here would invert every downstream measurement, so these run in CI (NumPy only)."""
import sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kernel import asym  # noqa: E402

N = 1500


def case(kind, seed):
    r = np.random.default_rng(seed)
    if kind == "linear_nongaussian":
        x = r.uniform(-1, 1, N)
        return x, x + 0.6 * r.uniform(-1, 1, N)
    if kind == "anm":
        x = r.uniform(-2, 2, N)
        return x, x ** 3 + r.normal(0, 1, N)
    if kind == "low_noise_monotone":
        x = r.uniform(0, 1, N)
        return x, x ** 3 + 0.01 * r.normal(0, 1, N)
    if kind == "heteroscedastic":
        x = r.uniform(-2, 2, N)
        return x, np.sin(x) + (0.2 + 0.4 * np.abs(x)) * r.normal(0, 1, N)
    if kind == "discrete_cause":
        x = r.integers(0, 5, N).astype(float)
        return x, x + r.uniform(-1.5, 1.5, N)
    raise ValueError(kind)


EXPECT = {"D4_entropy_lingam": "linear_nongaussian", "D5a_anm_hsic": "anm", "D5b_reci": "low_noise_monotone",
          "D5c_igci": "low_noise_monotone", "D6_hnm_hsic": "heteroscedastic", "D10_cds": "discrete_cause"}


class SignConvention(unittest.TestCase):
    def test_each_signal_says_x_to_y_on_its_textbook_case(self):
        for name, kind in EXPECT.items():
            wins = 0
            for seed in range(5):
                x, y = case(kind, seed)
                s = asym.SIGNALS[name](x, y, seed)
                self.assertIsNotNone(s, (name, kind))
                wins += s > 0
            self.assertGreaterEqual(wins, 4, "%s on %s: x -> y in only %d of 5" % (name, kind, wins))

    def test_antisymmetry(self):
        for kind in set(EXPECT.values()):
            x, y = case(kind, 7)
            a, b = asym.all_signals(x, y, seed=3), asym.all_signals(y, x, seed=3)
            for k in a:
                if a[k] is None:
                    self.assertIsNone(b[k], k)
                else:
                    self.assertAlmostEqual(a[k], -b[k], places=6, msg=(k, kind))

    def test_continuous_only_signals_decline_discrete_pairs(self):
        x, y = case("discrete_cause", 1)
        self.assertIsNone(asym.entropy_lingam(x, y))
        self.assertIsNone(asym.igci_slope(x, y))


if __name__ == "__main__":
    unittest.main()
