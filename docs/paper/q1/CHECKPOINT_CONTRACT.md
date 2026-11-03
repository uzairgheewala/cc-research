# Crucis: Q1 checkpoint scope and evidence contract

Tickets: DLV-05, DLV-06, DLV-07, DLV-08, DLV-09, DLV-10, DLV-11, PRG-01.
Adopted for the 6 Nov checkpoint on 3 Nov 2026 through Uzair's instruction to
freeze stage 1 of the agreed plan. Contract ID: `crucis-q1-checkpoint-2026-11-03-v1`.

## What is frozen

The checkpoint's research scope and current numerical evidence basis are fixed.
The prose, citations, PDF, public packaging and submission are not yet final.
The machine-readable baseline is [checkpoint_contract.json](checkpoint_contract.json).
It fixes all 78 registry entries, their 13 source files and formatted values.
The evidence commit at capture is `cf536c12df7fad928a3c7e76b51f2d441cf7efb8`;
11 sources are tracked-clean there and two external CausalBench metadata files
are separately hashed in `manifests/excluded/external.sha256`.

This freeze permits continued subsystem implementation. It does not freeze the
Crucis architecture around the legacy levels, current adapters or graph-only
answers. No new paid run, empirical matrix or funding amount is adopted here.

## Research identity and deliverable

**Crucis** is an independent, system-agnostic framework for auditing causal
discovery systems and their claims, with a versioned benchmark/evaluation suite.
Its intended scope includes faithful native evidence, controlled experiments,
execution/collection, measurement, provenance, reporting and validation of the
auditor itself. Supporting different systems, modes and response types requires
explicit capability and test evidence; archival capacity alone is not support.

The Q1 paper presents the framework/methodology and the empirical audit of
causal-discovery systems and benchmarks. Causal-Copilot supplies a rich worked
case. Q1's broader goal remains the generic package, auditor validation and a
defensible multi-system study, as recorded in the 1 Nov empirical-study rebase.
The present adapter panel is a starting point, not a limit on that goal.

