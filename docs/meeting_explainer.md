# Causal-Copilot capstone: plain-language explainer (for TA check-in 1, 19-23 Oct 2026)

Written 2026-10-10. Every number below comes from a file named next to it; if a file changes, this page is out of date
(tracker ticket TEAM-02 checks the numbers against their sources).

## What the project is, in one paragraph

Causal-Copilot is an open-source "AI agent" that is given a table of measurements and is meant to work out what causes
what, drawing the answer as a graph of arrows. It runs a standard statistical algorithm and then asks a large language
model (GPT-4o) to review and fix the graph. My Quarter 1 job is to run it, unmodified, on a fixed set of datasets and
measure carefully what each step does to the answer.

## The test I use: same numbers, different column names

Every dataset is given to the agent three times. The numbers are byte-for-byte identical; only the column names change:

- **real**: the true names (e.g. "Age", "Length");
- **neutral**: V01, V02, ... (no hint at all);
- **swapped**: true names, but on the wrong columns.

If the agent were reading the data, the three answers would be the same. If it is reading the names, the answers follow
the names.

## What I found so far (54 runs on four named datasets, plus Sachs)

Source: `analysis/reports/bundle1_results.md`, section 0.

- With real names the final graph agrees with the reference well: arrow accuracy (directed-edge F1) **0.68**.
- With neutral names it falls to **0.02**; with swapped names to **0.07**. Same numbers in all three.
- The language-model step wrote **93%** of the final arrows with real names and **90%** with swapped names, so it writes
  arrows from what the names suggest, not from the data.
- The bootstrap (resampling) step throws away most of the algorithm's undecided edges: **30%** survive.
- **12 of 84** live runs crashed: 9 at one step where the model's answer uses a key the code does not read, 3 at start-up.

In short: on well-known datasets the agent looks good because the language model recognises the names, and the
statistical part of its answer is mostly discarded.

## What happens next (Quarter 1 plan, `analysis/reports/q1_execution_plan.md`)

1. **A fixed dataset suite** (`docs/q1/datasets.md`, frozen 2026-10-10): the five datasets above (S1) plus 10 simulated
   scenarios from the CausalArena benchmark (S2), where the true graph is known exactly and the agent cannot have
   memorised it. Columns are shuffled because the benchmark's files list causes before effects, which leaks the answer.
2. **Baselines**: standard algorithms (PC, GES, FCI, ...) on the same files, scored the way the benchmark scores them.
3. **The live run** of the agent on S2 (30 runs, about the cost of the earlier ones, started by me after a free test run).
4. **A sound refinement**: a version of the review step that cannot make the graph worse than the algorithm's own output
   and only asks the model about pairs the data leave undecided. Tuned on the dev split, tested once on the test split.

## Honest limits

- On the real datasets the "reference graphs" are curated, not known truth. Sachs has at least three published versions
  (19, 17 and 20 edges) and the repo's Auto MPG differs from the benchmark's version
  (`analysis/results/reference_reliability/reliability.json`).
- All language-model runs so far use one model (GPT-4o). A second model is planned.
- The checkpoint (2 Nov) reports only what has run by then; nothing is extrapolated.
