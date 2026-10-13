"""Unit tests for refinement v2 (BND-11): the data part never deletes, the names part never crashes or contradicts the data."""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import refinement_v2 as R2  # noqa: E402
import cc_graph as G  # noqa: E402

KEYS = ["certain_edges", "uncertain_edges", "bi_edges", "half_certain_edges", "half_uncertain_edges", "none_edges", "none_existence"]


def boot(p, none=1.0):
    b = {k: np.zeros((p, p)) for k in KEYS}
    b["none_existence"] = np.full((p, p), none)
    return b


class V2Data(unittest.TestCase):
    def test_never_deletes_algorithm_adjacency(self):
        S0 = np.zeros((3, 3), int)
        S0[1, 0] = 1                     # 0 -> 1
        S0[1, 2] = S0[2, 1] = 2          # 1 - 2
        V, src = R2.v2d(S0, boot(3, none=1.0))       # resamples never saw any edge
        self.assertTrue(G.is_adjacent(V, 0, 1) and G.is_adjacent(V, 1, 2))
        self.assertEqual(len(src), 2)

    def test_adds_only_at_ADD(self):
        S0 = np.zeros((3, 3), int)
        b = boot(3, none=0.05)           # connected 0.95 for every pair
        b["uncertain_edges"][:] = 1.0
        V, src = R2.v2d(S0, b)
        self.assertEqual(sum(1 for s in src if s["source"] == "bootstrap: added"), 3)
        b2 = boot(3, none=0.2)           # connected 0.8 < 0.9
        V2, src2 = R2.v2d(S0, b2)
        self.assertEqual(len(src2), 0)


class Names(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(R2.parse_reply('{"direction": "A->B"}'), "A->B")
        self.assertIsNone(R2.parse_reply("A->B"))
        self.assertIsNone(R2.parse_reply('{"direction": "A->B", "why": "x"}'))
        self.assertIsNone(R2.parse_reply('{"direction": "a->b"}'))
        self.assertIsNone(R2.parse_reply(None))

    def test_agreement_cycle_marks_abstain(self):
        M = np.zeros((3, 3), int)
        M[1, 0] = 1                      # 0 -> 1 committed by data
        M[1, 2] = M[2, 1] = 2            # 1 - 2
        M[0, 2] = M[2, 0] = 2            # 0 - 2
        ans = {(1, 2): ["A->B"] * 3,     # 1 -> 2
               (0, 2): ["B->A"] * 3}     # 2 -> 0; together with 0 -> 1 -> 2 a cycle
        V, recs = R2.apply_names(M, ans)  # pairs in sorted order: (0, 2) is taken first, so (1, 2) is the one refused
        used = {tuple(r["pair"]): r for r in recs}
        self.assertTrue(used[(0, 2)]["used"])
        self.assertFalse(used[(1, 2)]["used"])
        self.assertEqual(used[(1, 2)]["why"], "would create a directed cycle")
        V2, recs2 = R2.apply_names(M, {(1, 2): ["A->B", "B->A", "A->B"]})
        self.assertFalse(recs2[0]["used"])
        V3, recs3 = R2.apply_names(M, {(1, 2): ["A->B", None, "A->B"]})
        self.assertEqual(recs3[0]["why"], "abstained (invalid reply after one retry)")
        P = np.zeros((2, 2), int)
        P[1, 0] = 4                      # 0 o-> 1 (arrowhead at 1 set by the data)
        V4, recs4 = R2.apply_names(P, {(0, 1): ["B->A"] * 3})
        self.assertEqual(recs4[0]["why"], "contradicts the mark set by the data")
        V5, recs5 = R2.apply_names(P, {(0, 1): ["A->B"] * 3})
        self.assertTrue(recs5[0]["used"])
        self.assertEqual(G.pair_type(V5, 0, 1), "a->b")


class RunnerParse(unittest.TestCase):
    def test_runner_and_rule_parse_alike(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness"))
        import names_runner as NR
        for t in ['{"direction": "A->B"}', '{"direction": "B->A"}', '{"direction": "unknown"}', "A->B", '{"direction": "maybe"}',
                  '{"direction": "A->B", "x": 1}', None, "", '["A->B"]']:
            self.assertEqual(NR.parse_reply(t), R2.parse_reply(t), t)


if __name__ == "__main__":
    unittest.main()
