"""K0 engine cache (kernel v3). The engines are the only slow step of a build (GES ~7 s and a ~20 s causal-learn import
per process, against < 0.5 s for everything after them), and their output depends only on the canonical table. This
module stores that output once and hands it back to kernel.build.build(eng=...), so every rule, knowledge, granularity
and calibration experiment runs on cached engine records.

  eng = cache.engines(X, names)            # run_engines() on a miss, the stored result on a hit
  led, info = build.build(X, names, rule="C3", eng=eng, ...)

Key (binding time: fixed when the entry is written; invalidated only by a change of any part):
  data_sha     sha256 of the canonical table before jitter (kernel.build.run_engines's own data_sha). Names and the
               caller's column order cannot reach it: identical columns are byte-identical, so their tie-break order
               leaves the table unchanged.
  manifest     sha256 of engines/MANIFEST.json (engine versions, source-tree hashes, settings)
  settings     alpha, GES on/off, GES timeout, jitter-seed rule
The entry holds every field kernel.build reads from run_engines(): PC's recorded tests, marks and stages, GES's marks,
score and failure, the jitter seed and the deviation text. A hit is recomputed from the stored fields; the table itself is
re-derived from the caller's data (and re-jittered with the stored seed), and its hash is checked against the key, so a
corrupted or mismatched entry is an error, never a silent substitution.

Failure modes named in advance (docs/design/q2_kernel_v3_design.md, K0):
  * key too coarse (two tables, one entry): the key is the full table hash plus manifest and settings;
  * stale engines: the manifest hash is in the key;
  * jitter mismatch: the jitter seed is stored and the jittered table's hash is checked on every hit;
  * BLAS threads and kernels: the thread environment and OPENBLAS_CORETYPE are in the key. Both change floating-point
    summation, so p-values differ in the 14th digit and every ledger hash changes. Found on the first K0 check: the host
    changed between the v2 runs (OpenBLAS detected SkylakeX) and v3 (it fell back to Prescott); SKYLAKEX reproduces v2;
  * timing in the ledger: engine seconds are stored and reported; the ledger hash covers variables, evidence, knowledge,
    claims and overrides only, so a hit reproduces the ledger hash exactly (K0 must-show 1).
"""
import gzip, hashlib, json, os, zlib
from pathlib import Path

import numpy as np

from engines.core import EngineResult

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = Path(os.environ.get("CC_ENGINE_CACHE", str(ROOT / "cache" / "engines")))
FORMAT = "cc-engine-cache/1"


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def manifest_sha():
    return _sha((ROOT / "engines" / "MANIFEST.json").read_bytes())


THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_CORETYPE")


def settings(with_ges=True, ges_timeout_s=600, alpha=0.05, ges_lambda_scale=1.0):
    """The BLAS thread count is part of the key: it changes floating-point summation order, so p-values written under
    different thread counts differ in the last digits (seen on the first K0 check: 1e-14 differences in every p-value)."""
    return {"alpha": alpha, "with_ges": bool(with_ges), "ges_timeout_s": ges_timeout_s, "jitter": "sd 1e-6, seed crc32(data_sha) unless given",
            "threads": {k: os.environ.get(k) for k in THREAD_VARS},
            **({"ges_lambda_scale": ges_lambda_scale} if ges_lambda_scale != 1.0 else {})}


def canonical(X, names):
    from kernel import build as B
    X = np.asarray(X, dtype=float)
    _, order = B.variables(X, [str(n) for n in names])
    Xc = X[:, order]
    return order, Xc, _sha(np.ascontiguousarray(Xc, dtype="<f8").tobytes())


def key(data_sha, st, man=None):
    man = man or manifest_sha()
    return _sha(("%s|%s|%s" % (FORMAT, man, json.dumps(st, sort_keys=True))).encode())[:16] + "-" + data_sha


def path_for(k, root=None):
    root = Path(root or DEFAULT_DIR)
    return root / k[:2] / (k + ".json.gz")


def _res_to_json(r):
    if r is None:
        return None
    return {"engine": r.engine, "ok": bool(r.ok),
            "marks": None if r.marks is None else np.asarray(r.marks).astype(int).tolist(),
            "stages": {k: np.asarray(v).astype(int).tolist() for k, v in (r.stages or {}).items()},
            "tests": [[ph, int(i), int(j), [int(s) for s in S], float(p)] for ph, i, j, S, p in (r.tests or [])],
            "score": None if r.score is None else float(r.score), "seconds": float(r.seconds or 0.0), "failure": r.failure}


