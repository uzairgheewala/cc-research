# B1: the data-only claim ledger (Q2 build)

Tickets: BLD-02, BLD-14, CAP-05, CAP-09, CAP-11, TGT-10, TGT-19 (proposed). Bundle B1 of `plans/q2_dag.json`; gates
B1.1-B1.3 of `plans/q2_build_prereg.json`; rungs R1-R5 of `plans/b1_prereg.json` (amended once,
`plans/b1_prereg_amendment_1.json`). Written 2026-10-15. No model calls.

## Where we are now

The ledger kernel exists and passed its held-out test. On CausalArena's test scenarios, with columns shuffled, the
frozen data-only kernel beats plain PC with maxP by +0.053 (semantic) and +0.115 (formula) directed F1, and by +0.073 and
+0.053 DV-1 precision; every interval is above zero. It matches GES on F1 (-0.001 and +0.002, intervals across zero) while
its committed claims are more often right (+0.028 and +0.030 DV-1 precision, intervals above zero). Every one of 1,750
ledgers (1,250 dev, 500 held-out) passes the verifier (V1-V13) and the independent re-derivation (K7).

**Landmark ER-F (floors): met.** **ER-4a route A (data-only F1 above GES on one family): not met**, as predicted (Q-B1d).

## What the kernel is

- **K0** variables by content hash; engines see columns in canonical order only (sorted by the sha256 of their values).
- **K1** two data-pattern engines on the canonical table: causal-learn PC with maxP, every CI test recorded as evidence;
  GES (BIC). A singular correlation matrix is retried once with seeded 1e-6 jitter and recorded as a deviation.
- **K2** PC re-derived from its own tests (`kernel/derive.py`); the kernel uses the re-derivation, which leaves open
  any orientation on a directed cycle (section "Two engine defects").
- **K3** rule C3, chosen on dev by the pre-registered selection rule: GES's adjacencies; a GES direction that PC's
  committed direction contradicts is opened, then the surviving directions are re-derived (collider and Meek
  licences), so a direction survives only if GES committed it and its licence still holds.
- **K4** evidence: one ci_test record per distinct test (about 1,500 per 25-variable table) and one score_delta record per
  pair either engine found adjacent; every claim cites the records on its own pair and the premises of its licence.
- **K6** ledger v0.2 (`ledger/schema02.py`): plan, deviations, assumptions with sensitivities, lineage, question,
  orientation convention, engine outputs, reviews. **K7** `kernel/checker.py` re-derives every claim from the records
  alone, NumPy only.

## Rungs and gates

| Rung / gate | Result | Evidence |
|---|---|---|
| R1 PC-only regime equals the plain library call | 250/250 dev and 250/250 held-out files equal, except the pairs set aside by recorded defects (dev 16 files, 44 pairs; held-out 17 files, 47 pairs) | `analysis/results/q2_b1/dev_*.jsonl`, `test_*.jsonl` |
| R2 / **B1.3** verifier and K7 on every ledger; mutation tests | 1,250 dev and 500 held-out ledgers pass V1-V13 and K7; removing one cited record fails V2; removing a load-bearing uncited test fails K7 | rows above; `tests/test_q2_kernel.py` |
| R3 / **B1.1** I1 and I2 with full engine reruns | 50/50 files (one per dev scenario): claims and evidence identical under 6 column orders; 50/50 repeat builds give the same ledger hash | `analysis/results/q2_b1/invariance_dev.json` |
| R4 selection rule on dev | eligible C3 and GES; chosen **C3** (higher DV-1 precision) | `analysis/results/q2_b1/dev_selection.json`, `plans/b1_freeze.json` |
| R5 / **B1.2** held-out against plain PC maxP | **pass** (both metrics, both families; refutation threshold -0.05 nowhere near) | `analysis/results/q2_b1/heldout.json` |

### Held-out (test splits, frozen kernel 3b87f8fc1c3cb09f, rule C3; scenario-cluster 95% intervals)

