"""Apply Uzair's 3 Nov local-commit authorization to the W2 handoff rules once."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
path = ROOT / "audit/AGENTS.md"
expected = "fb76fc8a467ee3b10088c925cbef49aab7e7afeda2c9d708486659cd7a388dd1"
raw = path.read_bytes()
if hashlib.sha256(raw).hexdigest() != expected:
    raise SystemExit("audit/AGENTS.md changed or this patch already ran; refusing")
old = b"- Write commit messages to `docs/commit_msgs/<execution>_cc-research.txt`. Uzair commits. Never run git write commands."
new = (b"- Automatic local milestone commits are authorized by Uzair (3 Nov 2026). Follow the root milestone-commit workflow.\n"
       b"  The migration hold applies until this package is in its own repository. Do not push or publish without authorization.\n"
       b"  This replaces older no-git/Uzair-commits wording in historical handoffs; preserve those historical documents.")
if raw.count(old) != 1:
    raise SystemExit("Expected exactly one old commit instruction")
newline = b"\r\n" if b"\r\n" in raw else b"\n"
path.write_bytes(raw.replace(old, new.replace(b"\n", newline)))
print("Updated audit local-commit policy; no Git commands or commits executed")
