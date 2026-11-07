"""DLV-07: create one source-only multi-repository ZIP from explicit Git commits.

No working-tree copy, Git history, private workbench, credentials or live runs.
The manifest proves snapshot bytes, not scientific validity or disclosure completeness.
"""
import argparse
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

NAMES = {'cc-research', 'causal-copilot-q1', 'crucis'}
OVERLEAF = {'report.tex', 'reference.bib', 'numbers.tex', 'numbers_table.tex',
            'style/dsc180reportstyle.sty', 'style/dsc180bibstyle.bst'}
spec = importlib.util.spec_from_file_location('submission_secret_scan', Path(__file__).with_name('secret_scan.py'))
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
        raise ValueError('Unsafe archive path: ' + name)
    for part in path.parts:
        low = part.lower()
        if (low == '.git' or low == '.env' or low.startswith('.env.') or
                low.endswith(('.pem', '.key', '.p12')) or low in {'_local', 'vault'}):
            raise ValueError('Forbidden archive path: ' + name)


def check_content(name, data):
    if len(data) > 50 * 1024 * 1024:
        raise ValueError('File exceeds source-package size bound: ' + name)
    if not name.endswith(scanner.SKIP_SUFFIX):
        for label, pattern in scanner.PATTERNS:
            if pattern.search(data):
                raise ValueError('Secret pattern (' + label + ') in ' + name)
    if name.endswith('.zip'):
        if name != 'docs/paper/q1/releases/checkpoint-2026-11-06/overleaf-source.zip':
            raise ValueError('Unreviewed nested archive: ' + name)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if len(archive.namelist()) != 6 or set(archive.namelist()) != OVERLEAF:
                raise ValueError('Unexpected nested Overleaf members')
            for member in archive.namelist():
                safe_name(member)
                check_content(member, archive.read(member))
    elif name.endswith('.gz'):
        # Existing public scientific JSONL snapshots are retained, but compressed
        # bytes must not bypass the scan or permit unbounded decompression.
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
            expanded = stream.read(50 * 1024 * 1024 + 1)
        check_content(name[:-3], expanded)
    elif name.endswith(('.tar', '.tgz', '.7z', '.rar')):
        raise ValueError('Unreviewed nested archive: ' + name)


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def disclosure_check(files):
    if not {'README.md', 'AI_USE.md'} <= set(files):
        raise ValueError('Each repository needs committed README.md and AI_USE.md')
    readme = files['README.md'].decode('utf-8')
    if 'AI_USE.md' not in readme or 'contribution' not in readme.lower():
        raise ValueError('README must link the AI/human contribution disclosure')


def snapshot(repo, commit, require_disclosure=True):
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Use a full explicit commit SHA, not a moving branch')
    resolved = git(repo, 'rev-parse', '--verify', commit + '^{commit}').decode().strip()
    tree = git(repo, 'rev-parse', resolved + '^{tree}').decode().strip()
    entries = {}
    for raw in git(repo, 'ls-tree', '-rz', '--full-tree', resolved).split(b'\0'):
        if not raw:
            continue
        meta, name = raw.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = name.decode('utf-8')
        safe_name(name)  # inspect names before requesting any file bodies
        if mode not in {'100644', '100755'} or kind != 'blob':
            raise ValueError('Symlink/submodule/special entry needs explicit review: ' + name)
        entries[name] = (mode, oid)
    with zipfile.ZipFile(io.BytesIO(git(repo, 'archive', '--format=zip', resolved))) as archive:
        files = {item.filename: archive.read(item) for item in archive.infolist() if not item.is_dir()}
        if len(files) != len([x for x in archive.infolist() if not x.is_dir()]) or set(files) != set(entries):
            raise ValueError('Archive omissions, duplicates or substitutions need explicit review')
    for name, data in files.items():
        oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if oid != entries[name][1]:
            raise ValueError('Archive bytes differ from committed blob: ' + name)
        check_content(name, data)
    if require_disclosure:
        disclosure_check(files)
    return files, {'commit': resolved, 'tree': tree, 'files': {
        name: {'sha256': sha(data), 'bytes': len(data), 'mode': entries[name][0]}
        for name, data in sorted(files.items())}}


