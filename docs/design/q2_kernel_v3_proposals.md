# Kernel v3: proposed changes found during the Q2 build (not adopted)

Written 2026-10-15, after the held-out reads of B1-B5. Nothing here changes a frozen result: each item is a proposal for
the next kernel version, which needs its own pre-registration, dev run, freeze and a fresh held-out read (the test splits
of B1-B5 have each been read once; a v3 read is a second read of the same splits and must be reported as such; a clean v3
test needs scenarios no version has been scored on).

Each entry: what was seen, the class it belongs to, the proposed fix, and the test that would show the fix works.

## K3-1 Identical columns let names reach the data-only ledger

- **Seen (B3).** Across the three name arms, D's directed F1 differs on 8 semantic and 22 formula dev files and on 0
  semantic and 19 formula test files (of 125). Every such file has a group of exactly identical columns.
- **Class.** Any tie-break among indistinguishable columns. The kernel uses var_id = sha256(values + name) so that column
  order cannot matter (I1 holds); the price is that the name bytes choose which identical column gets which jittered
  values, and the jitter then separates them.
- **Fix.** Treat a group of identical columns as interchangeable: build once, then withdraw (to x-y, recorded as a
  deviation) every claim whose relation changes under some permutation of the group; equivalently, keep only claims that
  are identical for all members. Record the group in the ledger as an `identical_columns` assumption.
- **Test.** New invariant I1b (relabelling): D claims identical under the three name arms on 100% of dev files with
  identical columns; R3 unchanged.

## K3-2 Engine directed cycles (recorded in B1, handled, kept)

- Kept as built: cycles from causal-learn's maxP stage and its Meek step are withdrawn and recorded (amendment 1). The
  upstream note is `docs/drafts/bug_reports/causal_learn_meek_directed_cycle.md` (EXT-07, Uzair decides whether to send).

## K3-3 Intervention orientations: collapsed paths, false-positive shifts, weak propagation

- **Seen (B2).** On formula test files 70 of 112 intervention orientations are true edges in that direction (semantic
  299 of 396), yet D+I's DV-1 precision does not fall. The dev diagnostic
  (`analysis/results/q2_b2/orientation_diag_dev_<family>.json`) splits the wrong orientations:
  - **Collapsed paths** (an ancestral non-edge): 61 of 70 wrong direct orientations on semantic, 33 of 60 on formula.
  - **Shift-test false positives** (reversed, unrelated or backward pairs): 9 on semantic, 27 on formula.
  - **Weak Meek propagation** from intervention orientations: right 16 of 44 on semantic and 10 of 25 on formula.
- **Classes.** (a) Shift evidence says "T is an ancestor of Y", and the rule turns it into "T -> Y" on any adjacent
  pair, so a wrong adjacency becomes a confident wrong edge. (b) Welch tests at alpha 0.01 with no multiplicity control,
  fragile on deterministic formula relations. (c) Propagation compounds both.
- **Fixes (candidates, one at a time on dev).**
  - (a) Where T also shifts a variable Z that the ledger connects on a path from T to Y, record T -> Y as an ancestral
    (DV-1) claim only.
  - (b) Holm or Benjamini-Hochberg across the shift tests of one file.
  - (c) No Meek propagation from intervention-sourced orientations, or propagation only through data-licensed arrows.
- **Test.** On dev: the share of intervention orientations that are true edges rises in both families, and D+I's DV-1
  precision is not lower.

## K3-4 Edge-level calibration at high thresholds (B4)

- **Seen (dev, out of fold).** Calibrated edge claims at c/g = 4 on semantic: claimed 0.807, realised 0.638. DV-1 claims
  are well calibrated (ECE 0.038 / 0.022); the gates concern DV-1 only.
- **Class.** Isotonic maps on 11 stability levels (B = 10 resamples) with few claims at the top level: the top bin is
  fitted on small, scenario-correlated counts.
- **Fix (candidate).** B = 20 resamples, a minimum of 50 claims per isotonic block, fitted per family with scenario-level
  shrinkage.
- **Test.** Out-of-fold edge ECE <= 0.05 and realised >= claimed - 0.03 at c/g = 4 on dev.

## Where route A would come from (ER-4a)

Data-only F1 above GES needs directions GES does not already have. C3 takes GES's adjacencies and keeps a GES direction
only when its licence survives the PC audit, so on F1 it can at best tie GES (it did: -0.001, +0.002). Candidates, all
for a new pre-registration: (a) a third engine with a different error profile (e.g. a pretrained amortised model, once the
checkpoints are reachable); (b) a direction test that goes beyond the Markov equivalence class on pairs left open
(non-Gaussian residual independence, LiNGAM-style, or unequal-noise-variance ordering), entered as its own evidence type
with its assumption recorded and a sensitivity under which it is withdrawn; scores alone cannot help here, since
Markov-equivalent graphs score the same under BIC; (c) accepting route A is not this kernel's claim and carrying ER-4a
on route B with a stronger knowledge source.
