# AB-03 Engine forensics: perfect-oracle and determinism checks across the engines agents call

Ticket: AUD-35 (advances EXT-03, CAP-05, CAP-11). Written 2026-10-12. No data, no model calls.
Script: `analysis/engine_forensics.py` (extends `engine_oracle_check.py`, AUD-27). Results: `analysis/results/engine_forensics/forensics.json`.

## Where we are now

The same 120 random DAGs (6-12 variables) x 6 column orders used in AUD-27, with d-separation in the true DAG as the
independence test. A correct PC returns the true CPDAG every time, in every order; a correct FCI (no latents) the true
skeleton.

## Results (together with AUD-27)

| Engine | Exact class / 720 | DAGs order-invariant / 120 | Defect class |
|---|---|---|---|
| causal-learn 0.1.3.8 and 0.1.4.8 (PyPI), PC and FCI | 720 | 120 | correct |
| **Causal-Copilot's vendored causal-learn PC** (AUD-27) | 460 | 56 | extra adjacency (separating set never tested), order dependent |
| gCastle 1.0.4 PC `original` / `stable` (AUD-27) | 456 / 460 | 56 / 56 | extra adjacency, order dependent |
| gCastle 1.0.4 PC `parallel` | 720 | 120 | correct |
| pgmpy 1.1.2 PC, `orig` / `stable` / `parallel`, max_cond_vars unbounded and default 5 | 720 each | 120 each | correct |
| **dodiscover (git main 6e64456) PC** | 597 of 717 completed (3 runs raised) | 88 | orientation only (skeleton exact in 717/717), order dependent |
| dodiscover FCI (skeleton) | 717 | 120 | correct |
| tigramite 5.2.10.1 PCMCI+ (tau_max 0, OracleCI) | 720 | 120 | correct |

**New defect: dodiscover's PC orients wrongly with a perfect oracle, and can return a cyclic graph.** Minimal
counterexample (5 variables, columns in index order): true DAG 0->1, 4->1, 1->2, 4->2. The true CPDAG is fully directed
(v-structure 0->1<-4, then Meek R1 gives 1->2 and Meek R2 gives 4->2). dodiscover returns 2->4, which closes the cycle
4->1->2->4. Errors across the 720 runs: 122 true arrows reversed, 89 arrows committed where the class leaves the pair
undirected, none missing. Three runs raised `NetworkXError: The edge v3-v2 not in graph` in one pass and none in a
rerun of identical inputs: the orientation phase is also not deterministic.

**Determinism.** Causal-Copilot's vendored FCI under joblib threading: 3 runs x 40 DAGs identical in this pass; the
533 vs 531 difference seen in AUD-27 (all 720 runs) was not reproduced here. Recorded as "observed once, not reproduced".

## Prediction P5

P5 said at least one more widely used engine besides gCastle `original`/`stable` returns a **wrong skeleton** under a
perfect oracle. **Refuted as stated:** every other engine tested gets the skeleton exactly. A different defect class was
found instead (dodiscover PC orientation). Not tested: Tetrad (py-tetrad; Java is present in the sandbox, the jar was not
fetched), pcalg (R not installed; would run on Uzair's machine), causal-learn GES/CD-NOD with an oracle score (not
defined in the libraries).

## Gates

- Every engine version pinned: pgmpy 1.1.2, tigramite 5.2.10.1, dodiscover git 6e64456, pywhy-graphs 0.1.0, networkx
  3.6.1 in the second environment (`forensics.json: engine_versions`). Wheel hashes: PyPI wheels as resolved by uv; the
  git commit pins dodiscover.
- One command reproduces it: `python analysis/engine_forensics.py --python2 <venv with pgmpy, tigramite, dodiscover> --vendored <Causal-Copilot>/externals/causal-learn --out analysis/results/engine_forensics`.
- Shim recorded: `nx.d_separated = nx.is_d_separator` for dodiscover's Oracle (removed in networkx 3.5).

## What this changes

1. Engine defects are not unique to Causal-Copilot: two widely used Python libraries (gCastle's default PC, dodiscover's
   PC) fail a perfect-information test. A ledger engine must run the oracle and permutation checks as part of its CI.
2. Safe defaults for reuse: causal-learn (PyPI), pgmpy, tigramite PCMCI+, gCastle `parallel`.
3. Draft upstream reports (for Uzair to send or not; EXT-03): `docs/drafts/bug_reports/`.
