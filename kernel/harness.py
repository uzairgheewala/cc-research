"""K0 subsystem harness (kernel v3): fill the engine cache once, then run any post-engine experiment from it.

  python -m kernel.harness fill    --family semantic --split dev [--source obs|obs_int] [--resamples 10] [--workers 2]
  python -m kernel.harness check-v2 --family semantic          # K0 must-show 1: cache rebuild == stored v2 dev ledgers
  python -m kernel.harness score   --family semantic --split dev --rule C3 [--limit N]

fill is the only command that starts the engines; every other command opens the cache read-only and raises on a miss,
so an experiment can never silently fall back to an engine run (and so its wall clock is the post-engine time only).
Held-out discipline: no command here reads a test split unless --held-out-read FREEZE_ID is given and matches a v3
freeze (plans/k*_freeze.json); fill on a test split is allowed (it reads data, scores nothing) and is logged.
"""
import argparse, gzip, json, multiprocessing as mp, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # as every v2 runner: BLAS summation order fixed
    os.environ[_k] = "1"
# OpenBLAS picks its kernels from the host CPU; the v2 ledgers were written on a host it detected as SkylakeX, and a later
# host fell back to Prescott, which changes p-values in the 14th digit and so every ledger hash (found by K0 check-v2,
# 15 Oct). The kernel family is pinned unless the caller pins another; it is part of the cache key.
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
LOG = ROOT / "analysis" / "results" / "q2_v3" / "access_log.jsonl"


def resample_indices(n, B, seed=20261015):
    """The row resamples kernel.confidence.bootstrap draws (same generator, same order)."""
    import numpy as np
    rng = np.random.default_rng(seed)
    return [rng.integers(0, n, n) for _ in range(B)]


def tables(path, source):
    """-> list of (label, X, names) the engines see for one file."""
    from score import bench
    s = bench.load(path)
    names = list(s["node_ids"])
    if source == "obs":
        return [("obs", s["values"], names)]
    if source == "obs_int":
        return [("obs_rows", s["values"][: s["n_obs"]], names)]
    if source == "pooled":
        return [("pooled", pooled_table(path)[0], names)]
    raise ValueError(source)


def pooled_table(path):
    """Regime D x R (E4): the five replicate files of one scenario stacked in replicate order (5,000 rows). Same graph
    and generator in every replicate (checked: truth_info equal). Scored as its own regime, never mixed into D."""
    import numpy as np
    from score import bench
    path = str(path)
    assert "__rep000.npz" in path, "pooled tables are keyed by the scenario's rep000 file"
    parts, names0, T0 = [], None, None
    for r in range(5):
        pr = path.replace("__rep000.npz", "__rep%03d.npz" % r)
        s = bench.load(pr)
        names = list(s["node_ids"])
        T = bench.truth_info(bench_family(pr), Path(pr).name)["T"]
        if names0 is None:
            names0, T0 = names, T
        assert names == names0 and T == T0, "replicates of %s differ in names or graph" % Path(path).name
        parts.append(s["values"])
    return np.vstack(parts), names0


def bench_family(path):
    return "semantic" if "/semantic/" in str(path) or Path(path).name.startswith("semantic") else "formula"


def _fill_one(args):
    path, source, resamples, seed, lam = args
    from kernel import cache
    t0 = time.time()
    out = []
    for label, X, names in tables(path, source):
        cache.engines(X, names, created_utc="", ges_lambda_scale=lam)
        if resamples:
            for b, idx in enumerate(resample_indices(X.shape[0], resamples, seed)):
                cache.engines(X[idx], names, created_utc="")
        out.append(label)
    return {"file": Path(path).name, "tables": out, "seconds": round(time.time() - t0, 1), "hits": cache.STATS["hit"], "misses": cache.STATS["miss"]}


