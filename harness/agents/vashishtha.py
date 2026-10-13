"""AB-05 adapter: Vashishtha et al., "Causal Order: The Key to Leveraging Imperfect Experts in Causal Inference".

Repository: Causal_Order_Imperfect_Experts (no licence shown: evaluation use only, never redistributed).
Entry point used: causal_discovery.strategies.triplet.run_triplet_experiment (the README's recommended "triplet"
strategy: one prompt per 3-variable subset, majority vote per pair, CoT tie-breaker with the expert model), then the
repository's own entropy-based cycle removal (utils/cycle_remover.remove_cycles) exactly as run_triplet.py does when
the merged graph has cycles. --agent-opt strategy=pairwise runs strategies/pairwise.run_pairwise_experiment instead.

Downstream "order-constrained discovery": the repository ships NO code for it. The paper's described use (our reading;
the paper text could not be re-checked in this session) is to take the expert causal order and use it to orient a data
algorithm's output. Implemented HERE (harness code, labelled as such): causal-learn PC (Fisher-z, alpha 0.05, the same
PC MATMCD calls) on the shuffled data; PC's committed arrows are kept (source "data"); each pair PC leaves undirected is
oriented by the LLM's partial order, i.e. a -> b if a is an ancestor of b in the acyclic LLM graph (source
"llm_order"); a pair the LLM graph does not order stays undecided. No arbitrary total order is imposed.
The LLM-only graph (after cycle removal) is reported as variant "llm_only_triplet_dag".

LLM interception: causal_discovery/utils/llm_client.py:_get_client() hard-codes `OpenAI(api_key=os.environ[...])`
(no client or base_url parameter anywhere in the call chain). Narrowest patch: the module attribute
`causal_discovery.utils.llm_client._get_client` is replaced by a function returning `openai.OpenAI(api_key=<dummy>,
http_client=<probe gate>)`. query_llm(), its retry loop, the prompts and parsing are unchanged. `delay` (a CLI
parameter of the repo, seconds of sleep before each call) is set to 0 (default here; --agent-opt delay=N).
The PC step runs before the first LLM call, so a data failure costs nothing.
Options: strategy=triplet|pairwise, subgraph_model=<model> (default --model), expert_model=<model> (default --model),
prompt_type=<pairwise prompt, default cot>, delay=0, pc_alpha=0.05.
"""
import ast
import re

DEFAULTS = {"strategy": "triplet", "delay": "0", "pc_alpha": "0.05", "prompt_type": "cot"}

# assumed live completion lengths (tokens) used to pad stub replies; ESTIMATES, recorded per call
ASSUME_SUBGRAPH = 200       # triplet prompt asks for reasoning then <Answer>; max_completion_tokens=300 in the repo
ASSUME_TIEBREAK = 220       # CoT tie-breaker, max_completion_tokens=400
ASSUME_PAIRWISE = 220


def _text(body):
    return "\n".join(str(m.get("content") or "") for m in body.get("messages") or [])


def stub_reply(body, kit):
    t = _text(body)
    rng = kit.rng
    if "create a directed acyclic graph" in t:
        m = re.findall(r"Input: (?:Nodes: )?(\[.*?\])", t)
        nodes = list(ast.literal_eval(m[-1])) if m else []
        order = nodes[:]
        rng.shuffle(order)
        edges = [(order[i], order[j]) for i in range(len(order)) for j in range(i + 1, len(order)) if rng.random() < 0.45]
        ans = "[" + ", ".join("('%s','%s')" % e for e in edges) + "]"
        return kit.filler(ASSUME_SUBGRAPH) + "\n<Answer>" + ans + "</Answer>"
    if "Which cause-and-effect relationship is more likely" in t:
        n = ASSUME_TIEBREAK if "For a causal graph used" in t else ASSUME_PAIRWISE
        return kit.filler(n) + "\nTherefore answer is <Answer>%s</Answer>" % rng.choice("ABC")
    return kit.filler(50) + "\n<Answer>C</Answer>"


def _pc(data, names, alpha):
    from causallearn.search.ConstraintBased.PC import pc
    cg = pc(data, alpha=alpha, indep_test="fisherz", node_names=list(names), show_progress=False)
    G = cg.G.graph
    d = len(names)
    directed, undirected, bidirected = [], [], []
    for i in range(d):
        for j in range(i + 1, d):
            a, b = G[i, j], G[j, i]
            if a == -1 and b == 1:
                directed.append((i, j))
            elif a == 1 and b == -1:
                directed.append((j, i))
            elif a == -1 and b == -1:
                undirected.append((i, j))
            elif a == 1 and b == 1:
                bidirected.append((i, j))
    return directed, undirected, bidirected


