"""Tickets: DLV-05. Failure injection protects a complete prior output generation."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('checkpoint_builder', Path(__file__).resolve().parents[1] / 'build_paper.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildTransaction(unittest.TestCase):
    def test_late_failure_restores_all_primary_outputs(self):
        for fail_name in ['report.pdf', 'overleaf_upload.zip']:
            with self.subTest(fail_name=fail_name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); source = root / 'candidate'; source.mkdir()
                names = ['build-receipt.json', 'report.pdf', 'overleaf_upload.zip']
                for name in names:
                    (root / name).write_bytes(b'old ' + name.encode())
                    (source / name).write_bytes(b'new ' + name.encode())
                original = {name: (root / name).read_bytes() for name in names}
                real_replace = builder.os.replace
                failed = False
                def replace(src, dst):
                    nonlocal failed
                    if not failed and Path(dst).name == fail_name:
                        failed = True
                        raise OSError('synthetic late promotion failure')
                    return real_replace(src, dst)
                with patch.object(builder.os, 'replace', replace):
                    with self.assertRaisesRegex(RuntimeError, 'prior primary outputs restored'):
                        builder.promote_outputs({n: source / n for n in names}, root)
                self.assertEqual(original, {n: (root / n).read_bytes() for n in names})
                self.assertTrue(all((source / n).exists() for n in names))

    def test_success_preserves_historical_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'candidate.pdf'
            source.write_bytes(b'new'); (root / 'report.pdf').write_bytes(b'old')
            builder.promote_outputs({'report.pdf': source}, root)
            self.assertEqual((root / 'report.pdf').read_bytes(), b'new')
            self.assertEqual(next((root / 'history').iterdir()).read_bytes(), b'old')


if __name__ == '__main__': unittest.main()
