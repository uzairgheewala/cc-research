# W3: the direction rule (R3), the ledger contract (R0) and the correctness fixes (R1)

Tickets: BLD-22, BLD-19, BLD-20, ADV-01, BLD-06. Written 31 Oct 2026 (UTC) by chat W3, on the second laptop.
Inputs: program v3 sections 3-4, rebase-2026-10-24 section 5, w5-restart-2026-10-30, the q1 page (site/pgs/pg_q1.py),
analysis/reports/run_trace/q011_gas_void.md, fork branches bld-06-refinement-v2 (55a490a) and ext-03-cycle-step-key (da55264),
site/copilot/, analysis/reports/copilot_code_notes.md, ledger/DESIGN.md and ledger/schema02.py, audit/adapters.py.
Nothing here spent API credit. Nothing was committed; messages are in docs/commit_msgs/bld22_*.txt.

## 1. R3, the direction rule (BLD-22): what was done

### 1.1 The current rule, and the case against it
On branch bld-06-refinement-v2, refinement v2's data part (`v2d`) gives every linked pair the commonest of the nine typed
bootstrap outcomes. A direction is therefore committed whenever an arrow is the *plurality* of the 20 resamples. gas/void
(q011): void -> gas in 8 of 20, against 5 that point the true way: committed, wrong, and never shown to the model.

### 1.2 The sufficiency rule (r3s)
For every pair v2d leaves fully directed d: keep d only if at least K_MIN of the N resamples give exactly d. K_MIN is the
smallest count whose two-sided 95% Wilson lower bound is above 1/2 ("a majority of resamples, with 95% confidence"); N = 20
gives K_MIN = 15. Otherwise the pair stays linked with its direction open (o-o if any resample or the algorithm gave the pair
a PAG mark, else undirected), with source `data: direction open (k of N below K_MIN)`.
- Links never change. Since K_MIN > N/2, every arrow r3s keeps is one v2d commits: the rule only removes arrows, so it adds
  no directed cycle.
- K_MIN comes from the confidence level, not from the data. The sweep over K below is sensitivity on dev only.
- Typed gaps: semi-directed marks (o->, o-) pass through unchanged; resample stability is not correctness (section 1.4).

### 1.3 The replay table (development battery, exact references)
The battery: CausalArena dev split, replicate 0, both families, replayed with Causal-Copilot's own PC and bootstrap
(`jobs/bootstrap_replay_ca_dev`, `jobs/bootstrap_replay_ca_formula_dev`): 35 files with a result (semantic 23 of 25, in released
column order; formula 12 of 25, columns permuted; the other 15 failed in the replay: 13 on a singular correlation matrix in PC's
Fisher-z test, 2 on the per-file time limit).
Counts are over unordered pairs in all 35 files. Source: `analysis/results/refinement_r3/dev.json` (sha256 929a7c69...).

| Graph | True links found | False links | Missed | Right arrows | Wrong arrows | Open | Arrows on false links | Direction precision |
|---|---|---|---|---|---|---|---|---|
| S0, the algorithm's own graph | 667 | 275 | 686 | 415 | 109 | 143 | 235 | 0.792 |
| S1, unmodified main's bootstrap step | 590 | 238 | 763 | 413 | 108 | 69 | 218 | 0.793 |
| **v2d, the current rule** | 667 | 275 | 686 | **443** | **116** | **108** | **250** | **0.793** |
| **r3s, the sufficiency rule** | 667 | 275 | 686 | **295** | **38** | **334** | **58** | **0.886** |

How the last column is derived: direction precision = right / (right + wrong) on true links found. v2d: 443 / (443 + 116) =
0.793. r3s: 295 / (295 + 38) = 0.886.

Paired, r3s minus v2d on the same files (95% interval: 2,000 bootstrap resamples of the 35 files, seed 20261031):
- wrong arrows -78 [-96, -59]: 67% of v2d's wrong arrows removed (78 / 116);
- right arrows -148 [-176, -123]: 67% of v2d's right arrows kept (295 / 443);
- open directions +226;
- arrows on false links -192 [-229, -157]: 77% removed;
- direction precision +0.093 [+0.063, +0.125];
- directed F1 (committed arrows only) -0.074 [-0.093, -0.057]. That metric scores an open direction as a miss, so a
  rule that abstains loses on it by construction. It is reported, not targeted.

