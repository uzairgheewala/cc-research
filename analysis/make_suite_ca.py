"""Build S2 of the Quarter 1 suite: 10 CausalArena semantic test scenarios, columns shuffled, three name arms (BND-05).

  python analysis/make_suite_ca.py                      # writes datasets/suite_q1s2/, exits 1 if any gate fails
  python analysis/make_suite_ca.py --check              # rebuilds in memory and compares with what is on disk

Source per scenario: replicate 0 of the observational-only release
(external/causalarena/scm/semantic/data/semantic_obs_only/semantic_<domain>_<slug>__semantic_obs_only__rep000.npz).
Scenarios: plans/splits.json families.semantic.s2_test_scenarios (fixed by the split rule before any tuning).

Column order. CausalArena's released column order is a topological order of the true graph (every true edge runs from
an earlier to a later column; analysis/causalarena_order_baseline.py). Each scenario's columns are permuted with a
generator seeded by sha256("cc-research-s2-shuffle-v1:<scenario_id>"); a draw that is still topological is replaced by
the next draw (counter appended to the seed string) and the number of draws is recorded.

Arms (body bytes identical in all three; only the header differs; paths are opaque codes):
  real      the scenario's own node ids on their own columns
  neutral   V01..Vnn
  swapped   the node ids moved by a derangement chosen to minimise pairs adjacent in both the reference read by data and
            the reference read by label (depth-first, lexicographic, node budget; whether the minimum is proved is recorded)

Values: x[:, :, 0] (float32, standardised by the release) written with 9 significant digits, which round-trips float32.

Gates, per scenario (exit 1 if any fails):
  D1  body of every arm byte-identical to the others
  D2  real arm header equals the node ids in shuffled order; ids match ^[A-Za-z0-9_]+$
  D3  swapped labelling is a derangement
  D4  shared adjacent pairs between the two references equals the search result
  D5  every arm parses to the source values (float32 exact) in shuffled order, n rows x d columns
  D6  reference has d variables and at least one edge; the file is observational only (n_int == 0, no intervened cell)
  D7  no code, directory or file name contains a role word or any token (>= 4 letters) of any scenario id or domain
  D8  reference by data equals the release's g (permuted) and equals graph.json's edges read by name; g identical in rep000-rep004
  D9  permutation recorded, applying it to the source columns reproduces the CSV, and the share of true edges that run from an
      earlier to a later CSV column is below 100%
  D10 swap overlap reported: shared pairs, search nodes and whether the minimum is proved are recorded per family
  D11 scenario is in the test split and not in the dev split; S2 has 10 scenarios, at most one per domain; no S1 family
"""
import argparse
import glob
import hashlib
import io
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CA = ROOT / "external" / "causalarena" / "scm" / "semantic"
SUITE = "suite_q1s2"
ROLES = [("real", 1), ("neutral", 2), ("swapped", 3)]
ROLE_WORDS = ["real", "neutral", "swap", "shuffl", "orig", "true", "fake"]
S1_FAMILIES = ["sachs", "abalone", "autompg", "concrete", "dwd"]
NODE_BUDGET = 2_000_000
SHUFFLE_SALT = "cc-research-s2-shuffle-v1"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def shuffle_perm(scenario, d, E):
    """perm[k] = released column index placed at CSV column k."""
    draws = 0
    while True:
        tag = "%s:%s" % (SHUFFLE_SALT, scenario) + ("" if draws == 0 else ":%d" % draws)
        seed = int(sha(tag.encode())[:16], 16)
        perm = [int(v) for v in np.random.default_rng(seed).permutation(d)]
        draws += 1
        pos = {r: k for k, r in enumerate(perm)}
        if any(pos[c] > pos[e] for c, e in E):
            return perm, draws, tag


def best_derangement(E, p, budget=NODE_BUDGET):
    """As make_suite.best_derangement, plus a node budget. Returns perm, overlap, nodes, proved_minimal."""
    adj = {frozenset(e) for e in E}
    nbr = {k: set() for k in range(p)}
    for (u, v) in E:
        nbr[u].add(v)
        nbr[v].add(u)
    st = {"best": None, "overlap": None, "nodes": 0, "cut": False}

    def dfs(k, perm, used, cost):
        st["nodes"] += 1
        if st["nodes"] > budget:
            st["cut"] = True
            return
        if st["overlap"] is not None and cost >= st["overlap"]:
            return
        if k == p:
            st["best"], st["overlap"] = list(perm), cost
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
            if st["overlap"] == 0 or st["cut"]:
                return

    dfs(0, [], set(), 0)
    return st["best"], st["overlap"], st["nodes"], bool(st["overlap"] == 0 or not st["cut"])


def to_matrix(edges, p):
    """Repo convention: M[e, c] == 1 means c -> e (row = effect)."""
    M = np.zeros((p, p), dtype=int)
    for c, e in edges:
        M[e, c] = 1
    return M


