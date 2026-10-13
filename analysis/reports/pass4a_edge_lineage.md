# Pass 4a: where each edge in the final graph comes from

Question: for every pair of variables, which step of the refinement stage set its final status, and on what evidence? Baseline `a31aa7c`. Tools: `lineage.py` (per run), `refinement_offline.py` plus its two report scripts (no LLM), `encoding_consumers.py` (micro-tests).

Stage names used throughout: S0 = what the chosen algorithm returned; S1 = after the bootstrap edits (`postprocess/judge.py:68-86`); S2 = after the LLM review; S3 = after KCI pruning; S4 = after the cycle step (the "revised graph").

## 1. Method and gates

`lineage.py` reads one recorded run. It re-states each refinement step independently of the repo code, replays the recorded evidence through it, and compares with what the run actually produced.

| Gate | Check | Linear_Gaussian golden run | sachs golden run |
|---|---|---|---|
| A | S0 equals the state's `converted_graph` | PASS | PASS |
| B | graph rebuilt from the bootstrap buckets and LLM answers equals the graph the run passed to KCI | PASS | PASS |
| C | rebuilt graph after KCI removals equals the graph the run passed to the cycle step | PASS | PASS |
| D | the cycle step's output equals the state's `revised_graph` | PASS | PASS |
| E | every pair whose status changed is covered by recorded evidence of the step that changed it | PASS | PASS |
| F | every LLM answer names variables of the dataset | PASS | PASS |

Gates B and C are the important ones: they show that my reading of the code predicts the run's intermediate graphs exactly, cell for cell. A reading that was wrong anywhere would fail them.

Per-run outputs: `results/lineage/<run_id>/lineage.md` and `lineage.json`.

## 2. FACTS from the two live runs (gpt-4o, one run each)

Linear_Gaussian (5 variables, one true edge X2 -> X4; the LLM chose XGES):
- S0 was the single edge X2 --- X4, undirected. That is the correct answer for an algorithm that can only identify the equivalence class: adjacency F1 1.00, distance to the true CPDAG 0.
- The bootstrap found that undirected edge in 19 of 20 resamples (0.95). The bootstrap step deleted it, because the rule reads only the frequency of the directed form (0.00 to 0.05).
- The LLM answered D ("uncertain") for all 10 pairs, and also answered about 5 self-pairs such as (X1, X1).
- Final graph: empty. Adjacency recall 0, distance to the true CPDAG 1.

sachs (11 proteins; the LLM chose FCI with alpha 0.05, the `rcit` test, depth 4):
- S0: 9 circle-circle edges and 1 "associated" edge. Against the repo's reference graph: adjacency precision 0.90, recall 0.47, F1 0.62.
- The bootstrap step deleted all 10. Example: PKC o-o P38 had that exact status in 16 of 20 resamples.
- The LLM answered about all 55 pairs and 11 self-pairs in 11 calls: A (left causes right) 6, C 28, D 21. Its 6 A answers became 6 directed edges.
- Final graph: 6 directed edges, every one set by the LLM, none identical to what the algorithm returned. Adjacency precision 0.83, recall 0.26, F1 0.40. Four match the reference direction, one is reversed (PIP2 -> PIP3; the reference has PIP3 -> PIP2), one is absent from the reference (P38 -> Jnk).
- Two of the six, Mek -> Erk and PIP3 -> Akt, are between pairs the algorithm did not connect, and for which 19 of 20 and 20 of 20 resamples showed no edge.
- KCI pruning removed nothing. No cycle was found.

Paper comparison:
- PAPER CLAIM (section 2.4): "Moderate-confidence edges are passed to the LLM". CODE VERIFIED and seen live: every pair is passed, including pairs of a variable with itself. `judge_functions.py:236` puts every low-frequency directed entry into the review bucket, and almost every entry is low-frequency.
- PAPER CLAIM (section 2.4): LLM recommendations "are not permitted to override high-confidence decisions made by the bootstrap procedure". APPARENTLY DIVERGENT, seen live: `judge.py:88` creates `fixed_pairs = []` and never fills it, and two LLM additions went against 0.95 and 1.00 no-edge frequencies.

## 3. FACTS from the offline experiment (no LLM, no cost)

Design: for each dataset and algorithm, call the repo's own `fit`, `bootstrap` (20 resamples), `bootstrap_recommend` and `kci_pruning` with wrapper-default hyperparameters, and apply the bootstrap edits with the function that passed gate B. 10 datasets with ground truth or a reference (4 bundled, 6 from the repo's simulator), up to 18 algorithms, seed 0: 113 cells, 96 completed. Seeds 1 and 2 were added for 7 algorithm families: 140 more cells, all completed. Tables: `results/offline/refinement_offline.md` and `refinement_offline_seeds.md`.

Survival of an algorithm-output edge through the bootstrap step, by the edge's type (seed 0, all cells):