By family:
- Semantic: v2d gets 330 right and 82 wrong (precision 0.801); r3s gets 219 right and 23 wrong (0.905); gain +0.104 [+0.070, +0.143].
- Formula, columns permuted: v2d gets 113 right and 34 wrong (0.769); r3s gets 76 right and 15 wrong (0.835); gain +0.067 [+0.007, +0.133].
- The semantic replays keep the released column order, which can favour PC's orientation (BND-06). The permuted family is
  the harder and more honest one.

Live dev runs (contested references, agreement only, not pooled):
- suite_b1, 51 runs against Causal-Copilot's bundled reference graphs: v2d commits 10 arrows that agree and 3 that do not.
  r3s opens all 13 (none reaches 15 of 20), and opens 58 of the 61 arrows on links the reference lacks.
- pass 4b (Sachs, 18 runs): neither rule commits an arrow on a true link.

Sensitivity to K (dev only; K = 15 is frozen):

| K (of 20) | 12 | 13 | 14 | **15** | 16 | 17 | 18 | 20 |
|---|---|---|---|---|---|---|---|---|
| right | 344 | 329 | 315 | **295** | 268 | 248 | 220 | 142 |
| wrong | 68 | 59 | 46 | **38** | 27 | 22 | 14 | 9 |
| precision | 0.835 | 0.848 | 0.873 | **0.886** | 0.909 | 0.919 | 0.940 | 0.940 |

There is no knee: each step up in K trades right arrows for wrong ones at a steady rate. That is why K is fixed by a
confidence level rather than chosen from this curve.

### 1.4 Which wrong arrows survive, and why
- Of the 38 wrong arrows r3s keeps, 37 sit on edges whose direction the true CPDAG compels. In other words, the resamples
  *agree* on a wrong arrow (at least 15 of 20).
- That is a stable error, not an unstable one, and no resampling rule can see it. It is the misspecified score or test
  found in X1-X5: a linear test on nonlinear mechanisms.
- So r3s is the floor for direction from resampling. What remains belongs to R4: the engine slot, v4 candidates and interventions.
- Reversible true edges (direction not identifiable from the pattern): v2d commits 28 arrows on them, 16 right and 12
  wrong, close to a coin flip. r3s keeps 4 (3 right, 1 wrong).

### 1.5 Frozen, and the regression check
- `analysis/results/refinement_r3/RULE.json`, frozen 2026-10-31T04:37:25Z.
  - **Composite sha256 `80c2ee4ec73a39fb6df64d0ead73a5f61cb801727e269af35abdcd9baa403daf`**: the rule file, its frozen
    imports (refinement_v2, refinement_v1, cc_graph, lineage, causalarena_io) and the pre-registration.
  - The rule file alone: `022696870a8dfe97be8ce77ca43c1cef59ed4e88bb3c1b41b2ba6461a4d901cd`.
  - Pre-registration `plans/r3_prereg.json`: `b2d48ccde8941dfa9d425118d40f3c16bbc610af265a5c412eea9072b9402296`.
- No held-out file has been read for r3s. The access log has one line: the regression read.
- Regression, gas/void, `regress_q011.json`, **pass**. On the BLD-06 branch run's own bootstrap table, v2d gives void -> gas
  and r3s gives o-o (8 of 20, below 15): linked, direction open.
  - In the live pipeline this pair would now go to the names part, which the live run measures (L5).
  - It is a regression check only, never a threshold.

### 1.6 Pre-registered predictions for the held-out reads (plans/r3_prereg.json)
| ID | Metric | Supported if | Refuted if | Dev |
|---|---|---|---|---|
| P1 | share of v2d's wrong arrows removed | >= 0.50 | <= 0.30 | 0.672 |
| P2 | share of v2d's right arrows kept (the cost) | >= 0.50 | <= 0.35 | 0.666 |
| P3 (primary) | r3s direction precision | >= 0.85 | <= 0.80 | 0.886 |
| P4 (primary) | lower end of the paired precision gain's interval | >= 0.001 | <= -0.05 | 0.063 |
| P5 (primary) | links identical in every file | 1 | 0 | 1 |
| P6 | share of arrows on false links removed | >= 0.50 | <= 0.25 | 0.768 |

Batteries:
- **H3, primary, never looked at:** CausalArena test split, *replicate 1*, both families (25 + 25 files). It needs two
  free compute jobs (`jobs/r3_heldout_*_rep1.json`, script `analysis/refinement_r3_replay.py`).
- **H1, secondary:** the replicate-0 test replays. These were opened before by BND-10 and by BLD-06's data part, for other rules.
- **H2, secondary:** the S2 live bootstrap tables, opened before by BND-10 and BLD-06.

