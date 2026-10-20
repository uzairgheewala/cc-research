"""TGT-18 / CAP-07: the family-2 read's freeze guard (analysis/q2_family2.py, plans/v3_freeze_deviation_1.json).

Must show: the read is allowed on the frozen code with the three kernel files added after the freeze (and only those, at
their recorded sha256); it refuses a changed or missing frozen file, an unexpected added file, or a changed core; inside
the read process the added files cannot be imported. The real guard is called in a subprocess (it changes sys.meta_path).
"""
import json, subprocess, sys, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "analysis"))


class FreezeStatusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import q2_family2 as F
        from kernel import freeze
        cls.F = F
        cls.rec = json.loads((HERE / "plans" / "v3_freeze.json").read_text())
        cls.dev = json.loads((HERE / "plans" / "v3_freeze_deviation_1.json").read_text())
        cls.h, cls.listing = freeze.code_sha256()
        cls.core = freeze.core_sha256()

    def test_current_tree_passes_with_deviation(self):
        st = self.F.freeze_status(self.rec, self.listing, self.core, self.dev)
        self.assertTrue(st["ok"], st)
        self.assertEqual(sorted(st["added"]), sorted(self.dev["added_files"]))

    def test_current_tree_fails_without_deviation(self):
        st = self.F.freeze_status(self.rec, self.listing, self.core, None)
        self.assertFalse(st["ok"])

    def test_changed_missing_unexpected_core(self):
        L = dict(self.listing)
        L["kernel/build.py"] = "0" * 64
        self.assertEqual(self.F.freeze_status(self.rec, L, self.core, self.dev)["changed"], ["kernel/build.py"])
        L = dict(self.listing)
        del L["kernel/derive.py"]
        self.assertFalse(self.F.freeze_status(self.rec, L, self.core, self.dev)["ok"])
        L = dict(self.listing, **{"kernel/new_thing.py": "1" * 64})
        self.assertEqual(self.F.freeze_status(self.rec, L, self.core, self.dev)["unexpected_added"], ["kernel/new_thing.py"])
        L = dict(self.listing, **{"kernel/asym.py": "2" * 64})
        self.assertEqual(self.F.freeze_status(self.rec, L, self.core, self.dev)["unexpected_added"], ["kernel/asym.py"])
        self.assertFalse(self.F.freeze_status(self.rec, self.listing, "3" * 64, self.dev)["ok"])

    def test_real_guard_allows_read_and_blocks_added_imports(self):
        log = HERE / "analysis" / "results" / "q2_v3" / "access_log.jsonl"
        if log.exists() and "v3 family2 read" in log.read_text():
            self.skipTest("the family-2 read has happened; the guard now refuses a second read by design")
        code =("import sys; sys.path[:0] = [%r, %r]; import q2_family2 as F; rec = F._guard('0cda331ea81cf0dd'); "
                "print('BLOCKED', rec['_status']['blocked_modules']);\n"
                "try:\n import kernel.asym\n print('IMPORTED')\nexcept ImportError as e:\n print('REFUSED', e)\n"
                "from kernel import build, v3\nprint('FROZEN_OK')") % (str(HERE), str(HERE / "analysis"))
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=str(HERE), timeout=120)
        self.assertEqual(out.returncode, 0, out.stderr[-2000:])
        self.assertIn("REFUSED", out.stdout)
        self.assertNotIn("IMPORTED", out.stdout)
        self.assertIn("FROZEN_OK", out.stdout)
        self.assertIn("kernel.linkfilt", out.stdout)


if __name__ == "__main__":
    unittest.main()
