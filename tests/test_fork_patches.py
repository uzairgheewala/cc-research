"""INF-06 / BLD-06 / EXT-03: fork branches are checked and labelled; the BLD-06 drop-in equals refinement v2.

The drop-in (jobs/fork/bld-06/refinement_v2_dropin.py, the exact file the BLD-06 patch adds to Causal-Copilot) must give
the same graph and records as analysis/refinement_v2.py on the same inputs. verify_tree must accept a branch tree only
when its files match the branch manifest and the checkout is on that branch.
"""
import hashlib, importlib.util, json, os, sys, tempfile, unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "analysis"))
sys.path.insert(0, str(HERE / "harness"))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def random_case(rng, p):
    S0 = np.zeros((p, p), int)
    for a in range(p):
        for b in range(a + 1, p):
            r = rng.random()
            if r < 0.15:
                S0[b, a] = 1
            elif r < 0.25:
                S0[a, b] = 1
            elif r < 0.33:
                S0[a, b] = 2
            elif r < 0.36:
                S0[a, b] = 6
    keys = ["certain_edges", "uncertain_edges", "bi_edges", "half_certain_edges", "half_uncertain_edges", "none_edges"]
    boot = {k: np.round(rng.random((p, p)) * (rng.random((p, p)) < 0.3), 1) for k in keys}
    boot["none_existence"] = np.round(rng.random((p, p)), 2)
    boot["none_existence"] = np.minimum(boot["none_existence"], boot["none_existence"].T)
    return S0, boot


class DropInTest(unittest.TestCase):
    def test_same_as_refinement_v2(self):
        import refinement_v2 as R2
        D = load(HERE / "jobs" / "fork" / "bld-06" / "refinement_v2_dropin.py", "dropin")
        rng = np.random.default_rng(7)
        for _ in range(40):
            S0, boot = random_case(rng, int(rng.integers(4, 9)))
            M1, s1 = R2.v2d(S0, boot)
            M2, s2 = D.v2d(S0, boot)
            self.assertTrue(np.array_equal(M1, M2))
            self.assertEqual(s1, s2)
            pairs = D.askable_pairs(M2)
            choices = [["A->B"] * 3, ["B->A"] * 3, ["A->B", "B->A", "A->B"], ["unknown"] * 3, [None, "A->B", "A->B"]]
            ans = {pr: choices[int(rng.integers(0, len(choices)))] for pr in pairs}
            V1, r1 = R2.apply_names(M1, ans)
            V2, r2 = D.apply_names(M2, ans)
            self.assertTrue(np.array_equal(V1, V2))
            self.assertEqual(r1, r2)

    def test_names_part_retries_and_never_crashes(self):
        D = load(HERE / "jobs" / "fork" / "bld-06" / "refinement_v2_dropin.py", "dropin2")
        S0 = np.zeros((3, 3), int)
        S0[0, 1] = 2                                       # 0 --- 1, undirected
        boot = {k: np.zeros((3, 3)) for k in ["certain_edges", "uncertain_edges", "bi_edges", "half_certain_edges",
                                               "half_uncertain_edges", "none_edges"]}
        boot["uncertain_edges"][0, 1] = boot["uncertain_edges"][1, 0] = 1.0
        boot["none_existence"] = np.ones((3, 3))
        boot["none_existence"][0, 1] = boot["none_existence"][1, 0] = 0.0
        calls = []

        def ask(prompt):
            calls.append(prompt)
            if len(calls) == 1:
                raise RuntimeError("provider error")       # counts as invalid, retried once
            return {"direction": "A->B"}
        V, rec = D.refine(S0, boot, ["rain", "wet", "x"], ask)
        self.assertEqual(len(calls), 4)                    # 3 paraphrases + 1 retry
        self.assertEqual(rec["names"][0]["direction"], "a->b")
        self.assertEqual(V[1, 0], 1)                       # repo convention: M[i, j] = 1 means j -> i
        V2, rec2 = D.refine(S0, boot, ["rain", "wet", "x"], None)
        self.assertEqual(rec2["refinement"], "v2d")


class BranchIdentityTest(unittest.TestCase):
    def test_specs_match_their_files(self):
        for spec_path in sorted((HERE / "jobs" / "fork").glob("*.json")):
            spec = json.loads(spec_path.read_text())
            self.assertEqual(hashlib.sha256((HERE / spec["patch"]).read_bytes()).hexdigest(), spec["patch_sha256"])
            self.assertEqual(hashlib.sha256((HERE / spec["manifest"]).read_bytes()).hexdigest(), spec["manifest_sha256"])
        dropin = (HERE / "jobs" / "fork" / "bld-06" / "refinement_v2_dropin.py").read_text().splitlines()
        patch = (HERE / "jobs" / "fork" / "bld-06-refinement-v2.patch").read_text()
        added = [l[1:] for l in patch.split("+++ b/postprocess/refinement_v2_dropin.py", 1)[1].splitlines()[2:] if l.startswith("+")]
        self.assertEqual(added, dropin)                    # the patch adds exactly the tested file

    def test_verify_tree_branch_mode(self):
        import cc_common as C
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            repo, research = d / "repo", d / "research"
            (repo / "pkg").mkdir(parents=True)
            (repo / "main.py").write_text("print(1)\n")
            (repo / "pkg" / "a.py").write_text("A = 2\n")
            (repo / ".git" / "refs" / "heads").mkdir(parents=True)
            (repo / ".git" / "HEAD").write_text("ref: refs/heads/t-1-x\n")
            (repo / ".git" / "refs" / "heads" / "t-1-x").write_text("abc123\n")
            (research / "jobs" / "fork").mkdir(parents=True)
            man = research / "jobs" / "fork" / "t-1-x.sha256"
            man.write_text("".join("%s  ./%s\n" % (hashlib.sha256((repo / r).read_bytes()).hexdigest(), r) for r in ("main.py", "pkg/a.py")))
            spec = {"branch": "t-1-x", "ticket": "T-1", "patch_sha256": "p", "manifest": "jobs/fork/t-1-x.sha256",
                    "manifest_sha256": hashlib.sha256(man.read_bytes()).hexdigest()}
            (research / "jobs" / "fork" / "t-1-x.json").write_text(json.dumps(spec))
            old = (C.RESEARCH, C.FORK_DIR, os.environ.get("CC_BRANCH"))
            C.RESEARCH, C.FORK_DIR = research, research / "jobs" / "fork"
            os.environ["CC_BRANCH"] = "t-1-x"
            try:
                v = C.verify_tree(repo)
                self.assertTrue(v["ok"], v)
                self.assertEqual(v["git"], {"branch": "t-1-x", "commit": "abc123"})
                self.assertEqual(v["extra_unexpected"], [])       # .git is not walked
                (repo / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
                self.assertFalse(C.verify_tree(repo)["ok"])         # right files, wrong checkout
                (repo / ".git" / "HEAD").write_text("ref: refs/heads/t-1-x\n")
                (repo / "pkg" / "a.py").write_text("A = 3\n")
                v = C.verify_tree(repo)
                self.assertFalse(v["ok"])
                self.assertEqual(v["changed"], ["pkg/a.py"])
            finally:
                C.RESEARCH, C.FORK_DIR = old[0], old[1]
                if old[2] is None:
                    os.environ.pop("CC_BRANCH", None)
                else:
                    os.environ["CC_BRANCH"] = old[2]


if __name__ == "__main__":
    unittest.main()
