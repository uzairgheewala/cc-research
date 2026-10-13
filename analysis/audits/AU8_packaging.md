# AU8 Packaging and delivery: how causal tools reach users, what their outputs must carry, and what the claim ledger should emit

Tickets: AUD-25, CAP-09, EXT-02
Written 2026-10-12 by an audit agent; sources read on that date.

## Where we are now

This is a desk audit. It is built on 43 typed rows (`AU8_packaging.json`) drawn from about 50 sources. Those sources are primary pages, regulator documents, GitHub issues, and our local copy of the Causal-Copilot code at commit a31aa7c. It extends the prior notes cluster2 (agents), cluster3/cluster6 (provenance and warrants) and cluster5 (reification, PROV, nondeterminism), and does not repeat them.

Two limits shaped what could be read:
- The shared web-search budget ran out near the end, so the causal-claims-registry search did not run.
- The GitHub API was not available to this session, so issue evidence comes from individual issue pages, not counts.

## Question

How are causal-analysis tools delivered today (library, notebook, GUI, agent or chat, SaaS, report)? What do users and regulators need from their outputs (provenance of each claim, uncertainty, reproducibility, explanation, audit trail)? What do users complain about? From that: what should the outputs and interface of our planned claim ledger look like if it is to be adopted?

## Method

**Inclusion rule.** A source is included if it does at least one of the following:
- documents a delivery mode or output format of a causal tool;
- states a reporting or record requirement from a regulator or reporting guideline;
- records a user complaint (a GitHub issue, a forum thread, or a review or survey of practice).

**How sources were read.**
- Regulator texts were read from the issuing body where possible: FDA PDFs, the ICH PDF, the EMA PDF, Federal Reserve letters, and artificialintelligenceact.eu for the EU AI Act article text.
- GitHub issue list pages were read in their default (open-issues) view. Individual issues were opened where the title suggested a complaint about outputs, knowledge handling or reproducibility.
- Causal-Copilot's outputs were judged from its paper (arXiv 2504.13263 HTML) and from its report generator code.

**Labels.** Every number is labelled `reported` (from the authors' own paper or table), `claim (vendor)` (marketing, press or sales pages), `second-hand` (someone else's summary) or `our reading` (our reading of code).

## Findings

### A. Delivery modes (11 rows)

1. **Libraries dominate real use; GUIs and agents are minor.**
   - A 2026 scoping review of 72 medical causal-discovery studies (Liu et al., JMIR Med Inform 14:e82499) found R the most used software, in 22 studies, with *pcalg* the most cited package. Tetrad appeared in 10 studies and Python in 7 (`reported`).
   - 27 studies (37.5%) named no software at all (`reported`).
   - https://medinform.jmir.org/2026/1/e82499

2. **Tetrad is the reference stack and is delivered four ways: GUI, command line, Python and R.**
   - Its command-line tool, causal-cmd, writes one text file per run that holds the log, the parameters and the graph. `--json-graph` adds a JSON graph equivalent to the GUI export.
   - Background knowledge is read from a plain text file with `addtemporal` (tiers), `forbiddirect` and `requiredirect` sections. Bootstrap ensembles have a `--seed` option.
   - This is the closest thing the field has to a standard run record and a standard format for declared knowledge (K).
   - https://bd2kccd.github.io/docs/causal-cmd/ ; https://www.cmu.edu/dietrich/philosophy/tetrad/ ; https://arxiv.org/abs/2308.07346

3. **Notebooks plus explicit assumptions is the PyWhy pattern.** DoWhy presents analysis as model, identify, estimate, refute, with assumptions as "first-class citizens" that are tested where possible. Its own paper concedes "no global validator method for a causal estimate" (`reported`).
   - https://www.pywhy.org/dowhy/main/ ; https://arxiv.org/abs/2108.13518

