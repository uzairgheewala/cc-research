# W1 hand-off: the Q1 paper (DLV-05 checkpoint, DLV-06 final) — resume point

Tickets: DLV-05, DLV-06, DLV-07, DLV-11, BND-13, PRG-01
Written 3 Nov 2026 by W1 (the paper workstream, a Claude chat) so the work can continue in Codex and come back.
**This file is the single resume point.** A session that picks up W1 reads it first, works from section 6, and before
ending appends to section 9 and updates section 2. Anything not here or in the files it names is not part of W1's state.

**Current checkpoint boundary (3 Nov, stage 1):** read `CHECKPOINT_CONTRACT.md`
and run `check_checkpoint_contract.py` before editing or migrating paper inputs.
Crucis is the selected name. The checkpoint stays on the frozen pre-package
sources while subsystem work proceeds; no live audit-tree lock or paper port is
implied. This adopted checkpoint contract takes precedence over older port
examples and provisional naming in the historical handoffs it references.

**Stage-2 cutover, 3 Nov:** Crucis now lives in the sibling `../crucis` repository,
under the Python namespace `crucis_causal` (distribution/command `crucis-causal`). `docs/migrations/crucis-separation.json`
records the verified extraction and lifts the initial commit hold. References
below to that hold describe the earlier handoff; current root AGENTS.md governs
automatic local commits. Historical audit results remain at their research paths;
the paper has not been ported. Current subsystem work continues in Crucis.

---

## 1. What W1 is and owns
- **The Q1 paper is the auditor paper** (program v3, 29 Oct): an open protocol for auditing causal-discovery systems and
  the first audit of the field under it, with Causal-Copilot as the worked case traced stage by stage. Q2 (another
  workstream) is the system that rebuilds Causal-Copilot; its results (refinement v2) do **not** appear in this paper,
  except one sentence saying a companion project exists. Two papers must never claim the same result.
- **Owned files:** `docs/paper/q1/**`, `docs/q1/**`. Everything else belongs to another workstream:
  - W2: the audit package (`audit/`, `tests/test_audit_*`), protocol, and its move to its own repository (in progress, 3 Nov).
  - W3: the system / fork branches / `analysis/refinement_*`.
  - W5: tickets (`tracker/`), program doc, site, Slack, shared contracts. **Ticket and contract changes go to W5**: write
    the request in `docs/paper/q1/w5_requests.md`, never edit `tracker/catalogue.py` yourself.
