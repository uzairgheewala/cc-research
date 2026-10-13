# AU1 — Field systems: who discovers causal graphs, from what evidence, with which directions, measured how

Tickets: STR-01, AUD-18, DOM-11
Written 2026-10-12 by an audit agent; sources read on that date.

## Where we are now

75 systems are typed in `AU1_field_systems.json` (13 classical, 7 continuous-optimisation, 12 pretrained, 23 LLM-assisted, 19 agents or agent environments, 1 benchmark control). This extends and corrects the cluster 1, 2, 7 and 8 notes and DOM-11. No code was run; every number is labelled. The shared web-search budget ran out after 16 searches, so the 2026 sweep for agents and time-series LLM methods is incomplete (see "Searches run").

## Question

Which causal-discovery systems exist today? For each: what evidence may it use (D observational data, I interventional data, K declared knowledge such as names, descriptions, LLM priors or tiers), where do its edge directions come from (data pattern, functional-form asymmetry, interventions, LLM/name knowledge, column order), and how was it evaluated (benchmarks, reported numbers, and any control for variable names or column order)?

## Method

- **Inclusion rule.** A row is a system that outputs a graph or orientations, or an agent that runs discovery. I also kept three effect-estimation agents (CAIS, CATE-B, LLM4Causal) because the brief names them, and one control (RandomRegress). Position papers without a system (Wu et al. 2506.00844) and calibration studies (Kumar et al. 2608.23660) are cited in the text, not tabled. CausalMACE (arXiv 2508.18797) turned out to be a Minecraft multi-agent paper and is excluded.
- **Sources, in order of preference:**
  - arXiv abs and HTML pages, proceedings pages, GitHub pages and PyPI metadata, all read today with a fetch tool;
  - the project's local snapshot of the released CausalArena result CSVs (`external/causalarena/results/tables/...`, mirroring `huggingface.co/datasets/LAMDA-Tabular/CausalArena/raw/main/results/tables/...`; live Hugging Face was blocked by the proxy);
  - the project's earlier notes, used where I did not re-open a paper today. Those rows are labelled `second-hand (cluster/DOM note)`.
- **Labels on numbers:**
  - `reported`: from the method authors' own table.
  - `reported (CausalArena authors' table, not the method authors)`: shown as `rep-CA` below.
  - `reported (X authors, as baseline)`: shown as `rep-other`.
  - `second-hand`: from a project note.
  - `measured (project)`: copied from `audit_context.md` and not re-verified here.
- **Direction-source codes:**
  - `DATA`: v-structures, Meek rules, CI or score patterns.
  - `FUNC`: functional-form asymmetry (non-Gaussian or additive noise).
  - `SCORE(scale)`: a least-squares score whose directions follow marginal variance (varsortability).
  - `INT`: interventions.
  - `LEARNED`: a pretrained prior.
  - `LLM`: names, descriptions or LLM knowledge.
  - `COL*`: column index, entering only through a benchmark wrapper that forces undirected edges to a DAG.
  - `AGENT`: the agent's own reasoning over data and experiments.
- **What "not found" means here.** Code was searched on the paper page, the abs page and one web search. GitHub search and the GitHub API were refused in this session, and commit dates are not visible on GitHub pages, so `last_commit_or_release` uses PyPI upload dates where they exist.

## Findings

### 1. Where directions come from, by family

| Family | Rows | Direction source | What it implies for our controls |
|---|---|---|---|
| Constraint/score (PC, FCI, GES, GIES, IGSP, UT-IGSP, JCI, CDIS) | 8 | **DATA**, plus **INT** for GIES, IGSP and UT-IGSP. Undirected CPDAG edges stay undirected unless a wrapper forces a DAG. On CausalArena it does: the TabCausal/CausalArena runners orient "from the smaller node index to the larger" and the released columns follow a topological `node_order` (DOM-07). PC, GES/GIES and CDIS therefore get part of their published direction accuracy from **layout** (`COL*`). | A column-shuffle arm changes these published numbers. That makes it a validity issue for the leaderboard itself, not only for agents. |
| Functional (LiNGAM, ANM, CAM, RESIT, DAS) | 5 | **FUNC**. They need no names and are order-free in principle. DirectLiNGAM's greedy order search can still depend on ties (not checked). | Low on CausalArena semantic (0.203-0.208, rep-CA), so the mechanisms there are not what these models assume. |
| Continuous optimisation (NOTEARS, NOTEARS-MLP, DAGMA, GOLEM, GraN-DAG, DCDI, SDCD) | 7 | **SCORE**. Linear least-squares variants orient along marginal-variance order (Reisach et al., varsortability; cluster8). DCDI and SDCD add INT. | CausalArena z-scores its data, which removes the variance cue. Consistent with NOTEARS/DAGMA at 0.18-0.20 (rep-CA). |
| Pretrained / amortised (AVICI, CSIvA, SEA, FoundCause, CDFM, Arrow, TabCausal, CauScale, + 4 new 2025-26 abstracts) | 12 | **LEARNED** from a synthetic SCM prior. Whatever regularities the prior has, including sortability artefacts, are inherited: AVICI "may be exploiting" correlation artefacts on iSCMs (cluster8). AVICI, Arrow and FoundCause are variable-equivariant by architecture. SEA uses positional embeddings (order-sensitive by construction, permutation augmentation in training). CDFM, CauScale and TabCausal state nothing. | These are the strongest published numbers on CausalArena semantic, and none was tested with shuffled columns. |
| LLM-assisted (23 rows) | 23 | **LLM/name knowledge**, mixed with DATA in 19 of 23 rows. Mixing rules differ: hard or soft priors (Ban, Srivastava); the LLM verifies only data-proposed edges (ILS-CSL, MosaCD); data vetoes LLM arrows (Li & Russo, MosaCD); a causal order elicited from names (Vashishtha); probabilistic fusion (Kitson & Constantinou); trust-weighted arbitration (CauTion); BIC-gated LLM edits (CauScientist). | Every one of them can take directions from names; only three measured what happens when names change. |
| Agents (19 rows) | 19 | Mostly **DATA (LLM-chosen algorithm) + LLM refinement**: Causal-Copilot, ALCM, MAC, MATMCD, CEA, CausalSteward, CMA. Active-learning agents (ACDB, CausaLab, LeGIT, IGDA) use **INT**. causal-learn+ deliberately keeps the LLM out of edges. | Agents are where names enter silently; our Causal-Copilot measurement (0.306 / 0.232 / 0.142 for real / neutral / swapped names, project) is the only name-swap result for a full discovery agent we know of. |

