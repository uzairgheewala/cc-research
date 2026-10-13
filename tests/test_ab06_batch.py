"""AB-06 (AUD-38): the plan grid is complete and well formed, the batch runner never pays twice for a crash and stops
at the total cap before starting a run, and the scorer reads the runner's edge format. No model calls, no agents run.

    python -m unittest tests/test_ab06_batch.py -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
PLANS = KIT / "plans" / "ab06"
BATCH = KIT / "harness" / "agent_batch.py"


def local(p):
    return Path(str(p).replace("/research", str(KIT), 1))


class Grid(unittest.TestCase):
    def setUp(self):
        self.plans = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(PLANS.glob("*.json")) if p.name != "BUDGET.json"]

    def test_full_grid(self):
        self.assertEqual(len(self.plans), 120)
        self.assertEqual(json.loads((PLANS / "BUDGET.json").read_text())["total"]["runs"], 120)
        cells = Counter((p["agent"], p["arm"]) for p in self.plans)
        self.assertEqual(set(cells.values()), {10})
        self.assertEqual({a for a, _ in cells}, {"causaliq", "pywhyllm", "matmcd", "vashishtha"})
        self.assertEqual(len({p["run"]["out"] for p in self.plans}), 120)
        self.assertEqual(len({p["run"]["out_stub"] for p in self.plans}), 120)

    def test_names_maps(self):
        for p in self.plans:
            r = p["run"]
            self.assertEqual(r["shuffle_seed"], 20261010)
            self.assertGreater(r["max_usd"], 0)
            self.assertGreater(r["max_calls"], 0)
            if p["arm"] == "real":
                self.assertFalse(r.get("names_map"))
                continue
            m = json.loads(local(r["names_map"]).read_text(encoding="utf-8"))
            self.assertEqual(len(set(m.values())), len(m), "names map must be one-to-one")
            if p["arm"] == "swapped":
                self.assertEqual(set(m.values()), set(m), "swapped arm permutes the real names")
                self.assertTrue(all(k != v for k, v in m.items()), "swapped arm moves every name")
            else:
                self.assertTrue(all(v.startswith("V") and v[1:].isdigit() for v in m.values()))


def _plan(tmp, name, est=1.0, cap=1.5):
    out = Path(tmp) / "runs" / name
    pl = {"agent": "causaliq", "arm": "real", "scenario_id": name,
          "run": {"scenario": "/nonexistent.npz", "out": str(out) + "/", "out_stub": str(out) + "_stub/", "max_usd": cap,
                  "max_calls": 5, "shuffle_seed": 1, "model": "x"},
          "basis": {"stub_est_usd": est}}
    (Path(tmp) / "plans" / (name + ".json")).write_text(json.dumps(pl))
    return out


def _run(tmp, *extra):
    return subprocess.run([sys.executable, str(BATCH), "--plans", str(Path(tmp) / "plans")] + list(extra),
                          capture_output=True, text=True, timeout=120)


class Batch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        (Path(self.tmp) / "plans").mkdir()

    def _summary(self, out, status, usd):
        out.mkdir(parents=True, exist_ok=True)
        (out / "summary.json").write_text(json.dumps({"status": status, "est_usd_at_served_prices": usd}))

    def test_ok_runs_are_skipped(self):
        self._summary(_plan(self.tmp, "a"), "ok", 0.5)
        r = _run(self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertFalse((Path(self.tmp) / "plans" / "BATCH_live.jsonl").exists())

    def test_paid_failure_is_not_retried_by_default(self):
        self._summary(_plan(self.tmp, "a"), "agent_failed", 0.4)
        r = _run(self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("--retry-failed", r.stdout)
        self.assertIn("$0.40", r.stdout)          # counted as spent
        self.assertFalse((Path(self.tmp) / "plans" / "BATCH_live.jsonl").exists())

    def test_total_cap_stops_before_a_run(self):
        _plan(self.tmp, "b", est=1.0)
        (Path(self.tmp) / "plans" / "BATCH_live.jsonl").write_text(json.dumps({"plan": "z.json", "usd": 59.5}) + "\n")
        r = _run(self.tmp, "--max-usd-total", "60")
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("total cap", r.stdout)
        self.assertEqual(len((Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()), 1)


class ScorerFormat(unittest.TestCase):
    def test_edges_reads_both_formats(self):
        sys.path.insert(0, str(KIT / "analysis"))
        try:
            from ab06_score import edges
        except ImportError as e:   # numpy or the CausalArena loaders missing on this interpreter
            self.skipTest(str(e))
        D, U = edges([{"from_idx": 0, "to_idx": 2, "source": "llm"}, [3, 1]], [{"a_idx": 4, "b_idx": 1}, [2, 0]])
        self.assertEqual(D, {(0, 2), (3, 1)})
        self.assertEqual(U, {(1, 4), (0, 2)})


if __name__ == "__main__":
    unittest.main()
