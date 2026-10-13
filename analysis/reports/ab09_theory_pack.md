# AB-09 Theory pack: five statements, proofs, and checks on every public CausalArena file

Ticket AUD-40 (also RQ-04, RQ-06). Written 2026-10-12. No model calls.

- **Checks:** `analysis/theory_checks.py`. One command (`nice python analysis/theory_checks.py`, 8-11 minutes on
  the shared CPUs) writes `analysis/results/theory/theory_checks.json` and `CONTRACT.json` (`score_bearing: false`).
- **Tests:** `tests/test_theory.py`, 17 hand-checkable cases; all pass.
- **Inputs:** the released files (250 semantic, 250 formula, 100 synthetic) and the stored learned graphs in
  `cc-research/analysis/results/methods/` (7,151 non-failed rows, 7 methods, both column arms).

**Prediction P12:** every statement holds on all public CausalArena files to numerical precision; one counterexample
refutes a statement and forces a restatement.

**Outcome:**
- T1-T4 hold as stated, with the conditions given below.
- **T5 is refuted as briefed.** Its coverage clause is false in general, and false on the data: 70 semantic and 100
  formula target pairs have the same answer in every graph of the class, yet the CPDAG rule abstains on them. T5 is
  restated below, and the restated form holds exactly.
- One further correction to earlier text: "F1 = S × a" holds per file, not for family means (gap up to 0.009).

### Status labels

| Label | Meaning |
|---|---|
| **ours (identity, simple)** | Elementary bookkeeping. Not found in print by AB-15, but not a research contribution. |
| **ours (new)** | A result we have not found in the literature, still elementary in proof. |
| **standard (cite)** | Someone else's theorem; we restate it and check it. |

### Preconditions (checked on every file)

| Family | Files | True graph is a DAG, no 2-cycles | Columns in a topological order | `cc_graph.cpdag_of` = causal-learn `dag2cpdag` |
|---|---|---|---|---|
| Semantic | 250 | 250 | 250 | 250 |
| Formula | 250 | 250 | 250 | 250 |
| Synthetic | 100 | 100 | 100 | 100 |

Every released file lists its columns in causal order. T4 depends on that.

### Notation

**True graph.**
- `T` is the set of true arrows; `A_T` is the set of true adjacencies (unordered pairs).
- `n_T = |A_T| = |T|`, because the truth has no 2-cycles.

**Learned graph.**
- `D` is the set of committed arrows.
- `U` is the set of undecided pairs. The marks in `undecided_pairs` are ignored, as the scorer ignores them.
- `A_P` is the set of predicted adjacencies: the pairs of `D` together with `U`. `n_P = |A_P|`.

**Skeleton and orientation coordinates.** These are the definitions in `rescore_controls.py`.
- `TP_adj = |A_P ∩ A_T|`.
- Skeleton F1: `S = 2 TP_adj / (n_P + n_T)`.
- Among true-positive adjacencies:
  - `right` committed arrows match the true direction;
  - `wrong` committed arrows are reversed;
  - `u_TP` pairs are undecided.
- Commit rate `c = (right + wrong)/TP_adj`; commit accuracy `q = right/(right + wrong)`.
- Orientation accuracy `a = (right + u_TP/2)/TP_adj`.

**Directed scores.** These follow the scoreboard (`causalarena_io.directed_scores`).
- The predicted arrow set `P` is `D` plus the arrows the orientation rule adds for `U`.
- `TP_dir = |P ∩ T|`.
- Directed precision is `TP_dir/|P|` and recall is `TP_dir/n_T`.
- `F1 = 2 TP_dir / (|P| + n_T)`. This equals 0 when `TP_dir = 0`, matching the scorer.

**Rules for undecided pairs.**
- The **random rule** orients each undecided pair by a fair coin.
- `E[F1]` is the expectation under the random rule, computed **exactly** by enumerating the joint distribution of
  `(TP_dir, |P|)` over the coins. It is not sampled.

---

## T1. Directed F1 = S × a

**Status:** ours (identity, simple). AB-15 found no prior statement. ACDB's layered metrics and Petersen's
random-guess expectations are the nearest relatives.

**Condition (C): every predicted adjacency yields exactly one arrow.** Concretely:
- `D` contains no 2-cycle;
- no pair is both committed in `D` and listed in `U`.

Under (C), `|D| + |U| = n_P`.

**Statement.**
1. Let a rule `ρ` turn each undecided pair into exactly one arrow (the coin, or the authors' "lower" rule, for
   example). Under (C), its directed F1 is
   `F1_ρ = S × a_ρ`, where `a_ρ = TP_dir(ρ)/TP_adj`.
2. For the random rule in particular,
   `E[F1] = S × a`, with `a = c q + (1 − c)/2`.
3. **Corrected form.** If a rule yields `m` arrows, then
   `F1_ρ = S × a_ρ × (n_P + n_T)/(m + n_T)`.
   - Rule "both": `m = n_P + |U|`.
   - Rule "drop": `m = n_P − |U|`.

   If (C) fails and the coin can add a second arrow on an already-committed pair, `|P|` becomes random and no product
   form holds. Example: truth `0→1`, `D = {0→1}`, `U = {0−1}`. Then `E[F1] = 5/6`, while `S × a = 3/2`.

**Proof.**
1. **Denominators.** Under (C), each predicted adjacency carries exactly one predicted arrow, so `|P| = n_P`.
   - The precision denominator is the number of predicted adjacencies.
   - The recall denominator `n_T` is the number of true adjacencies, because the truth has no 2-cycles.
2. **Numerator.** An arrow can be a true arrow only if its pair is a true adjacency. On each true-positive adjacency
   exactly one arrow is predicted, and it is in `T` exactly when its direction is right. So `TP_dir` counts the
   true-positive adjacencies whose predicted arrow is right.
