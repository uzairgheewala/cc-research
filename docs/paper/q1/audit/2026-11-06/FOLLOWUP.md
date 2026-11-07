# Q1 checkpoint reproduction follow-up

Tickets DLV-05 and DLV-07. Recorded 6 November 2026 (Pacific time).

The author confirmed submitting the archived report PDF and the combined source
ZIP. The [submission record](../../verify/submission-status-2026-11-06.json)
identifies the artifacts. The [original audit](REPORT.md) records the earlier
observations, including incomplete validation attempts.

| What a reader can check | Result and boundary |
|---|---|
| Archived report and linked numbers | Run the commands in the [repository README](../../../../../README.md). They verify 78 registry entries, 13 numerical sources, 19 frozen files and the original release artifacts. |
| FCI scoring contrast | The audit independently re-scored the same retained graph against its generating reference for all 225 eligible semantic cases. The original log had 250 rows and 25 failures. This measures a difference between scoring rules on the same graphs. |
| Name controls | The audit re-aggregated four other systems' retained per-scenario rows and the heterogeneous tally. Causal-Copilot's earlier pre-cycle, committed-arrow row uses a separate cohort. The tally is descriptive. |
| Causal-Copilot companion | Its isolated reproduction and four tests passed against its retained graphs. Its comparison covers the refinement intervention documented in the companion README. |
| Stage and crash diagnostics | The replay below read the retained historical stage states. The largest completed-pair change was at bootstrap, with adjacency F1 changing by −0.270 on 22 completed main-control runs. All eight main-control runs flagged as cyclic at entry to the cycle step crashed there. The public tree supplies the frozen summaries. |
| BND-08 label following | Replaying the rule before cycle handling gives 86 label-only arrows out of 109 discriminating arrows across ten swapped runs (78.90%). The same calculation on the nine completed runs gives 81/101 at both the pre-cycle and final endpoints (80.20%). The historical numerical rule clears 80% only on the completed subset. The declared endpoint is inconclusive under its own point rule. Counts are descriptive because edges within a family are dependent. |
| CausalBench | The 586 retained cells were re-merged in the first audit. The original filtered intervention arrays are separate inputs. See the filtered-array replay below for the exact scope of the additional evaluator check. |

## Re-run with the required inputs

With the locally retained CausalArena files and both CausalBench metadata files
present at the recorded paths, run the scoped evidence audit from the repository
root. The output is a new receipt and should go outside the evidence tree.

```sh
python -B docs/paper/q1/verify/audit_checkpoint_evidence.py --out /path/to/new-receipt.json
```

The stage replay uses Crucis source `827b43cfd02dc9037c074adeda6512ade5d402a6`.
Install that revision or make it importable, set `CRUCIS_DATA_ROOT` to the
research repository, and supply the original retained stage records and reference
arrays. The relevant inputs are described by `manifests/excluded/`.
The script prints the aggregate [stage and endpoint receipt](stage-replay.json).

```sh
python -B -m docs.paper.q1.verify.replay_checkpoint_stages
```

The endpoint check keeps both the original completed-output calculation and a
separate pre-cycle calculation. The all-reached diagnostic admits the pre-cycle
graph of a run that later crashed. It leaves the historical run status, protocol,
registry, manuscript and submitted artifacts intact.

## CausalBench evaluator replay

The [filtered-array replay receipt](causalbench-replay.json) covers eight cells:
MeanDifference and seeded random networks at both edge budgets in K562 and RPE1.
The replay verified both input archive hashes and ran CausalBench's split and
statistical evaluator. Every graph hash, edge count, true/false positive count,
false omission rate and Wasserstein score matched the retained cells. Counts,
graph identities and false omission rates were compared exactly. Distances used
an absolute tolerance of `1e-10`.

Run with Python 3.12 and `causalbench==1.1.2`, NumPy, SciPy, scikit-learn and
pandas in a separate environment. The receipt records the package versions used
for scoring. Put both hash-matched filtered arrays and their sidecars under
`external/causalbench/`. The hash check uses whole NPZ bytes. Keep outputs
outside the repository's retained results.

```sh
python -B -m docs.paper.q1.verify.replay_causalbench
```

This check begins with the frozen filtered arrays. The first audit re-merged all
586 retained result rows. Recomputing every control and biological comparison
from arrays and regenerating the filtered inputs from raw H5AD remain separate
checks.

## Crucis test timing

The isolated Windows rerun of
`test_source_alias_filter_generation_and_consumer_cannot_inherit_cursor` passed
in 89.5 seconds using Python 3.12.13. A previous run's 45-second bound expired.
The public baseline's exact revision passed GitHub Actions on Windows 3.12 and
Ubuntu 3.10/3.12. Its Windows suite took about 26 minutes. A timed SQLite probe
found no single traced `execute` call lasting at least 0.2 seconds. The evidence
resolves the observed timeout as insufficient for this test run. It does not
identify a single runtime bottleneck. Source changes to the runtime would need
separate measurement and validation.

## Public reproduction limits

The archived source and committed results cover evidence integrity and the
recorded-result checks above. A fresh public checkout still lacks the retained
Causal-Copilot stage inputs and the hash-bound filtered CausalBench arrays.
Whole-paper native replay would also require historical model and execution
conditions. This audit used local records and public packages and made no new
model calls.