| Type in S0 | Edges | Still adjacent in S1 |
|---|---|---|
| directed | 361 | 347 (96%) |
| undirected | 204 | 32 (16%) |
| circle-circle | 24 | 3 (12%) |
| bidirected | 8 | 1 (12%) |
| circle-arrow | 8 | 2 (25%) |

Across seeds 0, 1 and 2 (59 dataset-algorithm combinations complete for every seed): directed 97-98%, undirected 8-11%, circle-circle 12-17%.

Adjacency F1 before and after the bootstrap step, mean over datasets, mean over three seeds:

| Algorithm | Output class | S0 | S1 | Datasets worse in every seed | Better in any seed |
|---|---|---|---|---|---|
| PC | CPDAG | 0.86 | 0.44 | 8 of 9 (the ninth is worse in two of three seeds) | 0 |
| GES | CPDAG | 0.88 | 0.35 | 9 of 9 | 0 |
| GRaSP | CPDAG | 0.88 | 0.34 | 9 of 9 | 0 |
| XGES | CPDAG | 0.87 | 0.43 | 8 of 8 | 0 |
| FGES | CPDAG | 0.82 | 0.40 | 8 of 8 | 0 |
| FCI | PAG | 0.85 | 0.30 | 8 of 8 | 0 |
| DirectLiNGAM | DAG | 0.76 | 0.76 | 0 of 8 | 2 |

Seed 0 only: ICA-LiNGAM 0.86 to 0.86 and NOTEARS-linear 0.83 to 0.83 (both always return fully directed graphs).

Other facts:
- In every completed cell and every seed, the list sent for LLM review contained every pair and every self-pair.
- KCI pruning removed 8 edges in all of seed 0 (DirectLiNGAM 4, NOTEARS-linear 3, InterIAMB 1).
- Micro-tests on single-edge graphs (`results/encoding/encoding_consumers.md`): each of the six non-directed codes is deleted by the bootstrap step even when it appears in 100% of resamples; KCI pruning examines only cells above the diagonal, so an edge stored below the diagonal is never tested; the "associated" code is not counted by the bootstrap tally at all and is described to the LLM by an empty sentence.

## 4. A correction to an earlier ledger entry: the bootstrap is not random from run to run

Earlier I recorded the bootstrap as unseeded. The code does not seed it, but the process does:

- CODE VERIFIED (traced in my sandbox): importing the pipeline imports `semopy`, and `semopy/model_generation/parameters.py:22` calls `random.seed(123)` at import time. `bootstrap_iteration` draws its resample with `random.choices` from that same generator, and the CLI runs the bootstrap in the main process (`parallel=False`).
- Seen in records: the initial state of Python's generator is identical in all three Docker runs (dry run and both golden runs) and in every sandbox run. In three repeated stub runs on the same data, all 20 resampled graphs were identical run to run.
- Consequence: for a given dataset, algorithm and hyperparameters, the "bootstrap confidence" is a fixed number, not a fresh sample. Repeating a run does not average it out. Run-to-run variation in live repeats should therefore come from the LLM's choices and from any algorithm that uses numpy's generator, which is not seeded.
- UNCLEAR until pass 4b: whether this holds when the LLM's query parse changes the path through the statistics step (that step also draws from the same generator, so a different path would shift the resamples).

My offline seeds 0-2 deliberately vary the resample draw, so the offline result above is not an artefact of the one draw the pipeline happens to use.

## 5. INFERENCES

- I4.1 The bootstrap step treats "not found as a directed edge" as "not found". For any algorithm whose correct output contains undirected or circle marks, it removes most of the correct answer. The measured loss is large and one-sided: in 50 of 51 CPDAG/PAG combinations adjacency F1 fell in every seed, and it never rose.
- I4.2 After that deletion, the LLM review is the only route by which an edge can return, and it returns as a directed edge. On sachs the final graph is, in effect, the LLM's answer to 55 questions about protein names.
- I4.3 The two live runs are single runs. They show that the mechanism operates in production; they do not estimate how often.
- I4.4 Fully directed outputs (LiNGAM family, NOTEARS) pass through the bootstrap step almost unchanged. The damage is specific to equivalence-class outputs, which is the output class of the algorithms the LLM selected in both live runs.

## 6. Threats to validity

- Offline cells use wrapper-default hyperparameters, not LLM-chosen ones.
- 8-variable simulated graphs and four small bundled datasets; no large or nonlinear settings.
- Torch-based wrappers (GOLEM, CORL, NOTEARS-nonlinear, Hybrid) could not run in my sandbox and are missing. One HITON-MB cell failed with an index error inside the wrapper.
- The sachs reference graph is the repo's `base_graph.npy` (19 edges). Published Sachs graphs differ from each other, so scores against it are "agreement with the repo's reference", not accuracy.
- Adjacency F1 is the fairest single number across output classes, but it ignores orientation; the tables also give distance to the true CPDAG.

## 7. NEXT

Pass 4b (live repeats) measures how stable sections 2's observations are and whether the LLM's edges follow the names or the data. The plan, datasets and analysis code are built and self-tested; see `reports/pass4b_design.md`.
