# Kernel v3 on dev: link recovery, the floor, decision weights, and what actually moved (K1–K4)

Bundles K1–K4 of `docs/design/q2_kernel_v3_design.md`, measured on the dev split through the K0 experiment loop.
Written 2026-10-15. No model calls. No test split read.

## Where we are now

Every lever in the design was built and measured on dev in one session, because each experiment now takes seconds.

- **Most of the planned link levers failed their gates, and we now know why.**
- **The floor is measured.** The semantic family misses 32% of true links. Of those, 9% of all true links have no
  usable signal at all; 14% are a search gap the available tests cannot close without losing more precision than
  they gain.
- **Three things moved the numbers:**
  - pooling a scenario's five replicates (5,000 rows), which cuts misses by 5–8 points and raises answer precision;
  - not acting on the weakest class of directions (Meek rule 1);
  - a confidence model on ledger features.

Together they bring the precision landmark within reach on dev for the pooled regime. They are pre-registered as
kernel v3 (`plans/v3_prereg.json`).

## 1. Missed links: what the levers did

Semantic dev, 125 files, v2 kernel (rule C3): link recall 0.678, link precision 0.631, missed share 0.322.

| Lever (design item) | Links recovered (right) | Precision of recovered | Net effect | Verdict |
|---|---|---|---|---|
| E1+E2 test battery (Fisher z, rank z, residual chi-square), ledger neighbourhoods + full set | 833 (277) | **0.33** | recall 0.678 → 0.732, precision 0.631 → 0.592 | fails the precision gate |
| same, separating sets drawn from the dependence pool (30 files) | 263 (90) | 0.34 | | fails |
| nonparametric cell-mean residual test, dependence pool (30 files) | 172 (59) | 0.34 | | fails |
| cross-fitted boosting residuals on all other variables, to upgrade a recovery (30 files) | 141 (60) | 0.43 | | fails |
| GES penalty halved (λ 0.5) | misses 0.322 → 0.277 | link precision 0.631 → **0.493** | directed F1 0.522 → 0.466, DV-1 0.756 → 0.695 | fails |
| link audit (cut a link the battery separates), common neighbours (30 files) | cuts 111: 74 false, 37 true | | link F1 unchanged | neutral |
| **pooled replicates (5,000 rows), regime D×R** | misses 0.322 → **0.237** | link precision 0.631 → 0.597 | directed F1 0.522 → 0.551, DV-1 precision 0.756 → **0.816** | the only lever that helps |

Formula, pooled: misses 0.336 → 0.284, F1 0.440 → 0.476, DV-1 0.814 → 0.831.

**Why the tests fail: two diagnoses.**

- **The false recoveries are shadows, not noise.** 84% of them are pairs where one variable causes the other through a
  mediator. As a claim "X and Y are causally connected, direction and directness open" they are 85–89% right.
- **No available test separates a shadow from a weak direct link at 1,000 rows on these mechanisms.** Handed the true
  parents of the descendant (which do separate the pair in the true graph), the nonparametric tests still call
  the pair dependent: cell-mean residuals 94%, cross-fitted boosting 81%. The Gaussian linear test, which is
  calibrated (10%), lacks power. Residualising on three or more parents with interacting, formula-like mechanisms
  leaves dependence behind. So a nonlinear test "recovers" a mediated path as a link.

## 2. The floor, measured

For every link v2 misses, an oracle test is handed the right conditioning set: the child's other true parents.
(`analysis/q2_floor.py`, `analysis/results/q2_v3/floor_dev_<family>.json`.)

| Class of missed link | Semantic: share of true links (of misses) | Formula | What it means |
|---|---|---|---|
| **floor**: no oracle test detects it at 1,000 rows, nor the linear one at 5,000 | **9.0%** (28%) | **6.8%** (20%) | no usable signal at this scale: a justified miss |
| sample size: only the pooled linear test detects it | 3.8% (12%) | 1.8% (5%) | more rows of the same system would |
| method, linear: the linear oracle detects it at 1,000 rows | 14.2% (44%) | 20.1% (60%) | a search gap: the engines did not find or keep the right conditioning set |
| method, nonlinear: only the flexible oracle detects it (upper bound; that test is anti-conservative) | 5.2% (16%) | 4.9% (14%) | a nonlinear test with the right set might |
| **all misses** | 32.2% | 33.6% | |

The search gap is the largest class, yet every way we tried to close it adds false links faster than true ones. The
tested levers were a lower GES penalty, neighbourhood searches and a dependence pool. The best attainable at 1,000
rows with these tests is near v2. With 5,000 rows it is 24% / 28% missed. The justified floor is 9% / 7% of true links.

## 3. Where the wrong answers come from (DV-1, "if I set t, does y move?")

Semantic dev; first wrong edge on the claimed paths of each wrong "yes":

| Culprit | Wrong yes answers |
|---|---|
| a true link oriented the wrong way | 381 |
| a false link between causally unrelated variables | 370 |
| a shadow pointing the wrong way | 54 |
| shadows pointing the right way | 0: a shadow X → Y is a right answer to "does Y move if I set X" |

