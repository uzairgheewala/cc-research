"""AB-02 (AUD-34) reproduction gate: our runs on the released Bayesys files against the published table.

  python analysis/ab02_bayesys_repro.py --causal-learn PATH [--root external/bayesys] [--xlsx external/bayesys/results_noisyPaper.xlsx]
         [--out analysis/results/ab02]

Published: Constantinou et al. 2021, results_noisyPaper.xlsx (Experiment "N", no noise). PC-Stable, FCI and FGES were run
with rcausal 1.1.1 (Tetrad). Their precision and recall give 0.5 credit to a true adjacency with the wrong or no
orientation (so TP can be fractional; "# of edges" is the number of edges in the learned graph).

Ours: causal-learn 0.1.4.8 on the released column order, G-squared test (PC stable, FCI), BDeu score (GES, d <= 40).
Scored with the same half-credit rule. Two alphas for the constraint-based methods, both declared here before any
comparison: 0.05 (what ab02_bayesys.py ran) and 0.01 (Tetrad's usual default). The published table states neither.

Gate criteria (written 2026-10-13, after opening the workbook's sheet headers and ASIA rows, before computing any of
our numbers against them):
  a cell REPRODUCES if |F1_ours - F1_pub| <= 0.05 AND |edges_ours - edges_pub| <= max(1, 0.10 x true edges);
  the gate PASSES if at least two PC-Stable or FCI cells reproduce under one alpha (the alpha is reported, and the
  freedom of two alphas is stated next to the verdict). GES vs FGES is reported, never part of the gate.
Scope: 6 networks x {0.1k, 1k, 10k}; PATHFINDER only at 0.1k (PC at 1k takes 740-770 s per run here; FCI longer).
Resumable: one JSON line per (net, size, method, alpha) in <out>/bayesys_repro_runs.jsonl. No model calls.
"""
import argparse, json, os, signal, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ALG = {"pc": "PC-Stable", "fci": "FCI", "ges": "FGES"}
F1_TOL, EDGE_TOL_SHARE = 0.05, 0.10
SIZES = ("0.1k", "1k", "10k")


def published(xlsx):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    out = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        h = [str(x).strip() if x is not None else "" for x in rows[0]]
        ix = {k: h.index(k) for k in ("Algorithm", "Dataset", "Experiment type", "# of edges", "Precision", "Recall", "F1 Score")}
        for r in rows[1:]:
            if not r[ix["Algorithm"]] or str(r[ix["Experiment type"]]).strip() != "N":
                continue
            rec = {k: r[i] for k, i in ix.items()}
            ok = all(isinstance(rec[k], (int, float)) for k in ("# of edges", "Precision", "Recall", "F1 Score"))
            out[(str(rec["Algorithm"]).strip(), str(rec["Dataset"]).strip())] = (
                {"edges": rec["# of edges"], "precision": rec["Precision"], "recall": rec["Recall"], "f1": rec["F1 Score"]}
                if ok else {"failed": str(rec["# of edges"])})
    return out


def half_scores(D, U, T):
    tadj = {frozenset(e) for e in T}
    right = sum(1 for e in D if e in T)
    wrong = sum(1 for e in D if (e[1], e[0]) in T)
    und = sum(1 for u in U if frozenset(u) in tadj)
    tp = right + 0.5 * (wrong + und)
    n = len(D) + len(U)
    p = tp / n if n else 0.0
    r = tp / len(T) if T else 0.0
    return {"edges": n, "tp_half": tp, "precision": round(p, 4), "recall": round(r, 4),
            "f1": round(2 * p * r / (p + r), 4) if p + r else 0.0, "directed": len(D), "undirected": len(U)}


