# Pass 6: literature and system map

How this was produced: five search agents each covered one cluster and returned a written report (kept unedited in `literature/agent_reports/`, about 130 works in total). This file is my synthesis. The agents read pages through a summarising fetch tool, so their quotes and numbers are second-hand.

Verification status used below:
- **V** = I opened the paper myself (arXiv HTML or alphaXiv text) and confirmed the specific claim cited here.
- **A** = (historical) reported by an agent and not re-checked. As of 2026-10-10 no A claims remain (REP-13).
- **S** = a search-scope statement: what an incomplete search found or did not find.


## Verification update (2026-10-10, REP-13)

Every claim in this file that was marked A has been re-read in its primary source: 72 claims, 55 confirmed (V), 17 corrected, 0 removed. Table with URLs, sections and short quotes: `analysis/literature/bnd02/rep13_claims.md`. Pages were read through a summarising fetch tool, so quotes must be checked against the PDF before they go into a course or mentor document. The corrections below **supersede the text** of sections 1-6:

- **L08** (s1 row 4): In the current implementation a consensus LLM direction is a hard directional fact, enforced only if its adjacency survives CI-based skeleton reduction. Making LLM constraints defeasible (calibrated against CI-test confidence) is stated as future work.
- **L09** (s1 row 4): Drop 'strong': the arrow is blocked whenever a CI test removed the adjacency; no evidence-strength threshold. LLM input can orient surviving edges but cannot add edges.
- **L10** (s1 row 4): DAG output confirmed. Synthetic graphs have 5-15 nodes, but benchmarks go up to CHILD (20 nodes). Say 'DAGs only, 5-20 nodes'.
- **L18** (s2 LLMs as imperfect experts): Guarantee and epsilon-expert model confirmed, but the bound is a posterior estimate that holds only if the epsilon-expert model is right. 'The only guarantee of this form' is a claim about our search, not the paper: write 'the clearest guarantee of this form we found'.
- **L19** (s2 LLMs as imperfect experts): Partly. Over-confidence is the stated cause for text-davinci-003; on ALARM, G* was excluded because of 'ambiguities in the metadata'. Say: 'their LLM test violated it, through over-confidence and ambiguous metadata'.
- **L25** (s2 Memorisation): It is a matched verbalization-swap ablation: the seeded story and variable names change while graph, SCM and data stay fixed. Not a swap of names between variables. Say 'story/name re-verbalization holding data fixed'.
- **L26** (s2 Memorisation): Variables are real-word keywords drawn at random (possibly causally unrelated) so the agent must rely on the data; the paper does not frame this as a memorisation control. Say 'randomly drawn keyword names'.
- **L28** (s2 Trust, deferral, abstention): Disagreement-driven querying confirmed, but the expert in the experiments is simulated, not an LLM. Add 'with a simulated expert'.
- **L38** (s2 Bootstrap): Wrong as stated. They found resampling frequencies good confidence indicators overall; calibration depended on the model (well calibrated for linear Gaussian, poorer on Child, often over-estimating). Remove from 'persistently miscalibrated'; cite only Banerjee et al. for that.
- **L44** (s2 Background knowledge): True for Meek (knowledge only orients; inconsistency makes the procedure fail). Andrews et al.'s tiered-knowledge FCI variant also forbids some adjacencies. Say 'orientation-only knowledge never deletes an adjacency; knowledge can forbid adjacencies, but is never silently overridden'.
- **L49** (s2 Single-objective): Sizes: Hyttinen 7, ACI 9 (11 real), Russo 2024 10, Li and Russo 20 (CHILD), Bromberg and Margaritis 37 (ALARM). Say 'most stop at 7-20 variables'. ACI does export a per-claim confidence (ancestral, not per edge).
- **L52** (s2 Agents): MAC reports mean +/- std over 10 seeds, so it is not a single-run evaluation. No renaming control confirmed (authors flag memorisation as a limitation).
- **L53** (s2 Agents): Not post-hoc: the LLM proposes the initial graph from metadata and amends it in an iterative loop with a data-driven model. Benchmarks: Arctic sea ice, Sangiovese, synthetic Alzheimer's (not all 'famous'). No renaming control confirmed.
- **L62** (s2 Translate-then-solve): Soundness is inherited from the hard (correctness) critics, which an LLM cannot be; LLMs can act as soft (style) critics and can help write hard critics.
- **L68** (s6 Leads): ID and authors correct. The Sachs ground-truth discussion found is in Section 4 (A.4 mentions Sachs only in passing); no dedicated Sachs appendix found (last ~8k characters of the page not read). Say 'Brouillard et al.'s discussion of the Sachs ground truth (s4)'.
- **L69** (pass7_framing_test_and_candidates.md s3 L5): Claim holds but has no citation; add Tam et al. 2408.02442 (NL-to-Format two-step keeps natural-language performance).
- **L71** (s3; pass7_framing_test_and_candidates.md L6): Both have a data veto. Symbolic (argument-level) traceability is a property of Li and Russo's ABA; MosaCD's method as read describes none. Attribute traceability to Li and Russo only.
- **L73** (s2 Bootstrap): Friedman, Goldszmidt and Wyner, UAI 1999 confirmed on the first author's abstract page (https://ai.stanford.edu/~nir/Abstracts/FGW2.html).
- LINC, SatLM and Faithful CoT were not re-read individually; the shared claim in section 2 now rests on Logic-LM alone (L58), and the three names are dropped from it.
- Statements of the form "not found" / the "Open" list in section 3 are search-scope statements (what an incomplete search reached), not claims about a work; they are marked S.

