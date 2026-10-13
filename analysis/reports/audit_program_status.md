# Audit program status: what the free bundles found, and what it does to the wedge

Ticket: AUD-32 (program). Written 2026-10-13, after the first pass through `plans/audit_dag.json`. No model calls and nothing
spent. Every number here is from a bundle report named in the table.

## Where we are now

| Bundle | Status | Headline (report) |
|---|---|---|
| AB-01 Controlled scoreboard | done | maxP removes PC's order effect in all three families (P2 supported). Under the controlled setting PC scores 0.463 on semantic, against a published 0.333. The authors' rule adds about +0.21 to FCI everywhere. GIES with targets is unaffected by layout (`ab01_controlled_scoreboard.md`) |
| AB-02 Second scoreboard | **waits on you** | gCastle alarm ids are not in causal order (tau of id vs depth between −0.22 and 0.02), and PC was not reproduced, so there is no claim. Bayesys needs a browser download (`ab02_second_scoreboard.md`) |
| AB-03 Engine forensics | done | dodiscover's PC fails the perfect-oracle test and can return a cyclic graph. pgmpy and tigramite are correct. Three bug-report drafts are written (`ab03_engine_forensics.md`) |
| AB-04 Decision value | done | On CausalArena, learned graphs capture 0-55% of the ceiling's decision value; on synthetic, PC and GES are worth less than doing nothing. On Causal Chambers, GES lifts precision by 0.10, within 0.08 of the ceiling (`ab04_decision_value.md`) |
| AB-05 Agent probes | **waits on you** | All four agents run end to end offline. Live caps total $3.55, plus $0.03 for Causal-Copilot on gpt-4o-mini (`ab05_probe_prep.md`) |
| AB-06 Field audit | to do | Proposed budget about $57, or about $29 with PyWhy-LLM on gpt-4o-mini; recompute after AB-05 |
| AB-07 Knowledge elicitation | **waits on you** | 900 requests are pre-registered (about $3.1). The scorer reproduces 0.714 with oracle tiers |
| AB-08 Name-reliance benchmark | done | 2,500 files with a rho dial; reference curves as predicted (`ab08_benchmark_card.md`) |
| AB-09 Theory pack | done | T1-T4 hold. T5 was restated: the CPDAG abstains on some pairs whose answer is constant (`ab09_theory_pack.md`) |
| AB-10 Interviews | **waits on you** | The kit is ready. First ask course staff about an IRB determination |
| AB-11 Teardown | done | No tool stores an evidence-linked source for each direction. In 7 of 9 tools a required edge creates a connection the data did not support (`AB11_vendor_claims.md`) |
| AB-12 RCA probe | done | PetShop: declared topology with abstention scores AC@3 0.93 at 92% coverage, against 0.21 for a learned PC graph (P15 supported) (`ab12_rca_probe.md`) |
| AB-13 Regulation map | done | 50 requirements mapped. Five ledger gaps (BLD-14). Venue: the W3C AI Computed Provenance Community Group (`AB13_regulation_map.md`) |
| AB-14 Market | to do | Waits on AB-10 |
| AB-15 Positioning | done | All five claims are partly open. Mandatory citations: Colombo & Maathuis 2014, CARE, Li & Russo 2026, GENESIS (`AB15_positioning.md`) |
| AB-16 / AB-17 | to do | Gate on 14 Nov; paper skeleton by 21 Nov |

## The landmark criteria after this pass

| | Criterion | Before (12 Oct) | Now |
|---|---|---|---|
| L1 | Layout and engine channels move a published score by ≥ 0.05 or a rank, on two scoreboards | met on one board | **Stronger on one board, second board pending.** All three CausalArena families now show it (PC with maxP against the published PC row, released order, expectation rule: +0.13 semantic, +0.14 formula, +0.13 synthetic; FCI gains about +0.21 from the authors' rule). Engine defects now cover three libraries (Causal-Copilot's copy, gCastle default PC, dodiscover PC). The second scoreboard waits on Bayesys. Novelty is narrowed by Colombo & Maathuis: the signed bias of the default conflict rule, the authors' index rule and the engine defects are ours; the order dependence itself is not |
| L2 | ≥ 3 of ≥ 5 LLM systems lose ≥ 0.10 with swapped names, with a dose-response | 1 system | **Instruments ready, no new data.** The rho-dial benchmark (AB-08) and the four agent adapters (AB-05) are built. CARE already shows a single-system collapse, so only the field-level, layout-controlled, dose-response version is new |
| L3 | Most methods within 0.05 of "nothing moves", ceiling ≥ 0.15 above the best, on ≥ 2 benchmarks | met on CausalArena | **Holds on CausalArena (three families), not on Causal Chambers.** P6 is supported on 4 of 5 benchmarks and inconclusive on Chambers. P7 is supported on semantic and synthetic, inconclusive on formula (0.149), Chambers (0.084) and Sachs. Restate L3 as "on LLM-drafted and generator benchmarks", with physical data as the contrast. The decision-value framing itself (the empty-graph baseline plus the CPDAG ceiling on a public leaderboard) was not found in prior work |
| L4 | A constructive system beating reproduced methods on decision value with calibration | format only | **Format v0.1 tested against 10 real tools; v0.2 gaps listed (BLD-14).** AB-12 shows the constructive pattern working in one vertical: declared knowledge with abstention beats a learned graph by 0.72 AC@3. That is the same mechanism L4 claims, in RCA rather than CausalArena |
| L5 | Theory explaining the measurements | identity checked | **Done, as restated.** Five statements were checked on 7,151 rows. The bounded-harm bound is ours; the conflict-rule order dependence is Colombo & Maathuis's |
| C1 | Demand evidence | none | Interview kit ready; waits on the course-staff question |
| C2 | One vertical where order knowledge plus abstention beats learned graphs | none | **Supported in RCA (PetShop, P15).** Almost all of the gap comes from topology rather than abstention |
| C3 | A regulatory hook | desk notes | **Mapped.** The traceability and record-keeping requirements (FDA, EMA, AI Act Art. 12) match ledger fields. The real gaps are pre-specification, assumptions, lineage and review. SR 26-2 (Apr 2026) puts generative AI out of its scope |

## What the wedge looks like now

1. **The paper spine is measurement plus decision value.** The strongest, least-scooped results are the controlled scoreboard (L1 with three channels), decision value with its ceiling (L3, CausalArena-scoped, with a physical contrast) and the engine forensics. Each has a one-command reproduction.
2. **The constructive leg should be scoped to what AB-12 shows.** In domains where the structure is declared (service topology), an evidence-typed claim set that keeps knowledge separate from data, and abstains, beats learned graphs by a wide margin. A CausalArena version must clear GIES's 0.11-0.15 lift on decision value, not F1.
3. **Name reliance (L2) needs the live AB-05, AB-06 and AB-07 runs** before it can be weighed. It is the cheapest way to make the paper field-level.
4. **The commercial angle has one positive vertical signal (RCA)**, pricing per investigation ($3-8.45, from AB-11 pricing signals) and a standards venue. Demand is untested until the interviews.

## Where we're going

These need you:

1. The live runs: AB-05 (about $3.6 in total) and AB-07 (about $3.1).
2. The Bayesys download for AB-02.
3. The course-staff question for AB-10.

Then I run AB-06 with the budget recomputed from AB-05, score AB-07 (O1-O5), finish AB-02 and prepare the AB-16 wedge memo for 14 Nov.
