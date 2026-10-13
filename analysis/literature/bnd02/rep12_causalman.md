# REP-12 — CausalSteward's external score for Causal-Copilot on CausalMan

## Verdict: **OBTAINABLE**
The data is open-access on Zenodo under CC BY 4.0. It is 11.2 GB, split into a 3-part zip. Caveats are listed below.

## CausalSteward (the source of the score)
- **Citation.** Tagliapietra, Marchioni, Willig, Luettin, Halilaj, Kersting. *CausalSteward: An Agentic Divide-Conquer-Combine Copilot for Causal Discovery.* arXiv:2607.01936.
- **URL read.** https://arxiv.org/html/2607.01936v1
- **Datasets.** Sec. 6.1 uses "CausalMan Small (53 nodes, 108 edges)" and "CausalMan Medium (186 nodes, 553 edges)".
- **Causal-Copilot on Small** (Table 1 / Table 2):
  - F1 **0.078 (std 0.012)**, precision 0.260, SHD 117.4.
  - This matches the "F1 0.08 at 53 variables" figure.
- **How Causal-Copilot was run.**
  - Table 1 caption: "CausalCopilot executed FCI on Small and XGES on Medium."
  - No further configuration is given in the text I read.
  - Sample size and the subset used are deferred to Appendix F, which is **not verified** (not in the returned text).
- **Code.** The Reproducibility Statement says "We provide the complete code-base" but gives no URL in the text I read.
- **Author overlap.** CausalSteward shares authors with CausalMan: Tagliapietra, Luettin, Halilaj, Willig, Kersting.

## CausalMan (the dataset)
- **Citation.** Tagliapietra, Luettin, Halilaj, Willig, Pychynski, Kersting. *CausalMan: A physics-based simulator for large-scale causality.* arXiv:2502.12707. The header reads "Preliminary work. Under review."
- **URLs read.** https://arxiv.org/abs/2502.12707v1, https://arxiv.org/html/2502.12707v1
- **What it is.** A physics-based simulator of press-fitting magnetic valves into hydraulic blocks. It has Small and Medium datasets:
  - Partially observable graphs with 53 and 186 observed nodes.
  - Full graphs with 157 and 605 nodes.
  - Mixed data types, causal insufficiency, nonlinear mechanisms and interventions (Introduction / contributions).
- **Data URL given in the paper.** https://zenodo.org/records/13871097

### Zenodo record (https://zenodo.org/records/13871097)
- **Record.** "CausalMan Dataset", DOI 10.5281/zenodo.13871097.
  - Creators: "Anonymous, Anonymous".
  - Published 2024-10-01, v1.
- **Access.** **Open.** Licence **CC BY 4.0**.
- **Files (11.2 GB total).** `data.zip.001` (5.2 GB), `data.zip.002` (5.2 GB), `data.zip.003` (673.3 MB), `README.txt` (1.2 kB).
- **README.txt** (https://zenodo.org/records/13871097/files/README.txt):
  - `Interventional_table.csv` is a binary row-aligned mask; an all-zero row marks an observational sample.
  - The data is **not normalised**.
  - Partially observable files come from latent projection and "can contain bidirected edges", which are encoded as a pair of opposite directed edges.
  - A `partID` column should be dropped.
  - An HTML graph viewer is included.
- **Newer version.** The page says a newer version exists. **I could not open it (NOT VERIFIED):** fetching https://zenodo.org/records/13871097/latest was refused with HTTP 429 (rate limited), so I did not retry. The v1 files above remain listed as open.

## Implications for reproducing the 0.078
- **Scoring convention.** The 53-node graph is a latent projection with bidirected edges stored as two opposite directed edges. A directed-F1 scorer will count each bidirected pair as two true edges. We must match CausalSteward's convention (Appendix F, not verified), or the F1 will not be comparable.
- **Rows used.** Use observational rows only, via the `Interventional_table.csv` all-zero rows, unless Appendix F says otherwise.
- **Download.** Download all three zip parts, then concatenate and extract them. Budget about 11 GB of disk.

## Typed gaps
- CausalSteward Appendix F (sample size, subset, scoring): not verified.
- The newer Zenodo version (file changes, licence): not verified because of rate limiting.
- The CausalSteward code URL: not found.
