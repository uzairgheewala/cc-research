"""Building blocks for Atlas v2 pages. Pages are plain Python modules that set BODY (an HTML string).

Numbers come only through common.n / common.t (site/registry.py). Terms come through T(), which the build checks against
site/terms.py. CURRENT holds the slug of the page being rendered (set by site/build.py).
"""
import html as _html

from common import COND, MONO, SANS, PILLAR, STATUS, n, t, v, tag  # noqa: F401  (re-exported for pages)
from terms import TERMS

CURRENT = [""]
INK, MUTED, LINE, PAPER = "#17201B", "#4E5751", "#C9CEC6", "#FFFFFF"


def esc(x):
    return _html.escape(str(x), quote=True)


def _inline(name):
    """'Tier, partial order' -> 'tier'; 'Declared knowledge (K)' -> 'declared knowledge'; acronyms and CamelCase kept."""
    base = name.split(",")[0].split(" (")[0]
    first = base.split(" ")[0]
    return base[0].lower() + base[1:] if first[1:] == first[1:].lower() else base


def T(term_id, text=None):
    """A term: defined here if this is its introducing page, otherwise a link to the glossary."""
    name, definition, intro, _ = TERMS[term_id]
    label = text or _inline(name)
    if intro == CURRENT[0]:
        return f'<dfn class="term" id="t-{term_id}" data-term="{term_id}" title="{esc(definition)}">{label}</dfn>'
    return f'<a class="term" data-term="{term_id}" href="glossary.html#{term_id}" title="{esc(definition)}">{label}</a>'


def P(text, size=16):
    return f'<p class="prose" style="margin: 0; font-size: {size}px; line-height: {int(size * 1.62)}px; color: #23302A">{text}</p>'


def H2(text, anchor=None):
    a = f' id="{anchor}"' if anchor else ""
    return f'<h2{a} style="margin: 8px 0 0; font-family: {COND}; font-size: 28px; line-height: 34px">{text}</h2>'


def H3(text):
    return f'<h3 style="margin: 0; font-family: {COND}; font-size: 21px; line-height: 27px">{text}</h3>'


def section(*parts, gap=14):
    return f'<section style="display: flex; flex-direction: column; gap: {gap}px">{"".join(parts)}</section>'


def ul(items, size=16):
    lis = "".join(f'<li style="margin: 0 0 6px">{x}</li>' for x in items)
    return f'<ul class="prose" style="margin: 0; padding-left: 22px; font-size: {size}px; line-height: {int(size * 1.6)}px">{lis}</ul>'


def box(inner, tone="plain", flex=None):
    bg, bd = {"plain": (PAPER, LINE), "blue": ("#E6EEF6", "#1D5C99"), "orange": ("#FBEFE4", "#B85A12"),
              "purple": ("#EFEAF6", "#5B3E8E"), "red": ("#F6E7E7", "#8E2A2A"), "dark": ("#17201B", "#17201B")}[tone]
    fg = "#F2F3EF" if tone == "dark" else INK
    fl = f"flex: {flex}; min-width: 0; " if flex else ""
    return (f'<div style="{fl}padding: 18px 20px; background: {bg}; color: {fg}; border: 1.5px solid {bd}; border-radius: 12px; '
            f'display: flex; flex-direction: column; gap: 10px; font-size: 15px; line-height: 23px">{inner}</div>')


def grid(cells, min_w=300):
    return (f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min({min_w}px, 100%), 1fr)); gap: 14px; '
            f'align-items: stretch">{"".join(cells)}</div>')


