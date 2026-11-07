# AI use and human contributions

Tickets: DLV-05, DLV-06, DLV-07. Disclosure prepared 6 November 2026.

This project used AI extensively. ChatGPT/Codex assisted research planning,
software implementation, debugging, literature and evidence checking, manuscript
drafting, and simulated review. Earlier project handoffs also identify Claude
assistance. Exact model versions were not retained for every historical exchange.
AI-produced code and prose were revised through multiple iterations; this was
more than spelling correction or autocomplete.

## Human responsibility

Uzair Gheewala set the research direction, questions, scope and priorities;
approved designs and experimental plans; made scientific and editorial decisions;
challenged proposed framing and interpretations; edited the manuscript in
Overleaf; and selected and submitted the checkpoint. He remains responsible for
the submitted claims and code. These responsibilities do not mean every line was
manually written or independently inspected by a human. This statement does not
attribute authorship or validation to a mentor or to the AI reviewers.

## Substantive assistance and important prompts

The table summarizes important instruction families, including repeated design
and debugging exchanges. Summaries are reconstructions, not verbatim quotations.
Exact excerpts and one labeled editorial cleanup follow the table. The private research
assistance tooling is described by its function; its implementation and unrelated
private records are not needed to reproduce the public analyses.

| Area | Important prompt summary | Resulting work and checks |
|---|---|---|
| Research questions and controls | Identify what a final graph score cannot distinguish; separate data, names, layout, scoring and recorded stages; retain competing explanations and scope limits. | Controlled audit plans and interpretation boundaries. Historical plans, result files and the checkpoint contract retain the actual rules and limits. |
| Instrumentation and analysis | Record system identity, model calls and intermediate outputs without rewriting the original system; score retained graphs; compare paired runs and account for crashes. | Harness and analysis scripts, retained evidence and synthetic regression tests. Full native replay needs separately declared data and execution conditions. |
| Reusable auditing software | Design and implement separate system-connection, experiment, execution, measurement and finding contracts; use concrete examples, bounded work, failure/recovery cases and acceptance gates. | Standalone Crucis code and its own design/test records. This repository holds historical research, not the current framework implementation. |
| Literature and evidence | Read primary work, trace claims to passages, compare the closest overlapping work, and preserve contradictory evidence and access limitations. | Bibliography and `docs/paper/q1/lit_claims.json`, scoped review records and narrower claims. A citation key passing lint is not proof of entailment or a fresh full-text read. |
| Numerical integrity | Bind every printed scientific value to a named source, selector and operation; preserve the frozen numerical contract. | Registry, source hashes and checks covering 78 entries, 13 numerical sources and 19 frozen files. These are evidence readback checks, not independent native reruns. |
| Drafting and presentation | Improve framing, flow, section structure, transitions, citation placement and appendix navigation without expanding the supported claims. | AI-written suggestions and drafts, followed by substantial human revisions and section-by-section dialogue. Actual course LaTeX styles retained. |
| Adversarial and editorial review | Give specialist reviewers bounded investigations and sanitized packets; retain findings, no-finding results, disagreements and adjudications. | Recorded AI reviews, author-exposed rechecks and amendments. Shared models and correlated context limit independence; agreement does not prove truth. |
| Reproduction and delivery | Recompute available recorded results, test isolated installs/archives, inspect the PDF and prepare source-bound submission packages. | Commands and actual outcomes in repository receipts. Missing data, skipped tests and pending public updates remain visible. |

### Important prompt excerpts

The source label identifies the conversation in which the author gave the
instruction. Quoted snippets are verbatim unless marked edited.

