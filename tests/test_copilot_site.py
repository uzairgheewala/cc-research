"""Inside Causal-Copilot (TEAM-13): the extractor's call resolution and state tracking on a synthetic repo, and the site
build on the committed model, content and excerpts (no Causal-Copilot checkout needed)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site" / "copilot"))

import extract  # noqa: E402

SRC = {
    "pkg/__init__.py": "",
    "pkg/a.py": (
        "from pkg.b import helper, Worker\n"
        "class Step:\n"
        "    def __init__(self, args):\n"
        "        self.w = Worker()\n"
        "    def forward(self, global_state):\n"
        "        x = helper(global_state.data.table)\n"
        "        global_state.results.graph = x\n"
        "        self.w.run()\n"
        "        jobs = [self.tidy]\n"
        "        return global_state\n"
        "    def tidy(self):\n"
        "        return 1\n"),
    "pkg/b.py": (
        "def helper(t):\n"
        "    return t\n"
        "class Worker:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    def run(self):\n"
        "        return helper(0)\n"),
}


class Extractor(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        repo = Path(self.d.name)
        for rel, txt in SRC.items():
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (repo / rel).write_text(txt)
        mods, funcs = [], []
        for rel in sorted(SRC):
            m, fs = extract.parse_module(repo, rel)
            mods.append(m)
            funcs += fs
        self.F = {f["id"]: f for f in extract.resolve(funcs, mods)}

    def tearDown(self):
        self.d.cleanup()

    def calls(self, fid):
        return {(c["to"], c["how"]) for c in self.F[fid]["calls"]}

    def test_import_typed_and_reference_calls(self):
        c = self.calls("pkg/a.py::Step.forward")
        self.assertIn(("pkg/b.py::helper", "import"), c)
        self.assertIn(("pkg/b.py::Worker.run", "typed"), c)       # self.w = Worker() in __init__
        self.assertIn(("pkg/a.py::Step.tidy", "reference"), c)    # passed as a value, not called
        self.assertTrue({("pkg/b.py::Worker.__init__", "class"), ("pkg/b.py::Worker.__init__", "import-class")} & self.calls("pkg/a.py::Step.__init__"))

    def test_state_reads_and_writes(self):
        f = self.F["pkg/a.py::Step.forward"]
        self.assertIn("data.table", f["reads"])
        self.assertIn("results.graph", f["writes"])

    def test_callers(self):
        self.assertEqual(self.F["pkg/b.py::helper"]["callers"], ["pkg/a.py::Step.forward", "pkg/b.py::Worker.run"])


class Site(unittest.TestCase):
    def test_model_is_from_the_baseline_manifest(self):
        import hashlib
        m = json.load(open(ROOT / "site" / "copilot" / "model.json", encoding="utf-8"))
        self.assertEqual(m["manifest_sha256"], hashlib.sha256((ROOT / m["manifest"]).read_bytes()).hexdigest())
        self.assertEqual(m["counts"]["llm_points_unjoined"], 0)
        self.assertEqual(m["counts"]["parse_errors"], 0)

    def test_build_is_clean(self):
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, str(ROOT / "site" / "copilot" / "build.py"), "--out", d], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout[-1500:] + p.stderr[-1500:])
            self.assertIn(" 0 errors", p.stdout)
            self.assertTrue((Path(d) / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
