"""relay.py - prepare, record and check the messages that carry milestones, summaries and artifacts to Slack (RELAY.md).

Nothing here talks to Slack. `prepare` commands write a message to relay_out/ (JSON + the text); an agent or Uzair posts it
(dev: posted directly; prod: created as a Slack draft that Uzair sends); `record` then logs where it landed and links every
ticket in it to that message. `check` (also run by `trace.py check`) reports stale artifacts, owed corrections and overdue digests.

  python tracker/relay.py digest --channel dev|prod [--point "text naming IDs" ...]
  python tracker/relay.py milestones --channel dev|prod
  python tracker/relay.py artifact PATH --tickets ID [ID ...] --summary TEXT --channel dev|prod
  python tracker/relay.py record relay_out/<file>.json --ts 1791580546.004809 [--draft] [--file-id F...] [--thread TS]
  python tracker/relay.py check
"""
import argparse, collections, datetime, hashlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
LOG = HERE / "relay_log.jsonl"
OUT = HERE / "relay_out"
CHANNELS = {"dev": "C0C7Q2CA2G7", "prod": "C0C8CQK1XME"}
CADENCE_DAYS = {"dev": 8, "prod": 8}          # a digest at least weekly once the first one is posted
PREPARED_GRACE_DAYS = 2
ICON = {"done": "✅", "done_needs_evidence": "✅", "in_progress": "👀", "reopened": "👀", "todo": "⏳", "blocked": "🔴", "open": "🔵", None: "·"}


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def iso(t=None):
    return (t or now()).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def log():
    return [json.loads(l) for l in open(LOG, encoding="utf-8") if l.strip()] if LOG.exists() else []


# ----------------------------------------------------------------------------- views of the tracker per channel
def scope(G, channel):
    """{id: (status shown, title)} for what this channel's readers see: every dev ticket (dev), or every prod row (prod)."""
    import trace as T
    if channel == "dev":
        return {t: (G["deveff"](t), G["dev"][t]["title"]) for t in G["dev"]}
    return {p: (T.PUBLISH[G["derived"][p]], T.title_of(p, G) or G["dev"].get(p, {}).get("title", "")) for p in G["prod"]}


def baseline(channel):
    for r in reversed(log()):
        if r["channel"] == channel and r.get("snapshot") is not None and not r.get("draft_only"):
            return r
    return None


def due_soon(G, channel, days=14):
    import trace as T
    today = now().date(); out = []
    ids = G["dev"] if channel == "dev" else [p for p in G["prod"] if p in G["dev"]]
    for t in ids:
        d = G["dev"][t].get("due")
        if d and G["deveff"](t) not in ("done",):
            dd = datetime.date.fromisoformat(d)
            if 0 <= (dd - today).days <= days:
                out.append((d, t))
    return sorted(out)


def roll_up_line(t, G):
    """Where a dev ticket shows up for prod readers: the group or deliverable it feeds."""
    import trace as T
    homes = [p for p, cur in G["curated"].items() if t in cur and p != t]
    parents = [e["src"] for e in G["inn"][t] if e["rel"] == "parent_of"]
    bits = []
    for p in homes:
        cur = G["curated"][p]; k = sum(1 for x in cur if G["deveff"](x) == "done")
        bits.append("%s %s (%d of %d done)" % (p, G["prod"][p]["title"], k, len(cur)))
    bits += ["%s %s" % (p, G["dev"][p]["title"][:60]) for p in parents]
    return "; ".join(bits)


