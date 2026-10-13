"""Does the column order of CausalArena's released files give away edge directions?

Check 1 (no model): share of true edges whose cause sits in an earlier column than its effect.
Check 2 (a deliberately naive method that READS the column order): regress every variable on all variables
in earlier columns (ordinary least squares), keep predecessors with |t| above the two-sided 1% point, and
orient each kept pair earlier -> later. Scored like every other method (directed-edge precision/recall/F1, SHD).
Control: the same method after a seeded shuffle of the columns (truth permuted alongside), which removes the
order information and nothing else.

No LLM. python causalarena_order_baseline.py --root external/causalarena --out analysis/results/causalarena_calibration
"""
import argparse
import glob
import json
import os
import statistics as st
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402

ALPHA = 0.01
SEED = 20261007


def order_regression(X, alpha=ALPHA):
    n, d = X.shape
    pred = set()
    for j in range(1, d):
        A = np.column_stack([np.ones(n), X[:, :j]])
        beta, *_ = np.linalg.lstsq(A, X[:, j], rcond=None)
        resid = X[:, j] - A @ beta
        dof = n - A.shape[1]
        if dof <= 0:
            continue
        s2 = float(resid @ resid) / dof
        cov = s2 * np.linalg.pinv(A.T @ A)
        se = np.sqrt(np.clip(np.diag(cov), 1e-300, None))
        t = beta / se
        crit = stats.t.ppf(1 - alpha / 2, dof)
        for i in range(j):
            if abs(t[i + 1]) > crit:
                pred.add((i, j))
    return pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = {"alpha": ALPHA, "shuffle_seed": SEED, "families": {}}
    for fam in ("semantic", "formula"):
        files = sorted(glob.glob(os.path.join(a.root, "scm", fam, "data", "*obs_only*", "*.npz")))
        rng = np.random.default_rng(SEED)
        fw = tot = 0
        per = {"as_released": {}, "columns_shuffled": {}, "all_pairs_earlier_to_later": {}}
        for f in files:
            s = CA.load(f)
            X, g = s["values"], s["g"]
            d = g.shape[0]
            truth = CA.true_edges(g)
            fw += sum(1 for i, j in truth if i < j)
            tot += len(truth)
            key = s["meta"].get("scenario_id", os.path.basename(f))
            per["as_released"].setdefault(key, []).append(CA.directed_scores(order_regression(X), set(), truth, d, "drop"))
            per["all_pairs_earlier_to_later"].setdefault(key, []).append(
                CA.directed_scores({(i, j) for i in range(d) for j in range(i + 1, d)}, set(), truth, d, "drop"))
            perm = rng.permutation(d)                       # new column k holds old column perm[k]
            inv = np.argsort(perm)
            truth_p = {(int(inv[i]), int(inv[j])) for i, j in truth}
            per["columns_shuffled"].setdefault(key, []).append(
                CA.directed_scores(order_regression(X[:, perm]), set(), truth_p, d, "drop"))
        res = {"files": len(files), "scenarios": len(per["as_released"]), "true_edges": tot,
               "true_edges_cause_in_earlier_column": fw, "share": (fw / tot) if tot else None}
        for name, groups in per.items():
            res[name] = {m: round(st.mean(st.mean(x[m] for x in v) for v in groups.values()), 3)
                         for m in ("precision", "recall", "f1", "shd")}
            res[name]["f1_scm_std"] = round(st.pstdev([st.mean(x["f1"] for x in v) for v in groups.values()]), 3)
        out["families"][fam] = res
        print(fam, json.dumps(res))
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "order_baseline.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
