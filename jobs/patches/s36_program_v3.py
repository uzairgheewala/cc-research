"""s36 (30 Oct): program v3 tickets, the move to the second laptop, and the image-record class fix.

Tickets: PRG-01, DLV-05, DLV-06, DLV-08..DLV-12, BLD-19..BLD-24, ADV-01, PRD-01, PRD-02, CRS-01, CRS-09, INF-11, INF-01, INF-04, INF-06, INF-10

1. tracker/catalogue.py: program v3 (project doc claude/program-v3-2026-10-29.md) as tickets.
   - New prefixes, each under an existing category (no new Slack select option is needed):
     PRG -> "15 Decisions", ADV -> "9 Evaluation protocol", PRD -> "14 Stretch".
   - A1 is the existing pair DLV-05 (checkpoint, 6 Nov) and DLV-06 (final, 4 Dec), re-cut to the auditor paper;
     A2-A6 are DLV-08..DLV-12. R0-R5 are BLD-19..BLD-24.
   - The program doc's "CRS-06" for Prof. Umesh's written confirmation is CRS-09: CRS-06 already names the Q2 deliverables,
     and CRS-08 is the PA ticket WAVE_STATE named in wave B (never added). IDs are never reused.
   - CRS-01 (TA check-in 1) is done: held Thu 29 Oct; its outcomes are program v3 section 0 (pointer evidence: V1).
   - INF-11: the move to the second laptop (migration doc step 4, docs/hosts.md).
2. WAVE_STATE.md "Current" re-cut to program v3 and the move (repin INF-10 after review).
3. cc.ps1 build kept no earlier record of manifests/image_ids.json (ensureimage did): the rebuild on the new laptop
   (31 Oct 01:26 UTC) overwrote the 21 Oct record. Class fix: build keeps the earlier record as image_ids_before_<stamp>.json
   and names it in previous_record, as ensureimage does (repin INF-01, INF-04, INF-06 after review). The lost record is
   restored from git HEAD as image_ids_before_20261031T012646Z.json and named in the current record.
Run once from cc-research: py -3 jobs\\patches\\s36_program_v3.py   (refuses twice)."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ---- 1. catalogue
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides s36" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides s36 (2026-10-30): program v3 (claude/program-v3-2026-10-29.md) as tickets; the move to the second laptop
CATS.update({"PRG": "15 Decisions", "ADV": "9 Evaluation protocol", "PRD": "14 Stretch"})
_P3 = "project:claude/program-v3-2026-10-29.md"
_P3K = "project:claude/program-v3-kickoffs-2026-10-29.md"
ITEMS.append(item("PRG-01", "PRG", "Program v3: two papers and two repos (Q1 the auditor, Q2 the system), with the adversary loop between them",
                  "in_progress",
                  criterion=("The program doc (sections 0-11, decisions P3-1..P3-6 with defaults) and the kickoff prompts for chats W1-W5 are "
                             "written; P3-4 (private engine core) is answered by Prof. Umesh; the five chats are open and each owns its files"),
                  evidence=[_P3, _P3K],
                  note=("29 Oct, after the TA check-in. Defaults in brackets in section 10; P3-4 is an ask (CRS-09, PRD-02). "
                        "This chat (W5) keeps the program doc, the tracker and the site; changes to the ledger format or audit protocol go through it.")))
ITEMS.append(item("DLV-08", "DLV", "A2 Audit protocol spec v1: finding kinds (closed list), regimes, truth tiers, development and sealed batteries, certificate",
                  "todo", kind="deadline", due="2026-12-04",
                  criterion=("A versioned spec in the Q1 repo: each finding kind with its control, effect size with interval and evidence files; "
                             "the four regimes; the truth tiers (exact, contested, provenance-only, mismatched); a public development battery and a "
                             "hashed sealed battery read once per declared version; the certificate (system identity, battery hash, every number with "
                             "its source, the rerun command)"),
                  evidence=[_P3 + " (section 2.2)"], note="Program v3 A2; chat W2. Outlined in the checkpoint's introduction (DLV-05)."))
ITEMS.append(item("DLV-09", "DLV", "A3 audit package: adapter interface, controls L0-L2, report generator; one command audits a system end to end",
                  "todo", kind="deadline", due="2026-12-04",
                  criterion=("audit/ package with tests: the adapter interface designed against the five audited systems plus PC and GES before it is "
                             "frozen; L0 scoring, L1 metamorphic controls, L2 stage tracing for Python systems; reports and certificates; each bundle "
                             "audits one system end to end and equals the existing audit results to 0.001"),
                  evidence=[_P3 + " (section 2.4)", _P3K + " (W2)"], note="Program v3 A3; chat W2. The Q1 repo is renamed to the audit repo when this lands (P3-3)."))
ITEMS.append(item("DLV-10", "DLV", "A4 Audit results rerun through the package: per-system tables L0-L2 and provenance by arm difference (L3-lite)",
                  "todo", kind="deadline", due="2026-12-04", blocked_by="DLV-09",
                  criterion="Every audit in the Q1 paper is produced by the package; no new API spend except a rerun Uzair approves",
                  evidence=[_P3 + " (section 2.4)"], note="Program v3 A4; chat W2 bundle 5."))
ITEMS.append(item("DLV-11", "DLV", "A5 Benchmark shortcut audits as the paper's appendix: CausalArena layout (AB-01) and the CausalBench metric (BEN-13)",
                  "todo", kind="deadline", due="2026-12-04",
                  criterion="The two benchmark audits re-stated under the protocol (finding kinds, truth tiers), numbers from their result files",
                  evidence=[_P3 + " (section 2.3)"], note="Program v3 A5; chat W1 (cited at the checkpoint), W2 (rerun)."))
ITEMS.append(item("DLV-12", "DLV", "A6 Public scorecards: one page per audited system, generated from the audit reports",
                  "todo", kind="deadline", due="2026-12-04", blocked_by="DLV-10",
                  criterion="One site page per audited system, every number read from a report through site/registry.py",
                  evidence=[_P3 + " (section 2.4)"], note="Program v3 A6; chat W5 (site v4 routes after 6 Nov)."))
_R = [("BLD-19", "R0 The contract: the claim-ledger format and a ledger writer in the agent",
       "The ledger format agreed by W2, W3 and W5 and written into the program doc; the agent writes one ledger per run on a fork branch", "2026-12-04", None),
      ("BLD-20", "R1 Correctness fixes: the 16 code notes plus the cycle fix, live, one fork branch per ticket",
       "Each fix from analysis/reports/copilot_code_notes.md on its own branch with a stub run; the live run is proposed with its cost and run by Uzair", "2026-12-04", None),
      ("BLD-21", "R2 Typed state and per-edge provenance in the agent",
       "Every edge in the agent's output carries its source (data, interventions, declared knowledge, model call) in the ledger", "2026-12-04", "BLD-19"),
      ("BLD-22", "R3 The direction rule (commit an arrow only on sufficient evidence, else name the next experiment) and knowledge as orient-only tiers",
       "On saved development cases: wrong, right and open directions and links reported separately for the current and the new rule; the rule "
       "pre-registered and hashed before any held-out read; gas/void a regression check only", None, None),
      ("BLD-23", "R4 The engine slot: kernel v3, the v4 candidates and interventions behind one interface",
       "The agent calls the engine through the ledger contract; swapping engines changes no agent code", None, "BLD-19"),
      ("BLD-24", "R5 A report rendered from the ledger",
       "The user-facing report is generated from the ledger alone; every sentence traces to a claim", None, "BLD-21")]
for _id, _t, _cr, _due, _bb in _R:
    ITEMS.append(item(_id, "BLD", _t, "todo", criterion=_cr, due=_due, blocked_by=_bb,
                      evidence=[_P3 + " (section 3)", "project:claude/rebase-2026-10-24.md (section 5)"],
                      note="Program v3 system phase; chat W3. Never on the fork's main; B tunes on A's development battery only."))
ITEMS.append(item("ADV-01", "ADV", "Adversary loop log: B (the system) against A (the auditor), round by round", "in_progress",
                  criterion=("One row per round: A version, B version, battery hash, findings opened, findings closed, regressions; a finding "
                             "closes only by a sealed read; new finding kinds pre-registered before they run on B; the table appears in both papers"),
                  evidence=[_P3 + " (section 4)"],
                  note=("Round 0 is recorded in program v3 section 4 (review step deleting links, cycle crash, names driving direction; "
                        "refinement v2 closed links and crashes, not direction). Round 1: the direction rule (BLD-22) against a plurality-trap probe "
                        "and a direction battery (A, L4 seed).")))
ITEMS.append(item("PRD-01", "PRD", "Pharma bars: P1 perturbation-data target prioritisation and P2 RWE assumption ledger", "todo",
                  criterion=("One table per shape: buyer, job to be done, evidence demanded (primary sources: ICH M14, FDA RWE guidance, "
                             "published Perturb-seq validation), a numeric bar, the distance from today's measured results, the cheapest next "
                             "experiments; every figure labelled primary, second-hand, vendor claim, analyst claim or estimate"),
                  evidence=[_P3 + " (section 5)"], note="Program v3 section 5; chat W4. Targets to validate, not facts; nothing is called sellable before a sealed read meets them."))
ITEMS.append(item("PRD-02", "PRD", "IP and licence check before any commercial step: UCSD student IP policy, Causal-Copilot's MIT licence, the mentor's authorship",
                  "todo",
                  criterion=("Questions for Prof. Huang and Prof. Umesh written from UCSD's actual policy page; the private-core proposal (P3-4) put "
                             "to Prof. Umesh; what needs an expert flagged (not legal advice)"),
                  evidence=[_P3 + " (sections 5-6)"], note="Program v3 sections 5-6; chat W4."))
ITEMS.append(item("CRS-09", "CRS", "Written confirmation from Prof. Umesh (course professor) of the one-person group the TA approved on 29 Oct",
                  "in_progress", kind="deadline",
                  criterion="A written reply from Prof. Umesh, saved without contact details under docs/course/ and named here",
                  note=("30 Oct: Uzair sent the emails; awaiting replies. The program doc called this CRS-06, which already names the Q2 "
                        "deliverables; CRS-08 is the PA ticket named in WAVE_STATE (wave B)."), evidence=[_P3 + " (section 0)"]))
ITEMS.append(item("INF-11", "INF", "Move to the second laptop (30 Oct): migration checks and the host record used to size wave sheets",
                  "in_progress",
                  criterion=("Migration doc step 4 passes on the new laptop: every file outside git matches manifests/excluded/ (data_manifest "
                             "--check), the three repos are clean at the GitHub heads, ci_check_portable and snapshot --check pass, the Q1 "
                             "repo reproduces, the hooks path is set, and preflight nollm passes on the rebuilt images; docs/hosts.md records "
                             "CPU family, AVX-512, cores, RAM and Docker memory, with manifests/hosts/laptop2.json from tools/host_probe.ps1"),
                  evidence=["docs/hosts.md", "tools/host_probe.ps1", "project:claude/migration-2026-10-30.md"],
                  note=("30 Oct (W5, from the device shell): 31,824 of 31,826 excluded files re-hashed equal, none missing or added, all sizes "
                        "equal (the two CausalBench .h5ad files, 19.4 GB, are left to the native --check); repos at cf536c1 / a31aa7c "
                        "(55a490a, da55264) / 43d0c75 as on GitHub; ci_check 0 errors; snapshot ok; Q1 reproduce exact; hooksPath tools/hooks. "
                        "Images rebuilt by Uzair from 31 Oct 01:26 UTC; preflight held until he says.")))
for _i in ITEMS:
    if _i["id"] == "DLV-05":
        _i["title"] = "A1 checkpoint: the Q1 paper (the auditor) title, abstract, introduction with literature review, data, public code link (Fri 6 Nov)"
        _i["criterion"] += "; framed as the auditor paper (program v3 section 2, PRG-01), with Causal-Copilot as the worked case"
        _i["note"] = ((_i.get("note") or "") + " 30 Oct: program v3 A1 checkpoint; chat W1 has priority until 6 Nov.").strip()
    if _i["id"] == "DLV-06":
        _i["title"] = "A1 Q1 final paper: the auditor, its protocol, the audits, results and limits (Fri 4 Dec)"
        _i["note"] = ((_i.get("note") or "") + " 30 Oct (program v3): re-cut from a replication-style report to the auditor paper; the "
                      "earlier criterion was: " + _i["criterion"]).strip()
        _i["criterion"] = ("The full Q1 paper (program v3 A1): the audit protocol (DLV-08), the package (DLV-09), the audits under it (DLV-10), "
                           "the benchmark appendix (DLV-11) and limits, with Causal-Copilot as the worked case (DLV-01 to DLV-04); every number "
                           "reproducible from the Q1 repo with the command named next to it")
    if _i["id"] == "CRS-01":
        _i["status"] = "done"
        _i["criterion"] = _i.get("criterion") or "The TA check-in is held and its outcomes are recorded"
        _i["evidence"] = list(_i.get("evidence") or []) + [_P3 + " (section 0)"]
        _i["note"] = ((_i.get("note") or "") + " 30 Oct: held Thu 29 Oct 10:45. Outcomes (program v3 section 0): one-person group approved by "
                      "the TA (written confirmation: CRS-09); Q1 and Q2 as separate papers and repos; next deadline Fri 6 Nov.").strip()
'''
p.write_text(c, encoding="utf-8", newline="\n")
print("catalogue: s36 appended")

# ---- 2. WAVE_STATE.md "Current"
w = ROOT / "WAVE_STATE.md"
s = w.read_text(encoding="utf-8")
a, b = s.index("## Current\n"), s.index("## Wave A: what was built")
NEW = """## Current
Updated 2026-10-30 (W5, the program chat). Tickets: PRG-01, INF-11, CRS-09, DLV-05
- **Program v3** (29 Oct, project doc `claude/program-v3-2026-10-29.md`, PRG-01) replaces the wave-C menu (D-11). Q1 is the
  auditor (DLV-05 checkpoint 6 Nov and DLV-06 final 4 Dec, plus DLV-08..12); Q2 is the system (BLD-19..24, R0-R5); the
  adversary loop is ADV-01; the product bars and IP check are PRD-01/02. C-a became the checkpoint (chat W1); C-b and C-c
  wait for program v3's order of work. Waves A and B: complete (readbacks below).
