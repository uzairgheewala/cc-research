"""Link filters L8 (shadow ordering) and L7 (resampling stability) on the v3 ledger's found links (dev; plans/linkfilt_prereg.json).

  python analysis/q2_linkfilt.py collect-l8   -> analysis/results/q2_v3/linkfilt_l8_links_dev.jsonl.gz (125 files per family)
  python analysis/q2_linkfilt.py collect-l7   -> analysis/results/q2_v3/linkfilt_l7_links_dev.jsonl.gz (25 rep000 files per family;
                                                 needs the resample engines: kernel.harness fill --resamples 10)
  python analysis/q2_linkfilt.py evaluate     -> analysis/results/q2_v3/linkfilt_dev.json
"""
import gzip, json, multiprocessing as mp, os, sys, time
from collections import defaultdict
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
RES = ROOT / "analysis" / "results" / "q2_v3"
L8F, L7F = RES / "linkfilt_l8_links_dev.jsonl.gz", RES / "linkfilt_l7_links_dev.jsonl.gz"
OPEN = ("meek_r1", "meek_r3")
GRID = {"L8a": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "L8b": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "L7": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}
BAR, MIN_RECALL, MIN_CUTS = 0.80, 0.10, 30


def _ledger(X, names):
    from kernel import build as B, cache, experiment
    led, _ = B.build(X, names, rule="C3", eng=cache.engines(X, names, read_only=True), created_utc="")
    if led is None:
        return None
    return experiment.configure(led, OPEN)


def _label(e, I, anc_of):
    a, b = tuple(sorted(e))
    T = I["T"]
    if (a, b) in T or (b, a) in T:
        return "true"
    desc = I["desc"]
    if b in desc[a] or a in desc[b]:
        return "shadow"
    if anc_of[a] & anc_of[b]:
        return "common_cause"
    return "unrelated"


def _base(path, family):
    import numpy as np
    from score import bench
    name = Path(path).name
    s = bench.load(path)
    X, names = np.asarray(s["values"], dtype=float), list(s["node_ids"])
    g = _ledger(X, names)
    if g is None:
        return None
    D, U = g
    I = bench.truth_info(family, name)
    n = I["n"]
    anc_of = {v: {a for a in range(n) if v in I["desc"][a]} for v in range(n)}
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    return name, bench.scenario_of(name), X, names, D, U, I, adj, anc_of


def _one_l8(args):
    path, family = args
    from kernel import linkfilt as F
    b = _base(path, family)
    if b is None:
        return None
    name, scen, X, names, D, U, I, adj, anc_of = b
    ra, rb = F.dpi_ratios(adj, F.spearman_matrix(X)), F.dpi_ratios(adj, F.mi_matrix(X))
    links = [{"a": min(e), "b": max(e), "label": _label(e, I, anc_of), "L8a": ra[e], "L8b": rb[e]} for e in sorted(adj, key=sorted)]
    return {"file": name, "scenario": scen, "D": sorted(map(list, D)), "U": sorted(map(list, U)), "links": links}


def _one_l7(args):
    path, family = args
    from kernel import harness
    b = _base(path, family)
    if b is None:
        return None
    name, scen, X, names, D, U, I, adj, anc_of = b
    counts, done = defaultdict(int), 0
    for idx in harness.resample_indices(X.shape[0], 10):
        g = _ledger(X[idx], names)
        if g is None:
            continue
        done += 1
        for e in {frozenset(x) for x in g[0]} | {frozenset(u) for u in g[1]}:
            counts[e] += 1
    links = [{"a": min(e), "b": max(e), "label": _label(e, I, anc_of), "L7": counts[e] / done if done else None}
             for e in sorted(adj, key=sorted)]
    return {"file": name, "scenario": scen, "resamples": done, "D": sorted(map(list, D)), "U": sorted(map(list, U)), "links": links}


def _collect(fn, out, reps, workers):
    from score import bench
    with gzip.open(out, "wt") as fh:
        for fam in ("semantic", "formula"):
            fs = [str(p) for p in bench.files(fam, split="dev")]
            if reps is not None:
                fs = [f for f in fs if any(f.endswith("__rep%03d.npz" % r) for r in reps)]
            t0 = time.time()
            with mp.get_context("fork").Pool(workers) as pool:
                k = 0
                for r in pool.imap(fn, [(f, fam) for f in fs]):
                    if r:
                        r["family"] = fam
                        fh.write(json.dumps(r) + "\n")
                        k += 1
            print(fam, "files", k, "%.0fs" % (time.time() - t0), flush=True)