Search limits: the shared search budget ran out, so the sweep of works citing Causal-Copilot is incomplete, and whether an arXiv v3 of the paper exists is unknown. "Not found" below means "not found in an incomplete search".

## 1. The five works that bound this project

| Work | What it establishes | What it leaves open | Status |
|---|---|---|---|
| Zheng, Verma, Gill, Dai, Spirtes, Zhang, "Causal Discovery in the Era of Agents", arXiv 2606.23608 (June 2026) | Position: agents "should not supply edges, orientations, priors, constraints or causal conclusions"; "provenance is not bookkeeping; it is part of what a graph mark means" | No schema and no evaluation. Calls for "audit trails that separate data, assumptions, agent recommendations, user decisions and algorithmic outputs" and for testing whether agent guidance reduces over-interpretation of partially identified graphs | V |
| Kitson and Constantinou, "LLM-Augmented Causal Discovery: Probabilistic Fusion of Edge Existence and Orientation", arXiv 2608.27472 (Aug 2026) | Four probabilities per pair (absent, forward, backward, undirected), LLM and data fused, variable names obfuscated; on Sachs F1 0.606 data, 0.400 LLM, 0.727 fused; LLM better at orientation than at existence | Values are "empirical support ... rather than calibrated posterior probabilities"; source is lost after fusion; no circle or bidirected state; no abstention | V for the representation, name obfuscation, the quoted sentence and the Sachs figures; the rest re-read 2026-10-10 (REP-13) |
| Kumar et al., "From Causal Plausibility to Causal Reliability", arXiv 2608.23660 (Aug 2026) | Calibration of LLM direct-edge answers measured: recall above precision in 94.4% of model-dataset pairs; verbalised confidence badly calibrated (ECE about 0.2), agreement across prompts much better (about 0.02) | No use of calibration inside a discovery method; no abstention rule; Sachs not included | V |
| Li and Russo, UAI 2026, PMLR 337:3631-3667 (arXiv 2602.16481) | LLM constraints kept only if five queries agree, entered as defeasible assumptions; a required arrow is dropped if strong data evidence removed that adjacency; memorisation-resistant benchmark from random graphs mapped onto CauseNet | DAGs only, about 15 nodes, no confidence on individual LLM statements | V for venue, method outline and the CauseNet protocol; the details re-read 2026-10-10 (REP-13) |
| Tagliapietra et al., "CausalSteward", arXiv 2607.01936 (July 2026) | The only external evaluation using Causal-Copilot as a baseline that was found: F1 0.078 (53 nodes) and 0.014 (186 nodes); "CausalCopilot was steered towards XGES, as it often preferred intractable methods such as FCI" | Does not say which of Causal-Copilot's graphs was scored or what its refinement stage contributed | V |

