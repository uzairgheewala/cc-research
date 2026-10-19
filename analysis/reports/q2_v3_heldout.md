# Kernel v3: held-out results (second read of the CausalArena test splits)

Pre-registration `plans/v3_prereg.json` (written after the dev experiments, before this read; hashed in
`manifests/evidence/v3_prereg_2026-10-15.sha256`). Freeze `plans/v3_freeze.json`, id 0cda331ea81cf0dd. The data-only
core is the same as B1's (core_sha256 9268cd74…), and so are the four confidence models. One logged read per family and
regime (`analysis/results/q2_v3/access_log.jsonl`, 20:20–20:21Z). Written 2026-10-15. No model calls.

**This is the second read of these test splits.** v2 (B1–B4) read them once. No unread split exists. The numbers
below sit beside v2's, and the version count is two.

## Where we are now

v3 does not change a single claim of the ledger. It changes what is acted on and how sure each answer says it is:

- directions from the weakest rule (Meek R1/R3) are not acted on;
- every answer carries a probability from a model on the ledger's own features.

On the held-out files:

- **ER-2 (precision at half coverage) is met for formula in both regimes** (lower ends 0.876 and 0.863).
- **ER-2 is not met for semantic in either regime.** Data-only: 0.830 [0.783, 0.874]. Pooled 5,000 rows: 0.866
  [**0.799**, 0.918], one thousandth short of the bar.
- **ER-3 is not met anywhere.** Calibration error is 0.021–0.026 (v2: 0.057 / 0.036), but every upper end lands
  between 0.051 and 0.074.

## Results

| Family, regime | Tables | Half-coverage precision [95% interval] | Coverage | ECE [interval] | Realised − claimed at c/g = 1 / 2 / 4 (lower ends) | ER-2 | ER-3 |
|---|---|---|---|---|---|---|---|
| semantic, D | 125 | **0.830** [0.783, 0.874] | 0.545 | 0.021 [0.007, 0.063] | +0.021 / +0.021 / +0.028 (−0.019 / −0.019 / −0.016) | not met | not met (ECE upper) |
| semantic, D×R | 25 | **0.866** [**0.799**, 0.918] | 0.516 | 0.026 [0.009, 0.074] | −0.006 / −0.009 / −0.021 (−0.063 / −0.065 / −0.087) | not met (by 0.001) | not met |
| formula, D | 125 | **0.908** [0.876, 0.942] | 0.562 | 0.025 [0.010, **0.051**] | +0.014 / +0.017 / +0.021 (−0.019 / −0.015 / −0.011) | **met** | not met (ECE upper by 0.001) |
| formula, D×R | 25 | **0.911** [0.863, 0.953] | 0.605 | 0.021 [0.008, 0.058] | +0.021 / +0.020 / +0.018 (−0.023 / −0.025 / −0.027) | **met** | not met (ECE upper) |

### Beside v2 (the first read of the same splits)

| Family | v2 B4: half-coverage precision [interval], ECE | v3 D: same | Note |
|---|---|---|---|
| semantic | 0.812 [0.756, 0.864], 0.057 | 0.830 [0.783, 0.874], 0.021 | v2 scored replicate 0 of each scenario (25 files); v3 D scores all 125 files (pre-registered) |
| formula | 0.899 [0.854, 0.939], 0.036 | 0.908 [0.876, 0.942], 0.025 | same difference in file sets |

The file sets differ by design: v2's B4 used one replicate per scenario to halve its stability compute, while v3 needs
no resamples. The interval is set by the 25 scenario clusters in both, so the comparison is fair in spirit but not
file-for-file. A rep000-only v3 number would be a third look at the split and was not computed.

## Predictions (plans/v3_prereg.json)

| Prediction | Verdict |
|---|---|
| P-V3a ER-2 met in D×R for both families (refuted if either lower end ≤ 0.80) | **Refuted** on semantic: lower end 0.799 |
| P-V3b ER-2 not met in D for semantic, met in D for formula | **Supported** |
| P-V3c ER-3 not met in either regime | **Supported** for the outcome, partly wrong on the reason. In D the realised-minus-claimed lower ends clear −0.03 (125 files give enough claims). ER-3 fails on the ECE upper end instead (0.051–0.074). In D×R both parts fail. |
| P-V3d point ECE ≤ 0.04 everywhere (refuted if any > 0.06) | **Supported** (0.021–0.026) |

## What the numbers say

- **Calibration is now good in point terms and slightly under-claims.** In D, realised precision is above the claimed
  probability at every threshold (+0.014 to +0.028). The ECE upper ends sit just above 0.05 because 25 scenario
  clusters make the interval wide.
- **Semantic precision is capped by missed links**, as the dev blame analysis showed. A "no" answer is wrong whenever a
  true path runs through a link the ledger missed. Pooling five replicates lifts semantic from 0.830 to 0.866, but 25
  pooled tables give a wide interval.
- **The landmark rule's interval unit is now the binding constraint for ER-3 and semantic ER-2.** Every remaining miss
  is within 0.001–0.024 of its bar, and every interval is ±0.04–0.06 wide on 25 scenarios. The rule stays as written.

## Where we're going

Three options, in order of what each would buy, for Uzair's choice:

1. More scenarios. CausalArena has no unread split. A second benchmark family with released targets, or new
   CausalArena scenarios if released, would narrow every interval.
2. A v4 aimed at semantic misses: the 14% search gap measured on dev.
3. Route A (accuracy above GES), which needs direction evidence beyond the equivalence class.
