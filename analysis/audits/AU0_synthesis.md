# AU0: what the eight desk audits say about direction

Tickets: AUD-26, STR-01, STR-06, DEC-01
Written 2026-10-12 from AU1-AU8 (385 typed rows; about 630 source links across the eight tables, not deduplicated; read that day) and one free check run the
same day (`analysis/authors_rule_layout_check.py`). Labels: **evidenced** means a cited source or our measurement says
so; **inference** is our reading, to be argued, not quoted.

## 1. Checked before relying on it

AU1 stated that CausalArena's own baseline runners orient undecided pairs from the lower to the higher column index, so
the published PC/GES/GIES numbers carry part of the layout leak. We already had both orientation rules scored for our
reproductions, on released and on shuffled columns (semantic, public half):

| Method | Gain from the authors' rule, released order | Same, shuffled columns |
|---|---|---|
| PC (Causal-Copilot's causal-learn copy) | +0.062 | -0.003 |
| GES | +0.022 | -0.001 |
| FCI | +0.221 | -0.006 |

**Evidenced:** the gain is entirely layout; it vanishes under shuffling. For GES it is small (+0.022, and our GES with
the authors' rule, 0.550, matches the published GIES 0.552). For a method that leaves many pairs undecided it is large
(FCI +0.221, because FCI leaves 73% of found pairs undecided). AU1's point holds, with the size now measured: the
leaderboard rows that leave pairs undecided are the ones the leak inflates. PC scores 0.428 with shuffled columns
against 0.335 in released order under the random rule; AU6 traces that order dependence to Causal-Copilot's modified
copy of causal-learn (code reading, not yet tested; see 4).

## 2. The three questions from the audit program

**Where is there room for a result nobody else has?** (AU1, AU2, AU4, AU6)
- Evidenced: no published system or benchmark crosses names (real / neutral / swapped) with column layout; CARE has
  names only on small graphs, ReplaySCM order only, ACDB anonymises without a names arm. No LLM method or agent reports
  on CausalArena. No library records where an edge's direction came from. No benchmark scores abstention or calibration
  per edge, and none scores end-to-end discovery agents at 20-40 variables.
- Evidenced: the crowded corner is graph recovery from data plus names on famous bnlearn graphs (27 of 43 name-using
  rows), where memorisation is a confound and classical baselines usually win.
- Inference: the open corner is exactly ours: controlled order provenance at 20-40 variables, with a data-only floor.

**What makes a tool worth using?** (AU5, AU7, AU8)
- Evidenced: buyers pay for effect estimation and experimentation (large exits), not for learned graphs; no vendor
  publishes graph accuracy. Industrial root-cause analysis ranks causes over declared topology (R = K), and in an
  independent benchmark learned-graph RCA lost to a non-causal baseline (AC@1 0.09-0.32 vs 0.67).
- Evidenced: graph metrics do not track decision value; effect identification under sufficiency depends on the causal
  order, not on the edge set; a reversed edge costs more than a missing one; in biology the value is precision on a few
  top claims checked by experiment. No numeric graph-accuracy threshold for usefulness was found.
- Evidenced: regulators and reviewers reward provenance, pre-specification and frozen, traceable models; the EMA/FDA
  precedent (PROCOVA) is a guarantee that holds whatever the ML component does, which is our "never below data-only".
- Inference: approaching 0.957 F1 is not the practical target. The target is **correct order on the pairs a decision
  needs, with per-claim provenance and calibrated abstention**, scored by decision value (held-out interventional claim
  precision at stated coverage), with F1 kept as the comparability view.

**Build or reuse, benchmark or not?** (AU4, AU6, AU8)
- Reuse (permissive licences): upstream causal-learn 0.1.4.8 pinned, lingam, `gies`, AVICI; Tetrad and pcalg only as
  external cross-checks (GPL). Build: canonical hashing, per-edge typed test records given a partial order, the
  order-invariance gate, bootstrap + calibration, IDA/identification status, intervention attribution, and the claim
  schema itself (JSON Schema + PROV-O export) with a `ledger verify` command.
- Benchmark: start with an overlay on CausalArena (B1 "ArenaShuffle", about 4 weeks: server-side arms, declared regime,
  scored confidence matrices); the paper-grade contribution is B2, a generator whose names disagree with the data on a
  set fraction of edges, giving a name-reliance curve (6-8 weeks). Causal Chambers is a name-leak demonstration, not an
  orientation test (its graphs are one layer deep).

## 3. Paths, with what each needs

| Path | What it produces | Cost | Risk | Feeds |
|---|---|---|---|---|
| A. Field audit under controls | names x layout x scale on the leaderboard and on runnable agents (Causal-Copilot, Vashishtha order elicitor, PyWhy-LLM, MATMCD, causaliq) | baselines free; agents need API budget (one-run probe first) | low | T1, T2; a measurement paper |
| B. Claim ledger as an evidence layer | schema-first ledger, data-only floor, invariance + knowledge-honoured checks, decision-value scoring | free (engine) plus A3-style elicitation | medium | T3, T4; product angle |
| C. Benchmark (B1 then B2) | a controlled public track and a name-reliance curve | free to build; hosting | medium | E2; a benchmark paper |
| D. Decisions layer | DV-1 interventional claim precision, AID, experiment-choice regret | free | low-medium | T5, T6 |

Inference: A, B and D share one scorer and one set of arms; C reuses both. The order that keeps every step useful on
its own: free re-scores and scorer first (A-baselines, D metrics), then the ledger kernel (B) evaluated by that scorer,
then B1, with agents (A) as soon as an API budget is approved.

## 4. Free work this unlocks now (no model calls)

1. Re-score every leaderboard baseline we can run with shuffled columns and the expectation rule; publish both (BEN-07).
2. Sortability audit (varsortability, R2-sortability) of CausalArena's public families (BEN-07).
3. d-separation-oracle test of Causal-Copilot's causal-learn copy vs PyPI 0.1.3.8 vs 0.1.4.8 vs gCastle settings
   under all column permutations of small DAGs (turns AU6's code reading into a demonstration).
4. DV-1 (held-out interventional claim precision with a risk-coverage curve) and ancestor/O-set AID in the scorer.
5. The ledger's claim schema (JSON Schema + PROV-O mapping) and `ledger verify` checks, before any engine code.

## 5. Decisions for Uzair

1. Which path mix to commit to (the table above); DEC-01 still open.
2. A one-run API cost probe of Causal-Copilot (under $1) to size path A's agent budget; DEC-02 (A3) as before.
3. 3-5 practitioner interviews (SRE, marketing science, real-world evidence) to test whether abstention and provenance
   are worth paying for; the audits found no evidence either way.
4. EXT-01 (telling CausalArena's maintainers about column order) now has a second reason: their own baseline runners
   use it.

## 6. Corrections to carry into other documents

- Say "Causal-Copilot's modified copy of causal-learn" is order-dependent, not "causal-learn 0.1.3.8" (AU6; to confirm
  with item 4.3).
- SR 11-7 was replaced by SR 26-2 on 17 Apr 2026, which excludes generative and agentic AI (AU5, AU8).
- CausalArena's semantic graphs were drafted with LLM assistance; report real-name gains as measured against
  LLM-drafted graphs and prefer the neutral arm as the primary score there (AU2, AU4).
