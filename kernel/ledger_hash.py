"""The ledger hash rule, taken from ledger/verify.py (v0.1, hashed evidence) so kernel and verifier cannot drift."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("_ledger_verify01", Path(__file__).resolve().parent.parent / "ledger" / "verify.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
canonical_hash = _mod.canonical_hash
