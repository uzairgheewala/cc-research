"""Build "Inside Causal-Copilot" (TEAM-13): a guided site that explains how every part of Causal-Copilot works.

    python site/copilot/build.py [--out site/_build/copilot]
    python site/copilot/build.py --bind STEP [STEP ...] | all    record that a step page was read against the current code

Reads only committed files (CI has no Causal-Copilot checkout): model.json (extract.py), excerpts.json (snip.py),
content/steps/*.json and algorithms.json (hand-written walkthroughs), replay.json (export_replay.py), findings in each step
file, and a few result files for numbers. Pages: the run map, nine step pages, reference pages (state, model points,
algorithms, prompts, modules and functions, off-path code), the replay, and about. A "Show what our audits found" switch
reveals the findings layer on every page; without JavaScript it is a checkbox.

Fails (exit 1) on: model.json not built from the baseline manifest it names; a content function or prompt that is not in the
model; an excerpt whose function hash differs from the one snip.py copied; a finding whose source report is missing; a
number whose source file or pointer is missing; a broken internal link. Lists step pages whose functions changed since they
were bound (re-read)."""
import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = "https://github.com/uzairgheewala/Causal-Copilot/blob/a31aa7cab277d7e19478bc326dbec154525969cc/"
STEP_ORDER = ["setup", "data-and-query", "statistics-and-knowledge", "eda", "selection", "execution", "refinement",
              "evaluation", "report"]
BINDINGS = HERE / "bindings.json"
ERRORS, WARN, SOURCES = [], [], {}


def esc(x):
    return html.escape(str(x), quote=True)


def load(p):
    return json.load(open(p, encoding="utf-8"))


# ------------------------------------------------------------------ inputs
MODEL = load(HERE / "model.json")
F = MODEL["functions"]
EX = load(HERE / "excerpts.json") if (HERE / "excerpts.json").exists() else {"functions": {}, "ranges": {}}
STEPS = {}
for p in sorted((HERE / "content" / "steps").glob("*.json")):
    d = load(p)
    STEPS[d["slug"]] = d
ALGOS = load(HERE / "algorithms.json") if (HERE / "algorithms.json").exists() else []
REPLAY = load(HERE / "replay.json") if (HERE / "replay.json").exists() else None
MODS = {m["path"]: m for m in MODEL["modules"]}
EXPLAINED = {}
for _slug, _d in STEPS.items():
    for _s in _d.get("sequence", []):
        EXPLAINED.setdefault(_s["function"], [])
        if _slug not in EXPLAINED[_s["function"]]:
            EXPLAINED[_s["function"]].append(_slug)


def num(path, *ptr, fmt=None):
    """A number from a committed result file, recorded with the file's sha256 (listed on the about page)."""
    f = ROOT / path
    if not f.exists():
        ERRORS.append("number source missing: %s" % path)
        return "?"
    SOURCES[path] = hashlib.sha256(f.read_bytes()).hexdigest()
    d = load(f)
    try:
        for k in ptr:
            d = d[k] if not callable(k) else k(d)
    except (KeyError, IndexError, TypeError, StopIteration):
        ERRORS.append("number not found: %s %s" % (path, ptr))
        return "?"
    s = fmt.format(d) if fmt and isinstance(d, (int, float)) else str(d)
    return f'<a class="ev" href="{evbase()}{esc(path)}" title="{esc(path)}">{esc(s)}</a>'


EVBASE = [""]


def evbase():
    return EVBASE[0]


# ------------------------------------------------------------------ links and small parts
def mod_slug(path):
    return "m-" + re.sub(r"[^A-Za-z0-9]+", "-", path[:-3]).strip("-").lower()


def fn_anchor(fid):
    return "f-" + hashlib.sha1(fid.encode()).hexdigest()[:10]


def fn_link(fid, text=None, prefix=""):
    f = F[fid]
    label = text or ((f["cls"] + "." if f["cls"] else "") + f["name"])
    return f'<a class="fn" href="{prefix}{mod_slug(f["path"])}.html#{fn_anchor(fid)}" title="{esc(fid)}"><code>{esc(label)}</code></a>'


def src_link(path, a=None, b=None, text=None):
    frag = ("#L%d-L%d" % (a, b)) if a and b else ("#L%d" % a if a else "")
    return f'<a class="src" href="{UPSTREAM}{esc(path)}{frag}">{esc(text or path)}</a>'


def chip(text, tone="plain"):
    col = {"plain": ("#4E5751", "#FFFFFF", "#C9CEC6"), "llm": ("#5B3E8E", "#EFEAF6", "#5B3E8E"),
           "write": ("#8E2A2A", "#F6E7E7", "#8E2A2A"), "cli": ("#1D5C99", "#E6EEF6", "#1D5C99"),
           "warn": ("#9A4A0E", "#FBEFE4", "#B85A12")}[tone]
    return (f'<span class="chip" style="display: inline-block; padding: 0 8px; border-radius: 10px; border: 1px solid {col[2]}; '
            f'background: {col[1]}; color: {col[0]}; font-size: 12px; line-height: 19px; font-weight: 600">{esc(text)}</span>')


def code_block(text, first_line, path=None):
    rows = text.split("\n")
    body = "\n".join(f'<span class="ln">{first_line + i:>4}</span> {esc(r)}' for i, r in enumerate(rows))
    link = (f'<div class="codehead">{src_link(path, first_line, first_line + len(rows) - 1, "%s, lines %d-%d" % (path, first_line, first_line + len(rows) - 1))}</div>'
            if path else "")
    return f'<figure class="code">{link}<pre><code>{body}</code></pre></figure>'


def finding(fd, prefix=""):
    lab = fd.get("label", "unclear")
    return (f'<div class="finding"><span class="flabel">{esc(lab)}</span> {esc(fd["text"])} '
            f'<a class="fsrc" href="{evbase()}{esc(fd["source"])}">{esc(fd["source"].split("/")[-1])}</a></div>')


def P(t):
    return f'<p class="prose">{t}</p>'


def H2(t, a=None):
    return f'<h2{" id=%s" % esc(a) if a else ""}>{t}</h2>'


def table(headers, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr%s>%s</tr>" % ((' class="%s"' % r[1]) if isinstance(r, tuple) else "",
                                    "".join(f"<td>{c}</td>" for c in (r[0] if isinstance(r, tuple) else r))) for r in rows)
    return f'<div class="tbl"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# ------------------------------------------------------------------ checks
