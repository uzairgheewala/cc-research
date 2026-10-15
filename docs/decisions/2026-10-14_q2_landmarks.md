# Decision record: the landmark set for the Q2 build (2026-10-14)

Tickets: DEC-05 (context), AUD-47 (pre-registration), BLD-02..05, BLD-07, BLD-14. Written after Uzair asked, on 14 Oct,
how many of the benchmark targets must be reached "to land a solid wedge and/or paper; that's the constraints that we'll
then work under". The thresholds below are fixed before B0 starts and hashed in
`manifests/evidence/q2_landmarks_2026-10-14.sha256`. They add to, and never relax, the gates in `plans/q2_build_prereg.json`.

Scoring rule for every row: held-out test splits of `plans/splits.json` only, scored once per frozen kernel version; a
landmark counts when the lower end of the paired 95% bootstrap interval clears the threshold.

## The binding set

| # | Row | Threshold | Paper | Wedge | Known at |
|---|---|---|---|---|---|
| F | Floors: directed F1 on semantic and formula >= PC maxP - 0.01 | gate B1.2 (hashed) | required | required | B1 |
| 1 | Name reliance 0 by construction; 100% of directions carry a source | gates B3.1, B3.2 (hashed) | required | required | B3 |
| 2 | DV-1 precision of committed claims > 0.80 at >= 50% coverage, semantic and formula | clears c/g = 4 | required | required | B4 |
| 3 | Calibration: ECE <= 0.05; realised precision >= claimed - 0.03 at c/g = 1, 2, 4 | gates B4.1, B4.2 (hashed) | required | required | B4 |
| 4a | One F1 landmark: directed F1 above data-only GES on at least one family under controls, or B3 lifts F1 by > 0.03 over B1 with model tiers | | required (one of two) | not needed | B1 / B3 |
| 4b | RCA: AC@3 >= 0.90 with declared topology while the ledger fills gaps (PetShop) | | not needed | required | B5 |
| - | Causal Chambers: DV-1 precision within 0.03 of GES | report only | report only | report only | B1 |
| - | Stretch: directed F1 >= 0.634 on semantic under controls | | not needed; main-track candidate if hit | not needed | B3 |

Paper: floors + landmarks 1, 2, 3, 4a. Wedge: floors + landmarks 1, 2, 3, 4b. Both: five distinct landmarks.

## Failure conversions, decided in advance

| Failure | Consequence |
|---|---|
| Floors fail (B1.2 refuted, <= -0.05) | Method half dead. Paper A (measurement only). No wedge |
| F holds, 1 fails | A construction defect: fix as a class before any downstream step |
| F, 1 hold; 2 or 3 fails | D&B paper as benchmark + instrumentation. Wedge delayed |
| 1-3 hold, 4a fails | D&B paper on reliability, stated plainly |
| 1-3 hold, 4b fails | Paper lands; the wedge moves to AB-14's second vertical |

## Constraints on the constraints

1. Rows 2 and 3 are the ones most tempting to tune: B4's calibration map is fitted on dev and frozen before any test score.
2. Order of knowing: F at B1, 4a at B1 or B3, 1 at B3, 2-3 at B4, 4b at B5. B5 is built only if B1-B4 passed.