3. **The identity.** Combining the two:
   `F1 = 2 TP_dir/(n_P + n_T) = [2 TP_adj/(n_P + n_T)] × [TP_dir/TP_adj] = S × a_ρ`.
   If `TP_adj = 0`, both sides are 0.
4. **The random rule.** The denominator `n_P + n_T` does not depend on the coins, so the expectation passes through:
   `E[F1] = 2 E[TP_dir]/(n_P + n_T)`.
   Each true-positive adjacency contributes 1 if committed right, 0 if committed wrong, and 1/2 if undecided. So
   `E[TP_dir] = right + u_TP/2 = a × TP_adj`.
   Substituting `right = c q TP_adj` and `u_TP = (1 − c) TP_adj` gives `a = c q + (1 − c)/2`.
5. **The corrected form.** With `m` arrows, the precision denominator is `m` instead of `n_P`. That gives the
   factor `(n_P + n_T)/(m + n_T)`.

**No correction term is needed for reversed true adjacencies.** A reversed adjacency is still a true-positive
adjacency: it counts in `S`, and it counts as 0 inside `a` through `q`. Only the arrow count, which sets the precision
denominator, can break the product. ∎

**Numerical check:** 7,151 rows (every non-failed row of 7 methods × 3 families × 2 arms). All pass.

| Quantity | Max abs. error over all rows | Tolerance |
|---|---|---|
| Exact `E[F1]` − `S × a` | 2.8e-16 | 1e-12 |
| `a` − (`c q + (1 − c)/2`) | 1.1e-16 | 1e-12 |
| Stored "lower" F1 − `S × a_lower` | 2.8e-16 | 1e-12 |
| Stored "both" F1 − corrected form | 2.8e-16 | 1e-12 |
| Stored "drop" F1 − corrected form | 2.8e-16 | 1e-12 |
| Stored sampled random-rule F1: distance to nearest support point of the exact distribution | 5.0e-16 | 1e-9 |

- **Condition (C)** holds in all 7,151 rows. No row has a 2-cycle or a pair that is both committed and undecided.
- **Sampled vs exact.** For each method, family and arm, the mean of (sampled − exact) was divided by its exact
  standard error, giving a z-score.
  - All 38 groups have |z| ≤ 1.31; the largest is GES formula shuffled, z = +1.31.
  - LiNGAM and NOTEARS have no undecided pairs, so for them z = 0 identically.
  - The stored random-rule scores therefore differ from the exact expectation only by coin noise.
- **One pitfall found and fixed in the checker.** In the shuffled arms the stored "lower" score orients by the column
  order the method saw, not the released one. The check uses the runner's permutation, seed `20261010 + crc32(file)`.

Per method and family (released arm; shuffled arms identical up to 2.8e-16):

| Method | Semantic max err | Formula max err | Synthetic max err |
|---|---|---|---|
| PC (Causal-Copilot copy) | 2.2e-16 | 1.7e-16 | 2.2e-16 |
| PC (upstream causal-learn) | 2.2e-16 | 1.1e-16 | n/a |
| PC maxP (upstream) | 2.2e-16 | 1.7e-16 | n/a |
| GES (BIC) | 2.2e-16 | 2.2e-16 | 2.2e-16 |
| FCI | 2.2e-16 | 1.7e-16 | 2.8e-16 |
| DirectLiNGAM | 1.1e-16 | 2.2e-16 | 1.1e-16 |
| NOTEARS | 1.1e-16 | 8.3e-17 | 1.1e-16 |

The full per-arm table is in the JSON under `statements.T1.per_method`.

**Limits.**
1. **Per file, not for averages.** The identity holds file by file. The mean of `S × a` over files is not
   `mean(S) × mean(a)`.
   - The gap reaches 0.009 (NOTEARS synthetic: mean F1 0.177 against 0.168 from the product of means) and 0.007
     (GES semantic: 0.527 against 0.520).
   - AUD-28's "about 0.46 for maxP by F1 = S × a (family means)" is consistent with the measured mean of 0.461, but
     only by luck of small covariance. Quote measured mean F1, not products of means.
2. **FCI.** For PAGs every non-tail-arrow edge is an undecided pair for the scorer, so `a` is a scoring convention
   there, not an orientation accuracy in the PAG sense.

---

## T2. Three-term error budget

**Status:** ours (identity, simple). The lemma `K ≥ 0` below is ours (new, elementary). AB-15 found no prior error
budget of this form.

**Credits.** For a true adjacency `e`, define two credits:
- the **true CPDAG's credit** `v_C(e)`: 1 if `e` is compelled, 1/2 if the CPDAG leaves it undecided;
- the **method's credit** `v(e)`: 1 if committed right, 0 if committed wrong, 1/2 if undecided.

**Shorthands.**
- `a_C = Σ_{e ∈ A_T} v_C(e) / n_T`.
- `N = n_P + n_T`.
- `Σ_TP` sums over the method's true-positive adjacencies.

**Terms.** Define
- **identifiability** `I = 1 − a_C`;
- **finite-sample skeleton error** `K = a_C − (2/N) Σ_TP v_C(e)`;
- **algorithm orientation error** `O = (2/N) Σ_TP (v_C(e) − v(e))`.

The orientation error splits into three parts:
- `O_wrong = (2/N) × #{compelled, committed wrong}`;
- `O_abstain = (2/N) × ½ × #{compelled, left undecided}`;
- `O_beyond = (2/N) × ½ × (#wrong − #right on pairs the CPDAG leaves undecided)`.

**Statement.**
1. Under (C), `1 − E[F1] = I + K + O` exactly.
2. `I` is the loss of the true CPDAG under the random rule: `I = 1 − E[F1(true CPDAG)]`.
3. `I ≥ 0` and `K ≥ 0`. `O` is signed: `O_beyond < 0` when a method commits correctly on pairs the equivalence class
   cannot orient. A method can do that by luck, or legitimately through functional form (LiNGAM) or layout.

