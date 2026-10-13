# Audit program: map the field before committing to a path

Tickets: STR-01, STR-06, DOM-07, DOM-11, DOM-12, BEN-07 (new tickets AUD-18..AUD-25 proposed below)
Written 2026-10-12. Status: desk audits AU1-AU8 started the same day; compute audits AU9-AU11 wait on decisions.

## Why

The Atlas shows where this project sits in one slice of the space (CausalArena, 20-40 variables, no hidden causes).
Before choosing which path to commit to (the claim ledger, a benchmark of our own, a product, a field audit), we need
the whole field on one table: who else works in each cell, how they are measured, what the limits are, who would pay for
which guarantee, and what accuracy actually matters downstream. Every audit below answers a question that changes a
decision; none is a literature review for its own sake.

## Shared rules (all audits)

- Every claim carries its source URL and the date read. Vendor and press claims are labelled `claim (vendor)`; numbers
  from a paper's own table are `reported`; numbers we reproduced are `measured` (only AU9-AU11 produce those).
- A source we could not open is listed as `not read` with the reason, never summarised from its abstract as if read.
- "Not found" is a statement about the searches listed, which are recorded.
- Output per audit: `AUx_<name>.md` (findings, open questions, what it changes) and `AUx_<name>.json`
  (the typed table, one record per row, schema below), in `analysis/audits/`.
- Quotes under 15 words; everything else paraphrased.

## The audits

| ID | Question | Decision it informs | Typed table (one row per) | Cost |
|---|---|---|---|---|
| AU1 Field systems | Which causal-discovery systems exist (classical, continuous-optimisation, pretrained, LLM-assisted, agents), what evidence each may use, where its edge directions come from, and how it was evaluated? | E1 scope; which systems to run under our controls; positioning | system: category, year, venue, regimes D/I/K, order source, controls reported (names, layout), benchmarks + best reported numbers, code URL, licence, last commit, CPU-runnable, cost per graph, scale | desk |
| AU2 Benchmarks | Which benchmarks and datasets exist for discovery and causal reasoning, where does their ground truth come from, and how can they leak? | which benchmarks Q2 uses; whether to build our own (AU4) | benchmark: task, ground-truth origin (synthetic / LLM-written / expert / physical), size, regimes, metrics, known leaks (names, layout, sortability, memorisation), licence, maintenance, who reports on it | desk |
| AU3 Theory and limits | For each cell of Q x R x W, what is identifiable, from what, at what sample cost, and what is the best known bound? | fills the Atlas back slabs and the limits on Level 2 | cell: question, regime, world assumptions, identifiability result, theorem + reference, finite-sample rate if known, open problems | desk |
| AU4 Own benchmark | What would a benchmark need to measure order provenance and decision value without the leaks AU2 finds, and what would it cost to build? | E2 (public agent track); a benchmark paper | requirement: source of the requirement, how existing benchmarks fail it, candidate design, effort | desk |
| AU5 Commercial applications | Who sells or buys causal discovery and causal analysis, for which decisions, with what claimed guarantees, and where it fails in practice? | STR-06 product angle; which guarantee to optimise | product or use case: vendor, sector, decision supported, method, claimed accuracy or guarantee, pricing model, evidence of adoption, failure reports | desk |
| AU6 Core engines | Which libraries and engines exist, what can each do (algorithms, tests, interventions, background knowledge, scale, determinism, order invariance), and what would our engine reuse? | the ledger's build vs reuse | engine: language, algorithms, CI tests, interventional data, background knowledge, outputs (CPDAG/PAG/scores), scale, column-order invariance, licence, maintenance | desk |
| AU7 Value of accuracy | How do graph errors become decision errors, and at what accuracy does a discovery tool become worth using? | the practical target: does approaching 0.957 matter, or reliability and abstention? | finding: setting, graph metric, downstream metric, relation, threshold if any, source | desk |
| AU8 Packaging | How are causal tools delivered (library, notebook, agent, SaaS, report), what do users and regulators need from outputs (provenance, uncertainty, reproducibility), and what do users complain about? | what our outputs look like; the report and API of the ledger | delivery mode or requirement: example tools, user need, regulator text, complaint evidence | desk |
| AU9 Field runs (E1) | Under our controls (shuffled columns; real / neutral / swapped names), where does each runnable agent get its directions? | the field-level result for T2 | measured, per system x benchmark x arm | live: API cost per agent; needs Uzair |
| AU10 Knowledge elicitation (A3) | Can a model reading names supply correct tiers, and what do neutral and swapped names do? | DEC-02, G1, T3(c) | measured O1-O5 | live: about 900 short calls; DEC-02 |
| AU11 Pretrained models | Do AVICI, CDFM and other released models show PC's direction pattern, and are they order-invariant as claimed? | T1 | measured budgets | free, blocked: checkpoints on huggingface.co |

## Proposed tickets

AUD-18..AUD-25 for AU1-AU8 (category "3 Audit"), each closing with its `.md` and `.json` and a check that every row has a
source. AU9-AU11 already exist as STR-01, RQ-10..14 and REP-07/BEN-07/BEN-11.

## What happens after

A synthesis (`AU0_synthesis.md`) that answers, with the tables in hand:
1. Where in Q x R x W is there room for a result nobody else has, and is it reachable this year?
2. Which practical target (score, guarantee, abstention, cost) makes a tool worth using, per application?
3. Build vs reuse for the core engine; benchmark of our own or not; which systems AU9 should run.
Then the Atlas gains the field (AU1, AU2) on Levels 1-2, the limits (AU3) on the back slabs, and a value layer (AU5, AU7).
