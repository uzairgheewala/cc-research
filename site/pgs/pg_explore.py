"""Explore (s27, TEAM-11): the research so far, four ways. Everything renders as plain tables, so the page works with
JavaScript off; a small script adds search and filters. The same data is written as explore.json (export through an
allowlist: no private path, no note text; site/build.py checks). Design: claude/site-v3-design-2026-10-20.md section 6."""
import hashlib
import json
import re

from pagekit import *  # noqa: F401,F403
import common
import gapkit as G

SNAP = common.SNAP
LEVER_STATUS = ["USED", "TRIED", "PARTLY", "BARRED", "UNMEASURED", "N/A"]
LEVER_PLAIN = {"USED": "in use", "TRIED": "tried, did not pass", "PARTLY": "partly measured", "BARRED": "excluded by design",
               "UNMEASURED": "not measured yet", "N/A": "does not apply here"}
ITEM_FIELDS = ("id", "title", "status", "category", "pillar", "kind", "level")   # the export allowlist for tracker items


def lever_status(cell):
    m = re.match(r"(USED|TRIED|PARTLY|BARRED|UNMEASURED|N/A)", cell or "")
    return m.group(1) if m else "UNMEASURED"


def levers():
    out = []
    for kind, key in (("link", "lev.links"), ("direction", "lev.dirs")):
        for r in G.val(key):
            rid = r.get("#", "")
            src = r.get("Source of evidence") or r.get("Source") or ""
            verdict = r.get("Verdict / what is wrong") or r.get("Verdict") or ""
            out.append({"id": rid, "kind": kind, "source": src, "status": lever_status(r.get("Status")),
                        "status_text": r.get("Status", ""), "verdict": verdict, "key": key})
    return out


LEV = levers()
applicable = [x for x in LEV if x["status"] != "N/A"]
ruled = [x for x in applicable if x["status"] in ("USED", "TRIED", "BARRED")]


def lm_history():
    rows = []
    for lid, lm in G.LM.items():
        if lm.get("history"):
            for h in lm["history"]:
                rows.append({"landmark": lid, "plain": lm["plain"], "family": h["family"], "read": h["read"],
                             "value_key": h["value"], "cons_key": h["cons"], "historic": h["value"].startswith(tuple(_superseded()))})
        else:
            d = G.derive(lid)
            for p in d["parts"]:
                if p["x"] is not None:
                    rows.append({"landmark": lid, "plain": lm["plain"], "family": p["label"], "read": "binding read",
                                 "value_key": p["value"], "cons_key": p.get("cons"), "historic": False})
    return rows


def _superseded():
    import registry
    return list(getattr(registry, "SUPERSEDED", {}))


HIST = lm_history()


def hist_table():
    rows = []
    for r in HIST:
        spec = G.LM[r["landmark"]].get("fmt", "{:.3f}")
        spec = None if spec == "{:,}" else spec
        v = common.n(r["value_key"], spec, historic=r["historic"])
        c = common.n(r["cons_key"], spec, historic=r["historic"]) if r["cons_key"] else "–"
        rows.append([esc(r["plain"]), esc(r["family"]), esc(r["read"]), v, c, G.chip(G.derive(r["landmark"])["type"])])
    return table(["Landmark", "Part", "Read", "Result", "Cautious end", "Now"], rows,
                 caption="Older reads are kept as history; the newest read of a frozen version is the one a landmark uses.")


def gapmap_table():
    rows = []
    for gid, g in G.GAPS.items():
        sh = G.shares(gid)
        rows.append([esc(g["plain"]), esc(g["family"]), common.n(g["total"]), G.state_bar(gid),
                     "%d%%" % round(100 * sh["understood"]) + (" (pending)" if sh["pending"] else "")])
    return table(["Error class", "Family", "How many", "By state", "Cause known"], rows)


