"""The committed comparison is reproduced from the recorded run states, and every reduced state matches its manifest."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run  # noqa: E402


class Reproduce(unittest.TestCase):
    def test_comparison_reproduces(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "x.json"
            subprocess.run([sys.executable, str(ROOT / "analysis" / "bld06_live_compare.py"), "--out", str(out)], check=True,
                           capture_output=True)
            self.assertEqual(run.close(json.loads(out.read_text()), json.loads(run.COMMITTED.read_text())), [])

    def test_prereg_hash(self):
        r = json.loads(run.COMMITTED.read_text())
        self.assertEqual(r["prereg_sha256"], hashlib.sha256((ROOT / "plans" / "bld06_live_prereg.json").read_bytes()).hexdigest())

    def test_reduced_states_match_manifest(self):
        man = json.loads((ROOT / "recorded" / "MANIFEST.json").read_text())
        for rel, rec in man["reduced"].items():
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), rec["reduced_sha256"], rel)

    def test_suite_files_match_their_cards(self):
        mapping = json.loads((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_text())
        for arm, spec in mapping["arms"].items():
            f = ROOT / spec["dataset_arg"].split(":", 1)[1]
            self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(), spec["sha256"], arm)


if __name__ == "__main__":
    unittest.main()
