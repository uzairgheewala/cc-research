"""Zero-API experiment: what do the deterministic refinement steps do to each algorithm's output?

For every (dataset, algorithm, seed) cell it calls the repo's OWN functions, unmodified:
  wrappers.<Algo>({}).fit(data)                        -> S0  (wrapper default hyperparameters)
  postprocess.judge_functions.bootstrap(...)           -> resample frequencies (20 resamples)
  postprocess.judge_functions.bootstrap_recommend(...) -> buckets
  [lineage.step_bootstrap: the edits of judge.py:68-86, validated against live runs by gate B]
  postprocess.judge_functions.kci_pruning(...)         -> removals (the LLM review is skipped)
and scores S0, S1 (after bootstrap edits) and S3n (bootstrap + KCI, no LLM) against ground truth.

Differences from a pipeline run, stated: hyperparameters are wrapper defaults, not LLM-chosen; the
Python/numpy RNGs are seeded per cell (the pipeline does not seed); no LLM step.

  python refinement_offline.py --out DIR [--budget-s 140] [--only ALGO]     (resumable; rerun until 'ALL DONE')
"""
import argparse
import contextlib
import glob
import io
import json
import os
import random
import signal
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cc_graph as G  # noqa: E402
from lineage import step_bootstrap  # noqa: E402

ALGOS = ["PC", "FCI", "GES", "XGES", "GRaSP", "DirectLiNGAM", "ICALiNGAM", "FGES", "NOTEARSLinear", "Hybrid",
         "BAMB", "HITONMB", "IAMBnPC", "InterIAMB", "MBOR", "GOLEM", "CORL", "NOTEARSNonlinear"]
# On the simulated datasets only the core families are run (Markov-blanket and torch-based wrappers
# are run on the bundled datasets only, to keep the experiment inside the sandbox time limits).
CORE = ["PC", "FCI", "GES", "XGES", "GRaSP", "FGES", "DirectLiNGAM", "ICALiNGAM", "NOTEARSLinear"]
BUNDLED = {"Linear_Gaussian": "data/dataset/Linear_Gaussian",
           "Linear_Nongaussian": "data/dataset/Linear_Nongaussian",
           "LiNG_10nodes": "data/dataset/20241024_145159_Linear-Non-gaussian_id_0_nodes10_samples1000",
           "sachs(reference)": "data/dataset/sachs"}
SIM = [("sim_linear_gaussian_p8_s%d" % s, dict(noise_type="gaussian", function_type="linear"), s) for s in (0, 1, 2)] + \
      [("sim_linear_uniform_p8_s%d" % s, dict(noise_type="uniform", function_type="linear"), s) for s in (0, 1, 2)]


def datasets(repo):
    out = {}
    for name, rel in BUNDLED.items():
        d = os.path.join(repo, rel)
        csv = os.path.join(d, "sachs.csv") if name.startswith("sachs") else sorted(
            f for f in glob.glob(os.path.join(d, "*.csv")) if "ground_truth" not in f)[0]
        out[name] = (pd.read_csv(csv), np.load(sorted(glob.glob(os.path.join(d, "*.npy")))[0]), "bundled")
    from data.simulator.dummy import DataSimulator
    for name, kw, seed in SIM:
        random.seed(seed)
        np.random.seed(seed)
        with contextlib.redirect_stdout(io.StringIO()):
            graph, df = DataSimulator().generate_dataset(n_nodes=8, n_samples=1000, edge_probability=0.3, **kw)
        df = pd.DataFrame(df)
        if "domain_index" in df.columns:
            df = df.drop(columns=["domain_index"])
        out[name] = (df, np.asarray(graph), "repo simulator, seed %d" % seed)
    return out


