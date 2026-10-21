"""Inside Causal-Copilot (C1): extract a typed model of Causal-Copilot's first-party code from its AST.

    python site/copilot/extract.py --repo ../Causal-Copilot [--externals-listing FILE]

Reads the code at upstream a31aa7c (checked against manifests/baseline_a31aa7c.sha256 before anything is read: every listed
first-party .py and prompt file must match), and writes site/copilot/model.json:

  modules     path, package, lines, sha256, docstring, classes, functions, imports, on the CLI path or not
  functions   one record per def (methods as Class.name): line span, signature, docstring, sha256 of its source,
              calls (resolved, with how), unresolved call names, global_state fields read and written, prompt files it
              opens, LLM points (joined from analysis/results/llm_inventory/llm_inventory.csv by file and line)
  state       every global_state.<a>.<b> field: writers and readers
  prompts     every prompt/context text file and the functions that name it
  steps       main.py's 8 logged steps and the refinement stages, as function ids
  unresolved  what the AST cannot see (dynamic dispatch, setattr), listed, never hidden

No network, no imports of the code under study (pure AST), deterministic output (sorted keys)."""
import argparse
import ast
import csv
import hashlib
import json
import os
import re

from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
MANIFEST = RESEARCH / "manifests" / "baseline_a31aa7c.sha256"
INVENTORY = RESEARCH / "analysis" / "results" / "llm_inventory" / "llm_inventory.csv"
SKIP_DIRS = ("externals/", "output/", "data/dataset/", ".git/", "asset/")
TEXT_EXT = (".txt", ".md", ".json")
DYNAMIC = [{"from": "causal_discovery/program.py::Programming.forward", "registry": "causal_discovery/wrappers/__init__.py",
            "methods": ["__init__", "fit"], "line": 22,
            "why": "algo_func = getattr(wrappers, global_state.algorithm.selected_algorithm); algo_func(arguments).fit(data)"}]
TOP_PACKAGES = {"causal_discovery", "causal_inference", "preprocess", "postprocess", "report", "llm", "utils", "global_setting",
                "user", "web_demo", "data", "externals", "main"}
STATE_ROOTS = ("global_state", "self.global_state", "state")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def manifest_check(repo):
    """Every listed first-party file we read must match the baseline manifest; returns (digest, checked)."""
    digest = sha(MANIFEST.read_bytes())
    checked, bad = 0, []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        h, p = line.split(None, 1)
        p = p.strip()[2:] if p.strip().startswith("./") else p.strip()
        if p.startswith(SKIP_DIRS) or not p.endswith((".py",) + TEXT_EXT):
            continue
        f = repo / p
        if not f.exists():
            bad.append("missing " + p)
            continue
        checked += 1
        if sha(f.read_bytes()) != h:
            bad.append("changed " + p)
    if bad:
        raise SystemExit("the code does not match baseline a31aa7c: %s" % bad[:10])
    return digest, checked


