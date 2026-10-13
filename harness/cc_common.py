"""Shared helpers for the Causal-Copilot research harness.

Lives OUTSIDE the Causal-Copilot repo. Nothing here edits repo source files.
"""
import argparse
import dataclasses
import fnmatch
import hashlib
import json
import os
import pickle
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
RESEARCH = HARNESS_DIR.parent
REPO = Path(os.environ.get("CC_REPO", "/app")).resolve()
MANIFEST = RESEARCH / "manifests" / "baseline_a31aa7c.sha256"
# sha256 of the manifest file itself (tree at upstream commit a31aa7c, zip unpack, .env excluded)
EXPECTED_MANIFEST_DIGEST = "725e06274856c2187c2a650b1a7217968d633c03baca292609d505e4429fbacf"
BASELINE_COMMIT = "a31aa7c"

# Files a run is known/allowed to create inside the repo. Anything else new is reported.
ALLOWED_EXTRA = [
    ".env",
    "output/*",
    "causal_discovery/context/hp_rerank_prompt_test.txt",
    "__pycache__/*", "*/__pycache__/*", "*.pyc",
    ".pytest_cache/*", ".ruff_cache/*",
]
PLACEHOLDER_KEYS = {"", "your_openai_api_key_here", "your_openrouter_api_key_here"}


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


_HASH_CACHE = {}


def _hash_cached(path, use_cache):
    """sha256 of a file; with use_cache, reuse an earlier hash when size and mtime are unchanged."""
    st = os.stat(path)
    key = str(path)
    sig = (st.st_size, st.st_mtime_ns)
    if use_cache and key in _HASH_CACHE and _HASH_CACHE[key][0] == sig:
        return _HASH_CACHE[key][1]
    digest = sha256_file(path)
    _HASH_CACHE[key] = (sig, digest)
    return digest


def verify_tree(repo=REPO, manifest=MANIFEST, use_cache=False):
    """Compare the repo tree with the recorded baseline. Read-only.

    use_cache=False hashes every file (used before a run). use_cache=True re-hashes only files whose
    size or modification time changed since the earlier check in this process (used after a run)."""
    out = {"repo": str(repo), "manifest": str(manifest), "baseline_commit": BASELINE_COMMIT,
           "manifest_digest_ok": False, "n_listed": 0, "missing": [], "changed": [],
           "extra_allowed": 0, "extra_unexpected": [], "ok": False}
    if not manifest.is_file():
        out["error"] = "manifest file not found"
        return out
    out["manifest_digest_ok"] = (sha256_file(manifest) == EXPECTED_MANIFEST_DIGEST)
    listed = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        if rel.startswith("./"):
            rel = rel[2:]
        listed[rel] = digest
    out["n_listed"] = len(listed)
    for rel, digest in listed.items():
        p = repo / rel
        if not p.is_file():
            out["missing"].append(rel)
        elif _hash_cached(p, use_cache) != digest:
            out["changed"].append(rel)
    for root, _dirs, files in os.walk(repo):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), repo).replace(os.sep, "/")
            if rel in listed:
                continue
            if any(fnmatch.fnmatch(rel, pat) for pat in ALLOWED_EXTRA):
                out["extra_allowed"] += 1
            else:
                out["extra_unexpected"].append(rel)
    out["ok"] = bool(out["manifest_digest_ok"] and not out["missing"] and not out["changed"])
    return out


class Scrubber:
    """Replaces secret values with a marker in anything written to disk or console."""

    def __init__(self):
        self.secrets = []

    def refresh(self):
        self.secrets = []
        for name in ("OPENAI_API_KEY", "OPENROUTER_API_KEY"):
            v = os.environ.get(name, "")
            if v and v not in PLACEHOLDER_KEYS and len(v) >= 8:
                self.secrets.append((v, "<REDACTED:%s>" % name))

    def __call__(self, text):
        for v, marker in self.secrets:
            if v in text:
                text = text.replace(v, marker)
        return text


def key_status(name="OPENAI_API_KEY"):
    v = os.environ.get(name)
    if v is None:
        return "missing"
    if v.strip() in PLACEHOLDER_KEYS:
        return "placeholder"
    return "set"


