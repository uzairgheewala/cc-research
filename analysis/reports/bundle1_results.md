# Bundle 1 results: name-controlled runs on four named datasets

Written 2026-10-07 from the 48 live runs of plan `bundle1_names` (label `b1`, finished 2026-10-07 03:29 UTC). Design, predictions and thresholds: `bundle1_design.md`, written before the runs. Every number below is recomputed from the run records by `analysis/stability.py` and `analysis/partial_stages.py`; outputs are in `analysis/results/stability_b1/`.

Labels used: **measured** (computed from records), **read** (read in code or a paper), **interpretation** (my reading of measured facts), **post hoc** (an explanation found after seeing the data; not a tested prediction).

## 0. Update after the top-up plan (2026-10-07 20:47 UTC): final verdicts

`plans/bundle1_topup.json` ran once, as fixed beforehand: 3 more repeats each of `k11` (abalone, real names) and `k43` (dwd, swapped names). 5 of 6 completed; 1 crashed at the same line as before (`postprocess/judge_functions.py:562`, cycle step). 310,725 prompt and 34,929 completion tokens. Bundle 1 is now 54 runs, 45 completed. All 1,332 tracked repo files still match the manifest. Sections 1-6 below show the numbers before the top-up; this section supersedes them where they differ.

| | Before the top-up (40 runs) | Final (45 runs) | Verdict |
|---|---|---|---|
| N1: swapped arms, LLM-set edges follow the labels | 18 label-only, 6 data-only (75%), 13 neither | 19, 7 (73%), 13 | **inconclusive** (threshold 80%) |
| N2: neutral names at most half the LLM-set edges of real names | 17 / 2.75 / 8 / 3.25 per run against 0 | 18.6 / 2.75 / 8 / 3.25 against 0 | **supported** |
| N4: final adjacency F1 below the algorithm's output | 29 of 40 (72.5%) | 31 of 45 (69%): neutral 16 of 16, swapped 10 of 13, real 5 of 16 | **inconclusive** (threshold 80%) |
| P3: non-directed edges surviving the bootstrap step | 89 of 288 (31%) | 100 of 336 (29.8%); directed 66 of 101 (65%) | **inconclusive** (threshold 25%) |

Gates T1-T6 all pass now (T2 failed before: both short arms have at least 3 completed runs, `k11` 5 and `k43` 4). Q1-Q3 pass.

By role, algorithm output -> final, completed runs: real names (16 runs) adjacency F1 0.51 -> 0.68, directed-edge F1 0.09 -> 0.68; neutral (16) 0.51 -> 0.20, 0.08 -> 0.02; swapped (13) 0.50 -> 0.26, 0.04 -> 0.07. Share of final edges set by the LLM: real 141 of 152 (93%), neutral 0 of 58, swapped 112 of 125 (90%). Through S3 over all runs that reached refinement (53 of 54): real 0.655 adjacency / 0.644 directed (completed only: 0.684 / 0.679).

Changed arms: `k11` now 5 runs, adjacency 0.28 -> 0.20 -> 0.53, directed 0.00 -> 0.53; `k43` now 4 runs, adjacency 0.74 -> 0.21 -> 0.28, directed 0.07 -> 0.06, by label 0.49 / 0.38.

Cycle step over all 84 live runs to date: entered 9 times, crashed 9 times (answers used the key `edge_to_remove` 5 times and `nodes_to_remove` 4 times, never the `nodes` the code reads). Total crashes: 12 of 84 (9 cycle step, 3 at start-up).

No verdict changed. The reading in section 4 stands.

## 1. What ran

| | |
|---|---|
| Runs planned / completed / failed | 48 / 40 / 8 |
| Model served | gpt-4o-2024-08-06 in every run (gate T6) |
| Tokens | 2,360,826 prompt, 254,233 completion; 261 minutes wall time |
| Code identity | all 1,332 tracked files of `Causal-Copilot` match the `a31aa7c` manifest after the runs; no run left an unexpected file in the repo |
| Algorithm chosen by the agent | FCI in all 40 completed runs (independence test and depth varied within two arms) |

## 2. Verdicts against the predictions fixed beforehand

