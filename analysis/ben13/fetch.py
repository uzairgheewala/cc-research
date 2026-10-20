"""BEN-13 S0: get CausalBench's inputs into external/causalbench/ (resumable; run on Uzair's machine, host Python).

Tickets: BEN-13

    python -m analysis.ben13.fetch [--only k562.h5ad,summary_stats.xlsx] [--dir external/causalbench]
                                   [--import-from DIR ...] [--no-download]

The URLs are causalbench 1.1.2's own (data_access/datasets/*.py). Every file is checked before it is accepted: never empty,
the right magic bytes for its format, and, where known, the size and md5 that figshare publishes (article 20029387). A
file that fails the check is set aside as <name>.rejected (an empty one is removed), never recorded as fetched.

figshare's download links answer programmatic requests with an empty body (wave A, 20 Oct), so the two expression files
come from a browser download: open the two figshare links below in a browser, let them land in Downloads, and this
script imports them by their published file names (from ~/Downloads, or each --import-from folder), checking size and
md5 before moving them in. Other files are downloaded (HTTP Range resume). A finished file is never fetched again.

Writes external/causalbench/FETCHED.json: per file its size, sha256, md5, source and status; `_required_ok` is true only
when every required file passed its checks. The literature files are optional (CORUM's old address may be gone: it is
then reported missing, not fatal). Data kept outside git: hash it with `python tools/data_manifest.py` afterwards.
"""
import argparse, hashlib, json, os, shutil, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
HDF5, ZIP, GZ = b"\x89HDF\r\n\x1a\n", b"PK\x03\x04", b"\x1f\x8b"
# name, url, required, size, md5, magic, browser file name (figshare's published name)
FILES = [
    ("k562.h5ad", "https://plus.figshare.com/ndownloader/files/35773219", True, 10661879995,
     "4f1122ce1c7f13299a68df6459a266d3", HDF5, "K562_essential_raw_singlecell_01.h5ad"),
    ("rpe1.h5ad", "https://plus.figshare.com/ndownloader/files/35775606", True, 8700873216,
     "6a2a9d0d2bf4ec147f4d1104043b268c", HDF5, "rpe1_raw_singlecell_01.h5ad"),
    ("summary_stats.xlsx", "https://ars.els-cdn.com/content/image/1-s2.0-S0092867422005979-mmc2.xlsx", True, None, None, ZIP,
     "1-s2.0-S0092867422005979-mmc2.xlsx"),
    ("protein.links.txt.gz", "https://stringdb-static.org/download/protein.links.detailed.v11.5/9606.protein.links.detailed.v11.5.txt.gz",
     False, None, None, GZ, None),
    ("protein.physical.links.txt.gz", "https://stringdb-static.org/download/protein.physical.links.detailed.v11.5/9606.protein.physical.links.detailed.v11.5.txt.gz",
     False, None, None, GZ, None),
    ("protein.info.txt.gz", "https://stringdb-static.org/download/protein.info.v11.5/9606.protein.info.v11.5.txt.gz", False, None, None, GZ, None),
    ("corum_complexes.txt.zip", "https://mips.helmholtz-muenchen.de/corum/download/releases/current/humanComplexes.txt.zip",
     False, None, None, ZIP, None),
]
UA = {"User-Agent": "cc-research-ben13/1 (UCSD DSC 180A; contact via repository)"}


def digests(p):
    s, m = hashlib.sha256(), hashlib.md5()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""):
            s.update(b)
            m.update(b)
    return s.hexdigest(), m.hexdigest()


def check(p, size=None, md5=None, magic=None):
    """None when the file passes; otherwise the reason. Size and magic first (cheap), md5 last."""
    p = Path(p)
    if not p.exists():
        return "missing"
    n = p.stat().st_size
    if n == 0:
        return "empty file"
    if size is not None and n != size:
        return "size %d, expected %d" % (n, size)
    if magic:
        with open(p, "rb") as fh:
            head = fh.read(len(magic))
        if head != magic:
            return "not the expected format (first bytes %r)" % head[:16]
    if md5:
        got = digests(p)[1]
        if got != md5:
            return "md5 %s, expected %s" % (got, md5)
    return None


def set_aside(p, why):
    p = Path(p)
    if not p.exists():
        return None
    if p.stat().st_size == 0:
        p.unlink()
        return "removed (empty)"
    dst = Path(str(p) + ".rejected")
    os.replace(p, dst)
    return "set aside as %s (%s)" % (dst.name, why)


