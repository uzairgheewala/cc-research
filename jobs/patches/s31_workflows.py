"""s31 (TEAM-13): add the "Inside Causal-Copilot" build to the two workflows (Pages and CI), right after the Atlas build.
Run once from cc-research: py -3 jobs\patches\s31_workflows.py   (refuses twice). The agent cannot write .github files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDITS = {
    ".github/workflows/pages.yml": ("      - run: python site/build.py\n",
                                    "      - run: python site/build.py\n      - run: python site/copilot/build.py\n"),
    ".github/workflows/ci.yml": ("      - name: Site builds from the snapshot\n        run: python site/build.py\n",
                                 "      - name: Site builds from the snapshot\n        run: python site/build.py\n"
                                 "      - name: Inside Causal-Copilot builds from the committed model\n        run: python site/copilot/build.py\n"),
}
for rel, (old, new) in EDITS.items():
    p = ROOT / rel
    t = p.read_bytes().decode("utf-8")
    assert "site/copilot/build.py" not in t, "already applied: " + rel
    assert t.count(old) == 1, "anchor not found once in " + rel
    p.write_bytes(t.replace(old, new, 1).encode("utf-8"))
    print("updated", rel)
