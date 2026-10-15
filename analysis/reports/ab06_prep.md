# AB-06 Name reliance across LLM-using systems: the run plan (v2 + amendment 1)

Ticket: AUD-38 (also RQ-05, RQ-17, STR-01). The runs are Uzair's. Every piece below ran end to end on the stub model, and
the batch runner's v2 rules are unit-tested (`tests/test_ab06_batch.py`, `tests/test_probe_gate.py`).

## Where we are now

- The Causal-Copilot part has run: 30 runs on gpt-4o-mini, scored in `ab06_cc_second_model.md`.
- The agent grid has not run live. The v1 budget ($58) came from stub runs, and the AB-05 live probes showed it was low:
  - the full grid is about **$92**, not $58;
  - it would take about **100 hours** if run one at a time.
- The plan is therefore v2:
  - live-calibrated caps;
  - a parallel batch runner;
  - a tier A that answers P9 and P10 (90 runs, about $52, in v2);
  - a pre-registration hashed before any live grid call.
- **Amendment 1 (14 Oct, `plans/ab06_prereg_amendment_1.json`), after tier A started.** 14 runs had been attempted when a
  machine restart stopped the batch at about 08:29 UTC: 12 were ok, and 2 Vashishtha runs had stopped on their caps.
  - Vashishtha ties far more pairs on small scenarios: 85% and 93% at 17 variables, against 37.7% on the 25-variable
    probe scenario, and each tie is a gpt-4o call. Its 20 tier-A runs would cost about $60.
  - Vashishtha is therefore cut to the first five scenarios in tier A. Tier A is now **80 runs, about $48**.
  - Cap hits and interruptions resume without a flag.
  - Spending is read from the call logs, so runs killed by the restart are counted.
  - P9, P10 and the scorer are unchanged.

## The agent grid (`plans/ab06/`, made by `plans/make_ab06_plans.py`)

