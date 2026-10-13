# DOM-07 — Primary-source deep reads

Prepared 2026-10-10. Every claim names the URL read and the section, line or table. Quotes are under 15 words.
Line numbers for code come from the fetch tool's numbered rendering of the raw file. They may be off by ±1; re-check them against a local clone before citing in the paper.
"Not verified" means I could not open the source.

---

## (a) CausalArena (Li, Liu, Wang, Ye; arXiv 2609.11897v1, 10 Sep 2026) — appendices B and C

**Citation.** Zi-Rong Li, Si-Yang Liu, Tian-Zuo Wang, Han-Jia Ye. *CausalArena: Benchmarking Causal Discovery in the Foundation Model Era.* arXiv:2609.11897v1, 2026. (https://arxiv.org/abs/2609.11897)

**URLs read**
- Paper HTML: https://arxiv.org/html/2609.11897v1. The fetch tool's text **stops mid-sentence in Sec. 6.2** at about 77k characters. Appendices A–C were never returned.
- Paper PDF: https://arxiv.org/pdf/2609.11897 and https://arxiv.org/pdf/2609.11897v1 both returned 0 characters of text.
- Other attempts: alphaxiv.org/abs and alphaxiv.org/pdf (landing pages only) and export.arxiv.org (refused by robots.txt).
- **Result: Appendix B and Appendix C text is NOT VERIFIED.** Everything below comes from the main text plus the official release files: the HF dataset `LAMDA-Tabular/CausalArena`, the HF Space `LAMDA-Tabular/CausalArena-leaderboard`, and the same authors' public baseline code in `LAMDA-Tabular/TabCausal`.
- **No CausalArena GitHub repository exists.** The LAMDA-Tabular org lists 12 repos and none is CausalArena (https://github.com/orgs/LAMDA-Tabular/repositories). The evaluation tooling lives in the HF dataset under `tools/`.

### What the main text establishes
- **Appendix B is where the answers live, but I could not read it.** Sec. 4.5 says: "Thresholding, CPDAG/PAG conversion rules, runtime budgets, and wrapper defaults are specified in Section B." The wrappers "return a directed adjacency estimate" (Sec. 4.5).
- **Metrics.** Sec. 4.5: "Primary metrics are directed-edge precision, recall, F1, and SHD". The main text gives no SHD formula. The Table 2 caption warns that "SHD is not commensurate across families of different graph size."
- **Replicates and averaging.** Sec. 4.5: each SCM is run with "five in the current main protocol" replicates, and "replicate scores are averaged before aggregation". Sec. 5.1 says tables use "per-unit, replicate-averaged scores, summarized as family-level means." The Table 2 caption says "Cells report mean (standard deviation)."
- **Sample sizes.** Sec. 4.5: the observation-only split uses n_obs = 1000. The mixed split uses 800 observational plus 200 interventional rows.
- **Method list.** Sec. 4.5 lists 18 methods: RandomRegress, CDIS, GIES, IGSP, PC, DAS, LiNGAM, DAGMA, NOTEARS, NOTEARS-MLP, SDCD, Arrow, AVICI, CauScale, CDFM, FoundCause, SEA, TabCausal. **FCI and GES are not in the list.** "GES" appears only as the GIES row run without targets (see code evidence below).
- **The paper averages over all 100 semantic scenarios; the public release has 50.** Sec. 4 says the arena has "100 semantic operational scenarios". It also says "The public Hugging Face package currently releases half of each family."
  - The released breakdown table confirms the paper's averaging: `scenario_count` = 10 per domain × 10 domains, and `replicate_rows` = 50 per domain (https://huggingface.co/datasets/LAMDA-Tabular/CausalArena/raw/main/results/tables/breakdown/semantic_domain_f1_representative.csv; header and rows).
  - The public manifest has `released_per_domain` = 5 (https://huggingface.co/datasets/LAMDA-Tabular/CausalArena/raw/main/scm/semantic/release_split_manifest.json).
  - **So the published 33.522 is a mean over 100 scenarios, half of which are held out. A rerun on the public 50 cannot reproduce it exactly.**
- **Column shuffling.** The main text describes none. The only related wording is RandomRegress as "a fixed-random-order regression control" (Sec. 6.1).

### Answers to questions (i)–(v)

**(i) Method configurations.** Appendix B is not verified. The best available evidence is the same authors' paper-baseline runners in https://github.com/LAMDA-Tabular/TabCausal.
- **Why this repo is the right evidence (inference, not stated by the authors):**
  - The authors are identical (TabCausal arXiv 2605.31156: Li, Liu, Wang, Ye).
  - The baseline lists overlap: PC, GIES, CDIS, IGSP, NOTEARS(-MLP), LiNGAM, DAGMA, DAS, SDCD, RandomRegress, AVICI, SEA.
  - The runners read exactly the CausalArena `.npz` keys `x`, `g` and `mask`. See `run_pc.py` lines 86–88, which match `tools/replay_sampler/replay_sampler.py` lines 920–926.

| Method | Library / call | Settings (file: line) | Undirected-edge handling |
|---|---|---|---|
| PC | causal-learn `pc` (`baselines/paper_algorithms/run_pc.py` L13–14) | `pc(X, alpha=alpha, indep_test=indep_test, stable=True, show_progress=False)` (L106–112). Defaults: `--alpha` 0.05 (L146), `--indep_test` "fisherz" (L147–148). `uc_rule`/`uc_priority` are not passed, so causal-learn defaults apply. On exception the output is an all-zero matrix (L115–117). | `--orientation_strategy` default "liberal" (L150–153). See (ii). |
| GIES (and "GES") | Python `gies` package, `from gies import GIES` (`run_gies.py` L23) | `GIES(score="int", verbose=False)` (L121). BIC penalty `lambda_gies = np.log(n_samples) / 2.0` when the flag is −1 (L99–101, L163–164). Targets come from the flag channel `x[...,1]` (L92, L104–118). The baselines README says GIES with no targets "is the observational GES setting" (`baselines/README.md` L124). | "liberal" default (L171), via `cpdag_to_dag_strategy` (L131, L64–69) |
| NOTEARS | `notears.linear.notears_linear` (`run_notears.py` L16) | `lambda1` 0.1 (L85), `loss_type="l2"` (L53), `w_threshold=0.0` (L54), `h_tol=1e-8` (L55), `max_iter=100` (L56). Then fixed `B = (W_abs >= 0.5)` (L21, L30), diagonal set to 0 (L31). | n/a (DAG output) |
| LiNGAM | causal-learn **DirectLiNGAM** (`run_lingam.py` L13) | `DirectLiNGAM(random_state=seed)` (L48), seed default 0. `W = adjacency_matrix_.T` (L50). Threshold `|W| >= 0.5` (L19, L28). | n/a |
| FCI | none | Not among the CausalArena methods. (`metrics.py` has a `pag_metrics`, but no CausalArena row uses it.) | — |

- Max degree / depth: PC passes no depth limit (L106–112), so causal-learn's default applies (unbounded; library default, not verified here).
- Preprocessing: classical baselines z-score each column, then clip to ±10 (`baselines/paper_algorithms/preprocess.py` L11–17). The README says "Value columns are z-scored per graph over all rows" (`baselines/README.md` L115). The released `.npz` files are already standardised (`replay_sampler.py` L819–829).
- Timeout: "300-second wall-clock timeout by default" (`baselines/README.md` L63).
- Ground truth for scoring: `G_true` is `g` restricted to the observed `mask` on both axes (`run_pc.py` L88, L94). **Check that our rerun drops latent variables in the same way.**

**(ii) Undirected / undecided edges.** The evidence contradicts our assumption of random orientation.
- `baselines/README.md` L118–119: "uncertain edges were not randomized" and "`liberal` strategy orients them from the smaller node index to the larger".
- Code, `run_pc.py` L59–68: `elif G[i, j] == -1 and G[j, i] == -1:` … `if i < j: A[i, j] = 1`. The GIES runner has the same logic at L64–69.
- Bidirected entries (both 1) fall through and are **dropped** (`run_pc.py`; there is no branch for them).
- **Interaction with column order (important).** Released columns follow `generator_spec.json` `node_order` (`replay_sampler.py` L887, L926; README: "same graph, node order").
  - In the one scenario I checked, `node_order` equals the generation-step order, with roots first. That makes it a topological order. Source: https://huggingface.co/datasets/LAMDA-Tabular/CausalArena/raw/main/scm/semantic/artifacts/education/021_classroom_co2_attention_reading_classroom_co2_and_reading_attention/generator_spec.json, `node_order` vs `generation_steps`.
  - If this holds across files, then "smaller index → larger index" always orients a true undirected edge in the **causal** direction. That systematically favours PC and GIES.
  - Status: this is an inference from one scenario plus code, and should be verified on all 50 public scenarios.

**(iii) SHD definition.** CausalArena's own text is not verified. Its schema says only `shd` = "Structural Hamming Distance after applying the official orientation/output rule." (https://huggingface.co/datasets/LAMDA-Tabular/CausalArena/raw/main/schemas/summary_columns.md L18). `nshd` = "Normalized SHD." (L19), with no formula. The authors' code gives two implementations, and both count a **reversed edge as 1**:
- `baselines/paper_algorithms/metrics.py`, `dag_metrics` (L196–219):
  - L207: `diff = np.abs(A_true - A_pred)`
  - L208: `shd = np.sum(diff) - 0.5 * np.sum(diff * diff.T)`
  - A reversal gives sum(diff) = 2 minus 0.5·2 = **1**. Missing or extra edges count 1 each.
  - F1, precision and recall come from sklearn on the flattened directed matrices (L202–204).
- `tabcausal/metrics.py`:
  - L21: `"""Compute SHD with edge reversals counted as one edit."""`
  - L24–26: `mistakes = diff + diff.T`, then clipped to 1, then `np.triu(..., k=1).sum()`
- Both are computed on the **directed adjacency after orientation**. That is a DAG-like matrix, not a CPDAG, so undirected edges never reach SHD.
- **Reading of our gap: our SHD is 37.5, their published value is 33.522, and F1 matches.** If our SHD counts reversals as 2 (for example cdt's `SHD(double_for_anticausal=True)` default, or FP+FN), F1 stays the same and SHD rises by exactly the number of reversed edges per graph. A gap of about 4 per graph is plausible for 25–67-edge graphs.
- The second confound is 100 vs 50 scenarios, from point (v).

**(iv) Column order shuffling.** No evidence of shuffling anywhere.
- `replay_sampler.py` has no shuffle or permutation code (keyword search). It writes `node_ids=np.array(node_order…)` (L926).
- Neither `run_pc.py`, `run_gies.py`, `run_notears.py` nor `run_lingam.py` shuffles. Seeds are set but unused for permutation, and files are processed in sorted order.
- The submission format carries a `node_order` array (`tools/validate_submission.py` L183, L193–195).
- Conclusion: columns are presented in the generator's `node_order`, which is topological in the one checked scenario.

**(v) Files per scenario and how std is computed.**
- Five replicate files per scenario and regime: the selection rule includes "all 5 replicates for obs-only and obs+int exports". Files are named `…__semantic_obs_only__rep000.npz` to `rep004` (release_split_manifest.json).
- The edge-error shards show `"reps": 5` (https://huggingface.co/spaces/LAMDA-Tabular/CausalArena-leaderboard/raw/main/assets/data/semformula_edge_error_shards/Formula__biology_physiology_and_ecology__monod_microbial_growth.js).
- The validator enforces a unique key (method, family, graph_key, regime, repeat) (`tools/validate_submission.py` L123–126).
- The std in the main table is most likely **across SCMs of replicate-averaged scores**:
  - The breakdown CSV has separate columns `F1_scm_std` and `F1_rep_std_mean`.
  - PC's synthetic SHD std (148.9) is far larger than any within-SCM replicate spread would produce.
  - Status: inference. Appendix C is not verified.
- Published PC row (https://huggingface.co/datasets/LAMDA-Tabular/CausalArena/raw/main/results/tables/main/main_leaderboard_shd_wide_with_std.csv): `PC,--,115.370 (148.919),--,33.522 (9.355),--,31.100 (6.782),59.997 (55.019)`.
- GIES semantic obs-only is 33.404 (15.167). NOTEARS is 38.082 (8.459). LiNGAM is 38.930 (9.316).
- The compact table note reads: "Each cell reports F1 / SHD as mean\scorestd{standard deviation}." (results/tables/paper_compact/main_compact_f1_shd.tex)

### What it leaves open
- The Appendix B wording itself. The authors' code is strong evidence, but CausalArena may have used different flags than the TabCausal defaults.
- Whether every semantic `node_order` is topological (one scenario checked).
- The `nshd` normaliser.
- Whether the std is computed over 100 SCM means or over 500 rows.

### Relevance
- The SHD gap is fully explainable without any bug in our PC: reversal = 1 in their code, plus 100 vs 50 scenarios.
- "Liberal" orientation combined with topological column order is a validity concern. It inflates CPDAG-producing methods, and our audit should **re-score with permuted columns**.
- Action items:
  1. Recompute our SHD with `dag_metrics` (L207–208).
  2. Apply the liberal orientation rule.
  3. Restrict to the `mask` columns.
  4. Report public-50-only alongside the full-100 published numbers.

---

## (b) CausalDS (Leban & Sun; arXiv 2607.08093v1, 9 Jul 2026)

**Citation.** Andrej Leban, Yuekai Sun. *CausalDS: Benchmarking Causal Reasoning in Data-Science Agents.* arXiv:2607.08093.
**URLs read:** https://arxiv.org/abs/2607.08093, https://arxiv.org/html/2607.08093v1 (Sec. 1–3 only; Sec. 5 and App. A.1/A.9 were not returned), https://github.com/andleb/causalds

**Establishes**
- Each "scene" is a sampled SCM plus synthetic observational data plus a natural-language story. Graph properties are "calibrated against empirical histograms from real-world causal datasets" (Sec. 3.1).
- An observation model replaces some variables with noisy measurement bundles (Sec. 3.2). Real-data grounding of distributions is optional (Abstract). There are 953 scenes with 3 observation-model variants each (Sec. 3.5).
- Tasks span Pearl's rungs R1–R3 (Sec. 3.4, Table 1). The only graph task, "causal sketch", asks the agent to "Recover the story-implied graph as a directed edge set". That is graph recovery from the story, **not** discovery from data.
- Abstention on non-identifiable estimands is "a first-class scored outcome" (Sec. 1). R1 prediction may require a "central 90% interval" (App. A.16, as reported).
- Agents run in mini-swe-agent inside a sandboxed Docker container with no network (Sec. 3.6).
- From the GitHub README:
  - Licence: code Apache-2.0, data CC0-1.0.
  - Contents: a released 100-task exam plus an HF mirror.
  - Scoring: CausalDSScore combines (1 − Pass Rate), SNR and Med. F1-Loss on the structure-recovery pool.
  - Six models were evaluated (Claude Opus 4.8 is reported first at 0.2780).

**Leaves open**
- The exact scoring formulas (App. A.9, Tabs. 8–10) are not verified.
- It does not evaluate Causal-Copilot; no mention in the text I read.

**Relevance**
- It is a template for scoring abstention and intervals in an agent audit.
- It is not a discovery-from-data benchmark, so it is not a substitute for CausalArena.

---

## (c) CARE (Dong, Liu, Aloui, Tarokh, Carlson — Duke; arXiv 2511.16016v1)

**Identification.**
- Searching "CARE" with LLM and causal discovery returns *CARE: Turning LLMs Into Causal Reasoning Expert* (arXiv 2511.16016). It is the only "CARE" whose method takes **outputs of causal-discovery algorithms plus data** as input, which matches our project context.
- The other hit, arXiv 2402.18139 ("CARE-CA"), is a causal-QA prompting method with no discovery algorithms, so I rejected it.
- Venue: not stated on the abs page.

**URLs read:** https://arxiv.org/html/2511.16016v1, https://arxiv.org/abs/2511.16016

**Establishes**
- It is an SFT framework that teaches an LLM to use algorithm outputs. The Abstract describes "teaching them to effectively utilize the outputs" of discovery algorithms.
- Motivation: prompting with algorithm output "sometimes degrades the causal discovery performance of LLMs" (Sec. 1). LLMs lean on variable-name semantics (Sec. 4, O1).
- Algorithms used: PC, GES, ICA-LiNGAM, DirectLiNGAM, FCI, GRaSP, BOSS (Sec. 2, 4).
- Model: Qwen2.5-1.5B-Instruct with LoRA (r=8, α=16) for 30 epochs (Sec. 6, App. A.3).
- Augmentations include variable-name permutation and column reordering (Sec. 5.2, A1).
- Edge-F1 is judged by GPT-4.1-mini acting as an LLM parser (Sec. 3.1, 6.1). Table 2, Permuted condition: ASIA 0.460, ALARM 0.618, vs best baseline 0.152 and 0.446.

**Leaves open**
- No code link was found.
- The LLM-judge metric is non-deterministic.
- Only a 1.5B model was tested, and scalability to large graphs is untested (App. D).

**Relevance**
- It is direct evidence that LLM+algorithm agents (like Causal-Copilot) are sensitive to names. Name and column permutation is a must-have audit condition.

---

## (d) ACI — Ancestral Causal Inference (Magliacane, Claassen, Mooij)

**Citation.** S. Magliacane, T. Claassen, J. M. Mooij. *Ancestral Causal Inference.* arXiv:1606.07035v3.
- The repo README states a NIPS 2016 paper (https://github.com/caus-am/aci).
- The NeurIPS proceedings page could not be fetched, so the venue is verified only via the README.

**URLs read:** https://arxiv.org/abs/1606.07035, https://arxiv.org/pdf/1606.07035v3, https://github.com/caus-am/aci

**Establishes**
- **Loss (Sec. 3, Eq. 13).** L(W; I) is the sum of weights w_j of the input statements that candidate ancestral structure W violates under the rules R. The paper describes it as summing "the weights of all the inputs that are violated". The search minimises L over ancestral structures.
- **Weights.**
  - Frequentist: w = |log p − log α| (Eq. 14).
  - Bayesian: w = log posterior odds log[p(i|D)/p(¬i|D)] (Eq. 15).
  - Independences should get "a much smaller weight" than dependences (Sec. 3).
- **Confidence score (Sec. 4, Eq. 16).** C(f) = min L with ¬f forced (at infinite weight) − min L with f forced. This approximates the log-odds of f under a Markov-logic view. C(f) > 0 favours f.
- **Solver.** ASP, "For ACI we use the state-of-the-art ASP solver clingo 4" (Sec. 3). The coarser ancestral representation gives orders-of-magnitude speedups over HEJ (Abstract).
- **Code.** Licence BSD-2-Clause; mostly R plus ASP encodings plus Matlab experiments; needs clingo 4 (repo README).

**Leaves open**
- Calibration of C(f) as a probability is not claimed; it is only a log-odds approximation.
- Scaling past roughly 10–15 variables.

**Relevance**
- ACI's C(f) is a principled per-edge or per-ancestry confidence that could be fed into the same calibration study as bootstrap frequencies (DOM-08).
- The weighted-violation loss is also a clean formalism for "LLM constraint vs data".

---

## (e) Li & Russo — LLM constraints in Causal ABA with data veto

**Citation.** Zihao Li, Fabrizio Russo (Imperial College London). *Leveraging Large Language Models for Causal Discovery: a Constraint-based, Argumentation-driven Approach.* Proceedings of the 42nd Conference on Uncertainty in Artificial Intelligence (UAI 2026), PMLR 337:3631–3667. arXiv:2602.16481.

**URLs read:**
- https://arxiv.org/html/2602.16481v1
- https://proceedings.mlr.press/v337/li26e.html
- https://raw.githubusercontent.com/briziorusso/ArgCausalDisco/main/abapc.py
- https://raw.githubusercontent.com/briziorusso/ArgCausalDisco/main/causalaba.py
- https://github.com/briziorusso/ArgCausalDisco

**Establishes**
- **Elicitation.** An LLM elicits required and forbidden arrows from names and descriptions. It is queried 5×, and only constraints proposed in all runs are kept (Sec. 4.1, App. A.3). The paper itself says "Consensus does not guarantee correctness" (Sec. 4.1).
- **Data veto (Sec. 4.2).**
  - Skeleton reduction: "edges corresponding to a high-confidence independence test are removed".
  - Then: "we discard any required arrow whose corresponding undirected edge was removed".
  - Forbidden arrows only restrict orientation.
  - The paper gives no numeric "high-confidence" cutoff. Sec. 6.1 uses α = 0.05 for the G² test.
- **Priority and weights.** CI facts are soft weighted constraints, ranked by p-value strength. LLM arrows are hard constraints (Sec. 4.2, footnote 2: "changing from a hard constraint to a soft, weighted constraint"). The solver is clingo ASP. Symbolic traceability comes from stable semantics (Sec. 3).
- **Evaluation.**
  - Data: bnlearn networks plus 54 CauseNet-grounded synthetic DAGs (5/10/15 nodes), with 5,000 samples × 50 repeats.
  - Metrics: NSHD, F1, SID.
  - Baselines: MPC, ABAPC, FGS, NOTEARS-MLP, GRaSP, BOSS, LLM-BFS (Sec. 5–6).
- **Code level (ArgCausalDisco `main` branch).** No paper-specific repo URL is given; the paper says "our repository" without a link (Sec. 6.1). I am treating the authors' base repo as the closest implementation. It is **not verified** to be the exact paper code.
  - `abapc.py`:
    - L108: `dep_type_PC = "indep" if p > alpha else "dep"`
    - L109: `initial_strength(p, len(S), alpha, 0.5, n_nodes, ...)` assigns a strength to each CI fact.
    - L122: the strength becomes a weak-constraint weight `:~ ext_… [-{int(s[5]*1e14)*2}]`.
    - L137: a `skeleton_rules_reduction` flag is passed through.
  - `causalaba.py`:
    - L105–107: `if skeleton_rules_reduction:`, then `forbidden_edges = indep_facts.keys()`, then `G.remove_edges_from(...)`. Any pair with a recorded independence fact is removed; there is no extra strength check in this code.
    - L114/116: `req_dir = set(prior_knowledge.required)`, `forb_dir = set(prior_knowledge.forbidden)`.
    - L132–134: forbidden arrows become the ASP constraint `":- arrow({X},{Y})."`.
    - L135–139: required arrows become the fact `"arrow({X},{Y})."` **only if** `(X,Y)` and `(Y,X)` are not in `forbidden_edges`. Otherwise it logs "Required edge … is in the forbidden edges set." **This is the data veto, at code level.**
  - No "llm" string appears in either file. LLM output enters only through the `prior_knowledge` object.

**Leaves open**
- The exact repository and commit for the UAI paper.
- How "high-confidence" maps to `indep_facts`. The code removes every pair with an independence fact. The paper speaks of high confidence.
- The paper is internally inconsistent about which model was used (gemini-2.5-flash vs -flash-lite).

**Relevance**
- This is the reference design for **"LLM proposes, data vetoes, every edge traceable to its supporting facts"**. It maps directly onto the typed-provenance requirement in our Causal-Copilot audit.
- The `causalaba.py` L135–139 pattern is the minimal veto rule to replicate.
