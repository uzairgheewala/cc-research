"""REP-09 (BND-07): reproduce the Causal Chambers authors' GES baseline on their 20-variable light-tunnel subgraph.

  PYTHONDONTWRITEBYTECODE=1 python analysis/rep09_ges.py

Protocol, pinned from the authors' notebook case_studies/causal_discovery_iid.ipynb (juangamella/causal-chamber-paper,
copy in external/causal_chambers_docs/paper__case_studies_causal_discovery_iid.ipynb) and the paper (arXiv 2404.11341v2,
Fig. 5 caption and Appendix I, task a1):
  data       lt_interventions_standard_v1, experiment uniform_reference (10000 rows), raw values (no standardization)
  variables  red green blue current ir_1 ir_2 ir_3 vis_1 vis_2 vis_3 pol_1 pol_2 angle_1 angle_2 l_11 l_12 l_21 l_22
             l_31 l_32 (notebook cell 14)
  truth      causalchamber.ground_truth.graph('lt','standard').loc[variables, variables] (induced subgraph, cell 15)
  method     ges.fit_bic(data, phases=['forward','backward','turning']) (ges 1.1.0, the authors' pinned version)
  metric     for every DAG in the estimated CPDAG (sempler.utils.all_dags): precision = |est & truth| / |est|,
             recall = |est & truth| / |truth| over directed edges (cell 10); the paper reports the range over the set

Without the data (download blocked) the script still runs two checks that need no data:
  (1) the true subgraph printed by the authors (TikZ, cell 15) equals the subgraph from causalchamber 0.2.8;
  (2) the authors' estimated CPDAG (TikZ, cell 25) re-scored with this script's metric reproduces their printed
      precision/recall lists (cell 27). This pins the metric and the truth, not the GES run.
Writes analysis/results/chambers/rep09_ges.json.
"""
import contextlib, io, json, re, sys, time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chambers_io as C  # noqa: E402

GT = C.ground_truth()
NB = C.DOCS / "paper__case_studies_causal_discovery_iid.ipynb"
VARS = ['red', 'green', 'blue', 'current', 'ir_1', 'ir_2', 'ir_3', 'vis_1', 'vis_2', 'vis_3', 'pol_1', 'pol_2',
        'angle_1', 'angle_2', 'l_11', 'l_12', 'l_21', 'l_22', 'l_31', 'l_32']
PAPER = {"url": "https://arxiv.org/abs/2404.11341 (v2, 2024-08-26; HTML https://arxiv.org/html/2404.11341v2)",
         "published": "Nature Machine Intelligence 2025, doi 10.1038/s42256-024-00964-x",
         "where": "Fig. 5 (panel a, task a1) and Appendix I, task a1",
         "quotes": ["GES and PCMCI+ return a set of 12 and 5 plausible graphs (Fig. 5 caption)",
                    "we take 10000 observations from a subset of the variables (App. I, a1)"],
         "numbers_source": "Fig. 5a shows the numbers as a figure; the values are read from the notebook output "
                           "(cell 27), which prints them for the figure"}
LO_P, HI_P, LO_R, HI_R = 0.55, 0.60, 0.56, 0.62   # printed range (two decimals)


def precision(est, truth):
    return np.logical_and(est, truth).sum() / est.sum()


def recall(est, truth):
    return np.logical_and(est, truth).sum() / truth.sum()


def all_dags(cpdag):
    with contextlib.redirect_stdout(io.StringIO()):
        import sempler.utils
    return sempler.utils.all_dags(cpdag)


def notebook():
    return json.load(open(NB, encoding="utf-8"))


def cell_text(nb, i):
    return "".join("".join(o.get("text", "")) for o in nb["cells"][i].get("outputs", []))


def tikz_to_adj(t, p):
    """'\\draw[->...] (i) edge (j)' -> A[i,j] = 1; '\\draw[-, thick...] (i) edge (j)' (undirected) -> A[i,j] = A[j,i] = 1."""
    A = np.zeros((p, p), dtype=int)
    for style, i, j in re.findall(r"\\draw\[([^\]]*)\] \((\d+)\) edge \((\d+)\)", t):
        i, j = int(i), int(j)
        if style.startswith("->"):
            A[i, j] = 1
        elif style.startswith("-"):
            A[i, j] = A[j, i] = 1
    return A


def printed_metrics(nb):
    t = cell_text(nb, 27)
    prec = [float(x) for x in re.search(r"precision:\s*(.*)", t).group(1).split()]
    rec = [float(x) for x in re.search(r"recall:\s*(.*)", t).group(1).split()]
    return prec, rec


def score_cpdag(cpdag, truth):
    dags = all_dags(cpdag)
    return [round(float(precision(d, truth)), 6) for d in dags], [round(float(recall(d, truth)), 6) for d in dags]


