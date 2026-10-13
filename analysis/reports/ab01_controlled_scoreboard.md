# AB-01 Controlled scoreboard: CausalArena complete

Ticket: AUD-33. Written 2026-10-13. No model calls. Results are in `analysis/results/rescore_v2/` (`rescore_controls_v2.py`). New runs:

- `baseline_variants_run.py`:
  - PC from upstream causal-learn 0.1.4.8 with the default collider rule, maxP and definite maxP;
  - GIES with the released intervention targets, using `gies` 0.0.3 with seeded jitter of 1e-6.
- Synthetic PC runs with a 300 s limit per file.

## Where we are now

Every published scoreboard method we can run now has numbers in three settings:

- released columns with the authors' rule;
- released columns with the expectation rule;
- shuffled columns with the expectation rule.

All three use the same files, paired across arms. The scored families are semantic, formula and synthetic (100 public files), in regime D; and semantic and formula in regime D+I (GIES with targets).

## Corrected leaderboard

The controlled number is the last numeric column: columns shuffled, undecided pairs oriented at random.

| Family | Method | Regime | Published | Released, authors' rule | Released, expectation | **Controlled** | Files |
|---|---|---|---|---|---|---|---|
| semantic | GIES with targets | D+I | 0.568 | 0.551 | 0.539 | **0.539** | 250 |
| semantic | GES (BIC) | D | 0.552 | 0.550 | 0.528 | **0.528** | 225 |
| semantic | PC upstream, maxP (ours, configuration change) | D | - | 0.529 | 0.462 | **0.463** | 225 |
| semantic | PC upstream, definite maxP | D | - | 0.517 | 0.444 | **0.445** | 225 |
| semantic | PC, Causal-Copilot copy | D | 0.333 | 0.396 | 0.335 | **0.428** | 250 |
| semantic | PC upstream, default rule | D | 0.333 | 0.424 | 0.356 | **0.426** | 225 |
| semantic | FCI (not on the board) | D | - | 0.578 | 0.357 | **0.361** | 225 |
| semantic | DirectLiNGAM | D | 0.203 | 0.196 | 0.196 | **0.194** | 250 |
| semantic | NOTEARS | D | 0.203 | 0.146 | 0.146 | **0.146** | 250 |
| formula | GIES with targets | D+I | 0.517 | 0.524 | 0.514 | **0.515** | 250 |
| formula | GES (BIC) | D | 0.467 | 0.491 | 0.468 | **0.470** | 178 |
| formula | PC upstream, maxP | D | - | 0.461 | 0.360 | **0.359** | 175 |
| formula | PC, Causal-Copilot copy | D | 0.220 | 0.398 | 0.304 | **0.355** | 250 |
| formula | PC upstream, definite maxP | D | - | 0.468 | 0.355 | **0.354** | 175 |
| formula | PC upstream, default rule | D | 0.220 | 0.404 | 0.298 | **0.349** | 175 |
| formula | FCI | D | - | 0.518 | 0.311 | **0.318** | 174 |
| formula | DirectLiNGAM | D | 0.240 | 0.255 | 0.255 | **0.244** | 250 |
| formula | NOTEARS | D | 0.185 | 0.169 | 0.169 | **0.168** | 250 |
| synthetic | GES (BIC) | D | 0.480 | 0.571 | 0.487 | **0.487** | 71 |
| synthetic | PC upstream, maxP | D | - | 0.522 | 0.435 | **0.435** | 95 |
| synthetic | PC upstream, default rule | D | 0.307 | 0.383 | 0.300 | **0.396** | 95 |
| synthetic | PC, Causal-Copilot copy | D | 0.307 | 0.350 | 0.273 | **0.383** | 97 |
| synthetic | FCI | D | - | 0.596 | 0.371 | **0.371** | 93 |
| synthetic | DirectLiNGAM | D | 0.207 | 0.195 | 0.195 | **0.195** | 100 |
| synthetic | NOTEARS | D | 0.276 | 0.177 | 0.177 | **0.178** | 100 |

The file counts differ by method because failed or timed-out files are dropped from both arms. Upstream PC raises on singular correlation matrices, GES fails on some synthetic files, and synthetic PC hit the 300 s limit on 3-5 dense files.

## The three layout channels, per family

Each channel is measured in directed F1, paired files.

