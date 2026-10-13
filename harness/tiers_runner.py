"""AB-07 / A3 (DEC-02): ask the model for tiers over shown variable names (plans/a3_tiers_requests.jsonl). Run by Uzair only.

  python /research/harness/tiers_runner.py --requests /research/plans/a3_tiers_requests.jsonl \
         --prereg /research/plans/a3_prereg.json --out /research/plans/results/a3_tiers_answers.jsonl [--stub]

Each request is one chat call (temperature 0, max_tokens from the pre-registration). A valid reply is exactly
{"tiers": [[name, ...], ...]} containing every shown name exactly once (surrounding whitespace ignored). Otherwise the
question is asked once more with a reminder naming the problem; a second invalid reply is an abstention (tiers null).
Nothing raises on a bad reply. Every raw reply, the served model, token usage and timing are written per request.
Resumable: requests already in --out are skipped. Live runs refuse to start unless the request file's sha256 equals the
pre-registration's (thresholds and prompts were fixed before the calls).
--stub answers offline (no key, no network, no cost) with a deterministic pattern that includes malformed replies, so the
retry and abstention paths run before any live call.
The key is read the way the pipeline reads it (python-dotenv on /app/.env; real environment variables win); never printed.
"""
import argparse, hashlib, json, os, sys, time, zlib
from pathlib import Path

REMINDER = ("\n\nYour previous reply could not be used: {problem}. Reply with the JSON object only, "
            "{{\"tiers\": [[...], ...]}}, containing every listed name exactly once, spelled exactly as listed.")


def parse_reply(text, names):
    """-> (tiers as list of lists, None) or (None, problem)."""
    if text is None:
        return None, "no reply"
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`")
        t = t[t.find("{"):] if "{" in t else t
    try:
        d = json.loads(t)
    except (TypeError, ValueError):
        return None, "not valid JSON"
    if not isinstance(d, dict) or set(d) != {"tiers"} or not isinstance(d["tiers"], list) or not d["tiers"]:
        return None, "the object must have exactly one key, tiers, holding a non-empty list"
    seen, tiers = [], []
    for tier in d["tiers"]:
        if not isinstance(tier, list) or not all(isinstance(x, str) for x in tier):
            return None, "every tier must be a list of names"
        tiers.append([x.strip() for x in tier if x.strip()])
        seen += tiers[-1]
    want = set(names)
    missing, extra = want - set(seen), set(seen) - want
    dup = len(seen) != len(set(seen))
    if missing or extra or dup:
        return None, "missing %d, unknown %d, duplicated %s" % (len(missing), len(extra), dup)
    return [t for t in tiers if t], None


def stub_reply(rid, names, attempt):
    h = zlib.crc32(rid.encode())
    if attempt == 0 and h % 40 == 0:
        return "Here are the tiers: inputs first."                       # malformed: exercises the retry
    if h % 150 == 1:
        return json.dumps({"tiers": [names[:-1]]})                        # missing a name twice: exercises the abstention
    k = 1 + h % 4
    order = sorted(names, key=lambda n: zlib.crc32((rid + n).encode()))
    return json.dumps({"tiers": [order[i::k] for i in range(k)]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--requests", required=True)
    ap.add_argument("--prereg", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stub", action="store_true")
    ap.add_argument("--model", default=None, help="default: the pre-registered model")
    ap.add_argument("--max-calls", type=int, default=None, help="hard cap on API calls in this session (default: pre-registered cap)")
    a = ap.parse_args()
    raw = Path(a.requests).read_bytes()
    req_sha = hashlib.sha256(raw).hexdigest()
    pre = json.load(open(a.prereg, encoding="utf-8"))
    if req_sha != pre["requests_sha256"]:
        msg = "request file sha256 %s.. does not match the pre-registration %s.." % (req_sha[:12], pre["requests_sha256"][:12])
        if not a.stub:
            sys.exit("ABORTED: " + msg)
        print("[tiers] warning (stub): " + msg)
    reqs = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {json.loads(l)["id"] for l in open(out, encoding="utf-8") if l.strip()}
    client = None
    if not a.stub:
        from dotenv import load_dotenv
        load_dotenv("/app/.env")
        if not os.environ.get("OPENAI_API_KEY") or os.environ["OPENAI_API_KEY"].startswith("stub"):
            sys.exit("ABORTED: no OPENAI_API_KEY in the environment or /app/.env")
        from openai import OpenAI
        client = OpenAI()
    model = a.model or pre["model"]
    cap = a.max_calls or pre["call_cap"]
    calls, ptok, ctok, invalid_total, abstained = 0, 0, 0, 0, 0
    print("[tiers] %d requests (%d already answered), model %s%s, request file sha256 %s, call cap %d"
          % (len(reqs), len(done), model, " (STUB)" if a.stub else "", req_sha[:16], cap), flush=True)
    with open(out, "a", encoding="utf-8") as fh:
        for r in reqs:
            if r["id"] in done:
                continue
            attempts, tiers, problem = [], None, None
            for attempt in (0, 1):
                if calls >= cap:
                    print("[tiers] call cap %d reached; stopping (rerun to continue)" % cap)
                    return 3
                prompt = r["prompt"] + (REMINDER.format(problem=problem) if attempt else "")
                t = time.time()
                if a.stub:
                    text, served, usage = stub_reply(r["id"], r["names_shown"], attempt), "stub", {}
                else:
                    try:
                        resp = client.chat.completions.create(model=model, temperature=pre.get("temperature", 0),
                                                              max_tokens=pre.get("max_tokens", 1500),
                                                              messages=[{"role": "user", "content": prompt}])
                        text, served = resp.choices[0].message.content, resp.model
                        usage = {"prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens}
                    except Exception as e:  # noqa: BLE001 - an API error is recorded like an invalid reply, never raised
                        text, served, usage = None, None, {"error": "%s: %s" % (type(e).__name__, str(e)[:200])}
                calls += 1
                ptok += usage.get("prompt_tokens", 0)
                ctok += usage.get("completion_tokens", 0)
                attempts.append({"attempt": attempt, "reply": text, "served_model": served, "usage": usage,
                                 "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "seconds": round(time.time() - t, 2)})
                tiers, problem = parse_reply(text, r["names_shown"])
                if tiers is not None:
                    break
                invalid_total += 1
            abstained += tiers is None
            rec = {k: r[k] for k in ("id", "family", "scenario", "arm", "phrasing", "split")}
            rec.update({"tiers": tiers, "abstained": tiers is None, "last_problem": problem if tiers is None else None,
                        "attempts": attempts, "requests_sha256": req_sha, "stub": a.stub, "model_requested": model})
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
    usd = ptok / 1e6 * 2.5 + ctok / 1e6 * 10.0
    print("[tiers] done: %d calls, %d invalid replies, %d abstentions, tokens %d prompt + %d completion (~$%.2f at gpt-4o list)"
          % (calls, invalid_total, abstained, ptok, ctok, usd))
    return 0


if __name__ == "__main__":
    sys.exit(main())