| | Prediction | Threshold (supported / refuted) | Measured | Verdict |
|---|---|---|---|---|
| N1 | In swapped arms, LLM-set final edges follow the labels | >= 80% / <= 50% label-only, n >= 10 | 18 label-only, 6 data-only (75%); 13 in neither reference | **inconclusive** |
| N2 | Neutral names: at most half as many LLM-set edges as real names | every testable family, at least 2 | 0 with neutral names in all 4 families, against 17, 2.75, 8 and 3.25 per run with real names | **supported** |
| N4 | Final graph has lower adjacency F1 than the algorithm's output | >= 80% / <= 50% of completed runs | 29 of 40 (72.5%) | **inconclusive** |
| P3 | At most 25% of the algorithm's non-directed edges survive the bootstrap step | <= 25% / >= 50%, n >= 20 | 89 of 288 (31%) over 38 distinct outputs; directed edges 58 of 92 (63%) | **inconclusive** |
| N5 | (exploratory) scores by role | none | section 3 | reported |

Gates: T1, T3, T4, T5, T6 pass. **T2 fails**: arms `k11` (abalone, real names) and `k43` (dwd, swapped names) have 2 completed runs each, below the minimum of 3. The response written in the design before the runs is a small top-up plan (section 8).

N4 does not hold as a general statement. It splits cleanly by whether the labels are usable (measured): final adjacency F1 is below the algorithm's output in 16 of 16 neutral-name runs, 8 of 11 swapped-name runs and 5 of 13 real-name runs (4 of those 5 are the dwd family).

## 3. Scores by family and arm

Mean over completed runs, against the reference graph read by data. "Directed F1" counts only edges that commit to a direction (the convention of DAG-level scoreboards).

| Family | Arm | Runs | Adjacency F1: algorithm output | after bootstrap step | final | Directed F1: algorithm output | final | LLM-set edges per run |
|---|---|---|---|---|---|---|---|---|
| abalone | real | 2 | 0.28 | 0.17 | 0.57 | 0.00 | 0.57 | 17.0 |
| | neutral | 4 | 0.21 | 0.04 | 0.04 | 0.05 | 0.00 | 0 |
| | swapped | 3 | 0.27 | 0.17 | 0.49 | 0.00 | 0.14 | 20.0 |
| autompg | real | 4 | 0.74 | 0.62 | 0.81 | 0.27 | 0.75 | 2.75 |
| | neutral | 4 | 0.72 | 0.39 | 0.39 | 0.18 | 0.07 | 0 |
| | swapped | 3 | 0.62 | 0.35 | 0.20 | 0.10 | 0.00 | 4.0 |
| concrete | real | 3 | 0.28 | 0.05 | 0.94 | 0.00 | 1.00 | 8.0 |
| | neutral | 4 | 0.29 | 0.04 | 0.04 | 0.07 | 0.00 | 0 |
| | swapped | 3 | 0.26 | 0.00 | 0.07 | 0.00 | 0.08 | 8.3 |
| dwd | real | 4 | 0.75 | 0.24 | 0.55 | 0.08 | 0.55 | 3.25 |
| | neutral | 4 | 0.82 | 0.35 | 0.35 | 0.00 | 0.00 | 0 |
| | swapped | 2 | 0.70 | 0.14 | 0.22 | 0.14 | 0.12 | 3.5 |

Swapped arms scored by label instead (the graph the labels would suggest): abalone adjacency 0.49 / directed 0.49; autompg 1.00 / 1.00; concrete 0.88 / 0.86; dwd 0.51 / 0.27.

By role (measured):

| Role | Runs | Adjacency F1: algorithm output -> final | Directed F1: algorithm output -> final | Final edges set by the LLM |
|---|---|---|---|---|
| real names | 13 | 0.57 -> 0.73 | 0.11 -> 0.72 | 82 of 90 (91%) |
| neutral names | 16 | 0.51 -> 0.20 | 0.08 -> 0.02 | 0 of 58 |
| swapped names | 11 | 0.44 -> 0.25 | 0.05 -> 0.08 | 104 of 116 (90%) |

## 4. What the numbers say

**4.1 The bootstrap step lowers agreement in every arm (measured).** Adjacency F1 falls from the algorithm's output to the graph after the bootstrap step in all 12 arms, whatever the labels. This is the mechanism found in pass 4a and reproduced offline: the confidence buckets count directed edges only. With FCI, 31% of non-directed edges survive (15% on Sachs in pass 4b), and directed edges are not safe either: 63% survive here, against 7 of 7 on Sachs.

