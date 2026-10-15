# AB-06, Causal-Copilot on a second model (gpt-4o-mini): results

Tickets: AUD-38 (AB-06, its Causal-Copilot part), RQ-17 ("do results hold for a second model?"), BND-12 (second-model
part, absorbed by AB-06). Plan: `plans/ab06_cc_gpt4omini_s2.json`, run by Uzair 13-14 Oct (result index
`plans/results/20261014T043637Z_ab06_cc_gpt4omini_s2.result.json`).

The design is BND-08's: 10 CausalArena semantic test scenarios × real / neutral / swapped names on identical numbers,
columns shuffled, the repository's default query, the pipeline unmodified. The model is gpt-4o-mini instead of gpt-4o.
It is scored exactly as BND-08: `stability.py`, `partial_stages.py` and `s2_analysis.py` with label `ab06cc` →
`analysis/results/ab06_cc/`. The thresholds are BND-08's, fixed in code on 10 Oct. Re-scored 14 Oct after the rerun of q042
(`plans/results/20261014T070329Z_ab06_cc_gpt4omini_s2_q042.result.json`); every family now has all three arms.

## Where we are now

Names matter less on the smaller model, but the structure of the result holds.

| | gpt-4o (BND-08) | gpt-4o-mini (this run) |
|---|---|---|
| M2: real names lift S3 directed F1 ≥ 0.10 over neutral (≥ 8 families) | 5 of 10: refuted | 4 of 10: refuted |
| M3: swapped arms, LLM-set edges follow the labels (≥ 0.80, n ≥ 30) | 0.80 (81 of 101): supported | 0.71 (141 of 198): inconclusive |
| M4: without names, below plain PC on the same file (≥ 8 families) | 8 of 10: supported | 9 of 10: supported |
| Name reliance, S3 directed F1 real − swapped (paired, 10 families) | **0.167** | **0.094** |
| Real − neutral | 0.093 | 0.064 |
| Final graph below the algorithm's own adjacency F1 (completed runs) | 23 of 24 | 26 of 27 |
| Non-directed algorithm edges kept by the bootstrap step | 73 of 378 (19%) | 89 of 458 (19%) |

Mean by role over all runs that reached S3 (S0 = the algorithm's output, S3 = the graph handed to the cycle step):

| Role | Directed F1 S0 → S3, gpt-4o | gpt-4o-mini | Adjacency F1 S0 → S3, gpt-4o | gpt-4o-mini |
|---|---|---|---|---|
| real | 0.175 → 0.287 | 0.233 → 0.208 | 0.568 → 0.447 | 0.586 → 0.383 |
| neutral | 0.211 → 0.193 | 0.180 → 0.144 | 0.585 → 0.315 | 0.586 → 0.296 |
| swapped | 0.206 → 0.120 | 0.205 → 0.114 | 0.585 → 0.223 | 0.584 → 0.184 |

**Reading:**

- On gpt-4o-mini, the model review lowers directed F1 even with real names (0.233 → 0.208); on gpt-4o it raised it
  (0.175 → 0.287). The smaller model's knowledge is not good enough to pay for what the pipeline throws away.
- Swapped names still cost the most on both models: 0.114 vs 0.120 at S3.
- The skeleton loss is the same on both models. The bootstrap step keeps 19% of non-directed edges on both, and the final
  graph is below the algorithm's own adjacency F1 in 26 of 27 completed runs. That loss happens before any name is read.
- The smaller model sets more edges that neither reading supports: 225 "neither" against 74 on gpt-4o. That is why M3's
  share falls: its edges are noisier, not more data-driven. Data-only edges stay below the chance line (57 against a
  Binomial 95th percentile of 111).
- For P9 (AB-06), Causal-Copilot counts once, on gpt-4o (0.167, at least 0.10). gpt-4o-mini is reported here as RQ-17
  (0.094).

## Integrity

- Code identity OK in every run with a summary; one model snapshot throughout (gpt-4o-mini-2024-07-18). FCI with the
  `rcit` test was chosen in 29 of 29 recorded runs.
- partial_stages gates Q1-Q3 pass. stability.py gates T3-T6 pass, and T2 passes with `--min-runs 1` (one run per arm,
  the design). T1 reports the I/O-lost q042 attempt as an excluded run; its rerun fills the arm.
- Cost: 3,537,034 prompt + 543,861 completion tokens over the 29 runs with a summary, $0.86 at gpt-4o-mini prices
  ($0.03 per run). Pipeline wall time 475-2,231 s, median 734 s (the q042 rerun took 1,249 s).

## Run accounting (33 folders with label `ab06cc`)

| Runs | What happened | Counted as |
|---|---|---|
| 26 | completed | scored |
| 2 (q071 real s2_07, q101 real s2_10) | crashed at `postprocess/judge_functions.py:562`, the cycle-step key (answers `removed_edge`) | crashes, scored at S3 |
| 1 (q041 real s2_04) | the pipeline completed, then the harness could not write `summary.json`: `OSError: [Errno 5] Input/output error` at 00:21 UTC | scored at S3 from the recorded state snapshots |
| 1 (q042 neutral s2_04) | the same I/O error from 00:24 UTC hit the state snapshots, then the pipeline itself failed in `06c_hyperparameters` | infrastructure loss; rerun 14 Oct 06:40 UTC (`…bca118`), completed, scored |
| 2 (`20261013T202422Z…7862a9`, `20261014T063956Z…e3eec3`) | a folder created 26-44 s before each plan's first run, with an empty console and no model calls: a launcher artefact, seen once per plan | not runs |

**The I/O error.** Both failures fall in one six-minute window (14 Oct, 00:19-00:25 UTC). Nothing else of ours was running
then: the stub batch had ended at 22:49, the live probes at 22:47. Errno 5 on a Docker Desktop bind mount of a Windows
folder usually means another Windows process held the files, for example OneDrive sync or an antivirus scan, or the disk
paused. The cause is not identified.

The fix is made as a class in our harness:

- every harness write of a summary, result or call log now retries an EIO with backoff
  (`harness/cc_common.py dump_json`, `harness/agent_probe.py`, `harness/probe_llm.py`);
- Causal-Copilot's own writes cannot be protected without changing it, so a run hit inside the pipeline is rerun.

## Where we're going

- Done: the q042 rerun is in, and M2 and M4 now have 10 families.
- The AB-06 agent grid adds the four other systems (`ab06_prep.md`).