def lever_table():
    rows = []
    for x in LEV:
        rows.append(f'<tr data-status="{x["status"]}" data-kind="{x["kind"]}"><td style="padding: 6px 8px; font-family: {MONO}">'
                    f'{esc(x["id"])}</td><td style="padding: 6px 8px">{esc(x["kind"])}</td><td style="padding: 6px 8px">{esc(x["source"])}</td>'
                    f'<td style="padding: 6px 8px; white-space: nowrap">{esc(LEVER_PLAIN[x["status"]])}</td>'
                    f'<td style="padding: 6px 8px">{esc(x["verdict"])}</td></tr>')
    btns = "".join(f'<button type="button" class="fbtn" data-filter="{s}">{esc(LEVER_PLAIN[s])} '
                   f'({sum(1 for x in LEV if x["status"] == s)})</button>' for s in LEVER_STATUS)
    return (f'<div class="filters" data-for="levtab" style="display: flex; flex-wrap: wrap; gap: 6px">'
            f'<button type="button" class="fbtn on" data-filter="">all ({len(LEV)})</button>{btns}</div>'
            f'<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; padding: 6px 8px">'
            f'<table id="levtab" style="border-collapse: collapse; width: 100%; font-size: 14px; line-height: 20px"><thead><tr>'
            + "".join(f'<th style="padding: 6px 8px; text-align: left; color: #4E5751">{h}</th>' for h in ("#", "Kind", "Source of evidence", "Status", "What was found"))
            + f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<p style="margin: 0; font-size: 13px; color: #4E5751">From <a href="{common.EVBASE[0]}docs/design/q2_lever_map.md">the lever map</a>.</p>')


ITEMS = [{k: i.get(k) for k in ITEM_FIELDS} for i in SNAP["items"]]
STATUS_PLAIN = {"done": "done", "in_progress": "in progress", "todo": "to do", "open": "open", "blocked": "blocked",
                "reopened": "reopened"}


def items_table():
    cats = sorted({i["category"] for i in ITEMS}, key=lambda c: (int(c.split()[0]) if c.split()[0].isdigit() else 99, c))
    opts = "".join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in cats)
    sts = "".join(f'<option value="{s}">{esc(STATUS_PLAIN.get(s, s))}</option>' for s in sorted({i["status"] for i in ITEMS}))
    rows = "".join(f'<tr data-cat="{esc(i["category"])}" data-status="{esc(i["status"])}"><td style="padding: 6px 8px; font-family: {MONO}; '
                   f'white-space: nowrap">{esc(i["id"])}</td><td style="padding: 6px 8px">{esc(i["title"])}</td>'
                   f'<td style="padding: 6px 8px; white-space: nowrap">{esc(STATUS_PLAIN.get(i["status"], i["status"]))}</td>'
                   f'<td style="padding: 6px 8px">{esc(i["category"])}</td></tr>' for i in ITEMS)
    return (f'<div class="itemfilters" style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center">'
            f'<label>Search <input id="isearch" type="search" placeholder="for example: names, calibration" style="font: inherit; padding: 4px 8px"></label>'
            f'<label>Category <select id="icat" style="font: inherit"><option value="">all</option>{opts}</select></label>'
            f'<label>Status <select id="istatus" style="font: inherit"><option value="">all</option>{sts}</select></label>'
            f'<span id="icount" style="color: #4E5751"></span></div>'
            f'<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; padding: 6px 8px">'
            f'<table id="itab" style="border-collapse: collapse; width: 100%; font-size: 14px; line-height: 20px"><thead><tr>'
            + "".join(f'<th style="padding: 6px 8px; text-align: left; color: #4E5751">{h}</th>' for h in ("Ticket", "What", "Status", "Category"))
            + f'</tr></thead><tbody>{rows}</tbody></table></div>')