4. **No-code front ends and company libraries have not lasted.**
   - Microsoft's ShowWhy no-code suite was archived on 17 Dec 2025.
   - McKinsey's CausalNex "reached end of life" on 24 June 2026.
   - causaLens now sells "Digital Workers" (docker-packaged multi-agent systems). Its homepage says, as `claim (vendor)`, that every worker has "full audit trails and automated evaluation", but gives no schema or evidence.
   - Causaly sells a literature knowledge graph with cited answers ("70M directional relationships", `claim (vendor)`). Its page does not describe provenance for each relationship.
   - https://github.com/microsoft/showwhy ; https://github.com/mckinsey/causalnex ; https://causalens.com/ ; https://www.causaly.com/

5. **LLM agents deliver a chat or web front end and a report.**
   - Causal-Copilot runs from a command line or a Gradio web demo and ends in a LaTeX/PDF report that an LLM "populates" from a template. The paper reports no user study and no evaluation of the reports (`reported`).
   - CAIS, CATE-B, LLM4Causal, Causal Agent and CausalAgent use chat-style entry points. Per prior note cluster2, CATE-B and CAIS keep state stores, but none of these agents records, for each final edge, which stage produced it.
   - Zheng et al. (2026, causal-learn+) argue the agent "should not supply edges", and call for audit trails that separate data, assumptions, agent recommendations, user decisions and algorithm outputs (prior notes cluster2 and cluster6).
   - https://arxiv.org/html/2504.13263 ; https://arxiv.org/abs/2606.23608

6. **Browser tools for declared DAGs are what epidemiologists share.** DAGitty runs in the browser, needs no install, and has had model sharing since 2014. A ledger export in DAGitty syntax costs little and reaches reviewers in that field.
   - https://dagitty.net/

### B. Output formats and standards (11 rows)

- **Graph marks.** Downstream users need CPDAG and PAG endpoint semantics kept intact. When outputs flatten a mark, they assert ancestry the evidence does not license. See causal-learn #266 under D.
- **Two confidence numbers per edge.** bnlearn's `boot.strength` already separates existence frequency ("strength") from direction probability given existence ("direction"). These two numbers are the same two factors we measure: directed F1 = skeleton F1 x direction accuracy.
  - https://www.bnlearn.com/documentation/man/arc.strength.html
- **Justifying each edge is the gap the reporting literature measures.** Tennant et al. (IJE 2021) reviewed 234 applied articles (`reported`):
  - of the 144 articles that showed a DAG, 8 (6%) cited sources to justify arcs;
  - 48 of 234 (21%) stated their estimand;
  - none tested whether the DAG was compatible with the data.
  - Their recommendations include "justify any omitted arc" and "state adjustment sets".
  - https://eprints.whiterose.ac.uk/id/eprint/180527/1/dyaa213.pdf
- **Provenance standards that already exist.** None of these has been applied to causal-discovery output (prior note cluster3).
  - W3C PROV-O (Recommendation, 30 April 2013): Entity, Activity and Agent, plus `qualifiedDerivation`. https://www.w3.org/TR/prov-o/
  - PROV-AGENT for LLM calls. https://arxiv.org/abs/2508.02866
  - Nanopublications, which separate an assertion from its provenance (prior note cluster5).
  - Workflow Run RO-Crate (Leo et al., PLoS ONE 2024), which packages run records. https://www.researchobject.org/workflow-run-crate/
  - SLSA provenance, a software supply-chain model in which consumers verify signed provenance against expectations and rebuilding is optional ("can rebuild the artifact, if desired"). This is the pattern for "verify without rerunning". https://slsa.dev/spec/v1.0/provenance
- **Documentation genres.**
  - Model cards (Mitchell et al.) cover intended use, evaluation across conditions and caveats. https://arxiv.org/abs/1810.03993
  - Datasheets (Gebru et al.) do the same for datasets. https://arxiv.org/abs/1803.09010
- **Reproducibility norms.**
  - The NeurIPS checklist (items 4-8) asks for code and data, settings and "how they were chosen", correctly defined error bars, and compute per run. https://neurips.cc/public/guides/PaperChecklist
  - Prior note cluster2: most causal-agent papers report single runs.
  - Prior note cluster5: temperature 0 does not make hosted LLMs deterministic, so recorded responses must be replayed.
- **Causal-claims registry: not found by these searches.** The targeted search did not run because the budget was exhausted. The closest claim-level standard we know of is nanopublications.

