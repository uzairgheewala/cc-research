"""BEN-13 S0: the CausalBench fetcher's checks (analysis/ben13/fetch.py). Standard library only; no network.

Must show: an empty file is never accepted (wave A, 20 Oct: rpe1.h5ad was recorded as fetched at 0 bytes); a file of the
wrong size, format or md5 is set aside, not recorded; a browser download with the published name is imported after its
checks; `_required_ok` is true only when every required file passed; a second run does not recompute a recorded file.
"""
import hashlib, importlib, json, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

HDF5 = b"\x89HDF\r\n\x1a\n"


class FetchChecksTest(unittest.TestCase):
    def setUp(self):
        self.F = importlib.import_module("analysis.ben13.fetch")
        self.orig = self.F.FILES
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.out, self.dl = t / "cb", t / "Downloads"
        self.out.mkdir()
        self.dl.mkdir()
        self.body = HDF5 + b"x" * 1000
        md5 = hashlib.md5(self.body).hexdigest()
        self.F.FILES = [("a.h5ad", "http://invalid.example/a", True, len(self.body), md5, HDF5, "A_raw.h5ad"),
                        ("b.h5ad", "http://invalid.example/b", True, len(self.body), md5, HDF5, "B_raw.h5ad"),
                        ("opt.gz", "http://invalid.example/c", False, None, None, b"\x1f\x8b", None)]

    def tearDown(self):
        self.F.FILES = self.orig
        self.tmp.cleanup()

    def run_fetch(self):
        rc = self.F.main(["--dir", str(self.out), "--import-from", str(self.dl), "--no-download"])
        return rc, json.loads((self.out / "FETCHED.json").read_text())

    def test_empty_and_wrong_files_are_rejected(self):
        (self.out / "a.h5ad").write_bytes(b"")                          # what figshare's empty body left behind
        (self.dl / "B_raw.h5ad").write_bytes(b"<html>" + b"x" * (len(self.body) - 6))   # right size, wrong format
        rc, rec = self.run_fetch()
        self.assertEqual(rc, 1)
        self.assertFalse(rec["_required_ok"])
        self.assertEqual(rec["a.h5ad"]["status"], "failed")
        self.assertEqual(rec["b.h5ad"]["status"], "failed")
        self.assertFalse((self.out / "a.h5ad").exists())                # the empty file is gone
        self.assertTrue((self.dl / "B_raw.h5ad").exists())              # a bad download is left where it was
        self.assertEqual(rec["opt.gz"]["status"], "failed")             # optional: reported, not fatal on its own

    def test_bad_md5_is_set_aside(self):
        bad = HDF5 + b"y" * 1000
        (self.out / "a.h5ad").write_bytes(bad)
        (self.dl / "B_raw.h5ad").write_bytes(self.body)
        rc, rec = self.run_fetch()
        self.assertEqual(rec["a.h5ad"]["status"], "failed")
        self.assertTrue((self.out / "a.h5ad.rejected").exists())
        self.assertEqual(rec["b.h5ad"]["status"], "ok")

    def test_browser_downloads_are_imported_and_recorded(self):
        (self.dl / "A_raw.h5ad").write_bytes(self.body)
        (self.dl / "B_raw.h5ad").write_bytes(self.body)
        (self.out / "a.h5ad.partial").write_bytes(b"")
        rc, rec = self.run_fetch()
        self.assertEqual(rc, 0)
        self.assertTrue(rec["_required_ok"])
        self.assertEqual(rec["a.h5ad"]["md5"], rec["a.h5ad"]["md5_expected"])
        self.assertIn("browser download", rec["a.h5ad"]["source"])
        self.assertFalse((self.dl / "A_raw.h5ad").exists())
        self.assertFalse((self.out / "a.h5ad.partial").exists())
        # second run: the recorded file is kept without recomputing it
        calls = []
        orig = self.F.digests
        self.F.digests = lambda p: calls.append(p) or orig(p)
        try:
            rc2, rec2 = self.run_fetch()
        finally:
            self.F.digests = orig
        self.assertEqual(rc2, 0)
        self.assertEqual(calls, [])
        self.assertEqual(rec2["a.h5ad"]["sha256"], rec["a.h5ad"]["sha256"])

    def test_real_entries_carry_sizes_md5_and_names(self):
        for name, url, required, size, md5, magic, browser in self.orig:
            if name.endswith(".h5ad"):
                self.assertTrue(required and size and md5 and magic == HDF5 and browser, name)


if __name__ == "__main__":
    unittest.main()
