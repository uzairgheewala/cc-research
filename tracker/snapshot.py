"""One file that the site, both Slack lists and the digests agree on.

  python tracker/snapshot.py           write site/snapshot.json
  python tracker/snapshot.py --check   recompute and compare with the committed site/snapshot.json (exit 1 on drift)

Contents: every tracker item (status, evidence level, pillar), the bundles and milestones of the Q1 plan, the state of
both Slack lists (row files, their hashes, pending updates), and every number the site prints (site/registry.py) with
its source file and that file's sha256. `hash` is the sha256 of the canonical JSON of everything except `generated_utc`
and `hash` itself, so two machines that read the same files produce the same hash.
Read-only on everything except site/snapshot.json. No network.
"""
import argparse, datetime, hashlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(HERE), str(ROOT / "site")]
import catalogue as C  # noqa: E402
import pillars  # noqa: E402
from registry import REG  # noqa: E402

OUT = ROOT / "site" / "snapshot.json"


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def metrics():
    out, errors, cache = {}, [], {}
    for key, spec in sorted(REG.items()):
        src = spec["src"]
        try:
            if "literal" in spec:
                txt = (ROOT / src).read_text(encoding="utf-8")
                ctx = spec.get("context") or spec["literal"]
                if spec["literal"] not in ctx or not re.search(r"(?<![0-9.])" + re.escape(ctx) + r"(?![0-9])", txt):
                    raise ValueError("literal %r (in %r) not found" % (spec["literal"], ctx))
                val = spec["literal"]
                val = float(val) if re.fullmatch(r"-?[0-9.]+", val) else val
            else:
                if src not in cache:
                    cache[src] = load(src)
                d = cache[src]
                if "fn" in spec:
                    val = spec["fn"](d)
                else:
                    val = d
                    for k in spec["ptr"]:
                        val = val[k]
            out[key] = {"value": val, "src": src}
        except Exception as e:  # noqa: BLE001 - every failure is reported, none is fatal until the end
            errors.append("%s <- %s: %s" % (key, src, e))
    srcs = sorted({v["src"] for v in out.values()})
    return out, {s: sha_file(ROOT / s) for s in srcs}, errors


def items():
    st = load("tracker/status.json")
    rows = [{"id": i["id"], "category": i["category"], "title": i["title"], "kind": i.get("kind"),
             "status": i["effective_status"], "level": i.get("level"), "pillar": pillars.pillar(i["id"])}
            for i in st["items"]]
    return st["verified_utc"], rows


def bundles():
    dag = load("plans/q1_dag.json")
    audit = load("plans/audit_dag.json")
    out = []
    for plan, b in [("q1", b) for b in dag["bundles"]] + [("audit", b) for b in audit["bundles"]]:
        bid = b["id"]
        out.append({"id": bid, "title": b.get("title"), "status": C.BUNDLE_STATUS.get(bid) or "todo",
                    "blocked_by": b.get("depends_on") or b.get("blocked_by") or [], "closes": b.get("closes", []),
                    "window": b.get("window"), "llm_cost": b.get("llm_cost"), "approval_needed": b.get("approval_needed"),
                    "uzair_actions": b.get("uzair_actions") or [], "note": C.BUNDLE_NOTE.get(bid, ""), "plan": plan,
                    "track": b.get("track"), "serves": b.get("serves") or []})
    return out, dag.get("milestones", []) + audit.get("milestones", [])


def lists():
    out = {}
    for which in ("dev", "prod"):
        rows = ROOT / "tracker" / ("%s_rows.json" % which)
        upd = ROOT / "tracker" / ("list_updates_%s.json" % which)
        u = json.load(open(upd, encoding="utf-8")) if upd.exists() else {"updates": {}, "rows_no_longer_in_files": []}
        out[which] = {"slack_list": u.get("list"), "rows": len(json.load(open(rows, encoding="utf-8"))),
                      "rows_sha256": sha_file(rows), "pending_updates": len(u.get("updates", {})),
                      "pending_removals": len(u.get("rows_no_longer_in_files", []))}
    return out


def changes(limit=8):
    """The newest posted dev digests (tracker/relay_log.jsonl): when, the summary points, and what finished. Drafts and
    prod digests are left out; the prod channel's drafts are Uzair's to send."""
    f = ROOT / "tracker" / "relay_log.jsonl"
    if not f.exists():
        return []
    recs = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    recs = [r for r in recs if r.get("type") == "digest" and r.get("channel") == "dev" and not r.get("draft_only")]
    out = []
    for r in sorted(recs, key=lambda r: r.get("posted_utc") or "", reverse=True):
        if len(out) >= limit:
            break
        sec, points, done = None, [], []
        for line in (r.get("text") or "").splitlines():
            line = line.strip()
            if line.startswith("**"):
                mm = re.match(r"\*\*([^*]+)\*\*", line)
                sec = mm.group(1).strip().lower() if mm else None
                continue
            if line.startswith("•"):
                item = line.lstrip("•").strip()
                if sec == "summary":
                    points.append(item)
                elif sec == "done":
                    done.append(item.replace("✅", "").strip())
        if points:
            out.append({"posted_utc": r.get("posted_utc"), "points": points, "done": done, "tickets": r.get("tickets", [])})
    return out


def build():
    verified, its = items()
    bs, ms = bundles()
    m, srcs, errors = metrics()
    body = {"schema": 1, "status_verified_utc": verified, "items": its, "bundles": bs, "milestones": ms,
            "lists": lists(), "metrics": m, "sources": srcs, "changes": changes()}
    canon = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return body, hashlib.sha256(canon).hexdigest(), errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    body, h, errors = build()
    for e in errors:
        print("METRIC ERROR " + e)
    if a.check:
        old = json.load(open(OUT, encoding="utf-8")) if OUT.exists() else {}
        if old.get("hash") != h:
            print("snapshot drift: committed %s, recomputed %s. Run `python tracker/snapshot.py` and commit." % (
                (old.get("hash") or "none")[:12], h[:12]))
            sys.exit(1)
        print("snapshot ok %s" % h[:12])
        sys.exit(1 if errors else 0)
    snap = {"hash": h, "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **body}
    OUT.parent.mkdir(exist_ok=True)
    json.dump(snap, open(OUT, "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True, ensure_ascii=False)
    counts = {}
    for i in body["items"]:
        counts.setdefault(i["pillar"], [0, 0])
        counts[i["pillar"]][0] += 1
        counts[i["pillar"]][1] += i["status"] == "done"
    print("snapshot %s: %d items (%s), %d bundles, %d metrics, %d sources, %d errors" % (
        h[:12], len(body["items"]), ", ".join("%s %d/%d" % (k, v[1], v[0]) for k, v in sorted(counts.items())),
        len(body["bundles"]), len(body["metrics"]), len(body["sources"]), len(errors)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
