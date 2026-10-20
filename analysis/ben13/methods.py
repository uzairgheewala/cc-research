"""BEN-13 S1-S2: the methods and controls that are scored. Each returns a list of (parent id, child id) pairs.

Tickets: BEN-13

Published rows reproduced (CausalBench Challenge report, arXiv 2308.15395, Kowiel et al.):
  mean_difference(k)   for every gene A with knockdown cells in the training split and every other gene B:
                       |mean(B | A knocked down) - mean(B | non-targeting)|; the k largest pairs. No thresholds.
                       Ties are broken by (parent, child) id so the ranking is deterministic (not specified in the
                       report; recorded in the pre-registration).
Baselines: random_network(k) (seeded, uniform over ordered pairs of distinct genes), and literature networks
(STRING / CORUM pairs among the dataset's genes, built in analysis/ben13/literature.py) used as predicted networks.

Controls (pre-registered in plans/ben13_prereg.json):
  rewire_children(net)  keep each parent and its out-degree, draw its children uniformly among the other genes
                        (edge placement: how much of a score the choice of parents carries on its own)
  permute_labels(net)   apply one random bijection of gene ids to every pair (keeps the graph's shape, removes what
                        the specific genes carry: the statistical metric then sees an unrelated network of the same
                        shape, and the biological metric sees names that no longer match)
  test_oracle(k)        mean_difference ranked on the TEST split itself: the metric's echo ceiling for a
                        total-effect ranking at k edges (not a method; used only as a reference point)
"""
import numpy as np

CTRL = "non-targeting"


def group_means(X, interventions, gene_names):
    """-> (control mean vector, {gene id: mean vector of its knockdown cells}) over the rows given."""
    interventions = np.asarray(interventions)
    ctrl = X[interventions == CTRL].mean(axis=0, dtype=np.float64)
    names = set(gene_names)
    means = {}
    for gid in np.unique(interventions):
        if gid in names:
            means[gid] = X[interventions == gid].mean(axis=0, dtype=np.float64)
    return ctrl, means


def mean_difference_scores(X, interventions, gene_names):
    """-> list of (score, parent, child), every parent with knockdown cells, every child != parent."""
    ctrl, means = group_means(X, interventions, gene_names)
    out = []
    for a in sorted(means):
        d = np.abs(means[a] - ctrl)
        for j, b in enumerate(gene_names):
            if b != a:
                out.append((float(d[j]), a, b))
    return out


def top_k(scored, k):
    scored = sorted(scored, key=lambda t: (-t[0], t[1], t[2]))
    return [(a, b) for _, a, b in scored[:k]]


def mean_difference(X, interventions, gene_names, k):
    return top_k(mean_difference_scores(X, interventions, gene_names), k)


def random_network(gene_names, k, seed):
    rng = np.random.default_rng(seed)
    g = len(gene_names)
    seen, out = set(), []
    while len(out) < min(k, g * (g - 1)):
        i, j = rng.integers(0, g, size=2)
        if i != j and (i, j) not in seen:
            seen.add((i, j))
            out.append((gene_names[i], gene_names[j]))
    return out


def rewire_children(net, gene_names, seed):
    rng = np.random.default_rng(seed)
    outdeg = {}
    for a, _ in net:
        outdeg[a] = outdeg.get(a, 0) + 1
    out = []
    for a in sorted(outdeg):
        others = [g for g in gene_names if g != a]
        pick = rng.choice(len(others), size=min(outdeg[a], len(others)), replace=False)
        out += [(a, others[i]) for i in sorted(pick)]
    return out


def permute_labels(net, gene_names, seed):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(gene_names))
    m = {g: gene_names[perm[i]] for i, g in enumerate(gene_names)}
    return [(m[a], m[b]) for a, b in net]
