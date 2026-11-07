# Checkpoint repository, disclosure and reproduction audit

Tickets: DLV-05, DLV-06, DLV-07. 6 November 2026.

This audit has completed the bounded checks below and identified unresolved
reproduction, operational and publication gaps. It is not a whole-paper native
reproduction or a fresh full-text literature review. The submitted manuscript is
unchanged, at SHA-256
`59898a48fcc5b6006fcb8be739dd92e314faa55edc002a2000161a1ace7709cf`.
The author confirmed submitting the archived PDF. Exact upload time and an
authenticated Gradescope receipt are not available.

## What was actually checked

| Finding/input family | Actual check | Result and boundary |
|---|---|---|
| All numerical sources | Frozen contract, registry/lock check and hashes of all numerical sources | 78 entries, 13 sources and 19 frozen files match. This verifies values and integrity, not original experimental validity. |
| FCI scoring comparison | Separately implemented directed F1 and seeded undecided-pair orientation from retained edges, checked against local public generating-graph bytes | All 225 eligible graph/reference pairs agree with retained scores and the frozen mean at paper precision. Of 250 recorded rows, 25 failed rows were excluded by the original analysis. No new FCI fit or language-model call. |
| Agent name controls | Reaggregate retained real/swapped per-scenario F1 rows; reconstruct the eligibility and losing-entry tally | Four agent summaries and the heterogeneous tally match. The earlier Causal-Copilot entry remains a different cohort/stage/scorer and is read back, not independently re-scored here. |
| CausalBench | Rerun the original summary producer over 586 retained cell results, including reported controls and predictions | No differences; four reproduced rows remain within the recorded tolerances. This re-merges retained evaluations, not raw interventions, and is not an independent evaluator implementation. |
| Companion comparison | Export the exact staged tree into isolation; run reproduction and all hash/reproduction tests | Recomputed JSON matches; four tests pass. Retained final graphs cannot independently establish the bootstrap stage attribution. |
| Stage, crash and label-following claims | Bind the existing diagnostic snapshots and frozen counts; recheck their interpretation boundaries | Prior evidence and qualifications retained. Full intermediate-state reconstruction and an independent endpoint reconciliation remain open. |
| MATMCD and reference facts | Frozen report/mapping integrity and interpretation review | Point versus interval distinction retained; reference provenance does not become ground truth. No fresh native run or licence determination. |
| Manuscript inventory | Generate anchored block/citation/number-key coverage | 42 source blocks and the numerical source crosswalk are indexed in `evidence-coverage.json`. Block inventory is not 42 independently reviewed scientific claims. |
| Public reader routes | Observe three public defaults, the advertised fork branches, both website roots and their same-origin links | Both roots and all 21 selected same-origin endpoints returned HTTP 200, with no queue deferrals. This is not a recursive crawl or browser/JavaScript evaluation. |
| Stable Crucis software | Exact staged-tree secret, package and publication-metadata checks, followed by full conformance attempt and bounded isolated probe | First three checks pass. Full conformance did not finish; the isolated test exceeded 45 seconds. No current full-suite pass claimed. |

The detailed generated inventory excludes manuscript prose duplication; its
anchors bind to the one canonical source. Full raw logs and private prompt-custody
mapping remain outside this repository and the submission ZIP. The sanitized
site/repository observations and bounded-test receipt are retained here.

## Findings and dispositions

**A01: Whole-paper public reproduction is incomplete (high confidence).**
The companion reproduces its particular retained-graph comparison. The research
ZIP contains frozen summaries, diagnostics and analysis code, but excludes full
run states, interaction logs and raw intervention arrays. The audited research
GitHub releases endpoint lists no releases; that is not proof no archive exists
elsewhere. Every affected claim must retain its actual available evidence level.
Disposition: scope clarified in READMEs and submission guide; public intermediate
graph reductions, raw-data acquisition pins and independent evaluator replay are
open work. No native/paid experiment or frozen contract change was authorized.

**A02: Stable framework conformance is operationally unresolved (high confidence
for the observation; root cause unknown).** At public source
`827b43cfd02dc9037c074adeda6512ade5d402a6`, the full gate remained in
`test_source_alias_filter_generation_and_consumer_cannot_inherit_cursor` for
several minutes and was stopped after preserving its partial log. A fresh test
invocation also exceeded a declared 45-second audit budget. The captured stack
was at `execution/owners.py:447`, SQLite `COMMIT`, while admission was being
processed. Competing machine load was not controlled. This is an incomplete
validation result, not proof of an infinite loop or a specific correctness bug.
Disposition: runtime untouched; retain the failure and route a focused storage,
content-size and liveness investigation to the subsystem owner. Do not weaken
validation or claim a newly validated framework commit. Active S5 work is excluded.

