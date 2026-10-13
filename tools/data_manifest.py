"""Hash the data kept out of git, so the repo still pins it.

  python tools/data_manifest.py                 update manifests/excluded/<root>.sha256 for every excluded root
  python tools/data_manifest.py --budget 150    stop after ~150 s and resume on the next call (state in manifests/excluded/.state.json);
                                                in this mode files already hashed are not re-checked; run once without --budget after
  python tools/data_manifest.py --check         re-hash and report files that changed or disappeared (exit 1 if any)

Excluded roots (see .gitignore): external/, runs/, jobs/transfer/. Output lines use sha256sum format
("<hash>  <path>") sorted by path, so `sha256sum -c` works from the cc-research folder. A file whose size and
mtime are unchanged since it was last hashed is not re-read.
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "manifests" / "excluded"
ROOTS = ["external", "runs", "jobs/transfer"]
STATE = OUT / ".state.json"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk(root):
    base = ROOT / root
    if not base.exists():
        return []
    files = []
    for dp, dn, fn in os.walk(base):
        dn[:] = sorted(d for d in dn if d != "__pycache__")
        files += [Path(dp) / f for f in fn]
    return sorted(files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=0, help="seconds; 0 = no limit")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    state = json.load(open(STATE)) if STATE.exists() else {}
    t0, done_all, changed = time.time(), True, []
    for root in ROOTS:
        for p in walk(root):
            rel = p.relative_to(ROOT).as_posix()
            prev = state.get(rel)
            if prev and a.budget and not a.check:
                continue                      # chunked mode: trust files already hashed (stat is slow on mounted folders)
            st = p.stat()
            key = "%d:%d" % (st.st_size, int(st.st_mtime))
            if prev and prev["key"] == key and not a.check:
                continue
            if a.budget and time.time() - t0 > a.budget:
                done_all = False
                break
            h = sha(p)
            if prev and prev["sha256"] != h:
                changed.append(rel)
            state[rel] = {"key": key, "sha256": h, "bytes": st.st_size}
        if not done_all:
            break
    present = {p.relative_to(ROOT).as_posix() for r in ROOTS for p in walk(r)} if done_all else set(state)
    gone = sorted(set(state) - present)
    for g in gone:
        state.pop(g)
    json.dump(state, open(STATE, "w"), indent=0, sort_keys=True)
    for root in ROOTS:
        rows = sorted((k, v) for k, v in state.items() if k.startswith(root + "/"))
        with open(OUT / (root.replace("/", "_") + ".sha256"), "w", encoding="utf-8", newline="\n") as fh:
            fh.writelines("%s  %s\n" % (v["sha256"], k) for k, v in rows)
    total = sum(v["bytes"] for v in state.values())
    print("%s: %d files, %.1f MB hashed; %d changed, %d gone%s" % (
        "complete" if done_all else "partial (run again)", len(state), total / 1e6, len(changed), len(gone),
        "" if not changed else " -> " + ", ".join(changed[:5])))
    sys.exit(0 if done_all and not (a.check and (changed or gone)) else (2 if not done_all else 1))


if __name__ == "__main__":
    main()
