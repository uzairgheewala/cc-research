"""Kernel v4 candidates on CausalArena dev (BLD-18, wave B): GES with a score that fits nonlinear and discrete mechanisms.

Tickets: BLD-18, TGT-18, TGT-19

    python -m v4.dev list
    python -m v4.dev fill [--workers 2]                       v3 engine records for every dev file on this machine (first)
    python -m v4.dev engines  --knob A1 [--family semantic formula] [--part 1/4] [--workers 2]   GES variant per dev file
    python -m v4.dev evaluate [--knobs G0 G1 A1 A2 R1] [--family semantic formula] [--workers 2]   -> analysis/results/v4/dev.json
    python -m v4.dev decide                                                                           -> analysis/results/v4/decision.json

Pre-registration: plans/v4_prereg.json (knobs, metrics, predictions and the decision rule; hashed before any dev number).
Dev only: no test split, no family-2 file. The ledger is v3's (kernel/build.py rule C3, the v3 direction view and v3's
confidence-model recipe refitted out of fold by scenario), with GES's output replaced by the knob's; PC and every other
part of the table's engine record come from the v3 engine cache, unchanged.

Knobs (v4/scores.py):
  G0  v3's GES (ges.fit_bic: forward, backward, turning), read from the v3 engine cache: the baseline
  G1  gauss score, forward + backward only (no turning): the search control for the non-linear knobs
  A1  additive score (hinge basis, discrete parents as indicators), lam 1, forward + backward
  A2  additive score, lam 2, forward + backward
  R1  rff score (linear terms + random Fourier features, ridge), lam 1, forward + backward
Why no turning phase for the new scores: the additive and rff scores are not score-equivalent (Markov-equivalent DAGs score
differently), which GES's turning operator assumes; on the first smoke file the turning phase did not finish in 8 minutes
while forward + backward took 13 s. G1 measures what dropping the turning phase alone does.

Engine records are cached in cache/v4/<knob>/<data_sha[:2]>/<data_sha>.json.gz (marks over the canonical columns, the
package's final score, the knob's score of the true DAG, seconds, typed failure).
"""
import argparse, gzip, hashlib, json, multiprocessing as mp, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
for _p in (ROOT, ROOT / "ledger", ROOT / "analysis"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
CACHE = Path(os.environ.get("CC_V4_CACHE", str(ROOT / "cache" / "v4")))
RES = Path(os.environ.get("CC_V4_RESULTS", str(ROOT / "analysis" / "results" / "v4")))
PREREG = ROOT / "plans" / "v4_prereg.json"
KNOBS = {
    "G0": None,
    "G1": {"design": "gauss", "lam": 1.0, "phases": ["forward", "backward"]},
    "A1": {"design": "additive", "lam": 1.0, "phases": ["forward", "backward"]},
    "A2": {"design": "additive", "lam": 2.0, "phases": ["forward", "backward"]},
    "R1": {"design": "rff", "lam": 1.0, "phases": ["forward", "backward"]},
}
FAMILIES = ("semantic", "formula")
TIMEOUT_S = 900
OPEN = ("meek_r1", "meek_r3")


def dev_files(family, limit=0):
    from score import bench
    fs = [str(p) for p in bench.files(family, split="dev")]
    if not limit:
        return fs
    first = [f for f in fs if f.endswith("__rep000.npz")]          # smoke: one file per scenario first
    return (first + [f for f in fs if f not in first])[:limit]


def cache_path(knob, data_sha):
    return CACHE / knob / data_sha[:2] / ("%s.json.gz" % data_sha)


def knob_sha(knob):
    return hashlib.sha256(json.dumps(KNOBS[knob], sort_keys=True).encode()).hexdigest()[:16]


# ------------------------------------------------------------------------------------------------ engines
def run_knob(Xc, knob, true_parents=None):
    """GES under the knob's score on the canonical (possibly jittered) table -> record dict."""
    import ges
    from engines.core import _alarm, _classify, cpdag_to_marks
    from v4.scores import DesignScore
    k = KNOBS[knob]
    t0 = time.time()
    Z = (Xc - Xc.mean(0)) / Xc.std(0)
    S = DesignScore(Z, k["design"], lam=k["lam"])
    rec = {"knob": knob, "knob_sha": knob_sha(knob)}
    try:
        with _alarm(TIMEOUT_S):
            C, score = ges.fit(S, phases=list(k["phases"]))
        M = cpdag_to_marks(C)
        rec.update(ok=True, marks=M.astype(int).tolist(), score=float(score), failure=None)
    except Exception as e:  # noqa: BLE001 - typed failure, as engines.core
        rec.update(ok=False, marks=None, score=None, failure=_classify(e))
    rec["seconds"] = round(time.time() - t0, 2)
    rec["local_scores"] = len(S._cache)
    if true_parents is not None:
        rec["true_dag_score"] = float(sum(S.local_score(j, set(true_parents[j])) for j in range(S.p)))
    return rec


def engines_one(args):
    path, family, knob = args
    import numpy as np
    from score import bench
    from kernel import cache
    s = bench.load(path)
    name = Path(path).name
    eng = cache.engines(s["values"], list(s["node_ids"]), read_only=True)
    out = cache_path(knob, eng["data_sha"])
    if out.exists():
        return {"file": name, "hit": True}
    order = list(eng["order"])
    T = bench.truth_info(family, name)["T"]
    pos = {v: k for k, v in enumerate(order)}                 # original index -> canonical position
    parents = [[] for _ in order]
    for a, b in T:
        parents[pos[b]].append(pos[a])
    rec = run_knob(np.asarray(eng["Xc"], dtype=float), knob, parents)
    rec.update(file=name, family=family, data_sha256=eng["data_sha"])
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    with gzip.open(tmp, "wt", encoding="utf-8") as fh:
        json.dump(rec, fh)
    os.replace(tmp, out)
    return {"file": name, "hit": False, "seconds": rec["seconds"], "ok": rec["ok"]}


def cmd_engines(a):
    if KNOBS[a.knob] is None:
        raise SystemExit("G0 is v3's engine: it is read from the v3 cache, never recomputed")
    k, n = (int(x) for x in a.part.split("/"))
    jobs = [(f, fam, a.knob) for fam in a.family for f in dev_files(fam, a.limit)]
    jobs = [j for i, j in enumerate(jobs) if i % n == k - 1]
    print("[v4] engines %s part %d/%d: %d files" % (a.knob, k, n, len(jobs)), flush=True)
    t0 = time.time()
    with mp.get_context("fork").Pool(a.workers) as pool:
        rows = []
        for r in pool.imap_unordered(engines_one, jobs):
            rows.append(r)
            if len(rows) % 10 == 0:
                print("[v4] %s %d / %d files (%.0f s)" % (a.knob, len(rows), len(jobs), time.time() - t0), flush=True)
    done = RES / "engines" / ("%s_part%dof%d.json" % (a.knob, k, n))
    done.parent.mkdir(parents=True, exist_ok=True)
    done.write_text(json.dumps({"knob": a.knob, "knob_sha": knob_sha(a.knob), "files": len(rows),
                                "failed": sum(1 for r in rows if r.get("ok") is False),
                                "computed": sum(1 for r in rows if not r["hit"])}, indent=1))
    print("JOB-COMPLETE %s %d files" % (a.knob, len(rows)))
    return 0


# ------------------------------------------------------------------------------------------------ evaluate
def knob_eng(eng, knob):
    """v3's engine record with GES replaced by the knob's (None: the record is missing)."""
    from engines.core import EngineResult
    import numpy as np
    if KNOBS[knob] is None:
        return eng, None
    p = cache_path(knob, eng["data_sha"])
    if not p.exists():
        return None, None
    with gzip.open(p, "rt", encoding="utf-8") as fh:
        rec = json.load(fh)
    g = EngineResult("ges_v4_%s" % knob, rec["ok"], marks=None if rec["marks"] is None else np.array(rec["marks"], dtype=int),
                     score=rec["score"], seconds=rec["seconds"], failure=rec["failure"])
    return dict(eng, ges=g), rec


def file_rows(args):
    """One dev file under every knob: claim rows (as kernel.v3.claim_rows) and engine-level scores."""
    path, family, knobs = args
    from score import bench, dv, graph
    from kernel import build as B, cache, claim_features as CF, experiment, k4_eval
    from engines import core
    s = bench.load(path)
    name = Path(path).name
    X, names = s["values"], list(s["node_ids"])
    eng0 = cache.engines(X, names, read_only=True)
    I = bench.truth_info(family, name)
    order = list(eng0["order"])
    out = {"file": name, "scenario": bench.scenario_of(name), "pairs": dv.n_pairs(I["n"], I["targets"]), "knobs": {}}
    for knob in knobs:
        eng, rec = knob_eng(eng0, knob)
        if eng is None:
            out["knobs"][knob] = {"missing": True}
            continue
        r = {}
        g = eng["ges"]
        if g is not None and g.ok:
            Dc, Uc = core.marks_to_sets(g.marks)
            Dg, Ug = core.map_back(Dc, Uc, order)
            r["ges_directed_f1"] = graph.directed_f1(Dg, Ug, I["T"], graph.file_seed(name))["f1"]
            co = graph.coords(Dg, Ug, I["T"])
            r["ges_skeleton_f1"] = co["S"]
            tadj = {frozenset(e) for e in I["T"]}
            padj = {frozenset(e) for e in Dg} | {frozenset(u) for u in Ug}
            r["ges_false_adj"] = len(padj - tadj)
            r["ges_missed_adj"] = len(tadj - padj)
            if rec is not None and rec.get("true_dag_score") is not None and rec.get("score") is not None:
                r["true_minus_found"] = rec["true_dag_score"] - rec["score"]
        else:
            r["ges_failed"] = True
        led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
        if led is None:
            r["ledger_failed"] = True
            out["knobs"][knob] = r
            continue
        D, U = experiment.configure(led, OPEN)
        r["ledger_directed_f1"] = graph.directed_f1(D, U, I["T"], graph.file_seed(name))["f1"]
        cl = dv.claims(I["n"], D, U, I["targets"])
        F = CF.features(k4_eval._relabel(led, D, U), I["targets"], cl)
        r["rows"] = [{"f": F[(t, y)], "ok": (y in I["desc"][t]) == v} for (t, y), v in sorted(cl.items())]
        r["ledger_sha256"] = led["report"]["ledger_sha256"]
        out["knobs"][knob] = r
    return out


def oof_probs(files, knob):
    """v3's confidence recipe (gradient boosting + isotonic map), fitted out of fold by scenario (5 folds)."""
    from kernel import v3
    fs = [{"file": f["file"], "scenario": f["scenario"], "rows": f["knobs"][knob]["rows"]} for f in files]
    scen = sorted({f["scenario"] for f in fs})
    fold = {s: k % 5 for k, s in enumerate(scen)}
    probs = {}
    for k in range(5):
        m = v3.fit_model([f for f in fs if fold[f["scenario"]] != k])
        for f in fs:
            if fold[f["scenario"]] == k:
                probs[f["file"]] = v3.apply_model(m, f["rows"])
    return probs


def paired_half(files, probs, a, b):
    """Scenario-cluster bootstrap of precision_half(a) - precision_half(b) on the same resampled scenarios."""
    from kernel import v3
    from score import paired
    by = {}
    for f in files:
        g = by.setdefault(f["scenario"], {"a": [0, []], "b": [0, []]})
        for side, knob in (("a", a), ("b", b)):
            g[side][0] += f["pairs"]
            g[side][1] += [(p, r["ok"]) for p, r in zip(probs[knob][f["file"]], f["knobs"][knob]["rows"])]
    groups = {s: [v] for s, v in by.items()}

    def stat(gs):
        A = [tuple(x["a"]) for g in gs for x in g]
        Bq = [tuple(x["b"]) for g in gs for x in g]
        return v3.half(A)[0] - v3.half(Bq)[0]
    return paired.cluster_bootstrap(groups, stat=stat)


def paired_metric(files, key, a, b):
    from score import paired
    by = {}
    for f in files:
        ka, kb = f["knobs"].get(a, {}), f["knobs"].get(b, {})
        if key in ka and key in kb:
            by.setdefault(f["scenario"], []).append(ka[key] - kb[key])
    return paired.cluster_bootstrap(by) if by else None


def cmd_evaluate(a):
    from kernel import v3
    import numpy as np
    out = {"tickets": ["BLD-18", "TGT-18", "TGT-19"], "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest() if PREREG.exists() else None,
           "knobs": {k: KNOBS[k] for k in a.knobs}, "families": {}}
    for fam in a.family:
        jobs = [(f, fam, list(a.knobs)) for f in dev_files(fam, a.limit)]
        with mp.get_context("fork").Pool(a.workers) as pool:
            rows = list(pool.imap(file_rows, jobs, chunksize=2))
        usable = [f for f in rows if all("rows" in f["knobs"].get(k, {}) for k in a.knobs)]
        res = {"files": len(rows), "usable_all_knobs": len(usable),
               "missing": {k: sum(1 for f in rows if f["knobs"].get(k, {}).get("missing")) for k in a.knobs},
               "ges_failed": {k: sum(1 for f in rows if f["knobs"].get(k, {}).get("ges_failed")) for k in a.knobs}, "knobs": {}}
        probs = {}
        for k in a.knobs:
            fs = [{"file": f["file"], "scenario": f["scenario"], "pairs": f["pairs"], "rows": f["knobs"][k]["rows"]} for f in usable]
            probs[k] = oof_probs(usable, k)
            sc = v3.scored(fs, probs[k])
            eng_m = {m: float(np.mean([f["knobs"][k][m] for f in usable if m in f["knobs"][k]]))
                     for m in ("ges_directed_f1", "ges_skeleton_f1", "ges_false_adj", "ges_missed_adj", "ledger_directed_f1")}
            tm = [f["knobs"][k]["true_minus_found"] for f in usable if "true_minus_found" in f["knobs"][k]]
            eng_m["true_dag_at_least_found_share"] = float(np.mean([x >= -0.1 for x in tm])) if tm else None   # GES score drift (X1)
            eng_m["true_minus_found_median"] = float(np.median(tm)) if tm else None
            res["knobs"][k] = {"landmark": {x: sc[x] for x in ("precision_half", "coverage_half", "er2_interval", "ece", "ece_interval",
                                                               "ER-2_met", "ER-3_met", "claims")}, "engine": eng_m}
            print("%-8s %s  P@half %.3f [%.3f, %.3f] cov %.3f ECE %.3f | GES dirF1 %.3f skelF1 %.3f falseAdj %.1f | true>=found %s" % (
                fam, k, sc["precision_half"], sc["er2_interval"]["lo"], sc["er2_interval"]["hi"], sc["coverage_half"], sc["ece"],
                eng_m["ges_directed_f1"], eng_m["ges_skeleton_f1"], eng_m["ges_false_adj"], eng_m["true_dag_at_least_found_share"]), flush=True)
        base = "G0"
        res["paired_vs_G0"] = {k: {"precision_half": paired_half(usable, probs, k, base),
                                   "ges_directed_f1": paired_metric(usable, "ges_directed_f1", k, base),
                                   "ges_skeleton_f1": paired_metric(usable, "ges_skeleton_f1", k, base),
                                   "ges_false_adj": paired_metric(usable, "ges_false_adj", k, base)}
                               for k in a.knobs if k != base}
        if "G1" in a.knobs:
            res["paired_vs_G1"] = {k: {"precision_half": paired_half(usable, probs, k, "G1"),
                                       "ges_skeleton_f1": paired_metric(usable, "ges_skeleton_f1", k, "G1")}
                                   for k in a.knobs if k not in ("G0", "G1")}
        out["families"][fam] = res
    RES.mkdir(parents=True, exist_ok=True)
    (RES / ("dev%s.json" % ("_smoke" if a.limit else ""))).write_text(json.dumps(out, indent=1, default=float))
    return 0


# ------------------------------------------------------------------------------------------------ decide
def decide(dev, pre):
    """The pre-registered rule (plans/v4_prereg.json, 'rule'), applied to analysis/results/v4/dev.json."""
    R = pre["rule"]
    sem, form = dev["families"]["semantic"], dev["families"]["formula"]
    base_sem = sem["knobs"]["G0"]["landmark"]
    base_form = form["knobs"]["G0"]["landmark"]
    rows = {}
    for k in R["candidates"]:
        ls, lf = sem["knobs"][k]["landmark"], form["knobs"][k]["landmark"]
        d = sem["paired_vs_G0"][k]["precision_half"]
        eligible = (ls["coverage_half"] >= R["min_coverage"] and ls["ece"] <= R["max_ece"]
                    and lf["precision_half"] >= base_form["precision_half"] - R["formula_tolerance"])
        rows[k] = {"semantic_precision_half": ls["precision_half"], "formula_precision_half": lf["precision_half"],
                   "semantic_gain_vs_G0": d, "eligible": eligible,
                   "adoptable": eligible and d["point"] >= R["min_gain"] and d["lo"] > 0}
    adopt = [k for k in rows if rows[k]["adoptable"]]
    E = lambda fam, k, m: dev["families"][fam]["knobs"][k]["engine"].get(m)
    best_add = max(("A1", "A2"), key=lambda k: E("semantic", k, "ges_skeleton_f1"))
    g1g0 = sem["knobs"]["G1"]["landmark"]["precision_half"] - base_sem["precision_half"]
    elig = [k for k in rows if rows[k]["eligible"]]
    best_elig = max(elig, key=lambda k: rows[k]["semantic_precision_half"]) if elig else None
    Q = {"Q1": {"knob": best_add, "value": sem["paired_vs_G1"][best_add]["ges_skeleton_f1"]["point"], "bar": ">= 0.03"},
         "Q2": {"value": E("semantic", "A1", "true_dag_at_least_found_share"), "bar": ">= 0.30"},
         "Q3": {"value": 1 - E("semantic", "A1", "ges_false_adj") / E("semantic", "G1", "ges_false_adj"), "bar": ">= 0.20 reduction"},
         "Q4": {"value": g1g0, "bar": "|.| <= 0.01"},
         "Q5": {"knob": best_elig, "value": None if best_elig is None else rows[best_elig]["formula_precision_half"] - base_form["precision_half"],
                "bar": ">= -0.01"}}
    Q["Q1"]["holds"] = Q["Q1"]["value"] >= 0.03
    Q["Q2"]["holds"] = Q["Q2"]["value"] is not None and Q["Q2"]["value"] >= 0.30
    Q["Q3"]["holds"] = Q["Q3"]["value"] >= 0.20
    Q["Q4"]["holds"] = abs(Q["Q4"]["value"]) <= 0.01
    Q["Q5"]["holds"] = None if Q["Q5"]["value"] is None else Q["Q5"]["value"] >= -0.01
    winner = max(adopt, key=lambda k: rows[k]["semantic_precision_half"]) if adopt else None
    return {"rows": rows, "winner": winner, "predictions": Q, "base_semantic_precision_half": base_sem["precision_half"],
            "outcome": ("adopt %s as the v4 score: freeze it and read it once on the fresh held-out family (family 2, rep001)" % winner)
            if winner else "no candidate clears the rule: the score lever alone does not move dev precision enough; v3 stays the kernel"}


def cmd_decide(a):
    dev = json.loads((RES / "dev.json").read_text())
    pre = json.loads(PREREG.read_text())
    out = decide(dev, pre)
    out["prereg_sha256"] = hashlib.sha256(PREREG.read_bytes()).hexdigest()
    (RES / "decision.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps({"winner": out["winner"], "outcome": out["outcome"]}))
    return 0


def fill_one(args):
    path, family = args
    from score import bench
    from kernel import cache
    s = bench.load(path)
    hit = cache.has(s["values"], list(s["node_ids"]))
    cache.engines(s["values"], list(s["node_ids"]))           # v3's engines on a miss (another BLAS kernel), cached
    return hit


def cmd_fill(a):
    """v3 engine records for every dev file under this machine's BLAS settings, before the knob runs (which read them
    read-only, so parallel parts never race on one cache entry)."""
    jobs = [(f, fam) for fam in a.family for f in dev_files(fam, a.limit)]
    with mp.get_context("fork").Pool(a.workers) as pool:
        hits = list(pool.imap_unordered(fill_one, jobs))
    out = RES / "engines" / "v3_fill.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"files": len(hits), "already_cached": sum(hits), "computed": len(hits) - sum(hits)}, indent=1))
    print("JOB-COMPLETE fill %d files, %d computed" % (len(hits), len(hits) - sum(hits)))
    return 0


def cmd_list(a):
    print(json.dumps({fam: len(dev_files(fam)) for fam in FAMILIES}), json.dumps({k: knob_sha(k) for k in KNOBS if KNOBS[k]}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("list", "fill", "engines", "evaluate", "decide"))
    ap.add_argument("--knob", default="A1", choices=sorted(KNOBS))
    ap.add_argument("--knobs", nargs="*", default=list(KNOBS))
    ap.add_argument("--family", nargs="*", default=list(FAMILIES))
    ap.add_argument("--part", default="1/1")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0, help="first N files per family (smoke)")
    a = ap.parse_args(argv)
    return {"list": cmd_list, "fill": cmd_fill, "engines": cmd_engines, "evaluate": cmd_evaluate, "decide": cmd_decide}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
