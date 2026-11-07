# DSC 180A checkpoint code submission

Tickets: DLV-05, DLV-07. Prepared 6 November 2026.

Upload the combined source ZIP, as required by the newer instructor clarification
supplied by Uzair. The public assignment page still mentions a repository link;
the supplied clarification is more specific. No upload or course acceptance is
performed by the packaging command. The report has already been submitted,
according to the author, using the archived PDF.

## Contents and reader route

| Directory | Purpose | What it can reproduce |
|---|---|---|
| `causal-copilot-q1/` | Small companion comparison with retained graphs and data | Its recorded original/refinement comparison, offline, with four hash/reproduction tests. It does not reproduce the whole Crucis paper or locate intermediate-stage loss. |
| `cc-research/` | Canonical paper source, inspected PDF, historical evidence and analyses | Frozen numerical readback, archived build verification, retained-score reaggregation and declared analysis paths. Full intermediate-state/native replay is not self-contained. |
| `crucis/` | Public S1–S4 auditing framework source with declared disclosure overlay | Install/CLI/package checks and included synthetic conformance tests. A full current conformance attempt is incomplete; the exact issue and time-bound probe are disclosed in `VALIDATION.json`. |

The root `MANIFEST.json` binds the included source and guide/validation files to
their hashes, source commits where applicable, and any explicit overlay.
`VALIDATION.json` states actual
tests, gaps and scope. Each repository includes `AI_USE.md` and a short README
statement distinguishing AI assistance from human decisions. The private research
assistance tooling and its conversations are excluded.

Use separate environments if dependencies conflict. For the companion:

```sh
cd causal-copilot-q1
python -m pip install -r requirements.txt
python -B run.py reproduce
python -B run.py test
```

For the research record, preserve the folder name `cc-research`:

```sh
cd ../cc-research
python -m pip install -r requirements-ci.txt
python -B tools/check_checkpoint_ci.py
python -B docs/paper/q1/build_numbers.py --check
python -B docs/paper/q1/verify/verify_checkpoint_release.py
```

The CI helper reconstructs only two pinned CausalBench metadata sidecars from
tracked copies if absent. It launches no experiment. To build a new PDF candidate,
install XeLaTeX/BibTeX and the course template dependencies, then follow the
archived checkpoint README. The existing inspected PDF is already included.

For the framework:

```sh
cd ../crucis
python -m pip install .
python -m crucis_causal --help
python -B tools/package_check.py
```

The full development gate is documented in the framework README. Its incomplete
result in this audit must remain visible; successful CLI/package checks do not
supersede it. No paid/native scientific execution is needed for these commands.

## Reproduction limits

The [audit report](audit/2026-11-06/REPORT.md) maps findings to the checks actually
performed. FCI re-scoring additionally needs the CausalArena reference files under
`external/causalarena/`, with the exact hashes in the coverage receipt. They are
public source data, but are not included in this source ZIP. Full stage attribution
needs retained intermediate states; CausalBench raw evaluation needs the filtered
expression/intervention arrays and evaluator environment. Their hashes and
analysis code do not substitute for the inputs. No newly executed model campaign
or whole-paper native reproduction is claimed.

To repeat the available evidence audit after arranging those public inputs:

```sh
python -B docs/paper/q1/verify/audit_checkpoint_evidence.py --out ../evidence-audit.json
```

Missing reference files are reported as gaps; they are not evidence of a negative
scientific result. The retained-cell CausalBench summary can be re-merged without
raw expression data, which remains a different check from recomputing evaluations.

## Rebuilding a version-bound package

Run `tools/checkpoint_submission.py --help`. Supply exactly the three permitted
repository names, checkout paths and full commit SHAs, this guide, and a sanitized
validation JSON whose `commits` match those SHAs. The output receipt records the
ZIP hash. The command refuses overwriting an existing archive and rejects moving
refs, unsafe paths, secret patterns, unexpected nested archives or extra inputs.
Committed gzip result text is boundedly decompressed and scanned. The reviewed
six-member Overleaf source archive is checked recursively.

For this checkpoint, `--crucis-disclosure-overlay` explicitly sources only the
framework README/disclosure from the named research-commit directory. Runtime
and test files remain at the public framework base. The overlay exists because
the attempted framework gate did not complete; it is not a way to label that gate
passed or to publish a pending framework commit. No `.git` directory or history
is needed by a source-submission ZIP.
