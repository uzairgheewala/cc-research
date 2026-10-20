"""BEN-13 S0: CausalBench's preprocessing, streamed, so a 10.7 GB K562 file fits a small-memory machine.

Tickets: BEN-13

    python -m analysis.ben13.stream_preprocess --h5ad external/causalbench/k562.h5ad \
        --summary external/causalbench/summary_stats.xlsx --sheet TabB_K562_day6_summary_stat \
        --out external/causalbench/dataset_k562_filtered.npz [--chunk-rows 2048]

Reproduces causalbench 1.1.2 `data_access.utils.preprocessing.preprocess_dataset` (and `CreateDataset.preprocess_and_save`)
array for array, but never holds the expression matrix in memory. The original reads the whole file with `sc.read`
(K562: 310,385 x 8,563 float32 = 10.6 GB) and copies it twice. Here:

  metadata   obs (gene, gene_id) and var (gene_name, ids) are read with anndata in backed mode (X stays on disk).
  pass 1     row chunks: per-row total counts (np.sum over the full row, float32, as scanpy's filter_cells), the row's own
             target-gene value, and the raw target-gene columns of the control cells.
  decide     strong perturbations (summary sheet), the 10th-percentile knockdown filter per gene (np.percentile on the same
             control column), output row order (genes in first-appearance order, cells in file order), zero-count drop,
             median count, kept columns (intervened gene ids with > 100 cells).
  pass 2     row chunks again: kept rows and columns, divided by (count / median) in float32, log1p, written into a
             disk-backed array at their output positions; then np.savez streams it into the .npz in 16 MB pieces.

Peak memory is about chunk_rows x n_genes x 4 bytes x 3 (default 2048 rows: about 0.2 GB on K562) plus the control
columns (controls x strong genes x 4 bytes, about 45 MB) and the output's page cache, which the OS can drop.
Every arithmetic step uses the same NumPy call on the same dtype as the original, so the output is identical bit for
bit under the same NumPy (checked against the original on synthetic files: tests/test_ben13_stream.py).
A small sidecar JSON records counts, the median, digests and the gene-name map later steps need (instead of the
original's GeneNameMapLoader, which reads both full files again).
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

import numpy as np

CTRL = "non-targeting"


def _log(msg):
    print("[ben13.stream %s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def strong_perts(summary_stats):
    """Exactly causalbench's get_strong_perts."""
    filtered = summary_stats[summary_stats["Number of DEGs (anderson-darling)"] > 50]
    filtered = filtered[filtered["percent knockdown"] <= -0.3]
    filtered = filtered[filtered["number of cells (filtered)"] > 25]
    return [s.split("_")[1] for s in filtered["genetic perturbation"].values]


def _rows(X, start, stop):
    a = X[start:stop]
    if hasattr(a, "toarray"):
        a = a.toarray()
    return np.ascontiguousarray(a)


def sha256_array(a, chunk=1 << 20):
    h = hashlib.sha256()
    h.update(str(a.dtype).encode() + str(a.shape).encode())
    flat = a.reshape(-1) if a.ndim else a.reshape(1)
    for i in range(0, flat.size, chunk):
        h.update(np.ascontiguousarray(flat[i:i + chunk]).tobytes())
    return h.hexdigest()


