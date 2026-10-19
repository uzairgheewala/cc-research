"""Direction signals round 2 (plans/dirsig2_prereg.json), dev, regime D, both families.

  python analysis/q2_dirsig2.py collect   -> analysis/results/q2_v3/dirsig2_links_dev.jsonl.gz
  python analysis/q2_dirsig2.py evaluate  -> analysis/results/q2_v3/dirsig2_dev.json

Round 1's per-link scores are joined from dirsig_links_dev.jsonl.gz (not recomputed).
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
sys.path.insert(0, str(ROOT / "analysis"))
RES = ROOT / "analysis" / "results" / "q2_v3"
ROWS = RES / "dirsig2_links_dev.jsonl.gz"
R1 = RES / "dirsig_links_dev.jsonl.gz"
OPEN = ("meek_r1", "meek_r3")


def _one(args):
    path, family = args
    import numpy as np
    from score import bench
    from kernel import asym_cond as C, build as B, cache, experiment
    name = Path(path).name
    s = bench.load(path)
    X, names = np.asarray(s["values"], dtype=float), list(s["node_ids"])
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    if led is None:
        return []
    D, U = experiment.configure(led, OPEN)
    I = bench.truth_info(family, name)
    T = set(I["T"])
    nb = defaultdict(set)
    for a, b in D:
        nb[a].add(b)
        nb[b].add(a)
    for a, b in U:
        nb[a].add(b)
        nb[b].add(a)
    children = defaultdict(set)
    for a, b in D:
        children[a].add(b)
    corr = np.corrcoef(X, rowvar=False)
    indeg = defaultdict(int)
    for a, b in T:
        indeg[b] += 1

    def zset(v, other):
        z = [k for k in nb[v] if k != other and k not in children[v]]
        z.sort(key=lambda k: -abs(corr[v, k]) if np.isfinite(corr[v, k]) else 0.0)
        return z[:C.MAX_COND]
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    out = []
    for e in sorted(tuple(sorted(p)) for p in adj):
        a, b = e
        truth = 1 if (a, b) in T else (-1 if (b, a) in T else 0)
        seed = zlib.crc32(("%s:%d:%d" % (name, a, b)).encode())
        Za, Zb = zset(a, b), zset(b, a)
        child = b if truth > 0 else (a if truth < 0 else None)
        out.append({"file": name, "a": a, "b": b, "ma": C.masspoint(X[:, a]), "mb": C.masspoint(X[:, b]),
                    "gated": C.gated(X[:, a], X[:, b]), "nza": len(Za), "nzb": len(Zb),
                    "child_indeg": indeg[child] if child is not None else None,
                    "c": C.all_cond(X, a, b, Za, Zb, seed=seed), "d14": C.mass_side(X[:, a], X[:, b])})
    return out


def collect(workers=4):
    from score import bench
    with gzip.open(ROWS, "wt") as fh:
        for fam in ("semantic", "formula"):
            fs = [str(p) for p in bench.files(fam, split="dev")]
            t0 = time.time()
            k = 0
            with mp.get_context("fork").Pool(workers) as pool:
                for rows in pool.imap(_one, [(f, fam) for f in fs]):
                    for r in rows:
                        r["family"] = fam
                        fh.write(json.dumps(r) + "\n")
                        k += 1
            print(fam, "links", k, "%.0fs" % (time.time() - t0), flush=True)


def evaluate():
    import q2_dirsig as R
    r1 = {}
    with gzip.open(R1, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            if r["regime"] == "D":
                r1[(r["family"], r["file"], r["a"], r["b"])] = r
    rows = defaultdict(list)
    with gzip.open(ROWS, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            base = r1[(r["family"], r["file"], r["a"], r["b"])]
            m = dict(base)
            m.update({k: r[k] for k in ("ma", "mb", "gated", "nza", "nzb", "child_indeg")})
            m["s"] = dict(base["s"], **r["c"], D14_mass_side=r["d14"])
            rows[r["family"]].append(m)
    sigs = list(next(iter(rows.values()))[0]["s"])
    out = {"prereg": "plans/dirsig2_prereg.json", "cells": {}}
    for fam, R_ in rows.items():
        true_rows = [r for r in R_ if r["truth"] != 0]
        gated_true = [r for r in true_rows if r["gated"]]
        open_all = sum(1 for r in true_rows if r["led"] == 0)
        cell = {"true_found": len(true_rows), "gated_true": len(gated_true), "gate_keep_share": round(len(gated_true) / len(true_rows), 3),
                "left_open_true_all": open_all, "left_open_true_gated": sum(1 for r in gated_true if r["led"] == 0), "signals": {}}
        for sig in sigs:
            ung, gat = R._acc(true_rows, sig), R._acc(gated_true, sig)
            cf = R._crossfit([r for r in R_ if r["gated"]], sig)
            # yield over ALL left-open true links (pre-registered denominator)
            cf["open_yield_all"] = round(cf["open_acted"] / open_all, 3) if open_all else 0.0
            cf["licence"] = bool(cf["open_accuracy"] is not None and cf["open_accuracy"] >= R.BAR and cf["open_yield_all"] >= R.MIN_YIELD)
            multi = [r for r in gated_true if (r["child_indeg"] or 0) >= 2]
            single = [r for r in gated_true if r["child_indeg"] == 1]
            cell["signals"][sig] = {"ungated": ung, "gated": gat, "gated_child_multi_parent": R._acc(multi, sig),
                                    "gated_child_single_parent": R._acc(single, sig),
                                    "gated_by_stratum": {s: R._acc([r for r in gated_true if R._stratum(r) == s], sig) for s in
                                                         ("committed_right", "committed_reversed", "open_class_orients", "open_class_open")},
                                    "crossfit_gated": cf}
        d14 = [r for r in true_rows if r["s"]["D14_mass_side"] is not None]
        cell["D14_mass_side"] = R._acc(d14, "D14_mass_side")
        out["cells"][fam] = cell
        print("==", fam, "true found", len(true_rows), "gated", len(gated_true), "(%.0f%%)" % (100 * cell["gate_keep_share"]),
              "left-open true: all", open_all, "gated", cell["left_open_true_gated"], "| D14", cell["D14_mass_side"])
        for sig, d in cell["signals"].items():
            if sig == "D14_mass_side":
                continue
            cf = d["crossfit_gated"]
            print("  %-18s ungated %-5s gated %-5s | 1 parent %-5s 2+ parents %-5s | open-orients %-5s reversed %-5s | licence %s (acc %s, yield of all open %s)" % (
                sig, d["ungated"]["acc"], d["gated"]["acc"], d["gated_child_single_parent"]["acc"], d["gated_child_multi_parent"]["acc"],
                d["gated_by_stratum"]["open_class_orients"]["acc"], d["gated_by_stratum"]["committed_reversed"]["acc"],
                cf["licence"], cf["open_accuracy"], cf["open_yield_all"]))
    json.dump(out, open(RES / "dirsig2_dev.json", "w"), indent=1)


if __name__ == "__main__":
    {"collect": collect, "evaluate": evaluate}[sys.argv[1]]()
