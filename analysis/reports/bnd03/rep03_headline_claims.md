# REP-03: the paper's headline claims and what we can say about each

Paper: arXiv 2504.13263v2. Evidence comes from the research ledger (snapshot 2026-10-09; sections FACTS, LIVE RUNS, OFFLINE EXPERIMENT, BUNDLE 1, INFERENCES) and from the static audits in this bundle (AUD-12, AUD-14, REP-04). **No new measurements were made for this table.**
Labels: **[R]** read in the paper. **[M]** measured (code read). **[L]** ledger measurement. **[I]** interpretation.
Status values: **reproduced**; **not reproducible (+ reason)**; **not attempted**; **contradicted (scope)** where our own measurements point the other way in the setting we tested.

## Cross-cutting reasons why Tables 2-3 cannot be reproduced from the repo

- R-a [L F18] [M] The benchmark data directories are not in the repo: `simulated_data/heavy_benchmarking_v6` (tests/benchmarking_config.py:8) and `simulated_data/copilot_benchmark_v5` (evaluation/benchmarking_integrated_config.py:7).
- R-b [L F17, F19, I1] The integrated benchmark scores `results.converted_graph`, the algorithm output before refinement (evaluation/benchmarking_integrated.py:333-344). `revised_metrics` is never assigned. The refinement stage is therefore not part of what the code scores.
- R-c [M] The scorer orients every non-directed predicted edge, bidirected included, from the ground truth (evaluation/evaluator.py:154-215, default path :285). The same scorer is used for the preliminary benchmark (tests/benchmarking.py:31, 262). [I] F1 for CPDAG/PAG outputs is an oracle-orientation upper bound. This is REP-04 D11.
- R-d [M] The repo's baseline harness uses `gpt-4o-mini` (tests/selection_test.py:21), while the paper names GPT-4o (p.30). REP-04 D23.
- R-e [L] LLM answers vary on byte-identical requests at temperature 0 (F29), and live runs crash 12 of 84 times (F28, F28a). A re-run would not give one fixed number per cell without many repeats.

## Table

