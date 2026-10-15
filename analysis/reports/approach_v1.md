# Approach v1: the reliability-first claim ledger (design, pending DEC-05)

Tickets: DEC-05 (the decision this design serves), BLD-02..05, BLD-07, BLD-14, CAP-10, BLD-06. Written 2026-10-14.
It builds on program v2 §4 (state, stages K0-K7, invariants I1-I7) and changes it only where the audit taught something.
Nothing here is built until Uzair decides DEC-05; it is the option-B build in `ab16_wedge_decision.md`.

## Where we are now

The audit measured how existing systems fail. This design turns each failure into a guarantee, a mechanism that enforces
it, and a test that fails if the guarantee breaks. The pieces that exist already:

- the ledger record format and verifier V1-V8 (BLD-13);
- the frozen refinement rule v2 (BLD-06);
- the tier elicitation runner and its measured accuracy (AB-07);
- the orient-only rule and its bounded-harm proof (AB-09 T3);
- the decision-value scorer (AB-04);
- the engine oracle and permutation checks (AB-03);
- the probe gate's handling of model calls (AB-05/06).

The engine that produces claims does not exist yet.

## 1. The contract: each guarantee answers a failure the audit measured

| | Guarantee | Failure it answers (measured) | Mechanism | Test that fails if it breaks |
|---|---|---|---|---|
| G1 | Column order changes nothing (I1) | Authors' rule +0.21 F1; PC conflict rule −0.07; vendored PC wrong on 36% of oracle problems (AB-01, AB-03) | Order-invariant engine (causal-learn PC with maxP); no evidence type for column position; open pairs stay open; the scoreboard view uses the expectation rule only | Permutation test: 6 orders × every dev file, claims identical after renaming |
| G2 | Same inputs give the same ledger (I2) | One unreproduced FCI difference under threading (AB-03) | Seeds recorded; single-threaded engines in the kernel; canonical hash over variables, evidence, knowledge and claims | Rerun hash equality (V6) |
| G3 | Never below the data-only output (I3 and the floor) | Causal-Copilot below plain PC without names in 8 of 10 / 9 of 10 families; its final graph below its own algorithm's adjacency F1 in 49 of 51 completed runs (BND-08, AB-06) | With no knowledge admitted, D+K output = D output exactly; knowledge cannot delete or add a connection (G5); any regime's difference from D traces to named records | Regime-diff test on every dev and held-out file; held-out DV-1 and F1 ≥ the data-only kernel's |
| G4 | No claim without evidence; an independent checker re-derives every claim (I4, K7) | Agents emit edges with no record of why (AB-11: no tool stores a per-direction source linked to evidence) | `Claim` cites evidence ids; K7 re-derives from the ledger alone | Verifier V1-V8 on every run; mutation tests (delete one evidence record → the claim is rejected) |
| G5 | Knowledge orders connected pairs and nothing else (I5); bounded harm | Causal-Copilot's review adds edges; MATMCD's LLM answers can forbid both directions and delete a connection; swapped names cost 0.094-0.167 F1 (BND-08, AB-05, AB-06) | Knowledge enters only as tiers, applied only to pairs the data left undirected; T3 bounds the harm by the directions it decided | Swapped-name arm on held-out files: the skeleton is identical to D, the loss is ≤ the T3 bound, and it is reported |
| G6 | An intervention outranks a stated name (I6) | (design rule; AB-04 Chambers shows interventions carry most of the usable signal) | Fixed priority intervention > data (strong) > knowledge > data (weak); conflicts recorded | Constructed conflicts on Chambers and CausalArena D+I files |
| G7 | A malformed or truncated model reply can neither crash a run nor silently degrade it (I7, widened) | Causal-Copilot crashed in 18 of 19 cycle-step entries (unnamed JSON key); Vashishtha lost 91% of answers to truncation with only a printed warning (AB-05) | Every supplier reply is schema-validated; `finish_reason=length` counts as a failure; one retry, with a larger limit for truncation, then abstain; the failure and abstention rates are ledger fields, never only log lines | Fault-injection tests: a missing key, truncation, invalid JSON, a 429 storm. The run completes, the counts appear in the ledger, and the claims equal the D output on the affected pairs |
| G8 | Confidence is calibrated and abstention is chosen on held-out data | Learned graphs commit to most pairs at precision near "nothing moves" (AB-04) | Replicate-agreement frequency mapped to probability by a map fitted on dev scenarios and frozen; the selective view at a user-stated cost ratio c/g | Within-family held-out calibration error ≤ 0.05; risk-coverage curve; claimed precision at the stated threshold |

