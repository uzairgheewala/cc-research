"""AB-05 (AUD-37) close-out: live probe calls against the stub's estimates, per agent and call kind. No model calls.

  python analysis/ab05_live_calibration.py [--out analysis/results/ab05]

Reads runs/ab05/<agent>/calls.jsonl (live, Uzair's runs of 13 Oct) and runs/ab05/stub_plan/<agent>/calls.jsonl (the stub
run of the same plan: same scenario, same shuffle). For every call kind it reports count, mean prompt and completion
tokens, mean seconds, finish reasons and served models, and the live/stub ratios that plans/calibrate_ab06.py uses.

Two agent-specific measurements:
  Vashishtha et al.  share of triplet answers that carry no <Answer> tag (the repo parses only tagged answers:
                     utils/helpers.py parse_answer_tag; an untagged answer becomes "[]" and casts no vote), and the number
                     of tie-breaker calls the run needs, recomputed from the live answers with the repository's own merge
                     rule (strategies/triplet.py merge_triplet_votes: a pair is a tie when two or three of
                     {A->B, B->A, no connection} share the top count; a "[]" answer counts for none of them).
  MATMCD             calls left after the cap (2 x d(d-1) is fixed by the code) and their cost at live means.
Writes <out>/live_calibration.json.
"""
import argparse, ast, collections, itertools, json, re, statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICES = {"gpt-4o-mini": (0.15, 0.60), "gpt-4o": (2.50, 10.00)}


def price(model):
    m = (model or "").replace("stub:", "")
    return PRICES["gpt-4o-mini"] if m.startswith("gpt-4o-mini") else PRICES["gpt-4o"]


def text_of(body):
    out = []
    for m in body.get("messages") or []:
        c = m.get("content")
        if isinstance(c, list):
            c = "".join(p.get("text", "") for p in c if isinstance(p, dict))
        out.append(str(c or ""))
    return "\n".join(out)


def system_of(body):
    for m in body.get("messages") or []:
        if m.get("role") == "system":
            c = m.get("content")
            if isinstance(c, list):
                c = "".join(p.get("text", "") for p in c if isinstance(p, dict))
            return str(c or "")
    return ""


def kind(agent, body):
    t, s = text_of(body), system_of(body)
    if agent == "vashishtha":
        if "create a directed acyclic graph" in t:
            return "triplet"
        if "Which cause-and-effect relationship is more likely" in t:
            return "tiebreak"
        return "other"
    if agent == "matmcd":
        if s.startswith("You are a helpful assistant for causal inference"):
            return "constraint_yes_no"
        if s.startswith("You are an expert in"):
            return "domain_knowledge"
        return "other"
    if agent == "pywhyllm":
        return "context" if "helpful assistant for r" in s[:40] else "pair"
    return "single"


def load(path):
    if not Path(path).exists():
        return []
    return [r for r in (json.loads(l) for l in open(path, encoding="utf-8") if l.strip()) if "request" in r]


def summarise(agent, calls):
    by = collections.defaultdict(list)
    for r in calls:
        by[kind(agent, r["request"])].append(r)
    out = {}
    for k, rs in sorted(by.items()):
        u = [r.get("usage") or {} for r in rs]
        out[k] = {"calls": len(rs),
                  "prompt_mean": round(st.mean(x.get("prompt_tokens", 0) for x in u), 1),
                  "completion_mean": round(st.mean(x.get("completion_tokens", 0) for x in u), 1),
                  "completion_max": max(x.get("completion_tokens", 0) for x in u),
                  "seconds_mean": round(st.mean(r.get("seconds") or 0 for r in rs), 3),
                  "max_completion_tokens": sorted({str(r["request"].get("max_completion_tokens") or r["request"].get("max_tokens")) for r in rs}),
                  "temperature": sorted({str(r["request"].get("temperature")) for r in rs}),
                  "finish": dict(collections.Counter(str(r.get("finish_reason")) for r in rs)),
                  "requested_models": dict(collections.Counter(str(r.get("requested_model")) for r in rs)),
                  "served_models": dict(collections.Counter(str(r.get("served_model")) for r in rs)),
                  "usd": round(sum(r.get("usd") or 0 for r in rs), 6)}
    return out


def parse_answer_tag(text):                      # the repository's rule (utils/helpers.py), copied
    if text is None:
        return None
    m = re.search(r"<Answer>(.*?)</Answer>", text)
    return m.group(1).strip() if m else None


def str_2_lst(s):                                # utils/helpers.py
    lst = ast.literal_eval(s)
    return [e if isinstance(e, tuple) else (e,) for e in lst]


