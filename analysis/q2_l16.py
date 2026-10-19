"""L16: applicability conditions for the link filters licensed on formula (dev; plans/l16_prereg.json). Tickets: TGT-18, TGT-19

  python analysis/q2_l16.py collect    -> analysis/results/q2_v3/l16_files_dev.jsonl.gz (125 dev obs files per family:
                                          v3 ledger links with labels and L8a ratios, and the observable features G1-G6)
  python analysis/q2_l16.py evaluate   -> analysis/results/q2_v3/l16_dev.json

A gate is decided per file from that file's data and ledger only (features G1-G6); truth labels are used only to score.
The filter is L8a (triangle order on |Spearman|, kernel/linkfilt.py) exactly as linkfilt-1. Nothing here changes the
kernel. Dev split only.
"""
import gzip, json, math, multiprocessing as mp, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(ROOT / "analysis"))
RES = ROOT / "analysis" / "results" / "q2_v3"
FILES = RES / "l16_files_dev.jsonl.gz"
OUT = RES / "l16_dev.json"
FEATURES = ("G1_triangle_share", "G2_dpi_violation_share", "G3_real_triangle_estimate", "G4_discrete_share", "G5_monotone_gap", "G6_density")
CUTS = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
PCTS = [10, 20, 30, 40, 50, 60, 70, 80, 90]
BAR, MIN_RECALL, MIN_CUTS, RHO_GUARD = 0.80, 0.10, 30, 0.30


# ------------------------------------------------------------------------------------------------------------ features
def _norm_sf(z):
    return math.erfc(abs(z) / math.sqrt(2))


def triangles(adj):
    nb = {}
    for e in adj:
        a, b = tuple(e)
        nb.setdefault(a, set()).add(b)
        nb.setdefault(b, set()).add(a)
    out = set()
    for e in adj:
        a, b = sorted(e)
        for m in (nb[a] & nb[b]) - {a, b}:
            out.add(tuple(sorted((a, b, m))))
    return sorted(out)


def storey_pi1(pvals, lam=0.5):
    """1 - Storey's pi0 at lambda, clipped to [0, 1]; None without p-values."""
    if not pvals:
        return None
    pi0 = sum(1 for p in pvals if p > lam) / (len(pvals) * (1 - lam))
    return max(0.0, 1.0 - min(1.0, pi0))


def g3_pvalues(S_signed, tris, n):
    """For each triangle, the weakest link by |Spearman| tested for independence given the third variable: Fisher z on the
    partial correlation of ranks (one conditioning variable, n - 4 degrees)."""
    out = []
    for t in tris:
        pairs = [(t[0], t[1], t[2]), (t[0], t[2], t[1]), (t[1], t[2], t[0])]
        a, b, m = min(pairs, key=lambda q: (abs(S_signed[q[0], q[1]]), q))
        rab, ram, rbm = S_signed[a, b], S_signed[a, m], S_signed[b, m]
        den = math.sqrt(max(1e-12, (1 - ram ** 2) * (1 - rbm ** 2)))
        r = max(-0.999999, min(0.999999, (rab - ram * rbm) / den))
        z = 0.5 * math.log((1 + r) / (1 - r)) * math.sqrt(max(1, n - 4))
        out.append(_norm_sf(z))
    return out


def features(X, adj, ratios):
    import numpy as np
    from kernel import linkfilt as F
    n, p = X.shape
    R = np.column_stack([F._ranks(X[:, j]) for j in range(p)])
    Ssg = np.nan_to_num(np.corrcoef(R, rowvar=False), nan=0.0)
    Psg = np.nan_to_num(np.corrcoef(X, rowvar=False), nan=0.0)
    links = sorted(adj, key=sorted)
    in_tri = [e for e in links if ratios[e] is not None]
    tris = triangles(adj)
    g3p = g3_pvalues(Ssg, tris, n)
    return {
        "G1_triangle_share": len(in_tri) / len(links) if links else None,
        "G2_dpi_violation_share": (sum(1 for e in in_tri if ratios[e] < 0.5) / len(in_tri)) if in_tri else None,
        "G3_real_triangle_estimate": storey_pi1(g3p),
        "G4_discrete_share": sum(1 for j in range(p) if len(np.unique(X[:, j])) <= 10) / p,
        "G5_monotone_gap": (float(np.mean([abs(Ssg[tuple(sorted(e))]) - abs(Psg[tuple(sorted(e))]) for e in links])) if links else None),
        "G6_density": len(links) / p,
    }, {"triangles": len(tris), "g3_tests": len(g3p)}