### 2. Answer (1): which systems report any control for names or column order

Among the 43 rows that may use K, **3 report a measured name control on graph recovery**:
- **CARE** (arXiv 2511.16016) is the only one with a **names-swapped** arm. Arms: original, anonymised, permuted. Asia F1 0.460 and Alarm 0.618 under permuted names (second-hand, DOM-07; scored with an LLM parser). Column reordering is a training augmentation, not a measured factor.
- **Kitson & Constantinou** (arXiv 2608.27472) replace names with neutral but still meaningful aliases ("asia" becomes "endemic_travel"). Fusion F1 0.760 vs BNSL 0.662 vs LLM 0.572 (reported). No column-order control.
- **DMCD** (arXiv 2602.20333) renames to X1..Xn but keeps paraphrased descriptions. Fluxnet F1 rises from 0.751 to 0.79 renamed. Removing descriptions on Tennessee Eastman drops F1 from 0.209 to 0.07 (reported). No column control.

Other controls:
- **Generator-side** (names carry no structure by construction):
  - ACDB anonymises labels and permutes node indices. That is the only `columns_shuffled` entry, applied as a generator precaution, not measured.
  - Causal Agent draws names at random from a 311-word pool.
  - CausaLab puts random SCMs behind fixed template names.
- **Memorisation-only** (post-cutoff or unpublished graphs, no name manipulation):
  - Kıcıman (row-completion probe plus post-cutoff pairs);
  - Takayama (an unpublished health dataset);
  - Vashishtha (less-known graphs);
  - Srivastava (post-cutoff graphs plus completion probes);
  - Li & Russo (CauseNet-grounded novel DAGs);
  - Tench & Demeester (probe).
- **Answer-order (positional-bias) controls**, not column order: MosaCD and CauTion ask each direction in both framings.
- **Architecture-level order invariance**, never measured as a test:
  - AVICI, Arrow, FoundCause by design.
  - FoundCause also averages 10 random permutations at inference.
  - SEA trains with permutation augmentation.
  - Only PC-stable has a published order-independence guarantee (skeleton only; Colombo & Maathuis 2014).
- **Nobody on the CausalArena leaderboard** reports a column-shuffle run. The CausalArena text describes none (DOM-07, re-checked today on the HTML: not stated).
- **Counting rule.** No system reports all three of neutral names, swapped names and shuffled columns. That three-arm control is what the project already runs.

### 3. Evaluation practice

- **Famous named graphs dominate.** 27 of the 43 K-using rows evaluate on bnlearn or other famous named graphs (Asia, Sachs, Alarm, Child, Insurance, Tübingen, Neuropathic, Auto MPG). Those graphs are memorised by current LLMs (Srivastava 2510.16530; cluster 1/2).
- **Where a classical baseline is included in agent or active settings, it usually wins:**
  - ACDB: PC+greedy 42.7 directed F1 vs Sonnet 4.6 at 31.7 and GPT-5.4 at 22.9, below a random DAG at 23.6 (reported).
  - MAC: zero-shot GPT-4o beats the proposed multi-agent models on Sachs (SHD 18, reported).
  - CausalSteward: XGES (0.309) beats CaST (0.10-0.13) on Neuropathic Pain (second-hand).
  - Srivastava: on Sweden transport, PC 0.57 vs LLM 0.31 (second-hand).
