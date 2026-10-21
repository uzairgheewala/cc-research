"""s33: tracker/verify.py::digest hashes POSIX relative paths in POSIX order, so a directory or glob evidence digest is
the same on Windows as on CI (Linux). Before this, on Windows every directory item showed "changed since its pin"
(20 Oct: the pre-commit hook blocked a commit on kernel/, calibration/, plans/results/). Linux digests do not change:
pins stay valid. tools/hooks/ci_check_portable.py covers the hook until this is applied.

Run once from cc-research after sheet A's return is packed (tracker/verify.py is in jobs/waves/A/identity.sha256):
    py -3 jobs\\patches\\s33_verify_posix.py   then   py -3 tools\\ci_check.py   (0 errors, on Windows too)"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "tracker" / "verify.py"
EDITS = [
    ('def digest(ev):\n',
     'DIGEST_POSIX = True   # s33: digests use POSIX relative paths and POSIX order on every OS\n\n\n'
     'def _posix_rel(f, base):\n    return Path(os.path.relpath(f, base)).as_posix()\n\n\ndef digest(ev):\n'),
    ('        files = sorted(glob.glob(str(target)))\n',
     '        files = sorted(glob.glob(str(target)), key=lambda f: Path(f).as_posix())\n'),
    ('        files = sorted(str(p) for p in target.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")\n',
     '        files = sorted((str(p) for p in target.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"),\n'
     '                       key=lambda f: Path(f).as_posix())\n'),
    ('                h.update(("%s:%d\\n" % (os.path.relpath(f, target), os.path.getsize(f))).encode())\n',
     '                h.update(("%s:%d\\n" % (_posix_rel(f, target), os.path.getsize(f))).encode())\n'),
    ('        h.update(("%s:%s\\n" % (os.path.relpath(f, RESEARCH.parent), sha(f))).encode())\n',
     '        h.update(("%s:%s\\n" % (_posix_rel(f, RESEARCH.parent), sha(f))).encode())\n'),
]
t = P.read_bytes().decode("utf-8")
assert "DIGEST_POSIX" not in t, "already applied"
for old, new in EDITS:
    assert t.count(old) == 1, "anchor not found once: " + old[:70]
    t = t.replace(old, new, 1)
P.write_bytes(t.encode("utf-8"))
print("updated tracker/verify.py")