def _one(args):
    path, family = args
    from kernel import linkfilt as F
    import q2_linkfilt as LF
    b = LF._base(path, family)
    if b is None:
        return None
    name, scen, X, names, D, U, I, adj, anc_of = b
    ra = F.dpi_ratios(adj, F.spearman_matrix(X))
    feats, info = features(X, adj, ra)
    links = [{"a": min(e), "b": max(e), "label": LF._label(e, I, anc_of), "L8a": ra[e]} for e in sorted(adj, key=sorted)]
    return {"file": name, "scenario": scen, "family": family, "features": feats, "info": info,
            "D": sorted(map(list, D)), "U": sorted(map(list, U)), "links": links}


def collect(workers):
    from score import bench
    t0 = time.time()
    with gzip.open(FILES, "wt") as fh:
        for fam in ("semantic", "formula"):
            fs = [str(p) for p in bench.files(fam, split="dev")]
            with mp.get_context("fork").Pool(workers) as pool:
                k = 0
                for r in pool.imap(_one, [(f, fam) for f in fs]):
                    if r:
                        fh.write(json.dumps(r) + "\n")
                        k += 1
            print(fam, k, "files", "%.0fs" % (time.time() - t0), flush=True)


# ------------------------------------------------------------------------------------------------------------ evaluate
def _load():
    with gzip.open(FILES, "rt") as fh:
        return [json.loads(l) for l in fh]


def _gate(f, g, side, t):
    v = f["features"][g]
    if v is None:
        return False
    return v <= t if side == "le" else v >= t


def _pool(files, gatefn, c):
    cut = fl = 0
    for f in files:
        fl += sum(1 for l in f["links"] if l["label"] != "true")
    cf = 0
    for f in files:
        if not gatefn(f):
            continue
        for l in f["links"]:
            if l["L8a"] is not None and l["L8a"] < c:
                cut += 1
                cf += l["label"] != "true"
    return cut, cf, fl


def _pct(vals, q):
    import numpy as np
    return float(np.percentile(vals, q)) if vals else None


def folds(files):
    out = {}
    for fam in ("semantic", "formula"):
        sc = sorted({f["scenario"] for f in files if f["family"] == fam})
        out.update({s: k % 5 for k, s in enumerate(sc)})
    return out


def _choose(train, feats):
    best = None
    for g in feats:
        vals = [f["features"][g] for f in train if f["features"][g] is not None]
        for side in ("le", "ge"):
            for q in PCTS:
                t = _pct(vals, q)
                if t is None:
                    continue
                for c in CUTS:
                    cut, cf, fl = _pool(train, lambda f: _gate(f, g, side, t), c)
                    if cut < MIN_CUTS or cf / cut < BAR:
                        continue
                    key = (cf / fl, cf / cut)
                    if best is None or key > best[0]:
                        best = (key, {"feature": g, "side": side, "pct": q, "threshold": t, "cut_off": c})
    return best[1] if best else None


