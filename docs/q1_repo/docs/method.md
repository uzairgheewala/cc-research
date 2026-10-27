# Method: the controls and the metrics, in plain language

## What Causal-Copilot does to a table (the steps we measure)
1. Reads the table and the user's question; a language model summarises the data and, from the column names, what the domain
   might be ("domain knowledge").
2. Picks a statistical discovery algorithm and its settings (the model ranks candidates).
3. Runs the algorithm: the first graph (we call it S0). Links may be directed (A → B) or left open (A o-o B).
4. **Refinement** (the step this project focuses on): the graph is resampled 20 times (bootstrap); a rule sorts each cell into
   high, middle and low support; the model reviews the middle ones, one variable at a time; a conditional independence test
   (KCI) prunes; a cycle step breaks directed cycles. The result is the delivered graph.
5. Writes a report.

The project site explains each step from the code:
[Inside Causal-Copilot](https://uzairgheewala.github.io/cc-research/copilot/).

## The controls
- **Identical numbers, three name arms.**
  - Each scenario is written three times with byte-identical data: real names, neutral names (V01…), and real names moved
    onto the wrong columns.
  - If a step's output changes between arms, the change came from the names.
- **Shuffled columns and opaque paths.** Column order and file path carry no information about the answer.
- **Code identity.** Every run checks the agent's code against a sha256 manifest of upstream commit `a31aa7c` (or records the
  branch commit and its diff, for fork runs). Nothing is seeded or retried; the recorder only observes.
- **Pre-registration.** The comparison of the two versions (`plans/bld06_live_prereg.json`) was written and hashed before any
  graph was scored. The script checks that hash into its output (`prereg_sha256`).
- **Same image, same tables.** Both versions ran in the same Docker image on the same 30 tables, on 21-22 Oct 2026.

## The metrics
- **Adjacency F1:** are the right pairs linked, ignoring direction?
  - precision = linked pairs that are truly linked / pairs linked;
  - recall = truly linked pairs that are linked / true links;
  - F1 = their harmonic mean.
- **Directed F1:** the same, counting a link only when its arrow points the true way.
  - Only a mark that commits to a direction counts as a prediction (`analysis/cc_graph.py::score`, the convention of DAG-level
    scoreboards). An honest "linked, direction not identified" therefore scores as a miss. That is why directed F1 sits so
    far below adjacency F1.
- **Delivered directed F1:** directed F1 of what the user receives. A run that crashed delivers no graph and scores 0.
- **Paired gain:** branch minus main on the same table, averaged.
  - The 95% interval resamples the 10 scenarios with replacement, 2000 times, with a fixed seed (`score/paired.py`). The
    three arms of one scenario are not independent, so they move together.
  - A gain is "established" only when the interval excludes zero.

## The pre-registered rule
- `drop_in` means:
  - the branch's final adjacency F1 is not lower than main's by more than 0.02 (L2);
  - the algorithm stage agrees between the two arms within 0.03 (L3), so the arms are comparable.
- Outcome: `drop_in`.
  - L2: +0.276, interval +0.206 to +0.335.
  - L3: algorithm stage differs by 0.010.
- Delivered directed F1 (L1): +0.071, interval +0.035 to +0.110. This counts crashes as 0, so it measures completion as much
  as accuracy.
