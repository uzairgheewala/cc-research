# Quarter 1 checkpoint (due Fri 6 Nov 2026): title, abstract, introduction, and the public code link

Tickets: DLV-05, CRS-02, DLV-07, BND-13, DLV-01. Re-cut 27 Oct by the agent to the course page
(dsc-capstone.org/2026-27/assignments/projects/q1, read 27 Oct). Status: **outline**.

What the course asks for:
- **Report, graded by the mentor:** the title, abstract and introduction sections, written in the course's LaTeX template
  on Overleaf. The introduction is an introductory paragraph, a literature review and discussion of prior work, and a
  description of the relevant data.
- **Code, graded by the TA:** a link to a public GitHub repository with the code so far (DLV-07, `tools/export_q1.py`).

Rules for filling this outline:
- Every number names its source file.
- A placeholder `[[name: source]]` is filled from that source only, never typed by hand.
- The results sections of the earlier outline moved unchanged to the final-report outline at the end; the checkpoint quotes
  at most the one result the introduction needs.

## Title (pick one; about 12 words)
- "Causal-Copilot, Step by Step: Where an LLM Agent's Causal Graph Comes From"
- "Links Kept, Arrows Unsettled: A Controlled Replication of Causal-Copilot's Review Step"

## Abstract (150-200 words; five sentences)
1. **Problem.** LLM agents now run causal discovery end to end, but which part of their answer comes from the data, the
   variable names or their own rules is not measured.
2. **What we do.** Run Causal-Copilot (commit a31aa7c, GPT-4o) unmodified on tables with known graphs. Hold the numbers fixed
   while the names change (real, neutral, swapped), and record every intermediate graph and model call.
3. **Finding.** Its review step removes most links the algorithm found and crashes on [[8 of 30: bld06_live_compare.json
   completed.main]] runs.
4. **Improvement.** A replacement review keeps them: adjacency F1 [[0.596 vs 0.321: same, means.*.final_adj_f1]]; it finishes
   every run at [[$4.84 vs $12.57: same, usd]]. Directed accuracy does not improve measurably
   ([[+0.014, -0.017 to +0.038: same, paired_branch_minus_main.L2_dir]]).
5. **Next.** When to commit to an arrow, and when to leave it open.

## 1. Introduction (about one page)
1. **Why causal structure matters.** Decisions need "what if we change X"; experiments are often impossible, so structure is
   learned from observational data. Algorithms carry assumptions an expert must match.
2. **What agents promise.** Causal-Copilot automates the expert: data inspection, algorithm choice, a model review of the
   graph, a report. Its paper claims the review respects high-confidence bootstrap decisions and checks moderate ones.
   Recorded runs show otherwise (paper-vs-code D1-D2, `claude/causal-copilot-research-ledger.md`; site page
   copilot/step-refinement.html).
3. **The question and the controls.** Stated as in the abstract. Name arms, shuffled columns, code identity,
   pre-registration (`docs/q1_repo/docs/method.md`).
4. **Contribution so far.**
   - A recorded, reproducible replication.
   - A stage-by-stage diagnosis.
   - A drop-in replacement for the review step, measured against the original on the same image.
   - One traced case, showing the defect in each.

## 2. Prior work (about one page; sources: `analysis/literature/agent_reports/`)
- **LLM-assisted causal discovery.** Models used as experts on variable names: pairwise direction queries, orders and tiers,
  full graphs. Cluster 1.
- **Causal agents and how they are evaluated.** Causal-Copilot and the systems in our field audit: causaliq-knowledge,
  MATMCD, PyWhy-LLM, Vashishtha et al. Cluster 2.
  - The audit's finding to cite: swapped names cost three of five systems ≥ 0.10 directed F1.
  - The one that resists is the one whose data decide the graph (`analysis/reports/ab06*`; site page `names`).
- **Benchmarks and their shortcuts.**
  - CausalArena: published scores read the column layout (`analysis/reports/ab01_controlled_scoreboard.md`).
  - Memorisation and leakage: CARE already used moved-name controls. Cluster 8.
- **Bootstrap support and reliability of discovered edges.** Clusters 3-4.
- **What we add:** a stage-level account of one widely used agent, under controls, with recorded evidence for every step.

## 3. Data (half a page; source: `docs/q1/datasets.md`, frozen 10 Oct, manifest `manifests/evidence/suite_q1_2026-10-10.sha256`)
- **S2, the main suite:**
  - 10 CausalArena semantic test scenarios (Hugging Face `LAMDA-Tabular/CausalArena`, CC BY 4.0), each written three times
    with byte-identical numbers (real, neutral, swapped names);
  - columns shuffled, opaque paths;
  - the true graph is the simulating graph.
- **S1:** Sachs (protein signalling; the reference is contested, with at least three published versions) and four named
  real datasets (abalone, Auto MPG, concrete, DWD), each with real, neutral and moved names.
- **Recorded runs:** what one run contains (model calls, state after each stage, refinement sub-steps). How many: S1 84, S2
  30 + 30 + 30.
- **Limits:**
  - semantic scenarios are simulated;
  - one run per arm;
  - one model.

## 4. Code link (DLV-07)
- The public Q1 repository's URL goes here once Uzair has created it and CI is green.
- Before submission: re-run `py -3 tools\export_q1.py` so the repo matches the cc-research commit the report quotes.

---

# Outline for the final report (Fri 4 Dec): results sections, carried over from the 22 Oct outline

## 1. Question and setup (half a page)

- **Question:** what does Causal-Copilot (Lancelot39/Causal-Copilot, commit a31aa7c, GPT-4o) do to a causal graph, step by
  step? How much of its answer comes from the data, and how much from the variable names?
