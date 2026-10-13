"""Build a name-controlled dataset suite from datasets bundled with Causal-Copilot (bundle 1).

  python make_suite.py --repo /path/to/Causal-Copilot --out /path/to/cc-research/datasets/suite_b1

For every source dataset that has a reference graph, three arms are written. The numbers are
byte-identical in all three; only the header line differs. Directory and file names are opaque codes
so that the file path (which Causal-Copilot shows to the LLM) says nothing about the dataset or arm.

  role      column labels
  real      the dataset's own names, on their own columns
  neutral   V01..Vnn
  swapped   the dataset's own names, each moved to another column (a derangement chosen by an
            exhaustive, deterministic search to minimise the pairs that are adjacent both in the
            reference read by label and in the reference read by data)

Sources are the four named real datasets in the repo that also appear in CausalArena's real-data
slice (Abalone, Auto MPG, Concrete Compressive Strength, Deutscher Wetterdienst). Their reference
graphs are the repo's base_graph.npy files; scores against them are agreement with those references.

Gates (exit code 1 if any fails), per family:
  D1  body of every arm byte-identical to the source file's body
  D2  the real arm's header equals the source header
  D3  the swapped labelling is a derangement
  D4  shared adjacent pairs between the two references equals the search result
  D5  every arm parses to the source's shape and values
  D6  the reference has the same number of variables as the data and at least one edge
  D7  no arm code, directory or file name contains a source name or a role word
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SOURCES = [   # (family, repo-relative csv, repo-relative reference, family code digit)
    ("abalone", "data/dataset/Abalone/Abalone.csv", "data/dataset/Abalone/base_graph.npy", 1),
    ("autompg", "data/dataset/Auto_mpg/Auto_mpg.csv", "data/dataset/Auto_mpg/base_graph.npy", 2),
    ("concrete", "data/dataset/CCS_Data/CCS_Data.csv", "data/dataset/CCS_Data/base_graph.npy", 3),
    ("dwd", "data/dataset/DWD/DWD.csv", "data/dataset/DWD/base_graph.npy", 4),
]
ROLES = [("real", 1), ("neutral", 2), ("swapped", 3)]
FORBIDDEN_IN_NAMES = ["abalone", "auto", "mpg", "ccs", "concrete", "dwd", "real", "neutral", "swap", "shuffl", "orig"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def ref_edges(ref):
    """(cause, effect) index pairs. ref[i, j] == 1 means j -> i; this holds both for the repo's 0/1
    files and for its causal-learn style +1/-1 files (checked edge by edge for each source)."""
    return sorted((int(j), int(i)) for i, j in np.argwhere(np.asarray(ref) == 1))


def to_matrix(edges, p):
    M = np.zeros((p, p), dtype=int)
    for c, e in edges:
        M[e, c] = 1
    return M


def best_derangement(E, p):
    """Lexicographically first derangement perm (label on column k is names[perm[k]]) minimising the
    number of true edges (u, v) whose relabelled pair {perm[u], perm[v]} is also adjacent in E."""
    adj = {frozenset(e) for e in E}
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
    return state["best"], state["overlap"], state["nodes"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--suite", default="suite_b1")
    a = ap.parse_args()
    repo, out = Path(a.repo), Path(a.out)
    refdir = out / "_reference"
    refdir.mkdir(parents=True, exist_ok=True)
    mapping = {"format": 2, "suite": a.suite, "arms": {}, "families": {}, "gates": {}}
    all_ok = True
    for family, csv_rel, ref_rel, digit in SOURCES:
        raw = (repo / csv_rel).read_bytes()
        ref = np.load(repo / ref_rel)
        nl = raw.index(b"\n")
        header, body = raw[:nl], raw[nl:]
        cr = header.endswith(b"\r")
        names = header.rstrip(b"\r").decode("utf-8").split(",")
        p = len(names)
        src_df = pd.read_csv(repo / csv_rel)
        E = ref_edges(ref)
        g = {"D6_reference_matches_data": bool(ref.shape == (p, p) and len(E) > 0 and list(src_df.columns) == names)}
        perm, overlap, nodes = best_derangement(E, p)
        inv = [perm.index(k) for k in range(p)]
        by_data = to_matrix(E, p)
        by_label = to_matrix([(inv[u], inv[v]) for (u, v) in E], p)
        np.save(refdir / ("%s_by_data.npy" % family), by_data)
        np.save(refdir / ("%s_swapped_by_label.npy" % family), by_label)
        labels = {"real": names, "neutral": ["V%02d" % (k + 1) for k in range(p)], "swapped": [names[perm[k]] for k in range(p)]}
        d1 = d5 = d7 = True
        codes = {}
        for role, rd in ROLES:
            code = "k%d%d" % (digit, rd)
            codes[role] = code
            d = out / code
            d.mkdir(parents=True, exist_ok=True)
            hb = ",".join(labels[role]).encode("utf-8") + (b"\r" if cr else b"")
            data = raw if role == "real" else hb + body
            f = d / (code + ".csv")
            f.write_bytes(data)
            back = f.read_bytes()
            d1 &= back[back.index(b"\n"):] == body
            if role == "real":
                g["D2_real_header_is_source_header"] = back[:back.index(b"\n")] == header
            df = pd.read_csv(f)
            d5 &= df.shape == src_df.shape and list(df.columns) == labels[role] and np.array_equal(df.values, src_df.values)
            d7 &= not any(w in code.lower() for w in FORBIDDEN_IN_NAMES)
            mapping["arms"][code] = {
                "family": family, "role": role,
                "dataset_arg": "research:datasets/%s/%s/%s.csv" % (a.suite, code, code),
                "sha256": sha(back), "bytes": len(back), "path_says_name": False,
                "column_labels": labels[role], "data_in_each_column_is_really": names,
                "reference_by_data": "_reference/%s_by_data.npy" % family,
                "reference_by_label": ("_reference/%s_swapped_by_label.npy" % family) if role == "swapped" else (
                    None if role == "neutral" else "_reference/%s_by_data.npy" % family),
            }
        shared = len({frozenset(map(int, x)) for x in np.argwhere(by_data == 1)} & {frozenset(map(int, x)) for x in np.argwhere(by_label == 1)})
        g.update({"D1_bodies_byte_identical": bool(d1), "D3_swapped_is_derangement": all(perm[k] != k for k in range(p)),
                  "D4_shared_pairs_match_search": shared == overlap, "D5_parsed_values_identical": bool(d5),
                  "D7_opaque_names": bool(d7)})
        mapping["families"][family] = {
            "source_csv": csv_rel, "source_sha256": sha(raw), "reference": ref_rel,
            "reference_sha256": sha((repo / ref_rel).read_bytes()),
            "rows": int(src_df.shape[0]), "columns": names, "arms": codes,
            "reference_edges": ["%s->%s" % (names[c], names[e]) for c, e in E],
            "swapped_labels_by_column": labels["swapped"],
            "adjacent_pairs_shared_by_the_two_references": shared, "search_nodes_visited": nodes,
            "gates": g,
        }
        mapping["gates"][family] = bool(all(g.values()))
        all_ok &= all(g.values())
        print("%-9s p=%d n=%d edges=%d shared=%d arms=%s gates=%s" % (family, p, src_df.shape[0], len(E), shared, codes,
                                                                    "PASS" if all(g.values()) else {k: v for k, v in g.items() if not v}))
    (out / "MAPPING.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
