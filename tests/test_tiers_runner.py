"""harness/tiers_runner.parse_reply: the validation rule for A3 tier replies (AUD-48)."""
import json, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness"))
from tiers_runner import parse_reply, stub_reply  # noqa: E402

NAMES = ["a", "b", "c"]


class ParseReply(unittest.TestCase):
    def test_valid(self):
        t, p = parse_reply('{"tiers": [["a"], ["b", "c"]]}', NAMES)
        self.assertEqual(t, [["a"], ["b", "c"]])
        self.assertIsNone(p)

    def test_code_fence_and_whitespace(self):
        t, _ = parse_reply('```json\n{"tiers": [[" a "], ["b", "c"]]}\n```', NAMES)
        self.assertEqual(t, [["a"], ["b", "c"]])

    def test_missing_unknown_duplicate(self):
        for bad in ('{"tiers": [["a"], ["b"]]}', '{"tiers": [["a", "x"], ["b", "c"]]}', '{"tiers": [["a", "a"], ["b", "c"]]}'):
            t, p = parse_reply(bad, NAMES)
            self.assertIsNone(t)
            self.assertTrue(p)

    def test_not_json_or_wrong_keys(self):
        for bad in ("inputs first", '{"order": [["a", "b", "c"]]}', '{"tiers": []}', None):
            self.assertIsNone(parse_reply(bad, NAMES)[0])

    def test_stub_is_deterministic(self):
        self.assertEqual(stub_reply("x|y", NAMES, 0), stub_reply("x|y", NAMES, 0))


if __name__ == "__main__":
    unittest.main()
