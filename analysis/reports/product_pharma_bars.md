Tickets: PRD-01 (feeds PRD-02, PRG-01). Written 2026-10-30 by W4 (product path and IP). Desk research only: no model calls,
no API spend, no runs. Inputs: `claude/program-v3-2026-10-29.md` sections 5-6, `claude/ab14-market.md`,
`analysis/reports/ab14_market.md`, `analysis/reports/ben13_s1_s2.md`, `analysis/audits/AB13_regulation_map.{md,json}`,
`ledger/schema02.py`, and the kernel reports named next to each number.

# Pharma bars: what P1 and P2 would have to prove, and how far the project is from it

## Where we are now

Program v3 (section 5) named two pharma shapes for the system (B) and asked for the bar each would have to clear. This
report writes, for each shape, the buyer, the job, the evidence that buyer would demand (from primary sources), a numeric
bar, the distance from what the project has measured, and the cheapest experiments that would shrink that distance.

The short version:

- **P1, target prioritisation from perturbation screens, is not measurable yet.** The project has never run B on
  perturbation data. What it has measured is that CausalBench's main score cannot be the bar: MeanDifference reaches
  0.89-0.95 of the score a ranking of total effects computed on the test split gets (the "echo ratio" in BEN-13), and
  its second metric does not separate MeanDifference from random networks in 3 of 4 cells. A buyer's bar has to be set
  on knockdowns the method has never seen. The first two experiments (a held-out-gene split with baselines, and a scale
  curve) need no API credit and turn most of the P1 bar from estimates into measurements.
- **P2, the RWE assumption ledger, is close on format and far on validation.** Against ICH M14 (final at FDA on
  4 March 2026), ledger v0.2 records 4 of the 17 requirement rows mapped below, records 8 in part, and has no field for
  5. No validation on published RWE cases exists. The cheapest validation set, RCT-DUPLICATE's 32 trial emulations, is
  too small on its own to separate a good flag from a lucky one (section 4.4).
- **Two corrections to program v3 follow** (section 8): the P1 bar wording about "edge-placement share" should go,
  and the licence note needs a GPL caveat (details in `docs/decisions/2026-10-30_product_ip_questions.md`).