**Reading the terms through a hybrid graph.** Let `H` be the method's skeleton oriented as the true CPDAG would orient
it: compelled true adjacencies right, class-undecided ones by coin, false adjacencies arbitrary (they never score).
By T1,
- `F1(H) = (2/N) Σ_TP v_C`;
- `F1(true CPDAG) = a_C`, because the CPDAG's skeleton is the true one and so `S = 1`.

So
- `I = 1 − F1(true CPDAG)`;
- `K = F1(true CPDAG) − F1(H)` is the loss from replacing the true skeleton by the learned one, with orientation held
  at the oracle;
- `O = F1(H) − E[F1]` is the loss from the method's own orientation on the adjacencies it found.

**Proof of the sum.**
1. The sum telescopes: `I + K + O = 1 − (2/N) Σ_TP v(e)`.
2. Each true-positive adjacency contributes `v(e)` to `E[TP_dir]`, and `n_P` is constant under (C). So
   `(2/N) Σ_TP v(e) = E[F1]`, as in T1.
3. Statement 2 is T1 applied to the true CPDAG, which satisfies (C) and has `S = 1`. ∎

**Proof that `K ≥ 0`.**
1. Write `t = TP_adj`, `W = Σ_TP v_C` and `V = Σ_{A_T} v_C`. Then `K = V/n_T − 2W/N`.
2. Two facts bound `W`:
   - every missed true edge has `v_C ≥ 1/2`, so `V ≥ W + (n_T − t)/2`;
   - every credit is at most 1, so `W ≤ t`.
3. Since `N ≥ t + n_T`, it is enough to show `2W n_T ≤ (t + n_T)(W + (n_T − t)/2)`.
4. This rearranges to `W (n_T − t) ≤ (n_T − t)(n_T + t)/2`. That holds because `W ≤ t ≤ (n_T + t)/2`. ∎

In words: with oracle orientation, a learned skeleton never beats the true one, even if it drops exactly the edges the
class cannot orient.

**Numerical check:** 7,151 rows. All pass.

| Check | Max abs. error | Tolerance |
|---|---|---|
| `I + K + O` − (`1 − E[F1]`), per file | 2.2e-16 | 1e-12 |
| `I` − (1 − exact `E[F1]` of the true CPDAG) | 3.3e-16 | 1e-12 |

- `K < 0` occurs in 0 rows, as the lemma says.
- `O < 0` occurs in 104 rows, 78 of them on synthetic files (mainly LiNGAM, NOTEARS and GES), where `O_beyond` is
  negative.

Family means. Released arm for all methods; both arms for PC. Each method row is averaged over the files that method
finished, so `I` varies slightly between methods.

| Method | Family | Arm | Files | 1 − F1 | I | K | O | O: wrong on compelled | O: undecided on compelled | O: beyond class | Old split (skeleton / orientation) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PC (Causal-Copilot copy) | semantic | released | 250 | 0.667 | 0.043 | 0.382 | 0.241 | 0.197 | 0.045 | -0.000 | 0.346 / 0.278 |
| PC (Causal-Copilot copy) | semantic | shuffled | 250 | 0.573 | 0.043 | 0.372 | 0.159 | 0.121 | 0.040 | -0.002 | 0.334 / 0.196 |
| PC (Causal-Copilot copy) | formula | released | 250 | 0.697 | 0.029 | 0.457 | 0.211 | 0.134 | 0.075 | +0.002 | 0.428 / 0.240 |
| PC (Causal-Copilot copy) | formula | shuffled | 250 | 0.645 | 0.029 | 0.452 | 0.165 | 0.094 | 0.071 | +0.000 | 0.422 / 0.194 |
| PC (Causal-Copilot copy) | synthetic | released | 97 | 0.725 | 0.125 | 0.334 | 0.265 | 0.223 | 0.034 | +0.008 | 0.240 / 0.359 |
| PC (Causal-Copilot copy) | synthetic | shuffled | 97 | 0.614 | 0.125 | 0.330 | 0.159 | 0.129 | 0.031 | -0.002 | 0.236 / 0.252 |
| PC (upstream causal-learn) | semantic | released | 225 | 0.645 | 0.040 | 0.382 | 0.223 | 0.173 | 0.051 | -0.002 | 0.347 / 0.258 |
| PC (upstream causal-learn) | semantic | shuffled | 226 | 0.576 | 0.040 | 0.381 | 0.154 | 0.108 | 0.048 | -0.002 | 0.346 / 0.189 |
| PC (upstream causal-learn) | formula | released | 175 | 0.700 | 0.026 | 0.460 | 0.215 | 0.129 | 0.085 | +0.000 | 0.433 / 0.241 |
| PC (upstream causal-learn) | formula | shuffled | 177 | 0.652 | 0.026 | 0.460 | 0.166 | 0.087 | 0.080 | -0.000 | 0.434 / 0.192 |
| PC maxP (upstream) | semantic | released | 225 | 0.539 | 0.040 | 0.382 | 0.117 | 0.073 | 0.045 | -0.001 | 0.347 / 0.152 |
| PC maxP (upstream) | semantic | shuffled | 226 | 0.538 | 0.040 | 0.381 | 0.116 | 0.072 | 0.045 | -0.001 | 0.346 / 0.151 |
| PC maxP (upstream) | formula | released | 175 | 0.640 | 0.026 | 0.460 | 0.155 | 0.073 | 0.081 | +0.001 | 0.433 / 0.181 |
| PC maxP (upstream) | formula | shuffled | 177 | 0.640 | 0.026 | 0.460 | 0.154 | 0.074 | 0.079 | +0.000 | 0.434 / 0.180 |
| GES (BIC) | semantic | released | 225 | 0.473 | 0.040 | 0.333 | 0.099 | 0.092 | 0.010 | -0.002 | 0.302 / 0.131 |
| GES (BIC) | formula | released | 184 | 0.535 | 0.025 | 0.392 | 0.118 | 0.105 | 0.013 | -0.001 | 0.371 / 0.138 |
| GES (BIC) | synthetic | released | 71 | 0.509 | 0.161 | 0.271 | 0.078 | 0.073 | 0.022 | -0.017 | 0.153 / 0.196 |
| FCI | semantic | released | 225 | 0.645 | 0.040 | 0.383 | 0.221 | 0.026 | 0.197 | -0.003 | 0.349 / 0.255 |
| FCI | formula | released | 178 | 0.682 | 0.025 | 0.450 | 0.207 | 0.025 | 0.182 | +0.000 | 0.425 / 0.232 |
| FCI | synthetic | released | 93 | 0.625 | 0.129 | 0.323 | 0.172 | 0.023 | 0.157 | -0.008 | 0.226 / 0.269 |
| DirectLiNGAM | semantic | released | 250 | 0.804 | 0.043 | 0.607 | 0.153 | 0.165 | 0.000 | -0.012 | 0.580 / 0.180 |
| DirectLiNGAM | formula | released | 250 | 0.745 | 0.029 | 0.548 | 0.168 | 0.174 | 0.000 | -0.006 | 0.523 / 0.194 |
| DirectLiNGAM | synthetic | released | 100 | 0.805 | 0.122 | 0.613 | 0.069 | 0.075 | 0.000 | -0.006 | 0.554 / 0.129 |
| NOTEARS | semantic | released | 250 | 0.854 | 0.043 | 0.641 | 0.170 | 0.175 | 0.000 | -0.005 | 0.614 / 0.197 |
| NOTEARS | formula | released | 250 | 0.831 | 0.029 | 0.579 | 0.224 | 0.225 | 0.000 | -0.001 | 0.555 / 0.247 |
| NOTEARS | synthetic | released | 100 | 0.823 | 0.122 | 0.644 | 0.056 | 0.078 | 0.000 | -0.022 | 0.591 / 0.109 |

