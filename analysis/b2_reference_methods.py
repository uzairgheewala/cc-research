"""Two reference "methods" on the B2 name-reliance benchmark (AB-08), written in the standard row format
(baseline_variants_run.py / causalarena_methods.py: per file `directed_edges` and `undecided_pairs`), so b2_score.py and any
other reader of method rows read them unchanged.

  names_oracle  returns G_N (`g_names`, the graph the names suggest) exactly: a perfect name-reader, no data used.
                Its F1 against the data's graph G_D is 1 - rho by construction.
  pc            PC from upstream causal-learn (--causal-learn PATH, e.g. engines/cl_0.1.4.8), stable, Fisher-z, alpha 0.05,
                default collider rule, on the released (already shuffled) columns: a data-only method; it never sees names.
                Output: a CPDAG (undirected edges are undecided pairs). (GES via the `ges` package was the first choice; it
                took over 2 minutes on one d = 25 file on the shared 2-CPU machine, so PC is used.)

  python analysis/b2_reference_methods.py --method names_oracle --data external/b2_namereliance \
      --split dev --tracks linear nonlinear --reps 1 --out analysis/results/b2/names_oracle_rows.json
  python analysis/b2_reference_methods.py --method pc --causal-learn ../engines/cl_0.1.4.8 --data external/b2_namereliance \
      --split dev --tracks linear --reps 1 --scenarios 6 --out analysis/results/b2/pc_rows.json
--scenarios k takes, from the requested split, the first scenario listed for each of the first k domains in name order
(plans/splits.json dev_by_domain), so the subset is fixed before any result is seen.
No model calls. Tickets: AUD-39, STR-02, EVL-02
"""
import argparse, json, os, sys, time, zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def ensure_ca(data_root):
    sys.path.insert(0, str(HERE))
    try:
        import causalarena_io  # noqa: F401
    except ImportError:
        sys.path.append(str(Path(data_root).resolve().parents[1] / "analysis"))
    import causalarena_io as CA
    return CA


def pick_files(data_root, split, tracks, reps, k_scen):
    man = json.load(open(Path(data_root) / "MANIFEST.json", encoding="utf-8"))
    splits = json.load(open(Path(data_root).resolve().parents[1] / "plans" / "splits.json", encoding="utf-8"))["families"]["semantic"]
    allowed = None
    if k_scen:
        by_dom = splits["%s_by_domain" % split] if "%s_by_domain" % split in splits else None
        if by_dom is None:
            raise SystemExit("no %s_by_domain in splits.json" % split)
        allowed = {by_dom[dom][0] for dom in sorted(by_dom)[:k_scen]}
    out = []
    for rel in sorted(man["files"]):
        track, rtag, name = rel.split("/")
        slug, rep = name[len("b2_%s_%s_" % (track, rtag)):-len(".npz")].split("__rep")
        if track not in tracks or int(rep) >= reps or slug not in splits[split]:
            continue
        if allowed is not None and slug not in allowed:
            continue
        out.append(rel)
    return out, man


