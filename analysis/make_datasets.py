"""Build the derived datasets for the name-versus-data test (pass 4b). Reads the repo, writes only under cc-research/datasets.

  python make_datasets.py --repo /path/to/Causal-Copilot --out /path/to/cc-research/datasets

Design. Two things in a prompt can tell the model which dataset it is looking at: the file path
(Causal-Copilot puts the path in the knowledge prompt) and the column names. Four arms separate them.
The numbers in every file are byte-identical to the repo's sachs.csv; only the header line and the
file name differ.

  arm     file                 path says "sachs"   column labels
  sachs   sachs/sachs.csv      yes                 real names, on their own data
  d01     d01/d01.csv          no                  real names, on their own data
  d02     d02/d02.csv          no                  V01..V11
  d03     d03/d03.csv          no                  real names, each moved to another protein's column

For d03 the labels are a derangement of the real names (no label stays on its own column), chosen by an
exhaustive, deterministic search so that the reference graph read "by label" and the reference graph read "by data"
share as few adjacent pairs as possible. That makes "this edge follows the names" and "this edge follows
the data" distinguishable for every edge.

Gates (the script exits non-zero if any fails):
  D1  the body (everything after the header line) of every derived file is byte-identical to the source
  D2  sachs/sachs.csv is byte-identical to the source file
  D3  d03's labelling is a derangement
  D4  the by-label and by-data reference graphs of d03 share the recorded number of adjacent pairs
  D5  every file parses with pandas to the same shape and the same values as the source
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd



def sha(b):
    return hashlib.sha256(b).hexdigest()


def ref_edges(ref):
    """(cause, effect) index pairs; the repo file uses the causal-learn convention, which for value 1
    coincides with Causal-Copilot's: ref[i, j] == 1 means j -> i."""
    return sorted((int(j), int(i)) for i, j in np.argwhere(ref == 1))


