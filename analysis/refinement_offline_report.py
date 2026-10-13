"""Aggregate refinement_offline.py cells into tables (markdown + json).   python refinement_offline_report.py CELLS_DIR OUT_DIR"""
import glob
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

cells_dir, out_dir = sys.argv[1], Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
cells = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(cells_dir, "*.json")))]
ok = [c for c in cells if c["status"] == "ok"]
bad = [c for c in cells if c["status"] != "ok"]


def f(v):
    return "n/a" if v is None else "%.2f" % v


L = ["# Offline refinement experiment (no LLM, no API cost)", "",
     "%d cells run, %d completed, %d failed. Each cell: one dataset, one algorithm with wrapper-default hyperparameters, seed 0, 20 bootstrap resamples, using the repo's own `fit`, `bootstrap`, `bootstrap_recommend` and `kci_pruning`." % (len(cells), len(ok), len(bad)), "",
     "S0 = algorithm output. S1 = after the bootstrap edits of `judge.py:68-86`. S3n = S1 after KCI pruning, with the LLM review skipped.", ""]

# 1. survival by S0 edge type, pooled
pool = defaultdict(lambda: [0, 0])
per_algo = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for c in ok:
    for t, d in c["S0_edges_by_type_and_survival"].items():
        pool[t][0] += d["n"]
        pool[t][1] += d["survive_bootstrap_step"]
        per_algo[c["algo"]][t][0] += d["n"]
        per_algo[c["algo"]][t][1] += d["survive_bootstrap_step"]
L += ["## 1. Does an edge survive the bootstrap step? By the edge's type in the algorithm output", "",
      "| Edge type in S0 | Edges (all cells) | Still adjacent in S1 | Survival |", "|---|---|---|---|"]
for t, (n, s) in sorted(pool.items(), key=lambda kv: -kv[1][0]):
    L.append("| %s | %d | %d | %.0f%% |" % (t, n, s, 100.0 * s / n))
L += ["", "## 2. Same, per algorithm", "", "| Algorithm | Output types seen | Edges | Survive | Survival |", "|---|---|---|---|---|"]
for al in sorted(per_algo):
    n = sum(v[0] for v in per_algo[al].values())
    s = sum(v[1] for v in per_algo[al].values())
    types = ", ".join("%s %d" % (t, v[0]) for t, v in sorted(per_algo[al].items(), key=lambda kv: -kv[1][0]))
    L.append("| %s | %s | %d | %d | %s |" % (al, types, n, s, ("%.0f%%" % (100.0 * s / n)) if n else "n/a"))

# 3. accuracy by stage, mean over datasets, per algorithm
L += ["", "## 3. Accuracy against ground truth by stage (mean over datasets; adjacency F1 ignores orientation)", "",
      "| Algorithm | Datasets | adj F1 S0 | adj F1 S1 | adj F1 S3n | adj recall S0 | adj recall S1 | SHD vs CPDAG S0 | S1 | S3n | Datasets where S1 has lower adj F1 than S0 | higher |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|"]
agg = {}
for al in sorted({c["algo"] for c in ok}):
    cs = [c for c in ok if c["algo"] == al]
    m = lambda key, st: sum((c["score_" + st][key] or 0.0) for c in cs) / len(cs)
    worse = sum(1 for c in cs if (c["score_S1"]["adj_f1"] or 0) < (c["score_S0"]["adj_f1"] or 0) - 1e-9)
    better = sum(1 for c in cs if (c["score_S1"]["adj_f1"] or 0) > (c["score_S0"]["adj_f1"] or 0) + 1e-9)
    agg[al] = {"n": len(cs), "adj_f1": [m("adj_f1", s) for s in ("S0", "S1", "S3n")],
               "adj_recall": [m("adj_recall", s) for s in ("S0", "S1")],
               "shd_cpdag": [m("shd_vs_true_cpdag", s) for s in ("S0", "S1", "S3n")], "worse": worse, "better": better}
    a = agg[al]
    L.append("| %s | %d | %s | %s | %s | %s | %s | %.1f | %.1f | %.1f | %d | %d |" % (
        al, a["n"], f(a["adj_f1"][0]), f(a["adj_f1"][1]), f(a["adj_f1"][2]), f(a["adj_recall"][0]), f(a["adj_recall"][1]),
        a["shd_cpdag"][0], a["shd_cpdag"][1], a["shd_cpdag"][2], a["worse"], a["better"]))

# 4. LLM review queue size
L += ["", "## 4. How many pairs the bootstrap step queues for LLM review", "",
      "In every completed cell the queue contained every unordered pair and every self-pair: %s." % (
          "TRUE" if all(c["pairs_queued_for_llm_review"] == c["pairs_total"] and c["self_pairs_queued"] == c["p"] for c in ok) else "FALSE (see cells)"), ""]

# 5. where symmetric marks are stored + KCI coverage
L += ["## 5. Where each wrapper stores its marks (upper vs lower triangle), which decides what the KCI step can see", "",
      "`kci_pruning` only examines cells `[i, j]` with `i < j` (upper triangle).", "",
      "| Algorithm | Nonzero cells in upper triangle | in lower triangle | KCI removals (all cells) |", "|---|---|---|---|"]
for al in sorted({c["algo"] for c in ok}):
    cs = [c for c in ok if c["algo"] == al]
    L.append("| %s | %d | %d | %d |" % (al, sum(c["S0_nonzero_cells"]["upper"] for c in cs),
                                         sum(c["S0_nonzero_cells"]["lower"] for c in cs), sum(c["kci_removed"] for c in cs)))

L += ["", "## 6. Every cell", "", "| Dataset | Algorithm | True edges | S0 adj | S1 adj | S3n adj | adj F1 S0 | S1 | S3n | SHD-CPDAG S0 | S1 | S3n |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for c in sorted(ok, key=lambda c: (c["dataset"], c["algo"])):
    L.append("| %s | %s | %d | %d | %d | %d | %s | %s | %s | %d | %d | %d |" % (
        c["dataset"], c["algo"], c["n_true_edges"], c["S0_adjacencies"], c["S1_adjacencies"], c["S3n_adjacencies"],
        f(c["score_S0"]["adj_f1"]), f(c["score_S1"]["adj_f1"]), f(c["score_S3n"]["adj_f1"]),
        c["score_S0"]["shd_vs_true_cpdag"], c["score_S1"]["shd_vs_true_cpdag"], c["score_S3n"]["shd_vs_true_cpdag"]))
L += ["", "## 7. Cells that did not complete", "", "| Dataset | Algorithm | Error | Where |", "|---|---|---|---|"]
for c in sorted(bad, key=lambda c: (c["algo"], c["dataset"])):
    L.append("| %s | %s | %s | %s |" % (c["dataset"], c["algo"], c["error"].replace("|", "/")[:140], c.get("where")))
L += ["", "Errors mentioning `_Mock` or `DataLoader` come from this sandbox's stand-in for PyTorch, not from the repo.", ""]
(out_dir / "refinement_offline.md").write_text("\n".join(L), encoding="utf-8")
json.dump({"pooled_survival_by_type": {k: {"n": v[0], "survive": v[1]} for k, v in pool.items()}, "per_algorithm": agg,
           "n_cells": len(cells), "n_ok": len(ok), "failed": [(c["dataset"], c["algo"], c["error"]) for c in bad]},
          open(out_dir / "refinement_offline_summary.json", "w"), indent=1)
print("\n".join(L[:75]))
