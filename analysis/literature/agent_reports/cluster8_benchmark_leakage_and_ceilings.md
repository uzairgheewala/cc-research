**Where we are now:** literature check finished. On the three gaps: (x) and (z) I found no precedent; (y) has one partial precedent (CARE). Marks: V = I opened the primary page, A = second-hand or memory. All V reads went through a fetch tool that summarises the page, so re-check exact numbers before citing.

## 1. Benchmark artifacts
- **Varsortability** (Reisach, Seiler, Weichwald, NeurIPS 2021, arXiv 2102.13647): varsortability averages above 0.94 in their simulated graphs and above 0.71 in common nonlinear ANMs (V). sortnregress matches continuous methods on raw data; on standardized data those methods fail to recover the DAG or its MEC (V).
- **R2-sortability** (Reisach, Tami, Seiler, Chambaz, Weichwald, NeurIPS 2023, arXiv 2303.18211): about 0.8 on average in default settings (V). R2-SortnRegress beats PC and matches or exceeds FGES when R2-sortability is high (V). Sachs has R2-sortability 0.82, yet PC is best there (SHD 11.4; empty graph 17) (V).
- **iSCM** (Ormaniec, Sussex, Lorch, Schölkopf, Krause, arXiv 2406.11601; ICLR 2025 venue is A): standardized SCMs become near-deterministic with depth; iSCMs have R2-sortability near 0.5. AVICI and R2-SortnRegress do worse on iSCMs, and the authors suggest AVICI "may indeed be exploiting the correlation artifacts" (V).
- **Column order** (Kitson & Constantinou, arXiv 2206.08952; Data Min. Knowl. Disc. 2024 is A): column order alone moves hill-climbing F1 by 0.412 on average, worst to optimal order. A 100x sample-size increase gives 0.161. PC-Stable moves 0.036 (V). They describe bnlearn-style files as alphabetical, effectively arbitrary (V); they do not claim released files are topologically ordered. Follow-up: HC-Stable/Tabu-Stable (PGM 2024, PMLR 246) (V).
- **Generator practice only:** ACDB (arXiv 2609.31675) "randomly permute[s] node indices so names do not leak topology" (V). This is a precaution, not an audit.

## 2. LLM leakage
- **Srivastava et al. 2025** (arXiv 2510.16530): near-perfect reconstruction F1 on BNLearn graphs with zero context. LLM-BFS F1 is 0.93 on Asia versus 0.56 on post-cutoff Alzheimer's; PC+LLM hybrid reaches 0.66-0.73. Control is post-cutoff graphs only; no anonymisation or shuffling (V).
- **Causal Parrots** (Zečević, Willig, Dhami, Kersting, arXiv 2308.13067): conceptual meta-SCM argument (V).
- **Label permutation: only CARE** (Dong, Liu, Aloui, Tarokh, Carlson, arXiv 2511.16016). Arms are Original / Random (anonymised) / Permuted (names shuffled onto wrong columns, data untouched), crossed with N in {0, 50, 200} and with/without algorithm output. o4-mini on Asia without algorithm output: 1.000, then 0.00-0.08, then about 0.15 (V). Column reordering is applied as a blanket augmentation, never as a measured factor (V).
- **Anonymisation only:** Kitson & Constantinou 2026 (arXiv 2608.27472; neutral aliases; "benchmark recognition cannot be ruled out") (V). Caliper (Yu & Zhou, arXiv 2606.04915; reasoning benchmarks, 7.6-29.6 pp drops) (V).
- **No control:** CEA (arXiv 2606.10607) flags a perfect Asia score as a "potential benchmark-leakage signal" (V). Causal-Copilot (arXiv 2504.13263) describes no name or order control, and its F1 basis (DAG vs CPDAG) is unstated (V, first 100k characters only).

## 3. Ceilings and decomposition
- **SID** (Peters & Bühlmann, Neural Computation 2015): returns lower and upper bounds for a CPDAG (V, via CRAN docs).
- **gadjid/AID** (Henckel, Würtzen, Weichwald, arXiv 2402.08616): extends to CPDAGs (V).
- **Wahl & Runge** (arXiv 2402.04952; AISTATS 2025): the s/c-metric is a metric on MECs; separation distances cannot distinguish MEC members (V).
- **Closest to a decomposition:** Faltenbacher, Wahl, Herman, Runge (arXiv 2502.14719) separate assumption violations from finite-sample CI errors for PC, use oracle-PC, and offer a growing-sample heuristic. There is no formal three-way split (V).
- **ACDB** says an observational agent "is bounded by the CPDAG", scores a CPDAG layer and a DAG layer separately, and reports a random-DAG floor of 23.6% directed F1 (V).
- arXiv 2409.19377 attributes score to simulation factors, and arXiv 2605.27477 gives per-edge RESOLVED/IMPOSSIBLE certificates; neither is a decomposition (V).
- I found no paper computing the expected DAG-level F1/SHD of the true CPDAG under random orientation, and no explicit "directed F1 penalises correct CPDAG output" critique.

