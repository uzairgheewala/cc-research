"""B2 name-reliance generator and scorer (AB-08, AUD-39): determinism, acyclicity, agreement = 1 - rho, shuffled columns,
and scorer sanity on the names oracle.

Most tests build files from synthetic source scenarios and need no external data. They need causalarena_io and
sortability_audit importable (they are in analysis/ in the cc-research checkout; elsewhere set B2_CA_ROOT to a CausalArena
root inside a checkout, e.g. .../cc-research/external/causalarena). The one test on a real CausalArena scenario is skipped
when that root is absent.
"""
import hashlib, json, os, sys, tempfile, unittest, zlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
CA_ROOT = Path(os.environ.get("B2_CA_ROOT", ROOT / "external" / "causalarena"))
try:
    import causalarena_io  # noqa: F401
except ImportError:
    sys.path.append(str(CA_ROOT.resolve().parents[1] / "analysis"))
try:
    import b2_generator as B
    import b2_score as S
    CA, SA = B._ensure_imports()
except ImportError as e:  # pragma: no cover
    raise unittest.SkipTest("causalarena_io / sortability_audit not importable: %s" % e)

SEED = 20261012


def random_dag(d, p, seed):
    rng = np.random.default_rng(seed)
    G = np.triu((rng.random((d, d)) < p).astype(np.int8), 1)   # causal order = index order, as CausalArena releases
    return G


def fake_source(d=14, p=0.3, seed=0, slug="toy"):
    G = random_dag(d, p, seed)
    return {"g": G, "node_ids": ["v%02d" % i for i in range(d)], "meta": {"scenario_id": slug, "domain_id": "toy"},
            "_file": "%s.npz" % slug}


class GraphSurgery(unittest.TestCase):
    def test_acyclic_count_agreement_nested(self):
        for t in range(25):
            G = random_dag(18, 0.25, t)
            m = int(G.sum())
            prev = None
            for rho in B.RHOS:
                GD, agree, info = B.break_graph(G, rho, SEED, "s%d" % t)
                self.assertTrue(B.is_acyclic(GD))
                self.assertEqual(int(GD.sum()), m)
                acc = float((agree == 1).sum()) / m
                self.assertLessEqual(abs(acc - (1 - rho)), 0.5 / m + 1e-12)
                self.assertEqual(info["k"], int(np.floor(rho * m + 0.5)))
                # every agreeing G_D edge is a G_N edge, every disagreeing one is not
                self.assertTrue(np.all(G[agree == 1] == 1))
                self.assertTrue(np.all(G[(agree < 0)] == 0))
                self.assertEqual(int(((agree != 0) != (GD != 0)).sum()), 0)
                if prev is not None:      # nested: edges kept at a larger rho were kept at every smaller rho
                    kept_now = (agree == 1)
                    self.assertTrue(np.all(prev[kept_now]))
                prev = agree == 1


class Files(unittest.TestCase):
    def make(self, src, rho, track, rep):
        return B.make_file(SA, src, src["meta"]["scenario_id"], "dev", rho, track, rep, SEED, "0" * 64)

    def test_determinism_bytes(self):
        src = fake_source()
        with tempfile.TemporaryDirectory() as tmp:
            hs = []
            for k in range(2):
                arrays, _ = self.make(src, 0.5, "nonlinear", 1)
                hs.append(B.write_npz(Path(tmp) / ("f%d.npz" % k), arrays))
            self.assertEqual(hs[0], hs[1])
            self.assertEqual(hs[0], hashlib.sha256((Path(tmp) / "f0.npz").read_bytes()).hexdigest())
            s = CA.load(Path(tmp) / "f0.npz")           # the existing loader reads the release format
            self.assertEqual(s["n_obs"], 1000)
            self.assertEqual(s["n_int"], 0)
            self.assertEqual(s["values"].shape, (1000, 14))
            self.assertFalse(s["intervened"].any())

    def test_file_contents(self):
        src = fake_source(seed=3)
        for track in B.TRACKS:
            for rho in B.RHOS:
                a, meta = self.make(src, rho, track, 0)
                GD, GN = a["g"] != 0, a["g_names"] != 0
                self.assertTrue(B.is_acyclic(GD))
                m = int(GD.sum())
                self.assertEqual(m, int(GN.sum()))
                self.assertLessEqual(abs((a["edge_agreement"] == 1).sum() / m - (1 - rho)), 0.5 / m + 1e-12)
                X = a["x"][:, :, 0].astype(float)
                self.assertLess(np.abs(X.mean(0)).max(), 1e-5)
                self.assertLess(np.abs(X.std(0) - 1).max(), 1e-4)
                perm = meta["column_permutation"]
                self.assertEqual(list(a["node_ids"]), [src["node_ids"][i] for i in perm])
                self.assertTrue(np.array_equal(GN, np.asarray(src["g"])[np.ix_(perm, perm)] != 0))

    def test_columns_shuffled(self):
        shares = []
        for t in range(12):
            src = fake_source(d=16, p=0.3, seed=100 + t, slug="toy%d" % t)
            a, _ = self.make(src, 0.0, "linear", 0)
            E = a["g"] != 0
            shares.append(E[np.triu_indices(E.shape[0], 1)].sum() / E.sum())
        self.assertLess(float(np.mean(shares)), 0.75)    # released order would give 1.0
        self.assertGreater(float(np.mean(shares)), 0.25)

    def test_r2_fast_matches_audit(self):
        src = fake_source(seed=5)
        a, _ = self.make(src, 0.25, "linear", 0)
        X = a["x"][:, :, 0].astype(float)
        self.assertLess(np.abs(B.r2_fast(X) - SA.r2_all(X)).max(), 1e-8)


