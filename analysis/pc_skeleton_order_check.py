"""BND-06 side check: is PC's column-order dependence (bnd06_interim.md, Q4c) a property of the causal-learn build we run?

  PYTHONPATH=<causal-learn root> python analysis/pc_skeleton_order_check.py --label vendored --out <json> [--every 10]

Runs causal-learn PC (stable=True, Fisher-z, alpha 0.05) on every k-th public semantic obs-only file in the released column
order and in the BND-06 shuffled order (default_rng(20261010 + crc32(file name))), maps the shuffled graph back, and counts
files whose skeleton (unordered adjacencies) differs between the two orders. Run once with the Causal-Copilot vendored
causal-learn 0.1.3.8 and once with upstream causal-learn (pip) to see whether the dependence comes from the build.
Reading of the vendored code (externals/causal-learn/causallearn/utils/PCUtils/SkeletonDiscovery.py, skeleton_discovery and
_process_node_pair): each unordered pair is tested once, as (x, y) with x < y, and conditioning sets are drawn from
adj(x) \\ {y} only; textbook PC also tries subsets of adj(y) \\ {x}. Which variable gets the lower index is the column order.
No LLM. Per-file limit via SIGALRM (default 120 s): a file over it is reported, not scored.
"""
import argparse
import contextlib
import glob
import io
import json
import os
import signal
import sys
import time
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402


def skeleton(G):
    d = G.shape[0]
    return {(i, j) for i in range(d) for j in range(i + 1, d) if G[i, j] != 0 or G[j, i] != 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--every", type=int, default=10)
    ap.add_argument("--timeout-s", type=int, default=120)
    a = ap.parse_args()
    import causallearn
    from causallearn.search.ConstraintBased.PC import pc
    root = HERE.parent / "external" / "causalarena" / "scm" / "semantic" / "data" / "semantic_obs_only"
    files = sorted(glob.glob(str(root / "*.npz")))[::a.every]

    def _alarm(signum, frame):
        raise TimeoutError
    signal.signal(signal.SIGALRM, _alarm)
    rows = []
    for f in files:
        key = os.path.basename(f)
        s = CA.load(f)
        X, d = s["values"], len(s["node_ids"])
        perm = list(np.random.default_rng(20261010 + zlib.crc32(key.encode())).permutation(d))
        out = {"file": key, "d": d}
        try:
            t0 = time.time()
            signal.alarm(a.timeout_s)
            with contextlib.redirect_stdout(io.StringIO()):
                G0 = pc(X, alpha=0.05, indep_test="fisherz", stable=True, show_progress=False).G.graph
                G1 = pc(X[:, perm], alpha=0.05, indep_test="fisherz", stable=True, show_progress=False).G.graph
            signal.alarm(0)
            out["seconds"] = round(time.time() - t0, 2)
        except Exception as e:  # noqa: BLE001
            signal.alarm(0)
            out["error"] = "%s: %s" % (type(e).__name__, e)
            rows.append(out)
            continue
        s0 = skeleton(G0)
        s1 = {tuple(sorted((int(perm[i]), int(perm[j])))) for i, j in skeleton(G1)}
        truth = {tuple(sorted(e)) for e in CA.true_edges(s["g"])}
        out.update({"adjacencies_released": len(s0), "adjacencies_shuffled": len(s1), "symmetric_difference": len(s0 ^ s1),
                    "true_adjacencies": len(truth), "skeleton_tp_released": len(s0 & truth), "skeleton_tp_shuffled": len(s1 & truth)})
        rows.append(out)
    ok = [r for r in rows if "error" not in r]
    res = {"label": a.label, "causallearn_file": causallearn.__file__, "files": len(rows), "scored": len(ok),
           "files_with_different_skeleton": sum(1 for r in ok if r["symmetric_difference"]),
           "mean_symmetric_difference": round(sum(r["symmetric_difference"] for r in ok) / len(ok), 3) if ok else None,
           "skeleton_tp_released_total": sum(r["skeleton_tp_released"] for r in ok),
           "skeleton_tp_shuffled_total": sum(r["skeleton_tp_shuffled"] for r in ok),
           "adjacencies_released_total": sum(r["adjacencies_released"] for r in ok),
           "adjacencies_shuffled_total": sum(r["adjacencies_shuffled"] for r in ok), "rows": rows}
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}))


if __name__ == "__main__":
    main()
