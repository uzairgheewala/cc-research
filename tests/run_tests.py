"""Run the unit tests and record the outcome in tests/last_run.json (INF-05 check)."""
import datetime, json, sys, unittest
from pathlib import Path

here = Path(__file__).resolve().parent
suite = unittest.defaultTestLoader.discover(str(here))
res = unittest.TextTestRunner(verbosity=1).run(suite)
json.dump({"ran": res.testsRun, "failures": len(res.failures), "errors": len(res.errors), "ok": res.wasSuccessful(),
           "python": sys.version.split()[0], "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
          open(here / "last_run.json", "w"), indent=1)
sys.exit(0 if res.wasSuccessful() else 1)