### C. Regulator and reviewer requirements (10 rows)

| Source (status) | What it requires that a ledger can supply | Label |
|---|---|---|
| FDA, *RWE: Non-Interventional Studies* (draft, March 2024) | Protocol finalised before the study starts; a prespecified analysis plan; "a causal diagram to specify the theorized causal relationship"; an approach to confounding "including assessment of unmeasured confounding"; sensitivity analyses with a rationale; traceability, described for example as an audit trail of data provenance. Patient-level data and code are **not** requested. | reported (guidance text) |
| FDA, *AI to Support Regulatory Decision-Making* (draft, Jan 2025) | Seven-step credibility framework: question → context of use → model risk (influence x consequence) → plan → execute → document results **and deviations** → adequacy. "All performance estimates should be provided with confidence intervals"; uncertainty of predictions to be estimated; plan for maintenance over the model's life cycle. | reported |
| ICH E9(R1) (2019) | Estimand attributes; "Key assumptions should be stated explicitly together with the estimand"; sensitivity analysis is needed for any estimand that matters for decisions. | reported |
| TARGET (BMJ/JAMA 2025, 21 items) | Target protocol and its emulation reported side by side; causal contrasts; identifying assumptions (6g/7g); all sensitivity analyses; data and code sharing (item 19). | reported |
| STROBE (2007) | Whole-report checklist for observational studies; no item on DAGs (per the EQUATOR page). | reported |
| ICH M14 (Step 4, Sept 2025) | Data sources and their fitness for the question; bias and confounding. Full text not read. | second-hand |
| EMA reflection paper on AI (Sept 2024) | Documentation in a "detailed and fully traceable manner"; models and preprocessing "frozen and documented" before database lock in pivotal trials; "Incremental learning approaches are not accepted"; preference for interpretable models; generative-model output needs human review. | reported |
| FDA-EMA good AI practice principles (Jan 2026) | Data governance and documentation; context of use; information in plain language. | second-hand (RAPS) |
| EU AI Act Arts. 12, 13 and 19, Annex IV | Lifetime automatic logs; instructions stating accuracy metrics, limitations and how to interpret output; logs kept at least six months; design choices "including the rationale and assumptions"; dated, signed test logs. These apply only to high-risk uses (Annex III, e.g. credit or employment). The artificialintelligenceact.eu labels give 2 Dec 2027 as the Annex III start date (verify against the Official Journal). | reported (article text) |
| US bank model risk: SR 11-7 (2011) → **SR 26-2 (17 Apr 2026)** | Documentation detailed enough for "parties unfamiliar with a model"; effective challenge; validation of conceptual soundness, ongoing monitoring and outcomes; vendor models validated too. SR 26-2 supersedes SR 11-7 and **puts generative and agentic AI out of scope** ("novel and rapidly evolving"). | reported |

Correction to the brief: SR 11-7 is no longer current. Its replacement, SR 26-2, explicitly leaves LLM agents to each firm's own controls. A deterministic engine that treats LLM input as recorded data is a "model" that bank validators know how to review. An agent that writes the edges itself is not.

Sources: https://www.fda.gov/media/177128/download ; https://www.fda.gov/media/184830/download ; https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf ; https://www.bmj.com/content/390/bmj-2025-087179 ; https://www.equator-network.org/reporting-guidelines/strobe/ ; https://www.raps.org/resource/ich-adopts-the-m14-guideline-on-observational-stud.html ; https://www.ema.europa.eu/en/documents/scientific-guideline/reflection-paper-use-artificial-intelligence-ai-medicinal-product-lifecycle_en.pdf ; https://www.raps.org/resource/ema-fda-issue-joint-ai-guiding-principles-for-drug.html ; https://artificialintelligenceact.eu/article/12/ ; https://artificialintelligenceact.eu/article/13/ ; https://artificialintelligenceact.eu/article/19/ ; https://artificialintelligenceact.eu/annex/4/ ; https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm ; https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf

