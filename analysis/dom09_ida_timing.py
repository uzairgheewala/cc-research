"""DOM-09 (timing half, BND-06): how long 'what if we set X?' answers take at 25 variables, with local IDA on a PC CPDAG.

  python analysis/dom09_ida_timing.py --out analysis/results/dom09/ida_timing.json

Scenario: backup_frequency_ransomware_loss (semantic, dev split, 25 variables, replicate 0). Graph: the CPDAG PC returned
on it in BND-06 (analysis/results/methods/pc_semantic_obs_rel.json: committed arrows + undecided pairs). Data: the same file.
Local IDA (Maathuis, Kalisch and Buehlmann 2009, Annals of Statistics 37(6A)): for every X, every set S of X's undirected
neighbours such that S together with X's parents creates no new v-structure at X (every member of S adjacent to every other
member of S and to every parent); the effect of X on Y for that parent set is the OLS coefficient of X in Y ~ X + pa + S
(0 if Y is in that set). Output: per (X, Y) the multiset of possible effects. Recorded: wall time, number of candidate
parent sets per X, the share of ordered pairs whose multiset holds one distinct value (identified up to the class), and the
share where the adjustment by X's TRUE parents is among the candidate sets (does the class contain the right answer).
The semantic SCMs are not all linear: the numbers are timing and identification counts, not effect accuracy.
"""
import argparse
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402

FILE = "semantic_cybersecurity_and_it_operations_backup_frequency_ransomware_loss__semantic_obs_only__rep000.npz"


def ols_coef(Xmat, y):
    beta, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(y)), Xmat]), y, rcond=None)
    return float(beta[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = json.load(open(ROOT / "analysis" / "results" / "methods" / "pc_semantic_obs_rel.json", encoding="utf-8"))["rows"]
    r = next(x for x in rows if x["file"] == FILE)
    s = CA.load(ROOT / "external" / "causalarena" / "scm" / "semantic" / "data" / "semantic_obs_only" / FILE)
    X = np.asarray(s["values"], dtype=float)
    d = X.shape[1]
    directed = {tuple(e) for e in r["directed_edges"]}
    und = {frozenset(u[:2]) for u in r["undecided_pairs"]}
    adj = lambda u, v: (u, v) in directed or (v, u) in directed or frozenset((u, v)) in und
    g = np.asarray(s["g"]) != 0                      # g[i, j]: i -> j
    t0 = time.time()
    cand, multisets = {}, {}
    for x in range(d):
        pa = sorted(u for (u, v) in directed if v == x)
        sib = sorted(u for p in und if x in p for u in p if u != x)
        sets = []
        for k in range(len(sib) + 1):
            for S in itertools.combinations(sib, k):
                if all(adj(u, v) for u, v in itertools.combinations(S, 2)) and all(adj(u, p) for u in S for p in pa):
                    sets.append(sorted(set(pa) | set(S)))
        cand[x] = sets
        for y in range(d):
            if y == x:
                continue
            multisets[(x, y)] = [0.0 if y in Z else ols_coef(X[:, [x] + Z], X[:, y]) for Z in sets]
    secs = time.time() - t0
    true_in = 0
    for x in range(d):
        tp = sorted(np.where(g[:, x])[0].tolist())
        true_in += int(tp in cand[x])
    ident = sum(1 for v in multisets.values() if len({round(e, 10) for e in v}) == 1)
    out = {"ticket": "DOM-09", "bundle": "BND-06", "file": FILE, "variables": d, "rows": int(X.shape[0]),
           "graph": "PC CPDAG from analysis/results/methods/pc_semantic_obs_rel.json (released column order)",
           "committed_arrows": len(directed), "undecided_pairs": len(und), "seconds_all_pairs": round(secs, 3),
           "ordered_pairs": len(multisets), "candidate_parent_sets_per_X": {str(k): len(v) for k, v in cand.items()},
           "max_candidate_sets": max(len(v) for v in cand.values()),
           "pairs_with_one_distinct_value": ident, "share_identified_in_class": round(ident / len(multisets), 4),
           "X_whose_true_parents_are_a_candidate_set": true_in,
           "note": "timing and identification counts only; the semantic SCMs are not all linear, so the OLS values are not checked against true effects"}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "candidate_parent_sets_per_X"}, indent=1))


if __name__ == "__main__":
    main()
