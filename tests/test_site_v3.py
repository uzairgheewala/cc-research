"""Site v3 (TEAM-10..12): the gap-type rule, combining parts, the explanation ledger contract, markdown tables, the prod-only
feed and the explorer export. Runs on synthetic snapshots; no result file is read except the spec itself."""
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "site" / "levels"), str(ROOT / "site"), str(ROOT / "site" / "pgs"), str(ROOT / "tracker")]

import common  # noqa: E402


def snap(metrics, items=()):
    return {"metrics": {k: {"value": v, "src": "analysis/results/x.json"} for k, v in metrics.items()}, "items": list(items),
            "bundles": [], "changes": [], "hash": "0" * 64, "generated_utc": "2026-10-20T00:00:00Z"}


class Base(unittest.TestCase):
    def setUp(self):
        self._saved = dict(common.SNAP)
        common.SNAP.clear()
        common.USED.clear()
        import gapkit
        self.G = importlib.reload(gapkit)
        self.G.PROBLEMS.clear()
        self.G.NOTES.clear()

    def tearDown(self):
        common.SNAP.clear()
        common.SNAP.update(self._saved)

    def use(self, metrics, items=()):
        common.SNAP.update(snap(metrics, items))


class TestPartRule(Base):
    def part(self, **kw):
        p = {"label": "x", "value": "k.v", "cons": "k.c", "bar": 0.8, "dir": "higher", "strict": True, "n": "k.n"}
        p.update(kw)
        return p

    def test_met_when_cautious_end_clears(self):
        self.use({"k.v": 0.9, "k.c": 0.85, "k.n": 25})
        self.assertEqual(self.G.derive_part(self.part())["type"], "met")

    def test_measurement_when_point_clears_and_range_does_not(self):
        self.use({"k.v": 0.83, "k.c": 0.783, "k.n": 25})
        d = self.G.derive_part(self.part())
        self.assertEqual(d["type"], "measurement")
        self.assertAlmostEqual(d["factor"], (0.047 / 0.03) ** 2, places=6)
        self.assertEqual(d["n_needed"], 62)

    def test_too_close_becomes_method(self):
        self.use({"k.v": 0.002, "k.c": -0.012, "k.n": 25})
        d = self.G.derive_part(self.part(bar=0.0))
        self.assertEqual(d["type"], "method")
        self.assertTrue(d["too_close"])

    def test_method_when_point_misses(self):
        self.use({"k.v": -0.001, "k.c": -0.007, "k.n": 25})
        self.assertEqual(self.G.derive_part(self.part(bar=0.0))["type"], "method")

    def test_strictness_at_the_bar(self):
        self.use({"k.v": 0.9, "k.c": 0.9})
        self.assertEqual(self.G.derive_part(self.part(bar=0.9, strict=False))["type"], "met")
        self.assertEqual(self.G.derive_part(self.part(bar=0.9, strict=True))["type"], "method")

    def test_lower_is_better(self):
        self.use({"k.v": 0.021, "k.c": 0.063, "k.n": 25})
        d = self.G.derive_part(self.part(bar=0.05, dir="lower", strict=False))
        self.assertEqual(d["type"], "measurement")
        self.use({"k.v": 0.021, "k.c": 0.045, "k.n": 25})
        self.assertEqual(self.G.derive_part(self.part(bar=0.05, dir="lower", strict=False))["type"], "met")

    def test_reach_without_a_value(self):
        self.use({})
        self.assertEqual(self.G.derive_part(self.part(value=None))["type"], "reach")
        self.assertEqual(self.G.derive_part(self.part(value="missing.key"))["type"], "reach")

    def test_bar_from_a_key_with_offset(self):
        self.use({"k.v": 0.926, "g": 0.916})
        p = {"label": "x", "value": "k.v", "bar_key": "g", "bar_offset": -0.03, "dir": "higher", "strict": False}
        self.assertEqual(self.G.derive_part(p)["type"], "met")


class TestCombineAndRuler(Base):
    def test_combine(self):
        self.assertEqual(self.G.combine(["met", "measurement", "met"], "all"), "measurement")
        self.assertEqual(self.G.combine(["method", "measurement"], "any"), "measurement")
        self.assertEqual(self.G.combine(["reach", "met"], "all"), "reach")

    def test_ruler_makes_comparability_and_keeps_value_type(self):
        self.use({"q2k.sem.f1": 0.523, "pub.sem.D.best": 0.634})
        d = self.G.derive("CA-SEM-TOP")
        self.assertEqual(d["type"], "comparability")
        self.assertEqual(d["value_type"], "method")

    def test_reach_is_not_hidden_by_the_ruler(self):
        self.use({"cb.k562.w": 0.442})
        self.assertEqual(self.G.derive("CB-K562")["type"], "reach")


