"""Static scan of every LLM call site in the Causal-Copilot tree (AST-based, no imports of the repo).

  python llm_inventory_scan.py REPO OUT_JSON

Two layers:
  api      a call to `<something>.chat_completion(...)` or a direct OpenAI client call: where a request is issued
  wrapper  a call to a repo function that itself contains an api call (e.g. LLM_parse_query): a logical decision point
"""
import ast
import json
import os
import sys

repo, out = sys.argv[1], sys.argv[2]
SKIP = ("externals" + os.sep, ".git" + os.sep, "output" + os.sep)
API_ATTRS = {"chat_completion"}
RAW_SDK = {"create"}           # client.chat.completions.create


def lit(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def src(node, text):
    try:
        return ast.get_source_segment(text, node)
    except Exception:
        return None


class V(ast.NodeVisitor):
    def __init__(self, rel, text):
        self.rel, self.text, self.stack, self.rows, self.funcs = rel, text, [], [], {}

    def visit_FunctionDef(self, node):
        self.stack.append(node)
        qual = ".".join(n.name for n in self.stack)
        self.funcs[qual] = node
        self.generic_visit(node)
        self.stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self.stack.append(node)
        self.generic_visit(node)
        self.stack.pop()

    def visit_Call(self, node):
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
        chain = src(f, self.text) or ""
        kind = None
        if name in API_ATTRS:
            kind = "api"
        elif name in RAW_SDK and "completions" in chain:
            kind = "api_raw_sdk"
        if kind:
            kw = {k.arg: k.value for k in node.keywords if k.arg}
            pos = node.args
            def get(key, idx=None):
                if key in kw:
                    return kw[key]
                if idx is not None and len(pos) > idx:
                    return pos[idx]
                return None
            prompt, system = get("prompt", 0), get("system_prompt", 1)
            jr, rf, temp, model, msgs = get("json_response"), get("response_format"), get("temperature"), get("model"), get("messages")
            encl = [n for n in self.stack if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            fn = encl[-1] if encl else None
            self.rows.append({
                "kind": kind, "file": self.rel, "line": node.lineno,
                "function": ".".join(n.name for n in self.stack) or "<module>",
                "function_span": [fn.lineno, fn.end_lineno] if fn else None,
                "call": chain,
                "json_response": (lit(jr) if jr is not None else False),
                "response_format": (src(rf, self.text) if rf is not None else None),
                "temperature": (src(temp, self.text) if temp is not None else "default 0.0"),
                "model_override": (src(model, self.text) if model is not None else None),
                "uses_messages_list": msgs is not None,
                "system_prompt": (lit(system) if system is not None and lit(system) is not None else (src(system, self.text) if system is not None else "default 'You are a helpful assistant.'")),
                "prompt_expr": (src(prompt, self.text) or "")[:160] if prompt is not None else None,
            })
        self.generic_visit(node)


rows, funcs_with_api, all_calls = [], {}, []
trees = {}
for root, dirs, files in os.walk(repo):
    rel_root = os.path.relpath(root, repo)
    if any((rel_root + os.sep).startswith(s) for s in SKIP):
        continue
    for fn in files:
        if not fn.endswith(".py"):
            continue
        path = os.path.join(root, fn)
        rel = os.path.relpath(path, repo).replace(os.sep, "/")
        text = open(path, encoding="utf-8", errors="replace").read()
        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            rows.append({"kind": "unparseable", "file": rel, "line": e.lineno, "function": None})
            continue
        v = V(rel, text)
        v.visit(tree)
        trees[rel] = (tree, text)
        rows.extend(v.rows)
        for r in v.rows:
            funcs_with_api.setdefault(r["function"].split(".")[-1], set()).add(rel)

# wrapper layer: calls (anywhere) to a function name that contains an api call, excluding generic names
wrappers = {n for n in funcs_with_api if n not in ("forward", "__init__", "<module>", "generation", "interaction", "main")}
wrows = []
for rel, (tree, text) in trees.items():
    class W(ast.NodeVisitor):
        def __init__(self):
            self.stack = []
        def visit_FunctionDef(self, node):
            self.stack.append(node.name); self.generic_visit(node); self.stack.pop()
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_ClassDef(self, node):
            self.stack.append(node.name); self.generic_visit(node); self.stack.pop()
        def visit_Call(self, node):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
            if name in wrappers:
                wrows.append({"kind": "wrapper", "file": rel, "line": node.lineno, "function": ".".join(self.stack) or "<module>",
                              "calls": name, "defined_in": sorted(funcs_with_api[name])})
            self.generic_visit(node)
    W().visit(tree)

# textual cross-check: every occurrence of 'chat_completion(' or 'completions.create(' outside llm/ and comments
import re
text_hits = []
for rel, (tree, text) in trees.items():
    for i, line in enumerate(text.splitlines(), 1):
        s = line.split("#", 1)[0]
        if re.search(r"\bchat_completion\(|completions\.create\(", s) and not re.search(r"^\s*(async\s+)?def\s", s):
            text_hits.append((rel, i))
api_lines = {(r["file"], r["line"]) for r in rows if r["kind"].startswith("api")}
# a multi-line call starts on the line the regex sees, so compare by (file, line)
missing = sorted(set(text_hits) - api_lines)
json.dump({"api_sites": [r for r in rows if r["kind"].startswith("api")], "wrapper_sites": wrows,
           "unparseable": [r for r in rows if r["kind"] == "unparseable"],
           "text_hits": len(text_hits), "text_hits_not_matched_by_ast": missing}, open(out, "w"), indent=1)
api = [r for r in rows if r["kind"].startswith("api")]
print("api call sites (AST):", len(api), "| outside llm/:", len([r for r in api if not r["file"].startswith("llm/")]))
print("textual occurrences:", len(text_hits), "| not matched by AST:", missing)
print("wrapper functions:", sorted(wrappers))
print("wrapper call sites:", len(wrows))
from collections import Counter
print("by top-level dir:", dict(Counter(r["file"].split("/")[0] for r in api)))
