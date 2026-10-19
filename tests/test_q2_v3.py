"""Kernel v3 pure parts (NumPy only): the direction view, decision weights, knowledge propagation leaves a ledger with no
knowledge unchanged, claim features, and the half-coverage statistic."""
import sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import q2_oracle as O  # noqa: E402
from kernel import build as B, claim_features as CF, experiment, views, weights  # noqa: E402
from score import dv  # noqa: E402


def ledger(p=8, seed=11):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((50, p))
    names = ["v%02d" % j for j in range(p)]
    edges = O.random_dag(p, seed)
    eng = O.fake_engines(X, names, log=O.pc_log(p, O.oracle(edges, p)))
    led, _ = B.build(X, names, rule="pc", eng=eng, created_utc="")
    return led


class DirectionView(unittest.TestCase):
    def test_open_classes_become_undirected_and_nothing_else_changes(self):
        for seed in range(6):
            led = ledger(seed=seed)
            D, U = views.graph_sets(led)
            D2, U2 = experiment.configure(led, ("meek_r1", "meek_r3"))
            pos = {v["name"]: v["position"] for v in led["variables"]}
            r1 = {(pos[c["x"]], pos[c["y"]]) for c in led["claims"] if c["relation"] == "x->y" and c["licensed_by"] in ("meek_r1", "meek_r3")}
            self.assertEqual(D2, D - r1)
            self.assertEqual(U2, set(U) | {tuple(sorted(e)) for e in r1})
            adj = lambda D_, U_: {frozenset(e) for e in D_} | {frozenset(u) for u in U_}  # noqa: E731
            self.assertEqual(adj(D, U), adj(D2, U2))           # the skeleton never changes

    def test_empty_open_set_is_the_identity(self):
        led = ledger()
        self.assertEqual(experiment.configure(led, ()), views.graph_sets(led))


class Weights(unittest.TestCase):
    def test_weights_are_nonnegative_and_cover_every_open_pair(self):
        for seed in range(6):
            led = ledger(seed=seed)
            D, U = views.graph_sets(led)
            n = len(led["variables"])
            W = weights.decision_weights(n, D, U, list(range(n)))
            self.assertEqual(set(W), set(U))
            for w in W.values():
                self.assertGreaterEqual(w["weight"], 0.0)
                self.assertTrue(all(s >= 0 for s in w["settle"]))

    def test_propagation_with_no_knowledge_leaves_the_ledger_unchanged(self):
        led = ledger()
        stmts = {"p0": None, "p1": None, "p2": None}
        led_k, info = weights.apply_tiers_propagating(led, stmts)
        self.assertEqual([(c["x"], c["y"], c["relation"]) for c in led_k["claims"]], [(c["x"], c["y"], c["relation"]) for c in led["claims"]])
        self.assertEqual(info["propagated"], [])


class Features(unittest.TestCase):
    def test_one_vector_per_answer_with_the_documented_length(self):
        led = ledger()
        D, U = views.graph_sets(led)
        n = len(led["variables"])
        cl = dv.claims(n, D, U, list(range(n)))
        F = CF.features(led, list(range(n)), cl)
        self.assertEqual(set(F), set(cl))
        self.assertTrue(all(len(v) == len(CF.NAMES) for v in F.values()))
        self.assertTrue(all(v[0] == (1.0 if cl[k] else 0.0) for k, v in F.items()))


class Half(unittest.TestCase):
    def test_half_coverage_keeps_ties_together(self):
        from kernel.v3 import half
        groups = [(10, [(0.9, True), (0.9, False), (0.9, True), (0.5, True), (0.4, False)])]
        p, c = half(groups)                                  # half of 10 pairs = 5 answers: all five are kept
        self.assertAlmostEqual(c, 0.5)
        self.assertAlmostEqual(p, 0.6)
        groups = [(6, [(0.9, True), (0.8, True), (0.8, False), (0.8, False), (0.1, True)])]
        p, c = half(groups)                                  # 3 needed; the 0.8 tie (3 answers) is kept whole: 4 kept
        self.assertAlmostEqual(c, 4 / 6)
        self.assertAlmostEqual(p, 0.5)


if __name__ == "__main__":
    unittest.main()
