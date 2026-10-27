"""BEN-13 S0-S2: the streamed CausalBench preprocessing, the evaluator shortcut and the methods.

The streamed preprocessing must equal causalbench 1.1.2's own preprocess_dataset bit for bit, at any chunk size, on the
machine that runs it. Needs causalbench and scanpy (the bench image); skipped in the kernel environment.
"""
import importlib.util, json, sys, tempfile, types, unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
HAVE = all(importlib.util.find_spec(m) for m in ("anndata", "h5py", "openpyxl"))
HAVE_CB = HAVE and importlib.util.find_spec("causalscbench") is not None

HAVE_REF = HAVE_CB and importlib.util.find_spec("scanpy") is not None


@unittest.skipUnless(HAVE_REF, "causalbench + scanpy not installed (bench image only)")
class StreamPreprocessTest(unittest.TestCase):
    """The streamed arrays equal causalbench's own preprocess_dataset, computed on this machine, bit for bit.

    A digest frozen on another machine cannot be the test: NumPy's float32 SIMD kernels (sum, log1p) round differently on
    AVX2 and AVX-512 CPUs (wave A, 20 Oct). What must hold is equality with the original on the same machine."""

    def test_matches_causalbench_on_this_machine_at_any_chunk_size(self):
        sys.modules.setdefault("gdown", types.ModuleType("gdown"))
        import warnings
        import pandas as pd
        from causalscbench.data_access.utils.preprocessing import preprocess_dataset
        from analysis.ben13 import synth, stream_preprocess as sp
        with tempfile.TemporaryDirectory() as d, warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for seed in (0, 1):
                h5, xl = synth.make(Path(d) / ("s%d" % seed), seed=seed)
                X, genes, iv = preprocess_dataset(str(h5), pd.read_excel(xl, sheet_name=synth.SHEET))
                for chunk in (97, 4096):
                    out = Path(d) / ("s%d_%d.npz" % (seed, chunk))
                    sp.main(["--h5ad", str(h5), "--summary", str(xl), "--sheet", synth.SHEET, "--out", str(out),
                             "--chunk-rows", str(chunk)])
                    z = np.load(out)
                    self.assertEqual(z["expression_matrix"].dtype, X.dtype)
                    self.assertTrue(np.array_equal(z["expression_matrix"], X))
                    self.assertEqual(z["var_names"].tolist(), list(genes))
                    self.assertEqual(z["interventions"].tolist(), list(iv))
                    info = json.loads(Path(str(out) + ".json").read_text())
                    if seed == 0:
                        self.assertGreaterEqual(info["zero_count_dropped"], 1)   # the zero-count branch is exercised
                    self.assertIn("excluded", set(iv))


@unittest.skipUnless(HAVE_CB, "causalbench not installed (bench image only)")
class EvaluatorAndMethodsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.modules.setdefault("gdown", types.ModuleType("gdown"))
        from analysis.ben13 import synth, stream_preprocess as sp
        cls.tmp = tempfile.TemporaryDirectory()
        d = Path(cls.tmp.name)
        h5, xl = synth.make(d / "raw", cells=15000, genes=120, seed=3, n_perturbed=45)
        sp.main(["--h5ad", str(h5), "--summary", str(xl), "--sheet", synth.SHEET, "--out", str(d / "dataset_k562_filtered.npz")])
        cls.truth = json.loads((d / "raw" / "synth_truth.json").read_text())["children"]
        cls.side = json.loads((d / "dataset_k562_filtered.npz.json").read_text())
        from analysis.ben13.run import Line
        cls.L = Line("k562", d)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_fast_evaluator_equals_original(self):
        from analysis.ben13 import evaluate
        for k in (20, 60):
            net = self.L.md(k)
            a = evaluate.statistical(self.L.ev, net, -1, 20)
            b = evaluate.statistical(self.L.ev, net, -1, 20, full=True)
            for key in ("tp", "fp", "wasserstein", "for", "negative_wasserstein"):
                self.assertAlmostEqual(a[key], b[key], places=12)

    def test_mean_difference_finds_planted_children(self):
        id_to_name = {i: n for n, i in self.side["name_to_id_pairs"]}
        net = self.L.md(40)
        hits = sum(1 for a, b in net if id_to_name.get(b) in set(self.truth.get(id_to_name.get(a), [])) | {id_to_name.get(a)})
        self.assertGreater(hits / len(net), 0.5)

    def test_controls_keep_shape(self):
        from analysis.ben13 import methods
        net = self.L.md(50)
        rw = methods.rewire_children(net, self.L.genes, 0)
        pm = methods.permute_labels(net, self.L.genes, 0)
        deg = lambda n: sorted(np.unique([a for a, _ in n], return_counts=True)[1].tolist())
        self.assertEqual(deg(rw), deg(net))
        self.assertEqual(deg(pm), deg(net))
        self.assertEqual(len(set(rw)), len(net))
        self.assertTrue(all(a != b for a, b in rw + pm))

    def test_dense_network_keeps_wasserstein_and_marks_for_undefined(self):
        # wave A (22 Oct): a dense network's path closure leaves no negatives; the cell must keep its Wasserstein score
        from analysis.ben13 import evaluate
        r = evaluate.statistical(self.L.ev, self.L.md(2000), -1, 500)
        self.assertIsNone(r["for"])
        self.assertIn("negative pairs", r["for_undefined"])
        self.assertTrue(r["wasserstein"] == r["wasserstein"])                # a number, not NaN
        with self.assertRaises(ValueError):                                   # the original evaluator cannot run it at all
            evaluate.statistical(self.L.ev, self.L.md(2000), -1, 500, full=True)


@unittest.skipUnless(HAVE_CB, "causalbench not installed (bench image only)")
class CellLoopTest(unittest.TestCase):
    def test_failed_cell_is_redone_and_undefined_for_is_printed(self):
        # sheet B (22 Oct): the cell loop's progress line formatted FOR as a number and crashed on a dense network
        sys.modules.setdefault("gdown", types.ModuleType("gdown"))
        from analysis.ben13 import synth, stream_preprocess as sp, run
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            h5, xl = synth.make(d / "raw", cells=6000, genes=40, seed=3, n_perturbed=20)
            sp.main(["--h5ad", str(h5), "--summary", str(xl), "--sheet", synth.SHEET, "--out", str(d / "dataset_k562_filtered.npz")])
            old = run.OUT
            run.OUT = d / "out"
            try:
                (run.OUT / "k562").mkdir(parents=True)
                (run.OUT / "k562" / "random_k50.json").write_text(json.dumps({"status": "failed", "error": "ValueError: x"}))
                rc = run.main(["cells", "--line", "k562", "--smoke", "--data-dir", str(d), "--only", "random_k50", "--draws", "2"])
                rec = json.loads((run.OUT / "k562" / "random_k50.json").read_text())
            finally:
                run.OUT = old
            self.assertEqual(rc, 0)
            self.assertEqual(rec["status"], "ok")
            self.assertEqual(rec["earlier_error"], "ValueError: x")
            self.assertIn("wasserstein", rec["statistical"])


if __name__ == "__main__":
    unittest.main()
