# Applicability conditions for the link filters (L16), on dev

Tickets: TGT-18, TGT-19

Pre-registration `plans/l16_prereg.json`, hashed before any of its numbers existed
(`manifests/evidence/l16_prereg_2026-10-19.sha256`, which also pins the code and its test). Code `analysis/q2_l16.py`
(features G1-G6, the gate search and the declared-condition rows; helpers tested in `tests/test_q2_l16_l5.py`). Results
`analysis/results/q2_v3/l16_dev.json` and per-file rows `l16_files_dev.jsonl.gz`. Dev split only; no test split read; no
kernel change; no model calls. The engine cache was rebuilt on a fresh host for this round; the rebuilt ledgers give the
same links and the same triangle ratios as linkfilt-1 in 250 of 250 files. L7 (the secondary row) was not run: it needs
the 500 resample engines, which were not rebuilt this round. Written 2026-10-19.

## Where we are now

On 16 Oct the triangle-order filter L8a earned a licence on formula (cuts right 81% of the time, a quarter of false links
cut) and not on semantic (63-71%). A kernel that does not know a dataset's family cannot use a family licence. The
question here was whether something it *can* see decides where the filter may act: either a condition computed from the
file itself, or a typed statement about the domain that someone declares.

**Observable: licensed by the letter, not transferable. Declared: cheap to be wrong about.** A gate on ledger density or
triangle share clears the pre-registered pooled bar by 0.003, but it does not rank scenarios within either family, and
on semantic files its cuts are still right only 73% of the time. A declared statement is worth a little when right and
costs almost nothing in answers when wrong. The declared route is the one to build.

## Results

### Observable gates (cross-fitted by scenario; folds mix both families; pooled over both)

| Gate | Cuts | Cut precision | False links cut | Semantic: precision / cut / true lost | Formula: precision / cut / true lost | Licence (pooled) | Transfer guard |
|---|---|---|---|---|---|---|---|
| Selected (all six features searched) | 1,195 | **0.803** | 20.2% | 0.735 / 21.7% / 4.6% | 0.870 / 19.1% / 2.7% | yes | **fails** |
| G1 triangle share | 1,156 | 0.811 | 19.8% | 0.749 / 21.0% / 4.1% | 0.872 / 18.9% / 2.6% | yes | fails (rho 0.18 / 0.26) |
| G2 strong-violation share | 477 | 0.782 | 7.9% | 0.759 / 13.0% / 2.4% | 0.845 / 4.0% / 0.7% | no | - |
| G3 estimated real-triangle share | 251 | 0.693 | 3.7% | 0.737 / 4.3% / 0.9% | 0.654 / 3.2% / 1.6% | no | - |
| G4 discrete-column share | 899 | 0.815 | 15.4% | 0.762 / 12.1% / 2.2% | 0.845 / 18.0% / 3.1% | yes | fails (rho -0.21 / -0.09; family AUC 0.93) |
| G5 monotone gap | 900 | 0.807 | 15.3% | 0.717 / 9.8% / 2.3% | 0.847 / 19.4% / 3.3% | yes | fails (rho 0.09 / 0.09) |
| G6 density | 1,182 | 0.800 | 19.9% | 0.731 / 21.3% / 4.6% | 0.871 / 18.9% / 2.6% | yes | fails (rho 0.33 / 0.18) |
| No gate (post hoc, not pre-registered; best cut-off 0.5) | 1,372 | 0.776 | 22.4% | 0.706 / 24.3% | 0.849 / 21.0% | no | - |

Every licensed gate chose the strictest cut-off (0.5) in every fold. The selected gate is G1 or G6 at roughly their 30th
or 40th percentile; it acts on 84 of 125 semantic files and 86 of 125 formula files. Transfer guard: Spearman rho between
the gate feature and per-scenario cut precision at the gate's cut-off, within semantic / within formula; the bar was
0.30 in both.

Answers with the selected gate's cuts (no re-orientation):

| | DV-1 precision | Coverage | Directed F1 |
|---|---|---|---|
| semantic | 0.793 -> 0.794 | 0.692 -> 0.697 | 0.513 -> 0.521 |
| formula | 0.843 -> 0.853 | 0.755 -> 0.768 | 0.435 -> 0.448 |

