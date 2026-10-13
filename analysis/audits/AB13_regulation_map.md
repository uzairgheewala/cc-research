# AB-13 Regulation and standards map: what the claim ledger must record

Tickets: AUD-44, CAP-09, EXT-02. Written 2026-10-12. Typed table: `AB13_regulation_map.json` (50 requirement rows, 7 venues).
Inputs: `ledger/DESIGN.md` and `ledger/schema.py` (cc-claim-ledger/0.1), plus the prior notes in AU5 and AU8.

## Scope and method

- **Question.** Which requirements in drug-regulatory, AI-regulatory, bank-model-risk and epidemiology reporting texts
  would a causal analysis, or a causal-AI tool, have to satisfy? For each one: which ledger field records it, and what is
  missing?
- **Inclusion.** A requirement is included only if it concerns causal claims, provenance, reproducibility,
  record-keeping, transparency or human oversight.
- **Sources.** Every row was read on the issuer's own page or PDF, except one: the ROBINS-E domain names are second-hand.
  - FDA and EMA PDFs, the ICH PDF, and Federal Reserve letters.
  - The European Commission's AI Act Service Desk for article text. EUR-Lex returned only the recitals; see "Unread".
  - The journal PDFs for TARGET, RECORD-PE, Tennant et al. and Ellison and Rhoma.
- **Caveat on locators.** Pages were read through a fetch tool that summarises each page against a prompt. Section and
  line locators come from those summaries, so spot-check them in the PDF before citing them externally.
- **Wording.** The findings are phrased as "the text requires X; field Y records it". This is a design audit, not legal
  advice. Most FDA and EMA texts are non-binding guidance, and several are still drafts; each row gives its status.

## Corrections to earlier project notes

- **SR 26-2 exists, and was read in the primary text.**
  - The Federal Reserve, OCC and FDIC issued it on 17 April 2026. It supersedes SR 11-7 and SR 21-8.
  - Footnote 3 of the attachment puts generative and agentic AI outside its scope.
  - It is described as most relevant to banking organisations with more than $30bn in assets, and it states no
    prescriptive requirements.
  - AU5 and AU8 had this right.
  - Note that the SR 11-7 page itself still shows no "superseded" notice.
- **The EU AI Act dates moved.**
  - The Council gave the Digital Omnibus its final approval on 29 June 2026.
  - The Service Desk's consolidated Art. 113 (as at 27 July 2026) now applies the high-risk duties from 2 December 2027
    for Annex III systems and 2 August 2028 for Annex I systems.
  - Publication in the Official Journal was not read.
- **The FDA AI credibility guidance is still a draft.** The FDA page, read on 12 Oct 2026, still lists the January 2025
  guidance as a draft (docket FDA-2024-D-4689).
  - The newer text is the joint FDA-EMA "Guiding Principles of Good AI Practice in Drug Development" (14 Jan 2026), which
    is principles only.
- **FDA finalised a device RWE guidance on 18 Dec 2025.**
  - It requires a causal diagram in the protocol, time-stamped protocol revisions, and the first instance of the data
    plus an audit trail.
  - The accompanying press release (15 Dec 2025) says identifiable patient-level data are no longer always required for
    certain device submissions. FDA says it intends to consider the same change for drugs.

## Is a causal-analysis tool high-risk under the EU AI Act?

- **Not as such.** The high-risk categories are:
  - a safety component of an Annex I product that needs third-party assessment, such as software in a regulated medical
    device;
  - a system used in an Annex III area: biometrics, critical infrastructure, education, employment, essential services
    including credit scoring and life or health insurance pricing, law enforcement, migration, and justice.
- **Medicines regulation and scientific research are not Annex III areas.**
- **Exclusions.**
  - Art. 2(6) excludes systems built and used solely for scientific research.
  - Art. 2(8) excludes R&D before a system is placed on the market.
  - Art. 2(12) excludes open-source releases, unless they are placed on the market as high-risk.
- **When the tool becomes high-risk: conditional.** It becomes high-risk when a deployer uses it for an Annex III
  purpose, for example to choose the features of a credit or insurance-pricing model, or when it ships inside a medical
  device.
  - Even then, the Art. 6(3) derogation for "preparatory" or "narrow procedural" tasks may apply.
  - The derogation never applies if the system profiles people, and the provider must document that assessment.
- **Consequence for the capstone.** It sits under the research exclusion. Arts. 12-14 matter only as the design target
  for a deployable version.

## Requirement to field matrix

Gap codes are defined in the next section. "none" means the current format records the requirement.

