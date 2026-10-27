# Wave state (read this first; method: docs/WAVES.md)

Updated 2026-10-22 (wave B readback) by the agent. Tickets: INF-10, INF-06, TGT-18, CAP-07, BEN-13, BLD-06, EXT-03, CAP-11

## Current
- Waves A and B: **complete** (readbacks below). Wave C: planned, waits for Uzair's choice D-11.
- Waiting commit messages: `docs/commit_msgs/q2_l16_l5_cc-research.txt`, `waves_adopted_cc-research.txt`,
  `wave_a_cc-research.txt`, `wave_a_fork_cc-research.txt`, `wave_a_rerun2_cc-research.txt`, `wave_a_rerun3_cc-research.txt`,
  `wave_a_readback_cc-research.txt`, `wave_b_build_cc-research.txt`, `wave_b_readback_cc-research.txt` (check which are already in git).
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

## Readback of sheet B (second run, 22 Oct; return_B.zip)
All 20 runs finished; 15 of 17 must-shows pass. The two that fail (M_V4_ADOPT, M_V4_Q2) are results.
- v4 (BLD-18, analysis/results/v4/decision.json): **no knob clears the pre-registered rule; v3 stays; no held-out file
  read.** The G0 canary reproduces v3's dev number (0.8077 vs 0.8078).
  - Semantic dev precision at half coverage, paired gain over G0 (0.808):
    - A1 +0.040 [-0.011, 0.094], and ineligible: formula 0.866 vs 0.881;
    - R1 +0.030 [-0.020, 0.076], eligible;
    - A2 +0.015 [-0.031, 0.065].
  - False adjacencies per file fall 38-60 % (Q3 holds) and skeleton F1 rises (Q1 holds).
  - Q2 fails: under every new score the true DAG never scores as high as GES's output on a semantic file. The score still
    prefers a wrong graph, so the functional form is not the whole story (discrete children are still Gaussian; the
    search is CPDAG-based).
  - Dropping the turning phase is neutral (Q4).
  - Reading (not a rule outcome): every nonlinear score moved precision the predicted way, but 25 dev scenarios cannot
    separate +0.03 from zero.
- Held-out family 2 replicate 1: 500 files written and sealed (heldout_seal.json, manifest sha256 15957c3b...).
- BEN-13 S2 complete for MeanDifference (analysis/reports/ben13_s1_s2.md):
  - P1 fails: placement shares 0.07-0.14;
  - P2 holds: 4 of 4 cells;
  - P3 holds: 0.90 / 0.95;
  - P4 holds: STRING links 0.132 vs at most 0.113 (K562), 0.118 vs 0.099 (RPE1);
  - the FOR metric does not separate MeanDifference from random networks.
- First run of sheet B failed on two classes, fixed:
  - result folders without CONTRACT.json;
  - an undefined FOR formatted as a number.
- Data manifest re-taken (external/ incl. CausalBench and the sealed family).

