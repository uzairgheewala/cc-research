# BND-11 preparation: refinement v2 frozen, names questions prepared (2026-10-12)

Tickets: BND-11, BLD-06, CAP-10, TGT-09, TGT-13, DLV-04

Code: `analysis/refinement_v2.py` (rule, modes and predictions in its docstring), `harness/names_runner.py`, `cc.ps1 names`,
`analysis/bootstrap_replay_family.py` (a copy of the pre-registered BND-08 replay script with `--family` and `--shuffle-seed`).
Pre-registration: `manifests/evidence/bnd11_prereg_2026-10-12.sha256`; rule frozen in `analysis/results/refinement_v2/RULE.json`
(sha256 443354d8..., 2026-10-12T09:44:07Z; it also pins refinement_v1.py, whose typing rule v2 reuses unchanged).

## Why v2 changes the data part

BND-10 showed the frozen v1 below the algorithm on the live S2 tables (R1 17 of 30): its KEEP rule removed 120 algorithm
adjacencies seen in fewer than half the resamples, 50 of them true. v2's data part (v2d) keeps every algorithm adjacency, adds a
pair only when it appears in at least 90% of resamples, and types pairs exactly as v1. This was decided after reading test
data, so v2d gets a fresh held-out set: the formula family's test split, replayed by a new compute job and read once through
`refinement_v2.py test` (refuses unless the frozen hash matches; logs the read).

## Dev results (data part, `analysis/results/refinement_v2/dev.json`, 92 files: 69 live tables + 23 semantic dev replays)

| | S0 | S1 (pipeline) | v2d |
|---|---|---|---|
| mean adjacency F1 | 0.557 | 0.302 | 0.557 |
| mean directed F1, undecided random | 0.290 | 0.170 | 0.310 |

R1 SUPPORTED (84 of 92), R2 SUPPORTED (87 of 92), R3 SUPPORTED (+0.021). For comparison only (labelled exploratory, those
tables were read in BND-10): on the 30 live S2 tables v2d meets R1 and R2 in 30 of 30, R3 +0.011
(`exploratory_s2_live.json`).

## Names part, ready to run

`plans/bnd11_names_requests.jsonl`: 262 pairs that v2d leaves adjacent and not directed (bidirected excluded), across the 30
S2 runs, 3 paraphrases each = 786 questions (real 261, neutral 252, swapped 273). About 44k prompt tokens; replies are a few
tokens each. At the same assumed $2.50 / $10 per million tokens this is well under $1.

Rule: an answer is used only if all three paraphrases agree on a direction, it does not contradict a PAG mark set by the
data, and it creates no directed cycle; every such edge is stored with source "names". A reply that is not exactly the JSON
asked for is asked once more, then counted as an abstention; API errors are recorded the same way, so the runner has no
crash path (CAP-10). Separating sets are not recorded by the pipeline for this step, so that check is reported as not done.

Stub check (offline, `--stub`, injected malformed replies): 786 questions, 807 calls, 25 invalid replies handled by retry or
abstention, no exception; `apply` produced R4-R6 (meaningless on stub answers, not reported as results).

## What Uzair runs (in cc-research, PowerShell)

1. `cc.ps1 compute bootstrap_replay_ca_formula_dev.json` (free; dev replays for the formula family)
2. `cc.ps1 compute bootstrap_replay_ca_formula_test.json` (free; the held-out set for v2d)
3. `cc.ps1 names bnd11_names_requests.jsonl stub` (free; checks the container path)
4. `cc.ps1 names bnd11_names_requests.jsonl` (LIVE, under $1)
