"""AB-05 adapter: MATMCD (D2I-Group/matmcd, MIT), ACL 2025 Findings.

Entry point used: the first agent stage of GTdatasets_experiment.py (experiment(), "Running ConstrainAgent..."), unchanged:
    adjacency_matrix = causal_discovery(data, labels, method="pc")                       # Utils/CausalDiscovery.py
    agent = ConstrainNormalAgent(labels, theme, graph_matrix=adjacency_matrix,
                                 causal_discovery_algorithm="pc", use_reasoning=False)
    constraint_matrix = agent.run(use_cache=False, cache_path=...)                         # 2 x d(d-1) LLM calls
    final = causal_discovery(data, labels, method="pc", constraint_matrix=constraint_matrix)
i.e. the Causal Constraint Agent (CC-Agent) on a data algorithm's graph. The Data Augmentation Agent (DA-Agent: web
search via Serper/Tavily, Web_tools.collect_web_content) is NOT run: it needs search-API keys and live web content,
which this audit does not provide; the "MATMCD" and "MATMCD-R" rows of the paper use it. This is recorded as a scope
limit, not a failure. Data: the shuffled, already standardised CausalArena values (the repo standardises with
StandardScaler in Utils/data.py; re-standardising standardised data is a no-op up to ddof).

Output mapping (Utils/CausalDiscovery.py cg2matrix: M[i, j] == 1 means j -> i; -1 undirected; 2 bidirected):
committed arrows; undirected and bidirected pairs are undecided. Direction source per final arrow a -> b:
"llm" if the LLM constraint required a -> b (C[a, b] == 1) or forbade b -> a (C[b, a] == 0) - causal-learn orients by
exactly those two rules (orient_by_background_knowledge); otherwise "data". Note that edge EXISTENCE is also gated by
the LLM: a pair the LLM answered "No" in both directions is forbidden both ways and removed from the skeleton.

LLM interception: ConstrainAgent/ConstrainAgent.py imports `OpenAIClient` and `MODEL`, `OPENAI_API_KEY` from config.py at
import time and builds `OpenAIClient(OPENAI_API_KEY, MODEL)` (Client/OpenAiClient.py: `OpenAI(api_key=api_key)`, no
client parameter). The README says to put keys into config.py; instead the adapter sets the module attributes
ConstrainAgent.ConstrainAgent.MODEL / OPENAI_API_KEY (configuration, as config.py would) and replaces
ConstrainAgent.ConstrainAgent.OpenAIClient with a subclass whose only change is the constructor:
`OpenAI(api_key=<dummy>, http_client=<probe gate>)`. inquire_LLMs (prompt, temperature, parsing) is inherited unchanged.
Importing ConstrainAgent also imports Client/ReactClient.py, which sets os.environ["OPENAI_API_KEY"] = "" (line 10);
harmless here because the key lives only in the probe gate.
"""
import re

ASSUME_KNOWLEDGE = 400      # assumed live completion tokens for the free-text domain-knowledge answer (estimate)
P_YES = 0.08                # stub: share of "<Yes>" answers (random; plumbing only)


def _sys(body):
    return "\n".join(str(m.get("content") or "") for m in body.get("messages") or [] if m.get("role") == "system")


def stub_reply(body, kit):
    s = _sys(body)
    if s.startswith("You are a helpful assistant for causal inference"):
        kit.assumed_completion_tokens = 2
        return "<Yes>" if kit.rng.random() < P_YES else "<No>"
    return kit.filler(ASSUME_KNOWLEDGE)          # "You are an expert in {theme}." domain-knowledge answer


def _edges_from_cg_matrix(M):
    d = M.shape[0]
    directed, undecided = [], []
    for i in range(d):
        for j in range(i + 1, d):
            a, b = M[i, j], M[j, i]
            if a == 1 and b != 1:
                directed.append((j, i))         # M[i, j] == 1: j -> i
            elif b == 1 and a != 1:
                directed.append((i, j))
            elif a == 1 and b == 1:
                undecided.append((i, j))        # cannot happen with cg2matrix; kept for safety
            elif a in (-1, 2) or b in (-1, 2):
                undecided.append((i, j))
    return directed, undecided