# ------------------------------------------------------------------------------------------------------------ evaluate
def _cut(link, filt, c):
    v = link.get(filt)
    if v is None:
        return False
    return v < c


def _stats(links, filt, c):
    cut = [l for l in links if _cut(l, filt, c)]
    false = [l for l in links if l["label"] != "true"]
    true = [l for l in links if l["label"] == "true"]
    cf = sum(1 for l in cut if l["label"] != "true")
    return {"cuts": len(cut), "cut_precision": round(cf / len(cut), 3) if cut else None,
            "cut_recall": round(cf / len(false), 3) if false else None,
            "true_lost": round((len(cut) - cf) / len(true), 3) if true else None,
            "cut_by_kind": {k: sum(1 for l in cut if l["label"] == k) for k in ("shadow", "common_cause", "unrelated", "true")}}


def _auc(pos, neg):
    """P(random true more stable than random false), ties half."""
    if not pos or not neg:
        return None
    import numpy as np
    p, q = np.array(pos), np.array(neg)
    gt = (p[:, None] > q[None, :]).sum() + 0.5 * (p[:, None] == q[None, :]).sum()
    return round(float(gt) / (len(p) * len(q)), 3)


def _answers(files_rows, cuts_by_file, family):
    """DV-1 precision / coverage and directed F1 of the ledger graph with and without the cuts (no re-orientation)."""
    from score import bench, dv, graph
    agg = {"base": [0, 0, 0, 0.0], "cut": [0, 0, 0, 0.0]}
    nf = 0
    for fr in files_rows:
        I = bench.truth_info(family, fr["file"])
        D = {tuple(e) for e in fr["D"]}
        U = {tuple(e) for e in fr["U"]}
        cuts = cuts_by_file.get(fr["file"], set())
        D2 = {e for e in D if frozenset(e) not in cuts}
        U2 = {e for e in U if frozenset(e) not in cuts}
        pairs = dv.n_pairs(I["n"], I["targets"])
        seed = graph.file_seed(fr["file"])
        for k, (d, u) in (("base", (D, U)), ("cut", (D2, U2))):
            ch = dv.check(dv.claims(I["n"], d, u, I["targets"]), I["desc"])
            agg[k][0] += len(ch)
            agg[k][1] += sum(ok for *_, ok in ch)
            agg[k][2] += pairs
            agg[k][3] += graph.directed_f1(d, u, I["T"], seed)["f1"]
        nf += 1
    out = {}
    for k, (com, ok, pairs, f1) in agg.items():
        out[k] = {"dv1_precision": round(ok / com, 3) if com else None, "coverage": round(com / pairs, 3), "f1": round(f1 / nf, 3)}
    return out


def _crossfit(files, filt, family):
    scen = sorted({f["scenario"] for f in files})
    fold = {s: k % 5 for k, s in enumerate(scen)}
    picks, test_links, cuts_by_file = [], [], {}
    for k in range(5):
        tr = [l for f in files if fold[f["scenario"]] != k for l in f["links"]]
        te_files = [f for f in files if fold[f["scenario"]] == k]
        best = None
        for c in GRID[filt]:
            st = _stats(tr, filt, c)
            if st["cuts"] >= MIN_CUTS and st["cut_precision"] is not None and st["cut_precision"] >= BAR:
                best = c                                   # grid ascending: keep the most permissive that passes
        picks.append(best)
        for f in te_files:
            test_links += [dict(l, _cutnow=best is not None and _cut(l, filt, best)) for l in f["links"]]
            if best is not None:
                cuts_by_file[f["file"]] = {frozenset((l["a"], l["b"])) for l in f["links"] if _cut(l, filt, best)}
    cut = [l for l in test_links if l["_cutnow"]]
    false = [l for l in test_links if l["label"] != "true"]
    cf = sum(1 for l in cut if l["label"] != "true")
    prec = cf / len(cut) if cut else None
    rec = cf / len(false) if false else 0.0
    res = {"cut_offs": picks, "cuts": len(cut), "cut_precision": None if prec is None else round(prec, 3),
           "cut_recall": round(rec, 3), "true_lost": round((len(cut) - cf) / max(1, sum(1 for l in test_links if l["label"] == "true")), 3),
           "cut_by_kind": {k: sum(1 for l in cut if l["label"] == k) for k in ("shadow", "common_cause", "unrelated", "true")},
           "licence": bool(prec is not None and prec >= BAR and rec >= MIN_RECALL)}
    return res, cuts_by_file


