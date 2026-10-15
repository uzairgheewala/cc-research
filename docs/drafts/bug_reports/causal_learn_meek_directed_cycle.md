# Draft note to causal-learn maintainers: PC with maxP can return a directed cycle (Meek step)

Ticket: EXT-07 (proposed). Status: draft; Uzair decides whether to send. Found 2026-10-15 by the Q2 kernel's
re-derivation check (kernel/derive.py; rung R1 of plans/b1_prereg.json).

## What we saw

`causallearn.search.ConstraintBased.PC.pc(X, 0.05, "fisherz", stable=True, uc_rule=1, uc_priority=3)` (causal-learn
0.1.4.8, PyPI) returns a graph with a directed cycle on 6 of 250 CausalArena dev files (5 semantic, 1 formula; 2.4%),
in the released column order as well as in our canonical order. Example (semantic, insurance_deductible_claim_reporting,
rep003): the final graph contains 21 -> 24 -> 5 -> 19 -> 0 -> 22 -> 7 -> 21 (indices of the canonical column order).

## Where it comes from

`Meek.meek` skips an orientation when `cg.G.is_ancestor_of(k, j)` reports that it would close a cycle. The ancestor test
reads `GeneralGraph.dpath`, which `add_directed_edge` updates incrementally (`adjust_dpath(i, j)` for a new edge i -> j).
That update records i and i's ancestors as ancestors of j, and i as an ancestor of j's descendants, but not i's ancestors
as ancestors of j's descendants; it never recomputes the closure. A path built up by earlier orientations can therefore
be missing from `dpath`, and the cycle check passes when it should fail. (Code reading, causal-learn 0.1.4.8
`graph/GeneralGraph.py:53-64`; the cycles above are the measurement. We have not tested a patched library.)

Our independent re-statement of the same loop (same lists of unshielded triples, triangles and kites, same order) with a
fresh reachability test reproduces the library's skeleton, its maxP colliders and its Meek output exactly on every other
dev file (244 of 250), and on the 6 differs only by leaving the cycle-closing pairs undirected.

## Suggested fix

Recompute reachability in the cycle check (or call `reconstitute_dpath` after each orientation in `Meek.meek`).

## How to reproduce

`kernel/derive.py` (pc_maxp_from_tests) and `kernel/run_b1.py` in cc-research; results in
`analysis/results/q2_b1/dev_*.jsonl` (field `r1_exact_without_defect_fix` false on the 6 files).
