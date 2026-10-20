# Wave state (read this first; method: docs/WAVES.md)

Updated 2026-10-20 (rerun 2 intake) by the agent. Tickets: INF-10, INF-06, TGT-18, BEN-13, REP-07

## Current
- Wave A: **second run returned 20 Oct; third run handed over** (`cc.ps1 wave A 2`; finished jobs are not repeated,
  tests and kit checks re-run because the kit changed). Sheet: 35 runs, 26 must-shows, 19 decisions.
- Waiting commit messages: `docs/commit_msgs/q2_l16_l5_cc-research.txt`, `waves_adopted_cc-research.txt`,
  `wave_a_cc-research.txt`, `wave_a_fork_cc-research.txt`, `wave_a_rerun2_cc-research.txt` (and the site chat's).
- Engine cache: `jobs/transfer/cache_engines_2026-10-19.tgz` (500 CausalArena dev entries); family-2 entries filled on the sheet (done).
- Defaults taken (20 Oct): D-1 plan yes; D-2 second family = our labelled generator (500 files), Causal Chambers wt
  report-only; D-3 BEN-13 names-only LLM arm no; D-4 public feed = dev digests; D-5 gaps page = new Act IV page (wave B);
  D-7 (rerun 2) main-control live arm only if the Causal-Copilot base image was rebuilt: on.

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

## Second run of sheet A (returned 20 Oct; intake by the decision table)
Ran ok: tests, kit checks, canary, X4, X5 (fetch, probe, 4 arms, score), family-2 fill (8 parts, 137 min).
- Canary: claim structure matches on this host (claims_sha256); full ledger hashes differ, as expected across CPU families.
  Decision "hosts agree": every number of the sheet is read as produced.
- X5 (REP-07, BEN-07): AVICI scm-v0 is far below GES on dev (semantic -0.281 [-0.330, -0.232], formula -0.146 [-0.193,
  -0.095]); its F1 is identical with original and shuffled columns (order effect 0.0, as its permutation-equivariant design
  implies). Decision: **D1 stays the paper's line; D2-score (a nonlinear score inside GES) is wave B2's design question.**
  Checked after the read (post hoc, not a result): AVICI is not reading edges backwards (on 60 semantic files, transposing
  its edges lowers F1 0.24 -> 0.15); it predicts about 13 edges where the truth has about 41, and even the best threshold
  in hindsight (about 0.1-0.2) gives F1 about 0.30, still far below GES's 0.53.
Failed, by class, fixed in the files now on disk:
- F2_READ refused: the freeze's code hash covers every .py file under kernel/, and three files were added there after the
  freeze (asym.py, asym_cond.py, linkfilt.py). No frozen file changed, none is missing, the core hash is equal. Deviation
  record written and hashed before the read (plans/v3_freeze_deviation_1.json): the guard checks frozen files one by one,
  the core, and the added files' sha256, and blocks importing the added files during the read. Nothing was read.
- FETCH_CB: figshare answers programmatic downloads with an empty body; the old fetcher took a 0-byte rpe1.h5ad as
  fetched. The fetcher now checks every file (never empty, format magic, published size and md5), runs on host Python, and
  imports the two expression files from a browser download in Downloads. Manual step: two browser downloads.
- STUB_03 / STUB_06: Docker had no `cc-research:a31aa7c-1` image. New run B_CC (`cc.ps1 ensureimage`) builds only what is
  missing and records whether the base image is still the one BND-08 ran on (M_CC_BASE); if not, LIVE_06M runs the same 30
  tables on unmodified main on the new image after the branch series (about $14, cap $25), so the comparison stays on one image.
- Runner: class A0 runs (tests, kit checks, image builds) now re-run when the kit's code identity changes.

## Manual steps before the sheet (Uzair)
1. Rerun 2: download the two CausalBench files in a browser into Downloads (figshare 35773219 K562, 10.7 GB; 35775606
   RPE1, 8.7 GB); the sheet imports and checks them. Commit the waiting messages when convenient.
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
