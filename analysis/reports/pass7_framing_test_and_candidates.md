# Pass 7 (draft for the decision gate): testing the working hypothesis, and candidate research questions

> **Verification update (2026-10-10, REP-13).** The 9 literature claims in this file were re-read in their primary sources: 7 confirmed, 2 corrected (`analysis/literature/bnd02/rep13_claims.md`). Corrections, which supersede the text:
> - **L69** (s3 L5): Claim holds but has no citation; add Tam et al. 2408.02442 (NL-to-Format two-step keeps natural-language performance).
> - **L71** (s3; pass7_framing_test_and_candidates.md L6): Both have a data veto. Symbolic (argument-level) traceability is a property of Li and Russo's ABA; MosaCD's method as read describes none. Attribute traceability to Li and Russo only.


This file does not choose a capstone direction. It sets out what the evidence supports, where the working hypothesis fails or needs narrowing, and three candidate questions with what would falsify each. The choice is Uzair's, with Prof. Huang. The live repeats of pass 4b are now in (`pass4b_results.md`); section 9 says what they change.

## 1. The hypothesis as stated

Semantic context that an LLM supplies should be inferred once, written down as an explicit typed artifact, and everything downstream should be deterministic processing of that artifact. The expected gain is reliability and auditability. Held as a hypothesis to be challenged.

## 2. Evidence for

- E1 (CODE VERIFIED, seen live). Causal-Copilot's final graph is one integer matrix. An edge the LLM asserted is stored exactly like an edge the algorithm found. In the sachs run all six final edges were written by the LLM and nothing in the saved state says so. Reconstructing that fact needed an external recorder and a replay tool.
- E2 (CODE VERIFIED, seen live). The elicited domain knowledge is free text that is pasted into four later prompts. It carried the dataset's identity ("Sachs dataset") into the algorithm choice, the hyperparameter choice and the edge review. The LLM's proposed background knowledge (five required edges) was dropped without a trace by a key filter.
- E3 (demonstrated). The record the hypothesis asks for can be built for this system: `lineage.py` attributes every final mark to a step and its evidence, and its gates B and C show the attribution reproduces the run's intermediate graphs exactly.
- E4 (literature, verified). Zheng et al. state the same principle ("provenance is not bookkeeping; it is part of what a graph mark means") and list the audit trail as unbuilt future work.
- E5 (literature). The logical point has a precise standard form: recording "the LLM asserted X -> Y" does not assert "X -> Y" (RDF reification). Causal-Copilot collapses the two.

## 3. Evidence against, or limits

- L1 (measured here). The largest measured damage so far comes from a deterministic step, not from the LLM. The bootstrap edit rule deletes stably present non-directed edges: adjacency F1 fell in 50 of 51 equivalence-class cases in every seed. An explicit artifact processed deterministically is no better than its processing rules. "Deterministic downstream" is not a reliability property by itself; the rules have to respect what the marks mean.
- L2 (literature, strong). Verification is relative to the artifact. Translate-then-solve systems give guarantees conditional on a faithful translation, and the faithfulness gap is measured at 3 to 29 points even when the formal check passes. There is no deterministic oracle for "the artifact says what the model meant", and none for "what the model meant is true".
- L3 (literature, and to be measured in pass 4b). "Infer once" freezes one draw. Hosted models are not repeatable at temperature 0, and the reported gains of the systems closest to the hypothesis depend on several samples and agreement between them. The better-calibrated confidence signal for edge judgements is agreement across prompts, which needs more than one inference.
- L4 (theory). No record makes an unidentifiable orientation identifiable. A provenance record shows which assumption or source carried an orientation; it does not validate it.
- L5 (literature). Forcing judgement into a schema at generation time can degrade the judgement; the working pattern is free-form reasoning first, structuring second.
- L6 (novelty). A typed per-pair representation with separate existence and orientation channels exists (Kitson and Constantinou 2026). The principle exists (Zheng et al. 2026). Data veto and abstention exist for DAG and CPDAG outputs (Li and Russo 2026; MosaCD 2025).
- L7 (wording). "Intensional to extensional" will be read by a philosophically literate audience in a different sense from the one intended. "Reification with provenance" is accurate and standard.

## 4. Where that leaves the hypothesis (INFERENCE)

It survives in a narrower, conditional form:

> An elicited judgement can be reified with provenance so that every later transformation of the graph is explicit, replayable and attributable. That gives auditability and reproducibility. Correctness of an edge still depends on three things the record does not supply, each needing its own test: faithfulness of the record to the judgement, calibration of the judgement, and identifiability of the claim.

Two things the original wording missed and the evidence adds: the deterministic rules need the same scrutiny as the LLM (L1), and one inference is a weaker basis than agreement across several (L3).

## 5. Candidate research questions

Common evaluation frame for all three (taken from what the literature leaves open, pass 6 section 3): score three layers separately (algorithm output, after bootstrap filtering, after LLM review); report adjacency and orientation separately; at least 5 repeats with spread; original, neutral and swapped names on the same numbers; include data with ground truth where names carry no meaning.

### RQ-A. What does each refinement step of a deployed causal agent do to the graph? (characterise)

