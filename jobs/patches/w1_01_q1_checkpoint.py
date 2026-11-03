"""w1-01 (31 Oct, chat W1): re-cut docs/q1/checkpoint_skeleton.md to the auditor paper (program v3, section 2).

Tickets: DLV-05, BND-13, DLV-07, DLV-11
The checkpoint now lives in docs/paper/q1/ (report.tex, numbers.json, lit_claims.json; design in DESIGN.md). The skeleton
becomes the index to it plus the final-report outline. BND-13 pins the skeleton, so verify.py --repin BND-13 follows.
Named w1-01, not s38, so it cannot collide with W5's patch numbers.
Run once from cc-research: python3 jobs/patches/w1_01_q1_checkpoint.py   (refuses twice, or on an unexpected old file)."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD_SHA = "3bcaaa561bdfbe7dfeb8597360b823b4db7b344f15a998bb1bb054b4f1d4fed9"
NEW = Path(__file__).resolve().parent / "w1_01" / "checkpoint_skeleton.md"
dst = ROOT / "docs" / "q1" / "checkpoint_skeleton.md"
cur = hashlib.sha256(dst.read_bytes()).hexdigest()
new = NEW.read_bytes()
assert cur != hashlib.sha256(new).hexdigest(), "already applied"
assert cur == OLD_SHA, "docs/q1/checkpoint_skeleton.md is not the 27 Oct version this patch was written for (%s)" % cur[:12]
dst.write_bytes(new)
print("w1-01 applied: docs/q1/checkpoint_skeleton.md re-cut (%s -> %s)" % (cur[:12], hashlib.sha256(new).hexdigest()[:12]))
