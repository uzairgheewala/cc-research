# Causal-Copilot, step by step: a controlled replication (DSC 180A, Quarter 1)

Uzair Gheewala · UCSD DSC 180A · domain D04 (causal discovery), mentor Prof. Biwei Huang

**Question.** [Causal-Copilot](https://github.com/Lancelot39/Causal-Copilot) is an LLM agent that runs a statistical causal
discovery algorithm and then has a language model review the graph. What does each step do to the graph, and where do its
changes come from: the numbers, the variable names, or its own decision rules? We run it unmodified on tables with known true
graphs, with the column names controlled, and record every intermediate graph and every model call.

**Q1 result so far.** On 30 tables (10 scenarios × real, neutral and swapped names), the unmodified review loses most of the
connections the algorithm found and crashes on 8 of 30 runs. A replacement review we wrote (refinement v2, on a branch of our
fork) keeps them and finishes every run, at under half the cost. Whether it also gets more arrow *directions* right is not
established: that interval includes zero.

| On the 30 tables (same Docker image, same day) | Unmodified | Refinement v2 |
|---|---|---|
| Runs completed | 22 of 30 | 30 of 30 |
| Links recovered (adjacency F1), 22 tables both completed | 0.321 | 0.596 |
| Arrows recovered (directed F1), same 22 tables | 0.183 | 0.197 (gain +0.014, interval −0.017 to +0.038) |
| API cost | $12.57 | $4.84 |

Every number in this table is recomputed from the recorded runs by `python run.py reproduce` (below).

## Start here

| If you want to | Open |
|---|---|
| see the result recomputed | `python run.py reproduce` (one minute, no API key) |
| follow one true link through both versions | [`analysis/reports/run_trace/q011_gas_void.md`](analysis/reports/run_trace/q011_gas_void.md) |
| understand the controls and the metrics | [`docs/method.md`](docs/method.md) |
| find any piece of code | [`docs/code_tour.md`](docs/code_tour.md) |
| know what the data are and where they come from | [`docs/q1/datasets.md`](docs/q1/datasets.md) and [Data](#data) |

## Layout

```
analysis/                     analysis code, as used in the research repo (copied verbatim, same paths)
  bld06_live_compare.py       the comparison table: reads recorded run states, scores them, paired bootstrap
  cc_graph.py                 graph encoding and scoring (adjacency F1, directed F1)
  trace_q011.py               the gas/void walkthrough (needs the full run archive; its output is committed)
  results/                    committed outputs: fork/bld06_live_compare.json, run_trace/q011_gas_void.json, ...
  reports/run_trace/          the gas/void walkthrough
score/paired.py               paired differences with a scenario-cluster bootstrap interval
datasets/suite_q1s2/          the 30 tables, the true graphs (_reference/*.npy), MAPPING.json (which column is which)
plans/                        the pre-registration (hashed before any graph was scored) and the run lists with costs
runs/<run_id>/state/          the recorded final state of each run, reduced to the two graphs the comparison reads
recorded/MANIFEST.json        for every reduced file: sha256 and size of the full recorded file it came from
docs/                         method, code tour, dataset cards
tests/                        reproduction test
run.py                        reproduce | table | test
tools/export_q1.py            how this repository is produced from the research repository
```

## Data

- **The 30 tables** are in `datasets/suite_q1s2/` (8 MB, in git). They are 10 semantic test scenarios of
  [CausalArena](https://huggingface.co/datasets/LAMDA-Tabular/CausalArena) (licence CC BY 4.0), each written three times with
  byte-identical numbers: real names, neutral names (V01…), and real names moved onto the wrong columns. Columns are shuffled
  and file paths are opaque codes, so neither the order nor the path tells the agent anything. The true graph is the one the
  data were simulated from (`_reference/*.npy`). The suite was frozen on 10 Oct 2026; `docs/q1/datasets.md` lists every
  file's sha256.
- **The recorded runs** (every model call, every intermediate graph, every state snapshot) are too large for git. The two graphs
  per run that the table needs are in `runs/`, reduced; `recorded/MANIFEST.json` gives the sha256 of each full file.

## Dependencies

- To reproduce the results from the recorded runs: Python 3.10 or newer and NumPy (`pip install -r requirements.txt`).
- To run Causal-Copilot live: Docker Desktop, an OpenAI API key, the fork and the research harness (next section). About
  $0.16-0.42 per run with gpt-4o.

## Commands

    pip install -r requirements.txt
    python run.py reproduce     # recompute analysis/results/fork/bld06_live_compare.json and compare with the committed one
    python run.py table         # print the results table from the committed file
    python run.py test          # the reproduction test

## Where the rest lives

- **The agent:** our fork, [uzairgheewala/Causal-Copilot](https://github.com/uzairgheewala/Causal-Copilot).
  - `main` is upstream commit `a31aa7c`, untouched.
  - Branch `bld-06-refinement-v2` (commit `{BRANCH_BLD06}`) holds refinement v2:
    `postprocess/refinement_v2_dropin.py`, called from `postprocess/judge.py`.
  - Branch `ext-03-cycle-step-key` (commit `{BRANCH_EXT03}`) holds the crash fix in the cycle step.
- **The research repository:** [uzairgheewala/cc-research](https://github.com/uzairgheewala/cc-research), commit `{CC_COMMIT}`.
  - It holds the harness that runs the agent in Docker and records it (`harness/run_traced.py`, `harness/cc_trace.py`,
    `harness/live_capped.py`), every analysis, the tracker and the project site.
  - This repository is a curated, reproducible subset of it, produced by `tools/export_q1.py` ({N_FILES} files, exported {EXPORTED_UTC}).
- **The project site:** [uzairgheewala.github.io/cc-research](https://uzairgheewala.github.io/cc-research/). Its
  [Inside Causal-Copilot](https://uzairgheewala.github.io/cc-research/copilot/) section explains every step of the agent from
  its code.

## Limits

- One run per table and arm.
- One model (gpt-4o-2024-08-06).
- 10 scenarios, from one benchmark.
- The intervals resample scenarios, not runs.
