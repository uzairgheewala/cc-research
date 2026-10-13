# Precedents, terminology and known limits for "compile semantic context into an explicit IR, then process deterministically"

## Where we are now

I located and read 22 core works plus 21 supporting sources in this session, each with a working URL. The literature supports a narrower hypothesis than the student's. Translate-then-solve gives guarantees that are **conditional on the translation being faithful**, and the 2024-2026 work measures that faithfulness gap directly. "Intensional -> extensional" is not the standard description of what he means. "Reification" is the most defensible of his own terms.

**Reliability of this report**
- Every page was read through a fetch tool that summarises with a small model. Quotes are as the tool returned them. Re-check any quote against the source before it goes into a mentor document.
- "Abstract-level read" means I did not read the full text.
- One page could not be read: `arxiv.org/pdf/2403.18120` (full text of "Don't Trust: Verify") was refused by the fetch proxy with HTTP 429 (rate limit). I did not retry. That work is covered from its ICLR abstract page only.
- Other blocked pages: ACM DL (403), PubMed (captcha), MIT Press and dblp (robots.txt), PhilPapers (403), export.arxiv.org (robots.txt).

---

## A. Core works (22)

### Terminology and philosophy

**1. Fitting, M. "Intensional Logic." Stanford Encyclopedia of Philosophy (first published 2006, substantive revision 2015).** https://plato.stanford.edu/entries/logic-intensional/
1. Claim: meanings are "intensions" and things designated are "extensions". Contexts "in which extension is all that matters" are extensional; those where "extension is not enough" are intensional (substitution of co-designating terms fails).
2. IR: Frege's sense/reference; Carnap's intension as "an assignment of an extension ... to each state-description".
3. Lost: an extension is one value of the intension at one state. Going from intension to extension discards how the value varies across states.
4. Guarantees: substitutivity holds only in extensional contexts.
5. Evaluation: encyclopedia survey, not empirical.
6. Implication: **limit on the wording.** In the standard sense, "extensionalizing" means evaluating at a fixed state. That fits "freeze one LLM judgement" loosely, but it says nothing about evidence or provenance.

**2. Kemp, G. "Willard Van Orman Quine." SEP (2010, rev. 2023).** https://plato.stanford.edu/entries/quine/
1. Claim: Quine's regimentation: "Paraphrasing a theory into classical logic imposes extensionality on it." Attitude attributions "violate extensionality" (Tom's believing the Dean sings well vs. Mary sings well).
2. IR: canonical first-order extensional notation.
3. Lost: whatever cannot be paraphrased (meanings, propositions, modality) is excluded from the regimented theory, not translated.
4. Guarantees: substitution of co-extensive predicates preserves truth value, but only inside the regimented fragment.
5. Evaluation: philosophical argument.
6. Implication: **closest philosophical precedent, and a warning.** Regimentation is lossy by design. The phrase "referentially opaque" was not confirmed verbatim in any page I fetched. The substitution-failure phenomenon is covered here and in S1 below.

**3. Hayes, P. J. and Patel-Schneider, P. F. (eds.) "RDF 1.1 Semantics." W3C Recommendation, 25 Feb 2014.** https://www.w3.org/TR/rdf11-semantics/
1. Claim: the reification vocabulary (rdf:Statement, rdf:subject, rdf:predicate, rdf:object) describes a triple as an object.
2. IR: a reified statement node that can carry provenance.
3. Lost: truth commitment. "A reification of a triple does not entail the triple, and is not entailed by it."
4. Guarantees: none about truth. The reification "only says that the triple token exists and what it is about". Provenance properties attach to a token, "a concrete realization", not the abstract triple.
5. Evaluation: normative specification.
6. Implication: **support, with a precise semantics.** "The LLM proposed X -> Y on evidence E" and "X -> Y" are logically independent statements. Causal-Copilot currently collapses the two.

### Translate-then-solve systems

**4. Wu, Jiang, Li, Rabe, Staats, Jamnik, Szegedy. "Autoformalization with Large Language Models." arXiv 2205.12615 (NeurIPS 2022 per the proceedings listing).** https://arxiv.org/abs/2205.12615
1. Builds: LLM translation of competition mathematics into Isabelle/HOL.
2. IR: Isabelle/HOL statements.
3. Lost: failure analysis lists definition/concept misalignment (46 cases), wrong function application (35), inconsistent or missing assumptions (26), and concepts with no library definition (15).
4. Guarantees: none on the translation. Proof checking covers only the formal statement.
5. Evaluation: manual inspection of 150 problems, 38 perfect ("25.3%"). MiniF2F proof rate rose from 29.6% to 35.2%.
6. Implication: **limit.** The term "autoformalization" comes from this line of work. The early base rate of faithful translation was about one in four.