def files_for(family, split, source, limit=0, reps=None):
    from score import bench
    regime = "obs_only" if source == "obs" else "obs_int"
    fs = [str(p) for p in bench.files(family, regime=regime, split=split)]
    if reps is not None:
        fs = [f for f in fs if any(f.endswith("__rep%03d.npz" % r) for r in reps)]
    return fs[:limit] if limit else fs


def log(rec):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as fh:
        fh.write(json.dumps(dict(rec, utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))) + "\n")


def cmd_fill(a):
    fs = files_for(a.family, a.split, "obs" if a.source == "pooled" else a.source, a.limit, [0] if (a.resamples or a.source == "pooled") else None)
    if a.split == "test":
        log({"what": "fill", "family": a.family, "split": "test", "source": a.source, "resamples": a.resamples, "scores": "none"})
    t0 = time.time()
    with mp.get_context("fork").Pool(a.workers) as pool:          # no maxtasksperchild: one engine import per worker
        for r in pool.imap_unordered(_fill_one, [(f, a.source, a.resamples, a.seed, a.ges_lambda_scale) for f in fs]):
            print("%-70s %6.1fs" % (r["file"][:70], r["seconds"]), flush=True)
    print("filled %d files in %.0fs" % (len(fs), time.time() - t0))


def _check_one(args):
    path, family, rules, ledger_dir = args
    from kernel import build as B, cache
    from score import bench
    s = bench.load(path)
    X, names, name = s["values"], list(s["node_ids"]), Path(path).name
    t0 = time.time()
    eng = cache.engines(X, names, read_only=True)
    t_eng = time.time() - t0
    out = {"file": name, "rules": {}, "seconds_engines_from_cache": round(t_eng, 3)}
    for rule in rules:
        t1 = time.time()
        led, _ = B.build(X, names, rule=rule, eng=eng, created_utc="")
        out["rules"][rule] = {"sha": led["report"]["ledger_sha256"] if led else None, "build_seconds": round(time.time() - t1, 3)}
        if ledger_dir:
            f = Path(ledger_dir) / family / rule / (name + ".ledger.json.gz")
            if f.exists():
                with gzip.open(f, "rt") as fh:
                    out["rules"][rule]["stored_ledger_sha"] = json.load(fh)["report"]["ledger_sha256"]
    return out


