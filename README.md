# cc-research: out-of-repo harness for Causal-Copilot

Everything in this folder is research tooling and evidence. Nothing here edits the `Causal-Copilot`
source tree. The baseline is upstream commit `a31aa7c` (zip unpack); every run first checks the
tree against `manifests/baseline_a31aa7c.sha256` and aborts if a baseline file is missing or changed.

Repository, CI and the Causal Atlas site: `docs/REPO.md`. Forking Causal-Copilot: `docs/FORK.md`.

## One-time setup

Open PowerShell in this folder (`...\DSC 180A\cc-research`).

1. Put the OpenAI key on the `OPENAI_API_KEY=` line of `..\Causal-Copilot\.env` (line 20).
   Provider and model are already set there (`openai`, `gpt-4o`).
2. Build the images (Docker Desktop must be running):

       powershell -ExecutionPolicy Bypass -File .\cc.ps1 build

   The build context contains only `requirements_cpu.txt`, so `.env` can never end up in an image.

## The three checks, in order

    powershell -ExecutionPolicy Bypass -File .\cc.ps1 preflight
    powershell -ExecutionPolicy Bypass -File .\cc.ps1 dryrun
    powershell -ExecutionPolicy Bypass -File .\cc.ps1 golden

| Command | What it does | LLM cost | Writes |
|---|---|---|---|
| `preflight` | code identity, Python, tools, imports, PC + KCI + LaTeX smoke tests, two tiny LLM calls | about 50 tokens | `preflight/preflight_<time>_<PASS/FAIL>.json` |
| `dryrun` | the full CLI pipeline on `Linear_Gaussian` with an offline stub in place of the LLM | none | `runs/<run_id>_STUB_.../` |
| `golden` | live runs from `plans/golden.json`: `Linear_Gaussian`, then `sachs` | roughly 20-25 calls per run | `runs/<run_id>/` (one per run) |

Each run ends by printing a must-show summary (also saved as `SUMMARY.txt`).

## What a run directory contains

- `SUMMARY.txt`, `summary.json`: the must-show list (identity, status or failing file:line, LLM calls and tokens, snapshots, selection, graphs, refinement captures, stage times, report).
- `meta.json`: arguments, environment, package versions, code-identity result, failure traceback.
- `llm_calls.jsonl`: every LLM call: calling file:line, stage, arguments, the request as sent, the raw response (served model snapshot, fingerprint, token usage), the parsed result.
- `events.jsonl` + `artifacts/*.pkl`: inputs and outputs of each refinement step (every bootstrap graph, the bootstrap buckets, the LLM edge decisions, the KCI removals, the cycle step).
- `state/NN_<stage>.pkl|.json`: the full state object after each pipeline stage.
- `rng_initial_states.pkl`: the random-number-generator states observed at start (observed, never set).
- `console.log`: everything printed.
- `pipeline_output/`: copy of the figures and report the pipeline wrote.

The API key is replaced by a marker in everything written here.

## What the harness does and does not do

- It calls `main.py`'s own `main()` with the repo's default query unless a plan says otherwise.
- It observes: hooks call the original functions with the original arguments and return what they returned. Nothing is seeded, retried or reordered.
- One interaction: the final "any questions?" prompt is answered "no" so the run can end unattended.
- A run writes into the repo only what the pipeline itself writes: `output/...` and `causal_discovery/context/hp_rerank_prompt_test.txt`.

## Plans and the optional queue runner

A plan is a small JSON file in `plans/` (see `plans/golden.json`). It can only name a dataset under
`data/dataset`, a data mode, a query, a label and a repeat count; anything else is rejected.

    powershell -ExecutionPolicy Bypass -File .\cc.ps1 plan <file.json>

Queue runner (optional): keeps a container running that executes any valid plan dropped into
`queue\inbox`. This is what lets Claude start live runs without you typing a command each time.
It spends API credit on its own, so start it only when you want that.

    powershell -ExecutionPolicy Bypass -File .\cc.ps1 queue      (start; leave the window open)
    powershell -ExecutionPolicy Bypass -File .\cc.ps1 stop       (exit after the current run)

It also stops by itself after 60 runs per session. Results land in `queue\done`, rejected plans and
the reason in `queue\rejected`, liveness in `queue\heartbeat.json`.
(Plan files must be written under another name and renamed to `*.json` inside `inbox`.)

## If cc.ps1 misbehaves: the raw commands

Run from this folder. `$R` is the repo, `$C` is this folder.

    $R = (Resolve-Path ..\Causal-Copilot).Path;  $C = (Get-Location).Path
    docker run --rm -i --init -v "${R}:/app" -v "${C}:/research" -w /app -e CC_REPO=/app -e PYTHONDONTWRITEBYTECODE=1 -e PYTHONUNBUFFERED=1 cc-research:a31aa7c-1 python /research/harness/preflight.py

Replace the last part with `python /research/harness/run_traced.py --dataset data/dataset/Linear_Gaussian --data-mode simulated --stub-llm`
for the dry run, or `python /research/harness/run_plan.py --plan /research/plans/golden.json` for the golden runs.

## Images

- `causal-copilot-cpu:a31aa7c`: built from the repo's `Dockerfile.cpu`, unmodified.
- `cc-research:a31aa7c-1`: adds only what `docker/Dockerfile.overlay` lists (TinyTeX on PATH for
  non-interactive runs, `psutil`, `latexmk` if absent), each with the file and line that needs it.

## Changes after the golden runs (harness version 2)

- `preflight.py`: the "source" shown for the API key was wrong when the key came from `.env` (it said "process environment"). The check now records where the key was before the repo is imported. The key handling itself was never affected.
- `run_traced.py`: `meta.json` now includes `dataset_identity` (SHA-256 of the dataset file, or of each file in the dataset folder).
- `run_plan.py`: a dataset may be given as `research:datasets/<dir>/<file>` to use a derived dataset stored in this folder instead of the repo; a plan may set `"interleave": true` to take repeats round-robin across entries.
- New folders: `datasets/` (derived datasets, mapping and reference graphs for pass 4b) and `analysis/` (analysis code, results, reports; see `analysis/README.md`).

## Pass 4b live repeats (28 runs, about one hour)

    powershell -ExecutionPolicy Bypass -File .\cc.ps1 plan pass4b_stability.json

Optional zero-cost check of the new plan features first (stub LLM, 4 runs, a few minutes, about 100 MB of run folders):

    powershell -ExecutionPolicy Bypass -File .\cc.ps1 plan selftest_stub.json

A run that fails is recorded with its reason and the plan continues. If the plan is interrupted, tell Claude which runs finished; the analysis works on whatever completed, and the remainder can be put in a follow-up plan.

## Bundle 1 (harness version 3)

- `run_plan.py`: a plan may set `"run_timeout_s"` (300..10800) to shorten the per-run time limit.
- `fetch_external.py` and `cc.ps1 fetch`: download public benchmark data into `external\` (CausalArena snapshot from Hugging Face; a few tabular Causal Chambers datasets). No LLM, no key, no cost. Report in `external\FETCH_REPORT.json`.
- `datasets\suite_b1\`: four named real datasets from the repo, each in three label arms on identical numbers. Design, predictions and must-show list: `analysis\reports\bundle1_design.md`.

    powershell -ExecutionPolicy Bypass -File .\cc.ps1 plan bundle1_names.json     (48 live runs, about 2.5-3 hours)
    powershell -ExecutionPolicy Bypass -File .\cc.ps1 fetch                       (independent, no cost)

Run long plans from a plain PowerShell window, not the VS Code terminal.
