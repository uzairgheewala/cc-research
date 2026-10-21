"""tools/ci_check.py with evidence digests computed exactly as on CI (Linux), on any OS. Run by tools/hooks/pre-commit.

tracker/verify.py::digest hashes "<relative path>:<sha256>" lines for directory and glob evidence, using os.path.relpath
and sorting native path strings. On Windows that path has backslashes and sorts differently, so every directory item
(kernel/, calibration/, plans/results/ ...) "changed since its pin" there while CI agrees with the pin (20 Oct: the hook
blocked a commit that CI would have passed). This runs the same check with POSIX paths and POSIX order, which is what
the pins were taken with. jobs/patches/s33_verify_posix.py makes the same fix in verify.py itself (it is in sheet A's
identity); once verify.digest is POSIX-safe this file only runs ci_check unchanged."""
import hashlib
import os
import runpy
import sys
from pathlib import Path, PurePath

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tracker"))
import verify  # noqa: E402

POSIX_SAFE = getattr(verify, "DIGEST_POSIX", False)      # set by s33


def _rel(f, base):
    return PurePath(os.path.relpath(f, base)).as_posix()


def digest(ev):
    target = verify.resolve(ev)
    raw = ev.split(" (")[0].strip()
    if any(ch in raw for ch in "*?["):
        files = sorted(verify.glob.glob(str(target)), key=lambda f: Path(f).as_posix())
    elif target.is_dir():
        files = sorted((str(p) for p in target.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"),
                       key=lambda f: Path(f).as_posix())
        if len(files) > 2000:
            h = hashlib.sha256()
            for f in files:
                h.update(("%s:%d\n" % (_rel(f, target), os.path.getsize(f))).encode())
            return "tree:" + h.hexdigest(), len(files)
    elif target.is_file():
        return verify.sha(target), 1
    else:
        return None, 0
    if not files:
        return None, 0
    h = hashlib.sha256()
    for f in files:
        h.update(("%s:%s\n" % (_rel(f, verify.RESEARCH.parent), verify.sha(f))).encode())
    return "set:" + h.hexdigest(), len(files)


if not POSIX_SAFE:
    verify.digest = digest
sys.argv = [str(ROOT / "tools" / "ci_check.py")] + sys.argv[1:]
runpy.run_path(str(ROOT / "tools" / "ci_check.py"), run_name="__main__")