- **No LLM method or agent appears on CausalArena.** The leaderboard holds exactly 18 methods (7 pretrained, 10 classical/continuous, 1 control; CausalArena Sec. 4.5).
- **CausalArena ordering (semantic obs-only, rep-CA):**
  - FoundCause 0.634 > GIES 0.552 > CDFM 0.434 > TabCausal 0.422 > CDIS 0.403 > SDCD 0.358 > PC 0.333 > SEA 0.332 > Arrow 0.309 = IGSP 0.309 > AVICI 0.278 > RandomRegress 0.252 > CauScale 0.249 > NOTEARS-MLP 0.221 > DAS 0.208 > LiNGAM 0.203 = NOTEARS 0.203 > DAGMA 0.182.
  - Our measured Causal-Copilot final F1 with real names (0.306, project, public-50 subset) would sit between Arrow and AVICI, below PC. With swapped names (0.142) it would sit below every published row.
- **Semantic scores do not transfer to real data.** On CausalArena real data (13 obs-only tasks, rep-CA), FoundCause falls to 0.212. The best real-data rows are CDFM 0.391 and TabCausal 0.342 obs-only (0.384 all). Every pretrained row's semantic advantage shrinks or reverses, which suggests the semantic/formula generators share regularities with the pretraining priors. This is an inference, not tested.
- **Cost per graph is rarely reported:**
  - Kitson & Constantinou: 18 requests per network per setup, mean 0.05 US cents per request.
  - CauTion: about 26k tokens on Win95pts, against SCP's 3.03M and LLM-BFS's 2.97M (all reported by CauTion).
  - CEA: 26-63 queries per dataset.
  - MosaCD: at least 10 queries per undirected edge.
  - LLM-BFS: about one query per node.
  - CausalArena runtimes: 0.8 to 193 s per row (rep-CA).
- **Corrections to earlier notes:**
  - MAC v1 evaluates three datasets (Auto MPG, DWD, Sachs), not five (cluster 2 said five).
  - CauScientist and CauTion code repositories are placeholders ("Code will be released soon" / "Coming soon").
  - CEA promises code on acceptance.
  - Kitson & Constantinou give no code link; the MIT `causaliq-knowledge` library (PyPI 0.6.0, 2026-04-10) by the same organisation is related but not verified as the paper's code.
  - TabCausal also appears as "CausalTab", an ICML 2026 workshop poster by the same four authors (identity inferred).
  - CAIS does effect estimation only.
  - CDIS's identity on CausalArena could not be resolved (acronym not expanded; reference [21]).

## Typed table (compact; full records in `AU1_field_systems.json`)

Cat: CL classical, CO continuous optimisation, PT pretrained, LLM LLM-assisted, AG agent, CTRL control. "Latent" = can represent hidden confounders. For LLM rows, "no" means the output is a DAG/CPDAG under sufficiency. Controls list only measured name or layout manipulations; other controls are in the JSON `other_controls` field.

