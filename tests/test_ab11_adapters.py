"""analysis/ab11_ledger_adapters.py never invents evidence (AUD-42, CAP-09).

Every evidence record in an adapter-built ledger must come from exactly one item the tool exposed (`sepsets` or
`adj_tests`), every id a claim cites must exist, and a tool that exposes nothing must yield claims with empty evidence and
direction_source "none". Also checked on the real ledgers in analysis/results/teardown/ when the teardown has been run.
"""
import json, sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
import ab11_ledger_adapters as LA  # noqa: E402

NAMES = ["a", "b", "c", "d"]
X = np.random.default_rng(0).normal(size=(50, 4))
ENG = {"name": "toy", "version": "0"}


def out(directed=(), undirected=(), other=(), sepsets=(), adj_tests=(), edge_meta=(), rule_records=()):
    return {"directed": [list(e) for e in directed], "undirected": [sorted(e) for e in undirected], "other": [list(e) for e in other],
            "sepsets": [list(s) for s in sepsets], "adj_tests": [list(s) for s in adj_tests], "edge_meta": [list(m) for m in edge_meta],
            "rule_records": [list(r) for r in rule_records]}


def run_of(o, K=None):
    return {"output": o, "perm": [2, 0, 3, 1], "shuffle_seed": 7, "knowledge_by_name": K}


def build(o, data_only=None, K=None, regime="D"):
    return LA.build_ledger("toy", run_of(o, K), data_only or o, X, NAMES, regime, ENG, 3, True, "t")


def exposed_items(o):
    items = [("sepset", tuple(sorted((NAMES[a], NAMES[b]))), tuple(NAMES[c] for c in cond)) for a, b, cond, _, _ in o["sepsets"]]
    items += [("adjtest", tuple(sorted((NAMES[a], NAMES[b]))), None) for a, b, _, _, _ in o["adj_tests"]]
    return sorted(items, key=repr)


def evidence_items(led):
    return sorted([("sepset" if e["id"].startswith("ev:sepset") else "adjtest", tuple(sorted(e["variables"])),
                    tuple(e["conditioning"]) if "conditioning" in e else None) for e in led["evidence"]], key=repr)


