# Wave B plan (22 Oct 2026)

Tickets: BLD-18, BLD-17, BEN-13, BLD-06, DLV-04, EXT-03, TGT-18, TGT-19, CAP-19, CRS-01, BND-13, INF-10

Uzair's go: 22 Oct, with defaults D-8 (v4 score candidates on dev, fresh held-out sealed), D-9 (parallel chats folded in)
and D-10 (no API spend on sheet B).

## Frontier and what was built

| # | Bundle | Built and checked in the sandbox | On sheet B |
|---|---|---|---|
| B-1 | Explanation ledger (TGT-18/19) and determinism (CAP-19) | `analysis/explanation_ledger.py`: 22 typed segments whose sizes sum to the anatomy totals in both families; CAP-19 recorded from sheet A's canary | ELEDGER (seconds) |
| B-2 | v4 score candidates (BLD-18) | `v4/scores.py` (gauss re-implementation equal to ges 1.1.0 on the first file; additive hinge + discrete indicators; random Fourier features), `v4/dev.py` (fill, engines, evaluate, decide), `v4/heldout_gen.py`; pre-registration `plans/v4_prereg.json` hashed in `manifests/evidence/v4_prereg_2026-10-22.sha256` before any ledger-level dev number; tests `tests/test_v4_scores.py`; smoke: engines on 24 files per knob, evaluate on 12 files per family (plumbing only) | V4_FILL, V4_ENG_* (4 knobs x 4 parts), V4_EVAL, V4_DECIDE, V4_HELDOUT (written and sealed, not read) |
| B-3 | BEN-13 fix (dense networks), P1-P4 scored by code, report generator | `analysis/ben13/evaluate.py`, `run.py`, `report.py`; tests updated and `tests/test_ben13_summary.py` | CB_REFILL_K/R (only the failed cells), CB_MERGE2, CB_REPORT |
| B-4 | BLD-06 graph quality; EXT-03 report | `plans/bld06_live_prereg.json` (hashed), `analysis/bld06_live_compare.py`, run on Uzair's machine through the bridge (JSON states only): rule **drop_in**; `docs/drafts/bug_reports/causal_copilot_cycle_step_keyerror.md` | nothing (done) |
| B-5 | Deliverables | `docs/meetings/2026-10-29_ta_checkin_agenda.md`, `docs/q1/checkpoint_skeleton.md` | nothing |
| - | Runner | `between` bar op (and its test) | DATA_MAN (hash external/ data) |

Behaviour-changing bundles on the sheet: B-2 (a full knob grid, every candidate has its own cell and G1 isolates the search
change) and B-3 (a reporting fix). Within the 2-4 limit.

## Deviation after the pre-registration hash

`v4/dev.py` gained the `fill` command (v3 engine records for this machine's BLAS kernel before the knob runs, so parallel
parts never race on one cache entry). It changes no metric, knob or rule. The pre-registration file is unchanged; the code
hash in `manifests/evidence/v4_prereg_2026-10-22.sha256` therefore no longer matches `v4/dev.py`, and this note is the record.

## Budget

- Agent: the build above (this turn).
- Operator: 491 core-minutes in all. The v4 engine grid is 16 parts of 17-32 minutes (about 5.4 core-hours; about 90 minutes
  of wall time at 4 workers within the 4.3 GB Docker budget, mem 0.8 GB per part); BEN-13 refill 30 + 25 minutes; evaluate
  about 40 minutes; data manifest about 20 minutes. Suggested: `cc.ps1 wave B 4`. No API spend.
- Round trips saved: the v4 grid, the BEN-13 refill and the data manifest on one sheet, instead of three.

## What the sheet decides

| Must-show | Bar | Gate |
|---|---|---|
| M_T_HOST, M_T_KERNEL, M_T_BENCH | tests pass | yes |
| M_TRACE, M_SITE | 0 errors | |
| M_V4_G0 | G0 through the v4 plumbing equals v3's dev precision 0.8078 within 0.005 (canary) | |
| M_V4_ADOPT | a knob clears the pre-registered rule | |
| M_V4_Q1..Q5 | the pre-registered predictions | |
| M_V4_SEAL | 500 held-out files written and sealed | |
| M_CB_S1, M_CB_P2, M_CB_P4 | reproduction still true; P2 and P4 hold | |
| M_ELEDGER | 22 segments | |

Decisions: `jobs/waves/B/sheet.json` "decisions" (adopt and freeze -> one held-out read on sheet C; none -> v3 stays and
wave C turns to the next lever; plumbing canary fails -> nothing read).
