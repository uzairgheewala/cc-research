"""Inside Causal-Copilot: copy the source lines the site prints into site/copilot/excerpts.json (CI has no Causal-Copilot
checkout, so the build reads code only from this file).

    python site/copilot/snip.py --repo ../Causal-Copilot

Copies (a) every excerpt range named in site/copilot/content/steps/*.json and (b) the full source of every function on the
CLI path (model.json on_cli_path). Each entry records the function's sha256 from model.json, so the build can refuse an
excerpt whose function changed. The repo is checked against the baseline manifest first (extract.manifest_check)."""
import argparse
import json
from pathlib import Path

import extract

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(extract.RESEARCH.parent / "Causal-Copilot"))
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    extract.manifest_check(repo)
    model = json.load(open(HERE / "model.json", encoding="utf-8"))
    F = model["functions"]
    lines = {}

    def src(path):
        if path not in lines:
            lines[path] = (repo / path).read_text(encoding="utf-8", errors="replace").splitlines()
        return lines[path]

    out = {"about": "Source lines printed by the Inside Causal-Copilot site, copied from upstream a31aa7c by site/copilot/snip.py.",
           "baseline_commit": model["baseline_commit"], "manifest_sha256": model["manifest_sha256"], "functions": {}, "ranges": {}}
    for fid, f in sorted(F.items()):
        if f["on_cli_path"] and f["name"] != "<module>":
            out["functions"][fid] = {"sha256": f["sha256"], "line": f["line"], "text": "\n".join(src(f["path"])[f["line"] - 1: f["end"]])}
    for p in sorted((HERE / "content" / "steps").glob("*.json")):
        d = json.load(open(p, encoding="utf-8"))
        for s in d.get("sequence", []):
            ex = s.get("excerpt")
            if ex:
                f = F[s["function"]]
                key = "%s:%d-%d" % (f["path"], ex["start"], ex["end"])
                out["ranges"][key] = {"function": s["function"], "sha256": f["sha256"],
                                      "text": "\n".join(src(f["path"])[ex["start"] - 1: ex["end"]])}
    text = json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    (HERE / "excerpts.json").write_text(text, encoding="utf-8")
    print("excerpts.json: %d functions, %d ranges, %d bytes" % (len(out["functions"]), len(out["ranges"]), len(text.encode())))


if __name__ == "__main__":
    main()
