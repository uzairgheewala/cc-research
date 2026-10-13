# Refinement v1: dev results, freeze, and the first test read (2026-10-11)

Tickets: BND-09, BND-10, CAP-06, TGT-09, BLD-06, DLV-04

Code: `analysis/refinement_v1.py` (no model call). Rule thresholds KEEP 0.5 and ADD 0.9 were fixed in the design note before
any replay and were not changed. Results: `analysis/results/refinement_v1/` (`dev.json`, `RULE.json`, `access_log.jsonl`,
`test_replay.json`; contract in `CONTRACT.json`).

S0 = the algorithm's own output; S1 = the graph after the pipeline's bootstrap step; v1 = our rule applied to the same
bootstrap tables. Predictions (BND-09): R1 v1 adjacency F1 >= S0 - 0.02 in >= 90% of files (refuted below 70%);
R2 v1 adjacency F1 > S1 in >= 90% (refuted below 70%); R3 mean directed-F1 difference v1 - S0 >= -0.01 (refuted <= -0.05).

## Dev (BND-09), 92 files

| Group | Files | R1 share | R2 share | R3 mean diff | Non-directed edges kept: S1 / v1 |
|---|---|---|---|---|---|
| live: pass 4b | 18 | 0.889 | 1.000 | +0.014 | 25 / 174 of 177 |
| live: bundle 1 | 51 | 0.706 | 0.980 | +0.031 | 114 / 383 of 406 |
| replay: CausalArena dev split | 23 | 0.913 | 0.870 | +0.014 | 67 / 106 of 114 |
| all | 92 | 0.793 INCONCLUSIVE | 0.957 SUPPORTED | +0.023 SUPPORTED | 206 / 663 of 697 |

Dev-split replay job: 25 files, 23 usable; 2 typed errors (one per-file timeout; one singular correlation matrix, an exactly
collinear scenario already known from BND-04). Mean adjacency F1 over all 92 files: S0 0.557, S1 0.302, v1 0.554. Where R1
fails (19 files), v1 drops adjacencies of S0 that were present in fewer than half the resamples and were right.

## Freeze

`RULE.json`: sha256 `da3cb260c1e25bb90e4cc2ad7e766db0f63ca4048fa60c456ed0a8f95287a962`, frozen 2026-10-11T01:11:03Z.
`refinement_v1.py test` refuses to run unless the file's hash equals the frozen one.

## Test, replay part (BND-10 part 1 of 2), 25 files

Access log: one test read at 2026-10-11T01:11:21Z with the frozen rule hash.

| | S0 | S1 (pipeline) | v1 |
|---|---|---|---|
| mean adjacency F1 | 0.619 | 0.585 | 0.622 |
| mean directed F1, undecided pairs random | 0.478 | 0.470 | 0.494 |
| mean directed F1, committed arrows only | 0.445 | 0.448 | 0.460 |
| non-directed S0 edges kept | 117 | 61 | 109 |

- R1 SUPPORTED: 23 of 25 (0.92).
- R2 REFUTED: 17 of 25 (0.68; refuted below 0.70). 3 files tie (the pipeline's bootstrap removed nothing that v1 keeps), 5 are
  lower by 0.015 to 0.033. On these PC-only replays the pipeline's bootstrap step removes little (S1 is 0.034 below S0), so
  "strictly above S1 in 90% of files" was a high bar. The verdict stands as pre-registered.
- R3 SUPPORTED: mean +0.016.

The 10 live S2 scenarios' bootstrap tables are the second part of the test; they exist only after the BND-08 live run.

## Disclosure

Before the freeze, the test replay file was opened once to count row statuses (25 ok, 0 errors) and read its header; no
score or graph field was printed and nothing was changed afterwards. The access log starts at the frozen read.

## Caveat on absolute numbers

Replay files keep CausalArena's released column order, which is topological, and causal-learn PC is column-order sensitive
(BND-06 Q4c: F1 0.335 released vs 0.428 shuffled). The R1-R3 comparisons are within a file and share one S0, so they are
unaffected; the absolute F1 values are released-order figures.

## Test, live S2 part (BND-10 part 2 of 2), 30 tables (added 2026-10-12)

Driver `analysis/refinement_v1_test_live.py` imports the frozen `refinement_v1.py` unchanged (hash checked) and logs the
read (`access_log.jsonl`, 2026-10-12T00:51:05Z). Result `analysis/results/refinement_v1/test_live_s2.json`. Before it ran, the
driver's docstring fixed the BND-10 verdict as the pooled test set (25 replay + 30 live tables), as dev pooled both kinds.
The live tables come from FCI with the RCIT test in 29 of 30 runs (20 bootstrap resamples), at 20-25 variables.

| Live S2, 30 tables | S0 | S1 (pipeline) | v1 |
|---|---|---|---|
| mean adjacency F1 | 0.579 | 0.300 | 0.569 |
| mean directed F1, undecided random | 0.365 | 0.217 | 0.347 |
| mean directed F1, committed only | 0.197 | 0.179 | 0.187 |
| non-directed S0 edges kept | 486 | 101 | 384 |

Live part alone: R1 REFUTED (17 of 30), R2 SUPPORTED (30 of 30), R3 INCONCLUSIVE (-0.019). Per scenario (mean of its three
arms): v1 within 0.02 of S0 in 6 of 10, above S1 in 10 of 10.

**BND-10 verdicts, pooled test set (55 tables):**
- R1 INCONCLUSIVE: 40 of 55 (0.73).
- R2 INCONCLUSIVE: 47 of 55 (0.85).
- R3 SUPPORTED: mean -0.003.

So the frozen v1 always beats the pipeline's own bootstrap step on these live tables, but it is not "never below the
algorithm": TGT-09 is not met by v1.

Mechanism (exploratory, after the read, `analysis/results/refinement_v1/diagnosis_test_live_s2.json`): over the 30 live tables
v1 dropped 120 of the algorithm's adjacencies whose resample frequency was below 0.5; 50 of those were true edges and 70 false
(median resample frequency of the dropped true edges 0.30). It added 7 pairs, all true. With FCI + RCIT at 20+ variables and 20
resamples, a true edge often appears in fewer than half the resamples, so the KEEP rule removes true and false edges at
nearly the same rate. Design consequence for v2 (BND-11, to be pre-registered on dev only): do not delete algorithm
adjacencies on resample frequency alone.
