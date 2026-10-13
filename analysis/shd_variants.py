"""REP-06 / BEN-08: which SHD definition reproduces CausalArena's published PC SHD (33.522 on semantic obs-only)?

Recomputes SHD under several common definitions from the stored PC graphs (pc_rows_v2.jsonl, alpha 0.05, the published
configuration); no rerun. Undecided pairs are oriented with the same per-file seed as the F1 calibration where a variant needs a DAG.

  python analysis/shd_variants.py --root external/causalarena --rows analysis/results/causalarena_calibration/pc_rows_v2.jsonl --out analysis/results/shd_variants
"""
import argparse, json, os, statistics as st, sys, zlib, glob
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
import cc_graph  # noqa: E402

PUBLISHED = {"shd": 33.522, "shd_scm_std": 9.355}


def orient_random(directed, undirected, seed):
    rng = np.random.default_rng(seed)
    pred = set(directed)
    for a, b in sorted(tuple(sorted(x)) for x in undirected):
        pred.add((a, b) if rng.integers(2) == 0 else (b, a))
    return pred


def variants(directed, undirected, truth, d, seed):
    dag = orient_random(directed, undirected, seed)
    out = {}
    pairs = [(a, b) for a in range(d) for b in range(a + 1, d)]
    def ptype(edges, und, a, b):
        if frozenset((a, b)) in und: return "u"
        if (a, b) in edges and (b, a) in edges: return "bi"
        if (a, b) in edges: return "ab"
        if (b, a) in edges: return "ba"
        return "none"
    # V0: our scorer: one per unordered pair whose arrows differ, after random orientation
    out["V0_pair_after_random_orientation"] = sum(ptype(dag, set(), a, b) != ptype(truth, set(), a, b) for a, b in pairs)
    # V1: edge-level, reversal counts 2 (|pred xor truth| on directed edges), after random orientation
    out["V1_edge_xor_after_random_orientation"] = len(dag ^ truth)
    # V2: CPDAG output vs true DAG, one per pair whose type differs (undirected vs directed counts 1), no orientation
    und = set(undirected)
    out["V2_pair_cpdag_vs_dag"] = sum(ptype(set(directed), und, a, b) != ptype(truth, set(), a, b) for a, b in pairs)
    # V3: pair-level vs the true CPDAG
    C = cc_graph.cpdag_of(set(truth), d)
    t_dir = {(c, e) for c in range(d) for e in range(d) if C[e, c] == 1 and C[c, e] == 0}
    t_und = {frozenset((a, b)) for a, b in pairs if C[a, b] == 2}
    out["V3_pair_cpdag_vs_true_cpdag"] = sum(ptype(set(directed), und, a, b) != ptype(t_dir, t_und, a, b) for a, b in pairs)
    # V4: skeleton only (missing + extra adjacencies)
    sk_p = {frozenset(e) for e in directed} | und
    sk_t = {frozenset(e) for e in truth}
    out["V4_skeleton_only"] = len(sk_p ^ sk_t)
    # V5: committed directions only (undecided pairs dropped), reversal counts 1: missing + extra + reversed
    sk_c = {frozenset(e) for e in directed}
    rev = sum(1 for (a, b) in directed if (b, a) in truth)
    out["V5_committed_only_reversal1"] = len(sk_c ^ sk_t) + rev
    # V6: undirected predicted edge counted as both directions (edge xor), reversal 2
    both = set(directed) | {(a, b) for x in und for a, b in [tuple(sorted(x)), tuple(sorted(x))[::-1]]}
    out["V6_edge_xor_undirected_as_both"] = len(both ^ truth)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True); ap.add_argument("--rows", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.rows, encoding="utf-8")]
    rows = [r for r in rows if r["alpha"] == 0.05]
    per = {}
    for r in rows:
        f = os.path.join(a.root, "scm", "semantic", "data", "semantic_obs_only", r["file"])
        s = CA.load(f)
        truth = CA.true_edges(s["g"])
        directed = {tuple(e) for e in r["directed_edges"]}
        und = {frozenset(p) for p in r["undirected_pairs"]}
        v = variants(directed, und, truth, r["d"], zlib.crc32(r["file"].encode()))
        assert v["V0_pair_after_random_orientation"] == r["random"]["shd"], (r["file"], v, r["random"]["shd"])
        for k, x in v.items():
            per.setdefault(k, {}).setdefault(r["scenario"], []).append(x)
    se = PUBLISHED["shd_scm_std"] / (50 ** 0.5) * (0.5 ** 0.5)
    tol = 3 * se
    res = {"published": PUBLISHED, "tolerance": round(tol, 2), "files": len(rows), "variants": {}}
    for k, sc in per.items():
        means = [st.mean(v) for v in sc.values()]
        m = st.mean(means)
        res["variants"][k] = {"mean": round(m, 2), "scm_std": round(st.pstdev(means), 2), "within_tolerance": abs(m - PUBLISHED["shd"]) <= tol,
                              "difference": round(m - PUBLISHED["shd"], 2)}
    res["matching"] = sorted(k for k, v in res["variants"].items() if v["within_tolerance"])
    os.makedirs(a.out, exist_ok=True)
    json.dump(res, open(os.path.join(a.out, "shd_variants.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
