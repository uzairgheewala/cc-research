"""Direction signals on the v3 ledger's found links (dev; plans/dirsig_prereg.json). Two steps:

  python analysis/q2_dirsig.py collect   -> analysis/results/q2_v3/dirsig_links_dev.jsonl.gz (one row per found link)
  python analysis/q2_dirsig.py evaluate  -> analysis/results/q2_v3/dirsig_dev.json (the pre-registered statistics)

collect reads the engine cache only; evaluate reads the rows only (seconds), so the statistics can be re-derived without
touching the data.
"""
import gzip, json, multiprocessing as mp, os, sys, time, zlib
from collections import defaultdict
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
RES = ROOT / "analysis" / "results" / "q2_v3"
ROWS = RES / "dirsig_links_dev.jsonl.gz"
OPEN = ("meek_r1", "meek_r3")
BAR, MIN_YIELD = 0.80, 0.10


def _one(args):
    path, family, regime = args
    import numpy as np
    from score import bench
    from kernel import asym, build as B, cache, harness, experiment
    name = Path(path).name
    if regime == "DxR":
        X, names = harness.pooled_table(path)
    else:
        s = bench.load(path)
        X, names = s["values"], list(s["node_ids"])
    X = np.asarray(X, dtype=float)
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    if led is None:
        return []
    D, U = experiment.configure(led, OPEN)
    pos = {v["name"]: v["position"] for v in led["variables"]}
    lic = {(pos[c["x"]], pos[c["y"]]): c["licensed_by"] for c in led["claims"] if c["relation"] == "x->y"}
    I = bench.truth_info(family, name)
    T, desc = set(I["T"]), I["desc"]
    mec_open = {frozenset(e) for e in I["cpdag_undirected"]}
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    out = []
    for e in sorted(tuple(sorted(p)) for p in adj):
        a, b = e
        truth = 1 if (a, b) in T else (-1 if (b, a) in T else 0)
        anc = 1 if b in desc[a] else (-1 if a in desc[b] else 0)
        led_dir = 1 if (a, b) in D else (-1 if (b, a) in D else 0)
        da, db = asym.is_discrete(X[:, a]), asym.is_discrete(X[:, b])
        seed = zlib.crc32(("%s:%d:%d" % (name, a, b)).encode())
        out.append({"file": name, "scenario": bench.scenario_of(name), "a": a, "b": b, "truth": truth, "anc": anc,
                    "led": led_dir, "lic": lic.get((a, b)) or lic.get((b, a)), "mec_open": frozenset(e) in mec_open,
                    "ptype": "cc" if not (da or db) else ("dd" if (da and db) else "cd"),
                    "s": asym.all_signals(X[:, a], X[:, b], seed=seed)})
    return out


def collect(workers=4):
    from score import bench
    RES.mkdir(parents=True, exist_ok=True)
    with gzip.open(ROWS, "wt") as fh:
        for fam in ("semantic", "formula"):
            for reg in ("D", "DxR"):
                fs = [str(p) for p in bench.files(fam, split="dev")]
                if reg == "DxR":
                    fs = [f for f in fs if f.endswith("__rep000.npz")]
                t0 = time.time()
                with mp.get_context("fork").Pool(workers) as pool:
                    k = 0
                    for rows in pool.imap(_one, [(f, fam, reg) for f in fs]):
                        for r in rows:
                            r.update(family=fam, regime=reg)
                            fh.write(json.dumps(r) + "\n")
                            k += 1
                print(fam, reg, "links", k, "%.0fs" % (time.time() - t0), flush=True)


# ------------------------------------------------------------------------------------------------------------ evaluate
def _stratum(r):
    if r["truth"] == 0:
        return None
    if r["led"] != 0:
        return "committed_right" if r["led"] == r["truth"] else "committed_reversed"
    return "open_class_open" if r["mec_open"] else "open_class_orients"


def _acc(rows, sig, key="truth"):
    v = [(r["s"][sig], r[key]) for r in rows if r["s"][sig] is not None and r[key] != 0 and r["s"][sig] != 0]
    if not v:
        return {"n": 0, "acc": None}
    return {"n": len(v), "acc": round(sum((s > 0) == (t > 0) for s, t in v) / len(v), 3)}


