"""analysis/interview_synthesis.py: PII refusal, schema and cross-field checks, and verdict thresholds (AUD-41).

All records are fake and live in a temp dir; nothing touches docs/interviews/notes/.
"""
import json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
import interview_synthesis as S  # noqa: E402

SCHEMA = json.loads((ROOT / "docs" / "interviews" / "notes_schema.json").read_text())


def codeset(h1="silent", h2="silent", h3="silent", p13="silent"):
    ev = lambda c: "" if c == "silent" else "paraphrased evidence for the code"  # noqa: E731
    return {h: {"code": c, "evidence": ev(c)} for h, c in zip(S.HYPOTHESES, (h1, h2, h3, p13))}


def record(i, p13="silent", h1="silent", sector="it_ops_sre", via="course_contact", **coding):
    yes = p13 == "supports"
    rec = {
        "schema": "ab10-interview-notes/0.1",
        "interview_id": f"P{i:02d}",
        "interview_month": "2026-10",
        "consent": {"path": "a", "verbal_consent": True, "audio_consent": False, "audio_recorded": False},
        "participant": {"sector": sector, "role_level": "individual_contributor", "company_size": "1000-9999",
                        "recruited_via": via},
        "decisions": [{"summary": "decided whether a config rollout caused a latency regression",
                       "type": "rca", "real_or_hypothetical": "real", "which_causes_how_sure": "yes" if yes else "no"}],
        "current_tools": ["datadog", "jupyter"],
        "trust_practices": ["checks whether a rollback reproduces the change"],
        "when_wrong": "a wrong root cause cost about a day of on-call time",
        "artefacts": {c: {"shown": True, "score": 3, "paraphrase": "would read the source column first"} for c in S.CARDS},
        "adoption_signals": {"would_try": "maybe", "budget_owner_named": "yes", "current_spend_band": "10k_100k",
                             "paraphrase": "platform team lead approves tools after a two-week trial"},
        "coding": {"student": codeset(h1=h1, p13=p13), **coding},
    }
    return rec


