# B4: calibrated confidence and the selective view (Q2 build)

Tickets: BLD-05, CAP-07, CAP-08, TGT-12, TGT-18 (proposed). Bundle B4 of `plans/q2_dag.json`; gates B4.1 and B4.2 of
`plans/q2_build_prereg.json` (hashed 14 Oct) and `plans/b4_prereg.json` (written before any B4 run); landmarks ER-2 and
ER-3. Frozen kernel and maps `plans/b4_freeze.json` (id e9871399f1b92e7d, rule C3, B1's core unchanged; four isotonic
maps hashed). Written 2026-10-15. No model calls.

## Where we are now

Every data-only claim now carries a probability: the share of 10 row-resamples that repeat it, mapped through an isotonic
curve fitted on dev and frozen. Calibration beats raw bootstrap frequencies by a wide margin on held-out scenarios
(ECE 0.057 / 0.036 against 0.199 / 0.165 raw, semantic / formula), so **TGT-12 is met**. But the pre-registered gates
are stricter, and one family misses them. Semantic held-out ECE is 0.057 against a gate of 0.05, so **B4.1 fails on
semantic**. B4.2 passes on point estimates. The landmarks use the conservative interval end, and neither is met:
- **ER-2:** the semantic selective view is 0.812 precise, but the lower end is 0.756.
- **ER-3:** the ECE upper ends are 0.097 and 0.076.

Formula alone would meet ER-2: 0.899, lower end 0.854.

The semantic miss is in the safe direction: realised precision is above what was claimed at every threshold.

## Must-show list

| Item | Result | Evidence |
|---|---|---|
| Stability per claim (B = 10 row resamples, seed 20261015), rep000 of every scenario | 25 files per family and split; held-out semantic 1,569 DV-1 claims and 1,019 edge claims; formula 3,119 and 903 | `analysis/results/q2_b4/stab_test_<family>.jsonl` |
| Isotonic maps fitted on all dev files, frozen before the held-out read | 4 maps, sha256 in the freeze | `calibration/map_<family>_<kind>.json`, `plans/b4_freeze.json` |
| Dev quality out of fold (5 folds by scenario) | ECE 0.038 semantic (raw 0.153), 0.022 formula (raw 0.181); half-coverage precision 0.813 / 0.856 | `analysis/results/q2_b4/fit_dev.json` |
| **B4.1** within-family ECE of calibrated DV-1 claims, held out, <= 0.05 | **fail on semantic (0.057)**; pass on formula (0.036) | `analysis/results/q2_b4/evaluate_test.json` |
| **B4.2** realised >= claimed - 0.03 at c/g = 1, 2, 4 | **pass** (points: semantic +0.045, +0.023, +0.000; formula +0.020, +0.024, +0.035) | same |
| TGT-12 calibrated better than raw frequencies, held out | **met**: raw minus calibrated ECE +0.143 [+0.090, +0.166] semantic, +0.129 [+0.081, +0.167] formula | `analysis/results/q2_b4/raw_vs_calibrated_test.json` |
| Held-out discipline | three logged reads (two stability runs, one evaluation), code and maps equal to the freeze | `analysis/results/q2_b4/access_log.jsonl` |

### Held out (test split; scenario-cluster 95% intervals, 25 scenarios per family)

| Family | DV-1 claims (coverage, precision) | Selective view: coverage, precision [CI] | ECE calibrated [CI] | ECE raw | Realised - claimed at c/g = 1 / 2 / 4 [lower ends] |
|---|---|---|---|---|---|
| semantic | 1,569 (0.764, 0.783) | 0.578, **0.812 [0.756, 0.864]** | **0.057** [0.048, 0.097] | 0.199 | +0.045 / +0.023 / +0.000 [-0.002 / -0.033 / -0.060] |
| formula | 3,119 (0.888, 0.834) | 0.615, **0.899 [0.854, 0.939]** | 0.036 [0.017, 0.076] | 0.165 | +0.020 / +0.024 / +0.035 [-0.024 / -0.023 / -0.009] |

Edge-level claims (not gated): calibrated ECE 0.041 semantic and 0.047 formula, against 0.227 and 0.215 raw. No edge
claim reaches probability 0.8 on test, so the c/g = 4 view keeps none.

The selective view keeps claims in order of probability until half of all target-outcome pairs are covered, ties
together (pre-registered). Large ties at one probability level push the cut to 0.58-0.62 coverage.

## Landmarks

| Landmark | Rule | Value | Verdict |
|---|---|---|---|
| ER-2 | lower end > 0.80 at coverage >= 0.5, both families | semantic 0.756, formula 0.854 | **not met** (semantic) |
| ER-3 | ECE upper end <= 0.05 and realised - claimed lower end >= -0.03 at each threshold, both families | ECE upper 0.097 / 0.076; semantic lower ends -0.033 and -0.060 | **not met** |

## Predictions

| Prediction (written before the runs) | Verdict |
|---|---|
| Q-B4a top-50%-coverage view > 0.78 precise on dev, out of fold (refuted < 0.72) | **Supported** (0.813, 0.856) |
| Q-B4b calibrated out-of-fold ECE on dev <= 0.05 (refuted > 0.08) | **Supported** (0.038, 0.022) |

## Why semantic missed

- **The miss comes from the scenarios, not the map.** At the same mean stability (0.648 on dev, 0.633 on test), semantic
  test claims are right more often than dev claims (0.783 against 0.744). A map fitted on 25 dev scenarios under-claims
  on the 25 test scenarios. Most of the ECE is that gap: at the 0.5 threshold, claimed 0.747 and realised 0.792. The
  formula family does not shift that way.
- **25 scenarios make wide intervals.** The design takes one replicate per scenario (changed from two before any run, to
  halve compute; recorded in the pre-registration). The interval is set mostly by between-scenario variance, so more
  replicates would narrow it only a little. ER-2 on semantic needs a point estimate near 0.86, not 0.81.
- **Calibration is far better than raw frequencies either way.** Raw bootstrap shares overstate by 0.13-0.19 ECE (the
  baseline Causal-Copilot's filter uses). The isotonic maps remove most of that.

## What would change it (proposals, not adopted; `docs/design/q2_kernel_v3_proposals.md`)

- Fit the map with scenario-level shrinkage, or report per-scenario calibration as an interval rather than one curve.
- Use B = 20 resamples and a minimum block size, so the top probability levels are not fitted on a handful of claims.
- Add more scenarios: every interval here comes from 25 clusters.

## Where we're going

B5 reads other systems' outputs as claims and takes the ledger to root-cause analysis (ER-4b). The build summary
(`analysis/reports/q2_build_results.md`) sets the landmark table and the routes that remain.
