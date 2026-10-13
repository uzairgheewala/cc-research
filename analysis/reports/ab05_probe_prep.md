# AB-05 (AUD-37) agent probes: offline preparation

Written 2026-10-12. No live API call was made, and no `.env` file or key was read. Every cost in this report is an
**estimate** from stub runs, with prompt tokens counted locally and completion lengths assumed (section 4). Stub graphs and
their F1 scores mean nothing, because the stub's answers are random.

## 1. Result in one table

These are stub runs on the first `semantic_obs_only` file
(`semantic_cybersecurity_and_it_operations_api_rate_limit_abuse_spillover__semantic_obs_only__rep000.npz`: 25 variables,
1,000 rows, 67 true edges), with shuffle seed 20261010. Each agent uses the model configuration in its plan file
(section 5).

| Agent | Installs (py3.10, pinned) | End to end in stub | Calls / run | Tokens / run (prompt + completion) | Est. cost / run, plan models | Est. cost / run, all gpt-4o | Failure points seen | Licence |
|---|---|---|---|---|---|---|---|---|
| Vashishtha et al. (triplet + order-oriented PC) | yes, 48 packages | yes (semantic). Formula rep000: no, fails at PC before any call. Runs with `--jitter 1e-6` | 2,334 (2,300 triplet on gpt-4o-mini + 34 tie-break on gpt-4o) | 884k + 520k | **$0.85** | $7.41 | Fisher-z singular matrix on formula rep000 and on 1 of 10 semantic dev files | **none shown**: evaluation use only, never redistribute |
| PyWhy-LLM (ModelSuggester, Pairwise) | yes, 50 | yes (semantic and formula) | 301 (1 expertise + C(25,2)) | 111k + 94k | **$1.22** (gpt-4o) | $1.22 | none | MIT |
| MATMCD (CC-Agent on PC) | yes, 89 | yes (semantic). Formula rep000: no, fails at its own first PC (`Utils/CausalDiscovery.py:84`), 0 calls. Runs with `--jitter 1e-6` | 1,200 (2 x d(d-1)) | 845k + 242k | **$0.27** (gpt-4o-mini) | $4.53 | same Fisher-z failure as Vashishtha | MIT |
| causaliq-knowledge (PDG graph generation) | yes, 42 | yes (semantic and formula) | 1 | 463 + 1,120 | **$0.012** (gpt-4o) | $0.012 | none | MIT |

Formula rep000 (`formula_biology_physiology_and_ecology_blood_oxygen_content__formula_obs_only__rep000.npz`, 22 variables,
31 true edges):

- PyWhy: 232 calls, $0.94.
- causaliq: 1 call, $0.011.
- With `--jitter 1e-6`: Vashishtha 1,568 calls ($0.63 with plan models, $5.05 all gpt-4o) and MATMCD 924 calls ($3.27 all gpt-4o).
- Without jitter, PC raises `ValueError: Data correlation matrix is singular` at `causallearn/utils/cit.py:174`. Upstream causal-learn PC fails the same way on 73-75 of 250 formula files in our earlier reproductions (`results/methods/pc_upstream_formula_obs_*.json`).
- The jitter is the kit's GIES convention (`analysis/baseline_variants_run.py`), seeded by crc32 of the file name. It is off by default and recorded in `summary.json`.

Every agent runs end to end on a 20-25 variable scenario. None had to be dropped.

Stub outputs are in `runs/ab05/stub/<agent>/<file>/`, `runs/ab05/stub_plan/<agent>/` (the plan files themselves) and
`runs/ab05/stub_dev/<agent>/<scenario>/`. That folder is gitignored and holds 216 MB, mostly `calls.jsonl`.

## 2. What runs, per agent

Every agent sees the variable names and data in shuffled column order: perm = `default_rng(seed + crc32(file name))`,
the same convention as `causalarena_methods.py`. Agents that take a domain string get the scenario's `domain_id` in plain
words (here "cybersecurity and it operations"). `--context-text` overrides it, and `--context-text ""` gives none.
Results are mapped back to the original column indices and scored with the random rule, seeded per file
(`probe_io.py` is an unchanged copy of `causalarena_io.load/directed_scores`, and a test checks that the copy still
agrees with the original).

### Vashishtha et al.

