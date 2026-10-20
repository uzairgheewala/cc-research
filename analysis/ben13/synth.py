"""BEN-13: a small synthetic CausalBench-shaped file (h5ad + summary sheet), for tests and smoke runs.

Tickets: BEN-13

    python -m analysis.ben13.synth --out DIR [--cells 4000 --genes 80 --seed 0]

Shaped like the Replogle et al. K562 file causalbench reads: dense float32 UMI counts, obs columns `gene` (perturbed gene
name or "non-targeting") and `gene_id` (Ensembl-like id), var index = ids with a `gene_name` column; plus a summary
sheet with the four columns get_strong_perts filters on. It covers the cases the preprocessing branches on: weak
perturbations (dropped), a perturbed gene with no expression column (kept whole), groups at or under 100 cells (marked
"excluded"), a duplicated gene name in var, zero-count cells, and genes listed out of file order.
Effects are planted: each perturbed gene knocks itself down and shifts a few fixed children, so methods have signal.
"""
import argparse, json
from pathlib import Path

import numpy as np

SHEET = "TabB_K562_day6_summary_stat"


def make(out, cells=4000, genes=80, seed=0, n_perturbed=12):
    import anndata
    import pandas as pd

    rng = np.random.default_rng(seed)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    names = ["G%03d" % i for i in range(genes)]
    names[7] = names[3]                                   # a duplicated gene name in var
    ids = ["ENSG%011d" % (1000 + i) for i in range(genes)]
    base_set = [2, 3, 5, 9, 11, 13, 17, 19, 23, 29, 31, 37]
    extra = [i for i in range(45, genes) if i not in base_set][:max(0, n_perturbed - len(base_set))]
    perturbed = ["G%03d" % i for i in base_set[:n_perturbed] + extra] + ["NOEXPR1"]
    weak = ["G%03d" % i for i in (41, 43)]
    groups = perturbed + weak + ["non-targeting"]
    sizes = {gname: int(rng.integers(60, 400)) for gname in groups}
    sizes["non-targeting"] = 0
    sizes["non-targeting"] = max(cells - sum(sizes.values()), cells // 5)
    sizes["G019"] = 100                                   # exactly 100 cells: excluded (> 100 required)
    labels = np.concatenate([[gname] * sizes[gname] for gname in groups])
    rng.shuffle(labels)
    n = labels.size
    base = rng.gamma(2.0, 2.0, size=genes)
    lib = rng.lognormal(0, 0.35, size=n)
    mu = np.outer(lib, base)
    children = {gname: rng.choice(genes, size=4, replace=False) for gname in perturbed}
    for gname in perturbed:
        rows = labels == gname
        if gname in names:
            j = names.index(gname)
            mu[rows, j] *= 0.25                           # knockdown
            for c in children[gname]:
                if c != j:
                    mu[rows, c] *= rng.choice([0.4, 2.2])
    X = rng.poisson(mu).astype(np.float32)
    X[rng.choice(n, size=3, replace=False)] = 0.0         # zero-count cells
    id_of = {}
    for nm, i in zip(names, ids):
        id_of.setdefault(nm, i)
    gene_id = [("non-targeting" if gname == "non-targeting" else id_of.get(gname, "ENSG99999999999")) for gname in labels]
    obs = pd.DataFrame({"gene": pd.Categorical(labels), "gene_id": pd.Categorical(gene_id)},
                       index=["cell%05d" % i for i in range(n)])
    var = pd.DataFrame({"gene_name": names}, index=ids)
    anndata.AnnData(X=X, obs=obs, var=var).write_h5ad(out / "synth.h5ad")
    rows = []
    for gname in perturbed + weak:
        strong = gname not in weak
        rows.append({"genetic perturbation": "%d_%s_P1P2_%s" % (len(rows), gname, id_of.get(gname, "X")),
                     "Number of DEGs (anderson-darling)": 120 if strong else 10,
                     "percent knockdown": -0.7 if strong else -0.1,
                     "number of cells (filtered)": sizes[gname]})
    pd.DataFrame(rows).to_excel(out / "summary_stats.xlsx", sheet_name=SHEET, index=False)
    truth = {gname: sorted(names[c] for c in children[gname]) for gname in perturbed}
    (out / "synth_truth.json").write_text(json.dumps({"children": truth, "sizes": sizes}, indent=1))
    return out / "synth.h5ad", out / "summary_stats.xlsx"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cells", type=int, default=4000)
    ap.add_argument("--genes", type=int, default=80)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--perturbed", type=int, default=12)
    a = ap.parse_args()
    print(make(a.out, a.cells, a.genes, a.seed, a.perturbed))