def cmd_check_v2(a):
    rows = {json.loads(l)["file"]: json.loads(l) for l in open(ROOT / "analysis" / "results" / "q2_b1" / ("dev_%s.jsonl" % a.family))}
    fs = files_for(a.family, "dev", "obs", a.limit)
    rules = ["pc", "ges", "C1", "C2", "C3"]
    t0 = time.time()
    with mp.get_context("fork").Pool(a.workers) as pool:
        res = pool.map(_check_one, [(f, a.family, rules, a.ledger_dir) for f in fs])
    wall = time.time() - t0
    n_eq = n_cmp = n_led_eq = n_led = 0
    bad = []
    for r in res:
        row = rows.get(r["file"])
        for rule, v in r["rules"].items():
            ref = (row or {}).get("rules", {}).get(rule, {}).get("ledger_sha256")
            if ref is not None:
                n_cmp += 1
                n_eq += v["sha"] == ref
                if v["sha"] != ref:
                    bad.append((r["file"], rule))
            if "stored_ledger_sha" in v:
                n_led += 1
                n_led_eq += v["sha"] == v["stored_ledger_sha"]
    out = {"family": a.family, "files": len(res), "rules": rules, "row_hashes_compared": n_cmp, "row_hashes_equal": n_eq,
           "stored_ledgers_compared": n_led, "stored_ledgers_equal": n_led_eq, "mismatches": bad[:20], "wall_seconds": round(wall, 1),
           "mean_build_seconds": round(sum(v["build_seconds"] for r in res for v in r["rules"].values()) / max(1, sum(len(r["rules"]) for r in res)), 3),
           "pass": n_cmp > 0 and n_eq == n_cmp and n_led_eq == n_led}
    p = ROOT / "analysis" / "results" / "q2_v3" / ("k0_check_v2_%s.json" % a.family)
    p.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(p, "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "mismatches"}, indent=1))
    if bad:
        print("first mismatches:", bad[:5])


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("fill")
    p.add_argument("--family", required=True, choices=("semantic", "formula"))
    p.add_argument("--split", required=True, choices=("dev", "test"))
    p.add_argument("--source", default="obs", choices=("obs", "obs_int", "pooled"))
    p.add_argument("--resamples", type=int, default=0)
    p.add_argument("--seed", type=int, default=20261015)
    p.add_argument("--ges-lambda-scale", type=float, default=1.0)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--workers", type=int, default=2)
    p.set_defaults(f=cmd_fill)
    p = sp.add_parser("check-v2")
    p.add_argument("--family", required=True, choices=("semantic", "formula"))
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--ledger-dir", default="/home/claude/work/q2/runs/q2_b1_dev")
    p.set_defaults(f=cmd_check_v2)
    _register_k1(sp)
    a = ap.parse_args()
    a.f(a)



# ---------------------------------------------------------------- K1: link recovery on cached engines (dev only)
def _k1_one(args):
    path, family, rule, max_k, q, full = args
    import numpy as np
    from kernel import build as B, cache, recover, views
    from score import bench
    s = bench.load(path)
    X, names, name = s["values"], list(s["node_ids"]), Path(path).name
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule=rule, eng=eng, created_utc="")
    if led is None:
        return {"file": name, "failure": "pc"}
    D, U = views.graph_sets(led)
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    t0 = time.time()
    r = recover.recover(X, adj, X.shape[1], max_k=max_k, q=q, full=full)
    I = bench.truth_info(family, name)
    tadj = {frozenset(e) for e in I["T"]}
    rec = {frozenset((i, j)) for i, j, _ in r["recovered"]}
    cut = {frozenset(e) for e in recover.audit(X, adj, X.shape[1], max_k=max_k)}
    return {"cut": len(cut), "cut_true": len(cut & tadj),"file": name, "scenario": bench.scenario_of(name), "true": len(tadj), "v2_adj": len(adj), "v2_tp": len(adj & tadj),
            "recovered": len(rec), "recovered_true": len(rec & tadj), "candidates": len(r["candidates"]), "tests": r["tests"],
            "seconds": round(time.time() - t0, 2),
            "missed_discrete": sum(1 for e in tadj - adj if any(r["discrete"][v] for v in e)),
            "recovered_true_discrete": sum(1 for e in (rec & tadj) if any(r["discrete"][v] for v in e))}


def cmd_k1(a):
    if a.split != "dev":
        raise SystemExit("k1 reads the dev split only")
    out = {}
    for fam in a.family:
        fs = files_for(fam, "dev", "obs", a.limit)
        t0 = time.time()
        with mp.get_context("fork").Pool(a.workers) as pool:
            rows = [r for r in pool.map(_k1_one, [(f, fam, a.rule, a.max_k, a.q, a.full) for f in fs]) if "failure" not in r]
        T = sum(r["true"] for r in rows)
        tp0 = sum(r["v2_tp"] for r in rows)
        adj0 = sum(r["v2_adj"] for r in rows)
        rec, rect = sum(r["recovered"] for r in rows), sum(r["recovered_true"] for r in rows)
        md, rd = sum(r["missed_discrete"] for r in rows), sum(r["recovered_true_discrete"] for r in rows)
        cut, cutt = sum(r["cut"] for r in rows), sum(r["cut_true"] for r in rows)
        res = {"files": len(rows), "true_links": T,
               "audit_k1b": {"cut": cut, "cut_true": cutt, "cut_false": cut - cutt,
                             "after_cut": {"recall": (tp0 + rect - cutt) / T, "precision": (tp0 + rect - cutt) / (adj0 + rec - cut)}},
               "v2": {"recall": tp0 / T, "precision": tp0 / adj0, "missed_share": 1 - tp0 / T},
               "k1": {"recall": (tp0 + rect) / T, "precision": (tp0 + rect) / (adj0 + rec), "missed_share": 1 - (tp0 + rect) / T},
               "recovered": rec, "recovered_true": rect, "recovered_precision": rect / rec if rec else None,
               "missed_recovered_share": rect / (T - tp0) if T > tp0 else None,
               "missed_touching_discrete": md, "recovered_true_touching_discrete": rd,
               "tests": sum(r["tests"] for r in rows), "wall_seconds": round(time.time() - t0, 1),
               "settings": {"rule": a.rule, "max_k": a.max_k, "q": a.q, "full": a.full}}
        out[fam] = dict(res, rows=rows)
        print(fam, json.dumps({k: v for k, v in res.items()}, default=float))
    p = ROOT / "analysis" / "results" / "q2_v3" / ("k1_dev_%s.json" % a.tag)
    p.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(p, "w"), indent=1)


