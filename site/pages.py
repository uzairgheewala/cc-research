"""The Atlas v2 page sequence (analysis/reports/site_flow_design.md; approved 2026-10-13, DEC-06).

Every page: slug (file name), act, title, the question it answers, the module that renders it, and the tickets its prose
depends on (the build lists a page under "pages to re-read" when any of them changed since the page was last reviewed:
status, number of evidence files or the ticket's note, the fingerprint in tracker/snapshot.py; review state lives in
site/reviewed.json). Q2 tickets are bound since S23 (20 Oct), so research that moves as evidence reaches the re-read list. Order here is reading order; prev/next follow it.
"""

ACTS = [
    ("I", "The problem"),
    ("II", "What we found"),
    ("III", "What we are building"),
    ("IV", "Where we are"),
]

PAGES = [
    dict(slug="index", act=None, n=0, short="Today", module="pg_today", words=600, plain=True,
         title="Causal Atlas", question="Where does the research stand today, against every landmark, and what does it mean for what we deliver?",
         tickets=["DEC-05", "AUD-45", "TGT-18", "TGT-19", "BEN-13", "INF-10", "TEAM-11"]),
    dict(slug="primer", act="I", n=1, short="What causal discovery is", module="pg_primer",
         title="What causal discovery is", question="What is being discovered, and why is direction the hard part?", tickets=[]),
    dict(slug="scoring", act="I", n=2, short="Scoring and the ceiling", module="pg_scoring",
         title="How it is scored, and the ceiling", question="What does a leaderboard number measure, and what is the best possible?",
         tickets=["AUD-40"]),
    dict(slug="space", act="I", n=3, short="The space of problems", module="pg_space",
         title="The space of problems", question="Which problems exist, and which one does this project work in?", tickets=[]),
    dict(slug="scoreboard", act="II", n=4, short="The scoreboard", module="pg_scoreboard",
         title="The scoreboard is not what it seems",
         question="Do published scores measure methods, or how the files happen to be laid out?",
         tickets=["AUD-33", "AUD-34", "AUD-35", "REP-15"]),
    dict(slug="decisions", act="II", n=5, short="Do graphs help decisions?", module="pg_decisions",
         title="Do learned graphs help decisions?",
         question="If you act on a learned graph, are you better off than assuming nothing moves?", tickets=["AUD-36", "AUD-40"]),
    dict(slug="names", act="II", n=6, short="Agents read names", module="pg_names",
         title="LLM agents read names, not data", question="Where does an LLM agent's direction come from?",
         tickets=["AUD-17", "AUD-37", "AUD-38", "AUD-48"]),
    dict(slug="rca", act="II", n=7, short="Where declared structure wins", module="pg_rca",
         title="Where declared structure wins",
         question="Is there a real setting where stated structure plus abstention beats learning a graph?", tickets=["AUD-43"]),
    dict(slug="theses", act="III", n=8, short="Theses and the ledger", module="pg_theses",
         title="Theses and the claim ledger", question="What does this project claim, and what would it build?",
         tickets=["DEC-01", "DEC-05", "BLD-02", "BLD-06", "TGT-18", "TGT-19", "CAP-07"]),
    dict(slug="market", act="III", n=9, short="Who would use it", module="pg_market",
         title="Who would use it: the market", question="Who would pay for an audited causal claim, and where should it start?",
         tickets=["AUD-45", "STR-06", "AUD-41"]),
    dict(slug="gaps", act="IV", n=10, short="How far, and why", module="pg_gaps", words=2600,
         title="How far, and why", question="How far is each result from the bar set for it, and why?",
         tickets=["TGT-18", "TGT-19", "CAP-07", "BEN-13", "TEAM-10"]),
    dict(slug="status", act="IV", n=11, short="Plan and status", module="pg_status",
         title="Plan and status", question="What is done, what is next, and what is waiting on whom?",
         tickets=["TGT-18", "TGT-19", "CAP-07", "BLD-16", "BEN-13", "INF-06", "INF-10"]),
    dict(slug="changes", act="IV", n=12, short="What changed recently", module="pg_changes",
         title="What changed recently", question="What moved since I last looked?", tickets=[]),
    dict(slug="q1", act="R", n=17, short="Q1: the review fix", module="pg_q1", words=1800,  # S35 (q1 page)
         title="Quarter 1: fixing Causal-Copilot's review step",
         question="What does Causal-Copilot's review step do to the graph, and does our replacement do better?",
         tickets=["BLD-06", "EXT-03", "DLV-04", "DLV-07"]),
    dict(slug="explore", act="R", n=16, short="Explore", module="pg_explore", words=20000,
         title="Explore the research", question="What has the research measured so far, and how does it fit together?",
         tickets=["TEAM-11"]),
    dict(slug="glossary", act="R", n=13, short="Glossary", module="pg_glossary",
         title="Glossary", question="What does a term mean, and where is it taught?", tickets=[]),
    dict(slug="evidence", act="R", n=14, short="Evidence index", module="pg_evidence", words=4000,
         title="Evidence index", question="Where does each number on this site come from?", tickets=[]),
    dict(slug="about", act="R", n=15, short="How this site is built", module="pg_about",
         title="How this site is built", question="How is this site made, and which pages need re-reading?", tickets=[]),
]

# pages exempt from the surface-form term scan (they link terms to the glossary instead of teaching them)
SCAN_EXEMPT = {"index", "status", "changes", "glossary", "evidence", "about", "explore", "q1"}  # q1: S35 (q1 page)
# the narrative sequence (prev/next run through these; reference pages link back home)
SEQUENCE = [p["slug"] for p in PAGES if p["act"] != "R"]
# old single-page anchors -> new pages (index.html#space etc. keep working)
REDIRECTS = {"space": "space.html", "bounds": "scoring.html", "theses": "theses.html", "bundles": "status.html",
             "stages": "names.html"}
