"""Build the Q1 checkpoint in scratch, preserving the last good PDF on failure.

Tickets: DLV-05, DLV-07. Requires the actual course template bibliography.
--overleaf produces a self-contained source bundle bound to the build receipt.
--no-pdf produces sources only and records that no current PDF was built.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
UPLOAD = ['report.tex', 'reference.bib', 'numbers.tex', 'numbers_table.tex',
          'style/dsc180reportstyle.sty', 'style/dsc180bibstyle.bst']
STYLE_HASHES = {
    'style/dsc180reportstyle.sty': '8b6a24551500813f874ca797ffdd16426d1b00725cbed3b87d2667a96e2597f7',
    'style/dsc180bibstyle.bst': '1c9e8a1567018e60360c9eb7ce1036bf9a9e551931112cdb742471212d8f9953',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd, cwd=HERE, log=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                            encoding='utf-8', errors='replace', timeout=240)
    if log:
        log.write_text(result.stdout + result.stderr, encoding='utf-8')
    return result


def step(name, cmd):
    result = run(cmd)
    output = (result.stdout + result.stderr).strip()
    print(f'[{name}] {output.splitlines()[-1] if output else "(no output)"}')
    if result.returncode:
        raise RuntimeError(f'{name}: {output}')


def promote_outputs(items, output):
    """Stage all outputs first; roll back primaries if any promotion fails.

    This is a local single-writer transaction, not a distributed atomic commit.
    The immutable scratch generation and backups survive even a rollback error.
    """
    transaction = Path(tempfile.mkdtemp(prefix='transaction-', dir=output))
    existed = {}
    for name, source in items.items():
        target = output / name
        existed[name] = target.exists()
        shutil.copy2(source, transaction / name)
        if target.exists():
            shutil.copy2(target, transaction / (name + '.old'))
            history = output / 'history' / f'{target.stem}-{sha(target)}{target.suffix}'
            history.parent.mkdir(exist_ok=True)
            if not history.exists():
                shutil.copy2(target, history)
    promoted = []
    try:
        for name in items:
            os.replace(transaction / name, output / name)
            promoted.append(name)
    except OSError as failure:
        for name in reversed(promoted):
            if existed[name]:
                os.replace(transaction / (name + '.old'), output / name)
            else:
                (output / name).unlink()
        raise RuntimeError('Output promotion failed; prior primary outputs restored; scratch retained') from failure


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--no-numbers', action='store_true')
    ap.add_argument('--no-pdf', action='store_true')
    ap.add_argument('--overleaf', action='store_true')
    ap.add_argument('--install-missing', action='store_true', help='Allow MiKTeX to install missing free template packages')
    ap.add_argument('--output-dir', type=Path, default=HERE / 'build')
    a = ap.parse_args(argv)
    step('frozen contract', [sys.executable, '-B', 'check_checkpoint_contract.py'])
    if not a.no_numbers:
        step('numbers', [sys.executable, '-B', 'build_numbers.py'])
    step('numbers check', [sys.executable, '-B', 'build_numbers.py', '--check'])
    step('lint', [sys.executable, '-B', 'lint_report.py', 'report.tex'])
    for name, expected in STYLE_HASHES.items():
        if not (HERE / name).is_file() or sha(HERE / name) != expected:
            raise RuntimeError(f'Actual course template missing/changed: {name}; no bibliography fallback')
    output = a.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix='candidate-', dir=output))
    for name in UPLOAD:
        destination = scratch / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(HERE / name, destination)
    receipt = {'tickets': ['DLV-05', 'DLV-07'], 'created_at': datetime.now(timezone.utc).isoformat(),
               'state': 'source-bundle-only', 'inputs': {name: sha(scratch / name) for name in UPLOAD},
               'template_url': 'https://www.overleaf.com/read/swwcqhtsdwbg',
               'template_source_project': '6556cf1443f932295cf9d008',
               'visual_review': 'pending', 'published': False, 'submitted': False}
    if not a.no_pdf:
        xe, bt = shutil.which('xelatex'), shutil.which('bibtex')
        if not xe or not bt:
            raise RuntimeError('XeLaTeX/BibTeX unavailable; no PDF built. Use --no-pdf for sources only.')
        tex = [xe, '-interaction=nonstopmode', '-halt-on-error']
        if a.install_missing:
            tex.append('-enable-installer')
        tex.append('report.tex')
        for i, cmd in enumerate([tex, [bt, 'report'], tex, tex], 1):
            result = run(cmd, scratch, scratch / f'step{i}.log')
            if result.returncode:
                raise RuntimeError(f'Compilation failed in {scratch.name}/step{i}.log; last good PDF preserved\n' +
                                   '\n'.join((result.stdout + result.stderr).splitlines()[-20:]))
        log = (scratch / 'report.log').read_text('utf-8', errors='replace')
        # Long tables and the contents may need additional bounded passes.
        for extra in range(3):
            if 'Label(s) may have changed' not in log:
                break
            result = run(tex, scratch, scratch / f'convergence-{extra+1}.log')
            if result.returncode:
                raise RuntimeError('Cross-reference convergence compile failed; old outputs preserved')
            log = (scratch / 'report.log').read_text('utf-8', errors='replace')
        if re.search(r'Citation .* undefined|Reference .* undefined|There were undefined|Label\(s\) may have changed', log):
            raise RuntimeError('Unresolved citations/references or unstable labels; candidate not promoted')
        biblog = (scratch / 'report.blg').read_text('utf-8', errors='replace')
        if re.search(r"Warning--I didn't find|error message", biblog):
            raise RuntimeError('Bibliography resolution error; candidate not promoted')
        receipt.update(state='compiled-unreviewed', pdf_sha256=sha(scratch / 'report.pdf'),
                       pages=re.findall(r'Output written on report\.pdf \((\d+) pages?', log)[-1],
                       layout_warnings=re.findall(r'(?:Overfull|Underfull) [^\n]+', log))
    if a.overleaf:
        bundle = scratch / 'overleaf_upload.zip'
        with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED) as z:
            for name in UPLOAD:
                z.write(scratch / name, name)
        receipt['bundle_sha256'] = sha(bundle)
    (scratch / 'build-receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    items = {'build-receipt.json': scratch / 'build-receipt.json'}
    if not a.no_pdf:
        items['report.pdf'] = scratch / 'report.pdf'
    if a.overleaf:
        items['overleaf_upload.zip'] = scratch / 'overleaf_upload.zip'
    promote_outputs(items, output)
    print(json.dumps(receipt, indent=2))
    print(f'Scratch retained: {scratch}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        sys.exit(str(error))
