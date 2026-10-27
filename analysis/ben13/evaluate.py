"""BEN-13: CausalBench's statistical and biological evaluation, called through causalbench 1.1.2's own classes.

Tickets: BEN-13

statistical(...) returns causalbench's output_graph block and false omission rate exactly as
`statistical_evaluation.Evaluator.evaluate_network(network, max_path_length, check_false_omission_rate=True,
omission_estimation_size)` computes them, but skips the per-depth tests of the path-closure edges
(`all_path_results`), which no published table reports and which cost most of the time on large networks (up to every
ordered gene pair). The closure itself, which decides which pairs count as negatives for the false omission rate, is
computed by the same loop as the original. `full=True` calls the original method unchanged; one canary run per sheet
checks that both give the same numbers (must-show B13-EVAL). When the closure leaves fewer negatives than the sample
needs, the fast path returns the Wasserstein score with "for": None and the reason in "for_undefined" (the original
cannot evaluate such a network at all).
"""
import random

import numpy as np


def _as_dict(network):
    d = {}
    for a, b in network:
        d.setdefault(a, set()).add(b)
    return d


def closure(network_as_dict, n_genes, max_path_length):
    """The original's loop, without the tests."""
    allc = {**network_as_dict}
    if max_path_length == -1:
        max_path_length = n_genes
    for _ in range(max_path_length - 1):
        deeper = {v: n.union(*[allc[nn] for nn in n if nn in allc]) for v, n in allc.items()}
        deeper = {v: c - {v} for v, c in deeper.items()}
        if deeper == allc:
            break
        allc = deeper
    return allc


def statistical(ev, network, max_path_length=-1, omission_estimation_size=500, full=False):
    """ev: causalscbench.evaluation.statistical_evaluation.Evaluator on the test split."""
    if full:
        if omission_estimation_size > 0:
            nd0 = _as_dict(network)
            allc0 = closure(nd0, len(ev.gene_names), max_path_length)
            free0 = len(ev.gene_names) * (len(ev.gene_names) - 1) - sum(len(v - {k}) for k, v in allc0.items())
            if free0 < omission_estimation_size:
                raise ValueError("only %d negative pairs for %d samples" % (free0, omission_estimation_size))
        r = ev.evaluate_network(network, max_path_length, omission_estimation_size > 0, omission_estimation_size)
        return {"tp": r["output_graph"]["true_positives"], "fp": r["output_graph"]["false_positives"],
                "wasserstein": float(r["output_graph"]["wasserstein_distance"]["mean"]),
                "for": float(r["false_omission_rate"]), "negative_wasserstein": float(r["negative_mean_wasserstein"]),
                "edges": len(set(network)), "evaluator": "causalbench-full"}
    nd = _as_dict(network)
    tp, fp, w = ev._evaluate_network(nd)
    allc = closure(nd, len(ev.gene_names), max_path_length)
    out = {"tp": tp, "fp": fp, "wasserstein": float(np.mean(w)) if w else float("nan"),
           "edges": sum(len(v) for v in nd.values()), "evaluator": "causalbench-fast"}
    if omission_estimation_size > 0:
        names = ev.gene_names
        free = len(names) * (len(names) - 1) - sum(len(v - {k}) for k, v in allc.items())
        if free < omission_estimation_size:
            # The false omission rate draws its negatives outside the network's path closure. A dense network (a random
            # one with thousands of edges, a literature network) closes over almost every pair, so the rate is undefined
            # for it; the original would loop for ever. The Wasserstein score above does not depend on it and is kept
            # (wave A, 22 Oct: 111 cells had dropped it with the rate).
            out["for"] = None
            out["for_undefined"] = "only %d negative pairs outside the path closure; %d needed" % (free, omission_estimation_size)
            return out
        edges = set()
        random.seed(0)
        while len(edges) < omission_estimation_size:
            pair = random.sample(range(len(names)), 2)
            edge = names[pair[0]], names[pair[1]]
            if edge[0] in allc and edge[1] in allc[edge[0]]:
                continue
            edges.add(edge)
        res = ev._evaluate_network(_as_dict(edges))
        out["for"] = res[0] / omission_estimation_size
        out["negative_wasserstein"] = float(np.mean(res[2]))
    return out


def biological(evaluators, network):
    """evaluators: {name: causalscbench biological_evaluation.Evaluator}; undirected true positives, as main_app."""
    out = {}
    net = list(set(network))
    for name, ev in sorted(evaluators.items()):
        tp = ev.evaluate_network(net)["true_positives"]
        out[name] = {"tp": tp, "precision": tp / len(net) if net else float("nan")}
    return out
