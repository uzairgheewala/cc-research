"""BEN-09 (BND-07): which declared interventions in CausalArena's released obs+int files move anything.

  python analysis/intervention_audit.py --out analysis/results/intervention_audit/intervention_audit.json

For every released obs+int file of the semantic and formula families (250 each: 800 observational rows, then 200
intervened rows, one target per row; x[:, :, 1] marks the target cell), and for every declared target j:
  target test    two-sample Kolmogorov-Smirnov, values of j in the rows where j is intervened vs the observational rows
  children test  the same for each true child of j (does the intervention propagate?)
Multiple testing: Holm at 1% over all target tests of a family, and separately over all child tests of a family.
A target is "in name only" if its own distribution does not move AND none of its children's does.
The release states the semantics as "do_resampling_and_descendant_recomputation": a resampled root drawn from its own
marginal is expected not to move; the count of roots among targets is reported next to the result.
"""
import argparse
import glob
import json
import os
from pathlib import Path

import numpy as np
from scipy.stats import ks_2samp

ROOT = Path(__file__).resolve().parents[1]


def holm(pvals, alpha):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    reject = [False] * len(pvals)
    m = len(pvals)
    for rank, i in enumerate(order):
        if pvals[i] <= alpha / (m - rank):
            reject[i] = True
        else:
            break
    return reject


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--alpha", type=float, default=0.01)
    a = ap.parse_args()
    out = {"alpha": a.alpha, "families": {}}
    for fam in ("semantic", "formula"):
        files = sorted(glob.glob(str(ROOT / "external" / "causalarena" / "scm" / fam / "data" / ("%s_obs_int" % fam) / "*.npz")))
        tests, ctests = [], []
        for f in files:
            z = np.load(f, allow_pickle=False)
            x, g = z["x"], (z["g"] != 0)
            vals, flags = x[:, :, 0].astype(float), x[:, :, 1] > 0
            n_obs = int(z["n_obs"][0])
            obs = vals[:n_obs]
            for j in np.where(flags.any(0))[0]:
                rows = flags[:, j]
                if rows[:n_obs].any():
                    raise SystemExit("intervened row among the observational block in %s" % f)
                p = ks_2samp(obs[:, j], vals[rows, j]).pvalue
                tests.append({"file": os.path.basename(f), "target": int(j), "is_root": bool(not g[:, j].any()),
                              "n_int_rows": int(rows.sum()), "p": float(p),
                              "children": [int(c) for c in np.where(g[j])[0]]})
                for c in np.where(g[j])[0]:
                    ctests.append({"key": len(tests) - 1, "child": int(c), "p": float(ks_2samp(obs[:, c], vals[rows, c]).pvalue)})
        rt = holm([t["p"] for t in tests], a.alpha)
        rc = holm([t["p"] for t in ctests], a.alpha)
        child_moves = {}
        for t, r in zip(ctests, rc):
            child_moves[t["key"]] = child_moves.get(t["key"], False) or r
        for i, (t, r) in enumerate(zip(tests, rt)):
            t["target_moves"] = bool(r)
            t["any_child_moves"] = bool(child_moves.get(i, False))
            t["in_name_only"] = not t["target_moves"] and not t["any_child_moves"]
        n = len(tests)
        roots = [t for t in tests if t["is_root"]]
        nonroots = [t for t in tests if not t["is_root"]]
        out["families"][fam] = {
            "files": len(files), "declared_target_instances": n,
            "target_moves": sum(t["target_moves"] for t in tests),
            "in_name_only": sum(t["in_name_only"] for t in tests),
            "roots": {"n": len(roots), "target_moves": sum(t["target_moves"] for t in roots),
                      "any_child_moves": sum(t["any_child_moves"] for t in roots), "in_name_only": sum(t["in_name_only"] for t in roots)},
            "non_roots": {"n": len(nonroots), "target_moves": sum(t["target_moves"] for t in nonroots),
                          "any_child_moves": sum(t["any_child_moves"] for t in nonroots), "in_name_only": sum(t["in_name_only"] for t in nonroots)},
            "targets_without_children": sum(1 for t in tests if not t["children"]),
            "tests": tests}
        s = out["families"][fam]
        print(fam, {k: v for k, v in s.items() if k != "tests"})
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
