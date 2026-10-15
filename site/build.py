"""Build the Causal Atlas (v2): a guided sequence of pages, every number from site/snapshot.json.

  python site/build.py                        -> site/_build/*.html (+ snapshot.json, build_report.json)
  python site/build.py --evidence-base URL    prefix for evidence links (default: GitHub blob URL of this commit when
                                              GITHUB_REPOSITORY and GITHUB_SHA are set, else a path relative to the page)
  python site/build.py --mark-reviewed SLUG [SLUG ...] | all
                                              record that a page's prose was re-read against the current snapshot
Design: analysis/reports/site_flow_design.md (approved 2026-10-13, DEC-06). Pages: site/pages.py; terms: site/terms.py.

Fails (exit 1) on: a number missing from the snapshot; a term used before the page that teaches it; a term whose
introducing page does not define it; a number printed before the page allowed to show it; a broken local link or
glossary anchor; an unlabelled $ figure on the market page; leftovers of the single-page site ("Level N", .dc.html).
Warns on: pages over the size budget; pages to re-read (their tickets changed since review).
"""
import argparse, html, importlib, json, os, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(HERE / "levels"), str(HERE), str(HERE / "pgs")]
import common  # noqa: E402
import pagekit  # noqa: E402
from pages import PAGES, ACTS, SEQUENCE, SCAN_EXEMPT, REDIRECTS  # noqa: E402
from terms import TERMS  # noqa: E402

