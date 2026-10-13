"""Score any method's rows on the B2 name-reliance benchmark (AB-08) against BOTH graphs in each file:
G_D (`g`, the graph the data follow) and G_N (`g_names`, the graph the names suggest).

Input rows are the standard method-row format (baseline_variants_run.py, causalarena_methods.py, b2_reference_methods.py):
per file `file` (the b2 file name), `directed_edges` [[cause, effect], ...] and `undecided_pairs` [[i, j, mark_i, mark_j], ...]
in the file's column indexing, and `method`. Reported per method, per track and per rho:
  f1_data           directed F1 vs G_D; undecided pairs oriented at random, seed crc32(file name) (CausalArena's rule)
  f1_names          directed F1 vs G_N, the same oriented prediction
  name_following    among committed arrows on pairs where the names disagree with the data (the pair's arrow in G_N differs
                    from its arrow in G_D, including absent), the share that are G_N arrows; data_following = share that are
                    G_D arrows; both pooled over files. *_reversed: the same on reversed pairs only (G_N a->b, G_D b->a),
                    where each committed arrow follows exactly one of the two
and per method (all its files, and per track): Spearman(f1_data, rho) over files, the OLS slope of f1_data on rho, and the
Spearman of the per-rho means. Prediction P11: rho_s <= -0.8 for name-readers; near 0 (|rho_s| <= 0.3) for data-only methods.

  python analysis/b2_score.py --data external/b2_namereliance --rows analysis/results/b2/*_rows.json \
      --out analysis/results/b2/b2_reference_scores.json
No model calls. Tickets: AUD-39, STR-02, EVL-02
"""
import argparse, json, os, statistics as st, sys, zlib
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
P11_READER, P11_FLAT = -0.8, 0.3


def ensure_ca(data_root):
    sys.path.insert(0, str(HERE))
    try:
        import causalarena_io  # noqa: F401
    except ImportError:
        sys.path.append(str(Path(data_root).resolve().parents[1] / "analysis"))
    import causalarena_io as CA
    return CA


def file_index(data_root):
    man = json.load(open(Path(data_root) / "MANIFEST.json", encoding="utf-8"))
    return {os.path.basename(rel): rel for rel in man["files"]}, man


def score_row(CA, row, z):
    """Scores for one row given the opened b2 npz z."""
    key = row["file"]
    GD, GN = np.asarray(z["g"]) != 0, np.asarray(z["g_names"]) != 0
    d = GD.shape[0]
    meta = json.loads(str(z["metadata_json"]))
    directed = {(int(e[0]), int(e[1])) for e in row.get("directed_edges", [])}
    und = {frozenset((int(p[0]), int(p[1]))) for p in row.get("undecided_pairs", [])}
    tD, tN = CA.true_edges(GD.astype(int)), CA.true_edges(GN.astype(int))
    seed = zlib.crc32(key.encode())
    sD = CA.directed_scores(directed, und, tD, d, "random", seed=seed)
    sN = CA.directed_scores(directed, und, tN, d, "random", seed=seed)
    cnt = {"dis_arrows": 0, "dis_names": 0, "dis_data": 0, "rev_arrows": 0, "rev_names": 0, "rev_data": 0}
    for a, b in directed:
        if (GD[a, b], GD[b, a]) == (GN[a, b], GN[b, a]):
            continue                                   # names and data agree on this pair
        cnt["dis_arrows"] += 1
        cnt["dis_names"] += int(GN[a, b])
        cnt["dis_data"] += int(GD[a, b])
        if (GN[a, b] and GD[b, a]) or (GN[b, a] and GD[a, b]):
            cnt["rev_arrows"] += 1
            cnt["rev_names"] += int(GN[a, b])
            cnt["rev_data"] += int(GD[a, b])
    return {"file": key, "method": row.get("method"), "rho": float(meta["rho"]), "track": meta["track"], "split": meta["split"],
            "slug": meta["slug"], "replicate": meta["replicate"], "f1_data": sD["f1"], "f1_names": sN["f1"],
            "precision_data": sD["precision"], "recall_data": sD["recall"], "failed": row.get("failed"), **cnt}


