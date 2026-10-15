# AB-16 Wedge decision (DEC-05): what the audit established, and the choice made

Ticket: DEC-05 (and DEC-01). Prepared 2026-10-14; **decided 2026-10-14 after AB-06 finished**: option B, see "Decision"
below and `docs/decisions/2026-10-14_wedge_decision.md`. No model calls. Every number below is quoted
from a bundle report; the report is named next to it. Labels: **measured** (a script computed it on public data),
**desk** (read from documents), **open** (not yet measured).

## Where we are now

The audit program set out to learn where LLM-assisted causal discovery stands, what limits it, and whether anything is
worth building. Sixteen of its seventeen bundles are done; AB-17 follows this decision.

- **AB-06, the field audit**, finished on 14 Oct (`ab06_field_audit.md`). P9 and P10 are both supported.
- **AB-10, interviews**, run whenever a chance arises and did not gate this decision.

This pack was first written while AB-06 was running. Section 6 stated in advance what its outcome would change.

**The audit's answer, in five measured findings:**

1. **The public scoreboard reads the file layout.** Released files list columns in causal order. The authors' scoring
   orients undecided pairs from the earlier column to the later one, which adds about +0.21 F1 to FCI. PC's conflict rule
   is order-dependent, and Causal-Copilot's copy of the PC engine is wrong on 36% of perfect-information problems. A
   second benchmark (Bayesys) also releases in causal order, but its half-credit scoring is robust to it (≤ 0.03). So the
   leak pays only under index tie-breaking. (AB-01, AB-02, AB-03)
2. **Learned graphs barely help a decision.** Asked "if I set T, does Y move?", the best method beats "nothing moves" by
   +0.11 precision on CausalArena semantic. The true equivalence class would score 1.000 there. On Causal Chambers, the
   one benchmark with physical truth, GES and GIES do clear the empty graph by 0.07-0.10. So the gap is large on
   CausalArena and smaller on physical data. (AB-04)
3. **LLM agents take their directions from the names.** In Causal-Copilot, swapped names cost 0.167 directed F1 on gpt-4o
   and 0.094 on gpt-4o-mini. Without names it ends below plain PC in 8 of 10 and 9 of 10 families. Its bootstrap step
   discards about 80% of non-directed edges before any name is read. Asked directly with no data, gpt-4o orders 69% of
   true edges from names and follows swapped names against the data. (BND-08, AB-06 CC part, AB-07)
4. **Agent pipelines fail on their own output formats, loudly or silently.** Causal-Copilot crashed in 18 of 19 live
   entries into its cycle step, because it reads a JSON key its prompt never names. Vashishtha et al. lose 91% of their
   triplet votes to their own 300-token limit and carry on as if nothing happened. (AB-05)
5. **Declared structure plus abstention wins where it exists.** In incident root-cause analysis (PetShop), the declared
   call graph plus abstention reaches AC@3 0.93 at 0.92 coverage, against 0.21 for a learned graph. (AB-12)

**The theory holds as stated, with two restatements (AB-09):**

- F1 = S × a holds per file.
- The three-term error budget holds.
- Orientation-only knowledge has bounded harm: 51,392 checks, 0 violations.
- PC's conflict rules are order-dependent. This is Colombo & Maathuis 2014 plus our implementation-specific mechanism.
- The CPDAG decision-value ceiling holds; its coverage clause is restated.

## 1. Scorecard: the landmark criteria set on 12 Oct (`plans/audit_dag.json`)