- **Moved to the second laptop 30 Oct** (INF-11, `docs/hosts.md`): Intel Core Ultra 7 155U, AVX2, no AVX-512, so the same
  BLAS family (HASWELL) as the first laptop; numbers read as before, and the canary confirms on the first sheet. The images
  were rebuilt there from 31 Oct 01:26 UTC (`manifests/image_ids.json`; the earlier record is
  `image_ids_before_20261031T012646Z.json`). The Causal-Copilot base is a new build again: a live comparison needs its own
  main control on this image (as LIVE_06M was).
- Waiting commit message: `docs/commit_msgs/program_v3_cc-research.txt` (the 27 Oct commits carried the wave A-B messages).
- Engine cache: `jobs/transfer/cache_engines_2026-10-19.tgz` (500 CausalArena dev entries); family-2 entries filled on the sheet (done).
- Defaults taken (20 Oct): D-1 plan yes; D-2 second family = our labelled generator (500 files), Causal Chambers wt
  report-only; D-3 BEN-13 names-only LLM arm no; D-4 public feed = dev digests; D-5 gaps page = new Act IV page (wave B);
  D-7 (rerun 2) main-control live arm only if the Causal-Copilot base image was rebuilt: on.

"""
s = s[:a] + NEW + s[b:]
w.write_text(s, encoding="utf-8", newline="\n")
print("WAVE_STATE: Current re-cut")

# ---- 3. cc.ps1 build keeps the earlier image record (as ensureimage does)
q = ROOT / "cc.ps1"
t = q.read_text(encoding="utf-8")
OLD = '''        $baseId = & docker image inspect $BaseImage --format "{{.Id}}"
        $runId  = & docker image inspect $Image --format "{{.Id}}"
        $info = @{ base_image = $BaseImage; base_id = "$baseId"; runtime_image = $Image; runtime_id = "$runId"; built_utc = (Get-Date).ToUniversalTime().ToString("o") }
        $info | ConvertTo-Json | Out-File -Encoding ascii (Join-Path $Research "manifests\\image_ids.json")
'''
NEWB = '''        $baseId = (& docker image inspect $BaseImage --format "{{.Id}}" | Out-String).Trim()
        $runId  = (& docker image inspect $Image --format "{{.Id}}" | Out-String).Trim()
        $recPath = Join-Path $Research "manifests\\image_ids.json"
        $nowUtc = (Get-Date).ToUniversalTime()
        $info = [ordered]@{ base_image = $BaseImage; base_id = $baseId; runtime_image = $Image; runtime_id = $runId;
                            built_utc = $nowUtc.ToString("o"); rebuilt = "base+overlay" }
        # INF-11 (30 Oct): keep the earlier record, as ensureimage does (a rebuild on the new laptop overwrote it once)
        if (Test-Path $recPath) {
            $keep = Join-Path $Research ("manifests\\image_ids_before_" + $nowUtc.ToString("yyyyMMddTHHmmssZ") + ".json")
            Copy-Item $recPath $keep
            $info["previous_record"] = (Split-Path -Leaf $keep)
        }
        $info | ConvertTo-Json | Out-File -Encoding ascii $recPath
'''
assert t.count(OLD) == 1, "cc.ps1 build block not found as expected"
q.write_text(t.replace(OLD, NEWB), encoding="utf-8", newline="\n")
print("cc.ps1: build keeps the earlier record")

# ---- 3b. restore the record the 31 Oct build overwrote
keep = ROOT / "manifests" / "image_ids_before_20261031T012646Z.json"
assert not keep.exists(), "record already restored"
old = subprocess.check_output(["git", "--no-optional-locks", "-c", "safe.directory=*", "show", "HEAD:manifests/image_ids.json"], cwd=ROOT)
keep.write_bytes(old)
r = ROOT / "manifests" / "image_ids.json"
cur = r.read_bytes().decode("ascii")
assert '"built_utc":  "2026-10-31T01:26:46' in cur and "previous_record" not in cur, "image_ids.json is not the 31 Oct build record"
nl = "\r\n" if "\r\n" in cur else "\n"
end = cur.rstrip().rstrip("}").rstrip()
cur = end + "," + nl + '    "rebuilt":  "base+overlay",' + nl + '    "previous_record":  "image_ids_before_20261031T012646Z.json"' + nl + "}" + nl
r.write_bytes(cur.encode("ascii"))
print("image record: earlier record restored and named")
