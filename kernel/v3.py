"""Kernel v3: the data-only ledger of v2 (unchanged core: kernel/build.py, derive.py, policy.py; same rule C3), read through
two v3 views and scored in two regimes. Pre-registered in plans/v3_prereg.json; frozen in plans/v3_freeze.json.

  python -m kernel.v3 fit      --family semantic formula --regime D DxR          # dev: fit and save the confidence maps
  python -m kernel.v3 evaluate --family semantic formula --regime D DxR --split dev|test [--held-out-read ID]

Views (post-ledger; the ledger and its hash are v2's):
  direction view   directions licensed only by Meek rule 1 or 3 are not acted on (shown as open). Dev: Meek R1
                   directions are right 64% / 60% of the time on true links, against 87% / 83% for collider directions.
  confidence view  every DV-1 answer gets a probability from a gradient-boosted model on ledger features
                   (kernel.claim_features), mapped through an isotonic map fitted on cross-fitted scores; one model per
                   family and regime, fitted on every dev scenario, frozen with its sha256.
Regimes
  D     one file, 1,000 rows (CausalArena as released); every file of the split (125 per family)
  DxR   a scenario's five replicate files pooled (5,000 rows; same graph and generator, checked); 25 tables per family.
        A different claim ("given 5,000 rows of this system"), reported beside D, never in its place.
"""
import argparse, hashlib, json, os, pickle, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
OPEN = ("meek_r1", "meek_r3")
RES = ROOT / "analysis" / "results" / "q2_v3"
CAL = ROOT / "calibration"
COST_RATIOS = (1, 2, 4)


def model_path(family, regime):
    return CAL / ("v3_%s_%s.pkl" % (family, regime))


def files_for(family, split, regime):
    from score import bench
    fs = [str(p) for p in bench.files(family, split=split)]
    return [f for f in fs if f.endswith("__rep000.npz")] if regime == "DxR" else fs


def claim_rows(args):
    """One table -> its DV-1 answers with features and correctness."""
    path, family, regime = args
    from score import bench, dv
    from kernel import build as B, cache, claim_features as CF, experiment, harness, k4_eval
    name = Path(path).name
    if regime == "DxR":
        X, names = harness.pooled_table(path)
    else:
        s = bench.load(path)
        X, names = s["values"], list(s["node_ids"])
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    if led is None:
        return {"file": name, "failure": "pc"}
    I = bench.truth_info(family, name)
    D, U = experiment.configure(led, OPEN)
    cl = dv.claims(I["n"], D, U, I["targets"])
    F = CF.features(k4_eval._relabel(led, D, U), I["targets"], cl)
    rows = [{"t": int(t), "y": int(y), "f": F[(t, y)], "yes": bool(v), "ok": (y in I["desc"][t]) == v} for (t, y), v in sorted(cl.items())]
    return {"file": name, "scenario": bench.scenario_of(name), "pairs": dv.n_pairs(I["n"], I["targets"]), "rows": rows,
            "ledger_sha256": led["report"]["ledger_sha256"]}


def _mk():
    from sklearn.ensemble import HistGradientBoostingClassifier as HGC
    return HGC(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, early_stopping=False, random_state=0)


def fit_model(files):
    """Gradient-boosted classifier on all files; isotonic map on 5-fold (by scenario) cross-fitted scores."""
    import numpy as np
    from kernel import confidence
    scen = sorted({f["scenario"] for f in files})
    fold = {s: k % 5 for k, s in enumerate(scen)}
    raw, ys = [], []
    for k in range(5):
        a = [r for f in files if fold[f["scenario"]] != k for r in f["rows"]]
        b = [r for f in files if fold[f["scenario"]] == k for r in f["rows"]]
        c = _mk().fit(np.array([r["f"] for r in a]), np.array([r["ok"] for r in a]))
        raw += list(map(float, c.predict_proba(np.array([r["f"] for r in b]))[:, 1]))
        ys += [float(r["ok"]) for r in b]
    clf = _mk().fit(np.array([r["f"] for f in files for r in f["rows"]]), np.array([r["ok"] for f in files for r in f["rows"]]))
    return {"clf": clf, "map": confidence.isotonic_fit(raw, ys)}


def apply_model(model, rows):
    import numpy as np
    from kernel import confidence
    if not rows:
        return []
    s = model["clf"].predict_proba(np.array([r["f"] for r in rows]))[:, 1]
    return [float(x) for x in confidence.isotonic_apply(model["map"], list(map(float, s)))]


def half(groups):
    """groups: list of (pairs, [(prob, ok)]) -> precision of the half-coverage view (B4's rule, ties together)."""
    items = sorted((x for g in groups for x in g[1]), key=lambda t: -t[0])
    tot = sum(g[0] for g in groups)
    kept, k = [], 0
    while k < len(items):
        kept.append(items[k])
        if len(kept) >= 0.5 * tot and (k + 1 == len(items) or items[k + 1][0] < items[k][0]):
            break
        k += 1
    return (sum(ok for _, ok in kept) / len(kept) if kept else float("nan")), (len(kept) / tot if tot else float("nan"))


