"""BND-08 / BEN-07: do CausalArena's released variable names encode the causal order?

  python analysis/name_prefix_check.py --out analysis/results/name_prefix/name_prefix.json

For every public semantic obs-only rep000 file: are the node_ids numbered ("V<k>_..."); if so, the share of true edges whose
parent number is below the child's (0.5 expected if the numbering carried no order). Same for the S2 suite's real-name arms.
"""
import argparse
import glob
import json
import os
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PFX = re.compile(r"^[Vv](\d+)_")


def forward_share(names, edges):
    k = [int(PFX.match(n).group(1)) for n in names]
    fwd = sum(k[p] < k[c] for p, c in edges)
    return fwd, len(edges)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = {"tickets": ["BND-08", "BEN-07"], "release": [], "s2": []}
    for f in sorted(glob.glob(str(ROOT / "external" / "causalarena" / "scm" / "semantic" / "data" / "semantic_obs_only" / "*rep000.npz"))):
        z = np.load(f, allow_pickle=False)
        names = [str(x) for x in z["node_ids"]]
        row = {"file": os.path.basename(f), "numbered": all(PFX.match(n) for n in names)}
        if row["numbered"]:
            g = z["g"] != 0                       # g[i, j]: i -> j
            fwd, n = forward_share(names, [(i, j) for i, j in zip(*np.where(g))])
            row.update({"edges": n, "parent_number_lower": fwd, "share": fwd / n})
        out["release"].append(row)
    m = json.loads((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_text(encoding="utf-8"))
    for code, arm in sorted(m["arms"].items()):
        if arm["role"] != "real":
            continue
        labels = arm["column_labels"]
        row = {"code": code, "family": arm["family"], "scenario": arm["scenario_id"], "numbered": all(PFX.match(n) for n in labels)}
        if row["numbered"]:
            R = np.load(ROOT / "datasets" / "suite_q1s2" / arm["reference_by_data"])   # repo convention: R[i, j] = 1 means j -> i
            edges = [(j, i) for i in range(len(labels)) for j in range(len(labels)) if R[i, j] == 1 and R[j, i] != 1]
            fwd, n = forward_share(labels, edges)
            row.update({"edges": n, "parent_number_lower": fwd, "share": fwd / n})
        out["s2"].append(row)
    out["summary"] = {"release_files": len(out["release"]), "release_numbered": [r["file"] for r in out["release"] if r["numbered"]],
                      "s2_numbered": [(r["family"], r.get("parent_number_lower"), r.get("edges")) for r in out["s2"] if r["numbered"]]}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out["summary"], indent=1))
    for r in out["release"]:
        if r["numbered"]:
            print(r["file"], r["parent_number_lower"], "/", r["edges"])


if __name__ == "__main__":
    main()
