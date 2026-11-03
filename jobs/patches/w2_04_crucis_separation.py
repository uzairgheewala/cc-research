"""Apply the authorized, verified Crucis cutover once (DLV-09, INF-06, BLD-11).

All source paths/hashes are inventoried; every removed file is backed up first.
No commits, remote writes or scientific evidence changes are made by this script.
"""
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]
WORKSPACE=ROOT.parent
CRUCIS=WORKSPACE/'crucis'
MIGRATION=WORKSPACE/'_repo_migration/2026-11-03'
RECEIPT=ROOT/'docs/migrations/crucis-separation.json'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
if RECEIPT.exists():raise SystemExit('Cutover already recorded; refuse twice')
if not (CRUCIS/'.git').is_dir():raise SystemExit('Standalone Crucis repository missing')
checks={
    'offline':'crucis-offline-tests-fixed.json',
    'data_backed':'crucis-data-backed-final.json',
    'installed':'installed_crucis_probe.json',
    'certificates':'stage2_certificates.json',
}
checked={}
for name,file in checks.items():
    p=MIGRATION/file;data=json.loads(p.read_text(encoding='utf-8'))
    ok=data.get('ok',data.get('pass',data.get('installed_from_wheel',False)))
    if not ok:raise SystemExit('Required check failed: '+file)
    checked[name]={'receipt':file,'sha256':sha(p)}
comparison=json.loads((MIGRATION/'crucis-rerun/comparison.json').read_text(encoding='utf-8'))['summary']['all']
if comparison['compared']!=1298 or not comparison['pass']:raise SystemExit('Numerical compatibility failed')
inventory=json.loads((ROOT/'docs/migrations/crucis-2026-11-03-source-inventory.json').read_text())['files']
targets=json.loads((MIGRATION/'stage2_cutover_targets.json').read_text(encoding='utf-8'))
move=[]
for row in inventory:
    path=(ROOT/row['source']).resolve()
    if not path.is_relative_to(ROOT):raise SystemExit('Source escapes research repository')
    if sha(path)!=row['source_sha256']:raise SystemExit('Concurrent source change: '+row['source'])
    if row['source'].startswith(('audit/','tests/')) and row['source'] not in targets and row['source']!='audit/__init__.py':
        move.append((path,row))
for name,info in targets.items():
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT) or sha(path)!=info['sha256']:raise SystemExit('Guarded metadata changed: '+name)
backup=MIGRATION/'stage2-before'
for path,row in move:
    dest=backup/row['source'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dest)
    if sha(dest)!=row['source_sha256']:raise SystemExit('Backup mismatch: '+str(path))
for name,info in targets.items():
    path=ROOT/name;dest=backup/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dest)
for name,info in targets.items():(ROOT/name).write_text(info['text'],encoding='utf-8')
for path,row in move:
    if not path.resolve().is_relative_to(ROOT):raise SystemExit('Unsafe removal target')
    path.unlink()  # Named inventoried file only; no recursive deletion.
receipt={'tickets':['DLV-09','DLV-10','INF-06','BLD-11'],'date':'2026-11-03',
    'standalone_repository':'../crucis','namespace':'crucis','evidence_env':'CRUCIS_DATA_ROOT',
    'source_inventory':'docs/migrations/crucis-2026-11-03-source-inventory.json',
    'moved_files':len(move),'backup_workspace_path':'_repo_migration/2026-11-03/stage2-before',
    'checks':checked,'numerical_comparison':comparison,
    'historical_b5_and_audit_results_retained':True,'checkpoint_inputs_preserved':True,
    'initial_commit_hold':'lifted by verified cutover','remote_publication':False}
RECEIPT.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
(CRUCIS/'provenance/separation.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print('Verified cutover complete: %d source files moved; local commit hold lifted' % len(move))
