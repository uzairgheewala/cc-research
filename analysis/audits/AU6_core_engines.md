# AU6 Core engines: what exists, what it can do, and what the claim ledger should reuse

Tickets: AUD-23, BLD-02, CAP-05
Written 2026-10-12 by an audit agent; sources read on that date.

## Question

Which libraries and engines exist for causal discovery and downstream causal analysis? For each: what can it do, how well
is it maintained, and how fast is it? What should the planned claim ledger reuse, and what should it build?

## Method

- **Inclusion rule.** Every engine named in the ticket, plus any engine that Causal-Copilot or CausalArena calls
  (gpucsl, XGES, culingam, pyCausalFS, GIES via pcalg). I also added a few that the searches surfaced and that fill a
  building block: pgmpy, Gamella's `ges`/`gies`, Uhler-lab `graphical_models`, and gadjid. Benchmarks and pretrained
  models are covered elsewhere (AU2, DOM-11), so they appear here only as engines.
- **Evidence used, in order of preference:**
  1. Code. I took `pip download` wheels and blobless `git clone`s of 33 repositories.
  2. Repository metadata:
     - commit counts from `git log --since=2025-10-12` on the default branch;
     - LICENSE files;
     - tag dates;
     - PyPI JSON and CRAN DESCRIPTION records.
  3. Official docs and individual issue pages.
  4. Papers (arXiv abstract pages).
- **What I could not reach.** The GitHub issue-list pages and the GitHub API were blocked (see Not read). Known issues are
  therefore taken from three places: the individual issue pages that search surfaced, commit messages (`git log --grep`),
  and my own reading of the code.
- **Web search budget.** The shared budget ran out partway through. Three planned issue-tracker searches did not run
  (listed under Searches).
- **Labels.**
  - `reported`: from the authors' own paper or README.
  - `claim (vendor)`: marketing-style statements without numbers.
  - `second-hand`: someone else's summary.
  - `code reading`: my reading of the source at the version named.
  - `repo metadata`: counts from git, PyPI or CRAN.
  - No numbers were measured in this audit. The 21-of-24 result and the IDA timing come from the project's own earlier runs.

## Findings

### F1. The order dependence we measured comes from Causal-Copilot's private fork of causal-learn, not from version 0.1.3.8 (code reading)

- **The vendored copy is a fork, not release 0.1.3.8.** I ran `diff -rq` of Causal-Copilot's `externals/causal-learn`
  (at commit a31aa7c, 2026-05-15) against the PyPI 0.1.3.8 wheel. About 25 files differ, and the fork adds BOSS, GST,
  CALM, FastKCI, RCIT and BatchKCI.
- **The skeleton step is rewritten.**
  - `causallearn/utils/PCUtils/SkeletonDiscovery.py` (lines 188–218) now runs in parallel with joblib.
  - It queues each pair once, `if x < y`, and `_process_node_pair` tests only conditioning sets drawn from
    adj(x)\{y}.
  - FCI's adjacency search has the same restriction (`causallearn/utils/FAS.py`, lines 193–197).
- **Why this matters.** PC visits ordered pairs, so it tests subsets of both adj(x)\{y} and adj(y)\{x}. Upstream
  causal-learn does this too: its loop `for x ...: for y in Neigh_x` covers both directions.
- **Consequence.** Suppose a separating set exists only among y's neighbours, and y has the higher column index. The fork
  never finds that set. The edge then stays, the stored separating set changes, and so do the colliders oriented from it.
  Which pairs lose half their tests depends on column order, so the output does too. This is a sufficient mechanism for
  the 21-of-24 result. I have not confirmed it with a d-separation oracle run (see Open questions).
- **Upstream PC barely changed between 0.1.3.8 and 0.1.4.8.** A whitespace-insensitive diff shows only a new `max_k`
  depth cap. `UCSepset.py` and `Meek.py` are unchanged. So "upstream 0.1.4.8 is order-invariant" says little about
  version and a lot about the fork. Unmodified PyPI 0.1.3.8 would probably also pass (inference, untested).
- **Two further reproducibility hazards in the fork:**
  - FastKCI silently falls back to KCI when it raises `ValueError` (`_process_node_pair`).
  - The Causal-Copilot PC wrapper defaults to `depth: 4`, while its own `PC.json` tells the LLM that -1 is the default.

### F2. gCastle's PC has the same one-sided pattern in its default variant (code reading)

- **The default variant tests only one side.** In gCastle 1.0.4, `castle/algorithms/pc/pc.py` (lines 388–401) loops
  `for i, j in combinations(nodes, 2)` and tests only subsets of adj(i)\{j}. This holds for the `original` (default) and
  `stable` variants. Only `variant='parallel'` tests both sides (`parallel_cell` calls `test(x, y)` and then
  `test(y, x)`).
- **Consequence.** gCastle PC with defaults is order-dependent by construction, and it can miss separations.
- **A metric bug was fixed only recently.** On 2026-05-29, gCastle fixed `MetricsDAG` reporting a true-positive rate
  above 1.0 when the estimate has bidirectional edges (commit a873bd5). Any published number computed with gCastle
  metrics before that date on CPDAG-like output is suspect.
- **Activity.** gCastle had 2 commits in 12 months (repo metadata).

### F3. Upstream causal-learn is the best permissive engine, but its orientation step is not fully order-free