Common thread across regulators: a **prespecified** design, an **explicit causal diagram** with stated assumptions, **sensitivity analyses**, **traceability** of data and decisions, **documented deviations**, and **uncertainty with intervals**. None of them asks for per-edge provenance by name. FDA asks for the diagram, and Tennant et al. show diagrams are rarely justified edge by edge. That is the opening for the ledger.

### D. User complaints (11 rows)

1. **Declared knowledge is not honoured.** This is the most repeated complaint and the most relevant to us.
   - causal-learn #219: "Background knowledge not working".
   - causal-learn #171: forbidden higher-tier variables still appear in separating sets, which is a correctness problem as well as a speed problem.
   - causal-learn #266: knowledge-driven FCI orientation turns `Z o-> Y` into `Z --> Y`. The issue was diagnosed by Glymour.
   - Tetrad #1954: GRaSP output "doesn't respect the tier knowledge".
   - https://github.com/py-why/causal-learn/issues/219 ; /171 ; /266 ; https://github.com/cmu-phil/tetrad/issues/1954
2. **Results change silently with column order.**
   - causal-learn #271: GIN gives no clusters under one column ordering and `[[1, 2]]` under a permutation of the same data.
   - DoWhy #1695: `estimate_probabilities()` "silently returns incorrect probabilities" when parent columns are reordered.
   - This is the library-level version of our CausalArena finding, where column order alone scores directed F1 0.680.
   - https://github.com/py-why/causal-learn/issues/271 ; https://github.com/py-why/dowhy/issues/1695
3. **Validation steps break across versions.** DoWhy #1028: a refuter fails on versions 0.9-0.11 on three operating systems. The only workaround is to downgrade to 0.8. https://github.com/py-why/dowhy/issues/1028
4. **Scale and speed.** causal-learn #90: background knowledge slows FCI at about 300 variables.
5. **Learning curve and communication.**
   - Tetrad #1905 (45 comments) begins with a user who cannot wire up the GUI.
   - The CAWS 2021 round table (PMLR 160) lists five challenges: heterogeneous data; non-causal relationships; the lack of gold-standard datasets; "Communicating causal analysis results to those outside the field", where reviewers are sceptical and there is no standard language for reporting; and education.
   - https://proceedings.mlr.press/v160/kummerfeld21a/kummerfeld21a.pdf
6. **Applied studies report poorly and rarely reach decisions.** JMIR 2026 (`reported`):
   - 37.5% of studies name no software;
   - 18.1% leave assumptions unvalidated;
   - 44.4% cite unmeasured confounding as a limitation;
   - 1 of 72 addresses clinical decision support.
7. **Credibility and output complexity.**
   - A CHI 2026 formative study (n=15, qualitative-data domain) found that existing tools ignore context, lack credibility, or give overly complex outputs. This is an abstract-level read in an adjacent domain.
   - Causalvis (2023): analysts check each step visually, but visualisation toolkits do not cover the whole process.
   - https://arxiv.org/abs/2602.06506 ; https://arxiv.org/abs/2303.00617
