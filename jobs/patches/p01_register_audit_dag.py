"""Register the approved audit DAG in the catalogue (AUD-33..48, DEC-05), close AUD-32 and DEC-02, and add AB-* bundle statuses.
Idempotent: refuses to run twice."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
s = p.read_text(encoding="utf-8")
assert 'item("AUD-33"' not in s, "already applied"
dag = json.load(open(ROOT / "plans" / "audit_dag.json", encoding="utf-8"))
DEC_REC = "docs/decisions/2026-10-12_audit_dag.md"

TITLES = {"AUD-33": "AB-01 Controlled scoreboard, CausalArena complete (all families, D and D+I, corrected leaderboard)",
          "AUD-34": "AB-02 Second scoreboard: layout and conflict channels on other public benchmarks",
          "AUD-35": "AB-03 Engine forensics: perfect-oracle and determinism checks for every engine agents call",
          "AUD-36": "AB-04 Decision-value scoreboard across benchmarks, with the usefulness threshold",
          "AUD-37": "AB-05 LIVE (small): agent probes, install and one-run cost per agent ($5 cap)",
          "AUD-38": "AB-06 LIVE: field audit of LLM-using systems under names x layout controls",
          "AUD-39": "AB-08 Name-reliance benchmark with a rho dial (decoupled semantics, B2)",
          "AUD-40": "AB-09 Theory pack: identity, error budget, bounded harm, conflict-rule order dependence, DV ceiling",
          "AUD-41": "AB-10 Practitioner interviews (C1)",
          "AUD-42": "AB-11 Competitive teardown: open tools hands-on, closed tools by documented claims",
          "AUD-43": "AB-12 Vertical probe: root-cause analysis",
          "AUD-44": "AB-13 Regulation and standards map: requirement -> ledger field",
          "AUD-45": "AB-14 Market and go-to-market hypotheses for two verticals",
          "AUD-46": "AB-15 Positioning closure: novelty matrix for L1-L5",
          "AUD-47": "AB-17 Paper skeleton and pre-registration manifest",
          "AUD-48": "AB-07 LIVE: knowledge elicitation run (A3, DEC-02): tiers, three phrasings, three name arms",
          "DEC-05": "AB-16 Wedge decision: paper spine, venue and the Q2 build"}
by_ticket = {b["closes"][0]: b for b in dag["bundles"]}
lines = []
for t, title in TITLES.items():
    b = by_ticket[t]
    crit = "Must show: " + "; ".join(b["must_show"]) + ". Gates: " + "; ".join(b["gates"])
    kind = "decision" if t.startswith("DEC") else "task"
    cat = "DEC" if t.startswith("DEC") else "AUD"
    note = "Bundle %s of plans/audit_dag.json (%s track); window %s..%s; cost: %s." % (b["id"], b["track"], b["window"][0], b["window"][1], b["llm_cost"])
    lines.append("item(%r, %r, %r, \"todo\", kind=%r, criterion=%r, due=%r, note=%r)," % (t, cat, title, kind, crit, b["window"][1], note))
block = "# ---- audit program (plans/audit_dag.json, approved 2026-10-12)\n" + "\n".join(lines) + "\n"

anchor = 'item("BEN-01", "BEN",'
assert s.count(anchor) == 1
s = s.replace(anchor, block + anchor)

old32 = 'item("AUD-32", "AUD", "Audit program DAG: research landscape, commercial landscape, wedge and paper", "in_progress",'
assert s.count(old32) == 1
s = s.replace(old32, old32.replace('"in_progress",', '"done",'))
s = s.replace('evidence=["plans/make_audit_dag.py", "plans/audit_dag.json", "analysis/reports/audit_dag.md"],',
              'evidence=["plans/make_audit_dag.py", "plans/audit_dag.json", "analysis/reports/audit_dag.md", "%s"],' % DEC_REC)
s = s.replace('note="Proposed 2026-10-12; awaiting approval. On approval: AUD-33..47 and DEC-05 enter the catalogue."),',
              'note="Approved by Uzair 2026-10-12 (%s); AUD-33..48 and DEC-05 issued."),' % DEC_REC)

old02 = 'item("DEC-02", "DEC", "Approve the tier-elicitation test (~900 short calls through Uzair\'s key)", "open", kind="decision"),'
assert s.count(old02) == 1
s = s.replace(old02, 'item("DEC-02", "DEC", "Approve the tier-elicitation test (~900 short calls through Uzair\'s key)", "done", kind="decision", '
                     'criterion="Uzair\'s decision recorded with what it approves", evidence=["%s"], checks=[G("%s", r"DEC-02 tier-elicitation test \\(AB-07\\) \\| approved")], '
                     'note="Approved 2026-10-12 with the audit DAG; the run is AUD-48 (AB-07)."),' % (DEC_REC, DEC_REC))

old_bs = "\nBUNDLE_NOTE = {"
assert s.count(old_bs) == 1
s = s.replace(old_bs, "\nBUNDLE_STATUS.update({b: \"todo\" for b in (%s)})\n" % ", ".join('"AB-%02d"' % i for i in range(1, 18)) + old_bs)
p.write_text(s, encoding="utf-8")
print("catalogue patched: %d audit tickets, AUD-32 and DEC-02 done" % len(TITLES))

# snapshot: show the audit DAG's bundles next to the Q1 bundles
q = ROOT / "tracker" / "snapshot.py"
t = q.read_text(encoding="utf-8")
old = '''def bundles():
    dag = load("plans/q1_dag.json")
    out = []
    for b in dag["bundles"]:'''
new = '''def bundles():
    dag = load("plans/q1_dag.json")
    audit = load("plans/audit_dag.json")
    out = []
    for plan, b in [("q1", b) for b in dag["bundles"]] + [("audit", b) for b in audit["bundles"]]:'''
assert t.count(old) == 1
t = t.replace(old, new)
old2 = '''"uzair_actions": b.get("uzair_actions") or [], "note": C.BUNDLE_NOTE.get(bid, "")})
    return out, dag.get("milestones", [])'''
new2 = '''"uzair_actions": b.get("uzair_actions") or [], "note": C.BUNDLE_NOTE.get(bid, ""), "plan": plan,
                    "track": b.get("track"), "serves": b.get("serves") or []})
    return out, dag.get("milestones", []) + audit.get("milestones", [])'''
assert t.count(old2) == 1
t = t.replace(old2, new2)
q.write_text(t, encoding="utf-8")
print("snapshot.py: audit bundles included")