Also verified by me: Srivastava et al., arXiv 2510.16530 (bnlearn graphs are reconstructed by GPT-4 from their names; post-cutoff graphs are not).

## 2. Map by theme (re-read 2026-10-10, REP-13; see the verification update)

**LLMs as imperfect experts.** Kıcıman et al. (2305.00050) showed strong pairwise accuracy and partial memorisation of the benchmark. Long et al. (2307.02390) give the only guarantee of the form "the true graph stays in the returned class with probability at least 1 - eta", under a constant-error expert model; their own LLM test broke it through over-confidence. Vashishtha et al. (2310.15117) show pairwise answers confuse direct with indirect causation and propose causal order as the interface. Ban et al. (2311.11689) let the LLM only verify edges the data proposed. Wu et al. (2506.00844) argue LLMs should have no decisional role at all.

**Memorisation.** Feng et al. (2407.19638): accuracy tracks how often a relation appears in training text. Srivastava et al. (V). Controls in use: neutral names (Kitson and Constantinou; DMCD 2602.20333), name swaps holding data fixed (CausalDS 2607.08093), meaningful names on unseen graphs (Li and Russo), random-word names (Han et al. 2408.06849).

**Trust, deferral, abstention.** Learning to defer per pair (Clivio et al. 2502.13132, two variables only). Selective querying where algorithms disagree (Tench and Demeester 2601.16715; CauTion 2606.03602; Causal Ensemble Agent 2606.10607, which has a with/without-LLM ablation). Filtering LLM orientations against the data (MosaCD 2509.23570). Three-zone thresholds with an explicit "unknown" band (Takayama et al. 2402.01454).

**Bootstrap aggregation over typed marks.** Friedman, Goldszmidt and Wyner (UAI 1999) already treat directed and undirected edges as separate bootstrap features. bnlearn's `boot.strength` reports strength regardless of direction and direction given presence, and thresholds strength only (Scutari and Nagarajan 2013). Tetrad keeps full edge-type frequencies including circle marks with several ensemble rules (software documentation). Debeire et al. (CLeaR 2024) vote over edge types with conservative tie-breaking. Jabbari et al. (1712.08626) show PAG edge-type frequencies need calibration. Kummerfeld and Rix (1910.02047) and Banerjee et al. (2503.15436) find bootstrap frequencies persistently miscalibrated. Error control exists only for adjacency-type selection (Meinshausen and Buhlmann 2010).

**Background knowledge with guarantees.** Meek (1995) and Perkovic et al. (2017) for CPDAGs with required and forbidden edges; Andrews, Spirtes and Cooper (AISTATS 2020) for FCI with tiered knowledge. Adding orientation knowledge never deletes an adjacency in these frameworks. Pairwise add/remove/orient edits on a PAG have no such result.

**Single-objective evidence combination.** Weighted constraints solved by answer-set programming (Hyttinen et al. 2014), Ancestral Causal Inference with a per-claim confidence that is zero when undetermined (Magliacane et al. 2016), argumentation (Bromberg and Margaritis 2009; Russo et al. 2024; Li and Russo, V). All stop at roughly 7-15 variables and none exports a per-edge support record.