def _res_from_json(d):
    if d is None:
        return None
    return EngineResult(engine=d["engine"], ok=d["ok"],
                        marks=None if d["marks"] is None else np.array(d["marks"], dtype=int),
                        stages={k: np.array(v, dtype=int) for k, v in d["stages"].items()},
                        tests=[(ph, i, j, tuple(S), p) for ph, i, j, S, p in d["tests"]],
                        score=d["score"], seconds=d["seconds"], failure=d["failure"])


def save(eng, k, st, root=None):
    p = path_for(k, root)
    p.parent.mkdir(parents=True, exist_ok=True)
    rec = {"format": FORMAT, "key": k, "settings": st, "manifest_sha256": manifest_sha(), "data_sha256": eng["data_sha"],
           "jittered": eng["jittered"] if eng["jittered"] is not False else False,
           "Xc_sha256": _sha(np.ascontiguousarray(eng["Xc"], dtype="<f8").tobytes()),
           "deviations": [dict(d, utc="") for d in eng["deviations"]],
           "pc": _res_to_json(eng["pc"]), "ges": _res_to_json(eng["ges"])}
    tmp = p.with_suffix(".tmp")
    with gzip.open(tmp, "wt", encoding="utf-8") as fh:
        json.dump(rec, fh, separators=(",", ":"))
    os.replace(tmp, p)
    return p


def load(k, order, Xc_raw, created_utc="", root=None):
    p = path_for(k, root)
    if not p.exists():
        return None
    with gzip.open(p, "rt", encoding="utf-8") as fh:
        rec = json.load(fh)
    if rec.get("format") != FORMAT or rec.get("key") != k:
        raise RuntimeError("engine cache entry %s has the wrong format or key" % p)
    Xc = Xc_raw
    if rec["jittered"] is not False:
        Xc = Xc_raw + 1e-6 * np.random.default_rng(rec["jittered"]).standard_normal(Xc_raw.shape)
    if _sha(np.ascontiguousarray(Xc, dtype="<f8").tobytes()) != rec["Xc_sha256"]:
        raise RuntimeError("engine cache entry %s does not match this table (hash of the engine input differs)" % p)
    return {"order": order, "Xc": Xc, "data_sha": rec["data_sha256"], "pc": _res_from_json(rec["pc"]), "ges": _res_from_json(rec["ges"]),
            "jittered": rec["jittered"], "deviations": [dict(d, utc=created_utc or "") for d in rec["deviations"]], "cached": k}


STATS = {"hit": 0, "miss": 0}


def engines(X, names, with_ges=True, ges_timeout_s=600, created_utc="", root=None, read_only=False, ges_lambda_scale=1.0):
    """run_engines() through the cache. read_only=True raises on a miss (harness runs that must not start engines).
    ges_lambda_scale != 1 runs the GES penalty variant (engines.variants); 1 is v2's engine, byte-identical."""
    from kernel import build as B
    order, Xc_raw, data_sha = canonical(X, names)
    st = settings(with_ges, ges_timeout_s, B.ALPHA, ges_lambda_scale)
    k = key(data_sha, st)
    eng = load(k, order, Xc_raw, created_utc, root)
    if eng is not None:
        STATS["hit"] += 1
        return eng
    if read_only:
        raise LookupError("engine cache miss for table %s (fill the cache first: python -m kernel.harness fill)" % data_sha[:12])
    STATS["miss"] += 1
    if ges_lambda_scale == 1.0:
        eng = B.run_engines(X, names, with_ges=with_ges, ges_timeout_s=ges_timeout_s, created_utc=created_utc)
    else:
        from engines import variants
        eng = B.run_engines(X, names, with_ges=False, created_utc=created_utc)
        if eng["pc"].ok and with_ges:
            eng["ges"] = variants.run_ges_pen(eng["Xc"], ges_lambda_scale, timeout_s=ges_timeout_s)
    assert eng["data_sha"] == data_sha and list(eng["order"]) == list(order)
    save(eng, k, st, root)
    eng = dict(eng, cached=None)
    return eng


def has(X, names, with_ges=True, ges_timeout_s=600, root=None):
    from kernel import build as B
    _, _, data_sha = canonical(X, names)
    return path_for(key(data_sha, settings(with_ges, ges_timeout_s, B.ALPHA)), root).exists()
