"""Record the audit-bundle results of 2026-10-13 in the catalogue: statuses, evidence and checks for AUD-33..48 and DEC-05,
bundle statuses and notes for AB-01..AB-17, and a new ticket BLD-14 (ledger v0.2 gaps found by AB-11 and AB-13).
Replaces the one-line placeholder items written by p01. Idempotent: refuses to run twice."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
s = p.read_text(encoding="utf-8")
assert "# ---- audit program results (p02)" not in s, "already applied"

R = "analysis/reports/"
RS = "analysis/results/"
ITEMS = {}


def it(tid, cat, title, status, criterion, evidence, checks, note, due, kind="task", blocked_by=None, reproduce=""):
    ITEMS[tid] = ("item(%r, %r, %r, %r, kind=%r, criterion=%r,\n     evidence=%r,\n     checks=[%s],\n     due=%r, blocked_by=%r, reproduce=%r,\n     note=%r),"
                  % (tid, cat, title, status, kind, criterion, evidence, ", ".join(checks), due, blocked_by, reproduce, note))


it("AUD-33", "AUD", "AB-01 Controlled scoreboard, CausalArena complete (all families, D and D+I, corrected leaderboard)", "done",
   "Must show: corrected leaderboard table; per-family layout gain by channel (authors' rule, conflict rule, engine copy). Gate: every runnable published row has released and shuffled numbers under both rules, files paired",
   ["analysis/baseline_variants_run.py", "analysis/rescore_controls_v2.py", RS + "rescore_v2/rescore_v2.json", RS + "rescore_v2/leaderboard_controlled.md",
    RS + "rescore_v2/leaderboard_controlled.json", RS + "rescore_v2/CONTRACT.json", R + "ab01_controlled_scoreboard.md"],
   ['J("analysis/results/rescore_v2/rescore_v2.json", ["predictions", "P2", "complete"], "true")',
    'G("analysis/reports/ab01_controlled_scoreboard.md", r"Corrected leaderboard")'],
   "Results in the report; predictions P1/P2 verdicts in rescore_v2.json.", "2026-10-17",
   reproduce="python analysis/baseline_variants_run.py ... (see report) && python analysis/rescore_controls_v2.py")
it("AUD-34", "AUD", "AB-02 Second scoreboard: layout and conflict channels on other public benchmarks", "blocked",
   "Must show: per-benchmark table: order correlation, sortability, layout gain per method. Gate: two published rows reproduced per benchmark before any re-score claim",
   [R + "ab02_second_scoreboard.md", "analysis/ab02_alarm_order.py", RS + "ab02/alarm_order.json", "analysis/audits/AB02_AB12_data_scouting.md"],
   ['J("analysis/results/ab02/alarm_order.json", ["P3_this_release"], "eq", "no (all |tau| < 0.3)")'],
   "gCastle alarm measured (no causal column order; PC not reproduced, so no re-score claim). Bayesys needs Uzair's browser download: zenodo.org and constantinou.info are refused by both network paths.",
   "2026-10-24", blocked_by="Uzair: download Bayesys data into external/bayesys")
it("AUD-35", "AUD", "AB-03 Engine forensics: perfect-oracle and determinism checks for every engine agents call", "done",
   "Must show: engine defect table (exact rate, order invariance, determinism, defect class). Gate: versions pinned; one command reproduces",
   ["analysis/engine_forensics.py", "analysis/engine_shims.py", RS + "engine_forensics/forensics.json", RS + "engine_forensics/CONTRACT.json",
    R + "ab03_engine_forensics.md", "docs/drafts/bug_reports/dodiscover_pc_oracle_cycle.md"],
   ['J("analysis/results/engine_forensics/forensics.json", ["engines", "dodiscover_pc", "exact_equivalence_class"], "eq", 597)',
    'J("analysis/results/engine_forensics/forensics.json", ["engines", "pgmpy_stable_unbounded", "exact_equivalence_class"], "eq", 720)',
    'J("analysis/results/engine_forensics/forensics.json", ["engines", "tigramite_pcmciplus", "exact_equivalence_class"], "eq", 720)'],
   "P5 refuted as worded (no further wrong skeleton); new defect class: dodiscover PC orients wrongly under an oracle and can return a cyclic graph. Bug-report drafts for EXT-03 in docs/drafts/bug_reports/.",
   "2026-10-24", reproduce="python analysis/engine_forensics.py --python2 <venv with pgmpy, tigramite, dodiscover> --vendored <Causal-Copilot>/externals/causal-learn --out analysis/results/engine_forensics")
it("AUD-36", "AUD", "AB-04 Decision-value scoreboard across benchmarks, with the usefulness threshold", "done",
   "Must show: decision-value table across benchmarks; risk-coverage figure; F1 vs DV scatter. Gate: claims checked against truth; baselines on exactly the files each method finished",
   ["analysis/decision_value_v2.py", "analysis/dv_chambers_sachs.py", "analysis/ab04_figures.py", RS + "decision_value_v2/decision_value_v2.json",
    RS + "decision_value_v2/dv_chambers_sachs.json", RS + "decision_value_v2/risk_coverage.png", RS + "decision_value_v2/f1_vs_dv.png",
    RS + "decision_value_v2/CONTRACT.json", R + "ab04_decision_value.md"],
   ['G("analysis/reports/ab04_decision_value.md", r"P6")', 'J("analysis/results/decision_value_v2/dv_chambers_sachs.json", ["benchmarks", "causal_chambers_lt", "methods", "true CPDAG", "precision_committed"], "eq", 1.0)'],
   "Five benchmarks: CausalArena semantic, formula, synthetic; Causal Chambers (physical truth, real interventions); Sachs (weak).", "2026-10-28",
   reproduce="python analysis/decision_value_v2.py && python analysis/dv_chambers_sachs.py --causal-learn <upstream causal-learn> ... && python analysis/ab04_figures.py ...")
it("AUD-37", "AUD", "AB-05 LIVE (small): agent probes, install and one-run cost per agent ($5 cap)", "blocked",
   "Must show: per agent: installs, runs, calls, tokens, cost, wall time, failure points. Gate: no key in any log; every call recorded; repo byte-identical",
   ["harness/agent_probe.py", "harness/probe_llm.py", "harness/probe_io.py", "harness/agents/registry.json", "docker/Dockerfile.probes",
    "plans/ab05_probe_causaliq.json", "plans/ab05_probe_pywhyllm.json", "plans/ab05_probe_matmcd.json", "plans/ab05_probe_vashishtha.json",
    "plans/ab05_cc_gpt4omini.json", R + "ab05_probe_prep.md", "tests/test_agent_probe.py"],
   ['G("analysis/reports/ab05_probe_prep.md", r"Proposed AB-06 budget")', 'J("plans/ab05_probe_vashishtha.json", ["budget_check", "sum_max_usd_all_four"], "le", 4.0)'],
   "Offline part done: all four agents run end to end with a stub model; caps total $3.55 + Causal-Copilot second model (~$0.03). Live runs are Uzair's (cc.ps1 probebuild, probe).",
   "2026-10-20", blocked_by="Uzair: live probe runs (approved cap $5)")
it("AUD-38", "AUD", "AB-06 LIVE: field audit of LLM-using systems under names x layout controls", "todo",
   "Must show: per agent x arm table; name-reliance figure; provenance shares. Gate: thresholds hashed before the calls; dev split only",
   [], [], "Budget proposed in the AB-05 report (about $57 for 4 agents x 3 arms x 10 dev scenarios, or about $29 with PyWhy on gpt-4o-mini); recompute from the first live calls before approval.",
   "2026-11-14", blocked_by="AUD-37")
it("AUD-48", "AUD", "AB-07 LIVE: knowledge elicitation run (A3, DEC-02): tiers, three phrasings, three name arms", "blocked",
   "Must show: O1-O5 verdicts; tier accuracy by arm; regression on model tiers vs 0.634 / 0.524. Gate: DEC-02 approved; prompts and thresholds hashed before the calls",
   ["analysis/a3_make_requests.py", "harness/tiers_runner.py", "analysis/a3_score.py", "plans/a3_prereg.json", "plans/a3_tiers_requests.jsonl",
    "plans/a3_scenarios.json", RS + "a3/selftest.json", "tests/test_tiers_runner.py"],
   ['J("plans/a3_prereg.json", ["requests"], "eq", 900)', 'J("analysis/results/a3/selftest.json", ["oracle_tiers", "verdicts", "O4", "value"], "ge", 0.71)'],
   "Ready: 900 requests pre-registered (sha256 in a3_prereg.json), estimate about $3.1 at gpt-4o list; scorer validated with oracle tiers (O4 0.714). Live run is Uzair's: cc.ps1 tiers a3_tiers_requests.jsonl.",
   "2026-10-28", blocked_by="Uzair: live tier run (DEC-02 approved)")
it("AUD-39", "AUD", "AB-08 Name-reliance benchmark with a rho dial (decoupled semantics, B2)", "done",
   "Must show: rho curve per method; benchmark card. Gate: generator's own sortability and layout reported; columns always shuffled",
   ["analysis/b2_generator.py", "analysis/b2_score.py", "analysis/b2_reference_methods.py", R + "ab08_benchmark_card.md", RS + "b2/b2_reference_scores.json",
    RS + "b2/b2_sortability.json", RS + "b2/CONTRACT.json", "tests/test_b2_generator.py"],
   ['J("analysis/results/b2/b2_reference_scores.json", ["methods", "names_oracle", "by_track_rho", "linear", "1.00", "f1_data_mean"], "eq", 0.0)',
    'G("analysis/reports/ab08_benchmark_card.md", r"[Ll]imitations")'],
   "Benchmark built and validated (2,500 files, 257.7 MB, outside git under external/b2_namereliance; manifest sha256). P11 holds for the reference methods; agent curves come from AB-06.",
   "2026-11-14")
it("AUD-40", "AUD", "AB-09 Theory pack: identity, error budget, bounded harm, conflict-rule order dependence, DV ceiling", "done",
   "Must show: proof notes; numerical checks. Gate: no statement beyond what the references support",
   ["analysis/theory_checks.py", RS + "theory/theory_checks.json", RS + "theory/CONTRACT.json", R + "ab09_theory_pack.md", "tests/test_theory.py"],
   ['J("analysis/results/theory/theory_checks.json", ["P12_holds_as_restated"], "true")'],
   "T1-T4 hold as stated; T5 restated (coverage = constant-answer share minus definite causes without a directed path). F1 = S x a holds per file, not for family means (corrects the AUD-28 wording).",
   "2026-11-07")
it("AUD-41", "AUD", "AB-10 Practitioner interviews (C1)", "blocked",
   "Must show: interview synthesis with quotes paraphrased. Gate: notes stored without personal data beyond role and sector",
   ["docs/interviews/human_subjects_check.md", "docs/interviews/guide.md", "docs/interviews/screener.md", "docs/interviews/consent_script.md",
    "docs/interviews/notes_schema.json", "docs/interviews/synthesis_plan.md", "analysis/interview_synthesis.py", "tests/test_interview_synthesis.py"],
   ['G("docs/interviews/human_subjects_check.md", r"generalizable knowledge")'],
   "Interview kit ready. First Uzair asks course staff whether an IRB determination is needed (path a: course-internal; path b: determination before the first interview).",
   "2026-11-07", blocked_by="Uzair: course-staff question, then recruiting and interviews")
it("AUD-42", "AUD", "AB-11 Competitive teardown: open tools hands-on, closed tools by documented claims", "done",
   "Must show: teardown table. Gate: vendor claims never presented as measurements",
   ["analysis/audits/AB11_vendor_claims.md", "analysis/audits/AB11_vendor_claims.json", "analysis/ab11_teardown_run.py", "analysis/ab11_ledger_adapters.py",
    RS + "teardown/teardown.json", RS + "teardown/CONTRACT.json", "tests/test_ab11_adapters.py"],
   ['G("analysis/audits/AB11_vendor_claims.md", r"Hands-on results")', 'J("analysis/results/teardown/teardown.json", ["tools"], "len_eq", 10)'],
   "33 tools by documentation, 10 run by hand. P14 strong form survives narrowed: no tool stores a per-direction source linked to evidence (CausalNex 'origin' and Tetrad verbose text are partial).",
   "2026-10-31")
it("AUD-43", "AUD", "AB-12 Vertical probe: root-cause analysis", "done",
   "Must show: RCA table; what a ledger adds here. Gate: datasets reachable",
   ["analysis/ab12_rca_probe.py", RS + "rca/rca_probe.json", RS + "rca/ab12_prereg.json", RS + "rca/CONTRACT.json", R + "ab12_rca_probe.md"],
   ['J("analysis/results/rca/rca_probe.json", ["P15", "verdict"], "eq", "supported")'],
   "PetShop test (48 issues): declared topology + abstention AC@3 0.93 at coverage 0.92 vs learned-graph (PC) 0.21; P15 supported, almost all of the gap from topology.",
   "2026-11-07")
it("AUD-44", "AUD", "AB-13 Regulation and standards map: requirement -> ledger field", "done",
   "Must show: requirement -> field matrix. Gate: primary texts only; summaries labelled second-hand",
   ["analysis/audits/AB13_regulation_map.md", "analysis/audits/AB13_regulation_map.json"],
   ['J("analysis/audits/AB13_regulation_map.json", ["rows"], "len_eq", 50)', 'G("analysis/audits/AB13_regulation_map.md", r"What this changes")'],
   "50 requirements, 21 texts; five ledger gaps ranked (plan/deviations, assumptions, lineage, reviews, question/context: BLD-14). Venue: W3C AI Computed Provenance CG.",
   "2026-10-24")
it("AUD-45", "AUD", "AB-14 Market and go-to-market hypotheses for two verticals", "todo",
   "Must show: two one-page vertical briefs. Gate: no number without its inputs",
   ["docs/market/README.md"], [], "Scaffolding only; waits on AB-10 interviews and uses AB-11 pricing signals.", "2026-11-12", blocked_by="AUD-41")
it("AUD-46", "AUD", "AB-15 Positioning closure: novelty matrix for L1-L5", "done",
   "Must show: novelty matrix. Gate: every claim of novelty bounded by the searches recorded",
   ["analysis/audits/AB15_positioning.md", "analysis/audits/AB15_positioning.json"],
   ['J("analysis/audits/AB15_positioning.json", ["rows"], "len_eq", 45)', 'J("analysis/audits/AB15_positioning.json", ["novelty_matrix"], "len_eq", 5)'],
   "All five claims partly open. Must cite Colombo & Maathuis 2014 (scoops PC order dependence), CARE (single-system name collapse), Li & Russo 2026 (orient-only LLM knowledge).",
   "2026-10-22")

new_bld = ("item('BLD-14', 'BLD', 'Claim ledger v0.2: plan and deviations, assumptions, lineage, reviews, question; verifier reports every check', 'todo', kind='task',\n"
           "     criterion='Fields for the five gaps AB-13 ranks (plan fixed before data with deviations; identifying assumptions and sensitivity; data lineage pointer; human review records; question / context of use / estimand), "
           "the AB-11 findings (verifier reports V2-V8 even when V1 fails; a y->x relation or an explicit orientation convention; knowledge-file import records required edges on unconnected pairs as overrides), each with a verifier test',\n"
           "     evidence=['analysis/audits/AB13_regulation_map.md', 'analysis/audits/AB11_vendor_claims.md'], checks=[], note='Found 2026-10-13 by AB-11 and AB-13.'),\n")

block = "# ---- audit program results (p02, 2026-10-13)\n"
for tid, text in ITEMS.items():
    pat = re.compile(r"^item\(%r, .*$\n" % tid, re.M)
    m = pat.search(s)
    assert m, tid
    s = s[:m.start()] + text + "\n" + s[m.end():]
s = s.replace("# ---- audit program (plans/audit_dag.json, approved 2026-10-12)\n", "# ---- audit program (plans/audit_dag.json, approved 2026-10-12; results p02 2026-10-13)\n" + block)
anchor = "# ---------------- 9 Evaluation protocol"
assert s.count(anchor) == 1
s = s.replace(anchor, new_bld + anchor)
STAT = {"AB-01": "done", "AB-02": "blocked", "AB-03": "done", "AB-04": "done", "AB-05": "blocked", "AB-06": "todo", "AB-07": "blocked", "AB-08": "done",
        "AB-09": "done", "AB-10": "blocked", "AB-11": "done", "AB-12": "done", "AB-13": "done", "AB-14": "todo", "AB-15": "done", "AB-16": "todo", "AB-17": "todo"}
NOTE = {"AB-01": "Controlled leaderboard written; see ab01 report.",
        "AB-02": "gCastle alarm: no causal order. Waits on Uzair: Bayesys download.",
        "AB-03": "dodiscover PC fails the oracle test (cyclic output); pgmpy, tigramite correct.",
        "AB-04": "Five benchmarks; learned graphs near 'nothing moves' on CausalArena, clearer lift on Causal Chambers.",
        "AB-05": "Stub runs pass for 4 agents; waits on Uzair: live probes (caps $3.55 + $0.03).",
        "AB-06": "Budget proposed (~$57); needs AB-05 live costs, then approval.",
        "AB-07": "900 requests pre-registered (~$3.1). Waits on Uzair: cc.ps1 tiers.",
        "AB-08": "2,500-file rho-dial benchmark; reference curves as predicted.",
        "AB-09": "T1-T4 hold; T5 restated; 7,151 rows checked.",
        "AB-10": "Kit ready. Waits on Uzair: IRB question to course staff, then interviews.",
        "AB-11": "33 tools by docs, 10 by hand; no tool records evidence-linked direction sources.",
        "AB-12": "PetShop: declared topology + abstention 0.93 AC@3 vs PC graph 0.21 (P15 supported).",
        "AB-13": "50 requirements mapped; 5 ledger gaps (BLD-14); venue W3C AI provenance CG.",
        "AB-14": "Scaffold only; waits on AB-10.",
        "AB-15": "All five claims partly open; mandatory citations listed.",
        "AB-16": "Gate on 14 Nov.", "AB-17": "After AB-16."}
old_bs = "\nBUNDLE_NOTE = {"
assert s.count(old_bs) == 1
s = s.replace(old_bs, "\nBUNDLE_STATUS.update(%r)\n" % STAT + old_bs)
s = s.rstrip("\n") + "\nBUNDLE_NOTE.update(%r)\n" % NOTE
p.write_text(s, encoding="utf-8")
print("catalogue: %d audit tickets updated, BLD-14 added, AB statuses and notes set" % len(ITEMS))
