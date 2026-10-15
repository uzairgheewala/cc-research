# AB-05 Agent probes: live results

Ticket: AUD-37. Prepared in `ab05_probe_prep.md`; the runs are Uzair's (`cc.ps1 probe`, `cc.ps1 plan`), 13-14 Oct.
Calibration of the live calls against the stub: `analysis/ab05_live_calibration.py` →
`analysis/results/ab05/live_calibration.json`.

## Where we are now

P8 ("at least three of the five systems run end to end on a 20-40 variable CausalArena scenario") is **supported**:
causaliq-knowledge, PyWhy-LLM and Causal-Copilot on gpt-4o-mini ran end to end. MATMCD and Vashishtha et al. were stopped
by our spending caps, not by an agent failure. Their caps were set from stub runs, and the live answers turned out longer.
**Both resumed and finished on 14 Oct** (the rerun replayed the 1,131 and 2,360 paid answers and added 69 and 53 new calls,
$0.009 and $0.651), so all five systems now run end to end.

| System | Model | Status | Calls | Tokens (prompt + completion) | Cost | Wall time | Directed F1 (shuffled columns) |
|---|---|---|---|---|---|---|---|
| causaliq-knowledge | gpt-4o | ok | 1 | 471 + 316 | $0.004 | 6 s | 0.231 (11 edges, all from names) |
| PyWhy-LLM | gpt-4o | ok | 301 | 113,261 + 114,397 | $1.43 | 21 min | 0.329 (170 edges, all from names) |
| MATMCD | gpt-4o-mini | ok after resume (stopped at our $0.41 cap on 13 Oct) | 1,200 | | $0.42 | 93 min + 1 min | 0.407: identical to its own first PC run |
| Vashishtha et al. | gpt-4o-mini (triplets) + gpt-4o (tie-breaker) | ok after resume (stopped at our $1.27 cap on 13 Oct) | 2,413 | | $1.91 | 137 min + 4 min | 0.407: identical to plain PC (its LLM order contradicts 14 of PC's 39 arrows, which are kept) |
| Causal-Copilot | gpt-4o-mini-2024-07-18 | probe crashed at `judge_functions.py:562`; in the AB-06 arm 26 of 30 runs completed | 31 (probe) | 135,185 + 16,957 | $0.03 | | see `ab06_cc_second_model.md` |

Spent on AB-05: $3.79 of the $5 cap.

On this scenario both hybrids end exactly at their own data-only graph: MATMCD's 390 "yes" constraints change nothing
in its final PC run, and Vashishtha's LLM order only orients pairs PC left open (2 here). Whether that holds across
scenarios is AB-06's P10.

## The stub's estimates were low, and by how much

The stub pads its fake answers to an assumed length; live answers were longer for three of the four agents.

| Agent, call kind | Calls | Live completion tokens (mean) | Stub assumption | Live prompt / stub prompt |
|---|---|---|---|---|
| MATMCD, domain knowledge ("You are an expert in ...") | 600 | 722 | 400 | 1.00 |
| MATMCD, yes/no constraint | 531 of 600 | 3 | 3 | 1.61 (the prompt carries the domain answer) |
| Vashishtha, triplet subgraph | 2,300 | 299 (limit 300) | 200 | 1.00 |
| Vashishtha, gpt-4o tie-breaker | 60 of 113 | 205 | 220 | 1.00 |
| PyWhy-LLM, pairwise | 300 | 381 | 312 | 1.01 |
| causaliq-knowledge | 1 | 316 | 1,165 | 1.00 |

Wall time is the bigger constraint. Calls are sequential inside an agent: MATMCD's domain answers take 8.7 s each, and
Vashishtha's triplets 3.4 s each. A 25-variable scenario therefore takes 1.5 h (MATMCD) or 2.3 h (Vashishtha).

## Vashishtha et al. lose 91% of their votes to their own token limit

The repository asks the triplet model to "give a reasoning for your answer and then output the directed graph" inside
`<Answer>` tags, with `max_completion_tokens=300` (`strategies/triplet.py`, `query_triplet_subgraph`). With the model its
README documents for triplets (gpt-4o-mini), 2,105 of 2,300 answers stopped at the limit (`finish_reason=length`). 2,096 of
them (91.1%) never reached the `<Answer>` tag.

- The parser (`utils/helpers.py`, `parse_answer_tag`) returns nothing for an untagged answer, and the triplet becomes `[]`.
- An empty answer casts no vote of any kind in `merge_triplet_votes`. 90 of the 300 pairs end with no vote at all.
- 113 pairs end tied and go to the gpt-4o tie-breaker; the stub, whose answers always carried the tag, produced 34.
- The repository prints "Warning: no answer for triplet" 2,096 times and carries on.
- So the run "works", but most of its orientation evidence comes from about 113 gpt-4o pairwise calls, not from the
  2,300-call vote the method describes.

This is the same failure class as Causal-Copilot's cycle-step crash (CAP-10: robustness to the model's output format),
with the opposite symptom: Causal-Copilot dies loudly, Vashishtha et al. degrade silently. We measure both as shipped and
patch neither. The finding joins the notes to maintainers (EXT-06).

## The Causal-Copilot crash is an upstream defect, and it is not model-specific

`LLM_remove_cycles` sends the prompt "choose an edge to remove this cycle, and save nodes of this edge in a list" with JSON
mode on. The code then reads `response['nodes']`, but the prompt never names that key. Across every live run recorded in
`runs/` (gpt-4o: bundle 1 and BND-08; gpt-4o-mini: the AB-05 probe and the AB-06 arm):

| Served model | Key the model chose | Cycle-step calls | Outcome |
|---|---|---|---|
| gpt-4o-2024-08-06 | `edge_to_remove` | 10 | KeyError, run lost |
| gpt-4o-2024-08-06 | `nodes_to_remove` | 5 | KeyError, run lost |
| gpt-4o-mini-2024-07-18 | `removed_edge` | 3 | KeyError, run lost |
| gpt-4o-mini-2024-07-18 | `nodes` and `removed_edge` | 1 | survived (the only live survivor) |

Of 19 live entries into the cycle step, 18 crashed. Whenever the refinement step meets a cycle, the run lives or dies by
which key the model happens to pick. Crashed runs are counted as crashes and scored at S3, the graph handed to the cycle
step. The issue is in the EXT-03 draft.

## Where we're going

- Done: both capped probes resumed and finished (14 Oct).
- AB-06: the agent grid is re-planned from these live numbers (`plans/calibrate_ab06.py`, `plans/ab06/BUDGET.json` v2,
  `plans/ab06_prereg.json` and its amendment 1); see `ab06_prep.md`.
