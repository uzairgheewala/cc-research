# BND-08: Causal-Copilot on CausalArena's named scenarios (S2), live results (2026-10-12)

Tickets: AUD-10, AUD-11, BND-08, DLV-02, DLV-03, RQ-05, RQ-15, AUD-17

Runs: `plans/bnd08_live.json`, run by Uzair 11-12 Oct (result index `plans/results/20261012T002122Z_bnd08_live.result.json`).
30 runs, one per arm: 10 CausalArena semantic test scenarios x real / neutral / swapped names on identical numbers, columns
shuffled, repo default query, unmodified pipeline. Pre-registration: `manifests/evidence/bnd08_prereg_2026-10-11.sha256`
(every listed file still matches). Analysis: `analysis/results/stability_s2/` (stability.py, partial_stages.py,
s2_analysis.py). Primary endpoint S3 = the graph handed to the cycle step, defined before the run because the cycle step
crashed in every live entry so far.

## Integrity

- Code identity OK in 30 of 30; one model snapshot throughout (gpt-4o-2024-08-06).
- partial_stages gates Q1-Q3 pass: rebuilt S2/S3 equal the recorded graphs; every crash has a cycle in S3; all 30 runs
  accounted for. Every run reached S3.
- stability.py gates T2-T6 pass (T2 with one run per arm, which is the design). T1 ("no arm left empty") fails by design:
  the only run of 6 arms crashed in the cycle step; those runs are scored at S3 by partial_stages.py.
- Lineage was recomputed on Uzair's machine after installing the container's missing pure-Python modules (pydot, networkx,
  scikit-learn, momentchi2, statsmodels); gate T5 (scores recomputed equal lineage's) passes in every run.

## Verdicts (thresholds fixed before the run, `analysis/s2_analysis.py`)

| Prediction | Result | Verdict |
|---|---|---|
| M1 the pipeline's bootstrap step lowers PC's adjacency F1 (dev replay, no LLM; >= 0.8 of files) | 19 of 23 usable dev files (0.83) | SUPPORTED |
| M2 real names lift S3 directed F1 by >= 0.10 over neutral (>= 8 of 10 families) | 5 of 10 (s2_01 +0.11, s2_04 +0.17, s2_05 +0.30, s2_08 +0.27, s2_09 +0.20; s2_02 -0.23, s2_07 -0.03, s2_03 +0.02, s2_06 +0.04, s2_10 +0.08) | REFUTED |
| M2 sensitivity without s2_02 (numbered names) | 5 of 9 (supported at 8, refuted at 4) | INCONCLUSIVE |
| M3 in swapped arms, LLM-set edges follow the labels | 81 of 101 distinct edges (0.80); data-only 20, below the Binomial 95th percentile 59 | SUPPORTED |
| M4 without names, the agent is below plain PC on the same file (>= 8 of 10) | 8 of 10 (exceptions s2_02, s2_10) | SUPPORTED |

M3 is computed as fixed in code, from stability.py's N1 count, which reads final graphs: it covers the 9 swapped runs that
completed (q033 crashed in the cycle step). M5 (names alone, optional part d) was not run. Gate L1 (no real name or scenario word in a neutral-arm prompt before the final
graph; 370 requests scanned, label variants with and without the numbering prefix) passes. All summarised, with the per-run
table, in `analysis/results/stability_s2/bnd08_summary.json`.

Mean by role over all 30 runs (S0 = the algorithm's output, S3 = before the cycle step; scored against the data's reference):

| Role | Directed F1 S0 -> S3 | Adjacency F1 S0 -> S3 |
|---|---|---|
| real | 0.175 -> 0.287 | 0.568 -> 0.447 |
| neutral | 0.211 -> 0.193 | 0.585 -> 0.315 |
| swapped | 0.206 -> 0.120 | 0.585 -> 0.223 |

Reading: names do raise directed F1 on average (+0.09 real vs neutral), but not by 0.10 in most families, so the
pre-registered "names carry the score" form is refuted. When names are swapped the LLM follows them (M3), and with no names
the agent ends below plain PC in 8 of 10 families (M4). Adjacency F1 falls from S0 to S3 in 29 of 30 runs; in completed
runs the final graph is below the algorithm's own adjacency F1 in 23 of 24 lineage-checked runs (stability N4). The pipeline's
bootstrap step keeps 73 of 378 non-directed algorithm edges (19%; P3 SUPPORTED).

s2_02 (the numbered-name scenario) is the family where real names did worst (-0.23): the hint did not help, and its neutral
run is the only one of 30 where the LLM chose PC rather than FCI, a one-run confound reported as such.

## Cost, time, crashes (AUD-11, live half)

- Tokens: 3,316,360 prompt + 439,357 completion over 30 runs (110k + 14.6k per run). At an assumed $2.50 / $10 per million:
  about $12.7. The stub-based estimate (84k + 7.5k per run, $9-12) was low: the stub picked PC, live runs picked FCI in 29 of
  30, and live prompts and answers are longer. Recorded so the next estimate uses live calibration from S2.
- Time: pipeline wall 302-1130 s per run (median 612 s); the plan took 5 h 32 min.
- Crashes: 6 of 30, all at postprocess/judge_functions.py:562 (`response['nodes']`, KeyError) on the first cycle-step answer;
  answer keys returned: `edge_to_remove` 5, `nodes_to_remove` 1. By role: real 5 of 10, swapped 1 of 10, neutral 0 of 10.
  A cycle appears only after the LLM sets edges, and with neutral names it set none. Live entries into the cycle step,
  bundle 1 plus S2: 15 of 15 crashed.
