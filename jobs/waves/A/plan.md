# Wave A: plan, run sheet and decision table (20 Oct 2026)

Tickets: INF-10, INF-06, BLD-06, EXT-03, TGT-18, TGT-19, CAP-07, REP-07, BEN-07, BEN-13, TEAM-09

## Frontier and what was built

| # | Bundle | Built in the sandbox (free) | On the sheet |
|---|---|---|---|
| A1 | Wave runner (INF-10) | `harness/wave.py` (preflight, canaries, gates, resume, parts within a memory budget, verdict, pack), `tests/test_wave_runner.py`, `analysis/wave_canary.py`, kernel image `docker/Dockerfile.kernel` | image builds, tests on the host and in the image, canary |
| A2 | Fork branches (INF-06, BLD-06, EXT-03) | `jobs/fork/*.patch` and branch descriptions, branch identity in `harness/cc_common.py` and `run_traced.py`, `jobs/fork/make_branches.ps1`, `harness/live_capped.py`, `tests/test_fork_patches.py` | stub runs of both branches; live BLD-06 validation (gated, capped) |
| A3 | Explanation round (TGT-18, TGT-19) | X1-X3 **run here** (`analysis/reports/q2_explain_dev.md`) | X4 kernel test (KCI), merged into the explanation ledger |
| A4 | Second held-out family (TGT-18, CAP-07) | `analysis/q2_family2.py`, amendment `plans/v3_prereg_amendment_1_family2.json`, smoke on 10 files | engine fill (heavy), the one logged read |
| A5 | X5 pretrained engine (REP-07, BEN-07) | `analysis/x5_pretrained.py`, `plans/x5_prereg.json`, X5 image | checkpoint fetch, probe, four runs, scoring |
| A6 | BEN-13 S0-S2 | streamed preprocessing (bit-identical to causalbench on synthetic files, peak about 0.5 GB), methods, controls, `plans/ben13_prereg.json`, bench image | download (19.4 GB), preprocessing, reproduction and control cells, merge |
| A7 | Site S23 (TEAM-09) | Q2 bindings, evidence-aware re-read, superseded reads, guarded literals, `tests/test_site_s23.py` | none |

Behaviour-changing bundles: A2 (the fork's two branches) and nothing else. Every other bundle is an instrument or a
read. A2's ablation is the branch against main (BND-08's unmodified runs on the same 30 tables).

## Budget

- **Agent:** all seven bundles were built in this wave, and X1-X3 ran here.
- **Operator, heavy:** about 1,320 core-minutes. With 2 workers inside a memory budget of 70% of Docker's memory, that is about 3-5 hours of wall time. The two largest pieces are the CausalBench download (about 1 hour, depending on bandwidth) and the family-2 engine fill (about 5.5 core-hours in 8 parts).
- **Operator, live:** about 7 hours of wall time, sequential, and about $14 with a hard cap of $25. It starts only after both branch stubs pass, and it runs alongside the heavy jobs.
- **Round trips saved:** this is one sheet for seven bundles. Bundle by bundle, it would take at least six.

## Decision table

The decision table is in `sheet.json`, under `decisions`. The verdict marks any outcome that no rule matches. In short:

- The canary does not match: numbers from this machine are read as host-specific.
- X5 P1 holds: wave B designs a pretrained engine inside the ledger. If P1 fails, D1 stays the line.
- Family 2 transfers: ER-2 and ER-3 are reported per family. If ECE is above 0.05, calibration is stated per family only.
- BEN-13 reproduces the published counts and rows: wave B writes the shortcut-share table. If it does not: diagnosis first, and no claim.
- Live BLD-06 passes (at least 25 of 30 runs complete): wave B scores it against BND-08 for the Q1 checkpoint.

## Rerun 2 (20 Oct, after the second run's intake)

Fixed by class: the family-2 guard (plans/v3_freeze_deviation_1.json), the CausalBench fetcher (checks, browser import,
host Python), the missing Causal-Copilot image (run B_CC, `cc.ps1 ensureimage`). New: must-shows M_CC_BASE (base image
equals BND-08's) and M_CB_FETCH; run LIVE_06M (main control on the same image, only when M_CC_BASE fails; about $14,
cap $25; decision D-7, default on). Class A0 runs re-run because the kit changed; finished heavy runs are kept.
