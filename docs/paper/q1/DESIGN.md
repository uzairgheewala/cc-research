# Q1 checkpoint (DLV-05): design

Tickets: DLV-05 (owner, W1), DLV-07 (code link), DLV-11 (cited, not re-run), PRG-01 (framing). Written 31 Oct 2026 by W1.
Framing: program v3, section 2 (`claude/program-v3-2026-10-29.md`). Owned files: `docs/q1/*`, `docs/paper/q1/*`.

## 1. What is delivered on Fri 6 Nov

| Part | Graded by | Form |
|---|---|---|
| Title, abstract, introduction (intro paragraph, literature review, data) | mentor | the course LaTeX template (Overleaf project "DSC Capstone LaTeX Template", read-only link on the course's Q1 page), compiled to PDF |
| Link to a public GitHub repo with the code so far | TA | `causal-copilot-q1` (DLV-07), re-exported from the cc-research commit the paper quotes, CI green |

The paper is **the auditor paper**: an open protocol for auditing causal-discovery systems and the first audit of the field
under it, with Causal-Copilot as the worked case. Refinement v2 (endeavour B) is not a result of this paper; it appears
once, as the round-0 response, without numbers (failure mode 11.2 of program v3: the two papers must not claim the same
result).

## 2. Axes (each one is a choice made once, with its binding time)

| Axis | Values | Bound when | Chosen |
|---|---|---|---|
| Where text lives | Overleaf only / repo only / repo, mirrored to Overleaf | now | repo (`docs/paper/q1/report.tex`), uploaded to Uzair's Overleaf copy of the template for submission |
| How a number enters the text | typed / macro from a registry | now | macro only: `numbers.json` (file + JSON pointer + format) → `numbers.tex`; a lint rejects any other numeral |
| When numbers are read | at writing / at every build | every build | every build; `numbers.lock.json` records value and source sha256, so a changed source shows as a diff, never silently |
| Which source files count | anything on disk / tracked in git at HEAD | build time | tracked and unchanged against HEAD; anything else is flagged in the lock (`git_state`) and in the appendix |
| How a prior-work claim enters | from the cluster reports / checked against the paper | before the PDF | checked: `lit_claims.json` holds each claim, its key, the passage read, and a verdict from a reader who did not write the sentence |
| Sentence without a citation in section 2 | allowed / marked as ours | lint time | must end with `\ours` (prints nothing) or carry a `\cite`; the lint fails otherwise |
| Bibliography entries | from memory / from the publisher or arXiv page | before the PDF | only entries whose metadata a checker read on the primary page |
| Data facts (shapes, licences) | from `docs/q1/datasets.md` / from the JSON behind it / from the licensor | build time | shapes from `datasets/**/MAPPING.json` and `external/causalbench/*.npz.json`; licences from the licensor's page, cited |
| Benchmark audits (DLV-11) | re-run / cited | now | cited from their result files (AB-01, BEN-13); nothing re-run |
| Compile | Overleaf / local | each bundle | local XeLaTeX in the agent's container (the template's fonts installed there); Overleaf is the submission path |

## 3. The number path

```
result file (cc-research, tracked)  --pointer-->  numbers.json entry  --build_numbers.py-->  numbers.tex  (\newcommand)
                                                                                     \-->  numbers_table.tex (appendix A)
                                                                                     \-->  numbers.lock.json (value, sha256, git state)
report.tex uses only \N... macros for numbers  --lint_report.py-->  0 bare numerals outside the allowlist
```

- An entry is `{key, file, ptr, fmt}` or `{key, op: sub|share|pct, args: [...], fmt}`, where every arg is itself a
  file + pointer. No other arithmetic exists, so every derived number shows its inputs in appendix A.
- Literal counts that a table reports (e.g. "10 scenarios") are entries too, pointed at the file that counts them.
- The lint's allowlist is closed and each pattern has a reason: names that contain digits (F1, GPT-4o, L0-L4, S1/S2,
  Q1/Q2, CC BY 4.0, K562, RPE1, section numbers in `\ref`), and anything inside `\cite`, `\url`, `\href`, `\label`.

## 4. The citation path

1. Draft section 2 from `analysis/literature/agent_reports/` (clusters 1-9), `analysis/reports/pass6_literature_map.md` and
   `analysis/literature/bnd02/rep13_claims.md` (the REP-13 re-reads, which supersede the cluster text where they differ).
