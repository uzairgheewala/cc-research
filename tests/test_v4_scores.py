"""BLD-18: kernel v4 candidate scores (v4/scores.py) and the pre-registered decision rule (v4/dev.py decide).

Must show: the gauss design reproduces ges 1.1.0 GaussObsL0Pen's local scores; a discrete parent enters as k - 1 indicators;
the additive score sees a nonlinear parent the linear score cannot; rff's degrees of freedom are a hat-matrix trace; the
decision rule picks the best adoptable candidate and returns 'none' when no gain clears the bar. Needs NumPy and ges.
"""
import importlib.util, json, sys, unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
HAVE_GES = importlib.util.find_spec("ges") is not None


def data(seed=0, n=1000):
    r = np.random.default_rng(seed)
    x = r.standard_normal(n)
    d = r.integers(0, 3, n).astype(float)
    y = x ** 2 + 0.8 * d + 0.3 * r.standard_normal(n)          # nonlinear in x, discrete effect of d
    z = 0.7 * y + 0.5 * r.standard_normal(n)
    X = np.stack([x, d, y, z], axis=1)
    return (X - X.mean(0)) / X.std(0)


class ScoresTest(unittest.TestCase):
    @unittest.skipUnless(HAVE_GES, "ges not installed")
    def test_gauss_equals_ges_package(self):
        from ges.scores.gauss_obs_l0_pen import GaussObsL0Pen
        from v4.scores import DesignScore
        Z = data()
        a, b = GaussObsL0Pen(Z), DesignScore(Z, "gauss")
        for x, pa in ((2, set()), (2, {0}), (2, {0, 1}), (3, {2}), (3, {0, 1, 2})):
            self.assertAlmostEqual(a.local_score(x, pa), b.local_score(x, pa), places=6)

    def test_discrete_parent_indicators(self):
        from v4.scores import DesignScore
        S = DesignScore(data(), "additive")
        self.assertTrue(S.discrete[1])
        self.assertEqual(S.parent_basis(1).shape[1], 2)        # 3 levels -> 2 indicator columns
        self.assertEqual(S.parent_basis(0).shape[1], 4)        # hinge basis

    def test_additive_sees_nonlinear_parent(self):
        from v4.scores import DesignScore
        Z = data(1)
        lin, add = DesignScore(Z, "gauss"), DesignScore(Z, "additive")
        g_lin = lin.local_score(2, {0}) - lin.local_score(2, set())
        g_add = add.local_score(2, {0}) - add.local_score(2, set())
        self.assertLess(g_lin, 10)                              # y = x^2: almost no linear signal
        self.assertGreater(g_add, 100)

    def test_rff_df_is_a_trace(self):
        from v4.scores import DesignScore
        S = DesignScore(data(2), "rff")
        rss, df = S.rss_df(2, {0, 1})
        self.assertGreater(df, 1.0)
        self.assertLess(df, 2 + 40)
        self.assertGreater(rss, 0)

    def test_full_score_sums_local_scores(self):
        from v4.scores import DesignScore
        S = DesignScore(data(3), "additive")
        A = np.zeros((4, 4), int)
        A[0, 2] = A[1, 2] = A[2, 3] = 1
        want = S.local_score(0, set()) + S.local_score(1, set()) + S.local_score(2, {0, 1}) + S.local_score(3, {2})
        self.assertAlmostEqual(S.full_score(A), want)


def fam(prec, cov=0.55, ece=0.03, skel=0.6, false=10.0, tmf=0.1):
    return {"landmark": {"precision_half": prec, "coverage_half": cov, "ece": ece},
            "engine": {"ges_skeleton_f1": skel, "ges_false_adj": false, "true_dag_at_least_found_share": tmf}}


def dev(gains, sem_prec, form_prec):
    knobs = ("G0", "G1", "A1", "A2", "R1")
    F = {"semantic": {"knobs": {k: fam(sem_prec[k]) for k in knobs},
                      "paired_vs_G0": {k: {"precision_half": {"point": gains[k][0], "lo": gains[k][1]}} for k in knobs if k != "G0"},
                      "paired_vs_G1": {k: {"ges_skeleton_f1": {"point": 0.04}} for k in ("A1", "A2", "R1")}},
         "formula": {"knobs": {k: fam(form_prec[k]) for k in knobs}}}
    return {"families": F}


class DecideTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("v4dev", HERE / "v4" / "dev.py")
        self.D = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.D)
        self.pre = json.loads((HERE / "plans" / "v4_prereg.json").read_text())

    def test_winner_is_best_adoptable(self):
        g = {"G1": (0.0, -0.01), "A1": (0.03, 0.005), "A2": (0.05, 0.01), "R1": (0.04, -0.002)}
        sp = {"G0": 0.80, "G1": 0.80, "A1": 0.83, "A2": 0.85, "R1": 0.84}
        fp = {k: 0.89 for k in sp}
        out = self.D.decide(dev(g, sp, fp), self.pre)
        self.assertEqual(out["winner"], "A2")
        self.assertFalse(out["rows"]["R1"]["adoptable"])         # interval touches 0
        self.assertTrue(out["predictions"]["Q1"]["holds"])

    def test_formula_loss_blocks_and_none_is_reported(self):
        g = {"G1": (0.0, -0.01), "A1": (0.03, 0.005), "A2": (0.01, -0.01), "R1": (0.0, -0.02)}
        sp = {"G0": 0.80, "G1": 0.80, "A1": 0.83, "A2": 0.81, "R1": 0.80}
        fp = {"G0": 0.89, "G1": 0.89, "A1": 0.87, "A2": 0.89, "R1": 0.89}
        out = self.D.decide(dev(g, sp, fp), self.pre)
        self.assertFalse(out["rows"]["A1"]["eligible"])            # formula 0.02 below G0
        self.assertIsNone(out["winner"])
        self.assertIn("v3 stays", out["outcome"])


if __name__ == "__main__":
    unittest.main()