The 6 Nov checkpoint contains title, abstract, introduction/problem statement,
prior work and relevant data, with a public code link and a PDF in the established
course template. The exact assignment time and mentor additions remain external
checks. Source: [official Q1 assignment](https://dsc-capstone.org/2026-27/assignments/projects/q1/).
The final Q1 report is due 4 Dec. An ICML-level paper is a development objective,
not a claim that the checkpoint is already a completed conference submission.

The title will use Crucis; exact subtitle wording remains editorial. The existing
draft title is historical until the paper-correction stage updates it. The
reconstruction/refinement system is the companion Q2 work: this paper may audit
the original system, but does not claim the companion's improvements as its own.

## Claim and evidence boundaries

| Claim family | Fixed basis | Required interpretation |
|---|---|---|
| CausalArena layout/scoring | `ab01.*` | A benchmark/scoring property. Forced orientation and index tie-breaking are distinct from expectation scoring or intrinsic system layout reliance |
| CausalBench metrics | `ben13.*` | Reproduction, total-effect ceiling and FOR findings retain their specific metric meanings. The earlier parent-placement interpretation is not substituted |
| Cross-system name controls | `ab06.*` | Declare each system/configuration, input regime, cohort, stage and scoring rule. The legacy P9 grouping is not a matched shared-cohort leaderboard |
| Causal-Copilot pipeline | `cc.*` | Original-system behavior; distinguish all runs from completed pairs, crashes from host errors, and bootstrap from model review |
| Label-following test | `bnd08.*` | BND-08's M3 rule supplies the pre-registration; it is not interchangeable with a later K11 threshold |
| Data/reference descriptions | `s1.*`, `s2.*`, `cb.*` | Registry prefixes name legacy data groups, not the new S1/S2 software subsystems. Reference reliability, information and population restrictions remain explicit |

Every printed number continues through `numbers.json` and `\nm{key}`. Existing
keys, source bytes, selectors, operations and formats cannot silently change.
Unsupported comparisons cannot be made valid by unchanged numeric values.
The numeric checker does not certify scientific interpretation or novelty.

These mandatory wording corrections remain OPEN for the paper stage:

1. Attribute the main adjacency loss to bootstrap within refinement, not the
   model review. The frozen diagnostic receipt recomputes the paired stage
   differences over completed runs; the real-arm-only K10 effect is a different
   estimand and must not be substituted for that aggregate.
2. Explain Causal-Copilot's S3/committed-mark name-reliance measurement and its
   exploratory label. The other agents use final graphs/expectation scoring on
   a different cohort; there are no shared scenarios between these suites.
3. Describe MATMCD as below its data-only graph on the point estimate. Its
   interval includes zero; a pre-registered point-rule finding does not imply
   an interval excluding zero.
4. Attribute the label-following test to the actual external pre-registration.
5. Add a checked Heuresis citation and precise comparison. Its benchmark and own
   harness are relevant prior work. The independent, system-agnostic framework
   contribution remains central; unsupported global-first or universal-coverage
   claims do not enter the paper.
6. Distinguish implemented, tested, designed and empirically validated scope.
   The current S1/S2 implementations are additive development; S3's 3 Nov note
   opens design. None automatically adopts a new public scientific protocol.

For migration safety, two byte-preserved diagnostic snapshots are in
`checkpoint_evidence/`: the recomputed rebase-facts receipt and MATMCD's existing
report. Their origin paths, hashes and capture status are in the JSON contract.
They support interpretation checks; they are not new registry inputs, fresh
model runs, a newly certified protocol, or evidence tracked at `cf536c1`.
The rebase-facts receipt recomputes stages/cohort checks but reads the historical
comparison/grid; it does not rerun all 1,298 historical numeric comparisons.

## Workstream and repository boundary

| Owner/home | Owns | Handoff obligation |
|---|---|---|
| Paper / `cc-research/docs/paper/q1/` | Manuscript, citations, number registry, this contract, PDF/bundle | Correct claims, preserve baseline; update HANDOFF and record actual build/submission state |
| Crucis subsystem workstream / current `audit/` | Reusable framework, protocol proposals, new subsystem implementation, package tests | Keep developing owned files; supply migration inventory and later explicit output port map |
| Research record / `cc-research` | Frozen study results, data/reference metadata, analysis/reproduction, paper, showcase | Preserve source paths/bytes during extraction; identify actual publication versions |
| Coordination | Tracker, site, Slack, migration and repository policy | Link evidence/status; keep delivery receipts; do not mark submission done before it occurs |
| Companion system workstream | Fork/reconstruction and its scientific improvements | Preserve separate claims, versions and result ownership |

This contract freezes the PAPER INPUTS. It does not lock the active `audit/`
working tree or reserve its latest contents for extraction. Before stage 2
moves any package files, it must capture an owned-file inventory and compare it
again at extraction. Concurrent edits require reconciling that inventory; never
overwrite or discard them. The diagnostic snapshots remain readable if the
original audit reports move or change.

## Migration and version rules

The checkpoint continues on the pre-package numerical sources. It does not wait
for a new certificate schema, new subsystem completion or fresh experiments.
The 13 research inputs remain at their current research paths during extraction.
Two excluded metadata files must remain available locally and receive an honest
public availability route; an excluded-data manifest is not a public download.

Later porting to Crucis is a separate reviewed contract revision: an exact
key-to-source map (including keys that stay), installed-package/certificate
checks, recorded repo commits, matching raw/formatted values, preserved units,
population, metric, verdict and confirmatory/exploratory meaning. Tolerance in a
certificate-reproduction check never silently authorizes changing paper values.
The paper build must support explicit repository roots and record both commits
before adopting any sibling-repo input. No port map is invented in this stage.

Local commits may advance HEAD after the repository split. The frozen evidence
commit stays as historical provenance; the final paper build also records its
actual source commit. Current HEAD equality is intentionally not a freeze check.
Generated lock HEAD/Git-state metadata may refresh while the frozen values and
source hashes remain identical. No automatic re-freeze or unexplained repin is
permitted. A necessary scientific change gets an explicit revision and rationale,
retaining this baseline for comparison.

## Checks and subsequent gates

From `cc-research`, with `tools/python.ps1 -B` (or the project interpreter):

```text
python -B docs/paper/q1/check_checkpoint_contract.py
python -B docs/paper/q1/build_numbers.py --check
python -B docs/paper/q1/lint_report.py
```

The first command checks frozen bytes, registry/claim coverage, exact lock
values/source set and a fresh number resolution. It never updates the baseline.
It accepts legitimate Git HEAD changes and permitted manuscript/citation edits.

Stage 1 is complete when this contract/manifest exist, all keys are covered,
sources match and the paper handoff points here. It does not close DLV-05.
Submission readiness additionally requires the corrections and citation review,
current PDF compilation/visual inspection, template bibliography, author details,
and a verified public code/evidence entry point matching the paper. The existing
Q1 export reproduces the companion comparison only; broader evidence coverage
and README links must be reconciled before claiming full paper reproduction.

Published parity is a later gate: actual authorized push, successful CI,
confirmed deployment and reconciled Slack receipts. Local generated files are
not proof of publication. The October 31 prod digest already exists; reconcile
its actual edited text and receipt rather than reposting it.

The user's no-commit-until-separation instruction remains active. This stage is
ready for a local milestone commit once that boundary is satisfied; it does not
waive the migration hold or authorize remote publication.