**What the table says.**
- **Identifiability** costs 0.03-0.04 on semantic and formula files and 0.12-0.16 on synthetic files.
- **The skeleton** is the largest term for every method (0.27-0.64).
- **PC's layout effect lives entirely in `O_wrong`.** Upstream PC loses 0.173 to wrong arrows on compelled edges in
  released order against 0.108 shuffled. Its `K` is the same in both arms. With maxP, `O_wrong` is 0.073 in both arms.
- **FCI's orientation loss is almost all abstention** (0.197). That is the scorer's price for circle marks, not
  wrong arrows.

**Relation to the 2026-10-07 budget (`error_budget_and_order.md`).** That budget used a different intermediate graph:
"own skeleton, every found edge right", whose F1 is `S`.
- Its two terms are skeleton `a_C − S` and orientation `S − E[F1]`.
- The last column of the table reproduces it: 0.346 / 0.278 for the Causal-Copilot PC copy, semantic, against
  0.35 / 0.28 in that note.
- The old orientation term also charges the algorithm for edges the class cannot orient:
  `S − E[F1] = O + (2/N) Σ_TP (1 − v_C)`.
- The old skeleton term can be negative. The new split separates the two and keeps `I, K ≥ 0`.

**Limits.**
1. **What "identifiability" means here.** It is relative to the true CPDAG, which is what conditional-independence
   methods without interventions can reach (Meek 1995; Andersson et al. 1997). Methods that use functional form
   (LiNGAM) can legitimately beat it, and that shows up as negative `O_beyond`.
2. **Coin variance.** The budget is for the expected F1 under the coin. A single sampled run differs from it by coin
   noise (T1).
3. **Labels.** "Finite-sample" in `K` is a label. For the Causal-Copilot copy, part of `K` is the engine defect found
   by AUD-27, not sample size.

---

## T3. Bounded harm of orientation-only knowledge (invariant I5)

**Status.**
- **Standard (cite):** the rule that knowledge only orients surviving adjacencies and never adds one. It appears in
  pcalg's `addBgKnowledge` (per AB-15) and in Li & Russo, UAI 2026, Sec. 4.2. Li & Russo also measure harm in
  low-quality LLM cells (mean ΔF1 −0.122, Sec. 6.2).
- **Related, not the same:** Chen, Ban, Wang, Lyu & Chen (arXiv 2306.07032). For hard edge priors in hill climbing,
  they show that order-consistent wrong priors cost at most one SHD up to equivalence, under their assumptions, and
  that order-reversed priors can cause "quasi-circles".
- **Ours (new, elementary):** only the exact bound below, for directed F1 under orientation-only knowledge on a fixed
  skeleton. No other novelty is claimed.

**Setting.**
- Start from a data-only output `(D, U)` satisfying (C).
- A knowledge step picks a set `Δ` of `k` predicted adjacencies and sets one arrow on each. It never adds or removes
  an adjacency (I5).
- `Δ` must include every pair whose arrow changes, including pairs re-oriented by propagation rules that the knowledge
  triggered.

**Statement.** Let `N = n_P + n_T` and let `v` be the method's credit as in T2.
1. **Exact change.**
   `E[F1'] − E[F1] = (2/N) Σ_{e ∈ Δ ∩ A_T} (v'(e) − v(e))`, with `v'(e) ∈ {0, 1}`.
2. **Harm bound.**
   `harm ≤ B(Δ) = (2/N) Σ_{e ∈ Δ ∩ A_T} v(e) ≤ 2 min(k, TP_adj)/N = S × min(k, TP_adj)/TP_adj`.
3. **Gain bound.** `gain ≤ (2/N) Σ_{Δ ∩ A_T} (1 − v(e))`.
4. **Tightness.**
   - `B(Δ)` is attained exactly by knowledge that is wrong on every decided true adjacency.
   - The k-bound `2 min(k, TP_adj)/N` is attained when, in addition, all `min(k, TP_adj)` decided pairs are true
     adjacencies that the data-only output had right.