- Hypotheses. A1: for algorithms that return equivalence classes, the bootstrap step lowers adjacency recall. A2: the LLM review's contribution to accuracy on a famous benchmark shrinks or reverses when the names are neutralised or swapped. A3: the final graph differs between repeated runs mainly through the LLM's choices.
- Falsified if. A1: equivalence-class outputs survive the step as well as directed ones. A2: LLM-set edges follow the data, not the labels, in the swapped-name arm. A3: repeats agree.
- Status. A1 is already supported offline (zero API cost) and seen in two live runs; A2 and A3 are exactly what pass 4b measures.
- Baselines. The algorithm's own output; the repo's refinement; the repo's refinement with the LLM step skipped.
- Novelty risk. Low for the audit itself (no published ablation of this stage was found, in an incomplete search); the general phenomena are known.
- Sensitivity. This is a critical audit of the mentor's system. It should be framed as building the audit trail that the field's own position paper asks for, and the question "what produced Table 2, and was refinement on" should go to the authors before anything is written up.

### RQ-B. How should bootstrap results over CPDAG and PAG marks be turned into per-edge decisions? (method, no LLM needed)

- Idea. Keep two quantities per pair: how often the pair is adjacent, and the distribution over mark types given adjacency. Decide adjacency from the first, orientation from the second, and leave a mark undetermined when the second is flat.
- Hypothesis. A type-preserving rule is at least as accurate as Causal-Copilot's rule on every algorithm family and strictly better on equivalence-class outputs, with no loss on fully directed outputs; and its adjacency confidence is better calibrated than the directed-only frequency.
- Falsified if. The repo's rule matches or beats it on adjacency F1 and distance to the true CPDAG across families, or calibration is no better.
- Baselines. The repo's rule; bnlearn's strength and direction; Tetrad's highest-type and majority ensembles; Debeire et al.'s vote.
- Metrics. Adjacency precision, recall, F1; orientation accuracy given adjacency; distance to the true CPDAG or PAG; Brier score and calibration error of the adjacency confidence; behaviour as the number of resamples grows from 20.
- Novelty risk. For CPDAGs this is established practice (bnlearn), so the CPDAG part is replication. For PAG marks the search found no peer-reviewed rule with guarantees and no calibration study of orientation; that part is open, and also harder.
- Cost. Runs entirely offline on recorded resamples.

### RQ-C. Can an LLM's judgement be used without letting it assert edges? (method, needs live runs)

- Idea. Data decide existence. The LLM is consulted only on pairs the data leave adjacent but unoriented, its answer is taken only when several differently worded queries agree, and each accepted orientation is stored as a separate, attributed record that later steps can read but that is never merged into the data's marks.
- Hypothesis. Compared with the repo's ungated review, the gated use has a lower false causal assertion rate and equal or better orientation accuracy on neutral-name and swapped-name data and on graphs the model cannot have memorised; on the original Sachs names the ungated review may look better, and the name controls show why.
- Falsified if. Ungated review is at least as accurate under the name controls, or agreement across prompts does not separate right from wrong orientations.
- Baselines. Algorithm output; repo refinement; LLM-only pairwise; if feasible, Kitson and Constantinou's fusion.
- Metrics. False causal assertion rate split by what the pair truly is (reversed, indirect, unrelated); coverage and selective risk for abstention; calibration of the agreement signal; cross-run agreement.
- Novelty risk. High if presented as a new fusion method (several 2025-2026 papers gate or veto LLM input). Lower if presented as the evaluation of gating inside a deployed agent with a per-edge record, which was not found.

### How the three relate to the hypothesis

The reified record is the frame, not a result. A schema cannot be falsified; rules that read it can. RQ-B and RQ-C are two sets of such rules, and RQ-A is the measurement that motivates them.

## 6. A possible split across the two quarters (for discussion, not decided)

- Q1 (replicate and characterise): RQ-A in full, on the unmodified system, with the harness and lineage tools as the reproducible artifact. Reproduce or fail to reproduce the relevant part of the paper's evaluation once the authors say what was scored.
- Q2 (contribution): the edge-evidence record with RQ-B as its first rule set, and RQ-C if time and API budget allow. RQ-B alone is a complete, defensible Q2 if its PAG part is taken seriously.

Alternatives worth weighing: RQ-A plus RQ-C only (more topical, more exposed to prior work and to model drift); RQ-B only as a pure statistics project (cleanest, least connected to agents).

## 7. What is still unknown

- What the paper's Table 2 scored.
- Whether the mentor wants a project that audits Causal-Copilot or one that extends it.
- The course's deliverable requirements beyond the introductory slides.
- The competing proposal's level of concreteness (the WorldReset document has not been provided).

## 8. DECISIONS

None on direction.

Recommendation on wording, for Uzair to accept or reject: say "reify with provenance" where the earlier drafts said "extensionalize".

## 9. Addendum after pass 4b (2026-10-06)

- RQ-A's three hypotheses now have live evidence on one dataset and one model. A1 (the bootstrap step lowers adjacency recall for equivalence-class outputs): supported, 15% of non-directed edges survived. A2 (the LLM review's contribution depends on the names): supported; final adjacency F1 on identical numbers and an identical neutral file path was 0.44 with the real names, 0.10 with neutral names and 0.01 with swapped names. A3 (runs differ mainly through the LLM): partly; algorithm and hyperparameter choice never varied, the variation came from the LLM's edge answers and from a randomised independence test.
- Consequence for the candidates. RQ-A is no longer an open question on Sachs with gpt-4o; as a capstone component it would need breadth (more datasets with meaningful names, a memorisation-resistant set, more than one model). RQ-C's premise is strengthened: an ungated LLM review writes edges from names regardless of data, so the comparison with a gated, attributed use is well motivated. RQ-B is unaffected and still the cheapest to run.
- Evidence for the limits in section 3: L3 is now measured (one identical request, three different answers, two of them crashing the run).
- Still no decision on direction.
