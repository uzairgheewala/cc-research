"""Validate checkpoint inputs in a data-free staged/CI tree (DLV-05, DLV-07).

Only the two pinned, public data-shape metadata summaries are materialized;
raw excluded datasets/runs are neither copied nor implied to be reproduced.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/'docs/paper/q1'
manifest=PAPER/'checkpoint_contract.json'
if not manifest.exists():
    if (PAPER/'report.tex').exists():raise SystemExit('Paper is staged without its evidence contract')
    print('checkpoint: no paper in this staged tree yet')
    raise SystemExit(0)
contract=json.loads(manifest.read_text(encoding='utf-8'))
for name,digest in contract['number_source_sha256'].items():
    if not name.startswith('external/'):continue
    if not name.startswith('external/causalbench/') or not name.endswith('_filtered.npz.json'):
        raise SystemExit('Unexpected excluded checkpoint metadata path: '+name)
    source=ROOT/'docs/migrations/checkpoint-metadata'/name
    if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:raise SystemExit('Metadata snapshot hash mismatch: '+name)
    target=ROOT/name
    if not target.exists():
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(source.read_bytes())
subprocess.run([sys.executable,'-B',str(PAPER/'check_checkpoint_contract.py')],cwd=ROOT,check=True)
subprocess.run([sys.executable,'-B',str(PAPER/'lint_report.py')],cwd=ROOT,check=True)
if (PAPER/'releases/checkpoint-2026-11-06/manifest.json').exists():
    subprocess.run([sys.executable,'-B',str(PAPER/'verify/verify_checkpoint_release.py')],cwd=ROOT,check=True)
    subprocess.run([sys.executable,'-B','-m','unittest','discover','-s',str(PAPER/'verify'),'-p','test_*.py'],cwd=ROOT,check=True)
