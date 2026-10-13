# Pass 5: what each algorithm family can identify, and what the pipeline keeps of it

Baseline `a31aa7c`. Sources: reading of the wrappers and `postprocess/`, the offline experiment (`results/offline/`), the micro-tests (`results/encoding/encoding_consumers.md`), and the two golden runs.

## 1. Background in one paragraph

Observational data alone usually cannot decide the direction of every edge. Under the standard assumptions, constraint-based and score-based methods recover an equivalence class: a CPDAG, in which a directed edge is common to every graph in the class and an undirected edge means "the data do not say which way". FCI allows hidden common causes and returns a PAG, whose endpoints can also be circles ("not determined"). Only methods that assume more, for example linear relations with non-Gaussian noise, return a single fully directed graph. So an undirected or circle mark is a result, not a gap: it is the algorithm reporting the limit of what the data identify.

## 2. The encoding (CODE VERIFIED)

One integer matrix `M`. `M[i, j] = 1` means j -> i. Other codes: 2 undirected, 3 bidirected, 4 circle-arrow, 5 circle-tail, 6 circle-circle, 7 "associated". A symmetric mark is stored in one cell only, and which cell depends on the wrapper: PC, GES, GRaSP and FCI mostly above the diagonal, XGES and FGES mostly below. The matrix has no field for where a mark came from or how strongly it is supported.

## 3. Per family

Survival = share of the family's S0 edges still adjacent after the bootstrap step, offline seed 0. "Not run" means the wrapper needs PyTorch, which my sandbox lacks, or is a time-series method outside the tabular CLI path.

| Family (wrappers) | What the method identifies | What the wrapper emits (edges seen, all seed-0 cells) | Survival through the bootstrap step | Share of nonzero cells above the diagonal (the only cells KCI pruning tests) |
|---|---|---|---|---|
| Constraint-based, no hidden variables: PC | CPDAG | directed 30, undirected 33 | 57% | 73% |
| Constraint-based with hidden variables: FCI | PAG | circle-circle 24, directed 14, bidirected 8, circle-arrow 8; "associated" seen live | 35% | 72% |
| Score-based: GES, FGES, XGES | CPDAG | GES directed 24, undirected 35; FGES 27, 18; XGES 27, 24 | GES 44%, FGES 60%, XGES 59% | GES 76%, FGES 24%, XGES 24% |
| Permutation-based: GRaSP | CPDAG | directed 24, undirected 35 | 44% | 76% |
| Linear non-Gaussian: DirectLiNGAM, ICA-LiNGAM | a single DAG, if the model holds | directed only | 97%, 100% | 41%, 34% |
| Continuous optimisation: NOTEARS-linear | returns a single DAG; the data identify it only under extra assumptions | directed only | 100% | 44% |
| Markov-blanket based: BAMB, IAMBnPC, InterIAMB, MBOR, HITON-MB | local neighbourhoods, then orientation | undirected, directed, and cell pairs (2, 1) that the encoding table does not define; HITON-MB returned no edges | 19-39% | 52-71% |
| GOLEM, CORL, NOTEARS-nonlinear, Hybrid, CDNOD, time-series wrappers | | not run | | |

Pooled over all algorithms, survival by edge type is: directed 96%, undirected 16%, circle-circle 12%, bidirected 12%. The per-family survival figures above are mostly a statement of how much of each family's output is non-directed.

## 4. What each consumer of the matrix does with a non-directed mark (CODE VERIFIED by micro-test)

| Consumer | Directed (1) | Undirected (2), bidirected (3), circle marks (4, 5, 6) | "Associated" (7) |
|---|---|---|---|
| Bootstrap tally | counted in its own layer | counted, each in its own layer | not counted at all |
| Bootstrap edit rule (`judge.py:68-86`) | kept if the directed frequency is at least 0.9; deleted if at most 0.1; otherwise queued | deleted, even when found in 100% of resamples, because only the directed layer is consulted | deleted |
| Text shown to the LLM | "B causes A" | a sentence per type; circle-circle is described as "has no D-seperation set with" | an empty sentence |
| LLM review answers | A, B: write a directed edge; C: delete; D: leave | same; an A or B answer replaces the mark with a directed edge | same |
| KCI pruning | tested only if stored above the diagonal | same | same |
| Cycle step | follows directed cells | a triangle of undirected edges stored in mixed cells is treated as a directed cycle and loses an edge (LLM chooses which) | |
| Evaluation in the pipeline | see section 5 | | |
| Effect estimation (`causal_inference/inference.py:65`) | builds its graph from the revised matrix | | |

## 5. Evaluation is not comparable across algorithms (CODE VERIFIED, seen in records)

`Judge.evaluation` (`postprocess/judge.py:232-259`) uses causal-learn's SHD and adjacency metrics for PC, FCI, GES and CDNOD, and a cell-by-cell comparison of the integer matrix with the 0/1 truth for every other algorithm. The same result therefore scores differently depending on who produced it. On Linear_Gaussian the single undirected edge X2 --- X4 scored SHD 0, F1 1.0 when PC produced it (stub dry run) and SHD 1, F1 0 when XGES produced it (golden run). The revised graph is not scored at all on the CLI path: `results.revised_metrics` is never assigned.

Separately, the repo's benchmark code (`causal_discovery/evaluation/benchmarking_integrated.py`) scores the algorithm output and never calls the refinement stage. UNCLEAR: which graph the paper's Table 2 scores. That is a question for the authors.

## 6. INFERENCES

- I5.1 The refinement stage is written as if every algorithm returned a DAG. For the families that return equivalence classes, each consumer in section 4 either drops the non-directed marks or converts them to directed edges. The information "the data do not determine this direction" does not survive to the final graph.
- I5.2 This matters most where the method selection goes most often. In both live runs the LLM chose an equivalence-class method (XGES, FCI), and CausalSteward (arXiv 2607.01936) reports that Causal-Copilot "often preferred intractable methods such as FCI" in their use of it.
- I5.3 Established practice already has the missing distinction. bnlearn reports edge strength regardless of direction and direction given presence as two numbers; Tetrad and Debeire et al. (CLeaR 2024) vote over full edge types including circle marks. Each of those would have kept the 95%-stable undirected edge that Causal-Copilot deleted. For PAG marks, however, there is no peer-reviewed aggregation rule with guarantees (literature report, section on resampling).

## 7. OPEN QUESTIONS

- Q5.1 Behaviour of the wrappers that were not run.
- Q5.2 Whether the simulated datasets are varsortable (Reisach et al., NeurIPS 2021), which would flatter NOTEARS-type methods; not yet measured.
- Q5.3 Whether the (2, 1) cell pairs from the Markov-blanket wrappers are intended.

## CONFIDENCE

High for sections 2, 4 and 5 (each row was executed against the repo's functions or seen in a record). Medium for the survival figures as estimates of general behaviour (small graphs, default hyperparameters).
