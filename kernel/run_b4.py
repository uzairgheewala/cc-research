"""B4 runner: stability by bootstrap, calibration maps fitted on dev, the selective view (D4.1-D4.4).

  python -m kernel.run_b4 stability --family semantic --split dev --rule C3 --out analysis/results/q2_b4/stab_dev_semantic.jsonl
  python -m kernel.run_b4 fit --rule C3                 # dev only: out-of-fold evaluation, then the frozen maps
  python -m kernel.run_b4 evaluate --rule C3 --held-out-read ID   # test split, frozen maps, once per freeze

Files: replicate rep000 of every scenario (1 per scenario, 25 per family and split), fixed in
plans/b4_prereg.json for compute (10 kernel rebuilds per file). Claims ranked: the DV-1 claims of the full-data ledger
(primary), and its directed claims (secondary: is the arrow right).
No model calls. Tickets: BLD-05, CAP-07, CAP-08, TGT-12, TGT-18 (proposed)
"""
import argparse, datetime, hashlib, json, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
REPS = ("__rep000.npz",)
COST_RATIOS = (1.0, 2.0, 4.0)
RES = ROOT / "analysis" / "results" / "q2_b4"
CAL = ROOT / "calibration"


def stab_one(args):
    path, family, rule, B = args
    from kernel import build as Bld, confidence, views
    from score import bench, dv
    s = bench.load(path)
    X, names = s["values"], list(s["node_ids"])
    name = Path(path).name
    I = bench.truth_info(family, name)
    t0 = time.time()
    led, info = Bld.build(X, names, rule=rule, created_utc="")
    if led is None:
        return {"file": name, "failure": info.get("failure")}
    D, U = views.graph_sets(led)
    cl = dv.claims(I["n"], D, U, I["targets"])
    st = confidence.bootstrap(X, names, rule, B=B, seed=20261015, dv_targets=I["targets"])
    dv_rows = [[t, y, int(v), int((y in I["desc"][t]) == v), st["dv"].get("%d>%d:%s" % (t, y, "yes" if v else "no"), 0.0)]
               for (t, y), v in sorted(cl.items())]
    pos = {v["name"]: v["position"] for v in led["variables"]}
    edge_rows = []
    for c in led["claims"]:
        if c["relation"] != "x->y":
            continue
        key = "%s|%s" % tuple(sorted((c["x"], c["y"])))
        f = st["rel"].get(key, {}).get("%s->%s" % (c["x"], c["y"]), 0.0)
        edge_rows.append([c["x"], c["y"], int((pos[c["x"]], pos[c["y"]]) in I["T"]), f, c["licensed_by"]])
    return {"file": name, "family": family, "split": bench.split_of(family, name), "scenario": bench.scenario_of(name),
            "pairs": dv.n_pairs(I["n"], I["targets"]), "B": st["B"], "B_completed": st["completed"], "dv": dv_rows, "edges": edge_rows,
            "ledger_sha256": led["report"]["ledger_sha256"], "seconds": round(time.time() - t0, 1)}


