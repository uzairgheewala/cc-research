"""B1 rung R3: I1 (column order changes nothing) and I2 (same input, same ledger) with full engine reruns.

  CC_CAUSAL_LEARN=PATH python -m kernel.invariance --split dev --out analysis/results/q2_b1/invariance_dev.json [--rule C3]

One file per scenario per family (the first replicate in sorted order). For each: the ledger is built from scratch
(engines rerun) under 6 column orders (identity, reversed, 4 seeded) and once more in the identity order. Compared:
  content   claims, evidence, knowledge and overrides, plus variables without their positions (positions are the only
            field that must change with the column order)
  hash      the ledger hash of the two identity-order builds (I2)
Pass: identical content under all 6 orders and identical hashes, on every file. No model calls.
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def content_hash(led):
    body = {k: led[k] for k in ("evidence", "knowledge", "claims", "overrides")}
    body["variables"] = sorted(({k: v for k, v in x.items() if k != "position"} for x in led["variables"]), key=lambda v: v["name"])
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def one(args):
    path, family, rule = args
    import numpy as np
    from kernel import build as B
    from score import bench
    s = bench.load(path)
    X, names = s["values"], list(s["node_ids"])
    d = X.shape[1]
    rng = np.random.default_rng(20261015)
    perms = [list(range(d)), list(range(d))[::-1]] + [list(rng.permutation(d)) for _ in range(4)]
    hashes, t0 = [], time.time()
    for p in perms:
        led, info = B.build(X[:, p], [names[j] for j in p], rule=rule, created_utc="")
        hashes.append(content_hash(led) if led else None)
    led0, _ = B.build(X, names, rule=rule, created_utc="")
    again, _ = B.build(X, names, rule=rule, created_utc="")
    return {"file": Path(path).name, "family": family, "content_identical": len(set(hashes)) == 1 and hashes[0] is not None,
            "hash_repeat_identical": again["report"]["ledger_sha256"] == led0["report"]["ledger_sha256"],
            "orders": len(perms), "seconds": round(time.time() - t0, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev")
    ap.add_argument("--rule", default="C3")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--out", default=str(ROOT / "analysis" / "results" / "q2_b1" / "invariance_dev.json"))
    a = ap.parse_args()
    from score import bench
    jobs = []
    for fam in bench.FAMILIES:
        seen = set()
        for f in bench.files(fam, "obs_only", a.split):
            sc = bench.scenario_of(f.name)
            if sc not in seen:
                seen.add(sc)
                jobs.append((str(f), fam, a.rule))
    import multiprocessing as mp
    with mp.get_context("fork").Pool(a.workers) as pool:
        rows = list(pool.imap_unordered(one, jobs))
    res = {"tickets": ["CAP-05", "CAP-11", "TGT-10", "BLD-02"], "rung": "R3 (plans/b1_prereg.json)", "rule": a.rule, "split": a.split,
           "files": len(rows), "content_identical": sum(r["content_identical"] for r in rows),
           "hash_repeat_identical": sum(r["hash_repeat_identical"] for r in rows), "rows": sorted(rows, key=lambda r: r["file"])}
    res["pass"] = res["content_identical"] == res["files"] and res["hash_repeat_identical"] == res["files"]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print("files %d; content identical under 6 orders %d; repeat hash identical %d; %s" % (
        res["files"], res["content_identical"], res["hash_repeat_identical"], "PASS" if res["pass"] else "FAIL"))
    sys.exit(0 if res["pass"] else 1)


if __name__ == "__main__":
    main()