What the gate does, in plain words: no cut-off of the ungated filter reaches 0.80 on the mixture (best 0.776 at 0.5).
Skipping the sparsest third of files (few triangles, few links) lifts it to 0.803. That is a real but small effect. It is
not the property that matters (whether the triangles are real), and it does not hold inside a family: within semantic and
within formula, denser files are not reliably the ones where cuts are right.

### Which feature tracks per-scenario cut precision (P-A2)

Absolute Spearman rho over the 48 scenarios with at least 5 cuts, at cut-off 0.7 (pooled): G6 density 0.43, G1 triangle
share 0.41, G4 discrete share 0.34, G5 monotone gap 0.32, G2 0.14, G3 0.14. G3 was meant to estimate the share of
triangles that are real (Storey's 1 - pi0 over the weakest link's partial-correlation p-values). Its medians point the
right way (0.73 semantic, 0.60 formula; the truth has real triangles at 55% and 35%), but scenario by scenario it says
nothing (rho -0.04 within semantic, -0.07 within formula). Each test is underpowered at 1,000 rows, and pooling their
p-values does not rescue them. This is the shadow-versus-weak-direct-link wall a fourth time.

G4 is the family detector named in advance: it separates the two generators almost perfectly (AUC 0.93) and orders
nothing inside either.

### The declared condition

The statement: "mechanisms are mostly chains: few direct effects alongside mediated ones of the same cause", typed as a
domain-structure record that licenses L8a and never cuts a link itself.

| | Cut precision | Cuts | True links lost | DV-1 precision | Coverage | Directed F1 |
|---|---|---|---|---|---|---|
| Right (declared on formula, true there) | 0.808 | 838 (25% of formula false links) | 5.6% | 0.843 -> 0.852 | 0.755 -> 0.772 | 0.435 -> 0.446 |
| Wrong (declared on semantic, false there) | 0.664 | 912 (30% of semantic false links) | 8.8% | 0.793 -> 0.791 | 0.692 -> 0.694 | 0.513 -> 0.513 |

A wrong declaration withdraws 8.8% of semantic true links (they become "no claim", not "independent"), yet answer
precision moves by -0.002 and F1 not at all, because the false links it also withdraws were costing as much. This is a
bounded harm in the same sense as thesis T3 bounds wrong tiers.

## Predictions

| | Verdict |
|---|---|
| P-A1 no observable feature earns the pooled licence for L8a | **Refuted**: four single features and the selected gate clear 0.80 pooled (0.800-0.815), each at the strictest cut-off |
| P-A2 G3 tracks per-scenario cut precision best (abs rho >= 0.40) | **Refuted**: G3 is last but one (0.14); density (0.43) and triangle share (0.41) lead |
| P-A3 any licensed gate fails the transfer guard | **Supported**: all five licensed gates fail it (best: G6, rho 0.33 within semantic, 0.18 within formula) |
| P-A4 a wrong declaration costs <= 0.02 DV-1 precision and <= 0.03 F1, and withdraws > 10% of semantic true links | **Partly**: the cost is -0.002 and 0.000 (supported); true links withdrawn 8.8%, below the predicted 10% |

## What this changes

- **L16 observable: TRIED.** A gate exists that clears the pooled bar on CausalArena, but it fails the pre-registered
  transfer guard, so it is recorded as "licensed here, not transferable" and is not acted on. Its pooled precision
  (0.803) sits 0.003 above the bar, and its semantic precision (0.735) sits below it.
- **L16 declared: the route to build.** L8a may act on a dataset when a typed domain-structure statement licenses it.
  The kernel records the statement as knowledge, the filter does the cutting, and the cost of a wrong statement is
  measured (above) and small in answers. This fits T3: knowledge decides what the data cannot, and never adds or removes
  a link by itself. Building it is a kernel change and waits for Uzair's go-ahead.
- Lever map: L16 moves from UNMEASURED to TRIED (observable) with the declared form designed and its value and harm
  measured.

## Where we're going

L5 (interventions as link evidence) is measured next on the same footing, in `analysis/reports/q2_l5_dev.md`. If it
licenses cuts on semantic, it is the observable route the gates above could not supply, because interventions separate a
shadow from a real direct link by construction.
