# DRAFT (not sent): the vendored causal-learn PC returns wrong skeletons with a perfect oracle

Repository: Lancelot39/Causal-Copilot (commit a31aa7c), `externals/causal-learn`. With d-separation as the CI test, its
PC returns the true CPDAG on 460 of 720 runs (120 random 6-12 node DAGs x 6 column orders) and order-invariant output on
56 of 120 DAGs; causal-learn 0.1.3.8 and 0.1.4.8 from PyPI return 720/720 and 120/120. Every error is an extra adjacency.
Also: its d-separation test fails in joblib loky worker processes (`NameError: nx`), so the oracle test cannot run as shipped.
Results: cc-research `analysis/results/engine_oracle/oracle.json` (AUD-27).
