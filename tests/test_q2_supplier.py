"""B0.2: the supplier contract's fault-injection suite (7 cases), and B3's orient-only rule on a ledger.

Pass (plans/q2_build_prereg.json B0.2): every case completes; each failure and each accepted normalisation is counted;
claims on affected pairs equal the data-only output.
"""
import copy, json, sys, unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from supplier import contract as C, tiers as TS  # noqa: E402
from kernel import build as B, checker, knowledge as K  # noqa: E402
import q2_oracle as O  # noqa: E402
import verify02  # noqa: E402

NAMES = ["rain", "wet_road", "skid", "speed"]
GOOD = json.dumps({"tiers": [["rain", "speed"], ["wet_road"], ["skid"]]})


def scripted(*replies):
    it = iter(replies)

    def transport(request, max_tokens, problem):
        r = next(it, None)
        if r is None:
            raise RuntimeError("no more scripted replies")
        return r
    return transport


CASES = {
    "missing_key": (C.Reply(text=json.dumps({"order": NAMES})), C.Reply(text=json.dumps({"order": NAMES}))),
    "truncation": (C.Reply(text=GOOD, finish_reason="length"), C.Reply(text=GOOD[:20], finish_reason="length")),
    "invalid_json": (C.Reply(text="Sure! rain comes first."), C.Reply(text="{tiers: rain}")),
    "code_fenced_json": (C.Reply(text="```json\n" + GOOD + "\n```"),),
    "empty_reply": (C.Reply(text=""), C.Reply(text="   ")),
    "http_429_storm": (C.Reply(status=429, error="429 Too Many Requests"),) * 3,
    "quota_refusal": (C.Reply(status=429, error="429 insufficient_quota: You exceeded your current quota"),),
}
EXPECT = {"missing_key": "abstained", "truncation": "abstained", "invalid_json": "abstained", "code_fenced_json": "accepted_normalised",
          "empty_reply": "abstained", "http_429_storm": "abstained", "quota_refusal": "stopped"}
FAILURE = {"missing_key": "schema", "truncation": "truncated", "invalid_json": "invalid_json", "empty_reply": "empty",
           "http_429_storm": "rate_limited", "quota_refusal": "quota"}


def data_only_ledger():
    p = 6
    rng = np.random.default_rng(3)
    X = rng.standard_normal((60, p))
    names = ["rain", "wet_road", "skid", "speed", "tyre_age", "brake_wear"]
    edges = [(0, 1), (1, 2), (3, 2), (4, 5)]                      # canonical indices; 4 - 5 stays open
    log = O.pc_log(p, O.oracle(edges, p))
    led, _ = B.build(X, names, rule="pc", eng=O.fake_engines(X, names, log=log), created_utc="")
    return led


class Contract(unittest.TestCase):
    def test_fault_suite(self):
        counts = C.Counts()
        for name, replies in CASES.items():
            out = C.call(scripted(*replies), {"q": name}, TS.schema(NAMES), max_tokens=100)
            counts.add(out)
            self.assertEqual(out.status, EXPECT[name], name)
            if name in FAILURE:
                self.assertIn(FAILURE[name], [a["failure"] for a in out.attempts], name)
            if name == "code_fenced_json":
                self.assertEqual(out.normalisations, ["code_fence"])
                self.assertEqual(out.value, [["rain", "speed"], ["wet_road"], ["skid"]])
            if name == "truncation":
                self.assertEqual([a["max_tokens"] for a in out.attempts], [100, 200])
        d = counts.as_dict()
        self.assertEqual(d["accepted_normalised"], 1)
        self.assertEqual(d["stopped"], 1)
        self.assertEqual(d["abstained"], 5)
        self.assertEqual(d["normalisations"]["code_fence"], 1)
        for f in ("schema", "truncated", "invalid_json", "empty", "rate_limited", "quota"):
            self.assertGreater(d["failures"][f], 0, f)

    def test_truncated_reply_is_never_accepted_even_if_it_parses(self):
        out = C.call(scripted(C.Reply(text=GOOD, finish_reason="length"), C.Reply(text=GOOD, finish_reason="length")), {}, TS.schema(NAMES), 50)
        self.assertEqual(out.status, "abstained")

    def test_transport_exception_is_typed(self):
        def boom(*a):
            raise ConnectionError("reset")
        out = C.call(boom, {}, TS.schema(NAMES))
        self.assertEqual(out.status, "abstained")
        self.assertEqual(out.attempts[0]["failure"], "transport")


