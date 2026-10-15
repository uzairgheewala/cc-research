# B0: engines, guards and the scorer (Q2 build)

Tickets: CAP-05, CAP-11, CAP-10, EVL-03, BLD-02. Bundle B0 of `plans/q2_dag.json`; gates B0.1 and B0.2 of
`plans/q2_build_prereg.json`. Written 2026-10-15. No model calls.

## Where we are now

Every number the Q2 build reports now passes through one scorer that reproduces the audit chapter exactly, and every
data-pattern engine the kernel uses is pinned, wrapped and checked against a perfect independence oracle. Both B0 gates
pass.

## Must-show list

| Item | Result | Evidence |
|---|---|---|
| Engine manifest (D0.1) | causal-learn 0.1.4.8, `ges` 1.1.0, `gies` 0.0.3, NumPy 1.26.4, SciPy 1.13.1, Python 3.11; source-tree sha256 per package; settings (alpha 0.05, Fisher-z, stable, maxP priority 3; GES lambda log(n)/2); threads 1 | `engines/MANIFEST.json`, `engines/manifest.py --check` |
| Oracle and permutation check on the wrapper (D0.2, **gate B0.1**) | **720/720** exact equivalence class under 6 column orders x 120 DAGs; **120/120** order-invariant after canonical ordering; the kernel's independent re-derivation equals the engine on 720/720 | `analysis/results/q2_b0/oracle_check.json` (`engines/oracle_check.py`) |
| Supplier contract and fault suite (D0.3, **gate B0.2**) | 7/7 cases complete with the expected outcome (missing key, truncation, invalid JSON, code-fenced JSON, empty reply, HTTP 429 storm, quota refusal); each failure and the one normalisation counted; with every phrasing failed, the D+K ledger's claims equal the data-only claims and verify | `analysis/results/q2_b0/fault_suite.json`; `tests/test_q2_supplier.py` |
| Scorer v2 reproduces the audit chapter (D0.4) | 102 numbers (AB-01 S, c, q, a, F1; AB-04 DV-1 coverage and precision; files) recomputed; max difference **0.000000** | `analysis/results/q2_b0/scorer_repro.json` (`score/repro.py`) |
| Baselines on the test splits (D0.5) | table below | `analysis/results/q2_b0/baselines.json` (`score/baselines.py`) |
| CI (DX.1) | 41 new unit tests run with NumPy and networkx only (also on Python 3.10 with NumPy 2.2.6) (no causal-learn): scorer, re-derivation on oracle logs, combination rules, ledger v0.2 and verifier V1-V13, K7 checker, mutation tests, cycle guard, supplier contract, interventions, knowledge, isotonic map | `tests/test_q2_*.py` |

### Baselines (controlled: shuffled columns, expectation rule; DV-1 pooled over the files each row finished)

| Family | Split | PC maxP F1 / DV-1 | GES F1 / DV-1 | GIES D+I F1 / DV-1 | Empty graph DV-1 | True CPDAG F1 / DV-1 (coverage) |
|---|---|---|---|---|---|---|
| semantic | dev | 0.457 / 0.726 | 0.534 / 0.764 | 0.548 / 0.765 | 0.652 | 0.961 / 1.000 (0.929) |
| semantic | test | 0.469 / 0.700 | 0.523 / 0.744 | 0.530 / 0.741 | 0.634 | 0.956 / 1.000 (0.922) |
| formula | dev | 0.365 / 0.749 | 0.467 / 0.812 | 0.499 / 0.847 | 0.694 | 0.975 / 1.000 (0.958) |
| formula | test | 0.355 / 0.772 | 0.469 / 0.795 | 0.531 / 0.855 | 0.712 | 0.971 / 1.000 (0.961) |

PC maxP and GES fail on 4-38 files per family and split (a singular correlation matrix: exact deterministic relations);
those files are excluded from every comparison with them, as in AB-01.

## Design notes

- **Canonical order.** Engines only ever see columns sorted by the sha256 of their values; identical columns are ordered
  by sha256(values + name), never by position. Column order therefore cannot reach the engines or the name-to-index
  assignment (I1 by construction; tested in B0.1 and B1 rung R3).
- **Recording engine.** PC runs through causal-learn's own components with a recording CI test, so every test the engine
  ran is an evidence record. The kernel then re-derives skeleton, maxP colliders and Meek orientations from those
  records with NumPy only (`kernel/derive.py`), which is the independent checker K7 uses.
- **Typed failures.** Every engine returns a result or a typed failure (`singular`, `timeout`, `error`, `environment`);
  nothing raises into the kernel.
- **The supplier contract** never accepts a reply cut off at the token limit, even if it parses; it allows exactly two
  normalisations (surrounding whitespace, one code fence), counts both, and stops (resumable) on a quota refusal.

## Where we're going

B1 builds the data-only ledger on these engines. Its first rung, PC-only equality with the plain library call, is where
the engine defect reported in `docs/drafts/bug_reports/causal_learn_meek_directed_cycle.md` was found.