2. Extract every cited sentence into `lit_claims.json` (`id`, `keys`, `claim`).
3. Independent readers (separate agents that did not draft the text) open each paper and return, per claim: `confirmed`,
   `corrected` (with the fix) or `not supported`, plus the section and a short quote, and the paper's metadata.
4. Apply corrections; drop anything `not supported`. `reference.bib` is written from the readers' metadata.
5. `lint_report.py --cites`: every `\cite` key has a `confirmed` or applied `corrected` verdict; every sentence of
   section 2 has a `\cite` or `\ours`.

## 5. Failure modes, named before they happen

1. **A number drifts after it is written** (a result is recomputed). The lock diff shows it; the build prints the change.
2. **A number is right but from the wrong file** (two files hold similar values, e.g. BND-08 vs BLD-06 main control). Each
   claim names its ticket in the registry; appendix A prints file and pointer next to the value.
3. **An interval end is rounded the wrong way** (s37 found 0.111 vs 0.110). Formats are applied to the raw value once, in
   the builder; never by hand.
4. **A source file is not in git** (CausalBench shapes live in `external/`). Allowed only with `git_state: excluded` and its
   manifest hash; flagged in appendix A.
5. **A citation is real but says something else** (REP-13 corrected 17 of 72). The independent read is the gate, not the
   draft.
6. **A bibliographic detail is wrong** (venue, year, author order). Metadata come from the primary page only.
7. **Name and layout controls described as novel when they are not** (CARE has name permutation; Kitson and Constantinou
   have column order). Section 2 says what is new: the combination (names and layout and stage traces) applied to deployed
   systems and to benchmarks, under pre-registration.
8. **The template does not compile outside Overleaf** (XeLaTeX fonts XCharter, Arial, Fira Code). In the container:
   XCharter and Fira Code from Debian packages; Arial is substituted by a local copy of Liberation Sans renamed to Arial
   (sans text appears nowhere in the body). Only the bibliography style differs: the template's `dsc180bibstyle.bst` is a
   modified econ.bst; the container build uses CTAN's `econ.bst` until the template's file is copied in, so reference
   formatting may differ slightly from Overleaf's.
9. **The code link points at a repo that does not match the paper.** Re-export from the quoted commit, then CI green, then
   submit; the paper prints the cc-research commit.
10. **Checkpoint scope creep** (results sections). Results go to the final-report outline in `docs/q1/checkpoint_skeleton.md`.
11. **Two papers claim one result.** Refinement v2 numbers stay out of this paper.

## 6. Bundles (each verifiable in one run of `make.sh`)

| Bundle | Builds | Must show |
|---|---|---|
| B1 Template, registry, lint | template vendored (`report.tex` replaced, style files kept); `numbers.json`, `build_numbers.py`, `lint_report.py`, `make.sh` | `build_numbers.py` resolves every entry against the files on the device; lock written; lint passes on a stub; PDF compiles |
| B2 Text | title, abstract, introduction, data section, code link; data table generated from the MAPPING files | lint 0 bare numerals; every macro used is defined; appendix A lists every number with file and pointer |
| B3 Literature | section 2 drafted; `lit_claims.json`; independent check; `reference.bib` | every `\cite` key confirmed or corrected-and-applied; every section-2 sentence has `\cite` or `\ours`; no unresolved citation in the log |
| B4 Hand-over | PDF; `docs/q1/checkpoint_skeleton.md` re-cut; export dry run of the Q1 repo to a scratch folder; commit message | PDF compiled from the device's files; the export dry run reproduces exactly; Uzair's steps listed (commit, re-export, CI, Overleaf upload, submit) |

## 7. What Uzair runs (no agent can)

1. Commit cc-research (`docs/commit_msgs/q1_checkpoint_cc-research.txt`).
2. `py -3 tools\export_q1.py`, then commit and push `causal-copilot-q1`; check that CI is green.
3. In Overleaf: copy the course template, upload `report.tex`, `reference.bib`, `numbers.tex`, `numbers_table.tex`,
   `data_table.tex`; recompile; check the PDF matches `docs/paper/q1/build/report.pdf`.
4. Submit the PDF and the repo link on Gradescope.