- **Deadlines:** checkpoint Fri **6 Nov 2026** (title, abstract, introduction = intro paragraph + literature review + data;
  LaTeX on the course's Overleaf template; PDF on Gradescope; plus the public code-repo link). Final report Fri 4 Dec.

## 2. State on 3 Nov 2026

**5 Nov author readability revision.** The next local candidate is
`build/report.pdf` (16 pages) and its matching `build/overleaf_upload.zip`.
It starts from Uzair's Overleaf export, keeps the course author–year style,
and reorganizes the introduction and appendix around the audit questions.
`verify/checkpoint-editorial-review-2026-11-05.json` binds both assessments and
the exact revised artifacts. The new rubric covers the mentor's four questions
and the reader's job in each section. The earlier fast-track receipt below
identifies the historical PDF in Git. Use XeLaTeX with `report.tex` in Overleaf.
The current candidate is for author review.

**5 Nov course checkpoint fast track.** The preceding locally reviewed package
is `build/report.pdf` (16 pages), with a matching `build/overleaf_upload.zip`.
`verify/research-workbench-checkpoint-2026-11-05.json` binds source, evidence,
review history and artifacts. The earlier reviewed package remains in build
history. The designated DLV-07 course code link remains
https://github.com/uzairgheewala/causal-copilot-q1. Its offline retained-graph
comparison was rerun successfully. The framework is at
https://github.com/crucis-lab/crucis. Stage-specific attribution uses separate
research evidence. Exact Gradescope time, any additional mentor requirements
and submission remain owner actions.

The abstract now reports the paired bootstrap finding on completions.
The paper scopes the name-control tally and benchmark scores to their
observed settings, distinguishes recorded capture from causal attribution,
and credits overlapping controls and measurement in Heuresis, Causal-Audit,
ACDB and TCD-Arena. BND-08 stays descriptive because the specified pre-cycle
endpoint and the implemented completed-final calculation differ. The number
registry, input bytes and thresholds remain frozen.


**Latest, structured-workflow continuation (3 Nov 2026):** a locally validated,
independently reviewed checkpoint is now built: `build/report.pdf`, 16 pages,
SHA-256 `55b41a2ba70b0ec5c7b5157ecc26107fbd76c997f27ff5246fc1d92d51ce9e7c`.
`verify/research-workbench-review-2026-11-03.json` binds source, PDF, Overleaf
bundle, findings, checks and remaining decisions. It is not human-approved,
published or submitted. The reusable system is in the separate research-workbench
project; canonical manuscript ownership remains here. No registry/source/value or
protocol threshold changed. This authorized kickoff supersedes the earlier wait.

**Previous preparation state:** the initial table below is historical. Repositories and sites are now
public, with local milestone commits enabled. The current branch
`paper/q1-checkpoint-corrections` holds a provisional interpretation correction
draft. Uzair asked to stop further paper work until he introduces his structured
approach. This takes precedence over the old P0 task ordering. Biwei Huang has
been removed from the author block at his instruction. No new mentor identity is
implied. The paper is not submission-ready.

### Historical baseline (12:15 PT)
| Item | State |
|---|---|
| cc-research HEAD | `cf536c1` (27 Oct). **Nothing committed since**; W1's files are untracked/modified in the work tree |
| `build_numbers.py --check` | 78 entries match the lock |
| `lint_report.py` | 0 errors, 0 warnings; 74 number keys used; 42 citation keys |
| `build/report.pdf` | 15 pages, compiled 31 Oct with XeLaTeX in Claude's container (CTAN `econ.bst` standing in) |
| Number sources | all tracked-clean at `cf536c1`, except `external/causalbench/dataset_{k562,rpe1}_filtered.npz.json` (outside git by design, hashed in `manifests/excluded/`) |
| Q1 code repo | `github.com/uzairgheewala/causal-copilot-q1`, public, CI "reproduce" green on `43d0c75` (27 Oct). A dry-run export from `cf536c1` (31 Oct, scratch folder) reproduced exactly and differed only in the README's commit line and export time |
| Patch w1-01 | applied: `docs/q1/checkpoint_skeleton.md` re-cut; BND-13 repinned; verify 0 problems, snapshot regenerated (31 Oct) |
| Emails in the author block | **empty placeholders** (`\studentemail`, `\mentoremail` in `report.tex`): Uzair fills them |
| W2's corrections to the paper (section 5) | **not yet applied** — first job of the next session |
| Heuresis positioning (section 5.5) | **not yet checked against the paper** |
| Project name | **Crucis** selected by Uzair on 3 Nov; manuscript title update belongs to paper corrections |
| Checkpoint scope/evidence | **Frozen** by `CHECKPOINT_CONTRACT.md` and `checkpoint_contract.json`: 78 keys, 13 numerical sources, 19 pinned files including registry/checker and diagnostic snapshots. This is not submission completion |
| Diagnostic preservation | `checkpoint_evidence/` holds the recomputed stage/cohort receipt and legacy MATMCD report with capture provenance; neither becomes a new paper-number source |

## 3. Rules (as of 3 Nov; AGENTS.md at the repo root wins where it is newer)
1. **Commits.** Root `AGENTS.md` (3 Nov) authorizes *local* milestone commits through `tools/skills/milestone-commit/SKILL.md`
   and `tools/commit_gate.py`, **but a temporary migration hold forbids any commit until the audit package is separated
   into its own repository** (see `_repo_migration/2026-11-03/PROGRESS.md`). Until the hold is lifted: no commits; keep
   the message in `docs/commit_msgs/q1_checkpoint_cc-research.txt` current. Never push, publish, merge, or rewrite history.
2. **Edits to pinned or shared files** go through a patch script in `jobs/patches/` (W1's are named `w1_NN_*.py`, so they
   never collide with W5's `sNN` numbers) with a hash guard on the old bytes, then: compile check, relevant tests with
   `--out` outside the repo, `python tracker/verify.py` (repin only W1's own evidence, after reviewing the diff, with
   `--repin ID`), `python tracker/trace.py check`, and `python tracker/snapshot.py` **last**. Files only W1 owns and that
   no ticket pins (`docs/paper/q1/**` today) can be edited directly.
3. Never open or print `../Causal-Copilot/.env`. Spend no API credit (no `cc.ps1` live jobs). `#causal-discovery` gets
   drafts only (W5's job). Don't rely on answers from Prof. Huang's group.
4. **Every number in the paper comes from a result file named next to it**: through `\nm{key}` and `numbers.json` only.
   `lint_report.py` enforces it (bare numerals and number words from "two" up fail).
5. **No literature claim without a citation, each checked against its paper** by a reader who did not write the sentence
   (`lit_claims.json`). New citations need the same check before they enter `reference.bib`.
6. Reply style Uzair wants: open with "where we are now", close with "where we're going"; plain language; derive metrics
   step by step; full design first, then bundles each with a must-show list.
7. Python: `tools/python.ps1` selects the workspace interpreter (`.tooling/venv`, Python 3.12, NumPy). Use `-B` (no
   bytecode). `py -3` and `cc.ps1` are Uzair's.

## 4. The paper's machinery (all in `docs/paper/q1/`)
| File | What it does |
|---|---|
| `report.tex` | the checkpoint in the course template: title, abstract, code link, Introduction (`sec:intro`), Prior work (`sec:prior`), Data (`sec:data`, Table 1), Code, references, Appendix A (`app:numbers`) |
| `style/dsc180reportstyle.sty` | the template's style file, byte-identical (sha256 `8b6a2455…`). The template's `dsc180bibstyle.bst` is **not** here (could not be copied byte-exactly); builds use CTAN `econ.bst`; Overleaf uses the real one |
| `numbers.json` | the registry: `{key, file, ptr, fmt}`, optional `re` (number inside a pre-registered text field), or `{key, op, args, fmt}` with ops sub, div, add, len, min, max, sum, mean, count_true, count_notnull; an arg may be `{"key": k}`. Pointers: JSON pointer + `*` (all children), `[k=v;k2=v2]` (first list item matching), `?k` (optional key) |
| `build_numbers.py` | resolves the registry from the cc-research root; writes `numbers.tex` (`\nm` definitions + `cc.head`), `numbers_table.tex` (Appendix A), `numbers.lock.json` (value, source sha256, git state); `--check` exits 1 on any drift |
| `lint_report.py` | numerals, number words, undefined/unused keys; every `\cite` key has a `confirmed`/`corrected-applied` claim and a bib entry; every sentence of `sec:prior` has `\cite` or `\ours` (prints nothing: marks our own statement) |
| `lit_claims.json`, `verify/` | 38 literature claims (23 confirmed, 15 corrected and applied) + 9 data facts; `verify/in_part*.json` (drafts), `out_part*.json` (checkers' verdicts, quotes, BibTeX) |
| `reference.bib` | 42 entries, metadata from the primary pages only |
| `data_facts.md` | licences and citations of every dataset, read at the licensor |
| `build_paper.py` (any OS) / `make.sh` (bash) | numbers → check → lint → XeLaTeX/BibTeX → `build/report.pdf`; `build_paper.py --overleaf` writes `build/overleaf_upload.zip` |
| `DESIGN.md` | axes, binding times, failure modes, bundles (31 Oct) |
| `CHECKPOINT_CONTRACT.md`, `checkpoint_contract.json`, `check_checkpoint_contract.py` | adopted checkpoint scope, exact evidence baseline and non-refreshing check; HEAD may legitimately advance after the split |
| `checkpoint_evidence/` | migration-safe diagnostic snapshots; origin/hash/status in the checkpoint contract |
| `w5_requests.md` | open requests to W5 and W2 |
| `docs/q1/checkpoint_skeleton.md` | index to all of this + the final-report outline |

Build: `python -B docs/paper/q1/build_paper.py` (from cc-research). XeLaTeX needs the fonts XCharter, Arial, Fira Code; if they
are not installed on Windows, use `--no-pdf --overleaf` and compile in Overleaf.

## 5. What other workstreams found that the paper must take in (read before editing)
Source: W2's notes of 31 Oct (claude.ai project doc `claude/w2-rebase-2026-10-31.md` §7, also written into
`claude/q1-checkpoint-2026-10-31.md` §2a). Summary, with what to do:

1. **"Causal-Copilot's review lowers adjacency F1 0.584 → 0.321" misattributes the loss.** On fork main (22 completed runs)
   the drop is almost all in the **bootstrap step** (S0 → S1: −0.270 [−0.327, −0.200]), which makes no model call; the LLM
   review step (S1 → S2) is +0.007 [−0.027, +0.042]; KCI and the cycle step change nothing measurable. BND-08's gpt-4o runs
   agree (−0.281 bootstrap, −0.003 review). The completed-only S0 mean is also 0.584, so the two numbers stand.
   **Do:** in the abstract and the intro bullet, say "refinement" and attribute the loss to the bootstrap step, not the
   model's review. If you print the stage numbers, they need registry keys pointing at a file: the package report for
   `causal_copilot@main` (K10 stage effects) under `audit/results/rerun_v1/` — on 3 Nov it sits at
   `audit/results/rerun_v1/reports/causal_copilot_main/` (the pre-C1 layout: `reports/`, `@`→`_`; C1 will move it); an untracked or about-to-move source is flagged in the lock
   and Appendix A. A wording-only fix with no new number needs no new key.
2. **The name-reliance sentence pools unlike measurements.** Causal-Copilot's 0.167 is directed F1 of S3 (the graph handed
   to the cycle step) under the committed-marks rule, on the q1s2 suite; the agents' numbers are final-graph F1 under the
   expectation rule on ca-ab06; the two share 0 of 10 scenarios. The claim stands as P9 (pre-registered that way). **Do:**
   say what Causal-Copilot's number measures, and that its runs predate the 14 Oct pre-registration (it was declared
   "already measured"), so under protocol v1 its K04 verdict is exploratory.
3. **MATMCD below its data-only graph.** K07 fires on P10's point rule (confirmatory), but the interval is [−0.066, 0.001]:
   the upper end touches zero. **Do:** say "below on the point estimate", or print the interval through a registry key.
4. **81 of 101** reproduces exactly; the pre-registered verdict is BND-08's M3 (K11's own threshold is exploratory). **Do:**
   name it as BND-08's pre-registered test.