- 4 agents: causaliq-knowledge, PyWhy-LLM, MATMCD and Vashishtha et al.
- 10 semantic dev scenarios: the first 10 of `plans/splits.json`, rep000, observational only.
- 3 name arms:
  - real names;
  - neutral names (V01..Vd, by a random shown position);
  - swapped names (every variable gets another variable's real name).
- Columns always shuffled (seed 20261010), jitter 1e-6.
- Models as each repository documents. No agent code is changed.

## Budget v2 (`plans/calibrate_ab06.py` → `plans/ab06/BUDGET.json`)

Each plan's own stub calls are re-priced with the live means of their call kind (`analysis/results/ab05/live_calibration.json`).
Vashishtha's tie-breaker count was taken as 37.7% of pairs in v2, as measured on the probe scenario (caps at 55%);
amendment 1 measures it per scenario where possible.

| Agent | Model | Runs | Estimate | Hours, one at a time | Per-run cap (sum) |
|---|---|---|---|---|---|
| causaliq-knowledge | gpt-4o | 30 | $0.13 | 0.0 | $0.90 |
| MATMCD | gpt-4o-mini | 30 | $9.94 | 38.5 | $12.65 |
| PyWhy-LLM | gpt-4o | 30 | $35.46 | 8.0 | $44.79 |
| Vashishtha et al. | gpt-4o-mini + gpt-4o | 30 | $89.45 | 56.6 | $129.27 |
| Total | | 120 | **$134.97** | **103.1** | $187.61 |

The Vashishtha row and the totals are amendment 1's: the tie share is measured where a scenario's triplets are complete,
and estimated at 0.85 elsewhere (caps at 1.0). v2 had $46.32 and $91.84.

What moved:

- **Vashishtha:** 91% of its triplet answers are cut off at its own 300-token limit, so many more pairs go to the gpt-4o
  tie-breaker (`ab05_probe_results.md`).
- **MATMCD:** its domain answers are 1.8 times the assumed length.
- **PyWhy-LLM:** its answers are 1.2 times the assumed length.

## Tiers (`plans/ab06/TIERS.json`, fixed in `plans/ab06_prereg.json`)

| Tier | Runs | What | Estimate | Hours, one at a time |
|---|---|---|---|---|
| **A** | 80 | causaliq-knowledge and MATMCD on all arms; PyWhy-LLM and Vashishtha real + swapped on the first five scenarios (alphabetical) | **$48.23** | 57.6 |
| B | 40 | PyWhy-LLM and Vashishtha: neutral, and real + swapped on the other five scenarios | $86.74 | 45.5 |

v2's tier A (90 runs, $51.98) included Vashishtha's real and swapped arms on all ten scenarios.

**Why this cut:**

- P9 needs paired real and swapped runs, at least 5 per system.
- P10 needs the real arm of the two agents that expose a data-only graph: MATMCD and Vashishtha.
- The neutral arm is the no-information contrast. It is kept in full for the two cheapest agents and deferred for the two
  most expensive.
- PyWhy-LLM and causaliq-knowledge read names only, so their swapped-name loss needs fewer scenarios to show.
- Vashishtha's five scenarios still meet P9's entry rule, and its five real-arm runs serve P10.

Tier B is worth running when AB-06's write-up needs the neutral contrast for every agent.

## The batch runner, v2 (`harness/agent_batch.py`, `cc.ps1 probebatch`)

**Unchanged from v1:**

- One process per run.
- Each run is hard-capped by its own `max_calls` and `max_usd`.
- Resumable: ok runs are skipped, and a failed run is not paid for twice unless `retry` is given.

**New in v2:**

- **`workers=N`:** up to N runs at once, interleaved across agents. Before a run starts, the batch requires spent + the
  hard caps of all running runs + this run's estimate ≤ the total cap. So the total can pass the cap by at most one run's
  (cap − estimate), the same guarantee as one worker. Each run's output goes to `<out>/probe_console.log`.
- **`tier=A`:** runs the plans listed under tier A. Also new: `scenario=a+b` and `arm=real+swapped`.
- **Honest spend on resume:** a retried run replays its paid answers free, and only new calls are counted
  (`est_usd_new_at_served_prices`).
- **Rate limits:** HTTP 429 responses do not use up `max_calls`. The agents' own clients retry them. More than
  max(25, 5% of max_calls) error responses stop the run.
- **I/O errors:** a transient `OSError` EIO on the bind mount is retried, not fatal.

## The scorer (`analysis/ab06_score.py`, v2)

Per agent and arm it reports:

- runs ok and not ok;
- mean directed F1 (the runner's expectation rule);
- DV-1 committed-claim precision and coverage against the released intervention targets;
- cost;
- the source of every directed edge.

It adds:

- **Causal-Copilot as the fifth system:** on gpt-4o, from BND-08's S3 directed F1, which is already known (0.167) and
  declared as such. gpt-4o-mini is reported as RQ-17.
- **The entry rule:** at least 5 paired scenarios per system.
- **Vashishtha's untagged-answer share** per run.

**Pre-registered (`plans/ab06_prereg.json`, hashed in `manifests/evidence/ab06_prereg_2026-10-14.sha256` with the
plans, tiers, budget, scorer and harness):**

| | Claim | Supported | Refuted |
|---|---|---|---|
| P9 | Name reliance is common | ≥ 3 of the 5 systems lose ≥ 0.10 directed F1 from real to swapped | none does |
| P10 | Knowledge can hurt | MATMCD or Vashishtha scores below its own data-only graph on DV-1, real names | both at or above |

The prereg file also fixes what each outcome does to the paper:

- If P9 holds only through names-only systems, it is reported as a design property, not a field-wide one.
- If P9 is refuted, L2 is dropped as a headline.

## Run log

- **14 Oct, first start:** a machine restart at about 08:29 UTC stopped the batch after 14 attempts (12 ok). This led to
  amendment 1.
- **14 Oct, resume:** 7 more runs finished, so tier A has 19 of 80 ok. Then the OpenAI account ran out of credits.
  - All 61 other runs ended within seconds with HTTP 429 `insufficient_quota` ("You have no credits remaining"), and
    the batch kept starting new ones.
  - The harness recorded these as agent failures. None of them is one.
  - Tier A spend so far is $12.21.
- **Amendment 2** (`plans/ab06_prereg_amendment_2.json`, operational only) fixes this class:
  - the probe gate stops a run that the provider refuses for billing as `aborted_quota` (exit 5);
  - such runs, and the 61 recorded earlier, resume like a cap hit;
  - the first quota stop ends the launching of new runs.

## Where we're going

1. Add OpenAI credits. The rest of tier A is estimated at about $33, about 47 h of runs one at a time, or about 12 h with
   4 workers. At least $45 leaves room for the caps.
2. Check for free: `cc.ps1 probebatch ab06 stub all workers=4 tier=A`.
3. Resume tier A: `cc.ps1 probebatch ab06 live all workers=4 tier=A cap=60`.
   - It should open with "already spent (live) $12.21", skip the 19 ok runs and resume the 61 others.
   - If the credits run out again, it now stops by itself (exit 5). Add credits and run the same command again.
4. Score: `python analysis/ab06_score.py`.
5. Optionally, tier B: `cc.ps1 probebatch ab06 live all workers=4 tier=B cap=140`.