## Readback of sheet A (fourth run, return_A.zip of 22 Oct)
Must-shows: 22 pass, 4 fail (M_X5_P1, M_X5_P3, M_F2_ER2, M_CC_BASE); the failures are results, not faults.
- Canary: hosts agree on claim structure: every number is read as produced.
- X4 (TGT-19): nonlinear-only missed links are kernel-detectable (+0.40 semantic, +0.52 formula over null).
- X5 (REP-07): AVICI far below GES: D1 stays the paper's line.
- Family 2, the one held-out read (TGT-18, CAP-07; analysis/results/q2_v3/family2_read.json; 500 files, 50 scenarios):
  precision at half coverage 0.795 [0.777, 0.811] at coverage 0.545; ECE 0.042 [0.030, 0.053]. ER-2 and ER-3 not met (the
  0.80 and 0.05 bars lie inside the intervals). Linear track 0.851 [0.826, 0.872], nonlinear 0.742 [0.726, 0.758].
  Pre-registered F1-F4 all hold: rule "transfer" (v3's reliability transfers; reported beside CausalArena, never pooled).
  The sheet's own table had no rule for "ER-2 fails, ECE passes"; the pre-registration's rules decide it.
- BEN-13 (analysis/results/ben13/summary.json): S0 shapes exact, S1 all four published rows reproduced. P1 refuted (edge
  placement carries 0.13 / 0.07 of MeanDifference's above-random Wasserstein: the score rests on specific pairs); P3 holds
  (0.90 / 0.95 of the total-effect ceiling); P2 holds in the 3 cells computed; P4 and rpe1 k5000 not computed: the false
  omission rate draws negatives outside the path closure, a dense network leaves none, and the cell also dropped its
  Wasserstein (111 cells; fix on sheet B). CORUM unreachable (certificate), reported missing as pre-registered.
- BLD-06 live on the fork: 30 / 30 completed vs 22 / 30 for unmodified main on the same rebuilt image (8 cycle-step
  KeyErrors; BND-08 had 6 / 30 on the old image); $4.84 vs $12.57. Graph quality is scored on sheet B (no credit).
- Base image rebuilt (M_CC_BASE fail): main control LIVE_06M ran as designed; it reproduces BND-08's cost ($12.57 vs $12.68).

## Third run of sheet A (20 Oct 22:34 UTC; stopped by Ctrl-C 21 Oct 17:25 UTC)
Tests and kit checks re-ran and passed. Then:
- B_CC started building the missing Causal-Copilot base image (FROM pytorch/pytorch:2.2.2-cuda11.8-cudnn8-runtime, one
  3.96 GB layer). About 2 minutes in (at about 1 GB of that layer) the Docker engine stopped answering: F2_READ, started
  at 22:39:02, failed on `500 Internal Server Error ... dockerDesktopLinuxEngine/_ping` before its container existed (the
  family-2 access log has no entry: nothing was read). The build never returned, the runner had no time limit, and every
  remaining run waited on it until Ctrl-C.
- FETCH_CB failed as designed: the two figshare files were not in Downloads yet (the manual step).
Fixed as a class (harness/wave.py; tests/test_wave_runner.py, 4 new tests): wall limit per run (default max(60 min,
6 x estimate)), optional stall limit (no new log output), the run's whole process tree and its named container are
stopped; statuses timeout / stalled / infra are not results and re-run on the next call; runs needing Docker wait while the
engine does not answer and the runner stops with exit 3 after 10 minutes; an exclusive run (B_CC) runs alone; Ctrl-C
stops jobs and containers and saves state; a heartbeat every 10 minutes. cc.ps1 names its container (CC_CONTAINER_NAME).
Why the engine stopped is not known from here (Docker Desktop's own logs would say): restart it before the next run.

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

## Wave B (built 22 Oct; sheet B)
Done in the build (no sheet needed): BLD-06 graph quality, pre-registered and scored on Uzair's machine through the bridge
(`analysis/results/fork/bld06_live_compare.json`): rule **drop_in**. Branch vs main on one image: completed 30 / 22;
delivered directed F1 +0.071 [0.035, 0.111]; final adjacency F1 0.596 vs 0.321 on the 22 tables both completed (main's
refinement lowers its own algorithm's adjacency F1 in 22 of 22 runs, the branch in 1 of 30, by 0.006); directed F1 +0.014
[-0.017, 0.039]. EXT-03 upstream draft; TA agenda; Q1 checkpoint outline; explanation ledger code; CAP-19.
On sheet B: v4 score grid on dev and the pre-registered decision; the sealed v4 held-out family; BEN-13 refill, P2 / P4,
report; data manifest. Details: `jobs/waves/B/plan.md`.

## Wave C (planned; Uzair's choice D-11)
Due dates: TA check-in Thu 29 Oct 10:45 (agenda ready: docs/meetings/2026-10-29_ta_checkin_agenda.md); Q1 checkpoint Mon 2 Nov
(outline ready, every placeholder filled: docs/q1/checkpoint_skeleton.md).
- C-a (default): the checkpoint document after the TA's format answer; no new runs needed.
- C-b: v4.1 with enough dev power. Family 2 replicate 0 (500 files, 50 scenarios; read once by frozen v3, never used to
  tune) becomes a second dev family; candidates A1, R1 and a discrete-aware child likelihood (Q2's finding), new hashed
  pre-registration; held-out: the sealed replicate 1 (same scenarios, new draws: the claim is about new draws). About
  6-8 core-hours on a sheet, no API spend.
- C-c: the fork branch live on S1 (Sachs and the four bundle-1 datasets, 16 arms, one run each) so DLV-04's live
  confirmation covers the whole suite. API spend at the 22 Oct per-run costs ($0.16 branch, $0.42 main): about $3 for the
  branch alone, about $10 with a main control on the same image (capped).