def preprocess_stream(h5ad, summary_stats=None, chunk_rows=2048, scratch=None):
    """-> (memmap expression matrix, gene_ids list, interventions list, info dict). summary_stats: DataFrame or None."""
    import anndata
    import pandas as pd

    t0 = time.time()
    ad = anndata.read_h5ad(h5ad, backed="r")
    n, g = ad.shape
    X = ad.X
    obs_gene = ad.obs["gene"].astype(str).to_numpy()
    obs_gene_id = ad.obs["gene_id"].astype(str).to_numpy()
    var_ids = np.asarray(ad.var_names.astype(str))
    var_gene_name = ad.var["gene_name"].astype(str).to_numpy()
    _log("%s: %d cells x %d genes, X %s" % (Path(h5ad).name, n, g, getattr(X, "dtype", "?")))

    # ---- which rows enter (strong perturbations + controls), and the genes' first-appearance order
    if summary_stats is not None:
        keep_set = set(strong_perts(summary_stats) + [CTRL])
        keep0 = np.fromiter((v in keep_set for v in obs_gene), bool, n)
        do_effect_filter = True
    else:
        keep0 = np.ones(n, bool)
        do_effect_filter = False
    genes_order = list(pd.unique(obs_gene[keep0]))
    rank = {gname: i for i, gname in enumerate(genes_order)}
    first_loc = {}
    for j, nm in enumerate(var_gene_name):
        first_loc.setdefault(nm, j)
    # the original wraps the lookup in try/except: a gene with no column keeps all its cells
    loc_of = {gname: first_loc[gname] for gname in genes_order if gname != CTRL and gname in first_loc}
    need_locs = sorted(set(loc_of.values()))
    col_of_loc = {loc: k for k, loc in enumerate(need_locs)}
    is_ctrl = keep0 & (obs_gene == CTRL)
    n_ctrl = int(is_ctrl.sum())

    # ---- pass 1
    row_sum = np.zeros(n, np.float32)
    self_val = np.full(n, np.nan, np.float32)
    row_loc = np.array([loc_of.get(gname, -1) for gname in obs_gene], np.int64)
    ctrl_cols = np.zeros((n_ctrl, len(need_locs)), np.float32)
    ci = 0
    need_arr = np.asarray(need_locs, np.int64)
    for s in range(0, n, chunk_rows):
        e = min(n, s + chunk_rows)
        sel = keep0[s:e]
        if not sel.any():
            continue
        A = _rows(X, s, e)
        row_sum[s:e] = np.sum(A, axis=1)          # scanpy filter_cells: np.sum(X, axis=1) on the float32 rows
        has = (row_loc[s:e] >= 0) & sel
        idx = np.nonzero(has)[0]
        self_val[s + idx] = A[idx, row_loc[s:e][idx]]
        c = np.nonzero(is_ctrl[s:e])[0]
        if c.size and need_arr.size:
            ctrl_cols[ci:ci + c.size] = A[c][:, need_arr]
        ci += c.size
        if (s // chunk_rows) % 25 == 0:
            _log("pass 1: %d / %d rows" % (e, n))
    assert ci == n_ctrl

    # ---- the knockdown-effect filter (filter_cells_by_pert_effect, k=10)
    kept = keep0.copy()
    thresholds = {}
    if do_effect_filter:
        for gname, loc in loc_of.items():
            thresh = np.percentile(ctrl_cols[:, col_of_loc[loc]], 10)
            thresholds[gname] = float(thresh)
            rows = keep0 & (obs_gene == gname)
            kept[rows] = self_val[rows] <= thresh
    # output order: genes in first-appearance order, cells in file order within a gene
    kept_idx = np.nonzero(kept)[0]
    order = np.argsort(np.array([rank[obs_gene[i]] for i in kept_idx], np.int64), kind="stable")
    out_rows = kept_idx[order]
    # normalize_per_cell(key_n_counts='UMI_count'): filter_cells(min_counts=1) drops zero-count cells, then the median
    counts = row_sum[out_rows]
    nonzero = counts >= 1
    out_rows, counts = out_rows[nonzero], counts[nonzero]
    counts_per_cell_after = np.median(counts)
    counts_per_cell = counts.copy()
    counts_per_cell += counts_per_cell == 0
    counts_per_cell /= counts_per_cell_after

    # ---- interventions and kept columns (the original's gene_to_interventions on the normalized frame)
    var_set = set(var_ids.tolist())
    ids = obs_gene_id[out_rows]
    count = {}
    for v in ids:
        if v in var_set or v == CTRL:
            count[v] = count.get(v, 0) + 1
    intervened_set = {v for v, c in count.items() if c > 100}
    interventions = [v if v in intervened_set else "excluded" for v in ids]
    col_mask = np.isin(var_ids, list(intervened_set))
    out_cols = np.nonzero(col_mask)[0]
    gene_ids = var_ids[out_cols].tolist()

    # ---- pass 2 into a disk-backed array
    dest = np.full(n, -1, np.int64)
    dest[out_rows] = np.arange(out_rows.size)
    scratch = Path(scratch or (Path(h5ad).parent / ".ben13_scratch"))
    scratch.mkdir(parents=True, exist_ok=True)
    mm_path = scratch / (Path(h5ad).stem + "_expr.npy")
    M = np.lib.format.open_memmap(str(mm_path), mode="w+", dtype=np.float32, shape=(out_rows.size, out_cols.size))
    for s in range(0, n, chunk_rows):
        e = min(n, s + chunk_rows)
        d = dest[s:e]
        idx = np.nonzero(d >= 0)[0]
        if not idx.size:
            continue
        A = _rows(X, s, e)[idx]                     # kept rows, all columns (the original divides the full matrix)
        A /= counts_per_cell[d[idx]][:, np.newaxis]
        np.log1p(A, out=A)                           # scanpy log1p on a dense float array
        M[d[idx]] = A[:, out_cols]
        if (s // chunk_rows) % 25 == 0:
            _log("pass 2: %d / %d rows" % (e, n))
    M.flush()
    info = {"cells_in": int(n), "genes_in": int(g), "strong_rows": int(keep0.sum()), "controls": n_ctrl,
            "after_effect_filter": int(kept.sum()), "zero_count_dropped": int((~nonzero).sum()),
            "cells_out": int(out_rows.size), "genes_out": int(out_cols.size),
            "median_count": float(counts_per_cell_after), "median_dtype": str(np.asarray(counts_per_cell_after).dtype),
            "genes_with_effect_filter": len(thresholds), "seconds": round(time.time() - t0, 1),
            "name_to_id_pairs": sorted(set(zip(var_gene_name.tolist(), var_ids.tolist()))),
            "intervened_ids_all": sorted(set(obs_gene_id.tolist()))}
    return M, gene_ids, interventions, info, mm_path


def write_npz(out, M, gene_ids, interventions):
    """Same call as CreateDataset.preprocess_and_save; np.savez writes a memmap in 16 MB pieces."""
    tmp = Path(str(out) + ".partial")
    with open(tmp, "wb") as fh:
        np.savez(fh, expression_matrix=M, var_names=gene_ids, interventions=interventions)
    os.replace(tmp, out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--summary", default="", help="summary_stats.xlsx (omit for the unfiltered dataset)")
    ap.add_argument("--sheet", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--chunk-rows", type=int, default=2048)
    ap.add_argument("--keep-scratch", action="store_true")
    a = ap.parse_args(argv)
    out = Path(a.out)
    side = Path(str(out) + ".json")
    if out.exists() and side.exists():
        _log("already done: %s" % out)
        return 0
    stats = None
    if a.summary:
        import pandas as pd
        stats = pd.read_excel(a.summary, sheet_name=a.sheet)
    M, gene_ids, interventions, info, mm_path = preprocess_stream(a.h5ad, stats, a.chunk_rows)
    write_npz(out, M, gene_ids, interventions)
    info.update({"tickets": ["BEN-13"], "source": str(Path(a.h5ad).name), "sheet": a.sheet or None,
                 "npz": str(out.name), "npz_bytes": out.stat().st_size,
                 "expression_sha256": sha256_array(np.load(mm_path, mmap_mode="r")),
                 "var_names_sha256": hashlib.sha256("\n".join(gene_ids).encode()).hexdigest(),
                 "interventions_sha256": hashlib.sha256("\n".join(interventions).encode()).hexdigest(),
                 "numpy": np.__version__, "python": sys.version.split()[0]})
    del M
    if not a.keep_scratch:
        try:
            os.remove(mm_path)
        except OSError:
            pass
    tmp = Path(str(side) + ".partial")
    tmp.write_text(json.dumps(info, indent=1))
    os.replace(tmp, side)
    _log("wrote %s: %d cells x %d genes (%.0f s)" % (out, info["cells_out"], info["genes_out"], info["seconds"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
