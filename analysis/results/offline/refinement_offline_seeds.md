# Offline refinement experiment across seeds 0, 1, 2

59 (dataset, algorithm) combinations have a completed cell for every seed; 236 completed cells in total were read.
A seed fixes the random numbers used by the 20 bootstrap resamples. The datasets do not change with the seed.

Gate S1 (every compared combination complete for every seed): PASS

## 1. Survival of algorithm-output edges through the bootstrap step, per seed

| Edge type in S0 | seed 0 | seed 1 | seed 2 |
|---|---|---|---|
| directed | 215/221 (97%) | 217/221 (98%) | 216/223 (97%) |
| undirected | 16/145 (11%) | 11/145 (8%) | 16/145 (11%) |
| o-o | 3/24 (12%) | 4/24 (17%) | 4/24 (17%) |
| bidirected | 1/8 (12%) | 1/8 (12%) | 1/8 (12%) |
| a o-> b | 2/6 (33%) | 2/6 (33%) | 2/6 (33%) |
| b o-> a | 0/2 (0%) | 0/2 (0%) | 0/2 (0%) |

## 2. Adjacency F1 before and after the bootstrap step, per algorithm

Mean over datasets within a seed, then mean ± spread (population s.d.) of those means across seeds. "Worse in every seed" counts datasets where S1 scored below S0 for all seeds; "better in any seed" counts datasets where S1 scored above S0 at least once.

| Algorithm | Datasets | adj F1 S0 | adj F1 S1 | Worse in every seed | Worse in some seeds | Better in any seed | S0 identical across seeds |
|---|---|---|---|---|---|---|---|
| DirectLiNGAM | 8 | 0.76 ± 0.00 | 0.76 ± 0.00 | 0 | 0 | 2 | 8 of 8 |
| FCI | 8 | 0.85 ± 0.00 | 0.30 ± 0.00 | 8 | 0 | 0 | 8 of 8 |
| FGES | 8 | 0.82 ± 0.00 | 0.40 ± 0.00 | 8 | 0 | 0 | 8 of 8 |
| GES | 9 | 0.88 ± 0.00 | 0.35 ± 0.00 | 9 | 0 | 0 | 9 of 9 |
| GRaSP | 9 | 0.88 ± 0.01 | 0.34 ± 0.00 | 9 | 0 | 0 | 8 of 9 |
| PC | 9 | 0.86 ± 0.00 | 0.44 ± 0.07 | 8 | 1 | 0 | 9 of 9 |
| XGES | 8 | 0.87 ± 0.00 | 0.43 ± 0.01 | 8 | 0 | 0 | 8 of 8 |

## 3. How much the bootstrap-step result itself moves between seeds

For each (dataset, algorithm): the number of adjacencies in S1 under each seed. A row is listed when the seeds disagree.

| Dataset | Algorithm | S0 adjacencies | S1 adjacencies by seed |
|---|---|---|---|
| LiNG_10nodes | FCI | 11/11/11 | 6 / 7 / 8 |
| LiNG_10nodes | PC | 11/11/11 | 8 / 9 / 9 |
| Linear_Nongaussian | PC | 1/1/1 | 0 / 0 / 1 |
| sachs(reference) | DirectLiNGAM | 11/11/11 | 11 / 10 / 11 |
| sachs(reference) | GES | 8/8/8 | 2 / 3 / 2 |
| sachs(reference) | PC | 8/8/8 | 4 / 2 / 3 |
| sachs(reference) | XGES | 8/8/8 | 3 / 3 / 2 |
| sim_linear_gaussian_p8_s0 | PC | 8/8/8 | 3 / 2 / 4 |
| sim_linear_gaussian_p8_s0 | XGES | 8/8/8 | 2 / 2 / 4 |
| sim_linear_gaussian_p8_s1 | GRaSP | 8/8/10 | 7 / 7 / 6 |
| sim_linear_gaussian_p8_s2 | DirectLiNGAM | 16/16/16 | 14 / 16 / 14 |
| sim_linear_gaussian_p8_s2 | PC | 8/8/8 | 5 / 3 / 5 |
| sim_linear_gaussian_p8_s2 | XGES | 8/8/8 | 4 / 5 / 4 |
| sim_linear_uniform_p8_s2 | PC | 8/8/8 | 4 / 2 / 2 |

14 of 59 combinations give a different number of surviving adjacencies depending on the seed.

## 4. LLM review queue

Every pair and every self-pair queued for LLM review in every cell and seed: TRUE.