def write_prepared(kind, channel, text, tickets, G, snapshot=None, artifacts=()):
    OUT.mkdir(exist_ok=True)
    stamp = now().strftime("%Y%m%dT%H%M%SZ")
    rec = {"type": kind, "channel": channel, "channel_id": CHANNELS[channel], "prepared_utc": iso(), "tickets": sorted(set(tickets)),
           "artifacts": list(artifacts), "snapshot": snapshot, "text": text, "text_sha": hashlib.sha256(text.encode()).hexdigest()[:16]}
    base = OUT / ("%s_%s_%s" % (stamp, kind, channel))
    json.dump(rec, open(str(base) + ".json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(str(base) + ".md", "w", encoding="utf-8").write(text + "\n")
    print(text)
    f = base.relative_to(RESEARCH).as_posix() + ".json"
    if channel == "dev":
        print("\n-> prepared %s\n   post it in #cd-tracker, then: python tracker/relay.py record %s --ts <message ts>" % (f, f))
    else:
        print("\n-> prepared %s\n   create it as a Slack draft in #causal-discovery, then: python tracker/relay.py record %s --draft\n"
              "   after Uzair sends it: python tracker/relay.py record %s --ts <message ts>" % (f, f, f))
    return base


def check_ids_for_channel(ids, channel, G):
    bad = [t for t in ids if t not in G["dev"] and t not in G["prod"]]
    if channel == "prod":
        bad += [t for t in ids if t in G["dev"] and t not in G["prod"]]
    return bad


# Messages go out through the Slack connector, which takes standard markdown: **bold** (a single *x* renders italic).
def short(text, n):
    """Cut a title at a word boundary with an ellipsis, never mid-word (Slack messages are read by people)."""
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0].rstrip(" ,;:(/")
    return cut + "…"


def ts_utc(ts):
    """A Slack message ts is epoch seconds: the time the message was actually sent (a later recording must not move it)."""
    import datetime as _dt
    return _dt.datetime.fromtimestamp(float(ts), _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ----------------------------------------------------------------------------- prepare
def cmd_digest(a, G):
    import trace as T
    cur = scope(G, a.channel)
    b = baseline(a.channel)
    prev = (b or {}).get("snapshot") or {}
    since = b["posted_utc"][:10] if b else None
    pts, ids = [], []
    for p in a.point or []:
        found = T.MENTION_RE.findall(p)
        bad = check_ids_for_channel(found, a.channel, G)
        if not found or bad:
            sys.exit("refused point %r: it must name at least one %s ID%s" % (
                p, "prod row" if a.channel == "prod" else "ticket", " (not valid here: %s)" % bad if bad else ""))
        pts.append(p); ids += found
    newly = lambda pred: [t for t in cur if pred(cur[t][0]) and not pred(prev.get(t))] if b else []
    done = newly(lambda s: s == "done")
    started = newly(lambda s: s == "in_progress")
    blocked = newly(lambda s: s == "blocked")
    reopened = [t for t in cur if b and prev.get(t) == "done" and cur[t][0] != "done"]
    added = [t for t in cur if b and t not in prev]
    tot = collections.Counter(s for s, _ in cur.values())
    where = "#cd-tracker (dev, %d tickets)" % len(cur) if a.channel == "dev" else "CD Tracker (%d rows)" % len(cur)
    L = ["**Digest %s UTC** · %s · %s" % (iso()[:10], where, "since %s" % since if since else "first digest, no earlier baseline")]
    if pts:
        L += ["", "**Summary**"] + ["• " + p for p in pts]
    for head, lst in (("Done", done), ("Reopened", reopened), ("Started", started), ("Newly blocked", blocked), ("New", added)):
        if lst:
            L += ["", "**%s** (%d)" % (head, len(lst))] + ["• %s %s %s" % (ICON[cur[t][0]], t, short(cur[t][1], 90)) for t in sorted(lst)]
    ds = due_soon(G, a.channel)
    if ds:
        L += ["", "**Due in the next 14 days**"] + ["• %s %s %s" % (d, t, short(G["dev"][t]["title"], 80)) for d, t in ds]
    L += ["", "Totals: ✅ %d%s · 👀 %d · ⏳ %d · 🔴 %d · 🔵 %d" % (
        tot["done"] + tot["done_needs_evidence"], " (%d need evidence)" % tot["done_needs_evidence"] if tot["done_needs_evidence"] else "",
        tot["in_progress"] + tot["reopened"], tot["todo"], tot["blocked"], tot["open"])]
    snap = {t: s for t, (s, _) in cur.items()}
    write_prepared("digest", a.channel, "\n".join(L), ids + done + reopened + started + blocked, G, snapshot=snap)


def cmd_milestones(a, G):
    cur = scope(G, a.channel)
    b = baseline(a.channel)
    if not b:
        sys.exit("no baseline for %s yet: post a digest first (it records what everyone has already seen)" % a.channel)
    prev = b["snapshot"]
    new_done = sorted(t for t in cur if cur[t][0] == "done" and prev.get(t) != "done")
    reopened = sorted(t for t in cur if prev.get(t) == "done" and cur[t][0] != "done")
    if not new_done and not reopened:
        print("no milestones since %s" % b["posted_utc"]); return
    L = []
    for t in new_done:
        if a.channel == "dev":
            s = G["st"][t]
            L += ["✅ *%s %s* (%s)" % (t, s["title"], s["level"]),
                  "• Closed by: %s" % (s["criterion"] or "-"),
                  "• Checks: %s" % ("; ".join(("PASS " if c["ok"] else "FAIL ") + c["detail"] for c in s["checks"]) or "-"),
                  "• Evidence: %s" % (", ".join("`%s`" % e for e in s["evidence"]) or "-")]
            r = roll_up_line(t, G)
            if r:
                L.append("• Feeds: " + r)
        else:
            v = G["prod_view"][t]
            L += ["✅ *%s %s* is done (evidence level %s)." % (t, cur[t][1], v["min_level"])]
            if v["type"] == "group":
                L.append("• All %d tickets closed: %s" % (len(v["curates"]), ", ".join(v["curates"])))
            else:
                L.append("• " + (G["st"][t]["criterion"] or G["dev"][t]["title"]))
        L.append("")
    for t in reopened:
        L += ["👀 *%s %s* was reopened: its evidence changed or a check now fails. Shown as in progress until re-verified." % (t, cur[t][1]), ""]
    snap = {t: s for t, (s, _) in cur.items()}
    write_prepared("milestone", a.channel, "\n".join(L).rstrip(), new_done + reopened, G, snapshot=snap)


def cmd_artifact(a, G):
    p = (RESEARCH / a.path).resolve()
    if not p.is_file() or RESEARCH not in p.parents:
        sys.exit("artifact must be a file inside cc-research")
    if p.name == ".env" or "Causal-Copilot" in p.parts:
        sys.exit("refused: never relay credentials or upstream files")
    bad = check_ids_for_channel(a.tickets, a.channel, G)
    if bad:
        sys.exit("refused: not valid %s IDs: %s" % (a.channel, bad))
    rel = p.relative_to(RESEARCH).as_posix(); h = sha(p)
    text = "**Artifact** `%s` (sha256 %s…) for %s\n%s" % (rel, h[:12], ", ".join(a.tickets), a.summary)
    write_prepared("artifact", a.channel, text, a.tickets, G, artifacts=[{"path": rel, "sha256": h}])


# ----------------------------------------------------------------------------- record
def cmd_record(a, G):
    import trace as T
    rec = json.load(open(RESEARCH / a.prepared if not Path(a.prepared).is_absolute() else a.prepared, encoding="utf-8"))
    if not a.draft and any(r.get("prepared_file") == str(a.prepared) for r in log() if not r.get("draft_only")):
        sys.exit("already recorded")
    if not a.draft and not re.match(r"^\d+\.\d+$", a.ts or ""):
        sys.exit("--ts must be the Slack message ts (e.g. 1791580546.004809); use --draft for a draft not yet sent")
    rec.update(prepared_file=str(a.prepared), ts=a.ts, thread_ts=a.thread, posted_utc=ts_utc(a.ts) if a.ts else iso(), recorded_utc=iso(), file_ids=a.file_id or [], draft_only=bool(a.draft))
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if not a.draft:
        ref = "slack:%s/%s" % (rec["channel_id"], a.ts)
        T.append_links([(t, "published_at", ref, rec["type"]) for t in rec["tickets"] if t in G["dev"] or t in G["prod"]])
    print("recorded %s in %s at %s%s; %d tickets linked" % (rec["type"], rec["channel"], a.ts or "-", " (draft only)" if a.draft else "",
                                                          0 if a.draft else len(rec["tickets"])))


# ----------------------------------------------------------------------------- checks (also called by trace.py check)
def findings(G):
    out = []
    entries = [r for r in log() if not r.get("draft_only")]
    for r in entries:
        for art in r.get("artifacts", []):
            p = RESEARCH / art["path"]
            if not p.exists():
                out.append(("WARN", "R1", "artifact %s relayed to %s at %s no longer exists" % (art["path"], r["channel"], r["ts"])))
            elif sha(p) != art["sha256"]:
                out.append(("WARN", "R1", "artifact %s changed since it was relayed to %s at %s: the Slack copy is stale" % (art["path"], r["channel"], r["ts"])))
    latest_claim = {}
    for r in entries:
        if r["type"] in ("milestone", "digest"):
            for t, s in (r.get("snapshot") or {}).items():
                latest_claim[(r["channel"], t)] = (s, r)
    for (ch, t), (s, r) in latest_claim.items():
        cur = G["deveff"](t) if ch == "dev" else (__import__("trace").PUBLISH.get(G["derived"].get(t)) if t in G["prod"] else None)
        if s == "done" and cur not in ("done", None) and t in (r.get("tickets") or []):
            out.append(("WARN", "R2", "%s was announced done in %s (%s) and is now %s: post a correction" % (t, ch, r["ts"], cur)))
    posted = {r.get("prepared_file") for r in entries}
    drafted = {r.get("prepared_file") for r in log() if r.get("draft_only")}
    for f in sorted(OUT.glob("*.json")) if OUT.exists() else []:
        relp = f.relative_to(RESEARCH).as_posix()
        if relp not in posted and (now() - datetime.datetime.fromtimestamp(f.stat().st_mtime, datetime.timezone.utc)).days >= PREPARED_GRACE_DAYS:
            out.append(("WARN", "R3", "%s %s (send and record it, or move it to relay_out/discarded/)" % (
                relp, "is a draft that was never sent" if relp in drafted else "was prepared but never posted and recorded")))
    for ch, days in CADENCE_DAYS.items():
        ds = [r for r in entries if r["channel"] == ch and r["type"] == "digest"]
        if ds and (now() - parse(ds[-1]["posted_utc"])).days >= days:
            out.append(("WARN", "R5", "last %s digest was %s; one is due" % (ch, ds[-1]["posted_utc"][:10])))
    return out


def cmd_check(a, G):
    f = findings(G)
    for x in f:
        print("  %s %s %s" % x)
    print("%d relay findings" % len(f))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("digest"); p.add_argument("--channel", choices=CHANNELS, required=True); p.add_argument("--point", action="append"); p.set_defaults(f=cmd_digest)
    p = sp.add_parser("milestones"); p.add_argument("--channel", choices=CHANNELS, required=True); p.set_defaults(f=cmd_milestones)
    p = sp.add_parser("artifact"); p.add_argument("path"); p.add_argument("--tickets", nargs="+", required=True); p.add_argument("--summary", required=True)
    p.add_argument("--channel", choices=CHANNELS, required=True); p.set_defaults(f=cmd_artifact)
    p = sp.add_parser("record"); p.add_argument("prepared"); p.add_argument("--ts"); p.add_argument("--draft", action="store_true")
    p.add_argument("--file-id", nargs="*"); p.add_argument("--thread"); p.set_defaults(f=cmd_record)
    p = sp.add_parser("check"); p.set_defaults(f=cmd_check)
    a = ap.parse_args()
    import trace as T
    G = T.build()
    a.f(a, G)


if __name__ == "__main__":
    main()
