"""Why the triangle filter (L8a) is precise on formula and not on semantic: the links it would cut at cut-off 0.7, by
what they are (dev, D; post hoc diagnosis, not pre-registered).

For every cut link: its label; for true links, whether the truth itself has a triangle there (a real direct link next to
a real path); whether either end is discrete (<= 10 values) or has a mass point (>= 1% on one value); and the cut link's
strength rank inside its weakest triangle.

  python analysis/q2_linkfilt_diag.py -> analysis/results/q2_v3/linkfilt_diag_dev.json
"""
import gzip, json, sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
RES = ROOT / "analysis" / "results" / "q2_v3"
CUT = 0.7


def main():
    from score import bench
    rows = defaultdict(list)
    with gzip.open(RES / "linkfilt_l8_links_dev.jsonl.gz", "rt") as fh:
        for line in fh:
            r = json.loads(line)
            rows[r["family"]].append(r)
    out = {}
    for fam, files in rows.items():
        paths = {p.name: p for p in bench.files(fam, split="dev")}
        c = Counter()
        by_type = defaultdict(Counter)
        for f in files:
            I = bench.truth_info(fam, f["file"])
            X = np.asarray(bench.load(str(paths[f["file"]]))["values"], dtype=float)
            T = I["T"]
            tadj = {frozenset(e) for e in T}
            nbT = defaultdict(set)
            for a, b in T:
                nbT[a].add(b)
                nbT[b].add(a)
            disc = [len(np.unique(X[:, j])) <= 10 for j in range(X.shape[1])]
            mass = [np.unique(X[:, j], return_counts=True)[1].max() / len(X) >= 0.01 for j in range(X.shape[1])]
            for l in f["links"]:
                if l["L8a"] is None:
                    continue
                a, b = l["a"], l["b"]
                kind = "discrete_end" if (disc[a] or disc[b]) else ("masspoint_end" if (mass[a] or mass[b]) else "continuous")
                cut = l["L8a"] < CUT
                by_type[kind]["in_triangle"] += 1
                by_type[kind]["in_triangle_false"] += l["label"] != "true"
                if not cut:
                    continue
                by_type[kind]["cut"] += 1
                by_type[kind]["cut_false"] += l["label"] != "true"
                c["cut"] += 1
                c["cut_" + l["label"]] += 1
                if l["label"] == "true":
                    true_tri = bool((nbT[a] & nbT[b]) and frozenset((a, b)) in tadj)
                    c["cut_true_in_true_triangle" if true_tri else "cut_true_no_true_triangle"] += 1
        d = {"cut_off": CUT, "cuts": dict(c),
             "by_pair_type": {k: {"in_triangle": v["in_triangle"], "false_share_in_triangle": round(v["in_triangle_false"] / v["in_triangle"], 3),
                                  "cuts": v["cut"], "cut_precision": round(v["cut_false"] / v["cut"], 3) if v["cut"] else None}
                              for k, v in by_type.items()}}
        out[fam] = d
        print("==", fam, json.dumps(d, indent=1))
    json.dump(out, open(RES / "linkfilt_diag_dev.json", "w"), indent=1)


if __name__ == "__main__":
    main()