**Agents and their evaluation.** Post-hoc LLM refiners: ALCM (2405.01744), MATMCD (2412.13667), MAC (2407.15073), Causal Modelling Agents (ICLR 2024), Causal-Copilot. All report gains on famous named benchmarks, mostly single runs, none with a renaming control. On the effect-estimation side, benchmarks now score stages separately (CausalVerify 2609.07944; CausalReasoningBenchmark 2602.20571; CauSciBench, ICML 2026). No stage-separated benchmark for discovery agents was found. Single-run agent evaluations misrank systems (Mehta 2602.11619).

**Translate-then-solve and its limits.** Logic-LM: the solver's guarantee is relative to the formalisation, and the formalisation step is where errors enter. Measured compile-versus-faithful gaps of 3 to 29 points (Zhang et al. 2606.31002); two-stage pipelines inducing fabricated axioms (Kim et al. 2604.19459); formalising hurting on knowledge-heavy tasks (Ganguly et al., NeurIPS 2025). Kambhampati et al. (ICML 2024): soundness comes only from external critics, and an LLM cannot be the critic. Temperature 0 is not deterministic (Atil et al. 2408.04667).

**Provenance models.** W3C PROV-DM (2013); PROV-AGENT (2508.02866) extends it to LLM invocations; nanopublications separate an assertion from its provenance. RDF 1.1 Semantics: "a reification of a triple does not entail the triple". No application of any of these to causal-discovery output was found.

## 3. What is already done, and what is open

Done, each separately:
- typed four-state fusion of LLM and data graphs (Kitson and Constantinou);
- measurement of LLM edge-confidence calibration (Kumar et al.);
- the provenance principle, stated without a schema (Zheng et al.);
- data veto over LLM constraints with symbolic traceability (Li and Russo; MosaCD);
- memorisation of bnlearn benchmarks, and several controls for it;
- strength/direction separation for CPDAG bootstrap output (bnlearn).

Open, as far as the search reached (S):
- a per-edge record of which stage introduced, removed or re-oriented each mark, that survives to the output;
- PAG marks (circle, bidirected) as first-class types in bootstrap aggregation and in any LLM fusion;
- calibration used inside the decision, with abstention accounted for;
- memorisation used as a signal at run time, not only audited afterwards;
- a stage-separated evaluation of a deployed agent (raw algorithm output, after bootstrap filtering, after LLM review) under original versus neutral versus swapped names, with repeats;
- any published ablation of Causal-Copilot's refinement stage.

## 4. Terminology

"Intensional to extensional" is not how this literature, or philosophy of language, describes the move. In the standard sense an intension is a meaning and an extension is what it picks out; the hypothesis uses "intensional" for "background semantic knowledge", which is a different sense. The terms in use are: elicitation (obtaining a judgement from an imperfect expert), semantic parsing or formalisation (text to a formal language), reification (making a statement an object that can carry provenance, without asserting it), provenance and audit trail, hard versus soft constraints, required and forbidden edges, existence versus orientation, deferral and abstention. The agent's suggested wording for the idea is "elicit once, reify with provenance, then verify".

## 5. Threats to any novelty claim, strongest first

1. Kitson and Constantinou already have a typed per-pair representation with separate existence and orientation channels and a name control. "Typed fusion" alone is taken.
2. Zheng et al. state the diagnosis and conclude that agents should supply no edges. A project that keeps any LLM edge input must argue for it, or adopt their position and build the audit trail they ask for.
3. Kumar et al. cover calibration measurement.
4. Li and Russo, MosaCD, CauTion cover data veto, abstention and trust estimation for DAG or CPDAG outputs.
5. The memorisation finding is published for bnlearn graphs; only its effect inside a deployed agent is new.

## 6. Leads not followed

Completing the citing-works sweep; reading Kitson and Constantinou and Li and Russo in full; the Tetrad source for the exact "Preserved" ensemble rule; the Sachs appendix of Brouillard et al. (2412.01953); value-of-information treatments of "ask the LLM, ask a person, or run an experiment".
