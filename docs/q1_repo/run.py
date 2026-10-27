"""python run.py reproduce | table | test   (see README.md)"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMITTED = ROOT / "analysis" / "results" / "fork" / "bld06_live_compare.json"


def close(a, b, path="", out=None):
    """Every difference between two JSON values, numbers compared to 1e-9."""
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append("%s/%s: only in one file" % (path, k))
            else:
                close(a[k], b[k], "%s/%s" % (path, k), out)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            close(x, y, "%s/%d" % (path, i), out)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if abs(a - b) > 1e-9:
            out.append("%s: %r != %r" % (path, a, b))
    elif a != b:
        out.append("%s: %r != %r" % (path, a, b))
    return out


def reproduce():
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "bld06_live_compare.json"
        subprocess.run([sys.executable, str(ROOT / "analysis" / "bld06_live_compare.py"), "--out", str(out)], check=True)
        diff = close(json.loads(out.read_text()), json.loads(COMMITTED.read_text()))
    if diff:
        print("NOT reproduced: %d differences, first: %s" % (len(diff), diff[:5]))
        return 1
    print("reproduced: the recomputed comparison equals %s" % COMMITTED.relative_to(ROOT))
    table()
    return 0


def table():
    r = json.loads(COMMITTED.read_text())
    m, P = r["means"], r["paired_branch_minus_main"]
    rows = [("Runs completed (of %d)" % r["arms"], r["completed"]["main"], r["completed"]["branch"], ""),
            ("Adjacency F1, %d tables both completed" % r["both_completed"], m["main"]["final_adj_f1"], m["branch"]["final_adj_f1"], P["L2"]),
            ("Directed F1, same tables", m["main"]["final_dir_f1"], m["branch"]["final_dir_f1"], P["L2_dir"]),
            ("Delivered directed F1 (crash = 0), all tables", m["main"]["delivered_dir_f1"], m["branch"]["delivered_dir_f1"], P["L1"]),
            ("API cost, USD", r["usd"]["main"], r["usd"]["branch"], "")]
    print("%-48s %10s %12s   %s" % ("", "unmodified", "refinement v2", "paired gain [95% interval]"))
    for name, a, b, p in rows:
        f = (lambda x: "%d" % x) if isinstance(a, int) else ((lambda x: "$%.2f" % x) if name.startswith("API") else (lambda x: "%.3f" % x))
        g = "%+.3f [%+.3f, %+.3f]" % (p["point"], p["lo"], p["hi"]) if p else ""
        print("%-48s %10s %12s   %s" % (name, f(a), f(b), g))
    print("pre-registered rule: %s (prereg sha256 %s)" % (r["rule"], r["prereg_sha256"][:12]))
    return 0


def test():
    return subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"]).returncode


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "reproduce"
    sys.exit({"reproduce": reproduce, "table": table, "test": test}.get(cmd, lambda: print(__doc__) or 2)())
