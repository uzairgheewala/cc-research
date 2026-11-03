# Data facts for section 3 (DLV-05), checked 30-31 Oct 2026

Read by an independent checker on the licensor's or publisher's page; nothing from memory. Shapes in the paper come from
the suite manifests (numbers.json), not from this file; this file holds licences, citations and cross-checks.

| Dataset | Licence (source) | Citation | Cross-check of shape |
|---|---|---|---|
| CausalArena | `license: cc-by-4.0` on the dataset card (huggingface.co/datasets/LAMDA-Tabular/CausalArena, raw README) | Li, Liu, Wang, Ye, arXiv 2609.11897 (v1 10 Sep 2026) | Paper: semantic pool of 100 scenarios in 10 domains, 17-25 variables and 25-67 edges each; 1,000 observational rows per run; half of each family public. Ours: 10 test scenarios, 20-25 variables, 35-58 edges, 1,000 rows (consistent) |
| CausalBench data (Replogle et al. 2022) | CC BY 4.0 (CausalBench README; figshare+ deposit 10.25452/figshare.plus.20029387.v1) | Replogle et al., Cell 185(14), 2022 | CausalBench Table 1: K562 162,751 samples, 10,691 observational, 622 gene interventions; RPE1 162,733, 11,485, 383. Ours (external/causalbench/*.npz.json): identical |
| CausalBench code | Apache License 2.0 (LICENSE.txt) | Chevalley et al., Communications Biology 8:412, 2025 (article itself CC BY-NC-ND 4.0) | - |
| Sachs | no licence found (Crossref record has none; science.org not readable) | Sachs et al., Science 308(5721), 2005 | - |
| Abalone | CC BY 4.0 (UCI page) | Nash et al. 1994, doi 10.24432/C55C7W | UCI 4,177 instances; ours 4,177 rows |
| Auto MPG | CC BY 4.0 (UCI page) | Quinlan 1993, doi 10.24432/C5859H | UCI 398 instances; ours 392 rows (Causal-Copilot's copy; CausalArena's index also 398) |
| Concrete | CC BY 4.0 (UCI page) | Yeh 1998, doi 10.24432/C5PK67 | UCI 1,030 instances, 9 attributes; ours 1,030 rows, 9 variables |
| DWD climate | DWD open data: "The Creative Commons BY 4.0 - Licence "CC BY 4.0" apply" (opendata.dwd.de Terms_of_use.pdf, May 2024); the Tuebingen pairs page states no licence | Mooij et al., JMLR 17(32), 2016 (pairs 0001-0004: DWD, 349 stations) | ours 349 rows, 5 variables; matches pairs 0001-0004 (provenance inferred, not stated by Causal-Copilot) |
| Causal-Copilot | MIT (LICENSE) | Wang et al., arXiv 2504.13263 (v2 21 Apr 2025) | - |

Notes carried into the paper: DWD has 5 variables (no latitude); the 50 public semantic models are half of a pool of 100;
cite the Communications Biology version of CausalBench; Sachs: "no licence stated".
