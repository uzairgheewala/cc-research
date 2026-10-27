"""INF-10: the wave runner (harness/wave.py) on a demo sheet, run on the host interpreter in a temporary folder.

Must show: a failing canary stops only its own run; a run gated on the canary's must-show is skipped; an unrelated run
still finishes; a second call resumes without re-running finished work; a changed file makes the runner refuse; the
verdict scores must-shows and matches the pre-written decision; pack writes a small zip.
"""
import hashlib, importlib.util, json, sys, tempfile, time, unittest, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def load_wave(root):
    spec = importlib.util.spec_from_file_location("wave_under_test", HERE / "harness" / "wave.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.RESEARCH, mod.ROOT = root, root.parent
    return mod


def py(code):
    return ["python", "-c", code]


class WaveRunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "cc-research"
        (self.root / "out").mkdir(parents=True)
        (self.root / "code.py").write_bytes(b"X = 1\n")          # bytes: text mode writes CRLF on Windows
        man = self.root / "identity.sha256"
        man.write_bytes(("%s  code.py\n" % hashlib.sha256(b"X = 1\n").hexdigest()).encode())
        self.wave = load_wave(self.root)
        d = self.root / "jobs" / "waves" / "T"
        d.mkdir(parents=True)
        counter = "import pathlib; p=pathlib.Path('out/count_%s'); p.write_text(str(int(p.read_text())+1) if p.exists() else '1');"
        self.sheet = {
            "wave": "T", "identity_manifest": "identity.sha256", "code_identity": self.wave.sha_file(man),
            "profiles": {},
            "runs": [
                {"id": "T0", "class": "A0", "profile": "host", "est_min": 0.01,
                 "cmd": py(counter % "T0" + "pathlib.Path('out/tests.json').write_text('{\"ok\": true}')"),
                 "done": {"file": "out/tests.json"}, "decides": ["M_tests"]},
                {"id": "CAN", "class": "A1", "profile": "host", "est_min": 0.01,
                 "cmd": py(counter % "CAN" + "import json; json.dump({'digest': 'bad'}, open('out/canary.json','w')); raise SystemExit(4)"),
                 "done": {"file": "out/canary.json", "contains": "good"}, "decides": ["M_canary"]},
                {"id": "SHORT", "class": "A2", "profile": "host", "est_min": 0.01, "parts": 2,
                 "cmd": py("import sys; k=sys.argv[sys.argv.index('--part')+1].split('/')[0]; open('out/short_%s.json' % k,'w').write('{\"n\": %s}' % k)"),
                 "merge": py("import json; json.dump({'n': sum(json.load(open('out/short_%d.json' % k))['n'] for k in (1,2))}, open('out/short.json','w'))"),
                 "done": {"file": "out/short_{k}.json"}, "decides": ["M_short"]},
                {"id": "HEAVY", "class": "A3", "profile": "host", "est_min": 60, "when": "pass(M_canary)",
                 "cmd": py("open('out/heavy.json','w').write('{}')"), "done": {"file": "out/heavy.json"}},
                {"id": "AFTER", "class": "A3", "profile": "host", "est_min": 1, "depends_on": ["SHORT"],
                 "cmd": py(counter % "AFTER" + "open('out/after.json','w').write('{\"x\": 2}')"), "done": {"file": "out/after.json"}},
            ],
            "must_shows": [
                {"id": "M_tests", "bundle": "A1", "metric": "json", "args": {"file": "out/tests.json", "ptr": ["ok"]}, "bar": {"op": "true"}, "gate": True},
                {"id": "M_canary", "bundle": "A1", "metric": "json", "args": {"file": "out/canary.json", "ptr": ["digest"]}, "bar": {"op": "==", "value": "good"}, "gate": True},
                {"id": "M_short", "bundle": "A1", "metric": "json", "args": {"file": "out/short.json", "ptr": ["n"]}, "bar": {"op": "==", "value": 3}},
            ],
            "decisions": [
                {"if": "pass(M_tests) and fail(M_canary) and skipped(HEAVY)", "then": "canary-mismatch: compare hosts"},
                {"if": "pass(M_canary)", "then": "proceed"},
            ],
            "return_files": ["out/*.json"],
        }
        self.sheet_path = d / "sheet.json"
        self.sheet_path.write_text(json.dumps(self.sheet))

    def tearDown(self):
        self.tmp.cleanup()

    def count(self, rid):
        p = self.root / "out" / ("count_%s" % rid)
        return int(p.read_text()) if p.exists() else 0

    def test_run_gate_resume_score_pack(self):
        W = self.wave.Wave(self.sheet_path, workers=2)
        self.assertEqual(W.run(), 0)
        v = json.loads((self.sheet_path.parent / "verdict.json").read_text())
        self.assertEqual(v["runs"]["T0"]["status"], "ok")
        self.assertEqual(v["runs"]["CAN"]["status"], "failed")          # the canary fails
        self.assertEqual(v["runs"]["HEAVY"]["status"], "skipped")       # its gated heavy run does not start
        self.assertEqual(v["runs"]["SHORT"]["status"], "ok")            # an unrelated run still finishes
        self.assertEqual(v["runs"]["AFTER"]["status"], "ok")
        self.assertEqual(v["must_shows"]["M_short"]["status"], "pass")
        self.assertEqual(v["must_shows"]["M_canary"]["status"], "fail")
        self.assertEqual([d["then"] for d in v["decisions_matched"]], ["canary-mismatch: compare hosts"])
        self.assertFalse((self.root / "out" / "heavy.json").exists())
        # resume: finished runs are not started again
        W2 = self.wave.Wave(self.sheet_path, workers=1)
        W2.run()
        self.assertEqual(self.count("T0"), 1)
        self.assertEqual(self.count("AFTER"), 1)
        self.assertLess(len((self.sheet_path.parent / "verdict.json").read_bytes()), 20000)
        z = self.wave.pack(self.sheet_path)
        names = zipfile.ZipFile(z).namelist()
        self.assertIn("jobs/waves/T/verdict.json", names)
        self.assertIn("out/short.json", names)

    def test_changed_kit_reruns_static_checks_only(self):
        W = self.wave.Wave(self.sheet_path, workers=1)
        W.run()
        self.assertEqual((self.count("T0"), self.count("AFTER")), (1, 1))
        # a new kit: one file changes, the identity manifest and the sheet's code_identity are re-taken
        (self.root / "code.py").write_bytes(b"X = 3\n")
        man = self.root / "identity.sha256"
        man.write_bytes(("%s  code.py\n" % hashlib.sha256(b"X = 3\n").hexdigest()).encode())
        self.sheet["code_identity"] = self.wave.sha_file(man)
        self.sheet_path.write_text(json.dumps(self.sheet))
        W2 = self.wave.Wave(self.sheet_path, workers=1)
        self.assertEqual(W2.run(), 0)
        self.assertEqual(self.count("T0"), 2)                          # the A0 test ran again under the new identity
        self.assertEqual(self.count("AFTER"), 1)                       # the finished A3 run kept its result
        W3 = self.wave.Wave(self.sheet_path, workers=1)
        W3.run()
        self.assertEqual(self.count("T0"), 2)                          # same identity: not again

    def test_refuses_changed_code(self):
        (self.root / "code.py").write_bytes(b"X = 2\n")
        W = self.wave.Wave(self.sheet_path)
        self.assertEqual(W.run(), 2)
        self.assertEqual(self.count("T0"), 0)
        v = json.loads((self.sheet_path.parent / "verdict.json").read_text())
        self.assertFalse(v["identity"]["ok"])
        self.assertIn("code.py", v["identity"]["changed_or_missing"])

    def test_validation(self):
        bad = dict(self.sheet)
        bad["runs"] = [dict(r) for r in self.sheet["runs"]]
        bad["runs"][3]["when"] = "pass(M_canary) and ok(HEAVY2)"
        bad["runs"][1]["when"] = "ok(SHORT) and"           # trailing operator
        bad["runs"].append({"id": "LIVE", "class": "L", "profile": "host", "cmd": ["x"], "done": {"file": "x"}})
        problems = self.wave.validate(bad)
        self.assertTrue(any("cap_usd" in p for p in problems))
        self.assertTrue(any("CAN" in p for p in problems))
        cyc = dict(self.sheet)
        cyc["runs"] = [dict(r) for r in self.sheet["runs"]]
        cyc["runs"][1]["when"] = "ok(HEAVY)"                # HEAVY reads M_canary, decided by CAN
        self.assertTrue(any("cycle" in p for p in self.wave.validate(cyc)))

    def test_between_op(self):
        self.assertTrue(self.wave.OPS["between"](0.81, [0.80, 0.82]))
        self.assertFalse(self.wave.OPS["between"](0.79, [0.80, 0.82]))

    def test_docker_argv(self):
        s = dict(self.sheet)
        s["profiles"] = {"kernel": {"image": "img:1", "env": {"OPENBLAS_CORETYPE": "SKYLAKEX"}, "mounts": []}}
        s["runs"] = [{"id": "K", "class": "A2", "profile": "kernel", "cmd": ["python", "a.py"], "mem_gb": 2.2,
                      "done": {"file": "x"}}]
        self.sheet_path.write_text(json.dumps(s))
        W = self.wave.Wave(self.sheet_path)
        W.state["env_overrides"] = {"OPENBLAS_CORETYPE": "HASWELL"}
        argv, _ = W.argv(s["runs"][0])
        self.assertEqual(argv[:8], ["docker", "run", "--rm", "--init", "--name", "wave-t-k", "--network", "none"])
        self.assertIn("OPENBLAS_CORETYPE=HASWELL", argv)
        self.assertIn("3g", argv)
        self.assertEqual(argv[-3:], ["img:1", "python", "a.py"])


class WaveLimitsTest(unittest.TestCase):
    """Rerun 3 (21 Oct): a hung image build blocked the sheet for 15 hours and the Docker engine stopped answering.
    Must show: a run past its wall limit or silent past its stall limit is stopped and recorded (not a result) and its
    dependents are skipped; the next call starts it again; runs needing Docker wait while the engine is down and the
    runner stops with exit 3 after the wait, starting nothing that needs it; a failure while the engine is down is
    recorded as infra, not as a result; an exclusive run never shares the machine."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "cc-research"
        (self.root / "out").mkdir(parents=True)
        self.wave = load_wave(self.root)
        self.dir = self.root / "jobs" / "waves" / "L"
        self.dir.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def sheet(self, runs):
        s = {"wave": "L", "profiles": {}, "runs": runs, "must_shows": [], "decisions": [], "return_files": []}
        sp = self.dir / "sheet.json"
        sp.write_text(json.dumps(s))
        return sp

    def test_timeout_and_stall_stop_runs(self):
        sp = self.sheet([
            {"id": "HANG", "class": "A1", "profile": "host", "est_min": 0.01, "timeout_min": 0.05,
             "cmd": py("import time; time.sleep(60)"), "done": {"file": "out/hang.json"}},
            {"id": "QUIET", "class": "A1", "profile": "host", "est_min": 0.01, "stall_min": 0.05,
             "cmd": py("import time; print('start', flush=True); time.sleep(60)"), "done": {"file": "out/quiet.json"}},
            {"id": "NEXT", "class": "A2", "profile": "host", "est_min": 0.01, "depends_on": ["HANG"],
             "cmd": py("open('out/next.json','w').write('{}')"), "done": {"file": "out/next.json"}}])
        t0 = time.time()
        self.assertEqual(self.wave.Wave(sp, workers=2).run(), 0)
        self.assertLess(time.time() - t0, 40)
        st = json.loads((self.dir / "state.json").read_text())["runs"]
        self.assertEqual(st["HANG"]["status"], "timeout")
        self.assertEqual(st["QUIET"]["status"], "stalled")
        self.assertEqual(st["NEXT"]["status"], "skipped")
        self.assertIn("stopped by the runner (timeout", (self.dir / "logs" / "HANG.log").read_text())
        # a later call starts the stopped run again (here it is fixed to finish)
        s = json.loads(sp.read_text())
        s["runs"][0]["cmd"] = py("open('out/hang.json','w').write('{}')")
        sp.write_text(json.dumps(s))
        self.wave.Wave(sp, workers=1, only={"HANG", "NEXT"}).run()
        st = json.loads((self.dir / "state.json").read_text())["runs"]
        self.assertEqual((st["HANG"]["status"], st["NEXT"]["status"]), ("ok", "ok"))

    def test_docker_down_waits_then_stops(self):
        self.wave.docker_alive = lambda timeout=30: False
        self.wave.DOCKER_WAIT_S = 3
        sp = self.sheet([
            {"id": "BUILD", "class": "A1", "profile": "host", "uses_docker": True, "est_min": 0.01,
             "cmd": py("open('out/build.json','w').write('{}')"), "done": {"file": "out/build.json"}},
            {"id": "PLAIN", "class": "A1", "profile": "host", "est_min": 0.01,
             "cmd": py("open('out/plain.json','w').write('{}')"), "done": {"file": "out/plain.json"}}])
        self.assertEqual(self.wave.Wave(sp, workers=1).run(), 3)
        st = json.loads((self.dir / "state.json").read_text())
        self.assertNotIn("BUILD", st["runs"])                          # never started
        self.assertFalse((self.root / "out" / "build.json").exists())
        self.assertEqual(st["runs"]["PLAIN"]["status"], "ok")          # work without Docker went ahead
        self.assertEqual(st["host"]["halted"], "docker")

    def test_failure_while_engine_down_is_infra(self):
        answers = iter([True, False])
        self.wave.docker_alive = lambda timeout=30: next(answers, False)
        self.wave.DOCKER_WAIT_S = 2
        sp = self.sheet([{"id": "B", "class": "A1", "profile": "host", "uses_docker": True, "est_min": 0.01,
                          "cmd": py("raise SystemExit(1)"), "done": {"file": "out/b.json"}}])
        self.wave.Wave(sp, workers=1).run()
        st = json.loads((self.dir / "state.json").read_text())["runs"]
        self.assertEqual(st["B"]["status"], "infra")

    def test_exclusive_runs_alone(self):
        stamp = "import json,time,pathlib; t0=time.time(); time.sleep(1.5); pathlib.Path('out/%s.json').write_text(json.dumps([t0, time.time()]))"
        sp = self.sheet([
            {"id": "BIG", "class": "A1", "profile": "host", "exclusive": True, "est_min": 0.01, "cmd": py(stamp % "big"),
             "done": {"file": "out/big.json"}},
            {"id": "S1", "class": "A1", "profile": "host", "est_min": 0.02, "cmd": py(stamp % "s1"), "done": {"file": "out/s1.json"}},
            {"id": "S2", "class": "A1", "profile": "host", "est_min": 0.03, "cmd": py(stamp % "s2"), "done": {"file": "out/s2.json"}}])
        self.assertEqual(self.wave.Wave(sp, workers=3).run(), 0)
        big = json.loads((self.root / "out" / "big.json").read_text())
        for k in ("s1", "s2"):
            a, b = json.loads((self.root / "out" / ("%s.json" % k)).read_text())
            self.assertTrue(b <= big[0] + 0.3 or a >= big[1] - 0.3, k)   # no overlap with the exclusive run


if __name__ == "__main__":
    unittest.main()
