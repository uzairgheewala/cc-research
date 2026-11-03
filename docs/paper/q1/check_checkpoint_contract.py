"""Check the frozen Q1 evidence boundary without refreshing it (DLV-05, DLV-07).

Run from cc-research: python -B docs/paper/q1/check_checkpoint_contract.py
This checks integrity and numerical consistency, not scientific wording or submission.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


PAPER = Path("docs/paper/q1")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(root):
    contract = json.loads((root / PAPER / "checkpoint_contract.json").read_text(encoding="utf-8"))
    errors = []
    if contract.get("schema_version") != 1:
        return ["unsupported checkpoint contract schema"], contract
    for rel, expected in contract["frozen_files"].items():
        path = (root / rel).resolve()
        if not path.is_relative_to(root):
            errors.append("frozen path escapes research root: " + rel)
        elif not path.is_file():
            errors.append("missing frozen file: " + rel)
        elif digest(path) != expected:
            errors.append("frozen bytes changed: " + rel)
    lock = json.loads((root / PAPER / "numbers.lock.json").read_text(encoding="utf-8"))
    if lock["values"] != contract["number_values"]:
        errors.append("number-lock keys or formatted values differ from checkpoint baseline")
    source_hashes = {path: data["sha256"] for path, data in lock["sources"].items()}
    if source_hashes != contract["number_source_sha256"]:
        errors.append("number-lock source set or hashes differ from checkpoint baseline")
    registry = json.loads((root / PAPER / "numbers.json").read_text(encoding="utf-8"))
    keys = [entry["key"] for entry in registry["entries"]]
    grouped = [key for claim in contract["claim_groups"] for key in claim["number_keys"]]
    if len(keys) != len(set(keys)) or len(grouped) != len(set(grouped)) or set(keys) != set(grouped):
        errors.append("claim groups must cover every registry key exactly once")
    # HEAD and per-source Git state can change as authorized local commits land.
    # Their capture-time values are provenance, not a ban on subsequent commits.
    if not errors:
        command = [sys.executable, "-B", str(root / PAPER / "build_numbers.py"), "--root", str(root), "--check"]
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8")
        if result.returncode:
            errors.append("existing number check failed: " + (result.stdout + result.stderr).strip())
    return errors, contract


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    try:
        errors, contract = check(args.root.resolve())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("CHECKPOINT CONTRACT FAILED: " + str(exc))
        return 1
    if errors:
        for error in errors:
            print("CHECKPOINT CONTRACT FAILED: " + error)
        return 1
    print("checkpoint contract: %s; %d keys, %d number sources, %d frozen files; OK" % (
        contract["contract_id"], len(contract["number_values"]),
        len(contract["number_source_sha256"]), len(contract["frozen_files"])))
    print("Scope/evidence freeze only; paper corrections, publication and submission have separate gates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
