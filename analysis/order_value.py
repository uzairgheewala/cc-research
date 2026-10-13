"""How much is coarse knowledge of causal ORDER worth? (no LLM; oracle knowledge taken from the true graph)

Takes plain PC's output on the public semantic files (published configuration, pc_rows_v2.jsonl) and re-orients its
adjacencies using a partial order of the variables given as tiers: an adjacency between two tiers is oriented
earlier -> later; inside a tier PC's own decision is kept, undecided pairs follow the scoreboard's random rule.
Tiers are cut from the true depth (longest path from a root): k equal-width depth bins, or "inputs versus the rest"
(inputs = variables with no cause in the graph), or the full depth. This is an upper bound on what tier knowledge of
that granularity can add to this skeleton; it says nothing yet about who could supply such knowledge correctly.
Also reports the regression-on-earlier-variables method under the same partial orders (a variable is regressed on
all variables in strictly earlier tiers).
"""
import argparse, glob, json, os, statistics as st, sys, zlib
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
from scipy import stats  # noqa: E402


def depth(d, E):
    par = {v: [] for v in range(d)}
    for c, e in E:
        par[e].append(c)
    memo = {}
    def dep(v):
        if v not in memo:
            memo[v] = 0 if not par[v] else 1 + max(dep(p) for p in par[v])
        return memo[v]
    return [dep(v) for v in range(d)]


def bins(dep, k):
    dmax = max(dep)
    return [min(k - 1, int(x * k / (dmax + 1))) for x in dep]


def tier_regression(X, tier, alpha=0.01):
    n, d = X.shape
    pred = set()
    for j in range(d):
        prev = [i for i in range(d) if tier[i] < tier[j]]
        if not prev:
            continue
        A = np.column_stack([np.ones(n), X[:, prev]])
        beta, *_ = np.linalg.lstsq(A, X[:, j], rcond=None)
        res = X[:, j] - A @ beta
        dof = n - A.shape[1]
        cov = float(res @ res) / dof * np.linalg.pinv(A.T @ A)
        t = beta / np.sqrt(np.clip(np.diag(cov), 1e-300, None))
        crit = stats.t.ppf(1 - alpha / 2, dof)
        pred |= {(prev[i], j) for i in range(len(prev)) if abs(t[i + 1]) > crit}
    return pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--pc", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = {}
    for f in glob.glob(os.path.join(a.root, "scm", "semantic", "data", "semantic_obs_only", "*.npz")):
        s = CA.load(f)
        data[os.path.basename(f)] = (s["values"], CA.true_edges(s["g"]))
    names = ["none", "inputs vs rest", "2 depth bins", "3 depth bins", "5 depth bins", "full depth"]
    res = {n: {"pc": {}, "reg": {}, "ordered": {}, "tiers": {}} for n in names}
    for line in open(a.pc, encoding="utf-8"):
        r = json.loads(line)
        if r["alpha"] != 0.05:
            continue
        X, E = data[r["file"]]
        d = r["d"]
        dep = depth(d, E)
        schemes = {"none": [0] * d, "inputs vs rest": [0 if x == 0 else 1 for x in dep], "2 depth bins": bins(dep, 2),
                   "3 depth bins": bins(dep, 3), "5 depth bins": bins(dep, 5), "full depth": dep}
        dire = {tuple(e) for e in r["directed_edges"]}
        und = [tuple(sorted(e)) for e in r["undirected_pairs"]]
        for name, t in schemes.items():
            pred, undec = set(), set()
            for x, y in list(dire) + und:
                if t[x] < t[y]:
                    pred.add((x, y))
                elif t[y] < t[x]:
                    pred.add((y, x))
                elif (x, y) in dire:
                    pred.add((x, y))
                else:
                    undec.add(frozenset((x, y)))
            f1 = CA.directed_scores(pred, undec, E, d, "random", seed=zlib.crc32(r["file"].encode()))["f1"]
            res[name]["pc"].setdefault(r["scenario"], []).append(f1)
            res[name]["ordered"].setdefault(r["scenario"], []).append(sum(1 for c, e in E if t[c] < t[e]) / len(E))
            res[name]["tiers"].setdefault(r["scenario"], []).append(len(set(t)))
            if name != "none":
                res[name]["reg"].setdefault(r["scenario"], []).append(
                    CA.directed_scores(tier_regression(X, t), set(), E, d, "drop")["f1"])
    mm = lambda g: round(st.mean(st.mean(v) for v in g.values()), 3) if g else None
    table = [{"order knowledge": n, "mean number of tiers": mm(res[n]["tiers"]), "share of true edges it orders": mm(res[n]["ordered"]),
              "PC skeleton re-oriented, F1": mm(res[n]["pc"]), "regression on earlier tiers, F1": mm(res[n]["reg"])} for n in names]
    os.makedirs(a.out, exist_ok=True)
    json.dump(table, open(os.path.join(a.out, "order_value.json"), "w", encoding="utf-8"), indent=1)
    for row in table:
        print(row)


if __name__ == "__main__":
    main()
