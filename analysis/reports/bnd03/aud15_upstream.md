# AUD-15: upstream branches against a31aa7c (2026-10-10)

Source: `analysis/results/upstream/upstream_check.json`, produced by `analysis/upstream_check.py` on a separate blobless
clone of https://github.com/Lancelot39/Causal-Copilot in the device's scratch space (never in Uzair's repo). All statements
below are **measured** from that clone unless marked.

- Upstream `main` is still `a31aa7c` (2026-05-15). 19 remote branches; one is newer than a31aa7c
  (`frontend-improvement`, 2026-06-01), and in it both crash functions are byte-identical to a31aa7c.
- **C1, cycle step** (`postprocess/judge_functions.py:562`, `return response['nodes']` in `LLM_remove_cycles`):
  a regression. Every branch from `cpu` (2025-01-13) to `feature-user-login-link` (2025-04-18) asked for structured output
  (`client.beta.chat.completions.parse(..., response_format=VarList)`) and read `.parsed.nodes`, which cannot miss the key.
  Commit `defa4df` (2025-06-26, "Unifying all the LLM call into a general LLMClient wrapper") replaced it with
  `chat_completion(..., json_response=True)` and dropped the schema, although `LLMClient.chat_completion` accepts
  `response_format` (`llm/llm_client.py:115`, used at :144-150). The `VarList` class is still defined two lines above the
  call and unused. Our live runs: 9 of 9 entries into this step crashed (answers used `edge_to_remove` or `nodes_to_remove`).
  Branches `maintenance`, `main`, `frontend-improvement` carry the regression; 5 older branches lack the function.
- **C2, start-up** (`global_setting/Initialize_state.py:178`, `info_extracted["linearity"]`): unguarded on all 19 branches;
  the line dates from October 2024 (`c4bdb69`, `155b19e`, `65257df`). Before `defa4df` the request used
  `response_format={"type": "json_object"}`, which enforces JSON but no keys, so an empty `{}` reply was already possible.
- **Interpretation.** No upstream branch fixes either crash. C1 has a one-argument fix (pass `response_format=VarList`);
  this is the content of the EXT-03 bug report, which stays Uzair's decision to send.
