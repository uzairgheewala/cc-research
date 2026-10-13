"""Unit tests for cc-research's own code (INF-05). Standard library only:  python -m unittest discover -s tests -v"""
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
import causalarena_io as cio  # noqa: E402
import cc_graph  # noqa: E402
import error_budget  # noqa: E402
import jobkit  # noqa: E402
import score_record  # noqa: E402


class Scorer(unittest.TestCase):
    truth = {(0, 1), (1, 2)}

    def test_drop_rule(self):
        s = cio.directed_scores({(0, 1)}, {frozenset((1, 2))}, self.truth, 3, "drop")
        self.assertAlmostEqual(s["precision"], 1.0); self.assertAlmostEqual(s["recall"], 0.5); self.assertAlmostEqual(s["f1"], 2 / 3)

    def test_both_rule(self):
        s = cio.directed_scores({(0, 1)}, {frozenset((1, 2))}, self.truth, 3, "both")
        self.assertAlmostEqual(s["precision"], 2 / 3); self.assertAlmostEqual(s["recall"], 1.0)

    def test_random_rule_is_seeded(self):
        a = cio.directed_scores(set(), {frozenset((0, 1)), frozenset((1, 2))}, self.truth, 3, "random", seed=7)
        b = cio.directed_scores(set(), {frozenset((0, 1)), frozenset((1, 2))}, self.truth, 3, "random", seed=7)
        self.assertEqual(a, b)
        with self.assertRaises(ValueError):
            cio.directed_scores(set(), {frozenset((0, 1))}, self.truth, 3, "random")

    def test_repo_matrix_is_transpose(self):
        import numpy as np
        g = np.array([[0, 1], [0, 0]])          # 0 -> 1, row = cause
        self.assertEqual(cio.to_repo_matrix(g)[1, 0], 1)   # repo: M[i, j] = 1 means j -> i


class EquivalenceClass(unittest.TestCase):
    def test_collider_is_compelled(self):
        self.assertEqual(error_budget.essential(3, {(0, 2), (1, 2)}), {(0, 2), (1, 2)})

    def test_chain_is_not(self):
        self.assertEqual(error_budget.essential(3, {(0, 1), (1, 2)}), set())

    def test_meek_rule_1(self):          # 0 -> 2 <- 1, 2 - 3  =>  2 -> 3 compelled
        self.assertEqual(error_budget.essential(4, {(0, 2), (1, 2), (2, 3)}), {(0, 2), (1, 2), (2, 3)})

    def test_cc_graph_cpdag_agrees(self):
        M = cc_graph.cpdag_of({(0, 2), (1, 2), (2, 3)}, 4)
        self.assertEqual(cc_graph.pair_type(M, 2, 3), "a->b")
        M2 = cc_graph.cpdag_of({(0, 1), (1, 2)}, 3)
        self.assertEqual(cc_graph.pair_type(M2, 0, 1), "undirected")

    def test_score_counts_undirected_as_no_direction(self):
        M = cc_graph.cpdag_of({(0, 1), (1, 2)}, 3)
        s = cc_graph.score(M, {(0, 1), (1, 2)}, 3)
        self.assertEqual(s["adj_f1"], 1.0)
        self.assertEqual(s["dir_predicted"], 0)


class Jobkit(unittest.TestCase):
    def test_finalize_independent_of_order(self):
        d = Path(tempfile.mkdtemp())
        try:
            a, b = jobkit.Parts(d / "a.json"), jobkit.Parts(d / "b.json")
            for k in ("x", "y", "z"):
                a.add(k, {"v": k})
            for k in ("z", "x", "y"):
                b.add(k, {"v": k})
            self.assertEqual(a.finalize({"h": 1}), b.finalize({"h": 1}))
        finally:
            shutil.rmtree(d)

    def test_resume_skips_done(self):
        d = Path(tempfile.mkdtemp())
        try:
            a = jobkit.Parts(d / "a.json"); a.add("x", {"v": 1})
            self.assertTrue(jobkit.Parts(d / "a.json").has("x"))
        finally:
            shutil.rmtree(d)

    def test_input_key_changes_with_content(self):
        d = Path(tempfile.mkdtemp())
        try:
            f = d / "f"; f.write_text("1")
            k1 = jobkit.input_key(f); f.write_text("2")
            self.assertNotEqual(k1, jobkit.input_key(f))
            self.assertNotEqual(jobkit.input_key(f, extra="alpha=0.05"), jobkit.input_key(f, extra="alpha=0.01"))
        finally:
            shutil.rmtree(d)


class ScoreContract(unittest.TestCase):
    def test_row_rejects_unknown_regime(self):
        with self.assertRaises(ValueError):
            score_record.row(ticket="X", family="f", scenario="s", method="m", regime="DK", columns_shuffled=True,
                             names="real", supplier="causalarena", split="dev", metrics={"directed_f1": 0.5})

    def test_row_needs_knowledge_source_with_K(self):
        with self.assertRaises(ValueError):
            score_record.row(ticket="X", family="f", scenario="s", method="m", regime="D+K", columns_shuffled=True,
                             names="real", supplier="causalarena", split="dev", metrics={"directed_f1": 0.5})

    def test_contract_names_shd_variant(self):
        c = {"tickets": [], "producer": "x", "score_bearing": True, "regime": "D", "split": "dev",
             "controls": {"columns_shuffled": True, "names": "real", "supplier": "s"}, "metric_defs": {"shd": "..."}}
        self.assertTrue(any("shd_variant" in p for p in score_record.check_contract(c)))

    def test_every_results_directory_conforms(self):
        p = subprocess.run([sys.executable, str(ROOT / "analysis" / "check_scores.py")], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-500:])


class Splits(unittest.TestCase):
    def test_frozen_and_disjoint(self):
        s = json.load(open(ROOT / "plans" / "splits.json"))
        for fam, v in s["families"].items():
            self.assertFalse(set(v["dev"]) & set(v["test"]), fam)
            self.assertEqual(len(v["dev"]) + len(v["test"]), 50)
        self.assertTrue(set(s["families"]["semantic"]["s2_test_scenarios"]) <= set(s["families"]["semantic"]["test"]))

    @unittest.skipUnless((ROOT / "external" / "causalarena").is_dir(), "needs external/causalarena, which is outside git (CI)")
    def test_regenerates_identically(self):
        d = Path(tempfile.mkdtemp())
        try:
            subprocess.run([sys.executable, str(ROOT / "analysis" / "make_splits.py"), "--root", str(ROOT / "external" / "causalarena"),
                            "--out", str(d / "s.json")], check=True, capture_output=True)
            self.assertEqual((d / "s.json").read_bytes(), (ROOT / "plans" / "splits.json").read_bytes())
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