class Tmp(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.dir = Path(self.td.name) / "notes"
        self.dir.mkdir()
        self.out = Path(self.td.name) / "out" / "synthesis.json"
        self.schema = Path(self.td.name) / "schema.json"
        self.schema.write_text(json.dumps(SCHEMA))

    def tearDown(self):
        self.td.cleanup()

    def write(self, recs):
        for r in recs:
            (self.dir / f"{r['interview_id']}.json").write_text(json.dumps(r))

    def run_main(self):
        return S.main(["--notes-dir", str(self.dir), "--schema", str(self.schema), "--out", str(self.out)])

    def refusals(self, recs):
        self.write(recs)
        _, refusals, _ = S.load_records(self.dir, SCHEMA)
        return refusals


class TestPII(Tmp):
    def assertRefused(self, rec, field, kind):
        refs = self.refusals([rec])
        hit = [r for r in refs if f": {field}: " in r and kind in r]
        self.assertTrue(hit, f"expected {kind} in {field}; got {refs}")
        return hit[0]

    def test_clean_record_passes(self):
        self.assertEqual(self.refusals([record(1)]), [])

    def test_email_refused_and_masked(self):
        r = record(1)
        r["when_wrong"] = "follow up at jane.doe@example.com about the outage"
        msg = self.assertRefused(r, "when_wrong", "email address")
        self.assertNotIn("jane.doe@example.com", msg)

    def test_phone_refused(self):
        for phone in ("(858) 555-0123", "858-555-0123", "+44 20 7946 0958"):
            r = record(1)
            r["adoption_signals"]["paraphrase"] = f"call them on {phone} next week"
            msg = self.assertRefused(r, "adoption_signals.paraphrase", "phone number")
            self.assertNotIn(phone, msg)

    def test_two_word_name_refused_in_nested_field(self):
        r = record(1)
        r["decisions"][0]["summary"] = "the lead, Maria Lopez, chose to roll back"
        self.assertRefused(r, "decisions[0].summary", "capitalised two-word name")

    def test_name_after_sentence_starter_still_caught(self):
        r = record(1)
        r["trust_practices"] = ["Then Sarah Jones checks the dashboard"]
        self.assertRefused(r, "trust_practices[0]", "capitalised two-word name")

    def test_name_in_coding_evidence_refused(self):
        r = record(1, p13="supports")
        r["coding"]["student"]["P13"]["evidence"] = "Priya Raman said only the top causes mattered"
        self.assertRefused(r, "coding.student.P13.evidence", "capitalised two-word name")

    def test_allowlisted_tools_and_sentence_starts_pass(self):
        r = record(1)
        r["current_tools"] = ["Google Meridian", "New Relic", "Looker Studio"]
        r["when_wrong"] = "The Team lost a day. Last Tuesday-style incidents are common."
        self.assertEqual(self.refusals([r]), [])

    def test_numbers_are_not_phones(self):
        r = record(1)
        r["when_wrong"] = "cost about $150,000 in 2026-10; confidence 0.93; 500 services"
        self.assertEqual(self.refusals([r]), [])

    def test_refusal_writes_nothing(self):
        r = record(1)
        r["when_wrong"] = "ask bob@corp.io"
        self.write([r, record(2)])
        self.assertEqual(self.run_main(), 2)
        self.assertFalse(self.out.exists())


class TestSchemaAndCrossField(Tmp):
    def test_extra_identity_field_refused(self):
        r = record(1)
        r["participant"]["employer"] = "acme"
        self.assertTrue(any("participant.employer: field not allowed" in x for x in self.refusals([r])))

    def test_bad_enum_and_id(self):
        r = record(1)
        r["participant"]["sector"] = "finance"
        refs = self.refusals([r])
        self.assertTrue(any("participant.sector" in x for x in refs))
        r2 = record(2)
        r2["interview_id"] = "Jane"
        self.assertTrue(any("interview_id" in x for x in self.refusals([r2])))

    def test_audio_without_consent(self):
        r = record(1)
        r["consent"]["audio_recorded"] = True
        self.assertTrue(any("audio_consent" in x for x in self.refusals([r])))

    def test_path_b_needs_determination(self):
        r = record(1)
        r["consent"]["path"] = "b"
        self.assertTrue(any("determination_ref" in x for x in self.refusals([r])))
        r["consent"]["determination_ref"] = "NHSR determination, Kuali ref pending-0001"
        self.assertEqual(self.refusals([r]), [])

    def test_p13_supports_needs_real_decision(self):
        r = record(1, p13="supports")
        r["decisions"][0]["real_or_hypothetical"] = "hypothetical"
        self.assertTrue(any("coding.student.P13" in x for x in self.refusals([r])))

    def test_non_silent_code_needs_evidence(self):
        r = record(1, h1="supports")
        r["coding"]["student"]["H1"]["evidence"] = ""
        self.assertTrue(any("coding.student.H1.evidence" in x for x in self.refusals([r])))

    def test_file_name_must_match_id(self):
        r = record(1)
        (self.dir / "other.json").write_text(json.dumps(r))
        _, refs, _ = S.load_records(self.dir, SCHEMA)
        self.assertTrue(any("file must be named P01.json" in x for x in refs))


class TestThresholds(unittest.TestCase):
    def test_p13_exactly_as_dag(self):
        cases = [  # (supports, n, verdict)
            (4, 8, "supported"), (3, 8, "inconclusive"), (2, 8, "inconclusive"), (1, 8, "refuted"),
            (3, 6, "supported"), (2, 6, "inconclusive"), (1, 6, "refuted"),
            (3, 5, "supported"), (2, 5, "inconclusive"), (1, 5, "refuted"), (0, 5, "refuted"),
            (2, 7, "inconclusive"), (4, 7, "supported"), (1, 7, "refuted"),
            (4, 4, "insufficient_n"), (0, 3, "insufficient_n")]
        for s, n, v in cases:
            self.assertEqual(S.verdict_p13(s, n), v, (s, n))

    def test_h_rules(self):
        cases = [  # (supports, refutes, n, verdict)
            (4, 0, 8, "supported"), (4, 4, 8, "inconclusive"), (3, 4, 8, "refuted"), (3, 3, 8, "inconclusive"),
            (1, 0, 8, "refuted"), (2, 0, 8, "inconclusive"), (3, 3, 6, "inconclusive"), (3, 0, 5, "supported"),
            (2, 3, 5, "refuted"), (2, 2, 5, "inconclusive"), (5, 0, 4, "insufficient_n")]
        for s, r, n, v in cases:
            self.assertEqual(S.verdict_h(s, r, n), v, (s, r, n))


class TestEndToEnd(Tmp):
    def test_eight_interviews_half_p13_supported(self):
        recs = [record(i, p13="supports" if i <= 4 else "silent", h1="supports" if i <= 2 else "silent")
                for i in range(1, 9)]
        self.write(recs)
        self.assertEqual(self.run_main(), 0)
        res = json.loads(self.out.read_text())
        self.assertEqual(res["n"], 8)
        self.assertEqual(res["status"], "provisional")
        self.assertEqual(res["verdicts"]["P13"]["verdict"], "supported")
        self.assertEqual(res["verdicts"]["P13"]["share_supports"], 0.5)
        self.assertEqual(res["verdicts"]["H1"]["verdict"], "inconclusive")  # 2/8 is not under a quarter
        self.assertEqual(res["verdicts"]["H3"]["verdict"], "refuted")  # 0 supports
        self.assertEqual(res["decisions"]["which_causes_how_sure_yes_real"], 4)

    def test_three_of_eight_inconclusive_and_sensitivity(self):
        recs = [record(i, p13="supports" if i <= 3 else "silent",
                       via="pywhy_community" if i <= 2 else "course_contact") for i in range(1, 9)]
        self.write(recs)
        self.run_main()
        res = json.loads(self.out.read_text())
        self.assertEqual(res["verdicts"]["P13"]["verdict"], "inconclusive")
        sens = res["sensitivity_excluding_causal_communities"]
        self.assertEqual(sens["n"], 6)
        self.assertEqual(sens["verdicts"]["P13"]["supports"], 1)
        self.assertEqual(sens["verdicts"]["P13"]["verdict"], "refuted")  # 1/6 < 1/4

    def test_reconciled_codes_make_it_final(self):
        recs = []
        for i in range(1, 6):
            r = record(i, p13="supports")
            r["coding"]["claude"] = codeset(p13="supports" if i != 5 else "silent")
            r["coding"]["reconciled"] = codeset(p13="supports" if i <= 2 else "silent")
            recs.append(r)
        self.write(recs)
        self.run_main()
        res = json.loads(self.out.read_text())
        self.assertEqual(res["status"], "final")
        self.assertEqual(res["coding_used"], "reconciled")
        self.assertEqual(res["verdicts"]["P13"]["supports"], 2)
        self.assertEqual(res["verdicts"]["P13"]["verdict"], "inconclusive")  # 2/5 = 0.4
        ic = res["inter_coder"]["by_hypothesis"]["P13"]
        self.assertEqual((ic["agree"], ic["n"], ic["disagreements"]), (4, 5, ["P05"]))
        self.assertEqual(ic["percent"], 0.8)

    def test_kappa(self):
        self.assertEqual(S.cohen_kappa([("supports", "supports"), ("silent", "silent")]), 1.0)
        self.assertIsNone(S.cohen_kappa([("silent", "silent")] * 3))  # expected agreement 1: undefined
        self.assertEqual(S.cohen_kappa([("supports", "silent"), ("silent", "supports")]), -1.0)

    def test_deterministic_output(self):
        self.write([record(i) for i in range(1, 6)])
        self.run_main()
        first = self.out.read_bytes()
        self.run_main()
        self.assertEqual(first, self.out.read_bytes())

    def test_blind_export_strips_coding(self):
        self.write([record(1, p13="supports")])
        blind = Path(self.td.name) / "blind"
        rc = S.main(["--notes-dir", str(self.dir), "--schema", str(self.schema), "--export-blind", str(blind)])
        self.assertEqual(rc, 0)
        b = json.loads((blind / "P01.json").read_text())
        self.assertEqual(b["coding"], {})
        self.assertEqual(b["decisions"][0]["which_causes_how_sure"], "unclear")

    def test_no_notes(self):
        self.assertEqual(self.run_main(), 1)


if __name__ == "__main__":
    unittest.main()