def scored(files, probs_by_file):
    """Landmark statistics with scenario-cluster bootstrap intervals (B = 2000, seed 20261014), as B4 evaluate."""
    from score import calib, paired
    byscen = {}
    for f in files:
        g = byscen.setdefault(f["scenario"], [0, []])
        g[0] += f["pairs"]
        g[1] += [(p, r["ok"]) for p, r in zip(probs_by_file[f["file"]], f["rows"])]
    groups = {s: [tuple(v)] for s, v in byscen.items()}
    p_half, c_half = half([g for v in groups.values() for g in v])
    allp = [x for v in byscen.values() for x in v[1]]
    out = {"tables": len(files), "scenarios": len(byscen), "claims": len(allp),
           "precision_half": p_half, "coverage_half": c_half,
           "er2_interval": paired.cluster_bootstrap(groups, stat=lambda gs: half([x for g in gs for x in g])[0]),
           "ece": calib.ece([p for p, _ in allp], [ok for _, ok in allp]),
           "ece_interval": paired.cluster_bootstrap({s: v[1] for s, v in byscen.items()},
                                                    stat=lambda gs: calib.ece([p for g in gs for p, _ in g], [ok for g in gs for _, ok in g])),
           "base_precision": sum(ok for _, ok in allp) / len(allp), "base_coverage": len(allp) / sum(v[0] for v in byscen.values())}
    gaps = {}
    for r_ in COST_RATIOS:
        pst = r_ / (1 + r_)

        def gap(gs, pst=pst):
            it = [x for g in gs for x in g if x[0] >= pst]
            return (sum(ok for _, ok in it) / len(it) - sum(p for p, _ in it) / len(it)) if it else float("nan")
        gaps[str(r_)] = paired.cluster_bootstrap({s: v[1] for s, v in byscen.items()}, stat=gap)
    out["realised_minus_claimed_intervals"] = gaps
    out["ER-2_met"] = out["er2_interval"]["lo"] > 0.80 and c_half >= 0.5
    out["ER-3_met"] = out["ece_interval"]["hi"] <= 0.05 and all(g["lo"] >= -0.03 for g in gaps.values())
    return out


def _collect(family, split, regime, workers):
    import multiprocessing as mp
    fs = files_for(family, split, regime)
    with mp.get_context("fork").Pool(workers) as pool:
        return [r for r in pool.map(claim_rows, [(f, family, regime) for f in fs]) if "failure" not in r]


def cmd_fit(a):
    meta = {}
    for fam in a.family:
        for reg in a.regime:
            files = _collect(fam, "dev", reg, a.workers)
            m = fit_model(files)
            p = model_path(fam, reg)
            p.parent.mkdir(exist_ok=True)
            blob = pickle.dumps(m, protocol=4)
            p.write_bytes(blob)
            meta["%s_%s" % (fam, reg)] = {"path": p.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(blob).hexdigest(),
                                          "dev_tables": len(files), "dev_claims": sum(len(f["rows"]) for f in files)}
            print(fam, reg, meta["%s_%s" % (fam, reg)])
    json.dump(meta, open(CAL / "v3_models.json", "w"), indent=1)


def _guard(a):
    if a.split != "test":
        return None
    fz = ROOT / "plans" / "v3_freeze.json"
    if not a.held_out_read or not fz.exists():
        raise SystemExit("the test split is read only with --held-out-read FREEZE_ID and plans/v3_freeze.json")
    from kernel import freeze
    rec = json.load(open(fz))
    h, _ = freeze.code_sha256()
    if rec["id"] != a.held_out_read or rec["code_sha256"] != h:
        raise SystemExit("code or freeze id does not match plans/v3_freeze.json")
    models = json.load(open(CAL / "v3_models.json"))
    for k, v in models.items():
        if hashlib.sha256((ROOT / v["path"]).read_bytes()).hexdigest() != rec["models"][k]:
            raise SystemExit("confidence model %s differs from the frozen one" % k)
    return rec


def cmd_evaluate(a):
    rec = _guard(a)
    out = {"split": a.split, "freeze": rec["id"] if rec else None, "families": {}}
    for fam in a.family:
        out["families"][fam] = {}
        for reg in a.regime:
            if rec:
                RES.mkdir(parents=True, exist_ok=True)
                with open(RES / "access_log.jsonl", "a") as fh:
                    fh.write(json.dumps({"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "what": "v3 evaluate", "family": fam,
                                         "regime": reg, "split": "test", "freeze": rec["id"]}) + "\n")
            files = _collect(fam, a.split, reg, a.workers)
            if a.split == "dev":
                # dev: out of fold by scenario (the frozen model saw every dev scenario)
                scen = sorted({f["scenario"] for f in files})
                fold = {s: k % 5 for k, s in enumerate(scen)}
                probs = {}
                for k in range(5):
                    m = fit_model([f for f in files if fold[f["scenario"]] != k])
                    for f in files:
                        if fold[f["scenario"]] == k:
                            probs[f["file"]] = apply_model(m, f["rows"])
            else:
                m = pickle.loads(model_path(fam, reg).read_bytes())
                probs = {f["file"]: apply_model(m, f["rows"]) for f in files}
            res = scored(files, probs)
            out["families"][fam][reg] = res
            print(fam, reg, "P@half %.3f [%.3f, %.3f] cov %.3f | ECE %.3f [%.3f, %.3f] | ER-2 %s ER-3 %s" % (
                res["precision_half"], res["er2_interval"]["lo"], res["er2_interval"]["hi"], res["coverage_half"], res["ece"],
                res["ece_interval"]["lo"], res["ece_interval"]["hi"], res["ER-2_met"], res["ER-3_met"]))
    p = RES / ("v3_%s.json" % a.split)
    json.dump(out, open(p, "w"), indent=1, default=float)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    for nm, fn in (("fit", cmd_fit), ("evaluate", cmd_evaluate)):
        p = sp.add_parser(nm)
        p.add_argument("--family", nargs="+", default=["semantic", "formula"])
        p.add_argument("--regime", nargs="+", default=["D", "DxR"])
        p.add_argument("--workers", type=int, default=2)
        if nm == "evaluate":
            p.add_argument("--split", default="dev", choices=("dev", "test"))
            p.add_argument("--held-out-read", default=None)
        p.set_defaults(f=fn)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