def fetch(url, dest, size=None, magic=None, tries=5):
    part = Path(str(dest) + ".partial")
    if part.exists() and (part.stat().st_size == 0 or (magic and part.read_bytes()[:len(magic)] != magic)):
        part.unlink()                                               # an empty or wrong-format partial is not resumed
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
                    last = 0
                    while True:
                        b = r.read(1 << 22)
                        if not b:
                            break
                        fh.write(b)
                        have += len(b)
                        if time.time() - last > 30:
                            last = time.time()
                            print("[fetch] %s %.2f / %s GB" % (dest.name, have / 1e9, "%.2f" % (total / 1e9) if total else "?"), flush=True)
            if have == 0:
                raise IOError("the server sent an empty body (a browser download is needed for this file)")
            if total and have != total:
                raise IOError("short read: %d of %d bytes" % (have, total))
            if size and have != size:
                raise IOError("size %d, expected %d" % (have, size))
            os.replace(part, dest)
            return
        except Exception as e:
            print("[fetch] %s attempt %d: %s" % (dest.name, attempt + 1, e), flush=True)
            if part.exists() and part.stat().st_size == 0:
                part.unlink()
            if "empty body" in str(e):
                break                                               # retrying does not change a refusal
            time.sleep(min(60, 5 * 2 ** attempt))
    raise IOError("download failed: %s" % url)


def import_from(dirs, browser_name, dest, size, md5, magic):
    """Move a browser-downloaded copy in after checking it. Returns (source path, None) or (None, reasons)."""
    reasons = []
    for d in dirs:
        src = Path(d).expanduser() / browser_name
        if not src.exists():
            continue
        why = check(src, size, md5, magic)
        if why:
            reasons.append("%s: %s" % (src, why))
            continue
        shutil.move(str(src), str(dest))                            # same drive: a rename; else a copy
        return str(src), None
    return None, reasons or ["%s not found in %s" % (browser_name, ", ".join(str(Path(d).expanduser()) for d in dirs))]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(HERE / "external" / "causalbench"))
    ap.add_argument("--only", default="")
    ap.add_argument("--import-from", action="append", default=None,
                    help="folder holding browser downloads (repeatable; default ~/Downloads and $CB_DOWNLOADS)")
    ap.add_argument("--no-download", action="store_true", help="import and check only")
    a = ap.parse_args(argv)
    dirs = a.import_from or [p for p in (os.environ.get("CB_DOWNLOADS"), str(Path.home() / "Downloads")) if p]
    d = Path(a.dir)
    d.mkdir(parents=True, exist_ok=True)
    rec_path = d / "FETCHED.json"
    rec = json.loads(rec_path.read_text()) if rec_path.exists() else {}
    rec.pop("_required_ok", None)
    only = set(filter(None, a.only.split(",")))
    failed_required = []
    for name, url, required, size, md5, magic, browser in FILES:
        if only and name not in only:
            continue
        dest = d / name
        note = None
        try:
            prev = rec.get(name, {})
            known = dest.exists() and prev.get("status") == "ok" and prev.get("bytes") == dest.stat().st_size and \
                (md5 is None or prev.get("md5") == md5)
            if dest.exists():
                why = check(dest, size, None if known else md5, magic)     # md5 again only for a file not yet recorded
                if why:
                    note = set_aside(dest, why)
                    rec.pop(name, None)
                    known = False
            if not known:
                source = None
                if not dest.exists():
                    src, reasons = (None, ["no browser file name"]) if not browser else import_from(dirs, browser, dest, size, md5, magic)
                    if src:
                        source = "browser download " + src
                    elif a.no_download:
                        raise IOError("; ".join(reasons))
                    else:
                        try:
                            fetch(url, dest, size, magic)
                            source = "download " + url
                        except Exception as e:
                            raise IOError("%s; import: %s%s" % (e, "; ".join(reasons),
                                          ("; open %s in a browser and run this again" % url) if browser else ""))
                why = check(dest, size, None, magic)
                sha, m5 = digests(dest)
                if not why and md5 and m5 != md5:
                    why = "md5 %s, expected %s" % (m5, md5)
                if why:
                    set_aside(dest, why)
                    raise IOError(why)
                left = Path(str(dest) + ".partial")
                if left.exists() and left.stat().st_size == 0:
                    left.unlink()
                rec[name] = {"status": "ok", "bytes": dest.stat().st_size, "sha256": sha, "md5": m5, "md5_expected": md5,
                             "url": url, "source": source or "present before this run"}
        except Exception as e:
            rec[name] = {"status": "failed", "error": str(e)[:600], "url": url, "required": required}
            if required:
                failed_required.append(name)
        if note:
            rec[name]["earlier_copy"] = note
        rec_path.write_text(json.dumps(rec, indent=1))
        print("[fetch] %s: %s%s" % (name, rec[name]["status"], "" if rec[name]["status"] == "ok" else " (%s)" % rec[name]["error"]), flush=True)
    if not only:
        missing = [n for n, _, req, *_ in FILES if req and rec.get(n, {}).get("status") != "ok"]
        failed_required = sorted(set(failed_required) | set(missing))
    rec["_required_ok"] = not failed_required
    rec["_required_failed"] = failed_required
    rec_path.write_text(json.dumps(rec, indent=1))
    return 1 if failed_required else 0


if __name__ == "__main__":
    sys.exit(main())
