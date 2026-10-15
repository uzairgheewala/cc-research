"""Kernel (B1): re-derivation from recorded tests, combination rules, the v0.2 ledger, K7 checker and verify02, all
without causal-learn (a d-separation oracle stands in for the data)."""
import copy, sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import q2_oracle as O  # noqa: E402
from engines import core  # noqa: E402
from kernel import build as B, checker, derive, policy, views  # noqa: E402
import verify02  # noqa: E402


def oracle_ledger(p, seed, rule="pc"):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((50, p))
    names = ["v%02d" % j for j in range(p)]
    _, order = B.variables(X, names)
    edges = O.random_dag(p, seed)                       # over canonical indices
    log = O.pc_log(p, O.oracle(edges, p))
    eng = O.fake_engines(X, names, log=log)
    led, info = B.build(X, names, rule=rule, eng=eng, created_utc="")
    return led, info, edges, order, names


class Derive(unittest.TestCase):
    def test_oracle_rederivation_is_true_cpdag(self):
        for k in range(40):
            p = (5, 6, 8, 10)[k % 4]
            edges = O.random_dag(p, 100 + k)
            log = O.pc_log(p, O.oracle(edges, p))
            d = derive.pc_maxp_from_tests(p, log)
            D, U = core.marks_to_sets(d["final"])
            Dt, Ut = O.true_cpdag(edges, p)
            self.assertEqual((D, {tuple(sorted(u)) for u in U}), (Dt, {tuple(sorted(u)) for u in Ut}), (p, edges))
            self.assertEqual(d["missing_tests"], [])

    def test_missing_test_is_reported(self):
        p = 6
        edges = [(0, 2), (1, 2), (2, 3), (3, 4)]
        log = O.pc_log(p, O.oracle(edges, p))
        log = [t for t in log if t[0] != "maxp"]
        d = derive.pc_maxp_from_tests(p, log)
        self.assertTrue(d["missing_tests"] or not [t for t in derive.unshielded_triples(d["skeleton"])])


class Policy(unittest.TestCase):
    def setUp(self):
        self.pc = {"D": {(0, 1)}, "U": {(1, 2)}, "labels": {(0, 1): ("v_structure", [])}}
        self.ges = {"D": {(1, 0), (2, 1)}, "U": {(2, 3)}, "labels": {}}

    def test_c1_c2_conflict_open(self):
        d1, _ = policy.decide("C1", 4, self.pc, self.ges)
        self.assertEqual(d1[(0, 1)].relation, "a-b")
        self.assertTrue(d1[(0, 1)].conflict)
        self.assertEqual(d1[(2, 3)].relation, "none")
        d2, _ = policy.decide("C2", 4, self.pc, self.ges)
        self.assertEqual(d2[(0, 1)].relation, "a-b")
        self.assertEqual(d2[(1, 2)].relation, "b->a")      # GES commits 2 -> 1, PC undirected
        self.assertEqual(d2[(2, 3)].relation, "a-b")

    def test_c3_follows_ges_skeleton_and_opens_conflicts(self):
        ges = {"D": {(0, 2), (1, 2), (2, 3)}, "U": set(), "labels": {}}      # 0 -> 2 <- 1 collider, then 2 -> 3 by R1
        pc = {"D": {(2, 0)}, "U": {(1, 2)}, "labels": {}}
        d, _ = policy.decide("C3", 4, pc, ges)
        self.assertEqual(d[(0, 2)].relation, "a-b")       # contradicted
        self.assertTrue(d[(0, 2)].conflict)
        self.assertEqual(d[(1, 2)].relation, "a-b")       # its collider partner lost its licence
        self.assertEqual(d[(2, 3)].relation, "a-b")       # R1 premise gone
        self.assertEqual(d[(0, 1)].relation, "none")

    def test_fallback_without_ges(self):
        d, fb = policy.decide("C3", 3, self.pc, None)
        self.assertTrue(fb)
        self.assertEqual(d[(0, 1)].relation, "a->b")


