"""Across-seed robustness of the bootstrap-step effect.   python refinement_offline_seeds.py OUT_DIR CELLS_DIR [CELLS_DIR ...]

A seed here fixes the Python/numpy RNG used by the bootstrap resampling (and by any randomised
algorithm). The datasets are the same for every seed, so the spread across seeds is resampling
noise of the 20-resample bootstrap; the spread across datasets is in the main report.

Gate S1: every (dataset, algorithm) kept in the comparison has a completed cell for every seed.
Gate S2: S0 is identical across seeds for algorithms that are deterministic given the data
         (reported per algorithm; a FALSE is a finding about the algorithm, not a failure).
"""
import glob
import json
import os
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

out_dir = Path(sys.argv[1])
out_dir.mkdir(parents=True, exist_ok=True)
cells = []
for d in sys.argv[2:]:
    cells += [json.load(open(f)) for f in sorted(glob.glob(os.path.join(d, "*.json")))]
ok = [c for c in cells if c["status"] == "ok"]
seeds = sorted({c["seed"] for c in ok})
by = defaultdict(dict)
for c in ok:
    by[(c["dataset"], c["algo"])][c["seed"]] = c
full = {k: v for k, v in by.items() if all(s in v for s in seeds)}
algos = sorted({k[1] for k in full})
gate_s1 = all(len(v) == len(seeds) for v in full.values())


def ms(xs):
    return "%.2f ± %.2f" % (st.mean(xs), st.pstdev(xs)) if xs else "n/a"


L = ["# Offline refinement experiment across seeds %s" % ", ".join(str(s) for s in seeds), "",
     "%d (dataset, algorithm) combinations have a completed cell for every seed; %d completed cells in total were read." % (len(full), len(ok)),
     "A seed fixes the random numbers used by the 20 bootstrap resamples. The datasets do not change with the seed.", "",
     "Gate S1 (every compared combination complete for every seed): %s" % ("PASS" if gate_s1 else "FAIL"), ""]

L += ["## 1. Survival of algorithm-output edges through the bootstrap step, per seed", "",
      "| Edge type in S0 | " + " | ".join("seed %d" % s for s in seeds) + " |", "|---|" + "---|" * len(seeds)]
pool = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for (ds, al), v in full.items():
    for s, c in v.items():
        for t, d in c["S0_edges_by_type_and_survival"].items():
            pool[t][s][0] += d["n"]
            pool[t][s][1] += d["survive_bootstrap_step"]
summary = {"seeds": seeds, "n_combinations": len(full), "survival": {}, "per_algorithm": {}}
for t in sorted(pool, key=lambda t: -pool[t][seeds[0]][0]):
    row = []
    for s in seeds:
        n, k = pool[t][s]
        row.append("%d/%d (%.0f%%)" % (k, n, 100.0 * k / n) if n else "0/0")
    summary["survival"][t] = {str(s): pool[t][s] for s in seeds}
    L.append("| %s | %s |" % (t, " | ".join(row)))

L += ["", "## 2. Adjacency F1 before and after the bootstrap step, per algorithm", "",
      "Mean over datasets within a seed, then mean ± spread (population s.d.) of those means across seeds. "
      "\"Worse in every seed\" counts datasets where S1 scored below S0 for all seeds; \"better in any seed\" counts datasets where S1 scored above S0 at least once.", "",
      "| Algorithm | Datasets | adj F1 S0 | adj F1 S1 | Worse in every seed | Worse in some seeds | Better in any seed | S0 identical across seeds |", "|---|---|---|---|---|---|---|---|"]
for al in algos:
    ks = [k for k in full if k[1] == al]
    f0 = [st.mean((full[k][s]["score_S0"]["adj_f1"] or 0.0) for k in ks) for s in seeds]
    f1 = [st.mean((full[k][s]["score_S1"]["adj_f1"] or 0.0) for k in ks) for s in seeds]
    d = lambda k, s: (full[k][s]["score_S1"]["adj_f1"] or 0.0) - (full[k][s]["score_S0"]["adj_f1"] or 0.0)
    worse_all = sum(all(d(k, s) < -1e-9 for s in seeds) for k in ks)
    worse_some = sum(any(d(k, s) < -1e-9 for s in seeds) and not all(d(k, s) < -1e-9 for s in seeds) for k in ks)
    better_any = sum(any(d(k, s) > 1e-9 for s in seeds) for k in ks)
    same_s0 = sum(all(full[k][s]["S0"] == full[k][seeds[0]]["S0"] for s in seeds) for k in ks)
    summary["per_algorithm"][al] = {"datasets": len(ks), "adj_f1_S0_by_seed": f0, "adj_f1_S1_by_seed": f1,
                                    "worse_all_seeds": worse_all, "worse_some_seeds": worse_some, "better_any_seed": better_any,
                                    "S0_identical_across_seeds": same_s0}
    L.append("| %s | %d | %s | %s | %d | %d | %d | %d of %d |" % (al, len(ks), ms(f0), ms(f1), worse_all, worse_some, better_any, same_s0, len(ks)))

L += ["", "## 3. How much the bootstrap-step result itself moves between seeds", "",
      "For each (dataset, algorithm): the number of adjacencies in S1 under each seed. A row is listed when the seeds disagree.", "",
      "| Dataset | Algorithm | S0 adjacencies | S1 adjacencies by seed |", "|---|---|---|---|"]
moved = 0
for k in sorted(full):
    s1 = [full[k][s]["S1_adjacencies"] for s in seeds]
    if len(set(s1)) > 1:
        moved += 1
        L.append("| %s | %s | %s | %s |" % (k[0], k[1], "/".join(str(full[k][s]["S0_adjacencies"]) for s in seeds), " / ".join(str(x) for x in s1)))
L += ["", "%d of %d combinations give a different number of surviving adjacencies depending on the seed." % (moved, len(full)), ""]
summary["combinations_where_S1_adjacency_count_depends_on_seed"] = moved
allq = all(c["pairs_queued_for_llm_review"] == c["pairs_total"] and c["self_pairs_queued"] == c["p"] for v in full.values() for c in v.values())
L += ["## 4. LLM review queue", "", "Every pair and every self-pair queued for LLM review in every cell and seed: %s." % ("TRUE" if allq else "FALSE"), ""]
summary["all_pairs_queued_every_cell"] = allq
summary["gate_S1"] = gate_s1
(out_dir / "refinement_offline_seeds.md").write_text("\n".join(L), encoding="utf-8")
json.dump(summary, open(out_dir / "refinement_offline_seeds_summary.json", "w"), indent=1)
print("\n".join(L))
