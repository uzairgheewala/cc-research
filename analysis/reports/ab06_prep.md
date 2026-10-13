# AB-06 Name reliance across LLM-using systems: the run plan

Ticket: AUD-38 (also RQ-05, RQ-17, STR-01). The runs are Uzair's. Every piece below ran end to end on the stub model.

## Where we are now

**The agent grid (`plans/ab06/`, made by `plans/make_ab06_plans.py`)**

- 4 agents: causaliq-knowledge, PyWhy-LLM, MATMCD and Vashishtha et al.
- 10 semantic dev scenarios: the first 10 of `plans/splits.json`, rep000, observational only.
- 3 name arms:
  - real names;
  - neutral names (V01..Vd, assigned by a random shown position);
  - swapped names (the A3 "moved" permutation, in which every variable gets another variable's real name).
- Every run has its columns shuffled (seed 20261010) and 1e-6 jitter.
- That makes 120 runs. Names maps are in `plans/ab06/names/`.

**Budget (`plans/ab06/BUDGET.json`, from the AB-05 stub runs)**

| Agent | Model | Runs | Estimate | Sum of per-run caps |
|---|---|---|---|---|
| causaliq-knowledge | gpt-4o | 30 | $0.35 | $1.50 |
| MATMCD | gpt-4o-mini | 30 | $6.58 | $10.08 |
| Vashishtha et al. | gpt-4o | 30 | $20.53 | $30.96 |
| PyWhy-LLM | gpt-4o | 30 | $30.51 | $45.87 |
| Total | | 120 | $57.97 | $88.41 |

The causaliq estimate is conservative. Its live probe used 316 completion tokens against the stub's 1,120.

**The batch runner (`harness/agent_batch.py`, `cc.ps1 probebatch`)**

- One process per run. Each run is hard-capped by its own `max_calls` and `max_usd`.
- **Total cap** (default $60). Before each run, the batch adds every logged attempt plus any live run made outside the batch. It stops, with exit code 3, before a run whose estimate would pass the cap. The total can therefore pass the cap by at most one run's cap minus its estimate.
- **Resumable.** Runs that ended ok are skipped. A run that crashed or hit its cap is not paid for twice unless `--retry-failed` is given.
- **Log.** `plans/ab06/BATCH_live.jsonl` gets one line per attempt.
- **Tests.** `tests/test_ab06_batch.py` checks the grid, the names maps, the skip and cap rules, and the scorer's edge format.

**The Causal-Copilot arm (`plans/ab06_cc_gpt4omini_s2.json`)**

- The BND-08 grid on a second model: 10 S2 families × real/neutral/swapped, interleaved, about 30 runs, about $1.
- It is scored with the BND-08 pipeline under the label `ab06cc`. Steps (no model calls):
  1. `stability.py --label ab06cc`;
  2. `partial_stages.py --label ab06cc`;
  3. `s2_analysis.py`, writing to `analysis/results/ab06_cc/`.
- Runs that die at the upstream key crash (`judge_functions.py:562`; see `ab05_probe_results.md`) count as crashes. They are scored from their algorithm-stage graph.

## The scorer (`analysis/ab06_score.py`)

Per agent and arm it reports:

- runs ok and not ok;
- mean directed F1 (the runner's expectation rule);
- DV-1 committed-claim precision and coverage against the released intervention targets;
- cost;
- the source of every directed edge, where the agent records it.

It then computes three comparisons:

- **Name reliance:** F1(real) − F1(swapped), paired by scenario.
- **The no-information contrast:** F1(real) − F1(neutral).
- **The data-only floor (P10):** where the agent exposes its own data-only graph (MATMCD `pc_only_initial`, Vashishtha `pc_only`), its DV-1 against the agent's final graph in the real arm.

Pre-registered predictions (`plans/audit_dag.json`):

| | Claim | Supported | Refuted |
|---|---|---|---|
| P9 | Name reliance is common | ≥ 3 agents lose ≥ 0.10 F1 from real to swapped | no agent does |
| P10 | Knowledge can hurt | ≥ 1 agent scores below its own data-only output on DV-1, real names | all at or above |

## Where we're going

Run order: the cheapest first, then the expensive ones once the cheap ones look sane.

1. `probebatch ab06 stub`
2. `probebatch ab06 live causaliq`
3. `probebatch ab06 live matmcd`
4. `probebatch ab06 live vashishtha`
5. `probebatch ab06 live pywhyllm`

Then `analysis/ab06_score.py` and the Causal-Copilot scoring above. The plans can be regenerated with PyWhy-LLM on gpt-4o-mini (`make_ab06_plans.py --pywhyllm-model gpt-4o-mini`), which brings the total to about $29. That would change the model under test, though, so gpt-4o stays the default.
