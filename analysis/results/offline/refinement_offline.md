# Offline refinement experiment (no LLM, no API cost)

113 cells run, 96 completed, 17 failed. Each cell: one dataset, one algorithm with wrapper-default hyperparameters, seed 0, 20 bootstrap resamples, using the repo's own `fit`, `bootstrap`, `bootstrap_recommend` and `kci_pruning`.

S0 = algorithm output. S1 = after the bootstrap edits of `judge.py:68-86`. S3n = S1 after KCI pruning, with the LLM review skipped.

## 1. Does an edge survive the bootstrap step? By the edge's type in the algorithm output

| Edge type in S0 | Edges (all cells) | Still adjacent in S1 | Survival |
|---|---|---|---|
| directed | 361 | 347 | 96% |
| undirected | 204 | 32 | 16% |
| o-o | 24 | 3 | 12% |
| bidirected | 8 | 1 | 12% |
| mixed(2,1) | 6 | 0 | 0% |
| a o-> b | 6 | 2 | 33% |
| b o-> a | 2 | 0 | 0% |

## 2. Same, per algorithm

| Algorithm | Output types seen | Edges | Survive | Survival |
|---|---|---|---|---|
| BAMB | undirected 13, directed 6, mixed(2,1) 2 | 21 | 8 | 38% |
| DirectLiNGAM | directed 75 | 75 | 73 | 97% |
| FCI | o-o 24, directed 14, bidirected 8, a o-> b 6, b o-> a 2 | 54 | 19 | 35% |
| FGES | directed 27, undirected 18 | 45 | 27 | 60% |
| GES | undirected 35, directed 24 | 59 | 26 | 44% |
| GRaSP | undirected 35, directed 24 | 59 | 26 | 44% |
| IAMBnPC | undirected 13, directed 5, mixed(2,1) 3 | 21 | 4 | 19% |
| ICALiNGAM | directed 65 | 65 | 65 | 100% |
| InterIAMB | undirected 17, directed 5, mixed(2,1) 1 | 23 | 9 | 39% |
| MBOR | undirected 16, directed 5 | 21 | 8 | 38% |
| NOTEARSLinear | directed 54 | 54 | 54 | 100% |
| PC | undirected 33, directed 30 | 63 | 36 | 57% |
| XGES | directed 27, undirected 24 | 51 | 30 | 59% |

## 3. Accuracy against ground truth by stage (mean over datasets; adjacency F1 ignores orientation)

| Algorithm | Datasets | adj F1 S0 | adj F1 S1 | adj F1 S3n | adj recall S0 | adj recall S1 | SHD vs CPDAG S0 | S1 | S3n | Datasets where S1 has lower adj F1 than S0 | higher |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BAMB | 4 | 0.20 | 0.06 | 0.06 | 0.18 | 0.04 | 9.0 | 8.8 | 8.8 | 2 | 0 |
| DirectLiNGAM | 8 | 0.76 | 0.76 | 0.78 | 0.85 | 0.85 | 9.9 | 9.6 | 9.1 | 0 | 1 |
| FCI | 8 | 0.85 | 0.30 | 0.30 | 0.84 | 0.22 | 8.0 | 7.5 | 7.5 | 8 | 0 |
| FGES | 8 | 0.82 | 0.40 | 0.40 | 0.78 | 0.34 | 4.9 | 6.2 | 6.2 | 8 | 0 |
| GES | 9 | 0.88 | 0.35 | 0.35 | 0.86 | 0.26 | 3.4 | 6.6 | 6.6 | 9 | 0 |
| GRaSP | 9 | 0.88 | 0.35 | 0.35 | 0.86 | 0.26 | 3.4 | 6.6 | 6.6 | 9 | 0 |
| HITONMB | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 9.7 | 9.7 | 9.7 | 0 | 0 |
| IAMBnPC | 4 | 0.20 | 0.05 | 0.05 | 0.18 | 0.03 | 9.2 | 7.8 | 7.8 | 2 | 0 |
| ICALiNGAM | 9 | 0.86 | 0.86 | 0.86 | 0.87 | 0.87 | 7.2 | 7.2 | 7.2 | 0 | 0 |
| InterIAMB | 4 | 0.46 | 0.31 | 0.31 | 0.44 | 0.29 | 8.8 | 8.5 | 8.2 | 2 | 0 |
| MBOR | 4 | 0.20 | 0.06 | 0.06 | 0.18 | 0.04 | 9.0 | 8.8 | 8.8 | 2 | 0 |
| NOTEARSLinear | 9 | 0.83 | 0.83 | 0.81 | 0.81 | 0.81 | 6.6 | 6.6 | 6.6 | 0 | 0 |
| PC | 9 | 0.86 | 0.44 | 0.44 | 0.86 | 0.36 | 4.2 | 6.2 | 6.2 | 9 | 0 |
| XGES | 8 | 0.87 | 0.42 | 0.42 | 0.84 | 0.35 | 3.9 | 5.9 | 5.9 | 8 | 0 |