**Correction (15 Oct, later the same day):** the table above blames the first edge of the claimed path that is not
in the true graph. `analysis/reports/q2_v3_anatomy.md` blames the first edge at which the path leaves T's true
descendants (the edge that actually makes the answer wrong): 343 unrelated false links, 231 common-cause false links,
120 reversed true links, 111 backward shadows. The reversed-link count above is overstated; the anatomy report supersedes
this table.

Wrong "no" answers come from missed links. Even pairs the ledger places in different components are only 79% right
(semantic). The precision of "no" is capped by the miss rate, which is why more rows help DV-1 most.

Direction accuracy by licence on true links (dev):

| Licence | Semantic | Formula |
|---|---|---|
| collider | 0.87 | 0.83 |
| Meek R2 | 0.75 | 0.80 |
| Meek R1 | **0.64** | **0.60** |

Not acting on R1/R3 directions (shown as open): semantic DV-1 precision 0.756 → 0.793 (coverage 0.805 → 0.692),
formula 0.814 → 0.843; "yes" precision +0.06.

## 4. Decision weights and knowledge propagation (K2)

| Measure | Semantic | Formula | Prediction |
|---|---|---|---|
| tier gain with Meek propagation from knowledge (real names) | +0.0263 vs +0.0255 without | +0.0230 vs +0.0221 | negligible: only 46 / 37 pairs propagate |
| share of the oracle tier gain in the top-weight third of open pairs | **0.39** | **0.46** | P-K2 (≥ 0.60) **refuted** |
| true-link share, top third vs all open pairs | 0.74 vs 0.74 | 0.59 vs 0.61 | weight does not predict which pairs are real |

Weight measures reach: how many other pairs and answers a decision settles. That is not the same as being right. With
an unlimited query budget, ordering by weight changes nothing. Propagation is not adopted: it adds 0.001 F1 and would
need checker support for a new licence. Weights stay as a tool for budgeted querying and experiment choice (T6), not
a landmark lever.

## 5. Confidence from ledger features (K4)

Out of fold by scenario (5 folds), gradient-boosted classifier on 11 ledger features (path count, weakest licence on
the path, score deltas, CI p-values, skeleton distance, degrees), isotonic map on cross-fitted scores
(`kernel/claim_features.py`, `kernel/k4_eval.py`, `kernel/v3.py`).

| Family, regime | Half-coverage precision [interval] | ECE [interval] | v2 B4 (dev, out of fold) |
|---|---|---|---|
| semantic, D | 0.808 [0.744, 0.865] | 0.028 [0.014, 0.068] | 0.813, ECE 0.038 |
| **semantic, D×R** | **0.878 [0.836, 0.913]** | **0.008** [0.003, 0.048] | — |
| formula, D | 0.891 [0.861, 0.915] | 0.020 [0.010, 0.046] | 0.856, ECE 0.022 |
| **formula, D×R** | **0.882 [0.852, 0.918]** | **0.007** [0.007, 0.048] | — |

ER-3 cannot be cleared at this benchmark size, whatever the calibration. Its rule needs the lower end of the
realised-minus-claimed interval to be ≥ −0.03 at every threshold. With 25 scenario clusters that interval is about
±0.04 wide even when the point gap is 0.000. Dev point gaps run −0.000 to −0.025; lower ends run −0.039 to −0.093.
ER-3 needs either more scenarios or a different interval unit. Changing the rule after seeing the data would not be
honest, so it stays as written and is reported as not met by construction.

## Predictions of the design (written before these runs)

| Prediction | Verdict |
|---|---|
| P-K0 cache reproduces v2 dev ledgers hash-for-hash | **supported** (1,250/1,250, all five rules) |
| P-K1a E1 alone recovers ≥ 40% of semantic misses (refuted < 25%) | **refuted** (17% for the full battery, at precision 0.33) |
| P-K1b misses ≤ 15% with precision ≥ v2 − 0.02 (refuted > 20% or precision < v2 − 0.04) | **refuted** |
| P-K1c floor is 25–40% of v2's misses (refuted outside 15–50%) | semantic 28%: supported; formula 20%: inside the band, below the range |
| P-K3a/b claim granularity via weak links | **not testable as designed**: weak links fail (precision 0.33); replaced by the direction view, which is measured above |
| P-K2 top-weight third captures ≥ 60% of the oracle gain (refuted < 45%) | **refuted** on semantic (0.39); formula 0.46 |
| P-K4 out-of-fold ECE ≤ 0.04 both families (refuted > 0.06) | **supported** (0.028, 0.020; 0.008, 0.007 in D×R) |

## What v3 is

Pre-registered in `plans/v3_prereg.json`, hashed in `manifests/evidence/v3_prereg_2026-10-15.sha256`.

- v2's data-only ledger, unchanged.
- The direction view (R1/R3 not acted on).
- The confidence view (feature model, frozen per family and regime).
- Scored in D and in D×R.

Its predictions:

- ER-2 met in D×R for both families;
- ER-2 not met in D for semantic, met in D for formula;
- ER-3 not met (interval width);
- point ECE ≤ 0.04 everywhere.

The test split will be read a second time and reported beside v2's first read.

## Where we're going

Freeze v3 once the test-split engine cache is filled, read the test split once, and report. The two open
structural questions are not answered by v3. The first is accuracy above GES (route A), which needs direction
evidence beyond the equivalence class. The second is the 14–20% search gap. Both are named for v4 with the numbers
above.
