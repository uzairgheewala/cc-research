# B5: the audit adapter and root-cause analysis through the ledger (Q2 build)

Tickets: BLD-15 (proposed), TGT-20 (proposed), CAP-09. Bundle B5 of `plans/q2_dag.json`; gates B5.1 and B5.2 of
`plans/q2_build_prereg.json` and `plans/b5_prereg.json`; landmark ER-4b. Frozen kernel `plans/b5_freeze.json` (id
e9871399f1b92e7d, rule C3, B1's core unchanged). Written 2026-10-15. No model calls.

## Where we are now

Two things now work. First, the ledger can read other systems' outputs. Five systems' AB-06 graphs become typed claims,
each arrow is traced to its source (data pattern or knowledge), and violations are named per pair (B5.1 passes). Second,
the ledger carries root-cause analysis. On the held-out PetShop issues, declared topology entered as knowledge on the
data-only ledger reproduces AB-12 exactly: AC@3 0.932 on answered issues, at 0.917 coverage. With only 44 answered issues
the interval's lower end is 0.841. **ER-4b is not met** under the interval rule, as predicted.

## Must-show list

| Item | Result | Evidence |
|---|---|---|
| **B5.1** every flagged violation traced to a pair, a claim and a source; 0 unknown sources where the agent records provenance | **pass** | `analysis/results/q2_b5/adapters.json` |
| **B5.2** PetShop held out: declared topology through the ledger with abstention, against learned-graph RCA (descriptive) | **reported**: declared AC@3 0.932 at coverage 0.917 (strict 0.854); learned ledger only 0.400 at 0.521 (strict 0.208) | `analysis/results/q2_b5/rca_test.json` |
| Gap curve (10% and 25% of declared edges withheld, 5 seeds), fill rules as rows | table below | same |
| Every RCA ledger verifies (V1-V13) | 8/8 test ledgers | same, `ledgers` |
| Held-out discipline | one logged read (13:14:17Z), code equal to the freeze | `analysis/results/q2_b5/access_log.jsonl` |

### Adapters (AB-06 outputs, dev scenarios)

| System | Runs | Arrows | Sources | Violations flagged |
|---|---|---|---|---|
| Causal-Copilot (gpt-4o, stage graphs rebuilt) | 30 | 529 | data 126, knowledge 403 | knowledge created a connection 384, deleted 32, reversed data 11; direction follows names 198 |
| MATMCD | 30 | 762 | knowledge 762 | reversed data 398, created 23, deleted 17; follows names 104 |
| causaliq | 30 | 414 | knowledge 414 | follows names 133 (no data floor to compare: 30 runs) |
| PyWhy-LLM | 9 | 1,165 | knowledge 1,165 | follows names 351 (no data floor: 9 runs) |
| Vashishtha et al. | 10 | 200 | data 178, knowledge 22 | follows names 4 |

"Follows names" means the arrow flips when names are swapped (paired real and swapped runs). Causal-Copilot's sources
are reconstructed from its stage graphs (`audit/export_cc_stages.py`; the S2 rebuild equals the recorded graphs 30/30)
and labelled that way, because Causal-Copilot does not record provenance itself.

### RCA, PetShop test split (48 issues; AB-12's traversal and margin abstention, tau 0)

| Ledger view | Coverage | AC@3 answered | AC@3 strict | AC@1 answered |
|---|---|---|---|---|
| **declared topology (knowledge) on the data-only ledger** | 0.917 | **0.932** [0.841, 1.000] | 0.854 | 0.735 |
| data-only ledger (learned graph) | 0.521 | 0.400 | 0.208 | 0.280 |
| 10% of declared edges withheld (mean of 5) | 0.904 | 0.831 | 0.750 | |
| + fill: every data claim | 0.904 | 0.711 | 0.642 | |
| + fill: claims both engines make | 0.883 | 0.779 | 0.688 | |
| + fill: claims joining disconnected parts | 0.904 | 0.793 | 0.717 | |
| 25% withheld (mean of 5) | 0.838 | 0.664 | 0.558 | |
| + fill: every data claim | 0.904 | 0.672 | 0.608 | |
| + fill: claims both engines make | 0.900 | 0.670 | 0.604 | |
| + fill: claims joining disconnected parts | 0.887 | 0.683 | 0.608 | |

## Predictions

| Prediction (written before the held-out read) | Verdict |
|---|---|
| P-B5a the ledger route reproduces AB-12 exactly (0.932 at 0.917) | **Supported** |
| P-B5b ER-4b not met under the interval rule | **Supported** (lower end 0.841) |
| P-B5c filling withheld declared edges with data claims lowers AC@3 against leaving the gaps | **Partly refuted.** It holds at 10% withheld (-0.04 to -0.12). At 25% withheld every fill rule raises coverage (0.838 to 0.887-0.904) and strict AC@3 (0.558 to 0.604-0.608), and AC@3 on answered issues stays level |

## What the numbers say

- **ER-4b is limited by sample size, not by the method.** With 44 answered issues, a lower end of 0.90 needs a point
  estimate near 0.98: at most one miss. The route to ER-4b is more issues (a second RCA benchmark, or the PetShop issues
  pooled across traffic regimes under a pre-registered rule), not a better ranking.
- **Data claims help only when the declared topology is badly incomplete.** With a tenth of the topology missing, filling
  the gaps from data adds wrong edges faster than right ones. With a quarter missing, the gaps cost more coverage than
  the wrong edges cost accuracy. The ledger records which edges came from where, so a reader can see that trade.
- **The adapter is the wedge's measurement half.** Every arrow in five systems' outputs now has a typed source, and every
  violation names its pair. The same classes the audit chapter counted by hand now come from one adapter.

## Deviation

The hashed order says "a bundle builds only on predecessors that passed". The queue ran B5's held-out read at 13:14,
13 seconds after B4's evaluation, and B4.1 failed on semantic. B5 uses nothing B4 produced: no calibration map, no
selective view (`audit/rca.py` imports only `kernel.build`, and `kernel.freeze` for the guard). So the B5 result does
not rest on B4. The order rule as written was still not honoured by an unattended queue, and it is recorded here.

## Where we're going

The build summary (`analysis/reports/q2_build_results.md`) puts the landmark table together and lays out the routes
that remain for ER-2, ER-3, ER-4a and ER-4b.