**Decision rule.** Adopt r3s on the branch if P3, P4 and P5 hold on H3. It is not adopted if P3 or P4 is refuted, or P5
fails. Otherwise the result is inconclusive and a larger battery comes next. H1 and H2 are reported beside H3 and cannot
overturn it. Each battery is read once under the composite hash.

### 1.7 Fork branch (one per ticket)
`bld-22-direction-sufficiency`, stacked on bld-06-refinement-v2 because it changes that branch's drop-in.
- **The patch:** `jobs/fork/bld-22-direction-sufficiency.patch` (sha256 c163160e...), two files.
  - `refinement_v2_dropin.py` gains `gate_directions` between the data part and the names part, and `refine` records
    `v2d_graph` and `direction_gates`.
  - `judge.py` passes `boot_num`.
  - `CC_DIRECTION=plurality` restores bld-06's behaviour.
- **Supporting files:** manifest and spec `jobs/fork/bld-22-direction-sufficiency.{sha256,json}` (bld-06's manifest with the
  two files re-hashed; a test checks that only those two differ); copies in `jobs/fork/bld-22/`; builder
  `jobs/fork/make_bld22.ps1` (Uzair runs it: a commit and a local push).
- **Tests:** `analysis/refinement_r3_test.py`, 8 tests, all passing in the VM. The drop-in gives the same graph as the
  analysis rule on all 104 dev cases; `plurality` gives v2d exactly; the names part is asked about every opened pair; links
  are never changed.

## 2. R3 next: the live run (proposed, not run): `plans/r3_live_proposal.json`
- **Arm R:** bld-22 on the 30 S2 tables, about $5.3. Each run records v2d's graph, every gate and every names answer, so the
  current rule (v2 = v2d + names) is rebuilt *inside the same run* on the same bootstrap tables and the same answers. The
  comparison is paired and free of bootstrap noise, so no separate bld-06 arm is needed.
- **Arm M:** unmodified main on the rebuilt image, about $13, the required control.
- **Total:** about $18-21, cap $30, about 12-14 h of wall time on the second laptop. Gated on the branch build, a free stub
  series (`plans/r3_stub.json`) and the tests on the host.
- **The new question it answers (L5):** do the directions r3s leaves open get handed to names? On swapped names the model
  follows the labels (BND-08: 81 of 101). If L5 holds, R3 part 2, "knowledge as orient-only tiers", has to come before r3
  ships with the names part reaching opened pairs.

## 3. R0, the contract (BLD-19): design, to be agreed with W2 and W5
The ledger format is the contract between A and B (program v3 section 1). R0 extends what exists. It does not invent anything.

### 3.1 Starting point
`cc-claim-ledger/0.2` (ledger/schema02.py, verify02.py: checks V1-V8) was built for the kernel. The agent's refinement record
(bld-06, bld-22) already holds the pieces of a ledger: per pair, the type, a source string, the resample tally, the gates,
and the names answers.

