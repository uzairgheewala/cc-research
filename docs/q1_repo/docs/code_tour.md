# Code tour

Five stops, in the order the work happened. Paths in this repository unless a link says otherwise.

1. **The agent's pipeline and its refinement step (upstream, unmodified).**
   - Fork `main`: [`main.py`](https://github.com/uzairgheewala/Causal-Copilot/blob/main/main.py), then
     [`postprocess/judge.py`](https://github.com/uzairgheewala/Causal-Copilot/blob/main/postprocess/judge.py) (`Judge.quality_judge`).
   - The bootstrap rule that deletes links:
     [`postprocess/judge_functions.py`](https://github.com/uzairgheewala/Causal-Copilot/blob/main/postprocess/judge_functions.py)
     `bootstrap_recommend`, lines 221-262; the deletion is `judge.py` lines 80-81.
   - Explained step by step, with the source:
     [Inside Causal-Copilot: refinement](https://uzairgheewala.github.io/cc-research/copilot/step-refinement.html).
2. **Our replacement, refinement v2.**
   - Fork branch `bld-06-refinement-v2`:
     [`postprocess/refinement_v2_dropin.py`](https://github.com/uzairgheewala/Causal-Copilot/blob/bld-06-refinement-v2/postprocess/refinement_v2_dropin.py).
   - `v2d` is the data part: it never deletes a link the algorithm found, and gives each pair its commonest bootstrap mark.
     **This is the direction rule the next experiment revisits.**
   - `apply_names` is the names part: it asks the model only about pairs the data leave open, three phrasings, used only if
     all three agree.
3. **How a run is recorded (research repository).**
   - [`harness/run_traced.py`](https://github.com/uzairgheewala/cc-research/blob/main/harness/run_traced.py) and
     [`harness/cc_trace.py`](https://github.com/uzairgheewala/cc-research/blob/main/harness/cc_trace.py).
   - What they record: every model call (request and raw reply), the state after every stage, and every refinement sub-step's
     inputs and outputs. Here only the final graphs are kept, in `runs/<run_id>/state/`.
4. **The comparison.**
   - `analysis/bld06_live_compare.py` reads those states, scores them with `analysis/cc_graph.py`, computes the paired
     intervals with `score/paired.py`, and applies the pre-registered rule from `plans/bld06_live_prereg.json`.
   - Output: `analysis/results/fork/bld06_live_compare.json`.
5. **One case, end to end.**
   - `analysis/reports/run_trace/q011_gas_void.md`: one true link (entrained gas → voids) followed through both versions.
   - The unmodified rule deletes it although all 20 resamples link the pair. Refinement v2 keeps it, but takes the backward
     arrow, which won 8 of 20 resamples.
