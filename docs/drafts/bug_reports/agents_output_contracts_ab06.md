# Draft notes to maintainers: findings from AB-05/AB-06 (EXT-06; for Uzair to send or not)

Each note states what was measured, where in the code it happens, and the smallest fix. All runs were on CausalArena semantic
scenarios with shuffled columns, through a recording proxy; nothing in the agents was modified.

## Vashishtha et al., Causal_Order_Imperfect_Experts (commit ad609dbd)

- **What:** with the README's two-model setup (`--subgraph-model gpt-4o-mini --expert-model gpt-4o`), 91% of triplet answers
  had no `<Answer>` tag on a 25-variable scenario (2,096 of 2,300), and 84% on average over ten runs.
  - 2,105 of 2,300 stopped at `finish_reason=length`.
  - `parse_answer_tag` returns `None`, the triplet becomes `[]`, and it casts no vote.
  - 38-93% of pairs then go to the gpt-4o tie-breaker.
- **Where:** `strategies/triplet.py`, `query_triplet_subgraph`: the prompt asks for reasoning before the tagged answer with
  `max_tokens=300`.
- **Smallest fix:** raise the limit, ask for the tagged answer first, or count untagged answers and stop or warn above a
  threshold. Today a single print line per triplet is the only sign.

## MATMCD, D2I-Group/matmcd (commit ef2c3eca)

- **What:** the constraint agent's "No" in both directions forbids the edge in the final PC run, which deletes connections
  the data found.
  - With neutral or swapped names, the final graph's directed F1 fell from 0.381 (its own first PC run) to 0.251 and
    0.259, below its own PC graph in 9 and 8 of 10 scenarios.
  - With real names, decision-value precision fell from 0.720 to 0.686.
- **Where:** `GTdatasets_experiment.py` passes the constraint matrix to `causal_discovery(..., constraint_matrix=C)`, where
  0 means forbidden.
  - Also: `ConstrainAgent/LLMs.py:174` describes `M[i, j] != 0` as "labels[i] is the cause of labels[j]", but `cg2matrix`
    uses `M[i, j] == 1` for j → i, so the graph shown to the model is reversed.
  - `LLMs.py:220` caches the graph sentence, so every prompt describes the first pair.
- **Smallest fix:** let knowledge orient, never delete: drop forbidden-both-ways constraints, or require data agreement
  before removing an edge. Fix the arrow description and the caching.

## PyWhy-LLM via guidance (pywhy-llm 66f2d59, guidance as pinned)

- **What:** one run of 80 crashed in `guidance/_schema.py` (`TokenUsage`): pydantic rejected a negative time-to-first-token
  (−1.04 s), so the library fails when the host clock steps backwards mid-call.
- **Smallest fix:** use a monotonic clock for latency, or clamp at 0.

## Causal-Copilot (EXT-03, unchanged)

`postprocess/judge_functions.py:562` reads `response['nodes']`, a key the prompt never names: 18 of 19 live entries into the
cycle step crashed. Draft: `causal_copilot_vendored_pc.md` and EXT-03.
