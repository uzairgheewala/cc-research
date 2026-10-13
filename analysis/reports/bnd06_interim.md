# BND-06 interim: order sensitivity and more published rows (2026-10-10)

Tickets: BEN-07, REP-07, BEN-11, RQ-16. Pre-registration: `plans/bnd06_prereg.json` (written before any shuffled run).
Numbers: `analysis/results/methods/bnd06_verdicts.json` and the per-method row files beside it. No model calls.

## Q4c: does any data-driven method read the column order? (REFUTED)

Family mean directed F1 on the 250 public semantic files, released vs shuffled column order (one permutation per file,
seed 20261010; graphs mapped back before scoring). Random rule = undecided pairs oriented at random (order-free).

| Method | F1 released | F1 shuffled | difference (random rule) | same under the authors' "lower" rule |
|---|---|---|---|---|
| PC (causal-learn, stable) | 0.335 | 0.428 | **-0.093** | 0.396 vs 0.426 |
| GES (`ges`, BIC) | 0.475 | 0.477 | -0.002 | 0.495 vs 0.477 |
| FCI (causal-learn) | 0.322 | 0.327 | -0.005 | **0.521 vs 0.321** |
| DirectLiNGAM | 0.196 | 0.194 | +0.002 | same |
| NOTEARS (linear) | 0.146 | 0.146 | 0.000 | same |

Prediction: |difference| <= 0.02 for every method (supported), > 0.05 for any (refuted). PC differs by 0.093: **refuted**.

PC's dependence is not in the orientation rule. causal-learn 0.1.3.8's PC with `stable=True` returns a different skeleton in
230 of 250 files when only the column order changes (reproduced directly on one file: 8 adjacencies differ; the same order
rerun is identical). Its committed-direction accuracy is 0.544 in released order and 0.722 shuffled. Released order is
topological, and PC does worse on it. Mechanism not yet diagnosed (candidate: order-dependent separating-set choice
and collider-conflict resolution; PC-stable's skeleton should be order-independent in theory, so this needs a closer look).

Consequences:
- RQ-16's reference number for PC (54% of committed directions right) holds for the released order only; shuffled it is 72%,
  close to GES (81%) and FCI (80%). The Q4a verdict (refuted) is unchanged.
- FCI's 0.32 -> 0.52 under the authors' rule is pure order leak (released vs shuffled under that rule: 0.521 vs 0.321).

## Published rows (REP-07), authors' rule, tolerance 3 SE of a 50-of-100 mean

| Method | ours F1 / SHD | published F1 / SHD | within |
|---|---|---|---|
| LiNGAM | 0.196 / 40.4 | 0.203 / 38.9 | both |
| NOTEARS | 0.146 / 39.3 | 0.203 / 38.1 | SHD only (F1 gap -0.057; tolerance 0.021) |
| GIES (GES) | 0.495 / 36.2 | 0.552 / 33.4 | SHD only; 0.550 without the 5 failing scenarios (BND-04) |
| PC | 0.396 / 35.4 | 0.333 / 33.5 | SHD only (REP-06) |

NOTEARS: our solver follows the authors' adapted `notears/linear.py` step for step (same loss, acyclicity term, bounds,
schedule, thresholds 0 then 0.5; release data are already z-scored), so the gap is not an implementation difference we
can see. It stays open (the unreleased 50 scenarios, or the environment).

## Still to do in BND-06
Pretrained models where DOM-11 found CPU checkpoints (AVICI), the formula family and the 100-file synthetic sample
(`plans/synth_sample_100.txt`, per-file limit 300 s), DOM-09 timing, and the CAP-17 package through `tools/validate_submission.py`.
