# Existing audits rerun through the audit package

Every stored number recomputed from raw outputs (result.json, summary.json, state snapshots, method rows, recorded artifacts) and compared with the stored file at its JSON pointer. Gate: |difference| <= 0.001; counts and verdicts exact.

| Bundle | Compared | Passed | Max abs difference |
|---|---|---|---|
| B1 | 188 | 188 | 4.9e-05 |
| B2 | 55 | 55 | 9.1e-05 |
| B3 | 1055 | 1055 | 4.9e-05 |
| all | 1298 | 1298 | 9.1e-05 |

## By audit

| Bundle | Audit | Numbers | Max abs difference | All pass |
|---|---|---|---|---|
| B1 | AB-01 | 66 | 4.9e-05 | True |
| B1 | AB-04 | 36 | 4.9e-05 | True |
| B1 | AB-06 | 72 | 4.9e-05 | True |
| B1 | BLD-06 | 14 | 2.2e-16 | True |
| B2 | AB-01 | 18 | 9.1e-05 | True |
| B2 | AB-06 | 25 | 4.8e-05 | True |
| B2 | BLD-06 | 12 | 0 | True |
| B3 | AB-06 | 21 | 4.9e-05 | True |
| B3 | BND-08 M3 | 6 | 0 | True |
| B3 | BND-08 by role | 27 | 0 | True |
| B3 | BND-08 crashes | 6 | 0 | True |
| B3 | BND-08 stages | 480 | 0 | True |
| B3 | RQ-17 by role | 27 | 0 | True |
| B3 | RQ-17 crashes | 6 | 0 | True |
| B3 | RQ-17 stages | 482 | 0 | True |

## Findings per system (protocol v1; F fires, c clear, i inconclusive, - not checkable, . not run)

| Audit | K01 | K02 | K03 | K04 | K05 | K06 | K07 | K08 | K09 | K10 | K11 | K12 | K13 | K14 | K15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| matmcd | c | **F** | c | **F** | c | . | **F** | . | . | c | - | c | c | - | **F** |
| vashishtha | c | c | c | c | i | . | c | . | . | c | - | i | c | - | **F** |
| pywhyllm | **F** | **F** | c | i | - | . | - | . | . | - | - | - | c | - | **F** |
| causaliq | c | c | c | **F** | - | . | - | . | . | - | - | - | c | - | **F** |
| causal_copilot@bnd08 | **F** | - | . | **F** | **F** | . | - | . | . | **F** | **F** | i | - | - | - |
| causal_copilot@ab06cc | **F** | - | . | c | c | . | - | . | . | **F** | **F** | **F** | - | - | - |
| causal_copilot@main | **F** | - | . | **F** | **F** | . | - | . | . | **F** | **F** | i | - | - | - |
| causal_copilot@bld06 | c | - | . | c | c | . | - | . | . | c | - | i | - | - | - |
| pc@semantic | **F** | c | . | . | . | c | - | . | . | - | - | - | - | - | c |
| pc@formula | **F** | c | . | . | . | c | - | . | . | - | - | - | - | - | c |
| ges@semantic | **F** | c | . | . | . | c | - | . | . | - | - | - | - | - | c |
| ges@formula | **F** | c | . | . | . | c | - | . | . | - | - | - | - | - | c |
| gies@semantic | c | c | . | . | . | c | - | . | . | - | - | - | - | - | **F** |
| gies@formula | c | c | . | . | . | c | - | . | . | - | - | - | - | - | **F** |
