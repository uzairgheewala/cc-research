# Pass 3: where Causal-Copilot depends on an LLM

Baseline: upstream commit `a31aa7c`. Tools: `llm_inventory_scan.py` (AST scan), `llm_inventory_build.py` (classification and reconciliation with recorded runs). Full table: `results/llm_inventory/llm_inventory.csv` (88 rows). Readable summary: `results/llm_inventory/llm_inventory.md`.

Labels used: CODE VERIFIED (read in the source and, where stated, seen in a recorded run), PARTIAL (classified from the prompt text only, function body not read line by line), PAPER CLAIM, UNCLEAR.

## Acceptance gates

| Gate | Meaning | Result |
|---|---|---|
| G1 | the AST scan and a plain text search find the same request-issuing call sites | PASS (51 = 51) |
| G2 | every logical LLM point has a classification | PASS (88 of 88) |
| G3 | every caller recorded in a live or stub run is a site in the inventory | PASS (107 recorded calls map to 14 sites) |
| G4 | recorded request flags (JSON mode, model) match what the static read predicts | PASS |

Classification basis: 47 points read in the source, 41 classified from their prompt only. The 41 are almost all in the web demo and the inference module, which the CLI pipeline does not reach.

## FACTS

- F3.1 CODE VERIFIED. 51 call sites issue an LLM request; 47 of them are outside the `llm/` client package. Counting each caller of the generic helper separately gives 88 logical LLM points.
- F3.2 CODE VERIFIED. By path: inference (web demo) 30, web demo only 23, report 19, discovery (CLI and web) 11, benchmark/test 2, online simulation 1, dead code 2.
- F3.3 CODE VERIFIED. By kind: 29 decisions, 30 descriptive, 19 interpretation, 3 format repair, the rest mixed or dead.
- F3.4 CODE VERIFIED. Three points write to the causal graph directly: `postprocess/judge_functions.py:288` (the A/B/C/D edge review), `postprocess/judge_functions.py:556` (which edge of a cycle to delete), `web_demo/help_functions.py:780` (parsing a user's edge edits).
- F3.5 Of the 29 decision points: 12 apply the answer with no check on its content (CODE VERIFIED for the 8 that were read, PARTIAL for 4 classified from the prompt); 14, all in the effect-estimation module, were not examined for checks; 3 have a partial check (the hyperparameter selector filters keys to the primary parameters but does not check values; two parsers in `causal_inference/main.py:31` and `web_demo/help_functions.py:852` use a lenient schema class). The filter's unknown algorithm names are dropped one step later at `rerank.py:58`.
- F3.6 CODE VERIFIED, seen live. The hyperparameter filter drops what the LLM proposed outside the primary list. In the sachs golden run the LLM proposed `background_knowledge` with five required edges; none reached the algorithm, and the state keeps no note that it was dropped.
- F3.7 CODE VERIFIED. What is kept of each discovery-path decision: the filter, rerank and hyperparameter prompts and answers are kept in `logging.*_conversation`; the query-parse prompt and answer are not kept (only the parsed fields); for the edge review only A/B/C answers with their explanation are kept in `results.llm_errors`, D answers are not; the cycle-step answer is not kept.
- F3.8 CODE VERIFIED, seen live. The domain-knowledge text elicited at `preprocess/dataset.py:121` and `:138` is prose, and it is pasted into the filter, rerank, hyperparameter and edge-review prompts. In the sachs run that text names the "Sachs dataset" and "Sachs et al. (2005)", so every later decision prompt carried the dataset's identity.
- F3.9 CODE VERIFIED. The knowledge prompt contains the dataset file path. Path and column names are therefore two separate cues to the dataset's identity (pass 4b separates them).
- F3.10 Sites on the CLI and report path never exercised by the recorded runs: the runtime estimator's LLM guess, `LLM_remove_cycles`, four report prompts (background, comparison, keywords, LaTeX conversion), LaTeX bug checking, and the follow-up discussion. Their behaviour is known from reading only.

## Token use seen live (two golden runs, gpt-4o, snapshot gpt-4o-2024-08-06)

| Stage | Calls | Prompt tokens | Completion tokens |
|---|---|---|---|
| Edge review (`judge_functions.py:288`) | 16 | 36,296 | 2,478 |
| Algorithm ranking (`rerank.py:103`) | 2 | 23,347 | 978 |
| Hyperparameters | 2 | 11,990 | 716 |
| Algorithm shortlist | 2 | 9,303 | 1,042 |
| Report and discussion (7 sites) | 16 | 15,596 | 5,668 |
| Query parse and domain knowledge | 6 | 2,690 | 2,077 |

The edge review is the largest consumer and the only stage whose answer becomes graph structure.

## INFERENCES

- I3.1 The discovery path has two kinds of LLM dependence that should be kept apart in any later design: choices about how to analyse (algorithm, hyperparameters, preprocessing), and assertions about the answer (edges). Only the second kind changes what the graph claims.
- I3.2 The domain-knowledge prose is the system's main hidden channel. It is elicited once, never typed, and then reused as free text in four later prompts. This is the closest thing in the code to the "context" in the working hypothesis, and it is the least inspected.

## OPEN QUESTIONS

- Q3.1 The 41 prompt-only classifications (web demo, inference) have not been read line by line.
- Q3.2 Whether the web demo's edge review differs from the CLI's in what it lets the LLM change (the demo asks first whether variable names are meaningful; the CLI does not).

## CONFIDENCE

High for counts and for the 12 discovery-path decision points. Medium for the web-demo and inference classifications.
