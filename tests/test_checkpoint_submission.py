"""DLV-07: submission packaging uses exact commits and excludes forbidden inputs."""
import importlib.util
import gzip
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('packager', Path(__file__).resolve().parents[1] / 'tools/checkpoint_submission.py')
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class Submission(unittest.TestCase):
    def test_unsafe_and_credential_paths(self):
        for name in ['../outside', '/outside', 'a\\b', '.git/config', '.env', 'x/.env.local', 'vault/x', '_local/x', 'key.pem']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                packager.safe_name(name)

    def test_valid_archive_is_exact_and_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'submission.zip'
            packager.write_zip(path, {'repo/README.md': b'synthetic content'})
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(archive.read('repo/README.md'), b'synthetic content')
            with self.assertRaises(ValueError):
                packager.write_zip(path, {})

    def test_unreviewed_nested_archive_fails(self):
        with self.assertRaises(ValueError):
            packager.check_content('unreviewed.zip', b'synthetic')

    def test_committed_snapshot_ignores_untracked_and_unstaged_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT).decode().strip()
            git('init')
            (root / 'README.md').write_text('AI contributions: see AI_USE.md')
            (root / 'AI_USE.md').write_text('Synthetic disclosure')
            git('add', 'README.md', 'AI_USE.md')
            git('-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.invalid',
                '-c', 'core.hooksPath=', 'commit', '-m', 'Synthetic fixture')
            commit = git('rev-parse', 'HEAD')
            (root / 'README.md').write_text('uncommitted replacement')
            (root / 'untracked.txt').write_text('untracked synthetic data')
            files, record = packager.snapshot(root, commit)
            self.assertEqual(record['commit'], commit)
            self.assertEqual(files['README.md'], b'AI contributions: see AI_USE.md')
            self.assertNotIn('untracked.txt', files)

    def test_moving_branch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'explicit commit'):
            packager.snapshot(Path('.'), 'main')

    def test_disclosure_overlay_changes_only_the_two_named_documents(self):
        files = {'README.md': b'Original', 'crucis_causal/core.py': b'synthetic runtime'}
        record = {'files': {'README.md': {'sha256': packager.sha(b'Original')}}}
        prefix = 'docs/paper/q1/audit/2026-11-06/crucis-disclosure/'
        donor = {prefix+'README.md': b'AI contributions: AI_USE.md', prefix+'AI_USE.md': b'Synthetic disclosure',
                 prefix+'crucis_causal/core.py': b'forbidden replacement'}
        packager.disclosure_overlay(files, record, donor, '1'*40)
        self.assertEqual(files['crucis_causal/core.py'], b'synthetic runtime')
        self.assertEqual(set(record['overlays']), {'README.md', 'AI_USE.md'})
        self.assertEqual(record['overlays']['README.md']['original_sha256'], packager.sha(b'Original'))

    def test_compressed_text_does_not_bypass_secret_scan(self):
        synthetic = ('OPENAI_API_KEY=' + 'A'*30).encode()
        with self.assertRaisesRegex(ValueError, 'Secret pattern'):
            packager.check_content('synthetic.jsonl.gz', gzip.compress(synthetic))

    def test_executable_mode_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'mode.zip'
            packager.write_zip(path, {'repo/run.sh': b'echo synthetic'}, {'repo/run.sh': '100755'})
            with zipfile.ZipFile(path) as archive:
                self.assertEqual((archive.getinfo('repo/run.sh').external_attr >> 16) & 0o777, 0o755)


if __name__ == '__main__':
    unittest.main()
