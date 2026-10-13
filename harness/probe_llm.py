"""AB-05 (AUD-37) LLM interception for the agent probes: one counting gate for every chat call.

Every agent's HTTP traffic to the chat-completions endpoint is routed through ProbeLLM.transport(), an httpx transport.
The adapters hand it to the agent's own client (openai.OpenAI(http_client=...), guidance.models.OpenAI(http_client=...),
or the httpx module used by causaliq-knowledge), so the agent's request building, retries and parsing are untouched.

What the gate does for every request:
  * enforces --max-calls and --max-usd BEFORE a new call is sent (raises CapReached, a BaseException, so no agent-side
    `except Exception` retry loop can swallow it; the runner records the state and exits cleanly);
  * --stub: answers offline with the adapter's deterministic fake in the format that agent parses (JSON or SSE stream);
  * live: forwards the unchanged request body to https://api.openai.com/v1/chat/completions with the real key, which
    only this object holds (the agent process sees a dummy key; OPENAI_BASE_URL points at a dead local port so an
    un-intercepted client fails fast instead of spending);
  * appends one record per request to calls.jsonl: request body, prompt sha256, served model, usage, seconds, cost.
  * resumable: a rerun into the same --out replays earlier successful responses for identical requests (free, marked
    "replayed") and continues with new calls; the caps apply to the whole logical run, replayed calls included.

Token counts in --stub mode are counted locally (tiktoken o200k_base when available, else characters/4; the counter used
is recorded), and stub completions are padded to an assumed length per call type (set by the adapter, recorded per call),
so stub-mode cost is an ESTIMATE of a live run, never a measurement.
"""
import collections
import hashlib
import json
import os
import random
import threading
import time
from pathlib import Path

import httpx

UPSTREAM_URL = "https://api.openai.com/v1/chat/completions"
DUMMY_KEY = "sk-probe-intercepted-not-a-key"
DEAD_BASE_URL = "http://127.0.0.1:9/v1"

# USD per 1M tokens (input, output). List prices; prefix match, more specific first.
PRICES = collections.OrderedDict([
    ("gpt-4o-mini", (0.15, 0.60)),
    ("gpt-4o", (2.50, 10.00)),
    ("gpt-4.1-mini", (0.40, 1.60)),
    ("gpt-4.1", (2.00, 8.00)),
])
GPT4O = (2.50, 10.00)


def price_for(model):
    m = (model or "").lower()
    for k, v in PRICES.items():
        if m.startswith(k):
            return v, False
    return GPT4O, True          # unknown model: priced as gpt-4o, flagged


def usd(prompt_tokens, completion_tokens, prices):
    return prompt_tokens / 1e6 * prices[0] + completion_tokens / 1e6 * prices[1]


class CapReached(BaseException):
    """A call or spending cap was reached. BaseException on purpose: agent code retries on `except Exception`."""

    def __init__(self, reason, state):
        super().__init__(reason)
        self.reason = reason
        self.state = state


class TokenCounter:
    """o200k_base (gpt-4o's tokenizer) if tiktoken can load it; else cl100k_base (gpt-4's; tiktoken verifies the file's
    sha256 against its own pin) if it is in the local tiktoken cache; else characters / 4. The name used is recorded."""

    def __init__(self, prefer=("o200k_base", "cl100k_base")):
        self.name = "chars/4"
        self._enc = None
        try:
            import tiktoken
        except Exception:  # noqa: BLE001
            return
        for enc in prefer:
            try:
                self._enc = tiktoken.get_encoding(enc)
                self.name = "tiktoken:" + enc
                return
            except Exception:  # noqa: BLE001  encoding file not downloadable / not cached: try the next, say which
                self._enc = None

    def count(self, text):
        text = text or ""
        if self._enc is not None:
            return len(self._enc.encode(text, disallowed_special=()))
        return (len(text) + 3) // 4

    def truncate(self, text, n):
        if self._enc is not None:
            return self._enc.decode(self._enc.encode(text, disallowed_special=())[:max(0, n)])
        return text[: 4 * max(0, n)]

    def chat_prompt(self, messages):
        """Prompt tokens of a chat request (content + 3 per message + 3 reply priming; the usual gpt-4o estimate)."""
        n = 3
        for m in messages or []:
            c = m.get("content")
            if isinstance(c, list):
                c = "".join(p.get("text", "") for p in c if isinstance(p, dict))
            n += 3 + self.count(str(c or "")) + self.count(str(m.get("role", "")))
        return n


