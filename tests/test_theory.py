"""Hand-checkable cases for the AB-09 theory pack (AUD-40): T1 (F1 = S x a and its corrected forms), T2 (three-term
budget), T3 (bounded harm of orientation-only knowledge), plus the T4 worked example and the T5 counterexample.
The numbers in each docstring can be checked on paper."""
import itertools, random, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
import theory_checks as TC  # noqa: E402

TC._import_cc(TC.DEF_CC)
try:
    import cc_graph as G  # noqa: E402
except ImportError:      # the graph helpers live in the cc-research tree
    G = None


def F(*pairs):
    return {frozenset(p) for p in pairs}


class T1Identity(unittest.TestCase):
    def test_worked_example(self):
        """Truth 0->1->2. Predicted: 1->0 (true pair, reversed), 1-2 undecided, 0->2 (false pair).
        nP = 3, nT = 2, TP_adj = 2: S = 4/5. right 0, wrong 1, undecided 1: a = (0 + 1/2)/2 = 1/4.
        Coin: TP_dir is 0 or 1 with prob 1/2 each, 3 arrows predicted: F1 is 0 or 2/5, mean 1/5 = S a."""
        T = {(0, 1), (1, 2)}
        D, U = {(1, 0), (0, 2)}, F((1, 2))
        k = TC.coords(D, U, T)
        self.assertAlmostEqual(k["S"], 0.8, places=15)
        self.assertAlmostEqual(k["a"], 0.25, places=15)
        self.assertAlmostEqual(k["a"], k["a_cq"], places=15)     # c = 1/2, q = 0: a = 0 + 1/4
        m, var, support = TC.expected_f1(D, U, T)
        self.assertAlmostEqual(m, 0.2, places=15)
        self.assertAlmostEqual(var, 0.04, places=15)
        self.assertEqual(support, [0.0, 0.4])

    def test_other_rules_closed_form(self):
        """Same graph. "both": 4 arrows, TP_dir 1: F1 = 2/6 = 1/3 = S (1/2)(5/6). "drop": 2 arrows, TP_dir 0: F1 = 0.
        "lower": 1-2 becomes 1->2 (true): TP_dir 1, 3 arrows: F1 = 2/5."""
        T = {(0, 1), (1, 2)}
        D, U = {(1, 0), (0, 2)}, F((1, 2))
        self.assertAlmostEqual(TC.rule_f1_closed_form("both", D, U, T), 1 / 3, places=15)
        self.assertAlmostEqual(TC.rule_f1_closed_form("drop", D, U, T), 0.0, places=15)
        self.assertAlmostEqual(TC.rule_f1_closed_form("lower", D, U, T), 0.4, places=15)
        # "lower" read in a layout where column 2 comes before column 1: 2->1 is wrong, F1 = 0
        self.assertAlmostEqual(TC.rule_f1_closed_form("lower", D, U, T, pos={0: 0, 1: 2, 2: 1}), 0.0, places=15)

    def test_condition_violated_is_flagged(self):
        """A pair both committed and listed undecided: the coin can add a second arrow, so the denominator moves.
        Truth 0->1, D = {0->1}, U = {0-1}: F1 is 1 or 2/3, mean 5/6, while the naive a = 3/2 > 1."""
        T, D, U = {(0, 1)}, {(0, 1)}, F((0, 1))
        k = TC.coords(D, U, T)
        self.assertFalse(k["one_arrow_per_pair"])
        m, _, _ = TC.expected_f1(D, U, T)
        self.assertAlmostEqual(m, 5 / 6, places=15)
        self.assertNotAlmostEqual(m, k["S"] * k["a"], places=6)

    def test_random_graphs(self):
        rng = random.Random(7)
        for _ in range(300):
            n = rng.randint(3, 7)
            order = list(range(n))
            rng.shuffle(order)
            T = {(order[i], order[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.4}
            if not T:
                continue
            D, U = set(), set()
            for x, y in itertools.combinations(range(n), 2):
                r = rng.random()
                if r < 0.25:
                    D.add((x, y))
                elif r < 0.5:
                    D.add((y, x))
                elif r < 0.7:
                    U.add(frozenset((x, y)))
            m, _, _ = TC.expected_f1(D, U, T)
            k = TC.coords(D, U, T)
            self.assertLess(abs(m - k["S"] * k["a"]), 1e-12)


@unittest.skipIf(G is None, "cc_graph not found")
class T2Budget(unittest.TestCase):
    def test_chain_all_right(self):
        """Truth 0->1->2: the CPDAG leaves both undecided, a_C = 1/2, I = 1/2. A method that commits both right has
        F1 = 1: K = 1/2 - 2(1/2 + 1/2)/4 = 0 and O = (2/4)(-1/2 - 1/2) = -1/2 (it beat the class by luck or form)."""
        T = {(0, 1), (1, 2)}
        cd, cu = TC.cpdag_parts(T, 3, G)
        b = TC.budget({(0, 1), (1, 2)}, set(), T, cd, cu)
        self.assertAlmostEqual(b["I"], 0.5, places=15)
        self.assertAlmostEqual(b["K"], 0.0, places=15)
        self.assertAlmostEqual(b["O"], -0.5, places=15)
        self.assertAlmostEqual(b["I"] + b["K"] + b["O"], 0.0, places=15)

    def test_collider_half_found(self):
        """Truth 0->2<-1 (both compelled): I = 0. Method finds only 0-2, undecided: S = 2/3, a = 1/2, F1 = 1/3.
        K = 1 - 2(1)/3 = 1/3; O = (2/3)(1/2) = 1/3 (abstained on a compelled edge). Sum 2/3 = 1 - F1."""
        T = {(0, 2), (1, 2)}
        cd, cu = TC.cpdag_parts(T, 3, G)
        b = TC.budget(set(), F((0, 2)), T, cd, cu)
        self.assertAlmostEqual(b["I"], 0.0, places=15)
        self.assertAlmostEqual(b["K"], 1 / 3, places=15)
        self.assertAlmostEqual(b["O"], 1 / 3, places=15)
        self.assertAlmostEqual(b["O_abstain_compelled"], 1 / 3, places=15)

    def test_sum_and_K_nonnegative_random(self):
        rng = random.Random(11)
        for _ in range(300):
            n = rng.randint(3, 7)
            T = {(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.4}
            if not T:
                continue
            cd, cu = TC.cpdag_parts(T, n, G)
            D, U = set(), set()
            for x, y in itertools.combinations(range(n), 2):
                r = rng.random()
                if r < 0.3:
                    D.add((x, y) if rng.random() < 0.5 else (y, x))
                elif r < 0.5:
                    U.add(frozenset((x, y)))
            b = TC.budget(D, U, T, cd, cu)
            m, _, _ = TC.expected_f1(D, U, T)
            self.assertLess(abs(b["I"] + b["K"] + b["O"] - (1 - m)), 1e-12)
            self.assertGreaterEqual(b["K"], -1e-12)          # lemma in the report: K >= 0
            self.assertGreaterEqual(b["I"], -1e-12)


class T3BoundedHarm(unittest.TestCase):
    def test_bound_and_identity(self):
        """Truth 0->1->2->3. Data-only: 0->1, 1->2 (right), 2-3 undecided, 0-3 undecided (false pair).
        nP = 4, nT = 3, N = 7, E[TP_dir] = 2.5, F1_0 = 5/7. Wrong knowledge sets 1->0 and 3->2 (k = 2): credits
        lost 1 + 1/2, so harm = 2(3/2)/7 = 3/7 (F1 = 2/7), equal to the exact bound; the k-bound is 2 min(2,3)/7 = 4/7."""
        T = {(0, 1), (1, 2), (2, 3)}
        D, U = {(0, 1), (1, 2)}, F((2, 3), (0, 3))
        f0, _, _ = TC.expected_f1(D, U, T)
        self.assertAlmostEqual(f0, 5 / 7, places=15)
        D2, U2, dec = TC.apply_orientations(D, U, {frozenset((0, 1)): (1, 0), frozenset((2, 3)): (3, 2)})
        f1, _, _ = TC.expected_f1(D2, U2, T)
        hb = TC.harm_bounds(D, U, T, dec)
        self.assertAlmostEqual(f1, 2 / 7, places=15)
        self.assertAlmostEqual(hb["bound_exact"], 3 / 7, places=15)
        self.assertAlmostEqual(hb["bound_k"], 4 / 7, places=15)
        self.assertAlmostEqual(f0 - f1, hb["bound_exact"], places=15)

    def test_k_bound_attained(self):
        """Tight case for the k-bound: data-only gets all three edges right with no false pair (N = 6, F1 = 1);
        knowledge reverses two of them: F1 = 2/6, harm 2/3 = 2 min(k, TP_adj)/N with k = 2."""
        T = {(0, 1), (1, 2), (2, 3)}
        D = set(T)
        D2, U2, dec = TC.apply_orientations(D, set(), {frozenset((0, 1)): (1, 0), frozenset((1, 2)): (2, 1)})
        f0, _, _ = TC.expected_f1(D, set(), T)
        f1, _, _ = TC.expected_f1(D2, U2, T)
        hb = TC.harm_bounds(D, set(), T, dec)
        self.assertAlmostEqual(f0 - f1, 2 / 3, places=15)
        self.assertAlmostEqual(hb["bound_k"], 2 / 3, places=15)

    def test_knowledge_cannot_connect(self):
        with self.assertRaises(ValueError):
            TC.apply_orientations({(0, 1)}, set(), {frozenset((1, 2)): (1, 2)})

    def test_edge_adding_contrast(self):
        """Same perfect graph (F1 = 1, N = 6). Adding m false arrows touches pairs with zero credit, yet
        F1 = 6/(6 + m): harm m/(6 + m), e.g. 1/2 at m = 6, tending to all of F1_0."""
        T = {(0, 1), (1, 2), (2, 3)}
        D = set(T) | {(0, 2), (0, 3), (1, 3), (4, 0), (4, 1), (4, 2)}
        f, _, _ = TC.expected_f1(D, set(), T)
        self.assertAlmostEqual(f, 0.5, places=15)

    def test_random_tiers_never_exceed_bound(self):
        rng = random.Random(3)
        for _ in range(300):
            n = rng.randint(3, 7)
            T = {(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.4}
            if not T:
                continue
            D, U = set(), set()
            for x, y in itertools.combinations(range(n), 2):
                r = rng.random()
                if r < 0.3:
                    D.add((x, y) if rng.random() < 0.5 else (y, x))
                elif r < 0.5:
                    U.add(frozenset((x, y)))
            tier = {v: rng.randint(0, 2) for v in range(n)}
            D2, U2, dec = TC.apply_orientations(D, U, TC.tier_decisions(D, U, tier))
            f0, _, _ = TC.expected_f1(D, U, T)
            f1, _, _ = TC.expected_f1(D2, U2, T)
            hb = TC.harm_bounds(D, U, T, dec)
            self.assertGreaterEqual(f1 - f0, -hb["bound_exact"] - 1e-12)
            self.assertLessEqual(f1 - f0, hb["gain_bound_exact"] + 1e-12)
            self.assertLessEqual(hb["bound_exact"], hb["bound_k"] + 1e-12)


class T4WorkedExample(unittest.TestCase):
    def setUp(self):
        try:
            TC.toy_pc(["a", "b", "c", "d"], 0, 2)
        except ImportError:
            self.skipTest("causal-learn 0.1.4.8 not found")

    def test_priority2_errs_in_causal_order_only(self):
        self.assertEqual(TC.toy_pc(["a", "b", "c", "d"], 0, 2), ["a->b", "c->b", "c-d"])   # c->b wrong
        self.assertEqual(TC.toy_pc(["d", "c", "b", "a"], 0, 2), ["a-b", "b->c", "d->c"])   # the true CPDAG

    def test_maxp_is_right_in_both_orders(self):
        for order in (["a", "b", "c", "d"], ["d", "c", "b", "a"]):
            self.assertEqual(TC.toy_pc(order, 1, 3), ["a-b", "b->c", "d->c"])

    def test_uc_model_priorities(self):
        """Claims (0,1,2) at 1 and (1,2,3) at 2 conflict on 1-2. Priority 2 keeps the first (2->1); 0 keeps the last."""
        UT = [(0, 1, 2), (1, 2, 3)]
        claims = set(UT)
        self.assertEqual(TC.uc_model(UT, claims, 2)[frozenset((1, 2))], (2, 1))
        self.assertEqual(TC.uc_model(UT, claims, 0)[frozenset((1, 2))], (1, 2))


@unittest.skipIf(G is None, "cc_graph not found")
class T5Ceiling(unittest.TestCase):
    def test_definite_cause_without_directed_path(self):
        """Truth T->A->Y<-B<-T (T=0, A=1, B=2, Y=3). CPDAG: T-A, T-B undirected; A->Y<-B compelled. The class has 3
        DAGs (A->T<-B would add a v-structure); Y is a descendant of T in all of them, but the CPDAG has no directed
        path T => Y, so the directed-path rule abstains on a pair whose answer is constant ("yes")."""
        T = {(0, 1), (0, 2), (1, 3), (2, 3)}
        cd, cu = TC.cpdag_parts(T, 4, G)
        self.assertEqual(cd, {(1, 3), (2, 3)})
        self.assertEqual(cu, {frozenset((0, 1)), frozenset((0, 2))})
        comps = TC.chain_component_orientations(4, cu, {frozenset(e) for e in T})
        members = [list(cd) + [a for part in combo for a in part] for combo in itertools.product(*comps)]
        self.assertEqual(len(members), 3)
        self.assertTrue(all(TC.reach_matrix(4, m)[0, 3] for m in members))
        self.assertEqual(TC.cpdag_claims(4, cd, cu, [0])[(0, 3)], "abstain")

    def test_claims_sound(self):
        """Truth 0->1<-2, 1->3: everything compelled; from 0: 1 and 3 are 'yes', 2 is 'no'."""
        T = {(0, 1), (2, 1), (1, 3)}
        cd, cu = TC.cpdag_parts(T, 4, G)
        cl = TC.cpdag_claims(4, cd, cu, [0])
        self.assertEqual(cl, {(0, 1): "yes", (0, 2): "no", (0, 3): "yes"})


if __name__ == "__main__":
    unittest.main()
