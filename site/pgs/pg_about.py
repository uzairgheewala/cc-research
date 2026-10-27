"""Reference: how this site is built, the rules the build enforces, and the pages whose prose needs re-reading."""
from pagekit import *  # noqa: F401,F403
import pagekit
import common

SNAP = common.SNAP
rr = getattr(pagekit, "REREAD", [])
rr_html = (ul([f'<a href="{r["page"]}.html">{r["page"]}</a>: {esc(r["why"])}' for r in rr], 15) if rr
           else P("None: every page's prose was last reviewed against the current state of its tickets.", 15))

BODY = "\n".join([
    question("How is this site made, and which pages need re-reading?"),
    P(f"The site is generated. <code>tracker/snapshot.py</code> reads the tracker ({len(SNAP['items'])} items, verified "
      f"{esc(SNAP['status_verified_utc'])}), both plans and every result file the pages quote, and writes "
      f"<code>site/snapshot.json</code>. <code>site/build.py</code> renders the pages from that one file, so the site, the two Slack "
      f"lists and the team digests always show the same state. Continuous integration recomputes the snapshot from the committed "
      f"files and refuses to publish if it differs."),
    H2("What the build checks"),
    ul(["Every number comes from the snapshot; a missing one stops the build.",
        "A term is used only on or after the page that teaches it (site/terms.py), and every term is taught where the glossary says.",
        "A result is printed only on or after the page that asks its question.",
        "Every link between pages and every glossary anchor resolves.",
        "Links into <a href=\"copilot/\">Inside Causal-Copilot</a> are checked by its own build (site/copilot/build.py), which runs next.",  # S29 (TEAM-13)
        "Every dollar figure on the market page carries an evidence label.",
        "Pages warn when they grow past about 1,800 words."]),
    H2("Pages to re-read"),
    P("Hand-written pages list the tickets their prose depends on. When one of those tickets changes status, the page is listed "
      "here until someone re-reads it and records the review (<code>python site/build.py --mark-reviewed PAGE</code>).", 15),
    rr_html,
    P(f"Snapshot <code>{SNAP['hash'][:12]}</code>, generated {esc(SNAP['generated_utc'])}. Design: "
      f"<code>analysis/reports/site_flow_design.md</code>.", 14),
])