def run(ctx):
    import numpy as np
    import ConstrainAgent.ConstrainAgent as CA
    from Client.OpenAiClient import OpenAIClient as _RepoOpenAIClient
    from Utils.CausalDiscovery import causal_discovery

    gate_client = ctx.llm.http_client()
    dummy = ctx.dummy_key

    class ProbeOpenAIClient(_RepoOpenAIClient):
        def __init__(self, api_key, model="gpt-4"):   # noqa: D401  only the client construction differs
            from openai import OpenAI
            self.client = OpenAI(api_key=dummy, http_client=gate_client)
            self.model = model

    CA.OpenAIClient = ProbeOpenAIClient
    CA.MODEL = ctx.model
    CA.OPENAI_API_KEY = dummy
    if "gpt" not in ctx.model:
        raise ValueError("MATMCD selects its OpenAI client only when the model name contains 'gpt' "
                         "(ConstrainAgent.py:76)")

    labels = tuple(ctx.names)
    theme = ctx.context or "the given system"
    data = np.asarray(ctx.data, dtype=float)
    prefix = sorted([a, b] for a in labels for b in labels if a != b and b.startswith(a))
    special = [n for n in labels if re.escape(n) != n]

    adj0 = causal_discovery(data, labels, method="pc")
    agent = CA.ConstrainNormalAgent(list(labels), theme, graph_matrix=adj0, causal_discovery_algorithm="pc",
                                    use_reasoning=False)
    C = agent.run(use_cache=False, cache_path=str(ctx.out / "matmcd_cache"))
    adj = causal_discovery(data, labels, method="pc", constraint_matrix=C)

    directed, undecided = _edges_from_cg_matrix(adj)
    d0, u0 = _edges_from_cg_matrix(adj0)
    src = {}
    for a, b in directed:
        src[(a, b)] = "llm" if (C[a, b] == 1 or C[b, a] == 0) else "data"
    for a, b in undecided:
        src[(a, b)] = "undecided"
    yes = int((C == 1).sum())
    both_yes = int(sum(1 for i in range(len(labels)) for j in range(i + 1, len(labels)) if C[i, j] == 1 and C[j, i] == 1))
    return {"directed": directed, "undirected": undecided, "edge_source": src,
            "provenance_exposed": "partly: the constraint matrix C is exposed, so each final arrow can be traced to an "
                                  "LLM constraint (required / reverse forbidden) or to PC alone",
            "decision_rule": "final PC with background knowledge from C (0 forbidden, 1 required, by name pattern)",
            "variants": {"pc_only_initial": {"directed": d0, "undirected": u0,
                                             "note": "the agent's own first PC run (no LLM) on the same data"}},
            "notes": {"theme": theme, "constraint_yes": yes, "constraint_pairs_yes_both_ways": both_yes,
                      "constraint_cells": int(C.size - len(labels)),
                      "name_prefix_collisions": prefix,
                      "name_prefix_note": "BackgroundKnowledge.add_*_by_pattern uses re.match (prefix match); a name "
                                          "that is a prefix of another makes a constraint apply to both "
                                          "(causallearn/utils/PCUtils/BackgroundKnowledge.py:135)",
                      "names_with_regex_metacharacters": special,
                      "scope": "CC-Agent only; DA-Agent (web search) not run",
                      "agent_quirks_seen_in_code": [
                          "ConstrainAgent/LLMs.py:174 writes 'labels[i] is the cause of labels[j]' for M[i, j] != 0, "
                          "but cg2matrix's M[i, j] == 1 means j -> i, and undirected pairs (-1) are also written as "
                          "causes: the PC graph shown to the LLM has its arrows reversed",
                          "ConstrainAgent/LLMs.py:220 builds the graph section once and caches it, so the sentence "
                          "'it seems that changes in X directly affect / do not affect Y' (lines 178-181) refers to "
                          "the first pair (labels[0], labels[1]) in every one of the d(d-1) prompts"]}}
