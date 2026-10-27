"""Produce the public Quarter 1 repository from this one: a curated, reproducible subset (decision V-1, 27 Oct 2026).

Tickets: DLV-07, DLV-05

    py -3 tools\\export_q1.py [--out ..\\causal-copilot-q1]

1. Copies the files in ALLOW verbatim, at the same relative paths, so the Q1 repository runs the very code the research
   used (analysis/bld06_live_compare.py and the modules it imports).
2. Writes the template files from docs/q1_repo/ (README, run.py, docs, tests, requirements, CI) and fills the README's
   commit placeholders.
3. Reduces each run state the comparison reads to the two graphs it uses (runs/<id>/state/<same file name>), and writes
   recorded/MANIFEST.json with the sha256 and size of every full file, so a reduced file can be checked against the archive.
4. Refuses the export if a written file is not in the allowlist or the template, if a file is over 5 MB, or if the
   secret patterns of tools/secret_scan.py match anything. Then it runs the exported repository's reproduction.

The output folder is replaced except for its .git, so the export is the same whatever was there before. No git command is
run; Uzair commits and pushes the output. Writes .github/workflows/ci.yml (agents cannot write .github files, so this runs on
the machine)."""
import argparse
import datetime
import fnmatch
import glob
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "q1_repo"
ALLOW = [
    "analysis/bld06_live_compare.py", "analysis/cc_graph.py", "analysis/trace_q011.py",
    "analysis/results/fork/bld06_live_compare.json",
    "analysis/results/run_trace/q011_gas_void.json", "analysis/results/run_trace/CONTRACT.json",
    "analysis/reports/run_trace/q011_gas_void.md", "analysis/results/fork/CONTRACT.json",
    "analysis/results/stability_s2/bnd08_summary.json",
    "score/__init__.py", "score/paired.py",
    "plans/bld06_live_prereg.json",
    "plans/results/fork_bld06_live.capped.json", "plans/results/fork_bld06_live_main.capped.json",
    "datasets/suite_q1s2/**",
    "docs/q1/datasets.md",
    "tools/export_q1.py",
]
TEMPLATE_MAP = {"README.md": "README.md", "run.py": "run.py", "requirements.txt": "requirements.txt",
                "gitignore": ".gitignore", "gitattributes": ".gitattributes", "ci.yml": ".github/workflows/ci.yml",
                "docs/method.md": "docs/method.md", "docs/code_tour.md": "docs/code_tour.md",
                "tests/test_reproduce.py": "tests/test_reproduce.py"}
CAPPED = ["plans/results/fork_bld06_live.capped.json", "plans/results/fork_bld06_live_main.capped.json"]
BND08 = "analysis/results/stability_s2/bnd08_summary.json"
KEEP = ("converted_graph", "revised_graph")
MAX = 5 * 1024 * 1024


def sha(b):
    return hashlib.sha256(b).hexdigest()


def allowed_files():
    out = []
    for pat in ALLOW:
        if "*" in pat:
            out += sorted(p for p in glob.glob(str(ROOT / pat), recursive=True) if Path(p).is_file() and "__pycache__" not in p)
        else:
            out.append(str(ROOT / pat))
    return [Path(p) for p in out]


def run_ids():
    ids = []
    for c in CAPPED:
        ids += [r["run_id"] for r in json.loads((ROOT / c).read_text(encoding="utf-8"))["runs"].values()]
    ids += [r["run_id"] for r in json.loads((ROOT / BND08).read_text(encoding="utf-8"))["runs"]]
    return sorted(set(ids))


def state_file(rid):
    """The file analysis/bld06_live_compare.py::last_state reads: the 99_final state, else the last state."""
    fs = sorted(glob.glob(str(ROOT / "runs" / rid / "state" / "*.json")))
    fin = [f for f in fs if f.endswith("99_final.json")]
    return Path(fin[-1] if fin else fs[-1]) if fs else None