| Area | Source | Excerpt |
|---|---|---|
| Research questions and controls | Continue W2 audit protocol | “Walk through rules fixed before exposure, threshold changes after seeing results, permitted amendments, and historical imports with uncertain timing.” |
| Instrumentation and analysis | Continue W2 audit protocol | “including how each output links to its premises, calculation, and comparison scope.” |
| Reusable auditing software | Continue W2 audit protocol | “Let’s choose the first S4 procedures and work through each one’s inputs, formula, when to withhold a result, and what evidence would qualify it.” |
| Literature and evidence | Checkpoint paper and workbench conversation | “Read its primary paper before drawing the distinction from an independent external-system auditor.” |
| Numerical integrity | Audit commit workflow and repo | “Freeze the checkpoint’s scope and evidence contract.” |
| Drafting and presentation | Checkpoint paper and workbench conversation | “Let's do the same short pass for flow and clarity while keeping the scope and linked numbers intact.” |
| Adversarial and editorial review | Audit commit workflow and repo | “build the reviewer system, and use the Crucis paper as the first test case” |
| Reproduction and delivery | Continue W2 audit protocol | “Report each against its expected value. Diagnose any mismatch to the line first.” |
| Milestone validation | Continue W2 audit protocol | “Walk through the held, inconclusive, corrected, and restricted cases end to end, then define each bundle’s acceptance and recovery gates.” |
| Commit workflow | Audit commit workflow and repo | “Local commits should happen automatically going forward.” |

Two additional paper-editing instructions shaped the balance between audit detail
and readable prose:

> “No rewriting or anything just review and assessment doesn't it seem a bit bloated to you?” (edited for spelling and concision)

> “the paper is not just supposed to be like outright writings of the claims”

The paper review retained the internal evidence links and checked which
qualifications needed to appear next to the claim. The excerpts represent the
work families and keep the disclosure focused on this project.

## How AI output was tested and challenged

The code uses synthetic tests, known-answer cases, evidence hashes, explicit
numerical selectors and isolated staged-tree checks. Recorded-result reproduction
is distinguished from rerunning the original model system. Scientific review
explicitly checked cohort and endpoint differences, completion-conditioned stage
comparisons, scoring-rule effects and uncertainty. Valid objections led to
corrections or narrower claims; historical unresolved issues were retained.

For the archived report, the build used XeLaTeX and BibTeX with the actual course
styles. All sixteen rendered pages were inspected, with no unresolved citations
or references and no overfull boxes. The archived-source receipt records the
exact PDF and inputs. Twelve focused checkpoint tests and eight staged-tree gates
passed. The broader repository suite reported 256 tests with 29 skips; those
skips do not establish reproduction of the omitted work.

Six explicit, exact-draft editorial lint dispositions cover grouped paragraph
attribution and structural prose counts. They are visible in the checker output,
invalidated by source edits, and cannot waive unchecked citations or undefined
number keys. Human reading was needed because automated rigor checks had missed
flow, framing and the difference between a ledger and a readable argument.

## Scope and remaining limits

This is a structured summary, consistent with the instructor clarification
supplied by the student that a structured summary including important prompts is
acceptable. It draws on the paper conversation, selected design/implementation
conversations and committed work records. The oldest segment of the W2 chat could not be retrieved in full because the chat tool could not return an oversized turn.
On 6 November, the author confirmed that these cover the important task families
he recalls. That confirmation does not recover missing historical message text.
Some older exact experiment-design/debugging prompts and model versions have not
been recovered; they are not fabricated here. The author should supplement any
important omitted task or instruction before representing the historical prompt
inventory as complete.

Language-model calls made by the causal-discovery systems during experiments are
separate from development assistance. Their identities, costs, requests and
available outputs belong to the experiment records, subject to the documented
access and data restrictions. No new paid campaign was run for this disclosure.

The post-submission audit and source ZIP do not certify universal scientific
correctness, independence of simulated reviewers or whole-paper native replay.
See `docs/paper/q1/POST_SUBMISSION_AUDIT.md` and the archive's review receipts for
the precise remaining checks. The author confirmed submitting the report and combined code ZIP. The
submission record identifies the local artifacts and the level of confirmation.
