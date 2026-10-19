"""Headroom ladder: how much each stage's errors cost at the answer level (dev, from the engine cache).

Starting from the ledger's own graph, repair one stage at a time with the truth and re-score DV-1 (all committed answers,
no confidence view). Each step's gain is the answer-level headroom of that stage; the order is from cheapest to hardest.

  O0  the ledger as it is (v2 or v3 direction view)
  O1  reversed found links turned the right way                     (direction accuracy)
  O2  + open found links that the truth orients, oriented           (direction commitment)
  O3  + false links removed                                          (link precision)
  O4  + missed links added, oriented by the truth                    (link recall; equals the truth, a sanity check)

  python analysis/q2_headroom.py -> analysis/results/q2_v3/headroom_dev.json
"""
import json, multiprocessing as mp, os, sys, time
from collections import Counter
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))

CONFIGS = {"v2_D": ((), "obs"), "v3_D": (("meek_r1", "meek_r3"), "obs"), "v3_DxR": (("meek_r1", "meek_r3"), "pooled")}


def _score(n, D, U, targets, desc):
    from score import dv
    cl = dv.claims(n, D, U, targets)
    ch = dv.check(cl, desc)
    return {"answered": len(ch), "ok": sum(ok for *_, ok in ch), "yes": sum(1 for *_, v, _ in ch if v),
            "yes_ok": sum(1 for *_, v, ok in ch if v and ok), "f1_num": 0.0}


def _one(args):
    path, family, open_lic, source = args
    from score import bench, graph
    from kernel import build as B, cache, harness, experiment
    name = Path(path).name
    if source == "pooled":
        X, names = harness.pooled_table(path)
    else:
        s = bench.load(path)
        X, names = s["values"], list(s["node_ids"])
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    if led is None:
        return None
    D, U = experiment.configure(led, open_lic)
    I = bench.truth_info(family, name)
    n, T, desc, targets = I["n"], set(I["T"]), I["desc"], I["targets"]
    tadj = {frozenset(e) for e in T}
    mec_open = {frozenset(e) for e in I["cpdag_undirected"]}
    seed = graph.file_seed(name)
    out = {}
    steps = []
    # O0
    D0, U0 = set(D), set(U)
    steps.append(("O0", D0, U0))
    # O1: reversed found links turned the right way
    D1 = {e for e in D0 if not ((e[1], e[0]) in T and e not in T)} | {(b, a) for (a, b) in D0 if (b, a) in T and (a, b) not in T}
    steps.append(("O1", D1, set(U0)))
    # O2: open found true links that the truth orients, oriented
    D2, U2 = set(D1), set()
    for u in U0:
        e = frozenset(u)
        if e in tadj and e not in mec_open:
            a, b = tuple(u)
            D2.add((a, b) if (a, b) in T else (b, a))
        else:
            U2.add(u)
    steps.append(("O2", D2, U2))
    # O3: false links removed
    D3 = {e for e in D2 if frozenset(e) in tadj}
    U3 = {u for u in U2 if frozenset(u) in tadj}
    steps.append(("O3", D3, U3))
    # O4: missed links added, oriented by the truth (MEC-open ones left open)
    D4, U4 = set(D3), set(U3)
    have = {frozenset(e) for e in D4} | {frozenset(u) for u in U4}
    for (a, b) in T:
        if frozenset((a, b)) not in have:
            if frozenset((a, b)) in mec_open:
                U4.add(tuple(sorted((a, b))))
            else:
                D4.add((a, b))
    steps.append(("O4", D4, U4))
    for k, Dk, Uk in steps:
        r = _score(n, Dk, Uk, targets, desc)
        r["f1_num"] = graph.directed_f1(Dk, Uk, T, seed)["f1"]
        out[k] = r
    from score import dv
    out["pairs"] = dv.n_pairs(n, targets)
    return out


def main():
    from score import bench
    res = {}
    for fam in ("semantic", "formula"):
        res[fam] = {}
        for cfg, (open_lic, source) in CONFIGS.items():
            fs = [str(p) for p in bench.files(fam, split="dev")]
            if source == "pooled":
                fs = [f for f in fs if f.endswith("__rep000.npz")]
            t0 = time.time()
            with mp.get_context("fork").Pool(4) as pool:
                rows = [r for r in pool.map(_one, [(f, fam, open_lic, source) for f in fs]) if r]
            pairs = sum(r["pairs"] for r in rows)
            lad = {}
            for k in ("O0", "O1", "O2", "O3", "O4"):
                c = Counter()
                for r in rows:
                    c.update(r[k])
                lad[k] = {"precision": round(c["ok"] / c["answered"], 3), "coverage": round(c["answered"] / pairs, 3),
                          "yes_precision": round(c["yes_ok"] / max(1, c["yes"]), 3), "f1": round(c["f1_num"] / len(rows), 3)}
            res[fam][cfg] = {"files": len(rows), "wall_seconds": round(time.time() - t0, 1), "ladder": lad}
            print(fam, cfg, " ".join("%s P %.3f cov %.3f F1 %.3f |" % (k, v["precision"], v["coverage"], v["f1"]) for k, v in lad.items()))
    json.dump({"split": "dev", "rule": "C3", "steps": {"O0": "ledger as is", "O1": "reversed found links righted", "O2": "+ open found links oriented",
                                                       "O3": "+ false links removed", "O4": "+ missed links added (= truth)"}, "families": res},
              open(ROOT / "analysis" / "results" / "q2_v3" / "headroom_dev.json", "w"), indent=1)


if __name__ == "__main__":
    main()
