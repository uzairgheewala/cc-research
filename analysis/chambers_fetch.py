"""Fetch the Causal Chambers inputs for BND-07 (BEN-10, REP-09) into the cloud workspace and verify them.

  python analysis/chambers_fetch.py

1. Data: every causal_chambers/* entry of external/FETCH_REPORT.json (directory.yaml and 8 zips) is downloaded from its
   recorded URL (https://causalchamber.s3.eu-central-1.amazonaws.com/downloadables/...) into external/causal_chambers/
   and its sha256 compared with the report. A mismatch stops the script (exit 2) and the bad file is kept as *.bad.
   A file already present with the right sha256 is not downloaded again.
2. Docs: dataset READMEs, variables.csv, the validation config tables, two generator scripts, regimes_targets.py and
   the authors' paper notebooks are fetched from raw.githubusercontent.com into external/causal_chambers_docs/ with
   their sha256 recorded in external/causal_chambers_docs/DOCS_FETCH.json (no reference hash exists for these).

Writes analysis/results/chambers/fetch_status.json with the outcome per file, including the exact error text when the
egress proxy refuses a host (the proxy's own reason is read with a raw CONNECT probe).
"""
import json, os, socket, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chambers_io as C  # noqa: E402

GH = "https://raw.githubusercontent.com/juangamella/causal-chamber/main/datasets/"
GP = "https://raw.githubusercontent.com/juangamella/causal-chamber-paper/main/"
DOC_FILES = {}
for d in C.DATASETS:
    DOC_FILES["%s__README.md" % d] = GH + d + "/README.md"
    DOC_FILES["%s__variables.csv" % d] = GH + d + "/variables.csv"
DOC_FILES.update({
    "lt_validate_v1_lt_validation_configs.csv": GH + "lt_validate_v1/lt_validation_configs.csv",
    "wt_validate_v1_wt_standard_validation_configs.csv": GH + "wt_validate_v1/wt_standard_validation_configs.csv",
    "lt_interventions_standard_v1_generators_uniform.py": GH + "lt_interventions_standard_v1/generators/uniform.py",
    "lt_validate_v1_generators_binary_interventions.py": GH + "lt_validate_v1/generators/binary_interventions.py",
    "wt_validate_v1_generators_binary_interventions.py": GH + "wt_validate_v1/generators/binary_interventions.py",
    "wt_walks_v1_regimes_targets.py": GH + "wt_walks_v1/regimes_targets.py",
    "paper__README.md": GP + "README.md",
    "paper__requirements.txt": GP + "requirements.txt",
    "paper__case_studies_causal_discovery_iid.ipynb": GP + "case_studies/causal_discovery_iid.ipynb",
    "paper__causal_validation.ipynb": GP + "causal_validation.ipynb",
})


def proxy_reason(host):
    """Ask the egress proxy for CONNECT to host and return its status line and body (the refusal reason)."""
    px = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not px:
        return None
    h, p = px.split("//")[-1].rstrip("/").split(":")
    try:
        s = socket.create_connection((h, int(p)), timeout=20)
        s.sendall(("CONNECT %s:443 HTTP/1.1\r\nHost: %s:443\r\n\r\n" % (host, host)).encode())
        r = s.recv(4096).decode(errors="replace")
        s.close()
        head, _, body = r.partition("\r\n\r\n")
        return {"status_line": head.splitlines()[0], "body": body.strip()}
    except OSError as e:
        return {"error": repr(e)}


def get(url, dest):
    tmp = Path(str(dest) + ".part")
    with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    tmp.replace(dest)


def main():
    C.DATA.mkdir(parents=True, exist_ok=True)
    C.DOCS.mkdir(parents=True, exist_ok=True)
    C.OUT.mkdir(parents=True, exist_ok=True)
    status = {"utc": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), "data": [], "docs": []}
    mismatch = False
    for e in C.fetch_report_entries():
        dest = C.EXT / e["file"]
        row = {"file": e["file"], "url": e["url"], "expected_sha256": e["sha256"], "expected_bytes": e["bytes"]}
        if dest.exists() and C.sha256(dest) == e["sha256"]:
            row.update(outcome="verified (already present)", sha256=e["sha256"])
        else:
            try:
                get(e["url"], dest)
                got = C.sha256(dest)
                row["sha256"] = got
                if got == e["sha256"]:
                    row["outcome"] = "verified"
                else:
                    row["outcome"] = "SHA256 MISMATCH"
                    dest.replace(str(dest) + ".bad")
                    mismatch = True
            except Exception as ex:  # noqa: BLE001 - the exact error is the record
                row.update(outcome="download failed", error=repr(ex))
                host = e["url"].split("/")[2]
                row["proxy_reason"] = proxy_reason(host)
        status["data"].append(row)
        print("%-50s %s" % (e["file"], row["outcome"]))
        if mismatch:
            break
    docs_rec = []
    for fn, url in DOC_FILES.items():
        dest = C.DOCS / fn
        try:
            get(url, dest)
            docs_rec.append({"file": fn, "url": url, "sha256": C.sha256(dest), "bytes": dest.stat().st_size})
        except Exception as ex:  # noqa: BLE001
            docs_rec.append({"file": fn, "url": url, "error": repr(ex)})
    json.dump({"utc": status["utc"], "source": "raw.githubusercontent.com (authors' GitHub repositories)",
               "files": docs_rec}, open(C.DOCS / "DOCS_FETCH.json", "w", encoding="utf-8"), indent=1)
    status["docs"] = [{"file": d["file"], "ok": "error" not in d} for d in docs_rec]
    json.dump(status, open(C.OUT / "fetch_status.json", "w", encoding="utf-8"), indent=1)
    n_ok = sum(r["outcome"].startswith("verified") for r in status["data"])
    print("data verified %d/%d; docs ok %d/%d" % (n_ok, len(status["data"]), sum(d["ok"] for d in status["docs"]),
                                                  len(status["docs"])))
    sys.exit(2 if mismatch else 0)


if __name__ == "__main__":
    main()