def _crossfit(files, feats):
    fd = folds(files)
    picks, test_cut, test_cf, test_fl, by_fam = [], 0, 0, 0, {"semantic": [0, 0, 0, 0], "formula": [0, 0, 0, 0]}
    cuts_by_file = {}
    for k in range(5):
        tr = [f for f in files if fd[f["scenario"]] != k]
        te = [f for f in files if fd[f["scenario"]] == k]
        pick = _choose(tr, feats)
        picks.append(pick)
        for f in te:
            fl = sum(1 for l in f["links"] if l["label"] != "true")
            tl = sum(1 for l in f["links"] if l["label"] == "true")
            test_fl += fl
            by_fam[f["family"]][2] += fl
            by_fam[f["family"]][3] += tl
            if pick is None or not _gate(f, pick["feature"], pick["side"], pick["threshold"]):
                continue
            cs = {(l["a"], l["b"]) for l in f["links"] if l["L8a"] is not None and l["L8a"] < pick["cut_off"]}
            cuts_by_file[f["file"]] = {frozenset(e) for e in cs}
            for l in f["links"]:
                if (l["a"], l["b"]) in cs:
                    test_cut += 1
                    test_cf += l["label"] != "true"
                    by_fam[f["family"]][0] += 1
                    by_fam[f["family"]][1] += l["label"] != "true"
    prec = test_cf / test_cut if test_cut else None
    rec = test_cf / test_fl if test_fl else 0.0
    fam_rows = {fam: {"cuts": v[0], "cut_precision": round(v[1] / v[0], 3) if v[0] else None,
                      "cut_recall": round(v[1] / v[2], 3) if v[2] else None, "true_lost": round((v[0] - v[1]) / v[3], 3) if v[3] else None}
                for fam, v in by_fam.items()}
    return {"picks": picks, "cuts": test_cut, "cut_precision": None if prec is None else round(prec, 3), "cut_recall": round(rec, 3),
            "by_family": fam_rows, "licence": bool(prec is not None and prec >= BAR and rec >= MIN_RECALL)}, cuts_by_file


def _spearman(x, y):
    import numpy as np
    from kernel import linkfilt as F
    if len(x) < 3:
        return None
    rx, ry = F._ranks(np.array(x, float)), F._ranks(np.array(y, float))
    c = np.corrcoef(rx, ry)[0, 1]
    return None if np.isnan(c) else round(float(c), 3)


def _scen_precision(files, c):
    """-> {scenario: (cut precision at c, cuts, family, mean of each feature)}"""
    import numpy as np
    out = {}
    for s in sorted({f["scenario"] for f in files}):
        fs = [f for f in files if f["scenario"] == s]
        cut = [l for f in fs for l in f["links"] if l["L8a"] is not None and l["L8a"] < c]
        cf = sum(1 for l in cut if l["label"] != "true")
        feats = {g: (float(np.mean([f["features"][g] for f in fs if f["features"][g] is not None])) if any(f["features"][g] is not None for f in fs) else None) for g in FEATURES}
        out[s] = {"precision": cf / len(cut) if cut else None, "cuts": len(cut), "family": fs[0]["family"], "features": feats}
    return out


def _rho_table(files, c):
    sp = _scen_precision(files, c)
    rows = {}
    for g in FEATURES:
        r = {}
        for fam in ("pooled", "semantic", "formula"):
            pts = [(v["features"][g], v["precision"]) for v in sp.values() if v["cuts"] >= 5 and v["precision"] is not None
                   and v["features"][g] is not None and (fam == "pooled" or v["family"] == fam)]
            r[fam] = _spearman([a for a, _ in pts], [b for _, b in pts])
            r[fam + "_n"] = len(pts)
        rows[g] = r
    left_out = sum(1 for v in sp.values() if v["cuts"] < 5)
    return rows, left_out


def _family_auc(files, g):
    pos = [f["features"][g] for f in files if f["family"] == "formula" and f["features"][g] is not None]
    neg = [f["features"][g] for f in files if f["family"] == "semantic" and f["features"][g] is not None]
    if not pos or not neg:
        return None
    gt = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg)
    a = gt / (len(pos) * len(neg))
    return round(max(a, 1 - a), 3)


