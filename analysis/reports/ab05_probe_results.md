# AB-05 Agent probes: live results so far

Ticket: AUD-37. Prepared in `ab05_probe_prep.md`; the runs are Uzair's (`cc.ps1 probe`, `cc.ps1 plan`).

## Where we are now

| System | Model | Status | Calls | Tokens (prompt + completion) | Cost | Directed F1 (shuffled columns) |
|---|---|---|---|---|---|---|
| causaliq-knowledge | gpt-4o-2024-08-06 | ok (live, 13 Oct) | 1 | 471 + 316 | $0.004 | 0.231 (11 edges proposed for 67 true edges; all from names) |
| PyWhy-LLM | gpt-4o | not yet run | | | | |
| MATMCD | gpt-4o-mini | not yet run | | | | |
| Vashishtha et al. | gpt-4o-mini + gpt-4o | not yet run | | | | |
| Causal-Copilot, second model | gpt-4o-mini-2024-07-18 | **crashed** (live, 13 Oct) at `postprocess/judge_functions.py:562` | 31 | 135,185 + 16,957 | about $0.03 | not scored (crash in refinement, after FCI with the `rcit` test; 28 edges before refinement) |

The causaliq stub assumed 1,120 completion tokens; the live reply used 316. The stub cost estimates are therefore conservative for this agent.

## The Causal-Copilot crash is an upstream defect, and it is not model-specific

`LLM_remove_cycles` sends the prompt "choose an edge to remove this cycle, and save nodes of this edge in a list" with JSON mode on. The code then reads `response['nodes']`, but the prompt never names that key. Across every live run recorded in `runs/`:

| Served model | Key the model chose | Calls | Outcome |
|---|---|---|---|
| gpt-4o-2024-08-06 | `edge_to_remove` | 10 | KeyError, run lost |
| gpt-4o-2024-08-06 | `nodes_to_remove` | 5 | KeyError, run lost |
| gpt-4o-mini-2024-07-18 | `removed_edge` | 1 | KeyError, run lost |
| stub | `nodes` (the stub was written to the code's expectation) | 1,752 | ok |

Of 115 live runs, 16 (14%) died at this line: 15 of 114 on gpt-4o and 1 of 1 on gpt-4o-mini. Three more gpt-4o runs died at start-up (`Initialize_state.py:178`, a KeyError on an empty answer; EXT-03's second item).

Whenever the refinement step meets a cycle, the run lives or dies by which key the model happens to pick. This is the same failure class as CAP-10 (robustness to malformed model output). We do not patch Causal-Copilot: it is measured as shipped. Crashed runs are counted as crashes and scored from the algorithm-stage graph (state `07a`). The issue joins the EXT-03 draft.

## Where we're going

- Run the three remaining probes, each stub first and then live.
- Run the AB-06 Causal-Copilot arm on gpt-4o-mini: the BND-08 grid, 30 runs, about $1 (`plans/ab06_cc_gpt4omini_s2.json`).
- Run the AB-06 agent grid (`plans/ab06/`):
  - 120 runs, an estimated $58 at the plan models, with a $60 total cap;
  - run one agent at a time, cheapest first;
  - details in `ab06_prep.md`.
