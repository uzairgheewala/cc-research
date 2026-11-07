"""DLV-05/DLV-07: synthetic archive and stale-binding regression checks."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('release', Path(__file__).with_name('verify_checkpoint_release.py'))
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseBindings(unittest.TestCase):
    def make(self, root):
        folder = root / 'releases/checkpoint-2026-11-06'
        folder.mkdir(parents=True)
        inputs = {}
        for name in release.INPUTS:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(('synthetic ' + name).encode())
            inputs[name] = release.sha(path.read_bytes())
        (root / 'build').mkdir()
        (root / 'build/report.pdf').write_bytes(b'synthetic PDF bytes')
        (folder / 'report.pdf').write_bytes(b'synthetic PDF bytes')
        with zipfile.ZipFile(folder / 'overleaf-source.zip', 'w') as archive:
            for name in inputs:
                archive.write(root / name, name)
        names = ['build/report.pdf', 'releases/checkpoint-2026-11-06/report.pdf',
                 'releases/checkpoint-2026-11-06/overleaf-source.zip']
        return {'schema_version': 1, 'inputs': inputs,
                'artifacts': {name: release.sha((root / name).read_bytes()) for name in names}, 'review_bindings': {}}

    def test_exact_release_passes_and_modified_source_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make(root)
            release.verify(root, manifest)
            (root / 'report.tex').write_bytes(b'changed synthetic claim')
            with self.assertRaisesRegex(ValueError, 'Canonical source differs'):
                release.verify(root, manifest)

    def test_changed_pdf_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make(root)
            (root / 'build/report.pdf').write_bytes(b'changed synthetic PDF')
            with self.assertRaisesRegex(ValueError, 'artifact'):
                release.verify(root, manifest)

    def test_unexpected_archive_member_fails_even_with_new_archive_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make(root)
            name = 'releases/checkpoint-2026-11-06/overleaf-source.zip'
            with zipfile.ZipFile(root / name, 'a') as archive:
                archive.writestr('unexpected.txt', 'synthetic extra input')
            manifest['artifacts'][name] = release.sha((root / name).read_bytes())
            with self.assertRaisesRegex(ValueError, 'archive members'):
                release.verify(root, manifest)

    def test_path_escape_fails_before_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make(root)
            manifest['artifacts']['../outside.txt'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'outside paper'):
                release.verify(root, manifest)


if __name__ == '__main__':
    unittest.main()