def run(method, X, alpha):
    import contextlib, io
    from ab02_bayesys import marks_to_sets
    with contextlib.redirect_stdout(io.StringIO()):
        if method == "pc":
            from causallearn.search.ConstraintBased.PC import pc
            return marks_to_sets(pc(X, alpha, "gsq", stable=True, uc_rule=0, uc_priority=2, show_progress=False).G.graph)
        if method == "fci":
            from causallearn.search.ConstraintBased.FCI import fci
            G, _ = fci(X, independence_test_method="gsq", alpha=alpha, show_progress=False, verbose=False)
            return marks_to_sets(G.graph)
        from causallearn.search.ScoreBased.GES import ges
        return marks_to_sets(ges(X, score_func="local_score_BDeu")["G"].graph)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent / "external" / "bayesys"))
    ap.add_argument("--xlsx", default=str(HERE.parent / "external" / "bayesys" / "results_noisyPaper.xlsx"))
    ap.add_argument("--causal-learn", required=True)
    ap.add_argument("--out", default=str(HERE / "results" / "ab02"))
    ap.add_argument("--run-timeout-s", type=int, default=900)
    ap.add_argument("--summarise-only", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.causal_learn).resolve()))
    from ab02_bayesys import load, NETS
    pub = published(a.xlsx)
    os.makedirs(a.out, exist_ok=True)
    runs_f = Path(a.out) / "bayesys_repro_runs.jsonl"
    done = {(r["net"], r["size"], r["method"], r["alpha"]) for r in map(json.loads, open(runs_f))} if runs_f.exists() else set()

    def _alarm(s, f):
        raise TimeoutError("run exceeded %d s" % a.run_timeout_s)
    signal.signal(signal.SIGALRM, _alarm)
    if not a.summarise_only:
        for net in NETS:
            for size in (("0.1k",) if net == "PATHFINDER" else SIZES):
                X, cols, T, src = load(a.root, net, size)
                methods = [("pc", 0.05), ("pc", 0.01), ("fci", 0.05), ("fci", 0.01)] + ([("ges", None)] if len(cols) <= 40 else [])
                for m, alpha in methods:
                    if (net, size, m, alpha) in done:
                        continue
                    rec = {"net": net, "size": size, "method": m, "alpha": alpha, "true_edges": len(T)}
                    t = time.time()
                    try:
                        signal.alarm(a.run_timeout_s)
                        D, U = run(m, X, alpha)
                        signal.alarm(0)
                        rec.update(half_scores(D, U, T))
                        rec["failed"] = None
                    except Exception as e:  # noqa: BLE001
                        signal.alarm(0)
                        rec["failed"] = "%s: %s" % (type(e).__name__, str(e)[:160])
                    rec["seconds"] = round(time.time() - t, 2)
                    with open(runs_f, "a") as fh:
                        fh.write(json.dumps(rec) + "\n")
                    print(net, size, m, alpha, rec.get("failed") or (rec["edges"], rec["f1"]), rec["seconds"], flush=True)
    rows = [json.loads(l) for l in open(runs_f)] if runs_f.exists() else []
    cells = []
    for r in rows:
        if r.get("failed"):
            continue
        p = pub.get((ALG[r["method"]], "%s_N_%s" % (r["net"], r["size"])))
        c = {k: r[k] for k in ("net", "size", "method", "alpha", "true_edges", "edges", "f1", "precision", "recall")}
        c["published"] = p
        if p and "f1" in p:
            c["d_f1"] = round(r["f1"] - p["f1"], 4)
            c["d_edges"] = r["edges"] - p["edges"]
            c["reproduces"] = abs(c["d_f1"]) <= F1_TOL and abs(c["d_edges"]) <= max(1, EDGE_TOL_SHARE * r["true_edges"])
        cells.append(c)
    gate = {}
    for alpha in (0.05, 0.01):
        rep = [c for c in cells if c["method"] in ("pc", "fci") and c["alpha"] == alpha and c.get("reproduces")]
        comp = [c for c in cells if c["method"] in ("pc", "fci") and c["alpha"] == alpha and "reproduces" in c]
        gate[str(alpha)] = {"cells_compared": len(comp), "cells_reproduced": len(rep),
                            "reproduced": ["%s %s %s" % (c["method"], c["net"], c["size"]) for c in rep],
                            "median_abs_d_f1": round(sorted(abs(c["d_f1"]) for c in comp)[len(comp) // 2], 4) if comp else None}
    passed = [k for k, v in gate.items() if v["cells_reproduced"] >= 2]
    out = {"tickets": ["AUD-34", "BEN-07"], "criteria": {"f1_tol": F1_TOL, "edge_tol": "max(1, 0.10 x true edges)",
           "gate": ">= 2 PC-Stable or FCI cells reproduce under one alpha", "alphas_tried": [0.05, 0.01]},
           "published_source": "results_noisyPaper.xlsx (Experiment N)", "gate_by_alpha": gate,
           "verdict": ("passed at alpha %s" % ", ".join(passed)) if passed else "not passed",
           "ges_vs_fges": [c for c in cells if c["method"] == "ges"], "cells": cells}
    json.dump(out, open(Path(a.out) / "bayesys_repro.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("gate_by_alpha", "verdict")}, indent=1))


if __name__ == "__main__":
    main()
