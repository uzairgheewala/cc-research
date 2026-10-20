"""INF-10: the wave runner (harness/wave.py) on a demo sheet, run on the host interpreter in a temporary folder.

Must show: a failing canary stops only its own run; a run gated on the canary's must-show is skipped; an unrelated run
still finishes; a second call resumes without re-running finished work; a changed file makes the runner refuse; the
verdict scores must-shows and matches the pre-written decision; pack writes a small zip.
"""
import hashlib, importlib.util, json, sys, tempfile, unittest, zipfile
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

    def test_docker_argv(self):
        s = dict(self.sheet)
        s["profiles"] = {"kernel": {"image": "img:1", "env": {"OPENBLAS_CORETYPE": "SKYLAKEX"}, "mounts": []}}
        s["runs"] = [{"id": "K", "class": "A2", "profile": "kernel", "cmd": ["python", "a.py"], "mem_gb": 2.2,
                      "done": {"file": "x"}}]
        self.sheet_path.write_text(json.dumps(s))
        W = self.wave.Wave(self.sheet_path)
        W.state["env_overrides"] = {"OPENBLAS_CORETYPE": "HASWELL"}
        argv, _ = W.argv(s["runs"][0])
        self.assertEqual(argv[:6], ["docker", "run", "--rm", "--init", "--network", "none"])
        self.assertIn("OPENBLAS_CORETYPE=HASWELL", argv)
        self.assertIn("3g", argv)
        self.assertEqual(argv[-3:], ["img:1", "python", "a.py"])


if __name__ == "__main__":
    unittest.main()