- **Entry point:** `strategies/triplet.run_triplet_experiment`, the README's triplet strategy. The subgraph model orients each 3-subset, votes are merged, and the expert model breaks ties with a CoT prompt.
- **Cycle removal:** the repo's `utils/cycle_remover.remove_cycles`, applied as `run_triplet.py` does.
- **What the repo lacks:** it ships **no** order-constrained discovery code.
- **Downstream step:** the harness implements the step as we read the paper's description. We could not re-check the paper here because arXiv is blocked from this sandbox. The step:
  - causal-learn PC (Fisher-z, alpha 0.05) runs on the shuffled data;
  - PC's committed arrows are kept and marked `data`;
  - each pair PC leaves undirected is oriented a -> b only if a is an ancestor of b in the acyclic LLM graph, and marked `llm_order`;
  - pairs the LLM graph does not order stay undecided. No arbitrary total order is imposed.
- **Variants reported:** `llm_only_triplet_dag` and `pc_only`.
- **Ordering:** the PC step runs **before** the first LLM call, so a data failure costs nothing.
- **Pairwise option:** `--agent-opt strategy=pairwise` runs the repo's pairwise strategy instead.

### PyWhy-LLM

- **Entry point:** the README's Modeler flow, unchanged: `ModelSuggester.suggest_domain_expertises` followed by `suggest_relationships(..., RelationshipStrategy.Pairwise)`.
- **Inputs:** names only; the library has no data interface. The library ignores treatment and outcome in the Pairwise branch, so None is passed.
- **Dependencies:** the RAG extras (langchain, chroma, sentence-transformers, torch) are not installed because `AugmentedModelSuggester` is not used. The package `__init__` imports cleanly without them.

### MATMCD

- **Entry point:** the first agent stage of `GTdatasets_experiment.py`, unchanged:
  - PC;
  - `ConstrainNormalAgent(..., use_reasoning=False).run(use_cache=False)`;
  - PC again with the constraint matrix as background knowledge.
- **Not run: the DA-Agent** (web search through Serper or Tavily). It needs search keys and live web content, so the paper's "MATMCD" and "MATMCD-R" rows are out of scope. This is a scope limit, not a failure.
- **Provenance:** a final arrow a -> b is marked `llm` when the constraint required a -> b or forbade b -> a; otherwise it is `data`. Edge existence is also gated by the LLM, because a pair answered "No" both ways is removed from the skeleton.

### causaliq-knowledge

- **Entry point:** `GraphGenerator("openai/<model>").generate_pdg_from_context(NetworkContext)`, as the CLI `cqknow generate-graph` calls it. This is one call per graph.
- **Configuration:** CLI defaults (temperature 0.1, prompt detail "standard", `max_tokens` 2000); variables are given as `type="continuous"` with no descriptions.
- **Decision rule:** each pair takes the PDG's `most_likely_state`. An exact forward/backward tie (orientation 0.5) is treated as **undecided**. This is a harness choice, made so that no direction comes from JSON key order.
- **Library DAG:** reported as a variant. It breaks ties **alphabetically** (`tie_breaks_applied`), which is a name-order channel worth knowing about.
- **Stale README:** the Quick Start (`causaliq_knowledge.llm.LLMKnowledge.query_edge`) does not exist at the pinned commit.

### Agent quirks found in code (recorded, not fixed)

**MATMCD:**
- `ConstrainAgent/LLMs.py:174` describes the PC graph as "labels[i] is the cause of labels[j]" for M[i, j] != 0. But `cg2matrix` uses M[i, j] == 1 to mean j -> i, and it also writes undirected pairs as causes. So the LLM is shown the data graph with its arrows reversed.
- `LLMs.py:220` builds that graph text once and caches it. The sentence at lines 178-181 ("it seems that changes in X directly affect / do not affect Y") therefore names the first pair in every one of the 600 prompts.
- `BackgroundKnowledge.add_*_by_pattern` matches by regex prefix (`causallearn/.../BackgroundKnowledge.py:135`). A name that is a prefix of another name widens a constraint. The adapter lists such collisions; there are none in the first file.
- `Client/ReactClient.py:10` sets `os.environ["OPENAI_API_KEY"] = ""` at import time.

## 3. LLM interception

All four agents send chat-completion requests over httpx. A single httpx transport, `harness/probe_llm.py` (`ProbeLLM`), is handed to each agent's own client. Every request goes through it.

