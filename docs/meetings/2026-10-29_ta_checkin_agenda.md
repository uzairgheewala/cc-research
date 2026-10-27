# TA check-in 1: brief (Thu 29 Oct 2026, 10:45 am PT, TA: Nate)

Tickets: CRS-01, DLV-05, DLV-07, BND-13. Re-cut 27 Oct by the agent to the course's check-in page
(dsc-capstone.org/2026-27/assignments/projects/q1-week5-checkin): 15-20 minutes, in person, shared with other D04 students,
no slides. The TA checks that we understand the problem, have a Q1 project, have code and know how it is organised, have
data, and know what blocks us. Plain-language background: `docs/meeting_explainer.md`.

**Have open on the laptop:**
- the Q1 repository: `README.md`, then `python run.py reproduce`;
- the site's refinement step page: https://uzairgheewala.github.io/cc-research/copilot/step-refinement.html;
- `analysis/reports/run_trace/q011_gas_void.md`.

## The two-minute explanation (say it, don't read it)
1. **Problem.** Causal discovery learns which variables drive which from data. Causal-Copilot is an LLM agent that does it end
   to end. It picks and runs a statistical algorithm, then has a language model review the graph and write a report.
2. **Question.** What does each step do to the graph, and where do its changes come from: the numbers, the variable names, or
   its own rules?
3. **How we test it.**
   - The agent runs unmodified on tables whose true graph is known.
   - The numbers stay identical while the names change (real, neutral, swapped), and the columns are shuffled.
   - Every model call and every intermediate graph is recorded.
4. **One result.** The review step throws away most of the links the algorithm found, and crashes on 8 of 30 runs. A
   replacement review we wrote keeps the links (0.596 against 0.321) and finishes every run, at under half the cost. It does
   not yet get more arrow directions right (+0.014, interval includes zero).
5. **Next.** Find out when the review should commit to an arrow and when it should leave the direction open (the gas/void
   case below).

## The TA's questions, and our answers
| TA asks | Answer |
|---|---|
| Clear idea of the problem and the techniques? | Yes. Constraint-based discovery (PC, FCI) and score-based (GES); bootstrap support; conditional independence tests (KCI); LLM review of edges. Metrics: adjacency F1 (right pairs) and directed F1 (right arrows), with paired scenario-cluster bootstrap intervals. Connections and directions are studied separately because the agent's errors differ in kind. |
| Feeling off-track? Mentor direction sufficient? | *(Uzair to say in his own words.)* Facts: domain mentor Prof. Huang; group meetings act as standups; the guidance so far is to make progress on Causal-Copilot; the direction was set by us. |
| Idea of the Q1 project? | A controlled replication and stage-by-stage diagnosis of Causal-Copilot, plus a first improvement to its review step, measured live against the unmodified agent. |
| Code started? Where, how organised? | Yes, three public repositories: (1) the Q1 repository, a curated, reproducible export (one command recomputes the results with no API key); (2) our fork of Causal-Copilot (`main` untouched, one branch per change); (3) cc-research, the full research repository with the harness, every analysis, a tracker and the project site. The code tour is in the Q1 repo's `docs/code_tour.md`. |
| Data in hand? Roadblocks? | Data in hand: 30 tables from CausalArena (CC BY 4.0, 10 scenarios × 3 name arms) and five named real datasets (Sachs and four others). Roadblocks: live runs cost API credit (about $5-13 per 30-run series, self-funded) and run on my own machine; some reference graphs are contested (Sachs has at least three published versions). |
| Groups? | *(Uzair.)* Working individually; the only student on the causal-discovery option so far. Quarter 2 groups (2-4) are formed by the mentor; not yet arranged. |
| Concerns about mentor or group? | *(Uzair.)* |
| Questions about expectations? | Below. |

## Code tour (five stops, about 3 minutes)
1. **The agent's refinement step, as published.** Fork `main`, `postprocess/judge.py` and `judge_functions.py`.
   `bootstrap_recommend` (lines 221-262) sorts every cell by its directed bootstrap support; `judge.py` lines 80-81 delete
   the low ones.
2. **Our replacement.** Branch `bld-06-refinement-v2`, `postprocess/refinement_v2_dropin.py`.
   - `v2d` never deletes a link the algorithm found, and gives each pair its commonest bootstrap mark.
   - `apply_names` asks the model only about pairs the data leave open.
3. **How a run is recorded.** cc-research `harness/run_traced.py` and `harness/cc_trace.py`.
4. **The comparison.** Q1 repo `analysis/bld06_live_compare.py`, from recorded states to the table, with the pre-registered
   rule in `plans/bld06_live_prereg.json`. Run `python run.py reproduce`.
5. **One case.** `analysis/reports/run_trace/q011_gas_void.md`.

## Results table (same Docker image, same 30 tables, 21-22 Oct)
| | Unmodified | Refinement v2 |
|---|---|---|
| Runs completed | 22 of 30 | 30 of 30 |
| Adjacency F1 (22 tables both completed) | 0.321 | 0.596 (+0.276, interval +0.206 to +0.335) |
| Directed F1 (same tables) | 0.183 | 0.197 (+0.014, interval −0.017 to +0.038: not established) |
| API cost | $12.57 | $4.84 |

Source: `analysis/results/fork/bld06_live_compare.json`, pre-registration `plans/bld06_live_prereg.json`.

## The gas/void case (if the TA asks "show me something specific")
In scenario q011, the true link is entrained gas → voids. Both versions start from the same algorithm output: linked, direction
open. All 20 bootstrap resamples link the pair.
- **The unmodified rule deletes it.** It reads only directed support (1 of 20 resamples) and treats the pair as weak. The
  model is later asked about the pair and answers that the relationship is "not clearly established", so the link stays deleted.
- **Refinement v2 keeps it, but takes the backward arrow.** Void → gas won 8 of 20 resamples: a plurality, not a majority.
  Once the data set a direction, the model is never asked.
- **What it shows:** a specific defect in each version, and the rule to study next. It is one pair, so it cannot set a
  threshold.

## Next experiment (no new live runs needed)
1. Replay the saved dev cases. Measure how often the current rule commits to a wrong arrow.
2. Write an explicit rule for when direction evidence is sufficient; otherwise leave the direction open.
3. Compare the two rules on the same saved inputs. Report wrong arrows, right arrows, open directions and links separately.
4. Freeze the rule before any fresh cases. Gas/void becomes a regression check, not a tuning case.

## Questions for the TA
1. **Q1 scope:** does the improved, forked Causal-Copilot belong in the Q1 report? Or should Q1 stay the study of the
   unmodified agent, with the fork as a preview?
2. **Repository:** is the Q1 repo's layout (curated export, verbatim analysis code, reduced run states with a manifest, one
   reproduce command) what you want to see? Anything missing for reproducibility?
3. **Checkpoint (Fri 6 Nov):** how long should the prior-work section be? Should the data section cover only the Q1 tables,
   or also the data planned for Q2?
4. **Groups:** is working individually acceptable through Q1, and when should the Q2 group be settled?
5. **Resources:** does the course provide any compute or API budget?