## 4. Amortized models

| Model | Order-equivariant by construction? | Checkpoint / CPU |
|---|---|---|
| AVICI (arXiv 2205.12934) | Yes, stated (V) | Public checkpoints; CPU backend flag since v1.0.6 (V) |
| Arrow (arXiv 2605.07204) | Yes, no positional encodings (V) | "Will soon" release weights (V); current status unknown |
| SEA (arXiv 2402.01929) | Not exact: randomly permuted positional embeddings; one embedding depends on node order (V) | Checkpoints in repo; README assumes CUDA (V) |
| CDFM (arXiv 2607.11508) | No claim made (V) | HF `DMIRLAB/CDFM`, `device="cpu"` option (V) |
| FoundCause (arXiv 2606.17516) | Abstract says "permutation-invariant" encoder (V) | None on page (V) |
| TabCausal (arXiv 2605.31156) | Not stated (V) | Not found |
| TabPFN probe (arXiv 2511.07236) | Position-indexed causal tokens, so probably not (inference) | None given (V) |
| CSIvA (arXiv 2204.04875) | Not verified | No code mentioned (V) |

- Do-PFN (arXiv 2506.06039) is effect estimation, not discovery (V); CausalPFN likewise (A).
- I found no "ArrowFM"; the model is "Arrow". CauScale has a HF repo `OpenCausaLab/causcale-model` (A).
- No paper found runs a shuffled-variable-order test at inference. CausalArena (arXiv 2609.11897) benchmarks seven of these models with directed F1/SHD against the DAG and no permutation test (V).

## 5. Real-data ground truth
- **Brouillard et al.** (arXiv 2412.01953; CLeaR 2025 is A): 167 papers reviewed. Sachs is the only real dataset in 35% of real-data papers. Its ground truth is "not definitive", cycles are often omitted, and results have "peaked at an SHD of around 12". Fewer than 5% of studies use interventional metrics. They recommend interventional metrics on unseen interventions (V). Two fetches gave different metric-usage percentages, so re-read before quoting those.
- **Zhang, Chen, Yao, Wang** (arXiv 2606.01789): literature-inconsistency rates are Sachs 26.7% (lowest), Child 54.0%, Asia 57.9% (V).
- **Causal Chambers** (Gamella, Peters, Bühlmann, arXiv 2404.11341): physical testbeds with validated ground truth (V).
- Mooij et al.'s JCI critique of Sachs: the PDF was truncated, so unverified. I found no paper titled "Sachs is not a benchmark".

## Ten most relevant works
1. Reisach et al. 2021 — varsortability
2. Reisach et al. 2023 — R2-sortability
3. Ormaniec et al. 2024/25 — iSCM
4. Kitson & Constantinou 2022/24 — column-order sensitivity
5. Dong et al. 2025 (CARE) — label permutation
6. Srivastava et al. 2025 — post-cutoff graphs
7. Faltenbacher et al. 2025 — PC error sources
8. Wahl & Runge 2024/25 with Henckel et al. 2024 — MEC-aware metrics
9. Brouillard et al. 2024/25 — real-data landscape
10. Li et al. 2026 (CausalArena) — foundation-model benchmark

## Not done, as far as this search reached
- **(x)** No paper shows a public benchmark's released files leaking edge directions through column order. Kitson & Constantinou show order sensitivity of algorithms, not a leak in files.
- **(y)** No three-way control (numbers vs names vs layout) for LLM agents. CARE covers names (anonymised and permuted) crossed with data presence, but treats layout as a nuisance.
- **(z)** No per-benchmark error budget separating identifiability, statistical and algorithmic loss.

Not verified: venues marked A, CSIvA's equivariance, current Arrow/TabCausal/FoundCause weight availability, CPU runtimes for any model. No code was run and no benchmark files were inspected.

**Where we're going:** the claims can be positioned against Kitson & Constantinou for (x), CARE for (y), and Faltenbacher et al. plus ACDB for (z). Before citing, re-read CARE Appendix C.4 and the Brouillard tables for exact wording.
