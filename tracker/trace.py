"""trace.py - the correlation layer: typed links between dev tickets, prod rows, evidence, runs, docs and Slack.

No LLM, no network. Reads catalogue.py, prod.json, links.txt, status.json (and relay_log.jsonl through relay.py);
writes only the files marked (w). The rules are in LINKS.md; the relay of messages to Slack is in RELAY.md.

Files (tracker/)
  catalogue.py     dev tickets (REP-01 ...), list "Dev CD Tracker"            hand-edited (agents may edit)
  prod.json        prod rows, list "CD Tracker" in #causal-discovery          `prod-apply` / `prod-add` / `prod-publish`
                   type "passthrough": the row IS a dev ticket (same ID, prod title may differ)
                   type "group": a new ID in the same encoding that rolls up several dev tickets (`curates` links)
  prod_spec.json   Uzair's curation instruction, applied with `prod-apply`
  links.txt        explicit typed links, one per line                        `link` / `unlink`, or by hand
  ids.lock    (w)  every ID ever issued (dev and group), and retirements      append-only
  reviews.jsonl(w) fingerprints of the dev tickets behind each prod row when it was last published or reviewed
  mirrors.json(w)  Slack List record IDs per row, per list                    `mirror`
  trace.json  (w)  the full graph with derived status; trace.md (w) the check report
  prod_rows.json, slack_links.json (w)  cells for the two Slack Lists

Commands
  check | show ID | graph [ID] [--depth N] | next-id PREFIX
  link SRC REL DST [DST ...] [--note TEXT] | unlink SRC REL DST | retire ID --note TEXT
  prod-apply SPEC.json | prod-add ID (--group --title T --curates ID.. [--category C --criterion X] | --passthrough [--title T])
  prod-rows | prod-publish [ID ...] --note TEXT | prod-set ID --published STATUS [--force --note WHY] | review ID --note TEXT
  mirror FILE.csv [--list dev|prod|LISTID] | slack-links
"""
import argparse, collections, csv, datetime, glob, hashlib, json, os, re, shlex, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
REPO = RESEARCH.parent / "Causal-Copilot"
sys.path.insert(0, str(HERE))
import catalogue as C  # noqa: E402

PROD, LINKS, LOCK, REVIEWS, MIRRORS = (HERE / f for f in ("prod.json", "links.txt", "ids.lock", "reviews.jsonl", "mirrors.json"))
STATUS = HERE / "status.json"
DEV_CHANNEL, PROD_CHANNEL = "C0C7Q2CA2G7", "C0C8CQK1XME"      # #cd-tracker (dev), #causal-discovery (prod)
LISTS = {"dev": "F0C869P25NE", "prod": "F0C8ADF3DNG"}         # "Dev CD Tracker", "CD Tracker"
PREFIXES = sorted(C.CATS, key=len, reverse=True)
DEV_RE = re.compile(r"^(%s)-\d{2,3}$" % "|".join(PREFIXES))
MENTION_RE = re.compile(r"(?<![\w-])((?:%s)-\d{2,3})(?![\w-])" % "|".join(PREFIXES))
POINTER_RE = {"slack": re.compile(r"^slack:C[A-Z0-9]+(/\d+\.\d+)?$"), "slacklist": re.compile(r"^slacklist:F[A-Z0-9]+(/Rec[A-Z0-9]+)?$"),
              "url": re.compile(r"^url:https?://\S+$"), "project": re.compile(r"^project:\S+"), "chat": re.compile(r"^chat:.+")}
STATUSES = ("done", "in_progress", "todo", "blocked", "open")
EMOJI = {"done": "✅", "done_needs_evidence": "✅", "in_progress": "👀", "todo": "⏳", "blocked": "🔴", "open": "🔵", "reopened": "👀", None: "·"}
SLACK_LABEL = {"done": "✅ Done", "done_needs_evidence": "✅ Done", "in_progress": "👀 In progress", "reopened": "👀 In progress",
               "todo": "⏳ To-do", "blocked": "🔴 Blocked", "open": "🔵 Open"}
# What a prod row may show for a derived status: prod never shows ✅ for work below its evidence bar or reopened.
PUBLISH = {"done": "done", "done_needs_evidence": "in_progress", "reopened": "in_progress", "in_progress": "in_progress",
           "todo": "todo", "blocked": "blocked", "open": "open"}
TICKET = {"dev", "prod"}
ARTIFACT = {"file", "repo", "run"}
POINTER = {"slack", "slacklist", "url", "project", "chat"}
ANY = TICKET | ARTIFACT | POINTER
# relation: (allowed source kinds, allowed target kinds, inverse name, acyclic, note required)
REL = {
    "curates":      ({"prod"}, {"dev"}, "curated_into", False, False),
    "blocks":       (TICKET, TICKET, "blocked_by", True, False),
    "parent_of":    ({"dev"}, {"dev"}, "child_of", True, False),
    "supersedes":   (TICKET, TICKET, "superseded_by", True, False),
    "duplicates":   ({"dev"}, {"dev"}, "duplicated_by", True, False),
    "answers":      ({"dev"}, {"dev"}, "answered_by", False, False),
    "implements":   ({"dev"}, {"dev"}, "implemented_by", False, False),
    "evidences":    (ARTIFACT | POINTER, {"dev"}, "evidenced_by", False, False),
    "produced_by":  ({"file", "repo"}, ARTIFACT, "produced", True, False),
    "published_at": (TICKET, {"slack", "url", "project"}, "publishes", False, False),
    "mirrors":      ({"slacklist"}, TICKET, "mirrored_by", False, False),
    "relates":      (ANY, ANY, "relates", False, True),
}
SCAN = ["README.md", "AGENTS.md", "GOALS_by_category_slack.txt", "analysis/README.md", "analysis/reports/*.md", "plans/*.json",
        "tracker/README.md", "tracker/LINKS.md", "tracker/RELAY.md", "docs/**/*.md", "harness/*.md"]
GROUPS = set()       # prod-only group IDs; filled by load_prod()


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def jl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()] if path.exists() else []


def kind_of(ref):
    if DEV_RE.match(ref):
        return "prod" if ref in GROUPS else "dev"
    if ":" in ref:
        k = ref.split(":", 1)[0]
        return k if k in ARTIFACT | POINTER else None
    return None


def norm_evidence(e):
    e = e.split(" (")[0].strip()
    return e if kind_of(e) in ARTIFACT | POINTER else "file:" + e


def lv(level):
    return int(level[1:]) if level else 0