def _declared(files):
    """Oracle gate (act on formula only) and the harm of the same filter wrongly declared on semantic."""
    import q2_linkfilt as LF
    form = [dict(f, links=[dict(l) for l in f["links"]]) for f in files if f["family"] == "formula"]
    sem = [f for f in files if f["family"] == "semantic"]
    cf_form, cuts_form = LF._crossfit(form, "L8a", "formula")
    picks = cf_form["cut_offs"]
    # wrong declaration: semantic files cut at formula's fold cut-offs (fold of the semantic scenario's position)
    sc = sorted({f["scenario"] for f in sem})
    fold = {s: k % 5 for k, s in enumerate(sc)}
    cuts_sem, cut, cf = {}, 0, 0
    true_sem = sum(1 for f in sem for l in f["links"] if l["label"] == "true")
    false_sem = sum(1 for f in sem for l in f["links"] if l["label"] != "true")
    for f in sem:
        c = picks[fold[f["scenario"]]]
        if c is None:
            continue
        cs = {frozenset((l["a"], l["b"])) for l in f["links"] if l["L8a"] is not None and l["L8a"] < c}
        cuts_sem[f["file"]] = cs
        for l in f["links"]:
            if frozenset((l["a"], l["b"])) in cs:
                cut += 1
                cf += l["label"] != "true"
    ans = LF._answers(sem, cuts_sem, "semantic")
    total_false = sum(1 for f in files for l in f["links"] if l["label"] != "true")
    return {"value_if_right": {"formula_crossfit": cf_form, "pooled_cut_recall": round(cf_form["cut_recall"] * sum(1 for f in form for l in f["links"] if l["label"] != "true") / total_false, 3),
                               "answers_formula": LF._answers(form, cuts_form, "formula")},
            "harm_if_wrong": {"semantic_cuts": cut, "cut_precision": round(cf / cut, 3) if cut else None, "true_lost": round((cut - cf) / true_sem, 3),
                              "false_cut": round(cf / false_sem, 3), "answers_semantic": ans,
                              "dv1_precision_change": round(ans["cut"]["dv1_precision"] - ans["base"]["dv1_precision"], 3),
                              "coverage_change": round(ans["cut"]["coverage"] - ans["base"]["coverage"], 3),
                              "f1_change": round(ans["cut"]["f1"] - ans["base"]["f1"], 3)}}


