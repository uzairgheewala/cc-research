"""The commit gate must inspect staged bytes and leave unstaged work untouched."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("commit_gate", Path(__file__).resolve().parents[1] / "tools/commit_gate.py")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class StagedTreeGate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="commit-gate-test-", dir=os.environ.get("MILESTONE_TEMP_DIR"))
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "sample"
        self.repo.mkdir()
        self.git("init", "--quiet")
        (self.repo / "check.py").write_text(
            "from pathlib import Path\nassert Path('value.txt').read_text() == 'good'\n", encoding="utf-8")
        (self.repo / ".commit-policy.json").write_text(json.dumps({"version": 1,
            "checks": [["{python}", "-B", "check.py"]]}), encoding="utf-8")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.DEVNULL)

    def stage(self, value):
        (self.repo / "value.txt").write_text(value, encoding="utf-8")
        self.git("add", "--", ".commit-policy.json", "check.py", "value.txt")

    def test_unstaged_fix_cannot_hide_bad_staged_bytes(self):
        self.stage("bad")
        (self.repo / "value.txt").write_text("good", encoding="utf-8")
        with self.assertRaises(subprocess.CalledProcessError):
            GATE.validate(self.repo)
        self.assertEqual(self.git("show", ":value.txt"), b"bad")

    def test_unstaged_work_does_not_contaminate_good_staged_bytes(self):
        self.stage("good")
        (self.repo / "value.txt").write_text("unfinished", encoding="utf-8")
        index_before = self.git("write-tree")
        GATE.validate(self.repo)
        self.assertEqual(index_before, self.git("write-tree"))
        self.assertEqual((self.repo / "value.txt").read_text(), "unfinished")

    def test_policy_is_read_from_index(self):
        self.stage("bad")
        (self.repo / ".commit-policy.json").write_text(json.dumps({"version": 1, "checks": []}), encoding="utf-8")
        with self.assertRaises(subprocess.CalledProcessError):
            GATE.validate(self.repo)

    def test_absolute_archive_paths_are_rejected(self):
        from unittest.mock import patch
        import io
        import zipfile
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr("../escape.txt", "bad")
        with patch.object(GATE, "git", side_effect=[b"tree", stream.getvalue()]):
            with self.assertRaises(ValueError):
                GATE.extract_index(self.repo, self.repo / "export")


if __name__ == "__main__":
    unittest.main()
