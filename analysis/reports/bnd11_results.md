# BND-11 results: refinement v2 on held-out data, and names only where the data are silent (2026-10-14)

Tickets: BND-11, BLD-06, CAP-10 (also TGT-09, TGT-13, DLV-04). Prepared in `bnd11_prep.md`. The rule was frozen on
2026-10-12 (`analysis/results/refinement_v2/RULE.json`, sha256 443354d8…). The predictions are in
`analysis/refinement_v2.py`, written before any answer or formula replay existed.

Inputs, all run by Uzair on 14 Oct:

- the two compute jobs `bootstrap_replay_ca_formula_dev` and `bootstrap_replay_ca_formula_test` (free);
- `cc.ps1 names bnd11_names_requests.jsonl`: 786 questions, 1,571 calls to gpt-4o-2024-08-06, 127,142 + 14,941 tokens,
  $0.47 at list prices.

## Where we are now

The data part of v2 passes its held-out test on every file. Names, used only where the data are silent, do no harm when
they are wrong. They also add almost nothing when they are right.

## Data part (v2d) on the held-out formula test replay

v2d keeps every algorithm adjacency, adds only pairs seen in ≥ 90% of resamples, and types pairs as v1.

The held-out set has 22 files. The replay produced 25 files, and 3 of them raised in PC; these are counted as errors in
the replay header and not scored. The set was read once (`analysis/results/refinement_v2/access_log.jsonl`) and the
output is `test_formula.json`.

| | Prediction | Result | Verdict |
|---|---|---|---|
| R1 | v2d adjacency F1 ≥ S0 − 0.02 in ≥ 90% of files | 22 of 22 | **supported** |
| R2 | v2d adjacency F1 > the pipeline's bootstrap step (S1) in ≥ 90% | 22 of 22 | **supported** |
| R3 | mean directed F1 (undecided random) v2d − S0 ≥ −0.01 | +0.010 | **supported** |

Means:

| | Adjacency F1 | Directed F1 (undecided random) |
|---|---|---|
| S0 (the algorithm) | 0.539 | 0.366 |
| S1 (the pipeline's bootstrap step) | 0.432 | 0.331 |
| v2d | 0.539 | 0.375 |

Every v2d edge carries a source.

This closes what BND-10 left open. v1 deleted true edges and fell below the algorithm on held-out tables. v2's data part
never falls below it, on data it had never seen.

## Names part on the 30 live S2 tables

The names part asks for pairs v2d leaves adjacent and undirected. A direction is used only if three paraphrases agree, it
does not contradict a PAG mark, and it creates no cycle.

| | Prediction | Result | Verdict |
|---|---|---|---|
| R4 | neutral names add no edge (≥ 9 of 10 families) | 10 of 10 | **supported** |
| R5 | swapped names: v2 within 0.05 of v2d (≥ 8 of 10) | 10 of 10 | **supported** |
| R6 | real names: v2 directed F1 > v2d (≥ 8 of 10) | 1 of 10 | **refuted** |

Mean directed F1 (undecided random) for real names: v2d 0.341, v2 0.355. For swapped names: v2d 0.406, v2 0.406.

**Why the names did so little.** gpt-4o wrapped 1,036 of its 1,571 replies in a Markdown code fence (```json …```).

- The frozen runner accepts only the bare JSON it asked for. A fenced reply is retried once, then counted as an abstention.
- 785 of 786 questions needed the retry, and 251 ended as abstentions.
- With three paraphrases required to agree, one abstention removes the pair. Only one names edge survived in the real
  arm.
- There was no crash path: every malformed reply was handled (CAP-10's requirement). But the strict contract turned a
  format habit into silent loss of evidence. This is the same failure class as Vashishtha et al.'s truncation
  (`ab05_probe_results.md`).

**Exploratory re-read, decided after the verdicts and labelled as such** (`analysis/bnd11_lenient_parse.py` →
`names_s2_exploratory_lenient.json`). The same recorded replies, with a surrounding code fence stripped before parsing:

- 251 abstentions become answers, and 33 answers change between the first and the second reply.
- The real arm then gets 16 names edges: v2 0.380 against v2d 0.341. R6 rises to 5 of 10, which is still refuted.
- The swapped arm gets 2 edges: 0.409 against 0.406, still harmless.

Even read leniently, names restricted to data-silent pairs are a small lever on these scenarios. This agrees with AB-07's
orient-only result: +0.02 to +0.04 F1 for GES.

## What this means for the build (`approach_v1.md`)

- **G3 and G5 hold in a live run.** The data part never drops below the algorithm on held-out data. Wrong names
  (swapped) cost nothing measurable, because they can only orient pairs the data left open and must agree across
  paraphrases.
- **G7 needs the lesson.** A supplier contract must say in advance which normalisations it accepts, for example a
  stripped code fence. It must count how often each was needed, and report abstentions as a ledger field.
  - A contract that is too strict degrades silently, like Vashishtha's truncation.
  - A contract that is too lenient lets malformed answers through.
  - B0's fault-injection suite gets a "fenced JSON" case.
- **The knowledge lever is modest here.** The value of the ledger is not that names lift the score. It is that the
  system cannot fall below its data, that wrong knowledge is bounded and visible, and that it says where every direction
  came from.

## Where we're going

- BLD-06 (the refinement replacement): v2 passes its held-out data test. The names part is safe but weak. Ticket notes
  are updated.
- CAP-10 closes: there is no crash path in 1,571 live calls. The fence finding moves into approach v1's G7.
