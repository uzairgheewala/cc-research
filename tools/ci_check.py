"""Checks CI runs on every push. Read-only.

  python tools/ci_check.py

1. Evidence pins: every pin in tracker/pins.json for evidence the item still lists is classified and checked.
   - in the repo: its digest is recomputed (tracker/verify.py's own digest) and must equal the pin, unless the
     tracker already reports that item as reopened (the drift is then known and shown, not hidden);
   - under an excluded root (external/, runs/, jobs/transfer/): must be listed in manifests/excluded/*.sha256;
   - repo: (the Causal-Copilot tree) and pointers (project:, chat:, slack:, url:) are counted, not checked here.
2. The tracker's own consistency: no done item below its required evidence level in tracker/status.json.
Exit 1 on any error. The checkout directory must be named cc-research (pins of file sets include that prefix).
"""
import fnmatch, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tracker"))
import verify  # noqa: E402

EXCLUDED = ("external/", "runs/", "jobs/transfer/", "queue/")
POINTERS = ("project:", "chat:", "slack:", "url:")


def excluded_listing():
    paths = set()
    for f in (ROOT / "manifests" / "excluded").glob("*.sha256"):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                paths.add(line.rstrip("\n").split("  ", 1)[1])
    return paths


def main():
    if ROOT.name != "cc-research":
        print("ci_check: the checkout folder must be named cc-research (it is %r)" % ROOT.name)
        sys.exit(1)
    pins = json.load(open(ROOT / "tracker" / "pins.json", encoding="utf-8"))
    status = {i["id"]: i for i in json.load(open(ROOT / "tracker" / "status.json", encoding="utf-8"))["items"]}
    listed = excluded_listing()
    current = {(i["id"], e) for i in status.values() for e in i.get("evidence", [])}
    counts = {"in_repo_ok": 0, "drift_known": 0, "excluded_listed": 0, "upstream": 0, "pointer": 0, "stale_pin": 0}
    errors, notes = [], []
    for key, pin in sorted(pins.items()):
        iid, ev = key.split("|", 1)
        raw = ev.split(" (")[0].strip()
        if (iid, ev) not in current:          # evidence no longer listed for the item: an old pin, not checked
            counts["stale_pin"] += 1
            continue
        if raw.startswith(POINTERS):
            counts["pointer"] += 1
            continue
        if raw.startswith("repo:"):
            counts["upstream"] += 1
            continue
        if raw.startswith(EXCLUDED):
            pat = raw.rstrip("/")
            hit = any(p == pat or p.startswith(pat + "/") or fnmatch.fnmatch(p, pat) for p in listed)
            if hit:
                counts["excluded_listed"] += 1
            elif not listed:
                notes.append("%s: %s is outside git and manifests/excluded/ is empty (run tools/data_manifest.py)" % (iid, raw))
            else:
                errors.append("%s: %s is outside git and not listed in manifests/excluded/" % (iid, raw))
            continue
        digest, nfiles = verify.digest(ev)
        if digest is None:
            errors.append("%s: evidence %s is missing from the repo" % (iid, raw))
        elif digest != pin["digest"]:
            if status.get(iid, {}).get("effective_status") == "reopened":
                counts["drift_known"] += 1
                notes.append("%s: %s changed since its pin; the tracker already shows the item as reopened" % (iid, raw))
            else:
                errors.append("%s: %s changed since it was pinned %s (repin with tracker/verify.py --repin %s after review)" % (
                    iid, raw, pin.get("pinned", "?"), iid))
        else:
            counts["in_repo_ok"] += 1
    for iid, it in status.items():
        if it.get("status") == "done" and it.get("effective_status") != "done" and it.get("effective_status") != "reopened":
            errors.append("%s: marked done but effective status is %s" % (iid, it.get("effective_status")))
    for n in notes:
        print("NOTE  " + n)
    for e in errors:
        print("ERROR " + e)
    print("ci_check: %s; %d errors" % (", ".join("%s %d" % kv for kv in counts.items()), len(errors)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
