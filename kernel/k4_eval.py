"""K4 dev evaluation: how well can the ledger rank its own DV-1 answers? Out-of-fold by scenario (5 folds), dev only.

  python -m kernel.k4_eval --family semantic formula [--open meek_r1 meek_r3] [--stability]

Models (each fitted on 4 folds, applied to the 5th; deterministic):
  stability   isotonic on resample stability (v2's B4 method), when the resample cache is filled
  features    gradient-boosted classifier on kernel.claim_features (and stability when available), then isotonic
Scores: precision at half coverage (claims kept in order of probability until half of all target-outcome pairs are
covered, ties together: B4's rule), ECE (10 bins), and the claimed-vs-realised gap at c/g = 1, 2, 4.
"""
import argparse, json, multiprocessing as mp, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))


def one(args):
    path, family, open_lic, stability = args[:4]
    pooled = len(args) > 4 and args[4]
    import numpy as np
    from score import bench, dv
    from kernel import build as B, cache, claim_features as CF, experiment, harness
    name = Path(path).name
    if pooled:
        X, names = harness.pooled_table(path)
    else:
        s = bench.load(path)
        X, names = s["values"], list(s["node_ids"])
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    if led is None:
        return None
    I = bench.truth_info(family, name)
    D, U = experiment.configure(led, tuple(open_lic))
    cl = dv.claims(I["n"], D, U, I["targets"])
    led_cfg = led if not open_lic else _relabel(led, D, U)
    F = CF.features(led_cfg, I["targets"], cl)
    stab = {}
    if stability:
        counts = {}
        idxs = harness.resample_indices(X.shape[0], 10)
        done = 0
        for idx in idxs:
            try:
                e2 = cache.engines(X[idx], names, read_only=True)
            except LookupError:
                return {"file": name, "missing_resamples": True}
            l2, _ = B.build(X[idx], names, rule="C3", eng=e2, created_utc="")
            if l2 is None:
                continue
            done += 1
            D2, U2 = experiment.configure(l2, tuple(open_lic))
            for k, v in dv.claims(I["n"], D2, U2, I["targets"]).items():
                counts[(k, v)] = counts.get((k, v), 0) + 1
        stab = {k: counts.get((k, v), 0) / max(1, done) for k, v in cl.items()}
    rows = []
    for (t, y), v in cl.items():
        rows.append({"f": F[(t, y)] + ([stab[(t, y)]] if stability else []), "yes": bool(v), "ok": (y in I["desc"][t]) == v})
    return {"file": name, "scenario": bench.scenario_of(name), "pairs": dv.n_pairs(I["n"], I["targets"]), "rows": rows}


def _relabel(led, D, U):
    import copy
    led = copy.deepcopy(led)
    pos = {v["name"]: v["position"] for v in led["variables"]}
    for c in led["claims"]:
        a, b = pos[c["x"]], pos[c["y"]]
        if c["relation"] == "x->y" and (a, b) not in D:
            c["relation"] = "x-y"
    return led


def half_coverage(probs, oks, pairs_total):
    order = sorted(range(len(probs)), key=lambda i: -probs[i])
    kept = []
    for k, i in enumerate(order):
        kept.append(i)
        if len(kept) >= 0.5 * pairs_total and (k + 1 == len(order) or probs[order[k + 1]] < probs[i]):
            break
    return (sum(oks[i] for i in kept) / len(kept) if kept else None), len(kept) / pairs_total


def evaluate(files, use):
    import numpy as np
    from sklearn.ensemble import HistGradientBoostingClassifier as HGC
    from kernel import confidence
    from score import calib
    scen = sorted({f["scenario"] for f in files})
    fold = {s: k % 5 for k, s in enumerate(scen)}
    probs, oks, yes = [], [], []
    for k in range(5):
        tr = [r for f in files if fold[f["scenario"]] != k for r in f["rows"]]
        te = [r for f in files if fold[f["scenario"]] == k for r in f["rows"]]
        Xtr, ytr = np.array([use(r) for r in tr]), np.array([r["ok"] for r in tr])
        Xte = np.array([use(r) for r in te])
        if Xtr.shape[1] == 1:
            m = confidence.isotonic_fit(list(Xtr[:, 0]), list(ytr.astype(float)))
            p = confidence.isotonic_apply(m, list(Xte[:, 0]))
        else:
            mk = lambda: HGC(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, early_stopping=False, random_state=0)  # noqa: E731
            # the isotonic map is fitted on cross-fitted scores of the training folds (in-sample scores are overconfident)
            trs = [f for f in files if fold[f["scenario"]] != k]
            inner = {f["scenario"]: j % 4 for j, f in enumerate(sorted(trs, key=lambda f: f["scenario"]))}
            raw_tr, y_tr = [], []
            for j in range(4):
                a_ = [r for f in trs if inner[f["scenario"]] != j for r in f["rows"]]
                b_ = [r for f in trs if inner[f["scenario"]] == j for r in f["rows"]]
                if not a_ or not b_:
                    continue
                c_ = mk().fit(np.array([use(r) for r in a_]), np.array([r["ok"] for r in a_]))
                raw_tr += list(c_.predict_proba(np.array([use(r) for r in b_]))[:, 1])
                y_tr += [float(r["ok"]) for r in b_]
            clf = mk().fit(Xtr, ytr)
            m = confidence.isotonic_fit(raw_tr, y_tr)
            p = confidence.isotonic_apply(m, list(clf.predict_proba(Xte)[:, 1]))
        probs += list(map(float, p))
        oks += [r["ok"] for r in te]
        yes += [r["yes"] for r in te]
    pairs = sum(f["pairs"] for f in files)
    prec, cov = half_coverage(probs, oks, pairs)
    gaps = {}
    for r in (1, 2, 4):
        cv = calib.claimed_vs_realised(probs, oks, r / (1 + r))
        gaps[str(r)] = cv
    return {"precision_half": prec, "coverage_half": cov, "ece": calib.ece(probs, oks), "claims": len(probs), "base_precision": sum(oks) / len(oks),
            "base_coverage": len(probs) / pairs, "gaps": gaps}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", nargs="+", default=["semantic", "formula"])
    ap.add_argument("--open", nargs="*", default=[])
    ap.add_argument("--stability", action="store_true")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--reps", default="all", help="'all' or 'rep000' (B4's design used rep000 only)")
    ap.add_argument("--save", default=None)
    ap.add_argument("--pooled", action="store_true", help="regime D x R: the scenario's five replicates pooled")
    a = ap.parse_args()
    from score import bench
    out = {}
    for fam in a.family:
        fs = [str(p) for p in bench.files(fam, split="dev")]
        if a.stability or a.reps == "rep000" or a.pooled:
            fs = [f for f in fs if f.endswith("__rep000.npz")]
        t0 = time.time()
        with mp.get_context("fork").Pool(a.workers) as pool:
            files = [r for r in pool.map(one, [(f, fam, a.open, a.stability, a.pooled) for f in fs]) if r]
        if any(f.get("missing_resamples") for f in files):
            raise SystemExit("resample cache incomplete for %s" % fam)
        res = {"files": len(files), "open": a.open, "stability": a.stability, "wall_seconds": round(time.time() - t0, 1)}
        res["features"] = evaluate(files, lambda r: r["f"])
        if a.stability:
            res["stability_only"] = evaluate(files, lambda r: [r["f"][-1]])
        out[fam] = res
        print(fam, json.dumps(res, default=float)[:1600])
    if a.save:
        json.dump(out, open(ROOT / "analysis" / "results" / "q2_v3" / (a.save + ".json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