G7 widens program v2's I7, which said only "cannot crash". The Vashishtha finding shows that silent degradation is the
worse failure, because nothing downstream notices it.

## 2. State and stages: what changes from program v2 §4

The typed state (`OrderEvidence`, `OrderLedger`, `PartialOrder`, `AdjacencyEvidence`, `Claim`, `Regime`) and stages
K0-K7 stand. The audit changes six things:

1. **K1 data-pattern source.** causal-learn PC (PyPI) with the maxP conflict rule. It is order-invariant in AB-01
   (released vs shuffled within 0.001) and the best data-only PC on CausalArena (0.463 semantic). causal-learn (PyPI) PC is
   exact on 720/720 oracle problems in AB-03; B0 re-runs that check on the maxP wrapper itself. FCI enters only in a declared latent regime (E5, out of scope).
2. **K1 knowledge source.** Tiers by consensus over three phrasings, which adds 3-9 points of correct order (AB-07).
   Per-phrasing tiers are kept in the ledger; phrasings that disagree on a pair leave it unordered. The snapshot, prompt
   hash and the names shown are recorded.
3. **K2.** No index tie-break anywhere. The scoreboard view (K6) orients open pairs at random per file seed and says so.
   The ledger keeps them open.
4. **K5.** The stability signal is replicate agreement: resampled reruns (AB-04 risk-coverage carries real signal,
   0.80-0.92 precision in the top 10-20%). It is calibrated by an isotonic map fitted on the dev split and frozen before
   the held-out split is read.
5. **K6 decision view.** DV-1 answers ("if I set T, does Y move?") with abstention at the user's stated cost ratio c/g,
   recorded as an input. The usefulness threshold from AB-04 (act only if precision > c/(g+c)) is computed per query.
6. **Ledger v0.2 fields (BLD-14, from AB-11 and AB-13).** Plan and deviations, assumptions, lineage, reviews, and the
   question and context. These make the ledger usable as an audit record.

## 3. Binding times

| Choice | Fixed when | Recorded where | Changes only by |
|---|---|---|---|
| Engines, versions, alpha, conflict rule | B0, before any kernel run | engine manifest (sha256) | a new manifest and a re-run of B0's oracle checks |
| Evidence priority rule (K2) | design (this document) | `ledger/DESIGN.md` | a decision record |
| Knowledge prompts, phrasings, consensus rule | before any held-out knowledge call | pre-registration manifest | a new manifest, held-out results discarded |
| Calibration map | end of dev (B4) | frozen file + sha256 | refit on dev only, with the held-out split untouched |
| Gate thresholds (every bundle below) | before the bundle's runs | `plans/<bundle>_prereg.json` + manifest | never after results are seen |
| Admitted sources (regime) | per run | ledger `Regime` | per run, by the caller |
| User cost ratio c/g | per query | ledger `question` (BLD-14) | per query |
| Model snapshot | per call | ledger knowledge record | per call; one snapshot per comparison |

## 4. Failure modes named in advance (in addition to program v2's Y1-Y11)

