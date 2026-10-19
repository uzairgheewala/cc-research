# Kernel v3 design: link recovery, decisions as a resource, claim granularity, and the engine cache

Status: draft for Uzair's approval, 2026-10-15. Nothing here changes a frozen v2 result. Every number below is from
the v2 held-out reads or from dev-only diagnostics written after them (`analysis/results/q2_b3/ceiling_dev.json`,
`analysis/results/q2_b2/orientation_diag_dev_*.json`, and the missed-link study in section 2).

## 0. Where we are now, as decisions

The ledger makes three kinds of decision on a table of 1,000 rows and 25 columns, and each kind has its own loss
(held-out, semantic family, kernel rule C3):

| Decision | What it says | Where it stands | What the loss is made of |
|---|---|---|---|
| **Connection** | X and Y are directly linked | we find 55% of true links; 37% of the links we claim are not true links (skeleton F1 0.66) | the largest loss, upstream of everything else |
| **Direction** | X -> Y, Y -> X, or open | committed on 83% of found links, 84% of those right | almost all directions come from one evidence type (collider patterns 4,523; propagation 594) |
| **Effect** | X affects Y (directly or through others) / does not / abstain | "yes" 69% right, "no" 82% right, 22% abstained | the "yes" claims are what the precision landmark grades |

Two facts set the design. First, the missed links are weak in the data (median correlation 0.06), and about a third
of the links we wrongly claim are the shadow of a missed one: X -> M -> Y with X–M invisible makes X–Y look direct.
Second, the top confidence band is 34% wrong on link claims in both families, stably, so no re-ranking fixes it; only a
different kind of claim does.

## 1. Axes

