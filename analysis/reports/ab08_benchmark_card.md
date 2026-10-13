# AB-08 benchmark card: B2 name-reliance benchmark with a rho dial (decoupled semantics)

Tickets: AUD-39 (this bundle), STR-02, EVL-02. Written 2026-10-12. No model calls anywhere in the construction or the
reference runs. Generator `analysis/b2_generator.py`, scorer `analysis/b2_score.py`, tests `tests/test_b2_generator.py`.

## 1. Purpose

On CausalArena's semantic family, systems that read variable names score far better when the names are real than when
they are swapped between columns (Causal-Copilot: 0.306 directed F1 real names, 0.232 neutral, 0.142 swapped). The
ground-truth graphs of that family were written with LLM help, so the names "agree" with the truth by construction, and
a name-reader is rewarded for reading names rather than data. B2 breaks that agreement on purpose and by a controlled
amount: the names suggest one graph (G_N, the CausalArena scenario's own graph) while the data follow another (G_D),
and the two disagree on a fraction rho of edges. Scored against G_D, a pure name-reader's F1 falls linearly as rho
rises; a data-only method's F1 does not depend on rho. The slope (and Spearman correlation) of F1 vs G_D against rho is
a dose-response measure of name reliance.

Prediction P11 (stated before any agent run): Spearman(F1 vs G_D, rho) <= -0.8 for name-readers and near 0 (we use
|rho_s| <= 0.3) for data-only methods.

## 2. Construction (design, fixed before the code was written)

Sources. The 50 CausalArena semantic scenarios (`external/causalarena/scm/semantic/data/semantic_obs_only`), rep000
of each, read with `causalarena_io.load`. From each we take only the names `node_ids` (N) and the true graph `g`
(G_N, row = cause). CausalArena's data values are not used. Each scenario keeps the split `plans/splits.json` gives it
(25 dev, 25 test); every derived file carries it, and nothing derived from a test scenario is used for tuning.

For each source scenario S and each rho in {0, 0.25, 0.5, 0.75, 1.0}:

1. Build G_D from G_N. Let m = |E(G_N)| and k = floor(rho m + 0.5). The edges of G_N are put in one order by a
   permutation seeded by (seed, crc32(slug)) that does not depend on rho, and the first k are broken one at a time,
   each with its own RNG seeded by (seed, crc32(slug), edge position). The breaking is therefore nested: G_D at a
   larger rho breaks the same edges as at a smaller rho, plus more (common random numbers across the dial).
   Breaking edge a -> b (in the current graph):
   - reverse: replace it by b -> a if that keeps the graph acyclic (no other path a ~> b);
   - otherwise rewire: delete it and add c -> b (a new cause for the same effect), else a -> c (a new effect for the
     same cause), else any u -> v, choosing uniformly among pairs that are adjacent neither in G_N nor in the current
     G_D and keep the graph acyclic. Edge count and acyclicity are kept.
   Unbroken edges are untouched. No broken edge can coincide with a G_N edge (a reversal of a DAG edge is never a DAG
   edge of the same graph; a rewired edge joins a pair not adjacent in G_N). So the names-implied direction accuracy
   on G_D, the share of G_D edges that are G_N edges, is exactly (m - k)/m = 1 - rho up to the rounding of k
   (|error| <= 0.5/m); the generator asserts it for every file.
   `edge_agreement[i, j]` (G_D edge positions only): 1 = the names agree (same edge in G_N), -1 = reversed (G_N has
   j -> i), -2 = rewired (G_N has no edge on that pair); 0 = no G_D edge.
2. Sample n = 1000 observational rows from G_D, two mechanism tracks, 5 replicates (seeds) per (S, rho, track):
   - `linear`: X_j = sqrt(r_j) * s_j / sd(s_j) + sqrt(1 - r_j) * e_j / sd(e_j), with s_j = sum_i w_ij X_i over the
     G_D parents, w_ij = sign * U[0.5, 2] (sign +/- with probability 1/2), e_j Gaussian. The weights are relative
     weights; the factor sqrt(r_j)/sd(s_j) keeps every marginal variance at 1 (the noise variance is 1 - r_j). This is
     the standardised (iSCM-style) form, chosen so the causal order cannot be read off variance accumulation; r_j, the
     share of a node's variance explained by its parents, is drawn per node from U[0.5, 0.9].
   - `nonlinear` (additive noise): the same form with s_j = sum_i w_ij h_ij(X_i), h_ij drawn per edge from
     {tanh(x), x^2 - 1} with probability 1/2 each (a mix), and e_j drawn per node as Gaussian or uniform with
     probability 1/2 each.
   Roots: X_j = e_j / sd(e_j). sd is the sample standard deviation over the n rows, so the formula is exact in the
   sample. Seeds: each variable's noise vector (and, nonlinear, its noise type) comes from an RNG seeded by
   (seed, crc32(slug), track, replicate, variable), so it is the same at every rho; the mechanism draws (r_j per node;
   weight, sign and h per edge) come from blake2b streams keyed by (seed, crc32(slug), track, replicate, attempt,
   variable identity), so at attempt 0 an unbroken edge has the same weight at every rho.
   **R2-sortability matching (design revision after a dev-only pilot, before the full run).** The pilot (8 dev
   scenarios, 1 replicate) showed the linear track's path-weighted R2-sortability against G_D falling with rho, 0.46 at
   rho 0 to 0.32 at rho 1: reversing edges turns CausalArena's many-parent sinks into many-child roots, and a root
   with many children is well predicted by them (high R2 given all other columns). That is a rho-dependent shortcut,
   so the generator now redraws the mechanism (attempt 1, 2, ...; the noise vectors are kept) until both the
   path-weighted and the edge-only R2-sortability against G_D are within 0.05 of 0.5, keeping the closest draw after
   100 attempts. The attempt used is recorded per file. With it the pilot was flat (linear 0.50, 0.48, 0.50, 0.48,
   0.50 across rho, with an earlier RNG layout). Only dev scenarios were used in the pilot.
   Columns are then standardised (mean 0, sd 1) and permuted with a recorded per-file seed (never causal order).
3. Release format: one compressed npz per file, readable by `causalarena_io.load` unchanged:
   `x` (n, d, 2) float32 (channel 0 values, channel 1 the intervened flag, all 0), `g` = G_D (row = cause) in the
   shuffled column order, `node_ids` = names in that order, `g_names` = G_N in the same indexing, `edge_agreement`
   (d, d) int8, `n_obs` = [1000], `n_int` = [0], plus `mask` (all 1) and `f` = [d] as in CausalArena's files, and
   `metadata_json` (source scenario and file, domain, slug, rho, k, m, break counts, track, replicate, every seed,
   split, generator version, sha256 of the generator script, column permutation). The zip entries carry a fixed
   timestamp so a rerun reproduces identical bytes.
4. Files go to `external/b2_namereliance/{track}/rho{xx}/b2_{track}_rho{xx}_{slug}__rep{r}.npz` (xx = 100 rho) with a
   `MANIFEST.json` holding the sha256 of every file; `--check` re-hashes them and checks the generator hash. The data
   are outside git (`external/`), never in the kit.

Leakage checks reported for every file (section 4): varsortability and R2-sortability against G_D (path-weighted and
edge-only, the functions of `sortability_audit.py`), the share of G_D edges that run earlier column -> later column,
and the names agreement. Target: sortabilities near 0.5 and flat across rho.

## 3. Parameters

| Parameter | Value |
|---|---|
| sources | 50 CausalArena semantic scenarios, rep000; d = 17..25, m = 26..67 edges |
| rho | 0, 0.25, 0.5, 0.75, 1.0; k = floor(rho m + 0.5) edges broken |
| tracks | linear (Gaussian noise), nonlinear (tanh / x^2 - 1 mix, Gaussian or uniform noise) |
| n | 1000 observational rows, 0 interventional |
| replicates | 5 per (scenario, rho, track) |
| weights | sign x U[0.5, 2], relative; parent signal rescaled so the explained share is r_j ~ U[0.5, 0.9] |
| R2 matching | redraw mechanism until R2-sortability (paths and edges) vs G_D is within 0.05 of 0.5; at most 100 draws |
| marginal variance | 1 (exact in sample before the final standardisation) |
| master seed | 20261012 (`--seed`) |
| files | 50 x 5 x 2 x 5 = 2500 |

What each rho means: at rho = 0 the names are the data's graph (CausalArena's own setting, with fresh data); at 0.25
one edge in four of G_D is not a G_N edge (reversed where possible, otherwise moved); at 0.5 half; at 0.75 three in
four; at 1.0 no G_D edge is a G_N edge, so a reader that returns G_N scores F1 = 0 against the data.