- **Skeleton.** PC-stable is the default (`stable=True`).
- **Collider conflicts are resolved first-come (code reading).** The default `uc_priority=2` ("prioritize existing
  colliders") keeps whichever conflicting collider it meets first in index order (`UCSepset.py`, lines 92–103). When
  colliders conflict, the output can therefore depend on order. pcalg's `solve.confl=TRUE` exists to remove exactly
  this (manual).
- **Separating sets.** causal-learn stores the union of separating sets per pair. Its co-author J. Ramsey says this
  behaves like conservative PC, and that Tetrad's PC-Stable keeps one set
  ([#175](https://github.com/py-why/causal-learn/issues/175)). Tetrad and causal-learn PC differed on 155 of 4,950
  pairs on a 100-variable fMRI dataset (second-hand, issue report).
- **Issue history:**

  | Issue or commit | What it reports | Status |
  |---|---|---|
  | [#82](https://github.com/py-why/causal-learn/issues/82) | PC learns different graphs under variable reordering | Maintainers say fixed; a contributor asked which commit fixed it and got no answer |
  | Meek-rule bug fix, commit ddac4d9 (2022-03-11) | Wrong Meek orientation rules | Fixed |
  | [#213](https://github.com/py-why/causal-learn/issues/213) | GES type error in 0.1.3.9 | The maintainer's workaround was to stay on 0.1.3.8 |
  | [#246](https://github.com/py-why/causal-learn/issues/246) | FCI rejects the fastkci and rcit tests | Open |

- **Maintenance.** 55 commits and 4 PyPI releases in 12 months; 0.1.4.8 was released 2026-07-11 (repo metadata).
- **Recent additions:**
  - custom CI tests (0.1.4.2);
  - RCIT and FastKCI;
  - DGES;
  - RLCD;
  - "forbid orientation within tier" (2026-02).

### F4. Order independence is documented only by pcalg, the PC-stable GPU ports, Tetrad's PC-Stable, and the equivariant pretrained models

- **pcalg.** `skel.method="stable"` gives an order-independent skeleton. Combining `conservative` or `maj.rule` with
  `solve.confl=TRUE` gives "fully order-independent output" (pc manual; Colombo & Maathuis, JMLR 15, 2014).
- **GPU ports.**
  - cuPC (GPL-3, R + CUDA, last commit 2021) implements PC-stable.
  - gpucsl (MIT, CuPy, last commit 2022) implements PC-stable, and its README says it resolves orientation conflicts to
    match pcalg. Causal-Copilot cites gpucsl as its GPU skeleton route.
- **Pretrained models.** AVICI, FoundCause and Arrow are permutation-equivariant by architecture (DOM-11).
- **Undocumented order behaviour.** bnlearn, Tetrad beyond PC, lingam, DoWhy-adjacent tools, dodiscover, DAGMA and
  NOTEARS say nothing about order.
- **Continuous-optimisation methods have a related scale artefact.** Varsortability: on standardised data some
  continuous methods fail to recover the true DAG or its equivalence class (Reisach, Seiler, Weichwald,
  [arXiv 2102.13647](https://arxiv.org/abs/2102.13647)).
- **Score search is order-sensitive.** Kitson & Constantinou report that column order alone moves hill-climbing F1 by
  0.412 on average, against 0.036 for PC-Stable (second-hand, cluster8 note).

### F5. Determinism has to be tested, not assumed

| Engine | What was found about determinism | Source |
|---|---|---|
| Tetrad | On 2026-07-31, maintainers added `TestBfciDeterminism` to investigate nondeterminism in BFCI and GFCI. They named global RNG use as a source and disabled random edge shuffling in one check. | commit [92a2aea](https://github.com/cmu-phil/tetrad/commit/92a2aea9e39e1f92e99094ad3625e4a0b536728f) |
| pgmpy | On 2026-04-09, GES was made "deterministic across hash seeds". Its result had depended on Python's per-process hash randomisation. | commit [fe19dd8](https://github.com/pgmpy/pgmpy/commit/fe19dd8ed5f5236974aef46701cbe15f2ea3a90c) |
| py-causal (Tetrad via causal-cmd) | Repeated PC runs with identical parameters gave different graphs. Unresolved as of 2019-12-24. | [py-causal #91](https://github.com/bd2kccd/py-causal/issues/91) |
| DoWhy | Per-simulation seeds in `DataSubsetRefuter` were fixed in 2026-06. | DoWhy commit log |
| PC and GES with Fisher-z (causal-learn, gCastle, pcalg) | No RNG in the code path (code reading), so they are deterministic given data and column order. They are not deterministic across column orders (F1–F3). | code reading |

### F6. PAG orientation is where implementations still churn

Tetrad's release notes show FCI and PAG orientation rules corrected across a whole series of releases (git tag dates):

| Release or commit | Date | Change |
|---|---|---|
| 7.6.1 | 2023-11-15 | Hotfix for a tiered-knowledge edge-forbidding bug |
| 7.6.6 | 2024-12-11 | "Final FCI orientation rule corrections" |
| 7.6.7 | 2025-06-04 | "Many FCI/PAG rule fixes" |
| 7.6.8 | 2025-06-11 | Discriminating-path rule reset to the published version; "guarantee legal PAG" bug fixed |
| 7.6.10 | 2026-01-06 | Knowledge-sensitive DAG-to-PAG conversion; an experimental FCIT variant that could produce invalid PAGs removed |
| Commit 1ed439d | 2026-09-01 | Fix for an R4 orientation difference in BFCI |

- **An older report of the same kind.** A Tetrad users-group thread from 2012-08-30 reports FCI with tiers giving a tail
  that contradicts the generating DAG. It records no fix
  ([thread](https://groups.google.com/g/tetrad-users-group/c/Y9Nqm801vFM)).
- **Knowledge in the PyWhy stack.** dodiscover never settled how required and forbidden edges should enter the
  orientation phase without producing an invalid CPDAG or PAG
  ([dodiscover #46](https://github.com/py-why/dodiscover/issues/46)).
- **What this means for us.** Any ledger mark that depends on FCI rules R4 and above must pin the engine and version, and
  should be cross-checked against a second engine.

### F7. Maintenance is concentrated in Tetrad, pgmpy, DoWhy and lingam; most of the PyWhy discovery stack is dormant

Commits on the default branch since 2025-10-12 (repo metadata):

| Activity | Engines (commits in 12 months) |
|---|---|
| Very active | Tetrad 2,051; pgmpy 422; py-tetrad 298; DoWhy 173 |
| Active | lingam 80; causal-learn 55; Tigramite 36; EconML 35; benchpress 28 |
| Low | gCastle (path) 2; CDT 2; pywhy-llm 2; causica 3; causal-cmd 6; gadjid 6 |
| Dormant (0) | dodiscover (last 2024-11-04), pywhy-graphs (2024-11-04), pywhy-stats (2024-05-03), AVICI, SDCD, DAGMA, cuPC, gpucsl, XGES, graphical_models, ges, gies |

- **CausalNex** declared end of life on 2026-06-24 (README). Its final 0.12.2 release went to PyPI on 2026-08-31.
- **pcalg's** latest release is **2.7-12 (2024-09-13)** per the cran.r-universe.dev DESCRIPTION. The
  cran.r-project.org index page, as fetched today, still showed 2.7-11 (2024-02-12), as DOM-10 cited. The same fetcher
  returned bnlearn 4.1.1 (2017) from CRAN, which is clearly stale, so I trust r-universe. Confirm with `available.packages()`.
- **bnlearn** 5.2.1 is on CRAN (2026-07-17).

### F8. Interventions, effects and experiment choice live mainly in GPL R and Java; permissive Python options are fragmentary

| Capability | Engines | Licence and status |
|---|---|---|
| Interventional structure learning | pcalg `gies` and `simy` | GPL |
| | Gamella's `gies` | BSD-3; dormant since 2025-03 |
| | dodiscover `PsiFCI` and `LearnInterventionSkeleton` | MIT; dormant, unreleased |
| | AVICI `interv` mask | MIT |
| | SDCD | MIT, preprint |
| | bnlearn (interventional BD score) | GPL |
| | Tetrad multi-dataset searches (IMaGES, FCI-IOD); no intervention-target model in the manual's list | GPL |
| Effects from a CPDAG or PAG | pcalg `ida`, `jointIda`, `idaFast`, `adjustment`, `gac`, `backdoor`, `optAdjSet` | GPL |
| | Tetrad: IDA editor (7.6.6), recursive adjustment and O-sets (7.6.10) | GPL |
| | Tigramite `CausalEffects` (time series only) | GPL-3 |
| | DoWhy identification | MIT; needs a full DAG in the pages read |
| | causal-learn | none found |
| Experiment choice | pcalg `opt.target` | GPL |
| | CBED | MIT (DOM-10) |

### F9. No LLM layer records where an edge came from

- **pywhy-llm.**
  - MIT; self-labelled "Experimental"; 2 commits in 12 months; not on PyPI.
  - It suggests edges, confounders, backdoor sets and IVs, and critiques graphs.
  - Its examples use `gpt-4`.
  - Nothing on its README covers provenance, caching or calibration.
- **pgmpy `ExpertInLoop`.**
  - It orients each added edge by LLM (via litellm; default `gemini/gemini-1.5-flash`) or by asking the user.
  - The page does not say whether the output records which orientations came from the LLM.
- **Causal-Copilot.**
  - Its LLM chooses the algorithm and hyperparameters through per-algorithm prompt files.
  - It also turns user text into forbidden, required and tier JSON (`causal_discovery/context/hyperparameters/PC.json`).
  - The GPU PC path drops background knowledge (wrapper comment).
- **The gap.** The ledger's per-edge source field (data, intervention, declared knowledge, LLM) has no counterpart in any
  engine read. This agrees with the cluster3 note's conclusion that a typed per-edge evidence record is the defensible gap.

### F10. Speed is not the constraint at CausalArena scale

- **Our scale.** At 20–40 variables and 1,000 rows, every classical engine runs in well under a second per fit.
- **IDA.** In our own earlier timing, local IDA over all 600 ordered pairs took 0.06 s (dom09 note).
- **Reported speed numbers (all at much larger scale):**
  - cuPC: on average 500x (cuPC-E) and 1300x (cuPC-S) faster than serial CPU, and one dataset fell from more than 11 h to
    about 4 s (reported, README and abstract).
  - XGES: "10 times faster" than GES (reported, abstract).
  - SDCD: "can scale to thousands of variables" (reported, abstract).
  - DAGMA: claims to be faster than NOTEARS and GOLEM, without numbers (claim, README).
  - causal-learn GES vs Tetrad: hours vs seconds on 100 variables (second-hand, #175).
- **What costs time for us.** Bootstrap (B ≈ 100) times scenarios times replicates times column permutations. That is
  embarrassingly parallel on CPU, and no GPU engine is needed.

## Typed table (summary)

The full rows, with all fields and sources, are in `AU6_core_engines.json` (36 rows).

- **Commits** means commits on the default branch since 2025-10-12.
- **Order inv.** means column-order invariance:
  - D = documented
  - K = known issue
  - U = unknown
  - E = equivariant by design
  - n/a = not applicable

| Engine | Lang | Licence | Last release | Commits | Order inv. | Deterministic | Interventions | Knowledge | Outputs |
|---|---|---|---|---|---|---|---|---|---|
| causal-learn 0.1.4.8 | Py | MIT | 0.1.4.8, 2026-07-11 | 55 | K (historic #82; collider priority) | yes for Fisher-z | CD-NOD index only | tiers, required, forbidden (PC/FCI/CD-NOD) | CPDAG, PAG, DAG |
| CC-vendored causal-learn fork | Py | MIT | none (a31aa7c) | 12 (CC) | **K: 21/24 files; one-sided skeleton** | yes, but FastKCI falls back silently | no | as upstream, filled in by an LLM | CPDAG, PAG |
| Tetrad | Java | **GPL-3** | 7.6.10, 2026-01-06 | 2,051 | D for PC-Stable only | partial (BFCI/GFCI RNG, 2026-07) | multi-dataset (IMaGES, FCI-IOD) | tiers, required, forbidden | CPDAG, PAG, edge-type bootstrap |
| py-tetrad | Py/Java | MIT (calls GPL) | v0.2.0, 2023 (git install) | 298 | U | U | as Tetrad | as Tetrad | as Tetrad |
| causal-cmd | Java CLI | GPL (pom) | v7.6.10, 2026-01-11 | 6 | U | U (py-causal #91) | as Tetrad | knowledge files | as Tetrad |
| pcalg | R/C++ | **GPL ≥2** | 2.7-12, 2024-09-13 | n/a | **D (stable + solve.confl)** | yes (pc) | gies, simy, opt.target | fixedGaps/Edges, addBgKnowledge | CPDAG, PAG, IDA, adjustment |
| bnlearn | R/C | **GPL ≥2** | 5.2.1, 2026-07-17 | n/a | U (HC order-sensitive, second-hand) | U | interventional BD score | whitelist, blacklist, arc priors | DAG, CPDAG, boot.strength |
| gCastle | Py | Apache-2.0 | 1.0.4, 2025-03-07 | 2 | **K (default variant one-sided)** | yes (PC) | no | PrioriKnowledge (PC, TTPM) | matrices, metrics |
| CDT | Py+R | MIT (repo) / Apache (PyPI) | 0.6.0, 2022 | 2 | U | U | GIES via pcalg | U | networkx |
| DoWhy | Py | MIT | 0.14, 2025-11-08 | 173 | n/a | partial | simulates on a given DAG | user DAG | effects, falsify_graph |
| dodiscover | Py | MIT | unreleased | 0 | U | U | PsiFCI | Context, skeleton phase only | CPDAG, PAG, Psi-PAG |
| pywhy-graphs | Py | MIT | 0.1.0, 2023 | 0 | n/a | n/a | n/a | n/a | ADMG, CPDAG, PAG classes |
| pywhy-stats | Py | MIT | 0.1, 2023 | 0 | n/a | U | k-sample tests | n/a | p-values |
| pywhy-llm | Py | MIT | v0.1 tag, 2025 | 2 | n/a | no | no | LLM suggestions | text suggestions |
| EconML | Py | MIT | 0.17.0, 2026-07-31 | 35 | n/a | U | n/a | roles X, W, Z | CATE with CIs |
| causica (DECI) | Py | MIT | 0.4.6, 2026-10-08 | 3 | U | U | evaluation only | constraint matrix | DAG posterior, ATE |
| Ananke | Py | Apache-2.0 | 0.5.0, 2023 | U | n/a | U | n/a | user ADMG | identification, estimates |
| CausalNex | Py | Apache-2.0 | 0.12.2, 2026-08-31 (EOL) | 9 | U | U | no | U | BN |
| Tigramite | Py | **GPL-3** | 5.2.10.1, 2026-01-14 | 36 | U | seeds handled | multi-context | link_assumptions | ts-CPDAG/PAG, effects |
| lingam | Py | MIT | 1.13.0, 2026-07-22 | 80 | U | yes (random_state) | no | path prior matrix | DAG, order, bootstrap |
| benchpress | Snakemake | **GPL-2** | v2.14.0, 2026-09-22 | 28 | U | U | per module | per module | benchmarks |
| AVICI | Py/JAX | MIT | 1.0.7, 2025-01-03 | 0 | **E** | U | interv mask | no | edge probabilities |
| SDCD | Py | MIT | 0.1.4, 2024 | 0 | U | U | yes | U | DAG |
| DAGMA | Py | Apache-2.0 | 1.1.1, 2023 | 0 | U (varsortability) | U | no | U | weighted DAG |
| NOTEARS ref. | Py | Apache-2.0 | v2.3 tag, 2020 | 1 | U (varsortability) | U | no | no | weighted DAG |
| cuPC | CUDA/R | **GPL-3** | none (2021) | 0 | D (PC-stable) | U | no | no | skeleton |
| gpucsl | Py/CUDA | MIT | 0.0.7, 2022 | 0 | D (PC-stable) | U | no | no | CPDAG |
| culingam | Py/CUDA | MIT | 0.0.8, 2024 | 0 | U | U | no | via lingam | via lingam |
| XGES | C++/Py | **none found** | 0.1.6, 2024 | 0 | U | U | no | no | CPDAG |
| ges / gies (Gamella) | Py | BSD-3 | 2025-03-03 | 0 | U | U | gies: yes | U | CPDAG, I-CPDAG |
| graphical_models (Uhler) | Py | BSD-3 | 0.1a21, 2024 | 0 | U | U | intervention classes | U | graph classes |
| pgmpy | Py | MIT | 1.1.2, 2026-04-30 | 422 | U | partial (GES fixed 2026-04) | on a given model | expert knowledge | DAG/PDAG, BN |
| gadjid | Rust/Py/R | MPL-2.0 | 0.1.0, 2024 | 6 | n/a | n/a | n/a | n/a | AID, SHD, SID |
| why-rs | Rust | MIT/Apache | 0.2.1, 2025-12 | 50 (new) | U | U | sampling | U | U |
| deep_causality_discovery | Rust | MIT | 0.3.4, 2026-01-22 | U | U | U | no | no | SURD report |
| Causal-Copilot wrappers | Py | MIT | v20250312 tag; HEAD 2026-05-15 | 12 | K (via the fork) | no (LLM) | no | LLM-written JSON | adjacency, report |

## (1) Building blocks the ledger needs: best existing implementation and gaps

**1. A joint CI or regression test for each candidate edge, given a partial order.**
- **Best existing pieces:**
  - lingam's `prior_knowledge` matrix: path or no-path constraints with an order-based search; MIT, active.
  - causal-learn's tiered `BackgroundKnowledge` for PC and FCI: MIT.
  - DoWhy `falsify_graph`: tests the local Markov conditions of a given DAG against a random-graph baseline; MIT.
  - Tetrad's Markov checker: GPL.
- **Gap.** No engine takes a partial order and returns, for every candidate edge, a typed test record: the test,
  conditioning set, p-value or effect size, and which order constraint licensed the direction. Our order-given regression
  result (0.714 with true depths) has no library home.
- **Decision.** Build it, using causal-learn's `CIT` classes (`register_ci_test`) as the test backend.

**2. Tiered background knowledge.**
- **Best existing implementations:**
  - causal-learn `BackgroundKnowledge`: tiers, forbid-within-tier (2026-02), regex patterns; MIT.
  - Tetrad knowledge box: the most exercised implementation; GPL.
  - pcalg `addBgKnowledge`: GPL.
- **Gaps:**
  - None of these records why a constraint exists or how confident it is.
  - Enforcement differs between engines. dodiscover applies knowledge in the skeleton phase only; GES in causal-learn
    takes no knowledge; Causal-Copilot's GPU PC path drops it.
- **Decision.** Reuse causal-learn's object as the carrier. Keep the source and confidence of each constraint in the ledger.

**3. Interventions as order evidence.**
- **Best existing implementations:**
  - pcalg `gies` and `simy`, which return I-essential graphs; GPL.
  - Gamella's `gies` in Python; BSD-3, dormant.
  - AVICI `interv` mask; MIT.
- **Gap.** None emits "this arrow is compelled by this intervention target" as a separate, typed fact.
- **Decision.** Build the per-edge attribution. Use `gies` (BSD-3) as the fitter, and pcalg only as a cross-check.

**4. Bootstrap and calibration.**
- **Best existing implementations:**
  - Tetrad edge-type bootstrap: frequencies of every mark type including no-edge, seedable; GPL.
  - bnlearn `boot.strength`: strength plus direction given presence (cluster3); GPL.
  - lingam `bootstrap()`: MIT.
- **Gap.** Calibration: none of the engines calibrates. DOM-08 picks Platt scaling over held-out scenarios.
- **Decision.** Build the resampling loop (trivial) and the calibrator. Copy bnlearn's split of strength vs direction,
  and Tetrad's full mark vector.

**5. PAG marks.**
- **Best existing implementations:**
  - Tetrad FCI, GFCI and BOSS-FCI: most maintained, but rules were still changing up to 2026-09; GPL.
  - pcalg `fci`, `rfci` and `fciPlus`: GPL.
  - causal-learn FCI: MIT; issue #246 is open.
  - pywhy-graphs PAG class: dormant.
- **Gap.** The engines disagree on rules R4 and above (F6).
- **Decision.** Reuse causal-learn FCI. Record the engine and version on every circle or arrowhead. Cross-check a sample of
  scenarios against Tetrad (run as a separate process).

**6. Effect sets via IDA or adjustment.**
- **Best existing implementations:** pcalg `ida`, `jointIda`, `gac` and `optAdjSet`, and Tetrad IDA and O-sets. All GPL.
- **Gaps:**
  - No permissive Python IDA or generalized-adjustment code was found in causal-learn, DoWhy or dodiscover (pages read).
  - The dom09 timing used our own script.
- **Decision.** Build local IDA and amenability checks in Python. This is small: one regression per candidate parent set,
  0.06 s per scenario. Validate the result against pcalg in a test harness that is not shipped.

**7. Experiment selection.**
- **Best existing implementations:** pcalg `opt.target` (GPL; deterministic, graph-only) and CBED (MIT; JAX; DOM-10).
- **Gap.** Neither scores experiments by expected change to ledger claims, nor handles latent confounders (DOM-10).
- **Decision.** Reuse both as baselines and build the ledger-aware objective.

**8. Deterministic hashing of outputs.**
- **Best existing implementation:** none. No engine read provides a canonical graph serialisation or hash.
- **Related fixes.** These show the problem is real:
  - pgmpy's hash-seed GES fix (2026-04);
  - Tetrad's BFCI/GFCI determinism work (2026-07);
  - causal-learn's `GeneralGraph.__hash__` fix (commit e685424, 2026-02).
- **Decision.** Build it. Hash a canonical form: sorted variable names, typed mark matrix, engine name and version or
  commit, CI test and parameters, data hash, seed and column permutation. Make it part of the claim id.

## (2) Known correctness and reproducibility issues, with links

| # | Engine | Issue | Kind | Source |
|---|---|---|---|---|
| 1 | CC-vendored causal-learn | Skeleton and FAS test adj(x) only for x<y, giving order-dependent and incomplete separation search | order dependence, correctness | code: `externals/causal-learn/causallearn/utils/PCUtils/SkeletonDiscovery.py` L188-218, `utils/FAS.py` L193-197 at [a31aa7c](https://github.com/Lancelot39/Causal-Copilot) |
| 2 | CC-vendored causal-learn | FastKCI `ValueError` silently replaced by KCI | reproducibility | same file, `_process_node_pair` |
| 3 | gCastle 1.0.4 | Default PC variant tests adj(i) only for i<j | order dependence | [pc.py](https://github.com/huawei-noah/trustworthyAI/blob/master/gcastle/castle/algorithms/pc/pc.py) (wheel 1.0.4, L388-401) |
| 4 | gCastle | `MetricsDAG` TPR > 1.0 with bidirectional edges; fixed 2026-05-29 | evaluation bug | [commit a873bd5](https://github.com/huawei-noah/trustworthyAI/commit/a873bd540d0a4299f1eb6a8394409c8805c5cf3f) |
| 5 | causal-learn | PC graphs depend on variable ordering; maintainers say fixed, fixing commit questioned | order dependence | [#82](https://github.com/py-why/causal-learn/issues/82) |
| 6 | causal-learn | Default `uc_priority=2` keeps the first conflicting collider in index order | order dependence (latent) | code: `utils/PCUtils/UCSepset.py` L92-103 (0.1.4.8) |
| 7 | causal-learn vs Tetrad | PC differs on 155 of 4,950 pairs; sepset-union vs single-sepset semantics, and different Fisher-z | cross-engine disagreement | [#175](https://github.com/py-why/causal-learn/issues/175) |
| 8 | causal-learn | Meek orientation rule bugs fixed 2022-03-11 | wrong orientation (fixed) | [commit ddac4d9](https://github.com/py-why/causal-learn/commit/ddac4d92a1759afaea6218f0f68b43c8973af1a5) |
| 9 | causal-learn | FCI rejects the fastkci and rcit tests (isinstance check in `fas`) | bug, open | [#246](https://github.com/py-why/causal-learn/issues/246) |
| 10 | causal-learn | GES broken in 0.1.3.9; workaround was to pin 0.1.3.8 | regression | [#213](https://github.com/py-why/causal-learn/issues/213) |
| 11 | Tetrad | Nondeterminism in BFCI/GFCI from global RNG under investigation | nondeterminism | [commit 92a2aea](https://github.com/cmu-phil/tetrad/commit/92a2aea9e39e1f92e99094ad3625e4a0b536728f) |
| 12 | Tetrad | FCI/PAG rule corrections across 7.6.6-7.6.10 and an R4 fix in 2026-09 | wrong orientation rules (fixed) | [releases](https://github.com/cmu-phil/tetrad/releases), [v7.6.8](https://github.com/cmu-phil/tetrad/releases/tag/v7.6.8), [commit 1ed439d](https://github.com/cmu-phil/tetrad/commit/1ed439d42e7424a459f10991a4c345135b355414) |
| 13 | Tetrad | FCI with tiers gives a tail contrary to the generating DAG (2012) | knowledge and orientation interaction | [users group](https://groups.google.com/g/tetrad-users-group/c/Y9Nqm801vFM) |
| 14 | py-causal / causal-cmd | Different graphs on repeated identical PC runs | nondeterminism (unresolved) | [py-causal #91](https://github.com/bd2kccd/py-causal/issues/91) |
| 15 | pgmpy | GES depended on Python hash seed; fixed 2026-04-09; separate GES edge-orientation fix | nondeterminism, orientation | [commit fe19dd8](https://github.com/pgmpy/pgmpy/commit/fe19dd8ed5f5236974aef46701cbe15f2ea3a90c), [commit 72a0f79](https://github.com/pgmpy/pgmpy/commit/72a0f795662b1319ce3d03550840738a6c6948d3) |
| 16 | dodiscover | Required/excluded edges only constrain the skeleton phase | knowledge handling | [#46](https://github.com/py-why/dodiscover/issues/46) |
| 17 | continuous methods (NOTEARS family) | Performance driven by varsortability; fails on standardised data | benchmark artefact | [arXiv 2102.13647](https://arxiv.org/abs/2102.13647) |
| 18 | PC family generally | Adjacency search is order-dependent; PC-stable and conservative variants fix it | order dependence (theory) | [Colombo & Maathuis, JMLR 15](https://jmlr.org/papers/v15/colombo14a.html), [pcalg pc manual](https://rdrr.io/cran/pcalg/man/pc.html) |

## (3) Build versus reuse

**Recommendation: reuse permissive Python engines as data-only backends, pinned by hash; build the ledger layer ourselves;
keep GPL engines as optional, out-of-process cross-checks.**

**Reuse**
- **Upstream causal-learn (MIT) as the default engine** for PC, FCI and GES plus CI tests:
  - pin 0.1.4.8 by wheel hash;
  - set `uc_priority` explicitly;
  - log it.
- **lingam (MIT)** for order-based fits and path priors.
- **AVICI (MIT)** as an equivariant amortised baseline.
- **Gamella's `gies` (BSD-3)** for interventional fits.
- **DoWhy and EconML (MIT)** downstream, once a claim set yields a DAG or an adjustment set.
- **Baselines.** CBED and pcalg `opt.target` remain experiment-design baselines (DOM-10).

**Build**
- The typed per-edge test record given a partial order (building block 1).
- Per-edge attribution of intervention evidence.
- The resampling and calibration layer (DOM-08).
- Python local IDA and generalized-adjustment amenability.
- The ledger-aware experiment objective.
- Canonical hashing.
- An **order-invariance gate**: run every engine under k column permutations and refuse to commit any mark that is not
  stable across them.

**Cross-check, but do not ship**
- Tetrad via causal-cmd, and pcalg via Rscript, in a CI job that compares marks on a fixed scenario sample.

**Do not use**
- The Causal-Copilot fork of causal-learn, except to reproduce Causal-Copilot.
- gCastle PC in its default variant.
- CDT and CausalNex (unmaintained and end of life).
- XGES (no licence).

**Risks**

| # | Risk | Mitigation |
|---|---|---|
| 1 | causal-learn's maintainer bandwidth: 55 commits in 12 months; #82 and #246 not clearly closed. | Pin the version; vendor nothing; contribute fixes upstream. |
| 2 | Building our own IDA or adjustment code risks subtle errors. | Validate against pcalg on random CPDAGs before any result relies on it. |
| 3 | GPL cross-checks constrain what can be redistributed (section 4). | Keep them as separate processes the user installs. |
| 4 | Orientation semantics differ across engines (#175; F6). | The ledger must store which engine's rules produced a mark; it cannot pool marks across engines without stating it. |
| 5 | The order-invariance gate multiplies compute by k. At our scale that is minutes, not hours. | Larger graphs would need the parallel or GPU PC-stable ports. |

## (4) Licences that constrain a public release

| Licence group | Engines | Constraint |
|---|---|---|
| GPL (copyleft) | Tetrad (GPL-3), causal-cmd (GPL per pom), pcalg (GPL ≥2), bnlearn (GPL ≥2), Tigramite (GPL-3), cuPC (GPL-3), benchpress (GPL-2) | Vendoring, linking or redistributing them inside our package would put the combined work under GPL terms. Calling them as separately installed programs is the usual way to keep a permissive release; whether that counts as aggregation is a legal question to confirm, not settled here. |
| Weak copyleft | gadjid (MPL-2.0) | File-level copyleft; using it as a dependency is fine, but modified files stay MPL. |
| No licence found | XGES (no LICENSE file, empty PyPI licence); also TabCausal, SEA and CauScale code from DOM-11 | Cannot redistribute. Running them locally for evaluation is a separate question. |
| Permissive | causal-learn, DoWhy, EconML, pywhy-*, dodiscover, causica, lingam, AVICI, SDCD, gpucsl, culingam, pgmpy, CDT (MIT); gCastle, DAGMA, NOTEARS, CausalNex, Ananke (Apache-2.0); ges, gies, graphical_models (BSD-3) | No constraint beyond attribution (and Apache's NOTICE). |

Further licence details:
- **py-tetrad** is MIT, but everything it runs is GPL-3.
- **CDT's** repository LICENSE says MIT, while its PyPI metadata says Apache 2.0. Its R backends are GPL.
- **Ananke** lists both an Apache classifier and "Other/Proprietary License" on PyPI. Check before vendoring.
- **Causal-Copilot** is MIT and keeps causal-learn's MIT LICENSE. Its other vendored code (pyCausalFS, notears,
  acceleration) ships without its own licence files. Treat that code as licence-unclear if we ever redistribute
  Causal-Copilot patches.

## What this changes for the project

1. **Re-word the column-order finding.** Instead of "causal-learn 0.1.3.8 is order-dependent", say "Causal-Copilot's
   modified causal-learn fork is order-dependent". The specific line-level mechanism (F1) strengthens the audit paper:
   the defect is introduced by the agent's own engineering, not inherited from the library.
2. **Add a d-separation-oracle test (ticket under BLD-02).** It would compare three engines under all column
   permutations of small DAGs:
   - the fork;
   - unmodified PyPI 0.1.3.8;
   - 0.1.4.8.

   It costs minutes and turns F1 from code reading into a mechanism demonstration. Run gCastle `original`, `stable` and
   `parallel` in the same harness.
3. **Make column-permutation invariance a gate in the ledger (CAP-05).** A mark enters the ledger only if it is stable
   across k permutations. Record the engine, version and wheel hash on every claim.
4. **Default engine stack** (MIT, BSD and Apache only): causal-learn 0.1.4.8 (pinned), lingam, `gies`, AVICI, with DoWhy
   and EconML downstream. Tetrad and pcalg run only as CI cross-checks.
5. **Build list for BLD-02**, roughly in order of value:
   1. canonical hashing;
   2. the per-edge typed test record given a partial order;
   3. the bootstrap and Platt layer;
   4. the order-invariance gate;
   5. Python IDA and amenability;
   6. intervention attribution;
   7. the ledger-aware experiment objective.
6. **Audit any published CausalArena or Causal-Copilot number that used gCastle PC defaults or gCastle `MetricsDAG`**
   before 2026-05-29. Flag to AU1 and AU9 which systems call gCastle.
7. **Probably correct DOM-10:** pcalg is likely 2.7-12 (2024-09-13) per r-universe, though the CRAN index page as
   fetched still shows 2.7-11; confirm in R.

## Open questions

- Does unmodified PyPI 0.1.3.8 show the 21-of-24 order dependence? I predict no from the diff, but this is untested.
- How often does causal-learn's `uc_priority=2` first-come collider resolution actually fire on CausalArena data? Logging
  conflicts would tell us. Does `uc_priority=3` or a pcalg-style `solve.confl` change directed F1?
- Is Tetrad's PC orientation order-independent beyond the skeleton? This was not documented in the pages read.
- Does bnlearn's `pc.stable` resolve collider conflicts order-independently? Not read.
- Does lingam's DirectLiNGAM have order-dependent tie-breaking under equal measures? Not read.
- Is calling GPL R or Java engines as subprocesses compatible with an MIT release? This needs a university licensing
  answer, not ours.
- Are DOM-11's pretrained models and CausalArena's own baselines (via TabCausal `baselines/`) running gCastle or
  vendored code with the same pattern? Not checked here.

## Not read

| Source | Reason |
|---|---|
| GitHub issue-list and commit-list pages (`/issues?q=`, `/commits/main`) | robots.txt disallowed WebFetch; individual issue pages and git clones were used instead |
| GitHub REST API | refused for this session by the proxy |
| search.maven.org (Tetrad artifact dates) | proxy denied the connection; git tags were used |
| cran.r-project.org/package=bnlearn, bnlearn.com/news | robots or client error; r-universe DESCRIPTION used |
| Rendered Tetrad manual algorithm pages | navigation-only render; the `_sources/*.md.txt` versions were read |
| gCastle GitHub README | robots-blocked; PyPI page and wheel source read |
| ParallelPC (arXiv 1510.03042, 1502.02454) | seen in search results only |
| XGES PMLR page (proceedings.mlr.press/v244/nazaret24a) | seen in search results only; venue not verified |
| Kitson & Constantinou, arXiv 2206.08952 | not re-read; numbers are second-hand from the cluster8 note |
| bnlearn `arc.strength` manual | not re-read; content from the cluster3 note |
| uhlerlab `graphical_model_learning` algorithms; `conditional_independence` | not opened beyond PyPI metadata and file listing |
| Ananke GitLab history; pgmpy PC and CI-test docs | not opened |

## Searches run

The full list is also in the JSON `searches` field.

**Web searches**
1. causal-learn github issue PC different results when column order changed
2. cmu-phil tetrad releases 7.6 py-tetrad causal-cmd
3. cuPC GPU PC algorithm causal discovery CUDA github
4. site:github.com py-why causal-learn issues PC "order" variables results differ (extended)
5. github causal-learn issue FCI wrong orientation bug background knowledge
6. github causal-learn issue GES nondeterministic results random
7. bnlearn CRAN 5.1 release 2025 NEWS Scutari
8. GPUCSL GPU constraint-based structure learning Python Hagedorn PC github
9. XGES extremely greedy equivalence search C++ github Nazaret Blei
10. Rust crate causal discovery PC algorithm structure learning
11. gadjid Rust adjustment identification distance causal graphs
12. fast C++ PC algorithm causal discovery library parallel ParallelPC pcalg
13. "causal discovery" library written in Rust python bindings PC GES fast 2025 (extended)

**Searches that did not run** (shared search budget exhausted): gCastle PC wrong-result issues; Tetrad FGES
nondeterminism issues; causal-learn GES tie-breaking issues.

**Non-search methods**
- PyPI JSON for 33 package names.
- r-universe DESCRIPTION for pcalg and bnlearn.
- Blobless git clones of 33 repositories, used for:
  - commit counts since 2025-10-12;
  - LICENSE files;
  - tag dates;
  - `git log --grep` on order, determinism, seed, Meek and orientation.
- Wheel diffs: causal-learn 0.1.3.8 vs 0.1.4.8 vs the Causal-Copilot fork. Code reading of gCastle 1.0.4 and DoWhy 0.14.
