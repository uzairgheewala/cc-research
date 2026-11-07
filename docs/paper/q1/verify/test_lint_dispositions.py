"""DLV-05: editorial dispositions cannot silently excuse a changed draft."""
import hashlib
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('paper_lint', Path(__file__).resolve().parents[1] / 'lint_report.py')
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


class ReviewedDispositions(unittest.TestCase):
    def policy(self, text='synthetic draft'):
        return {'schema_version': 1, 'source_sha256_utf8_lf': hashlib.sha256(text.encode()).hexdigest(),
                'dispositions': [{'error': 'prior-work sentence without citation: known transition', 'kind': 'grouped-attribution',
                                  'reason': 'Supported by the following cited sentence.',
                                  'evidence': ['synthetic-source']} ]}

    def test_exact_judgment_preserves_unreviewed_error(self):
        errors, notes = lint.reviewed_dispositions('synthetic draft', ['prior-work sentence without citation: known transition', 'new unsupported claim'], self.policy())
        self.assertEqual(errors, ['new unsupported claim'])
        self.assertEqual(len(notes), 1)

    def test_changed_draft_keeps_all_errors_and_requires_review(self):
        errors, notes = lint.reviewed_dispositions('changed draft', ['prior-work sentence without citation: known transition'], self.policy())
        self.assertIn('prior-work sentence without citation: known transition', errors)
        self.assertIn('stale', errors[-1])
        self.assertFalse(notes)

    def test_removed_error_does_not_leave_a_silent_exception(self):
        errors, notes = lint.reviewed_dispositions('synthetic draft', [], self.policy())
        self.assertIn('no-longer-triggered', errors[-1])
        self.assertFalse(notes)

    def test_duplicate_dispositions_fail(self):
        policy = self.policy()
        policy['dispositions'] *= 2
        errors, notes = lint.reviewed_dispositions('synthetic draft', ['prior-work sentence without citation: known transition'], policy)
        self.assertIn('prior-work sentence without citation: known transition', errors)
        self.assertFalse(notes)

    def test_missing_evidence_fails(self):
        policy = self.policy()
        policy['dispositions'][0]['evidence'] = []
        errors, notes = lint.reviewed_dispositions('synthetic draft', ['prior-work sentence without citation: known transition'], policy)
        self.assertIn('prior-work sentence without citation: known transition', errors)
        self.assertFalse(notes)

    def test_cannot_waive_undefined_number_or_unchecked_citation(self):
        for error in ['undefined number key synthetic', 'cited key without a checked claim in lit_claims.json: synthetic']:
            policy = self.policy()
            policy['dispositions'][0]['error'] = error
            errors, notes = lint.reviewed_dispositions('synthetic draft', [error], policy)
            self.assertIn(error, errors)
            self.assertFalse(notes)


if __name__ == '__main__':
    unittest.main()
