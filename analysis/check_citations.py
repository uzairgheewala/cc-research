"""Gate A1 for BND-03: every finding cites a source, and every file:line citation exists in the audited tree.

  python analysis/check_citations.py analysis/reports/bnd03/*.md   # writes analysis/results/bnd03_citations.json; exit 1 on failure

A finding is a table row (other than header/separator) or a bullet starting with an ID such as F3 / D12 / R-a.
A finding passes A1a if it contains a code citation (path.ext:line), a paper page (p.N), or a ledger / report reference
(F12, I1, D7, Q5, AUD-, REP-, DOM-, section). A1b: every code citation resolves to a file in ../Causal-Copilot
(exact relative path, or a unique-or-any path ending with the cited name) whose length covers the cited line(s).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent / "Causal-Copilot"
CODE = re.compile(r"\b([A-Za-z0-9_./-]+\.(?:py|txt|json|yaml|yml|html|js|toml|sh|cfg))((?::\d+(?:\s*[-–]\s*\d+)?)(?:\s*[,/]\s*:?\d+(?:\s*[-–]\s*\d+)?)*)")
REL = re.compile(r"\(:\d+|\s:\d+")
PATH_ONLY = re.compile(r"\b[A-Za-z0-9_/-]+\.py\b|\b[a-z_]+/[a-z_/]+")
ABSENCE = re.compile(r"\b(never|no |not |absent|missing|none)\b", re.I)
OTHER = re.compile(r"\bsee [a-z]\.\d|\bp\.\s?\d+|\b(?:F|I|D|Q|L)\d+[a-z]?\b|\b(?:AUD|REP|DOM|BEN|CAP)-\d+|\bR-[a-e]\b|\bsection\b|\bs\d|ledger|\[L|\[R\]", re.I)
SKIP_DIRS = {"output", "data", "asset", ".git", "__pycache__"}

files = [p for p in REPO.rglob("*") if p.is_file() and not (set(p.relative_to(REPO).parts) & SKIP_DIRS)]
by_suffix = {}
for p in files:
    rel = p.relative_to(REPO).as_posix()
    by_suffix.setdefault(p.name, []).append(rel)
nlines = {}


def length(rel):
    if rel not in nlines:
        nlines[rel] = sum(1 for _ in open(REPO / rel, encoding="utf-8", errors="replace"))
    return nlines[rel]


def resolve(path, maxline):
    path = path.lstrip("./")
    for pre in ("Causal-Copilot/", "repo:"):
        if path.startswith(pre):
            path = path[len(pre):]
    if (REPO / path).is_file():
        cands = [path]
    else:
        cands = [r for r in by_suffix.get(Path(path).name, []) if r.endswith(path)]
    ok = [c for c in cands if length(c) >= maxline]
    return cands, ok


def main(paths, dest=None):
    out = {"files": {}, "ok": True}
    for f in paths:
        txt = Path(f).read_text(encoding="utf-8").splitlines()
        rows, bad_cite, uncited = 0, [], []
        for i, line in enumerate(txt, 1):
            s = line.strip()
            sep = lambda t: bool(re.match(r"^\|[\s:|-]+\|$", t.strip()))
            is_header = i < len(txt) and sep(txt[i])
            is_row = s.startswith("|") and not sep(s) and not is_header
            is_bullet = bool(re.match(r"^[-*]\s+\**(F|D|R-|A|W|E|T)\d*[a-z]?[\s.:*\])]", s))
            if not (is_row or is_bullet):
                continue
            rows += 1
            cites = CODE.findall(line)
            if not cites and not OTHER.search(line) and not REL.search(line) and not (PATH_ONLY.search(line) and ABSENCE.search(line)):
                uncited.append(i)
            for path, lines_part in cites:
                if path.startswith(("analysis/", "tracker/", "docs/")) or "/mnt/" in path:
                    continue
                nums = [int(n) for n in re.findall(r"\d+", lines_part)]
                cands, ok = resolve(path, max(nums))
                if not ok:
                    bad_cite.append({"line": i, "cite": path + lines_part.strip(), "candidates": cands[:3]})
        res = {"findings": rows, "uncited_findings": uncited, "unresolved_citations": bad_cite}
        out["files"][Path(f).name] = res
        out["ok"] &= not uncited and not bad_cite
        print("%-36s findings %3d  uncited %d  unresolved %d" % (Path(f).name, rows, len(uncited), len(bad_cite)))
        for b in bad_cite[:8]:
            print("    line %d: %s %s" % (b["line"], b["cite"], b["candidates"]))
        if uncited:
            print("    uncited lines:", uncited[:15])
    dest = Path(dest) if dest else ROOT / "analysis" / "results" / "bnd03_citations.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("A1", "PASS" if out["ok"] else "FAIL")
    sys.exit(0 if out["ok"] else 1)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", default=None, help="default analysis/results/bnd03_citations.json (the BND-03 gate record)")
    a = ap.parse_args()
    main(a.files, a.out)