**What the gate does with each request:**
- **Caps:** it enforces `--max-calls` and `--max-usd` *before* sending. For the USD check it projects the next call at its prompt plus `max_tokens`, or plus 600 tokens when `max_tokens` is unset. It then raises `CapReached`.
- **Clean abort:** `CapReached` is a `BaseException`, so agent `except Exception` retry loops cannot swallow it. These loops exist in Vashishtha's `query_llm` and pairwise loop and in PyWhy's `while not success`. The runner records the state and exits with code 3.
- **Stub mode:** it answers with the adapter's deterministic fake (seeded by the request's sha256), in the same wire format: JSON, or SSE for guidance.
- **Live mode:** it forwards the unchanged body to `https://api.openai.com/v1/chat/completions` with the key. **Only this object holds the key.** The agent process gets a dummy key, and `OPENAI_BASE_URL` points at a dead local port, so any client that is not intercepted fails fast instead of spending.
- **Logging:** each request is logged to `calls.jsonl` with the full request, prompt sha256, served model, usage (and where it came from), seconds and cost.
- **Resuming:** a rerun into the same `--out` replays earlier answers to identical requests for free and continues. The caps apply to the whole logical run. Tested: after a cap at 50 calls, then at $0.50, the third run finished with 178 new and 123 replayed calls and a result identical to the uninterrupted run.

| Agent | Where the agent makes the call | How it is pointed at the gate | Monkeypatch? |
|---|---|---|---|
| Vashishtha | `utils/llm_client.py:40` calls `_get_client()`, which hard-codes `OpenAI(api_key=...)` at line 19. No client or base_url parameter exists anywhere in the call chain | module attribute `causal_discovery.utils.llm_client._get_client` is replaced; it returns `openai.OpenAI(api_key=<dummy>, http_client=<gate>)`. `query_llm`, prompts, retries and parsing are unchanged. `delay` (a repo CLI parameter) is set to 0 | yes, one attribute |
| PyWhy-LLM | guidance builds `openai.OpenAI(api_key, **kwargs)` (`guidance/models/_openai.py:32`) | injection: `ModelSuggester(guidance.models.OpenAI(model, api_key=<dummy>, echo=False, http_client=<gate>))` | **no** |
| MATMCD | `Client/OpenAiClient.py:6` calls `OpenAI(api_key=api_key)`, built at `ConstrainAgent.py:77/197` from names imported from `config.py` | sets `ConstrainAgent.ConstrainAgent.MODEL / OPENAI_API_KEY` (the values config.py would hold) and replaces `ConstrainAgent.ConstrainAgent.OpenAIClient` with a subclass that changes only `__init__`. `inquire_LLMs` is inherited | yes, one class name in one module |
| causaliq | `llm/openai_compat_client.py:121` opens `httpx.Client(timeout=...)` and posts to the class constant `BASE_URL` (`openai_client.py:62`) | module attribute `causaliq_knowledge.llm.openai_compat_client.httpx` is replaced by a namespace identical to httpx, except that `Client` uses the gate's transport | yes, one module attribute |

The live branch was exercised without network or key, against a local fake upstream (JSON, SSE with usage, a 429 passed through to the SDK, and the USD cap refusing a call before it was sent). The Authorization header carried the gate's key only, and the key never appeared in `calls.jsonl`. The test suite also runs every stub with a sentinel `OPENAI_API_KEY` in the environment and checks that it appears in no output file.

## 4. How tokens were counted, and what is assumed

