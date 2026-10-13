# BND-04 results: GES and FCI error budgets, the SHD question, the published GIES row (2026-10-10)

All numbers are **measured** from files named in brackets unless marked. No model calls. Runs: 250 public CausalArena
semantic observational files per method, in the cloud sandbox (2 shards each; logs in `analysis/results/methods/logs/`).
Gate C1 passes (the scorer still reproduces the published PC F1; `pc_calibration.json`). Every row carries its split label.

## 1. Predictions (fixed in `plans/q1_dag.json` before the runs) [`analysis/results/methods/bnd04_verdicts.json`]

| | Prediction | GES | FCI | PC (reference) | Verdict |
|---|---|---|---|---|---|
| Q4a | accuracy of committed directions <= 0.65 for both (refuted if either >= 0.75) | 0.807 | 0.798 | 0.544 | **REFUTED** |
| Q4b | direction errors cost each method >= 0.15 F1 (refuted if any <= 0.05) | 0.117 | 0.228 | 0.276 | **INCONCLUSIVE** |

Reading (interpretation): PC's weak orientation does not generalise. GES and FCI commit fewer directions but get about 80%
of them right. FCI's cost comes from what it leaves undecided (73% of the true adjacencies it finds), not from wrong arrows
(5%). RQ-16 is answered: the error pattern behind the Q4 hypothesis is PC-specific.

## 2. Error budgets [`error_budget_gesbic.json`, `error_budget_fci.json`]

| | skeleton P / R / F1 | of true adjacencies found: right / reversed / undecided | F1 random rule | F1 authors' rule | SHD random / authors' |
|---|---|---|---|---|---|
| GES (`ges` 1.1.0, BIC, log(n)/2) | 0.588 / 0.612 / 0.592 | 0.755 / 0.180 / 0.065 | 0.475 | 0.495 | 37.0 / 36.2 |
| FCI (causal-learn, Fisher-z, 0.05) | 0.698 / 0.457 / 0.550 | 0.212 / 0.054 / 0.734 | 0.322 | 0.521 | 36.0 / 29.2 |

## 3. Failures on deterministic variables

In 5 of the 50 scenarios (all 5 replicates each) the data contain an exactly collinear variable (correlation matrix of rank
d - 1; e.g. heatwave_cooling_center_use_illness). The `ges` package's Gaussian score raises "Singular matrix" and causal-learn's
Fisher-z test inside FCI raises "Data correlation matrix is singular"; PC ran on all 250 files. Failed files are scored as empty
graphs, as the authors' runners do (`except` -> zeros in TabCausal `run_gies.py`). The 5 scenarios: heatwave_cooling_center_use_illness,
injection_molding_cooling_warp, sleep_apnea_device_pressure_adherence, traffic_signal_offset_corridor_delay, wildfire_smoke_shelter_behavior.
One of them (s2_07) is in the Q1 suite S2: the pipeline's tests and scores face the same singularity there.

## 4. The published GIES row [`bnd04_verdicts.json` ges_vs_published_GIES]

Published (semantic obs-only, 100 scenarios): F1 0.552 (std 0.126), SHD 33.404 (std 15.167). Tolerance 3 SE of a 50-of-100 mean.

| | F1 | SHD | within tolerance |
|---|---|---|---|
| all 50, authors' rule | 0.495 | 36.2 | F1 no (gap -0.057), SHD yes |
| 45 without the failing scenarios (post hoc), authors' rule | 0.550 | 35.9 | both (gap -0.002, +2.5) |

Reading (interpretation): with the published score and phases (pcalg GIES via cdt in the authors' code; the `ges` package here,
same score and phases, a different implementation) the row reproduces wherever our implementation runs; the whole gap sits
in the five scenarios where it fails on singular data, which the R implementation evidently handled. The 45-scenario figure
is a post hoc selection and is labelled as such.

## 5. The SHD question (REP-06, BEN-08) [`causalarena_calibration/protocol_check.json`]

From the authors' code (TabCausal commit 6ca7194): SHD counts a reversed edge once (`metrics.py`), which is our pair-level SHD;
undecided CPDAG edges are oriented from the lower column index to the higher ("liberal", `run_pc.py`, `run_gies.py`, README:
"uncertain edges were not randomized"). With that rule our PC SHD is 35.43 (within 2.81 of 33.52) but F1 is 0.396 against
0.333 (outside 0.045); with random orientation F1 matches and SHD does not. No rule reproduces both on the public 50; the
published mean also covers 50 unreleased scenarios. Not settleable from public data. Appendix B of the paper, which the main
text says states the rule, could not be read; our earlier "random" reading is contradicted by the code.

## 6. The order leak, quantified

Every public file lists causes before effects. Under the authors' rule this hands the true direction to every undecided pair
that is truly adjacent: FCI's F1 rises from 0.322 to 0.521, GES's from 0.475 to 0.495, PC's from 0.335 to 0.396. Methods that
leave more pairs undecided gain more. This is the content of EXT-01 (Uzair's decision whether to send it).

## 7. What this changes

- REP-06 and BEN-08 close with a documented reason; RQ-16 closes (Q4a refuted, Q4b inconclusive).
- G1 (16 Oct): the "PC-like error pattern" motivation for refinement must be restated per method; for GES the remaining loss
  is mostly in the skeleton (F1 0.59), not in direction.
- BND-06 should report every method under both rules and flag the leak; the S2 suite already shuffles columns.