def run(ctx):
    import networkx as nx
    import openai
    import causal_discovery.utils.llm_client as lc
    from causal_discovery.utils.cycle_remover import remove_cycles

    o = dict(DEFAULTS, **ctx.opts)
    sub_model = o.get("subgraph_model", ctx.model)
    exp_model = o.get("expert_model", ctx.model)
    client = openai.OpenAI(api_key=ctx.dummy_key, http_client=ctx.llm.http_client())
    lc._get_client = lambda: client                        # the one monkeypatch (see module docstring)

    names = list(ctx.names)
    idx = {n: k for k, n in enumerate(names)}
    context = ("model the relation between various variables in %s" % ctx.context) if ctx.context \
        else "model the relation between the given variables"
    graph_config = {"nodes": names, "ground_truth_edges": [], "descriptions": None, "context": context}
    notes = {"context_sentence": context, "subgraph_model": sub_model, "expert_model": exp_model,
             "strategy": o["strategy"], "delay": int(o["delay"])}

    # the data step runs FIRST, so a data failure (e.g. a singular correlation matrix on a formula file) stops the
    # probe before any LLM call is paid for
    pc_dir, pc_und, pc_bi = _pc(ctx.data, names, float(o["pc_alpha"]))

    if o["strategy"] == "triplet":
        from causal_discovery.strategies.triplet import run_triplet_experiment
        r = run_triplet_experiment(graph_config=graph_config, subgraph_model=sub_model, expert_model=exp_model,
                                   delay=int(o["delay"]))
        predicted, edgewise = r["predicted_edges"], r["edgewise_dist"]
        n_cycles = len(list(nx.simple_cycles(nx.DiGraph(predicted)))) if predicted else 0
        notes.update({"subgroups": len(r["subgroup_list"]), "merged_edges": len(predicted), "merged_cycles": n_cycles})
        if n_cycles > 0 and edgewise:                       # as run_triplet.py main(): cycle removal only if cycles
            acyclic, thr, _ = remove_cycles(predicted, edgewise)
            notes["cycle_removal_threshold"] = thr
        else:
            acyclic = list(predicted)
        notes["llm_dag_edges"] = len(acyclic)
    elif o["strategy"] == "pairwise":
        from causal_discovery.strategies.pairwise import run_pairwise_experiment
        r = run_pairwise_experiment(graph_config=graph_config, prompt_type=o["prompt_type"], model=exp_model,
                                    delay=int(o["delay"]))
        acyclic = list(r["predicted_edges"])
        G0 = nx.DiGraph(acyclic)
        notes["pairwise_cycles"] = len(list(nx.simple_cycles(G0))) if acyclic else 0
        if notes["pairwise_cycles"]:
            notes["pairwise_order_note"] = "pairwise graph has cycles: no valid order; ancestors are taken from the " \
                                           "graph as returned, so pairs on a cycle are left undecided"
    else:
        raise ValueError("strategy must be triplet or pairwise")

    llm_dir = [(idx[a], idx[b]) for a, b in acyclic if a in idx and b in idx]
    G = nx.DiGraph()
    G.add_nodes_from(range(len(names)))
    G.add_edges_from(llm_dir)
    anc = {v: nx.ancestors(G, v) for v in G.nodes}

    def order(i, j):                                      # +1: i before j, -1: j before i, 0: not ordered / cycle
        ij, ji = i in anc[j], j in anc[i]
        return 1 if ij and not ji else (-1 if ji and not ij else 0)

    directed, undecided, src = [], [], {}
    agree = {"consistent": 0, "contradicts": 0, "not_ordered": 0}
    for i, j in pc_dir:
        directed.append((i, j))
        src[(i, j)] = "data"
        oo = order(i, j)
        agree["consistent" if oo == 1 else ("contradicts" if oo == -1 else "not_ordered")] += 1
    for i, j in pc_und + pc_bi:
        oo = order(i, j)
        if oo == 1:
            directed.append((i, j))
            src[(i, j)] = "llm_order"
        elif oo == -1:
            directed.append((j, i))
            src[(j, i)] = "llm_order"
        else:
            undecided.append((i, j))
            src[(i, j)] = "undecided_no_llm_order"
    notes.update({"pc_directed": len(pc_dir), "pc_undirected": len(pc_und), "pc_bidirected": len(pc_bi),
                  "pc_arrows_vs_llm_order": agree,
                  "downstream_step": "harness implementation (not in the repository): PC CPDAG, undirected pairs "
                                     "oriented by the LLM DAG's ancestor relation"})
    return {"directed": directed, "undirected": undecided, "edge_source": src,
            "provenance_exposed": "yes: PC-compelled arrows (data) vs arrows oriented by the LLM order (llm_order)",
            "decision_rule": "PC CPDAG; undirected pair a-b -> a->b iff a is an ancestor of b in the acyclic LLM graph",
            "variants": {"llm_only_triplet_dag" if o["strategy"] == "triplet" else "llm_only_pairwise":
                         {"directed": llm_dir, "undirected": [], "note": "the agent's LLM graph alone (after cycle "
                                                                        "removal for triplet)"},
                         "pc_only": {"directed": pc_dir, "undirected": pc_und + pc_bi,
                                     "note": "causal-learn PC alone on the same shuffled data (data floor)"}},
            "notes": notes}