| # | System | Cat | Regimes | Direction source | Latent | Name/layout controls (measured) | Headline number [label] | Code (licence) | CPU |
|---|---|---|---|---|---|---|---|---|---|
| 1 | PC | CL | D,K | DATA+COL* | no | none | CausalArena semantic, obs-only directed F1: 0.333 [rep-CA] | gh:py-why/causal-learn (MIT) | yes |
| 2 | FCI | CL | D,K | DATA | yes | none | FoundCause suite directed F1: 0.38 [rep-other] | gh:py-why/causal-learn (MIT) | yes |
| 3 | GES | CL | D,K | DATA+COL* | no | none | CausalArena semantic obs-only directed F1: 0.552 [rep-CA] | gh:juangamella/gies (BSD-3-Clause) | yes |
| 4 | GIES | CL | D,I | DATA+INT+COL* | no | none | CausalArena semantic, obs-only directed F1: 0.552 [rep-CA] | gh:juangamella/gies (BSD-3-Clause) | yes |
| 5 | LiNGAM family | CL | D,K | FUNC | no | none | CausalArena semantic, obs-only directed F1: 0.203 [rep-CA] | gh:cdt15/lingam (MIT) | yes |
| 6 | ANM | CL | D | FUNC | no | none | - | none (?) | unknown |
| 7 | CAM | CL | D | FUNC | no | none | - | none (?) | unknown |
| 8 | RESIT | CL | D | FUNC | no | none | - | none (?) | unknown |
| 9 | IGSP | CL | D,I | DATA+INT | no | none | CausalArena semantic, obs-only directed F1: 0.309 [rep-CA] | causaldag (not shown on PyPI) | yes |
| 10 | UT-IGSP | CL | D,I | DATA+INT | no | none | Causal Chambers precision / recall: 0.51 / 0.64 [2nd] | https://uhlerlab.github.io/causaldag/utigsp (?) | yes |
| 11 | JCI | CL | D,I | DATA+INT | ? | none | - | none (?) | unknown |
| 12 | DAS | CL | D | FUNC | no | none | CausalArena semantic, obs-only directed F1: 0.208 [rep-CA] | none (?) | yes |
| 13 | CDIS | CL | D,I | DATA+INT+COL* | ? | none | CausalArena semantic, obs-only directed F1: 0.403 [rep-CA] | none (?) | yes |
| 14 | RandomRegress | CTRL | D | RANDOM-ORDER | no | none | CausalArena semantic, obs-only directed F1: 0.252 [rep-CA] | none (?) | yes |
| 15 | NOTEARS | CO | D | SCORE(scale) | no | none | CausalArena semantic, obs-only directed F1: 0.203 [rep-CA] | gh:xunzheng/notears (Apache-2.0) | yes |
| 16 | NOTEARS-MLP | CO | D | SCORE(scale) | no | none | CausalArena semantic, obs-only directed F1: 0.221 [rep-CA] | gh:xunzheng/notears (Apache-2.0) | yes |
| 17 | DAGMA | CO | D | SCORE(scale) | no | none | CausalArena semantic, obs-only directed F1: 0.182 [rep-CA] | gh:kevinsbello/dagma (Apache 2.0) | yes |
| 18 | GOLEM | CO | D | SCORE(variance assumption) | no | none | - | gh:ignavierng/golem (Apache-2.0) | yes |
| 19 | GraN-DAG | CO | D | SCORE | no | none | - | none (?) | unknown |
| 20 | DCDI | CO | D,I | SCORE+INT | no | none | - | gh:slachapelle/dcdi (LICENSE.md present, type not shown) | unknown |
| 21 | SDCD | CO | D,I | SCORE+INT | no | none | CausalArena semantic, obs-only directed F1: 0.358 [rep-CA] | https://pypi.org/project/sdcd/ (MIT) | unknown |
| 22 | AVICI | PT | D,I | LEARNED+INT | no | none | CausalArena semantic, obs-only directed F1: 0.278 [rep-CA] | gh:larslorch/avici (MIT) | yes |
| 23 | CSIvA | PT | D,I | LEARNED+INT | no | none | FoundCause suite directed F1: 0.507 [rep-other] | none (?) | unknown |
| 24 | SEA | PT | D,I | LEARNED+INT+COL? | ? | none | CausalArena semantic, obs-only directed F1: 0.332 [rep-CA] | gh:rmwu/sea (not stated) | no |
| 25 | FoundCause | PT | D | LEARNED | yes | none | CausalArena semantic, obs-only directed F1: 0.634 [rep-CA] | gh:amazon-science/foundcause (Apache-2.0) | yes |
| 26 | CDFM | PT | D | LEARNED | yes | none | CausalArena semantic, obs-only directed F1: 0.434 [rep-CA] | gh:DMIRLAB-Group/CDFM (Apache-2.0) | yes |
| 27 | Arrow | PT | D | LEARNED | no | none | CausalArena semantic, obs-only directed F1: 0.309 [rep-CA] | none (unknown) | unknown |
| 28 | TabCausal | PT | D,I | LEARNED+INT | ? | none | CausalArena semantic, obs-only directed F1: 0.422 [rep-CA] | gh:LAMDA-Tabular/TabCausal (none) | yes |
| 29 | CauScale | PT | D | LEARNED | no | none | CausalArena semantic, obs-only directed F1: 0.249 [rep-CA] | gh:OpenCausaLab/CauScale (code: no LICENSE; HF checkpoints tagged Apache-2.0) | unknown |
| 30 | TabPFN causal probe | PT | D | LEARNED | ? | none | - | none (?) | unknown |
| 31 | DCD-PFN | PT | D | LEARNED | ? | none | - | none (?) | unknown |
| 32 | DAG-FM | PT | D | LEARNED | ? | none | - | none (?) | unknown |
| 33 | TabPFN-CFM | PT | D,K | LEARNED | ? | none | - | none (?) | unknown |
| 34 | Kiciman et al. | LLM | K | LLM | no | none | Tubingen pairs accuracy (GPT-4): 0.97 [2nd] | none (?) | unknown |
| 35 | Long et al. | LLM | D,K | DATA+LLM | no | none | - | none (?) | unknown |
| 36 | Ban et al. | LLM | D,K | DATA+LLM | no | none | - | gh:tyMadara/LLM-CD (not checked) | yes |
| 37 | ILS-CSL | LLM | D,K | DATA+LLM | no | none | - | gh:tyMadara/ILS-CSL (none shown) | yes |
| 38 | Takayama et al. SCP | LLM | D,K | DATA+LLM | no | none | Alarm F1: 91.2 [rep-other] | gh:mas-takayama/LLM-and-SCD (none shown) | yes |
| 39 | Vashishtha et al. causal order | LLM | D,K | DATA+LLM | no | none | Asia D_top (PC vs PC+LLM order): 1.50 vs 0.00 [rep] | gh:AniketVashishtha/Causal_Order_Imperfect_Experts (not checked) | yes |
| 40 | LLM-BFS | LLM | K,D | DATA+LLM | no | none | Asia F1: 0.93 [rep] | none (?) | unknown |
| 41 | Darvariu et al. LLM priors for CD-UCT | LLM | D,K | DATA+LLM | no | none | - | none (?) | unknown |
| 42 | chatPC | LLM | K | LLM | no | none | - | none (?) | unknown |
| 43 | LACR | LLM | K | LLM | no | none | - | none (?) | unknown |
| 44 | COAT | LLM | D,K | DATA | yes | none | - | none (?) | unknown |
| 45 | Srivastava et al. PC + LLM hard prior | LLM | D,K | DATA+LLM | no | none | post-cutoff Alzheimer's graph F1 PC / LLM / hybrid: 0.51 / 0.56 / 0.73 [2nd] | none (?) | unknown |
| 46 | L2D-CD | LLM | D,K | DATA+LLM | no | none | - | none (?) | unknown |
| 47 | MosaCD | LLM | D,K | DATA+LLM | no | none | Win95pts orientation F1: 0.81 [rep] | none (?) | unknown |
| 48 | CARE | LLM | D,K | DATA+LLM | no | names_neutralised,names_permuted | Asia edge F1 (LLM-judge parsed): 0.46 [2nd] | none (?) | unknown |
| 49 | CauScientist | LLM | D,I,K | DATA+LLM+INT | no | none | Cancer F1 (FCI -> +CauScientist): 33.3 -> 87.1 [rep] | gh:OpenCausaLab/CauScientist (none) | unknown |
| 50 | Tench & Demeester expert-guided model averaging | LLM | D,K | DATA+LLM | no | none | - | none (?) | unknown |
| 51 | CaPE | LLM | D,K | DATA | no | none | - | none (?) | unknown |
| 52 | ABAPC-LLM | LLM | D,K | DATA+LLM | no | none | - | gh:briziorusso/ArgCausalDisco (none shown) | yes |
| 53 | DMCD | LLM | D,K | DATA+LLM | no | names_neutralised | Fluxnet2015 F1: 0.751 [rep] | none (?) | unknown |
| 54 | CauTion | LLM | D,K | DATA+LLM | no | none | Win95pts F1: 85.2 [rep] | gh:OpenCausaLab/CauTion (none) | unknown |
| 55 | Kitson & Constantinou probabilistic fusion | LLM | D,K | DATA+LLM | no | names_neutralised | 26 networks F1 fusion / BNSL / LLM: 0.760 / 0.662 / 0.572 [rep] | gh:causaliq/causaliq-knowledge (MIT) | yes |
| 56 | PyWhy-LLM | LLM | K | LLM | ? | none | - | gh:py-why/pywhy-llm (MIT) | yes |
| 57 | Causal-Copilot | AG | D,K | DATA/FUNC (LLM-chosen algorithm)+LLM | yes | none | own Table 2 F1: 0.9 [rep] | gh:Lancelot39/Causal-Copilot (MIT) | yes |
| 58 | CausalSteward | AG | D,K | DATA+LLM | yes | none | CausalMan Small F1: 0.42-0.48 [2nd] | none (?) | unknown |
| 59 | Causal Ensemble Agent | AG | D,K | DATA+LLM | no | none | Alarm normalised Hamming ratio / PR-AUC: 0.049 / 0.952 [rep] | none (?) | unknown |
| 60 | Causal Modelling Agents | AG | D,K | DATA+LLM | yes | none | Alzheimer's normalised Hamming ratio (CMA vs GPT-4): 0.21 vs 0.27 [2nd] | none (?) | unknown |
| 61 | MATMCD | AG | D,K | DATA+LLM | no | none | AutoMPG normalised Hamming (PC -> MATMCD): 0.32 -> 0.04 [2nd] | gh:D2I-Group/matmcd (MIT) | yes |
| 62 | MAC | AG | D,K | DATA+LLM | no | none | Sachs SHD (zero-shot GPT-4o baseline beats proposed models): 18 [rep] | none (?) | unknown |
| 63 | ALCM | AG | D,K | DATA+LLM | no | none | Asia normalised Hamming (PC -> ALCM): 0.143 -> 0.089 [2nd] | none (?) | unknown |
| 64 | Causal Agent | AG | D | DATA | ? | names_neutralised | CausalTQA accuracy: >0.80 on all levels [rep] | gh:kairong-han/causal_agent (MIT) | yes |
| 65 | Causal AI Scientist | AG | D,K | n/a (effects or unevaluated) | ? | none | - | gh:causalNLP/causal-agent (MIT) | yes |
| 66 | CATE-B | AG | D,K | DATA+LLM | ? | none | - | none (?) | unknown |
| 67 | CausalAgent | AG | D,K | n/a (effects or unevaluated) | ? | none | - | none (?) | unknown |
| 68 | LLM4Causal | AG | D | n/a (effects or unevaluated) | ? | none | - | none (?) | unknown |
| 69 | TLVD | AG | D,K | DATA+LLM | yes | none | 5 datasets Acc / CAcc / ECit: +32.67% / +62.21% / +26.72% [rep] | none (?) | unknown |
| 70 | causal-learn+ | AG | D,K | DATA | ? | none | - | none (?) | unknown |
| 71 | ACDB entrants | AG | D,I | AGENT(D+I) | no | names_neutralised,columns_shuffled | ACDB weighted average directed F1 (%): Sonnet 4.6 raw 31.7; GPT-5.4 raw 22.9; PC+greedy 42.7; random DAG 23.6 [rep] | none (?) | unknown |
| 72 | CausaLab agents | AG | D,I | AGENT(D+I) | yes | none | CausaLab 6-node task accuracy / all-edge F1: 0.92 / 0.471 [rep] | none (built on DiscoveryWorld) | unknown |
| 73 | LeGIT | AG | D,I,K | DATA+LLM+INT | no | none | Alarm SHD (LeGIT / GIT / random): 17.4 / 19.6 / 38.8 [2nd] | none (?) | unknown |
| 74 | IGDA | AG | I,K | LLM | ? | none | - | none (?) | unknown |
| 75 | A-CBO | AG | K | LLM | ? | none | Corr2Cause macro F1 (GLM-5.1): 93.2 [rep] | none (?) | unknown |