| Method | Family | Authors' rule: F1_lower − F1_random (released) | Conflict rule: released − shuffled (expectation) | Commit accuracy q, released / shuffled |
|---|---|---|---|---|
| PC upstream, default rule | semantic | +0.068 | −0.070 | 0.59 / 0.74 |
| PC upstream, default rule | formula | +0.106 | −0.051 | 0.58 / 0.74 |
| PC upstream, default rule | synthetic | +0.083 | −0.096 | 0.46 / 0.64 |
| PC upstream, maxP | semantic / formula / synthetic | +0.067 / +0.101 / +0.087 | −0.001 / +0.001 / +0.000 | 0.82 / 0.82; 0.77 / 0.77; 0.73 / 0.73 |
| GES (BIC) | semantic / formula / synthetic | +0.022 / +0.023 / +0.084 | 0.000 / −0.002 / 0.000 | |
| GIES with targets | semantic / formula | +0.012 / +0.010 | 0.000 / −0.001 | |
| FCI | semantic / formula / synthetic | +0.221 / +0.207 / +0.225 | −0.004 / −0.007 / 0.000 | |
| DirectLiNGAM, NOTEARS | all | ≤ 0.010 | ≤ 0.011 | |

The engine-copy channel is the vendored copy minus upstream PC: released arm, expectation rule. It is −0.022 (semantic), +0.006 (formula) and −0.027 (synthetic) in F1. Most of the copy's skeleton defect (AUD-27) is masked here because PC with data rarely reaches the order-sensitive branch. The oracle test is where that defect shows.

## Predictions

These were written in `plans/audit_dag.json` before the runs.

- **P1 is supported for the expectation rule, and just short for the authors' rule on formula.** P1 says GIES with targets gains under 0.01 from shuffling under the expectation rule, and 0.01-0.04 under the authors' rule.
  - Expectation rule: +0.0001 semantic and +0.0006 formula.
  - Authors'-rule gain over shuffled: +0.0125 semantic and +0.0091 formula. Formula is 0.001 under the predicted lower bound. It is not refuted, since refutation needed above 0.05.
- **P2 is supported in all three families.** P2 says PC with maxP gives released and shuffled scores within 0.01.
  - Semantic +0.0011, formula −0.0007, synthetic −0.0003.
  - The order dependence of PC's default rule is removed by a configuration change, as AUD-28 predicted on half the semantic files.

## What changes

1. **The published PC row understates PC.** The same algorithm with an order-free collider rule (maxP) scores:
   - 0.463 on semantic (published 0.333), the 3rd-best published-method number after FoundCause (0.634) and GIES;
   - 0.359 on formula (published 0.220);
   - 0.435 on synthetic (published 0.307).

   No other knob is changed.
2. **The authors' rule inflates every method that leaves pairs undecided.** FCI gains about +0.21 in all three families; it is not on the board, but anyone scoring a PAG with this rule would see it. maxP-PC gains +0.07 to +0.10, and GES +0.02 to +0.08. With the conflict rule, PC's default configuration loses more than the authors' rule gives back. The two channels cancel on semantic (net −0.002), which is why the original order effect looked small and inconsistent.
3. **GIES with targets (D+I) is unaffected by layout.** Ours is 0.539 against a published 0.568 on semantic, and 0.515 against 0.517 on formula. That is a different implementation (Python `gies` with jitter vs pcalg via cdt). The semantic gap of 0.029 is the largest reproduction gap in the table and is noted as such.
4. **Published PC on formula (0.220) is below every arm we ran (0.298-0.404).** We do not know why; we did not run the authors' exact code path for that cell.
5. **Correction from AB-09 (T1).** F1 = S × a holds per file, not for family means. The "≈ 0.46 by S × a" in the AUD-28 report was an approximation; the measured maxP number is 0.462.

## Gates

- **Every runnable published row has released and shuffled numbers under both rules, with files paired: met.** Not runnable here:
  - FoundCause, CDFM, TabCausal, AVICI and other pretrained or GPU models (BND-06 notes);
  - IGSP, SDCD, CaScaLe, CDIS, SEA, DAS, DAGMA and NOTEARS-MLP, which are not in our environments.
- **Must-show:**
  - the corrected leaderboard table is above, with the machine-readable `leaderboard_controlled.json`;
  - the per-family layout gain by channel is above.