| # | Failure | Guard |
|---|---|---|
| Z1 | An engine defect returns through a dependency upgrade (the gCastle/dodiscover class, AB-03) | Pinned versions; the oracle and permutation checks run in CI on every change |
| Z2 | The kernel is order-invariant but a view is not (a sort, a dict order, a tie-break in plotting or export) | Views are covered by the same permutation test as claims |
| Z3 | The phrasing consensus hides real disagreement and turns it into confident order | Per-phrasing tiers recorded; any disagreement leaves the pair unordered; the disagreement rate is reported |
| Z4 | Silent degradation in a supplier (truncation, empty answer, default value) | G7: `finish_reason`, schema and emptiness are checked per reply; the failure rate is a ledger field with a stop threshold |
| Z5 | Calibration fitted on one family is quoted for another | Guarantee stated within family; cross-family numbers labelled as measured, not guaranteed (Y4) |
| Z6 | The audit adapter (B5) gets another agent's provenance wrong | Adapters written from the agent's code (MATMCD's constraint matrix, Vashishtha's `pc_only` vs `llm_order`, Causal-Copilot's stage lineage); an `unknown` source is allowed and counted, never guessed |
| Z7 | Held-out knowledge runs are cut short by caps or rate limits | Tiers cost 3 short calls per scenario (AB-07: 900 calls for 100 scenarios × 3 arms × 3 phrasings); the probe gate's cap and rate-limit rules are reused |
| Z8 | The semantic family's graphs were written with model help, so knowledge looks better than it is (Y1) | Formula family, Causal Chambers (physical truth), and the B2 ρ-dial benchmark (AB-08) reported beside semantic |
| Z9 | The data-only kernel is below published GIES, which makes the "never below data-only" floor look weak (Y2) | The floor is relative to the kernel's own D output by construction; absolute numbers are reported against the controlled scoreboard (AB-01), not the published one |

## 5. Bundles (each verifiable in one run, with a must-show list)

| Bundle | Scope | Must show | Gate (fixed before its runs) | Cost |
|---|---|---|---|---|
| **B0** Engines and guards | causal-learn PC maxP wrapper with deterministic settings; the oracle and permutation check as a CI test; the supplier contract (G7) as a library shared with `harness/probe_llm.py` and refinement v2's parse rule | Oracle 720/720 and 120/120 order-invariant; fault-injection suite green; CI log | All pass | none |
| **B1** Data-only ledger (BLD-02) | K0-K4, K7; ledger v0.2 fields (BLD-14); views K6 (scoreboard, claim list) | I1-I4 and I7 on every CausalArena dev file (semantic, formula); ledger hashes; scores under the expectation rule beside the controlled scoreboard; verifier report | All invariants pass on every dev file; on held-out, F1 and DV-1 ≥ plain PC maxP (expectation rule), paired by file | none |
| **B2** Interventions (BLD-03) | Order evidence from interventional rows; I6 conflicts | DV-1 on CausalArena D+I and Causal Chambers; conflicts recorded and resolved by priority | I6 on constructed conflicts; DV-1 ≥ B1 on the same files | none |
| **B3** Knowledge as tiers (BLD-04) | Tier supplier (3 phrasings, consensus), orient-only (I5), all three name arms | Real/neutral/swapped on held-out files: skeleton identical to D, harm ≤ T3 bound, neutral = D exactly | I3 and I5 on every file; never below B1; swapped-arm loss within the T3 bound in 100% of files | a few hundred short calls (Uzair runs) |
| **B4** Confidence and abstention (BLD-05) | Resampled reruns, the frozen calibration map, the selective view at c/g | Reliability diagram per family; risk-coverage; claimed vs realised precision at c/g = 1, 2, 4 | Within-family held-out calibration error ≤ 0.05 | none (B3's knowledge replies reused) |
| **B5** Audit adapter (the product core, after B1-B4 pass) | Read another agent's output (Causal-Copilot stages, MATMCD, Vashishtha, PyWhy-LLM, causaliq; RCA tools on PetShop) into typed ledger claims; run the verifier; report violations by class | On AB-06's outputs: every violation traced to a claim and a source (e.g., "knowledge created a connection", "direction from column position"); PetShop held-out | Adapter unit tests from each agent's code; zero `unknown` sources where the agent records provenance | none |

The order is strict: a bundle builds only on a predecessor that passed its gate. If B1's held-out floor fails, the design
returns to the kernel before anything else is built (program v2 gate G2's fallback).

## 6. Evaluation protocol

- **Benchmarks:**
  - CausalArena semantic and formula (dev for design, test held out by scenario number, `plans/splits.json`);
  - CausalArena synthetic;
  - Causal Chambers light tunnel (physical truth, real interventions);
  - Sachs (weak truth, reported as such);
  - AB-08's ρ-dial benchmark (dose-response of name reliance);
  - PetShop (RCA, B5).
- **Controls:**
  - columns always shuffled;
  - three name arms where names are read;
  - every scoring rule stated: the expectation rule for scoreboard F1, committed claims for DV-1.
- **Metrics:**
  - directed F1 and its factors S, c, q, a;
  - DV-1 precision and coverage against "nothing moves" and the CPDAG ceiling;
  - calibration error and risk-coverage;
  - AC@k for RCA;
  - cost per run;
  - invariant pass rates.
- **Held-out discipline:**
  - thresholds, prompts and the calibration map are hashed before held-out files are read;
  - one snapshot per comparison;
  - every deviation is recorded in the ledger's plan-and-deviations field.

## 7. Out of scope for this build

These are program v2's extensions:

- E2: a public agent track;
- E3: real experiments in the remote lab;
- E4: learned fusion;
- E5: hidden common causes, time series, 100+ variables.

They become candidates only after B4 passes. The product surface (a hosted audit service, dashboards, integrations) waits
for B5's held-out result.

## Where we're going

On DEC-05 = B:

1. B0, then B1, in that order, with no model calls.
2. AB-17 (paper skeleton and pre-registration) alongside B1.
3. B2 and B3 next; B3 needs a small live run from Uzair, planned when B1 passes.