def table(headers, rows, mono_cols=(), caption=None):
    th = "".join(f'<th style="padding: 8px 10px; text-align: left; font-weight: 600; color: {MUTED}; border-bottom: 1.5px solid {LINE}">{h}</th>'
                 for h in headers)
    trs = []
    for r in rows:
        tds = "".join(f'<td style="padding: 8px 10px; vertical-align: top; border-bottom: 1px solid #E3E6E0{"; font-family: " + MONO if i in mono_cols else ""}">{c}</td>'
                      for i, c in enumerate(r))
        trs.append(f"<tr>{tds}</tr>")
    cap = f'<p style="margin: 8px 0 0; font-size: 13px; line-height: 19px; color: {MUTED}">{caption}</p>' if caption else ""
    return (f'<div style="overflow-x: auto; background: {PAPER}; border: 1px solid {LINE}; border-radius: 12px; padding: 6px 8px">'
            f'<table style="border-collapse: collapse; width: 100%; font-size: 14px; line-height: 20px"><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>{cap}')


def figure(inner, caption):
    return (f'<figure style="margin: 0; display: flex; flex-direction: column; gap: 8px">'
            f'<div style="overflow-x: auto; background: {PAPER}; border: 1px solid {LINE}; border-radius: 12px; padding: 10px">{inner}</div>'
            f'<figcaption class="prose" style="font-size: 14px; line-height: 21px; color: #2C3631">{caption}</figcaption></figure>')


def question(q, before=None):
    """The page's opening: its question, and (optionally) the one thing it needs from earlier pages."""
    need = (f'<p style="margin: 6px 0 0; font-size: 14px; line-height: 20px; color: {MUTED}">Builds on: {before}</p>'
            if before else "")
    return (f'<div style="padding: 14px 18px; background: {PAPER}; border-left: 4px solid #1D5C99; border-radius: 6px">'
            f'<span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: #1D5C99">'
            f'The question</span><p style="margin: 4px 0 0; font-family: {COND}; font-size: 22px; line-height: 28px">{q}</p>{need}</div>')


def answer(text, next_q=None):
    nq = (f'<p style="margin: 10px 0 0; color: #C7CFC9"><b style="color: #F2F3EF">Which raises the next question:</b> {next_q}</p>'
          if next_q else "")
    return (f'<div style="padding: 18px 20px; background: #17201B; color: #F2F3EF; border-radius: 12px; font-size: 16px; '
            f'line-height: 25px"><span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; '
            f'color: #9CC7F0">The answer</span><p style="margin: 6px 0 0">{text}</p>{nq}</div>')


LABEL_COLOURS = {"primary": "#1D5C99", "second-hand": "#6A716B", "vendor claim": "#8E2A2A", "analyst claim": "#7A4BA8",
                 "survey": "#9A4A0E", "estimate": "#17201B", "anecdote": "#6A716B", "project measurement": "#1D5C99"}


def label(kind):
    """An evidence label for market figures (the market page's build check requires one next to every $ figure)."""
    base = kind.split(",")[0].split(" (")[0].strip()
    col = LABEL_COLOURS.get(base, "#6A716B")
    return (f'<span class="evlabel" style="display: inline-block; margin-left: 4px; padding: 0 7px; border: 1px solid {col}; '
            f'border-radius: 9px; font-size: 11px; line-height: 17px; font-weight: 600; color: {col}; white-space: nowrap">{kind}</span>')


def link(slug, text):
    return f'<a href="{"index" if slug == "index" else slug}.html">{text}</a>'


_DELEVEL = [("Level 1", "the space of problems (page 3)"), ("Level 2", "the scoring page (page 2)"),
            ("Level 3", "the theses page"), ("Level 4", "the status page"), ("Level 5", "page 6"),
            ("Main.dc.html", "space.html"), ("Bounds.dc.html", "scoring.html"), ("Theses.dc.html", "theses.html"),
            ("Bundles.dc.html", "status.html"), ("Stages.dc.html", "names.html"),
            ("Zoom: the next bundle", "The next bundle"),
            ("Zoom into one Causal-Copilot run, stage by stage", "One Causal-Copilot run, stage by stage (page 6)")]


def delevel(h):
    """Reuse a section of the old single-page levels with its cross-references pointed at the new pages."""
    for a, b in _DELEVEL:
        h = h.replace(a, b)
    return h
