# How downstream steps treat each edge code (pass 5 micro-tests)

Each row is one crafted 3-variable graph with a single mark between A and B, pushed through the repo's own functions.

| Code | Meaning | Stored in | Listed by `convert_to_edges` as | Counted by the bootstrap tally as | Survives the bootstrap step if found in 100% of resamples | KCI step looks at it |
|---|---|---|---|---|---|---|
| 1 | directed | upper [A,B] | certain [('B', 'A')] | certain at [(0, 1)] | yes | yes |
| 1 | directed | lower [B,A] | certain [('A', 'B')] | certain at [(1, 0)] | yes | **no** |
| 2 | undirected | upper [A,B] | uncertain [('A', 'B')] | uncertain at [(0, 1), (1, 0)] | **no** | yes |
| 2 | undirected | lower [B,A] | uncertain [('A', 'B')] | uncertain at [(0, 1), (1, 0)] | **no** | **no** |
| 3 | bidirected | upper [A,B] | bi [('A', 'B')] | bi at [(0, 1), (1, 0)] | **no** | yes |
| 3 | bidirected | lower [B,A] | bi [('B', 'A')] | bi at [(0, 1), (1, 0)] | **no** | **no** |
| 4 | o-> | upper [A,B] | half_certain [('B', 'A')] | half_certain at [(0, 1)] | **no** | yes |
| 4 | o-> | lower [B,A] | half_certain [('A', 'B')] | half_certain at [(1, 0)] | **no** | **no** |
| 5 | o- | upper [A,B] | half_uncertain [('B', 'A')] | half_uncertain at [(0, 1)] | **no** | yes |
| 5 | o- | lower [B,A] | half_uncertain [('A', 'B')] | half_uncertain at [(1, 0)] | **no** | **no** |
| 6 | o-o | upper [A,B] | none [('A', 'B')] | none at [(0, 1), (1, 0)] | **no** | yes |
| 6 | o-o | lower [B,A] | none [('A', 'B')] | none at [(0, 1), (1, 0)] | **no** | **no** |
| 7 | associated | upper [A,B] | associated [('B', 'A')] | no layer (not counted) | **no** | yes |
| 7 | associated | lower [B,A] | associated [('A', 'B')] | no layer (not counted) | **no** | **no** |

## Sentence shown to the LLM for each code

- code 1 (directed), upper [A,B]: "These variable pairs have certain directed edge between them: B causes A,"
- code 1 (directed), lower [B,A]: "These variable pairs have certain directed edge between them: A causes B,"
- code 2 (undirected), upper [A,B]: "These variable pairs have undirected relationship between them: A has undirected relationship with B,"
- code 3 (bidirected), upper [A,B]: "These variable pairs have hidden confounders between them: A has hidden confounder with B,"
- code 3 (bidirected), lower [B,A]: "These variable pairs have hidden confounders between them: B has hidden confounder with A,"
- code 4 (o->), upper [A,B]: "These variable pairs have non-descendant directed relationship between them: B is not a descendant of A,"
- code 4 (o->), lower [B,A]: "These variable pairs have non-descendant directed relationship between them: A is not a descendant of B,"
- code 5 (o-), upper [A,B]: "These variable pairs have non-descendant undirected relationship between them: B is not a descendant of A,"
- code 5 (o-), lower [B,A]: "These variable pairs have non-descendant undirected relationship between them: A is not a descendant of B,"
- code 6 (o-o), upper [A,B]: "These variable pairs have no D-seperation between them: A has no D-seperation set with B,"
- code 7 (associated), upper [A,B]: ""

## Cycle step on a triangle of undirected edges

- three undirected edges, all stored in the upper triangle: LLM cycle helper called 0 time(s); edges 3 -> 3.
- three undirected edges, stored A-B upper, B-C upper, A-C lower: LLM cycle helper called 1 time(s); edges 3 -> 2. Prompt: "B -> C -> A -> B"
