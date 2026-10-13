"""BND-08 part a: replay Causal-Copilot's bootstrap step on CausalArena semantic files (no LLM, no cost). Prediction M1.

For replicate 0 of every public semantic scenario in one split, with the repo's OWN functions, unmodified (as in
refinement_offline.py, which gate B validated against live runs):
  causal_discovery.wrappers.PC({}).fit(df)                 -> S0 (wrapper defaults)
  postprocess.judge_functions.bootstrap(..., boot_num=20)  -> resample frequencies
  postprocess.judge_functions.bootstrap_recommend          -> buckets
  lineage.step_bootstrap                                   -> S1 (the edits of judge.py:68-86)
The seven bootstrap frequency tables are stored per file (input to refinement v1).
KCI pruning and the LLM review are not run. Scores: adjacency and directed-edge F1 of S0 and S1 against the release's graph.
Columns keep the released order (only adjacency F1 enters M1; stated in the output header).

The split is a required argument and each split writes its own output. The test-split output is produced but must not be
opened before BND-10 (F3): its sha256 is recorded by the job runner, and BND-08 reports M1 on the dev split only.

  python /research/harness/compute_job.py --job /research/jobs/bootstrap_replay_ca_dev.json      (in the container)
"""
import argparse
import contextlib
import glob
import io
import json
import logging
import os
import random
import signal
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
import cc_graph as G  # noqa: E402
import jobkit  # noqa: E402

M1 = {"text": "M1: the bootstrap step lowers adjacency F1 below the algorithm's own output (PC, no LLM)",
      "supported_if_share_at_least": 0.80, "refuted_if_share_at_most": 0.50}


class FileTimeout(Exception):
    pass


def _alarm(signum, frame):
    raise FileTimeout("file exceeded the per-file limit")


def cell(df, truth_repo, seed=0):
    import causal_discovery.wrappers as W
    import postprocess.judge_functions as jf
    from lineage import step_bootstrap
    p = df.shape[1]
    E = G.truth_edges(truth_repo)
    random.seed(seed)
    np.random.seed(seed)
    sink = io.StringIO()
    logging.disable(logging.CRITICAL)
    t = time.time()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        S0, _info, _raw = W.PC({}).fit(df)
        S0 = np.asarray(S0)
        fit_s = time.time() - t
        _rec, boot = jf.bootstrap(data=df, full_graph=S0, algorithm="PC", hyperparameters={}, boot_num=20, ts=False, parallel=False)
        buckets = jf.bootstrap_recommend(S0, boot)
        S1, added, deleted = step_bootstrap(S0, buckets)
    s0, s1 = G.score(S0, E, p), G.score(S1, E, p)
    return {"p": p, "true_edges": len(E), "fit_s": round(fit_s, 1), "total_s": round(time.time() - t, 1),
            "S0_adjacencies": int(sum(G.is_adjacent(S0, a, b) for a, b in G.pairs(p))),
            "S1_adjacencies": int(sum(G.is_adjacent(S1, a, b) for a, b in G.pairs(p))),
            "bootstrap_added": len(added), "bootstrap_deleted_pairs": len({tuple(sorted(x)) for x in deleted}),
            "score_S0": s0, "score_S1": s1, "S0": S0.astype(int).tolist(), "S1": S1.astype(int).tolist(),
            # the seven resample-frequency tables (repo layout: M[i, j] is the frequency of the type on j -> i), so that
            # refinement v1 (BND-09/10) can be replayed on these files without rerunning the bootstrap
            "boot": {k: np.round(np.asarray(v, dtype=float), 4).tolist() for k, v in boot.items()}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=("dev", "test"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--repo", default="/app" if os.path.isdir("/app/postprocess") else str(RESEARCH.parent / "Causal-Copilot"))
    ap.add_argument("--file-timeout-s", type=int, default=1200)
    ap.add_argument("--budget-s", type=float, default=0)
    a = ap.parse_args()
    out = Path(a.out) if Path(a.out).is_absolute() else RESEARCH / a.out
    splits = json.load(open(RESEARCH / "plans" / "splits.json", encoding="utf-8"))["families"]["semantic"]
    want = set(splits[a.split])
    root = RESEARCH / "external" / "causalarena" / "scm" / "semantic" / "data" / "semantic_obs_only"
    files = sorted(f for f in glob.glob(str(root / "*__rep000.npz"))
                   if any(f.endswith("_%s__semantic_obs_only__rep000.npz" % s) for s in want))
    if len(files) != len(want):
        sys.exit("expected %d files for split %s, found %d" % (len(want), a.split, len(files)))
    parts = jobkit.Parts(out)
    budget = jobkit.Budget(a.budget_s)
    sys.path[:0] = [a.repo, os.path.join(a.repo, "externals", "causal-learn")]
    cwd = os.getcwd()
    # Environment problems are not data: import everything once and stop the job if anything is missing (exit 2),
    # instead of recording one "error" row per file and completing.
    os.chdir(a.repo)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import causal_discovery.wrappers  # noqa: F401
            import postprocess.judge_functions  # noqa: F401
            from lineage import step_bootstrap  # noqa: F401
    except Exception as e:  # noqa: BLE001
        print("ENVIRONMENT-ERROR %s: %s" % (type(e).__name__, e))
        sys.exit(2)
    finally:
        os.chdir(cwd)
    for f in files:
        key = os.path.basename(f)
        if parts.has(key):
            continue
        if not budget.ok(30):
            break
        s = CA.load(f)
        df = pd.DataFrame(s["values"], columns=["V%02d" % (k + 1) for k in range(len(s["node_ids"]))])
        truth = CA.to_repo_matrix(s["g"])
        os.chdir(a.repo)
        try:
            signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(a.file_timeout_s)
            try:
                r = cell(df, truth)
            finally:
                signal.alarm(0)
            r["status"] = "ok"
        except (ImportError, KeyboardInterrupt, SystemExit):
            raise
        except BaseException as e:  # noqa: BLE001  (algorithm failures and timeouts are data)
            tb = traceback.extract_tb(e.__traceback__)
            r = {"status": "error", "error": "%s: %s" % (type(e).__name__, str(e)[:300]),
                 "where": "%s:%d" % (tb[-1].filename, tb[-1].lineno) if tb else None}
        finally:
            os.chdir(cwd)
        r.update({"file": key, "scenario": s["meta"]["scenario_id"], "domain": s["meta"]["domain_id"], "split": a.split})
        parts.add(key, r)
        print("%s %s" % (key[:70], r["status"]), flush=True)
    header = {"split": a.split, "files": len(files), "errors": sum(1 for r in parts.done.values() if r.get("status") != "ok"), "method": "PC wrapper defaults; bootstrap 20 resamples; seed 0",
              "columns": "released order, neutral labels V01..", "M1": M1, "env": jobkit.environment()}
    jobkit.finish(parts, header, len(files))


if __name__ == "__main__":
    main()