def vashishtha_votes(calls):
    tri = {}
    for r in calls:
        t = text_of(r["request"])
        if "create a directed acyclic graph" in t:
            nodes = ast.literal_eval(re.findall(r"Input: (?:Nodes: )?(\[.*?\])", t)[-1])
            tri[tuple(nodes)] = r.get("response_text")
    order = []
    for g in tri:
        for n in g:
            if n not in order:
                order.append(n)
    parsed, untagged, unparseable = {}, 0, 0
    for g, txt in tri.items():
        a = parse_answer_tag(txt)
        if a is None:
            untagged += 1
            a = "[]"
        try:
            parsed[g] = str_2_lst(a)
        except (ValueError, SyntaxError):
            unparseable += 1
            parsed[g] = None
    ties = novote = 0
    for x, y in itertools.combinations(order, 2):
        xy = yx = ind = 0
        for g, e in parsed.items():
            if e is None or x not in g or y not in g:
                continue
            xy += (x, y) in e
            yx += (y, x) in e
            if [i for i in e if (x, y) not in e and (y, x) not in e]:
                ind += 1
        top = max(xy, yx, ind)
        ties += [xy, yx, ind].count(top) > 1
        novote += (xy + yx + ind) == 0
    p = len(order) * (len(order) - 1) // 2
    return {"triplets": len(tri), "variables": len(order), "pairs": p,
            "answers_without_tag": untagged, "share_without_tag": round(untagged / max(1, len(tri)), 4),
            "answers_unparseable": unparseable,
            "pairs_tied": ties, "share_pairs_tied": round(ties / max(1, p), 4), "pairs_with_no_vote": novote,
            "note": "a pair is sent to the gpt-4o tie-breaker when tied; untagged answers cast no vote, so truncation "
                    "turns votes into tie-breaker calls"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "analysis" / "results" / "ab05"))
    a = ap.parse_args()
    res = {"ticket": "AUD-37 / AB-05", "producer": "analysis/ab05_live_calibration.py", "agents": {}}
    for agent in ("causaliq", "pywhyllm", "matmcd", "vashishtha"):
        live = load(ROOT / "runs" / "ab05" / agent / "calls.jsonl")
        stub = load(ROOT / "runs" / "ab05" / "stub_plan" / agent / "calls.jsonl")
        summ = json.loads((ROOT / "runs" / "ab05" / agent / "summary.json").read_text(encoding="utf-8"))
        A = {"status": summ["status"], "calls": summ["calls"], "usd_live": summ["est_usd_at_served_prices"],
             "wall_seconds": summ["wall_seconds"], "f1": summ.get("directed_f1_random_rule"),
             "caps": summ.get("caps"), "live": summarise(agent, live), "stub": summarise(agent, stub), "ratios": {}}
        for k, L in A["live"].items():
            S = A["stub"].get(k)
            if S:
                A["ratios"][k] = {"calls_live_over_stub": round(L["calls"] / S["calls"], 4),
                                  "prompt_live_over_stub": round(L["prompt_mean"] / max(1e-9, S["prompt_mean"]), 4),
                                  "completion_live_over_stub": round(L["completion_mean"] / max(1e-9, S["completion_mean"]), 4)}
        if agent == "vashishtha":
            V = vashishtha_votes(live)
            V["stub"] = vashishtha_votes(stub)
            tb = A["live"].get("tiebreak", {})
            left = V["pairs_tied"] - tb.get("calls", 0)
            pi, po = PRICES["gpt-4o"]
            V["tiebreak_calls_left"] = left
            V["usd_to_finish"] = round(left * (tb.get("prompt_mean", 0) * pi + tb.get("completion_mean", 0) * po) / 1e6, 4)
            V["usd_full_run"] = round(A["usd_live"] + V["usd_to_finish"], 4)
            A["vashishtha"] = V
        if agent == "matmcd":
            d = summ["variables"]
            need = 2 * d * (d - 1)
            K = A["live"]
            per = {k: (v["prompt_mean"] * PRICES["gpt-4o-mini"][0] + v["completion_mean"] * PRICES["gpt-4o-mini"][1]) / 1e6 for k, v in K.items()}
            left_kn = d * (d - 1) - K.get("domain_knowledge", {}).get("calls", 0)
            left_yn = d * (d - 1) - K.get("constraint_yes_no", {}).get("calls", 0)
            A["matmcd"] = {"calls_by_code": need, "domain_knowledge_left": left_kn, "yes_no_left": left_yn,
                           "usd_to_finish": round(left_kn * per.get("domain_knowledge", 0) + left_yn * per.get("constraint_yes_no", 0), 4)}
            A["matmcd"]["usd_full_run"] = round(A["usd_live"] + A["matmcd"]["usd_to_finish"], 4)
        res["agents"][agent] = A
    Path(a.out).mkdir(parents=True, exist_ok=True)
    (Path(a.out) / "live_calibration.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    for agent, A in res["agents"].items():
        print(agent, A["status"], "calls", A["calls"], "usd %.4f" % A["usd_live"], "wall %.0fs" % A["wall_seconds"])
        for k, L in A["live"].items():
            print("   live %-18s n=%-5d pt=%-7s ct=%-6s s=%-6s finish=%s ratios=%s" % (k, L["calls"], L["prompt_mean"], L["completion_mean"], L["seconds_mean"], L["finish"], A["ratios"].get(k)))
        for x in ("vashishtha", "matmcd"):
            if x in A:
                print("   ", json.dumps({k: v for k, v in A[x].items() if k != "stub"}))
    if "vashishtha" in res["agents"]:
        print("    stub votes:", json.dumps(res["agents"]["vashishtha"]["vashishtha"]["stub"]))


if __name__ == "__main__":
    main()