## 4. Release and leakage checks (full run, 2026-10-12)

2500 files (50 scenarios x 5 rho x 2 tracks x 5 replicates), 257.7 MB (257,728,783 bytes) under
`external/b2_namereliance/`, plus `MANIFEST.json` (sha256 of every file, generator sha256) and `leakage_checks.json`
(every file's checks). 1250 files derive from dev scenarios and 1250 from test. Generation took 3 min 4 s of CPU
(7 min 20 s wall on the shared machine). `--check` re-hashes all 2500 files: 0 mismatches, 0 unlisted, generator hash
matches. Determinism: regenerating 3 scenarios (150 files) into a fresh folder gave 150 of 150 identical sha256.

Sortability and order checks by track and rho (means over 250 files per cell; R2 against G_D; summary in
`analysis/results/b2/b2_sortability.json`):

| track | rho | varsort. (paths) | R2-sort. paths (sd) | R2-sort. edges | R2-sort. paths vs G_N | earlier col -> later col share | names agreement |
|---|---|---|---|---|---|---|---|
| linear | 0 | 0.500 | 0.491 (0.031) | 0.500 | 0.491 | 0.509 | 1.000 |
| linear | 0.25 | 0.500 | 0.496 (0.031) | 0.494 | 0.521 | 0.497 | 0.747 |
| linear | 0.5 | 0.500 | 0.497 (0.029) | 0.489 | 0.542 | 0.502 | 0.494 |
| linear | 0.75 | 0.500 | 0.496 (0.034) | 0.483 | 0.575 | 0.487 | 0.247 |
| linear | 1 | 0.500 | 0.493 (0.041) | 0.473 | 0.600 | 0.505 | 0.000 |
| nonlinear | 0 | 0.500 | 0.499 (0.030) | 0.506 | 0.499 | 0.496 | 1.000 |
| nonlinear | 0.25 | 0.500 | 0.501 (0.029) | 0.500 | 0.496 | 0.506 | 0.747 |
| nonlinear | 0.5 | 0.500 | 0.503 (0.029) | 0.498 | 0.507 | 0.492 | 0.494 |
| nonlinear | 0.75 | 0.500 | 0.499 (0.027) | 0.499 | 0.509 | 0.494 | 0.247 |
| nonlinear | 1 | 0.500 | 0.501 (0.029) | 0.495 | 0.496 | 0.516 | 0.000 |

- Varsortability is 0.5 in every file (standardised columns, as expected). Path-weighted R2-sortability against G_D is
  0.49 to 0.50 in every cell, flat in rho; the edge-only version drifts slightly on the linear track (0.50 to 0.47).
  142 of 2500 files (125 linear, 58 of them at linear rho 1) found no draw inside the 0.05 band in 100 attempts and
  keep the closest draw; the per-file range of path R2-sortability is 0.33 to 0.58 (CausalArena's own semantic files:
  0.14 to 0.91, mean 0.54).
- Column order: the share of G_D edges running from an earlier to a later column is 0.49 to 0.52 in every cell (max
  per file 0.79); in CausalArena's released order it is 1.
- Name agreement (share of G_D edges that are G_N edges) equals 1 - rho to within 0.5/m in every file (asserted at
  generation). Of the broken edges, 61 to 62% are reversals and the rest are rewired to a new cause of the same effect
  (no rewire needed the fallbacks).
- Observation: on the linear track R2-sortability measured against G_N (not G_D) rises with rho to 0.60 at rho 1. An
  R2-ordering heuristic would therefore drift slightly towards the names' direction at high rho; it does not affect
  scores against G_D, but agents that sort by R2 could look marginally more name-following at rho 1.
- Identifiability: the CPDAG of G_D (the ceiling for any observational data-only method; undecided pairs at random)
  scores F1 0.958, 0.945, 0.951, 0.949, 0.939 against G_D across rho on the 25 dev scenarios (oriented share of edges
  0.91 to 0.89), so the graphs do not become harder to orient as rho rises.

## 5. Reference results (dev split only)

Scorer: `analysis/b2_score.py`; rows in `analysis/results/b2/`, scores in `b2_reference_scores.json` and
`b2_pc_dev25_scores.json`. Directed F1 vs G_D under the random rule (seed crc32(file name)).

Names oracle (returns G_N; 25 dev scenarios x 5 rho x 2 tracks x rep000, 250 files):

| rho | 0 | 0.25 | 0.5 | 0.75 | 1 |
|---|---|---|---|---|---|
| F1 vs G_D | 1.000 | 0.747 | 0.495 | 0.245 | 0.000 |
| F1 vs G_N | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| name-following share | | 1.00 | 1.00 | 1.00 | 1.00 |

Spearman(F1 vs G_D, rho) = -0.989 over files (OLS slope -1.00 per unit rho): name-reader pattern.

Data-only: PC (causal-learn 0.1.4.8 upstream, stable, Fisher-z, alpha 0.05). GES from the `ges` package was the
first choice but took over 2 minutes on a single d = 25 file on the shared machine, so PC was used. Specified subset:
6 dev scenarios (the first listed of each of the first 6 dev domains), rep000; the nonlinear track was added because
it was cheap. Extension: all 25 dev scenarios, linear, rep000.

| PC | rho 0 | 0.25 | 0.5 | 0.75 | 1 | Spearman over files | slope |
|---|---|---|---|---|---|---|---|
| linear, 6 scenarios: F1 vs G_D | 0.610 | 0.620 | 0.647 | 0.615 | 0.489 | -0.29 (p 0.12) | -0.10 |
| nonlinear, 6 scenarios: F1 vs G_D | 0.362 | 0.350 | 0.384 | 0.376 | 0.365 | +0.11 (p 0.55) | +0.01 |
| both tracks, 6 scenarios (60 files) | | | | | | -0.05 (p 0.69) | -0.04 |
| linear, 25 scenarios: F1 vs G_D | 0.570 | 0.613 | 0.586 | 0.606 | 0.535 | -0.09 (p 0.31) | -0.03 |
| linear, 25 scenarios: F1 vs G_N | 0.570 | 0.505 | 0.371 | 0.269 | 0.204 | | |
| linear, 25 scenarios: name-following share | | 0.18 | 0.14 | 0.15 | 0.19 | | |

P11 on the reference methods: holds. The perfect name-reader gives rho_s = -0.99 (<= -0.8); the data-only method
gives |rho_s| <= 0.3 in every cut (-0.29 on the specified 6-scenario linear subset, which is close to the limit;
-0.09 on all 25 dev scenarios). One caveat: PC's linear F1 at rho 1 is lower than at the other levels (0.535 against
0.57 to 0.61 on 25 scenarios; 0.489 on the 6-scenario subset), while the CPDAG ceiling drops by only 0.02. So a
data-only method can lose about 0.05 at rho 1 for reasons that have nothing to do with names (likely finite-sample
faithfulness on the reversed, many-child-root structures, together with the R2-matched draws). A data-only method also
"follows the names" on about 15 to 19% of disputed arrows through ordinary orientation errors; that is the floor for
the name-following share, not 0.