**Proof.**
1. **Nothing outside `Δ` changes.** I5 fixes `A_P`, so (C) still holds, `n_P` is unchanged, and `N` is unchanged.
   Each undecided or committed pair outside `Δ` keeps its arrow or its coin.
2. **So only the credits on `Δ` move.** By T1, `E[F1] = (2/N) Σ_TP v(e)`. The only terms that change are those of
   pairs in `Δ ∩ A_T`. False adjacencies in `Δ` score 0 before and after.
3. **The bounds.** Each changed term moves from `v(e)` to `v'(e) ≥ 0`, which gives the harm bound. Each `v(e) ≤ 1`
   and `|Δ ∩ A_T| ≤ min(k, TP_adj)`, which gives the k-bound. The gain bound follows from `v'(e) ≤ 1`.
4. **Equality.** It holds when `v'(e) = 0` on every decided true adjacency. For the k-bound it additionally needs
   `v(e) = 1` on `min(k, TP_adj)` of them. ∎

**Example attaining the k-bound.**
- Truth `0→1→2→3`; the data-only output is exactly the truth. So `N = 6` and F1 = 1.
- Knowledge reverses `0→1` and `1→2` (`k = 2`).
- F1 becomes 2/6, a harm of 2/3 = `2 × 2/6`.
- This is in `tests/test_theory.py`, along with a case where `B(Δ) = 3/7` is attained with mixed credits.

**Contrast: knowledge that may add connections.** Add `m` arrows on pairs that are neither predicted nor true.
- Directed F1 becomes `2 TP_dir/(N + m)`, so `harm = F1_0 × m/(N + m)`.
- The touched pairs had credit 0, so no bound of the form "credit of the pairs touched" can hold.
- The harm tends to all of `F1_0` as `m` grows, and SHD rises by exactly `m`, without limit.
- Under I5, harm is local: it is capped by the credit of the decided pairs and by `2k/N`. SHD changes by at most `k`.

**Numerical check.**
- **Data:** the 803 non-failed upstream PC rows (semantic and formula, released and shuffled).
- **Truth-derived tiers.** Each adjacency between tiers is drawn from the earlier tier to the later one. Tier
  schemes, built from true depth (the longest chain into a variable):
  - reversed depth (adversarial);
  - reversed depth in 3 bins;
  - 20 random permutations of depth levels;
  - 20 random permutations of 3 depth bins;
  - 20 random 3-tier assignments of variables.
- **Two controls:**
  - true depth, a gain check;
  - "adversarial all pairs", where every predicted true adjacency is set against the truth.
- **Total:** 51,392 checks. All pass.

| Scheme | Checks | Bound violated | Mean ΔF1 | Min ΔF1 | Mean `B(Δ)` | Mean k-bound | Share of `B(Δ)` used when harmful |
|---|---|---|---|---|---|---|---|
| true depth | 803 | 0 | +0.220 | +0.020 | 0.361 | 0.581 | n/a |
| reversed depth | 803 | 0 | −0.361 | −0.758 | 0.361 | 0.581 | 1.000 |
| reversed depth, 3 bins | 803 | 0 | −0.151 | −0.391 | 0.151 | 0.337 | 1.000 |
| random depth order (×20) | 16,060 | 0 | −0.069 | −0.694 | 0.361 | 0.581 | 0.404 |
| random 3 depth bins (×20) | 16,060 | 0 | −0.028 | −0.391 | 0.151 | 0.337 | 0.680 |
| random variable tiers (×20) | 16,060 | 0 | −0.046 | −0.417 | 0.241 | 0.490 | 0.335 |
| adversarial, all pairs | 803 | 0 | −0.361 | −0.758 | 0.361 | 0.581 | 1.000 |

- **Exact-change identity** (statement 1), recomputed from the oriented graph: max error 2.6e-16.
- **Adversarial schemes attain `B(Δ)`:** max error 1.1e-16.
- **Reversed depth zeroes directed F1 in every file.** Every true edge crosses depth levels, so all true-positive
  adjacencies are decided wrong.
- **Edge-adding contrast** (`m` = 1, 5, 25 added false arrows): the formula `F1_0 m/(N + m)` holds to 1.9e-16. Harm
  exceeds the touched-pair credit (0) in 803 of 803 rows for every `m`. Mean harm is 0.006, 0.028 and 0.105; the
  maximum at `m = 25` is 0.250.

**Limits.**
1. **Expected F1 only.** The bound is for expected F1 under the coin on a fixed data-only output. It says nothing about
   effects of knowledge on the skeleton search, which I5 forbids.
2. **Propagation counts toward `k`.** If an implementation propagates knowledge through Meek rules, every
   re-oriented pair must be counted in `k`. The bound is then in terms of that larger `k`.
3. **Decision value.** Directed F1 is the only metric bounded here. Reachability claims (T5) can change on pairs that
   no decided arrow touches, because a new arrow can open a directed path.

---

## T4. Order dependence of PC's collider-conflict rules

### T4a (standard, cite)

Colombo & Maathuis, "Order-independent constraint-based causal structure learning", JMLR 15:3921-3962, 2014
(arXiv 1211.3295; read in full by AB-15 and re-checked for this note).
- **Sec. 3.3, Example 3.** With the skeleton and separating sets fixed, PC's v-structure step is still
  order-dependent when two unshielded triples imply conflicting arrowheads on one edge. In pcalg's implementation at
  the time, "conflicting edges are simply overwritten", so the orientation is decided by the v-structure considered
  last.
- **Theorems 2-3.** The PC-stable skeleton is order-independent (oracle and sample versions).
- **Theorem 5.** CPC-stable and MPC-stable make order-independent v-structure decisions.
- **Theorems 6-7.** Only the list-based versions (LCPC-stable, LMPC-stable), which mark conflicts with bi-directed
  edges, are fully order-independent as CPDAG output.
