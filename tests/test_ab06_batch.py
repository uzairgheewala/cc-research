"""AB-06 (AUD-38): the plan grid is complete and well formed, the batch runner never pays twice for a crash and stops
at the total cap before starting a run, and the scorer reads the runner's edge format. No model calls, no agents run.

    python -m unittest tests/test_ab06_batch.py -v
"""
import json
import os
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
        self.plans = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(PLANS.glob("*__*__*.json"))]

    def test_tiers_partition_the_grid(self):
        T = json.loads((PLANS / "TIERS.json").read_text(encoding="utf-8"))["tiers"]
        names = {p.name for p in PLANS.glob("*__*__*.json")}
        self.assertEqual(set(T["A"]) | set(T["B"]), names)
        self.assertFalse(set(T["A"]) & set(T["B"]))
        self.assertEqual(len(T["A"]), 80)                         # amendment 1 (90 in v1)

    def test_caps_cover_the_live_estimate(self):
        for p in self.plans:
            b = p["basis"]
            self.assertIn("live_est_usd", b)
            self.assertGreaterEqual(p["run"]["max_usd"], b["live_est_usd"])

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


def _plan(tmp, name, est=1.0, cap=1.5, agent="causaliq", fake=None):
    out = Path(tmp) / "runs" / name
    pl = {"agent": agent, "arm": "real", "scenario_id": name,
          "run": {"scenario": "/nonexistent.npz", "out": str(out) + "/", "out_stub": str(out) + "_stub/", "max_usd": cap,
                  "max_calls": 5, "shuffle_seed": 1, "model": "x"},
          "basis": {"stub_est_usd": est}}
    if fake is not None:
        pl["fake"] = fake
    (Path(tmp) / "plans" / ("%s__%s__real.json" % (agent, name))).write_text(json.dumps(pl))
    return out


FAKE_PROBE = """
import json, sys, time
from pathlib import Path
pl = json.loads(Path(sys.argv[sys.argv.index("--plan") + 1]).read_text())
f = pl["fake"]
out = Path(pl["run"]["out"])
out.mkdir(parents=True, exist_ok=True)
with open(f["trace"], "a") as fh:
    fh.write("start %s %.3f\\n" % (pl["scenario_id"], time.time()))
time.sleep(f.get("sleep", 0.3))
new = f.get("usd_new", f["usd"])
if (out / "calls.jsonl").exists():                                # the gate keeps earlier attempts as calls.prevN.jsonl
    k = 1
    while (out / ("calls.prev%d.jsonl" % k)).exists():
        k += 1
    (out / "calls.jsonl").rename(out / ("calls.prev%d.jsonl" % k))
with open(out / "calls.jsonl", "a") as fh:                       # what the probe gate records: one line per call
    if f["usd"] - new > 1e-12:
        fh.write(json.dumps({"request": {}, "usd": f["usd"] - new, "replayed": True}) + "\\n")
    fh.write(json.dumps({"request": {}, "usd": new}) + "\\n")
(out / "summary.json").write_text(json.dumps({"status": f.get("status", "ok"), "est_usd_at_served_prices": f["usd"],
                                              "est_usd_new_at_served_prices": f.get("usd_new", f["usd"]),
                                              "failure_point": {"message": f.get("message", "")}}))
with open(f["trace"], "a") as fh:
    fh.write("end %s %.3f\\n" % (pl["scenario_id"], time.time()))
sys.exit({"ok": 0, "aborted_cap": 3, "failed": 4, "aborted_quota": 5}[f.get("status", "ok")])
"""


def _run(tmp, *extra, fake=False):
    env = dict(os.environ)
    if fake:
        script = Path(tmp) / "fake_probe.py"
        script.write_text(FAKE_PROBE)
        env["AB06_PROBE_SCRIPT"] = str(script)
    return subprocess.run([sys.executable, str(BATCH), "--plans", str(Path(tmp) / "plans")] + list(extra),
                          capture_output=True, text=True, timeout=120, env=env)


def _max_concurrency(trace):
    ev = []
    for line in Path(trace).read_text().splitlines():
        k, _, t = line.split()
        ev.append((float(t), 1 if k == "start" else -1))
    cur = best = 0
    for _, d in sorted(ev, key=lambda x: (x[0], x[1])):
        cur += d
        best = max(best, cur)
    return best