def find_graph_json(domain, scenario):
    for f in sorted(glob.glob(str(CA / "artifacts" / domain / "*" / "graph.json"))):
        g = json.loads(Path(f).read_text(encoding="utf-8"))
        if g.get("scenario_id") == scenario:
            return Path(f), g
    return None, None


def csv_bytes(header, X):
    buf = io.StringIO()
    np.savetxt(buf, X, fmt="%.9g", delimiter=",")
    return (",".join(header) + "\n").encode("utf-8"), buf.getvalue().encode("utf-8")


def build(write):
    splits = json.loads((ROOT / "plans" / "splits.json").read_text(encoding="utf-8"))
    sem = splits["families"]["semantic"]
    scenarios = sem["s2_test_scenarios"]
    out = ROOT / "datasets" / SUITE
    refdir = out / "_reference"
    files = {}
    mapping = {"format": 2, "suite": SUITE, "source": "CausalArena semantic, observational only, replicate 0",
               "split_file_sha256": sha((ROOT / "plans" / "splits.json").read_bytes()),
               "shuffle_salt": SHUFFLE_SALT, "value_format": "%.9g of float32", "arms": {}, "families": {}, "gates": {}}
    srcs = {}
    for s in scenarios:
        hits = sorted(glob.glob(str(CA / "data" / "semantic_obs_only" / ("semantic_*_%s__semantic_obs_only__rep000.npz" % s))))
        if len(hits) != 1:
            raise SystemExit("expected one rep000 file for %s, found %d" % (s, len(hits)))
        srcs[s] = Path(hits[0])
    domains = {}
    for s, f in srcs.items():
        z = np.load(f, allow_pickle=False)
        domains[s] = json.loads(str(z["metadata_json"]))["domain_id"]
    forbidden = set(ROLE_WORDS)
    for s in scenarios:
        forbidden |= {t.lower() for t in re.split(r"[_\W]+", s + "_" + domains[s]) if len(t) >= 4}
    test_set, dev_set = set(sem["test"]), set(sem["dev"])
    all_ok = True
    for idx, s in enumerate(scenarios, start=1):
        f = srcs[s]
        raw = f.read_bytes()
        z = np.load(f, allow_pickle=False)
        meta = json.loads(str(z["metadata_json"]))
        ids = [str(v) for v in z["node_ids"]]
        d = len(ids)
        x = z["x"]
        vals = x[:, :, 0]
        g = (z["g"] != 0).astype(int)
        E = sorted((int(i), int(j)) for i, j in np.argwhere(g != 0))       # (cause, effect), released order
        gates = {}
        gates["D6_reference_and_observational"] = bool(g.shape == (d, d) and len(E) > 0 and int(z["n_int"][0]) == 0
                                                      and not (x[:, :, 1] > 0).any() and vals.shape[1] == d)
        # D8: graph.json and other replicates
        gpath, gj = find_graph_json(meta["domain_id"], s)
        gj_edges = set()
        if gj is not None:
            for e in gj["edges"]:
                gj_edges.add((e["source"], e["target"]))
        npz_named = {(ids[c], ids[e]) for c, e in E}
        reps_same = True
        for r in range(1, 5):
            fr = Path(str(f).replace("rep000", "rep%03d" % r))
            if fr.exists():
                zr = np.load(fr, allow_pickle=False)
                reps_same &= bool(np.array_equal((zr["g"] != 0).astype(int), g)) and [str(v) for v in zr["node_ids"]] == ids
            else:
                reps_same = False
        edge_types = sorted({e.get("edge_type") for e in gj["edges"]}) if gj else []
        # shuffle
        perm, draws, tag = shuffle_perm(s, d, E)
        pos = {r: k for k, r in enumerate(perm)}
        Es = sorted((pos[c], pos[e]) for c, e in E)                         # (cause, effect), CSV order
        names = [ids[r] for r in perm]
        Xs = vals[:, perm]
        share_fwd = sum(1 for c, e in Es if c < e) / len(Es)
        share_fwd_released = sum(1 for c, e in E if c < e) / len(E)
        by_data = to_matrix(Es, d)
        gates["D8_reference_matches_release_and_graph_json"] = bool(
            gj is not None and npz_named == gj_edges and reps_same
            and np.array_equal(by_data, g[np.ix_(perm, perm)].T))
        # swapped labels
        dperm, overlap, nodes, proved = best_derangement(Es, d)
        inv = [dperm.index(k) for k in range(d)]
        by_label = to_matrix([(inv[u], inv[v]) for (u, v) in Es], d)
        labels = {"real": names, "neutral": ["V%02d" % (k + 1) for k in range(d)], "swapped": [names[dperm[k]] for k in range(d)]}
        fam = "s2_%02d" % idx
        refs = {"%s_by_data.npy" % fam: by_data, "%s_swapped_by_label.npy" % fam: by_label}
        for n, M in refs.items():
            b = io.BytesIO()
            np.save(b, M)
            files["_reference/" + n] = b.getvalue()
        codes, d1, d5, d7 = {}, True, True, True
        body0 = None
        for role, rd in ROLES:
            code = "q%02d%d" % (idx, rd)
            codes[role] = code
            hb, body = csv_bytes(labels[role], Xs)
            data = hb + body
            files["%s/%s.csv" % (code, code)] = data
            body0 = body if body0 is None else body0
            d1 &= body == body0
            if role == "real":
                gates["D2_real_header_is_shuffled_ids"] = bool(hb == (",".join(names) + "\n").encode()
                                                               and all(re.fullmatch(r"[A-Za-z0-9_]+", n) for n in ids))
            df = pd.read_csv(io.BytesIO(data))
            d5 &= bool(df.shape == (vals.shape[0], d) and list(df.columns) == labels[role]
                       and np.array_equal(df.values.astype(np.float32), Xs))
            d7 &= not any(w in code.lower() for w in forbidden)
            mapping["arms"][code] = {
                "family": fam, "role": role, "scenario_id": s,
                "dataset_arg": "research:datasets/%s/%s/%s.csv" % (SUITE, code, code),
                "sha256": sha(data), "bytes": len(data), "path_says_name": False,
                "column_labels": labels[role], "data_in_each_column_is_really": names,
                "reference_by_data": "_reference/%s_by_data.npy" % fam,
                "reference_by_label": ("_reference/%s_swapped_by_label.npy" % fam) if role == "swapped" else (
                    None if role == "neutral" else "_reference/%s_by_data.npy" % fam)}
        d7 &= not any(w in fam for w in forbidden)
        shared = len({frozenset(map(int, v)) for v in np.argwhere(by_data == 1)} & {frozenset(map(int, v)) for v in np.argwhere(by_label == 1)})
        dom_count = sum(1 for t in scenarios if domains[t] == domains[s])
        gates.update({
            "D1_bodies_byte_identical": bool(d1),
            "D3_swapped_is_derangement": all(dperm[k] != k for k in range(d)),
            "D4_shared_pairs_match_search": shared == overlap,
            "D5_parsed_values_identical": bool(d5),
            "D7_opaque_names": bool(d7),
            "D9_shuffle_recorded_and_not_topological": bool(np.array_equal(Xs, vals[:, perm]) and share_fwd < 1.0
                                                           and sorted(perm) == list(range(d))),
            "D10_swap_overlap_reported": bool(isinstance(overlap, int) and nodes > 0 and isinstance(proved, bool)),
            "D11_test_split_no_overlap": bool(s in test_set and s not in dev_set and len(scenarios) == 10 and dom_count == 1
                                              and not any(t in s for t in S1_FAMILIES)),
        })
        mapping["families"][fam] = {
            "scenario_id": s, "domain_id": meta["domain_id"], "graph_id": meta.get("graph_id"),
            "scenario_name": meta.get("scenario_name"),
            "source_npz": str(f.relative_to(ROOT)), "source_sha256": sha(raw),
            "graph_json": str(gpath.relative_to(ROOT)) if gpath else None,
            "graph_json_sha256": sha(gpath.read_bytes()) if gpath else None, "graph_json_edge_types": edge_types,
            "rows": int(vals.shape[0]), "variables": d, "edges": len(E),
            "column_order_released": ids, "column_permutation": perm, "shuffle_seed_string": tag, "shuffle_draws": draws,
            "share_edges_earlier_to_later": {"released": share_fwd_released, "csv": share_fwd},
            "columns": names, "arms": codes,
            "reference_edges": ["%s->%s" % (names[c], names[e]) for c, e in Es],
            "swapped_labels_by_column": labels["swapped"],
            "adjacent_pairs_shared_by_the_two_references": shared, "search_nodes_visited": nodes,
            "search_proved_minimal": proved, "gates": gates}
        ok = all(gates.values())
        mapping["gates"][fam] = bool(ok)
        all_ok &= ok
        print("%s %-46s d=%2d n=%d edges=%2d fwd %.2f->%.2f draws=%d shared=%d proved=%s %s" % (
            fam, s, d, vals.shape[0], len(E), share_fwd_released, share_fwd, draws, shared, proved,
            "PASS" if ok else {k: v for k, v in gates.items() if not v}))
    files["MAPPING.json"] = (json.dumps(mapping, indent=2) + "\n").encode("utf-8")
    if write:
        for rel, b in files.items():
            p = out / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b)
    return files, all_ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="rebuild in memory and compare with the files on disk")
    a = ap.parse_args()
    files, ok = build(write=not a.check)
    if a.check:
        out = ROOT / "datasets" / SUITE
        diff = [r for r, b in files.items() if not (out / r).exists() or (out / r).read_bytes() != b]
        print("rebuild identical" if not diff else "DIFFERS: %s" % diff[:10])
        ok &= not diff
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