| # | Claim (paraphrase; short quote) | Page | Status | Our evidence |
|---|---|---|---|---|
| 1 | Automates "the full pipeline of causal analysis for both tabular and time-series" data, incl. inference and actionable insights. | p.1 | **contradicted (scope)** | [M] The CLI is discovery-only. Effect estimation runs only in the web demo (AUD-12 section 1). The CLI time-series path dereferences a None revised graph (REP-04 D19, code trace). [L] F1. |
| 2 | "supports interactive refinement through natural language". | p.1 | not attempted (live) | [M] Present in the web demo (stage machine, graph edits). The CLI offers only a closing Q&A (REP-04 rows 3, 18). |
| 3 | Integrates "over 20 state-of-the-art" techniques. | p.1, p.2, p.33 | partly verified (static) | [L F6] 27 names / 25 imported / 20 profiles. [M] 6 profiled algorithms are tagged Unavailable to the selector; CORL crashes `program.py`; CALM is not imported (AUD-14 a.1, F1, F7). The inference side adds 5+ estimator families (AUD-12 section 3). |
| 4 | "superior performance compared to existing baselines" / "reliable, scalable, and extensible". | p.1 | **not reproducible** (R-a, R-b, R-d); **contradicted (scope)** for reliability | [L] Live: 12 of 84 runs crashed; the cycle step crashed 9 of 9 times when entered (F28a). Refinement degraded the algorithm's graph (S0 -> S1) in all 12 bundle-1 arms. Final adjacency F1 fell below the algorithm output in 31 of 45 completed bundle-1 runs (neutral names 16/16; N4 inconclusive overall). |
| 5 | Empirically "outperforms standard baselines across multiple tasks and datasets". | p.3 | not reproducible (R-a..R-d) | [L] I1: Table 2 probably measures selection + execution. Our only like-for-like measurement is the offline S0 F1 (wrapper defaults, 8-variable simulations): PC 0.86, GES 0.88, FCI 0.85, DirectLiNGAM 0.76 (ledger OFFLINE EXPERIMENT). It was not scored with the paper's oracle scorer. |
| 6 | Preliminary benchmark: GOLEM and NOTEARS (Linear) excel on linear data; constraint-based methods with RCIT are versatile (Fig. 4-5). | p.18-20 | not attempted | [M] Data absent (R-a). Scoring uses oracle orientation (R-c). [I] R-c would favour CPDAG/PAG methods over DAG methods in these figures; not measured. |
| 7 | Figures 6/12: FGES and GPU PC (Fisher-Z) scale to 100+ variables; runtime curves. | p.19, 23-25 | not attempted | [M] GPU PC lives in `externals/acceleration` (not in our copy). 1200 s timeout (tests/benchmarking.py:201-202). DOM-12 iii. |
| 8 | Time series (Figs. 15-22): pairwise Granger strong; VARLiNGAM alone completes at 100 variables; DYNOTEARS recommended. | p.25-29 | not attempted | [M] Granger wrapper `int()`s column names (AUD-14 F2), so the benchmark presumably used integer-named columns [I]. [L] Q5: time-series wrappers were never run by us. |
| 9 | Table 2, default (p=10, n=1000): CC 0.900 vs PC 0.920, FCI 0.910, GES 0.920, GPT-4o 0.850. | p.30 | not reproducible (R-a..R-d) | [R] In the paper's own table CC is below PC and GES in this row. [L] Our nearest numbers are the offline S0 F1 in row 5. |
| 10 | Table 2, dense (p=0.5): CC 0.780 vs 0.41-0.45 for the baselines. | p.30 | not reproducible | [I] With R-c, a method whose CPDAG keeps more adjacencies gains most in dense graphs; not measured. |
| 11 | Table 2, scale: p=50 0.950; p=100 0.910; p=500 0.860; p=1000, n=10000 0.870, where other methods are N/A. | p.30 | not reproducible | [M] DOM-12 iii: the code's scaling path is GPU PC/CDNOD/LiNGAM (externals) and FGES, chosen by the LLM. [L] The refinement stage would add about p^2/2 LLM pair questions and p(p-1)/2 unconditional KCI tests (F8, F9), but R-b says it was not scored. |
| 12 | Table 2, sample size / noise / mixed types (0.89-0.98). | p.30 | not reproducible | as rows 9-11 |
| 13 | Table 2, data quality: heterogeneous 0.780, measurement error 0.890, missing 0.770. | p.30 | not reproducible | [M] Missing data: the CLI imputes and z-scores all columns (stat_info_functions.py:469-470). |
| 14 | Table 2, compound: Clinical 0.690 (GPT-4o 0.040), Financial 0.650, Social Network (1000 nodes) 0.450 where others are N/A. | p.30, setup p.44-45 | not reproducible | [R] Setups are given only in prose (p.44-45). There are no generator configs in the repo for them [M: data dirs absent]. |
| 15 | Text: GPT-4o "predominantly selects FCI and PC algorithms with KCI", lacking adaptation. | p.30 | not attempted | [L] Causal-Copilot itself (with gpt-4o) chose FCI in every completed bundle-1 run (45/45) and in the sachs golden run. [I] On our real-data suite the system showed the same single-choice behaviour the paper attributes to the baseline. |
| 16 | Table 3, default (p=20, l=5): CC 0.673 vs PCMCI 0.695, DYNOTEARS 0.733. | p.31 | not reproducible | [R] CC is below two baselines in the paper's own table. |
| 17 | Text: "F1=0.182 for p=1000 vs next best 0.121". | p.31 | **internally inconsistent (read)** | [R] Table 3 gives 0.182 for "Very Large (p=100, l=3)". There is no p=1000 row. |
| 18 | Text: with large samples, CC "remains competitive (F1=0.649)". | p.31 | **internally inconsistent (read)** | [R] Table 3 gives 0.668 (n=5000) and 0.623 (n=2000). 0.649 appears in neither row. In both rows CC is the lowest except NTS-NOTEARS. |
| 19 | Table 3, lag (l=20 0.850; l=3 0.869) and noise (0.828 / 0.888) are best. | p.31 | not reproducible | [M] The CLI time-series path is broken at main.py:307 (REP-04 D19). [I] Table 3 cannot have come from the current `main.py` unchanged. |
| 20 | Case study: earthquakes report with DYNOTEARS and PSM (Fig. 23). | p.31-32 | not attempted | [R] The data preview in the figure shows standardised values (e.g. year = -1.866). [M] This is consistent with z-scoring (stat_info_functions.py:469-470). [L] earthquakes has no reference graph in the repo. |
| 21 | Refinement makes the output "accurate, interpretable, and aligned with domain knowledge". | p.7 | **contradicted (scope)** | [L] Offline: the bootstrap step lowered adjacency F1 in 50 of 51 CPDAG/PAG combinations and never raised it. Bundle 1: with real names about 93% of final edges were set by the LLM (I8). With neutral names the final graph is the damaged S1. |
| 22 | Conclusion: the automated approach "outperforms baseline methods". | p.33 | not reproducible | as row 4 |

## Summary

- [L][M] No headline performance number can be reproduced from the repo as released: the data are missing, refinement is not scored, the scorer orients edges from the truth, and the baseline model differs.
- [R] Two time-series sentences on p.31 contradict Table 3 (rows 17, 18).
- [L] Where we did measure (real-data suite, sachs, offline simulations), the refinement stage the paper credits for accuracy lowered the algorithm's adjacency F1 whenever names were uninformative.
