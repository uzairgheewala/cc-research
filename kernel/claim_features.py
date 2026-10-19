"""K4 claim features (kernel v3): what the ledger itself knows about how trustworthy each DV-1 answer is.

A DV-1 answer is "if t is set, does y move?": yes when y is reachable from t through committed arrows, no when y is
unreachable even through open pairs. Its correctness depends on every claim on the paths it rests on, so its features
are summaries of those claims, all computed from the ledger alone (no truth):

  yes answers                                   no answers
  n_paths       directed paths t -> y (cap 50)   open_paths     paths t -> y using at least one open pair (cap 50)
  path_len      length of the shortest path       skel_dist      undirected skeleton distance t - y (cap 6, 7 = none)
  weakest_lic   weakest licence on the best path  deg_t, deg_y   skeleton degrees
                (v_structure 3, meek_r2/r3 2,
                 meek_r1 1, other 0)
  min_score     smallest |GES score delta| on the best path
  max_p         largest CI-test p of a pair on the best path (its own recorded test with the largest p)
  r1_on_path    1 if every path uses a meek_r1 arrow
plus, when row-resample stability is available (K0 cache, B = 10), the share of resamples giving the same answer.
"""
import numpy as np

LIC = {"v_structure": 3, "meek_r2": 2, "meek_r3": 2, "meek_r1": 1}


def _paths(n, D, src, dst, cap=50, extra=()):
    nxt = {v: [] for v in range(n)}
    for a, b in D:
        nxt[a].append(b)
    for a, b in extra:
        nxt[a].append(b)
        nxt[b].append(a)
    out = []
    steps = [0]

    def dfs(u, path):
        steps[0] += 1
        if len(out) >= cap or steps[0] > 20000:      # bounded: a count, not an enumeration
            return
        if u == dst:
            out.append(list(path))
            return
        for v in sorted(nxt[u]):
            if v not in path and len(path) < 12:
                path.append(v)
                dfs(v, path)
                path.pop()
    dfs(src, [src])
    return out


def ledger_edges(led):
    pos = {v["name"]: v["position"] for v in led["variables"]}
    ev = {e["id"]: e for e in led["evidence"]}
    D, U, lic, score, pmax = set(), set(), {}, {}, {}
    for c in led["claims"]:
        a, b = pos[c["x"]], pos[c["y"]]
        if c["relation"] == "none":
            continue
        k = tuple(sorted((a, b)))
        sc = [abs(ev[e]["score"]) for e in c["evidence"] if e in ev and ev[e]["type"] == "score_delta"]
        ps = [ev[e]["p_value"] for e in c["evidence"] if e in ev and ev[e]["type"] == "ci_test"]
        score[k] = min(sc) if sc else 0.0
        pmax[k] = max(ps) if ps else 0.0
        if c["relation"] == "x->y":
            D.add((a, b))
            lic[(a, b)] = LIC.get(c["licensed_by"], 0)
        else:
            U.add(k)
    return D, U, lic, score, pmax


def features(led, targets, claims):
    """claims: {(t, y): bool} (dv.claims output). -> {(t, y): feature vector (list of floats)} and the feature names."""
    n = len(led["variables"])
    D, U, lic, score, pmax = ledger_edges(led)
    deg = np.zeros(n)
    for a, b in list(D) + list(U):
        deg[a] += 1
        deg[b] += 1
    skel = {v: set() for v in range(n)}
    for a, b in list(D) + list(U):
        skel[a].add(b)
        skel[b].add(a)

    def dist(s, t):
        seen, front, d = {s}, [s], 0
        while front and d < 6:
            d += 1
            nxt = []
            for u in front:
                for v in skel[u]:
                    if v == t:
                        return d
                    if v not in seen:
                        seen.add(v)
                        nxt.append(v)
            front = nxt
        return 7
    out = {}
    for (t, y), v in claims.items():
        if v:
            ps = _paths(n, D, t, y)
            best = min(ps, key=len) if ps else [t, y]
            edges = list(zip(best, best[1:]))
            f = [1.0, len(ps), len(best) - 1, min(lic.get(e, 0) for e in edges), min(score.get(tuple(sorted(e)), 0.0) for e in edges),
                 max(pmax.get(tuple(sorted(e)), 0.0) for e in edges), float(all(any(lic.get(e, 0) == 1 for e in zip(p, p[1:])) for p in ps)),
                 0.0, 0.0, deg[t], deg[y]]
        else:
            op = _paths(n, D, t, y, extra=U)
            f = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, len(op), dist(t, y), deg[t], deg[y]]
        out[(t, y)] = f
    return out


NAMES = ["is_yes", "n_paths", "path_len", "weakest_lic", "min_score", "max_p", "r1_on_path", "open_paths", "skel_dist", "deg_t", "deg_y"]
