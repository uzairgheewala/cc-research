"""Engine manifest (D0.1): versions, source-tree hashes and settings, fixed before any kernel run.

  python -m engines.manifest --causal-learn PATH [--write]      print (and with --write, store) engines/MANIFEST.json
  python -m engines.manifest --causal-learn PATH --check        exit 1 if the environment differs from MANIFEST.json

A package's tree hash is sha256 over "relative path\\0sha256(file)\\n" for every .py file in the package, sorted by path.
Changing an engine, a version or a setting means a new manifest and a re-run of B0's oracle and permutation checks
(binding time: approach_v1.md section 3).
"""
import argparse, hashlib, json, os, platform, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SETTINGS = {
    "pc_maxp": {"alpha": 0.05, "indep_test": "fisherz", "stable": True, "uc_rule": 1, "uc_priority": 3,
                "call": "causallearn.search.ConstraintBased.PC.pc(X, 0.05, 'fisherz', stable=True, uc_rule=1, uc_priority=3)"},
    "ges_bic": {"package": "ges", "call": "ges.fit_bic(Z), Z = column z-scores", "lambda": "log(n)/2", "phases": ["forward", "backward", "turning"]},
    "gies": {"package": "gies", "call": "gies.fit_bic(data, targets), one environment per intervened-cell pattern",
             "jitter_sd": 1e-6, "jitter_seed": "crc32(file name)"},
    "canonical_order": "columns sorted by sha256 of their float64 little-endian values; ties (identical columns) by original position",
    "threads": 1,
    "singular_data": "a singular correlation matrix is a typed failure 'singular'; the kernel may retry once with seeded Gaussian jitter "
                     "sd 1e-6 (the GIES baseline's rule) and records the retry in the run report",
}
PINS = {"python": "3.11", "numpy": "1.26.4", "scipy": "1.13.1", "causallearn": "0.1.4.8", "ges": "1.1.0", "gies": "0.0.3"}


def tree_sha256(pkg_dir):
    h = hashlib.sha256()
    pkg_dir = Path(pkg_dir)
    for f in sorted(pkg_dir.rglob("*.py")):
        if "__pycache__" in f.parts:
            continue
        rel = f.relative_to(pkg_dir.parent).as_posix()
        h.update(("%s\0%s\n" % (rel, hashlib.sha256(f.read_bytes()).hexdigest())).encode())
    return h.hexdigest()


def current(causal_learn):
    if causal_learn and str(Path(causal_learn).resolve()) not in sys.path:
        sys.path.insert(0, str(Path(causal_learn).resolve()))
    out = {"python": platform.python_version(), "packages": {}}
    for mod in ("numpy", "scipy", "causallearn", "ges", "gies"):
        try:
            m = __import__(mod)
        except ImportError:
            out["packages"][mod] = None
            continue
        pkg = Path(m.__file__).parent
        ver = getattr(m, "__version__", None)
        if ver is None:
            dist = next(iter(sorted(pkg.parent.glob("%s-*.dist-info" % ("causal_learn" if mod == "causallearn" else mod)))), None)
            ver = dist.name[:-len(".dist-info")].split("-")[1] if dist else "unknown"
        out["packages"][mod] = {"version": ver, "tree_sha256": tree_sha256(pkg)}
    return out


def manifest(causal_learn):
    cur = current(causal_learn)
    return {"format": "cc-engine-manifest/1", "tickets": ["CAP-05", "CAP-11", "BLD-02"], "pins": PINS, "settings": SETTINGS,
            "environment": cur, "threads_env": {k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}}


def differences(want, have):
    diffs = []
    if not have["python"].startswith(want["pins"]["python"]):
        diffs.append("python %s, pinned %s" % (have["python"], want["pins"]["python"]))
    for mod, w in want["environment"]["packages"].items():
        h = have["packages"].get(mod)
        if w is None:
            continue
        if h is None:
            diffs.append("%s missing" % mod)
        elif (h["version"], h["tree_sha256"]) != (w["version"], w["tree_sha256"]):
            diffs.append("%s %s/%s.. != pinned %s/%s.." % (mod, h["version"], h["tree_sha256"][:12], w["version"], w["tree_sha256"][:12]))
    return diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--causal-learn", default=os.environ.get("CC_CAUSAL_LEARN"))
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        want = json.load(open(HERE / "MANIFEST.json"))
        d = differences(want, current(a.causal_learn))
        print("engine manifest: %s" % ("matches" if not d else "DIFFERS: " + "; ".join(d)))
        sys.exit(1 if d else 0)
    m = manifest(a.causal_learn)
    for mod, v in m["environment"]["packages"].items():
        if v is not None:
            pin = PINS.get(mod)
            if pin and v["version"] != pin:
                raise SystemExit("%s is %s, pinned %s: refusing to write a manifest" % (mod, v["version"], pin))
    print(json.dumps(m, indent=1))
    if a.write:
        json.dump(m, open(HERE / "MANIFEST.json", "w"), indent=1)
        print("wrote", HERE / "MANIFEST.json")


if __name__ == "__main__":
    main()
