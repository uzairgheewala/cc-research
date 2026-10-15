# B2: interventions on the frozen ledger (Q2 build)

Tickets: BLD-03, CAP-03, TGT-06. Bundle B2 of `plans/q2_dag.json`; gates B2.1 and B2.2 of `plans/b2_prereg.json`
(written before any B2 run); landmark ER-C (report only). Frozen kernel `plans/b2_freeze.json` (id e9871399f1b92e7d,
rule C3, the B1 core unchanged). Written 2026-10-15. No model calls.

## Where we are now

Single-target intervention rows now enter the ledger as shift evidence, orient only pairs the data already made
adjacent, and never add or remove a connection. On CausalArena's held-out scenarios D+I is at least as precise as D in
both families (semantic +0.017 pooled DV-1, interval above zero; formula +0.004, interval across zero), and on the
Causal Chambers light tunnel the kernel's committed claims are more precise than GES's (0.926 against 0.916) and agree
with the held-back intervention rows 98.5% of the time, against 94.3% for the true DAG itself. Both gates pass; ER-C is
met.

## Must-show list

| Item | Result | Evidence |
|---|---|---|
| **B2.1** constructed conflicts resolved for the intervention and recorded; V4 and K7 accept every D+I ledger | 100% of constructed conflicts (unit tests); 0 failing ledgers among 500 dev, 500 held-out and 2 Chambers ledgers | `tests/test_q2_interventions.py`; `failing` columns below |
| **B2.2** D+I DV-1 precision >= D, mean per-file difference >= 0, CausalArena test, both families | **pass**: semantic +0.0166, formula +0.0048 | `analysis/results/q2_b2/summary_test.json` |
| **B2.2** Chambers pooled D+I >= D | **pass**: 0.9261 against 0.9250 | `analysis/results/q2_b2/chambers.json` |
| **ER-C** (report) kernel within 0.03 of GES on Chambers | **met**: D +0.009, D+I +0.010 above GES | same |
| Held-out discipline | one logged read each (Chambers 11:02:58Z, semantic 11:03:11Z, formula 11:16:23Z), code hash equal to the freeze | `analysis/results/q2_b2/access_log.jsonl` |

### CausalArena obs_int (125 files per family and split; scenario-cluster 95% intervals, B = 2000)

| Family | Split | D F1 | D+I F1 | F1 difference | D DV-1 (cov.) | D+I DV-1 (cov.) | Pooled DV-1 difference | Mean per-file difference | Oriented + propagated (right) | Conflicts | Failing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| semantic | dev | 0.511 | 0.527 | +0.017 [+0.008, +0.026] | 0.751 (0.836) | 0.759 (0.856) | +0.008 [-0.003, +0.021] | +0.006 | 412 + 44 (358) | 184 | 0 |
| formula | dev | 0.433 | 0.435 | +0.002 [-0.001, +0.006] | 0.802 (0.879) | 0.809 (0.859) | +0.007 [-0.002, +0.020] | +0.005 | 170 + 25 (120) | 216 | 0 |
| semantic | **test** | 0.506 | 0.517 | **+0.012 [+0.005, +0.019]** | 0.760 (0.763) | 0.777 (0.787) | **+0.017 [+0.006, +0.030]** | **+0.017** | 345 + 51 (299) | 146 | 0 |
| formula | **test** | 0.455 | 0.455 | +0.000 [-0.006, +0.005] | 0.824 (0.874) | 0.828 (0.862) | +0.004 [-0.003, +0.011] | **+0.005** | 106 + 6 (70) | 95 | 0 |

(D here is the kernel on the 800 observational rows of each obs_int file, so its numbers differ from B1's, which used
the observational files.)

### Causal Chambers light tunnel (BEN-10 sample; 20 non-constant variables, 11 single-target regimes, 39 true edges kept)

| Row | Committed | Coverage | DV-1 precision | Agreement with check-half rows |
|---|---|---|---|---|
| true DAG | 209 | 1.000 | 1.000 | 0.943 |
| true CPDAG | 207 | 0.990 | 1.000 | 0.942 |
| empty graph | 209 | 1.000 | 0.813 | 0.871 |
| PC maxP (plain call) | 194 | 0.928 | 0.887 | 0.928 |
| GES (BIC) | 203 | 0.971 | 0.916 | 0.975 |
| **kernel D (C3)** | 200 | 0.957 | **0.925** | **0.985** |
| **kernel D+I (C3)** | 203 | 0.971 | **0.926** | **0.985** |

Interventions oriented 21 pairs, none propagated, no conflicts. Both ledgers verify and pass K7.

## Predictions

| Prediction (written before the runs) | Verdict |
|---|---|
| P-B2a D+I raises DV-1 precision over D by 0.00-0.03 per family on test; refuted if any family below 0 | **Supported** (+0.017, +0.005 per file) |
| P-B2b on Chambers kernel D+I within 0.03 of GES or above | **Supported** (+0.010 above) |

## What the numbers do and do not say

- **Agreement above the true DAG's is not a contradiction.** The check rows test "does Y move when T is set"; the true
  DAG includes weak edges whose effect does not reach significance in 50-100 rows, so a graph that leaves some weak
  ancestral claims uncommitted can agree more often than the truth. ER-C is defined on DV-1 precision against the
  released graph for that reason; agreement is reported beside it.
- **Formula interventions orient fewer pairs correctly as true edges (70 of 112 on test, 62.5%) than semantic ones
  (299 of 396, 75.5%), yet D+I DV-1 precision does not fall.** "Right" here means the oriented pair is a true edge in
  that direction. The dev diagnostic (`analysis/results/q2_b2/orientation_diag_dev_<family>.json`, no held-out read)
  classes every intervention orientation:

  | Dev, rule C3 | True edge, right way | Ancestral non-edge | True edge reversed | Unrelated pair | Descendant to ancestor |
  |---|---|---|---|---|---|
  | semantic, oriented directly (412) | 342 | 61 | 3 | 4 | 2 |
  | semantic, propagated by Meek (44) | 16 | 4 | 7 | 11 | 6 |
  | formula, oriented directly (170) | 110 | 33 | 11 | 14 | 2 |
  | formula, propagated by Meek (25) | 10 | 2 | 4 | 6 | 3 |

  There are two classes. The first is a path the data collapsed into an edge: T is an ancestor of Y but not its parent.
  This is the largest wrong class, and it is right as an ancestral (DV-1) claim, which is why DV-1 does not fall. The
  second is a shift-test false positive (reversed, unrelated or backward pairs): rare on semantic (9 of 412) and common on
  formula (27 of 170), where deterministic relations make Welch tests fragile. On top of both, **Meek propagation from
  intervention orientations is right only 36-40% of the time**. Proposals: `docs/design/q2_kernel_v3_proposals.md` K3-3.
- **Coverage moves both ways.** Semantic D+I commits more (0.787 vs 0.763); formula commits slightly less (0.862 vs
  0.874), because conflicting pairs are opened rather than left in the data's direction.

## Follow-ups (proposed)

- K3-3 in `docs/design/q2_kernel_v3_proposals.md`: ancestral claims instead of edges where a path exists, multiplicity
  control on the shift tests, and no Meek propagation from intervention orientations, each tested on dev first.
- Chambers has one sample; a second light-tunnel or wind-tunnel sample would turn ER-C from a report into an interval.

## Where we're going

B3 adds knowledge tiers on the pairs data and interventions leave open (ER-1, ER-4a route B); B4 turns the D+I ledger's
claims into calibrated confidences (ER-2, ER-3).
