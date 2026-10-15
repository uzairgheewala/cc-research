# Q2 build: external requirements, deliverable sets, ladders and the DAG (design v1, draft for approval)

Tickets: BLD-02..05, BLD-14, CAP-03..05, CAP-07..09, CAP-11, TGT-10..12, TGT-06; proposed TGT-18..20, BLD-15.
Written 2026-10-14 after Uzair set the scope: "all of the landmarks up to and including Causal Chambers" are the external
requirements; work out the deliverables that constitute each, the ladders they decompose into, the shared DAG, and the
paths from here to each end goal. Inputs, all fixed: the landmark record (`docs/decisions/2026-10-14_q2_landmarks.md`),
the build pre-registration (`plans/q2_build_prereg.json`, gates B0.1-B5.2), approach v1, `ledger/DESIGN.md`, the
controlled scoreboard (`analysis/results/rescore_v2/`) and AB-04's decision-value tables.

Nothing here changes a hashed gate or threshold. Ladders refine the inside of a bundle; the gate stays the bundle's exit.
Status: draft. On approval the proposed tickets are issued and `plans/q2_dag.json` is hashed.

## Where we are now

Seven external requirements, two of which (floors, Chambers) are already partly answered by measurement. Baselines that
every requirement is scored against, on the controlled scoreboard (columns shuffled, expectation rule):

