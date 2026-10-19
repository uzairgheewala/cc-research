"""Kernel v3 experiment loop (K0 harness): one configuration of the post-engine kernel, scored on a split from the engine
cache, in seconds. Every K1-K4 dev experiment is a call of score().

  python -m kernel.experiment --family semantic formula --lam 1.0 --open meek_r1 meek_r3 [--source obs|pooled]

Configuration (each field is a typed choice; nothing else varies):
  lam      GES penalty scale (1.0 = v2's BIC engine; others need a cache fill with --ges-lambda-scale)
  rule     combination rule (v2's: pc, ges, C1, C2, C3)
  open     licence classes whose directions are withdrawn to "open" (K3 direction granularity)
  source   obs (one file = 1,000 rows) or pooled (a scenario's five replicates, 5,000 rows; regime D x R)
Scores: skeleton recall / precision / missed share, directed F1 (v2's expectation rule), DV-1 precision, coverage,
yes-precision and yes-rate, against the released truth. Dev only: a test split needs --held-out-read with a v3 freeze.
"""
import argparse, json, multiprocessing as mp, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))


def configure(led, open_lic=()):
    """The ledger's graph after the configuration's post-engine steps. -> (D, U) in position space."""
    from kernel import views
    D, U = views.graph_sets(led)
    if not open_lic:
        return D, U
    pos = {v["name"]: v["position"] for v in led["variables"]}
    lic = {(pos[c["x"]], pos[c["y"]]): c["licensed_by"] for c in led["claims"] if c["relation"] == "x->y"}
    D2 = {e for e in D if lic.get(e) not in open_lic}
    U2 = set(U) | {tuple(sorted(e)) for e in D if lic.get(e) in open_lic}
    return D2, U2


def _one(args):
    path, family, cfg = args
    from score import bench, dv, graph
    from kernel import build as B, cache, harness
    name = Path(path).name
    if cfg["source"] == "pooled":
        X, names = harness.pooled_table(path)
    else:
        s = bench.load(path)
        X, names = s["values"], list(s["node_ids"])
    eng = cache.engines(X, names, read_only=True, ges_lambda_scale=cfg["lam"])
    led, _ = B.build(X, names, rule=cfg["rule"], eng=eng, created_utc="")
    if led is None:
        return {"file": name, "failure": "pc"}
    D, U = configure(led, tuple(cfg["open"]))
    I = bench.truth_info(family, name)
    T = I["T"]
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    tadj = {frozenset(e) for e in T}
    ch = dv.check(dv.claims(I["n"], D, U, I["targets"]), I["desc"])
    return {"file": name, "scenario": bench.scenario_of(name), "true": len(tadj), "adj": len(adj), "tp": len(adj & tadj),
            "f1": graph.directed_f1(D, U, T, graph.file_seed(name))["f1"],
            "dv_pairs": dv.n_pairs(I["n"], I["targets"]), "dv_com": len(ch), "dv_ok": sum(ok for *_, ok in ch),
            "dv_yes": sum(1 for *_, v, ok in ch if v), "dv_yes_ok": sum(1 for *_, v, ok in ch if v and ok)}


def score(family, cfg, split="dev", workers=2, limit=0):
    from score import bench
    if split != "dev":
        raise SystemExit("kernel.experiment scores the dev split only")
    fs = [str(p) for p in bench.files(family, split=split)]
    if cfg["source"] == "pooled":
        fs = [f for f in fs if f.endswith("__rep000.npz")]
    fs = fs[:limit] if limit else fs
    t0 = time.time()
    with mp.get_context("fork").Pool(workers) as pool:
        rows = [r for r in pool.map(_one, [(f, family, cfg) for f in fs]) if "failure" not in r]
    S = lambda k: sum(r[k] for r in rows)  # noqa: E731
    return {"family": family, "config": cfg, "files": len(rows), "wall_seconds": round(time.time() - t0, 1),
            "skeleton_recall": S("tp") / S("true"), "skeleton_precision": S("tp") / S("adj"), "missed_share": 1 - S("tp") / S("true"),
            "f1": S("f1") / len(rows), "dv1_precision": S("dv_ok") / S("dv_com"), "dv1_coverage": S("dv_com") / S("dv_pairs"),
            "dv1_yes_precision": S("dv_yes_ok") / max(1, S("dv_yes")), "dv1_yes_rate": S("dv_yes") / S("dv_pairs"), "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", nargs="+", default=["semantic", "formula"])
    ap.add_argument("--lam", type=float, default=1.0)
    ap.add_argument("--rule", default="C3")
    ap.add_argument("--open", nargs="*", default=[])
    ap.add_argument("--source", default="obs", choices=("obs", "pooled"))
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--save", default=None, help="write the result (with rows) to analysis/results/q2_v3/<save>.json")
    a = ap.parse_args()
    cfg = {"lam": a.lam, "rule": a.rule, "open": sorted(a.open), "source": a.source}
    res = {}
    for fam in a.family:
        r = score(fam, cfg, workers=a.workers, limit=a.limit)
        res[fam] = r
        print("%-8s %s | missed %.3f skel-P %.3f F1 %.3f | DV-1 P %.3f cov %.3f yesP %.3f yes-rate %.3f | %d files %.0fs" % (
            fam, json.dumps(cfg), r["missed_share"], r["skeleton_precision"], r["f1"], r["dv1_precision"], r["dv1_coverage"],
            r["dv1_yes_precision"], r["dv1_yes_rate"], r["files"], r["wall_seconds"]))
    if a.save:
        p = ROOT / "analysis" / "results" / "q2_v3" / (a.save + ".json")
        p.parent.mkdir(parents=True, exist_ok=True)
        json.dump(res, open(p, "w"), indent=1)


if __name__ == "__main__":
    main()