def write_zip(path, files, modes=None):
    modes = modes or {}
    if path.exists():
        raise ValueError('Refusing to overwrite an existing submission ZIP')
    with zipfile.ZipFile(path, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            safe_name(name)
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = int(modes.get(name, '100644'), 8) << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(path) as archive:
        if set(archive.namelist()) != set(files):
            raise ValueError('Written archive member mismatch')
        for name, data in files.items():
            if archive.read(name) != data:
                raise ValueError('Written archive content mismatch: ' + name)


def disclosure_overlay(source, record, donor, donor_commit):
    """Only these documentation files may differ from the Crucis base commit."""
    record['overlays'] = {}
    for member in ('README.md', 'AI_USE.md'):
        origin = 'docs/paper/q1/audit/2026-11-06/crucis-disclosure/' + member
        payload = donor[origin]
        check_content(member, payload)
        record['overlays'][member] = {'source_repository': 'cc-research',
            'source_commit': donor_commit, 'source_path': origin,
            'original_sha256': record['files'].get(member, {}).get('sha256'), 'sha256': sha(payload),
            'reason': 'Additive disclosure documents; runtime and tests remain at the public Crucis base. Local full gate incomplete; not a validated Crucis commit.'}
        source[member] = payload
        record['files'][member] = {'sha256': sha(payload), 'bytes': len(payload), 'mode': '100644'}
    disclosure_check(source)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', action='append', required=True, help='name=checkout-path@full-commit-sha')
    ap.add_argument('--guide', type=Path, required=True)
    ap.add_argument('--validation', type=Path, required=True, help='Sanitized verification JSON included in the ZIP')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--max-bytes', type=int, default=256 * 1024 * 1024)
    ap.add_argument('--crucis-disclosure-overlay', action='store_true',
                    help='Only README.md and AI_USE.md from the committed cc-research audit overlay; declared separately from the Crucis source commit')
    args = ap.parse_args(argv)
    configured = {}
    for item in args.repo:
        name, value = item.split('=', 1)
        path, commit = value.rsplit('@', 1)
        if name not in NAMES or name in configured:
            raise ValueError('Unexpected/duplicate repository name')
        configured[name] = (Path(path), commit)
    if set(configured) != NAMES:
        raise ValueError('Exactly the three declared public project repositories are required')
    validation = json.loads(args.validation.read_text(encoding='utf-8'))
    files = {'README.md': args.guide.read_bytes(), 'VALIDATION.json': args.validation.read_bytes()}
    modes = {}
    sources = {}
    manifest = {'schema_version': 1, 'tickets': ['DLV-05', 'DLV-07'], 'repositories': {},
                'scope': 'Committed source snapshots with any explicitly declared documentation overlay; excludes .git and the private research workbench; not full native replay.'}
    for name, (repo, commit) in sorted(configured.items()):
        overlay = name == 'crucis' and args.crucis_disclosure_overlay
        source, record = snapshot(repo, commit, require_disclosure=not overlay)
        if overlay:
            disclosure_overlay(source, record, sources['cc-research'], manifest['repositories']['cc-research']['commit'])
        sources[name] = source
        manifest['repositories'][name] = record
        files.update({name + '/' + rel: data for rel, data in source.items()})
        modes.update({name + '/' + rel: row['mode'] for rel, row in record['files'].items()})
    if validation.get('commits') != {name: r['commit'] for name, r in manifest['repositories'].items()}:
        raise ValueError('Validation receipt must identify these exact commits')
    if sum(map(len, files.values())) > args.max_bytes:
        raise ValueError('Combined uncompressed size exceeds declared bound')
    for name in ('README.md', 'VALIDATION.json'):
        check_content(name, files[name])
    manifest['metadata_files'] = {name: {'sha256': sha(files[name]), 'bytes': len(files[name])}
                                  for name in ('README.md', 'VALIDATION.json')}
    files['MANIFEST.json'] = (json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    write_zip(args.out, files, modes)
    receipt = {'zip_sha256': sha(args.out.read_bytes()), 'members': len(files),
               'uncompressed_bytes': sum(map(len, files.values())),
               'commits': validation['commits'], 'submitted': False}
    args.out.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
