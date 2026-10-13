# Causal-Copilot: ceiling, distance to it, and paper shapes (discussion draft, 2026-10-06)

Companion to `claude/causal-copilot-research-ledger.md`. Written after pass 4b in answer to Uzair's question about the theoretical upper limit, commercial and research value, and a route to a NeurIPS-level paper. Nothing here is a decision.

Changes to standing assumptions (Uzair, 2026-10-06):
- Do NOT count on any answer from Prof. Huang's group. Ledger question Q3 (what produced paper Table 2) is to be answered from the code and our own runs, or reported as an open uncertainty.
- The WorldReset proposal was said to be sent in turn 6 but did not arrive (no attachment, nothing new in the DSC 180A folder). Still needed.

## 1. What "perfect causal analysis" can mean
Three walls that no pipeline removes:
1. Identifiability. Observational data plus the standard assumptions identify an equivalence class (CPDAG, or PAG with hidden variables), not a graph. More is identified only with more assumptions (non-Gaussianity, additive noise, heterogeneity across domains or time), interventions, or outside knowledge.
2. Finite samples. Independence testing has no uniformly valid nonparametric test with power; frequencies from resampling are not probabilities without calibration.
3. Untestable assumptions. Every causal conclusion rests on at least one assumption the data cannot check.

So the ceiling is not "outputs the true DAG". It is an analyst that is: sound (claims nothing beyond data + stated assumptions), complete (claims everything that is implied), calibrated (stated confidence matches hit rate), attributable (each mark names the evidence or assumption that carries it), decision-complete (for a query returns the identified value or sharp bounds, and the next measurement or experiment that would shrink them most), and cheap and repeatable.

## 2. Measurement axes
| Axis | Metric | Gold standard |
|---|---|---|
| Soundness / completeness | over-claim rate (marks asserted but not identified), under-claim rate, distance to true CPDAG/PAG | synthetic structural models with known truth |
| Calibration | ECE / Brier of adjacency and mark confidence; coverage of effect intervals | synthetic; held-out interventions |
| Interventional validity | error predicting held-out interventions; decision regret | real perturbation data (CausalBench, Causal Chambers, Sachs interventional arms) |
| Selection | regret against the best algorithm/hyperparameters in hindsight | synthetic grids |
| Invariance | change in output under neutral or permuted names on identical numbers; run-to-run agreement | our d01/d02/d03 protocol |
| Abstention | risk-coverage curve | synthetic + name controls |
| Attribution | share of final marks with a complete, replayable evidence record | lineage gates |
| Cost | tokens, wall time, crash rate | run records |

## 3. Ladder and where Causal-Copilot stands (evidence: ledger)
- L0 runs end to end unattended: mostly (3 of 28 runs crashed on malformed LLM JSON).
- L1 never worse than its own algorithm, type-preserving: NOT MET (final adjacency F1 below algorithm output in 25 of 25 runs; non-directed edges deleted).
- L2 attributable: NOT MET natively (lineage reconstructed from outside).
- L3 calibrated and abstaining: NOT MET (fixed 20 resamples, thresholds on directed frequency only; LLM answers applied unweighted).
- L4 knowledge used as labelled, defeasible evidence: NOT MET (LLM edges written regardless of data; final accuracy 0.44 / 0.10 / 0.01 on identical numbers depending on the header).
- L5 active (asks for the experiment or variable that matters): absent.
- L6 decision-grade effects with bounds and sensitivity: effect-estimation module exists, unexamined.
Stable today: algorithm and hyperparameter selection (identical within every arm).

## 4. Value
Buyers pay for decisions, not graphs. The market labelled "causal AI" is small (one analyst estimate: USD 56.2M in 2024, 456.8M by 2030). Adjacent decision markets are large and already causal: online experimentation (OpenAI-Statsig reported at USD 1.1B; Datadog-Eppo), marketing incrementality and mix modelling, real-world evidence and target discovery in pharma, root-cause analysis in IT operations. A discovery agent earns its place where experiments are expensive or impossible and a wrong call is costly, and there the selling point is the audit trail and the honest "not identified".

## 5. Where a real advance could come from
- Outside knowledge as accountable evidence: the only way past the identifiability wall without experiments. Pass 4b shows today's use is unaccountable recall.
- Amortised / foundation-model inference (prior-fitted networks): strong on synthetic data, only matching baselines on real systems so far; limited by prior mismatch.
- Closed-loop experiment selection.
- Evaluation realism: on real perturbation data, methods that look good on synthetic benchmarks have not beaten simple baselines. Measurement work has unusual leverage in this field.

## 6. Paper shapes, most reachable first
A. Evaluation paper: "agents report recall as discovery". Stage-attributed, name-controlled, repeated benchmark across several agents, datasets and models, with the label-permutation test and the lineage tool. Needs breadth: at least 3 agents or agent-style pipelines, about 10 datasets with meaningful names including memorisation-resistant ones, 3 models, 5 repeats.
B. A plus a fix: a refinement stage that is sound by construction (type-preserving aggregation; LLM consulted only on adjacent-but-unoriented pairs; contributions labelled), shown to dominate on the benchmark from A. Classic shape for the evaluations track.
C. Method/theory: aggregation and calibration for PAG marks with guarantees. Cleaner, harder, better suited to UAI or CLeaR.
Timeline anchor: NeurIPS 2026 deadlines were 4 and 6 May 2026 (main and evaluations/datasets tracks); 2027 dates not announced. A main-track paper from a solo two-quarter capstone is a stretch; the evaluations track or a workshop is realistic if A is broadened.
