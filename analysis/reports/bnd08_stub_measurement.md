# BND-08 stub run: time, calls, estimated live cost, and a name-order finding (2026-10-11)

Tickets: AUD-11, BND-08, AUD-10, BEN-07

Run by Uzair: `cc.ps1 plan bnd08_stub.json` (result index `plans/results/20261011T010405Z_bnd08_stub.result.json`).
6 runs: s2_05 (20 variables; q051 real, q052 neutral, q053 swapped) and s2_02 (21 variables; q021-q023). Stub LLM, no cost.
The `s2stub` runs read S2 data, which is test data: they are used only for time and call counts, never for scores.

## Measured (stub)

- All 6 COMPLETED; code identity OK; the stub picked PC (live bundle 1 picked FCI every time, so the live algorithm may differ).
- Pipeline wall time 198-291 s; whole plan step 314-437 s per run including container start.
  Stage times: refinement 79-148 s, EDA 23-40 s, report compile 20-40 s, algorithm 11-20 s.
- LLM calls per run: 223 (20 variables) and 430 (21 variables). Of these, 189 and 395 are `LLM_remove_cycles`: every run
  entered the cycle step, and the stub's well-formed answers keep the loop going one edge at a time.
- Live behaviour at that step differs: in bundle 1 the cycle step was entered 9 times live and crashed 9 times on the first
  answer (crash C1, judge_functions.py:562). Expect most S2 live runs to stop there. S3 (graph before the cycle step) is the
  primary endpoint for exactly this reason, so the crash does not cost the measurement.

## Estimated live cost (`analysis/stub_cost.py`, `analysis/results/stub_cost/bnd08_estimate.json`)

Calibration: 54 live bundle-1 runs (gpt-4o-2024-08-06): prompt tokens per prompt character and mean completion tokens per
caller function, applied to the stub's prompts.

| Case | Prompt tokens per run | Completion per run | 30 runs | At $2.50 / $10 per M tokens |
|---|---|---|---|---|
| cycle step crashes on its first call (as in bundle 1) | 84k (69k-95k) | 7.5k | 2.53M + 0.22M | about $9 |
| cycle loop runs as long as in the stub | 113k (81k-142k) | 12.1k | 3.38M + 0.36M | about $12 |

For scale, bundle 1 (54 runs) used 2.67M prompt and 0.29M completion tokens. Live prompts can be longer than the stub's
(the knowledge text the model writes is fed back into later prompts), so allow up to about 1.5x: a ceiling near $20.
The price per token is an assumption to check against the OpenAI billing page; the token counts are the measurement.

Time: live API time adds about 1.5 min per run (crash case) to 6 min (loop case) to the 3-5 min measured, so 30 runs take
roughly 3-6 hours. `run_timeout_s` 7200 in `plans/bnd08_live.json` is far above that and can stay (it is hashed in the
pre-registration manifest; changing it would need a new hash).

## Finding: one S2 family's real names encode the causal order

`analysis/name_prefix_check.py` -> `analysis/results/name_prefix/name_prefix.json`.
CausalArena's released node ids are numbered ("V1_countdown_policy_enabled", ...) in 2 of the 50 public semantic scenarios.
In pedestrian_countdown_compliance (our family s2_02), 34 of 38 true edges run from a lower number to a higher one (0.5
expected without an order signal); in pipe_pressure_transient_leak_flow (not in S2) 20 of 36. Our column shuffle does not
remove this: the number travels with the name. So in s2_02 the real-name arm carries an order hint the other nine families
lack, and any LLM method in CausalArena's own evaluation sees the same hint for that scenario.

Effect on BND-08: M2 (real minus neutral directed F1 >= 0.10 in >= 8 of 10 families) can be helped by this one family.
Options (Uzair's call, because changing the suite reopens DLV-01):
1. Keep the suite as frozen and report M2 also on the 9 other families (recommended; nothing is rebuilt, the hint is part of
   the benchmark as released and is itself a finding).
2. Strip the "V<k>_" prefixes from s2_02's real and swapped arms, rebuild, rehash, reopen DLV-01.
