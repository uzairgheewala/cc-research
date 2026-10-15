"""K6 views of a ledger (D1.5). Every view is computed from the claims alone, through variable names and declared
positions, so it is covered by the same permutation test as the claims (failure mode Z2).

  graph_sets(led)          committed arrows and open pairs in the caller's column positions (for scoring)
  scoreboard_row(led, seed)  directed edges after the expectation rule (open pairs at random, per-file seed), the
                           scoreboard's export; the ledger itself keeps the pairs open
  claim_list(led)          one line per adjacent pair: relation, source, licence, engines, conflict
"""
import numpy as np


def graph_sets(led):
    pos = {v["name"]: v["position"] for v in led["variables"]}
    D, U = set(), set()
    for c in led["claims"]:
        if c["relation"] == "x->y":
            D.add((pos[c["x"]], pos[c["y"]]))
        elif c["relation"] in ("x-y", "x<->y"):
            U.add(tuple(sorted((pos[c["x"]], pos[c["y"]]))))
    return D, U


def scoreboard_row(led, seed):
    D, U = graph_sets(led)
    rng = np.random.default_rng(seed)
    out = set(D)
    for a, b in sorted(U):
        out.add((a, b) if rng.integers(2) == 0 else (b, a))
    return sorted(out)


def claim_list(led):
    rows = []
    for c in led["claims"]:
        if c["relation"] == "none":
            continue
        rows.append({"x": c["x"], "y": c["y"], "relation": c["relation"], "source": c["direction_source"],
                     "licence": c["licensed_by"], "engines": c["engines"], "conflict": c["conflict"]})
    return sorted(rows, key=lambda r: (r["x"], r["y"]))