class FaultsLeaveDataOnly(unittest.TestCase):
    """Claims on affected pairs equal the data-only output: a table whose phrasings all failed gets no knowledge."""

    def test_every_failed_case_gives_data_only_claims(self):
        led_d = data_only_ledger()
        for name, replies in CASES.items():
            if EXPECT[name] == "accepted_normalised":
                continue
            stmts = {}
            counts = C.Counts()
            for ph in ("p0", "p1", "p2"):
                out = C.call(scripted(*replies), {}, TS.schema([v["name"] for v in led_d["variables"]]), 100)
                counts.add(out)
                stmts[ph] = None if out.status in ("abstained", "stopped") else {"tiers": out.value}
            led_k, info = K.apply_tiers(led_d, stmts, counts.as_dict())
            self.assertEqual([(c["x"], c["y"], c["relation"]) for c in led_k["claims"]],
                             [(c["x"], c["y"], c["relation"]) for c in led_d["claims"]], name)
            self.assertEqual(info["decided"], [])
            self.assertEqual({k for k, v in verify02.verify(led_k).items() if v}, set(), name)

    def test_one_answering_phrasing_is_not_enough(self):
        led_d = data_only_ledger()
        names = [v["name"] for v in led_d["variables"]]
        stmts = {"p0": {"tiers": [names]}, "p1": None, "p2": None}
        led_k, info = K.apply_tiers(led_d, stmts)
        self.assertEqual(info["decided"], [])


class OrientOnly(unittest.TestCase):
    def test_tiers_orient_only_open_pairs(self):
        led_d = data_only_ledger()
        open_pairs = [c for c in led_d["claims"] if c["relation"] == "x-y"]
        self.assertTrue(open_pairs)
        names = [v["name"] for v in led_d["variables"]]
        a, b = open_pairs[0]["x"], open_pairs[0]["y"]
        rest = [n for n in names if n not in (a, b)]
        tiers = [[b] + rest, [a]]                            # says b before a
        led_k, info = K.apply_tiers(led_d, {"p0": {"tiers": tiers}, "p1": {"tiers": tiers}, "p2": None})
        ck = {frozenset((c["x"], c["y"])): c for c in led_k["claims"]}
        c = ck[frozenset((a, b))]
        self.assertEqual((c["x"], c["y"], c["relation"], c["direction_source"]), (b, a, "x->y", "knowledge"))
        for c0 in led_d["claims"]:                         # nothing else changes; no connection added or removed
            c1 = ck[frozenset((c0["x"], c0["y"]))]
            if frozenset((c0["x"], c0["y"])) != frozenset((a, b)):
                self.assertEqual((c1["x"], c1["y"], c1["relation"]), (c0["x"], c0["y"], c0["relation"]))
        self.assertEqual({k for k, v in verify02.verify(led_k).items() if v}, set())
        self.assertTrue(checker.check(led_k)["ok"], checker.check(led_k)["errors"])
        self.assertEqual(led_k["report"]["regime"], "D+K")

    def test_disagreeing_phrasings_order_nothing(self):
        led_d = data_only_ledger()
        names = [v["name"] for v in led_d["variables"]]
        t1 = [names[:3], names[3:]]
        t2 = [names[3:], names[:3]]
        led_k, info = K.apply_tiers(led_d, {"p0": {"tiers": t1}, "p1": {"tiers": t2}, "p2": None})
        self.assertEqual(info["decided"], [])
        self.assertTrue(led_k["overrides"])                # both statements recorded as not used


if __name__ == "__main__":
    unittest.main()
