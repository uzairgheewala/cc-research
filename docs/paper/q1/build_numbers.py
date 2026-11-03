"""Every number in the Q1 paper, read from the result file that holds it (DLV-05, W1).

Tickets: DLV-05, DLV-07, DLV-11

    python3 docs/paper/q1/build_numbers.py [--root .] [--check]

Reads docs/paper/q1/numbers.json and writes, next to it:
- numbers.tex: one \\nm{key} definition per entry (the paper prints numbers only through \\nm);
- numbers_table.tex: appendix A, every key with its value, file and pointer;
- numbers.lock.json: value, the source file's sha256, and its git state (tracked-clean, modified, untracked, excluded).

An entry is {"key", "file", "ptr", "fmt"} (optionally "re": a regex whose group 1 is the number inside a text field) or {"key", "op", "args": [{"file", "ptr"}, ...], "fmt"}.
Pointers are JSON pointers with two extensions: a segment "*" takes every child (a list follows), and a segment
"[k=v;k2=v2]" takes the first list item whose fields equal those strings, and "?k" is k's value or None. Ops: sub, div, add, len, min, max, sum, count_true,
count_notnull, mean; an arg may be {"key": k}, an earlier entry's raw value. Nothing else is computed, so appendix A shows every input.
--check fails (exit 1) if any value differs from numbers.lock.json; without it the lock is rewritten and changes printed.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEL = re.compile(r"^\[(.+)\]$")


class Missing(Exception):
    pass


def walk(obj, segs, where):
    if not segs:
        return obj
    s, rest = segs[0], segs[1:]
    if s == "*":
        kids = list(obj.values()) if isinstance(obj, dict) else list(obj)
        return [walk(k, rest, where) for k in kids]
    m = SEL.match(s)
    if m:
        conds = [c.split("=", 1) for c in m.group(1).split(";")]
        for item in obj:
            if all(str(item.get(k)) == v for k, v in conds):
                return walk(item, rest, where)
        raise Missing("%s: no item matches %s" % (where, s))
    if s.startswith("?"):                      # optional key: None when absent
        return walk(obj[s[1:]], rest, where) if isinstance(obj, dict) and s[1:] in obj else None
    s = s.replace("~1", "/").replace("~0", "~")
    if isinstance(obj, list):
        try:
            return walk(obj[int(s)], rest, where)
        except (ValueError, IndexError):
            raise Missing("%s: bad index %s" % (where, s))
    if not isinstance(obj, dict) or s not in obj:
        raise Missing("%s: no key %r" % (where, s))
    return walk(obj[s], rest, where)


_cache = {}


def load(root, rel):
    if rel not in _cache:
        p = root / rel
        b = p.read_bytes()
        _cache[rel] = (json.loads(b.decode("utf-8")), hashlib.sha256(b).hexdigest())
    return _cache[rel]


def get(root, file, ptr):
    data, _ = load(root, file)
    segs = [s for s in ptr.split("/")[1:]] if ptr not in ("", "/") else []
    return walk(data, segs, "%s#%s" % (file, ptr))


def flat(v):
    if isinstance(v, list):
        out = []
        for x in v:
            out += flat(x)
        return out
    return [v]


OPS = {
    "sub": lambda a: a[0] - a[1],
    "div": lambda a: a[0] / a[1],
    "add": lambda a: sum(a),
    "len": lambda a: len(a[0]),
    "min": lambda a: min(x for x in flat(a) if x is not None),
    "max": lambda a: max(x for x in flat(a) if x is not None),
    "sum": lambda a: sum(x for x in flat(a) if x is not None),
    "mean": lambda a: (lambda xs: sum(xs) / len(xs))([x for x in flat(a) if x is not None]),
    "count_true": lambda a: sum(1 for x in flat(a) if x is True),
    "count_notnull": lambda a: sum(1 for x in flat(a) if x is not None),
}


def value(root, e, done):
    if "op" in e:
        args = [done[x["key"]]["raw"] if "key" in x else get(root, x["file"], x["ptr"]) for x in e["args"]]
        if e["op"] == "len":
            return OPS["len"](args)
        return OPS[e["op"]](args)
    v = get(root, e["file"], e["ptr"])
    if "re" in e:                              # a number stated inside a pre-registered text field
        m = re.search(e["re"], v)
        if not m:
            raise Missing("%s#%s: %r not found in %r" % (e["file"], e["ptr"], e["re"], v))
        v = float(m.group(1))
    return v


def fmt(v, f):
    if f == "raw":
        return str(v)
    if f.startswith("$"):
        return "\\$" + f[1:].format(v)
    if f.endswith("%}"):
        return f.format(v).replace("%", "\\%")
    return f.format(v)


def tex_escape(s):
    return (s.replace("\\", "\\textbackslash{}").replace("_", "\\_").replace("#", "\\#").replace("%", "\\%")
             .replace("&", "\\&").replace("$", "\\$").replace("{", "\\{").replace("}", "\\}").replace("~", "\\textasciitilde{}"))


def tt(s):
    """A path or pointer in monospace that may break after any slash."""
    return "\\texttt{%s}" % tex_escape(s).replace("/", "/\\allowbreak{}")


def git_states(root, files):
    """tracked-clean / modified / untracked / excluded (outside git by design, hashed in manifests/excluded)."""
    st = {}
    g = ["git", "--no-optional-locks", "-c", "safe.directory=*", "-C", str(root)]
    try:
        tracked = set(subprocess.run(g + ["ls-files", "--"] + files, capture_output=True, text=True, check=True).stdout.split("\n"))
        dirty = subprocess.run(g + ["status", "--porcelain", "--untracked-files=no", "--"] + files, capture_output=True,
                               text=True, check=True).stdout
        head = subprocess.run(g + ["rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except Exception as ex:  # noqa: BLE001 - recorded, never guessed
        return {f: "unknown (%s)" % type(ex).__name__ for f in files}, "unknown"
    mod = {l[3:].strip() for l in dirty.splitlines() if l.strip()}
    for f in files:
        if f.startswith("external/"):
            st[f] = "excluded"
        elif f not in tracked:
            st[f] = "untracked"
        elif f in mod:
            st[f] = "modified"
        else:
            st[f] = "tracked-clean"
    return st, head


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parents[2]))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-git", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    reg = json.loads((HERE / "numbers.json").read_text(encoding="utf-8"))
    entries = reg["entries"]
    errors, out = [], {}
    keys = set()
    for e in entries:
        k = e["key"]
        if k in keys:
            errors.append("duplicate key " + k)
        keys.add(k)
        if not re.fullmatch(r"[a-z0-9][a-z0-9.\-]*", k):
            errors.append("bad key %r (lower case, digits, dots, dashes)" % k)
        try:
            v = value(root, e, out)
            out[k] = {"raw": v, "text": fmt(v, e.get("fmt", "{}"))}
        except (Missing, FileNotFoundError, KeyError, TypeError, ValueError, ZeroDivisionError) as ex:
            errors.append("%s: %s" % (k, ex))
    if errors:
        print("\n".join("ERROR " + x for x in errors))
        return 1
    files = sorted({e["file"] for e in entries if "file" in e} | {x["file"] for e in entries for x in e.get("args", []) if "file" in x})
    states, head = ({f: "not checked" for f in files}, "not checked") if a.no_git else git_states(root, files)
    lock = {"cc_research_head": head, "sources": {f: {"sha256": load(root, f)[1], "git": states[f]} for f in files},
            "values": {k: out[k]["text"] for k in sorted(out)}}
    lock_path = HERE / "numbers.lock.json"
    old = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.exists() else None
    changed = []
    if old:
        for k in sorted(set(old["values"]) | set(lock["values"])):
            if old["values"].get(k) != lock["values"].get(k):
                changed.append("%s: %s -> %s" % (k, old["values"].get(k), lock["values"].get(k)))
        for f in sorted(set(old["sources"]) & set(lock["sources"])):
            if old["sources"][f]["sha256"] != lock["sources"][f]["sha256"]:
                changed.append("source changed: " + f)
    if a.check:
        if old is None or changed:
            print("\n".join(["CHECK FAILED"] + changed))
            return 1
        print("numbers: %d entries match the lock" % len(out))
        return 0
    # numbers.tex
    lines = ["% Generated by build_numbers.py from numbers.json. Do not edit.", "% cc-research HEAD " + head]
    for e in entries:
        lines.append("\\expandafter\\def\\csname nm@%s\\endcsname{%s}" % (e["key"], out[e["key"]]["text"]))
    lines.append("\\expandafter\\def\\csname nm@cc.head\\endcsname{%s}" % head[:12])
    (HERE / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # numbers_table.tex (appendix A)
    rows = []
    for e in entries:
        if "op" in e:
            src = "%s of: " % tex_escape(e["op"]) + "; ".join(("key " + tt(x["key"])) if "key" in x else
                                                             tt(x["file"]) + " " + tt(x["ptr"]) for x in e["args"])
        else:
            src = tt(e["file"]) + " " + tt(e["ptr"]) + ((" (pattern " + tt(e["re"]) + ")") if "re" in e else "")
        fl = [e["file"]] if "file" in e else [x["file"] for x in e["args"] if "file" in x]
        flag = "" if all(states[f] in ("tracked-clean", "not checked") for f in fl) else \
            " \\emph{(%s)}" % ", ".join(sorted({states[f] for f in fl if states[f] != "tracked-clean"}))
        rows.append("\\texttt{%s} & %s & {\\footnotesize %s%s} \\\\" % (tex_escape(e["key"]), out[e["key"]]["text"], src, flag))
    tab = ["% Generated by build_numbers.py. Do not edit.",
           "{\\small\\begin{longtable}{p{0.27\\linewidth} p{0.11\\linewidth} p{0.54\\linewidth}}",
           "\\toprule Key & Value & Source file and JSON pointer (cc-research) \\\\ \\midrule \\endhead"] + rows + \
          ["\\bottomrule\\end{longtable}}"]
    (HERE / "numbers_table.tex").write_text("\n".join(tab) + "\n", encoding="utf-8")
    lock_path.write_text(json.dumps(lock, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("numbers: %d entries from %d files; HEAD %s" % (len(out), len(files), head[:12]))
    for f in files:
        if states[f] not in ("tracked-clean", "not checked"):
            print("  source %s: %s" % (states[f], f))
    for c in changed:
        print("  changed " + c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