| | Required | Evidence | Status |
|---|---|---|---|
| **L1** Layout and engine channels move published scores | ≥ 0.05 F1 or a top-10 rank on two public scoreboards | CausalArena: authors' rule +0.21 (FCI), conflict rule −0.07 (PC), engine copy 36% wrong (measured). Bayesys: causal order in 3 of 5 networks, scoring robust (≤ 0.03); causal-learn GES order effect −0.07 to −0.09 on PROPERTY (measured) | **Partly met.** The score moves on one scoreboard; the mechanism is shown on two. Scoped: "the leak pays under forced-choice index tie-breaking" |
| **L2** Field-level name reliance | ≥ 3 of ≥ 5 systems lose ≥ 0.10 F1, real → swapped | causaliq-knowledge 0.251, Causal-Copilot 0.167 (gpt-4o-mini 0.094), MATMCD 0.122, PyWhy-LLM 0.202 on 4 pairs, Vashishtha 0.020 (AB-06, measured); knowledge level (A3) +0.61 vs labels, −0.05 vs data | **Met** (P9 supported), scoped: the one system that resists is the one whose data decide the graph |
| **L3** Decision value near "nothing moves" while the ceiling is far above | on ≥ 2 benchmarks with interventions | CausalArena semantic and synthetic yes, formula narrowly; Causal Chambers no (GES +0.10, gap 0.084) (measured) | **Partly met**, stated as a CausalArena result with a physical-benchmark contrast (the kill criterion's narrowing) |
| **L4** A constructive system | never below data-only; bounded harm; DV precision ≥ +0.05 over the best reproduced method at stated coverage; calibration error ≤ 0.05; on ≥ 2 benchmarks | Ledger format and verifier (BLD-13, 9 tests); refinement v2 frozen (BLD-06), dev R1-R3 supported; tiers used only to orient: GES 0.528 → 0.546 F1, DV 0.753 → 0.784 (measured); bounded-harm theorem holds | **Not met.** The components exist; there is no engine yet |
| **L5** Theory explains the measurements | T1-T5 | All hold; T5's coverage clause restated (measured on 7,151 rows) | **Met** (novelty: T3 exact bound and T4 mechanism ours; T4 rule ordering is Colombo & Maathuis) |
| **C1** Practitioners name decisions where provenance and abstention matter | interviews | Public demand only: AI-SRE root-cause tools, marketing measurement, pharma real-world evidence (AB-14, desk) | **Indirect only** |
| **C2** A vertical where declared order plus abstention beats learned graphs | one vertical | PetShop RCA: 0.93 vs 0.21 AC@3 (measured; most of the gap is the topology) | **Met on one public dataset** |
| **C3** A regulatory or standards hook | desk map | 50 requirements in 21 texts mapped to ledger fields (FDA RWE, ICH M14 final, EU AI Act logging); W3C AI Computed Provenance CG as a venue (AB-13, desk) | **Met (desk)** |

**Kill criteria, written before the runs:**

| Criterion | Status |
|---|---|
| P9 refuted → L2 dropped as a headline | not triggered: P9 supported |
| P6 refuted on a second benchmark → L3 becomes CausalArena-specific | partly triggered (Causal Chambers); already folded into L3's wording above |
| P13 refuted → product angle shelved | not testable without interviews; the product angle rests on indirect evidence and says so |

## 2. What the audit does not support

- **"LLMs can replace the data."** Tiers from names alone score 0.448 F1, below a data-only method (AB-07 O4 refuted).
- **"The scoreboard ranks methods correctly."** Under controlled scoring, PC with maxP moves from 0.333 to 0.463 on
  semantic, the third-best published-method number, from a configuration change alone (AB-01).
- **"Agents add knowledge on top of a sound data step."** Causal-Copilot's data step loses its skeleton before the model
  reads anything, and its model review then rewrites edges it has no evidence for (BND-08).
- **"A causal-AI platform is a market."** The money is in specific decisions (root cause, budget allocation, regulatory
  evidence), where buyers pay for answers they can defend (AB-14).

## 3. Options

| | Option | Paper spine | Q2 build | What it rests on | Main risk |
|---|---|---|---|---|---|
| **A** | Measurement paper only | "Controlled scoring of causal discovery, from scoreboards to agents": L1 + L3 + L5, plus L2 if AB-06 supports it | none beyond notes to maintainers (EXT-01, EXT-03, EXT-05) | measured now | Novelty is partial: Colombo & Maathuis cover the conflict rule, and CARE covers single-system name collapse. The contribution is the conjunction and the controls |
| **B** | Measurement + a reliability-first system | "LLM-assisted causal discovery breaks properties a user needs; a claim ledger with tested invariants restores them at a bounded cost": A's findings as the motivation, L4 as the method | The ledger kernel in bundles B0-B5 (`approach_v1.md`), gated by the invariants. Then an audit adapter that checks other agents' claims | A's evidence + T3 bounded harm + AB-07 orient-only gain + AB-12 | L4 thresholds may not all be met on two benchmarks (Y2 in program v2: the data-only kernel may not reach GIES). Then the paper falls back to A with the ledger as a tool |
| **C** | Vertical first | An RCA audit product for AI-SRE agents | Build the PetShop pipeline into a product now | C2 on one public dataset; C1 indirect | Builds features before the reliability gate. Contradicts DEC-06's "reliability before features" |
| **D** | Big bet | Learned fusion (E4) | A pretrained network over data plus unreliable tier statements | nothing measured yet | Absorbs the quarter, with no fallback paper |

**Recommendation: B, with A as the floor it cannot fall below.**

- A is already written in the evidence. Choosing B costs nothing on the measurement side: every A result stays in, and
  section 6 says which headline each AB-06 outcome allows.
- B is the only option that turns the audit's findings into something a user can rely on. That is the standard Uzair set
  on 13 Oct: invariants, never below data-only, bounded harm, held-out calibration before any product surface.
- C is where B leads once B passes its gate. The audit adapter (B5) is the vertical product's core: it reads another
  agent's output, types every claim's source, and runs the verifier. PetShop is its first held-out test. Building it
  before the kernel passes would ship an auditor less reliable than what it audits.

**Venue class.** A methods venue with a benchmark contribution: CLeaR, TMLR, or a main-track ML venue. A datasets and
benchmarks track fits option A alone. Dates are checked in AB-17, not here.

## 4. The Q2 build under B, in one table (full design: `approach_v1.md`)

| Bundle | What | Gate that must pass before the next bundle builds on it |
|---|---|---|
| B0 | Engines and harness for the kernel: causal-learn PC with maxP (order-invariant per AB-01/AB-03), oracle and permutation checks in CI, the probe gate's malformed-output handling reused | I1 and I2 on 120 oracle DAGs × 6 orders; engine oracle check 720/720 |
| B1 | Data-only ledger (BLD-02): K0-K4 and K7 of program v2, invariants I1-I4 and I7 | I1-I4 and I7 on every dev file; not below plain PC (expectation rule) on the held-out split |
| B2 | Interventions as order evidence (BLD-03) | I6; DV-1 on Causal Chambers at least the data-only kernel's |
| B3 | Knowledge as tiers, orient-only (BLD-04) | I5; bounded harm measured with swapped names on held-out files; never below B1 |
| B4 | Confidence, calibration, abstention (BLD-05) | calibration error ≤ 0.05 within family on held-out scenarios; risk-coverage reported |
| B5 | Audit adapter: other agents' outputs → typed ledger claims → verifier report | runs on the AB-06 outputs and PetShop. Each flagged violation is traceable to a claim (e.g., knowledge that created a connection) |

## 5. What Uzair decides (DEC-05)

1. **Spine:** A, B (recommended), C or D.
2. **Venue class:** methods with a benchmark contribution (fits B), or datasets and benchmarks (fits A).
3. **Build start:** start B0-B1 now, in parallel with AB-06 tier A (recommended; no model calls), or after AB-06.
4. **AB-06 tier B:** run it (about $87 more, mostly Vashishtha's gpt-4o tie-breaks: the neutral contrast and its other five scenarios) or not (recommended: decide after tier A).
5. **Product:** the audit adapter (B5) is built only after B1-B4 pass their gates (recommended), or earlier.

## 6. What AB-06 can still change (fixed before its runs, `plans/ab06_prereg.json`)

| AB-06 outcome | Effect on the spine |
|---|---|
| P9 supported (≥ 3 of 5 systems lose ≥ 0.10) | L2 is a headline: name reliance is field-wide |
| P9 holds only through names-only systems; both hybrids lose < 0.10 | Reported as a design property: data-anchored hybrids resist swapped names, and B3's orient-only rule is the principled form of what they do |
| P9 refuted | L2 is dropped as a headline; Causal-Copilot stays a case study |
| P10 supported | "Never below data-only" becomes a measured failure of existing hybrids, not only a design rule |
| P10 refuted | The invariant stays a requirement; the paper does not claim others violate it |

Under every outcome option B keeps its method contribution. Only the motivation section changes.

## Decision (14 Oct)

AB-06 resolved section 6. P9 is supported through names-only systems and one hybrid (MATMCD); the other hybrid
(Vashishtha) resists. P10 is supported: MATMCD falls below its own data-only graph. So L2 is a headline in the form
section 6 pre-stated: name reliance is common, and where it comes from is a design property.

Uzair delegated the choice ("making the wedge decision and closing out everything else", 14 Oct). It is taken as
recommended, under his 13 Oct constraint (reliability before features):

1. **Spine:** B, with A as the floor.
2. **Venue class:** methods with a benchmark contribution.
3. **Build:** B0 and B1 now; AB-17 alongside.
4. **AB-06 tier B:** not run.
5. **Product:** the audit adapter is built after B1-B4 pass their gates.

DEC-01: program v2 is adopted as amended by approach v1. E1 is done in scoped form (AB-06); E2-E5 wait for B4.
Record: `docs/decisions/2026-10-14_wedge_decision.md`.

## Where we're going

- AB-17: the paper skeleton (`docs/paper/skeleton.md`) and the build pre-registration (`plans/q2_build_prereg.json`), both
  hashed before any build run.
- B0, then B1 (`approach_v1.md`).
