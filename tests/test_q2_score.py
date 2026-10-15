"""Scorer v2 (D0.4): agrees with the audit chapter's scorer functions on random graphs (B0)."""
import random, sys, unittest, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))
from score import calib, dv, graph, paired, rca  # noqa: E402
import causalarena_io as CA  # noqa: E402
import cc_graph as CG  # noqa: E402
import itertools  # noqa: E402


def rand_graph(rng, n):
    D, U, T = set(), set(), set()
    for a, b in itertools.combinations(range(n), 2):
        r = rng.random()
        if r < 0.15:
            D.add((a, b) if rng.random() < 0.5 else (b, a))
        elif r < 0.25:
            U.add((a, b))
        if rng.random() < 0.2:
            T.add((a, b))
    return D, U, T


class Score(unittest.TestCase):
    def test_f1_matches_audit_scorer(self):
        rng = random.Random(1)
        for k in range(200):
            n = rng.randint(3, 12)
            D, U, T = rand_graph(rng, n)
            seed = zlib.crc32(("f%d" % k).encode())
            mine = graph.directed_f1(D, U, T, seed)
            ref = CA.directed_scores(D, {frozenset(u) for u in U}, T, n, "random", seed=seed)
            self.assertAlmostEqual(mine["f1"], ref["f1"], places=12)
            self.assertAlmostEqual(mine["precision"], ref["precision"], places=12)

    def test_cpdag_matches_audit_cpdag(self):
        rng = random.Random(2)
        for k in range(150):
            n = rng.randint(3, 10)
            order = list(range(n))
            rng.shuffle(order)
            T = {(order[i], order[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3}
            D, U = graph.cpdag(T, n)
            C = CG.cpdag_of(T, n)
            for a, b in itertools.combinations(range(n), 2):
                t = CG.pair_type(C, a, b)
                mine = "a->b" if (a, b) in D else "b->a" if (b, a) in D else "undirected" if (a, b) in U else "none"
                self.assertEqual(mine, t if t in ("a->b", "b->a", "none") else "undirected", (T, a, b))

    def test_dv1_claims(self):
        cl = dv.claims(3, {(0, 1)}, {(1, 2)}, [0])
        self.assertEqual(cl, {(0, 1): True})                       # 0 -> 1 definite; 2 only possibly reachable: abstain
        cl = dv.claims(3, set(), set(), [0])
        self.assertEqual(cl, {(0, 1): False, (0, 2): False})

    def test_ece_and_selective(self):
        probs = [0.9] * 10 + [0.1] * 10
        hits = [1] * 9 + [0] + [0] * 9 + [1]
        self.assertAlmostEqual(calib.ece(probs, hits), 0.0, places=12)
        cvr = calib.claimed_vs_realised(probs, hits, 0.5)
        self.assertEqual(cvr["kept"], 10)
        self.assertAlmostEqual(cvr["realised"], 0.9)
        s = dv.selective([(0.9, 1), (0.8, 1), (0.2, 0), (0.1, 1)], coverage_target=0.5)
        self.assertEqual(s["kept"], 2)
        self.assertEqual(s["precision"], 1.0)

    def test_paired_bootstrap_deterministic(self):
        by = {"s%d" % i: [0.01 * i, 0.02] for i in range(10)}
        a, b = paired.cluster_bootstrap(by), paired.cluster_bootstrap(by)
        self.assertEqual(a, b)
        self.assertLessEqual(a["lo"], a["point"])
        self.assertLessEqual(a["point"], a["hi"])

    def test_ac_at_k(self):
        r = rca.ac_at_k([{"ranking": ["a", "b"], "root": "b"}, {"ranking": None, "root": "c"}, {"ranking": ["c"], "root": "d"}], 2)
        self.assertEqual((r["answered"], r["ac"], r["coverage"]), (2, 0.5, 2 / 3))


if __name__ == "__main__":
    unittest.main()