def _df_descriptor(df):
    import pandas as pd
    try:
        h = hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values.tobytes()).hexdigest()
    except Exception as e:  # mixed / unhashable content
        h = "unhashable: %r" % (e,)
    return {"__dataframe__": True, "shape": list(df.shape),
            "columns": [str(c) for c in list(df.columns)[:500]], "sha256": h}


def to_jsonable(obj, _depth=0):
    """Best-effort, lossy conversion to JSON-friendly data (for human-readable summaries)."""
    if _depth > 12:
        return repr(obj)[:500]
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    try:
        import numpy as np
        if isinstance(obj, np.generic):
            return obj.item()
        if isinstance(obj, np.ndarray):
            if obj.size <= 20000:
                try:
                    return {"__ndarray__": True, "shape": list(obj.shape), "dtype": str(obj.dtype),
                            "data": obj.tolist()}
                except Exception:
                    pass
            return {"__ndarray__": True, "shape": list(obj.shape), "dtype": str(obj.dtype),
                    "sha256": hashlib.sha256(obj.tobytes()).hexdigest()}
    except ImportError:
        pass
    try:
        import pandas as pd
        if isinstance(obj, pd.DataFrame):
            return _df_descriptor(obj)
        if isinstance(obj, pd.Series):
            return {"__series__": True, "len": int(len(obj)), "name": str(obj.name)}
        if isinstance(obj, pd.Index):
            return [str(x) for x in obj[:500]]
    except ImportError:
        pass
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v, _depth + 1) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [to_jsonable(v, _depth + 1) for v in obj]
    if isinstance(obj, argparse.Namespace):
        return {"__namespace__": True, **{k: to_jsonable(v, _depth + 1) for k, v in vars(obj).items()}}
    if hasattr(obj, "model_dump") and callable(obj.model_dump):
        try:
            return {"__pydantic__": type(obj).__name__, **to_jsonable(obj.model_dump(), _depth + 1)}
        except Exception:
            pass
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {"__dataclass__": type(obj).__name__,
                **{k: to_jsonable(v, _depth + 1) for k, v in vars(obj).items()}}
    if type(obj).__name__ == "DictAsObject" and hasattr(obj, "_data"):
        return {"__dict_as_object__": True, **to_jsonable(obj._data, _depth + 1)}
    if isinstance(obj, bytes):
        return {"__bytes__": len(obj)}
    return {"__repr__": type(obj).__name__, "value": repr(obj)[:2000]}


def safe_copy(obj, _depth=0):
    """Deep, picklable copy for artifacts. DataFrames become descriptors (shape, columns, hash)."""
    if obj is None or isinstance(obj, (bool, int, float, str, bytes)):
        return obj
    if _depth > 12:
        return repr(obj)[:500]
    try:
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.copy()
        if isinstance(obj, np.generic):
            return obj.item()
    except ImportError:
        pass
    try:
        import pandas as pd
        if isinstance(obj, pd.DataFrame):
            return _df_descriptor(obj)
    except ImportError:
        pass
    if isinstance(obj, dict):
        return {safe_copy(k, _depth + 1) if isinstance(k, tuple) else k: safe_copy(v, _depth + 1)
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [safe_copy(v, _depth + 1) for v in obj]
    if isinstance(obj, tuple):
        return tuple(safe_copy(v, _depth + 1) for v in obj)
    if isinstance(obj, (set, frozenset)):
        return [safe_copy(v, _depth + 1) for v in obj]
    if isinstance(obj, argparse.Namespace):
        return {"__namespace__": True, **{k: safe_copy(v, _depth + 1) for k, v in vars(obj).items()}}
    if all(hasattr(obj, a) for a in ("user_data", "statistics", "results", "algorithm")):
        return {"__global_state__": "not copied here; see the state/ snapshots of this run"}
    try:
        data = pickle.dumps(obj, protocol=4)
        if len(data) <= 2_000_000:
            return pickle.loads(data)
    except Exception:
        pass
    return {"__repr__": type(obj).__name__, "value": repr(obj)[:2000]}


def dump_json(path, obj, scrub=None):
    text = json.dumps(obj, indent=2, default=repr, ensure_ascii=False)
    if scrub:
        text = scrub(text)
    Path(path).write_text(text, encoding="utf-8")
