# System-agnostic causal auditing: the distinction from Heuresis

Tickets: DLV-08, DLV-09, DLV-10, PRD-01.
Date: 3 Nov 2026. Status: source-checked positioning correction.

## The architectural contribution

Uzair correctly identified a mismatch in the initial landscape: it gave shared
tracing techniques too much weight relative to the object being built. The
project's product is an independent auditor of externally developed discovery
systems. Its contracts cover how a native system receives information, what it
returns, what can be observed, which scientific comparisons are justified, and
which evidence supports a finding. A particular benchmark and an agent harness
are inputs or integrations, not the definition of the auditor.

That distinction changes the related-work argument. Reusing an idea such as
tracing, an invariance test or a sealed record does not mean another project has
already built this auditing layer. Conversely, implementation independence is a
property to demonstrate across actual integrations, not permission to infer
unobserved internal behavior from arbitrary software.

## What the paper establishes

[Heuresis v1](https://arxiv.org/html/2610.22846v1), sections 4.2-4.3 and appendices
B/C, evaluates three models in its own harness on six simulated mechanism
families; reported instances have 10 variables and 600 rows. Its repair analysis
is anchored to PC deletions. It also supports other algorithms, graph edits,
orientation probes, and undirected edges. Appendix B reports instrument checks.
These are meaningful benchmark capabilities; they do not establish a reusable
auditor of arbitrary external discovery pipelines.

## What is already substantive in this project

| Contribution | Repository evidence | What is established |
|---|---|---|
| Independent system adapters and declared information/output capabilities | `audit/core/adapter.py`, `audit/systems/`, `audit/docs/subsystem1-implemented-support-2026-11-01.md` | Eight registered adapters, spanning five LLM/hybrid systems and PC/GES/GIES. Recorded integration and concrete native support have different evidence. |
| Controlled separation of data and semantics | `audit/controls/`, `audit/PROTOCOL.md`, `analysis/reports/ab06_field_audit.md`, `analysis/reports/ab08_benchmark_card.md` | Real/neutral/swapped-name comparisons and a semantics/data disagreement generator address reliance on information channels, beyond anonymizing an evaluation dataset. |
| Stage-specific failure localization | `audit/trace/recorder.py`, `audit/trace/stages.py`, `audit/trace/cc_stages.py` | Observation hooks and supported stage extractors identify additions, deletions, flips and other changes in actual recorded pipelines. |
| Evaluation-stack and engine audits | `analysis/reports/bundle1_results.md`, `analysis/reports/ab03_engine_forensics.md` | Benchmark-order shortcuts and version/mode-specific library defects are investigated separately from a method's statistical assumptions. |
| Scientific comparison rules | `audit/PROTOCOL.md`, `audit/protocol/`, `audit/metrics/`, `audit/findings.py` | Information regimes, reference tiers, run completion, explicit thresholds and findings constrain what comparisons and interpretations are valid. |
| Reusable native-system connection and scientific experiment contracts | `audit/connections/`, `audit/experiments/`, S1 support map and S2 implementation-scope note | Typed identities, mappings, output families, observation gaps, histories, scientific units and evidence bindings support heterogeneous integrations without inventing unavailable semantics. |
| Reviewable outputs | `audit/report/`, `audit/core/evidence.py` | Reports and certificates bind results to sources and recomputation. This is result verification within declared scope, rather than a promise of causal truth. |

The architecture is broader than a benchmark-specific tracing facility. This is
also why the package deserves its own repository, protocol versions, integration
tests and documentation, while cc-research presents the scientific argument and
empirical evidence.

## Correcting the supplied comparison without losing its central insight

The other chat's assessment gets the software-category distinction right, but
mixes completed research, current implementation and future goals. Retain its
central argument while making the following corrections:

- The current registry has eight adapters, not eight external LLM architectures.
  Classical methods account for three of those entries.
- Requiring a submitted graph does not establish that every edge direction is
  forced. The paper's working graph admits undirected edges. Its tool record and
  graph comparisons also cover more than restored edges alone.
- The claim that the authors assumed error-free libraries conflicts with their
  instrument-verification appendix. Our engine forensics remains substantive,
  especially its external-library/version scope, without making that claim.
- Applying Meek rules after submission does not itself prove that the tool
  record was erased or that all undecided edges were forced into a DAG.
- Stage mutation lineage is implemented; a complete native proof explaining
  every collider, separating set, Meek dependency and score asymmetry across all
  algorithm families is not established by the current support map. That is a
  stronger future integration obligation, not a current blanket capability.
- A controlled name effect supports reliance on that channel within the tested
  conditions. By itself it does not prove that a stage performs zero statistical
  work in every setting.
- Our oracle findings apply to named versions and modes: for example, the
  forensics report separates gCastle original/stable from its passing parallel
  mode, and the vendored causal-learn copy from passing PyPI releases.

No novel metric or universal-interceptor implementation is authorized merely by
the pasted assessment. Its proposed evidentiary-faithfulness statistic would need
a precise estimand, justified support criteria, missing-evidence handling and
validation before being claimed as a scientific result.

## Revised research framing

We develop a system-agnostic framework for auditing causal-discovery algorithms
and agents. It evaluates externally supplied systems under controlled changes to
their evidence and information channels, localizes failures across supported
pipeline stages, and connects findings to explicit scientific contracts and
reproducible evidence. Benchmark suites are versioned applications of this
framework. The generality claim should be demonstrated by integrations spanning
different system architectures and benchmark families.

For naming, this supports an identity associated with inspecting and evaluating
whole systems. A stress-test-arena metaphor captures only part of the product.
The name remains open; no repository or distribution brand has been fixed.