- **Control:** the same numbers are given under real, neutral and swapped column names. The columns are shuffled. The
  pipeline's code tree is checked before and after every run.
- **Suite (DLV-01, frozen 10 Oct):** `docs/q1/datasets.md`.
  - S1: Sachs plus four named real datasets.
  - S2: 10 CausalArena semantic test scenarios × 3 name arms, 30 tables.

## 2. Runs (DLV-02)

- S1: 84 live runs. S2: 30 live runs (BND-08, 11-12 Oct). Source: tracker DLV-02 note and `analysis/results/stability_s2/bnd08_summary.json`.
- The open gap: 6 S2 arms have no completed unmodified run. Their only run crashed in the cycle step and is scored at S3.
- The 22 Oct main-control series (`plans/results/fork_bld06_live_main.capped.json`, rebuilt image) reproduces BND-08:
  - 8 of 30 crashed, the same crash;
  - $12.57 against $12.68.

## 3. What each step does (DLV-03)

From `analysis/reports/bnd08_s2_results.md` and `analysis/reports/bundle1_results.md`:

| Finding | Number | Source |
|---|---|---|
| The bootstrap step lowers PC's adjacency F1 (M1) | 19 of 23 dev replay files | bnd08_s2_results.md |
| Real names lift S3 directed F1 by ≥ 0.10 over neutral (M2) | 5 of 10 families: refuted | bnd08_s2_results.md |
| LLM-set edges follow swapped labels (M3) | 81 of 101 distinct edges | bnd08_s2_results.md |
| Without names, below plain PC on the same file (M4) | 8 of 10 | bnd08_s2_results.md |
| Final adjacency F1, unmodified pipeline: algorithm output → final | 0.584 → 0.321 (22 completed runs, 22 Oct) | analysis/results/fork/bld06_live_compare.json |

## 4. A refinement that does not fall below its algorithm (DLV-04, live confirmation on S2)

Refinement v2 (branch `bld-06-refinement-v2` of our fork; `docs/FORK.md`) was run on the same 30 S2 tables, on the same image
as the main control (`analysis/results/fork/bld06_live_compare.json`, pre-registration `plans/bld06_live_prereg.json`):

- completed runs: 30 of 30, against 22 of 30;
- cost: $4.84 against $12.57;
- final adjacency F1, on the 22 tables where both completed: 0.596 against 0.321 (paired +0.276, interval 0.206 to 0.335);
- directed F1, the same tables: +0.014 (interval −0.017 to +0.038);
- final adjacency F1 below its own algorithm's output: 1 of 30 runs (by 0.006), against 22 of 22 for the unmodified pipeline;
- pre-registered rule outcome: **drop-in**.

Limit: one run per arm. Only the 10 S2 families are covered, not S1.

## 5. Benchmarks we use, audited (context, one paragraph each)

- **CausalArena:** published scores read the column layout (`analysis/reports/ab01_controlled_scoreboard.md`).
- **CausalBench:**
  - reproduced, all four MeanDifference rows (`analysis/results/ben13/summary.json`);
  - share table in `analysis/reports/ben13_s1_s2.md`: edge placement carries 0.07-0.14 of MeanDifference's above-random score
    (P1 fails); permuted labels fall to random level (P2 holds); 0.90 / 0.95 of the total-effect ceiling (P3 holds);
    STRING networks above same-size random networks (P4 holds).

## 6. Our own system so far (Quarter 2 preview, one paragraph)

- Kernel v3, the claim ledger.
- CausalArena held out (`analysis/results/q2_v3/v3_test.json`, regime D): semantic precision at half coverage 0.830
  [0.783, 0.874], ER-2 not met; formula 0.908 [0.876, 0.942], ER-2 met; ER-3 not met in either.
- Second family, held out (`analysis/results/q2_v3/family2_read.json`):
  - precision at half coverage 0.795 (0.777 to 0.811);
  - ECE 0.042;
  - target 0.80 not met.
- Next candidate: none adopted (`analysis/results/v4/decision.json`): three nonlinear GES scores gain +0.015 to +0.040
  in semantic dev precision, no interval excludes zero; v3 stays, the sealed held-out family is unread.

## 7. Limits and what is next

- Single runs per arm; one LLM (gpt-4o-2024-08-06).
- Rebuilt image: comparisons are made within one image.
- Results are hashed per CPU family; claim structure is checked across hosts (CAP-11, CAP-19).
- Next: DLV-04 on S1, the Quarter 1 final report (4 Dec).

## Number-to-ticket table

| Number | Ticket | Source file | Check |
|---|---|---|---|
| 30 / 30 vs 22 / 30 completed | BLD-06 | analysis/results/fork/bld06_live_compare.json `completed` | tracker check (p32) |
| 0.596 vs 0.321 final adjacency F1 | BLD-06, DLV-04 | same, `means.*.final_adj_f1` | tracker check (p32) |
| 0.795 [0.777, 0.811] | TGT-18 | analysis/results/q2_v3/family2_read.json `subsets.all` | TGT-18 checks (p31) |
| four MeanDifference rows reproduced | BEN-13 | analysis/results/ben13/summary.json `reproduction_all` | BEN-13 check (p31) |
| no v4 knob adopted; A1 +0.040 [-0.011, 0.094] | BLD-18 | analysis/results/v4/decision.json | BLD-18 check (p33) |
| P1 fails, P4 holds | BEN-13 | analysis/results/ben13/summary.json `predictions` | BEN-13 checks (p33) |
