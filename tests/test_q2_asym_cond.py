"""Round-2 direction signals (kernel/asym_cond.py): sign convention with a strong co-parent present, antisymmetry, the
gate, and the mass-point side. NumPy only."""
import sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kernel import asym_cond as C  # noqa: E402

N = 1500


def coparent_case(seed, hetero=False):
    """a -> b <- z, with z the stronger parent; columns [a, b, z]. hetero: b's noise scale grows with |a| (C6's case);
    otherwise constant noise (C5a's and C5b's case). Each signal is tested on the case its model assumes, as in round 1:
    on the other case C5a and C6 are weaker (checked by hand, 15 Oct: C6 3 of 5 on constant noise, C5a 2 of 5 on
    growing noise), which is the known trade-off between the two models, not a sign error."""
    r = np.random.default_rng(seed)
    a = r.uniform(-2, 2, N)
    z = r.uniform(-2, 2, N)
    if hetero:
        b = np.sin(a) + 2.0 * np.sin(1.5 * z) + (0.2 + 0.4 * np.abs(a)) * r.normal(0, 1, N)
    else:
        b = 0.6 * a ** 3 / 4 + 2.0 * np.sin(1.5 * z) + 0.3 * r.normal(0, 1, N)
    return np.column_stack([a, b, z])


class CondSigns(unittest.TestCase):
    def test_conditional_signals_say_a_to_b_with_a_strong_coparent(self):
        for name in ("C5a_cond_anm", "C6_cond_hnm", "C5b_cond_reci"):
            wins = 0
            for seed in range(5):
                X = coparent_case(seed, hetero=(name == "C6_cond_hnm"))
                s = C.COND[name](X, 0, 1, [], [2], seed)
                wins += s > 0
            self.assertGreaterEqual(wins, 4, "%s: a -> b in only %d of 5" % (name, wins))

    def test_antisymmetry(self):
        X = coparent_case(9)
        a = C.all_cond(X, 0, 1, [], [2], seed=1)
        b = C.all_cond(X, 1, 0, [2], [], seed=1)
        for k in a:
            self.assertAlmostEqual(a[k], -b[k], places=6, msg=k)

    def test_gate_and_mass_side(self):
        r = np.random.default_rng(0)
        x = r.uniform(0, 1, N)
        y = np.clip(x + r.normal(0, 0.3, N), 0.2, None)       # clamped child: mass point at 0.2
        self.assertTrue(C.masspoint(y) >= 0.20)
        self.assertFalse(C.gated(x, y))
        self.assertTrue(C.gated(x, x + r.normal(0, 0.1, N)))
        self.assertEqual(C.mass_side(x, y), 1.0)
        self.assertEqual(C.mass_side(y, x), -1.0)


if __name__ == "__main__":
    unittest.main()