## Answer (2): LLM methods and agents with public code we could run under our controls (AU9 shortlist)

**Arms.** Names real / neutral / swapped, crossed with columns as released / shuffled, on the CausalArena semantic public-50 set or a fixed subset.
**Effort scale.** S = under 1 day, M = 1-3 days, L = more than 3 days of adaptation.
**Call counts.** These are my arithmetic for 20-40-variable graphs, not reported figures.

| Rank | System | Code (licence) | Why it matters | Adaptation needed | Effort | LLM calls per graph per arm |
|---|---|---|---|---|---|---|
| 1 | Causal-Copilot (done) | gh:Lancelot39/Causal-Copilot (MIT) | The baseline; names arms already measured. | Add the column-shuffle arm only. | S | as now |
| 2 | Vashishtha et al. causal order | gh:AniketVashishtha/Causal_Order_Imperfect_Experts (licence not checked) | Elicits a causal **order** from names. That is exactly the "few bits of order knowledge" channel (depth + regression = 0.714, project). Tests whether names supply the order. | Feed CausalArena names and descriptions; plug the order into PC or a regression; subsample triplets. | M | Triplets grow cubically (1,140-9,880 per graph); must subsample. |
| 3 | Kitson & Constantinou (via causaliq-knowledge) | gh:causaliq/causaliq-knowledge (MIT; Ollama, OpenAI, Anthropic, Gemini and others) | Separate existence and orientation probabilities per edge; nearest design to the claim ledger; already uses aliases. | Confirm the library reproduces the paper's fusion; write a CausalArena loader. | M | 190-780 pairs, or 18 whole-graph requests per setup (paper protocol) |
| 4 | MATMCD | gh:D2I-Group/matmcd (MIT) | Agent that edits PC/DirectLiNGAM output with LLM constraints; ACL Findings 2025. | Disable web retrieval (otherwise a fourth evidence channel); add a data loader. | M | per constraint round; not reported |
| 5 | Takayama SCP | gh:mas-takayama/LLM-and-SCD (no licence; 3 commits, no README) | LLM sees the data result before giving priors; tests whether it overrides data. | Reverse-engineer the scripts; GPT-4-style probability prompts per pair. | M | about n² pair probabilities (190-780) |
| 6 | PyWhy-LLM pairwise | gh:py-why/pywhy-llm (MIT) | Cheapest "LLM-only" arm: the names-only ceiling and floor. | Thin wrapper. | S | 190-780 pairs |
| 7 | LLM-BFS (reimplementation) | none linked (paper says code exists) | Linear query count; a standard baseline in four papers. | Reimplement from the paper's prompts. | S-M | about n (20-40) |
| 8 | ILS-CSL / LLM-CD (Ban et al.) | gh:tyMadara/ILS-CSL (no licence), gh:tyMadara/LLM-CD (licence not checked) | The LLM can only confirm data-proposed edges; a contrast to Copilot's add-capable refiner. | Code assumes discrete data and precomputed BDeu/MINOBS scores; needs a Gaussian BIC path. | L | per proposed edge |
| 9 | Causal Agent (Han et al.) | gh:kairong-han/causal_agent (MIT) | ReAct agent over causal-learn. | Built for question answering; extracting a graph needs code changes. | L | per question |
| — | ABAPC-LLM (Li & Russo) | base repo gh:briziorusso/ArgCausalDisco (no licence; LLM part not in repo) | Data veto over LLM arrows. | clingo ASP scales to about 15 nodes; likely infeasible at 20-40. | L | 5 elicitation runs |

