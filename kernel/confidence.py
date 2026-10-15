"""Confidence, calibration and the selective view (bundle B4; D4.1-D4.3; guarantee G8).

K5  bootstrap(X, names, rule, B, seed): B row resamples with replacement (seeded); the frozen kernel is rebuilt on each;
    every DV-1 claim of the full-data ledger gets the share of resamples whose ledger makes the same claim
    ("T moves Y" / "T does not move Y"), and every adjacency claim the share giving the same relation.
    This is a stability measure. It becomes a probability only through a calibration map.
Map isotonic regression (pool-adjacent-violators, NumPy only) of correctness on stability, fitted on dev scenarios of one
    family and frozen with its sha256 before any held-out read. Evaluated out of fold on dev (folds by scenario).
View for a cost ratio c/g, act on claims whose calibrated probability is >= c/(g + c) (AB-04's usefulness threshold);
    at a coverage target, keep the most probable claims until the target share of all target-outcome pairs is reached.
"""
import json

import numpy as np


def isotonic_fit(x, y, w=None):
    """Pool-adjacent-violators on points sorted by x. Returns breakpoints (xs, ys) of the non-decreasing step function."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.ones_like(x) if w is None else np.asarray(w, dtype=float)
    o = np.argsort(x, kind="mergesort")
    x, y, w = x[o], y[o], w[o]
    ux, inv = np.unique(x, return_inverse=True)
    sw = np.bincount(inv, weights=w)
    sy = np.bincount(inv, weights=w * y)
    blocks = [[sy[i] / sw[i], sw[i], [ux[i]]] for i in range(len(ux))]
    out = []
    for b in blocks:
        out.append(b)
        while len(out) > 1 and out[-2][0] > out[-1][0]:
            v2, w2, x2 = out.pop()
            v1, w1, x1 = out.pop()
            out.append([(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, x1 + x2])
    xs, ys = [], []
    for v, _, xx in out:
        for xi in xx:
            xs.append(float(xi))
            ys.append(float(v))
    return {"x": xs, "y": ys}


def isotonic_apply(m, x):
    """Step interpolation: the value at the largest fitted x <= query (below the first point: the first value)."""
    xs, ys = np.asarray(m["x"]), np.asarray(m["y"])
    x = np.asarray(x, dtype=float)
    k = np.searchsorted(xs, x, side="right") - 1
    k = np.clip(k, 0, len(xs) - 1)
    return ys[k]


def bootstrap(X, names, rule, B=10, seed=20261015, dv_targets=None):
    """-> {"dv": {(t, y): share}, "rel": {(a, b): {relation: share}}, "B": B} over the caller's column positions."""
    from kernel import build as Bld, views
    from score import dv
    X = np.asarray(X, dtype=float)
    n, d = X.shape
    rng = np.random.default_rng(seed)
    dv_counts, rel_counts, done = {}, {}, 0
    for b in range(B):
        idx = rng.integers(0, n, n)
        led, info = Bld.build(X[idx], names, rule=rule, created_utc="")
        if led is None:
            continue
        done += 1
        D, U = views.graph_sets(led)
        if dv_targets is not None:
            for k, v in dv.claims(d, D, U, dv_targets).items():
                dv_counts[(k, v)] = dv_counts.get((k, v), 0) + 1
        for c in led["claims"]:
            key = tuple(sorted((c["x"], c["y"])))
            r = "none" if c["relation"] == "none" else ("x-y" if c["relation"] == "x-y" else "%s->%s" % (c["x"], c["y"]))
            rel_counts.setdefault(key, {})
            rel_counts[key][r] = rel_counts[key].get(r, 0) + 1
    return {"B": B, "completed": done, "seed": seed,
            "dv": {"%d>%d:%s" % (t, y, "yes" if v else "no"): c / done for ((t, y), v), c in dv_counts.items()} if done else {},
            "rel": {"%s|%s" % k: {r: c / done for r, c in v.items()} for k, v in rel_counts.items()} if done else {}}


def save_map(m, path, meta):
    rec = dict(meta, map=m)
    s = json.dumps(rec, indent=1, sort_keys=True)
    open(path, "w").write(s)
    import hashlib
    return hashlib.sha256(s.encode()).hexdigest()