8. **Abandonment.** ShowWhy and CausalNex, as above.
9. **Agents: no record of the source of each edge.**
   - Causal-Copilot restricts issue creation. Its visible issue numbers are mostly internal pull requests (we opened #1, #2, #5, #10, #20 and #30), so **no public user complaints were found**.
   - The one independent evaluation, CausalSteward, had to steer it to XGES because it "often preferred intractable methods such as FCI" (`reported` by CausalSteward, prior note cluster2).

## (1) Recommended output contract for the ledger

The contract has three layers: a claim record per edge, a run report per run, and a verifier. Each field below is traced to the requirement or complaint it answers (the C/D items above).

### Claim record

One record per variable pair per question (adjacency, orientation, ancestral, or effect-relevant).

| Field | Content | Answers |
|---|---|---|
| `claim_id` | Hash of (run_id, pair, question, mark) | traceability (FDA footnote, EMA 2.5.1) |
| `vars` | Stable variable ids derived from **column-content hashes**, plus display names; never positional indices | column-order complaints (#271, #1695); our 0.680 order leak |
| `mark` | Two endpoint marks (`-`, `>`, `o`), or `absent`; `status` ∈ {asserted, abstained, contradicted} | PAG semantics (#266); abstention |
| `support[]` | Typed items, each R ∈ {D, I, K}. **D:** test name, statistic, p-value, conditioning set, alpha; or the Meek/FCI rule id and the triple it fired on. **I:** intervention target, contrast, n. **K:** declarer, source file and line (causal-cmd knowledge format) or citation; for LLM-sourced K, model id, prompt hash, response hash, sample count and agreement | per-edge justification (Tennant: 6% justify arcs); nanopublication split; PROV |
| `derivation` | Ordered rule chain from support to mark, checkable by machine | "verify without rerun" (SLSA pattern); Zheng et al. audit trail |
| `data_only_mark` | The mark that D alone yields, and a flag if K or I changed it | "never below data-only" property; FDA sensitivity analyses |
| `confidence` | `p_adjacent` and `p_orient_given_adjacent`, kept separate, with bootstrap n and seed; calibration reference (benchmark regime, ECE, interval) | bnlearn semantics; FDA AI "confidence intervals"; EU AI Act Art. 13 accuracy metrics |
| `identifiability` | Compelled in the equivalence class / not identifiable from D under the assumptions / resolved only by K or I | ICH E9(R1) and TARGET "identifying assumptions" |
| `assumptions` | Ids into the run's assumption block (sufficiency, faithfulness, iid, test level) | E9(R1) A.5.1; Annex IV design assumptions |
| `invariance` | Mark under shuffled column order, and under neutral names (where names were used) | our controls; complaints #271 and #1695 |
| `retraction_set` | Minimal inputs whose removal or flip retracts the claim (where computable) | effective challenge (SR 11-7 / SR 26-2) |
| `gloss` | One plain-language sentence, filled from a **template**, not written by an LLM | plain-language principle; learning-curve complaints |

### Run report

Generated deterministically from the ledger, as HTML and PDF, plus a machine copy.

1. **Manifest.**
   - Hashes of the data and of each column.
   - Software versions with a lockfile, and the upstream commit.
   - Seeds.
   - LLM model ids, with the served responses stored for replay.
   - Signer and time.
2. **Question and context of use.** Q, R and W cell; intended decision; for effect questions, the estimand attributes (E9(R1)).
3. **Assumption block.** Each assumption is listed with the ids of the claims that depend on it.
4. **Claim table.** Asserted, abstained and contradicted claims, sorted by decision relevance, with the two confidences and their sources.
5. **Knowledge audit.** Every declared K item is listed as satisfied or overridden, with the reason. This answers #219, #171, #266 and #1954.
6. **Controls.**
   - Shuffled-order and neutral-name invariance rates.
   - Data-only versus final marks.
   - Run-to-run spread over seeds.
7. **Calibration and abstention.** Results on named benchmark regimes, with intervals. The report says so when the user's data lie outside those regimes.
8. **Deviations from plan** (FDA AI step 6), and **limitations** (W cells not covered, e.g. hidden confounders or time series).
9. **Mapping appendices.** Where each TARGET, FDA RWE and EU AI Act Art. 13 item is answered, or marked "not supplied".
10. **Exports.** Ledger JSON with its schema, PROV-O (JSON-LD), Tetrad JSON graph, DAGitty string, and an RO-Crate zip.

### Verifiable by a third party without rerunning

A shipped `ledger verify` command checks:
- (a) manifest and record hashes, and the signature;
- (b) that each `derivation` follows from its recorded `support` (Meek and FCI rules, acyclicity, knowledge consistency);
- (c) that every declared K item is satisfied or explicitly overridden;
- (d) the never-below-data-only rule: no claim's mark contradicts `data_only_mark` without a recorded I or K reason;
- (e) that stored LLM responses match their hashes and the K items built from them;
- (f) the report's summary numbers, recomputed from the claim table (and calibration figures, where truth is shipped).

What it **cannot** check without the data: the test statistics themselves. What it cannot check at all: whether a K item is true.

The report must state both limits. This matches the conditional-guarantee framing in prior note cluster5: verification is relative to the recorded artefact.

## (2) Interface forms most likely to be used

| Audience | Most likely forms (in order) | Evidence |
|---|---|---|
| Researchers | (1) Python library returning the ledger object, with an R path through reticulate; (2) CLI that reads causal-cmd knowledge files and writes Tetrad JSON plus ledger JSON; (3) notebook rendering with a per-edge drill-down | R, pcalg and Tetrad dominate applied use (JMIR 2026); Tetrad's four delivery modes; DoWhy's notebooks |
| Industry analysts | (1) Notebook widget or HTML report inside their existing platform; (2) chat or agent front end that **reads** the ledger and never writes edges; (3) a table export (CSV or Parquet) to BI tools | Causalvis (analysts want tools in their own environment); vendors moving to agents (causaLens, Causaly; vendor claims); SR 26-2 places agents outside model guidance; ShowWhy and CausalNex abandonment |
| Reviewers and regulators | (1) Static, signed run report (PDF/HTML) with TARGET, FDA and AI Act mapping appendices; (2) the verifier CLI plus an RO-Crate package they can open offline; (3) a DAGitty or PROV export for their own tools | FDA RWE (causal diagram, traceability); FDA AI (documented deviations, intervals); EMA (frozen, traceable); Tennant et al. recommendations |

## (3) Main adoption barriers, with evidence

1. **Trust in outputs, given known silent failures.** Knowledge is ignored (#219, #171, #266, #1954), column order changes results (#271, #1695), and agents pick directions from names (our measurement: 0.306 → 0.142 when names are swapped).
2. **No ground truth on user data, so validity cannot be shown.** CAWS 2021 (gold standards); JMIR 2026 (validation often not reported; confounding cited in 44.4% of studies).
3. **Communication and reporting.** There is no standard language (CAWS 2021); only 6% of DAG papers justify arcs and 21% state an estimand (Tennant 2021).
4. **Skills and learning curve.** Tetrad #1905; CAWS 2021 (education).
5. **Maintenance risk.** ShowWhy archived; CausalNex discontinued; DoWhy version breakage (#1028).
6. **Distance from decisions.** 1 of 72 medical studies reaches clinical decision support (JMIR 2026). Regulators accept causal diagrams as design inputs fixed in advance (FDA RWE, EMA freezing), not as discoveries made after the data are seen.
7. **Regulatory fit of LLM agents.** SR 26-2 excludes generative and agentic AI. EMA says generative output needs human review. Agent-made edges are therefore harder to defend than recorded K items.

## (4) Causal-Copilot's own output against these requirements

**Gets right**
- `reported`: an end-to-end report with sections for dataset and EDA, algorithm-selection rationale, the discovery result, revision by bootstrap and LLM, reliability, and inference (paper Sec. 2.5 and Fig. 23).
- `reported`: interactive checkpoints where the user can change assumptions or algorithms; command-line, web-demo and local Gradio deployment; an open repository under the MIT licence.
- `our reading`: bootstrap heatmaps are drawn per PAG edge type, so typed marks are at least visualised (`report_generation.py` `confidence_graph_prompts`).
- `our reading`: the edges the LLM forbade and the directions it added are listed with the LLM's reasons, which is partial provenance (`graph_revise_prompts`, around lines 587-665).
- `our reading`: the web-demo path exports JSON containing the selected algorithm, the reason, the arguments, the raw and revised graphs, and the bootstrap probabilities (`web_demo/demo_inf.py:1204-1219`).

**Gets wrong or leaves out** (all `our reading` of a31aa7c unless marked)
1. **Report prose is LLM-written.**
   - The reliability prompt orders the LLM: "Do Not include Numerical Numbers in your text!" (`report/report_generation.py:763`), so the confidence section gives only High/Moderate/Low bins at 0.9 and 0.1. This fails the FDA AI requirement for intervals and the EU AI Act Art. 13 requirement for accuracy metrics.
   - The graph narrative prompt says to "integrate background knowledge" when variable names have meanings (`:569`). The prose therefore leans on names, the same channel our measurements show drives its edge directions.
2. **The list of LLM-added directions is silently truncated to 10.** The list is sliced to `[:10]` and then tested for `> 10`, which can never be true (`:626-628`), so the "only a part" disclaimer never prints.
3. **The LLM-pruning section is included only for real-data mode** (`:966`). In simulated mode the report omits what the LLM changed.
4. **Unseeded randomness.**
   - Bootstrap resampling uses Python `random` with no seed (`postprocess/judge_functions.py:33`); the default is 20 resamples (`global_setting/state.py`, `boot_num`).
   - For more than 20 columns, the data preview shows 10 columns drawn with an unseeded `np.random.choice` (`:933`).
   - Reruns are therefore not reproducible from the report.
5. **No model identity in the report.** The model comes from the environment (`LLM_MODEL`, default `gpt-4o-mini`; temperature 0; `llm/llm_client.py:87,118`). The report records no model id, no prompts and no responses. The paper's text (as read) gives no seeds or LLM version for its experiments (`reported` absence).
6. **The machine-readable export is incomplete and unsafe.**
   - The command-line path writes only `report.pdf/.tex/.txt` and figures.
   - The web-demo JSON omits `llm_errors` (the direct and forbid records), `bootstrap_errors` and the conversation logs.
   - Full state is saved as a Python pickle (`demo_inf.py:768`). A pickle executes code when loaded, so a third party cannot safely load it.
7. **No per-edge source tag.** "The LLM proposed X→Y" is applied as X→Y (prior note cluster5, F20), and nothing records the data-only mark beside it. The paper says LLM suggestions "are treated as soft suggestions" (`reported`); our name-swap result (0.306 → 0.142) shows they are not soft in effect.
8. **No user study or report evaluation** (`reported`: none in the paper). The repository's benchmark scorer orients non-directed edges from the truth (our scope note), so its published numbers are not comparable with a ledger that abstains.

## Typed table

All 43 rows are in `AU8_packaging.json`: 11 delivery modes, 11 output requirements, 10 regulator requirements and 11 complaints. Each row has `sources`. Summary:

| Kind | Rows (name) |
|---|---|
| delivery_mode | Desktop GUI (Tetrad); CLI (causal-cmd); Python/R libraries; notebooks; DAGitty; no-code UI (ShowWhy); enterprise platforms/agents; literature platform (Causaly); agent + PDF report (Causal-Copilot); chat agents for effects (CAIS etc.); agent-restricted platform (causal-learn+) |
| output_requirement | typed marks; adjacency vs orientation confidence; per-edge justification; PROV-O; assertion vs provenance; RO-Crate; verify-without-rerun (SLSA); model card/datasheet; assumption statement; reproducibility checklist; claims registry (not found) |
| regulator_requirement | FDA RWE NIS; FDA AI credibility; ICH E9(R1); TARGET; STROBE; ICH M14; EMA AI reflection paper; FDA-EMA principles; EU AI Act 12/13/19/Annex IV; SR 11-7 → SR 26-2 |
| complaint | knowledge not honoured; column-order dependence; version breakage; knowledge slows search; learning curve; communication; no ground truth; poor applied reporting; credibility/complexity; abandonment; agents lack per-edge provenance |

## What this changes for the project

1. **Make the ledger a schema first.** Publish the claim record and run report schema (JSON Schema plus a PROV-O mapping) before building interfaces. Vendors claim audit trails without schemas, and libraries get abandoned, so a format that outlives our code is the adoption hedge.
2. **Make two checks default, verifiable properties of every run:** the knowledge-honoured check and the column-order/name invariance check. These are the field's most repeated complaints and our two central measurements. Report them in the run summary, not only in the paper.
3. **Use Tetrad's formats for interoperability.** Accept the causal-cmd knowledge file and write Tetrad JSON and DAGitty strings. This costs about a day and gives instant interoperability with the stack applied researchers already cite.
4. **Store two confidences per edge (bnlearn semantics) and report calibration with intervals per benchmark regime.** This links the capstone's skeleton x direction decomposition directly to the FDA AI and EU AI Act requirements.
5. **Build the report from a template, never from LLM prose.** An LLM may add a separately marked commentary box. This fixes four of the eight Causal-Copilot output defects above.
6. **Ship `ledger verify`** with the six checks (a)-(f) as the deliverable for reviewers, and state its two limits. This is the "conditional guarantee" in a form a reviewer can run.
7. **For CAP-09 and EXT-02, frame the positioning as follows:** the ledger supplies the per-edge justification that FDA's causal-diagram request and Tennant et al.'s recommendations imply, and that 94% of published DAGs lack. Under SR 26-2 and EMA's position, LLM input enters as recorded K data, not as an agent decision.
8. **Out of capstone scope:** a GUI, a no-code front end, or EU AI Act conformity. Mention them as future packaging only.

## Open questions

- Does any causal-claims registry or claim-level reporting standard exist outside nanopublications (e.g. the "causal claims in economics" database)? This search did not run.
- Do ICH M14 and the full FDA-EMA principles ask for causal diagrams or decision logs? Only summaries were read.
- How do users actually read bootstrap confidence? No user study of edge-confidence displays was found; a small reviewer pilot (5-10 people reading a ledger report against a Causal-Copilot PDF) would answer it.
- Does Causal-Copilot's current main branch (after a31aa7c) still truncate and strip numbers? Re-check before citing.
- Are Causal-Copilot's example reports (`asset/report_*.pdf`) consistent with the code reading? Not opened.

## Not read

- GitHub issue search pages with query or sort parameters: blocked by robots.txt for the fetch tool.
- GitHub API and `gh`: repository access not enabled for this session, so there are no issue counts or comment rankings.
- DoWhy #1708 (REFUTE critique and calibration benchmark): fetch error.
- SR 11-7 PDF attachment (sr1107a1.pdf): fetch error; the HTML letter was read instead.
- bnlearn `strength.html`: fetch error; `arc.strength.html` was read instead.
- CAIS architecture page body: only navigation and module names were returned.
- ICH M14 full text and the FDA-EMA ten-principles text: news summaries only.
- STROBE checklist files.
- Causal-Copilot example report PDFs.
- causaLens documentation: homepage only.
- Garg and Fetzer, "Causal Claims in Economics", and other registries: the search budget was exhausted.

## Searches run

- WebSearch: "github py-why causal-learn issue different results PC algorithm background knowledge"
- WebSearch: "github py-why dowhy issue refuter results confusing interpretation"
- WebSearch: "github Lancelot39 Causal-Copilot issues report generation error"
- WebSearch: "github cmu-phil tetrad issue causal-cmd output graph format results differ"
- WebSearch (extended): "survey practitioners barriers adoption causal discovery industry interviews"
- WebSearch: "interview study data scientists causal inference tools needs challenges CHI"
- WebSearch: "\"causal discovery\" scoping review applied health research reporting practices limitations adoption"
- WebSearch: "qualitative interview study practitioners causal inference workflow industry \"data scientists\" challenges paper"
- WebSearch: FDA RWE non-interventional studies draft 2024
- WebSearch: FDA AI regulatory decision-making draft guidance (two queries)
- WebSearch: TARGET guideline 2025
- WebSearch: SR 11-7 documentation quote
- WebSearch: SR 26-2 2026
- WebSearch: EMA AI reflection paper 2024
- WebSearch: ICH M14 Step 4
- WebSearch: FDA-EMA good AI practice principles 2026
- WebSearch: STROBE causal or DAG extension
- WebSearch (did not run, budget exhausted): Garg and Fetzer causal claims database
- Direct reads of GitHub issue pages:
  - causal-learn #1, #90, #171, #219, #266, #271, #272
  - DoWhy #1028, #1695
  - Tetrad #1905, #1954
  - Causal-Copilot #1, #2, #5, #10, #20, #30
  - default issue-list views of all four repositories
- Local code: Causal-Copilot `report/`, `web_demo/`, `global_setting/state.py`, `postprocess/judge_functions.py` and `llm/llm_client.py` at a31aa7c (`/home/claude/work/cc_src`).

## Where we're going

- AU0 synthesis should take items 1-6 of "What this changes" as the packaging decisions.
- CAP-09 should draft the claim-record JSON Schema and the template-built report skeleton against one CausalArena scenario.
- The reviewer pilot and the claims-registry search are the two follow-ups that would most change this audit.
