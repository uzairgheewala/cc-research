# DRAFT (not sent; Uzair decides): Causal-Copilot's cycle step crashes with KeyError 'nodes'

Ticket: EXT-03. Repository: Lancelot39/Causal-Copilot, commit a31aa7c. Status: draft for the maintainers; nothing has been
sent. Evidence lives in cc-research (paths below).

## What happens

When the graph that refinement hands to the cycle step contains a directed cycle, `postprocess/judge_functions.py`
`LLM_remove_cycles` asks the model to pick an edge and returns `response['nodes']`. The system prompt never names the key
`nodes`, so the JSON reply often uses another key, and the run stops with `KeyError: 'nodes'` (judge_functions.py:562).
The run then delivers no final graph and no report.

How often, on unmodified a31aa7c with gpt-4o (every run recorded by the cc-research harness):

| Run set | Crashed in the cycle step | Source |
|---|---|---|
| Bundle 1 (4 named real datasets x 3 name arms x 4 repeats) | 7 of 48 | `analysis/partial_stages.py` (docstring), bundle 1 runs |
| BND-08 (10 CausalArena semantic scenarios x 3 name arms) | 6 of 30 | `analysis/results/stability_s2/bnd08_summary.json` |
| Same 30 tables, rebuilt image, 22 Oct (main control) | 8 of 30 | `plans/results/fork_bld06_live_main.capped.json`, `analysis/results/fork/bld06_live_compare.json` |

The crash happens only when the graph handed to the cycle step is cyclic by the pipeline's own test (checked in every run:
`analysis/partial_stages.py` gate Q2), so it hits exactly the runs that need the step.

## Smallest fix (tested on a branch of our fork)

`jobs/fork/ext-03-cycle-step-key.patch` (one file, `postprocess/judge_functions.py`):

- name the key in the system prompt (`{"nodes": ["<cause>", "<effect>"]}`);
- read the reply defensively (the `nodes` key, else a single list value), and require two names that are on the cycle;
- otherwise remove the cycle's closing edge (last node to first), deterministic and logged.

On the branch's stub runs (`analysis/results/fork/fork_ext03_stub.json`) the cycle step ran without a KeyError. We have not
yet run the branch live on its own; the live comparison we did run (branch `bld-06-refinement-v2`, which replaces the
refinement stage) completed 30 of 30 runs on the same tables.

## Also worth knowing

- The `VarList` pydantic model declared in `LLM_remove_cycles` is never used (no structured-output call), which is probably
  where the key was meant to come from.
- A cycle can reach this step because refinement adds LLM-chosen directions on top of the algorithm's graph; our measurements of
  that stage are in `analysis/reports/bnd08_s2_results.md` (M1: the bootstrap step lowers PC's adjacency F1 on 19 of 23 dev
  replay files).
