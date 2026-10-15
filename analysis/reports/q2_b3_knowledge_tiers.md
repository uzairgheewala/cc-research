# B3: declared knowledge as tiers, on the pairs the data leave open (Q2 build)

Tickets: BLD-04, CAP-04, TGT-11, TGT-19 (proposed). Bundle B3 of `plans/q2_dag.json`; gates B3.1-B3.3 of
`plans/b3_prereg.json` (written before any B3 run); landmarks ER-1 and ER-4a route B. Frozen kernel
`plans/b3_freeze.json` (id e9871399f1b92e7d, rule C3, B1's core unchanged). Written 2026-10-15.

**No new model call.** Knowledge comes from AB-07's recorded gpt-4o tier replies (pre-registered prompts, three phrasings,
three name arms, collected 12 Oct), replayed through the supplier contract. A live run would send the same prompts to the
same model at temperature 0; it was not needed to build or validate anything here.

## Where we are now

Knowledge enters the ledger as tiers, orients only pairs the data left open, never adds or removes a connection, and is
cited on every claim it touches. On held-out scenarios the provenance guarantees hold on every file: with neutral names
the ledger equals the data-only one (125/125 per family), the skeleton never moves in any arm, the loss under moved names
stays inside its exact bound (125/125), and every ledger verifies. **ER-1 is met.** Real names lift directed F1 by
+0.019 (semantic) and +0.028 (formula), both above zero but below the +0.03 lower end route B needs. **ER-4a route B is not
met**, as predicted, so ER-4a (route A or B) is not met.

## Must-show list

| Item | Result | Evidence |
|---|---|---|
| **B3.1** neutral-arm D+K claims equal D on every held-out file; skeleton identical in every arm | **pass**: neutral 125/125 identical per family; skeleton 375/375 per family | `analysis/results/q2_b3/summary_test.json` |
| **B3.2** moved-arm expected-credit loss within the exact T3 bound, 100% of held-out files | **pass**: 125/125 per family (largest loss equals its bound on one file, never above) | same |
| **B3.3** real arm not below D by more than 0.01 | **pass**: +0.019, +0.028 | same |
| Every D+K ledger passes V1-V13 and K7 | 0 failing of 750 held-out and 750 dev ledgers | `ledgers_failing` per arm |
| Supplier contract on replay | every reply passed through it; 0 truncations detectable (AB-07 did not record finish_reason: listed limit), 30 schema failures retried on test, 10 abstentions (a phrasing that failed twice); consensus used on 375/375 file-arms per family | `supplier` blocks in the summary |
| Held-out discipline | one logged read per family (11:32:57Z semantic, 11:47:07Z formula), code hash equal to the freeze | `analysis/results/q2_b3/access_log.jsonl` |

### Held-out (test splits, 125 files per family; directed F1 with the expectation rule; scenario-cluster 95% intervals)

| Family | Arm | D F1 | D+K F1 | Gain [95% CI] | Expected-credit gain | Pairs decided (true edges right / wrong) | Claims = D | Skipped (cycle) |
|---|---|---|---|---|---|---|---|---|
| semantic | real | 0.525 | 0.543 | **+0.019 [+0.010, +0.030]** | +0.021 [+0.013, +0.031] | 415 (249 / 35) | 7 | 40 |
| semantic | neutral | 0.525 | 0.525 | 0 | 0 | 0 | **125** | 0 |
| semantic | moved | 0.525 | 0.523 | -0.001 [-0.007, +0.004] | -0.002 [-0.007, +0.004] | 473 (162 / 183) | 8 | 53 |
| formula | real | 0.485 | 0.513 | **+0.028 [+0.019, +0.037]** | +0.024 [+0.017, +0.032] | 361 (242 / 22) | 19 | 16 |
| formula | neutral | 0.484 | 0.484 | 0 | 0 | 0 | **125** | 0 |
| formula | moved | 0.485 | 0.488 | +0.003 [-0.006, +0.013] | +0.000 [-0.007, +0.008] | 414 (142 / 150) | 16 | 22 |

Dev, for comparison: real-arm gain semantic +0.026 [+0.018, +0.033], formula +0.022 [+0.017, +0.027]; moved -0.000 and
-0.005 [-0.011, +0.000]; neutral identical 125/125.

"Decided" pairs that are neither right nor wrong are pairs the data made adjacent that are not true edges; their direction
does not change directed F1.

## Predictions

| Prediction (written before the runs) | Verdict |
|---|---|
| P-B3a B3.1 holds | **Supported** |
| P-B3b real-arm gain between 0.00 and 0.03 on both families (route B not met); refuted if > 0.03 on either | **Supported** (+0.019, +0.028; neither lower end above 0.03) |

## What the numbers say

- **Wrong names cost almost nothing, by construction.** Moved names decide about as many pairs wrong as right (183 vs 162
  on semantic), yet the F1 change is within +-0.007: an open pair is scored by a seeded coin flip, so in expectation it earns
  half credit; a wrongly oriented one loses that half and a rightly oriented one gains it. That symmetry is what T3 bounds;
  the truth-free bound the ledger itself records averages 0.084-0.086 per file, the realised loss is near zero.
- **Real names help less than AB-07's post hoc number suggested** (GES 0.528 -> 0.546 with tiers on every adjacency) because
  B3 only touches pairs C3 left open (15% of the ledger's adjacencies on semantic dev, 13% on formula; 74% and 61% of those open pairs are true edges) and requires all answering phrasings to agree.
  That is the price of ER-1: knowledge can never reverse a data direction.
- **How far this rule can go.** With interval half-widths of about 0.01, a lower end above 0.03 needs a point gain near
  +0.04. The dev-only ceiling of the rule (every open pair that is a true edge oriented correctly: an oracle tier) is
  +0.060 [+0.049, +0.072] semantic and +0.044 [+0.036, +0.053] formula (`analysis/results/q2_b3/ceiling_dev.json`). gpt-4o's
  tiers capture 43% and 50% of it on dev. Route B with this rule needs about two thirds of the oracle on semantic and
  nearly all of it on formula.

## One finding about the data-only kernel (not a gate)

On tables with exactly identical columns, the kernel orders those columns by a hash that includes the variable name
(the documented tie-break, so column order cannot matter). Identical columns cannot be told apart by data, so which one
receives which jittered values, and therefore which claims, follows the name bytes. Across the three name arms the D
graph scores differently on 8 semantic and 22 formula dev files and 0 semantic and 19 formula test files (of 125 each).
This is the one place names reach the data-only ledger. It does not affect any B3 gate (each arm compares D+K with its own
D), but it is a defect against the stated principle. Proposed fix for the next kernel version: withdraw any claim that is
not invariant under permuting a group of identical columns (`docs/design/q2_kernel_v3_proposals.md`).

## Limits

- The replay cannot detect truncation (finish_reason not recorded by AB-07; max_tokens 1500). A live rerun would close it.
- One model (gpt-4o), one date. The second-model and CARE moved-names parts carried from BND-12 are not part of this result.

## Where we're going

B4 attaches calibrated confidence to the D+I claims (ER-2, ER-3); B5 takes the ledger to the audit adapter and RCA (ER-4b).
Route A (data-only F1 above GES) and route B both remain open for ER-4a; the build summary sets out what each would take.
