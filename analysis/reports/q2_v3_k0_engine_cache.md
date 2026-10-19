# K0: the engine cache and the experiment loop (kernel v3)

Bundle K0 of `docs/design/q2_kernel_v3_design.md`. Written 2026-10-15. No model calls; dev split only.

## Where we are now

The engines run once per table and never again. Every post-engine experiment (rules, link recovery, direction
granularity, knowledge, calibration) now runs from stored engine records. The stored records rebuild v2's dev ledgers
hash-for-hash: 1,250 of 1,250 (5 rules × 125 files × 2 families). A full dev-split experiment takes about 10 seconds
per family on one core. In v2 it took 30–70 minutes.

## Must-show list

| Item | Result | Evidence |
|---|---|---|
| (1) cache rebuild reproduces the v2 dev ledgers hash-for-hash | **1,250/1,250**: rules pc, ges, C1, C2, C3 × 125 dev files × 2 families, against both the stored ledgers and the hashes in the dev rows | `analysis/results/q2_v3/k0_check_v2_{semantic,formula}.json` |
| (2) a full dev-split experiment in under 3 minutes | **~10 s per family on one core** (125 files, rule C3, every score: skeleton, directed F1, DV-1) | `python -m kernel.experiment`; `analysis/results/q2_v3/k1_baseline_v2.json` |
| (3) B4 stability vectors from the cache equal the stored ones | pending the resample fill (queued) | — |
| Unit tests | 5 new tests (`tests/test_q2_cache.py`): round trip rebuilds the same ledger; the key separates tables, settings and thread environments; names and column order do not change the key; a mismatched entry is an error; a read-only miss raises | NumPy only |

## What the cache stores and how it is keyed

- **Key.** The canonical table's sha256 (names and the caller's column order cannot reach it), the engine manifest's
  sha256, and the settings. Settings cover alpha, GES on/off, GES timeout, the jitter rule, the BLAS environment, and
  the GES penalty scale for the K1 variant.
- **Entry.** PC's recorded tests, marks and stages; GES's marks, score and failure; the jitter seed; the deviation
  text; timings. A hit is re-derived from the caller's data, re-jittered with the stored seed, and its hash is checked
  against the key. A mismatch is an error, never a silent substitution.
- **Size.** About 30 KB per file (gzip JSON).

## A reproducibility defect found on the first check (fixed as a class)

The first rebuild matched v2's claims but not its ledger hashes. Every p-value differed in the 14th digit. The
container had moved to a new host between the v2 runs and v3. OpenBLAS picks its kernels from the CPU it detects: it
chose SkylakeX on the old host and fell back to Prescott (generic) on the new one, which changes the floating-point
summation order.

The fix, as a class:

- `OPENBLAS_CORETYPE` is pinned (SKYLAKEX reproduces v2 exactly; checked against HASWELL, SANDYBRIDGE, COOPERLAKE and
  NEHALEM).
- The BLAS thread count stays pinned at 1, as in every v2 runner.
- Both are part of the cache key, so entries written under different BLAS settings can never mix.

What this means for CAP-11 ("same inputs, same ledger hash"): it held within one host in v2. It now holds across
hosts once the BLAS kernel family is pinned. Without the pin it fails silently in the 14th digit.

## The experiment loop

| Command | What it does |
|---|---|
| `python -m kernel.harness fill …` | the only command that starts engines (sources: obs, obs_int rows, pooled replicates, row resamples, GES penalty variants) |
| `python -m kernel.harness check-v2 …` | must-show 1 |
| `python -m kernel.experiment …` | one configuration scored on dev in seconds |
| `python -m kernel.k2_eval …` | knowledge arms replayed from AB-07 answers (no model call) |

Every scoring command opens the cache read-only and refuses the test split.

## Where we're going

K1 (link recovery) and K2 (decision weights) were measured in the same session on this loop; see
`analysis/reports/q2_v3_k1_k2_dev.md`.