**A03: Public sites lag the implementation and submitted report (high confidence).**
The framework site still says execution/collection coordination is in design,
although the public default includes scoped S3/S4 implementations. The research
homepage still says checkpoint wording/citation/PDF work is open and presents the
checkpoint as the next deliverable. These are dated publication gaps; HTTP success
does not establish current content. Disposition: source-version observations
recorded; website/status amendments routed through `w5_requests.md`. No deployment.

**A04: Companion attribution and scope were too broad (high confidence).** Its
README attributed loss to the unmodified "review" and did not prominently separate
its refinement comparison from the whole Crucis paper. Disposition: changed to
"pipeline", added explicit scope and direct research/framework routes. Numerical
results and recorded inputs are unchanged. The gate identified existing pins on
the historical exporter and template. Their bytes remain unchanged in both
repositories. The proposed template/exporter update is retained as
`companion-export-disclosure.patch` for owner review and a deliberate repin.
The combined ZIP uses the already reviewed companion commit directly; do not
use the old exporter to overwrite its disclosure before that follow-up.

**A05: AI documentation and ZIP requirements were missing (high confidence).**
Instructor posts supplied by the author require a brief README contribution
statement, a structured summary with important prompts, and a ZIP upload. The
public assignment page still says to submit a repository link. Disposition: apply
the more specific, newer supplied instruction; add disclosure documents and a
source-only combined package with manifest and validation state. No claim that
the authenticated course interface or the pasted posts were independently read.
The author confirmed the disclosed important task families. Exact historical
messages/model versions remain incompletely recovered and are identified as such.

**A06: Effective scoring cohort deserves a clearer reader route (high confidence).**
The FCI re-score uses successful retained rows, not every public file. The paper
already says "evaluated semantic subset"; the audit now exposes the effective
cohort and original failures. Disposition: record it here and in the future
reproducibility map. Adding a new printed count to the frozen checkpoint is not
authorized; any revised numerical contract needs separate review.

**A07: Historical scientific uncertainties remain open.** The BND-08 specified
pre-cycle endpoint differs from its completed-final calculation; name-control
cohorts and scoring differ; paired completion selection differs from all-run
means; MATMCD's interval includes zero. These are preserved limitations, not newly
resolved defects. Any reconciliation must preserve original history and rules.

## Packaging and disclosure boundary

The combined ZIP includes separately named `causal-copilot-q1`, `cc-research`
and `crucis` trees, plus a root guide, manifest and validation receipt. It excludes
Git history, untracked/ignored files, credentials and the private research
assistance project. All code/test bytes come from explicit commits.

Because A02 blocks a validated Crucis documentation commit, only its `README.md`
and `AI_USE.md` are overlaid from the committed research repository's reviewed
`crucis-disclosure/` files. This is explicit in the archive manifest, including
original/replacement hashes and donor commit. It changes no runtime/test source
and is not represented as a committed or fully validated Crucis release. The
isolated framework documentation branch remains uncommitted pending its gate.

Public AI-use summaries describe substantive AI work, important prompt families,
available exact excerpts, human decisions, testing and limitations. They do not
include private tooling code, internal chat IDs, personal correspondence or an
invented complete transcript. Do not use vagueness to understate substantial
assistance. The report's archived PDF/source remain unchanged; the separate
`AI_USE.md` provides the allowed longer disclosure.

## Remaining order

1. Resolve A02 through the framework owner, preserving this failed/incomplete run.
   Check bounded storage and recovery behavior and rerun the exact acceptance gate.
2. Add reviewed, public intermediate-graph evidence and per-finding commands where
   disclosure/licence permits; validate them in an extracted source-only archive.
3. Recompute CausalBench evaluation from declared raw arrays/environment, and
   independently reconstruct the stage/label-following calculations. Treat missing
   inputs as gaps. No live model reruns without a separately approved plan/budget.
4. Review and publish source/README/site updates through the existing PR, CI and
   ownership process. Local readiness, remote availability and submission differ.
   Review the companion export patch and repin deliberately before regenerating
   that repository, so an old export cannot remove its current AI disclosure.
5. Preserve the actual code-submission receipt after the author uploads the ZIP.

The scope of this audit can be expanded, but none of these open items is made
green by agreement, source hashing or a successfully opened homepage.
