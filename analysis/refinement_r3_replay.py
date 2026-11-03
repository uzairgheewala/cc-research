"""BLD-22 held-out battery H3: Causal-Copilot's bootstrap step replayed on a CausalArena replicate never replayed before. No LLM.

Tickets: BLD-22, ADV-01

The same cell as analysis/bootstrap_replay_family.py (imported unchanged: PC with wrapper defaults, 20 resamples, seed 0,
neutral labels V01..), on replicate --replicate (default 1) of every scenario of one split and family, instead of replicate 0.
Replicate 0 of the test split (H1) was read by BND-10 and BLD-06's data part; replicates 1-9 have never been replayed, so
replicate 1 of the test split is the first battery the direction rule meets without anyone having looked at it.
Its scenarios (and graphs) are the test split's; its samples are new. The formula family's columns are permuted per file with
--shuffle-seed (seed + crc32(file name)), as in the earlier formula replays.

  python harness/compute_job.py --job jobs/r3_heldout_semantic_rep1.json      (in the container: cc.ps1 compute r3_heldout_semantic_rep1.json)
"""
import argparse
import contextlib
import glob
import io
import json
import os
import signal
import sys
import traceback
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
sys.path.insert(0, str(HERE))
import bootstrap_replay_family as BRF  # noqa: E402   (unchanged: its cell() is the replay)
import causalarena_io as CA  # noqa: E402
import jobkit  # noqa: E402


def files_for(fam, split, rep):
    want = set(json.load(open(RESEARCH / "plans" / "splits.json", encoding="utf-8"))["families"][fam][split])
    root = RESEARCH / "external" / "causalarena" / "scm" / fam / "data" / ("%s_obs_only" % fam)
    tag = "rep%03d" % rep
    files = sorted(f for f in glob.glob(str(root / ("*__%s.npz" % tag)))
                   if any(f.endswith("_%s__%s_obs_only__%s.npz" % (s, fam, tag)) for s in want))
    if len(files) != len(want):
        sys.exit("expected %d files for %s %s %s, found %d" % (len(want), fam, split, tag, len(files)))
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=("dev", "test"))
    ap.add_argument("--family", required=True, choices=("semantic", "formula"))
    ap.add_argument("--replicate", type=int, default=1)
    ap.add_argument("--shuffle-seed", type=int, default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--repo", default="/app" if os.path.isdir("/app/postprocess") else str(RESEARCH.parent / "Causal-Copilot"))
    ap.add_argument("--file-timeout-s", type=int, default=1200)
    ap.add_argument("--budget-s", type=float, default=0)
    a = ap.parse_args()
    if a.replicate == 0:
        sys.exit("refused: replicate 0 is the earlier replays' (H1); use bootstrap_replay_family.py")
    out = Path(a.out) if Path(a.out).is_absolute() else RESEARCH / a.out
    files = files_for(a.family, a.split, a.replicate)
    parts, budget = jobkit.Parts(out), jobkit.Budget(a.budget_s)
    sys.path[:0] = [a.repo, os.path.join(a.repo, "externals", "causal-learn")]
    cwd = os.getcwd()
    os.chdir(a.repo)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import causal_discovery.wrappers  # noqa: F401
            import postprocess.judge_functions  # noqa: F401
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
        vals, truth = np.asarray(s["values"]), CA.to_repo_matrix(s["g"])
        perm = None
        if a.shuffle_seed is not None:
            perm = np.random.default_rng(a.shuffle_seed + zlib.crc32(key.encode())).permutation(vals.shape[1])
            vals, truth = vals[:, perm], np.asarray(truth)[np.ix_(perm, perm)]
        df = pd.DataFrame(vals, columns=["V%02d" % (k + 1) for k in range(vals.shape[1])])
        os.chdir(a.repo)
        try:
            signal.signal(signal.SIGALRM, BRF._alarm)
            signal.alarm(a.file_timeout_s)
            try:
                r = BRF.cell(df, truth)
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
        r.update({"file": key, "scenario": s["meta"]["scenario_id"], "domain": s["meta"]["domain_id"], "split": a.split,
                  "replicate": a.replicate})
        if perm is not None:
            r.update({"perm": [int(x) for x in perm], "truth_repo": np.asarray(truth).astype(int).tolist()})
        parts.add(key, r)
        print("%s %s" % (key[:70], r["status"]), flush=True)
    header = {"tickets": ["BLD-22"], "battery": "H3" if a.split == "test" else "dev+", "split": a.split, "family": a.family,
              "replicate": a.replicate, "shuffle_seed": a.shuffle_seed, "files": len(files),
              "errors": sum(1 for r in parts.done.values() if r.get("status") != "ok"),
              "method": "PC wrapper defaults; bootstrap 20 resamples; seed 0 (bootstrap_replay_family.cell, unchanged)",
              "columns": ("released order" if a.shuffle_seed is None else "permuted per file (seed + crc32(file name))") + ", neutral labels V01..",
              "env": jobkit.environment()}
    jobkit.finish(parts, header, len(files))


if __name__ == "__main__":
    main()