class Ledger(unittest.TestCase):
    def test_oracle_ledger_is_true_cpdag_and_verifies(self):
        for k in range(12):
            p = (5, 7, 9)[k % 3]
            led, info, edges, order, names = oracle_ledger(p, 300 + k)
            res = verify02.verify(led)
            self.assertEqual({kk: v for kk, v in res.items() if v}, {}, k)
            self.assertTrue(checker.check(led)["ok"], checker.check(led)["errors"])
            Dt, Ut = O.true_cpdag(edges, p)                 # canonical indices -> original positions
            want_D = {(order[a], order[b]) for a, b in Dt}
            want_U = {tuple(sorted((order[a], order[b]))) for a, b in Ut}
            D, U = views.graph_sets(led)
            self.assertEqual((D, U), (want_D, want_U))

    def test_column_order_does_not_reach_the_claims(self):
        p = 7
        rng = np.random.default_rng(5)
        X = rng.standard_normal((40, p))
        names = ["v%d" % j for j in range(p)]
        edges = O.random_dag(p, 77)
        log = O.pc_log(p, O.oracle(edges, p))
        base, _ = B.build(X, names, rule="pc", eng=O.fake_engines(X, names, log=log), created_utc="")
        for perm in ([6, 5, 4, 3, 2, 1, 0], [2, 0, 6, 1, 5, 3, 4]):
            Xp = X[:, perm]
            led, _ = B.build(Xp, [names[j] for j in perm], rule="pc", eng=O.fake_engines(Xp, [names[j] for j in perm], log=log), created_utc="")
            self.assertEqual(led["claims"], base["claims"])
            self.assertEqual(led["evidence"], base["evidence"])
            self.assertEqual(led["report"]["permutation_check"]["identical"], True)

    def test_duplicate_columns_do_not_depend_on_order(self):
        p = 6
        rng = np.random.default_rng(9)
        X = rng.standard_normal((40, p))
        X[:, 4] = X[:, 1]                                  # an exact duplicate column
        names = ["v%d" % j for j in range(p)]
        log = O.pc_log(p, O.oracle(O.random_dag(p, 5), p))
        base, _ = B.build(X, names, rule="pc", eng=O.fake_engines(X, names, log=log), created_utc="")
        perm = [4, 3, 5, 0, 2, 1]
        Xp, Np = X[:, perm], [names[j] for j in perm]
        led, _ = B.build(Xp, Np, rule="pc", eng=O.fake_engines(Xp, Np, log=log), created_utc="")
        self.assertEqual(led["claims"], base["claims"])
        self.assertTrue(led["report"]["permutation_check"]["identical"])
        self.assertEqual(len({e["id"] for e in led["evidence"]}), len(led["evidence"]))

    def test_same_input_same_hash(self):
        a, _, _, _, _ = oracle_ledger(8, 11)
        b, _, _, _, _ = oracle_ledger(8, 11)
        self.assertEqual(a["report"]["ledger_sha256"], b["report"]["ledger_sha256"])

    def test_mutation_one_evidence_record_removed_is_rejected(self):
        led, *_ = oracle_ledger(8, 21)
        cited = sorted({e for c in led["claims"] for e in c["evidence"]})
        for eid in cited[:: max(1, len(cited) // 15)]:
            m = copy.deepcopy(led)
            m["evidence"] = [e for e in m["evidence"] if e["id"] != eid]
            failing = {k for k, v in verify02.verify(m).items() if v}
            self.assertTrue(failing - {"V6 hash (I2)"} or not checker.check(m)["ok"], eid)
            self.assertIn("V2 evidence closure (I4)", failing)

    def test_mutation_uncited_test_removed_is_caught_by_checker(self):
        """A separating test no claim cites is still load-bearing when it is the only one for its pair: the checker's
        re-derivation then keeps the pair adjacent and disagrees with the recorded engine output."""
        for seed in range(23, 40):
            led, *_ = oracle_ledger(9, seed)
            cited = {e for c in led["claims"] for e in c["evidence"]}
            sep = {}
            for e in led["evidence"]:
                if e["type"] == "ci_test" and "skeleton" in e["phases"] and e["p_value"] > 0.05:
                    sep.setdefault(frozenset(e["variables"]), []).append(e["id"])
            only = [ids[0] for ids in sep.values() if len(ids) == 1 and ids[0] not in cited]
            alone = [ids for ids in sep.values() if len(ids) == 1]
            if alone:
                eid = alone[0][0]
                m = copy.deepcopy(led)
                m["evidence"] = [e for e in m["evidence"] if e["id"] != eid]
                m["report"]["ledger_sha256"] = verify02.canonical_hash(m)
                self.assertFalse(checker.check(m)["ok"])
                return
        self.skipTest("no pair with a single separating test in these draws")


class LedgerV02Fields(unittest.TestCase):
    def setUp(self):
        self.led, *_ = oracle_ledger(6, 41)

    def _fails(self, led, name):
        led["report"]["ledger_sha256"] = verify02.canonical_hash(led)
        self.assertIn(name, {k for k, v in verify02.verify(led).items() if v})

    def test_v9_missing_plan_hash(self):
        led = copy.deepcopy(self.led)
        led["report"]["plan"] = {"prereg": "x"}
        self._fails(led, "V9 plan, assumptions, lineage, question")

    def test_v9_empty_assumptions(self):
        led = copy.deepcopy(self.led)
        led["report"]["assumptions"] = []
        self._fails(led, "V9 plan, assumptions, lineage, question")

    def test_v10_missing_pair(self):
        led = copy.deepcopy(self.led)
        led["claims"] = led["claims"][1:]
        self._fails(led, "V10 one claim per pair")

    def test_v11_convention(self):
        led = copy.deepcopy(self.led)
        led["report"]["orientation_convention"] = "rows are causes"
        self._fails(led, "V11 orientation convention")

    def test_v12_required_edge_on_unconnected_pair(self):
        led = copy.deepcopy(self.led)
        none = next(c for c in led["claims"] if c["data_only_relation"] == "none")
        led["knowledge"] = [{"id": "k1", "kind": "required_edge", "content": {"from": none["x"], "to": none["y"]},
                             "supplier": {"type": "person"}}]
        self._fails(led, "V12 required edges on unconnected pairs")

    def test_checks_run_even_when_v1_fails(self):
        led = copy.deepcopy(self.led)
        del led["claims"][0]["engines"]
        res = verify02.verify(led)
        self.assertTrue(res["V1 schema"])
        self.assertIn("V6 hash (I2)", res)
        self.assertNotIn("could not run", " ".join(res["V2 evidence closure (I4)"]))


if __name__ == "__main__":
    unittest.main()


class CycleGuard(unittest.TestCase):
    def test_open_cycles(self):
        D = {(0, 1), (1, 2), (2, 0), (3, 0), (2, 4)}
        D2, U2, opened = policy.open_cycles(D, set())
        self.assertEqual(D2, {(3, 0), (2, 4)})
        self.assertEqual(set(opened), {(0, 1), (1, 2), (0, 2)})
        self.assertEqual(U2, {(0, 1), (1, 2), (0, 2)})

    def test_guard_on_rule_decisions(self):
        dec = {(0, 1): policy.Decision("a->b", "pc", "v_structure"), (1, 2): policy.Decision("a->b", "ges", "score_search"),
               (0, 2): policy.Decision("b->a", "both", "meek_r1"), (2, 3): policy.Decision("a->b", "pc", "v_structure")}
        dec, opened = policy.guard(dec, 4)
        self.assertEqual(sorted(opened), [(0, 1), (0, 2), (1, 2)])
        self.assertTrue(all(dec[k].relation == "a-b" and dec[k].conflict for k in opened))
        self.assertEqual(dec[(2, 3)].relation, "a->b")


class EngineDivergence(unittest.TestCase):
    def test_divergent_engine_meek_is_recorded_not_fatal(self):
        p = 7
        X = np.random.default_rng(12).standard_normal((50, p))
        names = ["v%d" % j for j in range(p)]
        log = O.pc_log(p, O.oracle([(0, 2), (1, 2), (2, 3), (3, 4), (5, 6)], p))
        eng = O.fake_engines(X, names, log=log)
        M = eng["pc"].marks.copy()
        a, b = 2, 3                                   # flip one Meek orientation in the "engine" output
        M[a, b], M[b, a] = M[b, a], M[a, b]
        eng["pc"].marks = M
        led, info = B.build(X, names, rule="pc", eng=eng, created_utc="")
        types = [d["type"] for d in led["report"]["engine_outputs"]["pc"]["defects"]]
        self.assertIn("engine_meek_divergence", types)
        self.assertEqual({k for k, v in verify02.verify(led).items() if v}, set())
        self.assertTrue(checker.check(led)["ok"], checker.check(led)["errors"])
