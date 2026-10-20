# Explanation round X1-X3 (dev): why the ledger misses links, adds links and reverses directions

Tickets: TGT-18, TGT-19. Wave A, 20 Oct 2026. `analysis/q2_explain.py`; results in
`analysis/results/q2_v3/explain_x123_dev_<family>.json` and `explain_dev.json`. Pre-registration
`plans/q2_explain_prereg.json` (hashed in `manifests/evidence/explain_ben13_prereg_2026-10-20.sha256` before any number
existed). Dev split, 125 files per family, the frozen v3 ledger from the engine cache. No test split, no model calls.
X4 (a kernel test on the nonlinear-only class) is on wave A's run sheet.

## Answer in one paragraph

Both semantic gaps have the same mechanism: the engines score and test with a linear-Gaussian model, and the data come
from nonlinear and discrete mechanisms. Given the true graph, that score still wants 78% of the shadow links, 67% of the
common-cause links and 35% of the unrelated links the ledger adds. It also wants 76% of the "search gap" links the
ledger misses. Yet on 117 of 120 files GES's whole graph scores higher than the true graph (median +210 BIC). So GES is
not stopping short of a better graph. The score prefers a wrong one, in which shadow and common-cause links stand in for
the true links. The other missed-link classes (floor, nonlinear-only, sample size) are invisible to the score. The floor
stays a floor under a discrete-aware test. Half of the reversed directions go away when the true skeleton is used. The
pre-registered rule returns **D2-search**. Read with the global check, which was also pre-registered, the D2 lever is
**the score** (a model that fits the mechanisms, or a pretrained engine), not a better search over the same score. That
second sentence is a reading made after seeing the numbers.

## 1. X1: GES's own score as an oracle

The score is ges 1.1.0 GaussObsL0Pen on the z-scored table GES saw: the engine's data, jittered on the files where the
raw table is singular.

| | semantic | formula |
|---|---|---|
| missed, search gap (linear test finds it): share the score wants given the true parents | 553 of 726 (0.762), median gain +16.6 | 807 of 879 (0.918), median +208 |
| missed, nonlinear-only / sample size / floor: share the score wants | 0.004 / 0.000 / 0.000 | 0.014 / 0.000 / 0.000 |
| false, shadow: share the score wants added to the true graph | 0.781 (1,106) | 0.802 (1,468) |
| false, common cause | 0.669 (538) | 0.684 (621) |
| false, unrelated | 0.347 (389) | 0.299 (623) |
| files where the true DAG scores higher than GES's output | 3 of 120 (0.025) | 0 of 62 |
| median BIC of GES's output minus the true DAG | +210 | +2,429 |

Our rescoring reproduces GES's reported score to within 0.1 on 120 semantic files. On the other 5 semantic files and 63
formula files it does not, and those files are left out of the last two rows only. The formula mismatch is not yet
explained; formula's global row covers the 62 files that match.

## 2. X2: reversals with the true skeleton

The orientation rules are maxP priority 3 plus Meek (causal-learn 0.1.4.8, Fisher z). They are run on the true skeleton
and on the ledger's skeleton with the same data, with seeded jitter of 1e-6 on singular tables: 20 semantic files and
46 formula files.

| v3 reversals on found true links | semantic 330 | formula 376 |
|---|---|---|
| correct on the true skeleton (skeleton-caused) | 162 (0.491) | 234 (0.622) |
| still reversed on the true skeleton (rule-caused) | 125 (0.379) | 108 (0.287) |
| left open on the true skeleton | 43 (0.130) | 34 (0.090) |

On the true skeleton the same rules reverse 1,376 of 5,120 semantic true links. That is a 29% reversal rate among the
links they orient, against 25% on the ledger's skeleton. Fisher-z collider tests on these data are themselves a large
error source. These rules agree with v3's own direction view on 2,458 of 3,473 found semantic links (71%), so X2
attributes reversals under PC's rules, as the pre-registration says.

## 3. X3: is the floor real?

The test is a nested regression test that treats discrete columns as indicators. It is run on each floor link given the
other true parents, and on 250 true-null pairs per family.

| | semantic | formula |
|---|---|---|
| floor links detected at 0.05 | 0.054 of 459 (discrete endpoint: 0.049) | 0.051 of 297 (0.114) |
| true-null pairs rejected at 0.05 | 0.088 of 250 | 0.168 of 250 |
| detected beyond the null rate | -0.034 | -0.117 |

The floor is real: no detectable signal beyond what the test produces on nulls. The test is anti-conservative on nulls
(0.09-0.17 at a nominal 0.05), so even its raw detection rate overstates any signal.

## 4. Predictions (pre-registered) and the rule

| | prediction | result | |
|---|---|---|---|
| P1 | search-gap share the score wants >= 0.5 | 0.762 | holds |
| P2 | unrelated false links the score wants >= 0.3 | 0.347 | holds |
| P3 | true DAG scores higher on <= 0.3 of files | 0.025 | holds |
| P4 | >= 0.5 of reversals skeleton-caused | 0.491 | fails narrowly |
| P5 | floor detected beyond null <= 0.15 | -0.034 | holds |
| P6 | KCI detects the nonlinear-only class beyond null >= 0.3 | X4 on the run sheet | pending |

Rule: search share 0.762 >= 0.5, so the outcome is **D2-search**. The reading of D2 as "change the score, not the search"
rests on P3. P3 was pre-registered, but its role in choosing between the two D2 variants was not.

## 5. The explanation ledger after X1-X3 (semantic, dev)

| Gap | Size | Mechanism known now | Still open |
|---|---|---|---|
| missed links | 32.2% of true links | floor 9.0 (real: X3), nonlinear-only 5.2 and sample size 3.8 (invisible to the score), search gap 14.2: 10.8 wanted given the true parents but displaced by stand-in links the score prefers; 3.4 under the BIC penalty | whether a kernel test sees the nonlinear-only class (X4) |
| false links | 37% of claims | shadows (54%) and common cause (26%): the score wants most of them even given the true graph (0.78, 0.67) | 65% of unrelated links that the score does not want given the true graph: added only because of the wrong neighbourhood GES built |
| reversals | 330 | skeleton-caused 49%, rule-caused 38%, open 13% | - |

## 6. Changes after hashing (deviations, all before any decision was acted on)

The pre-registration file is unchanged. Code changes after the hash (code hash then `11d22b24...`, now `69b6ed64...`):

- Singular designs are recorded instead of crashing.
- X2 retries a singular table once with seeded jitter, as the kernel's own rule does.
- X2 reads v3's direction view. The first full run used v2's view and reported 444 reversals instead of 330.
- X1 scores the table GES saw.
- The score check tolerance moved from 1e-6 to 1.0, because GES's running total drifts by up to 0.03.

The first full run gave the same rule outcome (search share 0.767).

## Where this leaves the build choice

D1 (measurement plus ledger) stays the paper. The engine lever that would move the semantic gap is a score or engine that
fits nonlinear and discrete mechanisms, and X5 (pretrained engines under controls) is the cheapest test of that.