| Shape | Bars | Met today | Not met, with a number to compare | Not measurable yet | First experiment (cost) |
|---|---|---|---|---|---|
| P1 perturbation target prioritisation | 8 | 0 | 3, all on analogues only (P1-2, P1-4, P1-6: simulated or physical data, not perturbation screens) | 5 | E1 held-out-gene split and baselines (Uzair's machine, no API) |
| P2 RWE assumption ledger | 9 | 0 | 3 (P2-1 and P2-2 by desk mapping; P2-4 on an analogue) | 6 | F1 schema mapping to v0.2 (desk, free); F3 falsification simulation (free) |

Every bar in this report is a **target to validate, not a fact**. Each is labelled "estimate" and shows the anchor it was
set from. Nothing here should be read as "sellable"; program v3's rule holds that nothing is called sellable before a
sealed read meets the bar.

## 1. How to read this

Every figure carries one label, as in AB-14:

| Label | Meaning |
|---|---|
| **primary** | the issuer's own document, filing, release or paper (read on the issuer's or author's page) |
| **second-hand** | news, summaries, aggregators, or a library record of a paper not read |
| **vendor claim** | a company's statement about its own performance or results |
| **analyst claim** | a paid market-research figure |
| **estimate** | my arithmetic or my proposed bar, with inputs shown |
| **project measurement** | the project's own measured result, with its file |

Two further rules:

- **"Distance"** is bar minus today's number when both exist on the same task. When today's number exists only on a
  different task (simulated CausalArena files, the Causal Chambers light tunnel), it is marked **analogue** and is a
  hint, not a distance.
- **Regulatory text** was read through a fetch tool that summarises pages against a question, as in AB-13. The short
  quotes below came back as quotes, but section locators and wording must be checked in the PDF before anything is
  cited outside the project.

## 2. Design: the axes and the binding times

For each shape the same six fields are filled in. Bars are fixed at three binding times:

1. **Now (this report):** the bar's definition, the split it is measured on, and its threshold. The sha256 of this file
   is written in the commit message, so a later change to a bar is visible.
2. **Before the first data read of each experiment:** a pre-registration in `plans/` (owned by the chat that runs it),
   with seeds, tests and the exact scoring code hashed, as BEN-13 and the kernel reads did.
3. **At a sealed read:** a bar is "met" only on a sealed or held-out read, never on development data (program v3,
   section 4, rule 4).

## 3. P1: target prioritisation from perturbation screens

### 3.1 Buyer and job

- **Buyer (inference):** the discovery-biology side of a pharma or biotech: functional-genomics and computational-biology
  leads who run or buy pooled CRISPR screens with single-cell readout, and who own the budget for arrayed follow-up.
  Producers of perturbation maps (Recursion, academic atlas groups) are as likely to be partners or competitors.
- **Evidence that this budget exists:** Roche and Genentech have accepted six Recursion "Phenomaps", and Recursion
  reports **$213M** in upfront and milestone payments received from that collaboration, including **$30M** for each of
  two accepted neuroscience maps (primary, Recursion FY2025 results release, 25 Feb 2026). Recursion's statement that
  insights from the maps "are being validated" is a vendor claim.
- **Job to be done:** from a screen of thousands of knockdowns, rank which genes regulate a disease-relevant programme,
  say which links are direct, which are inferred and which are unknown, and so spend the arrayed validation budget on
  the predictions most likely to confirm. Each prediction must say how it would be checked.
- **Why causal claims matter to this buyer:** drug mechanisms with human genetic support are **2.6 times** as likely to
  succeed in development as those without, and the advantage grows with confidence that the gene is the causal one
  (primary, Minikel et al., medRxiv preprint read; published in Nature 629, 2024, per a library record, second-hand).
  This is the value anchor for "which gene is causal" claims, not evidence that perturbation-derived claims carry the
  same lift.

### 3.2 The evidence this buyer would demand

| Practice in the published record | What it shows | Label; source | What it forces into the bar |
|---|---|---|---|
| Score on perturbations never seen in training | Deep models (GEARS, scGPT) did not beat a simple linear model on unseen single knockdowns in Replogle K562 and RPE1, and an additive model beat them on double perturbations | primary (preprint); [Ahlmann-Eltze, Huber, Anders, bioRxiv 2024.09.16.613342](https://www.biorxiv.org/content/10.1101/2024.09.16.613342v1). Journal version not read | A held-out-gene split (P1-1) and a linear baseline (P1-3) |
| Remove systematic perturbed-vs-control differences before scoring | Simple baselines that average perturbed cells match or beat published methods; scores track how much systematic variation a dataset has | primary (authors' project page; paper not read); [Systema, Viñas Torné et al., Nature Biotechnology 2025](https://brbiclab.epfl.ch/projects/systema) | Scoring against the perturbed centroid, not only non-targeting cells (P1-2, P1-3) |
| Public challenge on CRISPRi Perturb-seq | 300 CRISPRi perturbations in H1 stem cells, ~1,000 cells each; models were "not yet consistently outperforming naive baselines across all metrics", and almost all scored worse than baseline on MAE | primary; [Arc Institute, Virtual Cell Challenge wrap-up, 6 Dec 2025](https://arcinstitute.org/news/virtual-cell-challenge-2025-wrap-up) | Baselines are the bar, not leaderboards (P1-3) |
| Network inference on real interventional data | "methods that use interventional information do not outperform those that only use observational data" | primary; [Chevalley et al., CausalBench, arXiv 2210.17283](https://arxiv.org/abs/2210.17283) | An observational baseline beside the interventional one (P1-3) |
| Knockdown efficacy and reproducibility | Median on-target knockdown 85.5% (K562) and 91.6% (RPE1); perturbation relationships agree across K562 timepoints (cophenetic correlation 0.82) much more than across cell lines (0.37) | primary (co-author's thesis chapter of Replogle et al., Cell 2022; check against Cell); [eScholarship](https://escholarship.org/content/qt59k3s8nq/qt59k3s8nq.pdf) | Cross-line agreement is reported, not thresholded (P1-8) |
| Orthogonal validation of top predictions | Of ten poorly annotated candidate ribosome-biogenesis factors, knockdown of nine caused substantial defects in an independent assay, with two independent guides per gene | primary (same thesis chapter) | The 0.9 precision anchor (P1-2) |

Our own measurements on CausalBench (project measurement, `analysis/reports/ben13_s1_s2.md`):

- **The reproduction is exact.** MeanDifference's published Wasserstein scores are reproduced in all four cells, and our
  fast evaluator equals causalbench's own.
- **The Wasserstein metric rewards total effects.** MeanDifference reaches 0.890-0.947 of a total-effect ranking computed
  on the test split itself (K562 k = 1000: 0.590 / 0.653 = 0.904). A method that recovers only direct links would score
  lower on it, not higher.
- **The split does not hold out knockdowns.** CausalBench's split is stratified by intervention (`plans/ben13_prereg.json`),
  so every knockdown is seen in training. MeanDifference ranks a knockdown's effect by measuring it.
- **The false omission rate does not separate MeanDifference from random networks** in 3 of 4 cells (within 0.035).
- **Choosing strongly perturbing parents alone earns 7-14% of MeanDifference's above-random score.** K562 k = 1000:
  (0.176 - 0.113) / (0.590 - 0.113) = 0.132. The other 86-93% comes from which children are picked for each parent.
  This is a decomposition of one method's score on one metric. It cannot be a bar for a different method (section 8, C1).

### 3.3 The P1 table: bar, distance, next experiment

| ID | What is measured | Bar (estimate, with anchor) | Today (label; file) | Distance | Next experiment |
|---|---|---|---|---|---|
| P1-1 | **The split.** Every P1 number is computed on knockdowns whose cells were withheld entirely from training | All P1 bars below use a pre-registered held-out-gene split (20% of knockdown genes, seeded), scored against both non-targeting cells and the perturbed centroid. Anchor: Ahlmann-Eltze et al.; Systema | Not built. BEN-13 uses CausalBench's intervention-stratified split (project measurement; `plans/ben13_prereg.json`) | The split does not exist | **E1** |
| P1-2 | **Precision of claims on held-out knockdowns.** A claim "knocking down X moves Y", with X held out, counts as right when the held-out cells show the shift (pre-registered test, FDR 0.05) | ≥ 0.90, with the lower 95% end ≥ 0.85, on ≥ 500 claims per cell line. Anchor: 9 of 10 top candidates confirmed by orthogonal knockdown in Replogle et al. | Not measured on perturbation data. Analogues: CausalArena held-out semantic precision at half coverage 0.830 [0.783, 0.874] (D, 1,000 rows) and 0.866 [0.799, 0.918] (DxR, 5,000 rows) (project measurement; `analysis/reports/q2_v3_heldout.md`); Causal Chambers light tunnel, committed claims agree with held-back intervention rows 98.5% of the time (project measurement; `analysis/reports/q2_b2_interventions.md`) | Unknown on P1. Analogue: 0.034-0.070 below 0.90 on the point; lower ends 0.051-0.067 below 0.85 | **E1** gives the base rate; **E3** gives B's number |
| P1-3 | **Better than simple baselines on the same split.** Baselines scored as claims at the same coverage: observational correlation ranking; STRING links; the linear model of Ahlmann-Eltze et al.; random | B's precision minus the best baseline's ≥ 0.10, with the paired-bootstrap interval above 0. MeanDifference is not a baseline here: it needs X's own knockdown | Not run on a held-out split. On CausalBench's own split, STRING networks score Wasserstein 0.132 (links) and 0.141 (physical) against 0.113 for same-size random networks in K562 (project measurement; BEN-13) | Unknown | **E1** |
| P1-4 | **Calibration on held-out knockdowns** | Expected calibration error ≤ 0.05, upper interval end included | Not measured on P1. Analogue: kernel v3 held-out ECE 0.021-0.026, upper ends 0.051-0.074, ER-3 not met (project measurement; `claude/q2-kernel-v3-results.md`, `analysis/reports/q2_v3_heldout.md`) | Analogue: upper ends 0.001-0.024 above 0.05 | **E3** |
| P1-5 | **Total and direct effects typed apart.** "Y moves when X is knocked down" (total) and "no measured mediator between X and Y" (direct) are separate claim types, scored separately | Total-effect claims meet P1-2. Direct-claim precision is reported, never pooled with total | Typing exists: B makes "connected, directness open" claims. On CausalArena, 84% of false links are mediated "shadows", and as connected claims they are 85-89% right; no forward shadow points the wrong way (project measurement; `analysis/reports/q2_v3_k1_k2_dev.md`) | Not scored on perturbation data | **E3** |
| P1-6 | **Abstention and licences.** No directed claim without a named licence (knockdown evidence, collider, Meek rule, declared knowledge); pairs with none stay "unknown" | 0 unlicensed directed claims. Directed claims licensed only by observational rules: held-out precision ≥ 0.80, reported per licence | Ledger check V13 requires evidence on the claim's own pair or named premises (`ledger/verify02.py`). Observational direction accuracy on CausalArena true links: collider 0.87 / 0.83, Meek R2 0.75 / 0.80, Meek R1 0.64 / 0.60 (project measurement; `claude/q2-kernel-v3-results.md`) | Analogue: Meek R1 is 0.16-0.20 below 0.80 | **E3**, per-licence breakdown |
| P1-7 | **Scale** | CausalBench K562 (622 genes after its filter, 162,751 cells) end to end, streamed, within laptop 2's memory, in ≤ 8 h wall time | The largest input B has run on has 23 variables (253 pairs) (project measurement; `docs/q1/datasets.md`). K562 has 193,131 gene pairs (763 times as many), RPE1 73,153 (289 times); Replogle's genome-wide K562 has 9,866 genes (48.7 million pairs) (estimate: n(n-1)/2) | 763 times the pair count; runtime curve unmeasured | **E2** |
| P1-8 | **Reproducibility across cell lines** | Report agreement on gene pairs shared by K562 and RPE1; no threshold, because Replogle's own cross-line similarity is 0.37 against 0.82 across timepoints | None | Not computed | **E4** |

### 3.4 The cheapest P1 experiments, in order

| # | Experiment | What it settles | Cost class | API |
|---|---|---|---|---|
| E0 | Check the Replogle numbers in the Cell paper itself, and the licence of the CausalBench and Replogle data files for product use | Whether the 0.9 anchor and the data can be cited and used | desk, ~1 h | none |
| E1 | Build the held-out-gene split on the streamed CausalBench files; score the four baselines as claims on held-out knockdowns at fixed coverages; record the base rate (share of held-out (X, Y) pairs that move) | P1-1 built; P1-3's baselines measured; the base rate that P1-2 must be read against | H job on Uzair's machine (19.4 GB of `.h5ad`, streamed as in BEN-13) | none |
| E2 | Kernel runtime and memory on gene subsets of 25, 50, 100 and 200, with the BLAS thread count pinned | A fitted curve that predicts the 622-gene time (P1-7), before anyone commits to it | H job, short | none |
| E3 | B's data-only and data-plus-interventions ledgers on a 100-200-gene subset, scored on the E1 split | P1-2, P1-4, P1-5 and P1-6 on real perturbation data for the first time | H job | none |
| E4 | Claims learned on K562 checked on RPE1's shared genes | P1-8 | desk, after E3 | none |

E1 to E3 belong to the chat that owns B's engine (W3) and to Uzair's machine. Each needs a pre-registration before the
first read. None needs a model call.

## 4. P2: the RWE assumption ledger

### 4.1 Buyer and job

- **Buyer:** the head of RWE or epidemiology at a sponsor, with biostatistics and regulatory affairs co-signing; CRO RWE
  practices as the channel (inference, from AB-14 Brief 3). ICH M14 asks for "an experienced, multidisciplinary study
  team" (primary; M14 section 5).
- **Job to be done:** before a non-interventional protocol and analysis plan go to FDA (R9: shared before the prespecified analyses), produce one record in which every
  causal assumption is typed (a DAG arc or a missing arc, no unmeasured confounding, positivity, measurement validity),
  has a source (literature, expert, data check), is tested against the data where it can be, carries its planned
  sensitivity analysis, and is bound to a dated plan. The record must let a reviewer re-derive every conclusion.
- **Why this buyer cares:** in FY2025, CDER acted on 10 NDA/BLAs that contained RWE. RWE contributed to 4 approvals, 1
  approval did not rely on it, and 4 received complete response letters and 1 a refusal to file. RWE protocols rose from
  10 (FY2023) to 11 (FY2024) to 31 (FY2025) (all primary; [FDA CDER RWE submissions page](https://www.fda.gov/science-research/real-world-evidence/real-world-evidence-submissions-center-drug-evaluation-and-research),
  content current as of 12 Jun 2026). The Biohaven troriluzole letter cited "lack of pre-specification and unmeasured
  confounding factors" (primary company release, via AB-14).
- **Market size:** AB-14's estimate for the regulatory core is $2.8-11.2M a year, and $20.3-101.7M a year across all
  registered RWE studies (estimates; inputs in `analysis/reports/ab14_market.md`, Brief 3). Nothing here changes them.

### 4.2 The evidence this buyer would demand: the regulatory texts

Each row was read on the issuer's page or PDF on 30 Oct 2026 unless marked. Status matters: two of the effectiveness texts
are still drafts.

| # | Text (status; date; docket) | What it says (short quote or close paraphrase; section) | Label; link |
|---|---|---|---|
| R1 | **ICH M14**, general principles for non-interventional studies using RWD for safety assessment (**final**; FDA publication 4 Mar 2026; FDA-2024-D-2754). Replaces the July 2024 draft | Scope is safety. FDA's page says its recommendations also apply to non-interventional studies of effectiveness | primary; [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m14-general-principles-planning-designing-analyzing-and-reporting-non-interventional-studies-utilize), [PDF](https://www.fda.gov/media/179795/download) |
| R2 | M14 section 5.1; section 7 | "the proposed study (design, data, methods, analysis) should be prespecified in the protocol"; "The statistical analysis should be prespecified" | primary; [PDF](https://www.fda.gov/media/179795/download) |
| R3 | M14 section 5.3 | Data must be shown "fit-for-use by assessing its relevance and reliability"; reliability includes accuracy, completeness, traceability and provenance (paraphrase) | primary; same PDF |
| R4 | M14 section 5.5.4 | "Directed acyclic graphs can be used to understand the relations between the variables"; "A number of approaches are available to address or evaluate unmeasured confounding" | primary; same PDF |
| R5 | M14 sections 3 and 7.1.3 | Quantitative bias analysis assesses "the sensitivity of study results"; "Sensitivity analyses should be pre-specified in the protocol and or the SAP with deviations documented in the final report"; bias-adjusted estimates need confidence intervals | primary; same PDF |
| R6 | M14 sections 6.1, 6.2.3 and 10 | Data management "should be recorded in sufficient detail so that they can be replicated"; "metadata-driven audit trails"; "ensure that an audit trail is maintained" | primary; same PDF |
| R7 | M14 sections 8.2 and 9 | Cites the ISPE/ISPOR HARPER protocol template as a framework sponsors may adapt; make the protocol "publicly available in appropriate public registers" and the results public | primary; same PDF; [HARPER, Value in Health 25(10), 2022](https://ispor.org/publications/journals/value-in-health/abstract/Volume-25--Issue-10/HARmonized-Protocol-Template-to-Enhance-Reproducibility-of-Hypothesis-Evaluating-Real-World-Evidence-Studies-on-Treatment-Effects--A-Good-Practices-Report-of-a-Joint-ISPE-ISPOR-Task-Force) |
| R8 | M14 section 1.3 | AI is named as possibly relevant, and the guideline says it "does not address those topics" | primary; same PDF |
| R9 | **FDA, Considerations for the Use of RWD and RWE** for drugs and biologics (**final**; Aug 2023; FDA-2021-D-1214) | "The protocol and SAP should be finalized and shared with FDA prior to conducting the prespecified analyses" (III.B.2); feasibility analyses "without evaluating outcomes for treatment arms" (III.B.2); "enable and maintain audit trails of data, starting from extracting RWD sources" (III.B.2); documentation that "would allow FDA to replicate the study analysis" (III.B.3); "Ensuring that FDA can access and verify relevant records", and sponsor electronic systems that comply with 21 CFR part 11 (III.B.6) | primary; [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-real-world-data-and-real-world-evidence-support-regulatory-decision-making-drug), [PDF](https://www.fda.gov/media/171667/download) |
| R10 | **FDA, RWE: Considerations Regarding Non-Interventional Studies** (**draft**; Mar 2024; FDA-2023-D-5470) | A protocol with "a causal diagram to specify the theorized causal relationship" (C, lines ~149-151); "assessment of unmeasured confounding" (E, ~226-227); "planned sensitivity analyses, including details on which factors are proposed to be changed" (E, ~246-247). It does not mention quantitative bias analysis or E-values | primary; [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-world-evidence-considerations-regarding-non-interventional-studies-drug-and-biological-products), [PDF](https://www.fda.gov/media/177128/download) |
| R11 | **FDA, Externally Controlled Trials** (**draft**; Feb 2023; FDA-2022-D-2983) | Describe every data source accessed while designing the control arm, keep audit trails of access and analyses, and test assumptions with sensitivity and bias analyses (AB-13 row 17; not re-read today) | primary via AB-13; [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-design-and-conduct-externally-controlled-trials-drug-and-biological-products), [PDF](https://www.fda.gov/media/164960/download) |
| R12 | **FDA device RWE guidance** (**final**; 18 Dec 2025; in effect 17 Feb 2026) | Protocol and analysis plan finalised before outcome data are reviewed; a relevance and reliability assessment in the study report (CDRH town-hall transcript read today); causal diagrams in the protocol (AB-13 row 19) | primary (town hall) and primary via AB-13; [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-real-world-evidence-support-regulatory-decision-making-medical-devices) |
| R13 | **FDA, AI to support regulatory decision-making** (**draft**; Jan 2025; FDA-2024-D-4689) | Still a draft when AB-13 read it (12 Oct 2026); not re-read today | primary via AB-13; [PDF](https://www.fda.gov/media/184830/download) |
| R14 | FDA's published complete response letters | More than 200 CRLs were published on openFDA on 10 Jul 2025, all for products later approved | second-hand; [RAPS](https://www.raps.org/resource/fda-publishes-200-complete-response-letters-in-tra.html) |

What the texts do **not** ask for, which bounds the pitch (as AB-13 found): no text asks for per-edge provenance by name.
FDA's draft asks for a causal diagram with its assumptions, and M14 says DAGs "can be used". The defensible claim is that
the ledger makes the required diagram and assumptions verifiable edge by edge, not that it meets a per-edge requirement.

### 4.3 ICH M14 against ledger v0.2

AB-13 mapped 50 requirement rows against ledger v0.1, but had no M14 row (an AB-14 correction). `ledger/schema02.py`
(BLD-14) since added `plan` (prereg path, sha256, fixed time), `deviations`, `assumptions` (statement, testable, a
sensitivity text), `lineage` (source, file, sha256, transformations), `question` (text, context of use, estimand) and
`reviews`. This table maps M14 to v0.2. It is a desk mapping (estimate of fit), and it does not check whether every
ledger the kernel writes fills these fields.

| # | M14 requirement (section) | v0.2 field(s) | Fit |
|---|---|---|---|
| M1 | Research question; target trial emulation may be used (4.1) | `question.text`, `question.estimand` | recorded |
| M2 | Multidisciplinary study team (5) | `reviews[]` (reviewer, scope, verdict) | partial: no roles or expertise |
| M3 | Design, data, methods and analysis prespecified in the protocol (5.1) | `plan.prereg`, `plan.prereg_sha256`, `plan.fixed_utc` | recorded |
| M4 | Fit for use: relevance and reliability; accuracy, completeness, traceability, provenance (5.3) | `lineage` | partial: provenance yes; no relevance assessment, no accuracy or completeness measures |
| M5 | Missing data described and handled (5.3.3, 7.1.2) | `lineage.transformations`, `assumptions[]` | partial: free text only |
| M6 | Operational definitions of exposure, outcome, covariates as code-based algorithms (5.4) | `variables.name`, `variables.data_id` | gap: no definition, code list or its hash (AB-13 G3) |
| M7 | DAGs to understand relations between variables (5.5.4) | `claims` (one per pair), `direction_source`, `knowledge` | recorded: declared and data-derived structure are typed apart |
| M8 | Address or evaluate unmeasured confounding (5.5.4) | `assumptions[]` (e.g. causal sufficiency) with `sensitivity` text | partial: no record of a run that evaluates it |
| M9 | Validation of key variables: PPV, sensitivity, specificity (5.6, 7.1.3) | none | gap |
| M10 | Data management recorded so it can be replicated (6.1) | `lineage.transformations`, certificate rerun command | partial: no code-list or extraction-query hash |
| M11 | Metadata-driven audit trails (6.2.3) | `report.created_utc` | gap: one timestamp per run (AB-13 G7) |
| M12 | Statistical analysis prespecified (7) | `plan` | recorded |
| M13 | Sensitivity analyses prespecified; deviations documented in the final report (7.1.3) | `assumptions[].sensitivity`, `deviations[]` | partial: deviations recorded; sensitivity runs not linked as records (G5, G8) |
| M14 | Quantitative bias analysis: indices prespecified; intervals for bias-adjusted estimates (7.1.3) | none | gap: the ledger holds no effect estimates (G9) |
| M15 | Protocol documents may follow HARPER (8.2) | none | gap: no export |
| M16 | Protocol in a public register; results public (9) | `plan.prereg` (a path) | partial: no registry id field |
| M17 | Audit trail maintained; records retained (10) | `report.ledger_sha256`, evidence hashes | partial: integrity yes, retention and access log no |

**Count: 4 recorded, 8 partial, 5 gaps out of 17** (estimate: desk mapping above).

### 4.4 The validation evidence this buyer already knows

RCT-DUPLICATE is the best-known test of whether database studies reproduce trials (primary;
[Wang, Schneeweiss et al., JAMA 2023;329(16):1376-1385](https://jamanetwork.com/journals/jama/fullarticle/2804067)):

- 32 trials were emulated in claims databases. The correlation between trial and database estimates was 0.82
  [0.64, 0.91]. Significance agreement was 72% in the abstract and 75% in the results text; estimate agreement 66%;
  standardized-difference agreement 75% (abstract) or 72% (text). The paper is inconsistent with itself on two of these.
- In a post hoc split, the 16 trials whose design could be closely emulated reached 94% significance agreement and a
  correlation of 0.93. The other 16 reached 50% and 0.53.

This split is exactly what an assumption ledger claims to see in advance: which emulations rest on assumptions the data
cannot support. It is also too small to prove it alone (estimate; Wilson 95% intervals): 15 of 16 is [0.72, 0.99] and 8
of 16 is [0.28, 0.72]. Even the paper's own split barely separates. A ledger flag would need more emulation pairs, or a
simulation with known truth, before its separation means anything.

### 4.5 The P2 table: bar, distance, next experiment

| ID | What is measured | Bar (estimate, with anchor) | Today (label; file) | Distance | Next experiment |
|---|---|---|---|---|---|
| P2-1 | **M14 coverage** | All 17 rows of section 4.3 recorded, or marked not applicable with a reason. Anchor: ICH M14 (R1-R8) | v0.2: 4 recorded, 8 partial, 5 gaps (estimate; section 4.3) | 13 rows | **F1**, then a v0.3 field proposal to W5 |
| P2-2 | **FDA drug-RWE and E9(R1) rows** (AB-13 rows 8-17, 29-30) | 12 of 12 recorded. Anchor: R9-R11 | 0 of 12 fully recorded under v0.1 (AB-13). Not re-mapped to v0.2 | 12 rows under v0.1; v0.2 unknown | **F1** |
| P2-3 | **Plan binding checked by the verifier** | The verifier rejects a ledger whose engine or knowledge differs from the plan hash; every analysis is labelled prespecified or post hoc; every deviation is dated. Anchor: R2, R9, M14 7.1.3 | v0.2 stores `plan` and `deviations`; verify02's V9 checks that `plan` exists and has a `prereg_sha256`. No check that the run's engine and knowledge match the plan appears in V1-V13 (project file; `ledger/verify02.py` docstring and V9 code) | One verifier check and one label field | **F1** |
| P2-4 | **The declared DAG tested against the data.** For each arc the sponsor declares absent, test the independence it implies | At n = 10,000, power ≥ 0.80 to flag one wrong arc, with a false-flag rate ≤ 0.05 per study, on simulated cohorts with binary and count variables like claims data. Anchor: Tennant et al. (via AB-13) found published DAGs almost never tested against data | Analogue: on 1,000-row simulated data, the Gaussian linear test wrongly rejects 10% of mediated pairs given the true parents (described as calibrated), the nonparametric tests 81-94% (project measurement; `analysis/reports/q2_v3_k1_k2_dev.md`). Binary and count variables untested | Analogue: false-flag rate 0.10 against 0.05; power unmeasured | **F3** |
| P2-5 | **Sensitivity analyses as records** | Every target effect has at least one prespecified sensitivity analysis recorded as a linked run (unmeasured-confounding bias analysis, alternative DAG, alternative definitions), with per-claim agreement. Anchor: M14 7.1.3; R10 | `assumptions[].sensitivity` is a text field. No sensitivity run records; no effect estimates (G5, G9) | The whole layer | **F1** (fields), then **F3** |
| P2-6 | **Validation on published cases** | A ledger flag, fixed before any result is read, separates trial-database agreement at least as well as RCT-DUPLICATE's post hoc split (94% against 50%), on at least 60 emulation pairs. Anchor: section 4.4 | Not run | All of it | **F4** |
| P2-7 | **Reproducible certificate** | Re-running the certificate's command reproduces every number to 0.001 | Exists for A's audit: the Q1 repo's `run.py reproduce` is exact (project measurement; `claude/w5-restart-2026-10-30.md`). Never run on an RWE study | Format exists; no RWE study | With **F3** |
| P2-8 | **System validation for submissions** | A qualified Part 11 gap assessment: audit trails, access control, electronic signatures, validation. Anchor: R9 III.B.6 | None; per-record audit trail absent (G7) | Far | **F6**, then an expert |
| P2-9 | **Domain fit** | An RWE practitioner reviews one end-to-end ledger for a realistic cohort and can trace every assumption to its source (qualitative) | None; the AB-10 interviews were not run | All of it | After **F2** and **F3** |

### 4.6 The cheapest P2 experiments, in order

| # | Experiment | What it settles | Cost class | API |
|---|---|---|---|---|
| F1 | Re-map AB-13's 12 drug-RWE rows and the 17 M14 rows to v0.2 field by field; list the v0.3 fields that close the gaps (variable definitions and code-list hashes; key-variable validation; per-record audit trail; sensitivity run records; derived effect estimates with bias-adjusted intervals; registry id) | P2-1, P2-2, P2-3 measured exactly; a contract proposal for W5 | desk, this chat | none |
| F2 | Render one existing ledger into HARPER's sections | Whether the ledger can fill the template sponsors already use (M15) | desk | none |
| F3 | Simulate cohorts with binary and count variables at n = 1,000, 10,000 and 100,000; declare a DAG with one wrong arc, then the right one; measure flag power and false-flag rate with the kernel's tests | P2-4 on its own task; the basis for P2-5's sensitivity runs | free (sandbox or a short H job) | none |
| F4 | Code RCT-DUPLICATE's 32 emulations (section 4.4), plus at least 28 more published emulation pairs, into ledgers from protocol documents only, with results redacted; hash the flag rule first | P2-6 | desk, days. Using a model to extract would cost credit: ask first | none unless approved |
| F5 | Code the published CRLs that mention RWE for reasons the ledger would have recorded (pre-specification, confounding, data fitness) | How much of a real rejection maps to ledger fields | desk | none |
| F6 | Draft a 21 CFR Part 11 gap list for the ledger and verifier (R9, III.B.6) | What an expert must review (P2-8) | desk, then an expert | none |

## 5. Which shape comes first

Program v3's default (P3-5: P2 format first, P1 as the performance stretch) still holds, for three measured reasons:

1. **P2's first experiments are free and mostly desk work** (F1, F2, F3), and they reuse the ledger and the certificate
   that the Q1 and Q2 papers need anyway.
2. **P1 cannot be scored until the split exists** (E1). The benchmark the project already reproduced measures total
   effects on seen knockdowns, which is not the buyer's question.
3. **P1's scale gap is about 763 times the pair count** of anything B has run (P1-7). Until E2 fits a curve, any
   P1 timeline is a guess.

What would change the order:

- E1 shows the base rate of "knockdown X moves Y" among held-out pairs is low (say under 0.2) and the baselines are weak.
  P1-2 would then be both hard and valuable, and P1 deserves W3 time sooner.
- F3 shows the kernel's tests cannot reach a 0.05 false-flag rate on binary and count data. P2-4, the ledger's one
  data-driven feature for RWE, would then be unavailable, and P2 shrinks to a documentation format that incumbents
  ("reproducible, traceable, and governed", Komodo, vendor claim via AB-14) already sell.

## 6. Failure modes, named before they happen

1. **Bars fitted to results.** These bars are written before E1-E4 and F1-F6. The file's sha256 goes in the commit
   message. A bar may change only in a new dated report that says why.
2. **Base-rate inflation in P1.** Knocking down essential genes moves many genes, so a high precision can be trivial. P1-2
   is read against E1's base rate, and P1-3 against baselines, both scored against the perturbed centroid (Systema).
3. **A total-effect metric rewarding pair-picking.** No P1 bar uses CausalBench's Wasserstein score (BEN-13 echo ratio
   0.89-0.95).
4. **Leakage in the RCT-DUPLICATE coding.** The trial results are public (section 4.4). Coding from redacted protocols, with a hashed
   flag rule, is the only defence. A coder who has read the JAMA paper should not code.
5. **Too few cases.** At 16 against 16, the intervals barely separate (section 4.4). P2-6 requires at least 60 pairs, or
   simulation with known truth.
6. **Regulatory wording from summaries.** Quotes came back from a summarising fetch tool. Every quote is checked in the
   PDF before it appears in a deck, a paper or an email.
7. **Scope mismatch.** M14 is scoped to safety studies. The effectiveness texts (R10, R11) are drafts and can change.
   A pitch that leans on them must say so.
8. **Data licences.** The CausalBench and Replogle files, and CausalArena, were downloaded for research. Their terms for
   product use were not checked (E0).
9. **The product story outrunning the papers.** Program v3 failure mode 4 applies unchanged: nothing here is a sales
   claim.

## 7. What a buyer would see today, honestly

- **P1:** "We reproduced CausalBench exactly and showed that its main score measures total effects on knockdowns the
  method has already seen. We have not yet run our system on perturbation data. Here is the held-out test we will hold
  ourselves to."
- **P2:** "Our claim ledger records 4 of ICH M14's 17 study-record requirements fully and 8 in part, with every causal
  claim tied to its evidence and a reproducible certificate. It has not been validated on a published RWE study."

## 8. Changes for W5 (program doc, contract, tickets)

These are proposals. W5 owns the program doc, the ledger contract and the tickets.

- **C1. Program v3, section 5, P1 bar.** Replace "Beat MeanDifference on held-out perturbations on structure, not
  pair-picking (edge-placement share well above its 7-14%)" with "precision of claims on held-out knockdowns ≥ 0.90
  (lower end ≥ 0.85), above the best simple baseline by ≥ 0.10, on a pre-registered held-out-gene split (P1-1 to P1-3)".
  Why: placement share decomposes MeanDifference's score on one metric (section 3.2). It is not something another
  method can be held to.
- **C2. Program v3, section 5, licence point 1.** "MIT-licensed, so a derived product is allowed with its notice kept"
  needs a caveat. The Causal-Copilot tree vendors a file marked GPLv2 and imports tigramite (GPL-3.0). See the decision
  doc, section 3.
- **C3. Ledger contract, v0.3 candidates (from M14's gaps):** variable definitions with code-list hashes (M6); key-variable
  validation records (M9); per-record audit trail (M11, M17); sensitivity analyses as linked run records (M13); derived
  effect estimates with bias-adjusted intervals (M14); a registry id (M16); a HARPER export (M15).
- **C4. Tickets.** PRD-01's evidence is this file; PRD-02's is `docs/decisions/2026-10-30_product_ip_questions.md`.
  Proposed new tickets (IDs from `trace.py next-id`, category 14 Stretch): E1, E2, E3 (owner W3, no API); F1, F2, F3, F5,
  F6 (owner W4); F4 (W4, ask before any model-assisted extraction).
- **C5. Program v3, section 5, IP point 2.** Add the relationship facts in the decision doc's section 4 (the README's
  "UCSD, Abel.ai" affiliation; Prof. Huang's company, Aether AI).

## Sources

Regulatory (primary unless marked):

- ICH M14 at FDA (final, 4 Mar 2026): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m14-general-principles-planning-designing-analyzing-and-reporting-non-interventional-studies-utilize ; PDF https://www.fda.gov/media/179795/download
- FDA, Considerations for the Use of RWD and RWE (final, Aug 2023): https://www.fda.gov/media/171667/download
- FDA, RWE: Non-Interventional Studies (draft, Mar 2024): https://www.fda.gov/media/177128/download
- FDA, Externally Controlled Trials (draft, Feb 2023): https://www.fda.gov/media/164960/download
- FDA, device RWE guidance (final, Dec 2025): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-real-world-evidence-support-regulatory-decision-making-medical-devices ; town hall transcript https://www.fda.gov/media/191329/download
- FDA, AI for regulatory decision-making (draft, Jan 2025): https://www.fda.gov/media/184830/download
- FDA RWE programme page and guidance list: https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence
- FDA CDER RWE submissions: https://www.fda.gov/science-research/real-world-evidence/real-world-evidence-submissions-center-drug-evaluation-and-research
- HARPER (ISPE/ISPOR, Value in Health 2022): https://ispor.org/publications/journals/value-in-health/abstract/Volume-25--Issue-10/HARmonized-Protocol-Template-to-Enhance-Reproducibility-of-Hypothesis-Evaluating-Real-World-Evidence-Studies-on-Treatment-Effects--A-Good-Practices-Report-of-a-Joint-ISPE-ISPOR-Task-Force
- RCT-DUPLICATE (JAMA 2023): https://jamanetwork.com/journals/jama/fullarticle/2804067
- CRLs on openFDA (second-hand, RAPS): https://www.raps.org/resource/fda-publishes-200-complete-response-letters-in-tra.html

Perturbation data and target discovery:

- Ahlmann-Eltze, Huber, Anders (bioRxiv): https://www.biorxiv.org/content/10.1101/2024.09.16.613342v1
- Systema (authors' project page): https://brbiclab.epfl.ch/projects/systema
- Virtual Cell Challenge 2025 wrap-up (Arc Institute): https://arcinstitute.org/news/virtual-cell-challenge-2025-wrap-up
- CausalBench (arXiv): https://arxiv.org/abs/2210.17283
- Replogle et al. 2022, thesis chapter version (eScholarship): https://escholarship.org/content/qt59k3s8nq/qt59k3s8nq.pdf
- Minikel et al. (medRxiv): https://www.medrxiv.org/content/10.1101/2023.06.23.23291765.full.pdf ; Nature record (second-hand): https://ideas.repec.org/a/nat/nature/v629y2024i8012d10.1038_s41586-024-07316-0.html
- Recursion FY2025 results release: https://ir.recursion.com/news-releases/news-release-details/recursion-reports-fourth-quarter-and-full-year-2025-financial

Project files: `analysis/reports/ben13_s1_s2.md`, `plans/ben13_prereg.json`, `analysis/reports/q2_v3_heldout.md`,
`analysis/reports/q2_v3_k1_k2_dev.md`, `analysis/reports/q2_b2_interventions.md`, `claude/q2-kernel-v3-results.md`,
`docs/q1/datasets.md`, `analysis/audits/AB13_regulation_map.json`, `ledger/schema02.py`, `ledger/verify02.py`,
`analysis/reports/ab14_market.md`.

## Where we're going

1. **F1 next** (desk, free, this chat): the exact v0.2 re-map of M14 and AB-13's drug rows, and the v0.3 field list for
   W5. It turns P2-1 to P2-3 from estimates into counts.
2. **F3** (free): the falsification simulation that decides whether P2 has a data-driven feature at all.
3. **E1 and E2** (W3 and Uzair's machine, no API): the held-out-gene split with baselines, and the scale curve. Until
   they run, P1's bars stay estimates.
4. The questions in `docs/decisions/2026-10-30_product_ip_questions.md` go to Prof. Umesh and Prof. Huang before any step
   that looks commercial.