class TestLedger(Base):
    TOT = {"q2a.sem.missed": 10, "q2a.sem.false": 6, "q2a.sem.reversed": 4,
           "q2a.for.missed": 3, "q2a.for.false": 2, "q2a.for.reversed": 1}

    def rows(self):
        r = []
        for fam in ("semantic", "formula"):
            k = fam[:3] if fam == "semantic" else "for"
            for gap, n in (("missed", self.TOT["q2a.%s.missed" % k]), ("false", self.TOT["q2a.%s.false" % k]),
                           ("reversed", self.TOT["q2a.%s.reversed" % k])):
                r.append({"board": fam, "gap": gap, "segment": "a", "size": n - 1, "unit": "links", "state": "mechanism_known",
                          "ticket": "TGT-18", "report": "r.md"})
                r.append({"board": fam, "gap": gap, "segment": "b", "size": 1, "unit": "links", "state": "walled",
                          "ticket": "TGT-18", "report": "r.md"})
        return r

    def test_absent_ledger_is_one_attributed_segment(self):
        self.use(self.TOT)
        sh = self.G.shares("sem-missed")
        self.assertTrue(sh["pending"])
        self.assertEqual(sh["by"]["attributed"], 10)
        self.assertEqual(sh["understood"], 0)
        self.assertEqual(self.G.PROBLEMS, [])

    def test_present_ledger_sums_and_shares(self):
        self.use(dict(self.TOT, **{"q2x.ledger": {"records": self.rows()}}))
        sh = self.G.shares("sem-missed")
        self.assertFalse(sh["pending"])
        self.assertAlmostEqual(sh["understood"], 1.0)
        self.assertEqual(self.G.PROBLEMS, [])

    def test_sum_mismatch_and_bad_state_and_unmapped_rows(self):
        rows = self.rows()
        rows[0]["size"] += 1
        rows[1]["state"] = "probably"
        rows.append({"board": "nowhere", "gap": "missed", "segment": "z", "size": 1, "state": "walled"})
        self.use(dict(self.TOT, **{"q2x.ledger": rows}))
        self.G.segments("sem-missed")
        self.assertTrue(any("sum to" in p for p in self.G.PROBLEMS))
        self.assertTrue(any("closed list" in p for p in self.G.PROBLEMS))
        self.assertEqual(len(self.G.unmapped_ledger_rows()), 1)

    def test_required_ledger_missing_is_a_problem(self):
        self.use(self.TOT)
        self.G.RULES["explain_ledger"]["required"] = True
        try:
            self.G.ledger_rows()
            self.assertTrue(any("required" in p for p in self.G.PROBLEMS))
        finally:
            self.G.RULES["explain_ledger"]["required"] = False


class TestSpecFile(unittest.TestCase):
    def test_closed_lists_and_references(self):
        spec = json.load(open(ROOT / "site" / "gaps_spec.json", encoding="utf-8"))
        for b in spec["boards"]:
            self.assertIn(b["ruler"]["verdict"], spec["plain"]["verdict"])
            for lid in b["landmarks"]:
                self.assertIn(lid, spec["landmarks"])
            for g in b.get("gaps", []):
                self.assertIn(g, spec["gaps"])
        for lid, lm in spec["landmarks"].items():
            self.assertIn(lm.get("combine", "all"), ("all", "any"))
            for p in lm["parts"]:
                self.assertIn(p["dir"], ("higher", "lower"))
                self.assertTrue("bar" in p or "bar_key" in p, lid)
        self.assertEqual(spec["rules"]["states"], ["unattributed", "attributed", "mechanism_known", "walled", "lever_disputed",
                                                   "lever_chosen", "acted_on"])


class TestMarkdownTable(unittest.TestCase):
    def test_parse(self):
        import snapshot
        txt = "# x\n\n## 2. Links\n\nintro\n\n| # | Source | Status |\n|---|---|---|\n| L1 | a | USED |\n| L2 | b | TRIED (x) |\n\n## 3. D\n| # | S |\n|---|---|\n| D1 | c |\n"
        rows = snapshot._md_table(txt, "## 2.")
        self.assertEqual([r["#"] for r in rows], ["L1", "L2"])
        self.assertEqual(rows[1]["Status"], "TRIED (x)")
        with self.assertRaises(ValueError):
            snapshot._md_table(txt, "## 9.")


class TestProdFeed(unittest.TestCase):
    def test_only_posted_prod_digests_and_the_lag(self):
        import snapshot
        recs = [
            {"type": "digest", "channel": "prod", "ts": "1.1", "posted_utc": "2026-10-15T04:26:17Z", "text": "*Summary*\n• P one"},
            {"type": "digest", "channel": "prod", "ts": None, "draft_only": True, "posted_utc": "2026-10-16T00:00:00Z", "text": "**Summary**\n• draft"},
            {"type": "digest", "channel": "dev", "ts": "2.2", "posted_utc": "2026-10-19T21:25:27Z", "text": "**Summary**\n• D one"},
            {"type": "digest", "channel": "dev", "ts": "2.1", "posted_utc": "2026-10-14T00:00:00Z", "text": "**Summary**\n• D old"},
        ]
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "tracker").mkdir()
            (Path(d) / "tracker" / "relay_log.jsonl").write_text("\n".join(json.dumps(r) for r in recs), encoding="utf-8")
            old = snapshot.ROOT
            snapshot.ROOT = Path(d)
            try:
                ch = snapshot.changes()
                lag = snapshot.changes_lag()
            finally:
                snapshot.ROOT = old
        self.assertEqual([c["points"] for c in ch], [["P one"]])
        self.assertTrue(all(c["channel"] == "prod" for c in ch))
        self.assertEqual(lag, {"dev_since_last_prod": 1, "last_prod_utc": "2026-10-15T04:26:17Z"})


class TestPlainBanned(unittest.TestCase):
    def test_patterns(self):
        import re
        sys.argv = ["build.py"]
        import build
        bad = ["see ER-2 here", "DV-1 precision", "the ECE is", "AC@3 of", "TGT-18 says", "directed F1"]
        ok = ["the best data-only method (GES)", "plain PC", "80% right"]
        for s in bad:
            self.assertTrue(any(re.search(p, s) for p, _ in build.PLAIN_BANNED), s)
        for s in ok:
            self.assertFalse(any(re.search(p, s) for p, _ in build.PLAIN_BANNED), s)


if __name__ == "__main__":
    unittest.main()