| Axis | Values | v2 | v3 |
|---|---|---|---|
| A1 evidence type for a connection | linear CI test (Fisher-z), GES score delta | both | plus nonlinear conditional test, mixed-type test, shift-under-intervention, pooled-replicate test |
| A2 claim granularity | direct link; direction; effect | all three, but a direct link is the only route to an effect | plus **weak link** (connection with below-threshold evidence) and **demotion** direct -> affects |
| A3 decision weight | none (every decision counted once) | none | weight = pairs it settles + effect answers it changes |
| A4 what knowledge may do | orient an open pair | orient | orient an open pair, or demote a claim's granularity; never add, remove or reverse |
| A5 data regime | D, D+I, D+K | per file | plus D×R (the scenario's 5 replicates pooled) as a separately scored regime |
| A6 compute | engines rerun per build | yes | engines cached by (data hash, manifest hash, resample seed) |

## 2. The missed links: what is recoverable, measured

Study on 10 dev scenarios per family (replicate 0), every true link the v2 skeleton missed (167 semantic, 115 formula).
Three tests per missed link: (a) held-out R² gain from adding the missed parent to a gradient-boosting fit on the
true parents (does a nonlinear conditional signal exist at all?); (b) plain correlation on the 5 pooled replicates
(does more data from the same system make it visible?); (c) whether either column is discrete (<= 10 distinct values).

| | semantic | formula |
|---|---|---|
| nonlinear conditional signal present (R² gain > 0.02) | 38% | 45% |
| visible with 5x rows (pooled z > 3) | 50% | 55% |
| involves a discrete column | **65%** | 9% |
| recoverable by at least one of (a), (b) | **66%** | **65%** |
| neither: no signal at this scale | 34% | 35% |

So "collapse the misses to zero" splits into two typed parts. About two thirds of the misses are recoverable, by
evidence types the engines do not use today; about one third are links whose effect is below what 1,000 rows (or
even 5,000) can show. The second part is a **floor**, and the honest claim is "every link above the floor, and the
floor measured and reported", not zero. The target for v3 is to cut missed links from ~33% of true links to ~12% on
dev, with link precision not falling.

The discrete-column figure is the single biggest lead: the Fisher-z test treats a yes/no column as Gaussian and loses
most of its power; 65% of semantic misses touch such a column. That is a feature problem and it is cheap.

## 3. Bundles

Order: K0 -> K1 -> K3 -> K2 -> K4. K5 is optional and last. Every bundle is dev-only until its gate passes; the held-out
policy is in section 5. Each bundle names its binding times and failure modes before it is built.

### K0 Engine cache and subsystem harnesses (the iteration-time bundle)

Measured on one file: GES 6.7 s, PC 0.2 s, process warm-up ~20 s; everything after the engines is under 0.5 s. B4's
stability runs 10 engine rebuilds per file. The cache turns every rule, knowledge, granularity and calibration
experiment into a seconds-per-split job.

- **Cache key**: `cache/engines/<manifest_sha>/<data_sha>[.r<seed>.<b>].npz` holding PC's CI-test records (i, j, S, p),
  the maxP/Meek engine graphs, GES's graph and per-edge local score deltas, timings, and the jitter seed if used.
  `data_sha` is the canonical table's hash (already computed by `kernel/build.run_engines`); resamples add seed and
  index. The manifest hash is the one in `engines/MANIFEST.json`.
- **Binding time**: the cache is filled once per (split, resample seed) and is invalidated only by a manifest change.
  A cache hit is recorded in the ledger's `engine_outputs` as `cached: true` with the key; the ledger hash does not
  depend on it.
- **Harnesses**: one entry point per subsystem (`kernel/harness/{policy,interventions,knowledge,confidence}.py`) that
  takes cached engine records and a rule, runs a split, and prints the subsystem's own score table. No engine import.
- **Must show**: (1) rule C3 rebuilt from cache reproduces the frozen v2 dev ledgers hash-for-hash, 250/250 files per
  family (determinism, and proof the cache carries everything the build reads); (2) a full dev-split policy experiment
  in under 3 minutes on the 2-core box; (3) the B4 stability vectors from cache equal the stored ones.
- **Failure modes named now**: a cache keyed too coarsely (missing the jitter seed) would silently mix tables -> the
  key includes the jitter seed and the ledger records it; a stale manifest -> the key includes the manifest hash;
  disk growth -> ~1.5 MB per file, ~1 GB for both splits and 10 resamples, acceptable.

### K1 Link recovery (connection evidence types)

Four new evidence types, each a typed record with its own licence, so a link found by one of them is never confused
with a Fisher-z link:

- **E1 mixed-type test.** For pairs where either column is discrete, replace Fisher-z with a test that respects the
  type (point-biserial / chi-square / rank-based partial correlation, chosen by the pair's types). Expected to address
  most of the 65% of semantic misses that touch a discrete column.
- **E2 nonlinear conditional test.** Regression-residual independence test (gradient boosting on the conditioning set,
  then a rank-based dependence test on the residuals), run only on pairs the linear test declared independent at the
  conditioning sets PC used. It never removes a link; it can add a **weak link** claim.
- **E3 shift-under-intervention as connection evidence** (D+I only). A shift of Y under do(T) with no path T ... Y in
  the ledger adds an **affects** claim, never a direct link.
- **E4 pooled replicates** (regime D×R). The scenario's five files pooled (n = 5,000). Scored as its own regime against
  baselines given the same rows; never mixed into D's numbers; reported beside them. This is the "more data" lever,
  and it is a different claim ("given 5,000 rows of this system"), so it gets its own column.

A **weak link** is a new claim relation: connected with evidence below the main threshold, carrying its evidence type
and p-value. It does not enter directed F1 as a link (it scores as undecided), it does enter the mediator search of
K3, and it is listed in the effect view as "possible".

- **Binding times**: the tests and thresholds are fixed in `plans/k1_prereg.json` before the dev run; multiplicity
  control (Benjamini-Hochberg across the new tests of one file) is part of the rule.
- **Must show**: missed true links on dev from ~33% to <= 15% of true links (E1+E2, D regime) and <= 12% with E4;
  skeleton precision not below v2 - 0.02; every new link claim carries its evidence type; K7 re-derives E1 and E2
  claims from their records (the checker gains two record types); the floor (links with no signal under any test)
  reported as a number per family.
- **Failure modes named now**: nonlinear tests raise false links -> BH control and the weak-link class absorb
  below-threshold finds without hurting F1; E1 changes which separating sets PC finds -> the engine's own skeleton is
  still cached and recorded, E1 runs as an audit layer on top, so the v2 behaviour is recoverable by rule; E4 tempts a
  scoreboard with 5x data -> D×R is a labelled regime, never the headline.

### K3 Claim granularity and demotion (depends on K1's weak links)

- **Demotion**: a direct-link claim X -> Y is demoted to **affects** when a mediator path X -> M -> Y exists in which at
  least one step is a weak link or an E3 affects claim, and the X–Y link's evidence is not stronger than the path's.
  The demotion is itself a claim with a licence (`mediator_path`) citing the records.
- **Knowledge may demote**: a tier statement that contradicts a direct link may demote it to affects (new invariant
  I8: knowledge never adds, removes or reverses a link, and never changes which pairs are reachable). ER-1's guarantees
  are kept because the skeleton and the direction set are untouched; only the granularity of a claim moves.
- **Must show** (dev, D regime): top-band link precision from 0.66 to >= 0.80; "X affects Y" claim precision from 0.69
  to >= 0.78 at coverage not below v2 - 0.05; directed F1 not below v2 - 0.01 (demoted links score as open); neutral
  names still equal D on 100% of files.
- **Failure modes named now**: over-demotion (true direct links demoted because a spurious weak link exists) -> the
  rule requires the path's evidence to be at least as strong as the link's, and the demotion count per file is
  reported; a demotion that changes reachability -> forbidden by I8 and checked by K7.

### K2 Decisions as a resource (weight and spending)

- **Weight** of an open or demotable decision = (number of other pairs its orientation would settle through Meek
  closure) + (number of effect answers that would change). Computed from the ledger alone, cached per file.
- **Spending by weight**: knowledge is asked about open pairs in descending weight (AB-07 replay: the same recorded
  answers, consumed in a different order, so no new model call); interventions are credited by the weight they
  settle; the experiment-choice rule (thesis T6) proposes the target that settles the most weight.
- **Costing by weight**: the selective view's cost of a wrong claim is multiplied by its weight; precision at a stated
  coverage is reported both unweighted (the landmark) and weight-adjusted.
- **Must show**: weight distribution per family (expect a long tail: a few collider-adjacent pairs settle many); real-arm
  tier gain per queried pair rises monotonically with weight on dev; the top-weight third of open pairs captures >= 60%
  of the oracle tier gain (ceiling +0.060 / +0.044).
- **Failure modes named now**: weight computed on a wrong skeleton inherits its errors -> weights are recomputed after
  K1/K3 and recorded with the skeleton hash; weight-ordering that changes which answers are used could be tuned on
  test -> the order rule is fixed in the pre-registration.

### K4 Calibration statistics

Scenario-level shrinkage of the isotonic map, B = 20 resamples, minimum block size 50, fitted per family. From
cache, this is minutes. Must show: out-of-fold ECE on dev <= 0.04 for both families and the claimed-vs-realised gap
within 0.03 at every threshold, on DV-1 and edge claims.

### K5 Direction evidence beyond the equivalence class (optional, for route A)

Non-Gaussian residual independence (LiNGAM-style) or unequal-noise-variance ordering on pairs left open, as a typed
evidence type with its assumption recorded and a sensitivity under which it is withdrawn. Only if K1-K3 leave ER-4a
route B short. Not scheduled.

## 4. Predictions (written now; refutation thresholds fixed)

| Id | Prediction | Refuted if |
|---|---|---|
| P-K0 | cache reproduces v2 dev ledgers hash-for-hash, 500/500 | any file differs |
| P-K1a | E1 alone recovers >= 40% of semantic missed links on dev | < 25% |
| P-K1b | E1+E2 bring missed links to <= 15% of true links with skeleton precision >= v2 - 0.02 | > 20% or precision < v2 - 0.04 |
| P-K1c | the floor (no signal under any test) is 25-40% of v2's misses | outside 15-50% |
| P-K3a | top-band link precision >= 0.80 on dev | < 0.74 |
| P-K3b | "affects" precision >= 0.78 at coverage >= v2 - 0.05 | < 0.74 |
| P-K2 | the top-weight third of open pairs captures >= 60% of the oracle tier gain | < 45% |
| P-K4 | out-of-fold dev ECE <= 0.04 both families | > 0.06 |

## 5. Held-out policy for v3

CausalArena has 50 scenarios per family, all used (25 dev, 25 test), and every v2 bundle has read the test split once.
There is no unread split. A v3 held-out read is therefore a **second read of the same split**, and it is reported as
such: the v2 and v3 numbers side by side, the version count (2) stated, the v3 rule pre-registered and chosen on dev
before the read. The selection-on-test risk is bounded by the number of versions, and it is disclosed rather than
hidden. The landmarks keep their rule (conservative interval end). If a second CausalArena release or another family
appears, v3's first read goes there instead.

## 6. What stays fixed

The v2 freezes, pre-registrations and results are not touched. v3 is a new kernel version with its own freeze
(`plans/k*_freeze.json`), and the v2 ledgers remain the comparison row in every v3 table.

## Where we're going

On approval: K0 first (it pays for itself on the first experiment), then K1, with E1 (mixed-type test) as its first
rung because it is cheap and addresses the largest measured share of misses. Each bundle ships with a must-show list,
a dev-only harness, and a pre-registration written before its dev run.
