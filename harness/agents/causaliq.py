"""AB-05 adapter: causaliq-knowledge (Kitson & Constantinou, CausalIQ; MIT).

Entry point used: the library's graph generation, as its CLI does it (cli/generate.py, `cqknow generate-graph`):
    GraphGenerator(model="openai/<model>", config=GraphGeneratorConfig(...), cache=None)
        .generate_pdg_from_context(NetworkContext, level=PromptDetail.STANDARD)          # ONE LLM call per graph
-> a PDG with P(forward), P(backward), P(undirected), P(none) per pair (graph/generator.py, graph/response.py).
The README's Quick Start (`causaliq_knowledge.llm.LLMKnowledge(...).query_edge(a, b)`) no longer exists in the code at
the pinned commit (no LLMKnowledge class anywhere under src/); graph generation is the current knowledge query API.
Config follows the CLI defaults (temperature 0.1, timeout 120 s, prompt detail "standard", LLM names; max_tokens is the
GraphGeneratorConfig default 2000, which the CLI does not override). The variables are given as NetworkContext
VariableSpec(name=<shown name>, type="continuous") with no descriptions; domain = the scenario's domain text
(network id is the neutral string "scenario"). Names only; the package has no data interface (data fusion is planned
for causaliq-discovery).

Decision rule: PDG most_likely_state per pair (causaliq_core PDG.EdgeProbabilities.most_likely_state, the state the
CLI prints): forward / backward -> committed arrow (source "llm"); undirected -> undecided; none -> no edge. Harness
choice, documented: an exact tie between forward and backward (orientation 0.5, the prompt's "uncertain") is treated
as undecided instead of taking most_likely_state's first key, so that no direction comes from JSON key order.
The library's own greedy DAG (PDG.to_dag_greedy) is reported as a variant.

LLM interception: OpenAIClient has no client or base-URL parameter; llm/openai_compat_client.py:completion() opens
`httpx.Client(timeout=...)` and posts to the class constant BASE_URL. Narrowest patch: the module attribute
`causaliq_knowledge.llm.openai_compat_client.httpx` is replaced by a namespace identical to httpx except that `Client`
returns an httpx.Client on the probe gate's transport. Payload, headers, parsing and error handling are unchanged.
OPENAI_API_KEY seen by the package is the dummy (OpenAIConfig requires one).
"""
import json
import types

ASSUME_EDGES_PER_VAR = 1.3     # stub: number of proposed edges = 1.3 x variables (estimate of a live answer's length)


def _text(body):
    return "\n".join(str(m.get("content") or "") for m in body.get("messages") or [])


def stub_reply(body, kit):
    t = "\n".join(str(m.get("content") or "") for m in body.get("messages") or [] if m.get("role") == "user")
    names = []
    for line in t.splitlines():
        if line.startswith("- "):
            names.append(line[2:].strip())
    rng = kit.rng
    k = int(round(ASSUME_EDGES_PER_VAR * len(names)))
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
    rng.shuffle(pairs)
    edges = []
    for a, b in pairs[:k]:
        if rng.random() < 0.5:
            a, b = b, a
        edges.append({"source": a, "target": b, "existence": round(rng.uniform(0.5, 0.95), 2),
                      "orientation": rng.choice([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])})
    out = json.dumps({"edges": edges})
    kit.assumed_completion_tokens = kit.counter.count(out)
    return out


def run(ctx):
    import httpx
    import causaliq_knowledge.llm.openai_compat_client as occ
    from causaliq_knowledge.graph.generator import GraphGenerator, GraphGeneratorConfig
    from causaliq_knowledge.graph.models import NetworkContext, VariableSpec
    from causaliq_knowledge.graph.view_filter import PromptDetail

    transport = ctx.llm.transport()
    shim = types.SimpleNamespace(**{k: getattr(httpx, k) for k in dir(httpx) if not k.startswith("__")})
    shim.Client = lambda *a, **kw: httpx.Client(*a, transport=transport, **kw)
    occ.httpx = shim                                       # the one monkeypatch (see module docstring)

    names = list(ctx.names)
    idx = {n: k for k, n in enumerate(names)}
    nc = NetworkContext(network="scenario", domain=ctx.context or "unspecified",
                        variables=[VariableSpec(name=n, type="continuous") for n in names])
    cfg = GraphGeneratorConfig(prompt_detail=PromptDetail.STANDARD, use_llm_names=True, request_id="ab05")
    gen = GraphGenerator(model="openai/" + ctx.model, config=cfg, cache=None)
    res = gen.generate_pdg_from_context(nc, level=PromptDetail.STANDARD)
    pdg = res.pdg

    directed, undecided, src, ties = [], [], {}, 0
    for a, b, p in pdg.existing_edges():
        if a not in idx or b not in idx:
            continue
        state = p.most_likely_state()
        if state in ("forward", "backward") and abs(p.forward - p.backward) < 1e-12 and p.forward >= max(p.undirected, p.none):
            state = "undirected"
            ties += 1
        if state == "forward":
            directed.append((idx[a], idx[b]))
            src[(idx[a], idx[b])] = "llm"
        elif state == "backward":
            directed.append((idx[b], idx[a]))
            src[(idx[b], idx[a])] = "llm"
        elif state == "undirected":
            undecided.append((idx[a], idx[b]))
            src[(idx[a], idx[b])] = "llm_undecided"
    variants = {}
    try:
        g = pdg.to_dag_greedy()
        dag = getattr(g, "dag", None) or g[0]
        ed = []
        for e in getattr(dag, "edges", {}) or {}:
            s, t = (e[0], e[1]) if isinstance(e, tuple) else (getattr(e, "source", None), getattr(e, "target", None))
            if s in idx and t in idx:
                ed.append((idx[s], idx[t]))
        variants["library_greedy_dag"] = {
            "directed": ed, "undirected": [],
            "note": "PDG.to_dag_greedy(): %s edges, %s skipped for cycles, %s alphabetical tie-breaks (a direction "
                    "taken from name order)" % (getattr(g, "edges_included", "?"), getattr(g, "edges_skipped_cycle", "?"),
                                                getattr(g, "tie_breaks_applied", "?"))}
    except Exception as e:  # noqa: BLE001  variant only; record why it is missing
        variants["library_greedy_dag_error"] = {"directed": [], "undirected": [], "note": "%s: %s" % (type(e).__name__, e)}
    md = res.metadata
    return {"directed": directed, "undirected": undecided, "edge_source": src, "variants": variants,
            "provenance_exposed": "all from the LLM (names only); per-pair probabilities exposed in the PDG",
            "decision_rule": "PDG most_likely_state per pair; exact forward/backward ties -> undecided",
            "notes": {"pdg_pairs_with_existence": len(list(pdg.existing_edges())), "orientation_ties": ties,
                      "finish_reason": getattr(md, "finish_reason", None), "max_tokens": cfg.max_tokens,
                      "library_reported_tokens": [getattr(md, "input_tokens", None), getattr(md, "output_tokens", None)],
                      "domain": nc.domain}}
