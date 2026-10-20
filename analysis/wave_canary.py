"""Wave canary (INF-10): recompute a few ledgers from scratch on this machine and compare their hashes with the agent's.

Tickets: INF-10

    python analysis/wave_canary.py --expect jobs/waves/A/canary_expected.json --out jobs/waves/A/out/canary.json
    python analysis/wave_canary.py --write --files F1 F2 ... --expect jobs/waves/A/canary_expected.json   (agent side)

Engines run fresh (a private, empty cache folder), so the check covers this machine's BLAS kernel, thread settings and
package builds, not just the shipped cache. Two digests per file:
  claims_sha256   the ledger's claims as structure (id, relation, direction source, licence, data-only relation, engines,
                  conflict): what every downstream number depends on. This decides `match`.
  ledger_sha256   the full ledger hash, which also covers test statistics; it differs between CPUs whose NumPy / OpenBLAS
                  kernels round differently (wave A, 20 Oct: an AVX2 host differs from the AVX-512 sandbox even with
                  OPENBLAS_CORETYPE pinned). Reported as `ledger_hash_match`, not judged.
"""
import argparse, hashlib, json, os, sys, tempfile
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(ROOT / "analysis"))


def ledger_hash(path, cache_root):
    import causalarena_load as L
    from kernel import build as B, cache
    s = L.load_any(path)
    eng = cache.engines(s["values"], list(s["node_ids"]), root=cache_root)
    led, _ = B.build(s["values"], list(s["node_ids"]), rule="C3", eng=eng, created_utc="")
    claims = sorted((c["id"], c["relation"], c.get("direction_source"), c.get("licensed_by"), c.get("data_only_relation"),
                     c.get("engines"), bool(c.get("conflict"))) for c in (led["claims"] if led else []))
    return {"file_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            "claims_sha256": hashlib.sha256(json.dumps(claims).encode()).hexdigest(),
            "ledger_sha256": led["report"]["ledger_sha256"] if led else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", required=True)
    ap.add_argument("--out", default="")
    ap.add_argument("--files", nargs="*", default=[])
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        if a.write:
            got = {str(Path(f).resolve().relative_to(ROOT)).replace("\\", "/"): ledger_hash(f, tmp) for f in a.files}
            exp = {"files": got, "digest": hashlib.sha256(json.dumps(got, sort_keys=True).encode()).hexdigest(),
                   "openblas_coretype": os.environ.get("OPENBLAS_CORETYPE")}
            Path(a.expect).write_text(json.dumps(exp, indent=1))
            print(json.dumps(exp, indent=1))
            return 0
        exp = json.loads(Path(a.expect).read_text())
        got, missing = {}, []
        for rel in exp["files"]:
            p = ROOT / rel
            if not p.exists():
                missing.append(rel)
                continue
            got[rel] = ledger_hash(p, tmp)
    same = {rel: (got[rel]["file_sha256"], got[rel]["claims_sha256"]) == (exp["files"][rel]["file_sha256"], exp["files"][rel]["claims_sha256"])
            for rel in got}
    hsame = {rel: got[rel]["ledger_sha256"] == exp["files"][rel]["ledger_sha256"] for rel in got}
    out = {"tickets": ["INF-10"], "match": bool(got) and all(same.values()) and not missing, "per_file": same,
           "ledger_hash_match": hsame,
           "missing": missing, "digest": hashlib.sha256(json.dumps(got, sort_keys=True).encode()).hexdigest(),
           "expected_digest": exp["digest"], "openblas_coretype": os.environ.get("OPENBLAS_CORETYPE"), "got": got}
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("match", "per_file", "ledger_hash_match", "missing", "openblas_coretype")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
