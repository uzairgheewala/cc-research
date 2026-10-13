"""R2-sortability of CausalArena's public files and the R2-SortnRegress baseline (Reisach et al., NeurIPS 2023).

R2 of a variable = coefficient of determination when it is regressed on all other variables (ordinary least squares).
R2-sortability = share of true edges whose effect has the larger R2 (0.5 = no information; ties count half).
R2-SortnRegress = sort variables by increasing R2, then regress each on its predecessors in that order (same rule
as causalarena_order_baseline.py: OLS, two-sided 1% t-test) and orient earlier -> later. It reads nothing but the
numbers and does not depend on column order.

No LLM. python causalarena_sortability.py --root external/causalarena --out analysis/results/causalarena_calibration
"""
import argparse
import glob
import json
import os
import statistics as st
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
from causalarena_order_baseline import order_regression  # noqa: E402


def r2_all(X):
    n, d = X.shape
    out = np.zeros(d)
    for j in range(d):
        A = np.column_stack([np.ones(n), np.delete(X, j, axis=1)])
        beta, *_ = np.linalg.lstsq(A, X[:, j], rcond=None)
        res = X[:, j] - A @ beta
        tss = float(((X[:, j] - X[:, j].mean()) ** 2).sum())
        out[j] = 1.0 - float(res @ res) / tss if tss > 0 else 0.0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = {}
    for fam in ("semantic", "formula"):
        per = {}
        for f in sorted(glob.glob(os.path.join(a.root, "scm", fam, "data", "*obs_only*", "*.npz"))):
            s = CA.load(f)
            X, g = s["values"], s["g"]
            d = g.shape[0]
            truth = CA.true_edges(g)
            r2 = r2_all(X)
            sortab = sum(1.0 if r2[e] > r2[c] else (0.5 if r2[e] == r2[c] else 0.0) for c, e in truth) / len(truth)
            order = np.argsort(r2, kind="stable")              # increasing R2
            pred_sorted = order_regression(X[:, order])
            pred = {(int(order[i]), int(order[j])) for i, j in pred_sorted}
            sc = CA.directed_scores(pred, set(), truth, d, "drop")
            sc["r2_sortability"] = sortab
            per.setdefault(s["meta"].get("scenario_id", os.path.basename(f)), []).append(sc)
        m = lambda k: round(st.mean(st.mean(x[k] for x in v) for v in per.values()), 3)
        out[fam] = {"scenarios": len(per), "r2_sortability_mean": m("r2_sortability"),
                    "r2_sortability_min_max": [round(min(st.mean(x["r2_sortability"] for x in v) for v in per.values()), 3),
                                               round(max(st.mean(x["r2_sortability"] for x in v) for v in per.values()), 3)],
                    "r2_sortnregress": {k: m(k) for k in ("precision", "recall", "f1", "shd")}}
        print(fam, json.dumps(out[fam]))
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "sortability.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