FILLER = ("offline stub reasoning text without domain meaning, written only to occupy the assumed length of a live "
          "reply so that token and cost estimates include completion tokens. ")


class StubKit:
    """Handed to an adapter's stub responder: a deterministic RNG seeded by the request, and a filler of n tokens."""

    def __init__(self, rng, counter):
        self.rng = rng
        self.counter = counter
        self.assumed_completion_tokens = None      # adapters set this for the record

    def filler(self, n_tokens):
        self.assumed_completion_tokens = n_tokens
        return self.counter.truncate(FILLER * (2 + n_tokens // 20), n_tokens)


def _canon(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _parse_sse(raw):
    """Collect content, finish_reason, model and usage from an SSE chat-completions body."""
    text, finish, model, usage = [], None, None, None
    for line in raw.decode("utf-8", "replace").splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if payload == "[DONE]":
            break
        try:
            ch = json.loads(payload)
        except ValueError:
            continue
        model = ch.get("model") or model
        if ch.get("usage"):
            usage = ch["usage"]
        for c in ch.get("choices") or []:
            d = c.get("delta") or {}
            if d.get("content"):
                text.append(d["content"])
            if c.get("finish_reason"):
                finish = c["finish_reason"]
    return "".join(text), finish, model, usage


def _sse_body(text, model, usage, include_usage, rid):
    created = int(time.time())
    out = []

    def emit(choices, extra=None):
        ch = {"id": rid, "object": "chat.completion.chunk", "created": created, "model": model, "choices": choices}
        if extra:
            ch.update(extra)
        out.append("data: " + json.dumps(ch) + "\n\n")

    emit([{"index": 0, "delta": {"role": "assistant", "content": ""}, "logprobs": None, "finish_reason": None}])
    for i in range(0, len(text), 24):
        emit([{"index": 0, "delta": {"content": text[i:i + 24]}, "logprobs": None, "finish_reason": None}])
    emit([{"index": 0, "delta": {}, "logprobs": None, "finish_reason": "stop"}])
    if include_usage:
        emit([], {"usage": usage})
    out.append("data: [DONE]\n\n")
    return "".join(out).encode("utf-8")


def _json_body(text, model, usage, rid):
    return json.dumps({"id": rid, "object": "chat.completion", "created": int(time.time()), "model": model,
                       "choices": [{"index": 0, "message": {"role": "assistant", "content": text},
                                    "logprobs": None, "finish_reason": "stop"}],
                       "usage": usage}).encode("utf-8")


class ProbeLLM:
    def __init__(self, out_dir, stub, model, max_calls, max_usd, stub_responder=None, api_key=None,
                 assumed_completion_tokens=600, log=print):
        self.out_dir = Path(out_dir)
        self.stub = bool(stub)
        self.model = model
        self.max_calls = max_calls
        self.max_usd = max_usd
        self.stub_responder = stub_responder
        self._key = api_key                       # live only; never written anywhere
        self.assumed_completion_tokens = assumed_completion_tokens
        self.counter = TokenCounter()
        self.log = log
        self._lock = threading.Lock()
        self._upstream = None
        self.calls_path = self.out_dir / "calls.jsonl"
        self.replay = collections.defaultdict(collections.deque)
        self.replay_source = None
        if self.calls_path.exists():
            n = 0
            for line in open(self.calls_path, encoding="utf-8"):
                if not line.strip():
                    continue
                r = json.loads(line)
                if r.get("ok") and r.get("request_sha256") and r.get("response_text") is not None \
                        and bool(r.get("stub")) == self.stub:
                    self.replay[r["request_sha256"]].append(r)
                    n += 1
            k = 1
            while (self.out_dir / ("calls.prev%d.jsonl" % k)).exists():
                k += 1
            self.replay_source = str(self.out_dir / ("calls.prev%d.jsonl" % k))
            os.replace(self.calls_path, self.replay_source)
            self.log("[probe-llm] resuming: %d earlier responses available for replay (%s)" % (n, self.replay_source))
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self._fh = open(self.calls_path, "a", encoding="utf-8")
        self.t = collections.Counter()           # calls, new_calls, replayed, errors, prompt/completion tokens
        self.usd_total = 0.0
        self.usd_gpt4o_total = 0.0
        self.seq = 0
        self.models_served = collections.Counter()
        self.usage_sources = collections.Counter()
        self.abort = None

    # ------------------------------------------------------------------------------------------------ public
    def transport(self):
        gate = self

        class _ProbeTransport(httpx.BaseTransport):
            def handle_request(self, request):
                return gate.handle(request)

        return _ProbeTransport()

    def http_client(self, **kw):
        return httpx.Client(transport=self.transport(), **kw)

    def state(self):
        return {"calls": self.t["calls"], "new_api_calls": self.t["new_calls"], "replayed_calls": self.t["replayed"],
                "error_calls": self.t["errors"], "prompt_tokens": self.t["prompt_tokens"],
                "completion_tokens": self.t["completion_tokens"], "usd_at_served_prices": round(self.usd_total, 6),
                "usd_at_gpt4o_list": round(self.usd_gpt4o_total, 6), "max_calls": self.max_calls,
                "max_usd": self.max_usd, "served_models": dict(self.models_served),
                "usage_sources": dict(self.usage_sources), "token_counter": self.counter.name}

    def close(self):
        try:
            self._fh.close()
        finally:
            if self._upstream is not None:
                self._upstream.close()

    # ------------------------------------------------------------------------------------------------ core
    def _write(self, rec):
        self._fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self._fh.flush()

    def _cap_check(self, body, prompt_est):
        if self.max_calls is not None and self.t["calls"] >= self.max_calls:
            return "max_calls (%d) reached" % self.max_calls
        if self.max_usd is not None:
            allowance = body.get("max_completion_tokens") or body.get("max_tokens") or self.assumed_completion_tokens
            prices, _ = price_for(body.get("model") or self.model)
            projected = usd(prompt_est, int(allowance), prices)
            if self.usd_total + projected > self.max_usd:
                return "max_usd (%.4f) would be exceeded: spent %.4f + next call up to %.4f" % (
                    self.max_usd, self.usd_total, projected)
        return None

    def handle(self, request):
        with self._lock:
            return self._handle(request)

    def _handle(self, request):
        path = request.url.path
        if request.method != "POST" or not path.rstrip("/").endswith("/chat/completions"):
            self._write({"event": "rejected_endpoint", "method": request.method, "path": path})
            return httpx.Response(404, json={"error": {"message": "probe gate: only POST .../chat/completions is "
                                                                  "allowed", "type": "probe_gate"}}, request=request)
        body = json.loads(request.content.decode("utf-8") or "{}")
        messages = body.get("messages") or []
        stream = bool(body.get("stream"))
        include_usage = bool((body.get("stream_options") or {}).get("include_usage"))
        req_sha = _sha(_canon(body))
        prompt_sha = _sha(_canon(messages))
        requested = body.get("model")
        self.seq += 1
        rid = "probe-%06d" % self.seq
        t0 = time.time()
        rec = {"seq": self.seq, "ts": round(t0, 3), "stub": self.stub, "requested_model": requested,
               "request_sha256": req_sha, "prompt_sha256": prompt_sha, "stream": stream, "request": body}

        # replay an identical earlier request (resume): free, no cap check
        if self.replay.get(req_sha):
            old = self.replay[req_sha].popleft()
            text, served, usage = old["response_text"], old["served_model"], old["usage"]
            self.t["replayed"] += 1
            rec.update({"ok": True, "replayed": True, "replayed_from_seq": old.get("seq")})
            return self._finish(rec, request, text, served, usage, old.get("usage_source", "replay"),
                                stream, include_usage, rid, t0, old.get("assumed_completion_tokens"))

        prompt_est = self.counter.chat_prompt(messages)
        reason = self._cap_check(body, prompt_est)
        if reason:
            self.abort = {"reason": reason, "at_seq": self.seq, "state": self.state()}
            self._write({"event": "cap_reached", "seq": self.seq, "reason": reason, "state": self.state(),
                         "blocked_request_sha256": req_sha, "blocked_prompt_sha256": prompt_sha})
            raise CapReached(reason, self.state())

        self.t["new_calls"] += 1
        if self.stub:
            kit = StubKit(random.Random(int(req_sha[:16], 16)), self.counter)
            text = self.stub_responder(body, kit)
            usage = {"prompt_tokens": prompt_est, "completion_tokens": self.counter.count(text)}
            usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]
            rec["ok"] = True
            return self._finish(rec, request, text, "stub:" + str(requested), usage, "counted:" + self.counter.name,
                                stream, include_usage, rid, t0, kit.assumed_completion_tokens)

        # live
        if self._upstream is None:
            self._upstream = httpx.Client(timeout=httpx.Timeout(240.0, connect=30.0))
        headers = {"Authorization": "Bearer " + self._key, "Content-Type": "application/json",
                   "Accept": "text/event-stream" if stream else "application/json"}
        try:
            up = self._upstream.post(UPSTREAM_URL, content=request.content, headers=headers)
        except httpx.HTTPError as e:
            self.t["calls"] += 1
            self.t["errors"] += 1
            rec.update({"ok": False, "error": "%s: %s" % (type(e).__name__, str(e)[:300]),
                        "seconds": round(time.time() - t0, 3)})
            self._write(rec)
            raise
        raw = up.content
        ctype = up.headers.get("content-type", "")
        text, served, usage, finish, usage_source = None, None, None, None, "api"
        if up.status_code == 200:
            if "event-stream" in ctype or stream:
                text, finish, served, usage = _parse_sse(raw)
            else:
                d = json.loads(raw)
                served = d.get("model")
                usage = d.get("usage")
                ch = (d.get("choices") or [{}])[0]
                text = (ch.get("message") or {}).get("content")
                finish = ch.get("finish_reason")
            if not usage:
                usage = {"prompt_tokens": prompt_est, "completion_tokens": self.counter.count(text or "")}
                usage_source = "counted:" + self.counter.name
        rec.update({"ok": up.status_code == 200, "status": up.status_code, "finish_reason": finish})
        if up.status_code != 200:
            rec["error_body"] = raw[:2000].decode("utf-8", "replace")
            self.t["errors"] += 1
        self._account(rec, served or requested, usage or {}, usage_source)
        rec.update({"served_model": served, "response_text": text, "seconds": round(time.time() - t0, 3)})
        self._write(rec)
        keep = {k: v for k, v in up.headers.items() if k.lower() in ("content-type", "retry-after", "retry-after-ms",
                                                                      "x-request-id")}
        return httpx.Response(up.status_code, headers=keep, content=raw, request=request)

    def _account(self, rec, model, usage, usage_source):
        pt, ct = int(usage.get("prompt_tokens") or 0), int(usage.get("completion_tokens") or 0)
        prices, assumed = price_for(model)
        c = usd(pt, ct, prices)
        c4o = usd(pt, ct, GPT4O)
        self.t["calls"] += 1
        self.t["prompt_tokens"] += pt
        self.t["completion_tokens"] += ct
        self.usd_total += c
        self.usd_gpt4o_total += c4o
        self.models_served[str(model)] += 1
        self.usage_sources[usage_source] += 1
        rec.update({"usage": {"prompt_tokens": pt, "completion_tokens": ct}, "usage_source": usage_source,
                    "usd": round(c, 8), "usd_at_gpt4o_list": round(c4o, 8), "price_assumed_gpt4o": assumed,
                    "cum_calls": self.t["calls"], "cum_usd": round(self.usd_total, 6)})

    def _finish(self, rec, request, text, served, usage, usage_source, stream, include_usage, rid, t0, assumed):
        # price stub calls at the model the live run would be served (the requested one)
        price_model = rec["requested_model"] if self.stub else served
        self._account(rec, price_model, usage, usage_source)
        rec.update({"served_model": served, "response_text": text, "assumed_completion_tokens": assumed,
                    "finish_reason": "stop", "seconds": round(time.time() - t0, 3)})
        self._write(rec)
        u = {"prompt_tokens": rec["usage"]["prompt_tokens"], "completion_tokens": rec["usage"]["completion_tokens"],
             "total_tokens": rec["usage"]["prompt_tokens"] + rec["usage"]["completion_tokens"]}
        if stream:
            return httpx.Response(200, headers={"content-type": "text/event-stream"},
                                  content=_sse_body(text, served, u, include_usage, rid), request=request)
        return httpx.Response(200, headers={"content-type": "application/json"},
                              content=_json_body(text, served, u, rid), request=request)


def resolve_live_key(dotenv_path="/app/.env"):
    """The key the pipeline would use: a real environment variable wins, else python-dotenv's reading of /app/.env.
    Returned to the caller only; never printed or written. The environment variable is then replaced by a dummy so
    agent code cannot reach the real key."""
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key or key.startswith("stub") or key == DUMMY_KEY:
        key = ""
        try:
            from dotenv import dotenv_values
            key = (dotenv_values(dotenv_path) or {}).get("OPENAI_API_KEY") or ""
        except Exception:  # noqa: BLE001
            key = ""
    return key


def isolate_environment():
    """Point every un-intercepted OpenAI-style client at nothing: dummy key, dead local base URL."""
    os.environ["OPENAI_API_KEY"] = DUMMY_KEY
    os.environ["OPENAI_BASE_URL"] = DEAD_BASE_URL
    os.environ.pop("OPENAI_API_BASE", None)
    os.environ.pop("OPENAI_ORG_ID", None)
