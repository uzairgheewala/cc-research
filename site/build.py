"""Build the Causal Atlas: one page, five zoom levels, every number from site/snapshot.json.

  python site/build.py                          -> site/_build/index.html (+ snapshot.json beside it)
  python site/build.py --evidence-base URL      prefix for evidence links (default: the GitHub blob URL of this commit
                                                when GITHUB_REPOSITORY and GITHUB_SHA are set, else a path relative to the page)
Fails if the snapshot is missing a number a level prints, or if a level still links to a canvas file name.
"""
import argparse, html, json, os, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE / "levels"))
import common  # noqa: E402

LEVELS = [("space", "1 Space", "main"), ("bounds", "2 Bounds", "bounds"), ("theses", "3 Theses", "theses"),
          ("bundles", "4 Bundles", "bundles"), ("stages", "5 Stages", "stages")]
CANVAS = {"Main.dc.html": "space", "Bounds.dc.html": "bounds", "Theses.dc.html": "theses",
          "Bundles.dc.html": "bundles", "Stages.dc.html": "stages"}

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#F2F3EF;color:#17201B;font-family:'IBM Plex Sans','Helvetica Neue',sans-serif;font-size:15px;line-height:22px}
a{color:#1D5C99}a:hover{color:#123E69}
a.ev{color:inherit;text-decoration:underline dotted #1D5C99;text-underline-offset:3px}
a.ev:hover{color:#1D5C99}
header.top{position:sticky;top:0;z-index:10;display:flex;flex-wrap:wrap;align-items:center;gap:10px 28px;padding:12px 24px;border-bottom:1px solid #C9CEC6;background:#FFFFFF}
header.top .brand{font-family:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;font-size:24px;line-height:30px;font-weight:700}
header.top nav{display:flex;flex-wrap:wrap;gap:4px;font-size:14px}
header.top nav a{padding:10px 14px;border-radius:22px;color:#17201B;text-decoration:none}
header.top nav a[aria-current=page]{background:#17201B;color:#FFFFFF}
header.top .meta{margin-left:auto;font-size:13px;line-height:18px;color:#4E5751}
header.top .zoom{display:flex;gap:4px}
header.top .zoom button{width:40px;height:40px;border-radius:20px;border:1px solid #C9CEC6;background:#FFFFFF;font-size:18px;cursor:pointer}
main.levels{padding:32px 24px 40px}
section.level{max-width:1360px;margin:0 auto;display:flex;flex-direction:column;gap:24px}
.js section.level{display:none}
.js section.level.active{display:flex;animation:zin .28s ease-out}
.js section.level.active.out{animation:zout .28s ease-out}
@keyframes zin{from{opacity:0;transform:scale(.97)}to{opacity:1;transform:none}}
@keyframes zout{from{opacity:0;transform:scale(1.03)}to{opacity:1;transform:none}}
footer.about{max-width:1360px;margin:0 auto 48px;padding:0 24px;font-size:13px;line-height:19px;color:#4E5751}
footer.about code{font-family:'IBM Plex Mono',monospace;font-size:12px}
@media (prefers-reduced-motion: reduce){.js section.level.active{animation:none}}
@media (max-width: 640px){main.levels{padding:20px 16px 32px} header.top{padding:10px 16px} header.top .meta{margin-left:0}}
"""

JS = """
(function(){
  document.documentElement.classList.add('js');
  var ids=%s, cur=null;
  function show(id, dir){
    if(ids.indexOf(id)<0) id=ids[0];
    ids.forEach(function(x){
      var s=document.getElementById(x); s.classList.remove('active','out');
      var a=document.querySelector('nav a[href="#'+x+'"]'); if(a){a.removeAttribute('aria-current');}
    });
    var s=document.getElementById(id); s.classList.add('active'); if(dir<0) s.classList.add('out');
    var a=document.querySelector('nav a[href="#'+id+'"]'); if(a) a.setAttribute('aria-current','page');
    cur=id; window.scrollTo(0,0);
  }
  function step(d){ var i=ids.indexOf(cur)+d; if(i>=0&&i<ids.length) location.hash=ids[i]; }
  window.addEventListener('hashchange',function(){ var id=location.hash.slice(1); show(id, ids.indexOf(id)<ids.indexOf(cur)?-1:1); });
  document.addEventListener('keydown',function(e){
    if(e.target.closest('input,textarea')) return;
    if(e.key==='+'||e.key==='='||e.key==='ArrowRight'&&e.altKey) step(1);
    if(e.key==='-'||e.key==='ArrowLeft'&&e.altKey) step(-1);
  });
  document.getElementById('zin').onclick=function(){step(1)};
  document.getElementById('zout').onclick=function(){step(-1)};
  show(location.hash.slice(1)||ids[0],1);
})();
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default=str(HERE / "snapshot.json"))
    ap.add_argument("--out", default=str(HERE / "_build"))
    ap.add_argument("--evidence-base", default=None)
    a = ap.parse_args()
    snap = json.load(open(a.snapshot, encoding="utf-8"))
    repo, sha = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_SHA")
    base = a.evidence_base or ("https://github.com/%s/blob/%s/" % (repo, sha) if repo and sha else "../../")
    common.SNAP.update(snap)
    common.EVBASE[0] = base

    sections, missing = [], []
    for sid, label, mod in LEVELS:
        try:
            m = __import__(mod)
        except KeyError as e:
            missing.append("%s: registry key %s not in snapshot" % (mod, e))
            continue
        body = m.BODY
        for canvas, target in CANVAS.items():
            body = body.replace('href="%s"' % canvas, 'href="#%s"' % target)
        left = re.findall(r'href="[A-Za-z]+\.dc\.html"', body)
        if left:
            missing.append("%s: unmapped canvas links %s" % (mod, left[:3]))
        sections.append('<section class="level" id="%s" aria-label="%s" data-zoom="%s">\n%s\n</section>' % (
            sid, html.escape(label), html.escape(m.ZOOM), body))
    if missing:
        for x in missing:
            print("BUILD ERROR " + x)
        sys.exit(1)

    unused = sorted(set(snap["metrics"]) - common.USED)
    lists = snap["lists"]
    sync = " · ".join("%s list %s" % (k, "in sync" if v["pending_updates"] == 0 and v["pending_removals"] == 0
                                      else "%d updates pending" % (v["pending_updates"] + v["pending_removals"]))
                      for k, v in sorted(lists.items()))
    nav = "".join('<a href="#%s">%s</a>' % (sid, label) for sid, label, _ in LEVELS)
    gen = snap["generated_utc"][:10]
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Causal Atlas</title>
<script>document.documentElement.classList.add("js")</script>
<meta name="description" content="Where causal discovery stands, where its limits are, and how this project is closing the distance. Built from tracker snapshot {snap['hash'][:12]}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<header class="top">
<span class="brand">Causal Atlas</span>
<nav aria-label="Zoom level">{nav}</nav>
<span class="zoom"><button id="zout" type="button" aria-label="Zoom out">−</button><button id="zin" type="button" aria-label="Zoom in">+</button></span>
<span class="meta">snapshot <code>{snap['hash'][:12]}</code> · {gen}<br>{sync}</span>
</header>
<main class="levels">
{chr(10).join(sections)}
</main>
<footer class="about">
<p><b>How this page is made.</b> Every number is read from <code>site/snapshot.json</code>, which <code>tracker/snapshot.py</code> builds from the tracker
(<code>tracker/status.json</code>, verified {snap['status_verified_utc']}), the Q1 plan and the result files it names; a dotted number links to its file.
The same snapshot feeds both Slack lists and the digests. CI rebuilds the snapshot from the committed files and fails if it differs
(<code>python tracker/snapshot.py --check</code>). {len(snap['metrics'])} numbers from {len(snap['sources'])} files; {len(snap['items'])} tracker items; {len(snap['bundles'])} bundles.</p>
</footer>
<script>{JS % json.dumps([s for s, _, _ in LEVELS])}</script>
</body>
</html>
"""
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(doc, encoding="utf-8", newline="\n")
    shutil.copyfile(a.snapshot, out / "snapshot.json")
    (out / ".nojekyll").write_text("")
    print("built %s (%d KB): %d levels, %d numbers used, %d registry numbers not printed%s" % (
        out / "index.html", len(doc) // 1024, len(sections), len(common.USED), len(unused),
        "" if not unused else " (" + ", ".join(unused[:8]) + ("…" if len(unused) > 8 else "") + ")"))


if __name__ == "__main__":
    main()