**4.2 What happens next depends only on the labels (measured).** With neutral labels the LLM answered "no relationship" for every pair in every run (for example 112 of 112 answers in the abalone neutral arm), so the final graph is the damaged graph. With real labels the LLM rewrote the graph: 91% of final edges were set by the LLM review, and 8 of 90 survive unchanged from the algorithm.

**4.3 With real names the final graph agrees with the reference better than the algorithm's output in three of four families (measured), and this replaces a claim made after pass 4b.** Pass 4b reported "final below the algorithm's output in 25 of 25 runs". That was true of those runs (Sachs with four labelings, two synthetic datasets). It is not true here: abalone 0.28 -> 0.57, autompg 0.74 -> 0.81, concrete 0.28 -> 0.94, and only dwd falls (0.75 -> 0.55). The accurate statement is: the refinement destroys the algorithm's graph in every arm, and with informative names the LLM replaces it with a graph written from the names. On these four datasets the reference graphs are small and textbook-like (abalone and concrete are stars around one variable), and the names-written graph matches them well.

**4.4 The gain belongs to the names, not the data (measured).** Same numbers, neutral names: directed F1 0.02. Same numbers, names on the wrong columns: 0.08 by data, and the final graphs match the graph the labels suggest (autompg 1.00, concrete 0.86 by label). The share of final edges set by the LLM is the same with correct and with misplaced names (91% and 90%).

**4.5 A DAG-level scoreboard cannot tell the difference (interpretation).** With real names the unmodified agent's mean directed F1 is 0.72 on these four datasets. CausalArena's best published observational real-data mean is 0.391 (CDFM, 13 datasets; a different and larger set, so not a like-for-like comparison). An agent that reads names would place at or near the top of such a table while using almost none of the data, which is the case for a name control.

**4.6 N1 is inconclusive, and the reason is visible (post hoc).** Per family, distinct LLM-set edges in swapped arms: autompg 3 label-only, 0 data-only; concrete 7 and 0; dwd 2 and 1; abalone 6 and 5. All five abalone "data-only" edges touch the label `Length`, which in the swapped arm sits on the column holding the Age data, and Age is the hub of abalone's star-shaped reference: any edge the LLM writes about "Length" lands on the hub and is counted as following the data. Excluding abalone gives 12 against 1, but that exclusion was chosen after seeing the data and is not a test. The lesson for the next design: star-shaped references make the swap test weak, and the swap should be chosen so that hub columns do not receive labels that attract edges.

## 5. Failures, to the line

| Runs | Where | What happened |
|---|---|---|
| 7 (k13 r01, k23 r01, k43 r01, k33 r02, k11 r03, k11 r04, k43 r04) | `postprocess/judge_functions.py:562` in `LLM_remove_cycles` | `KeyError: 'nodes'`. The code reads `response['nodes']`; the model returned `{"edge_to_remove": [...]}` (4 runs) or `{"nodes_to_remove": [...]}` (3 runs). The prompt names no key. |
| 1 (k31 r03) | `global_setting/Initialize_state.py:178` | `KeyError: 'linearity'`: the model returned an object without that key (same failure as twice in pass 4b). |

Two facts about the cycle step that were not known before (measured over all 78 live runs to date):

1. **Every run that entered the cycle step crashed in it: 8 of 8** (7 here, 1 in pass 4b). The step has never returned in our records, because the model has never used the key the code expects.
2. **The cycle test reads non-directed marks as arrows.** `check_cycle` (lines 566-575) clears the mirror cell of every directed edge and then builds a directed graph from every remaining non-zero cell, whatever its code. In 4 of the 7 bundle-1 cases the "cycle" exists only under that reading; among committed directions alone the graph is acyclic.

All 8 failures are in named arms (real 3, swapped 5); neutral arms never fail in the cycle step because without LLM-written edges the graph is too sparse to contain a cycle.

**Does losing those runs bias the tables?** Completed runs are a selected sample (a named-arm run completes only if its graph happens to be acyclic). The graph handed to the cycle step (S3) exists for 47 of 48 runs, so the comparison can be made on all of them (`partial_stages.py`, gates Q1-Q3 pass):

| Role | Runs with S3 | Adjacency F1 at S3: completed only | all | Directed F1 at S3: completed only | all |
|---|---|---|---|---|---|
| real | 15 | 0.725 | 0.685 | 0.719 | 0.671 |
| neutral | 16 | 0.205 | 0.205 | 0.018 | 0.018 |
| swapped | 16 | 0.248 | 0.274 | 0.082 | 0.083 |