- **Sec. 7.** A further minor order dependence remains through the order in which the orientation rules are applied.

Ramsey, "Improving accuracy and scalability of the PC algorithm by maximizing p-value", arXiv 1610.00378, 2016
(abstract only): for each unshielded triple, maxP decides the collider using the conditioning set with the highest
p-value. Ramsey's abstract claims no order-independence theorem, and we claim none for maxP in general.

In causal-learn 0.1.4.8 (code read for this note), maxP with `uc_priority=3` applies collider claims sorted by
p-value rather than by column index. So the outcome depends on column order only through exact p-value ties and the
orientation-rule order noted by Colombo & Maathuis.

### T4b (ours, new, elementary; specific to the causal-learn 0.1.4.8 implementation)

**Proposition.** Consider `uc_sepset` (`uc_rule=0`) on a fixed skeleton and fixed separating sets. A **collider
claim** `(x, y, z)` is an unshielded triple with `y` in no separating set of `{x, z}`. It asks for arrowheads into `y`
on the edges `x−y` and `z−y`.

1. **Processing order.** Claims are processed in non-decreasing order of the middle vertex's column index. The
   reason: `find_unshielded_triples` pairs adjacencies listed by `find_adj()` in row-major order of the endpoint
   that becomes the middle.
2. **Priority 2 (default).** For an edge `{u, v}` with column index `u < v`: if any claim at `u` is applied, the edge
   ends `v→u` and no later claim changes it.
   - The reason: claims at `v` are skipped once `v→u` is fully directed.
3. **Priority 0 (overwrite).** Every claim is applied and the last one wins. So any edge with a claim at `v` ends
   `u→v`.
4. **Meek's rules** (`Meek.meek`) do not re-orient the arrows the collider phase sets.
5. **Columns in causal order** (a topological order of the true DAG). For a true edge `u→v` (so `u < v`):
   - every claim at `u` is wrong, since it puts the arrowhead into the cause;
   - every claim at `v` is right.

   Hence, on every conflicted true edge:
   - priority 2 returns the wrong arrow whenever the claim at the earlier column is applied;
   - priority 0 always returns the right arrow.

   With the columns in reverse causal order the roles swap. In shuffled order, both rules are right or wrong
   according to where the column positions happen to fall.

**Argument.**
- Points 2 and 3 follow directly from the code paths:
  - priority 0 removes the edge and re-adds it as `x→y`, `z→y`;
  - priority 2 re-adds only if neither `y→x` nor `y→z` is already fully directed.
- Point 5 is the definition of a topological order: the cause has the smaller index.

**The mechanism in one line.** Under priority 2, "keep the first collider" keeps the claim decided first. Claims are
processed by the index of the collider vertex, and in causal order a smaller index means more upstream. So the arrow
that survives a conflict points upstream, which is wrong. ∎

What makes conflicts arise is finite-sample error, typically a spurious collider at the upstream endpoint, as in the
example below. How often that happens is measured, not proved.

### Worked example

**Setup.**
- True DAG `a → b → c ← d`. Its CPDAG is `a − b, b → c ← d`.
- The CI "test" is a hand-coded table, registered as a custom causal-learn test (`register_ci_test`, a `CIT_Base`
  subclass in `theory_checks.toy_pc`):
  - d-separation in the true DAG, returned as p = 0.5 + 0.01|S| when separated and 0.001 when connected;
  - two finite-sample errors: `p(a ⫫ c | ∅) = 0.08` and `p(a ⫫ c | {d}) = 0.07`.
- α = 0.05; PC-stable.

**Walk-through.**
1. **Skeleton.** `a − b`, `b − c`, `c − d` (correct). `a − c` is removed at level 0 with separating set ∅, because
   of the error.
2. **Claims.**
   - `(a, b, c)`: `b ∉ ∅`, so a **spurious** collider at `b`, asking for `c → b` (wrong).
   - `(b, c, d)`: `c ∉ sep(b, d) = ∅`, so the true collider at `c`, asking for `b → c` (right).
   - The two claims conflict on `b − c`.
3. **maxP.** For the triple `(a, b, c)`, maxP compares the highest p-value among separating sets containing `b`
   (0.52, from `{b, d}`) with the highest among those without `b` (0.08). It finds no collider, so there is no
   conflict.

Output of causal-learn 0.1.4.8 `pc(...)`. Each row was predicted before the run and checked in `theory_checks.json`
under `statements.T4.toy`; all six match.

| Column order | `uc_rule`, `uc_priority` | Output | vs. true CPDAG |
|---|---|---|---|
| a, b, c, d (causal) | 0, 2 (default) | a→b, **c→b**, c−d | wrong arrowhead into b; d→c missed |
| a, b, c, d (causal) | 0, 0 (overwrite) | a→b, b→c, d→c | b→c right; a→b over-committed |
| a, b, c, d (causal) | 1, 3 (maxP) | a−b, b→c, d→c | equals the true CPDAG |
| d, c, b, a (reversed) | 0, 2 (default) | a−b, b→c, d→c | equals the true CPDAG |
| d, c, b, a (reversed) | 0, 0 (overwrite) | a→b, **c→b**, d→c | wrong arrowhead into b |
| d, c, b, a (reversed) | 1, 3 (maxP) | a−b, b→c, d→c | equals the true CPDAG |

The same skeleton and the same tests give a wrong arrowhead under the default rule only in causal order, under
overwrite only in reverse order, and never under maxP.

### Numerical check on the released files

**Coverage.** Every semantic and formula file. Released and shuffled orders, the shuffle being the runner's seed. For
each file: one PC-stable skeleton (Fisher z, α = 0.05), then `uc_sepset` with priority 2 and with priority 0.
Files with a singular correlation matrix are skipped: 25 + 24 semantic and 75 + 73 formula, the same files the
upstream runs failed on.

