# Q1 checkpoint archive

Tickets: DLV-05, DLV-07.

This directory preserves the author's final Overleaf export and the locally built,
visually inspected PDF. `manifest.json` binds both to the six exact canonical
inputs in `docs/paper/q1/`, the course styles, evidence freeze and review records.
The PDF in `../../build/report.pdf` is an identical convenience copy. Earlier
sources and PDFs remain in Git history. Edit the canonical source, not this archive.

The checkpoint is locally validated and awaiting the author's submission. This
archive is not evidence of a remote push, public release or course submission.
The source ZIP is the original supplied export, without auxiliary files, logs,
credentials or research datasets. Upload it to Overleaf and select **XeLaTeX**.

From the repository root, verify the stored artifacts:

```powershell
& '.\tools\python.ps1' -B docs/paper/q1/verify/verify_checkpoint_release.py
```

To build a new candidate without overwriting this inspected release:

```powershell
& '.\tools\python.ps1' -B docs/paper/q1/build_paper.py --no-numbers --overleaf --output-dir docs/paper/q1/build/candidate-rebuild
```

This needs XeLaTeX, BibTeX and the course template's fonts/packages. The builder
checks the frozen evidence and number lock before compilation. It retains a
scratch generation and binds the PDF and bundle to its inputs. Its new PDF is
unreviewed until rendered and inspected. PDF timestamps can change binary hashes
on rebuilding; the manifest identifies the particular inspected output, not a
claim of byte-identical TeX builds on every machine.

Six exact-draft editorial lint dispositions are explicit in the verification
directory: four grouped paragraph attributions and two structural prose counts.
They retain reasons and evidence references and fail closed on a changed draft.
The citation-key and frozen numerical checks remain active. The manuscript itself
is byte-identical to the supplied export. Generated number files differ from the
previous checkout only in line endings; registry values and evidence are unchanged.

The checks establish artifact integrity and scoped review. They do not establish
full native rerun coverage, fresh full-text verification of every historical
citation, statistical identification beyond the recorded comparisons, or proof
that every scientific claim is true. Historical review limits and the BND-08
endpoint discrepancy remain explicit. Reproduction and public communication are
the next workstream described in `../../POST_SUBMISSION_AUDIT.md`.