class NoInventedEvidence(unittest.TestCase):
    def assert_closed(self, led, o):
        ids = [e["id"] for e in led["evidence"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate evidence ids")
        self.assertEqual(evidence_items(led), exposed_items(o), "evidence records must be exactly the exposed items")
        for e in led["evidence"]:
            self.assertIn(e["type"], LA.EVIDENCE_TYPES_ALLOWED)
            self.assertTrue(e.get("source_field"), "each record names the tool field it came from")
        for c in led["claims"]:
            for e in c["evidence"]:
                self.assertIn(e, ids)
            if not c["evidence"] and c["direction_source"] != "knowledge":
                self.assertEqual(c["licensed_by"], "none")
            if c["direction_source"] == "data_pattern":
                self.assertTrue(c["evidence"], "a data_pattern claim must cite an exposed record")
                self.assertTrue(any((r[0], r[1]) == (NAMES.index(c["x"]), NAMES.index(c["y"])) for r in o.get("rule_records", [])),
                                "a data_pattern claim needs a rule record from the tool")
            elif c["direction_source"] != "knowledge":
                self.assertEqual(c["direction_source"], "none")

    def test_nothing_exposed(self):
        o = out(directed=[(0, 1), (2, 1)], undirected=[(2, 3)])
        led = build(o)
        self.assertEqual(led["evidence"], [])
        self.assertTrue(all(c["evidence"] == [] and c["direction_source"] == "none" for c in led["claims"]))
        self.assertEqual(len(led["claims"]), 6)
        self.assert_closed(led, o)
        self.assertIn("V1 schema", {k for k, v in LA.V.verify(led).items() if v})

    def test_sepsets_only_cover_nonadjacent_pairs(self):
        o = out(directed=[(0, 1)], undirected=[(1, 2)], sepsets=[(0, 2, [1], None, "sepset"), (0, 3, [], None, "sepset"), (0, 3, [2], None, "sepset")])
        led = build(o)
        self.assert_closed(led, o)
        by = {(c["x"], c["y"]): c for c in led["claims"]}
        self.assertEqual(by[("a", "b")]["evidence"], [])          # adjacency: no record exposed, none cited
        self.assertEqual(len(by[("a", "d")]["evidence"]), 2)
        self.assertTrue(all(e["supports"] == "nonadjacent" and "p_value" not in e for e in led["evidence"]))

    def test_adjacency_tests_carry_only_exposed_numbers(self):
        o = out(directed=[(0, 1)], adj_tests=[(0, 1, 1e-6, 0.4, "p_matrix")], sepsets=[(2, 3, [0], 0.3, "sepsets")])
        led = build(o)
        self.assert_closed(led, o)
        ev = {e["id"]: e for e in led["evidence"]}
        self.assertEqual(ev["ev:adjtest:0"]["p_value"], 1e-6)
        self.assertNotIn("conditioning", ev["ev:adjtest:0"])      # not exposed, so not written

    def test_weights_and_origin_are_not_evidence(self):
        o = out(directed=[(0, 1)], edge_meta=[(0, 1, {"weight": 0.9, "origin": "learned"})])
        led = build(o)
        self.assertEqual(led["evidence"], [])
        c = next(c for c in led["claims"] if c["relation"] == "x->y")
        self.assertEqual(c["direction_source"], "none")
        self.assertEqual(c["tool_edge_meta"]["origin"], "learned")

    def test_expert_origin_cites_existing_knowledge_only(self):
        D = out(directed=[(0, 1)])
        o = out(directed=[(0, 1), (2, 3)], edge_meta=[(0, 1, {"origin": "learned"}), (2, 3, {"origin": "expert"})])
        led = build(o, data_only=D, K={"required": [("c", "d")]}, regime="D+K")
        self.assert_closed(led, o)
        c = next(c for c in led["claims"] if (c["x"], c["y"]) == ("c", "d"))
        self.assertEqual((c["direction_source"], c["knowledge"]), ("knowledge", ["k1"]))
        self.assertEqual(c["data_only_relation"], "none")
        res = LA.verify_relaxed(led)
        self.assertTrue(res["V3"])                                 # knowledge connected a pair the data left open

    def test_logged_collider_needs_an_exposed_separation(self):
        rr = [(0, 1, 2, "v_structure", "log"), (2, 1, 0, "v_structure", "log")]
        o = out(directed=[(0, 1), (2, 1)], sepsets=[(0, 2, [3], 0.4, "log")], rule_records=rr)
        led = build(o)
        self.assert_closed(led, o)
        by = {(c["x"], c["y"]): c for c in led["claims"]}
        self.assertEqual((by[("a", "b")]["direction_source"], by[("a", "b")]["licensed_by"], by[("a", "b")]["evidence"]),
                         ("data_pattern", "v_structure", ["ev:sepset:0"]))
        o2 = out(directed=[(0, 1), (2, 1)], sepsets=[(0, 2, [1], 0.4, "log")], rule_records=rr)   # b in the sepset: no licence
        led2 = build(o2)
        self.assert_closed(led2, o2)
        self.assertTrue(all(c["direction_source"] == "none" for c in led2["claims"]))
        o3 = out(directed=[(0, 1), (2, 1)], rule_records=rr)                                       # nothing to cite
        self.assertTrue(all(c["direction_source"] == "none" and not c["evidence"] for c in build(o3)["claims"]))

    def test_reversed_direction_is_recorded_not_hidden(self):
        D = out(directed=[(1, 0)])
        o = out(directed=[(0, 1)])
        c = next(c for c in build(o, data_only=D, regime="D+K")["claims"] if c["relation"] == "x->y")
        self.assertEqual((c["data_only_relation"], c.get("data_only_relation_exact")), ("x-y", "y->x"))

    def test_hash_is_consistent(self):
        led = build(out(directed=[(0, 1)]))
        self.assertEqual(led["report"]["ledger_sha256"], LA.V.canonical_hash(led))

    def test_real_teardown_ledgers(self):
        d = ROOT / "analysis" / "results" / "teardown"
        files = sorted((d / "ledgers").glob("*.json"))
        if not files:
            self.skipTest("teardown not run")
        if not (d / "raw").is_dir():
            self.skipTest("raw tool outputs not unpacked (kept outside git: runs/ab11_teardown_raw.tgz)")
        for f in files:
            tool, lab = f.stem.split("__")
            raw = d / "raw" / tool / ("probe.json" if tool == "pywhy-llm" else "worker.json")
            w = json.loads(raw.read_text())
            run = w["runs"]["D_seed20261010" if lab in ("D", "K") else "K_" + lab.split("D+K_")[1]]
            led = json.loads(f.read_text())
            with self.subTest(ledger=f.name):
                names = [v["name"] for v in led["variables"]]
                o = run["output"]
                exp = sorted([("sepset", tuple(sorted((names[a], names[b]))), tuple(names[c] for c in cond)) for a, b, cond, _, _ in o["sepsets"]] +
                             [("adjtest", tuple(sorted((names[a], names[b]))), None) for a, b, _, _, _ in o["adj_tests"]], key=repr)
                self.assertEqual(evidence_items(led), exp)
                ids = {e["id"] for e in led["evidence"]}
                self.assertTrue(all(e in ids for c in led["claims"] for e in c["evidence"]))


if __name__ == "__main__":
    unittest.main()
