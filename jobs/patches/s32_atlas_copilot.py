"""s32 (S29, TEAM-13): link the Atlas to Inside Causal-Copilot from every page's header (Reference group and the phone
menu), from the names page (the replay of the three name arms) and from the about page.

Run once from cc-research, after sheet A's return is packed (site/build.py, site/pgs/pg_names.py and site/pgs/pg_about.py
are in jobs/waves/A/identity.sha256):  py -3 jobs\\patches\\s32_atlas_copilot.py
then: python site/build.py && python site/copilot/build.py   (the second build checks every Atlas link into copilot/).
Links use "copilot/" or "copilot/<page>.html". The Atlas build runs first and cannot see those pages, so its link check
skips copilot/ targets and site/copilot/build.py checks every one of them (inbound_ok): nothing goes unchecked."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARK = "S29 (TEAM-13)"
EDITS = {
    "site/build.py": [
        ("""    groups.append('<div class="act"><span class="actlabel">Reference</span>%s</div>' % ref)\n""",
         """    ref += '<a class="ref" href="copilot/" title="How Causal-Copilot works, read from its code">Inside Causal-Copilot</a>'  # S29 (TEAM-13)\n"""
         """    groups.append('<div class="act"><span class="actlabel">Reference</span>%s</div>' % ref)\n"""),
        ("""                                   '<a href="%s">%s</a>' % (href(p["slug"]), html.escape(p["title"]))) for p in PAGES)\n""",
         """                                   '<a href="%s">%s</a>' % (href(p["slug"]), html.escape(p["title"]))) for p in PAGES)\n"""
         """    toc += '<li><a href="copilot/">Inside Causal-Copilot</a></li>'  # S29 (TEAM-13)\n"""),
        ("""            if target not in names:\n""",
         """            if target not in names and not target.startswith("copilot/"):  # S29 (TEAM-13): checked by site/copilot/build.py\n"""),
    ],
    "site/pgs/pg_names.py": [
        ("""    answer(f"From the names, in every system that lets the model decide a connection.""",
         """    P('To see where the names enter Causal-Copilot\\'s code, and one scenario run with real, neutral and moved names side '\n"""
         """      'by side, open <a href="copilot/replay.html">the replay</a> in Inside Causal-Copilot.'),  # S29 (TEAM-13)\n"""
         """    answer(f"From the names, in every system that lets the model decide a connection."""),
    ],
    "site/pgs/pg_about.py": [
        ("""        "Every link between pages and every glossary anchor resolves.",\n""",
         """        "Every link between pages and every glossary anchor resolves.",\n"""
         """        "Links into <a href=\\"copilot/\\">Inside Causal-Copilot</a> are checked by its own build (site/copilot/build.py), which runs next.",  # S29 (TEAM-13)\n"""),
    ],
}
texts = {}
for rel, edits in EDITS.items():
    t = (ROOT / rel).read_bytes().decode("utf-8")
    assert MARK not in t, "already applied: " + rel
    for old, new in edits:
        assert t.count(old) == 1, "anchor not found once in %s: %s" % (rel, old[:70])
        t = t.replace(old, new, 1)
    texts[rel] = t
for rel, t in texts.items():          # write only after every anchor matched
    (ROOT / rel).write_bytes(t.encode("utf-8"))
    print("updated", rel)