def main():
    C.OUT.mkdir(parents=True, exist_ok=True)
    nb = notebook()
    assert "".join(nb["cells"][14]["source"]).count("'") == 2 * len(VARS)
    truth = GT.graph("lt", "standard").loc[VARS, VARS].values
    truth_nb = tikz_to_adj(cell_text(nb, 15), len(VARS))
    cpdag_nb = tikz_to_adj(cell_text(nb, 25), len(VARS))
    p_print, r_print = printed_metrics(nb)
    p_re, r_re = score_cpdag(cpdag_nb, truth)
    und = int(((cpdag_nb == 1) & (cpdag_nb.T == 1)).sum() // 2)
    metric_check = {
        "truth_subgraph_edges_pkg_0_2_8": int(truth.sum()),
        "truth_subgraph_equals_authors_tikz": bool((truth == truth_nb).all()),
        "authors_cpdag": {"directed": int(((cpdag_nb == 1) & (cpdag_nb.T == 0)).sum()), "undirected": und},
        "authors_printed": {"precision": p_print, "recall": r_print, "n_dags": len(p_print)},
        "rescored_from_authors_cpdag": {"precision": [round(x, 2) for x in p_re], "recall": [round(x, 2) for x in r_re],
                                        "n_dags": len(p_re)},
    }
    metric_check["rescore_matches_printed"] = (sorted(round(x, 2) for x in p_re) == sorted(p_print)
                                               and sorted(round(x, 2) for x in r_re) == sorted(r_print))
    out = {"ticket": "REP-09", "bundle": "BND-07", "paper": PAPER,
           "notebook": {"file": "external/causal_chambers_docs/paper__case_studies_causal_discovery_iid.ipynb",
                        "url": "https://github.com/juangamella/causal-chamber-paper/blob/main/case_studies/causal_discovery_iid.ipynb",
                        "cells": {"variables": 14, "truth": 15, "data": 18, "ges_call": 23, "cpdag": 25, "metrics": 27, "metric_defs": 10}},
           "protocol": {"dataset": "lt_interventions_standard_v1", "experiment": "uniform_reference", "rows": 10000,
                        "variables": VARS, "standardized": False,
                        "method": "ges.fit_bic(X, phases=['forward','backward','turning'])", "ges_version": "1.1.0",
                        "truth": "causalchamber.ground_truth.graph('lt','standard').loc[variables, variables]",
                        "metric": "precision and recall over directed edges for each DAG in the estimated CPDAG"},
           "reported": {"precision_range": [LO_P, HI_P], "recall_range": [LO_R, HI_R], "n_dags": 12,
                        "precision_per_dag": p_print, "recall_per_dag": r_print},
           "metric_and_truth_check": metric_check}
    st = C.data_status("lt_interventions_standard_v1")
    if st in C.READABLE:
        if not hasattr(np, "Inf"):          # ges 1.1.0 uses np.Inf, removed in NumPy 2 (same shim as causalarena_methods.py)
            np.Inf = np.inf
        import ges
        X = C.load_experiment("lt_interventions_standard_v1", "uniform_reference")[VARS].values.astype(float)
        t0 = time.time()
        cpdag, score = ges.fit_bic(X, phases=["forward", "backward", "turning"], debug=0)
        secs = time.time() - t0
        p_ours, r_ours = score_cpdag(cpdag, truth)
        inside = (min(p_ours) >= LO_P - 0.005 and max(p_ours) <= HI_P + 0.005
                  and min(r_ours) >= LO_R - 0.005 and max(r_ours) <= HI_R + 0.005)
        same = bool((np.asarray(cpdag) != 0).astype(int).tolist() == cpdag_nb.tolist())
        out["ours"] = {"rows": int(len(X)), "precision_per_dag": p_ours, "recall_per_dag": r_ours, "n_dags": len(p_ours),
                       "precision_range": [min(p_ours), max(p_ours)], "recall_range": [min(r_ours), max(r_ours)],
                       "bic_score": float(score), "seconds": round(secs, 1), "cpdag_identical_to_authors": same,
                       "cpdag": np.asarray(cpdag).astype(int).tolist()}
        out["verdict"] = ("supported" if inside else "refuted (outside the reported range; explanation required)")
        out["verdict_rule"] = ("supported if every DAG's precision lies in [0.545, 0.605] and recall in [0.555, 0.625] "
                               "(the printed two-decimal range widened by rounding)")
    else:
        out["ours"] = {"status": "not run: lt_interventions_standard_v1.zip is %s in external/causal_chambers; the S3 host "
                                 "is refused by the egress proxy (analysis/results/chambers/fetch_status.json)" % st}
        out["verdict"] = "not tested (data unavailable in this workspace)"
        out["verdict_rule"] = ("supported if every DAG's precision lies in [0.545, 0.605] and recall in [0.555, 0.625] "
                               "(the printed two-decimal range widened by rounding); refuted otherwise unless explained")
    out["cdfm"] = {
        "reported_value": 0.727,
        "reported_source": "second-hand: project ledger (claude/causal-copilot-research-ledger.md) records 'CDFM paper F1 "
                           "CDFM .727, TabCausal .603, GES .426, PC .281' for Causal Chambers; CDFM arXiv 2607.11508v1 "
                           "has a 'Causal Chamber' subsection under 6.3 Real-world Benchmark (table of contents of "
                           "https://arxiv.org/html/2607.11508v1); the table itself was not readable through the fetch "
                           "tool here (HTML truncated, PDF returned no text), so metric, chamber subset and variables "
                           "are not pinned",
        "status": "not reproduced",
        "why": ["chamber data unavailable here (S3 host refused by the proxy)",
                "checkpoint: DOM-11 (analysis/literature/bnd02/dom11_pretrained_models.md) lists HF DMIRLAB/CDFM with "
                "a CPU device option, but huggingface.co is refused by this workspace's proxy (403 to CONNECT), so it "
                "cannot be loaded here",
                "CDFM's chamber protocol (which datasets, subgraph, rows, metric) is not pinned"],
        "note": "CDFM's GES row (.426, second-hand) comes from CDFM's own protocol and is not comparable with the "
                "Causal Chambers authors' precision/recall range without that protocol"}
    json.dump(out, open(C.OUT / "rep09_ges.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: out[k] for k in ("reported", "metric_and_truth_check", "verdict")}, indent=1))


if __name__ == "__main__":
    main()