### 3.2 Proposed `cc-claim-ledger/0.3` (agent profile): deltas against 0.2
| Axis | 0.2 | 0.3 proposal | Why (where it was seen) |
|---|---|---|---|
| relation | x->y, x-y, none, x<->y | + `x o-> y`, `x o- y` (PAG semi-marks, kept, not coerced) | FCI outputs in the S2 runs; r3s passes them through (typed gap) |
| direction_source | data_pattern, data_form, intervention, knowledge, none | + `data_resample` (a direction kept because the resamples agree) | r3s: the arrow's licence is the tally, not the algorithm's rule |
| licensed_by | v_structure, meek_r1..4, ..., score_search | + `algorithm_output` (the wrapper's own mark, rule not exposed), `resample_majority` (k >= K_MIN), `names_unanimous` (three paraphrases agree) | Causal-Copilot wrappers do not expose which rule oriented an edge |
| evidence types | ci_test, score_delta, functional_asymmetry, intervention_shift, knowledge_statement | + `resample_tally` (the nine typed counts of k of N, N, the K_MIN in force), `algorithm_output` (algorithm, hyperparameters, data hash) | the bootstrap tables are the evidence r3s uses |
| open direction | x-y with direction_source none | unchanged, and **required** to carry the gate's tally when an arrow was opened | an abstention must say what it abstained from |
| confidence | bootstrap frequency, calibrated probability | k / N with its Wilson interval; calibrated probability null until R4 | no calibration set exists for the agent yet |
| report | as 0.2 | + `system`: fork branch, commit, patch sha256, image id, model snapshot; `rule`: composite sha256 of the frozen rule | the certificate (program v3 section 2.2) needs system identity |
| verifier | V1-V8 | + V9 (the agent's delivered graph equals the graph rebuilt from the claims), V10 (every opened direction cites its resample_tally, and k < K_MIN holds in it) | the report and the ledger must not disagree (note 15, R5) |

### 3.3 Binding times
Each object is bound once, in this order, and a later stage only adds records:
1. variables, at data load (`var_id` = content hash);
2. algorithm output, at fit;
3. resample tallies, at the bootstrap;
4. gates, at refinement;
5. names answers, at the ask;
6. claims, at resolution;
7. report and hash, last.

### 3.4 Where things live
- The schema and verifier stay public in cc-research `ledger/`, later in `<system>-research`.
- The agent writes `ledger.json` beside its outputs, through a writer on branch `bld-19-ledger-writer` (stacked on bld-22).
  It vendors no cc-research code: it writes the format, and the public verifier checks it.
- An **offline builder** in cc-research turns any recorded run (state snapshots plus bootstrap pickles) into a 0.3 ledger.
  This lets R0 be verified on the BLD-06 and BLD-22 runs with no new live spend.

### 3.5 Failure modes, named before they happen
1. **The writer crashes and ends the run.** The writer is wrapped; a failure is recorded as `ledger_error` in the run summary
   and never stops the run.
2. **Format drift between writer and verifier.** The ledger carries `format` plus the schema sha256, and the verifier refuses
   unknown versions.
3. **Position mistaken for identity.** Variables are identified by content hash, so the three name arms of one table give the
   same `var_id`s.
4. **The report contradicts the ledger.** Caught by V9.
5. **An abstention hides a decision.** Caught by V10.

### 3.6 To agree (questions for W2 and W5; nothing is built until both answer)
- **W2-1** Does the audit package's L3 (claim provenance) read a system's ledger when it has one, and fall back to arm
  differences when it has none? Proposal: yes, one adapter path.
- **W2-2** Scoring convention: an open direction is no prediction. Proposal: the audit protocol reports right, wrong, open and
  partial separately, as in section 1.3, and treats directed F1 as secondary.
- **W2-3** The relation vocabulary with PAG semi-marks: keep them in typed findings, or map them? Proposal: keep them.
- **W2-4** Should typed findings cite claim ids (for example `knowledge_reversed_data` -> claim id)? Proposal: yes when a
  ledger exists.
- **W2-5 (battery):** B now uses CausalArena's test split, replicate 1, as R3's held-out H3. A must not count it in its
  sealed battery. CausalArena is public in any case, so A's sealed battery should come from a withheld-seed generator.
- **W5-1** The format name and version (`cc-claim-ledger/0.3`), and the program doc section that records it.
- **W5-2** BLD-19's criterion: "agreed by W2, W3 and W5" plus "a ledger from an unmodified run validates". Proposal: add
  "and from a BLD-22 run, offline".

### 3.7 R0 bundles
| Bundle | What | Must show |
|---|---|---|
| R0-1 | Agreement on 3.6, written into the program doc (W5) | the answers; the version string |
| R0-2 | `ledger/schema03.py`, `verify03.py` (V1-V10), and the offline builder over recorded runs | a ledger built from one BLD-06 branch run and one main run validates; the verifier re-derives every claim; V9 and V10 fail on hand-broken copies |
| R0-3 | Writer on branch bld-19-ledger-writer | stub series: one ledger per run; each validates; byte-identical to the offline builder's ledger for the same run |

## 4. R1, the correctness fixes (BLD-20): design
Source: the 16 notes in analysis/reports/copilot_code_notes.md, plus EXT-03 (done) and D1-D9. Each fix class gets its own
branch from a31aa7c, so each can be measured against main alone. The integration branch is their sum.

| Branch (proposed) | Notes | Defect class | How the fix is shown (free) |
|---|---|---|---|
| bld-20a-crash-guards | 2 (domain_index read before data load), 5 (EDA stationarity outside try), 6 (reranker's unknown-name filter works on a copy) | a crash path | a stub run that crashes on main (query with a domain index; a constant series; a stub model naming an unknown algorithm) completes on the branch |
| bld-20b-missingness | 4 (imputation fills in place before the missingness check) | silently wrong state | a table with injected missing values: main reports `missingness` False, the branch True; the graph is unchanged |
| bld-20c-hparam-keys | 11 (`lambda_1` vs `lambda1`; PCParallel has no profile), 10 (index restore is a no-op; `high_corr_features_removed` holds the kept columns) | a choice silently dropped or mislabelled | unit check: the NOTEARS choice reaches the wrapper; the removed list names the removed columns |
| bld-20d-hygiene | 3 (output directories ignored), 8 (prompt written into the repository each run) | side effects | the tree identity check shows no repository write after a stub run |
| (none) | 13, 14 (the review prompt has no bootstrap numbers; model edges shown as the algorithm's) | superseded | refinement v2 replaces that review on the integration line; fixed on main only if Uzair wants it |
| (none) | 15 (`meaningful_feature` never set: wrong report template) | belongs to R5 | the report is rendered from the ledger in R5 |
| (none) | 1, 7, 9, 12, 16 | documentation or out of the command-line path | recorded, not fixed |

- **Predictions:** no graph metric moves on the 30 S2 tables. None of them has missing values, a domain index or a constant
  series, so a moved metric would itself be a finding.
- **Live:** no live run of its own. R1 joins the integration branch's next live series, which can share arm M with the R3
  run if both are run on the same image in the same week.
- **Ticket change for W5:** BLD-20 holds four branches. Either sub-tickets (BLD-20a-d, or new IDs from `trace.py next-id
  BLD`), or one ticket with four evidence lines. Default: new IDs.

| Bundle | Must show |
|---|---|
| R1-1 per branch | the failing stub on main; the passing stub on the branch; the tree manifest and spec; the patch sha256 |
| R1-2 integration | the integration branch equals the sum of the patches (a test); its stub series completes |

## 5. Run sheet for Uzair (this wave)
| # | Step | Cost | Time (estimate) | Gate |
|---|---|---|---|---|
| 1 | Review; commit cc-research with `docs/commit_msgs/bld22_cc-research.txt` | 0 | | |
| 2 | `powershell -ExecutionPolicy Bypass -File .\jobs\fork\make_bld22.ps1`, then push the branch | 0 | 10 min | preflight nollm ok |
| 3 | `py -3 analysis\refinement_r3_test.py --out %TEMP%\r3t` on the host | 0 | 1 min | ok: true |
| 4 | `cc.ps1 compute r3_heldout_semantic_rep1.json` and `cc.ps1 compute r3_heldout_formula_rep1.json` (H3) | 0 | 1-2 h | JOB-COMPLETE |
| 5 | `$env:CC_BRANCH="bld-22-direction-sufficiency"; .\cc.ps1 plan r3_stub.json` | 0 | about 45 min | 6 of 6, record fields present |
| 6 | **Decision:** the live series R + M (`harness/live_capped.py --plan plans/r3_live.json --cap-usd 30 --branch bld-22-direction-sufficiency`, then `plans/r3_live_main.json --branch main`) | about $18-21 | 12-14 h | steps 2-5 pass; your go |

After steps 4-5, W3 reads H3 (then H1 and H2) with `refinement_r3.py heldout`, checks the stubs, and writes the live
pre-registration from `plans/r3_live_proposal.json` before step 6.

## 6. Decisions (defaults in brackets)
- **R3-1** Keep K_MIN at 15, from the 95% Wilson bound, rather than 16 (which first reaches 0.90 on dev). [15: frozen]
- **R3-2** H1 and H2 (free, already on disk): read now, or only after H3. [After H3, so the primary read comes first]
- **R3-3** Live arms. [R + M; B off]
- **R3-4** The names part reaches opened pairs in the live run. [Yes: that is L5's question; a "names off on opened pairs"
  switch is built only if L5 holds]
- **R3-5** The battery note to W2 (3.6, W2-5). [Yes]
- **R1-1** Sub-tickets for the four R1 branches. [New IDs, through W5]

## 7. Failure modes for R3, named before they happen
1. **Stable but wrong arrows.** The rule cannot catch them; they are left for R4.
2. **A different resample count.** K_MIN follows N, because the branch reads `boot_num`. A run with N = 10 uses K = 9.
3. **Open directions handed to names.** L5 measures it. Until then, r3 with names on is not "fixed direction".
4. **Holding H3 too tight.** It shares scenarios (graphs) with H1; only its samples are new. It tests the rule on new
   samples of known graphs, not on new graphs. A new-graph battery is the auditor's job (W2: generator with withheld seeds).
5. **Two rules diverging.** The branch's gate drifts from `refinement_r3.r3s`. The equality test runs on all dev cases, and
   the stub check rebuilds r3s from each run's own pickles.
