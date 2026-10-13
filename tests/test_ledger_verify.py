"""ledger/verify.py accepts a correct toy ledger and catches each invariant violation (BLD-13)."""
import copy, hashlib, json, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ledger"))
import verify as V  # noqa: E402

H = lambda s: hashlib.sha256(s.encode()).hexdigest()  # noqa: E731


def toy():
    """x -> y from a collider pattern; y - z left open by the data, oriented by a tier statement; z, w unconnected;
    an intervention on y agrees with the tier."""
    eng = {"name": "causal-learn", "version": "0.1.4.8"}
    led = {"format": "cc-claim-ledger/0.1",
           "variables": [{"var_id": H(n), "name": n, "position": i} for i, n in enumerate("xyzw")],
           "evidence": [
               {"id": "e1", "type": "ci_test", "variables": ["x", "y"], "conditioning": [], "p_value": 0.001, "supports": "adjacent", "engine": eng, "seed": 0},
               {"id": "e2", "type": "ci_test", "variables": ["x", "w"], "conditioning": ["y"], "p_value": 0.4, "supports": "nonadjacent", "engine": eng, "seed": 0},
               {"id": "e3", "type": "ci_test", "variables": ["y", "z"], "conditioning": [], "p_value": 0.002, "supports": "adjacent", "engine": eng, "seed": 0},
               {"id": "e4", "type": "knowledge_statement", "variables": ["y", "z"], "supports": "x->y"},
               {"id": "e5", "type": "intervention_shift", "variables": ["y", "z"], "statistic": 4.1, "supports": "x->y"},
               {"id": "e6", "type": "ci_test", "variables": ["z", "w"], "conditioning": [], "p_value": 0.7, "supports": "nonadjacent", "engine": eng, "seed": 0}],
           "knowledge": [{"id": "k1", "kind": "tier", "content": {"tiers": [["x", "y"], ["z"]]},
                          "supplier": {"type": "model", "model_id": "gpt-4o-2024-08-06", "prompt_sha256": H("p"), "phrasing_id": "a", "shown": ["names"]}}],
           "claims": [
               {"id": "c1", "x": "x", "y": "y", "relation": "x->y", "direction_source": "data_pattern", "licensed_by": "v_structure", "evidence": ["e1", "e2"], "data_only_relation": "x->y"},
               {"id": "c2", "x": "y", "y": "z", "relation": "x->y", "direction_source": "knowledge", "licensed_by": "tier", "evidence": ["e3", "e4", "e5"], "data_only_relation": "x-y", "knowledge": ["k1"]},
               {"id": "c3", "x": "z", "y": "w", "relation": "none", "direction_source": "none", "licensed_by": "adjacency_test", "evidence": ["e6"], "data_only_relation": "none"}],
           "overrides": [],
           "report": {"run_id": "toy", "regime": "D+I+K", "data_sha256": H("data"), "engines": [eng],
                      "permutation_check": {"permutations": 5, "identical": True}, "ledger_sha256": "0" * 64,
                      "unverifiable": ["statistics are recomputed only from the data", "supplier saw only what is recorded",
                                       "calibration outside its calibration set"]}}
    led["report"]["ledger_sha256"] = V.canonical_hash(led)
    return led


def failing(res):
    return {k for k, v in res.items() if v}


def rehash(led):
    led["report"]["ledger_sha256"] = V.canonical_hash(led)
    return led


class LedgerVerify(unittest.TestCase):
    def test_toy_passes(self):
        self.assertEqual(failing(V.verify(toy())), set())

    def test_missing_field(self):
        led = toy()
        del led["claims"][0]["direction_source"]
        self.assertIn("V1 schema", failing(V.verify(led)))

    def test_dangling_evidence(self):
        led = rehash(_set(toy(), lambda l: l["claims"][0]["evidence"].append("e99")))
        self.assertIn("V2 evidence closure (I4)", failing(V.verify(led)))

    def test_knowledge_adds_connection(self):
        led = rehash(_set(toy(), lambda l: l["claims"][2].update(relation="x->y", direction_source="knowledge", knowledge=["k1"])))
        self.assertIn("V3 knowledge never connects (I5)", failing(V.verify(led)))

    def test_follows_knowledge_against_intervention(self):
        led = rehash(_set(toy(), lambda l: l["evidence"][4].update(supports="y->x")))
        self.assertIn("V4 interventions outrank knowledge (I6)", failing(V.verify(led)))

    def test_unused_knowledge(self):
        led = rehash(_set(toy(), lambda l: l["claims"][1].update(knowledge=[])))
        self.assertIn("V5 knowledge honoured", failing(V.verify(led)))

    def test_hash(self):
        led = toy()
        led["claims"][0]["licensed_by"] = "meek_r1"
        self.assertIn("V6 hash (I2)", failing(V.verify(led)))

    def test_order_invariance(self):
        led = _set(toy(), lambda l: l["report"]["permutation_check"].update(identical=False))
        self.assertIn("V7 order invariance (I1)", failing(V.verify(led)))

    def test_floor_without_knowledge(self):
        led = _set(toy(), lambda l: l["report"].update(regime="D"))
        self.assertIn("V8 floor (I3)", failing(V.verify(led)))


def _set(led, f):
    f(led)
    return led


if __name__ == "__main__":
    unittest.main()
