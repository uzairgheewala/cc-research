# Causal discovery auditing: prior work, positioning, and naming

Tickets: DLV-08, DLV-09, DLV-10, PRD-01; repository workflow: INF-06, BLD-11.
Date: 3 Nov 2026, America/Los_Angeles. Status: desk review and naming proposal.

**Positioning correction:** the proposed product is a reusable, system-agnostic
auditor; its benchmark suites are replaceable evaluation inputs. A benchmark
with tracing in its own harness is methodological prior work, not an equivalent
software system. The initial comparison underweighted this architectural
distinction. See [the scope correction and implementation evidence](heuresis-scope-and-auditor-positioning-2026-11-03.md).

## Scope and evidence

This review screens 95 Exa search results from 14 search angles, representing 88
distinct URLs before collapsing paper versions and related project pages. The
[search register](causal-auditing-search-register-2026-11-03.json) retains the
queries' result identities. Separate naming checks followed. Primary papers,
publisher pages, official repositories, and package documentation support the
comparisons below. Search snippets were used for discovery, not as proof that a
system implements a capability. Competing software was not installed or executed.
Repository descriptions remain their authors' claims unless backed by a reviewed
paper; even a published evaluation is not an independent replication here.

This is a broad relevant-work map, not a guarantee that every paper or private
implementation has been found. A cell describing one project's documented focus
does not prove that it lacks every capability outside that focus. Versions and
web documentation can change. The dated source register makes later updates
possible without silently changing this review's basis.

## The most consequential comparisons

