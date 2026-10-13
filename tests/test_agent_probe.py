"""AB-05 (AUD-37): the agent-probe runner works offline for every installed agent, writes the required fields, never
writes the key, and stops cleanly at a call or spending cap.

Run with the probe interpreter (stdlib unittest only):
    /home/claude/work/agents/venv_probe/bin/python -m unittest tests/test_agent_probe.py -v      (sandbox)
    python -m unittest /research/tests/test_agent_probe.py -v                                   (cc-probes image)
Agent packages are looked up like the runner does: $PROBES_ROOT/<agent> (pip --target dirs) and $PROBES_SRC/<repo>.
An agent whose package cannot be imported is SKIPPED with the import error as the reason.
The scenario is $AB05_SCENARIO, else the first semantic_obs_only file found under external/causalarena.
"""
import glob
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
HARNESS = KIT / "harness"
RUNNER = HARNESS / "agent_probe.py"
REGISTRY = json.loads((HARNESS / "agents" / "registry.json").read_text())
AGENTS = ["vashishtha", "pywhyllm", "matmcd", "causaliq"]
IMPORT_PROBE = {
    "vashishtha": "import causal_discovery.strategies.triplet, causal_discovery.utils.cycle_remover, causallearn, openai",
    "pywhyllm": "import guidance; from pywhyllm.suggesters.model_suggester import ModelSuggester",
    "matmcd": "import ConstrainAgent.ConstrainAgent, Utils.CausalDiscovery",
    "causaliq": "from causaliq_knowledge.graph.generator import GraphGenerator",
}
SENTINEL = "sk" + "-SENTINEL-must-never-appear-0123456789"  # split so the secret scan does not flag a fake key
REQUIRED_SUMMARY = ["agent", "scenario", "mode", "model", "status", "failure_point", "calls", "new_api_calls",
                    "prompt_tokens", "completion_tokens", "est_usd_gpt4o_list", "est_usd_at_served_prices",
                    "token_counter", "wall_seconds", "directed_f1_random_rule", "scores", "shuffle_seed", "caps",
                    "agent_repo"]


def _first_existing(cands):
    for c in cands:
        if c and Path(c).exists():
            return str(c)
    return None


PROBES_ROOT = _first_existing([os.environ.get("PROBES_ROOT"), "/opt/probes", KIT.parent / "agents" / "venv_probe" / "probes"])
PROBES_SRC = _first_existing([os.environ.get("PROBES_SRC"), (Path(PROBES_ROOT) / "src") if PROBES_ROOT else None,
                              KIT.parent / "agents"])
TIKTOKEN_CACHE = _first_existing([os.environ.get("TIKTOKEN_CACHE_DIR"), "/opt/probes/tiktoken_cache",
                                  KIT.parent / "agents" / "venv_probe" / "tiktoken_cache"])


def _scenario():
    if os.environ.get("AB05_SCENARIO"):
        return os.environ["AB05_SCENARIO"]
    for base in (KIT / "external", KIT.parent / "run_pc" / "cc-research" / "external", Path("/research/external")):
        files = sorted(glob.glob(str(base / "causalarena" / "scm" / "semantic" / "data" / "semantic_obs_only" / "*.npz")))
        if files:
            return files[0]
    return None


SCENARIO = _scenario()


def _env():
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "OPENAI_API_KEY": SENTINEL})
    if PROBES_ROOT:
        env["PROBES_ROOT"] = PROBES_ROOT
    if PROBES_SRC:
        env["PROBES_SRC"] = PROBES_SRC
    if TIKTOKEN_CACHE:
        env["TIKTOKEN_CACHE_DIR"] = TIKTOKEN_CACHE
    return env


_IMPORT_CACHE = {}


def importable(agent):
    """(ok, reason) - imports the agent the way the runner does, in a fresh interpreter."""
    if agent in _IMPORT_CACHE:
        return _IMPORT_CACHE[agent]
    if not PROBES_ROOT:
        _IMPORT_CACHE[agent] = (False, "no PROBES_ROOT, /opt/probes or local venv_probe/probes found")
        return _IMPORT_CACHE[agent]
    spec = REGISTRY[agent]
    repo = Path(PROBES_SRC or "") / spec["repo_dir"]
    paths = [str(Path(PROBES_ROOT) / agent), str(repo / spec["src_subdir"]) if spec.get("src_subdir") else str(repo)]
    code = "import sys; sys.path[:0] = %r; %s" % (paths, IMPORT_PROBE[agent])
    cwd = tempfile.mkdtemp(prefix="ab05_imp_")
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=_env(), cwd=cwd, timeout=300)
    ok = p.returncode == 0
    reason = "" if ok else ("%s is not importable: %s" % (agent, (p.stderr.strip().splitlines() or ["?"])[-1]))
    _IMPORT_CACHE[agent] = (ok, reason)
    return ok, reason


def run_probe(agent, out, *extra, timeout=1200):
    cmd = [sys.executable, str(RUNNER), "--agent", agent, "--scenario", SCENARIO, "--shuffle-seed", "20261010",
           "--out", str(out), "--stub"] + list(extra)
    return subprocess.run(cmd, capture_output=True, text=True, env=_env(), cwd=str(out.parent), timeout=timeout)


class _Base(unittest.TestCase):
    def need(self, agent):
        if SCENARIO is None:
            self.skipTest("no CausalArena semantic_obs_only file found (set AB05_SCENARIO)")
        ok, reason = importable(agent)
        if not ok:
            self.skipTest(reason)


