"""BND-11 names part: ask the model the prepared direction questions (plans/bnd11_names_requests.jsonl). Run by Uzair only.

  python /research/harness/names_runner.py --requests /research/plans/bnd11_names_requests.jsonl \
         --out /research/plans/results/bnd11_names_answers.jsonl [--stub]

Each request is one short chat call (temperature 0, max 30 tokens). The reply must be exactly the JSON
{"direction": "A->B" | "B->A" | "unknown"}; otherwise the question is asked once more with a reminder; a second invalid reply
is recorded as an abstention (direction null). Nothing raises on a bad reply (CAP-10). Every raw reply, the served model,
the token usage and timing are written per request. Resumable: requests already in --out are skipped.
--stub answers offline (no key, no network, no cost) with a deterministic pattern that also injects malformed replies, so
the retry and abstention paths are exercised before any live call.
The key is read the way the pipeline reads it (python-dotenv on /app/.env; real environment variables win); it is never printed.
"""
import argparse
import hashlib
import json
import os
import sys
import time
import zlib
from pathlib import Path

VALID = {"A->B", "B->A", "unknown"}
REMINDER = " Reply with the JSON object only, exactly as asked, with no other text."


def parse_reply(text):
    """Same rule as analysis/refinement_v2.py parse_reply (kept in step by tests/test_refinement_v2.py)."""
    try:
        d = json.loads(text)
    except (TypeError, ValueError):
        return None
    if not isinstance(d, dict) or set(d) != {"direction"} or d["direction"] not in VALID:
        return None
    return d["direction"]


def stub_reply(rid, attempt):
    h = zlib.crc32(rid.encode())
    if attempt == 0 and h % 50 == 0:
        return "I think A causes B."                      # malformed first answer: exercises the retry
    if h % 200 == 1:
        return '{"direction": "maybe"}'                   # malformed twice: exercises the abstention
    return json.dumps({"direction": ["A->B", "B->A", "unknown"][h % 3]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--requests", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stub", action="store_true")
    ap.add_argument("--model", default=None, help="default: LLM_MODEL from the environment / .env, else gpt-4o")
    ap.add_argument("--max-calls", type=int, default=None, help="hard cap on API calls in this session (default 2 x requests)")
    a = ap.parse_args()
    reqs = [json.loads(l) for l in open(a.requests, encoding="utf-8")]
    req_sha = hashlib.sha256(Path(a.requests).read_bytes()).hexdigest()
    out = Path(a.out)
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
    model = a.model or os.environ.get("LLM_MODEL") or "gpt-4o"
    cap = a.max_calls or 2 * len(reqs)
    calls, ptok, ctok, invalid_total = 0, 0, 0, 0
    print("[names] %d requests (%d already answered), model %s%s, request file sha256 %s"
          % (len(reqs), len(done), model, " (STUB)" if a.stub else "", req_sha[:16]), flush=True)
    with open(out, "a", encoding="utf-8") as fh:
        for r in reqs:
            if r["id"] in done:
                continue
            attempts, direction, invalid = [], None, 0
            for attempt in (0, 1):
                if calls >= cap:
                    print("[names] call cap %d reached; stopping (rerun to continue)" % cap)
                    return 3
                prompt = r["prompt"] + (REMINDER if attempt else "")
                t = time.time()
                if a.stub:
                    text, served, usage = stub_reply(r["id"], attempt), "stub", {}
                else:
                    try:
                        resp = client.chat.completions.create(model=model, temperature=0, max_tokens=30,
                                                              messages=[{"role": "user", "content": prompt}])
                        text = resp.choices[0].message.content
                        served = resp.model
                        usage = {"prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens}
                    except Exception as e:  # noqa: BLE001  an API error is recorded like an invalid reply, never raised
                        text, served, usage = None, None, {"error": "%s: %s" % (type(e).__name__, str(e)[:200])}
                calls += 1
                ptok += usage.get("prompt_tokens", 0)
                ctok += usage.get("completion_tokens", 0)
                attempts.append({"attempt": attempt, "reply": text, "served_model": served, "usage": usage,
                                 "seconds": round(time.time() - t, 2)})
                direction = parse_reply(text)
                if direction is not None:
                    break
                invalid += 1
            invalid_total += invalid
            rec = {k: r[k] for k in ("id", "run", "arm", "role", "family", "a", "b", "paraphrase")}
            rec.update({"direction": direction, "abstained": direction is None, "invalid_replies": invalid,
                        "attempts": attempts, "requests_sha256": req_sha, "stub": a.stub})
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
    print("[names] done: %d calls, %d invalid replies, tokens %d prompt + %d completion" % (calls, invalid_total, ptok, ctok))
    return 0


if __name__ == "__main__":
    sys.exit(main())
