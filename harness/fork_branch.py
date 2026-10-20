"""INF-06: describe a ticket branch of the Causal-Copilot fork, so runs on it are checked and labelled.

Tickets: INF-06, BLD-06, EXT-03

    python harness/fork_branch.py describe --branch bld-06-refinement-v2 --ticket BLD-06 \
        --patch jobs/fork/bld-06-refinement-v2.patch --tree PATH_TO_A_CHECKOUT_OF_THE_BRANCH
    python harness/fork_branch.py show --branch bld-06-refinement-v2

`describe` writes jobs/fork/<branch>.sha256 (the baseline manifest with every file the patch touches re-hashed from the
given checkout, added files listed, deleted files dropped) and jobs/fork/<branch>.json (ticket, base commit, patch sha256,
manifest sha256, the touched files). harness/cc_common.verify_tree uses both when CC_BRANCH=<branch> is set, so a branch
run is refused unless the tree is exactly baseline + that patch and the checkout is on that branch.
Standard library only.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

RESEARCH = Path(__file__).resolve().parent.parent
BASE_MANIFEST = RESEARCH / "manifests" / "baseline_a31aa7c.sha256"
FORK = RESEARCH / "jobs" / "fork"
BASE_COMMIT = "a31aa7cab277d7e19478bc326dbec154525969cc"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def touched(patch_text):
    """-> {path: "modified" | "added" | "deleted"} from a git diff."""
    out = {}
    for block in re.split(r"(?m)^diff --git ", patch_text)[1:]:
        m = re.match(r"a/(\S+) b/(\S+)", block)
        if not m:
            continue
        path = m.group(2)
        if "\nnew file mode" in block.split("\n@@", 1)[0]:
            out[path] = "added"
        elif "\ndeleted file mode" in block.split("\n@@", 1)[0]:
            out[m.group(1)] = "deleted"
        else:
            out[path] = "modified"
    return out


def describe(branch, ticket, patch, tree):
    patch = Path(patch)
    files = touched(patch.read_text(encoding="utf-8"))
    lines = {}
    for line in BASE_MANIFEST.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d, rel = line.split("  ", 1)
            lines[rel[2:] if rel.startswith("./") else rel] = d
    for rel, kind in files.items():
        if kind == "deleted":
            lines.pop(rel, None)
        else:
            p = Path(tree) / rel
            if not p.is_file():
                raise SystemExit("%s is in the patch but not in %s" % (rel, tree))
            if b"\r\n" in p.read_bytes():
                raise SystemExit("%s has CRLF line endings: clone with core.autocrlf=false (docs/FORK.md)" % rel)
            lines[rel] = sha(p)
    FORK.mkdir(parents=True, exist_ok=True)
    man = FORK / ("%s.sha256" % branch)
    man.write_text("".join("%s  ./%s\n" % (lines[r], r) for r in sorted(lines)), encoding="utf-8")
    spec = {"branch": branch, "ticket": ticket, "base_commit": BASE_COMMIT, "base_tag": "baseline-a31aa7c",
            "patch": str(patch.relative_to(RESEARCH)).replace("\\", "/"), "patch_sha256": sha(patch),
            "manifest": str(man.relative_to(RESEARCH)).replace("\\", "/"), "manifest_sha256": sha(man),
            "files": files}
    (FORK / ("%s.json" % branch)).write_text(json.dumps(spec, indent=1) + "\n", encoding="utf-8")
    return spec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("describe", "show"))
    ap.add_argument("--branch", required=True)
    ap.add_argument("--ticket", default="")
    ap.add_argument("--patch", default="")
    ap.add_argument("--tree", default="")
    a = ap.parse_args()
    if a.cmd == "describe":
        print(json.dumps(describe(a.branch, a.ticket, a.patch, a.tree), indent=1))
    else:
        print((FORK / ("%s.json" % a.branch)).read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
