"""Scorer calibration: run plain PC on CausalArena's public semantic files and compare with the published PC row.

Published configuration (arXiv 2609.11897v1, Appendix B.4): stable PC, Fisher-z tests, alpha 0.05; undirected CPDAG
edges "randomly oriented with a fixed per-file seed" before directed-edge F1 and SHD are computed. Rule "random"
below does that (their seeds are not published, so single files differ; means over files should agree).
The other rules are a sensitivity table; --sensitivity adds alpha 0.01 (an earlier pass at alpha 0.01 without
stored graphs is kept in pc_rows.jsonl).

No LLM. Resumable: results are appended to a JSONL file and finished (file, alpha) pairs are skipped.
  python causalarena_pc_calibration.py --root external/causalarena --out analysis/results/causalarena_calibration --budget-s 150
  python causalarena_pc_calibration.py ... --report
"""
import argparse
import glob
import json
import os
import statistics as st
import sys
import zlib
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402

PUBLISHED = {"f1": 0.333, "f1_scm_std": 0.150, "shd": 33.522, "shd_scm_std": 9.355, "scenarios": 100}
RULES = ("random", "drop", "both", "lower")
OFFICIAL = (0.05, "random")


def run_pc(values, alpha):
    from causallearn.search.ConstraintBased.PC import pc
    cg = pc(values, alpha=alpha, indep_test="fisherz", stable=True, show_progress=False)
    A = cg.G.graph                      # causal-learn: A[i, j] == -1 and A[j, i] == 1 means i -> j
    d = A.shape[0]
    directed, undirected = set(), set()
    for i in range(d):
        for j in range(i + 1, d):
            if A[i, j] == 0 and A[j, i] == 0:
                continue
            if A[i, j] == -1 and A[j, i] == 1:
                directed.add((i, j))
            elif A[i, j] == 1 and A[j, i] == -1:
                directed.add((j, i))
            else:
                undirected.add(frozenset((i, j)))
    return directed, undirected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--repo", default=os.path.expanduser("~/cc"))
    ap.add_argument("--budget-s", type=float, default=150)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--sensitivity", action="store_true", help="also run alpha 0.01 (not the published configuration)")
    a = ap.parse_args()
    ALPHAS = (0.05, 0.01) if a.sensitivity else (0.05,)
    os.makedirs(a.out, exist_ok=True)
    res_f = os.path.join(a.out, "pc_rows_v2.jsonl")        # v2 rows also store the graph, so new rules need no rerun
    done = {}
    if os.path.exists(res_f):
        for line in open(res_f, encoding="utf-8"):
            r = json.loads(line)
            done[(r["file"], r["alpha"])] = r
    files = sorted(glob.glob(os.path.join(a.root, "scm", "semantic", "data", "semantic_obs_only", "*.npz")))
    if not a.report:
        sys.path[:0] = [os.path.join(a.repo, "externals", "causal-learn")]
        t0 = time.time()
        with open(res_f, "a", encoding="utf-8") as fh:
            for alpha in ALPHAS:
                for f in files:
                    key = (os.path.basename(f), alpha)
                    if key in done:
                        continue
                    if time.time() - t0 > a.budget_s:
                        print("budget reached; %d of %d done" % (len(done), len(files) * len(ALPHAS)))
                        return
                    s = CA.load(f)
                    t1 = time.time()
                    directed, undirected = run_pc(s["values"], alpha)
                    truth = CA.true_edges(s["g"])
                    row = {"file": key[0], "alpha": alpha, "scenario": s["meta"]["scenario_id"], "domain": s["meta"]["domain_id"],
                           "d": len(s["node_ids"]), "true_edges": len(truth), "directed": len(directed),
                           "undirected": len(undirected), "seconds": round(time.time() - t1, 2),
                           "directed_edges": sorted(directed), "undirected_pairs": sorted(sorted(x) for x in undirected)}
                    for rule in RULES:
                        row[rule] = CA.directed_scores(directed, undirected, truth, len(s["node_ids"]), rule,
                                                       seed=zlib.crc32(key[0].encode()))
                    fh.write(json.dumps(row) + "\n")
                    fh.flush()
                    done[key] = row
        print("all done: %d" % len(done))
    # report
    out = {"published_pc_semantic_obs_only": PUBLISHED, "files": len(files), "rows": len(done), "configs": []}
    # tolerance: three standard errors of a mean over 50 scenarios drawn without replacement from 100
    se = lambda sd: sd / (50 ** 0.5) * (0.5 ** 0.5)
    tol_f1, tol_shd = 3 * se(PUBLISHED["f1_scm_std"]), 3 * se(PUBLISHED["shd_scm_std"])
    for alpha in ALPHAS:
        rows = [r for (f, al), r in done.items() if al == alpha]
        if not rows:
            continue
        for rule in RULES:
            per = {}
            for r in rows:
                per.setdefault(r["scenario"], []).append(r[rule])
            f1 = [st.mean(x["f1"] for x in v) for v in per.values()]
            shd = [st.mean(x["shd"] for x in v) for v in per.values()]
            c = {"alpha": alpha, "undecided_pairs_rule": rule, "scenarios": len(per), "rows": len(rows),
                 "f1_mean": round(st.mean(f1), 3), "f1_scm_std": round(st.pstdev(f1), 3),
                 "shd_mean": round(st.mean(shd), 2), "shd_scm_std": round(st.pstdev(shd), 2)}
            c["official_configuration"] = (alpha, rule) == OFFICIAL
            c["f1_within_tolerance"] = abs(c["f1_mean"] - PUBLISHED["f1"]) <= tol_f1
            c["shd_within_tolerance"] = abs(c["shd_mean"] - PUBLISHED["shd"]) <= tol_shd
            out["configs"].append(c)
    out["tolerance"] = {"f1": round(tol_f1, 3), "shd": round(tol_shd, 2),
                        "how": "3 standard errors of a 50-scenario mean drawn without replacement from the 100 published scenarios"}
    out["complete"] = len(done) == len(files) * len(ALPHAS)
    off = [c for c in out["configs"] if c["official_configuration"]]
    out["gate_C1_official_configuration_reproduces_published_F1"] = bool(off and out["complete"] and off[0]["f1_within_tolerance"])
    out["gate_C2_official_configuration_reproduces_published_SHD"] = bool(off and out["complete"] and off[0]["shd_within_tolerance"])
    json.dump(out, open(os.path.join(a.out, "pc_calibration.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(out["tolerance"]))
    for c in out["configs"]:
        print(c)


if __name__ == "__main__":
    main()