def run_cell(df, truth, algo, seed):
    import causal_discovery.wrappers as W
    import postprocess.judge_functions as jf
    p = df.shape[1]
    E = G.truth_edges(truth)
    random.seed(seed)
    np.random.seed(seed)
    res = {"algo": algo, "seed": seed, "n": int(df.shape[0]), "p": int(p), "n_true_edges": len(E)}
    t = time.time()
    sink = io.StringIO()
    import logging
    logging.disable(logging.CRITICAL)
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        S0, info, raw = getattr(W, algo)({}).fit(df)
        S0 = np.asarray(S0)
        res["fit_s"] = round(time.time() - t, 2)
        t = time.time()
        _rec, boot = jf.bootstrap(data=df, full_graph=S0, algorithm=algo, hyperparameters={}, boot_num=20,
                                  ts=False, parallel=False)
        res["bootstrap_s"] = round(time.time() - t, 2)
        buckets = jf.bootstrap_recommend(S0, boot)
        S1, added, deleted = step_bootstrap(S0, buckets)
        t = time.time()
        kci = jf.kci_pruning(df, S1.copy())
        res["kci_s"] = round(time.time() - t, 2)
    S3n = S1.copy()
    for (a, b) in kci:
        S3n[a, b] = S3n[b, a] = 0
    codes = {G.CODE_NAMES[int(c)]: int((S0 == c).sum()) for c in np.unique(S0) if c != 0}
    cells = {"upper": int(np.count_nonzero(np.triu(S0, 1))), "lower": int(np.count_nonzero(np.tril(S0, -1)))}
    adj0 = [(a, b) for a, b in G.pairs(p) if G.is_adjacent(S0, a, b)]
    surv = [(a, b) for a, b in adj0 if G.is_adjacent(S1, a, b)]
    by_type = {}
    for a, b in adj0:
        t0 = G.pair_type(S0, a, b)
        key = "directed" if t0 in ("a->b", "b->a") else t0
        d = by_type.setdefault(key, {"n": 0, "survive_bootstrap_step": 0})
        d["n"] += 1
        d["survive_bootstrap_step"] += int((a, b) in surv)
    review = {tuple(sorted((int(i), int(j)))) for k in ("exist", "non-exist") for (i, j) in buckets["middle_prob_edges"][k]}
    res.update({
        "S0_codes": codes, "S0_nonzero_cells": cells, "raw_result_type": type(raw).__name__,
        "S0_adjacencies": len(adj0), "S1_adjacencies": int(sum(G.is_adjacent(S1, a, b) for a, b in G.pairs(p))),
        "S3n_adjacencies": int(sum(G.is_adjacent(S3n, a, b) for a, b in G.pairs(p))),
        "bootstrap_added": len(added), "bootstrap_deleted_pairs": len({tuple(sorted(x)) for x in deleted}),
        "S0_edges_by_type_and_survival": by_type,
        "pairs_queued_for_llm_review": len([r for r in review if r[0] != r[1]]), "pairs_total": len(G.pairs(p)),
        "self_pairs_queued": len([r for r in review if r[0] == r[1]]),
        "kci_removed": len(kci),
        "score_S0": G.score(S0, E, p), "score_S1": G.score(S1, E, p), "score_S3n": G.score(S3n, E, p),
        "S0": S0.astype(int).tolist(), "S1": S1.astype(int).tolist(),
    })
    return res


class CellTimeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise CellTimeout("cell exceeded the per-cell time limit of this sandbox")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.environ.get("CC_REPO", os.path.expanduser("~/cc")))
    ap.add_argument("--cell-timeout-s", type=float, default=95)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shard", default="0/1", help="k/n: process only every n-th cell starting at k")
    ap.add_argument("--budget-s", type=float, default=140)
    ap.add_argument("--only", default=None)
    ap.add_argument("--seeds", default="0")
    a = ap.parse_args()
    os.chdir(a.repo)
    sys.path[:0] = [a.repo, os.path.join(a.repo, "externals", "causal-learn")]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        data = datasets(a.repo)
    seeds = [int(s) for s in a.seeds.split(",")]
    only = set(a.only.split(",")) if a.only else None
    todo = [(d, al, s) for d in data for al in ALGOS for s in seeds if (not only or al in only)
            and (not d.startswith("sim_") or al in CORE)]
    k, n = [int(x) for x in a.shard.split("/")]
    todo = [c for i, c in enumerate(todo) if i % n == k]
    pending = [c for c in todo if not (out / ("%s__%s__s%d.json" % c)).exists()]
    print("cells: %d total, %d pending" % (len(todo), len(pending)))
    for d, al, s in pending:
        if time.time() - t0 > a.budget_s:
            print("budget reached; rerun to continue")
            return
        df, truth, src = data[d]
        t = time.time()
        try:
            signal.signal(signal.SIGALRM, _on_alarm)
            signal.alarm(int(a.cell_timeout_s))
            try:
                res = run_cell(df, truth, al, s)
            finally:
                signal.alarm(0)
            res["status"] = "ok"
        except BaseException as e:     # noqa: BLE001
            tb = traceback.extract_tb(e.__traceback__)
            res = {"algo": al, "seed": s, "status": "error", "error": "%s: %s" % (type(e).__name__, str(e)[:300]),
                   "where": "%s:%d" % (tb[-1].filename.split("/cc/")[-1], tb[-1].lineno) if tb else None}
        res.update({"dataset": d, "dataset_source": src, "cell_s": round(time.time() - t, 1)})
        (out / ("%s__%s__s%d.json" % (d, al, s))).write_text(json.dumps(res, default=float), encoding="utf-8")
        print("%-28s %-16s s%d  %-5s %5.1fs  %s" % (d, al, s, res["status"], res["cell_s"],
              res.get("error") or "S0 %s -> S1 %s -> S3n %s adj" % (res["S0_adjacencies"], res["S1_adjacencies"], res["S3n_adjacencies"])))
    print("ALL DONE")


if __name__ == "__main__":
    main()
