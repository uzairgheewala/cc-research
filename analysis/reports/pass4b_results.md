# Pass 4b results: run-to-run stability and the name-versus-data test

Plan `pass4b_stability` ran on 2026-10-06, 13:44 to 15:23 UTC: 28 runs, gpt-4o (served snapshot gpt-4o-2024-08-06 in every run), repo default query, baseline `a31aa7c` verified before every run. 25 runs completed, 3 failed inside the pipeline. Cost: 1,434,644 prompt and 170,413 completion tokens, 97 minutes. Full tables: `results/stability_p4b/stability.md`; per-run lineage: `results/stability_p4b/lineage/`. Design and thresholds: `reports/pass4b_design.md`.

Gates T1-T5 pass (every included run completed, passed code identity and lineage gates A-F; each arm has at least 3 runs; every run in an arm read the same bytes as recorded in `MAPPING.json`; variable names match the arm; accuracy recomputed here equals `lineage.py`'s). T6: one model snapshot per arm.

## 1. The three failed runs, to the line

| Run | Where | Cause |
|---|---|---|
| sachs r01, d01 r01 | `global_setting/Initialize_state.py:178`, `KeyError: 'linearity'` | The first LLM call (turn the query into a JSON of 9 fields) returned `{}`. The request was byte-identical to the one that returned all 9 fields in 24 other runs, same model snapshot, same system fingerprint, temperature 0. The code reads the keys without checking they exist. |
| d01 r02 | `postprocess/judge_functions.py:562`, `KeyError: 'nodes'` | The LLM's own added edges formed a cycle (Plcg -> PIP3 -> PIP2 -> Plcg). Asked which edge to remove, it answered `{"edge_to_remove": ["PIP3", "PIP2"]}`; the code reads the key `nodes`. |

All three are unchecked LLM outputs on the discovery path (pass 3, F3.5). 3 of 28 is an 11% crash rate for the unmodified CLI on this day; the interval on that is wide.

## 2. Predictions

| | Prediction | Result | Verdict by the rule fixed in advance |
|---|---|---|---|
| P1 | In d03 (real names moved onto other proteins' columns), LLM-set edges follow the labels | 27 follow the labels only, 0 follow the data only, 10 follow neither (5 runs) | SUPPORTED |
| P2 | With neutral names the LLM writes at most half as many edges | d02: 0 per run. d01: 6.3 per run | SUPPORTED |
| P3 | At most 25% of the algorithm's non-directed edges survive the bootstrap step | 18 of 119 (15%) over 14 distinct outputs; directed edges 7 of 7 | SUPPORTED |
| P4 | (exploratory) "sachs" in the path changes final adjacency F1 | 0.53 with (4 runs, s.d. 0.09), 0.44 without (3 runs, s.d. 0.07) | no verdict; not separable at this n |
| P5 | (exploratory) the algorithm choice varies between repeats | It did not: FCI with alpha 0.05, `rcit`, depth 4 in all 17 completed sachs-derived runs, XGES with alpha 2 in all 8 synthetic runs | no verdict |

Two qualifications on P1. The rule counted edges over runs, and the same edges recur: by distinct edge it is 6 label-only, 0 data-only, 2 neither, which is below the n = 10 the rule asked for. And the 10 "neither" are Raf -> Erk and P38 -> Jnk in each of the 5 runs, two edges the LLM also writes on the correctly labelled data; they are name-driven as well, just not in the reference graph.

## 3. What the swapped-name arm shows

In d03 the numbers are the Sachs numbers and each column carries another protein's name. Across 5 runs:

- The LLM wrote Raf -> Mek, Mek -> Erk, Plcg -> PIP2, PIP2 -> PKC, Raf -> Erk, P38 -> Jnk and PIP3 -> Akt in every run. These are textbook signalling edges between the labels. The data under those labels belong to other proteins.
- 7.2 of the 7.6 final edges per run were between columns the algorithm had not connected, and 6.2 per run were written where at least 90% of resamples showed no edge.
- Final graph against the data: adjacency F1 0.01 (the algorithm's own output scored 0.60). Final graph against the labels: adjacency F1 0.41.
- The knowledge text never named the Sachs dataset in this arm (0 of 5), nor in d01 (0 of 4). It named it in every run where the file path contained "sachs" (4 of 4). So explicit recognition of the dataset needed the path, but the edges did not: protein names alone were enough.
- KCI pruning removed one LLM-added edge (PIP3 -> PIP2) in 3 runs. That is the only place the data overruled the LLM, and it can only happen for edges stored above the diagonal.

With neutral names (d02) the LLM said "No Knowledge" in all 5 runs, answered D to all 275 pair questions, and changed nothing. The final graph was whatever the bootstrap step left: 1.0 edges on average, adjacency F1 0.10 against 0.62 for the algorithm's output.

## 4. Accuracy by stage (adjacency F1, mean over completed runs)

| Arm | Runs | S0 algorithm output | S1 after bootstrap step | S4 final | Scored against |
|---|---|---|---|---|---|
| sachs | 4 | 0.61 | 0.17 | 0.53 | repo reference |
| d01 | 3 | 0.63 | 0.19 | 0.44 | repo reference |
| d02 | 5 | 0.62 | 0.10 | 0.10 | repo reference |
| d03 | 5 | 0.60 | 0.11 | 0.01 | repo reference, by data |
| Linear_Gaussian | 5 | 1.00 | 0.00 | 0.00 | ground truth |
| LiNG 10 nodes | 3 | 0.33 | 0.12 | 0.12 | ground truth |

In all 25 completed runs the final graph had lower adjacency F1 than the graph the algorithm returned.

The other side of the ledger: with real, correctly placed names the LLM adds orientation that the algorithm's output did not have. In the sachs arm the final graph had 4.8 reference edges directed correctly and 1.8 reversed per run, and distance to the reference CPDAG fell from 19.8 to 16.2 (d01: 19.7 to 17.0). In d03 the same step raised that distance from 20.2 to 26.4. The gain on the named arms is recall of a well-known graph, not something the pipeline extracted from the numbers.

## 5. Stability

- **Same request, different answers.** The first request is identical in all 28 runs. It got three different answers: the full JSON 24 times, a JSON with two fields null instead of true/false twice, and `{}` twice. Temperature 0 did not make the model repeatable.
- **Where runs diverge.** In the named arms no two runs sent the same request after the knowledge step: the elicited knowledge prose differed every time (0 of the repeated knowledge requests were answered identically), and that prose is pasted into every later decision prompt.
- **Choices were stable anyway.** Algorithm and hyperparameters were identical within every arm. On all named arms the LLM again proposed `background_knowledge`, which was dropped; on d02 it did not propose it.
- **The algorithm itself was not repeatable on the Sachs data.** FCI with the `rcit` test gave 2 or 3 distinct outputs across 3 to 5 runs on byte-identical data, and a different bootstrap table in every run. `rcit` draws random features from numpy's generator, which nothing seeds.
- **The bootstrap is fixed when the algorithm is deterministic.** XGES gave one output and one bootstrap table across 5 runs (Linear_Gaussian) and across 3 runs (LiNG). That confirms the pass 4a correction: the resamples are the same every run.
- **LLM edge answers.** Identical in every run for 33 of 55 pairs (sachs), 35 of 55 (d01), 41 of 55 (d03); the edge/no-edge call was identical for 50, 50 and 55 of 55.
- **Final edges.** sachs: 10 distinct edges appeared across 4 runs, 4 of them in every run (Raf -> Mek, Mek -> Erk, PIP2 -> PIP3, PIP3 -> Akt). d01: 10 distinct, 4 in every run. d03: 9 distinct, 7 in every run. Synthetic arms: identical every run.

## 6. INFERENCES

- I6.1 On this dataset and model, the LLM review is a recall of textbook relations keyed on variable names. It is unaffected by which numbers sit under the names, and silent when the names carry no meaning.
- I6.2 The pipeline's final accuracy on a famous benchmark is therefore mostly a property of the benchmark's fame. With the file path held fixed, the same pipeline on the same numbers scores 0.44, 0.10 or 0.01 (arms d01, d02, d03) depending only on the header line.
- I6.3 The bootstrap step's deletion of non-directed edges (P3) is what hands the graph to the LLM: after it, 1 to 2 of about 10 edges remain.
- I6.4 Method selection, the stage the paper emphasises, was the stable part. The unstable parts were a randomised independence test and free-text knowledge.

## 7. Threats to validity

- One model snapshot, one day, one semantic dataset. 3 to 5 runs per arm; d01 has 3.
- Runs within an arm are not independent draws of edges; the same edges recur (see the P1 qualification).
- Scores on the sachs arms are agreement with the repo's reference graph, which is one of several published versions.
- The by-label reference in d03 shares 1 of 19 adjacent pairs with the by-data reference; no LLM-set edge fell on it.
- P3 was restated by edge type after the stub self-test and before any live repeat.

## 8. What changed in the ledger's open items

- "Does the LLM override high-confidence bootstrap decisions with a real model, and how often" is answered for this setting: 2.2 to 6.2 additions per run against a no-edge frequency of at least 0.9, in every named arm.
- "Is the bootstrap the same from run to run" is answered: yes for deterministic algorithms, no when the algorithm uses numpy randomness.
- New: the CLI crashes on malformed LLM JSON at two points (section 1).
