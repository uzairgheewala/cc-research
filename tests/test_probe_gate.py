"""AB-06 v2 (14 Oct): the probe gate's batch-safety rules, without any agent and without network.

  error responses (HTTP 429) do not use up max_calls, but too many of them stop the run;
  a resumed run reports only the cost of the calls it actually sent (usd_new_at_served_prices);
  a transient OSError EIO while appending to calls.jsonl is retried, not fatal.
Needs httpx (the probe image and the cloud probe venv have it); skipped otherwise.
    python -m unittest tests/test_probe_gate.py -v
"""
import errno
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT / "harness"))
try:
    import httpx
    import probe_llm as PL
except ImportError as e:  # noqa: F841
    httpx = None


def _req(i):
    body = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "question %d" % i}]}
    return httpx.Request("POST", "http://127.0.0.1:9/v1/chat/completions", content=json.dumps(body).encode())


def _ok(text="fine"):
    return httpx.Response(200, json={"model": "gpt-4o-mini-2024-07-18", "choices": [{"message": {"content": text},
                                                                                       "finish_reason": "stop"}],
                                     "usage": {"prompt_tokens": 1000, "completion_tokens": 100}})


@unittest.skipIf(httpx is None, "httpx not installed on this interpreter")
class Gate(unittest.TestCase):
    def setUp(self):
        self.out = Path(tempfile.mkdtemp())

    def _live(self, handler, max_calls, max_usd=10.0):
        g = PL.ProbeLLM(self.out, False, "gpt-4o-mini", max_calls, max_usd, api_key="not-a-key", log=lambda *a: None)
        g._upstream = httpx.Client(transport=httpx.MockTransport(handler))
        return g

    def test_rate_limited_calls_do_not_use_up_max_calls(self):
        n = {"i": 0}

        def handler(request):
            n["i"] += 1
            return httpx.Response(429, json={"error": {"message": "rate"}}) if n["i"] <= 3 else _ok()
        g = self._live(handler, max_calls=2)
        codes = [g.handle(_req(i)).status_code for i in range(5)]
        self.assertEqual(codes, [429, 429, 429, 200, 200])
        with self.assertRaises(PL.CapReached) as cm:
            g.handle(_req(9))
        self.assertIn("max_calls", cm.exception.reason)
        g.close()

    def test_too_many_errors_stop_the_run(self):
        g = self._live(lambda r: httpx.Response(429, json={"error": {"message": "rate"}}), max_calls=100)
        with self.assertRaises(PL.CapReached) as cm:
            for i in range(40):
                g.handle(_req(i))
        self.assertIn("error responses", cm.exception.reason)
        g.close()

    def test_resume_reports_only_new_spend(self):
        g = self._live(lambda r: _ok(), max_calls=50)
        for i in range(3):
            g.handle(_req(i))
        first = g.state()["usd_at_served_prices"]
        g.close()
        g2 = self._live(lambda r: _ok(), max_calls=50)
        for i in range(4):                     # three replayed, one new
            g2.handle(_req(i))
        s = g2.state()
        self.assertEqual(s["replayed_calls"], 3)
        self.assertAlmostEqual(s["usd_at_served_prices"], first * 4 / 3, places=9)
        self.assertAlmostEqual(s["usd_new_at_served_prices"], first / 3, places=9)
        g2.close()

    def test_resume_survives_a_line_cut_short(self):
        g = self._live(lambda r: _ok(), max_calls=50)
        for i in range(2):
            g.handle(_req(i))
        g.close()
        with open(self.out / "calls.jsonl", "a", encoding="utf-8") as fh:
            fh.write('{"seq": 3, "request": {"model": "gpt-4o-mini", "mess')        # a hard stop mid-write
        g2 = self._live(lambda r: _ok(), max_calls=50)
        for i in range(3):
            g2.handle(_req(i))
        s = g2.state()
        self.assertEqual((s["replayed_calls"], s["new_api_calls"]), (2, 1))
        g2.close()

    def test_quota_exhausted_stops_cleanly(self):
        body = {"error": {"message": "You have no credits remaining.", "type": "insufficient_quota", "code": "insufficient_quota"}}
        g = self._live(lambda r: httpx.Response(429, json=body), max_calls=50)
        with self.assertRaises(PL.QuotaExhausted):
            g.handle(_req(0))
        g.close()
        lines = [json.loads(l) for l in (self.out / "calls.jsonl").read_text().splitlines() if l.strip()]
        self.assertEqual(lines[-1].get("event"), "quota_exhausted")

    def test_eio_on_calls_log_is_retried(self):
        g = self._live(lambda r: _ok(), max_calls=5)
        real = g._fh

        class Flaky:
            def __init__(self):
                self.failed = False

            def write(self, s):
                if not self.failed:
                    self.failed = True
                    raise OSError(errno.EIO, "Input/output error")
                return real.write(s)

            def flush(self):
                real.flush()

            def close(self):
                pass
        g._fh = Flaky()
        with mock.patch.object(PL.time, "sleep", lambda s: None):      # no real waiting in the test
            g.handle(_req(0))
        g.close()
        lines = [json.loads(l) for l in (self.out / "calls.jsonl").read_text().splitlines() if l.strip()]
        self.assertEqual(len([l for l in lines if l.get("ok")]), 1)


if __name__ == "__main__":
    unittest.main()
