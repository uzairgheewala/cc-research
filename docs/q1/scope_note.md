# Quarter 1 scope: hidden common causes, time series, 100+ variables (DOM-12)

Written 2026-10-10. Code facts with file:line: `analysis/reports/bnd03/dom12_scope_code_facts.md` (gate A1 passes on it,
`analysis/results/bnd03_citations.json`). This note is a **proposal**; the G1 decision on 16 Oct confirms or changes it.

| Topic | What Causal-Copilot offers (measured in code) | Quarter 1 | Quarter 2 |
|---|---|---|---|
| Hidden common causes | FCI is the only wrapper that emits PAG marks (`wrappers/fci.py:103-160`). Whether confounding is suspected is decided only by LLM prompts. Refinement deletes marks by directed-edge bootstrap frequency (`postprocess/judge_functions.py:221-237`); the LLM review can only write `->` (`postprocess/judge.py:103-110`). Effect estimation treats `<->` and `o->` as parents (`causal_inference/inference.py:242-246`, micro-test in `analysis/reports/bnd03/evidence/`). | Measure what happens to PAG marks at each stage (already done offline and live for FCI runs: bundle 1, pass 4b). Report the effect-estimation defect as a finding. | A refinement that keeps PAG marks, and a PAG-aware score. |
| Time series | PCMCI, VARLiNGAM, DYNOTEARS, Granger, NTSNOTEARS wrappers. Time-series mode is set only by the LLM (`global_setting/Initialize_state.py:151-153`). The CLI path dereferences a `revised_graph` that is None after a lagged result (`main.py:307`, code trace). Granger needs integer column names (`causal_discovery/wrappers/granger_causality.py:93`). | Not run. A static note only (this file and AUD-14). | Fix-free audit runs on a time-series suite, if the Q2 proposal includes it. |
| 100+ variables | Scaling depends on CUDA and `externals/acceleration` (not audited); no execution timeout (`causal_discovery/program.py:9-82`); refinement asks the LLM about every pair and runs one KCI test per pair (`postprocess/judge_functions.py:236, 477-480`). | Not run. Our suites stay at 5-25 variables (`docs/q1/datasets.md`). | CPU paths (FGES, PC Fisher-z, XGES) at 50-100 variables without the LLM; LLM cost scaling measured on a stub. |

Reasons for the split: the Quarter 1 deliverable is a rigorous study of the unmodified pipeline on a fixed suite; each of
the three topics would need either new datasets with known truth, a GPU, or code fixes before a single run is meaningful.
Across all three, the repo's benchmark scorer orients every non-directed edge from the truth
(`causal_discovery/evaluation/evaluator.py:154-215`, default at :285), so no paper number in these areas is comparable to ours
until that is replaced.