**Not runnable today (no code found or placeholder repo):** CauScientist, CauTion, CEA, CausalSteward, MosaCD, CARE, DMCD, ALCM, MAC, CMA, LACR, chatPC, ACDB agents, CausaLab, Arrow (no weights).

**Free non-LLM arms for the same harness** (also AU11): FoundCause, CDFM, AVICI and TabCausal run on CPU. PC and GES can be scored under the liberal rule, random orientation and shuffled columns. FoundCause averages over permutations, so it is the natural negative control for the layout leak.

## Answer (3): where Q x R x W is crowded and where it is empty

Counts are rows of this table (one row can sit in several cells). "Graph" means skeleton and/or orientation.

| Q \ R | D | D+I | D+K | D+I+K | K only |
|---|---|---|---|---|---|
| Graph | **18** (functional, continuous, pretrained) | **13** (GIES, IGSP, UT-IGSP, JCI, CDIS, DCDI, SDCD, AVICI, CSIvA, SEA, TabCausal, 2 agent envs) | **33**, of which 29 LLM/agent rows (crowded) | **1** (CauScientist) | 5 |
| Effects of interventions | 2 | 1 | 5 | 0 | 0 |
| Choice of experiments | 0 | 2 (ACDB, CausaLab) | 1 (CaPE, simulated expert) | 1 (LeGIT) | 1 (IGDA) |