| # | Instrument (status; locator) | The text requires | Field(s) that record it | Gap | Label |
|---|---|---|---|---|---|
| 1 | FDA AI draft 2025 (draft; IV.A.1-IV.A.3 (Figure 1)) | Define the question of interest and the context of use (the model's role, what output is used for, what other evidence it is combined with); then rate model risk as model influence times decision consequence and scale credibility work to it. | `report.regime`, `claims.direction_source` | G2: no question or context-of-use field; regime and direction_source show how much knowledge shaped the output but no influence/consequence rating is recorded | read (primary) |
| 2 | FDA AI draft 2025 (draft; IV.A.4.a.i) | The credibility plan describes the model: inputs, outputs, architecture, features, parameters and the rationale for the modelling approach. | `report.engines`, `evidence.engine`, `evidence.type`, `claims.licensed_by` | engine configuration (CI test, alpha, score, max conditioning size) is not a required field; licensed_by names the rule but not its parameters | read (primary) |
| 3 | FDA AI draft 2025 (draft; IV.A.4.a.ii; IV.A.4.b) | Describe development and evaluation data: how collected, processed, stored and controlled, and whether fit for use; reliable data are accurate, complete and traceable. | `variables.var_id`, `evidence.data_sha256`, `report.data_sha256` | G3: hashes prove which bytes were analysed, not where they came from or how they were processed | read (primary) |
| 4 | FDA AI draft 2025 (draft; IV.A.4.a.iii (lines ~371-404); IV.B) | Track software version changes during training; name the sources of any pre-trained models; manage and report model changes over the life cycle. | `evidence.engine.version`, `evidence.engine.wheel_sha256`, `report.engines`, `knowledge.supplier.model_id`, `format` | G10 (minor): versions are pinned per run, but there is no change log across tool releases; model_id is a free string with no snapshot date | read (primary) |
| 5 | FDA AI draft 2025 (draft; IV.A.4.a.iii; IV.A.4.b (lines ~459-464)) | Give performance metrics with confidence intervals, estimate and interpret uncertainty of outputs, and consider repeatability or reproducibility studies. | `claims.confidence.bootstrap_frequency`, `claims.confidence.calibrated_probability`, `claims.confidence.calibration_set`, `report.permutation_check`, `report.seeds` | G6: no calibration metric with interval; seed-to-seed repeatability is not recorded as a check the way order invariance is | read (primary) |
| 6 | FDA AI draft 2025 (draft; IV.A.4.b (lines ~447-449)) | Where a human is in the loop, evaluate the performance of the human-AI team, not the model alone. | `knowledge.supplier.type`, `knowledge.supplier.shown`, `overrides` | G4: person-supplied knowledge is recorded, but a human's decision on the output (accept, edit, reject a claim) is not | read (primary) |
| 7 | FDA AI draft 2025 (draft; IV.A.6 (lines ~479-495)) | Document results of the plan and any deviations from it in a credibility assessment report, held for FDA on request or submitted. | `report`, `report.invariants`, `report.unverifiable`, `report.ledger_sha256` | G1: there is no plan object, so deviations cannot be stated against it | read (primary) |
| 8 | FDA RWE non-interventional draft 2024 (draft; III.B (lines ~112-113); III.E (lines ~215-216)) | Finalise the protocol before the study is conducted and prespecify the statistical analysis plan. | `report.created_utc` | G1: nothing proves the engine config and knowledge set existed before the data hash was first computed | read (primary) |
| 9 | FDA RWE non-interventional draft 2024 (draft; III.C (lines ~149-151, fn 16); III.B (lines ~137-139)) | Include in the protocol a causal diagram (DAGs or SWIGs given as examples) showing the theorised causal relationships, and describe the approach to causal inference. | `claims.relation`, `claims.direction_source`, `claims.licensed_by`, `claims.evidence`, `knowledge.kind`, `knowledge.content` | partial: FDA's diagram is an a priori theory; the ledger has no flag separating a prespecified hypothesised graph (as knowledge) from the discovered one, and no export of the final graph as a protocol figure | read (primary) |
| 10 | FDA RWE non-interventional draft 2024 (draft; III.E (lines ~226-230, ~246-247)) | The analysis plan says how confounding will be handled, including an assessment of unmeasured confounding and overadjustment on intermediates, and describes planned sensitivity analyses (what is varied and why). | `claims.relation (x<->y)`, `report.regime`, `report.unverifiable`, `claims.confidence.bootstrap_frequency` | G5 and G9: causal sufficiency is not recorded as an assumption; bootstrap is the only typed perturbation; no adjustment set or mediator list is derived from the final graph | read (primary) |
| 11 | FDA RWD EHR/claims final 2024 (final; III; IV.B.4; IV.D.1; V.E.1, V.E.3; I (fn 11)) | Give conceptual and operational (code-based) definitions for population, exposure, outcome and covariates, with computable phenotypes in machine-processable form; disclose unmeasured or imperfectly measured confounders and justify proxies; reliability includes traceability (known provenance, e.g. an audit trail). | `variables.name`, `variables.var_id`, `claims.relation (x<->y)`, `evidence.data_sha256` | G3: a variable has a name and content hash but no definition, code-list hash or proxy flag; provenance stops at the hash | read (primary) |
| 12 | FDA RWD EHR/claims final 2024 (final; IV.C) | Describe reasons for missing data, state the missingness assumptions and run sensitivity analyses on them. | `evidence.data_sha256` | G3 and G5: no record of deletion or imputation, nor of the missingness assumption the tests relied on | read (primary) |
| 13 | FDA RWD/RWE final 2023 (final; III.B.2; III.B.6) | Keep audit trails from RWD extraction to dataset retention that track user access, data changes, protocol changes and analyses; electronic systems meet 21 CFR part 11. | `report.created_utc`, `report.ledger_sha256`, `report.run_id` | G7: the hash gives integrity but not authenticity; there is no signature, access log or per-record timestamp | read (primary) |
| 14 | FDA RWD/RWE final 2023 (final; III.B.3) | Document data, code and algorithms well enough for FDA to replicate the analysis. | `report.engines`, `evidence.engine.wheel_sha256`, `report.seeds`, `evidence.seed`, `evidence.data_sha256`, `evidence.conditioning`, `evidence.statistic`, `evidence.p_value` | mostly met: engine, version, wheel hash, seed and data hash pin a rerun; missing are the engine configuration (see FDA AI row 2) and the preprocessing code hash (G3) | read (primary) |
| 15 | FDA RWD/RWE final 2023 (final; III.B.2; III.B.4) | Document the data sources evaluated and why each was chosen or excluded; label analyses outside the SAP as exploratory; identify and document protocol and SAP deviations; date-stamp revisions. | none | G1 and G8: no plan, no deviations, no exploratory flag, no links to other runs on other data | read (primary) |
| 16 | FDA ECT draft 2023 (draft; III.C.1 (lines ~385-397)) | Submit the SAP before enrolment; do not make design decisions while viewing external-control outcomes; date and justify any SAP change. | `knowledge.supplier.shown`, `report.created_utc` | G1: supplier.shown records what a knowledge supplier saw (analogous to blinding), but there is no plan hash and no proof of ordering | read (primary) |
| 17 | FDA ECT draft 2023 (draft; III.A.1 fn 18; III.C.1 (lines ~409-429)) | Describe every data source accessed while designing the control arm, including feasibility and exploratory analyses; generate audit trails of access to and analyses of those sources; make assumptions explicit and test them with sensitivity and bias analyses. | `report.data_sha256`, `report.unverifiable` | G8, G7, G5 | read (primary) |
| 18 | FDA device RWE final 2025 (final; V.B.2; VII.A) | Identify the first instance of the data, keep a data audit trail and retain transformations to a common data model; name RWD sources, versions and extraction dates. | `evidence.data_sha256`, `variables.var_id` | G3 | read (primary) |
| 19 | FDA device RWE final 2025 (final; VI; VI.B.3; VII.B) | Protocol includes causal diagrams; protocol and analysis plan are finalised before outcome data are reviewed; revisions are dated, time-stamped and justified; key design decisions and rationale documented. | `claims.relation`, `claims.licensed_by`, `claims.direction_source` | G1: graph and per-edge rationale are present; the time-stamped plan is not | read (primary) |
| 20 | FDA-EMA GAIP 2026 (guideline; Principles 6 and 8) | Record data origin, processing steps and the reasons for analytical choices so every step can be traced and verified (principle 6); evaluate the whole system including human interaction (principle 8). | `claims.evidence`, `claims.licensed_by`, `claims.direction_source`, `knowledge.supplier`, `overrides`, `report.ledger_sha256` | reasons for analytical choices are met at claim level (V2 closure); G3 for processing steps; G4 for human interaction | read (primary) |
| 21 | FDA-EMA GAIP 2026 (guideline; Principle 10) | Give plain-language information on purpose, performance, limitations, underlying data, updates and how to understand outputs. | `report.unverifiable`, `report.commentary`, `claims.direction_source` | the rendered human-readable report is promised in DESIGN.md but not specified; purpose field missing (G2) | read (primary) |
| 22 | EMA AI reflection paper 2024 (final; 2.5.1; 2.3.3.3; 2.5.3) | Document data sources, acquisition and every processing step in a detailed and fully traceable way, in line with GxP; keep development logs that allow secondary assessment. | `claims.evidence`, `evidence.data_sha256`, `evidence.engine`, `report.ledger_sha256` | G3 for processing before the hash; analysis steps after the hash are met | read (primary) |
| 23 | EMA AI reflection paper 2024 (final; 2.3.3.3; 2.3.7; 2.5.2) | In pivotal trials, freeze and record the preprocessing pipeline and all models in the SAP before database lock; incremental learning is not accepted there. | `evidence.engine.wheel_sha256`, `report.engines`, `report.seeds`, `knowledge.supplier.model_id`, `knowledge.supplier.prompt_sha256` | G1: frozen components are identified, but nothing proves they were frozen before database lock | read (primary) |
| 24 | EMA AI reflection paper 2024 (final; 2.5.5) | Prefer transparent models; black boxes need justification; explainability methods encouraged. | `claims.licensed_by`, `claims.evidence`, `evidence.statistic`, `evidence.p_value`, `evidence.conditioning` | none: each mark is explained by a named rule and the tests it fired on | read (primary) |
| 25 | EMA AI reflection paper 2024 (final; 2.3.5; 2.5.6; 2.8) | Generative language models can give plausible but wrong output, so their output needs close human supervision and quality review. | `knowledge.supplier.type`, `knowledge.supplier.model_id`, `knowledge.supplier.prompt_sha256`, `knowledge.supplier.shown`, `claims.data_only_relation` | G4: LLM statements are isolated and cannot add edges (V3), but a human's review of them is not recorded | read (primary) |
| 26 | EMA PROCOVA opinion 2022 (final; Q1, Q2, Q6) | The prognostic score is prespecified before unblinding, defined independently of the study data, and its weights are not adjusted to the trial. | `knowledge.supplier.shown`, `knowledge.content` | G1: binding times in DESIGN.md say knowledge is fixed before resolution, but the record cannot prove it was fixed before the data were seen | read (primary) |
| 27 | EMA PROCOVA opinion 2022 (final; Q6; Q1; Section 4) | Type I error control, unbiasedness and interval coverage do not depend on the prognostic model's performance; only efficiency does (asymptotically, under stated assumptions). | `claims.data_only_relation`, `report.invariants`, `report.regime` | partial: V3 and V8 give the analogous floor for the skeleton (knowledge never connects); orientations from knowledge carry no error guarantee, and the floor's own finite-sample error is not stated | read (primary) |
| 28 | EMA PROCOVA opinion 2022 (final; Q5) | Validate on data independent of both training and study data to avoid optimistic estimates; run sensitivity analyses on the assumed correlation. | `claims.confidence.calibration_set` | G6: calibration_set is an id, not a data hash, so disjointness from the analysed data cannot be checked | read (primary) |
| 29 | ICH E9(R1) (final; A.1; A.3.2-A.3.3; A.6) | Define the estimand (treatment, population, variable, intercurrent-event handling, population-level summary) in the protocol before the trial; the principles also apply to observational studies. | none | G2 and G9 | read (primary) |
| 30 | ICH E9(R1) (final; A.5.1; A.5.2.1; A.6) | State the key assumptions of the main estimator explicitly; plan sensitivity analyses in advance; report main, sensitivity and supplementary results, labelling each as prespecified, introduced while blinded, or post hoc. | `report.invariants`, `report.unverifiable`, `report.regime` | G5 and G1: invariants I1-I7 are properties of the tool, not the world assumptions (sufficiency, faithfulness, acyclicity, alpha) the claims rest on; no prespecified/post hoc label on a run | read (primary) |
| 31 | EU AI Act Arts. 2, 6, Annex III (final; Art. 6(1)-(4); Annex III 4, 5(a)-(c); Art. 2(6), 2(8), 2(12); Art. 113) | A system is high-risk if it is a safety component of an Annex I product needing third-party assessment, or is used in an Annex III area (e.g. credit scoring, life/health insurance pricing, employment, essential benefits); an Annex III system may escape via the narrow-task or preparatory-task derogation, unless it profiles people, and the provider must document that assessment. AI used solely for scientific research, and pre-market R&D, are outside the Act. | none | G2: no intended-purpose field from which the classification could be read | read (primary) |
| 32 | EU AI Act Arts. 12, 19 (final; Art. 12(1)-(2); Art. 19(1)) | High-risk systems log events automatically over their lifetime, giving traceability for risk situations, post-market monitoring and operational monitoring; providers keep logs they control for at least six months. | `report.run_id`, `report.created_utc`, `report.ledger_sha256`, `report.data_sha256`, `evidence`, `claims` | G7: one ledger per run is an event log for that run, but there is no cross-run log, per-event timestamp or retention statement | read (primary) |
| 33 | EU AI Act Art. 13 (final; Art. 13(3)(b)(i), (ii), (vi)) | Instructions state intended purpose, accuracy levels and the metrics used, factors affecting them, and specifications of input and training/validation data. | `claims.confidence.calibrated_probability`, `claims.confidence.calibration_set`, `report.regime` | G6 and G2 | read (primary) |
| 34 | EU AI Act Art. 13 (final; Art. 13(3)(b)(iii), (iv), (vii); 13(3)(f)) | Disclose foreseeable circumstances that create risk, features that help explain outputs, information for interpreting outputs, and mechanisms for collecting and interpreting logs. | `claims.licensed_by`, `claims.direction_source`, `claims.data_only_relation`, `report.unverifiable`, `report.ledger_sha256` | none in the format; verify.py is the log-interpretation mechanism | read (primary) |
| 35 | EU AI Act Art. 14 (final; Art. 14(4)(a)-(d)) | Overseers must be able to understand capabilities and limits, stay aware of automation bias, interpret output correctly, and decide to disregard, override or reverse an output. | `claims.direction_source`, `claims.data_only_relation`, `report.unverifiable`, `overrides` | G4: data_only_relation shows what the data alone support (an aid against automation bias), but a human override of a claim has no record type; overrides covers only knowledge vs. intervention | read (primary) |
| 36 | EU AI Act Art. 10 (final; Art. 10(2)(a)-(h)) | Training, validation and test data practices cover design choices, data origin and collection, preparation, the assumptions about what data represent, bias examination and data gaps. | `claims.confidence.calibration_set`, `evidence.data_sha256` | G3 and G5 | read (primary) |
| 37 | EU AI Act Art. 17 (final; Art. 17(1)(d), (f), (k)) | Providers keep a documented QMS including testing and validation procedures, data management across the data lifecycle, and record-keeping of relevant documentation. | `report`, `report.invariants`, `report.permutation_check` | mostly organisational and outside the record format; the ledger can be the per-run evidence a QMS points to | read (primary) |
| 38 | EU AI Act Annex IV (final; Annex IV 1(a), 1(c), 2(a), 2(b), 2(d), 2(g), 6) | Document version and relation to earlier versions, design choices with rationale and assumptions, third-party pre-trained models used, datasheets on data origin and preparation, lifecycle changes, and validation and test logs that are dated and signed. | `claims.licensed_by`, `report.engines`, `evidence.engine.version`, `knowledge.supplier.model_id`, `report.permutation_check`, `report.invariants`, `format` | G7: test results exist but are unsigned; G5 assumptions; G3 datasheets; G10 change log | read (primary) |
| 39 | SR 26-2 (2026) (final; §I; §II and fn 1-3) | A model is a quantitative method applying statistical or economic theory to turn inputs into estimates; generative and agentic AI are outside this guidance; it is most relevant to banking organisations over $30bn in assets and states no prescriptive requirements. | `knowledge.supplier.type`, `knowledge.supplier.model_id`, `claims.direction_source` | none for scoping: the ledger already separates the in-scope model (engines) from out-of-scope generative input (supplier type model) | read (primary) |
| 40 | SR 26-2 (2026) (final; §III; §V; §VII) | Document design choices, assumptions, judgements and data selection; effective challenge by objective, competent people with standing; ongoing monitoring and outcomes analysis; for vendor models, understand conceptual soundness and performance even when code is proprietary. | `claims.licensed_by`, `claims.evidence`, `evidence.type (intervention_shift)`, `report.invariants`, `report.unverifiable`, `report.ledger_sha256` | G5 assumptions; G4 the challenger's findings have no record; no link from claims to later observed intervention outcomes. Met: verify.py checks claims without code or data, which suits a validator facing a vendor tool | read (primary) |
| 41 | SR 11-7 (superseded) (final; letter text (documentation; validation sections)) | Documentation detailed enough that parties unfamiliar with a model understand its operation, limits and key assumptions; validation covers conceptual soundness, ongoing monitoring and outcomes analysis. | `claims.licensed_by`, `claims.evidence`, `report.unverifiable` | G5 assumptions | read (primary) |
| 42 | TARGET 2025 (guideline; Items 6g, 7g(i), 7g(ii)) | List the assumptions needed to identify each causal estimand and the variables they involve; justify the baseline confounders chosen and say how they were measured. | `claims.relation`, `claims.evidence`, `knowledge.content`, `variables.name` | G5 and G9: confounder choice would follow from the graph, but the derived adjustment set and its assumptions are not recorded | read (primary) |
| 43 | TARGET 2025 (guideline; Items 7h(i), 7h(ii), 14, 18, 19) | Describe sensitivity analyses, their rationale and the biases they target, and report all their results; describe models and software; report availability of data, code and materials, and registration. | `report.engines`, `evidence.engine.version`, `report.seeds` | G5 sensitivity; G1 registration | read (primary) |
| 44 | STROBE (guideline; Items 7, 8, 12(a)-(e), 16(a)) | Define every outcome, exposure, confounder and effect modifier and give data source and measurement for each; describe methods for confounding, missing data and sensitivity analyses; report which confounders were adjusted for and why. | `variables.name`, `variables.var_id`, `claims.relation`, `claims.evidence` | G3 definitions; G9 adjustment set and its reason | read (primary) |
| 45 | RECORD-PE 2018 (guideline; Items 7.1, 12.2, 12.3, 22.1) | Give complete code lists and algorithms for exposures, outcomes and confounders; describe data cleaning and record linkage and its quality; say how readers can obtain protocol, raw data and programming code. | `variables.var_id`, `evidence.data_sha256`, `report.engines` | G3 | read (primary) |
| 46 | Tennant et al. 2021 (guideline; Recommendations 2 and 5; Results) | Make every DAG available; assume arcs exist by default and justify each omitted arc with theory or evidence (only 6% of 144 DAG papers cited sources for arcs; none tested DAG-data consistency). | `claims.relation (none)`, `claims.evidence`, `evidence.supports (nonadjacent)`, `evidence.conditioning`, `claims.licensed_by` | none: each absent pair is a claim citing the separating test; this is the strongest single fit in the map | read (primary) |
| 47 | Tennant et al. 2021 (guideline; Recommendations 1, 6, 7, 8) | State the focal relationship and estimand; state the DAG-implied adjustment set for each estimand and report its estimate even if not the main result; justify alternative sets. | none | G2 and G9 | read (primary) |
| 48 | Ellison & Rhoma 2025 (guideline; Principles 3 and 4; Section 3.1; Conclusions) | Report the DAG's purpose and the reasoning for its arcs (theoretical, speculative or temporal); report unmeasured variables and temporal uncertainty; use machine-readable notation; compare results across plausible alternative DAGs. A narrative review, not a consensus checklist. | `claims.direction_source`, `claims.licensed_by`, `knowledge.kind (tier)`, `claims.relation (x<->y)` | G5 alternative-DAG sensitivity; machine-readable export is planned (DESIGN.md section 5) but not built | read (primary) |
| 49 | ROBINS-E 2024 (guideline; Preliminary considerations; domains (names second-hand)) | Before rating bias, specify the result being assessed and the causal effect it estimates; then judge seven bias domains (confounding first among them) and the likely direction of bias. | `claims.relation (x<->y)`, `report.unverifiable` | G2 and G5 | second-hand |
| 50 | W3C PROV-O (final; Sections 3.1 (starting point), 3.3 (qualified terms)) | Format venue: Entity, Activity, Agent with wasGeneratedBy, used, wasDerivedFrom, wasAttributedTo, wasAssociatedWith; qualified terms (qualifiedDerivation, Plan, hadPlan); no notion of rules or confidence. | `variables`, `evidence`, `knowledge.supplier`, `claims.evidence`, `claims.licensed_by`, `report.engines` | licensed_by maps naturally to prov:Plan via hadPlan; confidence and direction_source need an extension vocabulary; prov_export.py not written | read (primary) |

## Ledger gaps, ranked

The ranking weighs how many texts ask for the item, how binding those texts are, and whether the gap blocks a claim the
project already wants to make.

| Rank | Gap | What the texts require | Asked by | Proposed field (design only) |
|---|---|---|---|---|
| 1 | **G1 Plan binding and deviations** | The texts require the analysis plan, including models and any ML pipeline, to be fixed and dated before the data or outcomes are seen. Deviations must be dated, justified and labelled post hoc. | FDA AI (IV.A.6), FDA non-interventional (III.B, III.E), FDA RWD/RWE 2023 (III.B.2, III.B.4), FDA ECT (III.C.1), FDA devices 2025 (VII.B), EMA AI paper (2.3.3.3), PROCOVA (Q2, Q6), ICH E9(R1) (A.6), TARGET (18) | `plan`: sha256 of the engine config, alpha, knowledge set and prompt templates, with a timestamp and an optional registry id. The verifier checks that every claim's engine and knowledge match `plan`. Add `deviations[]` (what, when, why) and `analysis_status` ∈ {prespecified, post_hoc}. Without this, the PROCOVA analogy (knowledge fixed before data) cannot be shown, only asserted. |
| 2 | **G5 Assumptions and sensitivity** | The texts require the identifying assumptions to be stated explicitly and sensitivity analyses to be planned, with their rationale and all their results reported. | FDA non-interventional, FDA ECT, FDA EHR (IV.C), ICH E9(R1) (A.5), TARGET (6g, 7g, 7h), SR 26-2, Ellison and Rhoma, EU AI Act Art. 10(2)(d) and Annex IV 2(b) | `assumptions[]`, typed: causal_sufficiency, faithfulness, acyclicity, iid, test, alpha, missingness. Each names which claims depend on it. `sensitivity[]` records link sibling run ids (other alpha or test, knowledge subsets, alternative DAGs) and give the per-claim agreement rate. |
| 3 | **G3 Data lineage** | The texts require each data source, its version and extraction date, the cleaning, linkage and missing-data handling, and operational definitions or code lists, to be traceable. | FDA EHR/claims (final), FDA RWD/RWE 2023, FDA devices 2025, FDA AI (IV.A.4.a.ii), EMA AI (2.5.1), FDA-EMA principle 6, EU AI Act Art. 10 and Annex IV 2(d), STROBE 7-8, RECORD-PE 7.1, 12.2, 12.3 | `data_lineage` per `data_sha256`: source, version, extraction date, the hash of the transformation code and of a definitions or code-list document. The ledger should point to lineage by hash, not hold it; the verifier can only check that the pointer exists. |
| 4 | **G4 Human review** | The texts require that people can interpret, override or reject outputs, and that human-AI team performance and effective challenge are evaluated. | EU AI Act Art. 14(4), EMA AI (2.3.5, 2.5.6), FDA AI (IV.A.4.b), FDA-EMA principle 8, SR 26-2 (effective challenge) | `reviews[]`: reviewer (person id or role), timestamp, claim id, action ∈ {accept, reject, flag}, reason. To respect the binding times, a review never rewrites a claim. A rejection removes the claim from the "endorsed" view, and the data-only floor (V8) is unaffected. |
| 5 | **G2 Question and context of use** | The texts require the question of interest, the context of use, the intended purpose and (for effect estimates) the estimand to be stated. | FDA AI (IV.A.1-3), ICH E9(R1) (A.3), EU AI Act Art. 6 and 13(3)(b)(i), FDA-EMA principle 4, Tennant (rec. 1), ROBINS-E | `question`: free text plus typed `target_pairs` or `target_effect` (exposure, outcome), `context_of_use`, and `influence` ∈ {sole, contributory, exploratory}. This also gives the input for EU AI Act classification. |
| 6 | **G9 Derived adjustment set** | The texts require stating the adjustment set the graph implies and why the confounders were chosen. | FDA non-interventional (III.E), TARGET (7g), STROBE (16a), Tennant (recs. 6-8), ICH E9(R1) | `derived[]`: for each `target_effect`, the adjustment set or sets computed from the final graph by a named rule, or "not identifiable", plus the claim ids it rests on. |
| 7 | **G7 Audit trail and signatures** | The texts require audit trails of data access and analyses, Part 11 electronic records, lifetime logs kept for at least six months, and signed and dated test logs. | FDA RWD/RWE 2023 (III.B.2, III.B.6), FDA ECT (fn 18), EU AI Act Arts. 12 and 19, Annex IV 2(g) | Per-record `created_utc`; an optional detached signature over `ledger_sha256`; a `previous_ledger_sha256` chain across runs. Retention is policy, not format. |
| 8 | **G6 Performance with intervals** | The texts require performance metrics with confidence intervals, and validation data independent of training and study data. | FDA AI (IV.A.4), EU AI Act Art. 13(3)(b)(ii), PROCOVA (Q5) | `calibration`: metric (ECE, Brier), point estimate, interval, n, the regime it was fit in, and `calibration_data_sha256`. The verifier checks that this hash differs from `report.data_sha256`. |
| 9 | **G8 Multiplicity** | The texts require documenting every data source accessed and every analysis run, including exploratory and discarded ones. | FDA ECT (fn 18), FDA RWD/RWE 2023 (III.B.2) | Covered by the run chain (G7) plus `analysis_status` (G1). |
| 10 | **G10 Tool lifecycle** | The texts require version history and documentation of changes over the lifecycle. | FDA AI (IV.B), EU AI Act Annex IV 1(a), 6 | A CHANGELOG for the format and engines. This is a release-process item, not a ledger field. |

**What the ledger already meets.** Ranked by how many texts it serves and how directly:

1. **Traceability of each conclusion to its evidence.**
   - What the texts require:
     - "fully traceable" documentation (EMA 2.5.1);
     - recording the reasons for analytical choices so that each step can be verified (FDA-EMA principle 6);
     - traceability of outputs (EU AI Act Art. 12(2)).
   - What records it:
     - `claims.evidence` and `claims.licensed_by`, with V2 closure;
     - `report.ledger_sha256`.
2. **A justified causal diagram, edge by edge.**
   - What the texts require:
     - a causal diagram in the protocol (FDA non-interventional III.C; FDA devices VII.B);
     - justification of every omitted arc (Tennant rec. 5). Only 6% of the DAG papers Tennant reviewed cited sources
       for their arcs, and none tested the DAG against the data.
   - What records it:
     - every pair is a claim with `relation`, `direction_source`, `licensed_by` and evidence ids;
     - absent edges cite the separating test (`evidence.supports = nonadjacent`, `evidence.conditioning`).
3. **Reproducibility identifiers.**
   - What the texts require:
     - enough to replicate the analysis (FDA RWD/RWE III.B.3);
     - version tracking and the sources of pre-trained models (FDA AI IV.A.4.a.iii);
     - frozen models (EMA 2.3.3.3).
   - What records it:
     - `evidence.engine` (name, version, wheel hash);
     - `evidence.seed` and `report.seeds`;
     - `evidence.data_sha256`;
     - `knowledge.supplier.model_id` and `prompt_sha256`.
4. **Separation and attribution of LLM or human input.**
   - What the texts require:
     - human review of generative output (EMA 2.3.5);
     - SR 26-2's exclusion of generative AI, which means the bank must be able to tell the in-scope model apart from
       the out-of-scope LLM;
     - naming third-party pre-trained models (Annex IV 2(a)).
   - What records it:
     - `knowledge.supplier` (type, model_id, prompt hash, `shown`);
     - `direction_source` = knowledge;
     - V3, which ensures knowledge never creates an edge.
5. **Interpretation aids and a data-only floor.**
   - What the texts require:
     - information for interpreting outputs and limits (EU AI Act Art. 13(3)(b)(iv), (vii));
     - awareness of automation bias and of limits (Art. 14(4)(a), (b));
     - an ML component whose inferential guarantee does not depend on model quality (PROCOVA Q6).
   - What records it:
     - `claims.data_only_relation`;
     - `report.unverifiable`;
     - V8, the floor check.

## Recommended venue: W3C AI Computed Provenance Community Group

- **Proposal.** Propose a **causal-claim profile** to the
  [W3C AI Computed Provenance Community Group](https://www.w3.org/community/ai-computed-provenance/). The profile has
  three parts:
  - the PROV-O mapping in DESIGN.md section 4, with `licensed_by` expressed as a `prov:Plan` through
    `prov:qualifiedAssociation`/`prov:hadPlan`;
  - a small extension vocabulary for `direction_source`, `data_only_relation` and `confidence`, which PROV-O cannot
    express;
  - V1-V8 as a conformance test.
- **Why this group:**
  - **Scope match.** The group was proposed on 11 Aug 2026 to build provenance for AI-assisted science, on the principle
    that a computed result differs from an asserted one. That is the ledger's thesis: a direction must name its source,
    and LLM knowledge is recorded as asserted input, never as a computed result.
  - **Deliverable match.** The group's stated deliverables are a reference specification and a conformance test suite.
    `verify.py` is already a conformance checker.
  - **Low cost.** Community groups are free, need no W3C membership, and produce reports with royalty-free commitments.
    A student team can join this month.
  - **Timing.** With 14 participants, no visible drafts and an unsettled chair, an early, concrete contribution can shape
    the specification instead of conforming to it.
- **Risks:**
  - The group is two months old and may stall.
  - Its page does not mention PROV-O.
  - Community groups do not produce W3C standards.
- **Fallback.** If the group stalls, self-propose a "Causal Claims" community group, which needs only a short scope
  statement and supporters, and publish the same profile as a Community Group Report.
- **Venues considered and ranked lower:**
  - OHDSI: right audience for data lineage, but it has no causal-discovery workgroup, and its result schemas are not on
    its 2025 agenda.
  - EQUATOR: a TARGET or STROBE extension for machine-discovered DAGs is open territory, but it needs a Delphi process.
  - Pistoia LLM project: needs sponsorship, and its page does not mention provenance.
  - ISO/IEC SC 42 and IEEE: entry is through national bodies or a PAR; the texts are paywalled.

## What this changes

1. **DESIGN.md gets a section 6, "Regulatory fields (v0.2)".** It adds `plan` with `deviations[]` and
   `analysis_status` (G1), `assumptions[]` and `sensitivity[]` (G5), `data_lineage` by pointer (G3), `reviews[]` (G4),
   `question` and `context_of_use` (G2), and `derived[]` (G9).
   - Each is append-only, so the binding-time rule still holds.
   - New verifier checks: claims match the plan hash (G1); every assumption names its dependent claims (G5); the
     calibration data hash differs from the analysis data hash (G6); a review never mutates a claim (G4).
2. **The PROCOVA framing is restated.** EMA accepted ML because type I error, bias and coverage are independent of
   model quality, and because the model was **prespecified and fixed before unblinding**.
   - Our floor (V3, V8) matches the first condition for the skeleton only.
   - The second condition needs G1.
   - Until G1 exists, project text should say that the ledger "records" the knowledge supplied, not that the knowledge
     was "fixed before the data were seen".
3. **No regulator asks for per-edge provenance by name.** FDA asks for a causal diagram with stated assumptions. The
   FDA-EMA principles ask that each step can be traced and verified (paraphrase). Tennant shows that published DAGs almost never justify
   their arcs.
   - The pitch should therefore say that the ledger makes the required diagram verifiable edge by edge.
   - It should not say that the ledger meets a per-edge requirement.
4. **The SR 26-2 positioning becomes concrete.** The deterministic engine is a "model" that bank validators know how to
   review. The LLM is out of scope, and the ledger already records it as typed input (`supplier.type = model`). This
   split is the sales argument for banking.
5. **The EU AI Act is not a near-term driver for the capstone.** The research exclusion applies, and the Annex III
   duties start 2 Dec 2027. Arts. 12-14 stay as design targets, and G4 and G7 are the parts they add.
6. **The `prov_export.py` work moves up.** It is the deliverable for the recommended venue. It needs the small extension
   vocabulary, because PROV-O has no concept of confidence or of a rule.

## Unread

- **EU AI Act full text on EUR-Lex (HTML and PDF)**: fetch returned only the recitals (HTML truncated near recital 60, PDF near recital 62); articles were read on the Commission's AI Act Service Desk (consolidated as at 2026-07-27, marked non-binding display) instead. <https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689>
- **Digital Omnibus on AI as published in the Official Journal**: only the Council press release (final approval 2026-06-29) and the Service Desk's amended Art. 113 were read; OJ text not located. <https://www.consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/>
- **SR 11-7 attachment PDF**: fetch error; the SR 11-7 HTML letter page was read instead. <https://www.federalreserve.gov/supervisionreg/srletters/sr1107a1.pdf>
- **Tennant et al. 2021 on PMC**: reCAPTCHA block; read the White Rose repository PDF of the same article instead. <https://pmc.ncbi.nlm.nih.gov/articles/PMC8128477>
- **Poppe et al., How to develop causal DAGs for observational health research: a scoping review**: reCAPTCHA block. <https://pmc.ncbi.nlm.nih.gov/articles/PMC11875439>
- **Feeney, Hartwig and Davies, How to use DAGs: a guide for clinical researchers (BMJ 2025;388:e078226)**: only the repository landing page read; it is a tutorial, not a reporting guideline. <https://discovery.ucl.ac.uk/id/eprint/10193453>
- **ROBINS-E full paper and tool**: only the abstract record read; domain names are second-hand. <https://doaj.org/article/22d2860aab144282bee9e601f7fc66c3>
- **TARGET in JAMA and the editable checklist**: read the BMJ version instead. <https://jamanetwork.com/journals/jama/fullarticle/2837724>
- **ISO/IEC 42001:2023 and ISO/IEC 5338:2023 full texts**: paywalled; only catalogue pages (scope, dates) read; Annex A controls not read. <https://www.iso.org/standard/42001>
- **IEEE 7001-2021 full text**: only the catalogue page read. <https://standards.ieee.org/ieee/7001/6929/>
- **FDA device RWE guidance Appendix A**: fetch truncated before Appendix A. <https://www.fda.gov/media/190201/download>
- **FDA Data Standards for submissions containing RWD (2023) and FDA Registries guidance (2023)**: not fetched in this round. <https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence>
- **FDA draft Demonstrating Substantial Evidence of Effectiveness (file dated 2026-05-29)**: seen in search results only. <https://www.fda.gov/media/133660/download>
- **EMA reflection paper on RWD in non-interventional studies**: not fetched in this round (covered second-hand in AU5/AU8). <https://www.ema.europa.eu/>
- **W3C AI Computed Provenance CG GitHub repository and the remaining third of the W3C CG list page**: repository not opened; list page read to 100,000 characters only. <https://www.w3.org/groups/cg/>
- **Summarised, not verbatim:** every 'read (primary)' row was read through a summarising fetch tool; quote nothing from this file without checking the PDF.

## Searches run

- FDA real-world evidence guidance 2025 final guidance drug biological products (fda.gov)
- FDA final guidance artificial intelligence regulatory decision-making drug biological products credibility 2026 (fda.gov)
- FDA EMA guiding principles good AI practice drug development January 2026 (fda.gov, ema.europa.eu)
- EMA qualification opinion prognostic covariate adjustment PROCOVA (ema.europa.eu)
- AI Act Service Desk Article 12 record-keeping (europa.eu)
- Digital Omnibus on AI adopted Official Journal 2026 high-risk application postponed December 2027 (europa.eu)
- SR 26-2 model risk management supervisory guidance Federal Reserve 2026 (federalreserve.gov, occ.gov, fdic.gov)
- TARGET guideline transparent reporting of observational studies emulating a target trial 2025 BMJ JAMA
- reporting directed acyclic graphs recommendations epidemiology 2024 2025 checklist
- STROBE-DAG OR DAG reporting guideline consensus 2025 Delphi directed acyclic graphs reporting items
- Poppe Steen Loh directed acyclic graphs observational health research scoping review
- RECORD-PE checklist pharmacoepidemiology BMJ 2018
- ROBINS-E tool risk of bias non-randomized studies of exposures 2024
- IEEE 7001-2021 transparency of autonomous systems standard (ieee.org)
- OHDSI workgroup causal inference OR causal discovery OR evidence network 2025 (ohdsi.org, github.com)
- W3C community group provenance causal claims OR nanopublication OR AI provenance (w3.org)
- AI Computed Provenance Community Group W3C (w3.org)
- Pistoia Alliance project AI provenance OR causal OR FAIR OR large language models 2025 2026 (pistoiaalliance.org)