| Family | PC maxP (the floor's comparator) | GES (BIC) | GIES D+I | Empty graph DV-1 | CPDAG ceiling F1 |
|---|---|---|---|---|---|
| semantic | 0.463 | 0.528 | 0.539 | 0.647 | 0.957 |
| formula | 0.359 | 0.470 | 0.515 | 0.708 | 0.971 |
| Chambers (DV-1 precision) | 0.887 | 0.916 | 0.885 | 0.813 | 1.000 at 0.99 coverage |

Two facts from this table shape the design. (i) The gap PC maxP -> GES is 0.065 on semantic and **0.111 on formula**:
a kernel whose only data-pattern engine is PC cannot reach ER-4a's "above GES". The kernel therefore carries GES as a
second engine from B1, with a pre-registered combination rule. (ii) GES completed on 225 of 250 semantic and 178 of 250
formula files in the earlier run; the kernel must handle an engine that fails or times out as a typed event, not a crash
(G7 widened to engines).

## 1. External requirements

Each row: the statement, its threshold (from the landmark record), the scorer, the data it is judged on, the tickets it
serves, the measured starting point, and the bundle at whose exit it is known. "Held-out" means the test splits of
`plans/splits.json`, scored once per frozen kernel version; a requirement is met when the lower end of the paired 95%
bootstrap interval clears the threshold.

| ER | Statement | Threshold | Scorer | Judged on | Serves | Start | Known at |
|---|---|---|---|---|---|---|---|
| **ER-F** Floors | The data-only ledger is never below plain PC maxP | F1 and DV-1 paired mean diff >= -0.01, both families (B1.2; refuted at <= -0.05) | F1 expectation rule; DV-1 precision | held-out semantic, formula | BLD-02, CAP-05, CAP-06, CAP-11, TGT-09 | no kernel; comparator measured | B1 |
| **ER-1** Provenance and invariance | Every direction names its source; column order changes nothing; names orient only pairs the data left open; wrong names do bounded harm | I1 zero change; neutral arm == D byte-identical; skeleton identical across arms; swapped loss within the T3 bound in 100% of files (B3.1, B3.2); V1-V8 accepted | verifier; permutation test; arm diff | dev (invariants), held-out (arms) | BLD-04, BLD-14, CAP-04, CAP-05, CAP-09, TGT-10, TGT-11 | schema + verifier exist; no engine | B3 |
| **ER-2** Decision value | Claims the ledger commits to are right four times in five at half coverage | DV-1 precision > 0.80 at coverage >= 0.50, both families (clears c/g = 4) | DV-1 selective view | held-out semantic, formula | BLD-05, CAP-08, CAP-15 (part); proposed TGT-18 | GES 0.753 at 0.95 coverage; top 10-20% of replicate-agreed claims 0.80-0.92 | B4 |
| **ER-3** Calibration | Stated confidence matches hit rate | ECE <= 0.05 within family; realised >= claimed - 0.03 at c/g = 1, 2, 4 (B4.1, B4.2) | reliability diagram; selective view | held-out, map frozen on dev | BLD-05, CAP-07, TGT-12 | raw replicate agreement carries signal (AB-04), uncalibrated | B4 |
| **ER-4a** One accuracy landmark | Route A: data-only F1 above GES on one family under controls. Route B: B3's tiers lift F1 > 0.03 over B1 | either route, held-out | F1 expectation rule | held-out semantic, formula | CAP-01, CAP-02, CAP-04, TGT-01/03 (part), TGT-07 (part); proposed TGT-19 | GES 0.528 / 0.470; orient-only lift measured +0.018 over GES (AB-07) | B1 (route A) / B3 (route B) |
| **ER-4b** RCA | Declared topology plus abstention, through the ledger, holds the AB-12 result while the ledger fills topology gaps | AC@3 >= 0.90 at stated coverage on the PetShop held-out split | AC@k at coverage | PetShop test split | CAP-09; proposed BLD-15, TGT-20 | 0.90 measured outside the ledger (AB-12) | B5 |
| **ER-C** Physical truth | The kernel holds up where the truth is physical and the interventions real | DV-1 precision within 0.03 of GES (0.916); agreement with Welch tests on real interventional rows reported against the true DAG's 0.928 | DV-1; agreement | Causal Chambers light tunnel | BLD-03, CAP-03, TGT-06 | GES 0.916, PC maxP 0.887 | B2 |

ER-C is report-only in the landmark record. It is kept as a requirement here because it is the one data set where
"CausalArena-specific" cannot be said, and because B2's intervention evidence is built on it.

## 2. Deliverables (shared catalogue)

A deliverable is a file or module with a check that says whether it exists in the state claimed. IDs are stable; the
matrix in section 3 shows which requirements each serves. "Exists" marks work already done in the audit chapter.

**Layer 0: foundations (B0)**

| ID | Deliverable | Check | Exists |
|---|---|---|---|
| D0.1 | Engine manifest and wrappers: causal-learn PC (maxP), GES (BIC), GIES (targets); pinned versions, wheel sha256, alpha, single-threaded, seeds recorded; failure and timeout as typed events | manifest file; each wrapper returns a typed result or a typed failure on the fault suite | wrappers partly (AB-01, AB-03) |
| D0.2 | Oracle and permutation CI test on the wrappers: 120 DAGs x 6 orders | 720/720 exact, 120/120 invariant (B0.1) | test exists for the engines, not the wrappers |
| D0.3 | Supplier contract library: schema validation, `finish_reason`, retry rule, counts; fault-injection suite of 7 cases; shared by `harness/probe_llm.py`, refinement v2 and the B3 tier supplier | all 7 cases complete with the counts in the ledger (B0.2) | pieces in probe_llm and refinement v2 |
| D0.4 | Scorer v2 as one package: F1 (expectation rule) with S/c/q/a, DV-1 precision and coverage, risk-coverage, ECE, AC@k; paired bootstrap interval; CONTRACT.json | reproduces AB-01 and AB-04 numbers on their files to 0.001 | pieces across analysis/ |
| D0.5 | Baseline table on the **test splits**: PC maxP, GES, GIES D+I, empty graph, CPDAG ceiling, F1 and DV-1, per file | one file; paired with every later kernel score | all-public-files version exists |

**Layer 1: the kernel (B1)**

| ID | Deliverable | Check | Exists |
|---|---|---|---|
| D1.1 | Variable identity by content hash; canonical ledger hash (I2) | V6 passes; rerun equality | schema |
| D1.2 | K1 data-pattern evidence: every CI test (PC) and every score delta (GES) written as an evidence record | V2 closure; evidence count equals engine log | - |
| D1.3 | K2-K4 resolution: skeleton, v-structures, Meek R1-R4 with `licensed_by`; open pairs stay open; **two-engine combination rule** (section 4) | reproduces PC maxP's CPDAG exactly when GES evidence is withheld | - |
| D1.4 | Ledger v0.2 fields (BLD-14): plan and deviations, assumptions, lineage, reviews, question; verifier updated | V1 on v0.2; verifier report format | v0.1 |
| D1.5 | K6 views: scoreboard export (expectation rule, per-file seed), claim list; views under the same permutation test (Z2) | 6 orders, identical views after renaming | - |
| D1.6 | K7 re-derivation from the ledger alone | every claim re-derived; mutation test rejects a ledger missing one evidence record (B1.3) | - |
| D1.7 | B1 report: I1-I4, I7 on 100% of dev files; held-out score once | B1.1, B1.2, B1.3 | - |

**Layer 2: interventions and physical truth (B2)**

| ID | Deliverable | Check | Exists |
|---|---|---|---|
| D2.1 | `intervention_shift` evidence from D+I files (CausalArena targets) and Chambers; i-essential orientation; priority I6 | V4; constructed conflicts resolved for the intervention 100% (B2.1) | replay sampler (BEN-09) |
| D2.2 | Constructed conflict suite (intervention vs knowledge, intervention vs weak data) | all cases recorded and resolved by priority | - |
| D2.3 | Chambers adapter: light tunnel, 20 variables, 11 targets, real interventional rows; Welch agreement check | DV-1 and agreement computed for the kernel, GES, PC maxP, true DAG, empty graph | dv_chambers_sachs.py |
| D2.4 | B2 report | B2.2; ER-C numbers | - |

**Layer 3: knowledge as tiers (B3)**

| ID | Deliverable | Check | Exists |
|---|---|---|---|
| D3.1 | Tier supplier: 3 phrasings, consensus, per-phrasing tiers recorded, disagreement leaves a pair unordered; built on D0.3 | fault suite green; prompt sha256 in every record | AB-07 runner |
| D3.2 | Orient-only application (I5) with the per-file T3 harm bound | skeleton identical to D in every arm; bound computed per file | T3 proof (AB-09) |
| D3.3 | Name-arm harness for the ledger (real / neutral / swapped, columns shuffled) | neutral == D byte-identical | harness arms exist |
| D3.4 | B3 pre-registration: prompts, phrasings, consensus rule, thresholds hashed before the live run | manifest | - |
| D3.5 | Live run (Uzair; a few hundred short calls) and B3 report | B3.1-B3.3; ER-1; route B of ER-4a | - |

**Layer 4: confidence (B4)**

| ID | Deliverable | Check | Exists |
|---|---|---|---|
| D4.1 | K5 resampled reruns: replicate-agreement frequency per claim, seeds recorded | frequencies reproduce under rerun | AB-04 risk-coverage code |
| D4.2 | Calibration map (isotonic) fitted on dev, cross-validated by scenario, frozen and hashed | hash before any held-out read | - |
| D4.3 | Selective view at a stated c/g; usefulness threshold per query recorded in `question` | realised vs claimed table | threshold formula (AB-04) |
| D4.4 | B4 report: reliability diagrams per family, risk-coverage, claimed vs realised at c/g = 1, 2, 4 | B4.1, B4.2; ER-2, ER-3 | - |

**Layer 5: the adapter (B5)**

| ID | Deliverable | Check | Exists |
|---|---|---|---|
| D5.1 | Adapters: Causal-Copilot stages, MATMCD, Vashishtha, PyWhy-LLM, causaliq outputs -> typed claims with `direction_source` (or `unknown`, counted); violation classes | B5.1 on the AB-06 outputs | lineage tools (BLD-01) |
| D5.2 | PetShop adapter: declared topology as knowledge statements; RCA view ranking causes with abstention; topology-gap experiment (declared edges withheld) | AC@3 at coverage; reproduces AB-12 through the ledger | AB-12 scripts |
| D5.3 | B5 report | B5.2; ER-4b | - |

**Cross-cutting**

| ID | Deliverable | Check |
|---|---|---|
| DX.1 | CI: `tests/run_tests.py` + D0.2 + verifier mutation tests on every change; `tools/ci_check.py` | green before any held-out read |
| DX.2 | Amendment files for every deviation, hashed, as in AB-06 | manifest per amendment |
| DX.3 | Registry keys and site pages 8-10 for each bundle's numbers | build 0 errors |

## 3. Requirement x deliverable matrix

| | D0.1 | D0.2 | D0.3 | D0.4 | D0.5 | D1.1 | D1.2 | D1.3 | D1.4 | D1.5 | D1.6 | D2.1 | D2.3 | D3.1 | D3.2 | D3.3 | D4.1 | D4.2 | D4.3 | D5.1 | D5.2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ER-F | x | x | | x | x | x | x | x | | x | x | | | | | | | | | | |
| ER-1 | x | x | x | | | x | x | x | x | x | x | | | x | x | x | | | | | |
| ER-2 | | | | x | x | | | x | | | | x | | | | | x | x | x | | |
| ER-3 | | | | x | x | | | | | | | | | | | | x | x | x | | |
| ER-4a | x | | x | x | x | | x | x | | | | | | x | x | x | | | | | |
| ER-4b | | | | x | | x | | | x | | x | | | | x | | | | x | x | x |
| ER-C | x | | | x | | | x | x | | | | x | x | | | | | | | | |

Shared by every requirement: D0.4 (the scorer) and D0.5 (the baselines). Shared by six of seven: D1.3 (resolution).
Those three are the DAG's trunk; a defect there is a defect in every result.

## 4. The one open design choice: the two-engine combination rule (D1.3)

Reason: ER-4a route A. Candidates, to be chosen and pre-registered before B1's held-out read, and measured on dev only:

| Rule | Skeleton | Direction | Expected effect | Risk |
|---|---|---|---|---|
| C1 agreement | PC skeleton, GES skeleton: keep the intersection as `x-y`, the rest as `none` | commit only where both engines agree; else open | precision up, recall down; DV-1 up, F1 possibly down | fails ER-4a, helps ER-2 |
| C2 union with source | union of skeletons, each edge tagged by the engine(s) that found it | commit where both agree; where one engine is silent the other's compelled direction applies | recall up; F1 likely between PC and GES or above | F1 may still trail GES on formula |
| C3 GES-led, PC-audited | GES skeleton and directions; PC's CI evidence recorded; a direction PC's compelled evidence contradicts is set open | about GES's F1 (0.528 / 0.470) with openness where the engines disagree | nearest to the landmark; the floor against PC maxP is easy | "the kernel is GES with a ledger" (reviewer objection; answered by G1-G8, not by F1) |

The floor (ER-F) is against PC maxP whichever rule is chosen, as hashed. The pre-registration of the rule, with its dev
numbers, is deliverable D1.3's binding time. Prediction to fix then: C3 or C2 clears GES on semantic by >= 0.01 on dev;
formula is the harder family.

## 5. Ladders

A rung is a state with a test. A rung is passed on dev; the top rung is the requirement on held-out, read once.

**ER-F (floors)**
- R0 D0.1-D0.2: wrappers pass the oracle and permutation checks.
- R1 D1.2-D1.3: with GES withheld, the ledger's claim set equals PC maxP's CPDAG on every dev file (F1 identical to 0.000). This rung makes ER-F true by construction for the PC-only regime.
- R2 D1.1, D1.6: V1-V8 on every dev ledger; mutation tests reject.
- R3 D1.5: views pass the 6-order permutation test.
- R4 combination rule chosen (section 4) and its dev numbers recorded; floor still holds on dev.
- R5 held-out, once: B1.2.

**ER-1 (provenance and invariance)**
- R0 D0.3: fault suite green; `finish_reason=length` counted as failure.
- R1 D3.1: tier supplier records per-phrasing tiers, prompt hashes, what was shown.
- R2 D3.2: orient-only on dev; skeleton identical to D in 100% of files (I5).
- R3 D3.3: neutral arm byte-identical to D.
- R4 T3 bound per file; swapped loss within the bound on dev.
- R5 D3.4: prompts and thresholds hashed.
- R6 D3.5: live held-out run (Uzair); B3.1-B3.2.

**ER-2 (decision value)**
- R0 D0.4-D0.5: DV-1 with paired intervals; empty-graph and ceiling rows on the test splits.
- R1 B1 claims on dev: DV-1 precision >= empty graph (else the kernel over-commits; return to D1.3).
- R2 D4.1: replicate agreement per claim.
- R3 D4.3 on dev: precision of the top-50%-coverage selective view; prediction fixed before the read: > 0.78 on dev.
- R4 D2.1: interventions admitted (D+I files) raise DV-1 on dev (B2.2 on dev).
- R5 held-out, once.

**ER-3 (calibration)**
- R0 D0.4: ECE and reliability diagram.
- R1 raw replicate-agreement reliability on dev (the uncalibrated baseline, reported).
- R2 D4.2: isotonic map, cross-validated by scenario on dev; ECE on dev folds <= 0.05.
- R3 map frozen and hashed.
- R4 held-out, once: B4.1, B4.2.

**ER-4a (one accuracy landmark)**
- Route A: ER-F R0-R4, then held-out F1 above GES on one family (B1 read).
- Route B: ER-1 R1-R6, then real-arm F1 - B1 F1 > 0.03 on one family (B3 read). Prediction: route A is the likelier; route B's measured analogue is +0.018.

**ER-4b (RCA)**
- R0 D5.2: PetShop data and declared topology ingested as knowledge statements (`required_edge`, `tier`).
- R1 RCA view: rank candidate causes over declared topology with abstention; reproduce AB-12's 0.90 through the ledger on the dev split.
- R2 topology-gap experiment on dev: withhold 10%, 25% of declared edges; the ledger's data evidence fills gaps; AC@3 at coverage recorded against the declared-only and learned-only rows.
- R3 held-out split, once: AC@3 >= 0.90.

**ER-C (Chambers)**
- R0 D2.3: adapter; baselines (GES 0.916, PC maxP 0.887, true DAG 0.928 agreement) reproduced.
- R1 B1 kernel on Chambers: DV-1 precision recorded.
- R2 D2.1: interventions admitted; DV-1 >= B1 (B2.2).
- R3 agreement with Welch tests on the real interventional rows; report against the true DAG's 0.928.

## 6. The DAG

Bundles keep the pre-registered identities and gates; each is now a set of deliverables with the ladders' rungs as its
internal order. Formal file: `plans/q2_dag.json` (draft), checked with `tracker/plan_check.py`.

| Bundle | Deliverables | Rungs reached | Closes | Needs Uzair | Known at exit |
|---|---|---|---|---|---|
| B0 Engines, guards, scorer | D0.1-D0.5, DX.1 | ER-F R0; ER-1 R0; ER-2 R0; ER-3 R0 | CAP-05, CAP-11 | approve this plan | - |
| B1 Data-only ledger | D1.1-D1.7; the combination rule | ER-F R1-R5; ER-2 R1; ER-4a route A | BLD-02, BLD-14, CAP-09, TGT-10 | - | ER-F; ER-4a (A) |
| B2 Interventions and Chambers | D2.1-D2.4 | ER-C R0-R3; ER-2 R4 | BLD-03, CAP-03, TGT-06 | - | ER-C |
| B3 Knowledge as tiers | D3.1-D3.5 | ER-1 R1-R6; ER-4a route B | BLD-04, CAP-04, TGT-11 | live run | ER-1; ER-4a (B) |
| B4 Confidence and abstention | D4.1-D4.4 | ER-2 R2-R5; ER-3 R1-R4 | BLD-05, CAP-07, CAP-08, TGT-12, TGT-18 | - | ER-2, ER-3 |
| B5 Adapter and RCA | D5.1-D5.3 | ER-4b R0-R3 | BLD-15, TGT-20 | - | ER-4b |

Dependencies: B0 -> B1 -> {B2, B3} -> B4 -> B5 (as hashed). B2 and B3 are independent of each other. B4 needs B3's
replies only to reuse them (no new calls) and can start its dev work on B1's output as soon as B1 passes; its held-out
read waits for B3. B5 needs B1-B4 passed.

Milestones (what is known, not dates to chase): M1 floors known (B1 exit); M2 physical-truth row known (B2 exit);
M3 provenance known (B3 exit); M4 the paper's constraints all known (B4 exit); M5 the wedge's constraint known (B5 exit).

## 7. Paths from here to each end goal

Critical path for the paper: B0 -> B1 -> B4 (ER-F, ER-2, ER-3; ER-4a by route A at B1). B3 joins for ER-1 and sits on
the path only through its live run. Everything on this path is free of model calls except B3.

| End goal | Path | Free | Needs Uzair |
|---|---|---|---|
| ER-F | B0 -> B1 | all | - |
| ER-4a | B0 -> B1 (route A); else B1 -> B3 (route B) | route A | route B's live run |
| ER-C | B0 -> B1 -> B2 | all | - |
| ER-1 | B0 -> B1 -> B3 | dev rungs | the held-out live run |
| ER-2, ER-3 | B0 -> B1 -> (B2) -> B4 | all | - |
| ER-4b | B0 -> B1 -> B2/B3 -> B4 -> B5 | all | - |

Parallelism available once B1 passes: B2, B3's dev rungs, and B4's dev rungs can proceed at the same time; they share
only D1.3's output and D0.4's scorer.

## 8. Failure modes named in advance (beyond approach v1's Z1-Z9)

| # | Failure | Guard |
|---|---|---|
| Q1 | The combination rule is tuned on dev until it beats GES, then fails held-out | one rule, pre-registered with its dev numbers before the held-out read; a second rule means a new frozen version and an amendment |
| Q2 | GES fails or times out on a file and the kernel silently falls back to PC, changing the regime | engine failure is a typed event in the run report; the file is scored in both engines' rows or excluded in both, never one |
| Q3 | The scorer disagrees with the audit-chapter scorers by rounding | D0.4 reproduces AB-01 and AB-04 to 0.001 before use |
| Q4 | Held-out splits are read early by a baseline computation | baselines on the test splits are allowed (they are not tuned); kernel scores on them are logged with a counter that must read 1 per frozen version |
| Q5 | Chambers has one 1,000-row file; a 0.03 margin is inside its interval | ER-C is report-only; the interval is printed with the number |
| Q6 | PetShop's declared topology is complete, so the gap experiment is artificial | report the gap curve as a sensitivity, not a claim; AC@3 at 0% withheld is the landmark |
| Q7 | B4's map is fitted within family and quoted across families (Z5) | per-family maps; cross-family numbers labelled measured |

## Where we're going

On approval: issue TGT-18, TGT-19, TGT-20, BLD-15; hash `plans/q2_dag.json` with this document; patch the tracker;
start B0 with D0.4 (the scorer) and D0.1 (the engine manifest), because every later number passes through them.
