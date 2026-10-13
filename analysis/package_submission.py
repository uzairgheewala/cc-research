"""CAP-17: package our CausalArena method rows in the official submission format (external/causalarena/submission_template)
and run the official validator on every package. Nothing is submitted anywhere.

  python analysis/package_submission.py --rows-dir analysis/results/methods --out analysis/results/submission

One package per method x column order, because the validator rejects duplicate (method, family, graph, regime, repeat) keys
inside one summary.csv and requires every row's method to equal the manifest's method_name:
  analysis/results/submission/<method>__released/   method_name "ccr-<Name>"            (columns in the released order)
  analysis/results/submission/<method>__shuffled/   method_name "ccr-<Name>-colshuffled" (control: per-file column permutation,
                                                     seed 20261010 + crc32(file name); graph mapped back before scoring)
Each package: manifest.json (template fields plus regime, controls, orientation rule, nSHD definition, row sources),
summary.csv (one row per released file), predictions/<family>__<graph_key>__obs__rep<k>.npz with score_matrix (float32, equal to
the adjacency: these methods give no edge scores), adjacency (uint8, directed, release node order), node_order, and the
method's own output as committed (uint8, committed arrows) and undecided (uint8, symmetric, pairs left undecided).

Row sources, per family, whichever exist under --rows-dir (missing ones are listed in the manifest):
  semantic  <m>_semantic_obs_rel.json (gesbic, fci: <m>_semantic_obs.json from BND-04) and <m>_semantic_obs_shuf.json
  formula   <m>_formula_obs_rel.json / <m>_formula_obs_shuf.json
  synthetic <m>_synthetic100_rel.json / <m>_synthetic100_shuf.json   (the 100-file public sample)
Metrics are the scoreboard rule: undecided pairs oriented at random with the per-file seed crc32(file name) (CausalArena
Appendix B.2/B.4; causalarena_io.directed_scores rule "random"). The adjacency written to the .npz is rebuilt with that same
generator and checked against the stored F1 and SHD of every row (the script stops on any mismatch).
SHD is ours (one per unordered pair whose predicted arrows differ, REP-06); nshd = shd / (d (d - 1) / 2), our definition (the
template does not define it). Failed files: status "timeout" (TimeoutError from --file-timeout-s) or "failed"; their graph
metrics are left blank as the summary schema allows (our own family means score them as empty graphs).
"""
import argparse
import csv
import datetime
import json
import re
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
from causalarena_load import load_any  # noqa: E402

CAROOT = ROOT / "external" / "causalarena"
METHODS = {
    "pc": ("PC", "Graphical search", "causal-learn 0.1.3.8 as vendored in Causal-Copilot (externals/causal-learn): PC, stable=True, "
           "Fisher-z, alpha 0.05 (n_jobs default 4). Note: that vendored skeleton step falls back to a KCI test when Fisher-z raises "
           "ValueError (singular correlation matrix).", "causal-learn: MIT"),
    "gesbic": ("GES", "Graphical search", "ges 1.1.0 (Gamella) fit_bic on z-scored columns: Gaussian l0-penalised likelihood, "
               "lambda = log(n)/2, forward/backward/turning phases (the score of the published GIES row on observational files)",
               "ges: BSD 3-Clause"),
    "fci": ("FCI", "Graphical search", "causal-learn 0.1.3.8 (Causal-Copilot vendored) FCI, Fisher-z, alpha 0.05; PAG: tail->arrowhead "
            "committed, o->, o-o, <-> undecided", "causal-learn: MIT"),
    "lingam": ("DirectLiNGAM", "Functional assumptions", "causal-learn 0.1.3.8 DirectLiNGAM, random_state 0, edges |B| >= 0.5",
               "causal-learn: MIT"),
    "notears": ("NOTEARS", "Continuous optimization", "linear NOTEARS re-implemented in analysis/notears_linear.py after "
                "xunzheng/notears linear.py (Apache-2.0): lambda1 0.1, l2 loss, max_iter 100, h_tol 1e-8, edges |W| >= 0.5",
                "re-implementation of Apache-2.0 reference code"),
}
FAMILY_SRC = {
    "semantic": ("semantic/data/semantic_obs_only", lambda m, o: (["%s_semantic_obs_rel.json" % m, "%s_semantic_obs.json" % m]
                                                                 if o == "rel" else ["%s_semantic_obs_shuf.json" % m])),
    "formula": ("formula/data/formula_obs_only", lambda m, o: ["%s_formula_obs_%s.json" % (m, o)]),
    "synthetic": ("synthetic/data/synthetic_obs_only", lambda m, o: ["%s_synthetic100_%s.json" % (m, o)]),
}


