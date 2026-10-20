# Wave state (read this first; method: docs/WAVES.md)

Updated 2026-10-20 by the agent. Tickets: INF-10

## Current
- Wave A: **built; sheet handed over 20 Oct, not yet run.** Kit: applied on Uzair's machine 20 Oct (checks there: verify, trace, ci_check, site build all 0 errors).
  Run: `cc.ps1 wave A 2`, which runs `jobs/waves/A/sheet.json` (33 runs, 24 must-shows, 15 decisions) and returns
  `jobs/waves/A/return_A.zip`.
- Waiting commit messages: `docs/commit_msgs/q2_l16_l5_cc-research.txt`, `waves_adopted_cc-research.txt`, `wave_a_cc-research.txt`.
- Engine cache: `jobs/transfer/cache_engines_2026-10-19.tgz` (500 CausalArena dev entries); family-2 entries are filled on the sheet.
- Defaults taken (20 Oct): D-1 plan yes; D-2 second family = our labelled generator (500 files), Causal Chambers wt
  report-only; D-3 BEN-13 names-only LLM arm no; D-4 public feed = dev digests; D-5 gaps page = new Act IV page (wave B).

## Wave A: what was built, what the sheet decides
| # | Bundle | Built and checked in the sandbox | Sheet |
|---|---|---|---|
| A1 | Wave runner (INF-10) | harness/wave.py, tests (demo sheet: failing canary, gated skip, resume, refusal on changed code) | image builds, tests on host and image, canary, kit checks |
| A2 | Fork branches (INF-06, BLD-06, EXT-03) | patches from upstream's own a31aa7c blobs, branch identity in the harness, make_branches.ps1, capped live runner | stubs of both branches; live BLD-06 (30 runs, about $14, cap $25), gated on the stubs |
| A3 | Explanation round (TGT-18/19) | **X1-X3 done** (analysis/reports/q2_explain_dev.md): linear-score misspecification explains both semantic gaps; rule says D2-search, global check says the lever is the score | X4 (KCI) |
| A4 | Family 2 (TGT-18, CAP-07) | amendment hashed, smoke on 10 files | fill (about 5.5 core-hours), the one read |
| A5 | X5 (REP-07, BEN-07) | adapter, pre-registration, X5 image pins | fetch, runs, score |
| A6 | BEN-13 S0-S2 | streamed preprocessing bit-identical to causalbench (synthetic), methods, controls, pre-registration | download 19.4 GB, preprocess, 2 x 293 cells, merge |
| A7 | Site S23 (TEAM-09) | done: home, status and theses now come up for re-reading | kit checks only |

## First run of sheet A (started 20 Oct 16:49 UTC on Uzair's machine; fixes shipped the same day)
Host: Windows 11, 16 cores, Docker memory 6.2 GB (budget 4.3), no AVX-512 (BLAS runs HASWELL). Ran ok: image builds,
T_KERNEL, CHECKS (layout problem below), B2GEN (b2 files reproduce: sha 2723f443... as in the sandbox), X4 (all 8 parts),
X4_LEDGER; F2_FILL was running. Failed, by class, all fixed in the files now on disk:
- T_HOST: the runner test wrote its fixture in text mode (CRLF on Windows) and hashed LF bytes: fixture now bytes.
- T_BENCH: compared with a digest frozen in the sandbox; NumPy's float32 SIMD kernels round differently on AVX2 vs
  AVX-512. The test now runs causalbench's own preprocess_dataset on the same machine (scanpy added to the bench image).
- FETCH_X5: avici.backbone needs deepdiff to unpickle the checkpoint (psutil also added); inference now checked end to
  end on a random tiny checkpoint in a clean venv.
- CANARY: ledger hashes differ between this host and the sandbox for all three files, and also between the sandbox's
  SKYLAKEX and HASWELL runs: the full ledger hash (which covers test statistics) is not portable across CPUs, so CAP-11's
  "same hash on any machine once the BLAS kernel is pinned" holds only per CPU family (wave B: record on CAP-11). The
  canary now judges claim structure (claims_sha256), which matches under HASWELL in the sandbox.
- CHECKS: ran inside the container with the folder named "research" and without Causal-Copilot: now the kernel_tree
  profile mounts cc-research and Causal-Copilot side by side (.env masked by an empty file).
- Gating: tests' done checks now require "ok": true, so a failed test is never taken as done on resume.
Effect on the rerun: STUB_03/STUB_06, LIVE_06, BEN-13 and X5 were skipped behind T_HOST, T_BENCH and FETCH_X5; they run
on the rerun. Finished jobs (X4, B2GEN, fill parts) are not repeated.

## Manual steps before the sheet (Uzair)
1. Extract the kit over cc-research; commit the three waiting messages when convenient.
2. Fork: done 20 Oct (docs/FORK.md): main clone in place, both branch folders verified. Push the two branches and the tag
   when convenient (one git command in docs/FORK.md); the sheet does not need them on GitHub.
3. Python 3.8+ on Windows for the runner (`py -3 --version`).
4. Docker Desktop memory: at least 6 GB if possible (Settings, Resources).
5. The three unsent prod digest drafts: send or move to relay_out/discarded/.

## Wave B parallel workstreams (started 20 Oct while sheet A reruns; rules: project doc claude/wave-b-parallel-2026-10-20.md)
| Workstream | Tickets | Patch | Sheet B fragment |
|---|---|---|---|
| B1 explanation ledger (X1-X4 typed map; cross-host determinism) | TGT-18, TGT-19, CAP-19 | p26 | if any |
| B2 D2 designs: pretrained engine beside GES / nonlinear score inside GES, pre-registered pick | BLD-17, BLD-18 | p27 | jobs/waves/B/fragments/d2.json |
| B3 deliverables: TA agenda (29 Oct), Q1 checkpoint skeleton (2 Nov), PA | CRS-01, BND-13, CRS-08 | p28 | none |
| B4 reach and measurement: more scenarios, second RCA set, CausalArena real data | BEN-14, EVL-08 | p29 | jobs/waves/B/fragments/reach.json |
| Site v3 S24-S28 (S29 after return_A) | TEAM-10..12 | s24-s28 | none |
Rule while sheet A runs: no edits to files listed in jobs/waves/A/identity.sha256; patches applied after return_A.zip is packed.
X4 (back from sheet A, dev): KCI detects the nonlinear-only missed links 45.5% (semantic) / 63.2% (formula) against null
6.0% / 11.2%: P6 holds (+0.40 / +0.52).

## Wave B (after return_A.zip)
Intake by the decision table; explanation ledger complete (X4, X5); D1 / D2 settled; family-2 numbers beside CausalArena;
BEN-13 share table or protocol diagnosis; BLD-06 live scored against BND-08; site S24 gaps page and S25 prose sync (home,
status, theses on the re-read list); TA check-in agenda (Thu 29 Oct, 10:45 am; agenda by 28 Oct); Q1 checkpoint package
BND-13 (due 2 Nov); the logic for the chosen direction's first bundle; sheet B.

## Wave C
The chosen direction (v4 engine, or the improved Causal-Copilot) and its sheet; Q1 checkpoint submission.
