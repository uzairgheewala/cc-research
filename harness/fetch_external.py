"""Download public benchmark material that the analysis sandbox cannot reach. No LLM, no API key, no cost.

  python /research/harness/fetch_external.py                 (both sources)
  python /research/harness/fetch_external.py --only causalarena | chambers

Writes only under <cc-research>/external/:
  external/causalarena/...            snapshot of the Hugging Face dataset LAMDA-Tabular/CausalArena (CC-BY-4.0)
  external/causal_chambers/...        directory.yaml (the list of all datasets) and a few tabular datasets
  external/FETCH_REPORT.json          every file fetched (url, bytes, sha256), everything skipped and why, every error

It never raises on a download problem: the problem is recorded and the next item is tried.
Limits are PER SOURCE, so one source cannot use up another's allowance:
  CausalArena      one file at most --max-file-mb (300), the source at most --max-total-mb (1500)
  Causal Chambers  one file at most --chambers-max-file-mb (800), the source at most --chambers-max-total-mb (2500)
Causal Chambers is fetched first. The size of every Causal Chambers archive is asked for before anything is
downloaded and written to the report, so an archive that does not fit is listed as skipped with the size it needs.
CausalArena files matching --skip-regex (default: the synthetic sample files) are not downloaded.
Files already present with the expected size are not downloaded again.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cc_common import RESEARCH  # noqa: E402

HF_REPO = "LAMDA-Tabular/CausalArena"
HF_BASE = "https://huggingface.co"
CHAMBERS_DIRECTORY = "https://causalchamber.s3.eu-central-1.amazonaws.com/downloadables/directory.yaml"
# Tabular (non-image) Causal Chambers datasets wanted first. Names not present in the live directory are
# reported as "not in directory" and skipped; the saved directory.yaml then shows what does exist.
# In priority order: when the source allowance runs out, the later ones are the ones skipped.
CHAMBERS_WANTED = ["lt_interventions_standard_v1", "lt_validate_v1", "wt_validate_v1", "wt_intake_impulse_v1",
                   "wt_bernoulli_v1", "wt_walks_v1", "wt_changepoints_v1", "lt_malus_v1"]
SKIP_REGEX = r"^scm/synthetic/data/"


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


class Fetcher:
    def __init__(self, root, max_file_mb, max_total_mb):
        import requests
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "cc-research-fetch/1"
        self.root = root
        self.source = "(none)"
        self.max_file = int(max_file_mb * 1024 * 1024)
        self.max_total = int(max_total_mb * 1024 * 1024)
        self.total = 0                      # bytes downloaded for the CURRENT source
        self.grand_total = 0
        self.report = {"started_utc": utc(), "fetched": [], "skipped": [], "errors": [], "sources": {}}

    def begin_source(self, name, max_file_mb, max_total_mb):
        """Each source has its own allowance; nothing carries over from the previous source."""
        self.source = name
        self.max_file = int(max_file_mb * 1024 * 1024)
        self.max_total = int(max_total_mb * 1024 * 1024)
        self.total = 0
        self.report["sources"][name] = {"max_file_bytes": self.max_file, "max_total_bytes": self.max_total, "bytes": 0}

    def size_of(self, url):
        """Content-Length from a HEAD request, or None when the server does not say."""
        try:
            r = self.s.head(url, timeout=(15, 60), allow_redirects=True)
            if r.status_code == 200 and r.headers.get("Content-Length"):
                return int(r.headers["Content-Length"])
        except Exception:
            pass
        return None

    def get(self, url, **kw):
        last = None
        for attempt in range(3):
            try:
                r = self.s.get(url, timeout=(15, 120), **kw)
                if r.status_code == 200:
                    return r
                last = "HTTP %d" % r.status_code
                if r.status_code in (401, 403, 404):
                    break
            except Exception as e:                      # network errors are data here, not crashes
                last = "%s: %s" % (type(e).__name__, str(e)[:200])
            time.sleep(2 * (attempt + 1))
        raise RuntimeError(last)

    def download(self, url, dest, expect_bytes=None, md5=None, what=""):
        dest = Path(dest)
        rel = str(dest.relative_to(self.root)).replace(os.sep, "/")
        if expect_bytes is not None and expect_bytes > self.max_file:
            self.report["skipped"].append({"file": rel, "bytes_needed": expect_bytes,
                                           "why": "needs %.1f MB; the per-file limit for %s is %.0f MB" % (
                                               expect_bytes / 1048576.0, self.source, self.max_file / 1048576.0)})
            return False
        if dest.exists() and expect_bytes is not None and dest.stat().st_size == expect_bytes:
            self.report["skipped"].append({"file": rel, "why": "already present with the expected size"})
            return True
        if self.total + (expect_bytes or 0) > self.max_total:
            self.report["skipped"].append({"file": rel, "bytes_needed": expect_bytes,
                                           "why": "needs %.1f MB; only %.1f MB of the %.0f MB allowance for %s is left" % (
                                               (expect_bytes or 0) / 1048576.0, (self.max_total - self.total) / 1048576.0,
                                               self.max_total / 1048576.0, self.source)})
            return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_name(dest.name + ".part")
        try:
            r = self.get(url, stream=True)
            h, hm, n = hashlib.sha256(), hashlib.md5(), 0
            with open(tmp, "wb") as fh:
                for chunk in r.iter_content(1 << 20):
                    n += len(chunk)
                    if n > self.max_file or self.total + n > self.max_total:
                        raise RuntimeError("size limit reached while downloading")
                    h.update(chunk)
                    hm.update(chunk)
                    fh.write(chunk)
            if expect_bytes is not None and n != expect_bytes:
                raise RuntimeError("size mismatch: got %d, expected %d" % (n, expect_bytes))
            if md5 and hm.hexdigest() != md5:
                raise RuntimeError("md5 mismatch")
            os.replace(tmp, dest)
            self.total += n
            self.grand_total += n
            self.report["sources"][self.source]["bytes"] = self.total
            self.report["fetched"].append({"file": rel, "url": url, "bytes": n, "sha256": h.hexdigest(), "what": what})
            print("  ok   %-70s %10d bytes" % (rel[-70:], n))
            return True
        except Exception as e:
            try:
                tmp.unlink()
            except OSError:
                pass
            self.report["errors"].append({"file": rel, "url": url, "error": "%s: %s" % (type(e).__name__, str(e)[:300])})
            print("  FAIL %-70s %s" % (rel[-70:], str(e)[:120]))
            return False

    # ---- Hugging Face dataset snapshot (plain HTTP API; no login, no extra package)
    def causalarena(self, base, repo, skip_regex=None):
        skip = re.compile(skip_regex) if skip_regex else None
        out = self.root / "causalarena"
        print("[fetch] CausalArena: %s/datasets/%s" % (base, repo))
        url = "%s/api/datasets/%s/tree/main?recursive=true" % (base, repo)
        files, pages = [], 0
        try:
            while url and pages < 200:
                r = self.get(url)
                files += [x for x in r.json() if x.get("type") == "file"]
                url = (r.links.get("next") or {}).get("url")
                pages += 1
        except Exception as e:
            self.report["errors"].append({"file": "causalarena (file listing)", "url": url, "error": str(e)[:300]})
            print("  FAIL listing: %s" % str(e)[:160])
            return
        (out).mkdir(parents=True, exist_ok=True)
        (out / "_FILE_LIST.json").write_text(json.dumps(files, indent=1), encoding="utf-8")
        print("  %d files listed" % len(files))
        for x in sorted(files, key=lambda x: x.get("size") or 0):
            path = x["path"]
            if ".." in path.split("/") or path.startswith("/"):
                self.report["skipped"].append({"file": "causalarena/" + path, "why": "unsafe path"})
                continue
            size = (x.get("lfs") or {}).get("size", x.get("size"))
            if skip and skip.search(path) and not ((out / path).exists() and (out / path).stat().st_size == size):
                self.report["skipped"].append({"file": "causalarena/" + path, "why": "matches --skip-regex (not needed)"})
                continue
            self.download("%s/datasets/%s/resolve/main/%s" % (base, repo, path), out / path, expect_bytes=size, what="CausalArena")

    # ---- Causal Chambers tabular datasets
    def chambers(self, directory_url, wanted):
        out = self.root / "causal_chambers"
        print("[fetch] Causal Chambers directory: %s" % directory_url)
        if not self.download(directory_url, out / "directory.yaml", what="Causal Chambers dataset directory"):
            return
        try:
            import yaml
            directory = yaml.safe_load((out / "directory.yaml").read_text(encoding="utf-8"))
            datasets = directory["datasets"]
        except Exception as e:
            self.report["errors"].append({"file": "causal_chambers/directory.yaml", "error": "could not parse: %s" % str(e)[:200]})
            return
        self.report["chambers_directory"] = {k: {"image": bool(v.get("image")), "chamber": v.get("chamber")} for k, v in datasets.items()}
        # Ask for every archive's size first (one small request each), so limits are applied before any download
        # and the report says what each dataset would cost.
        sizes = {k: (self.size_of(v["url"]) if v.get("url") else None) for k, v in datasets.items()}
        self.report["chambers_sizes_bytes"] = sizes
        for k in sorted(sizes, key=lambda k: (sizes[k] is None, sizes[k] or 0)):
            print("  size %-34s %s%s" % (k, ("%9.1f MB" % (sizes[k] / 1048576.0)) if sizes[k] is not None else "  unknown",
                                       "  (image dataset)" if datasets[k].get("image") else ""))
        for name in wanted:
            d = datasets.get(name)
            if d is None:
                self.report["skipped"].append({"file": "causal_chambers/" + name, "why": "not in directory"})
                continue
            if d.get("image"):
                self.report["skipped"].append({"file": "causal_chambers/" + name, "why": "image dataset"})
                continue
            z = out / (name + ".zip")
            if (out / name).is_dir() and any((out / name).rglob("*.csv")):   # extraction is nested under <name>/
                self.report["skipped"].append({"file": "causal_chambers/" + name, "why": "already extracted"})
                continue
            if not self.download(d["url"], z, expect_bytes=sizes.get(name), md5=d.get("md5"), what="Causal Chambers " + name):
                continue
            try:
                dest = (out / name)
                dest.mkdir(parents=True, exist_ok=True)
                base = dest.resolve()
                with zipfile.ZipFile(z) as zf:
                    for m in zf.infolist():
                        target = (dest / m.filename).resolve()
                        if target != base and base not in target.parents:
                            raise RuntimeError("unsafe path in archive: %s" % m.filename)
                    zf.extractall(dest)
                z.unlink()
                self.report.setdefault("extracted", []).append({"dataset": name, "csv_files": len(list(dest.rglob("*.csv")))})
            except Exception as e:
                self.report["errors"].append({"file": "causal_chambers/%s.zip" % name, "error": "extract failed: %s" % str(e)[:200]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["causalarena", "chambers"], default=None)
    ap.add_argument("--max-file-mb", type=float, default=300, help="CausalArena: largest single file")
    ap.add_argument("--max-total-mb", type=float, default=1500, help="CausalArena: allowance for this source")
    ap.add_argument("--chambers-max-file-mb", type=float, default=800, help="Causal Chambers: largest single archive")
    ap.add_argument("--chambers-max-total-mb", type=float, default=2500, help="Causal Chambers: allowance for this source")
    ap.add_argument("--skip-regex", default=SKIP_REGEX, help="CausalArena paths not to download ('' to download everything)")
    ap.add_argument("--hf-base", default=HF_BASE, help="(testing) alternative base URL")
    ap.add_argument("--chambers-directory-url", default=CHAMBERS_DIRECTORY, help="(testing) alternative directory URL")
    ap.add_argument("--out", default=str(RESEARCH / "external"))
    a = ap.parse_args()
    root = Path(a.out)
    root.mkdir(parents=True, exist_ok=True)
    f = Fetcher(root, a.max_file_mb, a.max_total_mb)
    if a.only in (None, "chambers"):              # first: it is the smaller, more specific request
        f.begin_source("causal_chambers", a.chambers_max_file_mb, a.chambers_max_total_mb)
        f.chambers(a.chambers_directory_url, CHAMBERS_WANTED)
    if a.only in (None, "causalarena"):
        f.begin_source("causalarena", a.max_file_mb, a.max_total_mb)
        f.causalarena(a.hf_base, HF_REPO, a.skip_regex)
    f.report["finished_utc"] = utc()
    f.report["total_bytes"] = f.grand_total
    (root / "FETCH_REPORT.json").write_text(json.dumps(f.report, indent=1), encoding="utf-8")
    print("=" * 78)
    print("FETCH %s   fetched %d file(s), %.1f MB; skipped %d; errors %d" % (
        "DONE" if not f.report["errors"] else "DONE WITH ERRORS", len(f.report["fetched"]), f.grand_total / 1048576.0,
        len(f.report["skipped"]), len(f.report["errors"])))
    print("report: %s" % (root / "FETCH_REPORT.json"))
    print("=" * 78)
    sys.exit(0 if (f.report["fetched"] or f.report["skipped"]) and not f.report["errors"] else 1)


if __name__ == "__main__":
    main()