def cl_to_graph(M):
    """causal-learn endpoint marks -> committed arrows (i, j) and undecided pairs {(i, j): (mark_i, mark_j)}, i < j
    (the same conversion as baseline_variants_run.to_graph)."""
    d = M.shape[0]
    directed, undecided = set(), {}
    for i in range(d):
        for j in range(i + 1, d):
            a, b = int(M[i, j]), int(M[j, i])
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                directed.add((i, j))
            elif a == 1 and b == -1:
                directed.add((j, i))
            else:
                undecided[(i, j)] = (a, b)
    return directed, undecided


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True, choices=("names_oracle", "pc"))
    ap.add_argument("--causal-learn", default=None, help="pc only: folder holding the causallearn package")
    ap.add_argument("--data", required=True, help="b2 root (holds MANIFEST.json)")
    ap.add_argument("--split", default="dev", choices=("dev", "test"))
    ap.add_argument("--tracks", nargs="+", default=["linear"])
    ap.add_argument("--reps", type=int, default=1, help="use replicates 0..reps-1")
    ap.add_argument("--scenarios", type=int, default=0, help="0 = every scenario of the split")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    CA = ensure_ca(a.data)
    files, man = pick_files(a.data, a.split, a.tracks, a.reps, a.scenarios)
    if a.method == "pc":
        if not a.causal_learn:
            raise SystemExit("--causal-learn PATH is required for --method pc")
        sys.path.insert(0, str(Path(a.causal_learn).resolve()))
        import contextlib, io
        from causallearn.search.ConstraintBased.PC import pc
        engine = "causal-learn PC at %s, stable, fisherz, alpha 0.05, uc_rule 0, uc_priority 2" % Path(a.causal_learn).name
    else:
        engine = "names oracle: returns g_names (G_N)"
    rows = []
    for rel in files:
        key = os.path.basename(rel)
        z = np.load(Path(a.data) / rel, allow_pickle=False)
        meta = json.loads(str(z["metadata_json"]))
        s = CA.load(Path(a.data) / rel)
        d = len(s["node_ids"])
        t0, failed = time.time(), None
        if a.method == "names_oracle":
            directed, undecided = sorted([int(i), int(j)] for i, j in np.argwhere(z["g_names"] != 0)), []
        else:
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    M = pc(s["values"][: s["n_obs"]], 0.05, "fisherz", stable=True, show_progress=False).G.graph
                dset, und_m = cl_to_graph(np.asarray(M))
                directed = sorted([int(i), int(j)] for i, j in dset)
                undecided = sorted([int(i), int(j), int(m[0]), int(m[1])] for (i, j), m in und_m.items())
            except Exception as e:  # noqa: BLE001 - a failed file is data, scored as an empty graph
                directed, undecided, failed = [], [], "%s: %s" % (type(e).__name__, e)
        secs = time.time() - t0
        truth = CA.true_edges(s["g"])
        und = {frozenset(p[:2]) for p in undecided}
        sc = {rule: CA.directed_scores({tuple(e) for e in directed}, und, truth, d, rule, seed=zlib.crc32(key.encode()))
              for rule in ("random", "drop", "both")}
        regime = "D+K" if a.method == "names_oracle" else "D"
        rows.append({"contract": "v1", "ticket": "AUD-39", "family": "b2_namereliance", "scenario": meta["scenario_id"],
                     "file": key, "key": key, "path": rel, "replicate": meta["replicate"], "method": a.method, "regime": regime,
                     "controls": {"columns_shuffled": True, "names": "decoupled (rho dial)", "supplier": "b2 generator",
                                  "knowledge_source": "names oracle (g_names = G_N)" if a.method == "names_oracle" else None},
                     "split": meta["split"], "rho": meta["rho"], "track": meta["track"], "source_slug": meta["slug"],
                     "domain": meta["domain_id"], "d": d, "true_edges": len(truth), "failed": failed, "env": None,
                     "metrics": {"directed_f1": sc["random"]["f1"], "directed_precision": sc["random"]["precision"],
                                 "directed_recall": sc["random"]["recall"], "shd": sc["random"]["shd"], "seconds": round(secs, 2)},
                     "directed_edges": directed, "undecided_pairs": undecided, "scores": sc})
        print("%s %s f1=%.3f %.1fs" % (a.method, key, sc["random"]["f1"], secs), flush=True)
    header = {"method": a.method, "engine": engine, "family": "b2_namereliance", "regime": "D+K" if a.method == "names_oracle" else "D",
              "split": a.split, "tracks": a.tracks, "reps": a.reps, "scenarios": a.scenarios or "all", "files": len(rows),
              "data_manifest_generator_sha256": man["generator_sha256"], "ticket": "AUD-39",
              "scores_note": "scores are against g (G_D) under the random rule, seed crc32(file name); b2_score.py adds G_N"}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump({"header": header, "rows": rows}, f, sort_keys=True)


if __name__ == "__main__":
    main()
