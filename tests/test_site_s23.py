"""TEAM-08 / S23: the site's re-read detector sees evidence and note changes, superseded numbers need a historic mark,
and a hand-written sentence fails the build once its ticket has moved on."""
import sys, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "site"))
sys.path.insert(0, str(HERE / "site" / "levels"))
sys.path.insert(0, str(HERE / "site" / "pgs"))


class S23Test(unittest.TestCase):
    def setUp(self):
        import build
        self.b = build

    def test_fingerprint_and_migration(self):
        fp = self.b.fingerprint({"status": "in_progress", "evidence_n": 7, "note_sha": "abc"})
        self.assertEqual(fp, "in_progress|7|abc")
        self.assertFalse(self.b._changed("in_progress", fp))          # a pre-S23 review (status only) is not a change
        self.assertTrue(self.b._changed("in_progress|6|abc", fp))     # one more evidence file is
        self.assertTrue(self.b._changed("in_progress|7|xyz", fp))     # so is a new note

    def test_superseded_needs_historic(self):
        cur = '<a class="ev" href="x" title="q2.b4.sem.ece · f">0.05</a>'
        old = '<a class="ev" data-historic="1" href="x" title="q2.b4.sem.ece · f">0.05</a>'
        ok = '<a class="ev" href="x" title="q2v3.sem.D.ece · f">0.02</a>'
        self.assertEqual(len(self.b.superseded_errors("status", cur)), 1)
        self.assertEqual(self.b.superseded_errors("status", old + ok), [])

    def test_stale_literal_fails(self):
        guards = [{"page": "names", "text": "do not patch it", "ticket": "INF-06", "valid_while": ["todo"]}]
        page = {"names": "<p>we measure it as shipped and do not patch it.</p>"}
        self.assertEqual(self.b.literal_errors(page, [{"id": "INF-06", "status": "todo"}], guards), [])
        errs = self.b.literal_errors(page, [{"id": "INF-06", "status": "done"}], guards)
        self.assertEqual(len(errs), 1)
        self.assertIn("stale literal", errs[0])


if __name__ == "__main__":
    unittest.main()