REVIEWED = HERE / "reviewed.json"
WORD_BUDGET = 1800
# registry key prefix -> first page allowed to print it (a result may not appear before its question)
FIRST_PAGE = {"leak.": "scoreboard", "ab01.": "scoreboard", "ab02.": "scoreboard", "ab03.": "scoreboard", "bnd06.": "scoreboard",
              "ab04.": "decisions", "ab09.": "decisions", "cc.": "names", "ab07.": "names", "ab05.": "names",
              "ab12.": "rca", "ab14.": "market", "ab06.": "names"}

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#F2F3EF;color:#17201B;font-family:'IBM Plex Sans','Helvetica Neue',sans-serif;font-size:16px;line-height:25px}
a{color:#1D5C99}a:hover{color:#123E69}
a.ev{color:inherit;text-decoration:none;border-bottom:1px dotted #8FA9C4}
a.ev:hover,a.ev:focus{color:#1D5C99;border-bottom-color:#1D5C99}
a.term{color:inherit;text-decoration:none;border-bottom:1px dashed #6A716B}
a.term:hover,a.term:focus{color:#1D5C99}
dfn.term{font-style:normal;font-weight:600;background:#FFF4D6;padding:0 3px;border-radius:3px}
.prose{max-width:76ch}
header.top{position:sticky;top:0;z-index:10;background:#FFFFFF;border-bottom:1px solid #C9CEC6}
header.top .bar{max-width:1360px;margin:0 auto;display:flex;align-items:center;gap:16px 28px;padding:10px 24px;flex-wrap:wrap}
header.top .brand{font-family:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;font-size:22px;line-height:28px;font-weight:700;color:#17201B;text-decoration:none}
nav.steps{display:flex;gap:6px 18px;flex-wrap:wrap;font-size:13px;line-height:18px}
nav.steps .act{display:flex;align-items:center;gap:6px}
nav.steps .actlabel{font-weight:600;color:#4E5751;letter-spacing:.4px}
nav.steps a{display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:30px;padding:0 8px;border-radius:15px;border:1px solid #C9CEC6;color:#17201B;text-decoration:none;font-weight:600}
nav.steps a:hover{border-color:#1D5C99;color:#1D5C99}
nav.steps a[aria-current=page]{background:#17201B;border-color:#17201B;color:#FFFFFF}
nav.steps a.ref{border-style:dashed;font-weight:500}
details.toc{display:none}
header.top .meta{margin-left:auto;font-size:12px;line-height:16px;color:#4E5751;text-align:right}
main{padding:28px 24px 40px}
.page{max-width:1240px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
.kicker{font-size:13px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;color:#4E5751}
h1.title{margin:2px 0 0;font-family:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;font-size:42px;line-height:48px}
nav.pn{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:14px;margin-top:10px}
nav.pn a{display:flex;flex-direction:column;gap:2px;padding:14px 18px;background:#FFFFFF;border:1px solid #C9CEC6;border-radius:12px;text-decoration:none;color:#17201B}
nav.pn a:hover{border-color:#1D5C99}
nav.pn .dir{font-size:12px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:#4E5751}
nav.pn .next{text-align:right}
footer.about{max-width:1240px;margin:0 auto 40px;padding:0 24px;font-size:13px;line-height:19px;color:#4E5751}
footer.about code{font-family:'IBM Plex Mono',monospace;font-size:12px}
@media (max-width: 900px){nav.steps{display:none} details.toc{display:block;font-size:14px} details.toc summary{cursor:pointer;font-weight:600}
 details.toc ol{margin:8px 0 0;padding-left:20px} header.top .meta{display:none}}
@media (max-width: 640px){main{padding:18px 16px 32px} header.top{position:static} header.top .bar{padding:10px 16px} h1.title{font-size:32px;line-height:38px}
 .page [style*="grid-template-columns: repeat(auto-fit"]{grid-template-columns:1fr !important}
 .page [style*="flex: 1 1"]{flex-basis:100% !important;min-width:0 !important}
 .page > *{max-width:100%;min-width:0;overflow-x:auto}
 .page figure{max-width:100%;overflow-x:auto}
 .page table{display:block;max-width:100%;overflow-x:auto}}
"""

REDIRECT_JS = """<script>(function(){var m=%s;var h=location.hash.slice(1);if(m[h]){location.replace(m[h]);}})();</script>"""


def href(slug):
    return "%s.html" % slug


def visible_text(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(h))


def header(cur):
    groups = []
    for act, name in ACTS:
        links = "".join('<a href="%s"%s title="%s">%d</a>' % (href(p["slug"]), ' aria-current="page"' if p["slug"] == cur else "",
                                                              html.escape(p["title"]), p["n"])
                        for p in PAGES if p["act"] == act)
        groups.append('<div class="act"><span class="actlabel">%s · %s</span>%s</div>' % (act, name, links))
    ref = "".join('<a class="ref" href="%s"%s>%s</a>' % (href(p["slug"]), ' aria-current="page"' if p["slug"] == cur else "", p["short"])
                  for p in PAGES if p["act"] == "R")
    groups.append('<div class="act"><span class="actlabel">Reference</span>%s</div>' % ref)
    toc = "".join('<li>%s</li>' % ('<b>%s</b>' % html.escape(p["title"]) if p["slug"] == cur else
                                   '<a href="%s">%s</a>' % (href(p["slug"]), html.escape(p["title"]))) for p in PAGES)
    curp = next(p for p in PAGES if p["slug"] == cur)
    where = ("Act %s · page %d of %d" % (curp["act"], curp["n"], len(SEQUENCE) - 1)) if curp["act"] in ("I", "II", "III", "IV") else curp["short"]
    return ('<header class="top"><div class="bar"><a class="brand" href="index.html">Causal Atlas</a>'
            '<nav class="steps" aria-label="Pages">%s</nav>'
            '<details class="toc"><summary>%s</summary><ol>%s</ol></details>'
            '<span class="meta">updated %s · snapshot <code>%s</code><br>day-to-day work lives in the Slack lists</span></div></header>'
            % ("".join(groups), html.escape(where), toc, common.SNAP["generated_utc"][:10], common.SNAP["hash"][:12]))


def prevnext(cur):
    if cur not in SEQUENCE:
        return '<nav class="pn"><a href="index.html"><span class="dir">Back to</span><span>Home</span></a></nav>'
    i = SEQUENCE.index(cur)
    by = {p["slug"]: p for p in PAGES}
    out = []
    if i > 0:
        p = by[SEQUENCE[i - 1]]
        out.append('<a href="%s"><span class="dir">← Previous</span><span>%s</span></a>' % (href(p["slug"]), html.escape(p["title"])))
    if i + 1 < len(SEQUENCE):
        p = by[SEQUENCE[i + 1]]
        out.append('<a class="next" href="%s"><span class="dir">Next →</span><span>%s</span></a>' % (href(p["slug"]), html.escape(p["title"])))
    return '<nav class="pn">%s</nav>' % "".join(out)


def reread():
    """Pages whose tickets changed status since the page was last reviewed."""
    rev = json.load(open(REVIEWED, encoding="utf-8")) if REVIEWED.exists() else {}
    st = {i["id"]: i["status"] for i in common.SNAP["items"]}
    out = []
    for p in PAGES:
        seen = rev.get(p["slug"])
        if seen is None:
            if p["tickets"]:
                out.append({"page": p["slug"], "why": "never reviewed"})
            continue
        ch = ["%s: %s -> %s" % (t, seen.get(t), st.get(t)) for t in p["tickets"] if seen.get(t) != st.get(t)]
        if ch:
            out.append({"page": p["slug"], "why": "; ".join(ch)})
    return out


def mark_reviewed(slugs):
    rev = json.load(open(REVIEWED, encoding="utf-8")) if REVIEWED.exists() else {}
    st = {i["id"]: i["status"] for i in common.SNAP["items"]}
    for p in PAGES:
        if "all" in slugs or p["slug"] in slugs:
            rev[p["slug"]] = {t: st.get(t) for t in p["tickets"]}
    json.dump(rev, open(REVIEWED, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("marked reviewed:", ", ".join(sorted(rev)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default=str(HERE / "snapshot.json"))
    ap.add_argument("--out", default=str(HERE / "_build"))
    ap.add_argument("--evidence-base", default=None)
    ap.add_argument("--mark-reviewed", nargs="+", default=None)
    a = ap.parse_args()
    snap = json.load(open(a.snapshot, encoding="utf-8"))
    repo, sha = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_SHA")
    common.SNAP.update(snap)
    common.EVBASE[0] = a.evidence_base or ("https://github.com/%s/blob/%s/" % (repo, sha) if repo and sha else "../../")
    if a.mark_reviewed:
        mark_reviewed(a.mark_reviewed)
        return
    pagekit.REREAD = reread()
    pagekit.PRINTED = set()

    order = {p["slug"]: i for i, p in enumerate(PAGES)}
    errors, warnings, rendered, report = [], [], {}, {"pages": {}}
    for p in PAGES:
        pagekit.CURRENT[0] = p["slug"]
        try:
            mod = importlib.import_module(p["module"])
        except KeyError as e:
            errors.append("%s: registry key %s not in snapshot" % (p["slug"], e))
            continue
        body = mod.BODY
        kicker = ("Act %s · %s" % (p["act"], dict(ACTS)[p["act"]])) if p["act"] in dict(ACTS) else ("Reference" if p["act"] == "R" else "Start here")
        page_html = ('<div class="page"><div><div class="kicker">%s</div><h1 class="title">%s</h1></div>\n%s\n%s</div>'
                     % (kicker, html.escape(p["title"]), body, prevnext(p["slug"])))
        rendered[p["slug"]] = page_html
        # ---- checks on this page
        txt = visible_text(body)
        words = len(txt.split())
        used_terms = set(re.findall(r'data-term="([^"]+)"', body))
        nums = set(re.findall(r'class="ev"[^>]*title="([^" ]+) ·', body))
        report["pages"][p["slug"]] = {"words": words, "terms": sorted(used_terms), "numbers": sorted(nums)}
        pagekit.PRINTED |= nums
        if words > WORD_BUDGET:
            warnings.append("%s: %d words (budget %d)" % (p["slug"], words, WORD_BUDGET))
        if p["slug"] not in SCAN_EXEMPT:
            for tid in used_terms:
                if tid not in TERMS:
                    errors.append("%s: unknown term %s" % (p["slug"], tid))
                elif order[TERMS[tid][2]] > order[p["slug"]]:
                    errors.append("%s: term '%s' is taught later, on %s" % (p["slug"], tid, TERMS[tid][2]))
            for tid, (name, _d, intro, forms) in TERMS.items():
                if order[intro] > order[p["slug"]]:
                    for f in forms:
                        mm = re.search(r"(?i)" + f, txt)
                        if mm:
                            ctx = txt[max(0, mm.start() - 40): mm.end() + 40]
                            errors.append("%s: uses '%s' (term %s, taught on %s): ...%s..." % (p["slug"], mm.group(0), tid, intro, ctx))
                            break
        for key in nums:
            for pre, first in FIRST_PAGE.items():
                if key.startswith(pre) and order[first] > order[p["slug"]] and p["slug"] not in SCAN_EXEMPT:
                    errors.append("%s: number %s belongs to %s or later" % (p["slug"], key, first))
        if p["slug"] == "market":
            for blk in re.findall(r"<(td|li|p)\b[^>]*>(.*?)</\1>", body, flags=re.S):
                inner = blk[1]
                if re.search(r"\$\s?\d", visible_text(inner)) and "evlabel" not in inner:
                    errors.append("market: unlabelled $ figure: %s" % visible_text(inner)[:90])
        for bad in (r"Level [1-5]\b", r"\.dc\.html", r"Zoom (in|out)"):
            if re.search(bad, body):
                errors.append("%s: leftover from the single-page site: %s" % (p["slug"], bad))
    # every term is defined on its introducing page
    for tid, (_n, _d, intro, _f) in TERMS.items():
        if intro in rendered and ('data-term="%s"' % tid) not in rendered[intro]:
            errors.append("term %s is assigned to %s but that page does not teach it" % (tid, intro))
    # links
    names = {href(p["slug"]) for p in PAGES}
    for slug, h in rendered.items():
        for target in re.findall(r'href="([^"#:]+\.html)(?:#[^"]*)?"', h):
            if target not in names:
                errors.append("%s: broken link %s" % (slug, target))
        for t in re.findall(r'href="glossary\.html#([^"]+)"', h):
            if t not in TERMS:
                errors.append("%s: glossary anchor %s missing" % (slug, t))
    if any(k not in common.SNAP["metrics"] for k in common.USED):
        errors.append("numbers not in snapshot: %s" % sorted(k for k in common.USED if k not in common.SNAP["metrics"]))

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    keep = {href(p["slug"]) for p in PAGES}
    for f in out.glob("*.html"):          # pages that no longer exist (pages are overwritten, never deleted first)
        if f.name not in keep:
            try:
                f.unlink()
            except OSError as e:
                warnings.append("could not remove stale %s: %s" % (f.name, e))
    for p in PAGES:
        if p["slug"] not in rendered:
            continue
        extra = REDIRECT_JS % json.dumps(REDIRECTS) if p["slug"] == "index" else ""
        doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p["title"] if p["slug"] != "index" else "Causal Atlas")}{"" if p["slug"] == "index" else " · Causal Atlas"}</title>
<meta name="description" content="{html.escape(p["question"])}">
{extra}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
{header(p["slug"])}
<main>
{rendered[p["slug"]]}
</main>
<footer class="about"><p>Every number links to the file it comes from; the site is rebuilt from <code>site/snapshot.json</code>, which the
tracker writes from the committed result files. <a href="about.html">How this site is built</a> · <a href="glossary.html">Glossary</a> ·
<a href="evidence.html">Evidence index</a></p></footer>
</body>
</html>
"""
        (out / href(p["slug"])).write_text(doc, encoding="utf-8", newline="\n")
    shutil.copyfile(a.snapshot, out / "snapshot.json")
    (out / ".nojekyll").write_text("")
    report.update({"errors": errors, "warnings": warnings, "reread": pagekit.REREAD,
                   "numbers_used": len(common.USED), "unused": sorted(set(snap["metrics"]) - common.USED)})
    json.dump(report, open(out / "build_report.json", "w", encoding="utf-8"), indent=1)
    for w in warnings:
        print("WARN  " + w)
    for r in pagekit.REREAD:
        print("REREAD %s (%s)" % (r["page"], r["why"]))
    for e in errors:
        print("ERROR " + e)
    print("built %d pages in %s; %d numbers used, %d registry numbers not printed; %d errors, %d warnings, %d pages to re-read"
          % (len(rendered), out, len(common.USED), len(report["unused"]), len(errors), len(warnings), len(pagekit.REREAD)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
