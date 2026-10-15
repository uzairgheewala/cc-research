# Paper skeleton (AB-17, AUD-47): spine B, decided 2026-10-14

Decision: `docs/decisions/2026-10-14_wedge_decision.md`. Build pre-registration: `plans/q2_build_prereg.json`, hashed with
this file in `manifests/evidence/paper_prereg_2026-10-14.sha256` before any build run.

Every claim below is typed:

- **measured**: done, with the evidence file named;
- **to build**: a gate in the build pre-registration decides it;
- **desk**: read from documents.

The manuscript is drafted after B1 passes.

## Working title and one-paragraph argument

*Where the arrows come from: controlled audits of LLM-assisted causal discovery, and a claim ledger that never does worse
than its data.*

Published scores for causal discovery mix the method with the file layout. When asked a decision question, learned graphs
rarely beat "nothing moves". LLM-assisted systems take their directions from variable names. Most of them lose 0.10–0.25
F1 when the names are swapped, and one falls below its own data-only output. These failures share a cause: nothing records
where a direction came from, so nothing can stop knowledge from overriding data. We give a record format and a system, a
claim ledger, whose invariants make these failures impossible by construction:

- order invariance;
- never below data-only;
- knowledge orients but never connects;
- every claim checked.

We report its cost against the same controls.

## Claims

| # | Claim | Type | Evidence / gate |
|---|---|---|---|
| C1 | Published CausalArena scores read the column layout through three channels: the index tie-break, PC's conflict rule, and a defective vendored engine. The layout leak pays only under index tie-breaking (Bayesys's half-credit scoring is robust) | measured | `ab01_controlled_scoreboard.md`, `ab02_second_scoreboard.md`, `ab03_engine_forensics.md` |
| C2 | On "if I set T, does Y move?", learned graphs capture 0-55% of the identifiable ceiling on CausalArena; on physical data (Causal Chambers) GES comes within 0.08 | measured | `ab04_decision_value.md` |
| C3 | Name reliance is common: 3 of 5 systems lose ≥ 0.10 directed F1 with swapped names, and the one that resists is the one whose data decide the graph | measured (pre-registered P9) | `ab06_field_audit.md`, `bnd08_s2_results.md`, `ab06_cc_second_model.md` |
| C4 | Knowledge can make an agent worse than its own data: MATMCD falls below its own PC graph on decision value with real names, and far below with neutral or swapped names | measured (pre-registered P10) | `ab06_field_audit.md` |
| C5 | Theory: F1 = S × a per file, a three-term error budget, the exact harm bound for orientation-only knowledge, and the order dependence of conflict rules | measured on all public files | `ab09_theory_pack.md` |
| C6 | Names used only where the data are silent are harmless when wrong and weak when right (refinement v2: swapped within 0.05 in 10/10 families; real names help in 1/10) | measured (BND-11) | `bnd11_results.md` |
| C7 | The claim ledger keeps G1-G5 and G7 on every file and is never below the data-only kernel on held-out files | to build | gates B0-B3 |
| C8 | Its calibrated confidence and abstention meet a stated precision at a stated coverage within family | to build | gate B4 |
| C9 | The ledger's verifier finds the audit's failure classes in other agents' outputs: knowledge creating or removing connections, directions from position, output-contract failures | to build | gate B5 |
| C10 | Declared structure with abstention wins in incident root-cause analysis (0.93 vs 0.21 AC@3, PetShop) | measured; secondary | `ab12_rca_probe.md` |

## Sections

1. Introduction: the argument above; the contributions are C1-C4 (audit), C5 (theory) and C7-C9 (system).
2. Setting and controls: information regimes; name arms; shuffled columns; scoring rules; decision value.
3. Audit of scoreboards: C1, with EXT-01's recommendation.
4. Audit of decisions: C2.
5. Audit of LLM-assisted systems: C3, C4, C6. Output-contract failures: Causal-Copilot's key crash, Vashishtha's
   truncation, the guidance clock crash, gpt-4o's code fences.
6. Theory: C5.
7. The claim ledger: format, invariants, stages; C7-C9.
8. Limits and threats:
   - semantic graphs written with model help (Y1);
   - one benchmark family for the agent audit;
   - tier B not run;
   - interviews absent (C1 of the market is indirect).
9. Related work. Must cite: Colombo & Maathuis 2014 (order dependence), CARE (single-system name collapse), Li & Russo
   2026 (orient-only knowledge), Zheng et al. (agents should not supply edges), Vashishtha et al., MATMCD, PyWhy-LLM,
   causaliq, Causal-Copilot, CausalArena, Bayesys, Causal Chambers.

## Figures (existing unless marked)

| Figure | Source | Status |
|---|---|---|
| F1 | Layout channels per family | `analysis/results/rescore_v2/` (AB-01) |
| F2 | Decision value against "nothing moves" and the ceiling | `analysis/results/decision_value_v2/` figures (AB-04) |
| F3 | Name reliance by system and arm | `analysis/results/ab06/name_reliance.png` |
| F4 | Causal-Copilot's path through (S, a) by stage | site page 6 plots (BND-08) |
| F5 | The ledger: stages and invariants | to draw at B1 |
| F6 | Held-out ledger vs data-only kernel vs published methods | to draw at B1-B3 |
| F7 | Reliability diagram and risk-coverage | to draw at B4 |

## Venue

A methods venue with a benchmark contribution: CLeaR, TMLR, or a main-track ML venue. Dates and formats are checked
before drafting, not assumed here.

## Held-out discipline (binding)

- The kernel is designed on the dev splits (`plans/splits.json`: 25 dev scenarios per family).
- It is scored once per frozen version on the test splits (25 per family), on Causal Chambers and on the AB-08 benchmark.
- Every threshold is in `plans/q2_build_prereg.json` before the bundle that uses it runs.