def chain(node):
    """Attribute chain as a dotted string (a.b.c) or None."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def state_field(c):
    """'global_state.results.converted_graph.shape' -> 'results.converted_graph' (two levels below the root)."""
    for root in sorted(STATE_ROOTS, key=len, reverse=True):
        if c == root or c.startswith(root + "."):
            rest = c[len(root) + 1:].split(".")
            rest = [r for r in rest if r]
            if not rest:
                return None
            return ".".join(rest[:2])
    return None


class FuncVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls, self.reads, self.writes, self.strings, self.raises, self.setattrs = [], set(), set(), set(), set(), []
        self.assigns = {}   # local name or self.attr -> the callable chain it was assigned from (x = Filter(args))
        self.refs = []      # self.method used as a value (passed to Parallel, map, a callback list), not called here
        self._called = set()

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Call):
            c = chain(node.value.func)
            for t in node.targets:
                tc = chain(t)
                if c and tc:
                    self.assigns[tc] = c
        self.generic_visit(node)

    def visit_Call(self, node):
        c = chain(node.func)
        if c:
            self.calls.append((c, node.lineno))
            self._called.add(id(node.func))
        if isinstance(node.func, ast.Name) and node.func.id in ("setattr", "getattr") and node.args:
            tgt = chain(node.args[0])
            name = node.args[1].value if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) else None
            if tgt and (tgt in STATE_ROOTS or state_field(tgt + ".x") is not None):
                self.setattrs.append({"kind": node.func.id, "target": tgt, "name": name, "line": node.lineno})
        self.generic_visit(node)

    def visit_Attribute(self, node):
        c = chain(node)
        if c and c.startswith("self.") and c.count(".") == 1 and isinstance(node.ctx, ast.Load) and id(node) not in self._called:
            self.refs.append((c, node.lineno))
        if c:
            f = state_field(c)
            if f:
                (self.writes if isinstance(node.ctx, ast.Store) else self.reads).add(f)
        # do not descend: the inner chain is a prefix of this one
        if not isinstance(node.value, (ast.Attribute, ast.Name)):
            self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str) and re.search(r"\.(txt|json|md)\b", node.value):
            self.strings.add(node.value)

    def visit_Raise(self, node):
        if node.exc is not None:
            e = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
            self.raises.add(chain(e) or "?")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):   # nested defs are part of the enclosing function
        self.generic_visit(node)


def signature(fn):
    try:
        return "def %s(%s)" % (fn.name, ast.unparse(fn.args))
    except Exception:  # noqa: BLE001
        return "def %s(...)" % fn.name


def module_name(path):
    return path[:-3].replace("/", ".").removesuffix(".__init__")


def parse_module(repo, rel):
    src = (repo / rel).read_bytes()
    tree = ast.parse(src, filename=rel)
    lines = src.decode("utf-8", "replace").splitlines()
    mod = {"path": rel, "package": rel.split("/")[0] if "/" in rel else "(top level)", "lines": len(lines), "sha256": sha(src),
           "doc": (ast.get_docstring(tree) or "").strip()[:600], "classes": [], "functions": [], "imports": {}}
    funcs = []

    def add(fn, cls):
        fid = "%s::%s" % (rel, (cls + "." if cls else "") + fn.name)
        seg = "\n".join(lines[fn.lineno - 1: fn.end_lineno])
        v = FuncVisitor()
        for stmt in fn.body:
            v.visit(stmt)
        funcs.append({"id": fid, "path": rel, "cls": cls, "name": fn.name, "line": fn.lineno, "end": fn.end_lineno,
                      "lines": fn.end_lineno - fn.lineno + 1, "signature": signature(fn),
                      "doc": (ast.get_docstring(fn) or "").strip()[:800], "sha256": sha(seg.encode("utf-8")),
                      "_calls": v.calls, "reads": sorted(v.reads - v.writes | (v.reads & v.writes)), "writes": sorted(v.writes),
                      "_strings": sorted(v.strings), "raises": sorted(v.raises), "setattrs": v.setattrs,
                      "decorators": [ast.unparse(d) for d in fn.decorator_list], "_assigns": v.assigns, "_refs": v.refs})
        mod["functions"].append(fid)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add(node, None)
        elif isinstance(node, ast.ClassDef):
            mod["classes"].append({"name": node.name, "line": node.lineno, "bases": [ast.unparse(b) for b in node.bases],
                                   "doc": (ast.get_docstring(node) or "").strip()[:600]})
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add(sub, node.name)
        elif isinstance(node, ast.Import):
            for a in node.names:
                mod["imports"][a.asname or a.name.split(".")[0]] = {"module": a.name, "name": None}
        elif isinstance(node, ast.ImportFrom) and node.module:
            for a in node.names:
                mod["imports"][a.asname or a.name] = {"module": ("." * node.level) + node.module, "name": a.name}
    # module-level code (scripts): treat as a pseudo-function so main.py's top level is visible
    top = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))]
    if top:
        v = FuncVisitor()
        for stmt in top:
            v.visit(stmt)
        if v.calls:
            fid = "%s::<module>" % rel
            funcs.append({"id": fid, "path": rel, "cls": None, "name": "<module>", "line": top[0].lineno, "end": top[-1].end_lineno,
                          "lines": sum(n.end_lineno - n.lineno + 1 for n in top), "signature": "(module level code)",
                          "doc": "", "sha256": sha("\n".join(ast.unparse(n) for n in top).encode("utf-8")), "_calls": v.calls,
                          "reads": sorted(v.reads), "writes": sorted(v.writes), "_strings": sorted(v.strings), "raises": [],
                          "setattrs": v.setattrs, "decorators": [], "_assigns": v.assigns, "_refs": v.refs})
            mod["functions"].append(fid)
    return mod, funcs


def resolve(funcs, mods):
    """Resolve each call to a function id. How: local (same module), import, self (same class), class (constructor),
    unique-method (a method name defined once in the repo), or unresolved."""
    by_id = {f["id"]: f for f in funcs}
    by_mod = {}
    for f in funcs:
        by_mod.setdefault(f["path"], {})[(f["cls"] + "." if f["cls"] else "") + f["name"]] = f["id"]
    modpath = {module_name(m["path"]): m["path"] for m in mods}
    classes = {}
    for m in mods:
        for c in m["classes"]:
            classes.setdefault(c["name"], []).append(m["path"])
    methods = {}
    for f in funcs:
        if f["cls"]:
            methods.setdefault(f["name"], []).append(f["id"])
    imports = {m["path"]: m["imports"] for m in mods}

    def target_module(path, spec):
        mname = spec["module"]
        if mname.startswith("."):
            base = path.split("/")[:-1]
            lvl = len(mname) - len(mname.lstrip("."))
            base = base[:len(base) - (lvl - 1)] if lvl > 1 else base
            mname = ".".join(base + [mname.lstrip(".")])
        return modpath.get(mname)

    def class_of(path, c):
        """A callable chain (Filter, judge_mod.Judge) -> (module path, class name) if it names a first-party class."""
        n = c.split(".")[-1]
        if n in classes:
            if len(classes[n]) == 1:
                return classes[n][0], n
            spec = imports[path].get(c.split(".")[0])
            if spec:
                tm = target_module(path, spec) if spec["name"] else modpath.get(spec["module"])
                if tm in classes[n]:
                    return tm, n
            if path in classes[n]:
                return path, n
        return None

    attr_types = {}   # (module, class, attr) -> (module, class) from self.attr = Class(...)
    for f in funcs:
        for t, c in f["_assigns"].items():
            if t.startswith("self.") and f["cls"]:
                k = class_of(f["path"], c)
                if k:
                    attr_types[(f["path"], f["cls"], t[5:])] = k
    builtins_ = set(dir(__builtins__)) if not isinstance(__builtins__, dict) else set(__builtins__)
    for f in funcs:
        calls, unresolved = [], []
        here = by_mod.get(f["path"], {})
        local_types = {}
        for t, c in f["_assigns"].items():
            k = class_of(f["path"], c)
            if k:
                local_types[t] = k
        for c, ln in f.pop("_calls"):
            parts = c.split(".")
            hit, how = None, None
            if len(parts) == 1:
                n = parts[0]
                if n in here:
                    hit, how = here[n], "local"
                elif n in classes and len(classes[n]) == 1 and (n + ".__init__") in by_mod.get(classes[n][0], {}):
                    hit, how = by_mod[classes[n][0]][n + ".__init__"], "class"
                elif n in imports[f["path"]]:
                    spec = imports[f["path"]][n]
                    tm = target_module(f["path"], spec) if spec["name"] else None
                    if tm and spec["name"] in by_mod.get(tm, {}):
                        hit, how = by_mod[tm][spec["name"]], "import"
                    elif tm and (spec["name"] + ".__init__") in by_mod.get(tm, {}):
                        hit, how = by_mod[tm][spec["name"] + ".__init__"], "import-class"
            elif parts[0] == "self" and len(parts) == 2 and f["cls"]:
                k = f["cls"] + "." + parts[1]
                if k in here:
                    hit, how = here[k], "self"
                elif len(methods.get(parts[1], [])) == 1:
                    hit, how = methods[parts[1]][0], "unique-method"
            elif len(parts) == 2 and parts[0] in imports[f["path"]]:
                spec = imports[f["path"]][parts[0]]
                tm = modpath.get(spec["module"]) if not spec["name"] else target_module(f["path"], {"module": spec["module"] + "." + spec["name"], "name": None})
                if tm and parts[1] in by_mod.get(tm, {}):
                    hit, how = by_mod[tm][parts[1]], "import"
            if hit is None and len(parts) >= 2:
                owner = ".".join(parts[:-1])
                k = local_types.get(owner)
                if k is None and owner.startswith("self.") and f["cls"]:
                    k = attr_types.get((f["path"], f["cls"], owner[5:]))
                if k:
                    mid = by_mod.get(k[0], {}).get(k[1] + "." + parts[-1])
                    if mid:
                        hit, how = mid, "typed"
            if hit is None and len(parts) == 1 and parts[0] in local_types:
                pass
            if hit is None and len(parts) >= 2 and len(methods.get(parts[-1], [])) == 1 and parts[-1] not in ("forward", "run", "fit", "get"):
                hit, how = methods[parts[-1]][0], "unique-method"
            if hit and hit != f["id"]:
                calls.append({"to": hit, "line": ln, "how": how})
            elif not hit:
                root = parts[0]
                spec = imports[f["path"]].get(root)
                if spec and not (target_module(f["path"], spec) if spec["name"] else modpath.get(spec["module"])) \
                        and not spec["module"].startswith(".") and spec["module"].split(".")[0] not in TOP_PACKAGES:
                    kind = "library"
                elif len(parts) == 1 and root in builtins_:
                    kind = "builtin"
                elif root in ("logger", "print"):
                    kind = "logging"
                elif len(parts) >= 2 and (parts[-1] in methods or parts[-1] in {n.split(".")[-1] for n in by_id}):
                    kind = "internal-dynamic"
                else:
                    kind = "value-method"
                unresolved.append({"name": c, "line": ln, "kind": kind})
        called = {x["to"] for x in calls}
        for c, ln in f.pop("_refs", []):
            k = (f["cls"] or "") + "." + c[5:]
            if f["cls"] and k in here and here[k] not in called and here[k] != f["id"]:
                calls.append({"to": here[k], "line": ln, "how": "reference"})
                called.add(here[k])
        f["calls"] = sorted({(x["to"], x["how"]): x for x in calls}.values(), key=lambda x: (x["line"], x["to"]))
        f["calls_unresolved"] = unresolved
        f.pop("_assigns", None)
    # declared dynamic dispatch the AST cannot follow (typed "dynamic", with the line that does it)
    for d in DYNAMIC:
        src = by_id.get(d["from"])
        init = next((m for m in mods if m["path"] == d["registry"]), None)
        if not src or not init:
            continue
        for alias, spec in sorted(init["imports"].items()):
            tm = target_module(d["registry"], spec) if spec["name"] else None
            for meth in d["methods"]:
                mid = by_mod.get(tm, {}).get(spec["name"] + "." + meth) if tm else None
                if mid:
                    src["calls"].append({"to": mid, "line": d["line"], "how": "dynamic", "why": d["why"]})
    for f in funcs:
        f["callers"] = []
    for f in funcs:
        for c in f["calls"]:
            by_id[c["to"]]["callers"].append(f["id"])
    for f in funcs:
        f["callers"] = sorted(set(f["callers"]))
    return funcs


def prompts(repo, funcs):
    out = []
    names = {}
    for f in funcs:
        for s in f.pop("_strings"):
            names.setdefault(os.path.basename(s), set()).add(f["id"])
    for p in sorted(repo.rglob("*")):
        rel = p.relative_to(repo).as_posix()
        if rel.startswith(SKIP_DIRS) or not p.is_file() or not rel.endswith(".txt") or "requirements" in rel:
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        out.append({"path": rel, "lines": len(txt.splitlines()), "sha256": sha(p.read_bytes()), "head": txt[:1200],
                    "used_by": sorted(names.get(p.name, set()))})
    for f in funcs:
        f["prompts"] = sorted(x["path"] for x in out if f["id"] in x["used_by"])
    return out


def join_inventory(funcs):
    rows = list(csv.DictReader(open(INVENTORY, encoding="utf-8")))
    spans = {}
    for f in funcs:
        spans.setdefault(f["path"], []).append(f)
    out, missed = [], []
    for i, r in enumerate(rows):
        ln = int(r["line"]) if r["line"].isdigit() else None
        cands = [f for f in spans.get(r["file"], []) if ln and f["line"] <= ln <= f["end"] and f["name"] != "<module>"]
        cands.sort(key=lambda f: f["lines"])
        fid = cands[0]["id"] if cands else None
        if fid is None:
            missed.append("%s:%s" % (r["file"], r["line"]))
        rec = {"n": i + 1, "function_id": fid, **{k: r[k] for k in ("layer", "file", "line", "function", "path", "role", "kind",
               "effect_on_causal_output", "output_contract", "answer_validation", "answer_kept_in", "temperature", "basis",
               "observed_calls_real")}}
        out.append(rec)
    by = {}
    for r in out:
        if r["function_id"]:
            by.setdefault(r["function_id"], []).append(r["n"])
    for f in funcs:
        f["llm_points"] = by.get(f["id"], [])
    return out, missed


def steps(funcs):
    """main.py's logged steps, mapped to the functions each step calls (from the main() body, by line ranges)."""
    main = next(f for f in funcs if f["id"] == "main.py::main")
    src = (REPO / "main.py").read_text(encoding="utf-8").splitlines()
    marks = []
    for i in range(main["line"] - 1, main["end"]):
        m = re.search(r"logger\.(step|section)\((?:(\d+), *8, *)?\"([^\"]+)\"", src[i])
        if m:
            marks.append((i + 1, m.group(2), m.group(3)))
    out = []
    for k, (ln, n, title) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else main["end"] + 1
        ids = []
        for c in main["calls"]:
            if ln <= c["line"] < end and c["to"] not in ids and not c["to"].startswith("utils/logger.py"):
                ids.append(c["to"])
        out.append({"line": ln, "n": int(n) if n else None, "title": title, "calls": ids})
    return out