_EXISTS = {}     # path existence, memoised per process: the mounted folder answers each stat slowly (BND-05 day: 6 s per check)


_LISTING = {}


def _listing(d):
    """Names in directory d (cached); None if d is not a directory. One listing replaces a stat per file."""
    d = str(d)
    if d not in _LISTING:
        try:
            _LISTING[d] = set(os.listdir(d))
        except OSError:
            _LISTING[d] = None
    return _LISTING[d]


def _path_exists(p):
    p = Path(os.path.normpath(str(p)))
    names = _listing(p.parent)
    return names is not None and p.name in names


def _exists(key, fn):
    if key not in _EXISTS:
        _EXISTS[key] = fn()
    return _EXISTS[key]


def resolves(ref, k, dev, prod):
    if k == "dev":
        return ref in dev, "unknown dev ticket"
    if k == "prod":
        return ref in prod, "unknown prod row"
    if k in ("file", "repo"):
        raw = ref.split(":", 1)[1]
        p = (RESEARCH if k == "file" else REPO) / raw
        return _exists(str(p), lambda: bool(glob.glob(str(p))) if any(c in raw for c in "*?[") else _path_exists(p)), "path not found"
    if k == "run":
        q = RESEARCH / "runs" / ref[4:] / "meta.json"
        return _exists(str(q), lambda: _path_exists(q)), "run not found"
    if k in POINTER_RE:
        return bool(POINTER_RE[k].match(ref)), "malformed pointer"
    return False, "unknown node kind"


# ----------------------------------------------------------------------------- loading
def load_prod():
    rows = json.load(open(PROD, encoding="utf-8")) if PROD.exists() else []
    GROUPS.clear(); GROUPS.update(r["id"] for r in rows if r.get("type") == "group")
    return {r["id"]: r for r in rows}


