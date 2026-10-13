#!/usr/bin/env python
"""AB-12 vertical probe: root-cause analysis on the AWS PetShop dataset (tickets AUD-43, STR-06).

One command reproduces every number in analysis/results/rca/rca_probe.json:

    nice -n 10 /home/claude/work/engines/venv/bin/python -W ignore analysis/ab12_rca_probe.py

No LLM calls. Protocol frozen in analysis/results/rca/ab12_prereg.json before any test result was computed.

Methods (all reimplemented from Hardt et al.'s Apache-2.0 code in petshop/code; deviations listed in the report):
  a   ranked_correlation   graph-free; authors' ranked_correlation.py defaults (Pearson, abnormal pool, rank by p-value,
                           MAD>5 anomaly filter, top-3 output)                                         regime D
  a2  mad_rank             graph-free; MAD-score anomaly ranking at the analysed row (robust z, BARO-like, not BARO) D
  b   learned_traversal    authors' traversal (anomalous nodes without anomalous parents, anomalous path to target,
                           path-sum score) on a PC graph learned from the normal period                    D
  b_rand                   same, undirected PC edges oriented at random (seeded) - sensitivity             D
  b_lat                    POST HOC: latency-learned PC graph also used for availability issues            D
  c   declared_traversal   authors' baseline_anomaly_traversal on the released call graph (reversed)      D+K
  d   declared_traversal + abstention (rule frozen in prereg, tau tuned on train only)                    D+K
  e   ranked_correlation + abstention (same rule shape)                                                    D
  b+abstain                learned_traversal + abstention (extra row)                                      D
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import warnings
import zlib
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

warnings.filterwarnings("ignore")

KIT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = Path("/home/claude/work/ext2/petshop/dataset")
DEFAULT_CL = Path("/home/claude/work/engines/cl_0.1.4.8")
OUT_DIR = KIT / "analysis" / "results" / "rca"
PREREG = OUT_DIR / "ab12_prereg.json"

SCENARIOS = ["low_traffic", "high_traffic", "temporal_traffic1", "temporal_traffic2"]
GROUP = {"low_traffic": "low", "high_traffic": "high", "temporal_traffic1": "temporal", "temporal_traffic2": "temporal"}
MAD_C = 0.6744897501960817  # statsmodels.robust.mad default c = Gaussian.ppf(3/4)
THRESH = 5.0  # authors' DEFAULT_ANOMALY_DETECTION threshold
SEED = 20261012
TAU_GRID = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
KS = [1, 2, 3, 4, 5]
PATH_CAP = 200000  # guard on simple-path enumeration (recorded if hit)

# Published numbers (Hardt et al. 2024, Table 3, top-3 recall; arXiv 2311.04806v2) and the authors' notebook
# RCA-Dataset-Eval.ipynb outputs for traversal (train+test pooled, MAD threshold 5).
PUBLISHED_TOP3 = {
    "traversal": {("low", "latency"): 0.57, ("low", "availability"): 1.00, ("high", "latency"): 0.79,
                  ("high", "availability"): 1.00, ("temporal", "latency"): 1.00, ("temporal", "availability"): 1.00},
    "ranked_correlation": {("low", "latency"): 0.57, ("low", "availability"): 0.92, ("high", "latency"): 0.79,
                           ("high", "availability"): 0.92, ("temporal", "latency"): 0.75,
                           ("temporal", "availability"): 0.75},
    "epsilon_diagnosis": {("low", "latency"): 0.00, ("low", "availability"): 0.00, ("high", "latency"): 0.00,
                          ("high", "availability"): 0.33, ("temporal", "latency"): 0.12,
                          ("temporal", "availability"): 0.12},
}
NOTEBOOK_TRAVERSAL = {  # (n, empty fraction, top1, top3)
    ("low", "latency"): (14, 0.21, 0.571, 0.571), ("low", "availability"): (12, 0.00, 0.833, 1.000),
    ("high", "latency"): (14, 0.14, 0.571, 0.786), ("high", "availability"): (12, 0.00, 0.667, 1.000),
    ("temporal", "latency"): (8, 0.00, 1.000, 1.000), ("temporal", "availability"): (8, 0.00, 0.750, 1.000),
}
NOTEBOOK_SPECIFICITY = {("low", "latency"): 0.167, ("low", "availability"): 1.000, ("high", "latency"): 0.333,
                        ("high", "availability"): 1.000, ("temporal", "latency"): 0.600,
                        ("temporal", "availability"): 1.000}


# ----------------------------------------------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------------------------------------------

def _read_metrics(p: Path) -> pd.DataFrame:
    return pd.read_csv(p, header=[0, 1, 2], index_col=0)


def _permute(df: pd.DataFrame, rank: dict) -> pd.DataFrame:
    order = sorted(range(df.shape[1]), key=lambda i: (rank[df.columns[i][0]], i))
    return df.iloc[:, order]


def load_scenario(data: Path, sc: str, shuffle: bool):
    d = data / sc
    call_graph = nx.from_pandas_adjacency(pd.read_csv(d / "graph.csv", index_col=0), create_using=nx.DiGraph)
    normal = _read_metrics(d / "noissue" / "metrics.csv")
    issues = []
    for split in ["train", "test"]:
        names = sorted([x for x in os.listdir(d / split) if not x.startswith(".")], key=lambda s: int(s.split("_")[-1]))
        for name in names:
            m = _read_metrics(d / split / name / "metrics.csv")
            with open(d / split / name / "target.json") as f:
                t = json.load(f)
            issues.append({"scenario": sc, "split": split, "issue": name, "metrics": m, "target": t})
    perm = None
    if shuffle:
        nodes = sorted(set(c[0] for c in normal.columns) | set(c[0] for it in issues for c in it["metrics"].columns))
        rng = np.random.default_rng([SEED, SCENARIOS.index(sc)])
        perm = list(rng.permutation(nodes))
        rank = {n: i for i, n in enumerate(perm)}
        normal = _permute(normal, rank)
        for it in issues:
            it["metrics"] = _permute(it["metrics"], rank)
    return call_graph, normal, issues, perm


def reduce_df(df: pd.DataFrame, metric: str, stat: str) -> pd.DataFrame:
    dm = df.loc[:, (slice(None), [metric], [stat])].copy()
    dm.columns = [c[0] for c in dm.columns]
    return dm


# ----------------------------------------------------------------------------------------------------------------
# Anomaly detection (authors' data_preprocessing.py with dowhy 0.9.1 MedianDeviationScorer)
# ----------------------------------------------------------------------------------------------------------------

def train_detectors(normal_red: pd.DataFrame) -> dict:
    det = {}
    for c in normal_red.columns:
        x = normal_red[c].to_numpy(dtype=float)
        x = x[~np.isnan(x)]
        if x.shape[0] < 10:
            continue
        if np.std(x) == 0:
            det[c] = ("mean", float(np.mean(x)), None, 0.0)
        else:
            med = float(np.median(x))
            mad = float(np.median(np.abs(x - med)) / MAD_C)
            det[c] = ("mad", med, mad, THRESH)
    return det


def score_column(d, vals: np.ndarray):
    scores = np.zeros(vals.shape[0])
    ok = ~np.isnan(vals)
    if ok.sum() == 0:
        return np.zeros(vals.shape[0], dtype=bool), scores
    kind, center, mad, thr = d
    with np.errstate(divide="ignore", invalid="ignore"):
        s = np.abs(vals[ok] - center) if kind == "mean" else np.abs(vals[ok] - center) / mad
    scores[ok] = s
    scores[np.isnan(scores)] = 0
    return scores > thr, scores


def detect(normal: pd.DataFrame, abnormal: pd.DataFrame, target: str, metric: str, stat: str, detectors=None):
    """Returns (anomalous {node: score} at the analysed row, row index) or (None, row) when the target is not
    anomalous (the authors' empty result)."""
    if detectors is None:
        detectors = train_detectors(reduce_df(normal, metric, stat))
    A = reduce_df(abnormal, metric, stat)
    ind, sc = {}, {}
    for c in A.columns:
        if c in detectors:
            ind[c], sc[c] = score_column(detectors[c], A[c].to_numpy(dtype=float))
        else:
            ind[c], sc[c] = np.zeros(A.shape[0], dtype=bool), np.zeros(A.shape[0])
    row = 2
    for i in range(2, A.shape[0]):
        if ind[target][i]:
            row = i
            break
    if row >= A.shape[0] or not ind[target][row]:
        return None, row
    return {c: float(sc[c][row]) for c in A.columns if ind[c][row]}, row


# ----------------------------------------------------------------------------------------------------------------
# Traversal (authors' baseline_anomaly_traversal.py), on any DiGraph (declared reversed, or learned)
# ----------------------------------------------------------------------------------------------------------------

def traversal(cgraph: nx.DiGraph, anomalous: dict, target: str, check_acyclic: bool):
    info = {"cyclic_anomalous_subgraph": False, "path_cap_hit": False, "not_in_graph": []}
    anom = set(anomalous)
    H = cgraph.subgraph([v for v in anom if v in cgraph]).copy()
    if not nx.is_directed_acyclic_graph(H):
        info["cyclic_anomalous_subgraph"] = True
        if check_acyclic:
            raise ValueError("cyclic anomalous subgraph")
    roots = []
    for v in sorted(anom):
        if v not in cgraph:
            info["not_in_graph"].append(v)
            roots.append(v)
            continue
        if not (set(cgraph.predecessors(v)) & anom):
            roots.append(v)
    out = []
    info["_roots"] = list(roots)
    if target not in H:
        return out, roots, info
    for r in roots:
        if r == target or r not in H:
            continue
        best, n = -np.inf, 0
        for path in nx.all_simple_paths(H, r, target):
            n += 1
            best = max(best, float(np.sum([anomalous[x] for x in set(path)])))
            if n >= PATH_CAP:
                info["path_cap_hit"] = True
                break
        if n > 0:
            out.append((r, best))
    return out, roots, info


def declared_causal_graph(call_graph: nx.DiGraph) -> nx.DiGraph:
    return call_graph.reverse()


# ----------------------------------------------------------------------------------------------------------------
# PC on the normal period
# ----------------------------------------------------------------------------------------------------------------

def learn_pc(normal: pd.DataFrame, metric: str, stat: str, orient_seed: int):
    from causallearn.search.ConstraintBased.PC import pc

    R = reduce_df(normal, metric, stat)
    all_nodes = list(R.columns)
    keep = []
    for c in all_nodes:
        x = R[c].to_numpy(dtype=float)
        x = x[~np.isnan(x)]
        if x.shape[0] >= 10 and np.std(x) > 0:
            keep.append(c)
    X = R[keep].copy()
    X = X.fillna(X.mean())
    dropped_collinear = []
    t0 = time.time()
    while True:
        try:
            cg = pc(X.to_numpy(), 0.05, "fisherz", True, 0, 2, show_progress=False)
            break
        except ValueError as e:
            if "singular" not in str(e):
                raise
            C = np.abs(np.corrcoef(X.to_numpy(), rowvar=False))
            np.fill_diagonal(C, 0)
            i, j = np.unravel_index(np.nanargmax(C), C.shape)
            drop = X.columns[max(i, j)]
            dropped_collinear.append(drop)
            X = X.drop(columns=[drop])
    secs = time.time() - t0
    cols = list(X.columns)
    G = cg.G.graph
    directed, undirected, bidirected = [], [], []
    for i in range(len(cols)):
        for j in range(len(cols)):
            if G[i, j] == -1 and G[j, i] == 1:
                directed.append((cols[i], cols[j]))
            elif i < j and G[i, j] == -1 and G[j, i] == -1:
                undirected.append((cols[i], cols[j]))
            elif i < j and G[i, j] == 1 and G[j, i] == 1:
                bidirected.append((cols[i], cols[j]))
    two_way = nx.DiGraph()
    two_way.add_nodes_from(all_nodes)
    two_way.add_edges_from(directed)
    for a, b in undirected + bidirected:
        two_way.add_edge(a, b)
        two_way.add_edge(b, a)
    rng = np.random.default_rng(orient_seed)
    rand = nx.DiGraph()
    rand.add_nodes_from(all_nodes)
    rand.add_edges_from(directed)
    for a, b in undirected + bidirected:
        if rng.random() < 0.5:
            rand.add_edge(a, b)
        else:
            rand.add_edge(b, a)
    summary = {"n_vars_in_pc": len(cols), "n_nodes": len(all_nodes),
               "excluded_constant_or_sparse": sorted(set(all_nodes) - set(keep)),
               "dropped_collinear": dropped_collinear, "n_directed": len(directed),
               "n_undirected": len(undirected), "n_bidirected": len(bidirected), "seconds": round(secs, 2),
               "column_order": cols,
               "edges": {"directed": sorted(directed), "undirected": sorted(undirected),
                         "bidirected": sorted(bidirected)}}
    return two_way, rand, summary


# ----------------------------------------------------------------------------------------------------------------
# Graph-free methods
# ----------------------------------------------------------------------------------------------------------------

def ranked_correlation_full(abnormal: pd.DataFrame, anomalous: dict, target: str, metric: str, stat: str):
    """Authors' make_ranked_correlation defaults: pearsonr, data_pool='abnormal', rank_by='pvalue',
    filter_for_anomalous_metrics=True, imputation 'drop'. Returns the untruncated ranked list (score = -p)."""
    A = reduce_df(abnormal, metric, stat)
    x = A[target].to_numpy(dtype=float)
    out = []
    for c in A.columns:
        if c == target or c not in anomalous:
            continue
        y = A[c].to_numpy(dtype=float)
        ok = ~(np.isnan(x) | np.isnan(y))
        if ok.sum() < 2:
            continue
        p = pearsonr(x[ok], y[ok])[1]
        if p is None or np.isnan(p):
            continue
        out.append((c, -float(p)))
    return out


def mad_rank(anomalous: dict, target: str):
    return [(c, s) for c, s in anomalous.items() if c != target]


# ----------------------------------------------------------------------------------------------------------------
# Scoring
# ----------------------------------------------------------------------------------------------------------------

def sort_list(cands):
    return sorted(cands, key=lambda t: (-t[1] if np.isfinite(t[1]) else (-np.inf if t[1] > 0 else np.inf), t[0]))


def tie_hits(cands, truth, ks=KS, truncate=None):
    """Tie-aware expected hit@k. truncate=3 mimics a method that outputs only its top 3 (hit@k for k>3 = hit@3)."""
    srt = sort_list(cands)
    res = {}
    s_true = None
    for n, s in srt:
        if n == truth:
            s_true = s
    if s_true is None:
        return {k: 0.0 for k in ks}, None, None, None
    a = sum(1 for _, s in srt if s > s_true)
    g = sum(1 for _, s in srt if s == s_true)
    for k in ks:
        kk = min(k, truncate) if truncate else k
        res[k] = float(min(1.0, max(0.0, (kk - a) / g)))
    det_rank = [n for n, _ in srt].index(truth) + 1
    return res, det_rank, a + 1, a + g


def margin34(cands):
    srt = sort_list(cands)
    if len(srt) < 4:
        return None
    s3, s4 = srt[2][1], srt[3][1]
    if s3 == s4:
        return 0.0
    if np.isinf(s3) and s3 > 0:
        return float("inf")
    return float((s3 - s4) / max(abs(s3), 1e-12))


def abstains(cands, tau):
    if not cands:
        return True
    m = margin34(cands)
    return m is not None and m <= tau


# ----------------------------------------------------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------------------------------------------------

BASE_METHODS = ["ranked_correlation", "mad_rank", "learned_traversal", "learned_traversal_randorient",
                "learned_traversal_latgraph", "declared_traversal"]
TRUNCATE = {"ranked_correlation": 3}


def run_all(data: Path, shuffle: bool):
    rows = []
    pcs = {}
    for si, sc in enumerate(SCENARIOS):
        call_graph, normal, issues, perm = load_scenario(data, sc, shuffle)
        dgraph = declared_causal_graph(call_graph)
        learned = {}
        for metric in ["latency", "availability"]:
            seed = zlib.crc32(f"{sc}|{metric}".encode()) ^ SEED
            tw, rd, summ = learn_pc(normal, metric, "Average", seed)
            learned[metric] = (tw, rd)
            pcs[f"{sc}|{metric}"] = summ
        for it in issues:
            t = it["target"]
            tn, tm, ta = t["target"]["node"], t["target"]["metric"], t["target"]["agg"]
            truth = t["root_cause"]["node"]
            anomalous, row = detect(normal, it["metrics"], tn, tm, ta)
            base = {"scenario": sc, "group": GROUP[sc], "split": it["split"], "issue": it["issue"], "metric": tm,
                    "truth": truth, "analysed_row": row, "target_anomalous": anomalous is not None,
                    "n_anomalous": 0 if anomalous is None else len(anomalous),
                    "truth_anomalous": bool(anomalous is not None and truth in anomalous)}
            out = {}
            if anomalous is None:
                for m in BASE_METHODS:
                    out[m] = ([], {})
            else:
                out["ranked_correlation"] = (ranked_correlation_full(it["metrics"], anomalous, tn, tm, ta), {})
                out["mad_rank"] = (mad_rank(anomalous, tn), {})
                tw, rd = learned[tm]
                c, roots, info = traversal(tw, anomalous, tn, check_acyclic=False)
                out["learned_traversal"] = (c, info)
                c, roots, info = traversal(rd, anomalous, tn, check_acyclic=False)
                out["learned_traversal_randorient"] = (c, info)
                # post hoc sensitivity (not pre-registered): the PC graph learned on normal-period latency is used
                # for availability issues too, because most availability series are constant in the normal period
                c, roots, info = traversal(learned["latency"][0], anomalous, tn, check_acyclic=False)
                out["learned_traversal_latgraph"] = (c, info)
                c, roots, info = traversal(dgraph, anomalous, tn, check_acyclic=True)
                out["declared_traversal"] = (c, info)
            for m, (cands, info) in out.items():
                hits, det_rank, rlo, rhi = tie_hits(cands, truth, truncate=TRUNCATE.get(m))
                roots = info.pop("_roots", None) if isinstance(info, dict) else None
                if anomalous is None:
                    fclass = "target_not_anomalous"
                elif truth not in anomalous:
                    fclass = "truth_not_anomalous"
                elif roots is not None and truth not in roots:
                    fclass = "truth_has_anomalous_parent_in_graph"
                elif roots is not None and truth not in [n for n, _ in cands]:
                    fclass = "no_anomalous_path_to_target_in_graph"
                elif hits[3] >= 1.0:
                    fclass = "hit_at_3"
                elif hits[3] > 0:
                    fclass = "tie_straddles_rank_3"
                else:
                    fclass = "ranked_below_3"
                srt = sort_list(cands)
                shown = srt[:3] if m in TRUNCATE else srt
                rows.append({**base, "method": m, "n_candidates": len(cands),
                             "output": [[n, (s if np.isfinite(s) else str(s))] for n, s in shown[:10]],
                             "hits": hits, "rank_name_tiebreak": det_rank if (m not in TRUNCATE or (det_rank or 99) <= 3) else None,
                             "rank_range": [rlo, rhi] if rlo else None,
                             "margin34": margin34(cands), "_cands": cands, "outcome_class": fclass,
                             "flags": {k: v for k, v in info.items() if v}})
    return rows, pcs


def agg(rows, method, split=None, answered_only_tau=None, strict_tau=None, filt=None):
    R = [r for r in rows if r["method"] == method and (split is None or r["split"] == split)]
    if filt:
        R = [r for r in R if filt(r)]
    n = len(R)
    if n == 0:
        return None
    res = {"n": n}
    if answered_only_tau is None and strict_tau is None:
        for k in KS:
            res[f"AC@{k}"] = float(np.mean([r["hits"][k] for r in R]))
        res["Avg@5"] = float(np.mean([np.mean([r["hits"][k] for k in KS]) for r in R]))
        res["empty"] = float(np.mean([r["n_candidates"] == 0 for r in R]))
        res["coverage"] = 1.0
        return res
    tau = answered_only_tau if answered_only_tau is not None else strict_tau
    ans = [r for r in R if not abstains(r["_cands"], tau)]
    res["coverage"] = len(ans) / n
    res["n_answered"] = len(ans)
    for k in KS:
        res[f"AC@{k}_answered"] = float(np.mean([r["hits"][k] for r in ans])) if ans else None
        res[f"AC@{k}_strict"] = float(np.sum([r["hits"][k] for r in ans]) / n)
    res["Avg@5_answered"] = float(np.mean([np.mean([r["hits"][k] for k in KS]) for r in ans])) if ans else None
    res["Avg@5_strict"] = float(np.sum([np.mean([r["hits"][k] for k in KS]) for r in ans]) / n)
    return res


def tune_tau(rows, method):
    grid = []
    for tau in TAU_GRID:
        a = agg(rows, method, split="train", answered_only_tau=tau)
        grid.append({"tau": tau, "coverage": a["coverage"], "AC@3_answered": a["AC@3_answered"]})
    ok = [g for g in grid if g["coverage"] >= 0.5 and g["AC@3_answered"] is not None]
    if not ok:
        return 0.0, grid, "no tau reached train coverage 0.5; tau = 0"
    best = max(g["AC@3_answered"] for g in ok)
    tau = min(g["tau"] for g in ok if g["AC@3_answered"] == best)
    return tau, grid, "max train AC@3 on answered s.t. coverage >= 0.5; ties -> smallest tau"


def specificity(data: Path, taus: dict):
    """Authors' evaluate_specificity windows on the noissue period; 'silent' = empty or abstained."""
    out = []
    for sc in SCENARIOS:
        call_graph, normal, issues, _ = load_scenario(data, sc, False)
        dgraph = declared_causal_graph(call_graph)
        targets = sorted(set((it["target"]["target"]["node"], it["target"]["target"]["metric"],
                              it["target"]["target"]["agg"]) for it in issues))
        N = len(normal.index)
        for tn, tm, ta in targets:
            for split in range(int(N / 2), N - 3, int(N * 0.1)):
                nn, ab = normal.iloc[:split, :], normal.iloc[split:, :]
                anomalous, row = detect(nn, ab, tn, tm, ta)
                rec = {"scenario": sc, "group": GROUP[sc], "metric": tm, "split_at": split}
                if anomalous is None:
                    lists = {m: [] for m in ["ranked_correlation", "mad_rank", "learned_traversal",
                                             "learned_traversal_latgraph", "declared_traversal"]}
                else:
                    tw, _, _ = learn_pc(nn, tm, ta, 0)
                    twl = tw if tm == "latency" else learn_pc(nn, "latency", ta, 0)[0]
                    lists = {"ranked_correlation": ranked_correlation_full(ab, anomalous, tn, tm, ta),
                             "mad_rank": mad_rank(anomalous, tn),
                             "learned_traversal": traversal(tw, anomalous, tn, False)[0],
                             "learned_traversal_latgraph": traversal(twl, anomalous, tn, False)[0],
                             "declared_traversal": traversal(dgraph, anomalous, tn, False)[0]}
                for m, L in lists.items():
                    rec[m] = {"empty": len(L) == 0}
                    if m in taus:
                        rec[m]["abstain"] = abstains(L, taus[m])
                out.append(rec)
    return out


def bootstrap_gap(rows_d, rows_b, tau, n=2000, seed=SEED):
    """rows_* aligned lists (same issues). primary: answered-AC@3(d) - AC@3(b); strict: strict-AC@3(d) - AC@3(b)."""
    rng = np.random.default_rng(seed)
    hd = np.array([r["hits"][3] for r in rows_d])
    ad = np.array([not abstains(r["_cands"], tau) for r in rows_d])
    hb = np.array([r["hits"][3] for r in rows_b])
    m = len(hd)
    prim, strict = [], []
    for _ in range(n):
        idx = rng.integers(0, m, m)
        a = ad[idx]
        if a.sum() > 0:
            prim.append(hd[idx][a].mean() - hb[idx].mean())
        strict.append((hd[idx] * a).sum() / m - hb[idx].mean())
    q = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    return {"primary_ci95": q(prim), "strict_ci95": q(strict), "resamples": n, "seed": seed}


def verdict(gap):
    if gap >= 0.10:
        return "supported"
    if gap < 0.03:
        return "refuted"
    return "inconclusive"


def sanitize(o):
    if isinstance(o, dict):
        return {str(k): sanitize(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [sanitize(v) for v in o]
    if isinstance(o, (np.floating, float)):
        o = float(o)
        return o if np.isfinite(o) else ("inf" if o > 0 else ("-inf" if o < 0 else None))
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def sha_dataset(data: Path):
    h = hashlib.sha256()
    for p in sorted(data.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(data)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(DEFAULT_DATA))
    ap.add_argument("--causal-learn", default=str(DEFAULT_CL))
    ap.add_argument("--skip-specificity", action="store_true")
    args = ap.parse_args()
    sys.path.insert(0, args.causal_learn)
    data = Path(args.data)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    runs = {}
    pcs = {}
    for arm, shuf in [("released", False), ("shuffled", True)]:
        runs[arm], pcs[arm] = run_all(data, shuf)
        print(f"[{arm}] done {time.time() - t0:.1f}s", flush=True)
    rows = runs["released"]

    # tau tuned on train only
    taus, tune = {}, {}
    for m in ["declared_traversal", "ranked_correlation", "learned_traversal"]:
        taus[m], grid, rule = tune_tau(rows, m)
        tune[m] = {"tau": taus[m], "grid": grid, "rule": rule}

    def table(rows, split):
        T = {}
        T["a_ranked_correlation"] = {"regime": "D", **agg(rows, "ranked_correlation", split)}
        T["a2_mad_rank"] = {"regime": "D", **agg(rows, "mad_rank", split)}
        T["b_learned_traversal"] = {"regime": "D", **agg(rows, "learned_traversal", split)}
        T["b_rand_learned_traversal_random_orientation"] = {"regime": "D",
                                                            **agg(rows, "learned_traversal_randorient", split)}
        T["b_lat_posthoc_learned_traversal_latency_graph_for_both_metrics"] = {
            "regime": "D", "post_hoc": True, **agg(rows, "learned_traversal_latgraph", split)}
        T["c_declared_traversal"] = {"regime": "D+K", **agg(rows, "declared_traversal", split)}
        T["d_declared_traversal_abstain"] = {"regime": "D+K", "tau": taus["declared_traversal"],
                                             **agg(rows, "declared_traversal", split,
                                                   answered_only_tau=taus["declared_traversal"])}
        T["e_ranked_correlation_abstain"] = {"regime": "D", "tau": taus["ranked_correlation"],
                                             **agg(rows, "ranked_correlation", split,
                                                   answered_only_tau=taus["ranked_correlation"])}
        T["b_abstain_learned_traversal_abstain"] = {"regime": "D", "tau": taus["learned_traversal"],
                                                    **agg(rows, "learned_traversal", split,
                                                          answered_only_tau=taus["learned_traversal"])}
        return T

    results = {s: table(rows, s) for s in ["test", "train"]}
    results["all"] = table(rows, None)
    results_shuffled = {"test": table(runs["shuffled"], "test")}

    # breakdown on test by group x metric
    breakdown = {}
    for g in ["low", "high", "temporal"]:
        for met in ["latency", "availability"]:
            f = lambda r, g=g, met=met: r["group"] == g and r["metric"] == met
            breakdown[f"{g}|{met}"] = {
                m: {k: v for k, v in agg(rows, m, "test", filt=f).items() if k in ("n", "AC@1", "AC@3", "empty")}
                for m in ["ranked_correlation", "mad_rank", "learned_traversal", "learned_traversal_latgraph",
                          "declared_traversal"]}

    # P15
    T = results["test"]
    d, b = T["d_declared_traversal_abstain"], T["b_learned_traversal"]
    gap_primary = d["AC@3_answered"] - b["AC@3"] if d["AC@3_answered"] is not None else None
    gap_strict = d["AC@3_strict"] - b["AC@3"]
    key = lambda r: (r["scenario"], r["issue"])
    rd = sorted([r for r in rows if r["method"] == "declared_traversal" and r["split"] == "test"], key=key)
    rb = sorted([r for r in rows if r["method"] == "learned_traversal" and r["split"] == "test"], key=key)
    boot = bootstrap_gap(rd, rb, taus["declared_traversal"])
    primary_counts = d["coverage"] >= 0.5
    p15 = {"statement": "declared topology plus abstention beats learned-graph RCA on AC@3 by at least 0.1; "
                        "refuted if the gap is under 0.03",
           "d_AC@3_answered": d["AC@3_answered"], "d_coverage": d["coverage"], "d_AC@3_strict": d["AC@3_strict"],
           "b_AC@3": b["AC@3"], "gap_primary": gap_primary, "gap_strict": gap_strict,
           "verdict_primary": verdict(gap_primary) if (gap_primary is not None and primary_counts) else
           "not applicable (coverage < 0.5)",
           "verdict_strict": verdict(gap_strict), "bootstrap": boot,
           "gap_c_minus_b_no_abstention": T["c_declared_traversal"]["AC@3"] - b["AC@3"],
           "operationalisation": "see ab12_prereg.json (frozen before test results)"}
    p15["verdict"] = p15["verdict_primary"] if primary_counts else p15["verdict_strict"]
    # decomposition (descriptive, not part of the verdict)
    tau_d = taus["declared_traversal"]
    dec = {}
    for met in ["latency", "availability"]:
        f = lambda r, met=met: r["metric"] == met
        dd = agg(rows, "declared_traversal", "test", answered_only_tau=tau_d, filt=f)
        dec[met] = {"n": dd["n"], "d_AC@3_answered": dd["AC@3_answered"], "d_coverage": dd["coverage"],
                    "d_AC@3_strict": dd["AC@3_strict"],
                    "c_AC@3": agg(rows, "declared_traversal", "test", filt=f)["AC@3"],
                    "b_AC@3": agg(rows, "learned_traversal", "test", filt=f)["AC@3"],
                    "b_lat_posthoc_AC@3": agg(rows, "learned_traversal_latgraph", "test", filt=f)["AC@3"]}
        dec[met]["gap_primary"] = (dec[met]["d_AC@3_answered"] - dec[met]["b_AC@3"]) if dec[met]["d_AC@3_answered"] is not None else None
    p15["decomposition_by_metric"] = dec
    blat = T["b_lat_posthoc_learned_traversal_latency_graph_for_both_metrics"]["AC@3"]
    p15["post_hoc_vs_b_lat"] = {"b_lat_AC@3": blat, "gap_primary": (d["AC@3_answered"] - blat),
                                "gap_strict": d["AC@3_strict"] - blat,
                                "verdict_primary": verdict(d["AC@3_answered"] - blat),
                                "note": "post hoc; not the pre-registered comparison"}
    p15["share_of_gap_from_topology"] = {"c_minus_b": T["c_declared_traversal"]["AC@3"] - b["AC@3"],
                                         "d_answered_minus_c": d["AC@3_answered"] - T["c_declared_traversal"]["AC@3"]}

    outcome_classes = {}
    for m in BASE_METHODS:
        cnt = {}
        for r in rows:
            if r["method"] == m and r["split"] == "test":
                cnt[r["outcome_class"]] = cnt.get(r["outcome_class"], 0) + 1
        outcome_classes[m] = dict(sorted(cnt.items()))

    # column-order control
    def per_issue(rows, m):
        return {(r["scenario"], r["split"], r["issue"]): r for r in rows if r["method"] == m}
    col_ctrl = {}
    for m in BASE_METHODS:
        A, B = per_issue(runs["released"], m), per_issue(runs["shuffled"], m)
        changed_hits = [k for k in A if A[k]["hits"] != B[k]["hits"]]
        changed_list = [k for k in A if sorted(A[k]["_cands"]) != sorted(B[k]["_cands"])]
        col_ctrl[m] = {"issues": len(A), "issues_with_different_candidate_set_or_scores": len(changed_list),
                       "issues_with_different_tie_aware_hits": len(changed_hits),
                       "test_AC@3_released": agg(runs["released"], m, "test")["AC@3"],
                       "test_AC@3_shuffled": agg(runs["shuffled"], m, "test")["AC@3"],
                       "changed_examples": ["/".join(k) for k in changed_hits[:10]]}
    pc_diff = {}
    for k in pcs["released"]:
        er, es = pcs["released"][k]["edges"], pcs["shuffled"][k]["edges"]
        pc_diff[k] = {t: {"released": len(er[t]), "shuffled": len(es[t]),
                          "same": len(set(map(tuple, er[t])) & set(map(tuple, es[t])))} for t in er}
        sk_r = {frozenset(e) for t in er for e in er[t]}
        sk_s = {frozenset(e) for t in es for e in es[t]}
        pc_diff[k]["skeleton_identical"] = sk_r == sk_s
    col_ctrl["pc_graph_diff"] = pc_diff

    # reproduction vs published (authors' methods, train+test pooled as in their notebook)
    repro = {}
    for m, pub in [("declared_traversal", "traversal"), ("ranked_correlation", "ranked_correlation")]:
        for (g, met), v in PUBLISHED_TOP3[pub].items():
            f = lambda r, g=g, met=met: r["group"] == g and r["metric"] == met
            R = [r for r in rows if r["method"] == m and f(r)]
            det3 = float(np.mean([(r["rank_name_tiebreak"] or 99) <= 3 for r in R]))
            det1 = float(np.mean([(r["rank_name_tiebreak"] or 99) <= 1 for r in R]))
            a = agg(rows, m, None, filt=f)
            e = {"n": a["n"], "empty": a["empty"], "top1_tieaware": a["AC@1"], "top3_tieaware": a["AC@3"],
                 "top1_name_tiebreak": det1, "top3_name_tiebreak": det3, "published_top3": v}
            if pub == "traversal":
                nb = NOTEBOOK_TRAVERSAL[(g, met)]
                e.update({"notebook_n": nb[0], "notebook_empty": nb[1], "notebook_top1": nb[2], "notebook_top3": nb[3]})
            e["top3_reproduced_within_0.005"] = abs(a["AC@3"] - v) <= 0.005 + 1e-9 or abs(det3 - v) <= 0.005 + 1e-9
            repro[f"{pub}|{g}|{met}"] = e
    repro["epsilon_diagnosis_published_top3"] = {f"{g}|{m}": v for (g, m), v in PUBLISHED_TOP3["epsilon_diagnosis"].items()}

    spec = None
    if not args.skip_specificity:
        sp = specificity(data, taus)
        spec = {}
        for g in ["low", "high", "temporal"]:
            for met in ["latency", "availability"]:
                S = [r for r in sp if r["group"] == g and r["metric"] == met]
                e = {"windows": len(S)}
                for m in ["ranked_correlation", "mad_rank", "learned_traversal", "learned_traversal_latgraph",
                          "declared_traversal"]:
                    e[f"{m}_silent"] = float(np.mean([r[m]["empty"] for r in S]))
                    if m in taus:
                        e[f"{m}_silent_with_abstention"] = float(np.mean([r[m]["empty"] or r[m]["abstain"]
                                                                          for r in S]))
                e["notebook_traversal_specificity"] = NOTEBOOK_SPECIFICITY[(g, met)]
                spec[f"{g}|{met}"] = e
        print(f"[specificity] done {time.time() - t0:.1f}s", flush=True)

    def clean(r):
        r = {k: v for k, v in r.items() if k != "_cands"}
        r["hits"] = {f"AC@{k}": v for k, v in r["hits"].items()}
        return r

    with open(PREREG, "rb") as f:
        prereg_sha = hashlib.sha256(f.read()).hexdigest()
    out = {
        "bundle": "AB-12", "tickets": ["AUD-43", "STR-06"], "producer": "analysis/ab12_rca_probe.py",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dataset": {"name": "AWS PetShop RCA (Hardt et al., CLeaR 2024)", "path": str(data),
                    "sha256_all_files": sha_dataset(data), "licence": "data CC BY 4.0, code Apache-2.0"},
        "prereg": {"file": "analysis/results/rca/ab12_prereg.json", "sha256": prereg_sha},
        "protocol": {"primary_split": "test (48 issues: low 18, high 18, temporal1 6, temporal2 6)",
                     "tuning_split": "train (20 issues; every root cause is PetSearch_AWS::ECS::Fargate)",
                     "normal_period": "noissue/metrics.csv in full (589 rows low/high, 1652 temporal)",
                     "anomaly_detection": "MAD score (statsmodels-scaled) > 5, authors' default",
                     "target_statistic": "Average", "metric_scope": "target metric only (latency or availability)",
                     "AC@k": "tie-aware expected top-k hit, one root cause per issue; Avg@5 = mean AC@1..5",
                     "seeds": {"shuffle": SEED, "bootstrap": SEED,
                               "random_orientation": "crc32(scenario|metric) ^ 20261012"}},
        "tau_tuning": tune,
        "results": results,
        "results_shuffled_columns": results_shuffled,
        "test_breakdown": breakdown,
        "test_outcome_classes": outcome_classes,
        "P15": p15,
        "column_order_control": col_ctrl,
        "reproduction": repro,
        "specificity_noissue": spec,
        "pc_graphs": {arm: {k: {kk: vv for kk, vv in v.items() if kk not in ("edges", "column_order")}
                            for k, v in pcs[arm].items()} for arm in pcs},
        "pc_edges_released": {k: v["edges"] for k, v in pcs["released"].items()},
        "shuffle_permutation_seed": SEED,
        "per_issue": [clean(r) for r in rows],
        "per_issue_shuffled": [{"scenario": r["scenario"], "split": r["split"], "issue": r["issue"],
                                "method": r["method"], "hits": {f"AC@{k}": v for k, v in r["hits"].items()},
                                "rank_range": r["rank_range"]} for r in runs["shuffled"]],
        "cpu_seconds": round(time.process_time(), 1), "wall_seconds": round(time.time() - t0, 1),
    }
    with open(OUT_DIR / "rca_probe.json", "w") as f:
        json.dump(sanitize(out), f, indent=1, allow_nan=False)
    contract = {
        "producer": "analysis/ab12_rca_probe.py",
        "score_bearing": True,
        "tickets": ["AUD-43", "STR-06"],
        "regime": "D+K for declared topology (c, d); D otherwise (a, a2, b, b_rand, e, b+abstain); per-method "
                  "regime is in rca_probe.json results.*.*.regime",
        "split": "test",
        "controls": {"columns_shuffled": "both", "names": "not applicable", "supplier": "petshop"},
        "per_method_regime": {k: v["regime"] for k, v in results["test"].items()},
        "metric_defs": {"AC@k": "tie-aware expected hit of the single true root-cause node in the top k",
                        "Avg@5": "mean of AC@1..AC@5",
                        "coverage": "share of issues answered (not abstained)",
                        "AC@k_answered": "AC@k over answered issues",
                        "AC@k_strict": "AC@k with abstentions counted as misses"},
        "abstention_rule": "abstain iff no candidate, or >= 4 candidates and relative margin between 3rd and 4th "
                           "score <= tau; tau tuned on train only (ab12_prereg.json)",
        "prereg_sha256": prereg_sha,
        "files": {"rca_probe.json": "all results, per-issue ranks, P15 verdict",
                  "ab12_prereg.json": "protocol frozen before test results"},
    }
    with open(OUT_DIR / "CONTRACT.json", "w") as f:
        json.dump(sanitize(contract), f, indent=1, allow_nan=False)
    print(json.dumps({"test": {k: {kk: v[kk] for kk in v if kk.startswith("AC@3") or kk == "coverage"}
                               for k, v in results["test"].items()}, "P15": {k: p15[k] for k in p15 if k != "bootstrap"}},
                     indent=1, default=str))
    print(f"total wall {time.time() - t0:.1f}s cpu {time.process_time():.1f}s")


if __name__ == "__main__":
    main()