def git_head(repo, ref="HEAD"):
    try:
        return subprocess.run(["git", "-C", str(repo), "rev-parse", ref], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001 - recorded as unknown, never guessed
        return "unknown"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT.parent / "causal-copilot-q1"))
    ap.add_argument("--no-check", action="store_true")
    a = ap.parse_args(argv)
    out = Path(a.out).resolve()
    assert out != ROOT and ROOT not in out.parents, "the export must go outside cc-research"
    out.mkdir(parents=True, exist_ok=True)
    for p in out.iterdir():                      # replace everything except the output repository's own git folder
        if p.name == ".git":
            continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()

    written = {}

    def put(rel, data):
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        written[rel] = data

    for src in allowed_files():
        put(src.relative_to(ROOT).as_posix(), src.read_bytes())

    manifest = {"about": "Each runs/<id>/state file here keeps only results.converted_graph and results.revised_graph of the "
                         "recorded state; full_sha256 and full_bytes identify the full file in the run archive.", "reduced": {}}
    missing = []
    for rid in run_ids():
        f = state_file(rid)
        if f is None:
            missing.append(rid)
            continue
        full = f.read_bytes()
        st = json.loads(full.decode("utf-8"))
        slim = {"results": {k: (st.get("results") or {}).get(k) for k in KEEP}, "reduced_from": {"sha256": sha(full), "bytes": len(full)}}
        data = (json.dumps(slim, sort_keys=True) + "\n").encode("utf-8")
        rel = "runs/%s/state/%s" % (rid, f.name)
        put(rel, data)
        manifest["reduced"][rel] = {"full_sha256": sha(full), "full_bytes": len(full), "reduced_sha256": sha(data)}
    assert not missing, "runs without a state file: %s" % missing
    put("recorded/MANIFEST.json", (json.dumps(manifest, indent=1, sort_keys=True) + "\n").encode("utf-8"))

    fork = ROOT.parent / "Causal-Copilot"
    fill = {"{CC_COMMIT}": git_head(ROOT), "{BRANCH_BLD06}": git_head(fork, "bld-06-refinement-v2")[:7],
            "{BRANCH_EXT03}": git_head(fork, "ext-03-cycle-step-key")[:7],
            "{EXPORTED_UTC}": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
    for src, dst in TEMPLATE_MAP.items():
        data = (TEMPLATE / src).read_bytes()
        if dst == "README.md":
            text = data.decode("utf-8")
            fill["{N_FILES}"] = str(len(written) + len(TEMPLATE_MAP))
            for k, v in fill.items():
                text = text.replace(k, v)
            assert "{" + "CC_COMMIT}" not in text
            data = text.encode("utf-8")
        put(dst, data)

    # guards: allowlist, size, secrets
    sys.path.insert(0, str(ROOT / "tools"))
    import secret_scan
    allowed = {p.relative_to(ROOT).as_posix() for p in allowed_files()} | set(TEMPLATE_MAP.values()) | {"recorded/MANIFEST.json"}
    bad = []
    for rel, data in written.items():
        if rel not in allowed and not fnmatch.fnmatch(rel, "runs/*/state/*.json"):
            bad.append("not allowed: " + rel)
        if len(data) > MAX:
            bad.append("over 5 MB: %s (%d bytes)" % (rel, len(data)))
        if not rel.endswith(secret_scan.SKIP_SUFFIX):
            for name, rx in secret_scan.PATTERNS:
                if rx.search(data):
                    bad.append("secret pattern %s in %s" % (name, rel))
    on_disk = {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file() and ".git" not in p.relative_to(out).parts}
    bad += ["unexpected file on disk: " + x for x in sorted(on_disk - set(written))]
    if bad:
        print("\n".join("ERROR " + b for b in bad))
        return 1
    total = sum(len(d) for d in written.values())
    print("exported %d files (%.1f MB) to %s; cc-research %s" % (len(written), total / 1e6, out, fill["{CC_COMMIT}"][:12]))
    if a.no_check:
        return 0
    return subprocess.run([sys.executable, str(out / "run.py"), "reproduce"], cwd=str(out)).returncode


if __name__ == "__main__":
    sys.exit(main())