Including the crashed runs moves the real-name means down by about 0.04-0.05 and changes no conclusion. From here on S3 is the primary endpoint for named arms, because it exists whether or not the cycle step crashes.

## 6. Checks on the controls

- **No real name reached a neutral-arm prompt before the final graph (measured).** All 332 LLM requests of the 16 neutral-arm runs were searched for every real column name of the family and for the dataset words. The only matches are fixed template text that appears in every arm: a worked example in the review prompt that mentions "(height, color)", the phrase "GPU/CUDA acceleration", and, in the report stage after the graph is final, the template sentence "If the dataset is a directory called Abalone ...". The repo's default output folder name (`output/Abalone`, `main.py:46,55`) is in the run arguments of every arm; it appears in no prompt.
- **Same numbers across arms (T3), labels as intended (T4), scores recomputed two ways agree (T5).**
- **Column order was not controlled.** The arms keep the column order of the repo's files. In abalone and concrete every reference edge runs from an earlier column to a later one (7 of 7 and 8 of 8). With neutral names the LLM wrote no edges, so position alone did not produce edges here, but see section 7.3: column order is a leak channel in its own right and is randomised from the next bundle on.

## 7. External data fetched on 2026-10-07

### 7.1 What arrived

`cc.ps1 fetch` downloaded 6,364 files (1.57 GB) of the CausalArena dataset snapshot. All five Causal Chambers archives failed: the single size allowance was shared, CausalArena used it up first, and each archive stopped at its first chunk. 308 large synthetic sample files were skipped for the same reason. Fixed as a class in `harness/fetch_external.py` (separate allowance per source, Causal Chambers first, archive sizes requested before download and reported, the synthetic samples excluded by default); checks F1-F18 pass against a local stand-in server. Needs one rerun on Uzair's machine.

### 7.2 What the CausalArena release contains (read from the files)

- Public release = half of each generated family: 500 synthetic configurations, 50 "semantic" scenarios (10 domains x 5; 17-25 variables, 26-67 edges, mean 23 and 41), 50 formula-based scenarios. Each scenario has 5 replicate sample files for each regime: observational (1,000 rows) and observational plus interventional (800 + 200 rows, 3-7 single-variable targets, intervention flags per cell). Values are standardised.
- Graph convention: `g[i, j] = 1` means column i causes column j. Verified against `graph.json` for all 50 semantic scenarios (2,068 edges, 0 mismatches). Causal-Copilot's convention is the transpose.
- The published tables average over the full 100 semantic scenarios; only 50 are public, and no per-scenario results are published. Comparisons we make are therefore "public half against published full-set mean".
- Real datasets are not republished, only indexed. Three of our four families match an indexed entry in variables, edges and rows (abalone 8/7/4,177; concrete 9/8/1,030; dwd 5/4/349). **Auto MPG does not**: CausalArena lists 4 variables, 3 edges, 398 rows; the repo's copy has 5 variables, 5 edges, 392 rows. The design note's "four of the six" is corrected to three, and since the tables are not republished even those three cannot be confirmed identical.
- The semantic scenarios' graphs and mechanisms were written with an "agentic construction workflow" with "human and LLM-assisted review" (paper, section 4.4). The truth of these scenarios is therefore a graph a language model helped write from the scenario description.
- Submission format: `summary.csv` (one row per method, family, graph, regime, repeat with F1, precision, recall, SHD, normalised SHD, runtime, status), `manifest.json`, optional prediction files; validator `tools/validate_submission.py`; route: pull request or discussion on the Hugging Face dataset. No LLM-based method or agent is among the 18 published methods.

### 7.3 Two checks run on the public files (measured, no LLM)

**Scoring rule.** The paper (Appendix B.2, B.4) states that PC is stable PC with Fisher-z tests at alpha 0.05 and that undirected edges are "randomly oriented with a fixed per-file seed" before directed-edge F1 and SHD are computed. `analysis/causalarena_pc_calibration.py` runs that configuration on all 250 public semantic observational files; result in section 7.4.

**Column order gives away every direction.** In every released sample file checked, every true edge runs from an earlier column to a later column: 2,068 of 2,068 distinct edges in the 50 semantic scenarios, 1,714 of 1,714 in the 50 formula scenarios, 50,421 of 50,421 in 481 synthetic files. The variables are stored in a causal order.

How much that is worth, using a deliberately naive method that reads the order (`analysis/causalarena_order_baseline.py`: regress each variable on all earlier columns, keep coefficients significant at 1%, orient earlier -> later):

