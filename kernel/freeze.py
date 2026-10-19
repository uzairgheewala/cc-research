"""Freeze a kernel version before a held-out read (binding time: q2_build_prereg rule; failure modes Q1, Q4).

  python -m kernel.freeze --bundle b1 --rule C3 --write      writes plans/b1_freeze.json
  python -m kernel.freeze --bundle b1 --check                exit 1 if the code differs from the frozen version

The code hash is sha256 over "path\\0sha256(file)\\n" for every file below, sorted. A held-out runner refuses to read
the test split unless the current hash equals the frozen one; changing any listed file after a held-out read makes a
new kernel version whose held-out read is a second, separately logged read.
"""
import argparse, datetime, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TREES = ("kernel", "engines", "score", "supplier", "audit")
FILES = ("ledger/schema.py", "ledger/verify.py", "ledger/schema02.py", "ledger/verify02.py", "engines/MANIFEST.json")


def code_files():
    out = []
    for t in TREES:
        out += [p for p in (ROOT / t).rglob("*.py") if "__pycache__" not in p.parts]
    out += [ROOT / f for f in FILES if (ROOT / f).exists()]
    return sorted(set(out))


CORE = ("engines/core.py", "engines/MANIFEST.json", "kernel/derive.py", "kernel/policy.py", "kernel/build.py", "kernel/ledger_hash.py",
        "ledger/verify.py")


def core_sha256():
    """Hash of the files that make a data-only ledger's claims. Later bundles (B2-B5) must not change it: they record it
    in their own freeze, and it must equal B1's."""
    h = hashlib.sha256()
    for rel in CORE:
        h.update(("%s\0%s\n" % (rel, hashlib.sha256((ROOT / rel).read_bytes()).hexdigest())).encode())
    return h.hexdigest()


def code_sha256():
    h = hashlib.sha256()
    listing = {}
    for p in code_files():
        rel = p.relative_to(ROOT).as_posix()
        d = hashlib.sha256(p.read_bytes()).hexdigest()
        listing[rel] = d
        h.update(("%s\0%s\n" % (rel, d)).encode())
    return h.hexdigest(), listing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--rule", default=None)
    ap.add_argument("--note", default="")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--maps", nargs="*", default=[], help="calibration map files (under calibration/) to hash into the freeze")
    ap.add_argument("--same-core-as", default=None, help="refuse unless the data-only core equals this bundle's freeze (e.g. b1)")
    ap.add_argument("--models", default=None, help="a models index (e.g. calibration/v3_models.json): every model's sha256 goes into the freeze")
    ap.add_argument("--prereg", default=None, help="the pre-registration this freeze answers to (its sha256 goes into the freeze)")
    a = ap.parse_args()
    path = ROOT / "plans" / ("%s_freeze.json" % a.bundle)
    h, listing = code_sha256()
    if a.check:
        want = json.load(open(path))["code_sha256"]
        print("kernel code %s the frozen version (%s..)" % ("matches" if h == want else "DIFFERS from", want[:12]))
        sys.exit(0 if h == want else 1)
    if a.same_core_as:
        other = json.load(open(ROOT / "plans" / ("%s_freeze.json" % a.same_core_as)))
        if other["core_sha256"] != core_sha256():
            raise SystemExit("data-only core differs from %s's frozen core: refusing" % a.same_core_as)
    maps = {}
    for m in a.maps:
        maps[Path(m).name] = hashlib.sha256((ROOT / "calibration" / Path(m).name).read_bytes()).hexdigest()
    models = {}
    if a.models:
        for k, v in json.load(open(ROOT / a.models)).items():
            models[k] = hashlib.sha256((ROOT / v["path"]).read_bytes()).hexdigest()
    prereg = {"path": a.prereg, "sha256": hashlib.sha256((ROOT / a.prereg).read_bytes()).hexdigest()} if a.prereg else None
    rec = {"bundle": a.bundle, "id": h[:16], "code_sha256": h, "core_sha256": core_sha256(), "rule": a.rule, "note": a.note, "maps": maps, "models": models, "prereg": prereg,
           "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "files": listing}
    print(json.dumps({k: v for k, v in rec.items() if k != "files"}, indent=1))
    if a.write:
        json.dump(rec, open(path, "w"), indent=1)
        print("wrote", path)


if __name__ == "__main__":
    main()