def check_inputs():
    man = ROOT / MODEL["manifest"]
    if not man.exists() or hashlib.sha256(man.read_bytes()).hexdigest() != MODEL["manifest_sha256"]:
        ERRORS.append("model.json was built from a manifest that differs from %s (re-run extract.py)" % MODEL["manifest"])
    if EX.get("manifest_sha256") != MODEL["manifest_sha256"]:
        ERRORS.append("excerpts.json and model.json were taken from different code (re-run snip.py)")
    for slug in STEP_ORDER:
        if slug not in STEPS:
            ERRORS.append("step page content missing: content/steps/%s.json" % slug)
    for slug, d in STEPS.items():
        for s in d.get("sequence", []):
            if s["function"] not in F:
                ERRORS.append("%s: function not in the model: %s" % (slug, s["function"]))
                continue
            ex = s.get("excerpt")
            if ex:
                key = "%s:%d-%d" % (F[s["function"]]["path"], ex["start"], ex["end"])
                r = EX["ranges"].get(key)
                if not r:
                    ERRORS.append("%s: excerpt %s not in excerpts.json (re-run snip.py)" % (slug, key))
                elif r["sha256"] != F[s["function"]]["sha256"]:
                    ERRORS.append("%s: excerpt %s was copied from a different version of %s" % (slug, key, s["function"]))
        for k in ("llm_calls", "failure_paths", "change_here"):
            for x in d.get(k, []):
                if x.get("function") and x["function"] not in F:
                    ERRORS.append("%s: %s names a function not in the model: %s" % (slug, k, x["function"]))
        for fd in d.get("findings", []):
            if not (ROOT / fd["source"]).exists():
                ERRORS.append("%s: finding source missing: %s" % (slug, fd["source"]))
    for a in ALGOS:
        if a.get("fit_function") and a["fit_function"] not in F:
            ERRORS.append("algorithms.json: %s fit function not in the model: %s" % (a.get("class"), a["fit_function"]))


def step_functions(d):
    ids = [s["function"] for s in d.get("sequence", [])]
    for k in ("llm_calls", "failure_paths", "change_here"):
        ids += [x["function"] for x in d.get(k, []) if x.get("function")]
    return sorted(set(i for i in ids if i in F))


def reread():
    b = load(BINDINGS) if BINDINGS.exists() else {}
    out = []
    for slug, d in STEPS.items():
        seen = b.get(slug)
        if seen is None:
            out.append((slug, "never bound"))
            continue
        ch = [fid for fid in step_functions(d) if seen.get(fid) != F[fid]["sha256"]]
        if ch:
            out.append((slug, "functions changed or added since binding: %s" % ", ".join(ch[:5])))
    return out