**5. Pan, Albalak, Wang, Wang. "Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning." Findings of EMNLP 2023.** https://arxiv.org/abs/2305.12295
1. Builds: the LLM formulates and "a deterministic symbolic solver performs inference". A self-refiner uses solver error messages.
2. IR: logic programs (Pyke), FOL (Prover9), CSP (python-constraint), SAT (Z3).
3. Lost: "the model's applicability is inherently bounded by the expressiveness of the symbolic solver".
4. Guarantees: solver inference is deterministic. But "a valid symbolic representation does not necessarily equate to a 'correct' problem formulation". Non-executable cases silently fall back to chain-of-thought.
5. Evaluation: five datasets, +39.2% over standard prompting, +18.4% over CoT. GPT-4 executable rate: near 100% on synthetic sets, 79.9% on FOLIO, 32.6% on AR-LSAT.
6. Implication: **support in closed synthetic worlds, limit on realistic text.** The refinement loop repairs syntax, not meaning.

**6. Olausson, Gu, Lipkin, Zhang, Solar-Lezama, Tenenbaum, Levy. "LINC: A Neurosymbolic Approach for Logical Reasoning by Combining Language Models with First-Order Logic Provers." EMNLP 2023 (Outstanding Paper).** https://arxiv.org/abs/2310.15164
1. Builds: the LLM "acts as a semantic parser" to FOL and Prover9 does the deduction.
2. IR: first-order logic.
3. Lost, as named failure modes:
   - L1: implicit information "not explicitly listed in the premises".
   - L2: information lost through representation choices (one symbol for "Nazi German politician").
   - L3: syntax errors (38% StarCoder+, 24% GPT-3.5, 13% GPT-4).
   - L4: mistranslation.
4. Guarantees: prover soundness over the parsed formulas. Syntax errors surface as exceptions or Uncertain. L1 and L2 errors are silent.
5. Evaluation: FOLIO and balanced ProofWriter, three models, K=10 majority voting. GPT-4 + LINC scored +26% over CoT on ProofWriter and was comparable on FOLIO.
6. Implication: **the clearest named taxonomy of what stays implicit.** The reported gains depend on K=10 samples, which is not "infer once".

**7. Ye, Chen, Dillig, Durrett. "SatLM: Satisfiability-Aided Language Models Using Declarative Prompting." NeurIPS 2023.** https://arxiv.org/abs/2305.09656
1. Builds: the LLM writes a declarative specification and an automated theorem prover derives the answer.
2. IR: SAT/SMT constraints.
3. Lost: parsing errors yield conflicting or under-constrained specifications. Not all theories are easily encoded.
4. Guarantees: correctness "with respect to the parsed specification". The solver also returns ERROR / UNSAT / AMBIG, which enables abstention.
5. Evaluation: 8 datasets. +23% over program-aided LMs on a hard GSM subset. Selective accuracy 77% vs 45% on GSM-SYS at lower coverage.
6. Implication: **best statement of the conditional guarantee.** A declarative IR close to the problem text parses more accurately, and solver status doubles as an uncertainty signal.

**8. Lyu, Havaldar, Stein, Zhang, Rao, Wong, Apidianaki, Callison-Burch. "Faithful Chain-of-Thought Reasoning." IJCNLP-AACL 2023.** https://arxiv.org/abs/2301.13379
1. Builds: Translation (NL -> symbolic chain) then Problem Solving (deterministic solver).
2. IR: Python, Datalog, PDDL, relational expressions.
3. Lost: "the Translation stage is still opaque". Errors include wrong sub-questions (49% of GSM8K errors) and inverted relations (41% on CLUTRR).
4. Guarantees: the reasoning chain is faithful by construction to the answer. Faithfulness is distinguished from plausibility. Nothing is guaranteed about the translation.
5. Evaluation: better than CoT on 9 of 10 benchmarks, plus human evaluation of chains.
6. Implication: **support for auditability of the solve step.** The guarantee stops at the stage boundary.