def _repro_check(files):
    """The rebuilt ledgers' links and L8a ratios against linkfilt-1's stored rows."""
    p = RES / "linkfilt_l8_links_dev.jsonl.gz"
    if not p.exists():
        return {"checked": False}
    old = {}
    with gzip.open(p, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            old[r["file"]] = {(l["a"], l["b"]): l["L8a"] for l in r["links"]}
    same = diff = 0
    for f in files:
        o = old.get(f["file"])
        new = {(l["a"], l["b"]): l["L8a"] for l in f["links"]}
        if o is None:
            continue
        ok = set(o) == set(new) and all((o[k] is None and new[k] is None) or (o[k] is not None and new[k] is not None and abs(o[k] - new[k]) < 1e-12) for k in o)
        same += ok
        diff += not ok
    return {"checked": True, "files_identical": same, "files_different": diff}


def evaluate():
    files = _load()
    out = {"prereg": "plans/l16_prereg.json", "tickets": ["TGT-18", "TGT-19"], "files": {fam: sum(1 for f in files if f["family"] == fam) for fam in ("semantic", "formula")},
           "reproduction_vs_linkfilt1": _repro_check(files)}
    out["links"] = {fam: {k: sum(1 for f in files if f["family"] == fam for l in f["links"] if l["label"] == k) for k in ("true", "shadow", "common_cause", "unrelated")}
                    for fam in ("semantic", "formula")}
    out["feature_summary"] = {}
    import numpy as np
    for g in FEATURES:
        row = {}
        for fam in ("semantic", "formula"):
            v = [f["features"][g] for f in files if f["family"] == fam and f["features"][g] is not None]
            row[fam] = {"median": round(float(np.median(v)), 3) if v else None, "p10": round(_pct(v, 10), 3) if v else None,
                        "p90": round(_pct(v, 90), 3) if v else None, "missing": sum(1 for f in files if f["family"] == fam and f["features"][g] is None)}
        row["family_auc"] = _family_auc(files, g)
        out["feature_summary"][g] = row
    # selected gate over all features, then each feature alone
    sel, cuts_sel = _crossfit(files, FEATURES)
    out["selected_gate"] = sel
    out["single_feature"] = {g: _crossfit(files, (g,))[0] for g in FEATURES}
    # answers for the selected gate, per family
    import q2_linkfilt as LF
    if cuts_sel:
        out["selected_gate"]["answers"] = {fam: LF._answers([f for f in files if f["family"] == fam], cuts_sel, fam) for fam in ("semantic", "formula")}
    # correlations with per-scenario cut precision (P-A2 at 0.7; other cut-offs reported)
    out["rho_by_cut_off"] = {}
    for c in CUTS:
        rows, left = _rho_table(files, c)
        out["rho_by_cut_off"][str(c)] = {"rho": rows, "scenarios_left_out_fewer_than_5_cuts": left}
    # transfer guard for any licensed gate (selected and single features)
    def guard(res):
        if not res["licence"]:
            return None
        gs = [p["feature"] for p in res["picks"] if p]
        cs = [p["cut_off"] for p in res["picks"] if p]
        g = max(set(gs), key=gs.count)
        c = max(set(cs), key=cs.count)
        rows, _ = _rho_table(files, c)
        r = rows[g]
        return {"feature": g, "modal_cut_off": c, "rho_semantic": r["semantic"], "rho_formula": r["formula"],
                "passes": bool(r["semantic"] is not None and r["formula"] is not None and r["semantic"] >= RHO_GUARD and r["formula"] >= RHO_GUARD),
                "family_auc": _family_auc(files, g)}
    out["selected_gate"]["transfer_guard"] = guard(sel)
    for g in FEATURES:
        out["single_feature"][g]["transfer_guard"] = guard(out["single_feature"][g])
    out["declared"] = _declared(files)
    # verdicts
    any_lic = sel["licence"] or any(v["licence"] for v in out["single_feature"].values())
    r07 = out["rho_by_cut_off"]["0.7"]["rho"]
    absr = {g: abs(r07[g]["pooled"]) if r07[g]["pooled"] is not None else -1 for g in FEATURES}
    top = max(absr, key=absr.get)
    lic_gates = [v for v in [sel] + list(out["single_feature"].values()) if v["licence"]]
    harm = out["declared"]["harm_if_wrong"]
    out["verdicts"] = {
        "P-A1": "refuted" if any_lic else "supported",
        "P-A2": ("supported" if top == "G3_real_triangle_estimate" and absr[top] >= 0.40 else
                 "refuted" if (top != "G3_real_triangle_estimate" or absr["G3_real_triangle_estimate"] < 0.25) else "inconclusive"),
        "P-A2_detail": {"largest": top, "abs_rho": {g: round(v, 3) for g, v in absr.items()}},
        "P-A3": (None if not lic_gates else ("refuted" if any(v["transfer_guard"] and v["transfer_guard"]["passes"] for v in lic_gates) else "supported")),
        "P-A4": ("refuted" if harm["dv1_precision_change"] < -0.04 else
                 "supported" if (harm["dv1_precision_change"] >= -0.02 and harm["f1_change"] >= -0.03 and harm["true_lost"] > 0.10) else "partly"),
    }
    json.dump(out, open(OUT, "w"), indent=1, default=float)
    print(json.dumps({k: out[k] for k in ("files", "reproduction_vs_linkfilt1", "verdicts")}, indent=1))
    print("selected:", json.dumps({k: v for k, v in sel.items() if k != "answers"}, default=str))
    for g, v in out["single_feature"].items():
        print("  %-28s licence %-5s prec %s rec %s by fam %s" % (g, v["licence"], v["cut_precision"], v["cut_recall"], json.dumps(v["by_family"])))
    print("declared:", json.dumps(out["declared"], default=str)[:1500])


if __name__ == "__main__":
    if sys.argv[1] == "collect":
        collect(int(os.environ.get("WORKERS", "2")))
    else:
        evaluate()
