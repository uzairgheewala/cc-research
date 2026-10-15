# Decision record: the wedge (DEC-05) and the program (DEC-01), 2026-10-14

Tickets: DEC-05 (done), DEC-01 (done), AUD-47 (AB-17, unblocked). Decision pack: `analysis/reports/ab16_wedge_decision.md`.
Build design: `analysis/reports/approach_v1.md`.

Uzair, in chat on 2026-10-14, after AB-06's tier A finished:

> "please go ahead with the scoring and filling page 6 and making the wedge decision and closing out everything else to
> end our auditing chapter here"

He had stated the governing constraint on 13 Oct (`2026-10-13_atlas_v2_approved.md`): auditing is the more valuable
product, but reliability comes before anything is built on top. The pack's recommendation follows that constraint, so it
is taken as written, with AB-06's results in hand.

| Decision (pack section 5) | Taken | Why |
|---|---|---|
| 1. Paper spine | **B: measurement + a reliability-first claim ledger.** A (measurement only) is the floor | AB-06 supplied the last motivation: P9 and P10 supported, as section 6 pre-stated. L4 is the method contribution, built in gates |
| 2. Venue class | Methods with a benchmark contribution | B has both; dates are checked in AB-17 |
| 3. Build start | B0 and B1 now (no model calls), AB-17 alongside | Both inputs exist: approach v1 is written, and refinement v2 passed its held-out test (BND-11) |
| 4. AB-06 tier B | **Not run** | No verdict needs it. It costs about $87, mostly Vashishtha's gpt-4o tie-breaks. It can still be run later, unchanged |
| 5. Product | The audit adapter (B5) is built only after B1-B4 pass their gates | DEC-06: reliability before features |

**DEC-01 (program v2 and the extensions E1-E5).** Program v2 is adopted as amended by approach v1.

- E1, the field-wide audit, is done in scoped form: AB-06, five systems, CausalArena semantic.
- E2-E5 stay out of scope until B4 passes.

**What the decision binds:**

- Every B bundle's gate thresholds are hashed before its runs (`plans/q2_build_prereg.json`, AB-17).
- The reliability guarantees G1-G8 are the acceptance criteria. A bundle that misses its gate is fixed before anything
  builds on it.
- The measurement results (L1 scoped, L2, L3 scoped, L5, C2) stay in the paper whatever the build yields.