**9. Gao, Madaan, Zhou, Alon, Liu, Yang, Callan, Neubig. "PAL: Program-aided Language Models." arXiv 2211.10435 (ICML 2023, PMLR 202 per the proceedings listing).** https://arxiv.org/abs/2211.10435
1. Builds: the LLM writes programs as intermediate steps and "solving is delegated to the interpreter".
2. IR: Python.
3. Lost: decomposition errors remain. Only arithmetic and execution errors are removed.
4. Guarantees: deterministic execution of whatever program was written.
5. Evaluation: 13 tasks. +15% absolute on GSM8K over PaLM-540B with CoT.
6. Implication: **support for the division of labour.** The same pattern appears in Program of Thoughts (Chen, Ma, Wang, Cohen, TMLR 2023, https://arxiv.org/abs/2211.12588), with about 12% average gain over CoT.

**10. Kambhampati, Valmeekam, Guan, Verma, Stechly, Bhambri, Saldyt, Murthy. "LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks." ICML 2024, PMLR 235.** https://arxiv.org/abs/2402.01817
1. Claim: LLMs cannot plan or self-verify. Using them as "glorified translators" in a "unidirectional pipeline" is too narrow. The proposal is generate-test with external critics in a "bi-directional interaction regime".
2. IR: candidate plans plus critic models such as PDDL.
3. Lost or implicit: the verifier's domain model must itself be acquired, "with the help of human expert curation".
4. Guarantees: "soundness guarantees because of the external sound critics". LLMs "cannot take on the role of hard critics" and may only approximate soft or style critics.
5. Evaluation: position paper citing prior planning and graph-colouring verification studies.
6. Implication: **counter to the one-shot shape, support for independent verification.** An LLM check on the artifact does not count as verification.

### Typed interfaces and their limits

**11. "DSPy Assertions: Computational Constraints for Self-Refining Language Model Pipelines." arXiv 2312.13382.** https://arxiv.org/abs/2312.13382 (first authors listed as Arnav, Manish, Shangyin with equal contribution; submitted by Omar Khattab; full author list unverified)
1. Builds: "LM Assertions", constraints the LM output must satisfy, with retry and self-refinement.
2. IR: programmatic assertions over module outputs.
3. Lost: only what is expressible as a computable predicate is checked.
4. Guarantees: constraint compliance when the assertion passes. Nothing semantic.
5. Evaluation: four text-generation case studies. Constraints passed "up to 164% more often", "up to 37% more higher-quality responses". Abstract-level read.
6. Implication: **support for typed validation as an engineering pattern.** The mechanism is retry, so it is not single-inference.

**12. Tam, Wu, Tsai, Lin, Lee, Chen. "Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models." arXiv 2408.02442 (venue unverified).** https://arxiv.org/abs/2408.02442
1. Claim: "a significant decline in LLMs reasoning abilities under format restrictions".
2. IR: JSON / XML / YAML via JSON-mode or format instructions.
3. Lost: reasoning quality when generation is forced into the schema.
4. Guarantees: none. The mitigation is "NL-to-Format": reason in free text, then convert.
5. Evaluation: 3 reasoning and 4 classification datasets, several models. GSM8K with GPT-3.5-Turbo fell from about 76% to about 49% in JSON-mode. Some classification tasks improved.
6. Implication: **counterexample to "have the LLM emit the typed record directly".** The typed artifact should be a second step after free-form reasoning.

**13. Park, Wang, Berg-Kirkpatrick, Polikarpova, D'Antoni. "Grammar-Aligned Decoding." NeurIPS 2024.** https://arxiv.org/abs/2405.21047
1. Claim: grammar-constrained decoding "can distort the model's probability distribution", giving grammatical but lower-quality outputs. The ASAp algorithm corrects this.
2. IR: grammar-constrained output.
3. Lost: fidelity to the model's own conditional distribution.
4. Guarantees: ASAp output is grammatical and provably matches the LLM's distribution conditioned on the grammar. This is a limiting, sampling-based property.
5. Evaluation: code generation and structured NLP tasks. Abstract-level read.
6. Implication: **limit.** A schema guarantee is syntactic, and enforcing it can change which judgement gets recorded.

### Measured faithfulness gap

**14. Zhang, Gallardo Candela, Murthy, Xie, Wang, Raissi. "Beyond Compilation: Evaluating Faithful Natural-Language-to-Lean Statement Formalization." arXiv 2606.31002 (2026 preprint; exact date unverified).** https://www.alphaxiv.org/abs/2606.31002
1. Claim: "Lean verifies that a generated declaration is well typed, but not that it expresses the statement a user intended."
2. IR: Lean 4 statements.
3. Lost: semantic drift that survives compilation.
4. Guarantees: none. LLM judging is "not ... an equivalence oracle". It agreed with the human majority on 89.7% of an audited sample.
5. Evaluation: 8 systems, 400 graduate-level statements. The compile-faithfulness gap was 3.0 to 29.0 points. The largest was 89.5% compiled vs 60.5% faithful.
6. Implication: **strongest direct counter-evidence.** Passing the deterministic check overstates faithfulness in every system tested. Abstract-level read.

**15. Kim, Poiroux, Bosselut (EPFL). "Do LLMs Game Formalization? Evaluating Faithfulness in Logical Reasoning." arXiv 2604.19459 (2026; venue unverified).** https://arxiv.org/abs/2604.19459
1. Claim: "Formal verification guarantees proof validity but not formalization faithfulness."
2. IR: Lean 4 axiom systems built from natural-language premises.
3. Lost: premises mistranslated or fabricated. In a two-stage (formalize, then prove) pipeline, GPT-5 fabricated axioms in 107 cases (59 as "conclusion as axiom").
4. Guarantees: proof validity only.
5. Evaluation: FOLIO and Multi-LogiEval. Compilation 87-99%. 29 of 124 prediction errors were unfaithful formalizations. Two-stage accuracy was 59-76%, below unified generation.
6. Implication: **counterexample to naive stage separation.** Locking the formalization and then demanding a proof induced the model to invent support. Checking must cover the artifact, not only the derivation.

**16. Ganguly, Singh, Sankar, Zhang, Zhang, Iyengar, Han, Sharma, Kalyanaraman, Chaudhary. "Grammars of Formal Uncertainty: When to Trust LLMs in Automated Reasoning Tasks." NeurIPS 2025.** https://proceedings.neurips.cc/paper_files/paper/2025/hash/30ff6279fb18304d3eac481970157430-Abstract-Conference.html
1. Claim: LLMs "remain probabilistic while formal verification requires determinism". Uncertainty of the formal artifact can be quantified with a probabilistic context-free grammar over sampled outputs.
2. IR: SMT programs.
3. Lost: domain dependence. SMT autoformalization improved logical tasks by 34.8% and reduced factual-task accuracy by 44.5%.
4. Guarantees: none absolute. Selective verification cut errors 14-100% "with minimal abstention".
5. Evaluation: five LLMs. Token-probability entropy was ineffective. Grammar entropy reached AUROC > 0.93 on logic.
6. Implication: **support for carrying uncertainty with the artifact, limit on scope.** Formalizing can hurt badly on knowledge-heavy tasks, and causal plausibility judgements are knowledge-heavy. Abstract-level read.

### Nondeterminism and provenance

**17. Atil, Aykent, Chittams, Fu, Passonneau, Radcliffe, Rajagopal, Sloan, Tudrej, Ture, Wu, Xu, Baldwin. "Non-Determinism of 'Deterministic' LLM Settings." arXiv 2408.04667 (ACL Anthology lists a version as 2025.eval4nlp-1.12).** https://arxiv.org/abs/2408.04667
1. Claim: "none of the LLMs consistently delivers repeatable accuracy across all tasks, much less identical output strings" under settings meant to be deterministic.
2. IR: none. It introduces TARr@N (agreement of raw outputs over N runs) and TARa@N (agreement of parsed answers).
3. Lost: not applicable.
4. Guarantees: none. Causes given are serving optimisations such as continuous batching and prefix caching.
5. Evaluation: 5 models, 8 tasks, 10 runs. Accuracy varied up to 15% across runs, with best-to-worst gaps up to 70%.
6. Implication: **supports record-and-replay and undercuts "one call is the judgement".** Parsed answers agree more than raw strings, which is a small point in favour of a typed IR.

**18. Souza, Gueroudji, DeWitt, Rosendo, Ghosal, Ross, Balaprakash, Ferreira da Silva. "PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows." IEEE e-Science 2025.** https://arxiv.org/abs/2508.02866
1. Builds: an extension of W3C PROV for agents, motivated by agents that "hallucinate or reason incorrectly, propagating errors when one agent's output becomes another's input".
2. IR: a provenance graph with AIAgent (subclass of prov:Agent), AgentTool, AIModelInvocation, Prompt, ResponseData and AIModel (name, provider, temperature), linked by used / wasGeneratedBy / wasAttributedTo.
3. Lost: it records what happened, not whether it was right. The implementation records only agent ID and name.
4. Guarantees: traceability and root-cause queries (for example "What was the LLM prompt and response when a surprising agent decision was identified?").
5. Evaluation: one additive-manufacturing workflow across edge, cloud and HPC. Described as "an early step".
6. Implication: **direct support for the provenance half.** It also shows that provenance and correctness are separate properties.

### Claim / evidence representations

**19. Groth, Gibson, Velterop. "The anatomy of a nanopublication." Information Services & Use 30(1-2):51-56, 2010.** https://www.doi.org/10.3233/ISU-2010-0613
1. Claim: nanopublications are "core scientific statements with associated context".
2. IR: named-graph RDF separating the assertion from its provenance and attribution.
3. Lost: the surrounding argument of the source paper.
4. Guarantees: attribution and machine-readability, not truth.
5. Evaluation: model proposal, no empirical evaluation.
6. Implication: **support.** A 16-year-old precedent for one edge as one assertion plus a typed support record.

**20. SCSC Assurance Case Working Group. "Goal Structuring Notation Community Standard, Version 3." SCSC-141C, May 2021.** https://scsc.uk/scsc-141c
1. Claim: GSN is "a graphical argument notation which can be used to document explicitly the elements and structure of an argument and the argument's relationship to evidence".
2. IR: goals (claims) supported by sub-goals and evidence.
3. Lost: element definitions (context, assumption, justification) were not confirmed in my read.
4. Guarantees: structural explicitness only. The argument's soundness is still a human judgement.
5. Evaluation: community standard.
6. Implication: **support for the representation.** Safety engineering treats an explicit claim structure as reviewable, not as verified.

### Causal-discovery precedents closest to the application

**21. Long, Piché, Zantedeschi, Schuster, Drouin. "Causal Discovery with Language Models as Imperfect Experts." ICML 2023 workshop on Structured Probabilistic Inference & Generative Modeling.** https://arxiv.org/abs/2307.02390
1. Builds: an expert that "may provide erroneous information" orients edges inside a Markov equivalence class. Its answers are amended using consistency properties.
2. IR: edge-orientation decisions with a noise model (error probability ε) over the MEC.
3. Lost: the expert's reasons. Only the orientation is used.
4. Guarantees: p(G* in M_E,S) >= 1 - η, conditional on the noise model being right.
5. Evaluation: real-data case study. text-davinci-003 "is often over-confident", and on ALARM the true graph was excluded "even for small tolerance η".
6. Implication: **conditional support and a calibration limit.** The guarantee failed in practice because the LLM's uncertainty was miscalibrated.

**22. Li, Z. and Russo, F. "Leveraging Large Language Models for Causal Discovery: a Constraint-based, Argumentation-driven Approach." UAI 2026, PMLR 337:3631-3667.** https://proceedings.mlr.press/v337/li26e.html
1. Builds: ABAPC-LLM. LLMs act "as imperfect experts, eliciting semantic structural constraints" that are combined with statistical evidence through Causal Assumption-based Argumentation.
2. IR: structural constraints as defeasible assumptions in an argumentation framework.
3. Lost: not established from the abstract.
4. Guarantees: symbolic reasoning "to ensure correspondence between input constraints and output graphs". Described as "principled and conservative".
5. Evaluation: standard small and medium benchmarks, plus new semantically grounded random benchmarks and a protocol "to mitigate memorisation bias".
6. Implication: **nearest existing realisation of the hypothesis in causal discovery.** It is also a prior-art risk for novelty claims. Abstract-level read; the full text should be read before the framing is fixed.

---

## B. Supporting sources (verified; used for definitions and arguments)

**Philosophy and semantics**
- S1. Nelson, "Propositional Attitude Reports", SEP (2000, rev. 2019). Substitution failure in belief contexts and Frege's mode-of-presentation solution. https://plato.stanford.edu/entries/prop-attitude-reports/
- S2. Casati and Varzi, "Events", SEP (2002, rev. 2025). Davidson's analysis: "Brutus stabbed Caesar with a knife" asserts that an event occurred and had a property. The entry does not use the word "reification". https://plato.stanford.edu/entries/events/
- S3. Noy and Rector (eds.), "Defining N-ary Relations on the Semantic Web", W3C Note, 2006. "Ontologically the classes created in this way are often called 'reified relations'", explicitly distinguished from RDF statement reification. https://www.w3.org/TR/swbp-n-aryRelations/
- S4. Shanahan, "The Frame Problem", SEP (2004, rev. 2016). "Anything could be relevant", with "no a priori limits" on what may come into play. https://plato.stanford.edu/entries/frame-problem/
- S5. Turner, "The Philosophy of Computer Science", SEP (2013, rev. 2025). Fetzer 1988: deduction guarantees correctness "with respect to its specifications" only. Smith 1985 is mentioned briefly. https://plato.stanford.edu/entries/computer-science/

**Compilation and structured generation**
- S6. Darwiche and Marquis, "A Knowledge Compilation Map", JAIR 17:229-264, 2002. Compilation languages are compared by succinctness and by which queries and transformations are polytime. https://doi.org/10.1613/jair.989
- S7. Beurer-Kellner, Fischer, Vechev, "Prompting Is Programming" (LMQL), PLDI 2023. https://arxiv.org/abs/2212.06094
- S8. Willard and Louf, "Efficient Guided Generation for Large Language Models" (Outlines). "Guaranteeing the structure of the generated text." https://arxiv.org/abs/2307.09702
- S9. Geng, Josifoski, Peyrard, West, "Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning", EMNLP 2023. https://arxiv.org/abs/2305.13971

**Translate-then-solve and faithfulness**
- S10. Yang et al., "Neuro-Symbolic Artificial Intelligence: Towards Improving the Reasoning Abilities of Large Language Models", IJCAI 2025. Taxonomy: Symbolic->LLM, LLM->Symbolic, LLM+Symbolic. https://www.ijcai.org/proceedings/2025/1195
- S11. Lam, Thatikonda, Shareghi, "A Closer Look at Tool-based Logical Reasoning with LLMs: The Choice of Tool Matters", ALTA 2024. Executable rates vary by "near 50%" across Z3 / Pyke / Prover9. https://aclanthology.org/2024.alta-1.4
- S12. Liu, Zheng, Lu, Cao, Yan, "Rethinking and Improving Autoformalization...", ICLR 2025. The BEq equivalence metric, and the "absence of faithful and universal automated evaluation". https://proceedings.iclr.cc/paper_files/paper/2025/hash/d630537fc4402cfa3ebbc7450a0cac91-Abstract-Conference.html
- S13. Zhou, Staats, Li, Szegedy, Weinberger, Wu, "Don't Trust: Verify", ICLR 2024. Rejects solutions whose formalizations are inconsistent; +12% over majority voting on GSM8K. Abstract only. https://proceedings.iclr.cc/paper_files/paper/2024/hash/0a79ecda13603817de4cdfc68b417e89-Abstract-Conference.html
- S14. Sun, Sheng, Padon, Barrett, "Clover: Closed-Loop Verifiable Code Generation". Three-way consistency among code, docstring and formal annotation; up to 87% acceptance of correct instances with no false positives on its benchmark. https://arxiv.org/abs/2310.17807
- S15. Moore and Shah, "Evaluating Autoformalization Robustness via Semantically Similar Paraphrasing", arXiv 2511.12784 (venue unverified). Paraphrases change formalization outcomes. https://arxiv.org/abs/2511.12784
- S16. Mohammad and Sheikh, "The Faithfulness Gap", arXiv 2606.16541 (2026 preprint, not peer reviewed as far as I could confirm). Typecheck alone detected 41.2% of drifted formalizations on their benchmark. https://www.alphaxiv.org/abs/2606.16541

**Nondeterminism, replay, provenance**
- S17. Yuan et al., "Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference", arXiv 2506.09501 (listed as a NeurIPS 2025 oral in search results). Batch size, GPU count and GPU version change outputs; up to 9% accuracy variation. https://arxiv.org/abs/2506.09501
- S18. Chawla and Koul, "Chronicle: Cut-Point Replay for Regression Testing of LLM Agents", arXiv 2609.20625 (Sept 2026 preprint). Records runs "at its non-deterministic boundaries as immutable envelopes"; full replay is bit-stable. https://arxiv.org/abs/2609.20625 See also Mudasiru, "Deterministic Replay for AI Agent Systems", https://arxiv.org/abs/2607.16200.
- S19. Moreau and Missier (eds.), "PROV-DM: The PROV Data Model", W3C Recommendation, 2013. https://www.w3.org/TR/prov-dm/

**Evidence grading and causal context**
- S20. Guyatt et al., "GRADE: an emerging consensus on rating quality of evidence and strength of recommendations", BMJ 336(7650):924-926, 2008. Separates quality of evidence from strength of recommendation. https://www.bmj.com/content/336/7650/924
- S21. Zečević, Willig, Dhami, Kersting, "Causal Parrots: Large Language Models May Talk Causality But Are Not Causal", TMLR 2023. https://arxiv.org/abs/2308.13067
- Application paper: Wang et al., "Causal-Copilot: An Autonomous Causal Analysis Agent", https://arxiv.org/abs/2504.13263. It states that LLM recommendations "are treated as soft suggestions and are not permitted to override high-confidence decisions". No per-edge provenance mechanism appears in the paper text I read.

Definition sources for section (iv) are cited inline there.

---

## (i) Terminology verdict

"Intensional -> extensional" is not the standard description and will mislead a philosophically literate reader.

- In the standard usage, an intension is a meaning (for Carnap, an assignment of extensions across state-descriptions) and an extension is the thing designated. An "intensional context" is one where substituting co-designating terms can change truth value (Fitting; Nelson).
- The student uses "intensional context" for "background semantic knowledge". That is a different sense.
- The nearest genuine precedent is Quine's **regimentation**, which "imposes extensionality" by paraphrase into first-order notation. Quine regiments by discarding what cannot be paraphrased.
- One accurate link does exist. "The LLM judges that X causes Y" is an attitude report, hence strictly intensional. Recording it as an object without asserting the edge is **reification** in the RDF sense: "a reification of a triple does not entail the triple".

Standard terms by step:
- **Semantic parsing / (auto)formalization**: natural language to formal language.
- **Elicitation** (the LLM as "imperfect expert"): obtaining the judgement.
- **Reification**: making the judgement a first-class object carrying provenance.
- **Knowledge compilation**: offline translation into a target language chosen for which queries become tractable (Darwiche and Marquis). This is narrower than his metaphor.
- **Externalisation / materialisation**: persisting the result.
- **Grounding**: I found no definition supporting its use for this step. I would avoid it.

Recommended phrasing: "elicit once, reify with provenance, then verify". "Reification of context" is defensible. "Extensionalizing" is defensible only as an explicit analogy to Quine.

I found no source for "reification" as a term in ML experiment tracking.

## (ii) Strongest three arguments against the hypothesis

**1. Verification is relative to the artifact, and artifact faithfulness has no deterministic oracle.**
- Stated outright: "Formal verification guarantees proof validity but not formalization faithfulness" (Kim et al. 2026). "Lean verifies that a generated declaration is well typed, but not that it expresses the statement a user intended" (Zhang et al. 2026).
- Measured: compile-faithfulness gaps of 3 to 29 points in all eight systems (Zhang et al.). 25.3% perfect formalizations (Wu et al. 2022). "A valid symbolic representation does not necessarily equate to a 'correct' problem formulation" (Logic-LM).
- The faithfulness check is itself a human or an LLM, "not ... an equivalence oracle" (Zhang et al.).
- The philosophical root is Fetzer's point that deduction guarantees correctness only with respect to specifications (SEP, Turner).
- I found no source using the phrase "garbage in, verified garbage out". The argument is real; the slogan is unsourced.

**2. Decision-relevant context cannot be bounded in advance, and forcing it into the IR degrades the judgement.**
- LINC's dominant failures are L1 (needed information "not explicitly listed in the premises") and L2 (lost through representation choice).
- Logic-LM is "inherently bounded by the expressiveness of the symbolic solver".
- SMT autoformalization reduced factual-task accuracy by 44.5% (Ganguly et al.).
- Format restriction causes "a significant decline in LLMs reasoning abilities" (Tam et al.), and constrained decoding distorts the model's distribution (Park et al.).
- The general form is the frame problem: "anything could be relevant" (SEP, Shanahan).
- Kambhampati et al. add an architectural objection: the unidirectional translate-and-ship pipeline is too weak. What works is iterative generate-test with external critics.

**3. Inferring once freezes a sample; it does not remove the stochasticity or supply the missing warrant.**
- Temperature 0 is not deterministic: "none of the LLMs consistently delivers repeatable accuracy" (Atil et al.). Hardware and batch size alone shift outputs (Yuan et al.). Paraphrasing the input changes the formalization (Moore and Shah).
- The recorded artifact is therefore one draw, and the reported gains in LINC, DTV and Ganguly et al. rely on multiple samples.
- LLM confidence is a poor uncertainty field: "often over-confident" (Long et al.), and token-probability entropy is ineffective (Ganguly et al.).
- LLMs "cannot take on the role of hard critics" (Kambhampati et al.), so a second LLM pass is not independent verification.
- For causal content specifically: "Behind every causal conclusion there must lie some causal assumption that is not testable in observational studies" (Pearl 2009), and LLM causal answers may be recited correlations of causal facts (Zečević et al.). Deterministic downstream processing cannot validate the edge's content.

## (iii) Conditions under which translate-once-then-verify is reported to work

- **Closed world, premises explicit.** Executable rates near 100% on synthetic sets vs 32.6% on AR-LSAT (Logic-LM); L1 failures otherwise (LINC).
- **Target language close to the surface form of the input** and expressive enough. A declarative specification is "closer to the problem description", so the LLM parses it more accurately (SatLM).
- **A sound engine exists for the target language**, and the choice of engine matters (Lam et al.).
- **The engine returns diagnostic status usable for abstention.** ERROR / UNSAT / AMBIG in SatLM; rejection of inconsistent formalizations in DTV.
- **Redundancy.** K-way voting (LINC), verified-only aggregation (DTV), three-way consistency (Clover), strict two-judge consensus plus human audit (Zhang et al.). This is in tension with "once".
- **Task-specific uncertainty signals** for selective verification (Ganguly et al.).
- **Free-form reasoning first, structuring second** (Tam et al.).
- **External sound critics**, with the verifier's model curated by humans up front (Kambhampati et al.).
- **In causal discovery:** an explicit noise model, consistency constraints (acyclicity, MEC membership) and conservative integration (Long et al.; Li and Russo). The guarantee holds only if the assumed error rate is right.
- **For reproducibility:** capture prompt, response, model identity and parameters per invocation (PROV-AGENT) at the non-deterministic boundaries (Chronicle).

## (iv) Separating the eight properties

**Determinism** is a property of a procedure: identical input yields identical output. I found no canonical definition; Atil et al. operationalise it as agreement of raw outputs (TARr@N) or parsed answers (TARa@N) over N runs and show hosted LLMs fail it at temperature 0. **Reproducibility** is "obtaining consistent computational results using the same input data, computational steps, methods, code, and conditions of analysis", distinct from replicability, "consistent results across studies ... each of which has obtained its own data" (National Academies 2019, https://www.nap.edu/catalog/25303/reproducibility-and-replicability-in-science, quoted via https://www.nationalacademies.org/news/2019/05/new-report-examines-reproducibility-and-replicability-in-science-recommends-ways-to-improve-transparency-and-rigor-in-research); replaying a recorded LLM call gives reproducibility without determinism of the model. **Reliability** is the "ability of an item to perform as required, without failure, for a given time interval, under given conditions" (NIST AI RMF 1.0, citing ISO/IEC TS 5723:2022, https://doi.org/10.6028/NIST.AI.100-1); for agents, Yao et al. operationalise it as pass^k over repeated trials (https://arxiv.org/abs/2406.12045), so a replayed record says nothing about it. **Correctness** is always relative to a specification (SEP, Turner, on Fetzer; SatLM's "with respect to the parsed specification"), whereas accuracy is "closeness ... to the true values" (NIST); a deterministic, reproducible pipeline can be consistently incorrect. **Calibration** is "predicting probability estimates representative of the true correctness likelihood" (Guo, Pleiss, Sun, Weinberger, ICML 2017, https://arxiv.org/abs/1706.04599); an uncertainty field in the artifact is useful only if calibrated, and Long et al. found it was not. **Auditability** "enables the assessment of algorithms, data and design processes" (EU High-Level Expert Group on AI, Ethics Guidelines for Trustworthy AI, 2019, https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai), and provenance is "information about entities, activities, and people involved in producing a piece of data or thing, which can be used to form assessments about its quality, reliability or trustworthiness" (PROV-DM); it lets someone check, and does not perform the check. **Interpretability** "refers to the meaning of AI systems' output in the context of their designed functional purposes", distinct from explainability, "a representation of the mechanisms underlying AI systems' operation" (NIST); Lipton calls the notion "underspecified" (https://arxiv.org/abs/1606.03490), and Lyu et al. separate a faithful explanation from a plausible one. **Identifiability** is a property of the causal question, not the pipeline: a quantity Q is identifiable under assumptions A if any two models satisfying A that agree on the observed distribution also agree on Q (Pearl, "Causal inference in statistics: An overview", Statistics Surveys 3:96-146, 2009, DOI 10.1214/09-SS057, Definition 2, read at https://ftp.cs.ucla.edu/pub/stat_ser/r350-reprint.pdf; paraphrased because the extracted text contained an apparent typo, and page numbers were not confirmed). No amount of determinism, provenance or typing makes an unidentifiable edge orientation identifiable; it only makes visible which assumption carried it.

## (v) Most relevant works, 2024-2026

1. **Kambhampati et al., ICML 2024.** Defines the role boundary: LLMs generate and help build critics; soundness comes only from external verifiers. https://arxiv.org/abs/2402.01817
2. **Li and Russo, UAI 2026.** LLM-elicited constraints as defeasible assumptions in an argumentation framework for causal discovery. The closest prior art to the student's application. https://proceedings.mlr.press/v337/li26e.html
3. **Ganguly et al., NeurIPS 2025.** Uncertainty over LLM-generated formal artifacts, and evidence that formalizing hurts on factual tasks. https://proceedings.neurips.cc/paper_files/paper/2025/hash/30ff6279fb18304d3eac481970157430-Abstract-Conference.html
4. **Kim, Poiroux, Bosselut, 2026**, read with **Zhang et al., 2026.** Measured faithfulness gap and the axiom-fabrication failure in two-stage pipelines. https://arxiv.org/abs/2604.19459 and https://www.alphaxiv.org/abs/2606.31002
5. **Souza et al., PROV-AGENT, e-Science 2025.** A concrete PROV schema for LLM invocations inside workflows. https://arxiv.org/abs/2508.02866

Runner-up: Atil et al. (2024/2025), the empirical basis for recording the served response instead of trusting temperature 0.

---

## Leads not verified in this session

- Carnap, "Meaning and Necessity", and Davidson 1967: reached only through SEP entries.
- Quine's own texts and the exact phrase "referential opacity": not confirmed.
- Smith 1985, "The limits of correctness": ACM page returned 403. Confirmed only as a citation inside the SEP entry; DOI unverified.
- Spirtes, Glymour, Scheines, "Causation, Prediction, and Search": publisher page blocked; unverified.
- Guidance, vendor JSON-schema structured-output documentation, and the core DSPy paper: not searched or fetched.
- The term "extensional/intensional database" from logic programming: not checked. It may collide with the student's usage.
- Publication venues for Tam et al., Moore and Shah, Kim et al., and the 2026 preprints in S16 and S18: unverified. The 2026 single- and two-author preprints should be treated as weak evidence.

## Connection to the project ledger

I read `claude/causal-copilot-research-ledger.md` for context. Three of its recorded facts line up with the literature:
- JSON mode without schema enforcement (F3): even with a schema, the guarantee is structural only (S8; Logic-LM).
- Temperature 0.0 default and open question Q4: Atil et al. and Yuan et al. predict run-to-run variation, so recording served model and response per call is the right control.
- Edge-review answers applied as directed edges (F20): this is exactly the collapse of "LLM asserted X -> Y" into "X -> Y" that RDF reification semantics keeps apart.

## Where we're going

- **Reframe the hypothesis as a conditional claim:** "an elicited judgement can be reified with provenance so that every downstream transformation is deterministic and auditable; correctness of the edge remains conditional on faithfulness, calibration and identifiability, each of which needs its own test".
- **Read Li and Russo (UAI 2026) in full** before fixing the capstone framing. It is the main novelty risk.
- **Turn the three counter-arguments into falsifiable checks on Causal-Copilot:**
  1. Faithfulness: does the recorded edge rationale actually support the applied edit?
  2. Stability: TARa-style agreement of edge decisions across repeated live runs.
  3. Calibration: do stated confidences track agreement with ground truth on the bundled datasets?
- **Re-verify quotes against sources** before any of this enters a mentor-facing document, and retrieve the "Don't Trust: Verify" full text that the proxy refused.