def random_rule_adjacency(directed, undecided, d, seed):
    """Same generator and pair order as causalarena_io.directed_scores(rule="random")."""
    pred = set(directed)
    rng = np.random.default_rng(seed)
    for a, b in sorted(tuple(sorted(x)) for x in undecided):
        pred.add((a, b) if rng.integers(2) == 0 else (b, a))
    A = np.zeros((d, d), dtype=np.uint8)
    for i, j in pred:
        A[i, j] = 1
    return A, pred


def package(rows_dir, out_root, method, order, date):
    name, fam_label, config, lic = METHODS[method]
    mname = "ccr-%s" % name if order == "rel" else "ccr-%s-colshuffled" % name
    pkg = out_root / ("%s__%s" % (method, "released" if order == "rel" else "shuffled"))
    if pkg.exists():
        shutil.rmtree(pkg)
    (pkg / "predictions").mkdir(parents=True)
    summary, sources, missing, timeouts = [], {}, [], set()
    for fam, (sub, names) in FAMILY_SRC.items():
        src = next((rows_dir / n for n in names(method, order) if (rows_dir / n).exists()), None)
        if src is None:
            missing.append({"family": fam, "looked_for": names(method, order)})
            continue
        data = json.loads(src.read_text(encoding="utf-8"))
        sources[fam] = {"file": str(src.relative_to(ROOT)), "rows": len(data["rows"]),
                        "file_timeout_s": data["header"].get("file_timeout_s"), "shuffle_seed": data["header"].get("shuffle_seed"),
                        "env": data["header"].get("env")}
        if (order == "shuf") != (data["header"].get("shuffle_seed") is not None):
            raise SystemExit("%s: header shuffle_seed %r does not match order %s" % (src, data["header"].get("shuffle_seed"), order))
        if data["header"].get("file_timeout_s"):
            timeouts.add(data["header"]["file_timeout_s"])
        for r in data["rows"]:
            s = load_any(CAROOT / "scm" / sub / r["file"])
            d = len(s["node_ids"])
            directed = {tuple(e) for e in r["directed_edges"]}
            und = {frozenset(p[:2]) for p in r["undecided_pairs"]}
            seed = zlib.crc32(r["file"].encode())
            A, pred = random_rule_adjacency(directed, und, d, seed)
            sc = CA.directed_scores(directed, und, CA.true_edges(s["g"]), d, "random", seed=seed)
            ref = r["scores"]["random"]
            if abs(sc["f1"] - ref["f1"]) > 1e-12 or sc["shd"] != ref["shd"]:
                raise SystemExit("%s %s: rescored F1/SHD %s/%s differ from stored %s/%s" % (src.name, r["file"], sc["f1"], sc["shd"], ref["f1"], ref["shd"]))
            rep = int(re.search(r"rep(\d+)", r["file"]).group(1))
            failed = r.get("failed")
            status = "ok" if not failed else ("timeout" if failed.startswith("TimeoutError") else "failed")
            pfile = ""
            if status == "ok":
                C = np.zeros((d, d), dtype=np.uint8)
                for i, j in directed:
                    C[i, j] = 1
                U = np.zeros((d, d), dtype=np.uint8)
                for p in und:
                    i, j = tuple(p)
                    U[i, j] = U[j, i] = 1
                pfile = "predictions/%s__%s__obs__rep%d.npz" % (fam, r["scenario"], rep)
                np.savez_compressed(pkg / pfile, score_matrix=A.astype(np.float32), adjacency=A,
                                    node_order=np.array(s["node_ids"]), committed=C, undecided=U)
            met = (lambda v: "" if status != "ok" else v)
            summary.append({"method": mname, "benchmark_family": fam, "graph_key": r["scenario"], "regime": "obs", "repeat": rep,
                            "f1": met("%.6f" % ref["f1"]), "precision": met("%.6f" % ref["precision"]),
                            "recall": met("%.6f" % ref["recall"]), "shd": met(ref["shd"]),
                            "nshd": met("%.6f" % (ref["shd"] / (d * (d - 1) / 2))), "sid": "", "auroc": "", "ap": "",
                            "runtime_sec": r["metrics"]["seconds"], "status": status, "prediction_file": pfile,
                            "timeout_sec": data["header"].get("file_timeout_s") or "",
                            "config_note": ("columns %s; undecided pairs random (seed crc32(file))" % ("released" if order == "rel" else "shuffled (seed 20261010+crc32(file))"))
                                           + ("" if status == "ok" else "; %s: %s; scored as empty graph in our family means" % (status, failed[:80].replace(",", ";")))})
    cols = ["method", "benchmark_family", "graph_key", "regime", "repeat", "f1", "precision", "recall", "shd", "nshd", "sid", "auroc",
            "ap", "runtime_sec", "status", "prediction_file", "timeout_sec", "config_note"]
    with open(pkg / "summary.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(summary)
    manifest = {
        "method_name": mname, "method_family": fam_label, "version": "cc-research BND-06 (%s)" % date,
        "implementation_url": "analysis/causalarena_methods.py --method %s (cc-research repository, UCSD DSC 180 capstone; not public)" % method,
        "checkpoint_url": "N/A", "license": lic, "contact": "to be filled in before any submission",
        "parameter_count": "N/A",
        "training_disclosure": "N/A: classical method, no training or pretraining; no CausalArena SCMs, samples, metadata or generators used "
                               "for tuning (all settings are the published defaults fixed before the runs)",
        "supported_regimes": ["obs"], "supported_families": sorted(sources),
        "result_files": {"summary_csv": "summary.csv", "predictions_dir": "predictions"},
        "evaluation": {"dataset_release": "CausalArena public release sample files (external/causalarena/scm/*/data/*_obs_only)",
                       "protocol_version": "v1", "date": date,
                       "hardware": "cloud VM, 2 CPU cores, 7 GB RAM, no GPU",
                       "timeout_sec": max(timeouts) if timeouts else 0,
                       "notes": "rows from causalarena_methods.py --method %s --family <family> [--file-list plans/synth_sample_100.txt] "
                                "--file-timeout-s <t>%s; per-family timeouts in row_sources" % (method, " --shuffle-seed 20261010" if order == "shuf" else "")},
        "config": config,
        "regime": "D: observational data only (obs-only files; no interventions, no variable names, no knowledge)",
        "controls": {"columns": "released" if order == "rel" else "shuffled",
                     "columns_shuffled": order != "rel",
                     "shuffle": None if order == "rel" else "per-file permutation default_rng(20261010 + crc32(file name)); the graph is mapped back to the released node order before scoring and before writing predictions",
                     "names": "not applicable", "supplier": "causalarena",
                     "released_order_note": "the released column order is topological in the public files (column_order_check.json); a method that reads column order can benefit from it"},
        "orientation_rule": "undecided pairs (CPDAG undirected, PAG o->, o-o, <->, LiNGAM/NOTEARS 2-cycles) oriented at random with seed crc32(file name) (CausalArena Appendix B.2/B.4); adjacency in predictions/*.npz is that oriented graph",
        "shd_variant": "one per unordered pair whose predicted arrows differ from the true arrow(s) (REP-06)",
        "nshd_definition": "shd / (d (d - 1) / 2), ours; not taken from CausalArena",
        "failed_rows": {"timeout": sum(1 for x in summary if x["status"] == "timeout"), "failed": sum(1 for x in summary if x["status"] == "failed"),
                        "note": "metrics left blank as the summary schema allows; our family means score them as empty graphs"},
        "row_sources": sources, "families_missing": missing,
        "tickets": ["CAP-17", "BND-06", "REP-07", "BEN-07", "BEN-11"],
        "submitted": False,
    }
    (pkg / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return pkg, len(summary), manifest["failed_rows"], missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows-dir", default=str(ROOT / "analysis" / "results" / "methods"))
    ap.add_argument("--out", default=str(ROOT / "analysis" / "results" / "submission"))
    ap.add_argument("--methods", default="pc,gesbic,fci,lingam,notears")
    a = ap.parse_args()
    out_root, rows_dir = Path(a.out), Path(a.rows_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    date = datetime.date.today().isoformat()
    log = ["CAP-17 validator run %s (python %s, %s)" % (datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                                                      sys.version.split()[0], "external/causalarena/tools/validate_submission.py"), ""]
    index = []
    for m in a.methods.split(","):
        for order in ("rel", "shuf"):
            pkg, n, failed, missing = package(rows_dir, out_root, m, order, date)
            if n == 0:
                shutil.rmtree(pkg)
                log += ["== %s %s: no row files found; no package (looked for %s)" % (m, order, missing), ""]
                index.append({"package": pkg.name, "rows": 0, "validator_exit": None})
                continue
            cmd = [sys.executable, str(CAROOT / "tools" / "validate_submission.py"), str(pkg)]
            p = subprocess.run(cmd, capture_output=True, text=True)
            log += ["== $ python external/causalarena/tools/validate_submission.py %s" % pkg.relative_to(ROOT),
                    "rows %d, failed rows %s, families missing %s" % (n, failed, [x["family"] for x in missing]),
                    "-- stdout --", p.stdout.rstrip(), "-- stderr --", p.stderr.rstrip(), "exit code %d" % p.returncode, ""]
            index.append({"package": pkg.name, "rows": n, "failed_rows": failed, "families_missing": [x["family"] for x in missing],
                          "validator_exit": p.returncode})
            print(pkg.name, n, failed, "validator exit", p.returncode)
    (out_root / "validator_output.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    (out_root / "packages.json").write_text(json.dumps(index, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