5. **Heuresis (arXiv 2610.22846; found 3 Nov by the migration session).** `docs/research/heuresis-scope-and-auditor-positioning-2026-11-03.md`
   and the competitor register in `docs/research/`. Its conclusion: Heuresis is a benchmark plus its own harness, not an
   external-system auditor; shared tracing methods do not erase the framework contribution; do not claim global
   first/universal coverage. **Do:** check `sec:prior` and the intro against it. The sentence "We found no stage-by-stage
   evaluation of a deployed causal-discovery agent under name and layout controls\ours" and "none applies a common set of
   controls to the systems that are now deployed\ours" may need narrowing, and Heuresis likely needs a citation, checked
   against its paper like every other entry (add a claim to `lit_claims.json`, verdict from an independent read).
6. **CausalBench wording in program v3 §2.3** is wrong (W5's doc, not the paper): the 7–14% "placement share" is what
   choosing strongly perturbing *parents* alone earns; P1 (≥ 0.5) fails. The paper already cites P3 (0.90–0.95 of the test
   split's total-effect ceiling) and the FOR result instead. Nothing to change in the paper.
7. **CausalArena layout and CausalBench stay benchmark properties** (DLV-11), agreed with W2: K06 is clear for PC/GES/GIES
   under the expectation rule; the FCI gain (0.221) belongs to the forced-choice, index tie-break scoring. The paper already
   frames it that way.

## 6. Work queue (in order)
### P0 — before Fri 6 Nov (the checkpoint)
| # | Task | Must show |
|---|---|---|
| P0.0 | Read `CHECKPOINT_CONTRACT.md`; run `check_checkpoint_contract.py` before paper edits or package moves | all 78 keys covered exactly once; frozen sources/selectors/formats and lock values match; no implicit re-freeze |
| P0.1 | Apply section 5 items 1–4 to `report.tex` (abstract, intro bullets, contributions). New numbers only through new registry keys | lint 0 errors; `build_numbers.py --check` passes after a rebuild; the lock diff lists only added keys (no existing value changes); the changed sentences listed in section 9 |
| P0.2 | Heuresis check (section 5.5): read the positioning doc and Heuresis itself; narrow the `\ours` novelty sentences if needed; add a checked citation | `lit_claims.json` has the Heuresis claim with location, quote and an independent verdict; `reference.bib` entry from the primary page; lint passes |
| P0.3 | Build | `python -B docs/paper/q1/build_paper.py` (or `--no-pdf --overleaf` + Overleaf compile) gives a PDF with no undefined references; page count and any layout changes noted |
| P0.4 | Hand Uzair the submission steps (section 7) | — |

### P1 — the port to the audit package (after W2 is green; not for the checkpoint)
Gate: W2's C1 (paper contract v1.1: folders named exactly by audit, findings addressed as
`certificate.json#/body/findings/[id=K04]/effect/point` with `verdict`, `label`, `label_rule`, `margin` beside it) and C2
(certified `round@ca-ab06` for the P9 keys; `versions@causal_copilot-bld06-vs-main` for the `cc.*` keys), the Windows test
run, W5 adopting protocol v1.1, and the package's move to its own repository.
1. W2 writes `port_map.json` (key → `{file, ptr, fmt}` or `"stays"`). W1 does not ask W2 to edit `docs/paper/q1/`.
2. **New design item for W1:** after the split, package outputs live in a *sibling repository*. `build_numbers.py` resolves
   every file against the cc-research root today. Add a per-entry (or per-source) `repo` field naming a root relative to
   cc-research's parent, record each repo's HEAD in the lock, and print it in Appendix A. Design it first (axes, failure
   modes: moved roots, untracked outputs, two HEADs), then a patch.
3. Apply the map, rebuild; every value change is explained or the port stops; then update the protocol paragraph to the
   adopted protocol (regimes incl. `K`/`none`, verdict set incl. `not_applicable`, confirmatory/exploratory labels printed
   beside each finding).
Keys that stay on their current sources: `ab01.*`, `ben13.*` (DLV-11), `s1.*`, `s2.*`, `cb.*`, `ab06.p9.threshold`.

The adopted 3 Nov checkpoint contract keeps ALL existing checkpoint keys on their
current sources for this submission. Adding a key or performing the later port
requires an explicit contract revision with a reviewed rationale and retained
baseline; it is not a side effect of extracting the package. Existing Git HEAD
and lock Git-state metadata may update without changing the frozen evidence.

### P2 — final report (4 Dec, DLV-06; outline in `docs/q1/checkpoint_skeleton.md`)
Protocol v1.x (DLV-08), the package (DLV-09), results per system (DLV-10), benchmark appendix (DLV-11), limits; the
validation battery of planted faults if W2 builds it (it lets the paper say each finding kind fires on its planted fault
and never on its null twin). DLV-07 final export with the package included (decision on which recorded data ship).

## 7. Uzair's submission steps (checkpoint)
1. Fill `\studentemail` and `\mentoremail` in `report.tex` (or tell the session the addresses).
2. Commit cc-research once the migration hold is lifted (message `docs/commit_msgs/q1_checkpoint_cc-research.txt`). If
   the hold is still on by 6 Nov, the paper is still valid: its numbers are read from files unchanged since `cf536c1`,
   which is the commit it prints.
3. Re-export the Q1 repo only if its content should change (`py -3 tools\export_q1.py`, commit, push, CI green); the
   current public repo already reproduces the Causal-Copilot comparison and its CI is green.
4. Overleaf: copy the course template (read-only link on the course's Q1 page), replace `report.tex` and
   `reference.bib`, add `numbers.tex` and `numbers_table.tex` (`build_paper.py --overleaf` zips exactly these), recompile,
   compare with `build/report.pdf`.
5. Gradescope: the PDF and `https://github.com/uzairgheewala/causal-copilot-q1`.

## 8. Where the inputs are
- Program and contracts (claude.ai project docs; not on disk unless snapshotted under `docs/project_snapshots/`):
  `claude/program-v3-2026-10-29.md` (§0–2 framing), `claude/q1-checkpoint-2026-10-31.md` (W1↔W2 contract, §2a W2 notes),
  `claude/w2-rebase-2026-10-31.md` (protocol v1.1, paper contract §6), `claude/audit-package-build-2026-10-31.md`.
  This file carries everything W1 needs from them.
- On disk: `AGENTS.md`, `docs/REPO.md`, `_repo_migration/2026-11-03/PROGRESS.md` (migration state), `audit/PROTOCOL.md`,
  `audit/results/rerun_v1/` (W2's 14 audits), `docs/research/` (competitor review, Heuresis), the literature clusters
  `analysis/literature/agent_reports/`, `analysis/reports/pass6_literature_map.md`, `analysis/literature/bnd02/rep13_claims.md`.

## 9. Session log (append; newest last)
- **31 Oct (Claude, W1):** designed and built the checkpoint (B1 template/registry/lint, B2 text, B3 literature with
  independent checks, B4 PDF + skeleton re-cut + export dry run + commit message); wrote the W1↔W2 contract doc.
- **3 Nov (Claude, W1):** verified state (section 2); added `build_paper.py` (cross-platform build, Overleaf bundle) and this
  hand-off; folded in W2's notes, the 3 Nov commit policy and migration hold, and the Heuresis finding. No paper text changed.
- **3 Nov (Codex, organization stage 1):** adopted the Crucis checkpoint scope/evidence contract at Uzair's instruction;
  captured 78 existing registry keys, 13 source hashes and 19 frozen files. Added a read-only checker and migration-safe
  diagnostic snapshots. Recomputed stage/cohort facts with the existing `rebase_facts.py`; its stored comparison/grid
  readback is not a fresh rerun of all historical comparisons. Updated this handoff/kickoff and coordination requests.
  No manuscript, registry, existing number value, protocol, active subsystem code or tracker status changed. The known
  scientific wording corrections, Heuresis check and final PDF remain pending. Verification receipt is recorded beside
  the migration progress log after the stage checks. No commit: the user-required separation hold remains active.
  Checks passed: contract (78 keys / 13 sources / 19 frozen files), report lint (0 errors / 0 warnings), five scratch-copy
  integrity/compatibility probes and targeted secret scan (9 files, 0 findings). Tracker verify: 259 items, 151 done,
  0 reopened/problems; trace: 0 errors, 3 existing warnings (BLD-11 review and the known unrecorded prod delivery).
  Snapshot `06bf0b4e15f7` regenerated and checked. No new ticket was marked done and no evidence was repinned.
- **3 Nov (Codex, organization stage 2):** verified standalone Crucis installation with research imports blocked;
  recomputed all 1,298 historical comparisons within 0.001 and verified 28 historical/fresh certificates. Moved the
  inventoried runtime/docs/package tests to `../crucis`; retained research outputs and B5 modules. The cutover receipt
  lifts the commit hold. Added a CI/staged-tree route for the two pinned data-shape summaries without changing the
  frozen registry or numerical sources. The manuscript corrections and PDF remain pending; source/commit receipts
  are in the migration log. Root policy now authorizes automatic local commits after ready milestones.

- **3 Nov (Codex, post-publication preparation):** verified manually sent Slack
  announcements and saved a subsystem rehearsal sheet. On local branch
  `paper/q1-checkpoint-corrections`, prepared provisional Crucis framing and
  interpretation fixes: bootstrap versus model review; unmatched name-control
  cohorts and exploratory Causal-Copilot status; MATMCD point estimate and interval;
  BND-08 pre-registration; implemented versus proposed scope and repository roles.
  Removed unsupported global-first claims. No frozen registry/source/value changed.
  Lint passed with 0 errors/warnings (74 used keys, 42 citations); all 78 numbers
  and the checkpoint contract passed. Heuresis was re-read at the primary v1 paper
  (https://arxiv.org/html/2610.22846v1); no new citation entered the bibliography
  because its independent-reader gate remains pending.
  A local PDF attempt failed before XeLaTeX at the missing-template bibliography
  fallback: kpsewhich's output did not resolve to a usable econ.bst path. No fresh
  PDF was produced. The historical tracked PDF and generated number artifacts were
  restored byte-for-byte; the attempted build inputs/bundle are archived outside
  the repository under `_repo_migration/2026-11-03/paper-build-attempt/` and must not
  be treated as a current PDF or submission bundle.
  Uzair then requested a new structured paper workflow and removal of Biwei Huang
  from the author block. Applied the author change, kept this correction draft
  local for review, and stopped further paper development. No submission, new paid
  campaign or paper publication occurred. Await Uzair's approach before continuing.

- **3 Nov (Codex, structured workflow, DLV-05/DLV-06):** built the separate generic
  evidence/argument/review system and exercised fresh-context reviewer calibration
  before applying it here. Initial scientific reviewers covered correctness,
  identification/statistics, experimental design, closest work, reproducibility,
  significance, exposition and skeptical synthesis. Same-model correlation and
  actual access limits are recorded. Independent supplied-byte reproduction
  resolved all 78 numeric entries; no fresh raw-run/native campaign was run.
  Six reporting/scope findings were dispositioned and rechecked: conditional M3
  denominator, M3 endpoint mismatch, reference-overlap optimality wording, omitted
  Heuresis comparison and abstract coverage. Overlapping findings are retained.
  Added independently primary-read Heuresis and Causal-Audit references (C39/C40),
  a connected contribution argument and interpretation appendix.

  **New scientific boundary:** the BND-08 pre-run header describes S3, but the
  M3 calculation consumes completed final-output stability N1 counts and classifies
  adjacency, not directional agreement. The text now reports the informative
  subset and retained post-review pair state, discloses the mismatch and treats
  the counts descriptively. This fixes the reporting claim; it does not repair or
  amend the historical implementation/protocol. Any confirmatory endpoint claim
  requires separate authorized reconciliation. W5 request 10 records the handoff.

  Downloaded the actual course template source through its read-only Overleaf
  link. Existing .sty matches; actual .bst now retained with original notices.
  Replaced destructive/fallback building with scratch generation, strict template
  hashes, bounded reference convergence and rollback on late output failure.
  Independent failure injection found and verified a promotion-consistency fix;
  `verify/test_build_transaction.py` passes. MiKTeX dependencies and the official
  Fira Code face were installed locally; no template font substitution was used.
  PDF and self-contained Overleaf bundle use identical six input files; all 16
  pages rendered and inspected, no overfull boxes or unresolved cites/references.
  Preprint/unpaginated bibliography warnings and inherited template setup warning
  are recorded rather than filled with invented metadata. Historical PDF retained.

  Final scientific body is byte-identical to the source independently rechecked
  at SHA-256 `69e1ea438b7b7241e7267cfe27f531529bedf1438a28be64db57ba755d45c93d`;
  root separately verified preamble-only widow/orphan changes and rendered output.
  The project-local typed release preserves all reviews/dispositions and explicit
  limits; private packets remain outside this publishable source tree. The full
  legacy citation corpus was not freshly reread; existing verification records
  and their access limitations remain authoritative for those reads.

  Frozen checks pass: 78 keys, 13 number sources, 19 files; number values match;
  lint 0 errors/0 warnings, 74 used keys and 44 citation keys. Generated changes
  are HEAD provenance from historical cf536c1 to build base aef6492 plus platform
  line endings. Course dates confirmed publicly (6 Nov checkpoint, 4 Dec final);
  exact times remain unverified because Gradescope redirects to UCSD login.
  Author block remains Uzair only; no replacement mentor inferred. No tracker,
  site, Slack, protocol or remote publication/submission changed.

- **5 Nov (Codex, checkpoint fast track, DLV-05/DLV-07):** reconciled the
  checkpoint assertion inventory and material literature comparisons, ran
  three fresh scoped reviews and two separate exposed rechecks, then narrowed
  the remaining wording and inspected the actual course PDF. Original
  reviews, dispositions and detailed packets remain project-local. The
  research verification receipt binds the final candidate and specifies
  coverage, independence and scientific limits. No live run, protocol
  amendment, change to frozen evidence, remote publication or submission.

- **5 Nov (Codex, author readability revision, DLV-05/DLV-07):** built the
  Overleaf export and used the same versioned reading rubric on it and the
  revision. The paper now gives readers named questions, a compact level list,
  an appendix route and a stage locator. The evidence freeze and the number
  lock pass. The revised package was built locally with XeLaTeX and BibTeX.
  All pages were inspected and the six ZIP inputs match the PDF build.
  The judgment is an exposed editorial recheck. The literature paragraph
  about language models is the remaining readability finding.