EXPORT = {
    "about": "Causal Atlas explorer data (site v3, s27). Every value is a registry key of the snapshot below; landmark types "
             "are derived by site/gapkit.py. Tracker items carry only these fields: " + ", ".join(ITEM_FIELDS) + ".",
    "snapshot": SNAP.get("hash"), "generated_utc": SNAP.get("generated_utc"),
    "landmarks": [{"id": lid, "plain": G.LM[lid]["plain"], "type": G.derive(lid)["type"],
                   "parts": [{"label": p["label"], "value_key": p.get("value"), "value": p["x"], "cautious_end": p["c"],
                              "bar": p["bar_v"], "type": p["type"]} for p in G.derive(lid)["parts"]]} for lid in G.LM],
    "history": [{k: r[k] for k in ("landmark", "family", "read", "value_key", "cons_key", "historic")} for r in HIST],
    "gaps": [{"id": gid, "family": g["family"], "total": G.val(g["total"]),
              "by_state": G.shares(gid)["by"], "pending": G.shares(gid)["pending"]} for gid, g in G.GAPS.items()],
    "levers": [{k: x[k] for k in ("id", "kind", "source", "status", "verdict")} for x in LEV],
    "lever_coverage": {"ruled": len(ruled), "applicable": len(applicable)},
    "items": ITEMS,
}
EXPORT_TEXT = json.dumps(EXPORT, indent=1, sort_keys=True, ensure_ascii=False, default=str)
EXPORT_SHA = hashlib.sha256(EXPORT_TEXT.encode("utf-8")).hexdigest()

SCRIPT = """<script>
(function(){
  document.querySelectorAll('.filters').forEach(function(f){
    var tab=document.getElementById(f.getAttribute('data-for'));
    f.querySelectorAll('.fbtn').forEach(function(b){
      b.addEventListener('click',function(){
        f.querySelectorAll('.fbtn').forEach(function(x){x.classList.remove('on')}); b.classList.add('on');
        var s=b.getAttribute('data-filter');
        tab.querySelectorAll('tbody tr').forEach(function(r){r.style.display=(!s||r.getAttribute('data-status')===s)?'':'none'});
      });
    });
  });
  var q=document.getElementById('isearch'),c=document.getElementById('icat'),st=document.getElementById('istatus'),n=document.getElementById('icount');
  function apply(){
    var t=(q.value||'').toLowerCase(),k=0;
    document.querySelectorAll('#itab tbody tr').forEach(function(r){
      var ok=(!t||r.textContent.toLowerCase().indexOf(t)>=0)&&(!c.value||r.getAttribute('data-cat')===c.value)&&(!st.value||r.getAttribute('data-status')===st.value);
      r.style.display=ok?'':'none'; if(ok)k++;
    });
    n.textContent=k+' shown';
  }
  [q,c,st].forEach(function(e){e.addEventListener('input',apply);e.addEventListener('change',apply)}); apply();
})();
</script>
<style>.fbtn{font:inherit;font-size:13px;padding:4px 10px;border:1px solid #C9CEC6;border-radius:14px;background:#FFFFFF;cursor:pointer}
.fbtn.on{background:#17201B;color:#FFFFFF;border-color:#17201B}</style>"""

BODY = "\n".join([
    question("What has the research measured so far, and how does it fit together?"),
    P("Four views of the same result files. Each works as a plain table; with JavaScript on, the last two can be filtered. The "
      f'data behind this page is also a file: <a href="explore.json">explore.json</a> (sha256 <code>{EXPORT_SHA[:12]}</code>).'),
    H2("1. Landmarks over time"),
    hist_table(),
    H2("2. The map of the remaining errors"),
    gapmap_table(),
    G.legend_states(),
    H2("3. Every lever we know of, and what happened to it"),
    P(f"Every source of evidence for a link or a direction, and its status. {len(ruled)} of {len(applicable)} applicable "
      f"levers are measured or ruled on; the rest are partly measured or not yet measured."),
    lever_table(),
    H2("4. Every tracked item"),
    items_table(),
    SCRIPT,
])
