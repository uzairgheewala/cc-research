"""Run the unit tests and record the outcome in tests/last_run.json (INF-05 check).

  python tests/run_tests.py                                   all tests -> tests/last_run.json
  python tests/run_tests.py --out FILE [--pattern test_x*.py]  a wave sheet's record elsewhere (INF-10), last_run.json untouched
"""
import argparse, datetime, json, sys, unittest
from pathlib import Path

here = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--out", default=str(here / "last_run.json"))
ap.add_argument("--pattern", default="test*.py")
a = ap.parse_args()
suite = unittest.defaultTestLoader.discover(str(here), pattern=a.pattern)
res = unittest.TextTestRunner(verbosity=1).run(suite)
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
json.dump({"ran": res.testsRun, "failures": len(res.failures), "errors": len(res.errors), "skipped": len(res.skipped),
           "ok": res.wasSuccessful(), "pattern": a.pattern, "python": sys.version.split()[0],
           "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
          open(a.out, "w"), indent=1)
sys.exit(0 if res.wasSuccessful() else 1)
