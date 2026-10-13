**Where we are now:** search finished. Marks: **V** = I saw the raw primary text or file; **A\*** = primary page opened, but read through a summarising fetch (treat as A under the ledger rule); **A** = snippet or memory.

## 1. Causal Chambers
- **Remote Lab exists** (V, docs.causalchamber.ai, package README). `causalchamber.lab` drives Mk2 chambers in Zurich: real-time mode (`set/measure/wait`, one connection per chamber, about 10-12 Hz, described as suited to "active learning, experiment design") and a queue mode.
- **Access and cost:** request form, then "subscriber" credentials (V). No public price. Terms v1.1 (17 Mar 2026): fees per order form in CHF, included hours, right to impose rate limits, generated data jointly owned (A\*). No numeric limits published.
- **Controllable:** all inputs and sensor parameters, never sensor readings (A\*). Light Tunnel Mk2 has up to 99 variables; `linked_leds(_sigmoid)` configurations add tunable effects (V).
- **Simulator:** mechanistic simulators of specific phenomena only (wind-tunnel fan speed, current, pressure; light-tunnel sensors via `lt.Deterministic`; image decoders). Not a full twin (V).
- **Interventions in datasets** (V, READMEs):
  - `lt_interventions_standard_v1`: reference N=10,000 with all actuators independently randomised, plus single-target shifts (N=1,000 each) on R, G, B, both polarisers, six LEDs and the sensor parameters.
  - `lt_validate_v1`: 29 two-level randomised experiments, one per manipulable variable.
  - `wt_validate_v1`: 28 (hatch, loads, potentiometers, sensor parameters).
  - `wt_intake_impulse_v1`: impulses on intake load only, time series, built for an out-of-distribution task.
  - `wt_walks_v1` regime_jumps: 32 regimes of single- or multi-target interventions.
- **Ground truth:** an edge X→Y means intervening on X changes Y's distribution for some setting of the other inputs (V). Edges come from physics knowledge, each checked by a randomised two-level experiment (N=50-8,000 per config, V). Absent edges mean "no significant effect found"; the graph is explicitly not a model of observational dependence (V docs, A\* paper).
- **Graph shape, computed from the package's `ground_truth/main.py` (V):** Mk1 standard graphs are two-layer. Light tunnel 38 variables / 57 edges / 29 parents; wind tunnel 32 / 42 / 21. Every parent is a manipulable root and the longest path is 1. Orientation is trivial once actuator columns are known; the difficulty is power, nonlinearity and sensor-sensor confounding.
- **Results:**
  - Authors' notebook (V), 20-variable light-tunnel subgraph: GES precision .55-.60, recall .56-.62; UT-IGSP .51/.64 with hyperparameters picked against the truth.
  - CDFM paper 2607.11508 (A\*): F1 CDFM .727, TabCausal .603, GES .426, PC .281, AVICI 0.
  - CausalArena includes both tunnels (10k rows, 2k interventional; V), but I saw only pooled real-data scores.
  - No LLM or agent discovery result on chamber graphs appears in the maintainers' paper list (V); agent-tagged entries are forecasting, root-cause and datasheet tools.

## 2. LLM agents and active design
| Work | Environment | Scoring | Headline | Mark |
|---|---|---|---|---|
| ACDB, Deb, Shah, Krishnan 2026, arXiv 2609.31675 | simulated linear-Gaussian, 4-7 nodes, budgeted hard interventions, node indices permuted | directed F1, SHD, efficiency | PC+greedy 42.7 F1; Sonnet 4.6 31.7; GPT-5.4 22.9; random DAG 23.6 | V |
| CausaLab, Yang, Zhang … Peng 2026, 2605.26029 | simulated SCMs, 3-7 nodes, budget 4(k−1) | task accuracy, edge F1, SHD | GPT-5.2-high at 6 nodes: 92% accuracy but F1 .47 observational; 80% / .80 mixed. No classical baseline in the parts I read | V (partial read) |
| Auto-Bench (retitled Auto-Discovery-Bench), Chen et al. 2025, 2502.15224 | oracle graphs, 3-10 nodes, 2×nodes rounds | success rate | GPT-4o 100% at 3-5 nodes, 15-30% at 10; no non-LLM baseline | A\* |
| LeGIT, Li et al. 2025, 2503.01139 | bnlearn Asia/Child/Insurance/Alarm (8-37), ENCO, 33 rounds × 32 samples | SHD, SID | Alarm SHD: LeGIT 17.4, GIT 19.6, random 38.8; uses variable names | A\* |
| IGDA, Havrilla, Alvarez-Melis, Fusi 2025, 2502.17189 | edge-experiment oracle, 8 real graphs, metadata only | graph distance | "often outperforms" a numerical baseline | V (abstract) |
| BoxingGym, Gandhi et al. 2025, 2501.01540 | 10 probabilistic-model environments | information-gain regret, prediction | GPT-4o "struggles"; no graph scoring; no random-design agent | A\* |
| CausalGame, Chen et al. 2026, 2607.04293 | SCM-driven game, 14 scenarios, 10 deployments | survival, rubric | best 68.0% vs optimum 78-85% (V); random 52.0% (A\*) | V / A\* |
| Geng et al. 2025, 2505.17968 | black-box programs, languages, equations | recovery | LLMs fall short of Bayesian inference; active querying helps | V (abstract) |
| ReplaySCM, Batzoglou 2026, 2605.08197 | Boolean SCMs, 6-10 variables, interventions given, not chosen | held-out replay | bnlearn+DSL .60-.62 vs GPT-5.4 .29-.34 | A\* |
| DiscoveryWorld, Jansen et al., NeurIPS 2024, 2406.06769 | text world, 120 tasks | completion, knowledge | strong agents struggle; no graph scoring | V (abstract) |

