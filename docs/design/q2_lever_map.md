# The lever map: every source of evidence about links and directions, what we use, what we measured, what is left

Written 2026-10-15 after kernel v3 and the stage anatomy (`analysis/reports/q2_v3_anatomy.md`). Companion numbers:
`analysis/q2_headroom.py` -> `analysis/results/q2_v3/headroom_dev.json`. Dev only; no test split read; no model calls.

The operating rule this map serves: a lever enters the kernel only as a typed claim with a licence whose accuracy was
measured on dev before it is acted on. Scores move as a symptom of that; they are never the target of a change.

## 1. The headroom ladder: what each stage's errors cost (dev, DV-1 over all committed answers; directed F1)

Starting from the ledger's own graph, each stage is repaired with the truth in turn, cheapest first.

| Step | semantic v3, 1,000 rows: precision / coverage / F1 | semantic v3, pooled | formula v3, 1,000 rows |
|---|---|---|---|
| O0 the ledger as it is | 0.793 / 0.692 / 0.513 | 0.864 / 0.646 / 0.537 | 0.843 / 0.755 / 0.435 |
| O1 reversed found links turned right | 0.839 / 0.666 / 0.571 | 0.878 / 0.662 / 0.586 | 0.867 / 0.757 / 0.511 |
| O2 + open found links oriented where the truth does | 0.833 / 0.845 / 0.637 | 0.868 / 0.845 / 0.656 | 0.865 / 0.865 / 0.565 |
| O3 + false links removed | 0.859 / 0.962 / 0.780 | 0.895 / 0.959 / 0.835 | 0.854 / 0.979 / 0.771 |
| O4 + missed links added (the truth) | 1.000 / 0.944 / 0.968 | 1.000 / 0.941 / 0.965 | 1.000 / 0.967 / 0.983 |

Headroom by stage (semantic, 1,000 rows): reversed directions +0.046 precision, +0.06 F1; direction commitment +0.15
coverage, +0.07 F1; false links +0.03 precision, +0.14 F1; missed links +0.14 precision, +0.19 F1. Even a ledger that is
perfect on everything it found (O3) answers at 0.86, because a "no" is wrong whenever a missed link sits on the true
path. Missed links are the largest cost at both levels and the hardest to recover (9% of true links are floor).

## 2. Evidence sources for links ("X and Y are directly connected")

Status words: USED (in the kernel, with a measured accuracy); TRIED (measured on dev, failed or neutral at its gate);
UNMEASURED (not yet measured on dev); BARRED (excluded by a design invariant); N/A (no such data on this benchmark).