def externals_listing(path):
    if not path or not Path(path).exists():
        return []
    return json.load(open(path, encoding="utf-8"))


def main():
    global REPO
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(RESEARCH.parent / "Causal-Copilot"))
    ap.add_argument("--out", default=str(HERE / "model.json"))
    ap.add_argument("--externals-listing", default=str(HERE / "externals_listing.json"))
    a = ap.parse_args()
    REPO = Path(a.repo).resolve()
    digest, checked = manifest_check(REPO)
    rels = sorted(p.relative_to(REPO).as_posix() for p in REPO.rglob("*.py")
                  if not p.relative_to(REPO).as_posix().startswith(SKIP_DIRS))
    mods, funcs, errors = [], [], []
    for rel in rels:
        try:
            m, fs = parse_module(REPO, rel)
        except SyntaxError as e:
            errors.append({"path": rel, "error": str(e)})
            continue
        mods.append(m)
        funcs += fs
    funcs = resolve(funcs, mods)
    pr = prompts(REPO, funcs)
    inv, missed = join_inventory(funcs)
    st = {}
    for f in funcs:
        for fld in f["reads"]:
            st.setdefault(fld, {"writers": [], "readers": []})["readers"].append(f["id"])
        for fld in f["writes"]:
            st.setdefault(fld, {"writers": [], "readers": []})["writers"].append(f["id"])
    # the CLI path: everything reachable from main.py's main()
    reach, todo = set(), ["main.py::main"]
    by_id = {f["id"]: f for f in funcs}
    while todo:
        x = todo.pop()
        if x in reach:
            continue
        reach.add(x)
        todo += [c["to"] for c in by_id[x]["calls"]]
    for f in funcs:
        f["on_cli_path"] = f["id"] in reach
    for m in mods:
        m["on_cli_path"] = any(by_id[i]["on_cli_path"] for i in m["functions"])
    model = {
        "about": "Inside Causal-Copilot: a typed model of the first-party code at upstream a31aa7c, extracted from the AST by "
                 "site/copilot/extract.py. Calls carry how they were resolved; what the AST cannot resolve is listed.",
        "tickets": ["TEAM-13"],
        "baseline_commit": "a31aa7c", "manifest": "manifests/baseline_a31aa7c.sha256", "manifest_sha256": digest,
        "files_checked_against_manifest": checked,
        "counts": {"modules": len(mods), "functions": len(funcs), "lines": sum(m["lines"] for m in mods),
                   "cli_path_functions": len(reach), "calls_resolved": sum(len(f["calls"]) for f in funcs),
                   "calls_unresolved": sum(len(f["calls_unresolved"]) for f in funcs),
                   "calls_internal_dynamic": sum(1 for f in funcs for c in f["calls_unresolved"] if c["kind"] == "internal-dynamic"), "llm_points": len(inv),
                   "llm_points_unjoined": len(missed), "state_fields": len(st), "prompts": len(pr), "parse_errors": len(errors)},
        "modules": mods, "functions": {f["id"]: f for f in funcs}, "state": st, "prompts": pr, "llm_points": inv,
        "llm_points_unjoined": missed, "steps": steps(funcs), "parse_errors": errors,
        "externals": externals_listing(a.externals_listing),
    }
    Path(a.out).write_text(json.dumps(model, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print("model: %(modules)d modules, %(functions)d functions, %(lines)d lines; CLI path %(cli_path_functions)d functions; "
          "calls %(calls_resolved)d resolved / %(calls_unresolved)d unresolved; LLM points %(llm_points)d (%(llm_points_unjoined)d unjoined); "
          "%(state_fields)d state fields; %(prompts)d prompts; %(parse_errors)d parse errors" % model["counts"])


REPO = None
if __name__ == "__main__":
    main()
