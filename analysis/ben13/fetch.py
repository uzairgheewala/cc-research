"""BEN-13 S0: download CausalBench's inputs into external/causalbench/ (resumable; run on Uzair's machine, network on).

Tickets: BEN-13

    python -m analysis.ben13.fetch [--only k562.h5ad,summary_stats.xlsx] [--dir external/causalbench]

The URLs are causalbench 1.1.2's own (data_access/datasets/*.py). A partial download resumes from where it stopped (HTTP
Range); a finished file is never fetched again. Writes external/causalbench/FETCHED.json: per file its size, sha256
and status. The two expression files and the summary sheet are required; the literature files are optional (CORUM's
old download address may be gone: that source is then reported missing, not fatal).
Data kept outside git: hash it with `python tools/data_manifest.py` afterwards (AGENTS.md).
"""
import argparse, hashlib, json, os, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
FILES = [
    ("k562.h5ad", "https://plus.figshare.com/ndownloader/files/35773219", True, 10661879995),
    ("rpe1.h5ad", "https://plus.figshare.com/ndownloader/files/35775606", True, None),
    ("summary_stats.xlsx", "https://ars.els-cdn.com/content/image/1-s2.0-S0092867422005979-mmc2.xlsx", True, None),
    ("protein.links.txt.gz", "https://stringdb-static.org/download/protein.links.detailed.v11.5/9606.protein.links.detailed.v11.5.txt.gz", False, None),
    ("protein.physical.links.txt.gz", "https://stringdb-static.org/download/protein.physical.links.detailed.v11.5/9606.protein.physical.links.detailed.v11.5.txt.gz", False, None),
    ("protein.info.txt.gz", "https://stringdb-static.org/download/protein.info.v11.5/9606.protein.info.v11.5.txt.gz", False, None),
    ("corum_complexes.txt.zip", "https://mips.helmholtz-muenchen.de/corum/download/releases/current/humanComplexes.txt.zip", False, None),
]
UA = {"User-Agent": "cc-research-ben13/1 (UCSD DSC 180A; contact via repository)"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def fetch(url, dest, expect=None, tries=5):
    part = Path(str(dest) + ".partial")
    for attempt in range(tries):
        have = part.stat().st_size if part.exists() else 0
        req = urllib.request.Request(url, headers=dict(UA, **({"Range": "bytes=%d-" % have} if have else {})))
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                if have and r.status != 206:
                    have = 0                                        # server ignored the range: start over
                total = r.headers.get("Content-Length")
                total = int(total) + have if total else None
                with open(part, "ab" if have else "wb") as fh:
                    t0, last = time.time(), 0
                    while True:
                        b = r.read(1 << 22)
                        if not b:
                            break
                        fh.write(b)
                        have += len(b)
                        if time.time() - last > 30:
                            last = time.time()
                            print("[fetch] %s %.2f / %s GB" % (dest.name, have / 1e9, "%.2f" % (total / 1e9) if total else "?"), flush=True)
            if total and have != total:
                raise IOError("short read: %d of %d bytes" % (have, total))
            if expect and have != expect:
                raise IOError("size %d, expected %d" % (have, expect))
            os.replace(part, dest)
            return
        except Exception as e:
            print("[fetch] %s attempt %d: %s" % (dest.name, attempt + 1, e), flush=True)
            time.sleep(min(60, 5 * 2 ** attempt))
    raise IOError("gave up on %s" % url)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(HERE / "external" / "causalbench"))
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    d = Path(a.dir)
    d.mkdir(parents=True, exist_ok=True)
    rec_path = d / "FETCHED.json"
    rec = json.loads(rec_path.read_text()) if rec_path.exists() else {}
    only = set(filter(None, a.only.split(",")))
    failed_required = []
    for name, url, required, expect in FILES:
        if only and name not in only:
            continue
        dest = d / name
        try:
            if not dest.exists():
                fetch(url, dest, expect)
            if name not in rec or rec[name].get("bytes") != dest.stat().st_size:
                rec[name] = {"status": "ok", "bytes": dest.stat().st_size, "sha256": sha256(dest), "url": url}
        except Exception as e:
            rec[name] = {"status": "failed", "error": str(e)[:300], "url": url, "required": required}
            if required:
                failed_required.append(name)
        rec_path.write_text(json.dumps(rec, indent=1))
        print("[fetch] %s: %s" % (name, rec[name]["status"]), flush=True)
    rec["_required_ok"] = not failed_required
    rec_path.write_text(json.dumps(rec, indent=1))
    return 1 if failed_required else 0


if __name__ == "__main__":
    sys.exit(main())