The W axis (world assumptions) across the 74 non-control rows:
- **Hidden confounders:** 9 rows can represent latent confounding: FCI, FoundCause (pairwise flag), CDFM (bow-free ADMG), COAT, Causal-Copilot (FCI marks later deleted by refinement, DOM-12), CausalSteward, CMA, TLVD, CausaLab (hidden noise).
  - No LLM-fusion method handles PAG marks (cluster 1, confirmed here).
- **Time series:** only Causal-Copilot among the rows. Classical time-series methods (PCMCI, VARLiNGAM, DYNOTEARS) were outside the brief's list and are not typed. DMCD uses IT-monitoring data but does not describe temporal modelling.
- **More than 100 variables:** SEA (1,000 cap), CauScale (1,000), Causal-Copilot (1,000, own suite), CausalSteward (222), LLM-BFS (221), Arrow (107).
  - None of the K-using rows above 100 variables has a name control.
- **Sample size:** most LLM rows use n = 1,000-20,000 on discrete bnlearn data. Pretrained rows train on n = 50-4,096. CausalArena is fixed at 1,000 rows (800 + 200 when mixed).

**Crowded:**
1. Graph x D+K x sufficiency x famous bnlearn graphs up to 76 variables. About 25 LLM/agent systems sit here, mostly without name controls.
2. Graph x D x sufficiency x synthetic SCMs up to 100 variables: classical, continuous and pretrained methods.

**Thin:**
1. Graph x D+I x K: CauScientist only, with placeholder code.
2. Choice of experiments x K: LeGIT and IGDA, both on named famous graphs, plus CaPE with a simulated expert.
3. Hidden confounders x K with PAG semantics: COAT keeps the LLM out of edges; CausalSteward and Causal-Copilot have FCI underneath but no PAG-aware use of K.

**Empty (none found by these searches):**
1. Any K-using system evaluated with names neutral, names swapped **and** columns shuffled together.
2. Any LLM or agent entry on CausalArena.
3. Any column-shuffle audit of the CausalArena leaderboard itself.
4. Time series x K with any control.
5. More than 100 variables x K with any control.
6. An abstaining, per-edge-provenance output evaluated against a data-only floor. CEA and Kitson keep per-edge, per-source state; MosaCD abstains; none reports "never below its data-only output" as a property.

## What this changes for the project

1. **The layout result is about the leaderboard, not only about agents.** PC, GES/GIES and CDIS on CausalArena orient undirected edges by column index over a topological column order. Their published numbers, including the GIES 0.552 that is second only to FoundCause, carry part of the leak. AU9/AU11 should re-score these rows under shuffled columns before anything else; it costs no LLM calls.
2. **The three-arm control (neutral, swapped, shuffled) is unclaimed.** CARE is the only prior work with a swapped-names arm, and it is a fine-tuned 1.5B model scored by an LLM parser. Kitson & Constantinou and DMCD only neutralise names. This is the cleanest novelty claim the field table supports.
3. **Use the Vashishtha causal-order elicitor in AU9/AU10.** Its interface is a causal order, which our depth result (0.714) says is the high-value bit. Rank it second after Causal-Copilot.
4. **Positioning against the published ceiling.** FoundCause's 0.634 averages random permutations and should be roughly immune to layout, while GIES/PC are not. The honest comparison is FoundCause and GIES-shuffled, not GIES-as-released.
5. **The claim-ledger "never below data-only" property is unoccupied** as a stated, evaluated guarantee. The closest are MosaCD (abstains; data vetoes seeds), Li & Russo (data veto, about 15 nodes) and CauScientist (BIC-gated edits, no code). These are the three to cite as nearest neighbours.
6. **The real-data gap is a story by itself.** Every pretrained row loses most of its semantic advantage on CausalArena real data (FoundCause 0.634 to 0.212). Worth one line in the Atlas: semantic scores may reward prior-matching, not discovery.
7. **Licences gate redistribution.** Of the runnable LLM codes, Takayama, ILS-CSL and ArgCausalDisco have no licence. Running them for evaluation is fine to discuss with the mentor; redistributing wrappers is not (as DOM-11 says for TabCausal and SEA).

## Open questions

- What is CDIS (CausalArena ref [21])? Does it receive the liberal orientation in practice?
- Is every one of the 50 public semantic `node_order`s topological? DOM-07 checked one; the project's 0.680 vs 0.269 measurement implies most are.
- Does `causaliq-knowledge` 0.6.0 reproduce the Kitson & Constantinou fusion numbers?
- Does the Vashishtha repo run with current APIs, and under what licence?
- Do CDFM, TabCausal and CauScale change outputs under column permutation? This is AU11, run on CPU.
- Is there a 2026 LLM time-series discovery method with a name control? The search was blocked by the budget.

## Not read