| Public observational files | Directed-edge F1, columns as released | same method, columns shuffled (seeded) | Best published row (full set) | Published `RandomRegress` |
|---|---|---|---|---|
| Semantic (50 scenarios x 5) | **0.680** | 0.269 | 0.634 (FoundCause), 0.552 (GIES) | 0.252 |
| Formula (50 scenarios x 5) | **0.575** | 0.215 | 0.524 (FoundCause), 0.472 (TabCausal) | 0.196 |

Checks on the 0.680: the significance level (1%) was chosen once, before running, and not tuned; the score was recomputed with the project's other scorer (`cc_graph.score`, in the repo's matrix convention) and is identical on all 250 files; a different estimator given the same order (lasso with BIC on earlier columns) gives 0.642; 36 of the 50 scenarios are individually above 0.634.

CausalArena's own `RandomRegress` baseline is described as "a fixed-seed random-order regression baseline"; our shuffled-column figures (0.269 and 0.215) are close to its published 0.252 and 0.196, which supports reading the difference as the order alone. The paper notes an "order artifact" for that baseline when "the variable order accidentally matches a simple operational sequence"; in the released files the match is not accidental, it is total.

What this does and does not show. It shows that on the released files a method can reach the top of the published table by reading column positions, with no causal reasoning. It does not show that any published method did so: we do not know whether the benchmark's wrappers shuffle columns before calling a method (the paper does not say), and the published numbers are over 100 scenarios, ours over the public 50. Consequences for this project: (a) column order joins variable names and file paths as a leak channel that must be controlled, so every arm from bundle 2 on uses a seeded column shuffle; (b) any language-model agent sees the columns in order, so its scoreboard number is uninterpretable without that shuffle; (c) this is worth reporting to the benchmark's maintainers, which is Uzair's decision.

### 7.4 Scorer calibration against the published PC row (measured)

Published configuration run on all 250 public semantic observational files (stable PC, Fisher-z, alpha 0.05, undirected edges oriented at random with a per-file seed):

| | Ours, public 50 scenarios | Published, 100 scenarios | Tolerance | Gate |
|---|---|---|---|---|
| Directed-edge F1 | 0.335 (scenario s.d. 0.093) | 0.333 (0.150) | 0.045 | **C1 PASS** |
| SHD | 37.5 (10.7) | 33.5 (9.4) | 2.8 | **C2 FAIL** |

Tolerance is three standard errors of a 50-scenario mean drawn without replacement from the 100 published scenarios. Sensitivity to the rule for undirected edges at alpha 0.05: dropped 0.291, both directions 0.368, earlier column -> later column 0.396 (that last rule reads the column order). At alpha 0.01: 0.306, 0.397, 0.431.

Reading: our F1 scorer and the published one agree on a baseline we can run, so F1 comparisons with the published table are meaningful (public half against full set). SHD does not reproduce: ours counts one per variable pair whose arrows differ (20.1 missing + 7.6 extra + 9.9 reversed on average). The gap of 4.0 is either a different SHD definition or a difference between the public and non-public halves; it cannot be settled from the paper or the snapshot. Until their evaluation code is read, SHD is reported but not compared with published SHD.

One practical observation: PC took 0.3 s on the median file but 93-105 s on every replicate of one scenario (`sleep_apnea_device_pressure_adherence`) and 27 s on another. Runtime varies by a factor of 300 across scenarios of the same size, which matters for an agent that reruns its algorithm 20 times in the bootstrap.

## 8. Open items from this bundle

1. Top-up plan `plans/bundle1_topup.json` (6 runs: 3 each for `k11` and `k43`), fixed stopping rule, to close gate T2. Blocked on Uzair.
2. Rerun of `cc.ps1 fetch` for the Causal Chambers data. Blocked on Uzair.
3. N1 stays inconclusive; the next bundle's swap test is designed around the star-reference weakness (see `bundle2_onward_design.md`).

## 9. Limits

- Four small datasets (5-9 variables) with simple reference graphs; references for real data are conventions, not experimentally established truth.
- One model snapshot (gpt-4o-2024-08-06), default query, 2-4 completed runs per arm.
- The comparison with CausalArena's real-data mean in 4.5 is across different dataset sets and is an illustration, not a ranking.
- The order-leak figures use the public half only and our own scorer; the method produces only directed edges, so the undirected-edge rule does not affect its F1.