def _share(rows, num, den):
    n = sum(r[den] for r in rows)
    return round(sum(r[num] for r in rows) / n, 4) if n else None


def trend(rows):
    rhos = [r["rho"] for r in rows]
    f1 = [r["f1_data"] for r in rows]
    out = {"files": len(rows)}
    if len(set(rhos)) < 2:
        return out
    rs = spearmanr(rhos, f1)
    levels = sorted(set(rhos))
    means = [st.mean(r["f1_data"] for r in rows if r["rho"] == x) for x in levels]
    slope = float(np.polyfit(rhos, f1, 1)[0])
    rho_s = float(rs.correlation) if np.isfinite(rs.correlation) else None
    out.update({"spearman_f1_data_vs_rho": None if rho_s is None else round(rho_s, 4),
                "spearman_p": None if rho_s is None else float(rs.pvalue),
                "spearman_of_rho_means": round(float(spearmanr(levels, means).correlation), 4),
                "ols_slope_f1_data_per_unit_rho": round(slope, 4),
                "p11_pattern": None if rho_s is None else ("name-reader (rho_s <= %.1f)" % P11_READER if rho_s <= P11_READER
                                                           else "data-only (|rho_s| <= %.1f)" % P11_FLAT if abs(rho_s) <= P11_FLAT
                                                           else "intermediate")})
    return out


def summarise(scored):
    out = {}
    for m in sorted({r["method"] for r in scored}):
        R = [r for r in scored if r["method"] == m]
        per = {}
        for track in sorted({r["track"] for r in R}):
            per[track] = {}
            for rho in sorted({r["rho"] for r in R}):
                T = [r for r in R if r["track"] == track and r["rho"] == rho]
                per[track]["%.2f" % rho] = {
                    "files": len(T), "f1_data_mean": round(st.mean(r["f1_data"] for r in T), 4),
                    "f1_data_sd": round(st.pstdev(r["f1_data"] for r in T), 4),
                    "f1_names_mean": round(st.mean(r["f1_names"] for r in T), 4),
                    "name_following": _share(T, "dis_names", "dis_arrows"), "data_following": _share(T, "dis_data", "dis_arrows"),
                    "arrows_on_disagreeing_pairs": sum(r["dis_arrows"] for r in T),
                    "name_following_reversed": _share(T, "rev_names", "rev_arrows"),
                    "data_following_reversed": _share(T, "rev_data", "rev_arrows"),
                    "failed": sum(1 for r in T if r["failed"])}
        out[m] = {"by_track_rho": per, "trend_all": trend(R),
                  "trend_by_track": {t: trend([r for r in R if r["track"] == t]) for t in per}}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="b2 root (holds MANIFEST.json)")
    ap.add_argument("--rows", nargs="+", required=True, help="row files ({header, rows} JSON)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-file", action="store_true", help="also keep every per-file score in the output")
    a = ap.parse_args()
    CA = ensure_ca(a.data)
    idx, man = file_index(a.data)
    scored, missing = [], []
    for rf in a.rows:
        for row in json.load(open(rf, encoding="utf-8"))["rows"]:
            rel = idx.get(row["file"])
            if rel is None:
                missing.append(row["file"])
                continue
            with np.load(Path(a.data) / rel, allow_pickle=False) as z:
                scored.append(score_row(CA, row, z))
    out = {"producer": "analysis/b2_score.py", "tickets": ["AUD-39", "STR-02", "EVL-02"], "row_files": [os.path.basename(r) for r in a.rows],
           "data_generator_sha256": man["generator_sha256"], "rows_scored": len(scored), "rows_missing_file": missing[:20],
           "definitions": __doc__.split("\n\n")[1].strip(), "p11": {"name_reader_max_spearman": P11_READER, "data_only_max_abs_spearman": P11_FLAT},
           "methods": summarise(scored)}
    if a.per_file:
        out["per_file"] = scored
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1, sort_keys=True)
    for m, v in out["methods"].items():
        for track, rr in v["by_track_rho"].items():
            print(m, track, " ".join("%s:%.3f/%.3f" % (k, x["f1_data_mean"], x["f1_names_mean"]) for k, x in rr.items()))
        print(m, "trend", json.dumps(v["trend_all"]))


if __name__ == "__main__":
    main()