def evaluate():
    out = {"prereg": "plans/linkfilt_prereg.json", "bar": BAR, "min_recall": MIN_RECALL, "families": {}}
    data = {}
    for path, tag in ((L8F, "l8"), (L7F, "l7")):
        if not path.exists():
            continue
        with gzip.open(path, "rt") as fh:
            for line in fh:
                r = json.loads(line)
                data.setdefault((r["family"], tag), []).append(r)
    for fam in ("semantic", "formula"):
        F = {}
        for tag, filts in (("l8", ("L8a", "L8b")), ("l7", ("L7",))):
            files = data.get((fam, tag))
            if not files:
                continue
            links = [l for f in files for l in f["links"]]
            kinds = {k: sum(1 for l in links if l["label"] == k) for k in ("true", "shadow", "common_cause", "unrelated")}
            F[tag] = {"files": len(files), "links": len(links), "kinds": kinds}
            if tag == "l8":
                sh = [l for l in links if l["label"] == "shadow"]
                F[tag]["shadow_in_triangle_share"] = round(sum(1 for l in sh if l["L8a"] is not None) / len(sh), 3) if sh else None
                F[tag]["in_triangle_share_by_kind"] = {k: round(sum(1 for l in links if l["label"] == k and l["L8a"] is not None) / max(1, kinds[k]), 3) for k in kinds}
            if tag == "l7":
                import statistics as st_
                F[tag]["median_stability"] = {k: st_.median([l["L7"] for l in links if l["label"] == k and l["L7"] is not None] or [float("nan")]) for k in kinds}
                F[tag]["auc_true_vs_false"] = _auc([l["L7"] for l in links if l["label"] == "true"], [l["L7"] for l in links if l["label"] != "true"])
            for filt in filts:
                F[filt] = {"grid": {str(c): _stats(links, filt, c) for c in GRID[filt]}}
                cf, cuts = _crossfit(files, filt, fam)
                F[filt]["crossfit"] = cf
                F[filt]["answers"] = _answers(files, cuts, fam) if any(cuts.values()) else None
            if tag == "l7" and "l8" in F:
                # secondary: union of L7 and L8a cuts on the L7 files, each at its own cross-fitted cut-off
                l8_by_file = {f["file"]: f for f in data[(fam, "l8")]}
                merged = []
                for f in files:
                    g = l8_by_file.get(f["file"])
                    if g is None:
                        continue
                    a8 = {(l["a"], l["b"]): l["L8a"] for l in g["links"]}
                    merged.append(dict(f, links=[dict(l, L8a=a8.get((l["a"], l["b"]))) for l in f["links"]]))
                _, c7 = _crossfit(merged, "L7", fam)
                _, c8 = _crossfit(merged, "L8a", fam)
                union = {k: c7.get(k, set()) | c8.get(k, set()) for k in set(c7) | set(c8)}
                cut = [l for f in merged for l in f["links"] if frozenset((l["a"], l["b"])) in union.get(f["file"], set())]
                false = [l for f in merged for l in f["links"] if l["label"] != "true"]
                cfp = sum(1 for l in cut if l["label"] != "true")
                F["L7_or_L8a"] = {"cuts": len(cut), "cut_precision": round(cfp / len(cut), 3) if cut else None,
                                  "cut_recall": round(cfp / len(false), 3) if false else None,
                                  "answers": _answers(merged, union, fam) if any(union.values()) else None}
        out["families"][fam] = F
        print("==", fam, json.dumps({k: v for k, v in F.get("l8", {}).items()}), json.dumps(F.get("l7", {})))
        for filt in ("L8a", "L8b", "L7"):
            if filt in F:
                c = F[filt]["crossfit"]
                print("  %-4s crossfit cut-offs %s | cuts %d precision %s recall %s true lost %s | by kind %s | licence %s | answers %s" % (
                    filt, c["cut_offs"], c["cuts"], c["cut_precision"], c["cut_recall"], c["true_lost"], c["cut_by_kind"], c["licence"], F[filt]["answers"]))
                print("       grid:", " ".join("%s:%s/%s/%s" % (k, v["cuts"], v["cut_precision"], v["cut_recall"]) for k, v in F[filt]["grid"].items()))
        if "L7_or_L8a" in F:
            print("  L7_or_L8a", F["L7_or_L8a"])
    json.dump(out, open(RES / "linkfilt_dev.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "collect-l8":
        _collect(_one_l8, L8F, None, int(os.environ.get("WORKERS", "1")))
    elif cmd == "collect-l7":
        _collect(_one_l7, L7F, [0], int(os.environ.get("WORKERS", "2")))
    else:
        evaluate()