**What was checked.**
1. The triple order (point 1).
2. That a re-implementation of the rule in `uc_model` reproduces causal-learn's collider-phase output edge for edge
   (points 2-3).
3. That Meek keeps the collider-phase arrows (point 4).
4. That priority 0 sends every conflicted edge into the higher-index endpoint.

All hold in all 803 file-arm runs.

| Family / arm | Files | Conflicted edges | p2: into lower / higher index | p0: into higher index | Conflicted true edges | Wrong, p2 | Wrong, p0 | Claims on true edges at lower index, wrong |
|---|---|---|---|---|---|---|---|---|
| semantic / released | 225 | 1,703 | 1,442 / 211 | 1,703 | 1,208 | **1,013 (83.9%)** | **0 (0%)** | 1,582 of 4,772, all 1,582 wrong |
| semantic / shuffled | 226 | 1,708 | 1,494 / 155 | 1,708 | 1,212 | 534 (44.1%) | 613 (50.6%) | 2,380 of 4,791 (1,588 claims wrong in all) |
| formula / released | 175 | 838 | 755 / 66 | 838 | 468 | **421 (90.0%)** | **0 (0%)** | 690 of 2,125, all 690 wrong |
| formula / shuffled | 177 | 842 | 725 / 86 | 842 | 470 | 215 (45.7%) | 227 (48.3%) | 1,079 of 2,142 (693 claims wrong in all) |

**What the table shows.**
- On conflicted true edges in released (causal) order, the default rule is wrong 84-90% of the time and overwrite 0%.
  Shuffled, both are near a coin.
- Over all true edges oriented in the collider phase, released order:
  - default: 41.7% wrong (semantic) and 42.7% (formula);
  - overwrite: 10.5% and 13.4%.
- Shuffled, the two rules are 25-28% wrong (semantic) and about 27% (formula).

This is the mechanism behind AUD-28's q gap: 0.59 released against 0.74 shuffled for the default, the sign flipping
under overwrite, and no gap under maxP.

**Limits.**
1. **Implementation-specific.** T4b is a statement about causal-learn 0.1.4.8's `uc_sepset` processing order. Another
   library that orders triples differently (pcalg, Tetrad, gCastle) needs its own check.
2. **The trigger is measured, not proved.** That conflicts arise, and that the upstream claim is the spurious one,
   is measured on these files. The 1,582 claims at the upstream endpoint are 33% of claims on true edges (semantic,
   released).
3. **No general order-independence claim for maxP.** The measured released-vs-shuffled gap for maxP is 0.001 in q.

---

## T5. Decision-value ceiling of the true CPDAG

### Statement as briefed

1. For DV-1 claims ("is Y reachable from T": yes / no / abstain), the true CPDAG's committed claims are always
   correct:
   - "yes" means a directed path in the CPDAG;
   - "no" means no possibly directed path.
2. Its coverage equals the share of (T, Y) pairs whose answer is constant over the Markov equivalence class.

**Part 2 is false.** It fails in general and on CausalArena's files. Part 1 holds.

### Restated

1. **(Soundness; standard elements, our assembly.)**
   - A directed path from T to Y in the CPDAG is a directed path in every DAG of the class.
   - If the CPDAG has no possibly directed path from T to Y, then Y is not a descendant of T in any DAG of the
     class.
   - So the CPDAG's committed claims are true in every DAG of the class. In particular they are true in the true DAG:
     precision 1.
2. **(Coverage.)** `coverage = constant share − definite-cause share`.
   - The **constant share** is the share of pairs whose answer is the same in every DAG of the class.
   - The **definite-cause share** is the share of pairs where T is an ancestor of Y in every DAG of the class but the
     CPDAG has no directed path from T to Y.
3. **(When the briefed form holds.)** Coverage equals the constant share exactly when the second share is zero. That
   share can be positive.

### Proof

**Soundness of "yes".**
1. Every directed edge of a CPDAG has the same orientation in every member of the class. That is what the CPDAG
   (essential graph) represents: Meek 1995; Andersson, Madigan & Perlman, Ann. Statist. 25(2), 1997.
2. So a directed path in the CPDAG is present in every member.

**Soundness of "no".**
1. Suppose a member DAG has a directed path from T to Y.
2. Each of its edges appears in the CPDAG either with the same orientation or undirected.
3. So the CPDAG has a path from T to Y with no edge pointing back towards T: a possibly directed path.
4. Contrapositive: no possibly directed path in the CPDAG means no member has Y as a descendant of T.

**The converse is a cited result.** If there is a possibly directed path, some member has Y as a descendant of T: T is
not a definite non-cause. Fang et al. 2022 (Sec. 3.1) state "a variable X is a definite non-cause of another variable
Y if and only if there is no partially directed path from X to Y", citing Zhang (2006) and Perković et al.
(UAI 2017, arXiv 1707.02171).

**From soundness and the converse to the coverage formula.**
- "No" is complete for constant-"no" pairs, so every constant-"no" pair is covered.
- "Yes" via a directed path is sound but not complete.

**Counterexample to the briefed coverage clause.** Fang, Liu, Geng, Zhu & He, "A local method for identifying causal
relations under Markov equivalence", Artificial Intelligence 2022 (arXiv 2102.12685), give the general
characterisation: Theorem 1, via the critical set. Their Examples 1-2 (Sec. 3.2) show definite causes with no directed
path in the CPDAG. A minimal case, in `tests/test_theory.py`:
1. Truth `T → A → Y ← B ← T`.
2. CPDAG: `T − A`, `T − B` undirected; `A → Y ← B` compelled.
3. The class has 3 DAGs. `A → T ← B` is excluded because it would add a v-structure.
4. In every one of them, Y is a descendant of T, through `T → A` or `T → B`.
5. The CPDAG has no directed path `T ⇒ Y`, so the directed-path rule abstains on a pair whose answer is constant. ∎

