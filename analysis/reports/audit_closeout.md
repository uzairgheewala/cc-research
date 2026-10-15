# The audit chapter, closed (2026-10-14)

Ticket: AUD-32 (the audit program). Plan: `plans/audit_dag.json`, approved 12 Oct. Decisions: `docs/decisions/2026-10-14_wedge_decision.md`
and `2026-10-14_audit_closeout.md`. This report supersedes `audit_program_status.md` as the program's summary.

## Where we are now

All seventeen audit bundles are closed:

- sixteen done;
- AB-10 (interviews) carried forward, gating nothing.

The wedge is decided: spine B, measurement plus a reliability-first claim ledger, with measurement only as the floor. The
paper skeleton and the build's gate thresholds are hashed (AB-17).

Live spend for the whole program was $38.84, all through Uzair's key:

| Run | Cost |
|---|---|
| AB-07 knowledge elicitation | $2.08 |
| AB-05 probes | $3.79 |
| AB-06 Causal-Copilot second model | $0.86 |
| AB-06 grid | $32.11 |

The BND-11 names run alongside it cost $0.47.

## Bundles

| Bundle | Status | Result (report) |
|---|---|---|
| AB-01 Controlled scoreboard | done | Three layout channels on CausalArena; maxP removes PC's order effect; the authors' rule adds about +0.21 to FCI (`ab01_controlled_scoreboard.md`) |
| AB-02 Second scoreboard | done | Bayesys reproduced; it releases in causal order, but half-credit scoring is robust, so the leak needs index tie-breaking (`ab02_second_scoreboard.md`) |
| AB-03 Engine forensics | done | dodiscover's PC and gCastle's default fail the oracle test; causal-learn (PyPI), pgmpy and tigramite pass (`ab03_engine_forensics.md`) |
| AB-04 Decision value | done | Learned graphs capture 0-55% of the ceiling on CausalArena; physical data is the contrast (`ab04_decision_value.md`) |
| AB-05 Agent probes | done | All five systems run end to end; output-contract failures found in three (`ab05_probe_results.md`) |
| AB-06 Field audit | done | P9 supported: 3 of 5 systems lose ≥ 0.10 with swapped names, and the one that resists is the one whose data decide its graph. P10 supported: MATMCD falls below its own data. Causal-Copilot on a second model: same structure, smaller effect (`ab06_field_audit.md`, `ab06_cc_second_model.md`) |
| AB-07 Knowledge elicitation | done | Names give 69% correct order but follow swapped labels; tiers used only to orient help a little (`ab07_knowledge_elicitation.md`) |
| AB-08 Name-reliance benchmark | done | 2,500 files with a ρ dial (`ab08_benchmark_card.md`) |
| AB-09 Theory pack | done | T1-T5 hold; T5 restated (`ab09_theory_pack.md`) |
| AB-10 Interviews | carried forward | Kit ready; P13 and C1 still need them |
| AB-11 Teardown | done | No tool stores a per-direction source linked to evidence |
| AB-12 RCA probe | done | Declared topology plus abstention: 0.93 vs 0.21 AC@3 (`ab12_rca_probe.md`) |
| AB-13 Regulation map | done | 50 requirements mapped to ledger fields |
| AB-14 Market | done | Sell an audit of agents' causal claims; RCA first (`ab14_market.md`) |
| AB-15 Positioning | done | All five claims partly open; must-cite list |
| AB-16 Wedge decision | done | B, with A as the floor (`ab16_wedge_decision.md`) |
| AB-17 Paper skeleton and pre-registration | done | `docs/paper/skeleton.md`, `plans/q2_build_prereg.json`, `manifests/evidence/paper_prereg_2026-10-14.sha256` |

Landmark criteria at close:

| Criterion | Status |
|---|---|
| L1 | partly met (scoped) |
| L2 | met (scoped) |
| L3 | partly met (scoped) |
| L4 | to build |
| L5 | met |
| C1 | indirect |
| C2 | met on one dataset |
| C3 | desk |

## What carries into the build

- **Guarantees G1-G8 and gates B0-B5:**
  - each guarantee answers a failure measured here (`approach_v1.md`);
  - each gate is fixed in `plans/q2_build_prereg.json`.
- **Reusable pieces:**
  - refinement v2, the frozen data part (held-out 22/22);
  - the ledger format and verifier;
  - the engine oracle checks;
  - the probe gate, which now handles caps, rate limits, quota stops, EIO, resumes and cut-short logs;
  - the tier elicitation runner;
  - the decision-value scorer.
- **Lessons for the supplier contract (G7):**
  - Causal-Copilot's unnamed JSON key crashes the run;
  - Vashishtha's truncation silently loses its votes;
  - gpt-4o fences its JSON;
  - guidance's clock crash.

  A contract states which normalisations it accepts and counts every failure.

## Left open, by choice

| Item | Status |
|---|---|
| AB-10 interviews | P13 and C1 stay open |
| AB-06 tier B (about $87) | Not needed for any verdict |
| BND-12's CARE control and LLM/fused Sachs numbers | Moved to B3 |
| Notes to maintainers (EXT-01, EXT-03, EXT-06) | Drafted in `docs/drafts/bug_reports/`; Uzair's to send |
| causal-learn GES order effect on Bayesys PROPERTY (−0.07 to −0.09) | Reported, not explained |
| The site's 390 px overflow check | Not yet in CI |
| Q1-plan bundles BND-02, BND-03, BND-06 | External blockers only: CausalArena appendix B unreadable, AVICI checkpoint host unreachable, live-only claims |

## Where we're going

B0, then B1, under `plans/q2_build_prereg.json`. B1 is the first bundle with a held-out gate: the data-only kernel must not
fall more than 0.01 below plain PC with maxP on the test splits.