## 4. How many pairs the bootstrap step queues for LLM review

In every completed cell the queue contained every unordered pair and every self-pair: TRUE.

## 5. Where each wrapper stores its marks (upper vs lower triangle), which decides what the KCI step can see

`kci_pruning` only examines cells `[i, j]` with `i < j` (upper triangle).

| Algorithm | Nonzero cells in upper triangle | in lower triangle | KCI removals (all cells) |
|---|---|---|---|
| BAMB | 13 | 10 | 0 |
| DirectLiNGAM | 31 | 44 | 4 |
| FCI | 39 | 15 | 0 |
| FGES | 11 | 34 | 0 |
| GES | 45 | 14 | 0 |
| GRaSP | 45 | 14 | 0 |
| HITONMB | 0 | 0 | 0 |
| IAMBnPC | 17 | 7 | 0 |
| ICALiNGAM | 22 | 43 | 0 |
| InterIAMB | 15 | 9 | 1 |
| MBOR | 11 | 10 | 0 |
| NOTEARSLinear | 24 | 30 | 3 |
| PC | 46 | 17 | 0 |
| XGES | 12 | 39 | 0 |

## 6. Every cell

| Dataset | Algorithm | True edges | S0 adj | S1 adj | S3n adj | adj F1 S0 | S1 | S3n | SHD-CPDAG S0 | S1 | S3n |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LiNG_10nodes | BAMB | 9 | 12 | 7 | 7 | 0.29 | 0.12 | 0.12 | 17 | 15 | 15 |
| LiNG_10nodes | DirectLiNGAM | 9 | 9 | 9 | 9 | 0.33 | 0.33 | 0.33 | 14 | 14 | 14 |
| LiNG_10nodes | FCI | 9 | 11 | 6 | 6 | 0.30 | 0.13 | 0.13 | 17 | 14 | 14 |
| LiNG_10nodes | FGES | 9 | 9 | 6 | 6 | 0.33 | 0.13 | 0.13 | 14 | 14 | 14 |
| LiNG_10nodes | GES | 9 | 9 | 7 | 7 | 0.33 | 0.12 | 0.12 | 14 | 15 | 15 |
| LiNG_10nodes | GRaSP | 9 | 9 | 7 | 7 | 0.33 | 0.12 | 0.12 | 14 | 15 | 15 |
| LiNG_10nodes | HITONMB | 9 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 9 | 9 | 9 |
| LiNG_10nodes | IAMBnPC | 9 | 12 | 2 | 2 | 0.29 | 0.00 | 0.00 | 17 | 11 | 11 |
| LiNG_10nodes | ICALiNGAM | 9 | 9 | 9 | 9 | 0.33 | 0.33 | 0.33 | 14 | 14 | 14 |
| LiNG_10nodes | InterIAMB | 9 | 12 | 7 | 6 | 0.29 | 0.12 | 0.13 | 17 | 15 | 14 |
| LiNG_10nodes | MBOR | 9 | 12 | 7 | 7 | 0.29 | 0.12 | 0.12 | 17 | 15 | 15 |
| LiNG_10nodes | NOTEARSLinear | 9 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 9 | 9 | 9 |
| LiNG_10nodes | PC | 9 | 11 | 8 | 8 | 0.30 | 0.12 | 0.12 | 16 | 16 | 16 |
| LiNG_10nodes | XGES | 9 | 9 | 7 | 7 | 0.33 | 0.12 | 0.12 | 14 | 15 | 15 |
| Linear_Gaussian | BAMB | 1 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Gaussian | DirectLiNGAM | 1 | 1 | 1 | 1 | 1.00 | 1.00 | 1.00 | 1 | 1 | 1 |
| Linear_Gaussian | FCI | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Gaussian | FGES | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Gaussian | GES | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Gaussian | GRaSP | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Gaussian | IAMBnPC | 1 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Gaussian | ICALiNGAM | 1 | 1 | 1 | 1 | 1.00 | 1.00 | 1.00 | 1 | 1 | 1 |
| Linear_Gaussian | InterIAMB | 1 | 1 | 1 | 1 | 1.00 | 1.00 | 1.00 | 0 | 0 | 0 |
| Linear_Gaussian | MBOR | 1 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Gaussian | NOTEARSLinear | 1 | 1 | 1 | 1 | 1.00 | 1.00 | 1.00 | 1 | 1 | 1 |
| Linear_Gaussian | PC | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Gaussian | XGES | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Nongaussian | BAMB | 1 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Nongaussian | DirectLiNGAM | 1 | 1 | 1 | 1 | 1.00 | 1.00 | 1.00 | 1 | 1 | 1 |
| Linear_Nongaussian | FCI | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Nongaussian | FGES | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Nongaussian | GES | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Nongaussian | GRaSP | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Nongaussian | HITONMB | 1 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Nongaussian | IAMBnPC | 1 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Nongaussian | ICALiNGAM | 1 | 1 | 1 | 1 | 1.00 | 1.00 | 1.00 | 1 | 1 | 1 |
| Linear_Nongaussian | InterIAMB | 1 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Nongaussian | MBOR | 1 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 1 | 1 | 1 |
| Linear_Nongaussian | NOTEARSLinear | 1 | 1 | 1 | 1 | 1.00 | 1.00 | 1.00 | 1 | 1 | 1 |
| Linear_Nongaussian | PC | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| Linear_Nongaussian | XGES | 1 | 1 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0 | 1 | 1 |
| sachs(reference) | BAMB | 19 | 9 | 1 | 1 | 0.50 | 0.10 | 0.10 | 17 | 18 | 18 |
| sachs(reference) | DirectLiNGAM | 19 | 11 | 11 | 11 | 0.60 | 0.60 | 0.60 | 19 | 19 | 19 |
| sachs(reference) | FCI | 19 | 8 | 0 | 0 | 0.59 | 0.00 | 0.00 | 19 | 19 | 19 |
| sachs(reference) | FGES | 19 | 5 | 0 | 0 | 0.42 | 0.00 | 0.00 | 18 | 19 | 19 |
| sachs(reference) | GES | 19 | 8 | 2 | 2 | 0.59 | 0.19 | 0.19 | 17 | 19 | 19 |
| sachs(reference) | GRaSP | 19 | 8 | 2 | 2 | 0.59 | 0.19 | 0.19 | 17 | 19 | 19 |
| sachs(reference) | HITONMB | 19 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 | 19 | 19 | 19 |
| sachs(reference) | IAMBnPC | 19 | 9 | 2 | 2 | 0.50 | 0.19 | 0.19 | 18 | 18 | 18 |
| sachs(reference) | ICALiNGAM | 19 | 11 | 11 | 11 | 0.60 | 0.60 | 0.60 | 20 | 20 | 20 |
| sachs(reference) | InterIAMB | 19 | 10 | 1 | 1 | 0.55 | 0.10 | 0.10 | 17 | 18 | 18 |
| sachs(reference) | MBOR | 19 | 9 | 1 | 1 | 0.50 | 0.10 | 0.10 | 17 | 18 | 18 |
| sachs(reference) | NOTEARSLinear | 19 | 14 | 14 | 11 | 0.73 | 0.73 | 0.60 | 20 | 20 | 20 |
| sachs(reference) | PC | 19 | 8 | 4 | 4 | 0.59 | 0.35 | 0.35 | 17 | 18 | 18 |
| sachs(reference) | XGES | 19 | 8 | 3 | 3 | 0.59 | 0.27 | 0.27 | 17 | 18 | 18 |
| sim_linear_gaussian_p8_s0 | DirectLiNGAM | 8 | 10 | 10 | 9 | 0.89 | 0.89 | 0.94 | 9 | 9 | 8 |
| sim_linear_gaussian_p8_s0 | FCI | 8 | 8 | 3 | 3 | 1.00 | 0.55 | 0.55 | 6 | 6 | 6 |
| sim_linear_gaussian_p8_s0 | FGES | 8 | 6 | 5 | 5 | 0.86 | 0.77 | 0.77 | 6 | 7 | 7 |
| sim_linear_gaussian_p8_s0 | GES | 8 | 8 | 2 | 2 | 1.00 | 0.40 | 0.40 | 0 | 6 | 6 |
| sim_linear_gaussian_p8_s0 | GRaSP | 8 | 8 | 2 | 2 | 1.00 | 0.40 | 0.40 | 0 | 6 | 6 |
| sim_linear_gaussian_p8_s0 | ICALiNGAM | 8 | 9 | 9 | 9 | 0.94 | 0.94 | 0.94 | 7 | 7 | 7 |
| sim_linear_gaussian_p8_s0 | NOTEARSLinear | 8 | 7 | 7 | 7 | 0.93 | 0.93 | 0.93 | 7 | 7 | 7 |
| sim_linear_gaussian_p8_s0 | PC | 8 | 8 | 3 | 3 | 1.00 | 0.55 | 0.55 | 0 | 5 | 5 |
| sim_linear_gaussian_p8_s0 | XGES | 8 | 8 | 2 | 2 | 1.00 | 0.40 | 0.40 | 0 | 6 | 6 |
| sim_linear_gaussian_p8_s1 | DirectLiNGAM | 8 | 18 | 18 | 15 | 0.62 | 0.62 | 0.70 | 18 | 18 | 15 |
| sim_linear_gaussian_p8_s1 | FCI | 8 | 9 | 3 | 3 | 0.94 | 0.55 | 0.55 | 8 | 7 | 7 |
| sim_linear_gaussian_p8_s1 | FGES | 8 | 8 | 7 | 7 | 1.00 | 0.93 | 0.93 | 0 | 1 | 1 |
| sim_linear_gaussian_p8_s1 | GES | 8 | 8 | 7 | 7 | 1.00 | 0.93 | 0.93 | 0 | 1 | 1 |
| sim_linear_gaussian_p8_s1 | GRaSP | 8 | 8 | 7 | 7 | 1.00 | 0.93 | 0.93 | 0 | 1 | 1 |
| sim_linear_gaussian_p8_s1 | ICALiNGAM | 8 | 10 | 10 | 10 | 0.89 | 0.89 | 0.89 | 4 | 4 | 4 |
| sim_linear_gaussian_p8_s1 | NOTEARSLinear | 8 | 8 | 8 | 8 | 1.00 | 1.00 | 1.00 | 1 | 1 | 1 |
| sim_linear_gaussian_p8_s1 | PC | 8 | 9 | 7 | 7 | 0.94 | 0.93 | 0.93 | 2 | 1 | 1 |
| sim_linear_gaussian_p8_s1 | XGES | 8 | 8 | 7 | 7 | 1.00 | 0.93 | 0.93 | 0 | 1 | 1 |
| sim_linear_gaussian_p8_s2 | DirectLiNGAM | 8 | 16 | 14 | 14 | 0.67 | 0.73 | 0.73 | 15 | 13 | 13 |
| sim_linear_gaussian_p8_s2 | FCI | 8 | 8 | 3 | 3 | 1.00 | 0.55 | 0.55 | 7 | 7 | 7 |
| sim_linear_gaussian_p8_s2 | FGES | 8 | 7 | 2 | 2 | 0.93 | 0.40 | 0.40 | 1 | 6 | 6 |
| sim_linear_gaussian_p8_s2 | GES | 8 | 8 | 2 | 2 | 1.00 | 0.40 | 0.40 | 0 | 6 | 6 |
| sim_linear_gaussian_p8_s2 | GRaSP | 8 | 8 | 2 | 2 | 1.00 | 0.40 | 0.40 | 0 | 6 | 6 |
| sim_linear_gaussian_p8_s2 | ICALiNGAM | 8 | 8 | 8 | 8 | 1.00 | 1.00 | 1.00 | 6 | 6 | 6 |
| sim_linear_gaussian_p8_s2 | NOTEARSLinear | 8 | 9 | 9 | 9 | 0.94 | 0.94 | 0.94 | 7 | 7 | 7 |
| sim_linear_gaussian_p8_s2 | PC | 8 | 8 | 5 | 5 | 1.00 | 0.77 | 0.77 | 0 | 3 | 3 |
| sim_linear_gaussian_p8_s2 | XGES | 8 | 8 | 4 | 4 | 1.00 | 0.67 | 0.67 | 0 | 4 | 4 |
| sim_linear_uniform_p8_s0 | GES | 8 | 8 | 4 | 4 | 1.00 | 0.67 | 0.67 | 0 | 4 | 4 |
| sim_linear_uniform_p8_s0 | GRaSP | 8 | 8 | 4 | 4 | 1.00 | 0.67 | 0.67 | 0 | 4 | 4 |
| sim_linear_uniform_p8_s0 | ICALiNGAM | 8 | 8 | 8 | 8 | 1.00 | 1.00 | 1.00 | 6 | 6 | 6 |
| sim_linear_uniform_p8_s0 | NOTEARSLinear | 8 | 6 | 6 | 6 | 0.86 | 0.86 | 0.86 | 7 | 7 | 7 |
| sim_linear_uniform_p8_s0 | PC | 8 | 9 | 5 | 5 | 0.94 | 0.62 | 0.62 | 3 | 7 | 7 |
| sim_linear_uniform_p8_s1 | DirectLiNGAM | 8 | 9 | 9 | 9 | 0.94 | 0.94 | 0.94 | 2 | 2 | 2 |
| sim_linear_uniform_p8_s1 | FCI | 8 | 8 | 4 | 4 | 1.00 | 0.67 | 0.67 | 5 | 5 | 5 |
| sim_linear_uniform_p8_s1 | FGES | 8 | 8 | 7 | 7 | 1.00 | 0.93 | 0.93 | 0 | 1 | 1 |
| sim_linear_uniform_p8_s1 | XGES | 8 | 8 | 7 | 7 | 1.00 | 0.93 | 0.93 | 0 | 1 | 1 |
| sim_linear_uniform_p8_s2 | GES | 8 | 8 | 2 | 2 | 1.00 | 0.40 | 0.40 | 0 | 6 | 6 |
| sim_linear_uniform_p8_s2 | GRaSP | 8 | 8 | 2 | 2 | 1.00 | 0.40 | 0.40 | 0 | 6 | 6 |
| sim_linear_uniform_p8_s2 | ICALiNGAM | 8 | 8 | 8 | 8 | 1.00 | 1.00 | 1.00 | 6 | 6 | 6 |
| sim_linear_uniform_p8_s2 | NOTEARSLinear | 8 | 8 | 8 | 8 | 1.00 | 1.00 | 1.00 | 6 | 6 | 6 |
| sim_linear_uniform_p8_s2 | PC | 8 | 8 | 4 | 4 | 1.00 | 0.67 | 0.67 | 0 | 4 | 4 |