def _crossfit(rows, sig):
    """Pre-registered licence rule: threshold on |score| chosen on 4 scenario folds to reach the bar, measured on the 5th.
    Yield is over the left-open true links of the held-out fold (the links a licence would act on)."""
    scen = sorted({r["scenario"] for r in rows})
    fold = {s: k % 5 for k, s in enumerate(scen)}
    tested = [r for r in rows if r["truth"] != 0 and r["s"][sig] is not None and r["s"][sig] != 0]
    hits = n_acted = n_open = acted_open = hits_open = 0
    taus = []
    for k in range(5):
        tr = [r for r in tested if fold[r["scenario"]] != k]
        te = [r for r in tested if fold[r["scenario"]] == k]
        tau = None
        for q in (0.0, 0.5, 0.75, 0.9, 0.95, 0.98):
            mags = sorted(abs(r["s"][sig]) for r in tr)
            if not mags:
                break
            t = mags[int(q * (len(mags) - 1))]
            kept = [r for r in tr if abs(r["s"][sig]) >= t]
            if kept and sum((r["s"][sig] > 0) == (r["truth"] > 0) for r in kept) / len(kept) >= BAR and len(kept) >= 30:
                tau = t
                break
        taus.append(tau)
        if tau is None:
            n_open += sum(1 for r in te if r["led"] == 0)
            continue
        acted = [r for r in te if abs(r["s"][sig]) >= tau]
        n_acted += len(acted)
        hits += sum((r["s"][sig] > 0) == (r["truth"] > 0) for r in acted)
        op = [r for r in te if r["led"] == 0]
        n_open += len(op)
        ao = [r for r in op if abs(r["s"][sig]) >= tau]
        acted_open += len(ao)
        hits_open += sum((r["s"][sig] > 0) == (r["truth"] > 0) for r in ao)
    acc = hits / n_acted if n_acted else None
    acc_o = hits_open / acted_open if acted_open else None
    yld = acted_open / n_open if n_open else 0.0
    return {"thresholds_found": sum(t is not None for t in taus), "acted": n_acted,
            "accuracy": None if acc is None else round(acc, 3),
            "open_acted": acted_open, "open_accuracy": None if acc_o is None else round(acc_o, 3),
            "open_yield": round(yld, 3),
            "licence": bool(acc_o is not None and acc_o >= BAR and yld >= MIN_YIELD)}


def _top_quarter_disagreement(rows, sig):
    """P-DS5: collider-committed true links where the signal disagrees with the ledger, top quarter of |score|."""
    c = [r for r in rows if r["truth"] != 0 and r["led"] != 0 and r["lic"] == "v_structure" and r["s"][sig] not in (None, 0)]
    if not c:
        return {"n": 0}
    mags = sorted(abs(r["s"][sig]) for r in c)
    t = mags[int(0.75 * (len(mags) - 1))]
    dis = [r for r in c if abs(r["s"][sig]) >= t and (r["s"][sig] > 0) != (r["led"] > 0)]
    if not dis:
        return {"n": 0}
    sig_right = sum((r["s"][sig] > 0) == (r["truth"] > 0) for r in dis)
    return {"n": len(dis), "signal_right_share": round(sig_right / len(dis), 3)}


def evaluate():
    from kernel import asym
    sigs = list(asym.SIGNALS)
    by = defaultdict(list)
    with gzip.open(ROWS, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            by[(r["family"], r["regime"])].append(r)
    out = {"prereg": "plans/dirsig_prereg.json", "bar": BAR, "min_yield": MIN_YIELD, "cells": {}}
    for (fam, reg), rows in sorted(by.items()):
        true_rows = [r for r in rows if r["truth"] != 0]
        cell = {"found_links": len(rows), "true_found": len(true_rows),
                "strata": {s: sum(1 for r in true_rows if _stratum(r) == s) for s in
                           ("committed_right", "committed_reversed", "open_class_orients", "open_class_open")},
                "ptype": {p: sum(1 for r in true_rows if r["ptype"] == p) for p in ("cc", "cd", "dd")},
                "signals": {}}
        for sig in sigs:
            d = {"full_yield": _acc(true_rows, sig),
                 "by_stratum": {s: _acc([r for r in true_rows if _stratum(r) == s], sig) for s in cell["strata"]},
                 "by_ptype": {p: _acc([r for r in true_rows if r["ptype"] == p], sig) for p in ("cc", "cd", "dd")},
                 "shadows_ancestral": _acc([r for r in rows if r["truth"] == 0 and r["anc"] != 0], sig, key="anc"),
                 "crossfit": _crossfit(rows, sig),
                 "collider_disagreement_top_quarter": _top_quarter_disagreement(rows, sig)}
            tr = [r for r in true_rows if r["s"][sig] not in (None, 0)]
            if tr:
                mags = sorted(abs(r["s"][sig]) for r in tr)
                d["by_strength"] = {}
                for q in (0.5, 0.75, 0.9):
                    t = mags[int(q * (len(mags) - 1))]
                    kk = [r for r in tr if abs(r["s"][sig]) >= t]
                    d["by_strength"]["top_%d%%" % round(100 * (1 - q))] = round(sum((r["s"][sig] > 0) == (r["truth"] > 0) for r in kk) / len(kk), 3)
            cell["signals"][sig] = d
        out["cells"]["%s_%s" % (fam, reg)] = cell
    json.dump(out, open(RES / "dirsig_dev.json", "w"), indent=1)
    for k, c in out["cells"].items():
        print("==", k, "true found", c["true_found"], c["strata"], c["ptype"])
        for sig, d in c["signals"].items():
            cf = d["crossfit"]
            print("  %-18s full %s | top10%% %s | open-orients %s | reversed %s | cc %s cd %s dd %s | shadows %s | licence %s (acc %s yield %s) | disagree %s" % (
                sig, d["full_yield"], d.get("by_strength", {}).get("top_10%"), d["by_stratum"]["open_class_orients"]["acc"],
                d["by_stratum"]["committed_reversed"]["acc"], d["by_ptype"]["cc"]["acc"], d["by_ptype"]["cd"]["acc"], d["by_ptype"]["dd"]["acc"],
                d["shadows_ancestral"]["acc"], cf["licence"], cf["open_accuracy"], cf["open_yield"], d["collider_disagreement_top_quarter"]))


if __name__ == "__main__":
    {"collect": collect, "evaluate": evaluate}[sys.argv[1]]()
