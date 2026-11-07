"""DLV-05: known-answer restraint for the recorded-evidence audit."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('evidence_audit', Path(__file__).with_name('audit_checkpoint_evidence.py'))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class EvidenceAudit(unittest.TestCase):
    def test_directed_f1_distinguishes_reversal_and_empty_prediction(self):
        self.assertEqual(audit.f1({(0, 1)}, {(0, 1)}), 1)
        self.assertEqual(audit.f1({(1, 0)}, {(0, 1)}), 0)
        self.assertEqual(audit.f1(set(), {(0, 1)}), 0)
        self.assertEqual(audit.f1({(0, 1), (1, 2)}, {(0, 1)}), 2/3)

    def test_missing_reference_is_a_gap_not_negative_proof_or_reproduction(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = {
                'analysis/results/methods/fci_semantic_obs.json': {'rows': [{'file': 'synthetic.npz', 'failed': False}]},
                'analysis/results/rescore_v2/leaderboard_controlled.json': {'table': [
                    {'method': 'FCI', 'family': 'semantic', 'ours_released_expectation': .5, 'ours_released_authors_rule': 1.0}]}}
            for name, value in paths.items():
                path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(value))
            result = audit.scoring_audit(root, {})
            self.assertFalse(result['full_reference_cohort_available'])
            self.assertEqual(result['eligible_graphs'], 0)
            self.assertIsNone(result['gain_at_paper_precision'])
            self.assertEqual(result['mismatches'], [])
            self.assertEqual(len(result['reference_files_missing']), 1)


if __name__ == '__main__':
    unittest.main()
