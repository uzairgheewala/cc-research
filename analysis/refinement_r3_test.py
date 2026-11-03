"""Tests for refinement r3 (BLD-22): the sufficiency rule, its fork drop-in, and the branch files. No model call, NumPy only.

Tickets: BLD-22

    python analysis/refinement_r3_test.py --out DIR_OUTSIDE_THE_REPO      (writes DIR/refinement_r3_test.json)
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path[:0] = [str(ROOT.parent / "Causal-Copilot"), str(ROOT.parent / "Causal-Copilot" / "externals" / "causal-learn")]
import cc_graph as G  # noqa: E402
import refinement_r3 as R3  # noqa: E402
import refinement_v2 as V2  # noqa: E402

FORK = ROOT / "jobs" / "fork"
BRANCH = "bld-22-direction-sufficiency"


def dropin():
    spec = importlib.util.spec_from_file_location("bld22_dropin", FORK / "bld-22" / "refinement_v2_dropin.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def empty_boot(p):
    z = lambda: np.zeros((p, p))
    b = {k: z() for k in ("certain_edges", "uncertain_edges", "bi_edges", "half_certain_edges", "half_uncertain_edges", "none_edges")}
    b["none_existence"] = np.ones((p, p)) - np.eye(p)
    return b


def gas_void():
    """The q011 counts of the branch run (analysis/results/run_trace/q011_gas_void.json), on a two-variable table:
    a = gas (0), b = void (1); void -> gas 8, o-o 6, gas o-> void 4, gas -> void 1, bidirected 1; linked in 20 of 20."""
    b = empty_boot(2)
    b["certain_edges"][0, 1] = 8 / 20          # b->a  (void -> gas)
    b["certain_edges"][1, 0] = 1 / 20          # a->b  (gas -> void)
    b["none_edges"][0, 1] = b["none_edges"][1, 0] = 6 / 20
    b["half_certain_edges"][1, 0] = 4 / 20     # a o-> b
    b["bi_edges"][0, 1] = b["bi_edges"][1, 0] = 1 / 20
    b["none_existence"][:] = 0.0
    S0 = np.zeros((2, 2), dtype=int)
    S0[0, 1] = 6                                # the algorithm's own mark: o-o
    return S0, b


class Rule(unittest.TestCase):
    def test_k_min(self):
        self.assertEqual(R3.K_MIN, 15)
        self.assertLess(R3.wilson_lb(14, 20), 0.5)
        self.assertGreater(R3.wilson_lb(15, 20), 0.5)
        self.assertEqual(R3.k_min(10), 9)
        self.assertEqual(dropin().k_min(20), R3.K_MIN)

    def test_gas_void_synthetic(self):
        S0, b = gas_void()
        Vd, _ = V2.v2d(S0, b)
        self.assertEqual(G.pair_type(Vd, 0, 1), "b->a")          # the current rule: plurality 8 of 20 commits void -> gas
        R, _, gates = R3.r3s(S0, b)
        self.assertEqual(G.pair_type(R, 0, 1), "o-o")            # the sufficiency rule: linked, direction open
        self.assertEqual(gates[0]["k"], 8)

    def test_strong_arrow_kept(self):
        b = empty_boot(2)
        b["certain_edges"][1, 0] = 16 / 20
        b["uncertain_edges"][0, 1] = b["uncertain_edges"][1, 0] = 4 / 20
        b["none_existence"][:] = 0.0
        S0 = np.zeros((2, 2), dtype=int)
        S0[1, 0] = 1                                             # a -> b
        R, _, gates = R3.r3s(S0, b)
        self.assertEqual(G.pair_type(R, 0, 1), "a->b")
        b["certain_edges"][1, 0] = 14 / 20
        b["uncertain_edges"][0, 1] = b["uncertain_edges"][1, 0] = 6 / 20
        R, _, _ = R3.r3s(S0, b)
        self.assertEqual(G.pair_type(R, 0, 1), "undirected")      # no PAG mark anywhere: CPDAG-style open mark


class OnDevItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = R3.dev_items()
        cls.D = dropin()

    def test_only_removes_arrows_and_keeps_links(self):
        for it in self.items:
            Vd, _ = V2.v2d(it["S0"], it["boot"])
            R, _, _ = R3.r3s(it["S0"], it["boot"])
            for a, b in G.pairs(it["p"]):
                self.assertEqual(G.is_adjacent(Vd, a, b), G.is_adjacent(R, a, b), it["key"])
                t = G.pair_type(R, a, b)
                if t in ("a->b", "b->a"):
                    self.assertEqual(t, G.pair_type(Vd, a, b), it["key"])

    def test_fork_dropin_equals_analysis(self):
        os.environ.pop("CC_DIRECTION", None)
        for it in self.items:
            R, _, _ = R3.r3s(it["S0"], it["boot"])
            F, rec = self.D.refine(np.asarray(it["S0"]), it["boot"], ["v%d" % i for i in range(it["p"])], None, n_resamples=20)
            self.assertTrue(np.array_equal(R, F), it["key"])
            self.assertEqual(rec["refinement"], "r3s")
            Vd, _ = V2.v2d(it["S0"], it["boot"])
            self.assertTrue(np.array_equal(Vd, np.asarray(rec["v2d_graph"])), it["key"])
            P, rec2 = self.D.refine(np.asarray(it["S0"]), it["boot"], ["v%d" % i for i in range(it["p"])], None, n_resamples=20,
                                    direction="plurality")
            self.assertTrue(np.array_equal(Vd, P), it["key"])
            self.assertEqual(rec2["direction_gates"], [])

    def test_env_switch(self):
        it = self.items[0]
        os.environ["CC_DIRECTION"] = "plurality"
        try:
            P, rec = self.D.refine(np.asarray(it["S0"]), it["boot"], [], None)
            self.assertEqual(rec["direction_rule"], "plurality")
            os.environ["CC_DIRECTION"] = "bogus"
            with self.assertRaises(ValueError):
                self.D.refine(np.asarray(it["S0"]), it["boot"], [], None)
        finally:
            os.environ.pop("CC_DIRECTION", None)

    def test_names_part_sees_opened_pairs(self):
        """With a stand-in model that answers 'unknown', the names part changes nothing, and every opened pair is asked."""
        for it in self.items[:20]:
            asked = []

            def ask(prompt):
                asked.append(prompt)
                return {"direction": "unknown"}
            names = ["v%d" % i for i in range(it["p"])]
            V, rec = self.D.refine(np.asarray(it["S0"]), it["boot"], names, ask, n_resamples=20)
            R, _, gates = R3.r3s(it["S0"], it["boot"])
            self.assertTrue(np.array_equal(V, R), it["key"])
            n_askable = len(self.D.askable_pairs(R))
            self.assertEqual(len(asked), 3 * n_askable, it["key"])


class BranchFiles(unittest.TestCase):
    def test_spec_hashes(self):
        spec = json.loads((FORK / ("%s.json" % BRANCH)).read_text(encoding="utf-8"))
        h = lambda p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        self.assertEqual(spec["patch_sha256"], h(spec["patch"]))
        self.assertEqual(spec["manifest_sha256"], h(spec["manifest"]))
        man = dict(reversed(l.split("  ", 1)) for l in (ROOT / spec["manifest"]).read_text(encoding="utf-8").splitlines() if l)
        self.assertEqual(man["./postprocess/refinement_v2_dropin.py"], h("jobs/fork/bld-22/refinement_v2_dropin.py"))
        self.assertEqual(man["./postprocess/judge.py"], h("jobs/fork/bld-22/judge.py"))
        base = dict(reversed(l.split("  ", 1)) for l in (FORK / "bld-06-refinement-v2.sha256").read_text(encoding="utf-8").splitlines() if l)
        diff = sorted(k for k in set(man) | set(base) if man.get(k) != base.get(k))
        self.assertEqual(diff, ["./postprocess/judge.py", "./postprocess/refinement_v2_dropin.py"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a, rest = ap.parse_known_args()
    out = Path(a.out).resolve()
    if ROOT.resolve() in out.parents or out == ROOT.resolve():
        sys.exit("--out must be outside the repository")
    out.mkdir(parents=True, exist_ok=True)
    res = unittest.main(argv=[sys.argv[0]] + rest, exit=False, verbosity=2).result
    summ = {"tickets": ["BLD-22"], "ran": res.testsRun, "failures": len(res.failures), "errors": len(res.errors),
            "ok": res.wasSuccessful(), "rule_file_sha256": hashlib.sha256((HERE / "refinement_r3.py").read_bytes()).hexdigest()}
    (out / "refinement_r3_test.json").write_text(json.dumps(summ, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summ))
    sys.exit(0 if res.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
