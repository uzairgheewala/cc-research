"""BEN-13 S1-S2 runner: reproduce published rows, score the controls, merge into one summary.

Tickets: BEN-13

    python -m analysis.ben13.run cells --line k562 [--part 1/4] [--draws 20] [--only md_k1000,...]
    python -m analysis.ben13.run merge
    python -m analysis.ben13.run list --line k562

Inputs: external/causalbench/dataset_<line>_filtered.npz (+ .json sidecar) from analysis/ben13/stream_preprocess.py, the
literature files fetched next to it, plans/ben13_prereg.json (published targets, tolerances, protocol, hashed before
the first run). One JSON per cell in analysis/results/ben13/<line>/; a cell already written is skipped (resume).
Split and training data are causalbench's own: DatasetSplitter(npz) (test 20 %, random_state 0, stratified), training on
get_interventional() (every knockdown), evaluation on get_test_data().
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[2]
DATA = HERE / "external" / "causalbench"
OUT = HERE / "analysis" / "results" / "ben13"
PREREG = HERE / "plans" / "ben13_prereg.json"
KS = (1000, 5000)
LIT = ("string_network", "string_physical", "corum", "chipseq")


def cell_ids(draws, ks=KS):
    ids = []
    for k in ks:
        ids += ["md_k%d" % k, "oracle_k%d" % k, "random_k%d" % k]
        ids += ["rewire_md_k%d_s%d" % (k, s) for s in range(draws)]
        ids += ["permute_md_k%d_s%d" % (k, s) for s in range(draws)]
        ids += ["random_k%d_s%d" % (k, s) for s in range(1, draws)]
    ids += ["md_k%d_for1000" % k for k in ks] + ["md_k%d_path3" % k for k in ks] + ["md_k%d_fullcb" % ks[0]]
    for lit in LIT:
        ids += ["lit_%s" % lit] + ["permute_lit_%s_s%d" % (lit, s) for s in range(draws)]
        ids += ["random_lit_%s_s%d" % (lit, s) for s in range(draws)]
    return ids


class Line:
    def __init__(self, line, data_dir=DATA):
        import causalscbench.data_access.utils.splitting as splitting
        from causalscbench.evaluation import statistical_evaluation, biological_evaluation
        from analysis.ben13 import literature
        self.line = line
        npz = Path(data_dir) / ("dataset_%s_filtered.npz" % line)
        self.npz_sha = json.loads(Path(str(npz) + ".json").read_text())["expression_sha256"]
        t0 = time.time()
        sp = splitting.DatasetSplitter(str(npz), 1.0)
        Xtr, itr, genes = sp.get_interventional()
        self.Xtr, self.itr, self.genes = np.asarray(Xtr), list(itr), [str(g) for g in genes]
        Xte, ite, _ = sp.get_test_data()
        self.Xte, self.ite = np.asarray(Xte), list(ite)
        self.ev = statistical_evaluation.Evaluator(self.Xte, self.ite, self.genes)
        sides = sorted(Path(data_dir).glob("dataset_*_filtered.npz.json"))
        self.lit, self.lit_missing = literature.load_all(data_dir, line, sides)
        self.bio = {k: biological_evaluation.Evaluator(v) for k, v in self.lit.items()}
        self.lit_nets = {k: literature.restrict(v, self.genes) for k, v in self.lit.items()}
        self.load_s = round(time.time() - t0, 1)
        self._md = {}

    def md(self, k, test=False):
        from analysis.ben13 import methods
        key = (k, test)
        if key not in self._md:
            X, iv = (self.Xte, self.ite) if test else (self.Xtr, self.itr)
            if ("scores", test) not in self._md:
                self._md[("scores", test)] = methods.mean_difference_scores(X, iv, self.genes)
            self._md[key] = methods.top_k(self._md[("scores", test)], k)
        return self._md[key]

    def network(self, cid):
        from analysis.ben13 import methods
        p = cid.split("_")
        seed = int(p[-1][1:]) if p[-1].startswith("s") and p[-1][1:].isdigit() else 0
        if cid.startswith("md_k"):
            return self.md(int(p[1][1:]))
        if cid.startswith("oracle_k"):
            return self.md(int(p[1][1:]), test=True)
        if cid.startswith("random_lit_"):
            lit = cid[len("random_lit_"):cid.rfind("_s")]
            return methods.random_network(self.genes, len(self.lit_nets[lit]), 1000 + seed)
        if cid.startswith("random_k"):
            return methods.random_network(self.genes, int(p[1][1:]), seed)
        if cid.startswith("rewire_md_k"):
            return methods.rewire_children(self.md(int(p[2][1:])), self.genes, seed)
        if cid.startswith("permute_md_k"):
            return methods.permute_labels(self.md(int(p[2][1:])), self.genes, seed)
        if cid.startswith("permute_lit_"):
            lit = cid[len("permute_lit_"):cid.rfind("_s")]
            return methods.permute_labels(self.lit_nets[lit], self.genes, seed)
        if cid.startswith("lit_"):
            return self.lit_nets[cid[4:]]
        raise KeyError(cid)

    def score(self, cid, proto):
        from analysis.ben13 import evaluate
        lit_needed = [x for x in LIT if x in cid]
        if lit_needed and lit_needed[0] not in self.lit_nets:
            return {"status": "not_run", "why": "literature source missing: %s" % self.lit_missing}
        net = self.network(cid)
        mpl, oes = proto["max_path_length"], proto["omission_estimation_size"]
        if cid.endswith("_for1000"):
            oes = proto.get("omission_sensitivity", 1000)
        if cid.endswith("_path3"):
            mpl = 3
        t0 = time.time()
        st = evaluate.statistical(self.ev, net, mpl, oes, full=cid.endswith("_fullcb"))
        rec = {"status": "ok", "statistical": st, "biological": evaluate.biological(self.bio, net),
               "protocol": {"max_path_length": mpl, "omission_estimation_size": oes},
               "network_sha256": hashlib.sha256("\n".join("%s\t%s" % e for e in sorted(set(net))).encode()).hexdigest(),
               "seconds": round(time.time() - t0, 1)}
        if cid.endswith("_fullcb"):
            fast = evaluate.statistical(self.ev, net, mpl, oes)
            rec["fast_equals_full"] = all(abs(fast[k] - st[k]) < 1e-12 for k in ("wasserstein", "for", "tp", "fp"))
        return rec


def cmd_cells(a):
    pre = json.loads(PREREG.read_text())
    proto = dict(pre["protocol"])
    ks = KS
    if a.smoke:                                   # tiny synthetic files only: small budgets, few negatives
        ks, proto["omission_estimation_size"], proto["omission_sensitivity"] = (20, 50), 20, 40
    ids = cell_ids(a.draws, ks)
    if a.only:
        ids = [c for c in ids if c in set(a.only.split(","))]
    k, n = (int(x) for x in a.part.split("/"))
    ids = [c for i, c in enumerate(ids) if i % n == k - 1]
    out = OUT / a.line
    out.mkdir(parents=True, exist_ok=True)
    todo = [c for c in ids if not (out / ("%s.json" % c)).exists()]
    marker = out / (".part%dof%d.done" % (k, n))
    print("[ben13] %s part %s: %d cells, %d to do" % (a.line, a.part, len(ids), len(todo)), flush=True)
    if not todo:
        marker.write_text("JOB-COMPLETE %d cells\n" % len(ids))
        return 0
    L = Line(a.line, a.data_dir)
    print("[ben13] loaded %s in %.0f s: train %s, test %s, %d genes; literature %s, missing %s" % (
        a.line, L.load_s, L.Xtr.shape, L.Xte.shape, len(L.genes), {k: len(v) for k, v in L.lit_nets.items()},
        sorted(L.lit_missing)), flush=True)
    t_end = time.time() + a.budget_seconds if a.budget_seconds else None
    for c in todo:
        if t_end and time.time() > t_end:
            print("[ben13] budget used; run again to resume")
            return 3
        try:
            rec = L.score(c, proto)
        except Exception as e:
            rec = {"status": "failed", "error": "%s: %s" % (type(e).__name__, str(e)[:300])}
        rec.update({"tickets": ["BEN-13"], "line": a.line, "cell": c, "npz_sha256": L.npz_sha,
                    "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest()})
        tmp = out / ("%s.json.partial" % c)
        tmp.write_text(json.dumps(rec, indent=1, default=float))
        os.replace(tmp, out / ("%s.json" % c))
        st = rec.get("statistical", {})
        print("[ben13] %-28s W %.3f FOR %s (%.1f s)" % (c, st.get("wasserstein", float("nan")),
                                                       "%.3f" % st["for"] if "for" in st else "-", rec.get("seconds", 0)), flush=True)
    marker.write_text("JOB-COMPLETE %d cells\n" % len(ids))
    return 0


def _q(v):
    v = [x for x in v if x == x]
    if not v:
        return None
    return {"mean": float(np.mean(v)), "lo": float(np.percentile(v, 2.5)), "hi": float(np.percentile(v, 97.5)), "n": len(v)}


def summarise_line(line, pre):
    d = OUT / line
    if not d.exists():
        return {"status": "not_run"}
    R = {p.stem: json.loads(p.read_text()) for p in d.glob("*.json")}

    def st(c, key):
        r = R.get(c)
        return r["statistical"].get(key) if r and r.get("status") == "ok" else None

    def draws(prefix, key):
        return [r["statistical"][key] for c, r in R.items() if c.startswith(prefix) and r.get("status") == "ok"
                and key in r["statistical"]]

    s = {"cells": len(R), "reproduction": {}, "controls": {}, "literature": {}}
    tol = pre["tolerance"]
    ks = sorted({int(c[4:].split("_")[0]) for c in R if c.startswith("md_k")})
    for k in ks:
        tgt = pre["published"].get(line, {}).get("md_k%d" % k)
        w, f = st("md_k%d" % k, "wasserstein"), st("md_k%d" % k, "for")
        ok = None if w is None or f is None or tgt is None else (abs(w - tgt["wasserstein"]) <= tol["wasserstein"] and abs(f - tgt["for"]) <= tol["for"])
        s["reproduction"]["md_k%d" % k] = {"ours": {"wasserstein": w, "for": f}, "published": tgt, "within_tolerance": ok}
        wr = _q(draws("random_k%d" % k, "wasserstein"))
        fr = _q(draws("random_k%d" % k, "for"))
        rw, rf = _q(draws("rewire_md_k%d_" % k, "wasserstein")), _q(draws("rewire_md_k%d_" % k, "for"))
        pw, pf = _q(draws("permute_md_k%d_" % k, "wasserstein")), _q(draws("permute_md_k%d_" % k, "for"))
        ow = st("oracle_k%d" % k, "wasserstein")
        c = {"random": {"wasserstein": wr, "for": fr}, "rewire_children": {"wasserstein": rw, "for": rf},
             "permute_labels": {"wasserstein": pw, "for": pf}, "test_oracle_wasserstein": ow}
        if w is not None and wr and rw and w != wr["mean"]:
            c["placement_share_wasserstein"] = (rw["mean"] - wr["mean"]) / (w - wr["mean"])
            c["placement_share_wasserstein_range"] = [(rw["lo"] - wr["mean"]) / (w - wr["mean"]), (rw["hi"] - wr["mean"]) / (w - wr["mean"])]
        if f is not None and fr and rf and f != fr["mean"]:
            c["placement_share_for"] = (rf["mean"] - fr["mean"]) / (f - fr["mean"])
        if w is not None and ow:
            c["echo_ratio"] = w / ow
        s["controls"]["k%d" % k] = c
    for lit in LIT:
        r = R.get("lit_%s" % lit)
        if not r or r.get("status") != "ok":
            s["literature"][lit] = {"status": (r or {}).get("status", "not_run"), "why": (r or {}).get("why")}
            continue
        perm_bio = [x["biological"][lit]["precision"] for c2, x in R.items() if c2.startswith("permute_lit_%s_" % lit) and x.get("status") == "ok"]
        s["literature"][lit] = {
            "edges": r["statistical"]["edges"], "wasserstein": r["statistical"]["wasserstein"], "for": r["statistical"].get("for"),
            "random_same_size": {"wasserstein": _q(draws("random_lit_%s_" % lit, "wasserstein")), "for": _q(draws("random_lit_%s_" % lit, "for"))},
            "permuted": {"wasserstein": _q(draws("permute_lit_%s_" % lit, "wasserstein")), "own_precision": _q(perm_bio)},
            "md_precision_here": (R.get("md_k%d" % ks[0]) or {}).get("biological", {}).get(lit, {}).get("precision")}
    fc = next((r for c, r in R.items() if c.endswith("_fullcb")), None)
    s["fast_equals_full"] = fc.get("fast_equals_full") if fc else None
    s["sensitivity"] = {c: {"wasserstein": st(c, "wasserstein"), "for": st(c, "for")}
                        for c in sorted(R) if c.startswith("md_k") and c.endswith(("_for1000", "_path3"))}
    return s


def cmd_merge(a):
    pre = json.loads(PREREG.read_text())
    out = {"tickets": ["BEN-13"], "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest(),
           "lines": {line: summarise_line(line, pre) for line in ("k562", "rpe1")}}
    reps = [r["within_tolerance"] for L in out["lines"].values() if L.get("reproduction") for r in L["reproduction"].values()]
    out["reproduced_rows"] = sum(1 for x in reps if x)
    out["reproduction_all"] = bool(reps) and len(reps) == 4 and all(reps)
    out["fast_equals_full_all"] = all(L.get("fast_equals_full") for L in out["lines"].values() if L.get("cells"))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps({"reproduced_rows": out["reproduced_rows"], "reproduction_all": out["reproduction_all"],
                      "fast_equals_full_all": out["fast_equals_full_all"]}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("cells", "merge", "list"))
    ap.add_argument("--line", default="k562", choices=("k562", "rpe1"))
    ap.add_argument("--part", default="1/1")
    ap.add_argument("--draws", type=int, default=20)
    ap.add_argument("--only", default="")
    ap.add_argument("--data-dir", default=str(DATA))
    ap.add_argument("--budget-seconds", type=float, default=0)
    ap.add_argument("--smoke", action="store_true", help="synthetic smoke: k in (20, 50), 20 negatives; never for real data")
    a = ap.parse_args(argv)
    if a.cmd == "list":
        print("\n".join(cell_ids(a.draws)))
        return 0
    return cmd_cells(a) if a.cmd == "cells" else cmd_merge(a)


if __name__ == "__main__":
    sys.exit(main())
