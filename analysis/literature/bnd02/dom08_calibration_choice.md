# DOM-08 — Calibration method for bootstrap edge frequencies

Decision date: 2026-10-10. Setting: for each family there are 25 dev scenarios × 5 replicates. In each replicate, B bootstrap resamples give a frequency p̂(e) ∈ [0,1] for each directed candidate edge e. Semantic scenarios have 17–25 variables, so each scenario has about 270–600 ordered pairs.

## Primary evidence

| Source (URL read) | What it establishes for us |
|---|---|
| Friedman, Goldszmidt, Wyner, *Data Analysis with Bayesian Networks: A Bootstrap Approach*, arXiv 1301.6695 (https://arxiv.org/pdf/1301.6695v1) | Non-parametric bootstrap with m=100 (Sec. 4.1). Bootstrap edge confidence is conservative: "the bootstrap samples are quite cautious" (Sec. 4.2); "high confidence estimations seldom contain false positives" (Sec. 7). The right threshold is domain-dependent (0.8 vs 0.65): "the 'reasonable' level of confidence for thresholding depends on the domain" (Sec. 4.2). **Raw frequency is a ranking, not a calibrated probability.** |
| Meinshausen & Bühlmann, *Stability Selection*, arXiv 0809.2932v2 (https://arxiv.org/pdf/0809.2932v2) | A selection probability is a resampling frequency (Def. 1, Sec. 2.1). The error control is E(V) ≤ q²/((2π_thr−1)p) (Thm 1, Sec. 2.4), and it needs exchangeability of noise variables plus a "not worse than random guessing" condition. Suggested π_thr ∈ (0.6, 0.9). The paper never claims these frequencies are calibrated probabilities of correctness. |
| Jabbari, Naeini, Cooper, *Obtaining Accurate Probabilistic Causal Inference by Post-Processing Calibration*, arXiv 1712.08626 (https://arxiv.org/pdf/1712.08626v1) | Directly on point. Bootstrap-RFCI edge-type frequencies (200 resamples, Fisher-z) are "not guaranteed to represent calibrated posterior probabilities" (Sec. 1). A learned calibrator trained on simulated networks improved calibration (MCE, 5 equal-size bins) for most edge types; A↔B stayed overestimated (Sec. 4). The calibration set was small (N = 70–210 pairs, stratified by edge class and frequency bin; Sec. 3). Isotonic regression and BBQ are named but **not compared** (Sec. 2.3, 4). |
| Niculescu-Mizil & Caruana, ICML 2005 (https://mlanthology.org/icml/2005/niculescumizil2005icml-predicting) | **Primary PDF not verified**: the cornell.edu and citeseerx links failed. Secondary source, scikit-learn docs citing it (https://scikit-learn.org/stable/modules/calibration.html): isotonic is "more prone to overfitting, especially on small datasets"; isotonic is better only "when there is enough data (greater than ~ 1000 samples)"; sigmoid (Platt) "is most effective for small sample sizes". The same page cites Murphy (1973) for the Brier decomposition and warns that Brier mixes calibration with discrimination. |
| Kumar, Liang, Ma, *Verified Uncertainty Calibration*, arXiv 1909.10155 (https://arxiv.org/abs/1909.10155) | Platt and temperature scaling are "less calibrated than reported". Plug-in binned ECE estimators are inaccurate. Scaling-then-binning needs O(1/ε² + B) samples, versus O(B/ε²) for histogram binning (Abstract). |
| Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction*, arXiv 2107.07511 (https://arxiv.org/pdf/2107.07511) | The split-conformal guarantee needs i.i.d./exchangeable calibration points (Sec. 1.1, 6.1). It uses the ⌈(n+1)(1−α)⌉/n quantile. They suggest "n = 1000 is sufficient for most purposes" (Sec. 3.2). Marginal coverage does not give per-group coverage (Sec. 4.1). Dependent data "violate the standard exchangeability assumption" (Sec. 5.3). |

## Options weighed against our data

- **Effective sample size is the scenario, not the edge.**
  - Edges in the same scenario share the graph, the mechanisms and all 5 replicates' data generator, so they are strongly dependent.
  - We have about 7,000–15,000 edge rows per family but only **25 independent units**.
  - For conformal, Angelopoulos & Bates' exchangeability requirement (Sec. 1.1, 5.3) therefore holds only at the scenario level. With n = 25 the coverage quantile has granularity 1/26, which is far below their "n = 1000" guidance.
- **Raw frequency.**
  - Pros: no fitting, nothing to overfit.
  - Cons: Friedman et al. (Sec. 4.2, 7) and Jabbari et al. (Sec. 1, 4) both show it is not calibrated, with direction and size depending on domain and edge type.
  - Role: keep it as the **baseline row**, not the answer.
- **Isotonic regression.**
  - Non-parametric and monotone, but it overfits below about 1,000 independent points (scikit-learn citing Niculescu-Mizil & Caruana; primary not verified).
  - With 25 effective units and roughly 5–10% positive base rate, the step function will chase single scenarios.
  - Role: **reject as primary**. Report it only as a diagnostic.
- **Platt scaling** (logistic on logit(p̂) with Laplace smoothing).
  - Two parameters (slope and intercept), so it is low-variance with 25 units.
  - It preserves the ranking that Friedman et al. say is informative.
  - Kumar et al. warn it can be less calibrated than measured, so its calibration error must be estimated honestly on held-out scenarios (see protocol).
  - Role: **choose this**. Use beta calibration (3 parameters) only if the reliability diagram shows asymmetric distortion; that variant is not separately sourced here.
- **Split-conformal by scenario.**
  - It gives coverage of a set (for example an edge set with controlled miss rate), not a probability per edge.
  - Its guarantee is marginal over exchangeable scenarios, and at n = 25 it is coarse.
  - Role: use it for a **decision layer** later (an edge set with ≥ (1−α) recall of true edges, calibrated over held-out scenarios). Do not use it for per-edge confidence.

## Recommendation

1. **Primary calibrator: Platt scaling on logit(p̂).**
   - Smooth first: p̂ = (k + 0.5)/(B + 1).
   - Fit one calibrator per family, plus a pooled fit with a family-specific intercept as a sensitivity check.
   - Calibrate directed-edge frequency and adjacency (skeleton) frequency separately, because Jabbari et al. found edge-type-specific miscalibration (Sec. 4).
2. **Baseline:** raw frequency. **Diagnostic only:** isotonic regression.
3. **Conformal:** postpone to the set-valued decision layer. If used, apply the ⌈(n+1)(1−α)⌉ quantile over scenario-level nonconformity scores and state the n = 25 granularity in the paper.

## Evaluation protocol

- **Split by scenario (grouped).** All edges and all 5 replicates of a scenario stay on the same side.
  - Use 5-fold GroupKFold over the 25 dev scenarios (fit on 20, evaluate on 5), repeated with 5 different fold seeds.
  - Alternatively use leave-one-scenario-out. Never split edges of one scenario across fit and evaluate.
- **Replicates.** Use the 5 replicates as separate rows inside a scenario, or average p̂ over replicates. Either way, compute CIs by scenario-level bootstrap (resample scenarios, not edges).
- **Primary metric: Brier score** on held-out scenarios, with Murphy decomposition into reliability, resolution and uncertainty (Murphy 1973 via the scikit-learn docs). Reliability is the term the calibrator should reduce. Report log-loss as a secondary metric.
- **ECE.** Use 10 **equal-mass** bins (not equal-width), because edges are sparse. Report it with scenario-bootstrap CIs, since Kumar et al. note that binned plug-in ECE estimates are inaccurate.
- **Reliability diagram.** Equal-mass bins with a count histogram underneath and scenario-bootstrap error bars. Draw it per family and for directed vs skeleton separately.
- **Acceptance rule.** Adopt Platt only if held-out reliability (Brier-REL) or ECE improves on raw frequency and the 95% scenario-bootstrap CI excludes zero. Otherwise ship raw frequency and label it "uncalibrated ranking score".
- **Final check.** The 25 test scenarios (disjoint from dev) are scored once with the frozen calibrator.

## Typed gaps
- Niculescu-Mizil & Caruana primary PDF: not verified (secondary quotation only).
- No paper found that compares Platt, isotonic and conformal specifically for bootstrap edge frequencies at scenario-level n ≈ 25. Our study would be new evidence, and the paper should say so.