Pattern: where a classical baseline was included (ACDB, ReplaySCM, Geng) it beat the LLMs. The LLM wins (LeGIT, IGDA) rely on variable names of well-known graphs.

## 3. Classical baselines
- **He & Geng 2008, JMLR:** orient chain components by batch or sequential interventions (minimax, entropy). (A)
- **Eberhardt et al. 2005/2008:** N−1 single-node experiments worst case; about log2 N multi-node. (A)
- **Hauser & Bühlmann 2014, IJAR, arXiv 1205.4174:** greedy single-vertex strategy, and a minimum unbounded target set in polynomial time; compared with random (V abstract). Code in R `pcalg` (A).
- **Shanmugam et al. 2015; Kocaoglu et al. 2017:** separating systems, cost-optimal designs. (A)
- **Agrawal et al. 2019, ABCD, 1902.10347:** budgeted Bayesian design for targeted functionals, submodular guarantee, beats random (V abstract).
- **Squires et al. 2020, 2011.00641:** lower bound of the summed half-largest-clique sizes; directed-clique-tree policy; code `csquires/dct-policy` (V).
- **Choo et al. 2022:** verification number. (A)
- **Tigas et al. 2022, CBED, 2203.02016:** chooses target and value, nonlinear (V abstract).
- **Toth et al. 2022, ABCI, 2206.02063:** query-targeted, Gaussian-process models (V abstract).
- **Neural and amortised:** AIT 2109.02429, GIT 2211.13715, CAASL 2405.16718 (V abstracts).
- **"DOTS":** not identified. Nearest is Intersort (Chevalley et al., 2405.18314), which is not active.

## 4. CausalArena
- **GitHub:** none found. The paper footnote, dataset card and leaderboard link only the Hugging Face dataset and Space; the card ships `tools/validate_submission.py` and a replay sampler, no method wrappers (V card; A\* paper).
- **Replay sampler** (`tools/replay_sampler/replay_sampler.py`, added about 30 Sep; V, read in full with some extraction damage):
  - Targets are exactly the keys of `intervention_resamplers`, assigned round-robin, one target per row, values drawn from the declared resampler. There is no option to choose target or value.
  - In the one spec I opened (manufacturing/031, 22 nodes), 5 targets are declared, all roots; 7 nodes are flagged `intervenable`.
  - A `derived_from_parents` path redraws a non-root target from its own mechanism with parents intact. If any spec uses it, those rows are distributionally observational. Worth counting in the local snapshot.
- **Column order:** the sampler writes columns in `spec["node_order"]` with no shuffle; in that spec the order is topological (V). The paper's main text says nothing on permutation (A\*); appendix B was not read by me.
- **Discussion:** the dataset has one thread, the parquet-conversion bot (A\*). The Space showed none (A\*, the page may not have loaded its list). Web search found no follow-up on ordering, varsortability or leakage.
- **Leaderboard:** the Space lists exactly the paper's 18 methods, with no LLM or agent (V). TabCausal is by the same four authors (V, 2605.31156).

## 5. Static benchmark turned interactive
None found for CausalArena or any released executable-SCM suite. Nearest: AIT, GIT and LeGIT simulate interventions on bnlearn networks; ACDB and CausaLab use their own generators.

## Not found, as far as this search reached
- An LLM agent on the Causal Chambers Remote Lab, or scored on chamber graphs.
- An interactive agent benchmark over CausalArena's SCMs.
- An active benchmark combining named variables, a name or column-order control, and classical design baselines.
- Any public report of the CausalArena column order.

## Not verified
- Pages refused with HTTP 429: arxiv.org/html/2608.28245 (I-FLOP) and arxiv.org/html/2605.27022 (ORCA); abstracts only.
- CausalArena appendices B and C.4.
- Nature paper Appendix V p-value tables.
- Remote Lab prices and limits.
- Whether a GitHub repo exists: GitHub search was blocked for me, so "none" rests on the paper, card, Space and web search.
- BoxingGym venue.
- CausaLab was read by targeted search, not end to end.

**Worth saving:** Mk1 chamber graphs are depth-1 actuator→sensor; the CausalArena sampler intervenes only on declared targets, with no shuffle; ACDB (2609.31675) is the closest prior art.

**Where we're going:** the open design choice is between pool-based replay of recorded chamber interventions and a modified CausalArena sampler with arbitrary targets and shuffled columns.

Raw downloads are in `/tmp/claude-0/-home-claude/303fac33-a1f0-5ae9-88c2-1f3005f493e9/scratchpad/dl/`.