def bind(slugs):
    b = load(BINDINGS) if BINDINGS.exists() else {}
    for slug, d in STEPS.items():
        if "all" in slugs or slug in slugs:
            b[slug] = {fid: F[fid]["sha256"] for fid in step_functions(d)}
    BINDINGS.write_text(json.dumps(b, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("bound:", ", ".join(sorted(b)))


# ------------------------------------------------------------------ page frame
NAV = [("index", "One run"), ("steps", "The steps"), ("state", "State"), ("llm", "Model calls"), ("algorithms", "Algorithms"),
       ("prompts", "Prompts"), ("modules", "Code"), ("offpath", "Off the path"), ("replay", "Replay"), ("about", "About")]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#F2F3EF;color:#17201B;font-family:'IBM Plex Sans','Helvetica Neue',sans-serif;font-size:16px;line-height:25px}
a{color:#1D5C99}a:hover{color:#123E69}
a.ev,a.src{color:inherit;text-decoration:none;border-bottom:1px dotted #8FA9C4}
a.fn{text-decoration:none}a.fn code{color:#1D5C99}
code,pre{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:13px}
header.top{position:sticky;top:0;z-index:10;background:#FFFFFF;border-bottom:1px solid #C9CEC6}
header.top .bar{max-width:1360px;margin:0 auto;display:flex;align-items:center;gap:10px 22px;padding:10px 24px;flex-wrap:wrap}
.up{font-size:13px;color:#4E5751;text-decoration:none;border-right:1px solid #C9CEC6;padding-right:14px}.up:hover{color:#1D5C99}
.brand{font-family:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;font-size:21px;font-weight:700;color:#17201B;text-decoration:none}
nav.top{display:flex;gap:4px 6px;flex-wrap:wrap;font-size:13px}
nav.top a{padding:3px 10px;border:1px solid #C9CEC6;border-radius:14px;text-decoration:none;color:#17201B}
nav.top a[aria-current=page]{background:#17201B;color:#FFFFFF;border-color:#17201B}
.fswitch{margin-left:auto;font-size:13px;display:flex;align-items:center;gap:8px;cursor:pointer;user-select:none;padding:3px 10px 3px 4px;border:1px solid #B85A12;border-radius:14px;color:#9A4A0E}
.fswitch .knob{width:30px;height:18px;border-radius:9px;background:#E3E6E0;position:relative;display:inline-block}
.fswitch .knob::after{content:"";position:absolute;left:2px;top:2px;width:14px;height:14px;border-radius:7px;background:#FFFFFF;box-shadow:0 0 0 1px #C9CEC6}
#ff:checked ~ header .fswitch{background:#FBEFE4}
#ff:checked ~ header .fswitch .knob{background:#B85A12}
#ff:checked ~ header .fswitch .knob::after{left:14px}
#ff:focus-visible ~ header .fswitch{outline:2px solid #1D5C99}
main{padding:24px 24px 40px}
.page{max-width:1200px;margin:0 auto;display:flex;flex-direction:column;gap:18px}
.kicker{font-size:13px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;color:#4E5751}
h1{overflow-wrap:anywhere;margin:0;font-family:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;font-size:38px;line-height:44px}
h2{margin:10px 0 0;font-family:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;font-size:26px;line-height:32px}
h3{margin:4px 0 0;font-size:18px;line-height:24px}
.prose{max-width:80ch;margin:0}
.q{padding:12px 16px;background:#FFFFFF;border-left:4px solid #1D5C99;border-radius:6px;font-size:19px;line-height:27px}
.card{padding:16px 18px;background:#FFFFFF;border:1px solid #C9CEC6;border-radius:12px;display:flex;flex-direction:column;gap:8px;min-width:0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:12px}
.seq{display:flex;flex-direction:column;gap:12px;counter-reset:s}
.seq > .card{position:relative;padding-left:52px}
.seq > .card::before{counter-increment:s;content:counter(s);position:absolute;left:16px;top:16px;width:24px;height:24px;border-radius:12px;background:#17201B;color:#FFFFFF;font-size:13px;line-height:24px;text-align:center;font-weight:600}
figure.code{margin:0;background:#17201B;border-radius:10px;overflow:hidden}
figure.code .codehead{padding:6px 12px;background:#2C3631;font-size:12px}
figure.code .codehead a{color:#C7CFC9;border-bottom-color:#6A716B}
figure.code pre{margin:0;padding:10px 12px;overflow-x:auto;color:#E8ECE6;line-height:19px}
figure.code .ln{color:#6A716B;user-select:none}
.tbl{overflow-x:auto;background:#FFFFFF;border:1px solid #C9CEC6;border-radius:12px;padding:4px 6px}
.tbl table{border-collapse:collapse;width:100%;font-size:14px;line-height:20px}
.tbl th{text-align:left;padding:7px 8px;color:#4E5751;border-bottom:1.5px solid #C9CEC6;white-space:nowrap}
.tbl td{padding:7px 8px;border-bottom:1px solid #E3E6E0;vertical-align:top}
.finding{display:none;padding:8px 12px;background:#FBEFE4;border:1px solid #B85A12;border-radius:8px;font-size:14px;line-height:21px}
.flabel{display:inline-block;padding:0 7px;border-radius:9px;background:#9A4A0E;color:#FFFFFF;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.4px}
.fsrc{font-size:12px}
#ff:checked ~ main .finding{display:block}
#ff:checked ~ main .fonly{display:block}
.fonly{display:none}
.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr));gap:10px}
.flow a.box{display:flex;flex-direction:column;gap:4px;padding:12px 14px;background:#FFFFFF;border:1.5px solid #C9CEC6;border-radius:12px;text-decoration:none;color:#17201B;min-height:120px}
.flow a.box:hover{border-color:#1D5C99}
.flow .n{font-size:12px;font-weight:600;color:#4E5751;letter-spacing:.6px;text-transform:uppercase}
.flow .t{font-family:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;font-size:20px;line-height:24px;font-weight:600}
.small{font-size:13px;line-height:19px;color:#4E5751}
details.mod{background:#FFFFFF;border:1px solid #C9CEC6;border-radius:10px;padding:8px 12px}
details.mod summary{cursor:pointer;font-weight:600}
.fnrec{border-top:1px solid #E3E6E0;padding:12px 0;display:flex;flex-direction:column;gap:6px}
.arms{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.arm{background:#FFFFFF;border:1px solid #C9CEC6;border-radius:10px;padding:10px 12px;min-width:0;font-size:14px;line-height:20px;overflow-wrap:anywhere}
.arm pre{white-space:pre-wrap;margin:0;font-size:12px;line-height:17px;max-height:220px;overflow:auto;background:#F2F3EF;padding:6px;border-radius:6px}
footer.about{max-width:1200px;margin:0 auto 40px;padding:0 24px;font-size:13px;line-height:19px;color:#4E5751}
:not(pre) > code{overflow-wrap:anywhere;word-break:break-word}
details,summary,.fnrec,.card,.page > *{min-width:0;max-width:100%}
figure.code{max-width:100%;min-width:0;width:100%}
.fnrec > *,.card > *,details > *{min-width:0;max-width:100%}
figure.code pre{max-width:100%}
details{overflow:hidden}
.chip{max-width:100%;overflow-wrap:anywhere}
@media (max-width: 760px){.arms{grid-template-columns:1fr}}
@media (max-width: 640px){main{padding:16px 16px 32px} header.top{position:static} header.top .bar{padding:10px 16px} h1{font-size:30px;line-height:36px}
 .seq > .card{padding-left:16px;padding-top:44px} .seq > .card::before{top:12px} .fswitch{margin-left:0}}
"""


def frame(slug, title, kicker, body, depth=""):
    nav = "".join(f'<a href="{depth}{s}.html"{" aria-current=page" if s == slug else ""}>{esc(t)}</a>' for s, t in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Inside Causal-Copilot</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<input type="checkbox" id="ff" style="position: absolute; left: -9999px">
<header class="top"><div class="bar"><a class="up" href="{depth}../index.html">← Causal Atlas</a><a class="brand" href="{depth}index.html">Inside Causal-Copilot</a>
<nav class="top" aria-label="Sections">{nav}</nav>
<label class="fswitch" for="ff"><span class="knob" aria-hidden="true"></span> Show what our audits found</label></div></header>
<main><div class="page"><div><div class="kicker">{esc(kicker)}</div><h1>{esc(title)}</h1></div>
{body}
</div></main>
<footer class="about"><p>How Causal-Copilot works, read from its code at upstream commit a31aa7c (MIT licence, © 2026 Causal-Copilot
contributors; excerpts are quoted under that licence). Part of the <a href="{depth}../index.html">Causal Atlas</a>, a UCSD DSC 180
capstone. <a href="{depth}about.html">How this site is built</a>.</p></footer>
<script>(function(){{try{{var c=document.getElementById('ff');if(localStorage.getItem('cc-findings')==='1')c.checked=true;
c.addEventListener('change',function(){{try{{localStorage.setItem('cc-findings',c.checked?'1':'0')}}catch(e){{}}}});}}catch(e){{}}}})();</script>
</body>
</html>
"""


# ------------------------------------------------------------------ the run map
def step_stats(d):
    fids = [s["function"] for s in d.get("sequence", []) if s["function"] in F]
    reads = sorted({x["field"] for x in d.get("inputs", [])})
    writes = sorted({x["field"] for x in d.get("outputs", [])})
    return fids, reads, writes, len(d.get("llm_calls", []))


def state_matrix():
    groups = sorted({x["field"].split(".")[0] for d in STEPS.values() for x in d.get("inputs", []) + d.get("outputs", [])})
    rows = []
    for i, slug in enumerate(STEP_ORDER, 1):
        d = STEPS.get(slug)
        if not d:
            continue
        r = {x["field"].split(".")[0] for x in d.get("inputs", [])}
        w = {x["field"].split(".")[0] for x in d.get("outputs", [])}
        cells = []
        for g in groups:
            t = ("R" if g in r else "") + ("W" if g in w else "")
            bg = {"R": "#E6EEF6", "W": "#F6E7E7", "RW": "#EFEAF6"}.get(t, "")
            cells.append(f'<span style="display: inline-block; min-width: 30px; text-align: center; border-radius: 6px; background: {bg}; font-weight: 600">{t}</span>' if t else "")
        rows.append([f'{i}. <a href="step-{slug}.html">{esc(d["title"])}</a>'] + cells)
    return table(["Step"] + [f"<code>{esc(g)}</code>" for g in groups], rows)


def page_index():
    c = MODEL["counts"]
    boxes = []
    for i, slug in enumerate(STEP_ORDER, 1):
        d = STEPS.get(slug)
        if not d:
            continue
        fids, reads, writes, nllm = step_stats(d)
        chips = " ".join(x for x in [chip("%d model call%s" % (nllm, "" if nllm == 1 else "s"), "llm") if nllm else "",
                                      chip("%d functions" % len(fids)), chip("writes %d fields" % len(writes), "cli") if writes else ""] if x)
        boxes.append(f'<a class="box" href="step-{slug}.html"><span class="n">Step {i}</span><span class="t">{esc(d["title"])}</span>'
                     f'<span class="small">{esc(d["question"])}</span><span>{chips}</span></a>')
    graph_writers = [p for p in MODEL["llm_points"] if p["effect_on_causal_output"].startswith("direct")]
    body = [
        '<p class="q">What happens, step by step, when you run Causal-Copilot on a table of data, and where does each decision come from?</p>',
        P("Causal-Copilot is an agent: you give it a data file and a question, and it chooses a causal-discovery algorithm, runs "
          "it, refines the resulting graph with a language model, and writes a report. Every step reads and writes one shared "
          f"object, <code>global_state</code>. This site follows one command-line run through the code, step by step, at upstream "
          f"commit a31aa7c: {c['modules']} first-party modules, {c['functions']:,} functions, {c['lines']:,} lines (plus vendored "
          f"libraries, listed under <a href=\"offpath.html\">off the path</a>). {c['cli_path_functions']} of the functions are on "
          f"the path a command-line run takes."),
        H2("One run, in nine steps"),
        f'<div class="flow">{"".join(boxes)}</div>',
        P(f'Purple marks a step that asks the language model something. Across the whole codebase there are '
          f'<a href="llm.html">{c["llm_points"]} points</a> that call the model; {len(graph_writers)} of them write to the causal graph directly.'),
        f'<div class="finding"><span class="flabel">code verified</span> Our audits found that the final graph is mostly decided by the '
        f'model reading column names: with names swapped, the model follows the labels. The audit layer on each page shows where. '
        f'<a class="fsrc" href="{evbase()}analysis/reports/pass3_llm_dependency_map.md">pass3_llm_dependency_map.md</a></div>',
        H2("What each step reads and writes"),
        P("The shared state has parts; each step reads some and writes others. R reads, W writes, RW both."),
        state_matrix(),
        H2("How to read this site"),
        P('Each step page says what the step does in plain words, what it reads and writes in the shared state, the functions '
          'in the order a run calls them (with the code that matters), every question it asks the model and what happens to the '
          'answer, how it fails, and where you would change it. The reference pages list everything: '
          '<a href="state.html">every state field</a>, <a href="llm.html">every model call</a>, <a href="algorithms.html">every algorithm</a>, '
          '<a href="prompts.html">every prompt</a> and <a href="modules.html">every function</a>. The <a href="replay.html">replay</a> '
          'shows one real recorded run, three times: with real names, neutral names, and names moved to other columns.'),
        P('The switch at the top right, “Show what our audits found”, adds the findings of our audits to every page. Off, the site '
          'is a neutral guide to the code.'),
    ]
    return frame("index", "One run, end to end", "Inside Causal-Copilot", "\n".join(body))


def page_steps():
    rows = []
    for i, slug in enumerate(STEP_ORDER, 1):
        d = STEPS.get(slug)
        if not d:
            continue
        rows.append([str(i), f'<a href="step-{slug}.html">{esc(d["title"])}</a>', esc(d["question"])])
    return frame("steps", "The steps", "Inside Causal-Copilot", table(["#", "Step", "The question it answers"], rows))


def call_tree(fid, depth=0, seen=None, maxd=3):
    seen = set() if seen is None else seen
    f = F[fid]
    kids = [c for c in f["calls"] if not c["to"].startswith("utils/logger.py") and c["to"] not in seen]
    seen |= {c["to"] for c in kids}
    note = " <span class=small>(by name at run time: %d wrappers)</span>" % sum(1 for c in kids if c["how"] == "dynamic") if any(c["how"] == "dynamic" for c in kids) else ""
    kids_static = [c for c in kids if c["how"] != "dynamic"]
    tag = " " + chip("model", "llm") if f["llm_points"] else ""
    inner = ""
    if depth < maxd and kids_static:
        inner = "<ul>" + "".join("<li>" + call_tree(c["to"], depth + 1, seen, maxd) + "</li>" for c in kids_static) + "</ul>"
    elif kids_static:
        inner = ' <span class="small">… %d more calls</span>' % len(kids_static)
    return fn_link(fid) + tag + note + inner


def page_step(i, slug):
    d = STEPS[slug]
    parts = [f'<p class="q">{esc(d["question"])}</p>', P(esc(d["plain_summary"]))]
    io = []
    if d.get("inputs"):
        io.append('<div class="card"><h3>Reads</h3>' + "".join(
            f'<div><a href="state.html#{esc(x["field"])}"><code>{esc(x["field"])}</code></a> · {esc(x["what"])}</div>' for x in d["inputs"]) + "</div>")
    if d.get("outputs"):
        io.append('<div class="card"><h3>Writes</h3>' + "".join(
            f'<div><a href="state.html#{esc(x["field"])}"><code>{esc(x["field"])}</code></a> · {esc(x["what"])}</div>' for x in d["outputs"]) + "</div>")
    if io:
        parts.append(f'<div class="grid">{"".join(io)}</div>')
    parts.append(H2("What runs, in order"))
    seq = []
    for s in d.get("sequence", []):
        f = F[s["function"]]
        ex = s.get("excerpt")
        code = ""
        if ex:
            key = "%s:%d-%d" % (f["path"], ex["start"], ex["end"])
            r = EX["ranges"].get(key)
            if r:
                code = code_block(r["text"], ex["start"], f["path"])
        tags = " ".join(t for t in [chip("asks the model", "llm") if s.get("llm") else "",
                                     chip("%s:%d" % (f["path"], f["line"]))] if t)
        seq.append(f'<div class="card"><div style="display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: center">'
                   f'{fn_link(s["function"])} {tags}</div><p class="prose">{esc(s["what"])}</p>{code}</div>')
    parts.append(f'<div class="seq">{"".join(seq)}</div>')
    roots = []
    for s_ in d.get("sequence", []):
        if s_["function"] in F and s_["function"] not in roots and not any(s_["function"] in [c["to"] for c in F[r]["calls"]] for r in roots):
            roots.append(s_["function"])
    parts.append('<details class="mod"><summary>The call tree under this step (three levels; logging left out)</summary>'
                 '<div class="small" style="padding: 6px 0">' + "".join('<ul style="margin: 4px 0"><li>' + call_tree(r) + "</li></ul>" for r in roots[:6]) + "</div></details>")
    if d.get("llm_calls"):
        parts.append(H2("What it asks the model"))
        rows = []
        for x in d["llm_calls"]:
            pr = x.get("prompt")
            rows.append([fn_link(x["function"]) if x.get("function") in F else "",
                         (f'<a href="prompts.html#{esc(pr)}"><code>{esc(pr.split("/")[-1])}</code></a>' if pr else "inline"),
                         esc(x["asks"]), esc(x["answer_used"]), esc(x["checked"])])
        parts.append(table(["Where", "Prompt", "It asks", "The answer is used to", "What is checked"], rows))
    if d.get("failure_paths"):
        parts.append(H2("How it fails"))
        parts.append("".join(f'<div class="card">{fn_link(x["function"]) if x.get("function") in F else ""}<p class="prose">{esc(x["what"])}</p></div>'
                             for x in d["failure_paths"]))
    if d.get("change_here"):
        parts.append(H2("Where you would change it"))
        parts.append("".join(f'<div class="card">{fn_link(x["function"]) if x.get("function") in F else ""}<p class="prose">{esc(x["what"])}</p></div>'
                             for x in d["change_here"]))
    if d.get("findings"):
        parts.append('<div class="fonly">' + H2("What our audits found here") + "</div>")
        parts.append("".join(finding(x) for x in d["findings"]))
    prev = STEP_ORDER[i - 2] if i > 1 and STEP_ORDER[i - 2] in STEPS else None
    nxt = STEP_ORDER[i] if i < len(STEP_ORDER) and STEP_ORDER[i] in STEPS else None
    pn = '<div class="grid">' + (f'<a class="card" href="step-{prev}.html">← {esc(STEPS[prev]["title"])}</a>' if prev else "<span></span>") + \
         (f'<a class="card" style="text-align: right" href="step-{nxt}.html">{esc(STEPS[nxt]["title"])} →</a>' if nxt else "") + "</div>"
    parts.append(pn)
    return frame("steps", d["title"], "Step %d of %d" % (i, len(STEP_ORDER)), "\n".join(parts))


# ------------------------------------------------------------------ reference pages
def page_state():
    rows = []
    for fld in sorted(MODEL["state"]):
        s = MODEL["state"][fld]
        w = sorted(set(s["writers"]))
        r = sorted(set(s["readers"]))
        cli = any(F[x]["on_cli_path"] for x in w + r)
        rows.append(([f'<code id="{esc(fld)}">{esc(fld)}</code>', ", ".join(fn_link(x) for x in w[:8]) + (" …" if len(w) > 8 else "") or "<span class=small>none found</span>",
                      ", ".join(fn_link(x) for x in r[:8]) + (" …" if len(r) > 8 else ""), "yes" if cli else ""], ""))
    groups = sorted({k.split(".")[0] for k in MODEL["state"]})
    body = [P("Every step reads and writes one object, <code>global_state</code>, built in "
              + fn_link("global_setting/Initialize_state.py::global_state_initialization") + ". Its parts: " +
              ", ".join(f"<code>{esc(g)}</code>" for g in groups) + ". Below, every field the code touches (two levels deep), with "
              "the functions that write it and those that read it. Fields set by name at run time (<code>setattr</code>) cannot be "
              f"seen in the code's text; {sum(len(f['setattrs']) for f in F.values())} such calls are listed on the about page."),
            table(["Field", "Written by", "Read by", "On the command-line path"], rows)]
    return frame("state", "The shared state", "Reference", "\n".join(body))


def page_llm():
    rows = []
    for p in MODEL["llm_points"]:
        fid = p["function_id"]
        cli = fid and F[fid]["on_cli_path"]
        eff = p["effect_on_causal_output"]
        tone = "write" if eff.startswith("direct") else ("llm" if p["kind"] == "decision" else "plain")
        rows.append([str(p["n"]), fn_link(fid) if fid else esc(p["function"]), src_link(p["file"], int(p["line"]) if p["line"].isdigit() else None, None, "%s:%s" % (p["file"], p["line"])),
                     esc(p["path"]), esc(p["role"]), chip(p["kind"], tone), esc(eff),
                     f'<span class="finding" style="display: none">{esc(p["answer_validation"])}</span>' if False else esc(p["answer_validation"]),
                     "yes" if cli else ""])
    body = [P(f'Every place the code asks a language model something: {len(rows)} logical points (a shared helper called from '
              f'several places counts once per caller), from our inventory '
              f'<a class="ev" href="{evbase()}analysis/results/llm_inventory/llm_inventory.csv">llm_inventory.csv</a>. “Kind” says what the '
              'answer is for: a decision, a description, an interpretation or a format repair. Red marks the points whose answer '
              'writes the causal graph directly.'),
            table(["#", "Function", "Line", "Reached from", "Role", "Kind", "Effect on the causal output", "How the answer is checked", "CLI path"], rows)]
    return frame("llm", "Every model call", "Reference", "\n".join(body))


def page_algorithms():
    rows = []
    for a in ALGOS:
        rows.append([fn_link(a["fit_function"], a["class"]) if a.get("fit_function") in F else f'<code>{esc(a["class"])}</code>',
                     esc(a.get("family", "")), esc(a.get("library", "")), ", ".join(f"<code>{esc(x)}</code>" for x in a.get("primary_params", [])),
                     esc(a.get("assumptions", "")), esc(a.get("output", "")), esc(a.get("notes", ""))])
    body = [P("Every algorithm the agent can choose. Each is a wrapper class in <code>causal_discovery/wrappers/</code> with the same "
              "interface: built from a parameter dictionary, then <code>fit(data)</code> returns the graph. "
              + fn_link("causal_discovery/program.py::Programming.forward") + " picks the class by name at run time."),
            table(["Algorithm", "Family", "Wraps", "Main parameters", "Assumptions", "Output", "Notes"], rows)]
    return frame("algorithms", "Every algorithm", "Reference", "\n".join(body))


def page_prompts():
    cards = []
    for p in MODEL["prompts"]:
        used = ", ".join(fn_link(x) for x in p["used_by"]) or '<span class="small">no caller found by name</span>'
        cards.append(f'<details class="mod" id="{esc(p["path"])}"><summary><code>{esc(p["path"])}</code> '
                     f'<span class="small">{p["lines"]} lines</span></summary><p class="small">Used by: {used}</p>'
                     f'{code_block(p["head"], 1, p["path"])}<p class="small">First 1,200 characters; the full text is at the link.</p></details>')
    body = [P(f"The {len(MODEL['prompts'])} text files the code builds its prompts and algorithm descriptions from. Many are filled "
              "in with the dataset's statistics and the domain-knowledge text before they are sent."), "".join(cards)]
    return frame("prompts", "Every prompt file", "Reference", "\n".join(body))


def fn_record(fid):
    f = F[fid]
    rows = []
    if EXPLAINED.get(fid):
        rows.append('<div class="small">Explained in: ' + ", ".join(f'<a href="step-{x}.html">{esc(STEPS[x]["title"])}</a>' for x in EXPLAINED[fid]) + "</div>")
    if f["doc"]:
        rows.append(f'<p class="prose small">{esc(f["doc"].splitlines()[0])}</p>')
    if f["calls"]:
        rows.append('<div class="small">Calls: ' + ", ".join(fn_link(c["to"]) + (" (by name at run time)" if c["how"] == "dynamic" else "")
                                                         for c in f["calls"][:30]) + (" …" if len(f["calls"]) > 30 else "") + "</div>")
    if f["callers"]:
        rows.append('<div class="small">Called by: ' + ", ".join(fn_link(c) for c in f["callers"][:20]) + (" …" if len(f["callers"]) > 20 else "") + "</div>")
    if f["reads"] or f["writes"]:
        rows.append('<div class="small">State: ' + (("writes " + ", ".join(f'<a href="state.html#{esc(x)}"><code>{esc(x)}</code></a>' for x in f["writes"])) if f["writes"] else "")
                    + ("; " if f["writes"] and f["reads"] else "") + (("reads " + ", ".join(f'<a href="state.html#{esc(x)}"><code>{esc(x)}</code></a>' for x in f["reads"][:12])) if f["reads"] else "") + "</div>")
    if f["llm_points"]:
        rows.append('<div class="small">' + chip("asks the model", "llm") + " " + ", ".join(f'<a href="llm.html">point {n}</a>' for n in f["llm_points"]) + "</div>")
    if f["prompts"]:
        rows.append('<div class="small">Prompts: ' + ", ".join(f'<a href="prompts.html#{esc(p)}"><code>{esc(p.split("/")[-1])}</code></a>' for p in f["prompts"]) + "</div>")
    src = EX["functions"].get(fid)
    code = ""
    if src and src["sha256"] == f["sha256"]:
        code = f'<details><summary class="small">Source ({f["lines"]} lines)</summary>{code_block(src["text"], src["line"], f["path"])}</details>'
    else:
        code = f'<div class="small">{src_link(f["path"], f["line"], f["end"], "Source, lines %d-%d" % (f["line"], f["end"]))}</div>'
    tags = " ".join(t for t in [chip("command-line path", "cli") if f["on_cli_path"] else ""] if t)
    return (f'<div class="fnrec" id="{fn_anchor(fid)}"><div><code><b>{esc((f["cls"] + "." if f["cls"] else "") + f["name"])}</b></code> {tags}</div>'
            f'<code class="small">{esc(f["signature"])}</code>{"".join(rows)}{code}</div>')


def page_module(path):
    m = MODS[path]
    body = [P(f'<code>{esc(path)}</code> · {m["lines"]} lines · {src_link(path, text="view on GitHub")}' + (" · " + chip("command-line path", "cli") if m["on_cli_path"] else "")),
            P(esc(m["doc"])) if m["doc"] else "",
            (P("Classes: " + ", ".join(f'<code>{esc(c["name"])}</code>' + (f' ({esc(", ".join(c["bases"]))})' if c["bases"] else "") for c in m["classes"])) if m["classes"] else ""),
            "".join(fn_record(fid) for fid in m["functions"])]
    return frame("modules", path, "Code", '<div class="card">' + "".join(body) + "</div>")


def page_modules():
    by = {}
    for m in MODEL["modules"]:
        by.setdefault(m["package"], []).append(m)
    blocks = []
    for pkg in sorted(by, key=lambda p: (-sum(1 for m in by[p] if m["on_cli_path"]), p)):
        ms = sorted(by[pkg], key=lambda m: m["path"])
        rows = "".join(f'<div>{chip("CLI", "cli") if m["on_cli_path"] else ""} <a href="{mod_slug(m["path"])}.html"><code>{esc(m["path"])}</code></a> '
                       f'<span class="small">{m["lines"]} lines, {len(m["functions"])} functions</span></div>' for m in ms)
        blocks.append(f'<details class="mod"{" open" if any(m["on_cli_path"] for m in ms) else ""}><summary>{esc(pkg)} '
                      f'<span class="small">{len(ms)} modules, {sum(m["lines"] for m in ms):,} lines</span></summary>{rows}</details>')
    body = [P(f'Every first-party module, grouped by package. Each module page lists its functions: signature, what it calls '
              f'and who calls it, the state it reads and writes, model calls and prompts, and (for the {MODEL["counts"]["cli_path_functions"]} '
              f'functions on the command-line path) its source.'), "".join(blocks)]
    return frame("modules", "Modules and functions", "Code", "\n".join(body))


def page_offpath():
    off = [m for m in MODEL["modules"] if not m["on_cli_path"]]
    by = {}
    for m in off:
        by.setdefault(m["package"], []).append(m)
    desc = {"web_demo": "the browser interface (a separate entry point with its own model calls; not reached by a command-line run)",
            "causal_inference": "effect estimation after discovery (treatment effects, heterogeneous effects); reached from the web demo",
            "causal_discovery": "parts of the discovery package a command-line run does not reach (benchmarking, tests, runtime estimators)",
            "report": "report helpers not on the run's path", "preprocess": "preprocessing helpers not on the run's path",
            "postprocess": "post-processing helpers not on the run's path", "data": "simulators and dataset helpers",
            "utils": "utilities", "llm": "the model client", "user": "user interaction"}
    rows = [[esc(p), str(len(v)), "{:,}".format(sum(m["lines"] for m in v)), esc(desc.get(p, "")),
             ", ".join(f'<a href="{mod_slug(m["path"])}.html"><code>{esc(m["path"].split("/")[-1])}</code></a>' for m in sorted(v, key=lambda m: -m["lines"])[:6])]
            for p, v in sorted(by.items(), key=lambda kv: -sum(m["lines"] for m in kv[1]))]
    ext = [[esc(e["name"]), str(e["py_files"]), "{:,}".format(e["py_lines"]), esc(e.get("what", "")), esc(", ".join(e.get("subpackages", [])))]
           for e in MODEL.get("externals", [])]
    body = [P("Code a command-line run never reaches, described at module level: what it is for and where to start reading."),
            table(["Package", "Modules", "Lines", "What it is", "Largest modules"], rows),
            H2("Vendored libraries"),
            P("Copies of other projects inside <code>externals/</code>. The wrappers call some of them instead of the installed "
              "packages, so a defect in a copy is a defect in Causal-Copilot."),
            table(["Library", "Python files", "Lines", "What it is", "Parts"], ext),
            '<div class="finding"><span class="flabel">code verified</span> The vendored copy of PC gives wrong answers even when '
            'its independence tests are answered perfectly (an oracle test); the installed causal-learn does not. '
            f'<a class="fsrc" href="{evbase()}analysis/reports/ab03_engine_forensics.md">ab03_engine_forensics.md</a></div>'
            if (ROOT / "analysis/reports/ab03_engine_forensics.md").exists() else ""]
    return frame("offpath", "Off the command-line path", "Code", "\n".join(body))


def page_replay():
    if not REPLAY:
        return frame("replay", "Replay one run", "Replay", P("No replay file."))
    arms = REPLAY["arms"]
    stages = []
    keys = [s["stage"] for s in arms[0]["stages"]]
    for k in keys:
        cells = []
        for a in arms:
            s = next((x for x in a["stages"] if x["stage"] == k), None)
            if not s:
                cells.append('<div class="arm">–</div>')
                continue
            bits = []
            if s.get("columns"):
                bits.append("<b>Columns the agent sees</b> (first 8): " + ", ".join(f"<code>{esc(c)}</code>" for c in s["columns"][:8]))
            if s.get("statistics") and k.startswith("04a"):
                bits.append("<b>Statistics</b>: " + ", ".join(f"{esc(x)} = {esc(y)}" for x, y in s["statistics"].items() if y is not None))
            if s.get("knowledge_head"):
                bits.append(f"<b>Domain knowledge it wrote</b><pre>{esc(s['knowledge_head'])}</pre>")
            if s.get("candidates") and k.startswith("06a"):
                bits.append("<b>Shortlist</b>: " + ", ".join(map(esc, s["candidates"])))
            if s.get("selected") and k.startswith("06b"):
                bits.append(f"<b>Chosen</b>: {esc(s['selected'])}<pre>{esc(s.get('selected_reason') or '')}</pre>")
            if s.get("arguments") and k.startswith("06c"):
                bits.append("<b>Hyperparameters</b>: " + ", ".join(f"{esc(x)} = {esc(y)}" for x, y in s["arguments"].items()))
            calls = [c for c in a["llm_calls"] if c["stage"] and k.replace("__FAILED", "") in c["stage"]]
            if calls:
                c = calls[0]
                bits.append(f"<b>{len(calls)} model call{'s' if len(calls) != 1 else ''}</b>; the first asked:<pre>{esc(c['prompt_head'])}</pre>"
                            f"and got:<pre>{esc(c['answer_head'])}</pre>")
            cells.append('<div class="arm">' + ("<br>".join(bits) if bits else '<span class="small">nothing recorded for this view</span>') + "</div>")
        title = arms[0]["stages"][keys.index(k)]["title"]
        stages.append(f'<h3>{esc(title)}</h3><div class="arms">{"".join(cells)}</div>')

    def edge_summary(a, key):
        e = a[key]
        return ", ".join(f"{len(v)} {esc(k.replace('_', ' '))}" for k, v in e.items() if v and k != "all_edges")

    final = "".join(f'<div class="arm"><b>{esc(a["label"])}</b> · {esc(a["status"])}<br>After the algorithm: {edge_summary(a, "edges_after_algorithm")}<br>'
                    f'After refinement: {edge_summary(a, "edges_after_refinement")}<br>'
                    f'The model set the direction of {len(a["llm_set_direction"])} pairs and forbade {len(a["llm_forbade"])}'
                    f'{" (lists capped at 60)" if len(a["llm_forbade"]) >= 60 else ""}.</div>' for a in arms)
    heads = "".join(f'<div class="arm"><b>{esc(a["label"])}</b><br><span class="small">run {esc(a["run_id"])} · {esc(a["model"])}</span></div>' for a in arms)
    body = [P("One recorded run of unmodified Causal-Copilot (a31aa7c, gpt-4o) on a CausalArena scenario, three times: the same numbers "
              "with real column names, with neutral names (V01, V02, …), and with the real names moved to other columns. Read across "
              "a row to see what changes when only the names change. Columns were shuffled in every arm."),
            f'<div class="arms">{heads}</div>', H2("How it ends"), f'<div class="arms">{final}</div>',
            '<div class="finding"><span class="flabel">code verified</span> In this scenario the algorithm choice and the edges the '
            'model writes change with the names while the numbers are identical. Across 30 such runs, swapped names made the model '
            f'follow the labels. <a class="fsrc" href="{evbase()}analysis/reports/bnd08_s2_results.md">bnd08_s2_results.md</a></div>',
            H2("Stage by stage"), "".join(stages)]
    return frame("replay", "Replay one run", "Replay", "\n".join(body))


def page_about(rr):
    c = MODEL["counts"]
    un = {}
    for f in F.values():
        for x in f["calls_unresolved"]:
            un[x["kind"]] = un.get(x["kind"], 0) + 1
    hows = {}
    for f in F.values():
        for x in f["calls"]:
            hows[x["how"]] = hows.get(x["how"], 0) + 1
    setattrs = [(fid, s) for fid, f in F.items() for s in f["setattrs"]]
    body = [P(f'Built from Causal-Copilot at upstream commit a31aa7c. Before anything is read, the extractor checks '
              f'{MODEL["files_checked_against_manifest"]} first-party files against <code>{esc(MODEL["manifest"])}</code> '
              f'(sha256 <code>{MODEL["manifest_sha256"][:12]}</code>); the site build refuses a model taken from different code.'),
            H2("What the extractor sees"),
            table(["", "Count"], [["Modules", str(c["modules"])], ["Functions", "{:,}".format(c["functions"])], ["Lines", "{:,}".format(c["lines"])],
                                  ["On the command-line path", str(c["cli_path_functions"])], ["State fields", str(c["state_fields"])],
                                  ["Prompt files", str(c["prompts"])], ["Model call points (joined from the inventory)", "%d of %d" % (c["llm_points"] - c["llm_points_unjoined"], c["llm_points"])]]),
            P("How each call between first-party functions was resolved:"),
            table(["How", "Calls"], [[esc(k), "{:,}".format(v)] for k, v in sorted(hows.items(), key=lambda kv: -kv[1])]),
            P('“dynamic” is the one dispatch the code does by name at run time (the algorithm wrappers), declared in the extractor '
              'with the line that does it. Calls the extractor did not resolve, by kind:'),
            table(["Kind", "Calls"], [[esc(k), "{:,}".format(v)] for k, v in sorted(un.items(), key=lambda kv: -kv[1])]),
            P('“library” and “builtin” are calls into Python or other packages; “value-method” are methods on data values '
              '(DataFrames, lists, strings); “internal-dynamic” are method calls on objects whose class the extractor cannot infer: '
              'they may be first-party and are counted, not drawn.'),
            H2("Fields set by name"),
            table(["Function", "Call", "Line"], [[fn_link(fid), esc("%s(%s, %r)" % (s["kind"], s["target"], s["name"])), str(s["line"])] for fid, s in setattrs[:80]]),
            H2("Step pages to re-read"),
            P("A step page is bound to the code of the functions it describes; a page whose functions change comes up here." if rr else
              "None: every step page was read against the current code."),
            table(["Step", "Why"], [[esc(s), esc(w)] for s, w in rr]) if rr else "",
            H2("Number sources"),
            table(["File", "sha256"], [[f'<a class="ev" href="{evbase()}{esc(p)}">{esc(p)}</a>', f"<code>{h[:12]}</code>"] for p, h in sorted(SOURCES.items())]),
            H2("Files"),
            P("<code>site/copilot/extract.py</code> (the model), <code>snip.py</code> (the source lines printed), "
              "<code>export_replay.py</code> (the replay), <code>content/steps/*.json</code> and <code>algorithms.json</code> (the "
              "walkthroughs, written by reading the code), <code>build.py</code> (this site).")]
    return frame("about", "How this site is built", "About", "\n".join(body))


# ------------------------------------------------------------------ main
def atlas_pages():
    """File names of the Atlas pages (site/pages.py), the targets of this site's ../ links."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("atlas_pages", ROOT / "site" / "pages.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return {"%s.html" % p["slug"] for p in m.PAGES}


def links_ok(pages):
    names, atlas = set(pages), atlas_pages()
    for name, h in pages.items():
        for t in re.findall(r'href="([^"#:]+\.html)(?:#[^"]*)?"', h):
            if t.startswith("../"):
                if t[3:] not in atlas:
                    ERRORS.append("%s: link %s is not an Atlas page" % (name, t))
            elif t not in names:
                ERRORS.append("%s: broken link %s" % (name, t))


def inbound_ok(pages, out):
    """Links from the Atlas into this site. The Atlas build runs first and cannot see these pages, so this build checks
    them: every href="copilot/..." in the Atlas pages next to out must name a page built here ("copilot/" is the index)."""
    atlas_dir = out.parent
    if not (atlas_dir / "index.html").exists():
        return None
    n = 0
    for f in sorted(atlas_dir.glob("*.html")):
        for t in re.findall(r'href="copilot/([^"#]*)(?:#[^"]*)?"', f.read_text(encoding="utf-8")):
            n += 1
            if (t or "index.html") not in pages:
                ERRORS.append("Atlas %s: link copilot/%s is not a page of this site" % (f.name, t))
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "site" / "_build" / "copilot"))
    ap.add_argument("--bind", nargs="+", default=None)
    ap.add_argument("--evidence-base", default=None)
    a = ap.parse_args()
    if a.bind:
        bind(a.bind)
        return
    import os
    repo, sha = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_SHA")
    EVBASE[0] = a.evidence_base or ("https://github.com/%s/blob/%s/" % (repo, sha) if repo and sha else "../../../")
    check_inputs()
    rr = reread()
    pages = {"index.html": page_index(), "steps.html": page_steps(), "state.html": page_state(), "llm.html": page_llm(),
             "algorithms.html": page_algorithms(), "prompts.html": page_prompts(), "modules.html": page_modules(),
             "offpath.html": page_offpath(), "replay.html": page_replay()}
    for i, slug in enumerate(STEP_ORDER, 1):
        if slug in STEPS:
            pages["step-%s.html" % slug] = page_step(i, slug)
    for path in MODS:
        pages[mod_slug(path) + ".html"] = page_module(path)
    pages["about.html"] = page_about(rr)
    links_ok(pages)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, h in pages.items():
        (out / name).write_text(h, encoding="utf-8", newline="\n")
    for w in WARN:
        print("WARN  " + w)
    for s, why in rr:
        print("REREAD step %s (%s)" % (s, why))
    inbound = inbound_ok(pages, out)
    print("links from the Atlas: " + ("%d checked" % inbound if inbound is not None else "not checked (no Atlas build in %s)" % out.parent))
    for e in ERRORS:
        print("ERROR " + e)
    print("built %d pages in %s; %d errors, %d warnings, %d step pages to re-read" % (len(pages), out, len(ERRORS), len(WARN), len(rr)))
    sys.exit(1 if ERRORS else 0)


if __name__ == "__main__":
    main()