class Scorer(unittest.TestCase):
    def test_names_oracle(self):
        src = fake_source(d=16, p=0.3, seed=7)
        scored = []
        for rho in B.RHOS:
            for track in B.TRACKS:
                a, meta = B.make_file(SA, src, "toy", "dev", rho, track, 0, SEED, "0" * 64)
                key = "b2_%s_%s_toy__rep000.npz" % (track, B.rho_tag(rho))
                row = {"file": key, "method": "names_oracle",
                       "directed_edges": [[int(i), int(j)] for i, j in np.argwhere(a["g_names"] != 0)], "undecided_pairs": []}
                r = S.score_row(CA, row, a)
                m = int((a["g"] != 0).sum())
                k = int(np.floor(rho * m + 0.5))
                self.assertAlmostEqual(r["f1_data"], (m - k) / m, places=12)
                self.assertAlmostEqual(r["f1_names"], 1.0, places=12)
                if r["dis_arrows"]:
                    self.assertEqual(r["dis_names"], r["dis_arrows"])        # every disputed arrow follows the names
                    self.assertEqual(r["dis_data"], 0)
                scored.append(r)
        summ = S.summarise(scored)["names_oracle"]
        self.assertLessEqual(summ["trend_all"]["spearman_f1_data_vs_rho"], -0.8)
        self.assertEqual(summ["by_track_rho"]["linear"]["0.00"]["f1_data_mean"], 1.0)
        self.assertEqual(summ["by_track_rho"]["linear"]["1.00"]["f1_data_mean"], 0.0)

    def test_data_oracle_and_undecided(self):
        src = fake_source(d=12, p=0.35, seed=9)
        a, _ = B.make_file(SA, src, "toy", "dev", 0.75, "linear", 0, SEED, "0" * 64)
        E = [[int(i), int(j)] for i, j in np.argwhere(a["g"] != 0)]
        r = S.score_row(CA, {"file": "x.npz", "method": "data_oracle", "directed_edges": E, "undecided_pairs": []}, a)
        self.assertAlmostEqual(r["f1_data"], 1.0)
        self.assertEqual(r["dis_names"], 0)
        # all pairs undecided: the random rule is seeded by crc32(file name), so the score is reproducible
        und = [[min(e), max(e), -1, -1] for e in E]
        r1 = S.score_row(CA, {"file": "y.npz", "method": "u", "directed_edges": [], "undecided_pairs": und}, a)
        r2 = S.score_row(CA, {"file": "y.npz", "method": "u", "directed_edges": [], "undecided_pairs": und}, a)
        self.assertEqual(r1["f1_data"], r2["f1_data"])
        self.assertEqual(zlib.crc32(b"y.npz"), zlib.crc32("y.npz".encode()))


@unittest.skipUnless((CA_ROOT / "scm" / "semantic" / "data" / "semantic_obs_only").is_dir(), "needs external/causalarena")
class RealScenario(unittest.TestCase):
    def test_generate_twice_identical(self):
        splits = CA_ROOT.resolve().parents[1] / "plans" / "splits.json"
        slug = json.load(open(splits))["families"]["semantic"]["dev"][0]
        with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
            m1, c1 = B.generate(CA_ROOT, t1, [0.0, 1.0], ["linear"], 1, SEED, splits, slugs=[slug], quiet=True)
            m2, _ = B.generate(CA_ROOT, t2, [0.0, 1.0], ["linear"], 1, SEED, splits, slugs=[slug], quiet=True)
            self.assertEqual(m1["files"], m2["files"])
            self.assertEqual(len(m1["files"]), 2)
            self.assertTrue(B.check(t1))
            for c in c1:
                self.assertEqual(c["split"], "dev")
                self.assertAlmostEqual(c["name_agreement"], 1 - c["rho"], delta=0.5 / c["edges"] + 1e-12)


if __name__ == "__main__":
    unittest.main()