## 6. Intended use (AB-06)

Agents under audit (Causal-Copilot and the other LLM-using systems) are run on B2 files in AB-06, with the values and
`node_ids` only (the harness must never pass `g`, `g_names`, `edge_agreement` or `metadata_json` to an agent).
For each agent: F1 vs G_D by rho, Spearman and slope against rho, F1 vs G_N, and the name-following share, compared
with the data-only reference run on the same files. Name reliance is reported as the agent's slope minus the data-only
slope (difference in slopes, which removes the small rho-1 dip common to data methods), with rho 0 to 0.75 as a
sensitivity cut. Tuning (prompts, thresholds) uses dev files only; test files are for the final measurement.
Suggested budget: rep000 of the 25 test scenarios x 5 rho x 1 track = 125 agent runs per agent, the linear track
first.

## 7. Limitations

- Names from CausalArena semantic scenarios were LLM-drafted, and so were their graphs. G_N is therefore exactly what
  an LLM would tend to propose; this makes the benchmark sharp for LLM name-readers but also means rho 0 rewards them
  maximally, as CausalArena itself does.
- Rewired edges may create name-implausible pairs that a reader could detect (for example a new cause of an outcome
  from an unrelated subsystem). About 38% of broken edges are rewires; a sophisticated reader may treat them as
  implausible and drop them, which would raise its precision against G_D without reading data.
