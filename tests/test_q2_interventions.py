"""B2.1: constructed intervention-versus-knowledge and intervention-versus-data conflicts are resolved for the
intervention and recorded (I6); intervention orientations never add or remove a connection."""
import copy, sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kernel import build as B, checker, interventions as I, knowledge as K  # noqa: E402
import q2_oracle as O  # noqa: E402
import verify02  # noqa: E402

NAMES = ["a", "b", "c", "d", "e", "f"]


def ledger(edges):
    p = len(NAMES)
    X = np.random.default_rng(4).standard_normal((60, p))
    log = O.pc_log(p, O.oracle(edges, p))
    led, _ = B.build(X, NAMES, rule="pc", eng=O.fake_engines(X, NAMES, log=log), created_utc="")
    return led


def shift(t, y, moves=True):
    return {"id": "i:%s>%s" % (t, y), "type": "intervention_shift", "variables": [t, y], "conditioning": [], "statistic": 5.0 if moves else 0.1,
            "p_value": 1e-6 if moves else 0.9, "supports": "x->y" if moves else "none"}


def claim(led, u, v):
    return next(c for c in led["claims"] if {c["x"], c["y"]} == {u, v})


def ok(led):
    return {k for k, v in verify02.verify(led).items() if v} == set()


class Interventions(unittest.TestCase):
    def setUp(self):
        self.led = ledger([(0, 1), (2, 3)])                     # canonical 0 - 1 and 2 - 3: both open in the CPDAG
        self.pair = [(c["x"], c["y"]) for c in self.led["claims"] if c["relation"] == "x-y"][0]

    def test_shift_orients_open_pair(self):
        u, v = self.pair
        led, info = I.apply_interventions(self.led, [shift(v, u)])
        c = claim(led, u, v)
        self.assertEqual((c["x"], c["y"], c["relation"], c["direction_source"], c["licensed_by"]), (v, u, "x->y", "intervention", "i_essential"))
        self.assertTrue(ok(led))
        self.assertTrue(checker.check(led)["ok"], checker.check(led)["errors"])
        self.assertEqual(led["report"]["regime"], "D+I")

    def test_no_shift_does_not_orient(self):
        u, v = self.pair
        led, _ = I.apply_interventions(self.led, [shift(v, u, moves=False)])
        self.assertEqual(claim(led, u, v)["relation"], "x-y")

    def test_shift_on_unconnected_pair_adds_nothing(self):
        none = next(c for c in self.led["claims"] if c["relation"] == "none")
        led, _ = I.apply_interventions(self.led, [shift(none["x"], none["y"])])
        self.assertEqual(claim(led, none["x"], none["y"])["relation"], "none")
        self.assertTrue(ok(led))

    def test_intervention_beats_data_direction(self):
        led0 = ledger([(0, 2), (1, 2), (2, 3)])                 # collider 0 -> 2 <- 1, then 2 -> 3 by R1
        directed = [(c["x"], c["y"]) for c in led0["claims"] if c["relation"] == "x->y"]
        x, y = directed[0]
        led, info = I.apply_interventions(led0, [shift(y, x)])   # an intervention on the effect moves the cause
        c = claim(led, x, y)
        self.assertEqual((c["x"], c["y"], c["direction_source"], c["conflict"]), (y, x, "intervention", True))
        self.assertTrue(info["conflicts"])
        self.assertTrue(ok(led))

    def test_intervention_beats_knowledge_and_records_override(self):
        u, v = self.pair
        led_i, _ = I.apply_interventions(self.led, [shift(v, u)])     # intervention: v -> u
        rest = [n for n in NAMES if n not in (u, v)]
        tiers = [[u] + rest, [v]]                                     # knowledge: u before v
        led, info = K.apply_tiers(led_i, {"p0": {"tiers": tiers}, "p1": {"tiers": tiers}, "p2": None})
        c = claim(led, u, v)
        self.assertEqual((c["x"], c["y"], c["direction_source"]), (v, u, "intervention"))
        self.assertTrue(any(o["by"] == "i:%s>%s" % (v, u) for o in led["overrides"]))
        self.assertEqual(led["report"]["regime"], "D+I+K")
        self.assertTrue(ok(led), {k: v for k, v in verify02.verify(led).items() if v})

    def test_following_knowledge_against_an_intervention_fails_v4(self):
        u, v = self.pair
        led_i, _ = I.apply_interventions(self.led, [shift(v, u)])
        rest = [n for n in NAMES if n not in (u, v)]
        tiers = [[u] + rest, [v]]
        led, _ = K.apply_tiers(led_i, {"p0": {"tiers": tiers}, "p1": {"tiers": tiers}, "p2": None})
        bad = copy.deepcopy(led)
        c = claim(bad, u, v)
        c.update({"x": u, "y": v, "direction_source": "knowledge"})
        bad["report"]["ledger_sha256"] = verify02.canonical_hash(bad)
        self.assertIn("V4 interventions outrank knowledge (I6)", {k for k, x in verify02.verify(bad).items() if x})


if __name__ == "__main__":
    unittest.main()