class TestStubEndToEnd(_Base):
    """Each working adapter runs end to end offline on the first semantic file."""

    def _check(self, agent):
        self.need(agent)
        with tempfile.TemporaryDirectory(prefix="ab05_") as tmp:
            out = Path(tmp) / agent
            p = run_probe(agent, out)
            self.assertEqual(p.returncode, 0, "runner failed:\n" + p.stdout[-2000:] + p.stderr[-2000:])
            s = json.loads((out / "summary.json").read_text())
            for k in REQUIRED_SUMMARY:
                self.assertIn(k, s, "summary.json lacks %s" % k)
            self.assertEqual(s["status"], "ok")
            self.assertIsNone(s["failure_point"])
            self.assertEqual(s["mode"], "stub")
            self.assertGreater(s["calls"], 0)
            self.assertGreater(s["prompt_tokens"], 0)
            self.assertGreater(s["completion_tokens"], 0)
            self.assertGreater(s["est_usd_gpt4o_list"], 0.0)
            self.assertIsInstance(s["directed_f1_random_rule"], float)
            r = json.loads((out / "result.json").read_text())
            d = s["variables"]
            self.assertEqual(sorted(r["perm"]), list(range(d)))
            self.assertIn("directed", r)
            self.assertIn("undecided", r)
            for e in r["directed"]:
                self.assertTrue(0 <= e["from_idx"] < d and 0 <= e["to_idx"] < d)
                self.assertIn("source", e)
            calls = [json.loads(l) for l in (out / "calls.jsonl").read_text().splitlines() if l.strip()]
            self.assertEqual(len(calls), s["calls"])
            for c in calls:
                for k in ("prompt_sha256", "served_model", "usage", "seconds", "request", "response_text"):
                    self.assertIn(k, c)
            for f in out.rglob("*"):
                if f.is_file():
                    self.assertNotIn(SENTINEL, f.read_text(encoding="utf-8", errors="replace"),
                                     "the environment's API key leaked into %s" % f)

    def test_vashishtha(self):
        self._check("vashishtha")

    def test_pywhyllm(self):
        self._check("pywhyllm")

    def test_matmcd(self):
        self._check("matmcd")

    def test_causaliq(self):
        self._check("causaliq")


class TestCaps(_Base):
    """A call cap (and a spending cap) aborts cleanly: exit code 3, state recorded, no exception escapes."""

    def _cap(self, agent, cap):
        self.need(agent)
        with tempfile.TemporaryDirectory(prefix="ab05cap_") as tmp:
            out = Path(tmp) / agent
            p = run_probe(agent, out, "--max-calls", str(cap))
            self.assertEqual(p.returncode, 3, p.stdout[-2000:] + p.stderr[-2000:])
            self.assertNotIn("Traceback", p.stderr)
            s = json.loads((out / "summary.json").read_text())
            self.assertEqual(s["status"], "aborted_cap")
            self.assertEqual(s["calls"], cap)
            self.assertEqual(s["failure_point"]["type"], "CapReached")
            self.assertIn("max_calls", s["failure_point"]["message"])
            lines = [json.loads(l) for l in (out / "calls.jsonl").read_text().splitlines() if l.strip()]
            self.assertEqual(lines[-1].get("event"), "cap_reached")
            self.assertEqual(json.loads((out / "result.json").read_text())["status"], "aborted_cap")

    def test_call_cap_vashishtha(self):
        self._cap("vashishtha", 7)

    def test_call_cap_pywhyllm(self):
        self._cap("pywhyllm", 7)

    def test_call_cap_matmcd(self):
        self._cap("matmcd", 7)

    def test_call_cap_causaliq(self):
        self._cap("causaliq", 0)

    def test_usd_cap_and_resume(self):
        self.need("pywhyllm")
        with tempfile.TemporaryDirectory(prefix="ab05usd_") as tmp:
            out = Path(tmp) / "pywhyllm"
            p = run_probe("pywhyllm", out, "--max-usd", "0.05")
            self.assertEqual(p.returncode, 3, p.stdout[-1500:] + p.stderr[-1500:])
            s = json.loads((out / "summary.json").read_text())
            self.assertEqual(s["status"], "aborted_cap")
            self.assertIn("max_usd", s["failure_point"]["message"])
            self.assertLessEqual(s["est_usd_at_served_prices"], 0.05)
            n1 = s["calls"]
            p = run_probe("pywhyllm", out, "--max-usd", "0.10")          # resume: earlier answers are replayed
            self.assertEqual(p.returncode, 3)
            s2 = json.loads((out / "summary.json").read_text())
            self.assertEqual(s2["replayed_calls"], n1)
            self.assertGreater(s2["calls"], n1)


class TestScoringCopy(unittest.TestCase):
    """harness/probe_io.py's copy of directed_scores agrees with analysis/causalarena_io.py where that is importable."""

    def test_same_as_original(self):
        orig = None
        for base in (KIT / "analysis", KIT.parent / "run_pc" / "cc-research" / "analysis", Path("/research/analysis")):
            if (base / "causalarena_io.py").exists():
                orig = base
                break
        if orig is None:
            self.skipTest("analysis/causalarena_io.py not present")
        sys.path.insert(0, str(HARNESS))
        sys.path.insert(0, str(orig))
        try:
            import causalarena_io as A
            import probe_io as B
        except ImportError as e:
            self.skipTest("numpy not importable in this interpreter: %s" % e)
        truth = {(0, 1), (1, 2), (0, 3), (3, 4)}
        pred = {(1, 0), (1, 2), (2, 4)}
        und = {frozenset({0, 3}), frozenset({3, 4}), frozenset({1, 4})}
        for rule in ("random", "drop", "both", "lower"):
            self.assertEqual(A.directed_scores(pred, und, truth, 5, rule, seed=7),
                             B.directed_scores(pred, und, truth, 5, rule, seed=7))


if __name__ == "__main__":
    unittest.main()
