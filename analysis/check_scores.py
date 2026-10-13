"""Check the score contract over every results directory (EVL-01/02/03). Writes analysis/results/score_contract_report.json.

  python analysis/check_scores.py
"""
import glob, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_record as S  # noqa: E402

root = HERE / "results"
report = {"directories": {}, "nonconforming": [], "rows_checked": 0, "row_problems": []}
for d in sorted(p for p in root.iterdir() if p.is_dir()):
    c_path = d / "CONTRACT.json"
    if not c_path.exists():
        report["directories"][d.name] = ["CONTRACT.json missing"]
        report["nonconforming"].append(d.name)
        continue
    c = json.load(open(c_path, encoding="utf-8"))
    probs = S.check_contract(c)
    for f in glob.glob(str(d / "**" / "*.jsonl"), recursive=True):
        for line in open(f, encoding="utf-8"):
            if '"contract": "v1"' in line:
                r = json.loads(line)
                report["rows_checked"] += 1
                rp = S.check_row(r, c.get("metric_defs"))
                if rp:
                    report["row_problems"].append({"file": os.path.relpath(f, root), "problems": rp})
    report["directories"][d.name] = probs or "ok"
    if probs:
        report["nonconforming"].append(d.name)
report["nonconforming"] += sorted({x["file"].split(os.sep)[0] for x in report["row_problems"]} - set(report["nonconforming"]))
json.dump(report, open(root / "score_contract_report.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
for k, v in report["directories"].items():
    print("%-28s %s" % (k, v))
print("nonconforming: %s; rows checked %d" % (report["nonconforming"] or "none", report["rows_checked"]))
sys.exit(1 if report["nonconforming"] else 0)
