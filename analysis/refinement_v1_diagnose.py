"""Exploratory (after the BND-10 test read; changes nothing frozen): why v1 falls below the algorithm's own adjacency F1.

  python analysis/refinement_v1_diagnose.py --out analysis/results/refinement_v1/diagnosis_test_live_s2.json

For each live S2 table: adjacencies of S0 that v1 drops (connected < KEEP) split into true / false by the data reference, and
the pairs v1 adds (connected >= ADD) split the same way; the connected-frequency of dropped true edges.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import refinement_v1 as R  # noqa: E402
import refinement_v1_test_live as L  # noqa: E402
import cc_graph as G  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = {"label": "exploratory, post-test", "rows": []}
    tot = {"dropped_true": 0, "dropped_false": 0, "added_true": 0, "added_false": 0, "kept_true": 0, "kept_false": 0}
    conn_dropped_true = []
    for it in L.items("s2"):
        S0, boot, E, p = np.asarray(it["S0"]), it["boot"], it["E"], it["p"]
        und = {frozenset(e) for e in E}
        V, _ = R.v1(S0, boot)
        none = np.asarray(boot["none_existence"], dtype=float)
        c = dict.fromkeys(tot, 0)
        for x, y in G.pairs(p):
            a0, a1, t = G.is_adjacent(S0, x, y), G.is_adjacent(V, x, y), frozenset((x, y)) in und
            if a0 and not a1:
                c["dropped_true" if t else "dropped_false"] += 1
                if t:
                    conn_dropped_true.append(round(1 - float(none[x, y]), 3))
            elif a0 and a1:
                c["kept_true" if t else "kept_false"] += 1
            elif a1:
                c["added_true" if t else "added_false"] += 1
        for k in tot:
            tot[k] += c[k]
        out["rows"].append({"key": it["key"], "family": it["family"], "role": it["group"].split(":")[-1], **c})
    out["totals"] = tot
    out["connected_of_dropped_true_edges"] = {"n": len(conn_dropped_true), "values": sorted(conn_dropped_true)}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out["totals"]), out["connected_of_dropped_true_edges"]["n"], np.percentile(conn_dropped_true, [10, 50, 90]) if conn_dropped_true else None)


if __name__ == "__main__":
    main()
