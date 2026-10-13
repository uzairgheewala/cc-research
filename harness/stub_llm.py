"""Offline stand-in for the OpenAI API, for DRY RUNS ONLY (zero cost, no network).

It answers every prompt with canned, structurally valid text so the whole pipeline can be exercised
end to end. Its answers carry no meaning: a stub run tests plumbing, never causal conclusions.
Run directories produced with it are labelled STUB.
"""
import json
import re
import types

STUB_MODEL = "stub-llm"
_LETTERS = "DACBDDAC"


def _edge_review(user):
    pairs = re.findall(r"^\s*\((.+?), (.+?)\): A or B or C or D: explanations", user, flags=re.M)
    lines = []
    for i, (x, y) in enumerate(pairs):
        lines.append("(%s, %s): %s: Stub explanation with no domain meaning;" % (x, y, _LETTERS[i % len(_LETTERS)]))
    return "\n".join(lines) if lines else "(a, b): D: Stub explanation;"


def respond(system, user, json_mode):
    s, u = system or "", user or ""
    if "extract the information from the query" in s:
        return json.dumps({"linearity": None, "gaussian_error": None, "alpha": None, "heterogeneous": None,
                           "domain_index": None, "selected_algorithm": None, "waiting_minutes": None,
                           "accept_CPDAG": True, "time_series": False})
    if "Please choose the algorithms that provide most reliable" in u:
        return json.dumps({"reasoning": "stub", "algorithms": [
            {"name": "PC", "description": "stub description", "justification": "stub justification"},
            {"name": "GES", "description": "stub description", "justification": "stub justification"}]})
    if "Please choose the best algorithm considering all relevant factors" in s:
        return json.dumps({"theoretical_scores": {}, "empirical_scores": {},
                           "score_calculation": {"PC": {"theoretical": 4, "empirical": 4,
                                                        "weighted_calculation": "0.7 * 4 + 0.3 * 4 = 4.0",
                                                        "final_score": 4.0}},
                           "reason": "stub reason", "algorithm": "PC"})
    if "Please select the best hyperparameters" in u:
        def p(v, n):
            return {"value": v, "full_name": n, "reasoning": "stub", "explanation": "stub"}
        return json.dumps({"hyperparameters": {"alpha": p(0.05, "Significance level"),
                                               "indep_test": p("fisherz_cpu", "Independence test"),
                                               "depth": p(-1, "Maximum depth")}})
    if "A or B or C or D: explanations" in u:
        return _edge_review(u)
    if "form a cycle" in s:
        nodes = [n.strip() for n in u.split("->") if n.strip()]
        return json.dumps({"nodes": nodes[:2]})
    if "give me the name of the given dataset" in u:
        return "Stub dataset"
    if "comprehensive domain knowledge" in u:
        return "No Knowledge"
    if json_mode:
        if '"relationships"' in s or "relationships" in s:
            return json.dumps({"relationships": []})
        if '"indicator"' in s:
            return json.dumps({"indicator": False})
        return json.dumps({})
    return "Stub response with no meaning."


class _Resp(types.SimpleNamespace):
    def model_dump(self):
        return {"id": self.id, "model": self.model, "object": "chat.completion", "system_fingerprint": None,
                "choices": [{"index": 0, "finish_reason": "stop",
                             "message": {"role": "assistant", "content": self.choices[0].message.content}}],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}, "stub": True}


def install():
    from openai.resources.chat.completions import Completions
    counter = {"n": 0}

    def create(self_, *a, **k):
        counter["n"] += 1
        msgs = k.get("messages") or []
        system = "\n".join(str(m.get("content") or "") for m in msgs if m.get("role") == "system")
        user = "\n".join(str(m.get("content") or "") for m in msgs if m.get("role") == "user")
        content = respond(system, user, json_mode=bool(k.get("response_format")))
        msg = types.SimpleNamespace(role="assistant", content=content)
        return _Resp(id="stub-%d" % counter["n"], model=STUB_MODEL,
                     choices=[types.SimpleNamespace(index=0, finish_reason="stop", message=msg)],
                     usage=types.SimpleNamespace(prompt_tokens=0, completion_tokens=0, total_tokens=0))

    Completions.create = create
