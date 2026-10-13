"""Self-test for trace.py: builds a throwaway copy of tracker/ outside cc-research (other folders are symlinked, read-only use),
injects one failure of each kind and checks that `trace.py` reports it with the right code. Writes tracker/selftest_trace.json.

  python tracker/selftest_trace.py
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
results = []


def sandbox():
    root = Path(tempfile.mkdtemp(prefix="trace_selftest_"))
    (root / "cc-research").mkdir()
    os.symlink(RESEARCH.parent / "Causal-Copilot", root / "Causal-Copilot")
    for p in RESEARCH.iterdir():
        if p.name == "tracker":
            shutil.copytree(p, root / "cc-research" / "tracker", ignore=shutil.ignore_patterns("__pycache__"), copy_function=shutil.copy2)
        else:
            os.symlink(p, root / "cc-research" / p.name)
    return root / "cc-research"


def run(cwd, *args):
    p = subprocess.run([sys.executable, "tracker/trace.py", *args], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


SELF_REF = None


BASELINE_ERRORS = set()


def clean(out):
    """True if every ERROR line in a check output was already present in the baseline copy, or names only tickets whose
    evidence is selftest_trace.json itself. The self-test checks the checker; the live tracker's own errors are reported
    by `trace.py check`, not here, so each case asserts only the errors it introduced."""
    global SELF_REF
    if SELF_REF is None:
        sys.path.insert(0, str(HERE)); import catalogue as C
        SELF_REF = {i["id"] for i in C.ITEMS if any("selftest_trace.json" in e for e in i["evidence"])}
    for line in out.splitlines():
        if line.strip().startswith("ERROR") and line.strip() not in BASELINE_ERRORS:
            ids = set(re.findall(r"[A-Z]{2,4}-\d{2,3}", line))
            if not ids or not ids <= SELF_REF:
                return False
    return True


def expect(name, cond, out):
    results.append({"case": name, "ok": bool(cond), **({} if cond else {"output": out[-600:]})})   # deterministic when all pass
    print(("PASS " if cond else "FAIL ") + name)


def add(cwd, line):
    with open(cwd / "tracker" / "links.txt", "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def main():
    cwd = sandbox()
    T = cwd / "tracker"
    rc, out = run(cwd, "check")
    BASELINE_ERRORS.update(l.strip() for l in out.splitlines() if l.strip().startswith("ERROR"))
    expect("baseline check runs and reports its own errors", "errors" in out, out)

    rc, out = run(cwd, "link", "REP-01", "blocks", "REP-99"); expect("link CLI refuses an unknown ticket", rc != 0 and "unknown dev ticket" in out, out)
    rc, out = run(cwd, "link", "REP-01", "curates", "REP-02"); expect("link CLI refuses a mistyped relation", rc != 0 and "not allowed" in out, out)
    rc, out = run(cwd, "link", "REP-01", "relates", "REP-02"); expect("relates needs a note", rc != 0 and "needs --note" in out, out)

    add(cwd, "REP-01 blocks REP-99"); rc, out = run(cwd, "check"); expect("T1 dangling link in links.txt", rc == 1 and "T1" in out and "REP-99" in out, out)
    shutil.copy2(HERE / "links.txt", T / "links.txt")
    add(cwd, "REP-01 fixes REP-02"); rc, out = run(cwd, "check"); expect("T2 unknown relation", rc == 1 and "T2" in out and "fixes" in out, out)
    shutil.copy2(HERE / "links.txt", T / "links.txt")
    add(cwd, "REP-01 blocks REP-02"); add(cwd, "REP-02 blocks REP-01")
    rc, out = run(cwd, "check"); expect("T3 cycle in blocks", rc == 1 and "T3" in out, out)
    shutil.copy2(HERE / "links.txt", T / "links.txt")
    add(cwd, "DEC-02 blocks REP-01"); rc, out = run(cwd, "check")
    expect("W3 done ticket blocked by an unfinished one", clean(out) and "W3 REP-01 is done while blocked by unfinished ['DEC-02']" in out, out)
    shutil.copy2(HERE / "links.txt", T / "links.txt")

    add(cwd, "REP-01 parent_of REP-03"); add(cwd, "REP-02 parent_of REP-03")
    rc, out = run(cwd, "check"); expect("T8 two parents", rc == 1 and "T8" in out, out); expect("W4 done parent, unfinished child", "W4" in out, out)
    shutil.copy2(HERE / "links.txt", T / "links.txt")

    # prod rows: groups in the existing encoding, pass-through rows, derived status, overclaim gates
    rc, out = run(cwd, "prod-apply", "tracker/prod_spec.json"); expect("prod-apply is idempotent", rc == 0 and "added 0 rows" in out, out)
    rc, nid = run(cwd, "next-id", "REP"); nid = nid.strip()
    expect("next-id skips IDs held by prod groups", nid not in ("REP-14", "REP-15") and int(nid.split("-")[1]) >= 16, nid)
    rc, out = run(cwd, "prod-add", nid, "--group", "--title", "selftest group", "--curates", "REP-01", "REP-03")
    expect("group status derived from a done and an in-progress ticket", rc == 0 and "derived status in_progress" in out, out)
    rc, out = run(cwd, "prod-set", nid, "--published", "done"); expect("prod-set refuses ✅ when dev is not done", rc != 0 and "refused" in out, out)
    rc, out = run(cwd, "prod-set", nid, "--published", "done", "--force", "--note", "selftest")
    rc, out = run(cwd, "check"); expect("T6 forced prod overclaim is an error", rc == 1 and "T6 %s" % nid in out, out)
    rc, out = run(cwd, "prod-add", "REP-14", "--group", "--title", "again", "--curates", "REP-01"); expect("group IDs are never reused", rc != 0, out)
    rc, out = run(cwd, "prod-add", "CAP-99", "--passthrough"); expect("pass-through rows must be dev tickets", rc != 0, out)
    rc, out = run(cwd, "prod-add", nid[:4] + "99", "--group", "--title", "x", "--curates", "XYZ-1"); expect("groups refuse non-dev sources", rc != 0, out)
    shutil.copy2(HERE / "prod.json", T / "prod.json"); shutil.copy2(HERE / "links.txt", T / "links.txt")
    rc, out = run(cwd, "check"); expect("T4 removing the selftest group without retiring it", rc == 1 and "T4 %s" % nid in out, out)
    run(cwd, "retire", nid, "--note", "selftest group removed")
    rc, out = run(cwd, "prod-publish", "--note", "selftest"); expect("prod-publish records every row", rc == 0 and "published" in out, out)
    rc, out = run(cwd, "check"); expect("published list is consistent", clean(out), out)
    rc, out = run(cwd, "prod-rows"); rows = json.load(open(T / "prod_rows.json", encoding="utf-8"))
    g = [r for r in rows if r["ID"] == "AUD-16"]
    expect("prod-rows: one row per prod row, groups list their tickets", len(rows) == len(json.load(open(T / "prod.json"))) and g
           and "AUD-09" in g[0]["Evidence"] and g[0]["Kind"] == "group", out)

    # a dev ticket regresses under a published ✅ group
    st0 = (T / "status.json").read_text(encoding="utf-8")
    st = json.loads(st0)
    for r in st["items"]:
        if r["id"] == "AUD-03":
            r["effective_status"] = "reopened"
        if r["id"] == "REP-02":
            r["level"] = "V4"
    json.dump(st, open(T / "status.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    rc, out = run(cwd, "check", "--max-warn", "99")
    expect("T6 group shown ✅ after a dev ticket reopened", rc == 1 and "T6 AUD-16" in out, out)
    expect("W1 group suspect after its dev ticket changed", "W1 REP-14" in out, out)
    run(cwd, "review", "REP-14", "--note", "selftest re-read")
    rc, out = run(cwd, "check", "--max-warn", "99"); expect("review clears W1", "W1 REP-14" not in out, out)
    (T / "status.json").write_text(st0, encoding="utf-8")

    # a dev ticket may not take an ID issued to a prod group
    cat = (T / "catalogue.py").read_text(encoding="utf-8")
    (T / "catalogue.py").write_text(cat.replace("ITEMS = [\n", 'ITEMS = [\nitem("REP-14", "REP", "clash", "todo"),\n', 1), encoding="utf-8")
    rc, out = run(cwd, "check"); expect("T7/T4 dev ticket reusing a group ID", rc == 1 and "group REP-14 is also a dev ticket" in out, out)
    (T / "catalogue.py").write_text(cat, encoding="utf-8")

    # relay: summaries must cite tickets; records link messages; stale artifacts and owed corrections are caught
    rr = lambda *a: subprocess.run([sys.executable, "tracker/relay.py", *a], cwd=cwd, capture_output=True, text=True)
    p = rr("digest", "--channel", "prod", "--point", "no ticket here"); expect("relay refuses a summary point without an ID", p.returncode != 0, p.stdout + p.stderr)
    p = rr("digest", "--channel", "prod", "--point", "INF-01 is done"); expect("relay refuses dev-only IDs in prod", p.returncode != 0, p.stdout + p.stderr)
    p = rr("digest", "--channel", "dev", "--point", "Correlation layer in place (BLD-11)")
    f = re.search(r"tracker/relay_out/\S+_digest_dev\.json", p.stdout).group(0)
    p = rr("record", f, "--ts", "1791580000.000001"); expect("relay record links tickets to the message", p.returncode == 0 and
                                                          "BLD-11 published_at slack:C0C7Q2CA2G7/1791580000.000001" in (T / "links.txt").read_text(encoding="utf-8"), p.stdout + p.stderr)
    st = json.loads(st0)
    # The fixture ticket is chosen from the live data (a not-done ticket, curated into a prod group, written as a plain
    # item(...) line), so the case keeps testing "newly done" as real tickets close (REP-06 itself closed on 10 Oct).
    notdone = {r["id"] for r in st["items"] if r["status"] != "done"}
    pairs = [l.split()[::2] for l in (T / "links.txt").read_text(encoding="utf-8").splitlines() if " curates " in l]
    MT, MG = next((t, g) for g, t in pairs if t in notdone
                  and re.search(r'item\("%s", "[A-Z]+", "[^"]*", "(todo|in_progress|open)"' % re.escape(t), cat))
    for r in st["items"]:
        if r["id"] == MT:
            r["effective_status"] = "done"; r["status"] = "done"
    json.dump(st, open(T / "status.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    cat2 = re.sub(r'(item\("%s", "[A-Z]+", "[^"]*", )"(todo|in_progress|open)"' % re.escape(MT), r'\1"done"', cat)
    (T / "catalogue.py").write_text(cat2, encoding="utf-8")
    p = rr("milestones", "--channel", "dev"); expect("milestone names the newly done ticket and its roll-up", MT in p.stdout and MG in p.stdout, p.stdout + p.stderr)
    f = re.search(r"tracker/relay_out/\S+_milestone_dev\.json", p.stdout).group(0); rr("record", f, "--ts", "1791580000.000002")
    (T / "status.json").write_text(st0, encoding="utf-8"); (T / "catalogue.py").write_text(cat, encoding="utf-8")
    rc, out = run(cwd, "check", "--max-warn", "99"); expect("R2 correction owed when an announced milestone reopens", "R2 %s" % MT in out, out)
    p = rr("artifact", "tracker/LINKS.md", "--tickets", "BLD-11", "--summary", "spec", "--channel", "dev")
    f = re.search(r"tracker/relay_out/\S+_artifact_dev\.json", p.stdout).group(0); rr("record", f, "--ts", "1791580000.000003")
    with open(T / "LINKS.md", "a", encoding="utf-8") as fh:
        fh.write("\nchanged\n")
    rc, out = run(cwd, "check", "--max-warn", "99"); expect("R1 relayed artifact changed after posting", "R1 artifact tracker/LINKS.md" in out, out)
    p = rr("artifact", "../Causal-Copilot/README.md", "--tickets", "BLD-11", "--summary", "x", "--channel", "dev")
    expect("relay refuses files outside cc-research", p.returncode != 0, p.stdout + p.stderr)
    shutil.copy2(HERE / "LINKS.md", T / "LINKS.md"); shutil.copy2(HERE / "links.txt", T / "links.txt"); shutil.copy2(HERE / "prod.json", T / "prod.json")
    for x in ("relay_log.jsonl", "reviews.jsonl"):
        if (HERE / x).exists():
            shutil.copy2(HERE / x, T / x)
        elif (T / x).exists():
            (T / x).unlink()

    # IDs never vanish; retirement is explicit
    with open(T / "ids.lock", "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": "2026-10-01T00:00:00Z", "event": "issued", "id": "REP-98", "kind": "dev", "title": "x"}) + "\n")
    rc, out = run(cwd, "check"); expect("T4 issued ID that vanished", rc == 1 and "T4" in out and "REP-98" in out, out)
    run(cwd, "retire", "REP-98", "--note", "selftest"); rc, out = run(cwd, "check", "--max-warn", "99")
    expect("retire clears T4", "REP-98" not in out, out)

    # mentions of unknown IDs
    with open(T / "README.md", "a", encoding="utf-8") as fh:
        fh.write("\nSee REP-77 for details.\n")
    rc, out = run(cwd, "check", "--max-warn", "99"); expect("W5 unknown ID mentioned in a doc", "W5" in out and "REP-77" in out, out)

    # stale status.json
    cat = (T / "catalogue.py").read_text(encoding="utf-8")
    cat2, n = re.subn(r'(item\("REP-03", "REP", "[^"]*", )"in_progress"', r'\1"todo"', cat)
    (T / "catalogue.py").write_text(cat2, encoding="utf-8")
    rc, out = run(cwd, "check"); expect("T10 catalogue changed without verify", n == 1 and rc == 1 and "T10" in out and "REP-03" in out, out)
    (T / "catalogue.py").write_text(cat, encoding="utf-8")

    # bundles: done only when every ticket they close is done (T11); may start before their dependencies finish
    st = json.loads(st0)
    for r in st["items"]:
        if r["id"] == "BND-05":
            r["effective_status"] = "in_progress"
        if r["id"] == "BND-08":
            r["effective_status"] = "done"
    json.dump(st, open(T / "status.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    rc, out = run(cwd, "check", "--max-warn", "99")
    expect("T11 bundle done while tickets it closes are not", "T11 bundle BND-08 is done" in out, out)
    expect("a bundle may start before its dependencies finish (no W3)", "W3 BND-05" not in out, out)
    expect("a bundle may not finish before its dependencies (W3)", "W3 BND-08 is done while blocked by unfinished" in out, out)
    (T / "status.json").write_text(st0, encoding="utf-8")

    # evidence pinned to a closing-time manifest: new files do not reopen, a changed listed file does
    import hashlib
    h = hashlib.sha256((T / "LINKS.md").read_bytes()).hexdigest()
    (T / "m.sha256").write_text("%s  tracker/LINKS.md\n" % h, encoding="utf-8")
    probe = ("import sys, json; sys.path.insert(0, 'tracker'); import verify; "
             "print(json.dumps(verify.run_check({'t': 'manifest', 'path': 'tracker/m.sha256'})))")
    (T / "new_file.txt").write_text("added after closing\n", encoding="utf-8")
    p1 = subprocess.run([sys.executable, "-c", probe], cwd=cwd, capture_output=True, text=True)
    with open(T / "LINKS.md", "a", encoding="utf-8") as fh:
        fh.write("\nchanged\n")
    p2 = subprocess.run([sys.executable, "-c", probe], cwd=cwd, capture_output=True, text=True)
    expect("manifest evidence ignores files added later", p1.stdout.strip().startswith("[true"), p1.stdout + p1.stderr)
    expect("manifest evidence catches a changed listed file", p2.stdout.strip().startswith("[false"), p2.stdout + p2.stderr)
    shutil.copy2(HERE / "LINKS.md", T / "LINKS.md")

    # Slack mirror drift
    (T / "m.csv").write_text("Record ID,ID,Status,Evidence level\nRec01,REP-01,✅ Done,V3\nRec02,REP-02,👀 In progress,V3\nRec03,ZZZ-01,⏳ To-do,V0\n", encoding="utf-8")
    rc, out = run(cwd, "mirror", "tracker/m.csv", "--list", "dev")
    expect("mirror reports status drift, unknown and missing rows", rc == 1 and "REP-02 Status" in out and "ZZZ-01" in out and "missing from Slack" in out, out)
    m = json.load(open(T / "mirrors.json")); expect("mirror records Slack record IDs", m["lists"]["F0C869P25NE"].get("REP-01") == "Rec01", json.dumps(m)[:300])

    # unlink keeps history
    run(cwd, "link", "REP-01", "relates", "REP-02", "--note", "selftest"); run(cwd, "unlink", "REP-01", "relates", "REP-02")
    txt = (T / "links.txt").read_text(encoding="utf-8")
    expect("unlink removes the edge and leaves a comment", "# removed" in txt and "\nREP-01 relates REP-02" not in txt, txt[-300:])

    ok = all(r["ok"] for r in results)
    json.dump({"ok": ok, "passed": sum(r["ok"] for r in results), "total": len(results), "cases": results},
              open(HERE / "selftest_trace.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    shutil.rmtree(cwd.parent, ignore_errors=True)
    print("%d/%d passed" % (sum(r["ok"] for r in results), len(results)))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