| # | Source of evidence | Status | Where | Measured | Verdict / what is wrong |
|---|---|---|---|---|---|
| L1 | Marginal dependence (correlation) | USED | PC's first pass; GES score | implicit | fine; misses are weak links (median corr 0.06) |
| L2a | Conditional independence, Gaussian linear (Fisher z) | USED | PC audit of GES (rule C3) | calibrated (10% on separated pairs) but underpowered | the search gap: 14% / 20% of true links are found by this test with the right conditioning set, which the search does not find or keep |
| L2b | Conditional independence, rank-based | TRIED | K1 battery | recovered links 33% precise | fails the precision gate |
| L2c | Conditional independence, nonparametric (cell-mean residual, boosting residual) | TRIED | K1 | 81-94% of mediated shadows still called dependent given the true parents | misspecified at 1,000 rows on these mechanisms; adds shadows faster than links |
| L2d | Conditional independence, mixed-type / discrete-aware | PARTLY (inside the K1 battery, not isolated) | K1 E1 | inside the battery; not isolated | 57% of the semantic floor class touches a discrete column (15% formula): the floor is conditional on the tests used; a discrete-aware test is UNMEASURED on its own |
| L3a | Score-based fit, BIC (GES, lambda 1) | USED | engine | ties GES by construction | the kernel's links are GES's |
| L3b | Score penalty lowered (lambda 0.5) | TRIED | K1 | misses 32 -> 28%, link precision 0.63 -> 0.49, F1 down | fails |
| L3c | Nonlinear / generalised scores (GAM, kernel) | UNMEASURED | - | - | candidate for the nonlinear-only class (5% of true links) |
| L4 | More rows: a scenario's replicates pooled (D x R) | USED (as a regime) | K1 E4 | misses 32 -> 24%, DV-1 0.756 -> 0.816 | the one lever that worked; formula 34 -> 28% |
| L5 | Interventional data as link evidence (does Y shift under do(X) given Y's other parents) | TRIED (l5-1, 19 Oct) | obs_int dev, 125 files per family | reach 20% / 13% of false links; shadow cut (S) at most 36 cuts at 0.67; no-effect cut (N) 37 at 0.65 (formula); adds 9-14% true | no licence; the release is too thin (about 3 effective targets x 40 rows per semantic file; formula's interventions mostly ineffective). The signal is real: given the mediator the shift disappears for 48% of moved shadows and 7% of moved true links. Confirmed links 78% true vs 59% base: a candidate confidence feature |
| L6 | Nonlinear conditional residual (additive-noise style) as a "weak link" claim | TRIED | K1 E2 | precision 0.33-0.43 | fails; not separable from shadows |
| L7 | Resampling stability of a link (bootstrap the skeleton) | TRIED (linkfilt-1, 25 files per family) | AUC true vs false 0.76 / 0.74; cut precision 0.75 / 0.81 | cuts 5% / 38% of false links | licence on formula (0.81, 38%, 8% of true lost); not on semantic; no observable condition says which family a dataset is like (L16) |
| L8 | Shadow detection by strength ordering in ledger triangles (data-processing inequality; Spearman L8a, mutual information L8b) | TRIED (linkfilt-1) | L8a cut precision 0.63-0.71 / 0.81; L8b 0.64-0.68 / 0.73 | L8a cuts 25% of formula false links | licence on formula (L8a); not on semantic, where 83% of the true links it would cut sit in a real triangle (55% of semantic true links do, 35% of formula's); same condition problem (L16) |
| L9 | Link audit: cut a link the battery separates given common neighbours | TRIED | K1 audit | cut 111: 74 false, 37 true; F1 unchanged | neutral |
| L10 | In-degree-aware joint test at variables with many causes (CAP-01) | UNMEASURED | - | - | many-parent children are where conditioning sets are large and tests weak |
| L11 | Declared knowledge adding or removing links | BARRED | invariant: knowledge orients open pairs only; never adds, removes, reverses | - | by design (T3); K3 allows demotion only |
| L12 | Engine fusion (PC, GES agreement / union / GES-led-PC-audited) | USED | rule C3, chosen on dev | C3 best of five rules | other engines (LiNGAM, NOTEARS, FCI, AVICI) measured as baselines in the audit, not fused |
| L13 | Hidden common causes (FCI / PAG marks, CAP-14) | UNMEASURED | - | - | common-cause false links are 26% of false links, but those have an observed common cause; latent-cause handling is a different problem |
| L14 | Time order | N/A | - | - | CausalArena is cross-sectional |
| L15 | Sparsity / degree priors on the skeleton | UNMEASURED | - | - | formula clears ER-2 partly because its graphs are sparser; a prior is a tunable and must be pre-registered |
| L16 | Applicability condition for a link filter: observable from data, or declared as typed knowledge about the domain | TRIED (l16-1, 19 Oct) | 125 dev files per family; L8a | observable: density / triangle-share gates clear the pooled bar (0.800-0.815, 15-20% of false links) at cut-off 0.5, semantic precision 0.72-0.76; every licensed gate fails the transfer guard (within-family rho <= 0.33); G3 real-triangle estimate rho 0.14. Declared: right +0.009 DV-1 / +0.017 coverage / +0.011 F1 (formula); wrong -0.002 / +0.002 / 0.000 with 8.8% of semantic true links withdrawn | observable gate: licensed here, not transferable (not acted on). Declared domain-structure statement: the route to build (bounded harm, T3) |

## 3. Evidence sources for directions ("the found link X-Y points X -> Y")

| # | Source | Status | Measured accuracy on dev (semantic / formula) | Yield | Verdict |
|---|---|---|---|---|---|
| D1 | Collider patterns (v-structures) | USED, licence | 0.87 / 0.83 | 2,507 / 2,145 of ~2,500 committed | the workhorse; its errors are fake colliders built on missed or false links |
| D2a | Meek rule 1 (propagate past a collider) | TRIED (used in v2, withdrawn in v3) | 0.64 / 0.60 | 316 / 257 | too weak to act on; shown as open |
| D2b | Meek rule 2 (acyclicity) | USED, licence | 0.75 / 0.80 | 40 / 56 | kept |
| D2c | Meek rules 3, 4 | USED / N/A | 1 and 4 cases | - | negligible; R4 needs background knowledge |
| D3 | Score-based orientation (GES's own) | USED | same equivalence class as D1-D2 | - | nothing beyond the class |
| D4 | Non-Gaussian noise asymmetry (LiNGAM-style, entropy likelihood ratio) | TRIED (dirsig-1, 2) | 0.52 / 0.50; gated 0.58 / 0.51 | all continuous pairs | no licence; confidently wrong on children with mass points (0.04 semantic); pooled formula passes the rule on 23 open links (lead, not licence) |
| D5 | Nonlinear additive-noise asymmetry (ANM, RECI, IGCI) | TRIED (dirsig-1, 2) | ANM 0.55 / 0.50, RECI 0.57 / 0.61, IGCI 0.56 / 0.62 | all found links | no licence in D; IGCI on pooled formula 0.86 on 153 acted links (lead; needs a fresh family) |
| D6 | Conditional-variance (heteroscedastic) asymmetry | TRIED (dirsig-1, 2) | 0.57 / 0.60 | all found links | no licence |
| D7 | Interventional shifts as order evidence | USED, licence (B2) | measured in B2 | - | strongest source where targets exist; K3-3 false positives on spurious adjacencies |
| D8 | Declared knowledge tiers (orient open pairs only) | USED, licence (B3) | gpt-4o tiers capture 43% / 50% of the oracle tier gain | +0.026 / +0.022 F1 | route B; ceiling +0.060 / +0.044 |
| D9 | Time order | N/A | - | - | - |
| D10 | Conditional distribution similarity (any pair; discrete-aware) | TRIED (dirsig-1, 2) | 0.62 / 0.62; one-parent children 0.77 / 0.76 | all found links | no licence; best single signal; works only where the child has one parent, which the ledger cannot see |
| D10b | Conditional asymmetry: the pair's signal with each end's other ledger neighbours regressed out (C5a, C6, C5b) | TRIED (dirsig-2) | C5a 0.55 / 0.47, C6 0.51 / 0.42, C5b 0.60 / 0.62 | all found links | refuted (P2-4): the conditioning sets are ledger links and carry its errors; on formula conditioning on undetected children reverses the signal |
| D14 | Mass-point side (the clamped end is the child) | TRIED (dirsig-2) | the mass-point end is the child in 0.42 / 0.35 | pairs with one mass-point end | refuted and reversed: categorical and Bernoulli roots carry the mass points; too weak either way |
| D11 | Invariance across environments (ICP-style) | PARTLY | obs_int files only | - | overlaps D7 |
| D12 | Resampling stability of a direction | PARTLY (used for confidence in B4; unmeasured as a filter) | - | - | - |
| D13 | Global acyclicity beyond Meek (reject a direction that closes a cycle with strong evidence) | USED implicitly | Meek R2 | - | nothing beyond |

What the truth allows: only 8.5% (semantic) / 5.5% (formula) of true links are undecidable from observational data in
principle (equivalence-class open). The ledger decides 73% of the found links (v3) and leaves 674 / 532 open that the
truth orients: the direction ceiling is far above where we are, and the equivalence class is not what caps it.

## 4. Which we are addressing, and where it is going right or wrong

- Addressed and right: D1 collider (87%), D7 interventions, D8 tiers at their measured size, L4 pooling, L12 fusion rule,
  the withdrawal of D2a, abstention and calibration downstream of all this.
- Addressed and at their limit: L2a Fisher z (calibrated, underpowered), L3a GES (the kernel's links are its links).
- Tried and refuted at this sample size: L2b, L2c, L3b, L6, L9. The common cause: no test separates a mediated shadow
  from a weak direct link at 1,000 rows on these mechanisms.
- Barred by design: L11 (knowledge never touches links). This is a thesis, not a gap.
- Unmeasured, and the measurement is cheap (seconds to minutes from the cache): D4, D5, D6, D10 as direction licences;
  L5 (interventions for links), L7 (stability as a link filter), L8 (shadow strength ordering), L10 (in-degree-aware
  tests), L2d isolated (discrete-aware test on the floor class), L3c, L15.
- Not applicable here: L14, D9.

Count (corrected 16 Oct; the 15 Oct line said "28 sources, 18 of 26 (69%)", which did not match the tables): on 16 Oct
the tables have 21 link rows and 17 direction rows (D10b, D14, L16 added on 16 Oct), 38 in all, 36 applicable (L14, D9
are not). Status: USED 12, TRIED 14, BARRED 1, PARTLY 4 (L2d, L5, D11, D12), UNMEASURED 5 (L3c, L10, L13, L15, L16), N/A 2.
Measured or ruled: 27 of 36 (75%). History: 19 of 33 (58%) on 15 Oct; 25 of 35 (71%) after the direction rounds;
27 of 36 after the link filters.
19 Oct: L5 (PARTLY -> TRIED) and L16 (UNMEASURED -> TRIED): USED 12, TRIED 16, BARRED 1, PARTLY 3 (L2d, D11, D12),
UNMEASURED 4 (L3c, L10, L13, L15), N/A 2. Measured or ruled: 29 of 36 (81%).

Licence table (measure 4), 16 Oct: acted on in the kernel: D1 colliders, D2b Meek R2, D7 interventions, D8 knowledge
tiers. Licensed on dev but not actable (no applicability condition, L16): L8a and L7 on formula. 19 Oct: L8a is actable through a declared domain-structure statement (L16 declared form; built only on Uzair's go-ahead); its observable gate is licensed on CausalArena but not transferable. Leads (below the
pre-registered regime or family): IGCI on pooled formula.

## 5. How progress and completeness are measured from here (architecture, not scores)

1. Lever coverage: of the applicable sources, the share with a dev measurement and a verdict (USED / TRIED / BARRED).
   Today 69%. Complete when 100%: every source either carries a licence or a written reason it does not.
2. Per-stage headroom (section 1): the ladder is recomputed per kernel version. A version is a refinement when a
   headroom step shrinks without another growing. The ladder also decides what to work on: the largest step first,
   subject to its floor.
3. Attribution budget: every wrong answer has exactly one first cause (anatomy report, section 3). Per version: the six
   buckets (unrelated false link, common-cause false link, reversed link, backward shadow; missed link on path,
   reversed link on path). Progress is a bucket shrinking; a lever that moves the wrong bucket is suspect.
4. Licence table: every direction source that is acted on has its dev accuracy and yield in one table (D1, D2b, D7, D8
   today). A new source enters as a row before it enters the kernel; it is acted on only if its accuracy clears a
   pre-set bar (0.80 proposed, above R2's 0.75 and well above the withdrawn R1).
5. Floor accounting: the missed-link floor (9% / 7%) is conditional on the test battery; each new test class (L2d, L3c)
   re-measures it. A floor that shrinks under a new oracle test was not floor.
6. Invariants: I1-I8 pass on every file (already enforced by the checker); the count of invariants is itself a
   completeness measure of the ledger's typed state.
7. Read budget: held-out reads per family (two on CausalArena); a version is read held out only on a family with an
   unread split or by amendment, and the count is reported with every number.

A version's report carries all seven. Landmark scores appear in the same report as consequences, not as objectives.

## 6. What this says to measure next

Done 16 Oct:
- the collider-free direction signals (`analysis/reports/q2_dirsig_dev.md`): no licence in nine signals; both direction
  routes lead back to the skeleton;
- the link filters L8 and L7 (`analysis/reports/q2_linkfilt_dev.md`): both licensed on formula and not on semantic,
  because semantic scenarios put real direct links beside real mediated paths (55% of true links in a real triangle), the
  same shadow-versus-weak-direct-link wall a third time; neither can act until an applicability condition exists (L16).

Done 19 Oct:
- L16 (`analysis/reports/q2_l16_dev.md`): observable gates are licensed on CausalArena's mixture only by acting at a
  stricter cut-off on denser files, and fail the transfer guard; the declared form is cheap to be wrong about.
- L5 (`analysis/reports/q2_l5_dev.md`): no licence on CausalArena; the shadow signal is real but the release has too
  few targets and rows. Dense-intervention data (CausalBench, BEN-13; a pooled-replicate CausalArena check) is where it
  can be decided.

Next (19 Oct), in order: L2d on the floor class; pooled-replicate L5 (power); L5 rules N / X on Causal Chambers (dense
targets, no shadows); the declared L16 form as a kernel change (on approval); then L10, L15.

Earlier list (16 Oct), in order of headroom times cheapness:
1. L16: design the applicability condition, observable or declared, before any filter enters the kernel.
2. L2d on the floor class: does a discrete-aware test see any of the 459 semantic floor misses (57% touch a discrete
   column)? If yes, the floor was 9% only under the old battery.
3. L5 interventions for links on the obs_int dev files: the one source that separates a real direct link from a shadow
   by construction (setting the mediator breaks a shadow, not a direct link).
4. L10 and L15 as pre-registered tunables, last.

None of these is a kernel change. Each is a measurement that adds a row to the lever map, and the headroom ladder
says afterwards whether the architecture got better.