### Numerical check

**Method.**
- Data: all 250 semantic and 250 formula files, with the targets used by `decision_value.py` (≥ 5 single-target
  rows in the obs+int file).
- Every member of each true class was enumerated: compelled arrows plus every acyclic, v-structure-free orientation of
  each chain component (Andersson et al. 1997).
  - The largest class has 144 DAGs.
  - In total 3,475 member DAGs (semantic) and 1,125 (formula).
  - The first 64 members of each class were checked to reproduce the true CPDAG; 0 mismatches.

| Family | Files | Pairs | Coverage (here) | Coverage (`decision_value.json`) | Precision, every member | Constant share | Constant "yes" but abstained | Constant "no" but abstained |
|---|---|---|---|---|---|---|---|---|
| Semantic | 250 | 20,750 | 0.925301 | 0.9253 | 1.0 (6,815 yes + 12,385 no) | 0.928675 | **70 (0.337%)** | 0 |
| Formula | 250 | 34,115 | 0.959402 | 0.9594 | 1.0 (9,170 yes + 23,560 no) | 0.962333 | **100 (0.293%)** | 0 |

- **Restated coverage identity.** `coverage = constant share − definite-cause share` holds exactly in both families
  (difference 0 by count).
- **Briefed identity.** `coverage = constant share` fails, by 0.0034 (semantic) and 0.0029 (formula). P12 is refuted
  for the briefed T5; the restatement holds.
- **Completeness of "no".** Zero constant-"no" pairs are abstained, consistent with the cited converse on every pair
  checked.

### Limits

1. **The ceiling is the directed-path rule's, not the class's.** The 0.925 semantic ceiling is the coverage of the
   directed-path rule. Coverage over all pairs the class determines is 0.929. A rule using Fang et al.'s critical-set
   criterion would reach it.
2. **Precision 1 rests on assumptions.** It assumes the true graph is a DAG without latent confounders or selection,
   and the CPDAG is the population (oracle) one. For PAGs and latent variables the corresponding theory is Zhang
   (JMLR 9:1437-1474, 2008, causal reasoning with ancestral graphs).
3. **Background knowledge.** Fang, Zhao, Liu & He (arXiv 2207.05067; JMLR 26, 2025) show that pairwise background
   knowledge decomposes into an MPDAG plus residual clauses. The analogue of this check for MPDAGs is not done here.
4. **What DV-1 asks.** DV-1 asks whether Y is a descendant of T, not whether the effect is identified or non-zero. A
   descendant can still have a zero total effect under path cancellation (non-faithful parameters); that is not
   checked.
5. **Only the targets.** Only released intervention targets are T. On other variables the shares may differ.

---

## Summary for the audit paper

| Statement | Status | Holds on all public files? | Max error | Restatement |
|---|---|---|---|---|
| T1 F1 = S × a | ours (identity, simple) | yes, 7,151 rows; condition (C) met in all | 2.8e-16 | none; per file only, not for family means (gap ≤ 0.009) |
| T2 I + K + O | ours (identity, simple); `K ≥ 0` lemma ours (new) | yes, 7,151 rows | 2.2e-16 | `O` is signed (negative in 104 rows) |
| T3 bounded harm under I5 | ours (new) for the exact bound; rule standard (Li & Russo; pcalg); related Chen, Ban et al. | yes, 51,392 checks, 0 violations; bound attained to 1.1e-16 | 2.6e-16 | `k` must include propagated orientations |
| T4 conflict rules and order | standard (Colombo & Maathuis 2014) + ours (new, implementation-specific) | yes; toy example 6/6; mechanism reproduced in 803/803 runs | exact (counts) | none |
| T5 CPDAG ceiling | standard elements (Meek; Andersson et al.; Zhang; Perković et al.; Fang et al.) | precision yes; **briefed coverage clause no** | coverage gap 0.0034 / 0.0029 | coverage = constant share − definite-cause share (holds exactly) |

## References

The labels below record how much of each work was read: primary text read by AB-15 or for this note, abstract only,
or not opened.

**T1-T2**
- Andersson, Madigan & Perlman, "A characterization of Markov equivalence classes for acyclic digraphs", Ann. Statist.
  25(2), 1997. Standard; not re-read for this note.
- Meek, "Causal inference and causal explanations with background knowledge", UAI 1995. Standard; not re-read.

**T3**
- Chen, Ban, Wang, Lyu & Chen, "Mitigating prior errors in causal structure learning: towards LLM driven prior
  knowledge", arXiv 2306.07032. Read via AB-15.
- Li & Russo, "Leveraging large language models for causal discovery: a constraint-based, argumentation-driven
  approach", UAI 2026, PMLR 337 (arXiv 2602.16481). Read via AB-15.

**T4**
- Colombo & Maathuis, JMLR 15, 2014 (arXiv 1211.3295). Read: Sec. 3.3, Theorems 2-7, Sec. 7.
- Ramsey, arXiv 1610.00378, 2016. Abstract only.
- causal-learn 0.1.4.8 source: `UCSepset.py`, `GraphClass.find_unshielded_triples`, `cit.register_ci_test`. Read.

**T5**
- Fang, Liu, Geng, Zhu & He, Artificial Intelligence 2022 (arXiv 2102.12685). Read: definitions, Theorem 1,
  Examples 1-2.
- Fang, Zhao, Liu & He, arXiv 2207.05067 (JMLR 26, 2025). Abstract and summary via AB-15 and AU-3.
- Perković, Kalisch & Maathuis, "Interpreting and using CPDAGs with background knowledge", UAI 2017 (arXiv
  1707.02171). Not opened here; cited through Fang et al. 2022 and AU-3.
- Zhang, "Causal reasoning with ancestral graphs", JMLR 9, 2008. Abstract via AB-15.
