# DRAFT (not sent): PC `original` and `stable` keep edges a perfect oracle would remove

Repository: huawei-noah/trustworthyAI (gcastle 1.0.4, PyPI). With an oracle CI test (d-separation in the true DAG),
`castle.algorithms.PC(variant="original")` returns the true skeleton on 456 of 720 runs (120 random 6-12 node DAGs x 6
column orders) and `variant="stable"` on 460; `variant="parallel"` on 720. Every error is an extra adjacency: the
separating set exists but is only searched among the neighbours of one endpoint. Results:
cc-research `analysis/results/engine_oracle/oracle.json` (AUD-27). Reproduction script: `analysis/engine_oracle_check.py`.
