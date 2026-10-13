"""Shared I/O for the Causal Chambers bundle (BND-07; tickets BEN-10, REP-09).

Data:   external/causal_chambers/<name>.zip, the 8 dataset archives listed in external/FETCH_REPORT.json, each verified
        against the sha256 recorded there before any read (a mismatch raises; nothing is read from an unverified file).
Docs:   external/causal_chambers_docs/, dataset READMEs, variables.csv, validation configs and the authors' paper notebooks,
        fetched from raw.githubusercontent.com (juangamella/causal-chamber, juangamella/causal-chamber-paper); their URLs
        and sha256 are in external/causal_chambers_docs/DOCS_FETCH.json.
Graphs: the causalchamber package 0.2.8 (external/causalchamber_pkg, MIT), module causalchamber.ground_truth
        (functions variables(), edges(), graph()). Only that module is imported: causalchamber.datasets fetches
        directory.yaml from S3 at import time.

Experiment CSVs are read straight from the verified zip (no extraction), following the package's own convention in
causalchamber/datasets/main.py: a non-image dataset is a folder <name>/ holding one <experiment>.csv per experiment.
Here a CSV inside <name>/ counts as an experiment when it has a `timestamp` column (this excludes configuration tables
such as lt_validation_configs.csv).
"""
import hashlib, io, json, zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EXT = ROOT / "external"
DATA = EXT / "causal_chambers"
DOCS = EXT / "causal_chambers_docs"
OUT = ROOT / "analysis" / "results" / "chambers"

DATASETS = ["lt_interventions_standard_v1", "lt_validate_v1", "lt_malus_v1", "wt_validate_v1",
            "wt_intake_impulse_v1", "wt_bernoulli_v1", "wt_changepoints_v1", "wt_walks_v1"]


def fetch_report_entries():
    """Entries of external/FETCH_REPORT.json under causal_chambers/ (directory.yaml and the 8 zips)."""
    rep = json.load(open(EXT / "FETCH_REPORT.json", encoding="utf-8"))
    return [e for e in rep["fetched"] if e["file"].startswith("causal_chambers/")]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def expected_sha(name):
    for e in fetch_report_entries():
        if e["file"] == "causal_chambers/%s.zip" % name:
            return e["sha256"]
    raise KeyError(name)


def extracted_dir(name):
    """Folder holding the experiment CSVs when the zip was extracted by the fetcher (harness/fetch_external.py): the zip's
    sha256 was verified at download (FETCH_REPORT.json) and the zip itself was not kept. Layout <name>/<name>/*.csv."""
    for d in (DATA / name / name, DATA / name):
        if d.is_dir() and any(d.glob("*.csv")):
            return d
    return None


def data_status(name):
    """'verified' (zip present, sha256 matches FETCH_REPORT.json), 'extracted' (no zip; the fetcher's extracted folder,
    whose zip was verified at download), 'absent' or 'MISMATCH'."""
    p = DATA / ("%s.zip" % name)
    if p.exists():
        return "verified" if sha256(p) == expected_sha(name) else "MISMATCH"
    return "extracted" if extracted_dir(name) is not None else "absent"


READABLE = ("verified", "extracted")


def readable(name):
    return data_status(name) in READABLE


def open_verified(name):
    st = data_status(name)
    if st != "verified":
        raise RuntimeError("%s.zip is %s; refusing to read it" % (name, st))
    return zipfile.ZipFile(DATA / ("%s.zip" % name))


def experiments(name):
    """{experiment name: zip member path or CSV path} for a verified zip or the fetcher's extracted folder."""
    if data_status(name) == "extracted":
        out = {}
        for f in sorted(extracted_dir(name).glob("*.csv")):
            if "timestamp" in pd.read_csv(f, nrows=0).columns:
                out[f.stem] = str(f)
        return out
    z = open_verified(name)
    out = {}
    for m in z.namelist():
        parts = m.split("/")
        if len(parts) == 2 and parts[0] == name and parts[1].endswith(".csv"):
            cols = pd.read_csv(io.BytesIO(z.read(m)), nrows=0).columns
            if "timestamp" in cols:
                out[parts[1][:-4]] = m
    return out


def load_experiment(name, experiment):
    if data_status(name) == "extracted":
        return pd.read_csv(extracted_dir(name) / ("%s.csv" % experiment))
    z = open_verified(name)
    return pd.read_csv(io.BytesIO(z.read("%s/%s.csv" % (name, experiment))))


def ground_truth():
    """causalchamber.ground_truth.main (0.2.8). The subpackage re-exports only graph() and latex_name();
    variables() and edges() live in .main."""
    import contextlib, io as _io
    with contextlib.redirect_stdout(_io.StringIO()):   # the package prints a citation banner on import
        import causalchamber.ground_truth.main as gt
    return gt


def descendants(edges, v):
    ch = {}
    for a, b in edges:
        ch.setdefault(a, set()).add(b)
    seen, stack = set(), [v]
    while stack:
        for c in ch.get(stack.pop(), ()):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def longest_path(edges, nodes):
    ch = {}
    for a, b in edges:
        ch.setdefault(a, []).append(b)
    memo = {}

    def lp(v):
        if v not in memo:
            memo[v] = 0
            memo[v] = max([1 + lp(c) for c in ch.get(v, [])] or [0])
        return memo[v]
    return max(lp(v) for v in nodes)


def chamber_of(name):
    return name.split("_")[0]