## 7. Cells that did not complete

| Dataset | Algorithm | Error | Where |
|---|---|---|---|
| LiNG_10nodes | CORL | TypeError: '_Mock' object cannot be interpreted as an integer | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/corl/torch/frame/_reward.py:90 |
| Linear_Gaussian | CORL | TypeError: '_Mock' object cannot be interpreted as an integer | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/corl/torch/frame/_reward.py:90 |
| Linear_Nongaussian | CORL | TypeError: '_Mock' object cannot be interpreted as an integer | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/corl/torch/frame/_reward.py:90 |
| sachs(reference) | CORL | TypeError: '_Mock' object cannot be interpreted as an integer | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/corl/torch/frame/_reward.py:90 |
| LiNG_10nodes | GOLEM | TypeError: unsupported format string passed to _Mock.__format__ | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/notears/torch/golem.py:203 |
| Linear_Gaussian | GOLEM | TypeError: unsupported format string passed to _Mock.__format__ | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/notears/torch/golem.py:203 |
| Linear_Nongaussian | GOLEM | TypeError: unsupported format string passed to _Mock.__format__ | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/notears/torch/golem.py:203 |
| sachs(reference) | GOLEM | TypeError: unsupported format string passed to _Mock.__format__ | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/notears/torch/golem.py:203 |
| Linear_Gaussian | HITONMB | IndexError: index -17 is out of bounds for axis 2 with size 16 | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/joblib/parallel.py:763 |
| LiNG_10nodes | Hybrid | TypeError: 'DataLoader' object is not iterable | externals/causal-learn/causallearn/search/FCMBased/PNL/PNL.py:120 |
| Linear_Gaussian | Hybrid | TypeError: 'DataLoader' object is not iterable | externals/causal-learn/causallearn/search/FCMBased/PNL/PNL.py:120 |
| Linear_Nongaussian | Hybrid | TypeError: 'DataLoader' object is not iterable | externals/causal-learn/causallearn/search/FCMBased/PNL/PNL.py:120 |
| sachs(reference) | Hybrid | TypeError: 'DataLoader' object is not iterable | externals/causal-learn/causallearn/search/FCMBased/PNL/PNL.py:120 |
| LiNG_10nodes | NOTEARSNonlinear | TypeError: object of type '_Mock' has no len() | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/notears/torch/utils/lbfgsb_scipy.py:32 |
| Linear_Gaussian | NOTEARSNonlinear | TypeError: object of type '_Mock' has no len() | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/notears/torch/utils/lbfgsb_scipy.py:32 |
| Linear_Nongaussian | NOTEARSNonlinear | TypeError: object of type '_Mock' has no len() | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/notears/torch/utils/lbfgsb_scipy.py:32 |
| sachs(reference) | NOTEARSNonlinear | TypeError: object of type '_Mock' has no len() | /sessions/rcw-017bl4ttn1bvbjm9xvljn3tb/venv/lib/python3.10/site-packages/castle/algorithms/gradient/notears/torch/utils/lbfgsb_scipy.py:32 |

Errors mentioning `_Mock` or `DataLoader` come from this sandbox's stand-in for PyTorch, not from the repo.