| Work | What it evaluates or audits | Overlap and consequence for this project |
|---|---|---|
| [Heuresis: Benchmarking and Enhancing Agentic Causal Discovery](https://arxiv.org/html/2610.22846v1) | Synthetic discovery benchmark and its own instrumented agent harness. | Methodological comparator, not an equivalent independent auditor. Shared tracing techniques do not supply external-system contracts, cross-benchmark controls or our broader scientific evidence model. The architectural distinction is central to the separate scope correction linked above. |
| [Causal-Audit](https://arxiv.org/html/2604.02488), [implementation](https://github.com/marcoruizrueda/causal-audit) | Pre-discovery time-series diagnostics, risk estimation, and method recommendation or abstention. | Direct competition for the word "audit," with a different primary audit object: dataset/method suitability. The default package does not run discovery. Its README distinguishes the paper's four calibrated risk dimensions from six implementation scores, including heuristic behavior. Those scores do not establish graph correctness. A complementary diagnostic adapter is plausible. |
| [TCD-Arena](https://tcd-arena.github.io/) and [assumption-violation robustness study](https://arxiv.org/html/2310.13387v2) | Controlled violations and robustness profiles for time-series and iid discovery methods, respectively. | Strong prior art for stress-testing algorithms. Perturbing data and showing robustness failures cannot alone be our novelty. Their controlled experimental design is a methodological reference; different versions report different evaluation inventories, so this review does not combine their counts. |
| [DoWhy graph falsification](https://www.pywhy.org/dowhy/main/example_notebooks/gcm_falsify_dag.html), [GCM evaluation](https://www.pywhy.org/dowhy/main/user_guide/modeling_gcm/model_evaluation.html) | Compatibility of a supplied graph with data; fitted mechanisms, independence assumptions and model quality. | Graph/model validity is already a developed audit layer. A non-rejected graph is not established as the true graph. We should expose such checks with their assumptions rather than equate a good graph score or metadata check with causal truth. |
| [Self-Compatibility](https://proceedings.mlr.press/v238/faller24a.html) | Incompatibility between graphs learned on subsets of variables, without requiring known ground truth. | Particularly relevant to real-data audits. Passing is a necessary compatibility criterion, not sufficient correctness. This is a candidate future scientific check, not a capability currently implemented by our S1/S2 metadata layers. |
| [AssessLite](https://github.com/heidihelena/assesslite) | Declared structural assumptions, transformation attacks, stability/abstention decisions, and portable audit records for causal analyses. | Close overlap in invariance ledgers, controlled attacks, explicit uncertainty and audit export. The README describes native R/Python implementations and a shared schema, primarily around causal-analysis estimators. These implementation claims were not independently tested here. A ledger or three-way verdict alone does not distinguish us. |
| [OpenCausality](https://github.com/LEE-CHENYU/OpenCausality) | A causal-analysis workflow with estimation adapters, claim-strength gates, human review, and a hash-chained audit trail. | Important overlap in governed claims and provenance. Its documented workflow starts from a causal story/DAG and estimates relationships; our intended product evaluates independently supplied discovery systems. Governance and immutable records are established design territory. |
| [CausalProfiler](https://proceedings.mlr.press/v306/panayiotou26a.html), [code](https://github.com/panispani/causal-profiler) | Configurable generation of causal models, data, queries and ground truths with explicit coverage assumptions. | A potential source of test environments, and prior art for principled configurable benchmarks. It covers observation, intervention and counterfactual questions. Avoid claiming that configurable SCMs or transparent benchmark coverage are new by themselves. |
| [Benchpress](https://www.jstatsoft.org/article/view/v114i12) | Reproducible, modular structure-learning experiments across multiple libraries using a Snakemake workflow. | Strong prior art for adapters and reproducible execution. Owning our runtime and CI is useful engineering, but is not enough for a scientific contribution. |

## Other relevant systems and papers

| Work | Documented scope | Relationship |
|---|---|---|
| [CausalArena](https://arxiv.org/html/2609.11897) | Shared observational/interventional evaluation across synthetic, semantic, formula-grounded and real-data settings; versioned benchmark evolution. | Existing research input and possible benchmark integration. Regime diversity, freshness and diagnosability already motivate its design. |
| [ACDB](https://arxiv.org/html/2609.31675) | Budgeted hard interventions in linear-Gaussian SCMs; separate skeleton, DAG and intervention-efficiency scoring. | Active-discovery baseline and protocol comparator. Its own paper discusses density leakage and calibration limitations; do not copy its headline results as universal agent performance. |
| [CausaLab](https://arxiv.org/html/2605.26029) | Interactive synthetic laboratories, interventions, recovered graphs/equations, and mechanism-recovery trajectories. | Prior art for distinguishing successful predictions from faithful mechanism recovery and for inspecting intermediate reasoning. |
| [CausalDS](https://arxiv.org/html/2607.08093), [code](https://github.com/andleb/causalds) | Synthetic causal data-science scenes, observation-layer difficulty, identifiability, and abstention-aware deterministic evaluation. | Relevant to scientific task contracts and missing/non-identifiable answers. Broader than graph discovery alone. |
| [ACED-Bench](https://arxiv.org/html/2610.14381) | Active evidence acquisition and causal decisions in hidden categorical PGMs, with an evidence ledger. | Prior art for localizing investigation failures, lost evidence, commitment and stopping. It evaluates causal investigation rather than only graph recovery. |
| [AutoCause](https://arxiv.org/html/2608.00198v1), [code](https://github.com/marcoruizrueda/autocause) | Recorded expert choices, method comparison and link evidence grading for environmental time series. | An auditable analysis pipeline and companion to causal-audit. It could itself be a system under audit. |
| [causalcheck](https://pypi.org/project/causalcheck/) | Preflight diagnostics and method-family advice on data types, sample size, nonlinearity, noise, scales and related risks. | Another naming collision and assumption-screening comparator. Its documentation explicitly limits what these diagnostics can establish. |
| [CausalAudit](https://github.com/opencausality/CausalAudit) | Causal-drift monitoring of deployed ML models, comparing historical and current relationships. | Exact-name collision for CausalAudit/causalaudit. Different target from evaluating causal-discovery systems. |
| [CauseMe](https://causeme.uv.es/) | Time-series ground-truth datasets and submitted-graph evaluation. | Established benchmark/platform model, not a synonym for an end-to-end system audit. |
| [CausalBench / CausalBench+ platform](https://github.com/CausalBenchOrg/CausalBench) | Shared data, algorithms, metrics and evaluation services; package causalbench-asu. | Benchmark infrastructure comparator. Distinguish it from biological CausalBench. |
| [Biological CausalBench](https://www.nature.com/articles/s42003-025-07764-y), [code](https://github.com/causalbench/causalbench) | Gene-network inference from perturbational single-cell data, with biological and distribution-based metrics. | Existing research input. Reference incompleteness and metric interpretation must remain explicit. |
| [Causal Chambers](https://www.nature.com/articles/s42256-024-00964-x) | Controllable physical systems and empirically validated mechanistic models. | A route to external validity beyond synthetic graphs, with physical experimental assumptions of its own. |
| [causalAssembly](https://github.com/boschresearch/causalAssembly) | Semisynthetic production data and SCM generation, including interventions. | Possible test-generation integration; not a general auditor of arbitrary discovery software. |
| [Causal Testing Framework](https://github.com/CITCOM-project/CausalTestingFramework), [JOSS paper](https://joss.theoj.org/papers/10.21105/joss.07739) | Uses causal models and intervention effects to test complex software behavior. | Important methodological neighbor. Using causal inference to test software differs from specifically testing whether a discovery system supports its causal claims. |
| [recoverlite](https://github.com/heidihelena/recoverlite) | Pre-data simulations of whether a declared study-design/analysis pair recovers its target estimand under versioned criteria. | Related to testing the evaluator and the study design. Its README calls it a prototype, not a universal validity classifier. |
| [Causal Safety Engine](https://github.com/EM1805/causal-safety-and-alignment-engine) | A repository claiming discovery safety gates, multi-run stability, traceable artifacts and intervention blocking. | Adjacent implementation claims. Statements such as no false positives or certification through tests were not independently established by this review and should not be repeated as facts. |
| [Causal Transparency Framework](https://github.com/jgomarko/Causa-Transparency-framework) | Its repository describes causal accountability, counterfactual stability and metrics for ML predictions. | A neighboring model-accountability toolkit found during discovery; lower-confidence comparison based on repository search material, not an implementation review. |

## Papers that constrain our evaluation claims

| Prior work | Implication |
|---|---|
| [Beware of the Simulated DAG!](https://proceedings.neurips.cc/paper_files/paper/2021/file/e987eff4a7c7b7e580d659feb6f60c1a-Paper.pdf) | Generator-induced variance patterns can make structure recovery deceptively easy. A successful synthetic benchmark score needs shortcut controls. |
| [Unitless Unrestricted Markov-Consistent SCM Generation](https://proceedings.mlr.press/v275/herman25a.html) | Removing one sortability artifact need not remove others; graph density and coefficient-generation choices matter. |
| [Consistency evaluation of benchmarks used for causal discovery](https://arxiv.org/html/2606.01789v1) | Published benchmark graphs can disagree with domain literature. Literature/LLM consistency signals are not themselves experimentally established ground truth. |
| [Science-grounded, novel benchmarks](https://arxiv.org/html/2510.16530) | Memorization and training overlap undermine causal-discovery claims; recently authored scientific cases help address one leakage route without establishing every scientific edge. |
| [CausalGraph2LLM](https://arxiv.org/html/2410.15939v2) | Graph encodings and semantic context can move LLM results. Representation controls are substantive evaluation requirements. |

## A defensible position for our package

The proposed product evaluates causal-discovery **systems and the claims they
produce** under declared information, reference quality, input transformations,
budgets and observable execution. A benchmark is one versioned collection of
such tests. The reusable package should be able to host several batteries and
external benchmark adapters without making one dataset its identity.

The contribution to demonstrate is an independent auditing layer for externally
developed algorithms and agents: cross-system controlled comparisons, failure
localization, explicit scientific units and information boundaries, and results
that a reviewer can recompute from actual evidence. The S1/S2 contracts make
these concerns reusable across heterogeneous native interfaces; they are part of
the proposed method's architecture, not just packaging for one benchmark.
The review supplies the prior work and scope boundaries needed to substantiate
this contribution. A global priority claim still requires a dedicated novelty
argument; it does not follow from a feature checklist alone.

Our current protocol already distinguishes exact simulated truth from contested
or provenance-only references, and separates regime-matched scores from paired
controls. Its certificate verifies bound records and recomputed results; it is
not proof that a discovered causal graph is scientifically true. See
`audit/PROTOCOL.md` and `audit/report/certificate.py`.

Current implementation limits matter. S1 provides connection/evidence primitives;
S2 adds scientific metadata and bindings. Their conformance tests do not establish
complete native execution or new scientific measurement support. S3 is a design
proposal and S4 remains separate. See `audit/docs/subsystem2-implemented-scope-2026-11-02.md`
and `audit/docs/subsystem3-structure-design-2026-11-03.md`. Future product copy should
not promote these planned layers to current capabilities.

Before a benchmark release, demonstrate these distinctions experimentally:

1. A system can score well while relying on names, layout or other unintended cues.
2. An audit detects planted failures and does not simply condemn every system.
3. Findings retain their actual run sets, information regimes, uncertainty and
   missing-evidence states across adapters and benchmark families.
4. An independent environment can verify reports and reproduce supported numbers.
5. Results survive a fresh or held-out evaluation under rules fixed beforehand.

The existing research and saved acceptance receipts support parts of this program.
This literature review does not count as any new experimental validation.

## Names derived from the scope

| Candidate | Why it fits | Tradeoff revealed by the review |
|---|---|---|
| **Causal Crucible** | A place where discovery systems and their claims undergo controlled, demanding tests. Accommodates a toolkit, protocol, batteries and benchmark releases. | The unqualified name Crucible is crowded. In particular, [crucible-bench](https://pypi.org/project/crucible-bench/) already binds claims to measurements and exports recheckable records. Its documentation limits seals to record integrity, not truth. Use the full Causal Crucible name consistently, never a bare Crucible CLI or Crucible Benchmark. |
| **Causal Assay** | A controlled diagnostic procedure measuring specified properties under stated conditions. Suits profiles, controls, uncertainty and a panel of tests. | Can sound biological or like one diagnostic; explain that systems and their claims are the objects tested. Exact distribution-name availability has not been established. |
| **Causal Cross-Examination** | Conveys asking a system for evidence, challenging its answers and exposing contradictions. | Memorable research framing but long for a package; a shortened brand would need its own collision check. |

**First-round candidate, not selected:** Causal Crucible, with the subtitle
"Stress-testing causal discovery systems and their claims." A benchmark release
would be **Causal Crucible Benchmark v1**, not simply Crucible Benchmark.
The full name has no exact competing project identified in this search, but that
is not a reserved package name. PyPI availability checks were inconclusive.
No remote, distribution name, public site or license has been created or assigned.

Uzair requested further exploration after reviewing this pair. The name remains
open. The next round should vary the naming structure rather than substitute
more laboratory objects:

| New candidate | Derivation from the review | Example research title |
|---|---|---|
| **Causpect** | Causal + inspect: examine the system, its evidence and its claims without implying a guarantee. | Causpect: Evidence-Based Auditing of Causal Discovery Systems |
| **CausalSift** | Separate evidence-supported claims from shortcut-driven or unresolved claims through explicit controls. | CausalSift: Stress-Testing the Claims of Causal Discovery Systems |
| **Causal Scrutiny** | Directly names the critical evaluation role and accommodates several benchmark families. | Causal Scrutiny: Testing Data, Decisions, and Claims in Causal Discovery |
| **Causal Anvil** | A tougher-testing identity for the adversarial development and evaluation loop. | Causal Anvil: A Test Suite for Causal Discovery Systems |

My current preference for discussion is **Causpect**, because the coined word
retains the audit meaning while giving the project an identity separate from a
single benchmark or testing metaphor. Indexed searches did not surface an obvious
exact software collision for Causpect or Causift; registry names have not been
reserved or conclusively cleared. These remain proposals.

Other attractive roots were screened out: [Elenchus](https://praxon.dev/work/elenchus)
already names a verification-oriented AI harness, and
[Causcope](https://www.causal-atlas.app/) is already a causal-reasoning product.
This screening illustrates why an evocative name needs more than a plausible
etymology. Naming evidence is separate from the competitor-search register above.

Other meanings are less suitable: Sentinel suggests continuous deployed-model
monitoring, Ledger suggests only record keeping, and Proof or a universal
certification name would imply more than these tests can establish. Litmus also
suggests a single binary test, while this project's useful output is a profile
with explicit failures, uncertainties and untested scopes.

Another neighboring repository, [Lesz-Xi/crucible](https://github.com/Lesz-Xi/crucible),
uses crucible as an internal name for a broader research/governance workbench;
its README says the public identity is Wu-Weism. This further supports keeping
the complete two-word name if the candidate is adopted.

## Repository boundaries and the pending migration

- **Standalone auditor repository:** supported package, adapter contracts,
  protocol versions, conformance tests, benchmark definitions, documentation,
  examples, CI, contributor rules and a documentation/benchmark site.
- **cc-research:** research questions, methodology, pre-registrations, empirical
  results, limitations, paper artifacts, reproducibility records and the
  interactive research presentation. Cite a fixed auditor version for results.
- **causal-copilot-q1:** retain the existing course export until its relationship
  to the two repositories is deliberately updated. Do not silently repurpose it.

The auditor currently imports scientific utilities from research `score/`,
`analysis/` and `harness/`, and assumes research-relative data locations. Extraction
must separate supported runtime code from frozen research reference snapshots and
make evidence-root configuration explicit. Merely copying `audit/` or adding the
sibling research checkout to sys.path would not establish an independent package.

CI should distinguish synthetic/conformance tests from data-dependent reproduction.
Branch rules should target real check names after the first successful runs;
local automatic commits can continue on development branches while protected
remote changes go through review. Pages deployment and remote settings remain
separate from local preparation. No commits have been made during this review:
the user's required repository separation precedes all migration commits.
