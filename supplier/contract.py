"""The supplier contract (D0.3; approach_v1.md G7, failure mode Z4).

A supplier is anything that answers a question in text (a model behind an API, a stub, a person's file). Every answer
passes through call(): it is validated against a schema function, normalised only in the listed ways, retried at most
once (twice for rate limits), and ends in exactly one outcome:

  accepted             valid as received
  accepted_normalised  valid after a listed normalisation (code fence stripped, surrounding whitespace); counted
  abstained            no usable answer after the allowed attempts; the caller must fall back to data-only
  stopped              a provider refusal that no retry can fix (quota exhausted); the run stops, resumable

Failure classes, each counted (`Counts`) and written into the ledger's report by the caller:
  truncated     finish_reason == "length": never accepted, even if the text parses (a cut-off list is a silent loss);
                retried once with max_tokens doubled
  invalid_json  not JSON after normalisation
  schema        JSON, but the schema function rejects it (missing key, unknown names, ...)
  empty         no text
  rate_limited  HTTP 429 without a quota message: retried up to 2 times with backoff (the stub transport sleeps 0)
  quota         HTTP 429 insufficient_quota / no credits: outcome 'stopped'
  transport     any other non-200 or exception from the transport
A schema function takes the parsed JSON and returns (value, None) or (None, problem). The retry prompt names the problem.
"""
import json
from dataclasses import dataclass, field

FAILURES = ("truncated", "invalid_json", "schema", "empty", "rate_limited", "quota", "transport")
NORMALISATIONS = ("code_fence", "whitespace")
QUOTA_MARKERS = ("insufficient_quota", "no credits", "exceeded your current quota")


@dataclass
class Reply:
    text: str = None
    finish_reason: str = "stop"
    status: int = 200
    error: str = None
    model: str = None
    usage: dict = None


@dataclass
class Outcome:
    status: str
    value: object = None
    problem: str = None
    normalisations: list = field(default_factory=list)
    attempts: list = field(default_factory=list)


@dataclass
class Counts:
    calls: int = 0
    accepted: int = 0
    accepted_normalised: int = 0
    abstained: int = 0
    stopped: int = 0
    failures: dict = field(default_factory=lambda: {k: 0 for k in FAILURES})
    normalisations: dict = field(default_factory=lambda: {k: 0 for k in NORMALISATIONS})

    def add(self, outcome):
        self.calls += len(outcome.attempts)
        setattr(self, outcome.status, getattr(self, outcome.status) + 1)
        for a in outcome.attempts:
            if a.get("failure"):
                self.failures[a["failure"]] += 1
        for n in outcome.normalisations:
            self.normalisations[n] += 1

    def as_dict(self):
        return {"calls": self.calls, "accepted": self.accepted, "accepted_normalised": self.accepted_normalised,
                "abstained": self.abstained, "stopped": self.stopped, "failures": dict(self.failures),
                "normalisations": dict(self.normalisations)}


def normalise(text):
    """-> (text, [normalisations applied]). Only two are allowed: strip surrounding whitespace; strip one markdown
    code fence (``` or ```json) around the whole reply."""
    applied = []
    t = text
    if t != t.strip():
        applied.append("whitespace")
        t = t.strip()
    if t.startswith("```") and t.endswith("```") and len(t) >= 6:
        inner = t[3:-3]
        nl = inner.find("\n")
        first = inner[:nl] if nl >= 0 else ""
        if nl >= 0 and first.strip().isalpha():
            inner = inner[nl + 1:]
        applied.append("code_fence")
        t = inner.strip()
    return t, applied


def classify(reply):
    """-> failure class or None (the reply may still fail parsing or the schema)."""
    if reply.status == 429 or (reply.error and "429" in str(reply.error)):
        body = (reply.error or "") + (reply.text or "")
        return "quota" if any(m in body.lower() for m in QUOTA_MARKERS) else "rate_limited"
    if reply.status != 200 or reply.error:
        return "transport"
    if reply.text is None or not reply.text.strip():
        return "empty"
    if reply.finish_reason == "length":
        return "truncated"
    return None


def check(reply, schema_fn):
    """One reply -> (value, failure class or None, problem, normalisations)."""
    f = classify(reply)
    if f:
        return None, f, f, []
    t, applied = normalise(reply.text)
    try:
        parsed = json.loads(t)
    except (TypeError, ValueError):
        return None, "invalid_json", "not valid JSON", applied
    value, problem = schema_fn(parsed)
    if problem:
        return None, "schema", problem, applied
    return value, None, None, applied


def call(transport, request, schema_fn, max_tokens=None, sleep=lambda s: None):
    """transport(request, max_tokens, problem) -> Reply. problem is None on the first attempt, else the reason the
    previous reply was refused (the transport adds it to the prompt). Returns an Outcome; never raises."""
    attempts = []
    problem = None
    retries_left = 1
    rate_left = 2
    mt = max_tokens
    while True:
        try:
            r = transport(request, mt, problem)
        except Exception as e:  # noqa: BLE001 - a transport exception is a typed failure
            r = Reply(text=None, status=0, error="%s: %s" % (type(e).__name__, e))
        value, fail, prob, applied = check(r, schema_fn)
        attempts.append({"max_tokens": mt, "finish_reason": r.finish_reason, "status": r.status, "failure": fail,
                         "problem": prob, "normalisations": applied, "model": r.model})
        if fail is None:
            return Outcome("accepted_normalised" if applied else "accepted", value=value, normalisations=applied, attempts=attempts)
        if fail == "quota":
            return Outcome("stopped", problem=prob, attempts=attempts)
        if fail == "rate_limited" and rate_left > 0:
            rate_left -= 1
            sleep(2 ** (2 - rate_left))
            continue
        if fail in ("rate_limited",) or retries_left == 0:
            return Outcome("abstained", problem=prob, attempts=attempts)
        retries_left -= 1
        if fail == "truncated" and mt:
            mt = mt * 2
        problem = prob
