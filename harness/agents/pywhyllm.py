"""AB-05 adapter: PyWhy-LLM (py-why/pywhy-llm, MIT).

Entry point used: the README's "Modeler" flow, unchanged:
    modeler = ModelSuggester(<guidance model>)
    domain_expertises = modeler.suggest_domain_expertises(all_factors)                       # 1 call
    suggested_dag = modeler.suggest_relationships(treatment, outcome, all_factors, domain_expertises,
                                                  RelationshipStrategy.Pairwise)            # C(d,2) calls
(pywhyllm/suggesters/model_suggester.py). For the Pairwise strategy the treatment and outcome arguments are not used by
the library (model_suggester.py, suggest_relationships, Pairwise branch), so None is passed; CausalArena names none.
analysis_context (the library's documented parameter, default "causal mechanisms") is given the scenario's domain text
when there is one. The agent sees names only; it has no data interface.

Output mapping: each pair answered (A) or (B) is a committed arrow (source "llm"); (C) is no edge. The library has no
"undecided" answer, so there are no undecided pairs. With one expertise each pair is asked once.

LLM interception: no monkeypatching. ModelSuggester accepts a guidance model instance (model_suggester.py __init__);
the adapter builds guidance.models.OpenAI(model, api_key=<dummy>, echo=False, http_client=<probe gate>) - guidance passes
extra keyword arguments straight to openai.OpenAI (guidance/models/_openai.py). guidance streams (stream=True,
stream_options include_usage, logprobs) and the gate answers in the same SSE format in --stub mode.
Known agent behaviour: suggest_pairwise_relationship and suggest_domain_expertises loop `while not success` with no limit
when a reply cannot be parsed; only the probe's call cap bounds that loop. gen() is called without max_tokens.
"""

ASSUME_EXPERTISE = 200      # assumed live completion tokens (estimates, recorded per call)
ASSUME_PAIRWISE = 300


def _text(body):
    return "\n".join(str(m.get("content") or "") for m in body.get("messages") or [])


def stub_reply(body, kit):
    t = _text(body)
    if "recommending useful domain expertises" in t:
        return kit.filler(ASSUME_EXPERTISE) + "\n<domain_expertise>systems operations analysis</domain_expertise>" \
                                              "<explanation>stub</explanation>"
    if "which of the following is" in t and "<answer>" in t:
        ans = kit.rng.choices("ABC", weights=[0.2, 0.2, 0.6])[0]
        return "<thinking>" + kit.filler(ASSUME_PAIRWISE) + "</thinking>\n<answer>%s</answer>" % ans
    return kit.filler(50)


def run(ctx):
    import guidance
    from pywhyllm import RelationshipStrategy
    from pywhyllm.suggesters.model_suggester import ModelSuggester

    names = list(ctx.names)
    idx = {n: k for k, n in enumerate(names)}
    lm = guidance.models.OpenAI(ctx.model, api_key=ctx.dummy_key, echo=False, http_client=ctx.llm.http_client())
    modeler = ModelSuggester(lm)
    kw = {"analysis_context": ctx.context} if ctx.context else {}
    expertises = modeler.suggest_domain_expertises(names, **kw)
    edges = modeler.suggest_relationships(None, None, names, expertises, RelationshipStrategy.Pairwise, **kw)
    directed, src, unknown = [], {}, []
    for (a, b), cnt in edges.items():
        if a in idx and b in idx:
            directed.append((idx[a], idx[b]))
            src[(idx[a], idx[b])] = "llm"
        else:
            unknown.append([a, b])
    both = sorted({tuple(sorted(e)) for e in directed if (e[1], e[0]) in set(directed)})
    return {"directed": directed, "undirected": [], "edge_source": src,
            "provenance_exposed": "all directions come from the LLM (names only; no data interface)",
            "decision_rule": "Pairwise strategy, one expertise: (A) a->b, (B) b->a, (C) no edge",
            "notes": {"domain_expertises": expertises, "analysis_context": kw.get("analysis_context",
                                                                                 "causal mechanisms (library default)"),
                      "edges_returned": len(edges), "unmapped_edges": unknown, "pairs_with_both_directions": both}}
