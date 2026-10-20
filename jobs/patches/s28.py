"""s28 (site v3, TEAM-12): the public feed shows posted prod digests only (#causal-discovery, a Slack ts recorded), with a count of dev digests posted since; the build fails if a dev digest reaches the snapshot. Edits tracker/snapshot.py, site/pgs/pg_changes.py, site/build.py. Independent of s24-s27."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARK = 'def changes_lag'


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8", newline="\n")


def replace_once(rel, old, new):
    t = read(rel)
    n = t.count(old)
    assert n == 1, "%s: anchor found %d times (expected once): %r" % (rel, n, old[:80])
    write(rel, t.replace(old, new, 1))


def new_file(rel, text):
    p = ROOT / rel
    assert not p.exists(), "%s already exists" % rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def require(rel, marker, why):
    assert marker in read(rel), why


assert MARK not in read('tracker/snapshot.py'), "already applied: %r found in %s" % (MARK, 'tracker/snapshot.py')

old_doc = '    """The newest posted dev digests (tracker/relay_log.jsonl): when, the summary points, and what finished. Drafts and\n    prod digests are left out; the prod channel\'s drafts are Uzair\'s to send."""\n'
replace_once("tracker/snapshot.py", old_doc,
             '    """s28 (TEAM-12): the newest prod digests posted in #causal-discovery (tracker/relay_log.jsonl: channel prod, a Slack\n'
             '    ts recorded, not a draft): when, the summary points, and what finished. Dev digests never reach the public site; the\n'
             '    count of dev digests posted since the last prod one is changes_lag()."""\n')
replace_once("tracker/snapshot.py",
             '    recs = [r for r in recs if r.get("type") == "digest" and r.get("channel") == "dev" and not r.get("draft_only")]\n',
             '    recs = [r for r in recs if r.get("type") == "digest" and r.get("channel") == "prod" and not r.get("draft_only") and r.get("ts")]\n')
replace_once("tracker/snapshot.py",
             '            if line.startswith("**"):\n                mm = re.match(r"\\*\\*([^*]+)\\*\\*", line)\n',
             '            if line.startswith("*"):\n                mm = re.match(r"\\*{1,2}([^*]+)\\*{1,2}", line)\n')
replace_once("tracker/snapshot.py",
             '            out.append({"posted_utc": r.get("posted_utc"), "points": points, "done": done, "tickets": r.get("tickets", [])})\n    return out\n',
             '            out.append({"posted_utc": r.get("posted_utc"), "points": points, "done": done, "tickets": r.get("tickets", []),\n'
             '                        "channel": "prod"})\n    return out\n\n\n'
             'def changes_lag():\n'
             '    """s28: how many dev digests were posted after the newest posted prod digest (a count only; no dev text)."""\n'
             '    f = ROOT / "tracker" / "relay_log.jsonl"\n'
             '    if not f.exists():\n'
             '        return {"dev_since_last_prod": 0, "last_prod_utc": None}\n'
             '    recs = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]\n'
             '    recs = [r for r in recs if r.get("type") == "digest" and not r.get("draft_only") and r.get("ts")]\n'
             '    last = max((r.get("posted_utc") or "" for r in recs if r.get("channel") == "prod"), default="")\n'
             '    n = sum(1 for r in recs if r.get("channel") == "dev" and (r.get("posted_utc") or "") > last)\n'
             '    return {"dev_since_last_prod": n, "last_prod_utc": last or None}\n')
replace_once("tracker/snapshot.py", '"changes": changes()}', '"changes": changes(), "changes_lag": changes_lag()}')
replace_once("site/pgs/pg_changes.py",
             '    P("Each block is one digest the team posted, with its summary points and what it finished. Ticket IDs (AUD-45, RQ-10 …) "\n      "match the Slack lists and the status page."),\n',
             '    P("Each block is one digest the team posted in its public channel, with its summary points and what it finished. Ticket "\n'
             '      "IDs (AUD-45, RQ-10 …) match the Slack lists and the status page. Working notes stay in the team\'s own channel; "\n'
             '      + ("%d of them have been posted since the newest block below." % (SNAP.get("changes_lag") or {}).get("dev_since_last_prod", 0)\n'
             '         if (SNAP.get("changes_lag") or {}).get("dev_since_last_prod") else "none are newer than the newest block below.")),\n')
replace_once("site/build.py", "    if any(k not in common.SNAP[\"metrics\"] for k in common.USED):\n",
             "    # s28 (TEAM-12): the public feed carries posted prod digests only\n"
             "    for _c in common.SNAP.get(\"changes\") or []:\n"
             "        if _c.get(\"channel\") != \"prod\":\n"
             "            errors.append(\"changes: a %s digest (%s) is in the public feed; only posted prod digests may be\" % (_c.get(\"channel\"), _c.get(\"posted_utc\")))\n"
             "    if any(k not in common.SNAP[\"metrics\"] for k in common.USED):\n")

print("s28 applied")
