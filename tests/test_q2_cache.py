"""K0 engine cache (kernel v3): a stored engine result rebuilds the same ledger, hash for hash; the key separates
tables, settings and thread environments; a corrupted or mismatched entry is an error, never a silent substitute.
NumPy only (a d-separation oracle stands in for the engines)."""
import gzip, json, os, sys, tempfile, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import q2_oracle as O  # noqa: E402
from engines import core  # noqa: E402
from kernel import build as B, cache  # noqa: E402


def table(p=8, seed=3):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((60, p))
    names = ["v%02d" % j for j in range(p)]
    edges = O.random_dag(p, seed)
    eng = O.fake_engines(X, names, log=O.pc_log(p, O.oracle(edges, p)))
    eng["ges"] = core.EngineResult("ges_bic", True, marks=eng["pc"].marks.copy(), score=-12.5, seconds=0.1)
    return X, names, eng


class Cache(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_roundtrip_rebuilds_the_same_ledger(self):
        X, names, eng = table()
        st = cache.settings()
        k = cache.key(eng["data_sha"], st)
        cache.save(eng, k, st, self.root)
        order, Xc_raw, data_sha = cache.canonical(X, names)
        self.assertEqual(data_sha, eng["data_sha"])
        back = cache.load(k, order, Xc_raw, "", self.root)
        for rule in ("pc", "C3"):
            a, _ = B.build(X, names, rule=rule, eng=eng, created_utc="")
            b, _ = B.build(X, names, rule=rule, eng=back, created_utc="")
            self.assertEqual(a["report"]["ledger_sha256"], b["report"]["ledger_sha256"], rule)

    def test_key_separates_tables_settings_and_threads(self):
        X, names, eng = table()
        k1 = cache.key(eng["data_sha"], cache.settings())
        self.assertNotEqual(k1, cache.key(eng["data_sha"][::-1], cache.settings()))
        self.assertNotEqual(k1, cache.key(eng["data_sha"], cache.settings(ges_lambda_scale=0.5)))
        old = os.environ.get("OPENBLAS_CORETYPE")
        os.environ["OPENBLAS_CORETYPE"] = "SOMETHING_ELSE"
        try:
            self.assertNotEqual(k1, cache.key(eng["data_sha"], cache.settings()))
        finally:
            if old is None:
                del os.environ["OPENBLAS_CORETYPE"]
            else:
                os.environ["OPENBLAS_CORETYPE"] = old

    def test_names_and_column_order_do_not_change_the_key(self):
        X, names, eng = table()
        perm = [3, 0, 7, 1, 6, 2, 5, 4]
        _, _, d1 = cache.canonical(X, names)
        _, _, d2 = cache.canonical(X[:, perm], [names[j] for j in perm])
        _, _, d3 = cache.canonical(X, ["w%02d" % j for j in range(X.shape[1])])
        self.assertEqual(d1, d2)
        self.assertEqual(d1, d3)

    def test_mismatched_entry_is_an_error(self):
        X, names, eng = table()
        st = cache.settings()
        k = cache.key(eng["data_sha"], st)
        p = cache.save(eng, k, st, self.root)
        with gzip.open(p, "rt") as fh:
            rec = json.load(fh)
        rec["Xc_sha256"] = "0" * 64
        with gzip.open(p, "wt") as fh:
            json.dump(rec, fh)
        order, Xc_raw, _ = cache.canonical(X, names)
        with self.assertRaises(RuntimeError):
            cache.load(k, order, Xc_raw, "", self.root)

    def test_read_only_miss_raises(self):
        X, names, _ = table()
        with self.assertRaises(LookupError):
            cache.engines(X, names, root=self.root, read_only=True)


if __name__ == "__main__":
    unittest.main()
