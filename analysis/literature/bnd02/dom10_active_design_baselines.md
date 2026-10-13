# DOM-10 — Active experiment-design baselines with public code

Requirement: two intervention-selection baselines with public code that our audit can run against Causal-Copilot's intervention suggestions on CausalArena-style SCMs.

## Pick 1 — CBED (Causal Bayesian Experimental Design)

- **Paper.** Tigas, Annadani, Jesson, Schölkopf, Gal, Bauer. *Interventions, Where and How? Experimental Design for Causal Models at Scale.* NeurIPS 2022, arXiv 2203.02016. Source: the repo README at https://github.com/yannadani/cbed.
- **Repo.** https://github.com/yannadani/cbed
- **Licence.** MIT, per the repo sidebar. The README itself has no licence section (https://raw.githubusercontent.com/yannadani/cbed/main/README.md).
- **Language.** Python with JAX. R is optional; it is needed for SID and for the DAG-bootstrap posterior. DiBS is a git submodule (README, Installation).
- **Strategies.** `--strategy` takes `cbed`, `greedycbed`, `softcbed`, `random`, `ait` (README, "Reproducing the results"). So one install gives the CBED variants plus a random baseline plus AIT.
- **Inputs needed.**
  - A posterior model: `--model dag_bootstrap` for linear models or `dibs_nonlinear`. The README says "we use DAG bootstrap for the linear models and DiBS for nonlinear models."
  - An environment that returns interventional samples on demand (`envs/`; DREAM4 is supported).
  - Integration plan: wrap CausalArena's `tools/replay_sampler/replay_sampler.py` as the environment. It replays the generator-spec DSL with interventions (https://huggingface.co/datasets/LAMDA-Tabular/CausalArena/raw/main/tools/replay_sampler/README.md). This is a plan, not something tested.
- **CPU.** Not verified.
  - The README installs only `jax[cuda]`.
  - JAX itself has a CPU backend, and the R DAG-bootstrap path is CPU-bound, so CPU runs are plausible at our sizes (17–25 variables). DiBS nonlinear runs are likely slow on CPU.
  - This is an inference; test it with `--model dag_bootstrap --no_sid` first.

## Pick 2 — Hauser & Bühlmann OptSingle / OptUnb, via `pcalg::opt.target`

- **Paper.** A. Hauser, P. Bühlmann. *Two optimal strategies for active learning of causal models from interventions.* PGM-2012, pp. 123–130. Cited from the pcalg manual (https://rdrr.io/cran/pcalg/man/opt.target.html).
- **Code.** CRAN package `pcalg`, function `opt.target(essgraph, max.size, use.node.names = TRUE)`. Details from https://cran.r-project.org/web/packages/pcalg/index.html:
  - Licence: **GPL-2 | GPL-3**.
  - Version 2.7-11, published 2024-02-12.
  - Maintainer: M. Kalisch.
- **Language.** R with compiled C++ (Rcpp/RcppArmadillo; NeedsCompilation: yes).
- **Inputs needed.**
  - An `EssGraph` or `graphNEL` essential graph. In our pipeline this is the GIES estimate from the current obs and int data.
  - `max.size`: 1 for single-vertex targets (OptSingle), or p for unbounded targets (OptUnb).
  - The manual says the result treats the input graph as the true essential graph, "so estimation errors are ignored".
- **CPU.** Yes. It is a combinatorial computation on the essential graph and needs no GPU. That CPU is sufficient is my inference from the algorithm type; the manual does not state hardware.
- **Why this one.**
  - It is deterministic and cheap, with a permissive-enough licence for research use.
  - It cleanly separates "which target maximises orientable edges" from posterior uncertainty, which makes it a good graph-only contrast to CBED's Bayesian design.

## Considered and not picked

| Candidate | Reason not picked |
|---|---|
| DCT policy, Squires et al. 2020, arXiv 2011.00641; code https://github.com/csquires/dct-policy | No LICENSE file in the repo listing, so reuse terms are unclear. It also assumes a known essential graph and noiseless interventions (Abstract). Python with `causaldag 0.1a135` (requirements.txt). |
| ABCI, Toth et al., NeurIPS 2022, arXiv 2206.02063; code https://github.com/chritoth/active-bayesian-causal-inference (MIT) | Heavier stack: DiBS plus GPs plus conda env. It is aimed at causal-query inference rather than structure only. A good third option if needed. |
| ABCD-Strategy, Agrawal et al., AISTATS 2019, arXiv 1902.10347 | The paper gives no code URL (PDF checked). github.com/agrawalraj/active_learn could not be fetched, so it is not verified. |

## Typed gaps
- CBED CPU feasibility and runtime are not verified. Test before committing compute.
- Neither baseline natively handles latent confounders. CausalArena semantic SCMs include unobserved nodes (`mask`), so state this assumption gap in the paper.