class Batch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        (Path(self.tmp) / "plans").mkdir()

    def _summary(self, out, status, usd):
        out.mkdir(parents=True, exist_ok=True)
        (out / "summary.json").write_text(json.dumps({"status": status, "est_usd_at_served_prices": usd}))
        (out / "calls.jsonl").write_text(json.dumps({"request": {}, "usd": usd}) + "\n")

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
        self._summary(_plan(self.tmp, "z"), "ok", 59.5)            # spend recorded in another plan's call log
        r = _run(self.tmp, "--max-usd-total", "60")
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("total cap", r.stdout)
        self.assertFalse((Path(self.tmp) / "plans" / "BATCH_live.jsonl").exists())

    def test_killed_run_spend_is_counted_and_the_run_resumes(self):
        # a machine restart leaves calls.jsonl without summary.json: its spend counts, and the run is started again
        out = _plan(self.tmp, "k0", est=0.4, cap=0.5, fake=self._fake(usd=0.1))
        out.mkdir(parents=True, exist_ok=True)
        (out / "calls.jsonl").write_text(json.dumps({"request": {}, "usd": 0.7}) + "\n" + '{"request": {"cut short')
        r = _run(self.tmp, "--max-usd-total", "10", fake=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("already spent (live) $0.70", r.stdout)
        rec = json.loads((Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()[0])
        self.assertAlmostEqual(rec["spent_total"], 0.8)

    def test_cap_hit_resumes_without_flag_but_agent_failure_does_not(self):
        self._summary(_plan(self.tmp, "c1", fake=self._fake()), "aborted_cap", 0.2)
        self._summary(_plan(self.tmp, "f1", fake=self._fake()), "failed", 0.2)
        r = _run(self.tmp, fake=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        recs = [json.loads(x) for x in (Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()]
        self.assertEqual([x["scenario"] for x in recs], ["c1"])
        self.assertIn("f1__real.json: a live attempt already ended with status failed", r.stdout)

    def _fake(self, **kw):
        d = {"trace": str(Path(self.tmp) / "trace.txt"), "usd": 0.3}
        d.update(kw)
        return d

    def test_workers_run_concurrently_and_interleave_agents(self):
        for i, ag in enumerate(["causaliq", "causaliq", "matmcd", "matmcd"]):
            _plan(self.tmp, "s%d" % i, est=0.2, cap=0.3, agent=ag, fake=self._fake())
        r = _run(self.tmp, "--workers", "2", "--max-usd-total", "10", fake=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(_max_concurrency(Path(self.tmp) / "trace.txt"), 2)
        recs = [json.loads(x) for x in (Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()]
        self.assertEqual(len(recs), 4)
        starts = [l.split()[1] for l in (Path(self.tmp) / "trace.txt").read_text().splitlines() if l.startswith("start")]
        first_two = {"causaliq" if s in ("s0", "s1") else "matmcd" for s in starts[:2]}
        self.assertEqual(first_two, {"causaliq", "matmcd"})

    def test_running_runs_are_reserved_at_their_cap(self):
        # cap 1.0: two runs fit (0.4 + 0.5 reserved), the third waits until they finish (spent 0.6), then fits exactly
        for i in range(3):
            _plan(self.tmp, "r%d" % i, est=0.4, cap=0.5, fake=self._fake(usd=0.3, sleep=0.6))
        r = _run(self.tmp, "--workers", "3", "--max-usd-total", "1.0", fake=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(_max_concurrency(Path(self.tmp) / "trace.txt"), 2)
        recs = [json.loads(x) for x in (Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()]
        self.assertEqual(len(recs), 3)
        self.assertLessEqual(recs[-1]["spent_total"], 1.0 + 1e-9)

    def test_total_cap_with_workers_stops(self):
        for i in range(3):
            _plan(self.tmp, "c%d" % i, est=0.4, cap=0.5, fake=self._fake(usd=0.45, sleep=0.2))
        r = _run(self.tmp, "--workers", "2", "--max-usd-total", "1.0", fake=True)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertEqual(len((Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()), 2)

    def test_replayed_cost_is_not_counted_again(self):
        _plan(self.tmp, "p0", fake=self._fake(usd=1.0, usd_new=0.1))
        r = _run(self.tmp, "--max-usd-total", "10", fake=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        rec = json.loads((Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()[0])
        self.assertAlmostEqual(rec["usd_new"], 0.1)
        self.assertAlmostEqual(rec["spent_total"], 0.1)

    def test_interrupted_run_resumes_without_retry_flag(self):
        out = _plan(self.tmp, "i0", fake=self._fake())
        self._summary(out, "interrupted", 0.2)
        r = _run(self.tmp, fake=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        recs = [json.loads(x) for x in (Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()]
        self.assertEqual([x["scenario"] for x in recs], ["i0"])

    def test_quota_stop_ends_launching_and_quota_failures_resume(self):
        # an older run recorded as "failed" with the provider's no-credit message resumes without the flag;
        # a run that stops on quota ends the launching of new runs (exit 5)
        old = _plan(self.tmp, "q0", fake=self._fake())
        old.mkdir(parents=True, exist_ok=True)
        (old / "summary.json").write_text(json.dumps({"status": "failed", "failure_point": {
            "message": "Error code: 429 - You have no credits remaining. Add credits to continue"}}))
        _plan(self.tmp, "q1", fake=self._fake(status="aborted_quota", usd=0.0))
        _plan(self.tmp, "q2", fake=self._fake())
        r = _run(self.tmp, "--max-usd-total", "10", fake=True)
        self.assertEqual(r.returncode, 5, r.stdout + r.stderr)
        recs = [json.loads(x) for x in (Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()]
        self.assertEqual([x["scenario"] for x in recs], ["q0", "q1"])        # q2 never started
        self.assertIn("no credits or quota left", r.stdout)

    def test_tier_filter(self):
        _plan(self.tmp, "t1", fake=self._fake())
        _plan(self.tmp, "t2", fake=self._fake())
        (Path(self.tmp) / "plans" / "TIERS.json").write_text(json.dumps({"tiers": {"A": ["causaliq__t2__real.json"]}}))
        r = _run(self.tmp, "--tier", "A", fake=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        recs = [json.loads(x) for x in (Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()]
        self.assertEqual([x["scenario"] for x in recs], ["t2"])

    def test_scenario_filter_and_non_plan_files(self):
        _plan(self.tmp, "keep", fake=self._fake())
        _plan(self.tmp, "drop", fake=self._fake())
        (Path(self.tmp) / "plans" / "BUDGET.json").write_text("{}")
        r = _run(self.tmp, "--scenario", "keep", fake=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        recs = [json.loads(x) for x in (Path(self.tmp) / "plans" / "BATCH_live.jsonl").read_text().splitlines()]
        self.assertEqual([x["scenario"] for x in recs], ["keep"])


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