def to_matrix(edges, p):
    M = np.zeros((p, p), dtype=int)
    for c, e in edges:
        M[e, c] = 1
    return M


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    src = Path(a.repo) / "data" / "dataset" / "sachs" / "sachs.csv"
    ref = np.load(Path(a.repo) / "data" / "dataset" / "sachs" / "base_graph.npy")
    raw = src.read_bytes()
    nl = raw.index(b"\n")
    header, body = raw[:nl], raw[nl:]              # body starts with the newline that ends the header
    cr = header.endswith(b"\r")
    names = header.rstrip(b"\r").decode("utf-8").split(",")
    p = len(names)
    E = ref_edges(ref)
    adj = {frozenset(e) for e in E}

    # derangement search: label on column k is names[perm[k]].
    # Exhaustive depth-first branch and bound in lexicographic order, so the result is the
    # lexicographically first derangement with the fewest shared adjacent pairs. No random numbers.
    # by-data reference in label terms: true edge u->v appears as names[perm[u]] -> names[perm[v]]
    nbr = {k: set() for k in range(p)}
    for (u, v) in E:
        nbr[u].add(v)
        nbr[v].add(u)
    state = {"best": None, "overlap": None, "nodes": 0}

    def dfs(k, perm, used, cost):
        state["nodes"] += 1
        if state["overlap"] is not None and cost >= state["overlap"]:
            return
        if k == p:
            state["best"], state["overlap"] = list(perm), cost
            return
        for lab in range(p):
            if lab == k or lab in used:
                continue
            add = sum(1 for u in nbr[k] if u < k and frozenset((perm[u], lab)) in adj)
            perm.append(lab)
            used.add(lab)
            dfs(k + 1, perm, used, cost + add)
            perm.pop()
            used.discard(lab)
            if state["overlap"] == 0:
                return

    dfs(0, [], set(), 0)
    best, best_overlap, tried = state["best"], state["overlap"], state["nodes"]
    perm = best
    inv = [perm.index(k) for k in range(p)]        # column that carries label names[k]

    arms = {
        "sachs": {"dir": "sachs", "file": "sachs.csv", "labels": names, "path_says_sachs": True},
        "d01": {"dir": "d01", "file": "d01.csv", "labels": names, "path_says_sachs": False},
        "d02": {"dir": "d02", "file": "d02.csv", "labels": ["V%02d" % (k + 1) for k in range(p)], "path_says_sachs": False},
        "d03": {"dir": "d03", "file": "d03.csv", "labels": [names[perm[k]] for k in range(p)], "path_says_sachs": False},
    }
    out = Path(a.out)
    refdir = out / "_reference"
    refdir.mkdir(parents=True, exist_ok=True)
    # reference graphs in COLUMN-INDEX space (the space the pipeline's matrices live in)
    by_data = to_matrix(E, p)                                               # the data did not move
    by_label_d03 = to_matrix([(inv[u], inv[v]) for (u, v) in E], p)         # where the labels of each reference edge now sit
    np.save(refdir / "reference_by_data.npy", by_data)
    np.save(refdir / "d03_reference_by_label.npy", by_label_d03)

    gates, mapping = {}, {"source": {"file": "data/dataset/sachs/sachs.csv", "sha256": sha(raw), "bytes": len(raw),
                                     "reference_graph": "data/dataset/sachs/base_graph.npy",
                                     "reference_sha256": sha((Path(a.repo) / "data/dataset/sachs/base_graph.npy").read_bytes()),
                                     "columns": names, "rows": int(pd.read_csv(src).shape[0]),
                                     "reference_edges": ["%s->%s" % (names[c], names[e]) for c, e in E]},
                          "derangement_search": {"method": "exhaustive depth-first branch and bound, lexicographic order, no random numbers",
                                                 "search_nodes_visited": tried,
                                                 "rule": "lexicographically first derangement with the fewest shared adjacent pairs"},
                          "arms": {}}
    src_df = pd.read_csv(src)
    d1 = d5 = True
    for arm, spec in arms.items():
        d = out / spec["dir"]
        d.mkdir(parents=True, exist_ok=True)
        hb = ",".join(spec["labels"]).encode("utf-8") + (b"\r" if cr else b"")
        data = raw if arm == "sachs" else hb + body
        (d / spec["file"]).write_bytes(data)
        back = (d / spec["file"]).read_bytes()
        d1 &= back[back.index(b"\n"):] == body
        df = pd.read_csv(d / spec["file"])
        d5 &= df.shape == src_df.shape and list(df.columns) == spec["labels"] and np.array_equal(df.values, src_df.values)
        mapping["arms"][arm] = {
            "dataset_arg": "research:datasets/%s/%s" % (spec["dir"], spec["file"]),
            "sha256": sha(back), "bytes": len(back), "path_says_sachs": spec["path_says_sachs"],
            "column_labels": spec["labels"],
            "data_in_each_column_is_really": names,
            "reference_by_data": "_reference/reference_by_data.npy",
            "reference_by_label": "_reference/d03_reference_by_label.npy" if arm == "d03" else (
                None if arm == "d02" else "_reference/reference_by_data.npy"),
        }
    gates["D1_bodies_byte_identical"] = bool(d1)
    gates["D2_sachs_copy_byte_identical"] = (out / "sachs" / "sachs.csv").read_bytes() == raw
    gates["D3_d03_is_derangement"] = all(perm[k] != k for k in range(p))
    shared = len({frozenset(x) for x in map(tuple, np.argwhere(by_data == 1))} & {frozenset(x) for x in map(tuple, np.argwhere(by_label_d03 == 1))})
    gates["D4_shared_adjacent_pairs_matches_search"] = shared == best_overlap
    gates["D5_parsed_values_identical"] = bool(d5)
    mapping["d03"] = {"label_on_each_column": dict(zip(["column %d (data of %s)" % (k + 1, names[k]) for k in range(p)], arms["d03"]["labels"])),
                      "adjacent_pairs_shared_by_the_two_references": shared,
                      "by_label_reference_edges_in_column_terms": ["col%d->col%d" % (c + 1, e + 1) for c, e in ref_edges(by_label_d03)]}
    mapping["gates"] = gates
    (out / "MAPPING.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(json.dumps({"gates": gates, "d03_labels": arms["d03"]["labels"], "shared_adjacent_pairs": shared, "tries": tried,
                      "rows": src_df.shape[0], "sha": {k: v["sha256"][:12] for k, v in mapping["arms"].items()}}, indent=1))
    sys.exit(0 if all(gates.values()) else 1)


if __name__ == "__main__":
    main()
