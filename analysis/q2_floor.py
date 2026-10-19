"""The missed-link floor (kernel v3, K1): for every true link the frozen v2 kernel (rule C3) misses on a dev file, is
there any conditional dependence a test could detect, if it were handed the right conditioning set?

For a true link P -> C, the oracle conditioning set is C's other true parents: in the true graph P and C are adjacent,
and conditioning on the other parents removes every other path from P to C that runs through C's parents. Two oracle
tests, both at alpha 0.05:
  linear    Fisher z on the partial correlation of P and C given the other parents (the engines' own test family;
            well calibrated here: it rejects only 10% of shadow pairs given the descendant's true parents, dev check)
  flexible  cross-fitted gradient-boosting residuals of P and C on the other parents, residual dependence by rank
            correlation and binned chi-square (kernel.recover.flex_test); more power on nonlinear mechanisms but
            anti-conservative here (it rejects 81% of shadow pairs given the true parents), so an upper bound
and the same linear test on the scenario's five replicates pooled (5,000 rows).

Classes of a missed link (reported per family, with counts and shares):
  floor            no oracle test detects it at 1,000 rows, nor the linear test at 5,000: no usable signal
  sample_size      only the pooled linear test detects it: more rows of the same system would
  method_linear    the linear oracle detects it at 1,000 rows: the right conditioning set was not found (search gap)
  method_nonlinear only the flexible oracle detects it: a nonlinear test with the right set would (upper bound)
Dev split only; reads the engine cache (kernel.cache, read-only) and the dev files.

  python analysis/q2_floor.py --family semantic  -> analysis/results/q2_v3/floor_dev_semantic.json
"""
import argparse, json, multiprocessing as mp, os, sys
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))


def one(args):
    path, family = args
    import numpy as np
    from score import bench
    from kernel import build as B, cache, recover, views, harness
    s = bench.load(path)
    X, names, name = s["values"], list(s["node_ids"]), Path(path).name
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    if led is None:
        return {"file": name, "failure": "pc"}
    D, U = views.graph_sets(led)
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    I = bench.truth_info(family, name)
    T = I["T"]
    rep0 = path.split("__rep")[0] + "__rep000.npz"
    Xp, _ = harness.pooled_table(rep0)
    bat, batp = recover.Battery(X), recover.Battery(Xp)
    out = []
    for p_, c in sorted(T):
        if frozenset((p_, c)) in adj:
            continue
        others = sorted(x for x, y in T if y == c and x != p_)
        lin = bat.test(p_, c, others)["p0"]
        linp = batp.test(p_, c, others)["p0"]
        flex = recover.flex_test(X, p_, c, others)["p"]
        cls = ("method_linear" if lin <= 0.05 else "method_nonlinear" if flex <= 0.05 else "sample_size" if linp <= 0.05 else "floor")
        out.append({"edge": [int(p_), int(c)], "n_other_parents": len(others), "p_linear": lin, "p_flexible": flex, "p_linear_pooled": linp,
                    "discrete": bool(bat.disc[p_] or bat.disc[c]), "class": cls})
    return {"file": name, "scenario": bench.scenario_of(name), "true_links": len(T), "missed": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=("semantic", "formula"))
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    from score import bench
    fs = [str(p) for p in bench.files(a.family, split="dev")]
    fs = fs[: a.limit] if a.limit else fs
    with mp.get_context("fork").Pool(a.workers) as pool:
        rows = [r for r in pool.map(one, [(f, a.family) for f in fs]) if "failure" not in r]
    T = sum(r["true_links"] for r in rows)
    miss = [m for r in rows for m in r["missed"]]
    cls = {}
    for m in miss:
        cls[m["class"]] = cls.get(m["class"], 0) + 1
    out = {"family": a.family, "split": "dev", "files": len(rows), "true_links": T, "missed": len(miss), "missed_share": len(miss) / T,
           "classes": {k: {"count": v, "share_of_missed": v / len(miss), "share_of_true_links": v / T} for k, v in sorted(cls.items())},
           "discrete_share_of_floor": (sum(1 for m in miss if m["class"] == "floor" and m["discrete"]) / max(1, cls.get("floor", 0))),
           "rows": rows}
    p = ROOT / "analysis" / "results" / "q2_v3" / ("floor_dev_%s.json" % a.family)
    p.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(p, "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))


if __name__ == "__main__":
    main()