- **Prompt tokens.** They were counted with **tiktoken `cl100k_base`** (gpt-4's tokenizer), not o200k_base: this sandbox's proxy blocks the host that serves `o200k_base.tiktoken`. The cl100k file came from the PyPI wheel `tiktoken-offline` 0.1.1. Its sha256 (`223921b7...`) equals the hash tiktoken itself pins, and tiktoken re-checks it on load. The counter falls back to o200k_base, then cl100k_base, then characters / 4, and records which it used in every summary. In the image, o200k_base is cached at build time, so container stub runs count with gpt-4o's own tokenizer. For English, o200k counts are usually equal to or slightly below cl100k counts; this was **not measured here**. Chat overhead is the usual estimate of 3 tokens per message plus 3.
- **Completion tokens are assumed.** Stub replies are padded to these lengths, which are recorded per call as `assumed_completion_tokens`:

| Call type | Assumed tokens | Agent's own cap |
|---|---|---|
| Vashishtha triplet | 200 + answer (about 220) | `max_completion_tokens` 300 |
| Vashishtha tie-break | 220 | 400 |
| PyWhy expertise | 200 | none |
| PyWhy pairwise | 300 | none |
| MATMCD domain knowledge | 400 | none |
| MATMCD Yes/No | 2 | none |
| causaliq PDG | the JSON for 1.3 x d edges (about 1,100 tokens) | `max_tokens` 2000 |

- **Sensitivity.** Completions are 46-91% of the estimated cost. Per-run cost on the first file:

| Agent | Completions at 0.5x | As assumed | Completions at 2x |
|---|---|---|---|
| PyWhy | $0.75 | $1.22 | $2.15 |
| Vashishtha (plan models) | $0.65 | $0.85 | $1.23 |
| MATMCD (mini) | $0.20 | $0.27 | $0.42 |
| causaliq | $0.007 | $0.012 | $0.024 |

  The first live run's `calls.jsonl` gives the real lengths, so the AB-06 figures should be recomputed from it.
- **Prices.** gpt-4o list $2.50 / $10.00 per 1M tokens; gpt-4o-mini $0.15 / $0.60. `summary.json` gives both `est_usd_gpt4o_list` (every token at gpt-4o prices, as the brief asks) and `est_usd_at_served_prices`.

## 5. Live plans (`plans/ab05_probe_<agent>.json`)

**Rule for the caps.**
- `max_calls` = ceil(1.5 x stub calls).
- `max_usd` = 1.5 x the stub estimate at the plan's model prices, rounded up to the cent.
- `max_usd` is never set below the stub cost plus the gate's worst-case projection of one more call. Without that floor, the gate would refuse the run's own last call.
- The plans are generated by `plans/make_ab05_probe_plans.py`. All four were run in stub mode through `--plan` and finished inside their caps.

| Plan | Scenario, seed | Model | max_calls | max_usd | Basis (stub estimate) |
|---|---|---|---|---|---|
| causaliq | first semantic file, 20261010 | gpt-4o | 2 | 0.04 | $0.012. The 1.5x rule gives $0.02, but its one call can cost up to $0.021 at `max_tokens` 2000, so the gate would refuse it. The floor applies: stub cost + one worst-case call = $0.034, rounded up to $0.04 |
| pywhyllm | same | gpt-4o | 452 | 1.83 | $1.22 |
| matmcd | same | **gpt-4o-mini** | 1,800 | 0.41 | $0.27 |
| vashishtha | same | gpt-4o (expert / tie-break) and **gpt-4o-mini** (subgraph) | 3,501 | 1.27 | $0.85 |
| **Sum** | | | | **$3.55** (limit $4.00) | |

**Deviation from "model gpt-4o", flagged for Uzair.** The four agents cannot all run on gpt-4o inside $4.
- MATMCD alone would be about $4.53 per run, or $6.80 with the 1.5x margin.
- Vashishtha alone would be $7.41, or $11.03 with the margin.
- All four on gpt-4o would need about $19.7.

Both plans therefore use **the repositories' own model choices**:
- MATMCD's `config.py` sets `MODEL = "gpt-4o-mini"`.
- Vashishtha's README runs `--subgraph-model gpt-4o-mini --expert-model gpt-4o`.

If gpt-4o is required for every role, the alternative is to run only PyWhy and causaliq on gpt-4o ($1.87 in caps), or to raise the budget.

**Named before they happen (live failure modes):**
1. **Vashishtha, a malformed answer list.** One malformed `<Answer>` list among about 2,300 replies makes `ast.literal_eval` raise at `utils/helpers.py:35`, reached from `strategies/triplet.py:235`. This happens *after* all triplet calls are paid for. The answers stay in `calls.jsonl` and a rerun replays them for free, but the crash is deterministic. No guard was added, because that would change agent behaviour.
2. **Vashishtha, tie-breaks.** Each tie-break is about 4,100 prompt tokens on gpt-4o, about $0.013. The stub had 34 ties. Roughly 30 more ties than that reach the $1.27 cap, and the run exits with code 3; raise the cap and rerun to resume.
3. **PyWhy, unbounded loops and completions.** `while not success` loops have no limit (`model_suggester.py:32` for the expertise call, `:419` for each pair), and `gen()` has no `max_tokens`. Only the gate bounds these. If replies are twice the assumed length, the run reaches its $1.83 cap.
4. **MATMCD, an unparseable Yes/No reply.** A reply with neither "Yes" nor "No" makes `downstream_processing` return None (`LLMs.py:588-591`). Then `constrain_matrix[i, j] = None` raises at `ConstrainAgent.py:227`, which can come after up to 1,200 paid calls.
5. **causaliq, truncation.** If the model proposes more than about 70 edges, the JSON is cut at `max_tokens` 2000, and `graph/response.py:654` raises a parse error. That would cost one call.
6. **Fisher-z singular matrix.** Seen on formula files and on one of the 10 semantic dev scenarios (`injection_molding_cooling_warp`). It hits MATMCD and the Vashishtha downstream step, costs nothing (no LLM call is made), and is repaired by `--jitter 1e-6`.
7. **Rate limits.** With `delay=0`, a 429 is retried by the SDK and by Vashishtha's `query_llm` (up to 5 attempts with back-off). Every attempt counts against `max_calls`, but costs nothing.

**Wall time:** unknown until live. As a guess, Vashishtha makes about 2,300 sequential calls and MATMCD about 1,200, so each probably takes 1-3 h; PyWhy about 30 min; causaliq under a minute.

## 6. Container plan and the exact commands

`docker/Dockerfile.probes` builds a separate image, `FROM cc-research:a31aa7c-1`. `Dockerfile.overlay` and `cc.ps1` are unchanged.
- Each agent's pinned requirements go into their own `pip install --target /opt/probes/<agent>`.
- The agent sources are cloned from GitHub at the pinned commits and verified with `rev-parse`.
- `o200k_base` and `cl100k_base` are cached.
- The build fails if any agent cannot be imported.
- The build context is a temporary folder holding only the four requirement files. No `.env`, key, code or data is copied.
- **Do not push this image**: it contains the unlicensed Vashishtha code.

Run the following from the `cc-research` folder in PowerShell.

```powershell
# --- build once ---
$Research = (Get-Location).Path
$Repo     = Join-Path (Split-Path -Parent $Research) "Causal-Copilot"
$ctx = Join-Path $env:TEMP "cc-probes-context"
if (Test-Path $ctx) { Remove-Item -Recurse -Force $ctx }
New-Item -ItemType Directory -Path $ctx | Out-Null
Copy-Item (Join-Path $Research "harness\agents\requirements_*.txt") $ctx
docker build --build-arg BASE=cc-research:a31aa7c-1 -f (Join-Path $Research "docker\Dockerfile.probes") -t cc-probes:ab05-1 $ctx
docker image inspect cc-probes:ab05-1 --format "{{.Id}}"

# --- offline checks: unit tests, then every plan in stub mode (no network, no key, no cost) ---
docker run --rm -i --init --network none -v "${Research}:/research" -w /research -e PYTHONPATH= -e PYTHONDONTWRITEBYTECODE=1 `
  cc-probes:ab05-1 python -m unittest tests/test_agent_probe.py -v
foreach ($a in "causaliq", "pywhyllm", "matmcd", "vashishtha") {
  docker run --rm -i --init --network none -v "${Research}:/research" -w /research -e PYTHONPATH= -e PYTHONDONTWRITEBYTECODE=1 -e PYTHONUNBUFFERED=1 `
    cc-probes:ab05-1 python /research/harness/agent_probe.py --plan /research/plans/ab05_probe_$a.json --stub
}

# --- LIVE (spends money; one agent at a time; only the .env file is mounted, read-only) ---
$a = "causaliq"      # then "pywhyllm", "matmcd", "vashishtha"
docker run --rm -i --init -v "${Repo}\.env:/app/.env:ro" -v "${Research}:/research" -w /research -e PYTHONPATH= -e PYTHONDONTWRITEBYTECODE=1 -e PYTHONUNBUFFERED=1 `
  cc-probes:ab05-1 python /research/harness/agent_probe.py --plan /research/plans/ab05_probe_$a.json
```

The same live run written out without a plan file (Vashishtha shown; the other three take the values in their plans):

```powershell
docker run --rm -i --init -v "${Repo}\.env:/app/.env:ro" -v "${Research}:/research" -w /research -e PYTHONPATH= -e PYTHONUNBUFFERED=1 `
  cc-probes:ab05-1 python /research/harness/agent_probe.py --agent vashishtha `
  --scenario /research/external/causalarena/scm/semantic/data/semantic_obs_only/semantic_cybersecurity_and_it_operations_api_rate_limit_abuse_spillover__semantic_obs_only__rep000.npz `
  --shuffle-seed 20261010 --out /research/runs/ab05/vashishtha/ --model gpt-4o --agent-opt subgraph_model=gpt-4o-mini --max-calls 3501 --max-usd 1.27
```

**Exit codes.**
- **0:** ok.
- **3:** a cap was reached. The state is in `summary.json`. Rerunning the same command with a higher cap resumes and replays the earlier answers for free.
- **4:** the agent failed. `summary.json` `failure_point` gives the innermost frame and the innermost frame inside the agent repo.
- **2:** setup error, for example no key.

**Container details.**
- `-e PYTHONPATH=` clears the base image's `PYTHONPATH=/app`. Causal-Copilot also has a top-level `causal_discovery` package; the runner puts the agent first anyway, so this is belt and braces.
- `--network none` makes the stub runs provably offline.
- For the main session's `cc.ps1` command, the whole interface is `agent_probe.py --plan <file> [--stub]`.

## 7. Proposed AB-06 budget (estimate)

The estimate covers 3 arms (real, neutral and swapped names, all with shuffled columns) x 10 dev scenarios x the four agents.

**Per-run figures** are means over stub runs on the first 10 semantic dev scenarios in `plans/splits.json` order (rep000, d = 17-25), in the plan configurations.
- One scenario (`injection_molding_cooling_warp`) failed at PC for MATMCD and Vashishtha without jitter, so their means are over the 9 that ran.
- Real names are used for all arms. Neutral names are shorter, so this slightly overstates the neutral arm.

| Agent | Model(s) | Mean calls / run | Est. cost / run | Runs | Est. total |
|---|---|---|---|---|---|
| causaliq-knowledge | gpt-4o | 1 | $0.012 | 30 | $0.35 |
| PyWhy-LLM | gpt-4o | 250 | $1.017 | 30 | $30.51 |
| MATMCD | gpt-4o-mini | 986 | $0.214 | 30 | $6.43 |
| Vashishtha | gpt-4o-mini + gpt-4o tie-breaks | 1,765 | $0.666 | 30 | $19.97 |
| **Total** | | | | **120** | **$57.26** |

**Readings:**
- With the 1.5x cap margin used in AB-05, about $86 would be needed in caps.
- On gpt-4o for every role, the same grid is about **$308** (MATMCD $107, Vashishtha $170).
- PyWhy dominates the proposed total. On gpt-4o-mini its line would be about $1.83, and the total about **$29**.
- Causal-Copilot is budgeted separately in AB-06, at $0.46 per run measured.
- Recompute these figures from the first live `calls.jsonl` before approving.

## 8. Tests

`tests/test_agent_probe.py` uses stdlib unittest.
- **End to end:** it runs every importable adapter in stub mode on the first semantic file. It checks the required `summary.json` fields, the `result.json` structure and the index mapping, and that `calls.jsonl` has one record per call. It also checks that a sentinel environment key appears in no output.
- **Caps:** for each agent it checks that a call cap gives exit code 3 with state recorded, a `cap_reached` record and no traceback. It checks the USD cap and resume.
- **Scoring copy:** it checks that the copied scoring code matches `analysis/causalarena_io.py`.
- **Skipping:** an agent whose package cannot be imported is skipped, with the import error as the reason. Verified with an empty `PROBES_ROOT`: 9 tests skipped, 1 ran.

Sandbox result with `/home/claude/work/agents/venv_probe/bin/python` (CPython 3.10.20): **10 tests, OK, 106 s.**

## 9. Files

**New:**
- `harness/agent_probe.py`
- `harness/probe_llm.py`
- `harness/probe_io.py`
- `harness/agents/{vashishtha,pywhyllm,matmcd,causaliq}.py`
- `harness/agents/registry.json` (repo URLs, pinned commits, licences)
- `harness/agents/requirements_<agent>.txt` (resolved as of each repo's last commit date for Python 3.10; verified identical to what was installed)
- `plans/ab05_probe_<agent>.json`
- `plans/make_ab05_probe_plans.py`
- `docker/Dockerfile.probes`
- `tests/test_agent_probe.py`
- this report

**Unchanged:** `cc.ps1`, `Dockerfile.overlay` and every agent repository.

**Outside the kit:** the local venv is `/home/claude/work/agents/venv_probe` (per-agent `--target` folders in `probes/`, plus `tiktoken_cache/`).
