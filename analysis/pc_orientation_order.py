"""Why does PC orient worse when columns arrive in causal order? Mechanism check for the AUD-28 re-score.

PC's skeleton (stable variant) does not depend on column order, but on CausalArena's released files its commit accuracy
q is about 0.59 against about 0.74 with shuffled columns. Hypothesis: with finite-sample tests, collider decisions
conflict, and the conflict-resolution step (uc_priority) resolves conflicts in index order, which in causal order
systematically favours wrong arrowheads. Prediction (written before the run): with orientation rules designed to be
order independent of conflicts (maxP, uc_rule=1; definite maxP, uc_rule=2), the released/shuffled gap in q shrinks to
under 0.03; with the default (uc_rule=0, uc_priority=2) it stays near 0.15.

  python analysis/pc_orientation_order.py --causal-learn PATH --root external/causalarena --files-every 2

Upstream causal-learn only (PATH as for pc_upstream_run.py). Same shuffle as the runner (seed 20261010 + crc32 of the
file name). Writes analysis/results/rescore/pc_orientation_order.json. No model calls.
Tickets: AUD-28, REP-07
"""
import argparse, json, os, statistics as st, sys, zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402

CONFIGS = [("default uc_rule=0 uc_priority=2", 0, 2), ("uc_sepset, overwrite uc_priority=0", 0, 0),
           ("maxP uc_rule=1", 1, 3), ("definite maxP uc_rule=2", 2, 3)]


def orient(g, perm):
    """causal-learn graph -> directed set and undirected set in original indices."""
    d = len(perm)
    directed, und = set(), set()
    for i in range(d):
        for j in range(i + 1, d):
            a, b = g[i, j], g[j, i]
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                directed.add((perm[i], perm[j]))
            elif a == 1 and b == -1:
                directed.add((perm[j], perm[i]))
            else:
                und.add(frozenset((perm[i], perm[j])))
    return directed, und


def coords(directed, und, T):
    tadj = {frozenset(e) for e in T}
    padj = {frozenset(e) for e in directed} | und
    tp = len(tadj & padj)
    right = sum(1 for e in directed if e in T)
    wrong = sum(1 for e in directed if (e[1], e[0]) in T)
    P = tp / len(padj) if padj else 0
    R = tp / len(tadj) if tadj else 0
    S = 2 * P * R / (P + R) if P + R else 0
    return {"S": S, "c": (right + wrong) / tp if tp else 0, "q": right / (right + wrong) if right + wrong else None,
            "a": (right + 0.5 * (tp - right - wrong)) / tp if tp else 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--causal-learn", required=True)
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--family", default="semantic")
    ap.add_argument("--files-every", type=int, default=2)
    ap.add_argument("--seed", type=int, default=20261010)
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.causal_learn).resolve()))
    from causallearn.search.ConstraintBased.PC import pc
    folder = Path(a.root) / "scm" / a.family / "data" / ("%s_obs_only" % a.family)
    files = sorted(os.listdir(folder))[:: a.files_every]
    res = {c[0]: {"released": [], "shuffled": []} for c in CONFIGS}
    skipped = 0
    for f in files:
        s = CA.load(folder / f)
        X = s["values"][: s["n_obs"]]
        T = CA.true_edges(s["g"])
        d = X.shape[1]
        perm = list(np.random.default_rng(a.seed + zlib.crc32(f.encode())).permutation(d))
        try:
            one = {name: {arm: coords(*orient(pc(X[:, p], 0.05, "fisherz", stable=True, uc_rule=rule, uc_priority=prio,
                                                show_progress=False).G.graph, p), T)
                          for arm, p in (("released", list(range(d))), ("shuffled", perm))}
                   for name, rule, prio in CONFIGS}
        except ValueError:      # singular correlation matrix: the file is skipped in every configuration and arm
            skipped += 1
            continue
        for name, arms in one.items():
            for arm, c in arms.items():
                res[name][arm].append(c)
    out = {"tickets": ["AUD-28", "REP-07"], "family": a.family, "files": len(files), "skipped_singular": skipped,
           "prediction": "gap in q (shuffled - released) < 0.03 for maxP and definite maxP; about 0.15 for the default",
           "configs": {}}
    for name, v in res.items():
        m = {arm: {k: round(st.mean([x[k] for x in xs if x[k] is not None]), 4) for k in ("S", "c", "q", "a")} for arm, xs in v.items()}
        m["q_gap_shuffled_minus_released"] = round(m["shuffled"]["q"] - m["released"]["q"], 4)
        m["files"] = len(v["released"])
        out["configs"][name] = m
        print("%-36s n=%d  q released %.3f shuffled %.3f gap %+.3f   S %.3f/%.3f  c %.3f/%.3f" % (
            name, m["files"], m["released"]["q"], m["shuffled"]["q"], m["q_gap_shuffled_minus_released"],
            m["released"]["S"], m["shuffled"]["S"], m["released"]["c"], m["shuffled"]["c"]))
    os.makedirs(HERE / "results" / "rescore", exist_ok=True)
    json.dump(out, open(HERE / "results" / "rescore" / "pc_orientation_order.json", "w"), indent=1)


if __name__ == "__main__":
    main()
