"""Dev-only diagnostic for B2: what are the intervention orientations that are not true edges in that direction?

Every pair the frozen kernel (rule C3) orients from shift evidence (or propagates) on a dev obs_int file is classed as
  edge_right      a true edge a -> b
  edge_reversed   a true edge b -> a
  ancestral       not a true edge, but a is an ancestor of b (right as an ancestral claim, wrong for directed F1)
  anti_ancestral  not a true edge, b is an ancestor of a
  unrelated       neither is an ancestor of the other
Reads the dev split only (no held-out read); imports the frozen kernel without changing it.

  CC_CAUSAL_LEARN=... python analysis/q2_b2_orientation_diag.py --family formula --workers 2
  -> analysis/results/q2_b2/orientation_diag_dev_<family>.json
"""
import argparse, json, multiprocessing as mp, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))


def one(args):
    path, family = args
    import numpy as np
    from kernel import build as B, interventions as IV
    from score import bench
    s = bench.load(path)
    name = Path(path).name
    X, M, n_obs = s["values"], s["intervened"], s["n_obs"]
    names = list(s["node_ids"])
    single = M.sum(1) == 1
    by_t = {t: X[np.where(M[:, t] & single)[0]] for t in range(X.shape[1]) if (M[:, t] & single).any()}
    led_d, info = B.build(X[:n_obs], names, rule="C3", created_utc="", file_meta={"source": "diag", "file": name})
    if led_d is None:
        return {"file": name, "failure": info.get("failure")}
    _, iinfo = IV.apply_interventions(led_d, IV.shift_evidence(X[:n_obs], by_t, names))
    I = bench.truth_info(family, name)
    T, desc = I["T"], I["desc"]
    c = Counter()
    for src, pairs in (("oriented", iinfo["oriented"]), ("propagated", iinfo["propagated"])):
        for a, b in pairs:
            i, j = names.index(a), names.index(b)
            k = ("edge_right" if (i, j) in T else "edge_reversed" if (j, i) in T else
                 "ancestral" if j in desc[i] else "anti_ancestral" if i in desc[j] else "unrelated")
            c["%s:%s" % (src, k)] += 1
    return {"file": name, "classes": dict(c), "jittered": bool(led_d["report"]["engine_outputs"]["jittered"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=["semantic", "formula"])
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    from score import bench
    files = [str(p) for p in bench.files(a.family, regime="obs_int", split="dev")]
    with mp.get_context("fork").Pool(a.workers, maxtasksperchild=10) as pool:
        rows = pool.map(one, [(f, a.family) for f in files])
    tot = Counter()
    for r in rows:
        tot.update(r.get("classes", {}))
    jit = Counter()
    for r in rows:
        if r.get("jittered"):
            jit.update(r.get("classes", {}))
    out = {"family": a.family, "split": "dev", "rule": "C3", "files": len(rows), "failures": sum(1 for r in rows if "failure" in r),
           "totals": dict(sorted(tot.items())), "totals_on_jittered_files": dict(sorted(jit.items())),
           "jittered_files": sum(1 for r in rows if r.get("jittered")), "rows": rows}
    p = ROOT / "analysis" / "results" / "q2_b2" / ("orientation_diag_dev_%s.json" % a.family)
    json.dump(out, open(p, "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))


if __name__ == "__main__":
    main()