def save_prod(prod):
    key = lambda r: (r.get("order", 9999), r["id"])
    json.dump(sorted(prod.values(), key=key), open(PROD, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def parse_links():
    edges, errors = [], []
    if not LINKS.exists():
        return edges, errors
    for n, line in enumerate(open(LINKS, encoding="utf-8"), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        body, _, note = s.partition(" | ")
        try:
            toks = shlex.split(body)
        except ValueError as e:
            errors.append(("T2", "links.txt:%d cannot parse: %s" % (n, e))); continue
        if len(toks) < 3:
            errors.append(("T2", "links.txt:%d needs SRC REL DST" % n)); continue
        for dst in toks[2:]:
            edges.append({"src": toks[0], "rel": toks[1], "dst": dst, "note": note.strip(), "origin": "links.txt:%d" % n})
    return edges, errors


def derived_edges(dev):
    out = []
    for i in dev.values():
        for e in i["evidence"]:
            out.append({"src": norm_evidence(e), "rel": "evidences", "dst": i["id"], "note": "", "origin": "catalogue"})
        for b in MENTION_RE.findall(i.get("blocked_by") or ""):
            out.append({"src": b, "rel": "blocks", "dst": i["id"], "note": i["blocked_by"], "origin": "catalogue"})
    for plan in sorted(glob.glob(str(RESEARCH / "plans" / "*_dag.json"))):     # bundle DAGs: dependencies and closures
        P = json.load(open(plan, encoding="utf-8"))
        origin = "plan:" + Path(plan).name
        for bnd in P.get("bundles", []):
            if bnd["id"] not in dev:
                continue
            for dep in bnd["depends_on"]:
                out.append({"src": dep, "rel": "blocks", "dst": bnd["id"], "note": "", "origin": origin})
            for t in bnd["closes"]:
                out.append({"src": bnd["id"], "rel": "implements", "dst": t, "note": "", "origin": origin})
    if MIRRORS.exists():
        m = json.load(open(MIRRORS, encoding="utf-8"))
        for list_id, recs in m.get("lists", {}).items():
            for tid, rec in recs.items():
                out.append({"src": "slacklist:%s/%s" % (list_id, rec), "rel": "mirrors", "dst": tid, "note": "", "origin": "mirrors.json"})
    return out


def mention_edges():
    out = []
    for pat in SCAN:
        for f in sorted(glob.glob(str(RESEARCH / pat), recursive=True)):
            rel = Path(f).relative_to(RESEARCH).as_posix()
            txt = open(f, encoding="utf-8", errors="replace").read()
            for tid in sorted(set(MENTION_RE.findall(txt))):
                out.append({"src": "file:" + rel, "rel": "mentions", "dst": tid, "note": "", "origin": "scan"})
    return out


def fingerprint(rec, pins):
    ev = sorted((k, v["digest"]) for k, v in pins.items() if k.split("|", 1)[0] == rec["id"])
    core = {k: rec.get(k) for k in ("title", "status", "effective_status", "level", "criterion")}
    return hashlib.sha256(json.dumps([core, ev], sort_keys=True).encode()).hexdigest()[:16]


def derive_group(states):
    if not states:
        return None
    s = set(states)
    if "reopened" in s:
        return "reopened"
    if s <= {"done"}:
        return "done"
    if s <= {"done", "done_needs_evidence"}:
        return "done_needs_evidence"
    if s <= {"open"}:
        return "open"
    if s & {"in_progress", "done", "done_needs_evidence"}:
        return "in_progress"
    if "blocked" in s and not s & {"todo"}:          # every unfinished ticket that is not an open question is blocked
        return "blocked"
    return "todo"


# ----------------------------------------------------------------------------- the graph and every rule
def build():
    dev = {i["id"]: i for i in C.ITEMS}
    prod = load_prod()
    status = json.load(open(STATUS, encoding="utf-8")) if STATUS.exists() else {"items": [], "verified_utc": ""}
    st = {r["id"]: r for r in status["items"]}
    pins = json.load(open(HERE / "pins.json")) if (HERE / "pins.json").exists() else {}
    explicit, errs = parse_links()
    findings = [("ERROR",) + f for f in errs]
    F = lambda sev, code, msg: findings.append((sev, code, msg))
    edges = explicit + derived_edges(dev) + mention_edges()

    # T10 status.json must agree with catalogue.py
    stale = sorted(t for t, i in dev.items() if t not in st or st[t]["status"] != i["status"] or st[t]["title"] != i["title"]
                   or st[t]["evidence"] != i["evidence"])
    gone = sorted(set(st) - set(dev))
    if stale or gone:
        F("ERROR", "T10", "status.json disagrees with catalogue.py for %s: run `python tracker/verify.py` first" % ", ".join((stale + gone)[:12]))

    # T7 IDs
    for tid, n in collections.Counter(i["id"] for i in C.ITEMS).items():
        if n > 1:
            F("ERROR", "T7", "%s defined %d times in catalogue.py" % (tid, n))
        if not DEV_RE.match(tid):
            F("ERROR", "T7", "%s does not match the ID grammar" % tid)
    for pid, p in prod.items():
        typ = p.get("type")
        if typ == "group":
            if not DEV_RE.match(pid):
                F("ERROR", "T7", "group %s does not match the ID grammar" % pid)
            if pid in dev:
                F("ERROR", "T7", "group %s is also a dev ticket; group IDs are new IDs in the same encoding" % pid)
        elif typ == "passthrough":
            if pid not in dev:
                F("ERROR", "T7", "pass-through row %s is not a dev ticket" % pid)
        else:
            F("ERROR", "T7", "%s has type %r (group or passthrough)" % (pid, typ))
        if p.get("published_status") not in (None,) + STATUSES:
            F("ERROR", "T7", "%s published_status %r is not a status" % (pid, p.get("published_status")))

    # T4 IDs never vanish or get reused
    lock = jl(LOCK)
    issued = {r["id"]: r for r in lock if r.get("event") == "issued"}
    retired = {r["id"] for r in lock if r.get("event") == "retired"}
    for tid in sorted(set(issued) - set(dev) - GROUPS - retired):
        F("ERROR", "T4", "%s was issued (%s) and is gone; restore it or `trace.py retire %s --note ...`" % (tid, issued[tid]["t"][:10], tid))
    for tid in sorted((set(dev) | GROUPS) & retired):
        F("ERROR", "T4", "%s was retired and is defined again: IDs are never reused" % tid)
    for tid in sorted(set(dev) & {t for t, r in issued.items() if r.get("kind") == "prod"}):
        F("ERROR", "T4", "%s was issued as a prod group; a dev ticket may not take it (use `trace.py next-id`)" % tid)

    # T1 / T2
    for e in edges:
        if e["origin"] == "scan":
            continue
        ks, kd = kind_of(e["src"]), kind_of(e["dst"])
        if e["rel"] not in REL:
            F("ERROR", "T2", "%s unknown relation %r (allowed: %s)" % (e["origin"], e["rel"], ", ".join(REL))); e["bad"] = True; continue
        srcs, dsts, _, _, need_note = REL[e["rel"]]
        if ks not in srcs or kd not in dsts:
            F("ERROR", "T2", "%s %s %s %s: %s->%s not allowed for %s" % (e["origin"], e["src"], e["rel"], e["dst"], ks, kd, e["rel"])); e["bad"] = True
        for ref, k in ((e["src"], ks), (e["dst"], kd)):
            ok, why = resolves(ref, k, dev, prod)
            if not ok:
                F("ERROR" if e["origin"] != "catalogue" else "WARN", "T1", "%s %s: %s" % (e["origin"], ref, why)); e["bad"] = True
        if need_note and not e["note"]:
            F("WARN", "W7", "%s relates without a note (say why the two are related)" % e["origin"])
    good = [e for e in edges if not e.get("bad")]
    for k, n in collections.Counter((e["src"], e["rel"], e["dst"]) for e in good if e["origin"].startswith("links")).items():
        if n > 1:
            F("WARN", "W10", "duplicate link %s %s %s (%d times)" % (k[0], k[1], k[2], n))

    # T3 acyclic relations
    for rel, spec in REL.items():
        if not spec[3]:
            continue
        g = collections.defaultdict(set)
        for e in good:
            if e["rel"] == rel:
                g[e["src"]].add(e["dst"])
        color = {}
        def dfs(u, path):
            color[u] = 1
            for v in g[u]:
                if color.get(v) == 1:
                    F("ERROR", "T3", "cycle in %s: %s" % (rel, " -> ".join(path[path.index(v):] + [v]) if v in path else u + " -> " + v))
                elif v not in color:
                    dfs(v, path + [v])
            color[u] = 2
        for u in list(g):
            if u not in color:
                dfs(u, [u])

    out = collections.defaultdict(list); inn = collections.defaultdict(list)
    for e in good:
        out[e["src"]].append(e); inn[e["dst"]].append(e)
    deveff = lambda t: (st.get(t) or {}).get("effective_status")
    curated = {pid: ([pid] if p.get("type") == "passthrough" else [e["dst"] for e in out[pid] if e["rel"] == "curates"]) for pid, p in prod.items()}
    derived = {pid: (deveff(pid) if prod[pid].get("type") == "passthrough" else derive_group([deveff(t) for t in cur])) for pid, cur in curated.items()}
    eff = lambda t: deveff(t) if t in dev else derived.get(t)

    # T8 / W4 parents
    for t in dev:
        parents = [e["src"] for e in inn[t] if e["rel"] == "parent_of"]
        if len(parents) > 1:
            F("ERROR", "T8", "%s has %d parents: %s" % (t, len(parents), parents))
        kids = [e["dst"] for e in out[t] if e["rel"] == "parent_of"]
        if kids and eff(t) == "done" and any(eff(k) != "done" for k in kids):
            F("WARN", "W4", "%s is done but children are not: %s" % (t, [k for k in kids if eff(k) != "done"]))

    # T11 a bundle is done only when every ticket it closes is done
    for t, i in dev.items():
        if i.get("kind") == "bundle" and eff(t) in ("done", "done_needs_evidence"):
            undone = [e["dst"] for e in out[t] if e["rel"] == "implements" and eff(e["dst"]) != "done"]
            if undone:
                F("ERROR", "T11", "bundle %s is done but tickets it closes are not: %s" % (t, undone))

    # W3 blockers (a bundle may start before its dependencies finish; it may not finish before them)
    for t in list(dev) + sorted(GROUPS):
        blockers = [e["src"] for e in inn[t] if e["rel"] == "blocks"]
        open_b = [b for b in blockers if eff(b) not in ("done", "done_needs_evidence")]
        s = eff(t)
        early = ("done", "done_needs_evidence") if dev.get(t, {}).get("kind") == "bundle" else ("done", "done_needs_evidence", "in_progress")
        if s in early and open_b:
            F("WARN", "W3", "%s is %s while blocked by unfinished %s" % (t, s, open_b))
        if s == "blocked" and blockers and not open_b:
            F("WARN", "W3", "%s is blocked but every blocker is done (%s): unblock it" % (t, blockers))

    # prod rows
    last_review = {}
    for r in jl(REVIEWS):
        last_review[r["prod"]] = r
    mirrors = json.load(open(MIRRORS, encoding="utf-8")) if MIRRORS.exists() else {"lists": {}}
    prod_recs = mirrors.get("lists", {}).get(LISTS["prod"])
    prod_view = {}
    for pid, p in prod.items():
        cur = curated[pid]
        if p.get("type") == "group" and not cur:
            F("ERROR", "T5", "group %s curates no dev ticket" % pid)
        d = derived[pid]
        pub = p.get("published_status")
        if pub == "done" and d != "done":
            F("ERROR", "T6", "%s is published ✅ but its dev tickets say %s (%s)" % (
                pid, d, ", ".join("%s %s" % (t, deveff(t)) for t in cur if deveff(t) != "done")))
        elif pub is not None and d is not None and pub != PUBLISH[d]:
            F("WARN", "W2", "%s: prod shows %s, dev now says %s; run `trace.py prod-rows`, update the list, then `prod-publish`" % (pid, pub, d))
        fps = {t: fingerprint(st[t], pins) for t in cur if t in st}
        rv = last_review.get(pid)
        changed = sorted(t for t in cur if rv and rv["fingerprints"].get(t) != fps.get(t))
        if pub is not None and changed:
            F("WARN", "W1", "%s is suspect: %s changed since it was last published or reviewed (%s)" % (pid, changed, rv["t"][:16]))
        for t in cur:
            if any(e["rel"] in ("supersedes", "duplicates") for e in inn[t]):
                F("WARN", "W6", "%s curates %s, which is superseded or a duplicate" % (pid, t))
        if prod_recs is not None and pid not in prod_recs:
            F("WARN", "W9", "%s is not in the Slack list CD Tracker (%s)" % (pid, LISTS["prod"]))
        levels = [lv((st.get(t) or {}).get("level")) for t in cur]
        prod_view[pid] = {"type": p.get("type"), "curates": cur, "derived_status": d, "published_status": pub,
                          "min_level": "V%d" % min(levels) if levels else None, "suspect": changed, "last_review": rv["t"] if rv else None}

    # W5 mentions of IDs that do not exist
    for e in edges:
        if e["origin"] == "scan" and e["dst"] not in dev and e["dst"] not in GROUPS and e["dst"] not in retired:
            F("WARN", "W5", "%s mentions %s, which is not a ticket (typo, or never issued)" % (e["src"], e["dst"]))

    G = dict(dev=dev, prod=prod, st=st, pins=pins, edges=edges, good=good, out=out, inn=inn, eff=eff, deveff=deveff,
             curated=curated, derived=derived, findings=findings, prod_view=prod_view, lock=lock, issued=issued,
             retired=retired, status_utc=status.get("verified_utc"), mirrors=mirrors)
    try:
        import relay                                    # message relay checks (RELAY.md); optional
        findings += relay.findings(G)
    except ImportError:
        pass
    return G


def lock_new_ids(G):
    t = now(); new = []
    for tid, rec in list(G["dev"].items()) + [(g, G["prod"][g]) for g in sorted(GROUPS)]:
        if tid not in G["issued"]:
            new.append({"t": t, "event": "issued", "id": tid, "kind": kind_of(tid), "title": rec["title"]})
    if new:
        with open(LOCK, "a", encoding="utf-8") as fh:
            for r in new:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        G["issued"].update({r["id"]: r for r in new})
    return new


def next_id(prefix, G):
    nums = [int(t.split("-")[1]) for t in list(G["dev"]) + list(G["prod"]) + list(G["issued"]) if t.split("-")[0] == prefix]
    return "%s-%02d" % (prefix, max(nums or [0]) + 1)


def export(G):
    nodes = {}
    for t, i in G["dev"].items():
        r = G["st"].get(t, {})
        nodes[t] = {"kind": "dev", "title": i["title"], "category": C.CATS[i["cat"]], "status": i["status"],
                    "effective_status": r.get("effective_status"), "level": r.get("level"), "in_prod": t in G["prod"]}
    for p, v in G["prod_view"].items():
        nodes.setdefault(p, {"kind": "prod"}).update({"prod_title": G["prod"][p]["title"], "prod": v})
    for e in G["good"]:
        for ref in (e["src"], e["dst"]):
            nodes.setdefault(ref, {"kind": kind_of(ref)})
    json.dump({"generated_utc": now(), "status_verified_utc": G["status_utc"], "lists": LISTS,
               "relations": {k: {"inverse": v[2], "acyclic": v[3]} for k, v in REL.items()},
               "nodes": nodes, "edges": [{k: e[k] for k in ("src", "rel", "dst", "note", "origin")} for e in G["good"]],
               "findings": [{"severity": s, "code": c, "message": m} for s, c, m in G["findings"]]},
              open(HERE / "trace.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def title_of(ref, G):
    if ref in G["prod"] and (ref in GROUPS or G["prod"][ref].get("title")):
        return G["prod"][ref]["title"]
    return G["dev"][ref]["title"] if ref in G["dev"] else ""


def label(ref, G):
    k = kind_of(ref)
    if k in ("dev", "prod"):
        return "%s %s %s" % (EMOJI[G["eff"](ref)], ref, (G["dev"][ref]["title"] if k == "dev" else G["prod"][ref]["title"])[:70])
    return ref


# ----------------------------------------------------------------------------- commands
def cmd_check(a):
    G = build()
    new = lock_new_ids(G)
    export(G)
    errs = [f for f in G["findings"] if f[0] == "ERROR"]
    warns = [f for f in G["findings"] if f[0] == "WARN"]
    cnt = collections.Counter((e["rel"], e["origin"].split(":")[0]) for e in G["good"])
    in_prod = {t for cur in G["curated"].values() for t in cur}
    left_out = sorted(t for t in G["dev"] if t not in in_prod)
    L = ["# Trace check (%s)" % now(), "", "status.json verified %s. Dev tickets %d; prod rows %d (%d groups, %d pass-through). IDs newly locked: %d." % (
        G["status_utc"], len(G["dev"]), len(G["prod"]), len(GROUPS), len(G["prod"]) - len(GROUPS), len(new)), "",
         "## Links", "", "| relation | source | count |", "|---|---|---|"]
    L += ["| %s | %s | %d |" % (r, o, n) for (r, o), n in sorted(cnt.items())]
    L += ["", "## Findings: %d errors, %d warnings" % (len(errs), len(warns)), ""]
    L += ["- **%s %s** %s" % f for f in errs + warns] or ["none"]
    if G["prod"]:
        L += ["", "## Prod rows", "", "| ID | type | published | derived | min level | suspect | curates |", "|---|---|---|---|---|---|---|"]
        for p in prod_order(G):
            v = G["prod_view"][p]
            L.append("| %s | %s | %s | %s | %s | %s | %s |" % (p, v["type"], v["published_status"], v["derived_status"], v["min_level"],
                                                          ", ".join(v["suspect"]) or "-", ", ".join(v["curates"])))
        L += ["", "## Dev tickets in no prod row (%d)" % len(left_out), "", ", ".join(left_out)]
    open(HERE / "trace.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("links: %s" % ", ".join("%s %d" % (r, n) for r, n in sorted(collections.Counter(e["rel"] for e in G["good"]).items())))
    print("dev %d, prod rows %d (groups %d), not in prod %d, newly locked IDs %d; %d errors, %d warnings (trace.md)" % (
        len(G["dev"]), len(G["prod"]), len(GROUPS), len(left_out), len(new), len(errs), len(warns)))
    for f in errs + warns[: a.max_warn]:
        print("  %s %s %s" % f)
    if len(warns) > a.max_warn:
        print("  ... %d more warnings in trace.md" % (len(warns) - a.max_warn))
    sys.exit(1 if errs else 0)


def cmd_show(a):
    G = build()
    t = a.id
    if t in G["dev"]:
        i, r = G["dev"][t], G["st"].get(t, {})
        print("%s  [dev]\n  category %s | status %s | effective %s | level %s (required %s)" % (
            label(t, G), C.CATS[i["cat"]], i["status"], r.get("effective_status"), r.get("level"), r.get("required_level") or "-"))
        print("  criterion: %s" % (i["criterion"] or "-"))
        for p in r.get("problems") or []:
            print("  PROBLEM: " + p)
    if t in G["prod"]:
        v = G["prod_view"][t]
        print("%s  [prod %s] %s\n  published %s | derived %s | min level %s | last published/reviewed %s | suspect %s" % (
            EMOJI[v["derived_status"]], v["type"], title_of(t, G), v["published_status"], v["derived_status"], v["min_level"],
            v["last_review"], v["suspect"] or "-"))
    if t not in G["dev"] and t not in G["prod"]:
        print("%s [%s]" % (t, kind_of(t)))
    groups = collections.defaultdict(list)
    for e in G["out"][t]:
        groups[e["rel"]].append((e["dst"], e))
    for e in G["inn"][t]:
        groups[REL[e["rel"]][2] if e["rel"] in REL else "mentioned_in"].append((e["src"], e))
    for rel in sorted(groups):
        print("  %s:" % rel)
        for ref, e in groups[rel]:
            print("    %s%s%s" % (label(ref, G), "   | " + e["note"] if e["note"] and e["origin"] != "catalogue" else "",
                                  "" if e["origin"] in ("catalogue", "scan") else "   (%s)" % e["origin"]))
    for f in G["findings"]:
        if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(t), f[2]):
            print("  %s %s %s" % f)


def cmd_graph(a):
    G = build()
    keep = None
    if a.id:
        keep, frontier = {a.id}, {a.id}
        for _ in range(a.depth):
            nxt = set()
            for u in frontier:
                nxt |= {e["dst"] for e in G["out"][u]} | {e["src"] for e in G["inn"][u]}
            frontier = nxt - keep; keep |= nxt
    nid = lambda r: "n" + hashlib.md5(r.encode()).hexdigest()[:8]
    lines, seen = ["graph LR"], set()
    for e in G["good"]:
        if (e["rel"] == "mentions" and not a.mentions) or (e["rel"] == "evidences" and not a.evidence and not a.id):
            continue
        if keep is not None and not (e["src"] in keep and e["dst"] in keep):
            continue
        for r in (e["src"], e["dst"]):
            if r not in seen:
                seen.add(r); lines.append('  %s["%s"]' % (nid(r), label(r, G).replace('"', "'")[:60]))
        lines.append("  %s -->|%s| %s" % (nid(e["src"]), e["rel"], nid(e["dst"])))
    print("\n".join(lines))


def append_links(rows):
    with open(LINKS, "a", encoding="utf-8") as fh:
        for src, rel, dst, note in rows:
            fh.write("%s %s %s%s\n" % (src, rel, dst, " | " + note if note else ""))


def validate_link(src, rel, dst, note, G):
    if rel not in REL:
        return ["unknown relation %r; allowed: %s" % (rel, ", ".join(REL))]
    errs = []
    ks, kd = kind_of(src), kind_of(dst)
    if ks not in REL[rel][0] or kd not in REL[rel][1]:
        errs.append("%s->%s not allowed for %s (allowed %s -> %s)" % (ks, kd, rel, sorted(REL[rel][0]), sorted(REL[rel][1])))
    for ref, k in ((src, ks), (dst, kd)):
        ok, why = resolves(ref, k, G["dev"], G["prod"])
        if not ok:
            errs.append("%s: %s" % (ref, why))
    if REL[rel][4] and not note:
        errs.append("%s needs --note" % rel)
    return errs


def cmd_link(a):
    G = build()
    rows, errs = [], []
    for dst in a.dst:
        e = validate_link(a.src, a.rel, dst, a.note, G)
        errs += e
        if not e and not any(x["src"] == a.src and x["rel"] == a.rel and x["dst"] == dst for x in G["good"]):
            rows.append((a.src, a.rel, dst, a.note))
    if errs:
        sys.exit("refused: " + "; ".join(errs))
    append_links(rows)
    print("added %d link(s); run `trace.py check`" % len(rows))


def cmd_unlink(a):
    lines = open(LINKS, encoding="utf-8").read().splitlines() if LINKS.exists() else []
    keep, removed = [], 0
    for l in lines:
        body = l.split(" | ")[0].strip()
        toks = shlex.split(body) if body and not body.startswith("#") else []
        if len(toks) >= 3 and toks[0] == a.src and toks[1] == a.rel and a.dst in toks[2:]:
            rest = [d for d in toks[2:] if d != a.dst]; removed += 1
            if rest:
                keep.append("%s %s %s%s" % (toks[0], toks[1], " ".join(rest), l[len(l.split(" | ")[0]):]))
            keep.append("# removed %s: %s %s %s" % (now()[:10], a.src, a.rel, a.dst))
        else:
            keep.append(l)
    open(LINKS, "w", encoding="utf-8").write("\n".join(keep) + "\n")
    print("removed %d" % removed)


def cmd_next_id(a):
    G = build()
    if a.prefix not in C.CATS:
        sys.exit("unknown prefix; known: " + ", ".join(sorted(C.CATS)))
    print(next_id(a.prefix, G))


def record_review(pids, note, G, event="review"):
    with open(REVIEWS, "a", encoding="utf-8") as fh:
        for pid in pids:
            cur = G["curated"][pid]
            fh.write(json.dumps({"t": now(), "prod": pid, "event": event, "note": note,
                                 "fingerprints": {t: fingerprint(G["st"][t], G["pins"]) for t in cur if t in G["st"]},
                                 "states": {t: G["deveff"](t) for t in cur}}, ensure_ascii=False) + "\n")


def add_row(G, rid, typ, title="", curates=(), category=None, criterion="", kind=None, order=None):
    """Validate and add one prod row (no writes on refusal). Returns list of errors."""
    dev, prod = G["dev"], G["prod"]
    if rid in prod:
        return ["%s is already a prod row" % rid]
    if typ == "passthrough":
        if rid not in dev:
            return ["%s: pass-through rows must be dev tickets" % rid]
    elif typ == "group":
        if not DEV_RE.match(rid):
            return ["%s does not match the ID grammar" % rid]
        if rid in dev or rid in G["issued"]:
            return ["%s is already issued; use `trace.py next-id %s`" % (rid, rid.split("-")[0])]
        bad = [t for t in curates if t not in dev]
        if bad or not curates:
            return ["group %s needs dev tickets to curate (bad: %s)" % (rid, bad)]
        if not title:
            return ["group %s needs a title" % rid]
    else:
        return ["type must be group or passthrough"]
    row = {"id": rid, "type": typ, "title": title or "", "created": now(), "published_status": None, "history": []}
    if typ == "group":
        row.update(category=category or C.CATS[rid.split("-")[0]], criterion=criterion, kind=kind or "group")
    if order is not None:
        row["order"] = order
    prod[rid] = row
    if typ == "group":
        GROUPS.add(rid)
        G.setdefault("pending_links", []).extend((rid, "curates", t, "") for t in curates)   # written only on success
    return []


def cmd_prod_add(a):
    G = build()
    typ = "group" if a.group else "passthrough"
    errs = add_row(G, a.id, typ, a.title or "", a.curates or [], a.category, a.criterion or "")
    if errs:
        sys.exit("refused: " + "; ".join(errs))
    save_prod(G["prod"]); append_links(G.get("pending_links", []))
    G = build(); lock_new_ids(G)
    print("%s added (%s); derived status %s" % (a.id, typ, G["derived"][a.id]))


def cmd_prod_apply(a):
    """Apply a curation spec: {"rows": [{"type": "group", "prefix": "REP", "title": ..., "curates": [...], ...} |
    {"type": "passthrough", "id": ..., "title": optional}]}. Group IDs are assigned with next-id unless given. Idempotent."""
    spec = json.load(open(a.spec, encoding="utf-8"))
    G = build()
    by_title = {(r["type"], r.get("title"), r["id"] if r["type"] == "passthrough" else None): r["id"] for r in G["prod"].values()}
    added, skipped, errs = [], [], []
    for n, s in enumerate(spec["rows"]):
        typ = s["type"]
        key = (typ, s.get("title", ""), s.get("id") if typ == "passthrough" else None)
        if typ == "passthrough" and s["id"] in G["prod"] or typ == "group" and key in by_title:
            skipped.append(s.get("id") or by_title[key]); continue
        rid = s.get("id") or next_id(s["prefix"], G)
        e = add_row(G, rid, typ, s.get("title", ""), s.get("curates", []), s.get("category"), s.get("criterion", ""), s.get("kind"), order=n)
        if e:
            errs += e; continue
        added.append(rid)
        G["issued"][rid] = {"t": now(), "id": rid, "kind": kind_of(rid)}   # reserve within this run
    if errs:
        sys.exit("refused, nothing written: " + "; ".join(errs))
    save_prod(G["prod"]); append_links(G.get("pending_links", []))
    G = build(); lock_new_ids(G)
    json.dump({"applied_utc": now(), "spec": str(a.spec), "added": added, "skipped": skipped},
              open(HERE / "prod_apply_report.json", "w", encoding="utf-8"), indent=1)
    print("added %d rows, skipped %d already present" % (len(added), len(skipped)))
    for r in added:
        print("  %s %s" % (r, G["prod"][r]["title"] or "(dev title)"))


def prod_order(G):
    def key(p):
        r = G["prod"][p]
        cat = r.get("category") if r.get("type") == "group" else C.CATS[G["dev"][p]["cat"]]
        num = int(cat.split()[0]) if cat and cat.split()[0].isdigit() else 99
        return (num, p.split("-")[0], int(p.split("-")[1]) if r.get("type") == "passthrough" else 1000 + int(p.split("-")[1]))
    return sorted(G["prod"], key=key)


def links_cell(t, G, skip=("evidences", "mentions", "mirrors", "published_at")):
    parts = collections.defaultdict(list)
    for e in G["out"][t]:
        if e["rel"] not in skip:
            parts[e["rel"]].append(e["dst"])
    for e in G["inn"][t]:
        if e["rel"] not in skip:
            parts[REL[e["rel"]][2]].append(e["src"])
    return " · ".join("%s %s" % (r.replace("_", " "), ", ".join(sorted(set(v)))) for r, v in sorted(parts.items()))


def blockers_of(t, G):
    return sorted({e["src"] for e in G["inn"][t] if e["rel"] == "blocks"})


def prod_row_cells(p, G):
    r, v = G["prod"][p], G["prod_view"][p]
    status = SLACK_LABEL[PUBLISH[v["derived_status"]]]
    if r["type"] == "passthrough":
        s = G["st"][p]; dev_title = G["dev"][p]["title"]
        title = r.get("title") or dev_title
        crit = s["criterion"] or ("" if title == dev_title else "Dev ticket: " + dev_title)
        if s["criterion"] and title != dev_title:
            crit += " (dev ticket: %s)" % dev_title
        b = blockers_of(p, G)
        return {"Item": "%s  %s" % (p, title), "ID": p, "Category": s["category"], "Status": status, "Kind": s["kind"],
                "Evidence level": s["level"], "Closing criterion": crit, "Evidence": "\n".join(s["evidence"]),
                "Checks": "; ".join(("PASS " if c["ok"] else "FAIL ") + c["detail"] for c in s["checks"]), "Reproduce": s["reproduce"],
                "Reopen if": "; ".join(s["reopen_if"]), "Blocked by": ", ".join(b) or (s["blocked_by"] or ""),
                "Links": links_cell(p, G)}
    cur = v["curates"]
    states = [G["deveff"](t) for t in cur]
    c = collections.Counter(PUBLISH[s] for s in states)
    blk = ["%s ← %s" % (t, ", ".join(blockers_of(t, G))) for t in cur if blockers_of(t, G)]
    blk += ["%s ← %s" % (t, G["dev"][t]["blocked_by"]) for t in cur if G["dev"][t].get("blocked_by") and not blockers_of(t, G)]
    return {"Item": "%s  %s" % (p, r["title"]), "ID": p, "Category": r["category"], "Status": status, "Kind": r.get("kind", "group"),
            "Evidence level": v["min_level"],
            "Closing criterion": (r.get("criterion", "") + " " if r.get("criterion") else "") +
                                 "Closed when every ticket below is done at its required evidence level.",
            "Evidence": "\n".join("%s %s %s %s%s" % (EMOJI[PUBLISH[G["deveff"](t)]], t, G["st"][t]["level"], G["dev"][t]["title"],
                                                    {"done_needs_evidence": " (done, needs evidence)", "reopened": " (reopened)"}.get(G["deveff"](t), ""))
                                  for t in cur),
            "Checks": "%d of %d done; %d in progress; %d to-do; %d blocked; %d open; lowest evidence level %s" % (
                c["done"], len(cur), c["in_progress"], c["todo"], c["blocked"], c["open"], v["min_level"]),
            "Reproduce": "python tracker/trace.py show %s" % p,
            "Reopen if": "any ticket below reopens, or its evidence changes (trace.py T6 / W1)",
            "Blocked by": "; ".join(blk), "Links": links_cell(p, G)}


def cmd_prod_rows(a):
    G = build()
    rows = [prod_row_cells(p, G) for p in prod_order(G)]
    json.dump(rows, open(HERE / "prod_rows.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%d prod rows written to prod_rows.json" % len(rows))


def cmd_prod_publish(a):
    """Record that the Slack prod list now shows each row's derived status (run after updating the list)."""
    G = build()
    ids = a.ids or list(G["prod"])
    for p in ids:
        d = G["derived"][p]
        G["prod"][p]["published_status"] = PUBLISH[d]
        G["prod"][p].setdefault("history", []).append({"t": now(), "published_status": PUBLISH[d], "derived": d, "forced": False, "note": a.note})
    save_prod(G["prod"])
    record_review(ids, a.note, G, event="publish")
    print("published %d rows" % len(ids))


def cmd_prod_set(a):
    G = build()
    if a.id not in G["prod"]:
        sys.exit("unknown prod row")
    d = G["derived"][a.id]
    if a.published == "done" and d != "done" and not a.force:
        sys.exit("refused: %s's dev tickets say %s, not done. Fix the dev side, or --force --note WHY (logged)." % (a.id, d))
    if a.force and not a.note:
        sys.exit("--force needs --note")
    G["prod"][a.id]["published_status"] = a.published
    G["prod"][a.id].setdefault("history", []).append({"t": now(), "published_status": a.published, "derived": d, "forced": bool(a.force), "note": a.note or ""})
    save_prod(G["prod"])
    print("%s published_status -> %s (derived %s)" % (a.id, a.published, d))


def cmd_review(a):
    G = build()
    if a.id not in G["prod"]:
        sys.exit("unknown prod row")
    record_review([a.id], a.note, G)
    print("review recorded for %s" % a.id)


def cmd_retire(a):
    G = build()
    if a.id not in G["issued"]:
        sys.exit("%s was never issued" % a.id)
    with open(LOCK, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": now(), "event": "retired", "id": a.id, "note": a.note}) + "\n")
    print("%s retired; remove it from catalogue.py / prod.json and never reuse the ID" % a.id)


def cmd_mirror(a):
    """Compare a Slack List CSV export with the files and record its record IDs in mirrors.json."""
    G = build()
    which = a.list if a.list in LISTS else ("prod" if a.list == LISTS["prod"] else "dev")
    list_id = LISTS.get(a.list, a.list)
    rows = list(csv.DictReader(open(a.csv, encoding="utf-8-sig")))
    if not rows or "ID" not in rows[0]:
        sys.exit("CSV needs an ID column")
    universe = G["st"] if which == "dev" else G["prod"]
    recs, drift, extra, blank = {}, [], [], 0
    for r in rows:
        tid = (r.get("ID") or "").strip()
        if not tid:
            blank += 1; continue
        if tid not in universe:
            extra.append(tid); continue
        if r.get("Record ID"):
            recs[tid] = r["Record ID"].strip()
        if which == "dev":
            want_s, want_l = SLACK_LABEL[G["st"][tid]["effective_status"]], G["st"][tid]["level"]
        else:
            want_s, want_l = SLACK_LABEL[PUBLISH[G["derived"][tid]]], G["prod_view"][tid]["min_level"]
        if "Status" in r and r["Status"].strip() != want_s:
            drift.append("%s Status: Slack %r, files say %r" % (tid, r["Status"].strip(), want_s))
        if "Evidence level" in r and r["Evidence level"].strip() and r["Evidence level"].strip() != want_l:
            drift.append("%s Evidence level: Slack %s, files say %s" % (tid, r["Evidence level"].strip(), want_l))
    seen = {(r.get("ID") or "").strip() for r in rows}
    missing = sorted(set(universe) - seen)
    m = json.load(open(MIRRORS, encoding="utf-8")) if MIRRORS.exists() else {"lists": {}}
    if recs:
        m["lists"][list_id] = dict(sorted(recs.items()))
        m.setdefault("read_utc", {})[list_id] = now()
        json.dump(m, open(MIRRORS, "w", encoding="utf-8"), indent=1)
    print("%s list: rows %d (blank %d), record IDs recorded %d, drift %d, unknown IDs %d, missing from Slack %d" % (
        which, len(rows), blank, len(recs), len(drift), len(extra), len(missing)))
    for d in drift + ["unknown ID in Slack: " + x for x in extra] + ["missing from Slack: " + x for x in missing]:
        print("  " + d)
    sys.exit(1 if drift or extra or missing else 0)


def in_prod_cell(t, G):
    """Where a dev ticket shows in the prod list CD Tracker."""
    homes = []
    if t in G["prod"] and G["prod"][t].get("type") == "passthrough":
        homes.append("itself" + (" (as: %s)" % G["prod"][t]["title"] if G["prod"][t].get("title") else ""))
    homes += ["%s %s" % (p, G["prod"][p]["title"]) for p in sorted(GROUPS) if t in G["curated"][p]]
    return "; ".join(homes)


def cmd_slack_links(a):
    """Cells for the Dev CD Tracker list: Links (typed relations) and In prod (where the ticket shows in CD Tracker)."""
    G = build()
    cells = {t: {"Links": links_cell(t, G), "In prod": in_prod_cell(t, G)} for t in G["dev"]}
    json.dump(cells, open(HERE / "slack_links.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%d dev tickets have links, %d show in prod; slack_links.json written" % (
        sum(1 for c in cells.values() if c["Links"]), sum(1 for c in cells.values() if c["In prod"])))


def dev_row_cells(t, G):
    s, i = G["st"][t], G["dev"][t]
    return {"Item": "%s  %s" % (t, s["title"]), "ID": t, "Category": s["category"], "Status": SLACK_LABEL[s["effective_status"]],
            "Kind": s["kind"], "Evidence level": s["level"], "Closing criterion": s["criterion"], "Evidence": "\n".join(s["evidence"]),
            "Checks": "; ".join(("PASS " if c["ok"] else "FAIL ") + c["detail"] for c in s["checks"]), "Reproduce": s["reproduce"],
            "Reopen if": "; ".join(s["reopen_if"]), "Blocked by": s["blocked_by"] or "", "Due": i.get("due") or "",
            "Problems": "; ".join(s["problems"]), "Note": s["note"], "Links": links_cell(t, G), "In prod": in_prod_cell(t, G),
            "Verified": (G["status_utc"] or "")[:10]}


SYNCED = HERE / "synced"


def cmd_list_diff(a):
    """Cells that differ between the files and the last synced copy of a Slack list -> list_updates_<which>.json.
    Verified is sent only with another change. After pushing the updates: `trace.py list-synced <which>`."""
    G = build()
    which = a.which
    rows = {t: dev_row_cells(t, G) for t in G["dev"]} if which == "dev" else {p: prod_row_cells(p, G) for p in prod_order(G)}
    json.dump(list(rows.values()), open(HERE / ("%s_rows.json" % which), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    synced_f = SYNCED / ("%s.json" % which)
    old = json.load(open(synced_f, encoding="utf-8")) if synced_f.exists() else {}
    recs = G["mirrors"].get("lists", {}).get(LISTS[which], {})
    upd = {}
    for t, cells in rows.items():
        prev = old.get(t)
        if prev is None:
            upd[t] = {"record_id": recs.get(t), "cells": {k: v for k, v in cells.items() if v}}
            continue
        ch = {k: v for k, v in cells.items() if k != "Verified" and (prev.get(k) or "") != (v or "")}
        if ch:
            if "Verified" in cells:
                ch["Verified"] = cells["Verified"]
            upd[t] = {"record_id": recs.get(t), "cells": ch}
    gone = sorted(set(old) - set(rows))
    json.dump({"list": LISTS[which], "updates": upd, "rows_no_longer_in_files": gone},
              open(HERE / ("list_updates_%s.json" % which), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%s list: %d rows to update (%d new, need add_list_record), %d rows no longer in the files %s" % (
        which, len(upd), sum(1 for u in upd.values() if not u["record_id"]), len(gone), gone[:10]))


def cmd_list_synced(a):
    """Record that the Slack list now holds <which>_rows.json (run after pushing list_updates_<which>.json)."""
    rows = json.load(open(HERE / ("%s_rows.json" % a.which), encoding="utf-8"))
    SYNCED.mkdir(exist_ok=True)
    json.dump({r["ID"]: r for r in rows}, open(SYNCED / ("%s.json" % a.which), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("synced copy of the %s list updated (%d rows)" % (a.which, len(rows)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("check"); p.add_argument("--max-warn", type=int, default=25); p.set_defaults(f=cmd_check)
    p = sp.add_parser("show"); p.add_argument("id"); p.set_defaults(f=cmd_show)
    p = sp.add_parser("graph"); p.add_argument("id", nargs="?"); p.add_argument("--depth", type=int, default=1)
    p.add_argument("--mentions", action="store_true"); p.add_argument("--evidence", action="store_true"); p.set_defaults(f=cmd_graph)
    p = sp.add_parser("next-id"); p.add_argument("prefix"); p.set_defaults(f=cmd_next_id)
    p = sp.add_parser("link"); p.add_argument("src"); p.add_argument("rel"); p.add_argument("dst", nargs="+"); p.add_argument("--note", default=""); p.set_defaults(f=cmd_link)
    p = sp.add_parser("unlink"); p.add_argument("src"); p.add_argument("rel"); p.add_argument("dst"); p.set_defaults(f=cmd_unlink)
    p = sp.add_parser("prod-apply"); p.add_argument("spec"); p.set_defaults(f=cmd_prod_apply)
    p = sp.add_parser("prod-add"); p.add_argument("id"); g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--group", action="store_true"); g.add_argument("--passthrough", action="store_true")
    p.add_argument("--title"); p.add_argument("--curates", nargs="+"); p.add_argument("--category"); p.add_argument("--criterion"); p.set_defaults(f=cmd_prod_add)
    p = sp.add_parser("prod-rows"); p.set_defaults(f=cmd_prod_rows)
    p = sp.add_parser("prod-publish"); p.add_argument("ids", nargs="*"); p.add_argument("--note", required=True); p.set_defaults(f=cmd_prod_publish)
    p = sp.add_parser("prod-set"); p.add_argument("id"); p.add_argument("--published", choices=STATUSES, required=True)
    p.add_argument("--force", action="store_true"); p.add_argument("--note", default=""); p.set_defaults(f=cmd_prod_set)
    p = sp.add_parser("review"); p.add_argument("id"); p.add_argument("--note", required=True); p.set_defaults(f=cmd_review)
    p = sp.add_parser("retire"); p.add_argument("id"); p.add_argument("--note", required=True); p.set_defaults(f=cmd_retire)
    p = sp.add_parser("mirror"); p.add_argument("csv"); p.add_argument("--list", default="dev"); p.set_defaults(f=cmd_mirror)
    p = sp.add_parser("slack-links"); p.set_defaults(f=cmd_slack_links)
    p = sp.add_parser("list-diff"); p.add_argument("which", choices=("dev", "prod")); p.set_defaults(f=cmd_list_diff)
    p = sp.add_parser("list-synced"); p.add_argument("which", choices=("dev", "prod")); p.set_defaults(f=cmd_list_synced)
    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
