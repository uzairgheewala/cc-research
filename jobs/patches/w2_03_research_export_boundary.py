"""Keep the course export research-only as the auditor becomes a separate project.

Uzair authorized this boundary on 3 Nov 2026. The sole previous exporter change
was the optional W2 audit-package export; its exact bytes remain in w2_01's
payload and the migration backup. Recover the original research exporter only
when both that reviewed input and the original DLV-07 pin agree.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
target = ROOT / "tools/export_q1.py"
expected = "345e60638dc34190765b04f0f269a106ddb7a4b0639eed02c05a73f562a21f47"
if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
    raise SystemExit("Exporter changed or patch already applied; refusing")
original = subprocess.check_output(["git", "-C", str(ROOT), "show", "cf536c1:tools/export_q1.py"])
pin = json.loads((ROOT / "tracker/pins.json").read_text(encoding="utf-8"))["DLV-07|tools/export_q1.py"]["digest"]
if hashlib.sha256(original).hexdigest() != pin:
    raise SystemExit("Original exporter does not match the reviewed DLV-07 pin")
target.write_bytes(original)
print("Restored research-only course export; exact DLV-07 pin matches; no export or commit was run")
