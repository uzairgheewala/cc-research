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


def _md_table(text, heading):
    """s24: the first markdown table after the first line that starts with heading, as a list of dicts keyed by the header
    row (cells stripped; the separator row dropped). Fails when the heading or the table is missing."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith(heading)), None)
    if start is None:
        raise ValueError("heading %r not found" % heading)
    rows, header = [], None
    for l in lines[start + 1:]:
        if l.startswith("#"):
            break
        if not l.startswith("|"):
            if header is not None:
                break
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if header is None:
            header = cells
        elif all(set(c) <= set("-: ") for c in cells):
            continue
        else:
            rows.append(dict(zip(header, cells)))
    if not rows:
        raise ValueError("no table after %r" % heading)
    return rows


def metrics():
    out, errors, cache = {}, [], {}
    for key, spec in sorted(REG.items()):
        src = spec["src"]
        try:
            if "mdtable" in spec:
                val = _md_table((ROOT / src).read_text(encoding="utf-8"), spec["mdtable"])
            elif "literal" in spec:
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
             "status": i["effective_status"], "level": i.get("level"), "pillar": pillars.pillar(i["id"]),
             # S23: what the site's re-read detector compares (status alone missed research that moves as evidence)
             "evidence_n": len(i.get("evidence") or []),
             "note_sha": hashlib.sha256((i.get("note") or "").encode("utf-8")).hexdigest()[:12]}
            for i in st["items"]]
    return st["verified_utc"], rows


def bundles():
    dag = load("plans/q1_dag.json")
    audit = load("plans/audit_dag.json")
    q2 = load("plans/q2_dag.json")
    out = []
    for plan, b in [("q1", b) for b in dag["bundles"]] + [("audit", b) for b in audit["bundles"]] + [("q2", b) for b in q2["bundles"]]:
        bid = b["id"]
        out.append({"id": bid, "title": b.get("title"), "status": C.BUNDLE_STATUS.get(bid) or "todo",
                    "blocked_by": b.get("depends_on") or b.get("blocked_by") or [], "closes": b.get("closes", []),
                    "window": b.get("window"), "llm_cost": b.get("llm_cost"), "approval_needed": b.get("approval_needed"),
                    "uzair_actions": b.get("uzair_actions") or [], "note": C.BUNDLE_NOTE.get(bid, ""), "plan": plan,
                    "track": b.get("track"), "serves": b.get("serves") or []})
    return out, dag.get("milestones", []) + audit.get("milestones", []) + q2.get("milestones", [])


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
    """s28 (TEAM-12): the newest prod digests posted in #causal-discovery (tracker/relay_log.jsonl: channel prod, a Slack
    ts recorded, not a draft): when, the summary points, and what finished. Dev digests never reach the public site; the
    count of dev digests posted since the last prod one is changes_lag()."""
    f = ROOT / "tracker" / "relay_log.jsonl"
    if not f.exists():
        return []
    recs = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    recs = [r for r in recs if r.get("type") == "digest" and r.get("channel") == "prod" and not r.get("draft_only") and r.get("ts")]
    out = []
    for r in sorted(recs, key=lambda r: r.get("posted_utc") or "", reverse=True):
        if len(out) >= limit:
            break
        sec, points, done = None, [], []
        for line in (r.get("text") or "").splitlines():
            line = line.strip()
            if line.startswith("*"):
                mm = re.match(r"\*{1,2}([^*]+)\*{1,2}", line)
                sec = mm.group(1).strip().lower() if mm else None
                continue
            if line.startswith("•"):
                item = line.lstrip("•").strip()
                if sec == "summary":
                    points.append(item)
                elif sec == "done":
                    done.append(item.replace("✅", "").strip())
        if points:
            out.append({"posted_utc": r.get("posted_utc"), "points": points, "done": done, "tickets": r.get("tickets", []),
                        "channel": "prod"})
    return out


def changes_lag():
    """s28: how many dev digests were posted after the newest posted prod digest (a count only; no dev text)."""
    f = ROOT / "tracker" / "relay_log.jsonl"
    if not f.exists():
        return {"dev_since_last_prod": 0, "last_prod_utc": None}
    recs = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    recs = [r for r in recs if r.get("type") == "digest" and not r.get("draft_only") and r.get("ts")]
    last = max((r.get("posted_utc") or "" for r in recs if r.get("channel") == "prod"), default="")
    n = sum(1 for r in recs if r.get("channel") == "dev" and (r.get("posted_utc") or "") > last)
    return {"dev_since_last_prod": n, "last_prod_utc": last or None}


def build():
    verified, its = items()
    bs, ms = bundles()
    m, srcs, errors = metrics()
    body = {"schema": 1, "status_verified_utc": verified, "items": its, "bundles": bs, "milestones": ms,
            "lists": lists(), "metrics": m, "sources": srcs, "changes": changes(), "changes_lag": changes_lag()}
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
