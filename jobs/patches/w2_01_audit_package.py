"""w2-01 (31 Oct, chat W2): the audit package lands beside the B5 claim checker in audit/ (DLV-09).

Tickets: DLV-08, DLV-09, DLV-10, DLV-07
New files (owned by W2, written directly, not by this patch): audit/{core,protocol,metrics,controls,trace,systems,report,
rerun}/, audit/{__main__,run,collect,findings}.py, audit/PROTOCOL.md, audit/README.md, tests/test_audit_*.py,
tests/audit_fixtures/. This patch changes the two existing files the package touches:
  audit/__init__.py   docstring only: names both halves of the folder (the B5 modules are unchanged)
  tools/export_q1.py  ALLOW_AUDIT and --with-audit (off by default, so W1's 6 Nov checkpoint export does not change)
Repins after review: whichever tickets pin these two files (verify.py names them); then snapshot.py last.
Named w2-01, not s38, so it cannot collide with W5's patch numbers.
Run once from cc-research: python3 jobs/patches/w2_01_audit_package.py   (refuses twice, or on an unexpected old file)."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEW = Path(__file__).resolve().parent / "w2_01"
FILES = {"audit/__init__.py": ("a974ce921bf7f2883d87d9a3df50a49e2b1e24cf102ca07c27d84cc1e019f217", "audit__init__.py"),
         "tools/export_q1.py": ("466af0f53a9dcb77e66718384680d41dd8a9776cca0b9fad98ba9169af0615be", "export_q1.py")}
sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
plan = []
for rel, (old, src) in FILES.items():
    dst, new = ROOT / rel, (NEW / src).read_bytes()
    cur = sha(dst.read_bytes())
    assert cur != sha(new), "%s: already applied" % rel
    assert cur == old, "%s is not the version this patch was written for (%s)" % (rel, cur[:12])
    plan.append((dst, new, cur))
for dst, new, cur in plan:                       # every check passes before anything is written
    dst.write_bytes(new)
    print("w2-01: %s %s -> %s" % (dst.relative_to(ROOT).as_posix(), cur[:12], sha(new)[:12]))
