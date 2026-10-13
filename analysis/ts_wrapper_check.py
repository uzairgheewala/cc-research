"""AUD-14 (BND-03): one offline run of each time-series wrapper, as a no-cost compute job (no LLM, no network).

  cc.ps1 compute aud14_ts_wrappers.json      (in the container: python /research/harness/compute_job.py --job ...)

For each wrapper in causal_discovery.wrappers.ts_algorithms (PCMCI, VARLiNGAM, DYNOTEARS, GrangerCausality, NTSNOTEARS) at
a31aa7c, unmodified, with its default hyperparameters ({}), on the repo's own sample data/dataset/sim_ts/data.csv (3 variables,
lag 3), under three column-name forms:
  as_read    the names pandas reads from the file ("0", "1", "2": strings)
  int        the same names as Python integers
  named      "x0", "x1", "x2" (what a real dataset looks like)
Recorded per (wrapper, form): status ok / error, exception type, message and the innermost repo file:line, wall time, and the
type and shape of every value fit() returns (program.py:53 unpacks three). This checks the static AUD-14 findings: Granger
needs integer column names; NTSNOTEARS needs externals/ (absent from the static copy, present in the image or not).
"""
import argparse
import contextlib
import io
import os
import signal
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import jobkit  # noqa: E402


class FileTimeout(Exception):
    pass


def _alarm(signum, frame):
    raise FileTimeout("wrapper exceeded the time limit")


def describe(v):
    if isinstance(v, np.ndarray):
        return {"type": "ndarray", "shape": list(v.shape)}
    if isinstance(v, pd.DataFrame):
        return {"type": "DataFrame", "shape": list(v.shape)}
    if isinstance(v, dict):
        return {"type": "dict", "keys": sorted(map(str, v))[:12]}
    return {"type": type(v).__name__}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--repo", default="/app" if os.path.isdir("/app/postprocess") else str(HERE.parents[1] / "Causal-Copilot"))
    ap.add_argument("--timeout-s", type=int, default=600)
    ap.add_argument("--budget-s", type=float, default=0)
    a = ap.parse_args()
    out = Path(a.out) if Path(a.out).is_absolute() else HERE.parent / a.out
    parts, budget = jobkit.Parts(out), jobkit.Budget(a.budget_s)
    sys.path[:0] = [a.repo, os.path.join(a.repo, "externals", "causal-learn")]
    cwd = os.getcwd()
    os.chdir(a.repo)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import causal_discovery.wrappers as W
    except Exception as e:  # noqa: BLE001
        print("ENVIRONMENT-ERROR %s: %s" % (type(e).__name__, e))
        sys.exit(2)
    finally:
        os.chdir(cwd)
    base = pd.read_csv(Path(a.repo) / "data" / "dataset" / "sim_ts" / "data.csv")
    forms = {"as_read": list(base.columns), "int": [int(c) for c in base.columns], "named": ["x%d" % k for k in range(base.shape[1])]}
    items = [(w, f) for w in W.ts_algorithms for f in forms]
    for w, f in items:
        key = "%s|%s" % (w, f)
        if parts.has(key):
            continue
        if not budget.ok(30):
            break
        df = base.copy()
        df.columns = forms[f]
        rec = {"wrapper": w, "names": f, "columns": [str(c) for c in forms[f]], "columns_type": type(forms[f][0]).__name__}
        t = time.time()
        os.chdir(a.repo)
        sink = io.StringIO()
        try:
            signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(a.timeout_s)
            try:
                with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                    cls = getattr(W, w)
                    ret = cls({}).fit(df)
            finally:
                signal.alarm(0)
            rets = list(ret) if isinstance(ret, tuple) else [ret]
            rec.update({"status": "ok", "returns": len(rets), "return_values": [describe(v) for v in rets],
                        "program_py_53_unpacks_3": len(rets) == 3})
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as e:  # noqa: BLE001  wrapper failures are the data here
            tb = traceback.extract_tb(e.__traceback__)
            repo_frames = [fr for fr in tb if fr.filename.startswith(a.repo)]
            fr = (repo_frames or tb)[-1] if tb else None
            rec.update({"status": "error", "error": "%s: %s" % (type(e).__name__, str(e)[:300]),
                        "where": "%s:%d" % (os.path.relpath(fr.filename, a.repo), fr.lineno) if fr else None,
                        "innermost": "%s:%d" % (tb[-1].filename, tb[-1].lineno) if tb else None})
        finally:
            os.chdir(cwd)
        rec["seconds"] = round(time.time() - t, 1)
        rec["stdout_tail"] = sink.getvalue()[-300:]
        parts.add(key, rec)
        print(key, rec["status"], rec.get("error", ""), flush=True)
    header = {"ticket": "AUD-14", "bundle": "BND-03", "data": "data/dataset/sim_ts/data.csv", "wrappers": list(W.ts_algorithms),
              "forms": {k: [str(c) for c in v] for k, v in forms.items()}, "hyperparameters": "{} (wrapper defaults)",
              "env": jobkit.environment()}
    jobkit.finish(parts, header, len(items))


if __name__ == "__main__":
    main()