| Source | Reason |
|---|---|
| huggingface.co live files (leaderboard CSVs) | Proxy refused CONNECT (403); the project's local snapshot of the same released files was used |
| export.arxiv.org API, api.semanticscholar.org | Proxy refused (403) |
| GitHub search and repo API (licences, commit dates) | Session not bound to these repositories (403); GitHub web pages showed no commit dates |
| Full texts of Arrow (partly read), DAG-FM, DCD-PFN, TabPFN-CFM, TabPFN probe, CSIvA, SEA, CauScale | Only abs pages or partial HTML were read; numbers are limited to those pages or CausalArena |
| CausalArena appendices B-C | HTML truncated (DOM-07); CDIS and DAS citations unresolved |
| Code repos for GraN-DAG, ANM, CAM, RESIT, JCI; licence of the Vashishtha and LLM-CD repos | Not opened today |
| Kıcıman, Long, Ban, Darvariu, chatPC, LACR, COAT, L2D-CD, Tench & Demeester, CaPE, CMA, CATE-B, CausalAgent demo, LLM4Causal, LeGIT, IGDA, Srivastava (numbers), CausalSteward (numbers), MATMCD and ALCM (numbers) | Not re-opened today. Abs pages were opened for ALCM, MATMCD, CausalSteward and Causal Agent; numbers are labelled second-hand from the project notes. |
| Remaining text of MAC v1 after 100k characters | Fetch truncated |
| TabCausal HTML after 100k characters | Fetch truncated |

## Searches run (all on 2026-10-12)

Web searches (16; the 200-call shared budget then ran out):
1. CausalMACE causal discovery multi-agent LLM
2. LLM agent causal discovery 2026 arXiv benchmark Causal-Copilot baseline
3. pretrained causal discovery foundation model 2026 amortized supervised causal structure learning arXiv
4. "causal discovery" agent LLM arXiv 2026 autonomous end-to-end tabular agent framework (extended)
5. LLM causal discovery variable names anonymized permuted shuffled column order robustness 2026 (extended)
6. arXiv 2025 "causal discovery" "LLM agent" tool-use PyWhy causal-learn ReAct framework evaluation Sachs
7. CausaLab LLM interactive causal discovery benchmark arXiv 2605.26029
8. LLM causal discovery "post-cutoff" OR "unseen" graphs hybrid prior 2026 arXiv new method code github
9. github causal order triplet LLM Vashishtha code
10. github "Efficient Causal Graph Discovery Using Large Language Models" BFS code
11. "Causal Discovery with Language Models as Imperfect Experts" github; "LLMs are Effective Priors for Causal Graph Discovery" github
12. CDIS causal discovery algorithm interventional data
13. SDCD "Stable Differentiable Causal Discovery" arXiv
14-16. Refused by budget: LLM causal discovery prior-knowledge tiers 2026; LLM agent time-series causal discovery 2025-26; "Causal-Copilot" compared/baseline 2026

Direct fetches:
- arXiv abs/HTML pages: 2606.21212, 2607.11510, 2606.26467, 2602.14456, 2609.31675, 2504.13263, 2509.23570, 2601.13614, 2608.27472, 2606.10607, 2607.01936, 2606.03602, 2405.01744, 2402.01454, 2310.15117, 2402.01207, 2311.11689, 2306.16902, 2602.20333, 2407.15073, 2408.06849, 1803.01422, 2209.08037, 2006.10201, 1906.02226, 2007.01754, 1310.1533, 1705.10220, 1910.09007, 1611.10351, 2204.04875, 2511.07236, 2606.17516, 2607.11508, 2605.07204, 2605.31156, 2402.01929, 2602.08629, 2205.12934, 2609.11897
- JMLR pages: GES, GIES, LiNGAM, RESIT
- NIPS 2008 ANM page
- causal-learn PC and FCI docs
- ICML 2026 virtual page 71464
- GitHub pages: Causal-Copilot, matmcd, CauScientist, CauTion, ArgCausalDisco, LLM-and-SCD, ILS-CSL, causal_agent, causaliq-knowledge, causal-learn, causal-agent (CAIS), pywhy-llm, golem, dcdi, notears, TabCausal baselines README
- PyPI JSON: causal-learn, lingam, avici, dagma, gcastle, cdt, causaldag, gies, sdcd, pywhyllm, causalnex, tigramite, cause2e, causal-agent, causaliq-knowledge, causaliq-workflow
- Local files: CausaLab and A-CBO texts from an earlier download; the CausalArena result CSV snapshot; project notes cluster1/2/7/8, DOM-07, DOM-10, DOM-11, REP-03, DOM-12

## Where we're going

- The AU9 short list is ready: Causal-Copilot with a shuffle arm, Vashishtha order, causaliq-knowledge, MATMCD, then the PyWhy-LLM pairwise floor.
- The cheapest high-value run needs no LLM: re-score PC/GES/GIES/CDIS on CausalArena under shuffled columns, and FoundCause/CDFM/AVICI/TabCausal under permutation (AU11).
- A follow-up search sweep, once the budget resets, should cover 2026 agents and time-series LLM methods.