def _load(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def _pool(rows, kind="dv"):
    out = []
    for r in rows:
        if "failure" in r:
            continue
        for x in r[kind]:
            if kind == "dv":
                out.append({"scenario": r["scenario"], "file": r["file"], "stab": x[4], "ok": x[3]})
            else:
                out.append({"scenario": r["scenario"], "file": r["file"], "stab": x[3], "ok": x[2]})
    return out


def _metrics(probs, oks, pairs_total):
    from score import calib
    n = len(probs)
    order = sorted(range(n), key=lambda i: -probs[i])
    target = 0.5 * pairs_total
    kept = []
    for k, i in enumerate(order):
        kept.append(i)
        if len(kept) >= target and (k + 1 == n or probs[order[k + 1]] < probs[i]):
            break
    sel = {"coverage": len(kept) / pairs_total if pairs_total else None,
           "precision": sum(oks[i] for i in kept) / len(kept) if kept else None, "kept": len(kept)}
    cvr = {str(r): calib.claimed_vs_realised(probs, oks, r / (1 + r)) for r in COST_RATIOS}
    return {"claims": n, "pairs": pairs_total, "base_coverage": n / pairs_total if pairs_total else None,
            "base_precision": sum(oks) / n if n else None, "ece": calib.ece(probs, oks), "reliability": calib.reliability(probs, oks),
            "selective_at_half_coverage": sel, "claimed_vs_realised": cvr, "risk_coverage": calib.risk_coverage(probs, oks)}


def fit(rule):
    from kernel import confidence
    out = {"tickets": ["BLD-05", "CAP-07", "CAP-08", "TGT-12"], "rule": rule, "families": {}}
    CAL.mkdir(exist_ok=True)
    for fam in ("semantic", "formula"):
        rows = _load(RES / ("stab_dev_%s.jsonl" % fam))
        pairs_total = sum(r["pairs"] for r in rows if "failure" not in r)
        fam_out = {}
        for kind in ("dv", "edges"):
            pool = _pool(rows, kind)
            scen = sorted({p["scenario"] for p in pool})
            folds = {s: i % 5 for i, s in enumerate(scen)}
            oof = [None] * len(pool)
            for k in range(5):
                tr = [p for p in pool if folds[p["scenario"]] != k]
                m = confidence.isotonic_fit([p["stab"] for p in tr], [p["ok"] for p in tr])
                for i, p in enumerate(pool):
                    if folds[p["scenario"]] == k:
                        oof[i] = float(confidence.isotonic_apply(m, [p["stab"]])[0])
            raw = [p["stab"] for p in pool]
            oks = [p["ok"] for p in pool]
            m_all = confidence.isotonic_fit(raw, oks)
            pt = pairs_total if kind == "dv" else len(pool)
            fam_out[kind] = {"raw_stability_as_probability": _metrics(raw, oks, pt), "calibrated_out_of_fold": _metrics(oof, oks, pt)}
            sha = confidence.save_map(m_all, CAL / ("map_%s_%s.json" % (fam, kind)),
                                      {"family": fam, "kind": kind, "rule": rule, "fitted_on": "dev split, replicate rep000",
                                       "points": len(pool), "method": "isotonic (pool-adjacent-violators) of correctness on bootstrap stability, B=10"})
            fam_out[kind]["map_sha256"] = sha
        out["families"][fam] = fam_out
    json.dump(out, open(RES / "fit_dev.json", "w"), indent=1)
    for fam, v in out["families"].items():
        for kind, w in v.items():
            c = w["calibrated_out_of_fold"]
            print(fam, kind, "ECE oof %.3f (raw %.3f); at half coverage precision %s; claimed vs realised %s" % (
                c["ece"], w["raw_stability_as_probability"]["ece"], c["selective_at_half_coverage"],
                {k: (round(x["claimed"], 3) if x["claimed"] else None, round(x["realised"], 3) if x["realised"] else None) for k, x in c["claimed_vs_realised"].items()}))


def evaluate(rule):
    from kernel import confidence
    from score import paired
    out = {"tickets": ["BLD-05", "CAP-07", "CAP-08", "TGT-12", "TGT-18"], "rule": rule, "families": {}}
    for fam in ("semantic", "formula"):
        rows = [r for r in _load(RES / ("stab_test_%s.jsonl" % fam)) if "failure" not in r]
        pairs_total = sum(r["pairs"] for r in rows)
        fo = {}
        for kind in ("dv", "edges"):
            m = json.load(open(CAL / ("map_%s_%s.json" % (fam, kind))))["map"]
            pool = _pool(rows, kind)
            probs = [float(confidence.isotonic_apply(m, [p["stab"]])[0]) for p in pool]
            oks = [p["ok"] for p in pool]
            pt = pairs_total if kind == "dv" else len(pool)
            fo[kind] = _metrics(probs, oks, pt)
            if kind == "dv":
                # ER-2 interval: scenarios resampled; the half-coverage cut recomputed in every draw
                byscen = {}
                for p, pr in zip(pool, probs):
                    byscen.setdefault(p["scenario"], []).append((pr, p["ok"]))
                pairs_by = {}
                for r in rows:
                    pairs_by[r["scenario"]] = pairs_by.get(r["scenario"], 0) + r["pairs"]

                def stat(groups, keys=None):
                    items = [x for g in groups for x in g[1]]
                    tot = sum(g[0] for g in groups)
                    items.sort(key=lambda t: -t[0])
                    kept, k = [], 0
                    while k < len(items):
                        kept.append(items[k])
                        if len(kept) >= 0.5 * tot and (k + 1 == len(items) or items[k + 1][0] < items[k][0]):
                            break
                        k += 1
                    return sum(ok for _, ok in kept) / len(kept) if kept else float("nan")
                groups = {s: [(pairs_by[s], byscen.get(s, []))] for s in pairs_by}
                ci = paired.cluster_bootstrap({s: v for s, v in groups.items()}, stat=lambda gs: stat([x for g in gs for x in g]))
                fo[kind]["er2_interval"] = ci
                # ER-3 intervals: ECE (upper end must be <= 0.05) and realised - claimed at each threshold (lower end >= -0.03)
                from score import calib
                by2 = {s: [(pr, ok) for pr, ok in byscen.get(s, [])] for s in pairs_by}

                def ece_stat(gs):
                    items = [x for g in gs for x in g]
                    return calib.ece([x[0] for x in items], [x[1] for x in items]) if items else float("nan")
                fo[kind]["ece_interval"] = paired.cluster_bootstrap(by2, stat=ece_stat)
                gaps = {}
                for r_ in COST_RATIOS:
                    pst = r_ / (1 + r_)

                    def gap_stat(gs, pst=pst):
                        items = [x for g in gs for x in g if x[0] >= pst]
                        if not items:
                            return float("nan")
                        return sum(x[1] for x in items) / len(items) - sum(x[0] for x in items) / len(items)
                    gaps[str(r_)] = paired.cluster_bootstrap(by2, stat=gap_stat)
                fo[kind]["realised_minus_claimed_intervals"] = gaps
        out["families"][fam] = fo
    json.dump(out, open(RES / "evaluate_test.json", "w"), indent=1)
    for fam, v in out["families"].items():
        c = v["dv"]
        print(fam, "ECE %.3f; at half coverage %s; CI %s" % (c["ece"], c["selective_at_half_coverage"], {k: round(x, 3) for k, x in c["er2_interval"].items() if isinstance(x, float)}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=("stability", "fit", "evaluate"))
    ap.add_argument("--family", choices=("semantic", "formula"))
    ap.add_argument("--split", choices=("dev", "test"))
    ap.add_argument("--rule", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--B", type=int, default=10)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--held-out-read", default=None)
    a = ap.parse_args()
    RES.mkdir(parents=True, exist_ok=True)
    if a.what == "fit":
        return fit(a.rule)
    if a.split == "test" or a.what == "evaluate":
        from kernel import freeze
        fz_path = ROOT / "plans" / "b4_freeze.json"
        if not a.held_out_read or not fz_path.exists():
            raise SystemExit("the test split is read only with --held-out-read FREEZE_ID and plans/b4_freeze.json")
        fz = json.load(open(fz_path))
        h, _ = freeze.code_sha256()
        if fz["id"] != a.held_out_read or fz["code_sha256"] != h or fz.get("rule") != a.rule:
            raise SystemExit("kernel code, rule or freeze id does not match plans/b4_freeze.json")
        for f, want in fz.get("maps", {}).items():
            if hashlib.sha256((CAL / f).read_bytes()).hexdigest() != want:
                raise SystemExit("calibration map %s differs from the frozen one" % f)
        with open(RES / "access_log.jsonl", "a") as fh:
            fh.write(json.dumps({"utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "what": a.what,
                                 "family": a.family, "split": "test", "freeze": a.held_out_read, "rule": a.rule}) + "\n")
    if a.what == "evaluate":
        return evaluate(a.rule)
    from score import bench
    files = [str(f) for f in bench.files(a.family, "obs_only", a.split) if f.name.endswith(REPS)]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["file"] for l in open(out)} if out.exists() else set()
    jobs = [(f, a.family, a.rule, a.B) for f in files if Path(f).name not in done]
    print("%d files, %d to do" % (len(files), len(jobs)), flush=True)
    import multiprocessing as mp
    with mp.get_context("fork").Pool(a.workers, maxtasksperchild=5) as pool:
        for row in pool.imap_unordered(stab_one, jobs):
            with open(out, "a") as fh:
                fh.write(json.dumps(row) + "\n")
            print(row["file"][:70], row.get("seconds"), flush=True)


if __name__ == "__main__":
    main()
