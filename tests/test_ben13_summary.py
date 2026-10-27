"""BEN-13: the pre-registered predictions are scored by code from the summary, and the report reads every number from it.

Must show: P1-P4 verdicts follow plans/ben13_prereg.json's bars; a missing cell gives 'not computed', never pass or fail;
the report lists every prediction and the reproduction rows. NumPy only (no causalbench).
"""
import importlib.util, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, HERE / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def q(mean, lo, hi):
    return {"mean": mean, "lo": lo, "hi": hi, "n": 20}


def line(share, echo, perm_mean, k5000_random=True, string_w=0.13, rand_hi=0.12):
    c = {"k1000": {"placement_share_wasserstein": share, "echo_ratio": echo,
                   "permute_labels": {"wasserstein": q(perm_mean, 0.09, 0.12)}, "random": {"wasserstein": q(0.11, 0.10, 0.12)}},
         "k5000": {"permute_labels": {"wasserstein": q(perm_mean, 0.09, 0.12)},
                   "random": {"wasserstein": q(0.11, 0.10, 0.12) if k5000_random else None}}}
    return {"controls": c, "reproduction": {}, "literature": {"string_network": {
        "edges": 100, "wasserstein": string_w, "for": None, "random_same_size": {"wasserstein": q(0.11, 0.10, rand_hi)},
        "permuted": {"own_precision": q(0.1, 0.09, 0.11)}}}}


class PredictionsTest(unittest.TestCase):
    def setUp(self):
        self.run = load("analysis/ben13/run.py", "ben13_run")
        self.rep = load("analysis/ben13/report.py", "ben13_report")

    def test_verdicts(self):
        P = self.run.predictions({"k562": line(0.13, 0.90, 0.111), "rpe1": line(0.07, 0.95, 0.105)})
        self.assertEqual(P["P1"]["verdict"], "fails")
        self.assertEqual(P["P2"]["verdict"], "holds")
        self.assertEqual(P["P3"]["verdict"], "holds")
        self.assertEqual(P["P4"]["verdict"], "holds")
        P = self.run.predictions({"k562": line(0.6, 0.89, 0.2), "rpe1": line(0.7, 0.95, 0.105, string_w=0.11)})
        self.assertEqual((P["P1"]["verdict"], P["P2"]["verdict"], P["P3"]["verdict"], P["P4"]["verdict"]),
                         ("holds", "fails", "fails", "fails"))

    def test_missing_cell_is_not_computed(self):
        P = self.run.predictions({"k562": line(0.13, 0.90, 0.111), "rpe1": line(0.07, 0.95, 0.105, k5000_random=False)})
        self.assertEqual(P["P2"]["verdict"], "not computed")
        P = self.run.predictions({"k562": line(None, 0.90, 0.111), "rpe1": line(0.07, 0.95, 0.105)})
        self.assertEqual(P["P1"]["verdict"], "not computed")

    def test_report_lists_predictions(self):
        lines = {"k562": line(0.13, 0.90, 0.111), "rpe1": line(0.07, 0.95, 0.105)}
        s = {"prereg_sha256": "ab" * 32, "lines": lines, "reproduction_all": True, "fast_equals_full_all": True,
             "predictions": self.run.predictions(lines)}
        md = self.rep.build(s)
        for k in ("P1", "P2", "P3", "P4"):
            self.assertIn("| %s |" % k, md)
        self.assertIn("undefined", md)


if __name__ == "__main__":
    unittest.main()