| Family | Against | Files | Kernel F1 | Baseline F1 | F1 difference | Kernel DV-1 (coverage) | Baseline DV-1 (coverage) | DV-1 difference |
|---|---|---|---|---|---|---|---|---|
| semantic | PC maxP | 121 | 0.523 | 0.469 | **+0.053 [+0.020, +0.087]** | 0.773 (0.777) | 0.700 (0.939) | **+0.073 [+0.034, +0.115]** |
| semantic | GES | 121 | 0.522 | 0.523 | -0.001 [-0.007, +0.005] | 0.772 (0.778) | 0.744 (0.949) | +0.028 [+0.015, +0.042] |
| formula | PC maxP | 90 | 0.470 | 0.355 | **+0.115 [+0.082, +0.152]** | 0.825 (0.882) | 0.772 (0.951) | **+0.053 [+0.006, +0.105]** |
| formula | GES | 93 | 0.471 | 0.469 | +0.002 [-0.012, +0.017] | 0.825 (0.882) | 0.795 (0.965) | +0.030 [+0.009, +0.061] |

On every file, including the ones the baselines cannot run (semantic 5 and formula 37 jittered tables): semantic F1
0.525, DV-1 0.776 at coverage 0.778; formula F1 0.485, DV-1 0.844 at coverage 0.872. GES failed on 2 formula test files;
the rule fell back to PC there and the ledgers say so.

The kernel buys its higher DV-1 precision with lower coverage (0.78-0.88 against 0.94-0.97): it abstains where its two
engines disagree. B4 turns that trade into a stated cost ratio.

## Predictions

| Prediction (written before the runs) | Verdict |
|---|---|
| Q-B1a R1 holds; directed-cycle defects on 1-3% of files | **Partly.** R1 holds modulo recorded defects; defects on 6.4% of dev and 6.8% of held-out files once maxP-stage cycles are counted (the 1-3% figure counted only the first defect type) |
| Q-B1b C2 or C3 clears GES F1 on semantic dev by >= 0.01 | **Refuted** (C3 -0.012, C2 -0.011; the stored-row numbers disclosed in the pre-registration already pointed there) |
| Q-B1c the chosen rule beats PC maxP held-out F1 by >= 0.03 in both families | **Supported** (+0.053, +0.115) |
| Q-B1d ER-4a route A not met | **Supported** (F1 against GES -0.001 and +0.002) |

## Two engine defects (and one of ours)

1. **causal-learn 0.1.4.8 PC, Meek step.** The ancestor test reads an incrementally updated path matrix that is not
   transitively closed; on 6 dev and 6 held-out files the library's final graph differs from a fresh-reachability
   re-statement of the same loop, and on most of those it contains a directed cycle. Draft note:
   `docs/drafts/bug_reports/causal_learn_meek_directed_cycle.md` (EXT-07, proposed).
2. **maxP itself** applies colliders without an acyclicity check, so the graph can already be cyclic before Meek (10
   dev and 12 held-out files). The kernel withdraws every orientation on a directed cycle and records it.
3. **Ours.** The first frozen kernel accepted only defect 1 in its simplest shape and stopped with a build error on a
   held-out file where defects 1 and 2 met (both final graphs cyclic, one pair oriented oppositely). Diagnosed from the
   engine-versus-re-derivation equality only; fixed as a class (amendment 1): divergences are recorded, never fatal;
   cycles are withdrawn in PC, after every rule and after interventions; K7 re-applies both. The 36 rows of the aborted
   read are kept unread (`analysis/results/q2_b1/aborted/`); dev was rerun, the rule re-selected (C3 again), the kernel
   re-frozen and R3 rerun before the second, separately logged held-out read (`access_log.jsonl`).

## Deviations

- The pre-registration discloses that the five candidate rules had been computed from stored per-file rows on dev and
  test before the selection rule was written; the held-out read itself happened once per frozen version.
- One aborted held-out read (above).

## Where we're going

B2 (interventions, Causal Chambers), B3 (tiers on the open pairs) and B4 (confidence and the selective view) all build on
this frozen kernel; their dev runs are under way. ER-4a now rests on route B (B3).
