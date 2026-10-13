"""Reference: the glossary, generated from site/terms.py, grouped by the page that teaches each term."""
from pagekit import *  # noqa: F401,F403
from pages import PAGES
from terms import TERMS

groups = []
for p in PAGES:
    ts = [(k, v_) for k, v_ in TERMS.items() if v_[2] == p["slug"]]
    if not ts:
        continue
    dl = "".join(f'<div id="{k}" style="display: flex; flex-direction: column; gap: 2px; scroll-margin-top: 90px">'
                 f'<dt style="font-weight: 600">{name}</dt><dd style="margin: 0; color: #2C3631">{esc(d)}</dd></div>'
                 for k, (name, d, _i, _f) in ts)
    head = H3('Taught on page %d: <a href="%s">%s</a>' % (p["n"], p["slug"] + ".html", esc(p["title"])))
    groups.append(box(f'{head}'
                      f'<dl style="margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); '
                      f'gap: 12px 24px; font-size: 15px; line-height: 22px">{dl}</dl>'))

BODY = "\n".join([question("What does a term mean, and where is it taught?"),
                  P("Every technical term on this site, in the order the pages teach it. Each page only uses terms taught on that "
                    "page or earlier; the build checks this."),
                  *groups])
