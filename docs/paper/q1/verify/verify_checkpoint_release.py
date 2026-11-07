"""DLV-05/DLV-07: verify exact local checkpoint artifacts, not scientific truth.

Run from cc-research with the workspace Python. Does not rebuild, publish or submit.
"""
import hashlib
import json
from pathlib import Path
import zipfile

PAPER = Path(__file__).resolve().parents[1]
MANIFEST = PAPER / 'releases/checkpoint-2026-11-06/manifest.json'
INPUTS = {'report.tex', 'reference.bib', 'numbers.tex', 'numbers_table.tex',
          'style/dsc180reportstyle.sty', 'style/dsc180bibstyle.bst'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(paper, manifest):
    if manifest.get('schema_version') != 1 or set(manifest['inputs']) != INPUTS:
        raise ValueError('Unexpected release schema or source member set')
    for name, digest in manifest['inputs'].items():
        if sha((paper / name).read_bytes()) != digest:
            raise ValueError('Canonical source differs from release: ' + name)
    for name, digest in manifest['artifacts'].items():
        path = (paper / name).resolve()
        if not path.is_relative_to(paper.resolve()) or sha(path.read_bytes()) != digest:
            raise ValueError('Release artifact missing, outside paper, or changed: ' + name)
    archive_name = 'releases/checkpoint-2026-11-06/overleaf-source.zip'
    if set(manifest['artifacts']) != {'build/report.pdf', 'releases/checkpoint-2026-11-06/report.pdf', archive_name}:
        raise ValueError('Release must bind the current and archived PDF and source archive')
    if manifest['artifacts']['build/report.pdf'] != manifest['artifacts']['releases/checkpoint-2026-11-06/report.pdf']:
        raise ValueError('Current PDF differs from the archived release PDF')
    with zipfile.ZipFile(paper / archive_name) as archive:
        if len(archive.namelist()) != len(INPUTS) or set(archive.namelist()) != INPUTS:
            raise ValueError('Unexpected/duplicate archive members')
        for name, digest in manifest['inputs'].items():
            if sha(archive.read(name)) != digest:
                raise ValueError('Archive source differs from release: ' + name)
    for name, digest in manifest['review_bindings'].items():
        path = (paper / name).resolve()
        if not path.is_relative_to(paper.resolve()) or sha(path.read_bytes()) != digest:
            raise ValueError('Review binding missing or changed: ' + name)


if __name__ == '__main__':
    verify(PAPER, json.loads(MANIFEST.read_text(encoding='utf-8')))
    print('checkpoint release: exact six source files, archive, PDF and review bindings match; not a reproduction or submission receipt')