def cmd_check_b4(a):
    """K0 must-show 3: B4's bootstrap stability of every DV-1 answer, recomputed from cached resample engines (same rows,
    same rule), equals the stored values in analysis/results/q2_b4/stab_dev_<family>.jsonl."""
    from score import bench, dv
    from kernel import build as B, cache, views
    stored = {json.loads(l)["file"]: json.loads(l) for l in open(ROOT / "analysis" / "results" / "q2_b4" / ("stab_dev_%s.jsonl" % a.family))}
    fs = files_for(a.family, "dev", "obs", a.limit, [0])
    eq = tot = files = 0
    for f in fs:
        name = Path(f).name
        if name not in stored:
            continue
        s = bench.load(f)
        X, names = s["values"], list(s["node_ids"])
        I = bench.truth_info(a.family, name)
        led, _ = B.build(X, names, rule="C3", eng=cache.engines(X, names, read_only=True), created_utc="")
        D, U = views.graph_sets(led)
        cl = dv.claims(I["n"], D, U, I["targets"])
        counts, done = {}, 0
        for idx in resample_indices(X.shape[0], 10):
            l2, _ = B.build(X[idx], names, rule="C3", eng=cache.engines(X[idx], names, read_only=True), created_utc="")
            if l2 is None:
                continue
            done += 1
            D2, U2 = views.graph_sets(l2)
            for k, v in dv.claims(I["n"], D2, U2, I["targets"]).items():
                counts[(k, v)] = counts.get((k, v), 0) + 1
        mine = [[t, y, int(v), int((y in I["desc"][t]) == v), counts.get(((t, y), v), 0) / done] for (t, y), v in sorted(cl.items())]
        theirs = stored[name]["dv"]
        files += 1
        tot += len(theirs)
        eq += sum(1 for m_, t_ in zip(mine, theirs) if m_[:4] == t_[:4] and abs(m_[4] - t_[4]) < 1e-12) if len(mine) == len(theirs) else 0
    out = {"family": a.family, "files": files, "answers_compared": tot, "answers_equal": eq, "pass": files > 0 and eq == tot}
    json.dump(out, open(ROOT / "analysis" / "results" / "q2_v3" / ("k0_check_b4_%s.json" % a.family), "w"), indent=1)
    print(json.dumps(out))


def _register_k1(sp):
    p = sp.add_parser("check-b4")
    p.add_argument("--family", required=True, choices=("semantic", "formula"))
    p.add_argument("--limit", type=int, default=0)
    p.set_defaults(f=cmd_check_b4)
    p = sp.add_parser("k1")
    p.add_argument("--family", nargs="+", default=["semantic", "formula"])
    p.add_argument("--split", default="dev")
    p.add_argument("--rule", default="C3")
    p.add_argument("--max-k", type=int, default=2)
    p.add_argument("--q", type=float, default=0.05)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--tag", default="explore")
    p.add_argument("--full", action="store_true")
    p.set_defaults(f=cmd_k1)


if __name__ == "__main__":
    main()