- Agents that also read data could notice the disagreement, which is exactly what we want to measure: an agent that
  checks names against the data should keep a flat curve, and the name-following share separates "followed the names"
  from "followed the data" on disputed pairs.
- Reversed edges keep the skeleton. A pure name-reader therefore keeps the skeleton right at every rho and loses only
  orientation on reversed edges (and both adjacency and orientation on rewired ones); adjacency F1 falls by less than
  directed F1.
- Mechanisms are synthetic (iSCM-style linear-Gaussian and tanh / quadratic additive noise), not CausalArena's
  semantic generator specs. The data at rho 0 are therefore a fresh draw from G_N, not CausalArena's files.
- R2-sortability is matched by selecting among seeded mechanism draws. This removes the rho-dependent R2 shortcut on
  average, but the selection is on a statistic of the sample, and the edge-only R2-sortability on the linear track
  still drifts slightly (0.50 to 0.47). R2-sortability against G_N rises to 0.60 at linear rho 1 (section 4).
- Data-only flatness was checked with one method (PC) on dev files, rep000 only, and PC shows a small dip at rho 1.
  GES was not run (too slow on this machine).
- `controls.names = "decoupled (rho dial)"` is not yet in `score_record.NAMES`, so `check_scores.py` will reject this
  results folder until that value is added. It is the only contract problem left: `check_contract` reports nothing else.
