"""The goals tracker: every item as a ticket with a stable ID, a closing criterion and machine-checkable evidence.

Edit this file to add, change or close items; then run `python tracker/verify.py`. Never reuse an ID.
Status values: done, in_progress, todo, blocked, open (see README.md for the meaning and the emoji).
Kinds: task, target, question, decision, rule, deadline, risk, stretch.
Evidence paths: relative to cc-research/ ; "repo:" = relative to ../Causal-Copilot ; "project:" = claude.ai project doc ;
"slack:CHANNEL[/TS]" / "url:" / "chat:" = pointers that cannot be checked from here. Typed links between tickets: links.txt (LINKS.md).
Check types (see verify.py): json, exists, absent, grep, runs (optionally restricted to a manifest), manifest.
A done ticket must never pin a growing collection (a whole directory, runs/*): pin a dated manifest under manifests/evidence/ instead.
"""

P4B = "analysis/results/stability_p4b/stability.json"
B1 = "analysis/results/stability_b1/stability.json"
PS = "analysis/results/stability_b1/partial_stages.json"
LS = "analysis/results/stability_b1/neutral_leak_scan.json"
EB = "analysis/results/error_budget/error_budget.json"
OV = "analysis/results/error_budget/order_value.json"
CAL = "analysis/results/causalarena_calibration/"
OB, SO, PCC, COC, DMC = CAL + "order_baseline.json", CAL + "sortability.json", CAL + "pc_calibration.json", CAL + "column_order_check.json", CAL + "dataset_match_check.json"
OFF = "analysis/results/offline/refinement_offline_seeds_summary.json"
INV = "analysis/results/llm_inventory/llm_inventory.md"
FR = "external/FETCH_REPORT.json"
LB = "external/causalarena/results/tables/main/main_leaderboard_f1_wide_with_std.csv"
RL = "external/causalarena/results/tables/real/real_method_summary.csv"
R = "analysis/reports/"
SNAP = "docs/project_snapshots/2026-10-09/"
LED = SNAP + "causal-copilot-research-ledger.md"
B3 = "analysis/reports/bnd03/"
LB2 = "analysis/literature/bnd02/"
CIT = "analysis/results/bnd03_citations.json"
PROT = "analysis/results/causalarena_calibration/protocol_check.json"
MV = "analysis/results/methods/"
IA = "analysis/results/intervention_audit/intervention_audit.json"


def J(path, ptr, op, v=None, tol=None):
    return {"t": "json", "path": path, "ptr": ptr, "op": op, "v": v, "tol": tol}


def G(path, pattern):
    return {"t": "grep", "path": path, "pattern": pattern}


def item(id, cat, title, status, kind="task", criterion="", evidence=(), checks=(), reproduce="", reopen_if=(), due=None, blocked_by=None, note=""):
    return dict(id=id, cat=cat, title=title, status=status, kind=kind, criterion=criterion, evidence=list(evidence),
                checks=list(checks), reproduce=reproduce, reopen_if=list(reopen_if), due=due, blocked_by=blocked_by, note=note)


CATS = {"DLV": "0 Quarter 1 deliverables", "REP": "1 Replication", "DOM": "2 Domain exploration", "AUD": "3 Audit: Causal-Copilot", "BEN": "4 Audit: benchmarks and data",
        "TGT": "5 Targets", "CAP": "6 Required capabilities", "RQ": "7 Research questions", "BLD": "8 Build", "EVL": "9 Evaluation protocol",
        "INF": "10 Infrastructure", "CRS": "11 Course", "TEAM": "12 Team and communication", "EXT": "13 External outputs",
        "STR": "14 Stretch", "DEC": "15 Decisions", "RSK": "15 Risks", "BND": "16 Bundles"}

CODE_ID = "the Causal-Copilot tree stops matching manifests/baseline_a31aa7c.sha256"

ITEMS = [
# ---------------- 0 Quarter 1 deliverables: run Causal-Copilot on chosen datasets; rigorous exploration and refinement within them
item("DLV-01", "DLV", "Q1 dataset suite: the datasets Causal-Copilot is run on, frozen, with a card per dataset", "done",
     criterion="docs/q1/datasets.md holds one card per dataset (source, reference graph and how far it can be trusted, variables, rows, "
               "why chosen, sha256 of every arm) and the suite is declared frozen",
     evidence=["docs/q1/datasets.md", "manifests/evidence/suite_q1_2026-10-10.sha256", "datasets/suite_q1s2/MAPPING.json",
               "analysis/make_suite_ca.py", "analysis/make_dataset_cards.py"], due="2026-11-02",
     checks=[G("docs/q1/datasets.md", r"\*\*Status: frozen\.\*\* Manifest `manifests/evidence/suite_q1_2026-10-10\.sha256`"),
             {"t": "count", "glob": "datasets/suite_q1s2/q*/q*.csv", "eq": 30}]
            + [J("datasets/suite_q1s2/MAPPING.json", ["gates", "s2_%02d" % _k], "true") for _k in range(1, 11)],
     reproduce="python analysis/make_suite_ca.py --check && python analysis/reference_reliability.py && python analysis/make_dataset_cards.py --date 2026-10-10",
     reopen_if=["any file listed in manifests/evidence/suite_q1_2026-10-10.sha256 changes (F9)"],
     note="S1: Sachs (4 arms) and abalone, Auto MPG, concrete, DWD (3 arms each). S2: 10 CausalArena semantic test scenarios, "
          "columns shuffled, real/neutral/swapped, gates D1-D11 pass. One swapped labelling (s2_03) is the best found within the "
          "search budget (2 shared pairs), not proved minimal; recorded in its card."),
item("DLV-02", "DLV", "Q1 runs: Causal-Copilot run unmodified on every suite dataset under name controls, fully recorded", "in_progress",
     criterion="Every dataset in the frozen suite has completed live runs in each name arm (real, neutral, moved), every run recorded "
               "and the code tree verified before and after",
     evidence=["runs/*/meta.json", "plans/results/"], checks=[{"t": "runs", "live": True, "tree_ok": True}],
     note="Recorded: 84 live runs on S1 (Sachs + 4 bundle-1 families) and 30 on S2 (11-12 Oct). Gap: 6 S2 arms (q011, q033, q041, q051, "
          "q071, q101) have no completed run; their only run crashed at the cycle step and is scored at S3. Closing needs Uzair's choice: rerun "
          "those 6 (about $2.5; likely to crash again) or restate the criterion as 'reached S3'."),
item("DLV-03", "DLV", "Q1 exploration: what Causal-Copilot does to the graph on these datasets, stage by stage", "in_progress",
     criterion="A report section giving, per dataset and name arm, the score at each stage (S0-S4), which step set each final edge, "
               "crashes and stability, with every number tied to a tracker check",
     evidence=["analysis/reports/bundle1_results.md", "analysis/reports/pass4b_results.md", "analysis/reports/bnd08_s2_results.md"],
     note="Measurements exist for S1 (AUD-03 to AUD-09, RQ-01 to RQ-03) and S2 (AUD-10, stage table per arm); the Q1 write-up is not done."),
item("DLV-04", "DLV", "Q1 refinement research: a refinement step that never falls below its own algorithm on these datasets", "todo",
     criterion="A refinement variant evaluated on the frozen suite under the same controls: adjacency F1 never below the algorithm's "
               "output, no crashes from malformed model output, every LLM-set edge labelled with its source"),
item("DLV-05", "DLV", "Q1 checkpoint (Mon 2 Nov)", "todo", kind="deadline", due="2026-11-02",
     criterion="Checkpoint submitted, covering the frozen suite (DLV-01), the runs (DLV-02) and the exploration so far (DLV-03)"),
item("DLV-06", "DLV", "Q1 final: replication-style report on Causal-Copilot over the Q1 datasets (Fri 4 Dec)", "todo", kind="deadline", due="2026-12-04",
     criterion="Report covering DLV-01 to DLV-04, every number reproducible from cc-research with the command named next to it"),
# ---------------- 1 Replication
item("REP-01", "REP", "Run Causal-Copilot a31aa7c unmodified end to end with GPT-4o, fully recorded", "done",
     criterion="At least one completed live run per pass; every run has meta.json, llm_calls.jsonl, artifacts and state snapshots",
     evidence=["manifests/evidence/plans_results_2026-10-09.sha256", "manifests/evidence/runs_live_2026-10-09.sha256"],
     checks=[{"t": "runs", "live": True, "manifest": "manifests/evidence/runs_live_2026-10-09.sha256", "expect_total": 84, "expect_completed": 72},
             {"t": "manifest", "path": "manifests/evidence/runs_live_2026-10-09.sha256"}, {"t": "manifest", "path": "manifests/evidence/plans_results_2026-10-09.sha256"}],
     reproduce="cc.ps1 plan <plan file> (spends API credit)", reopen_if=[CODE_ID]),
item("REP-02", "REP", "Code untouched before and after every run (1,332 files byte-identical)", "done",
     criterion="Every live run's meta.json records tree_identity_after.ok and no unexpected files in the repo",
     evidence=["manifests/baseline_a31aa7c.sha256", "manifests/evidence/runs_live_2026-10-09.sha256"],
     checks=[{"t": "runs", "live": True, "tree_ok": True}, {"t": "manifest", "path": "manifests/evidence/runs_live_2026-10-09.sha256"}],
     reproduce="cd Causal-Copilot && sha256sum -c ../cc-research/manifests/baseline_a31aa7c.sha256", reopen_if=[CODE_ID]),
item("REP-03", "REP", "Reproduce the paper's headline claims (arXiv 2504.13263)", "in_progress",
     criterion="Each headline claim marked reproduced / not reproducible (with the reason) / not attempted",
     evidence=[B3 + "rep03_headline_claims.md", R + "pass4b_results.md", "project:claude/causal-copilot-research-ledger.md (I1, F17, F18, F19)",
               "repo:causal_discovery/evaluation/benchmarking_integrated.py", "repo:causal_discovery/tests/benchmarking_config.py"],
     checks=[G("repo:causal_discovery/tests/benchmarking_config.py", r"heavy_benchmarking_v6"), G(B3 + "rep03_headline_claims.md", r"\| 22 \|"),
             J(CIT, ["files", "rep03_headline_claims.md", "unresolved_citations"], "len_eq", 0)],
     note="22 claims tabled (BND-03): none reproducible from the repo (data absent; the scorer scores pre-refinement output and orients "
          "non-directed edges from the truth, evaluator.py:154-215). Live-only claims stay 'not attempted' until BND-08/12."),
item("REP-04", "REP", "Check the paper's text against the code (divergences D1-D9)", "done",
     criterion="Every methods-section claim about refinement and error handling checked against code and runs",
     evidence=[B3 + "rep04_paper_vs_code.md", CIT, "project:claude/causal-copilot-research-ledger.md (PAPER-vs-CODE)", R + "pass3_llm_dependency_map.md"],
     checks=[G("repo:postprocess/judge_functions.py", r"return response\['nodes'\]"), G(B3 + "rep04_paper_vs_code.md", r"D23"),
             J(CIT, ["files", "rep04_paper_vs_code.md", "unresolved_citations"], "len_eq", 0),
             J(CIT, ["files", "rep04_paper_vs_code.md", "uncited_findings"], "len_eq", 0)],
     reproduce="python analysis/check_citations.py analysis/reports/bnd03/*.md docs/q1/scope_note.md",
     note="Full pass over the methods sections (BND-03): 45 claims, divergences D10-D23 added to D1-D9; every code citation resolves in the a31aa7c tree (gate A1)."),
item("REP-05", "REP", "Reproduce CausalArena's published PC baseline (scorer calibration, F1)", "done",
     criterion="Published configuration on the 250 public semantic files; mean F1 within 3 standard errors of 0.333",
     evidence=[PCC, "analysis/causalarena_pc_calibration.py", LB],
     checks=[J(PCC, ["gate_C1_official_configuration_reproduces_published_F1"], "true"), J(PCC, ["complete"], "true")],
     reproduce="python analysis/causalarena_pc_calibration.py --root external/causalarena --out analysis/results/causalarena_calibration (resumable, about 10 min)",
     reopen_if=["CausalArena release files change", "their evaluation code shows a different orientation rule"]),
item("REP-06", "REP", "Explain why SHD does not reproduce (ours 37.5, published 33.5)", "done", kind="question",
     criterion="A definition or data difference identified that accounts for the gap, or a documented reason it cannot be settled",
     evidence=[PCC, PROT, "analysis/causalarena_protocol_check.py", LB2 + "dom07_deep_reads.md"],
     checks=[J(PCC, ["gate_C2_official_configuration_reproduces_published_SHD"], "false"), J(PROT, ["verdict", "shd_reproduced_under_code_rule"], "true"),
             J(PROT, ["verdict", "f1_reproduced_under_code_rule"], "false"), J(PROT, ["verdict", "any_rule_reproduces_both"], "false"),
             J(PROT, ["facts", "P2_liberal_orientation", "found"], "true")],
     reproduce="python analysis/causalarena_protocol_check.py --clone $HOME/scratch/tabcausal",
     note="Not settleable from public data. The authors' baseline code orients undecided CPDAG edges lower index -> higher ('liberal', "
          "TabCausal run_pc.py) and counts a reversal once; under that rule our SHD is 35.43 (within 2.81 of 33.52) but F1 0.396 "
          "(published 0.333, tolerance 0.045); under random orientation F1 matches and SHD does not. The published means also cover "
          "50 unreleased scenarios. The paper's appendix B (which states the rule) could not be read."),
item("REP-07", "REP", "Reproduce more published CausalArena rows: GES/GIES, FCI, LiNGAM, NOTEARS, AVICI, CDFM (CPU)", "in_progress",
     criterion="Each row within tolerance of the published mean, or the gap explained",
     evidence=[MV + "bnd06_verdicts.json", MV + "bnd06_families.json", R + "bnd06_interim.md", R + "bnd06_families.md", R + "bnd04_results.md"],
     checks=[J(MV + "bnd06_verdicts.json", ["methods", "lingam", "vs_published_authors_rule", "f1_within"], "true"),
             J(MV + "bnd06_c1_recheck.json", ["gate_C1_published_PC_F1_reproduced"], "true")],
     note="Semantic: LiNGAM within; GIES within where GES runs; NOTEARS F1 gap unexplained. Formula: LiNGAM and NOTEARS within; GES within "
          "after excluding its 18 singular-matrix scenarios; PC 0.304 vs 0.220 (upstream causal-learn PC raises on 72 formula files; scored "
          "empty that gives 0.218, consistent, not proof). Synthetic100: LiNGAM within; PC within under the authors' rule; GES 29 timeouts; "
          "NOTEARS 0.177 vs 0.276 unexplained. AVICI blocked: its checkpoint is only on huggingface.co, which the egress allowlist blocks. CDFM not run."),
item("REP-08", "REP", "Reproduce the R2-sortability analysis (Reisach et al. 2023) on CausalArena", "done",
     criterion="R2-sortability and R2-SortnRegress computed on all public semantic and formula files",
     evidence=[SO, "analysis/causalarena_sortability.py"],
     checks=[J(SO, ["semantic", "scenarios"], "eq", 50), J(SO, ["formula", "scenarios"], "eq", 50),
             J(SO, ["semantic", "r2_sortability_mean"], "approx", 0.571, 0.001)],
     reproduce="python analysis/causalarena_sortability.py --root external/causalarena --out analysis/results/causalarena_calibration"),
item("REP-09", "REP", "Reproduce the Causal Chambers authors' GES baseline and CDFM's chamber score", "done",
     criterion="Within the reported ranges on the same subgraph, or the difference explained",
     evidence=["analysis/rep09_ges.py", "analysis/results/chambers/rep09_ges.json", "analysis/reports/bnd07_chambers.md", "manifests/evidence/chambers_extracted_2026-10-12.sha256"],
     checks=[J("analysis/results/chambers/rep09_ges.json", ["verdict"], "eq", "supported"), J("analysis/results/chambers/rep09_ges.json", ["ours", "cpdag_identical_to_authors"], "true")],
     note="GES (BIC, forward/backward/turning) on lt uniform_reference, 10,000 rows, the authors' 20 variables: CPDAG identical to the "
          "authors'; 12 DAGs, precision 0.55-0.60, recall 0.564-0.615 (reported 0.55-0.60 / 0.56-0.62). CDFM's 0.727 recorded as not "
          "reproducible here: checkpoint only on huggingface.co (blocked by the egress allowlist) and its chamber protocol not pinned."),
item("REP-10", "REP", "Reproduce CARE's moved-names control on one classic graph", "todo",
     criterion="Our protocol gives the same direction of effect as CARE's on the same graph and model family"),
item("REP-11", "REP", "Reproduce Kitson & Constantinou's Sachs numbers (0.61 / 0.40 / 0.73)", "in_progress",
     criterion="Within their reported values, or the difference explained",
     evidence=["analysis/rep11_sachs_data.py", "analysis/results/rep11/rep11_sachs_data.json", "analysis/reports/rep11_sachs_data.md"],
     checks=[J("analysis/results/rep11/rep11_sachs_data.json", ["verdicts", "ensemble_f1_primary_B", "verdict"], "eq", "reproduced")],
     note="Data part (no LLM) reproduced within 0.05 with Python stand-ins for bnlearn/Tetrad: ensemble F1 0.647 vs 0.606, single-run mean "
          "0.259 vs 0.293; merge, DAG conversion and F1 cross-checked against the authors' PyPI code (identical). Conditional: Sachs has no "
          "data-identifiable direction, so the ensemble's arrows come from Tabu-Stable's orientation. Open: LLM 0.40 and fused 0.73 (BND-12, live)."),
item("REP-12", "REP", "Reproduce CausalSteward's external score for Causal-Copilot (F1 0.08 at 53 variables)", "open", kind="question",
     criterion="CausalMan data obtained and the run scored, or recorded as unobtainable", evidence=[LB2 + "rep12_causalman.md"],
     note="Obtainable (BND-02): Zenodo record 13871097, CC BY 4.0, 11.2 GB; published score F1 0.078 (std 0.012), FCI on the 53-node set. "
          "Not downloaded; a live run is a Q2 candidate."),
item("REP-13", "REP", "Re-read every second-hand literature claim before it enters the report", "done",
     criterion="Every claim marked A in the reports either re-read in the primary source (marked V) or removed",
     evidence=[LB2 + "rep13_claims.md", LB2 + "rep13_claims.json", R + "pass6_literature_map.md", R + "pass7_framing_test_and_candidates.md"],
     checks=[J(LB2 + "rep13_claims.json", [], "len_eq", 72), G(R + "pass6_literature_map.md", r"As of 2026-10-10 no A claims remain"),
             G(R + "pass6_literature_map.md", r"## Verification update \(2026-10-10, REP-13\)"),
             G(R + "pass7_framing_test_and_candidates.md", r"Verification update \(2026-10-10, REP-13\)")],
     note="72 claims: 55 confirmed, 17 corrected (corrections written into pass 6 and pass 7, superseding the text), 0 removed; Friedman et al. "
          "UAI 1999 confirmed separately. Read through a summarising fetch tool: quotes to be checked against the PDF before a mentor or course document."),
# ---------------- 2 Domain
item("DOM-01", "DOM", "Theory baseline: identifiability, finite samples, untestable assumptions; what 'perfect' means", "done",
     criterion="Written down with the measurement axes",
     evidence=["project:claude/causal-copilot-ceiling-and-positioning.md", R + "pass5_identifiability_vs_encoding.md"],
     checks=[{"t": "exists", "path": R + "pass5_identifiability_vs_encoding.md"}]),
item("DOM-02", "DOM", "Literature map in 9 clusters", "done",
     criterion="One saved report per cluster plus a synthesis",
     evidence=[R + "pass6_literature_map.md", "manifests/evidence/DOM-02_analysis_literature_agent_reports_2026-10-10.sha256"],
     checks=[{"t": "count", "glob": "analysis/literature/agent_reports/cluster*.md", "eq": 9}],
     note="Agent reports are second-hand (A) until re-read; see REP-13."),
item("DOM-03", "DOM", "Benchmark landscape and what '100%' means on each", "done",
     evidence=[SNAP + "benchmark-targets.md", "project:claude/benchmark-targets.md"], checks=[G(SNAP + "benchmark-targets.md", r"Better targets")], criterion="Each benchmark: truth source, size, best result, agents evaluated, name control"),
item("DOM-04", "DOM", "Nearest prior work for each claim we might make", "done",
     evidence=[R + "program_v2.md", "analysis/literature/agent_reports/cluster6_evidence_fusion_and_warrants.md",
               "analysis/literature/agent_reports/cluster8_benchmark_leakage_and_ceilings.md"],
     checks=[G(R + "program_v2.md", r"Position against the nearest work")], criterion="A positioning table naming what each nearest work does and does not do"),
item("DOM-05", "DOM", "Commercial landscape, first pass", "done",
     evidence=["docs/project_snapshots/2026-10-10/causal-copilot-ceiling-and-positioning.md", "project:claude/causal-copilot-ceiling-and-positioning.md (section 4)"],
     checks=[G("docs/project_snapshots/2026-10-10/causal-copilot-ceiling-and-positioning.md", r"## 4\. Value"),
             G("docs/project_snapshots/2026-10-10/causal-copilot-ceiling-and-positioning.md", r"Buyers pay for decisions, not graphs")],
     criterion="Who pays, for what decision"),
item("DOM-06", "DOM", "Weighing against the WorldReset forecasting project", "done",
     evidence=["docs/project_snapshots/2026-10-10/causal-vs-worldreset-weighing.md", "project:claude/causal-vs-worldreset-weighing.md"],
     checks=[G("docs/project_snapshots/2026-10-10/causal-vs-worldreset-weighing.md", r"## Course constraints"),
             G("docs/project_snapshots/2026-10-10/causal-vs-worldreset-weighing.md", r"## Weighing")],
     criterion="Written comparison on course constraints, feasibility and value"),
item("DOM-07", "DOM", "Deep reads: CausalDS, CARE, CausalArena appendices B-C, ACI scoring, Li & Russo implementation", "in_progress",
     criterion="Notes per work with quotes checked against the primary text", evidence=[LB2 + "dom07_deep_reads.md", PROT],
     note="CausalDS, CARE, ACI, Li & Russo done. CausalArena appendices B-C could not be read (HTML stops in section 6.2, PDF text empty); "
          "the scoring protocol was taken from the authors' baseline code instead (protocol_check.json). Closes when appendix B is read."),
item("DOM-08", "DOM", "Choose a calibration method for bootstrap confidence", "done", criterion="Method chosen with the evidence for it",
     evidence=[LB2 + "dom08_calibration_choice.md"], checks=[G(LB2 + "dom08_calibration_choice.md", r"## Recommendation")],
     note="Platt scaling fitted with whole scenarios held out (5 folds); raw frequency as the baseline; isotonic as a diagnostic; conformal deferred; Brier score primary."),
item("DOM-09", "DOM", "What is practical for 'what if we set X?' at 20-40 variables (IDA, adjustment on CPDAG/PAG, bounds)", "done",
     criterion="Short survey with run times on one 25-variable scenario",
     evidence=["analysis/literature/dom09_what_if.md", "analysis/dom09_ida_timing.py", "analysis/results/dom09/ida_timing.json"],
     checks=[J("analysis/results/dom09/ida_timing.json", ["variables"], "eq", 25), J("analysis/results/dom09/ida_timing.json", ["ordered_pairs"], "eq", 600)],
     note="Local IDA on PC's CPDAG at 25 variables: 600 pairs in 0.06 s; 52% identified within the class; true parents among the candidates "
          "for only 7 of 25 X. Computation is not the obstacle; skeleton recall is."),
item("DOM-10", "DOM", "Active experiment-design baselines: which to implement", "done", criterion="Two baselines chosen with code located",
     evidence=[LB2 + "dom10_active_design_baselines.md"], checks=[G(LB2 + "dom10_active_design_baselines.md", r"github\.com/yannadani/cbed")],
     note="CBED (MIT, Python/JAX) and pcalg::opt.target (GPL, R). R is not installable in either sandbox (CRAN blocked); recorded for Q2."),
item("DOM-11", "DOM", "Pretrained discovery models: order-invariance by design, CPU checkpoints", "done",
     criterion="Table per model, checked against code, not abstracts", evidence=[LB2 + "dom11_pretrained_models.md"],
     checks=[G(LB2 + "dom11_pretrained_models.md", r"AVICI")],
     note="Only AVICI, FoundCause and Arrow state variable-order equivariance; Arrow has no released weights; TabCausal, SEA and CauScale code carry no licence."),
item("DOM-12", "DOM", "Hidden common causes, time series, 100+ variables", "done", kind="stretch",
     criterion="Scoping note: what Causal-Copilot offers for hidden confounders, time series and 100+ variables, what Q1 covers, what moves to Q2",
     evidence=["docs/q1/scope_note.md", B3 + "dom12_scope_code_facts.md", CIT],
     checks=[J(CIT, ["files", "scope_note.md", "uncited_findings"], "len_eq", 0), J(CIT, ["files", "dom12_scope_code_facts.md", "unresolved_citations"], "len_eq", 0)],
     note="Proposal: Q1 measures what happens to PAG marks; time series and 100+ variables move to Q2. G1 (16 Oct) confirms or changes it."),
# ---------------- 3 Audit Causal-Copilot
item("AUD-01", "AUD", "Architecture map: 8-step CLI path, state object, LLM call points, storage", "done",
     criterion="Facts F1-F30 in the ledger, each with file:line", evidence=[LED, "project:claude/causal-copilot-research-ledger.md (FACTS)"],
     checks=[G(LED, r"F1\. Entry points"), G(LED, r"F30\.")],
     note="Only in the ledger; no standalone report in cc-research.", reopen_if=[CODE_ID]),
item("AUD-02", "AUD", "LLM dependency map: 51 call sites, 88 logical points, 29 decisions, 3 graph-writing points", "done",
     criterion="Static scan reconciled with recorded calls; gates G1-G4 pass",
     evidence=[INV, "analysis/results/llm_inventory/llm_inventory.csv", R + "pass3_llm_dependency_map.md"],
     checks=[G(INV, r"G1_ast_matches_text: \*\*PASS"), G(INV, r"G2_all_points_classified: \*\*PASS"),
             G(INV, r"G3_every_recorded_caller_is_a_known_site: \*\*PASS"), G(INV, r"G4_recorded_flags_match_static: \*\*PASS"),
             G(INV, r"Call sites that issue a request \(AST\): 51")],
     reproduce="python analysis/llm_inventory_scan.py && python analysis/llm_inventory_build.py", reopen_if=[CODE_ID]),
item("AUD-03", "AUD", "Edge lineage tool: every final edge traced to the step that set it", "done",
     criterion="Lineage gates A-F pass on every completed run analysed",
     evidence=["analysis/lineage.py", "manifests/evidence/AUD-03_analysis_results_lineage_2026-10-10.sha256", "manifests/evidence/AUD-03_analysis_results_stability_b1_lineage_2026-10-10.sha256", B1],
     checks=[J(B1, ["gates", "T5_scores_recomputed_equal_lineage"], "true"), J(P4B, ["gates", "T5_scores_recomputed_equal_lineage"], "true")],
     reopen_if=[CODE_ID]),
item("AUD-04", "AUD", "Refinement audit without the LLM: bootstrap step deletes non-directed edges", "done",
     criterion="Offline cells over seeds 0-2 complete (gate S1); live: S1 below S0 in every bundle-1 arm",
     evidence=[OFF, "analysis/results/offline/refinement_offline_seeds.md", R + "pass4a_edge_lineage.md", B1],
     checks=[J(OFF, ["gate_S1"], "true")],
     reproduce="python analysis/refinement_offline.py ... (see analysis/README.md)", reopen_if=[CODE_ID]),
item("AUD-05", "AUD", "Name controls on 5 datasets: real 93% / neutral 0% / moved 90% of final edges written by the LLM", "done",
     criterion="Pre-registered predictions evaluated by stability.py with gates T1-T6 passing",
     evidence=[P4B, B1, R + "pass4b_results.md", R + "bundle1_results.md"],
     checks=[J(P4B, ["predictions", "P1", "verdict"], "eq", "SUPPORTED"), J(B1, ["predictions", "N2", "verdict"], "eq", "SUPPORTED"),
             J(B1, ["gates", "T2_min_runs_per_arm"], "true")],
     reproduce="python analysis/stability.py --runs-dir runs --label b1 --mapping datasets/suite_b1/MAPPING.json --repo <repo> --out analysis/results/stability_b1",
     reopen_if=["new runs with label b1 or p4b are added"]),
item("AUD-06", "AUD", "Reliability: 12 of 84 runs crashed; cycle step failed 9 of 9; one request got 3 answers", "done",
     criterion="Every failure diagnosed to file:line from run records",
     evidence=[PS, "manifests/evidence/runs_live_2026-10-09.sha256", R + "bundle1_results.md"],
     checks=[{"t": "runs", "live": True, "manifest": "manifests/evidence/runs_live_2026-10-09.sha256", "expect_failed": 12},
             J(PS, ["cycle_step", "of_which_completed"], "eq", 0), J(PS, ["gates", "Q2_cycle_crashes_have_cycle_in_S3"], "true")]),
item("AUD-07", "AUD", "Stability: algorithm choice stable; edge decisions vary; bootstrap seeded by accident; numpy unseeded", "done",
     evidence=[P4B, B1, "project:claude/causal-copilot-research-ledger.md (F8a, F29)"], checks=[J(B1, ["predictions", "P5", "verdict"], "eq", "exploratory")],
     criterion="Per-arm stability tables produced for every arm"),
item("AUD-08", "AUD", "Survivor-bias check: crashed runs do not change conclusions", "done",
     criterion="S3 scores over all runs vs completed only, gates Q1-Q3 pass", evidence=[PS, "analysis/partial_stages.py"],
     checks=[J(PS, ["gates", "Q1_rebuilt_S2_S3_equal_recorded"], "true"), J(PS, ["gates", "Q3_all_runs_accounted"], "true")]),
item("AUD-09", "AUD", "Leak scan of neutral-name arms: no real name in any prompt before the final graph", "done",
     criterion="Gate L1: zero leaks; template text present in every arm is not a leak", evidence=[LS, "analysis/neutral_leak_scan.py"],
     checks=[J(LS, ["gate_L1_no_leak_before_final_graph"], "true"), J(LS, ["requests_scanned"], "ge", 300)],
     reproduce="python analysis/neutral_leak_scan.py --runs-dir runs --label b1 --mapping datasets/suite_b1/MAPPING.json --out analysis/results/stability_b1"),
item("AUD-10", "AUD", "Causal-Copilot on CausalArena's named scenarios (10 x real/neutral/moved, columns shuffled) [A2]", "done",
     criterion="30 runs analysed with T-gates and S3 endpoint",
     evidence=["plans/bnd08_live.json", "analysis/s2_analysis.py", "manifests/evidence/bnd08_prereg_2026-10-11.sha256",
               "analysis/results/stability_s2/s2_verdicts.json", "analysis/results/stability_s2/partial_stages.json", "analysis/results/stability_s2/bnd08_summary.json", "analysis/reports/bnd08_s2_results.md"],
     checks=[J("analysis/results/stability_s2/s2_verdicts.json", ["M2", "verdict"], "eq", "REFUTED"), J("analysis/results/stability_s2/s2_verdicts.json", ["M3", "verdict"], "eq", "SUPPORTED"),
             J("analysis/results/stability_s2/s2_verdicts.json", ["M4", "verdict"], "eq", "SUPPORTED"), J("analysis/results/stability_s2/bnd08_summary.json", ["Q_gates", "Q3_all_runs_accounted"], "true"),
             J("analysis/results/stability_s2/bnd08_summary.json", ["L1_neutral_leak_scan"], "true"), J("analysis/results/stability_s2/bnd08_summary.json", ["all_code_identity_ok"], "true")],
     note="30 live runs 11-12 Oct (gpt-4o-2024-08-06), all reached S3. M2 REFUTED (real-name lift >= 0.10 in 5 of 10 families; mean +0.09), "
          "M3 SUPPORTED (swapped: 81 of 101 LLM-set edges follow labels), M4 SUPPORTED (neutral S3 below plain PC in 8 of 10), M1 SUPPORTED "
          "(dev replay 19 of 23). Without s2_02: M2 5 of 9, INCONCLUSIVE."),
item("AUD-11", "AUD", "Behaviour at 20-40 variables: cost, runtime, crash rate", "done",
     criterion="Measured on a stub run, then on A2's live runs",
     evidence=["plans/bnd08_stub.json", "analysis/stub_cost.py", "analysis/results/stub_cost/bnd08_estimate.json",
               "analysis/reports/bnd08_stub_measurement.md", "analysis/results/stability_s2/bnd08_summary.json", "analysis/reports/bnd08_s2_results.md"],
     checks=[J("analysis/results/stub_cost/bnd08_estimate.json", ["stub_runs"], "len_eq", 6),
             J("analysis/results/stability_s2/bnd08_summary.json", ["cost", "prompt_tokens"], "eq", 3316360),
             J("analysis/results/stability_s2/bnd08_summary.json", ["crashes", "runs_cyclic_by_pipeline_test"], "eq", 6)],
     note="Live at 20-25 variables: 110k prompt + 14.6k completion tokens per run (about $12.7 for 30 at $2.50/$10 per M; the stub estimate "
          "was low because live runs chose FCI, the stub PC); 302-1130 s per run; 6 of 30 crashed at the cycle step (real 5, swapped 1, neutral 0)."),
item("AUD-12", "AUD", "Effect-estimation module (causal_inference/)", "done", criterion="Read and audited like the discovery path",
     evidence=[B3 + "aud12_effect_estimation.md", B3 + "evidence/mt_confounders_output.txt", CIT],
     checks=[J(CIT, ["files", "aud12_effect_estimation.md", "unresolved_citations"], "len_eq", 0), J(CIT, ["files", "aud12_effect_estimation.md", "uncited_findings"], "len_eq", 0),
             G("repo:causal_inference/inference.py", r"def sensitivity_analysis")],
     note="Reachable only from the web demo; causal_inference/main.py is broken (:32, :39); <-> and o-> treated as parents when choosing "
          "confounders (inference.py:242-246, micro-test); 'metalearners' has no wrapper; 'counterfactual' runs an interventional shift."),
item("AUD-13", "AUD", "Second model besides GPT-4o", "todo", criterion="Bundle-1 arms repeated with one other model"),
item("AUD-14", "AUD", "Torch-based and time-series wrappers, web-demo path, report quality", "in_progress",
     criterion="Torch and time-series wrappers, the web-demo path and report generation audited like the discovery path (file:line findings; one stub run where it runs offline)",
     evidence=[B3 + "aud14_wrappers_webdemo_report.md", CIT],
     checks=[J(CIT, ["files", "aud14_wrappers_webdemo_report.md", "unresolved_citations"], "len_eq", 0), J(CIT, ["files", "aud14_wrappers_webdemo_report.md", "uncited_findings"], "len_eq", 0)],
     note="Static audit done (BND-03): CORL crashes program.py (corl.py:93 vs program.py:53); Granger needs integer column names; the CLI "
          "time-series path plots a None revised_graph (main.py:307, code trace); the report's fixed text claims voting and 'top three' "
          "algorithms the code does not do. Still open: one offline stub run of a time-series wrapper."),
item("AUD-15", "AUD", "Upstream branches newer than a31aa7c", "done", criterion="Diff of refinement and crash points against main",
     evidence=[B3 + "aud15_upstream.md", "analysis/results/upstream/upstream_check.json", "analysis/upstream_check.py"],
     checks=[J("analysis/results/upstream/upstream_check.json", ["summary", "main_is_base"], "true"),
             J("analysis/results/upstream/upstream_check.json", ["summary", "branches"], "eq", 19),
             J("analysis/results/upstream/upstream_check.json", ["summary", "branches_without_crash_line", "C2"], "len_eq", 0)],
     reproduce="python analysis/upstream_check.py --clone $HOME/scratch/cc_up",
     reopen_if=["upstream main moves past a31aa7c (re-run the check)"],
     note="Upstream main is still a31aa7c. C1 (cycle step) is a regression from defa4df (2025-06-26), which dropped the structured-output "
          "schema; no branch fixes C1 or C2."),
# ---------------- 4 Benchmarks
item("AUD-18", "AUD", "Field audit: every causal-discovery system, its regimes, order source and evaluation controls", "done", criterion="Typed table with a source on every row, searches and unread sources listed, implications for the project",
     evidence=["analysis/audits/AU1_field_systems.md", "analysis/audits/AU1_field_systems.json"],
     checks=[G("analysis/audits/AU1_field_systems.md", r"What this changes"), J("analysis/audits/AU1_field_systems.json", ["rows"], "len_eq", 75)],
     note="Desk audit, 2026-10-12 (analysis/audits/AUDIT_PROGRAM.md). Sources read that day; second-hand items labelled."),
item("AUD-19", "AUD", "Benchmark audit: ground-truth origin, scored views and leak channels of every benchmark", "done", criterion="Typed table with a source on every row, searches and unread sources listed, implications for the project",
     evidence=["analysis/audits/AU2_benchmarks.md", "analysis/audits/AU2_benchmarks.json"],
     checks=[G("analysis/audits/AU2_benchmarks.md", r"What this changes"), J("analysis/audits/AU2_benchmarks.json", ["rows"], "len_eq", 69)],
     note="Desk audit, 2026-10-12 (analysis/audits/AUDIT_PROGRAM.md). Sources read that day; second-hand items labelled."),
item("AUD-20", "AUD", "Theory audit: identifiability, sample and experiment bounds per cell of Q x R x W", "done", criterion="Typed table with a source on every row, searches and unread sources listed, implications for the project",
     evidence=["analysis/audits/AU3_theory_limits.md", "analysis/audits/AU3_theory_limits.json"],
     checks=[G("analysis/audits/AU3_theory_limits.md", r"What this changes"), J("analysis/audits/AU3_theory_limits.json", ["rows"], "len_eq", 55)],
     note="Desk audit, 2026-10-12 (analysis/audits/AUDIT_PROGRAM.md). Sources read that day; second-hand items labelled."),
item("AUD-21", "AUD", "Own-benchmark audit: requirements, pitfalls and candidate designs", "done", criterion="Typed table with a source on every row, searches and unread sources listed, implications for the project",
     evidence=["analysis/audits/AU4_own_benchmark.md", "analysis/audits/AU4_own_benchmark.json"],
     checks=[G("analysis/audits/AU4_own_benchmark.md", r"What this changes"), J("analysis/audits/AU4_own_benchmark.json", ["rows"], "len_eq", 20)],
     note="Desk audit, 2026-10-12 (analysis/audits/AUDIT_PROGRAM.md). Sources read that day; second-hand items labelled."),
item("AUD-22", "AUD", "Commercial audit: who buys causal analysis, for which decision, with which guarantee", "done", criterion="Typed table with a source on every row, searches and unread sources listed, implications for the project",
     evidence=["analysis/audits/AU5_commercial.md", "analysis/audits/AU5_commercial.json"],
     checks=[G("analysis/audits/AU5_commercial.md", r"What this changes"), J("analysis/audits/AU5_commercial.json", ["rows"], "len_eq", 42)],
     note="Desk audit, 2026-10-12 (analysis/audits/AUDIT_PROGRAM.md). Sources read that day; second-hand items labelled."),
item("AUD-23", "AUD", "Engine audit: libraries, capabilities, defects; build vs reuse for the ledger", "done", criterion="Typed table with a source on every row, searches and unread sources listed, implications for the project",
     evidence=["analysis/audits/AU6_core_engines.md", "analysis/audits/AU6_core_engines.json"],
     checks=[G("analysis/audits/AU6_core_engines.md", r"What this changes"), J("analysis/audits/AU6_core_engines.json", ["rows"], "len_eq", 36)],
     note="Desk audit, 2026-10-12 (analysis/audits/AUDIT_PROGRAM.md). Sources read that day; second-hand items labelled."),
item("AUD-24", "AUD", "Value-of-accuracy audit: how graph errors become decision errors", "done", criterion="Typed table with a source on every row, searches and unread sources listed, implications for the project",
     evidence=["analysis/audits/AU7_value_of_accuracy.md", "analysis/audits/AU7_value_of_accuracy.json"],
     checks=[G("analysis/audits/AU7_value_of_accuracy.md", r"What this changes"), J("analysis/audits/AU7_value_of_accuracy.json", ["rows"], "len_eq", 45)],
     note="Desk audit, 2026-10-12 (analysis/audits/AUDIT_PROGRAM.md). Sources read that day; second-hand items labelled."),
item("AUD-25", "AUD", "Packaging audit: delivery modes, output requirements, regulator needs, user complaints", "done", criterion="Typed table with a source on every row, searches and unread sources listed, implications for the project",
     evidence=["analysis/audits/AU8_packaging.md", "analysis/audits/AU8_packaging.json"],
     checks=[G("analysis/audits/AU8_packaging.md", r"What this changes"), J("analysis/audits/AU8_packaging.json", ["rows"], "len_eq", 43)],
     note="Desk audit, 2026-10-12 (analysis/audits/AUDIT_PROGRAM.md). Sources read that day; second-hand items labelled."),
item("AUD-26", "AUD", "Audit synthesis: where the open room is, what makes a tool worth using, build vs reuse", "done", criterion="Answers the three program questions from AU1-AU8 with evidence and inference separated; layout claim checked",
     evidence=["analysis/audits/AU0_synthesis.md", "analysis/audits/AUDIT_PROGRAM.md", "analysis/authors_rule_layout_check.py", "analysis/results/authors_rule/check.json"],
     checks=[J("analysis/results/authors_rule/check.json", ["methods", "FCI", "shuffled_order", "layout_gain"], "le", 0.01), G("analysis/audits/AU0_synthesis.md", r"Decisions for Uzair")],
     note="Decision input for DEC-01."),
item("AUD-27", "AUD", "Engine oracle check: PC and FCI under a perfect independence oracle, every engine copy", "done",
     criterion="120 random DAGs x 6 column orders per engine; exact-class, order-invariance and defect counts per engine; Causal-Copilot's copy vs PyPI causal-learn vs gCastle",
     evidence=["analysis/engine_oracle_check.py", "analysis/results/engine_oracle/oracle.json", "analysis/results/engine_oracle/CONTRACT.json", "analysis/reports/aud27_31_free_steps.md"],
     checks=[J("analysis/results/engine_oracle/oracle.json", ["engines", "vendored/pc", "exact_equivalence_class"], "eq", 460),
             J("analysis/results/engine_oracle/oracle.json", ["engines", "pypi-0.1.3.8/pc", "exact_equivalence_class"], "eq", 720),
             J("analysis/results/engine_oracle/oracle.json", ["engines", "gcastle-1.0.4/gcastle_original", "exact_equivalence_class"], "eq", 456)],
     reproduce="python analysis/engine_oracle_check.py --engine vendored=<Causal-Copilot>/externals/causal-learn --engine pypi-0.1.3.8=<site-packages> --gcastle <site-packages>",
     note="No model calls. The copy's FCI step is not deterministic under threads (533 vs 531)."),
item("AUD-28", "AUD", "Controlled re-score: released vs shuffled columns for every runnable baseline; PC conflict-rule mechanism", "done",
     criterion="Files paired; S, c, q, a and F1 under both orientation rules; published values alongside; mechanism prediction written before the run",
     evidence=["analysis/rescore_controls.py", "analysis/pc_upstream_run.py", "analysis/pc_orientation_order.py", "analysis/results/rescore/rescore.json",
               "analysis/results/rescore/pc_orientation_order.json", "analysis/reports/aud27_31_free_steps.md"],
     checks=[J("analysis/results/rescore/rescore.json", ["methods", "PC (upstream causal-learn)", "semantic", "files_better_shuffled"], "eq", 175),
             J("analysis/results/rescore/pc_orientation_order.json", ["configs", "maxP uc_rule=1", "q_gap_shuffled_minus_released"], "le", 0.03),
             J("analysis/results/rescore/pc_orientation_order.json", ["configs", "default uc_rule=0 uc_priority=2", "q_gap_shuffled_minus_released"], "ge", 0.1)],
     reproduce="python analysis/pc_upstream_run.py && python analysis/rescore_controls.py && python analysis/pc_orientation_order.py"),
item("AUD-29", "AUD", "Sortability of the CausalArena release (varsortability, R2-sortability)", "done",
     criterion="Path-weighted and edge-only, per file and per family",
     evidence=["analysis/sortability_audit.py", "analysis/results/sortability/sortability.json", "analysis/reports/aud27_31_free_steps.md"],
     checks=[J("analysis/results/sortability/sortability.json", ["families", "semantic", "summary", "var_paths", "mean"], "eq", 0.5),
             J("analysis/results/sortability/sortability.json", ["families", "semantic", "summary", "files"], "eq", 250)],
     reproduce="python analysis/sortability_audit.py"),
item("AUD-30", "AUD", "Decision value (DV-1) and adjustment-identification distance for every baseline, with ceilings and the empty-graph baseline", "done",
     criterion="Committed-claim precision and coverage against truth; true CPDAG and DAG ceilings; empty-graph baseline; AID where defined, refusals counted",
     evidence=["analysis/decision_value.py", "analysis/results/decision_value/decision_value.json", "analysis/results/decision_value/CONTRACT.json", "analysis/reports/aud27_31_free_steps.md"],
     checks=[J("analysis/results/decision_value/decision_value.json", ["families", "semantic", "ceiling: true CPDAG", "reference", "precision_committed"], "ge", 0.999),
             J("analysis/results/decision_value/decision_value.json", ["families", "semantic", "baseline: empty graph (nothing moves)", "reference", "precision_committed"], "le", 0.65),
             J("analysis/results/decision_value/decision_value.json", ["families", "semantic", "GES (BIC)", "released", "precision_committed"], "le", 0.76)],
     reproduce="python analysis/decision_value.py",
     note="Baselines use all 250 files, methods the files they finished; AB-04 pairs them."),
item("AUD-31", "AUD", "Cost of one Causal-Copilot run (the approved one-run cost check)", "done",
     criterion="Per-run cost, calls, tokens and wall time from the API's own usage records",
     evidence=["analysis/results/stability_s2/cost_per_run.json", "analysis/reports/aud27_31_free_steps.md"],
     checks=[J("analysis/results/stability_s2/cost_per_run.json", ["cost_per_run_usd", "median"], "eq", 0.457),
             J("analysis/results/stability_s2/cost_per_run.json", ["runs"], "eq", 30)],
     note="Answered from the 30 logged BND-08 runs; nothing spent."),
item("AUD-32", "AUD", "Audit program DAG: research landscape, commercial landscape, wedge and paper", "done",
     criterion="Bundles with dependencies, windows, costs, runners, predictions and must-show lists; landmark and kill criteria; plan_check passes; approved by Uzair",
     evidence=["plans/make_audit_dag.py", "plans/audit_dag.json", "analysis/reports/audit_dag.md", "docs/decisions/2026-10-12_audit_dag.md"],
     checks=[J("plans/audit_dag.json", ["bundles"], "len_eq", 17), G("analysis/reports/audit_dag.md", r"What needs Uzair")],
     reproduce="python plans/make_audit_dag.py && python tracker/plan_check.py plans/audit_dag.json",
     note="Approved by Uzair 2026-10-12 (docs/decisions/2026-10-12_audit_dag.md); AUD-33..48 and DEC-05 issued."),
# ---- audit program (plans/audit_dag.json, approved 2026-10-12; results p02 2026-10-13)
# ---- audit program results (p02, 2026-10-13)
item('AUD-33', 'AUD', 'AB-01 Controlled scoreboard, CausalArena complete (all families, D and D+I, corrected leaderboard)', 'done', kind='task', criterion="Must show: corrected leaderboard table; per-family layout gain by channel (authors' rule, conflict rule, engine copy). Gate: every runnable published row has released and shuffled numbers under both rules, files paired",
     evidence=['analysis/baseline_variants_run.py', 'analysis/rescore_controls_v2.py', 'analysis/results/rescore_v2/rescore_v2.json', 'analysis/results/rescore_v2/leaderboard_controlled.md', 'analysis/results/rescore_v2/leaderboard_controlled.json', 'analysis/results/rescore_v2/CONTRACT.json', 'analysis/reports/ab01_controlled_scoreboard.md'],
     checks=[J("analysis/results/rescore_v2/rescore_v2.json", ["predictions", "P2", "complete"], "true"), G("analysis/reports/ab01_controlled_scoreboard.md", r"Corrected leaderboard")],
     due='2026-10-17', blocked_by=None, reproduce='python analysis/baseline_variants_run.py ... (see report) && python analysis/rescore_controls_v2.py',
     note='Results in the report; predictions P1/P2 verdicts in rescore_v2.json.'),
item('AUD-34', 'AUD', 'AB-02 Second scoreboard: layout and conflict channels on other public benchmarks', 'blocked', kind='task', criterion='Must show: per-benchmark table: order correlation, sortability, layout gain per method. Gate: two published rows reproduced per benchmark before any re-score claim',
     evidence=['analysis/reports/ab02_second_scoreboard.md', 'analysis/ab02_alarm_order.py', 'analysis/results/ab02/alarm_order.json', 'analysis/audits/AB02_AB12_data_scouting.md'],
     checks=[J("analysis/results/ab02/alarm_order.json", ["P3_this_release"], "eq", "no (all |tau| < 0.3)")],
     due='2026-10-24', blocked_by='Uzair: download Bayesys data into external/bayesys', reproduce='',
     note="gCastle alarm measured (no causal column order; PC not reproduced, so no re-score claim). Bayesys needs Uzair's browser download: zenodo.org and constantinou.info are refused by both network paths."),
item('AUD-35', 'AUD', 'AB-03 Engine forensics: perfect-oracle and determinism checks for every engine agents call', 'done', kind='task', criterion='Must show: engine defect table (exact rate, order invariance, determinism, defect class). Gate: versions pinned; one command reproduces',
     evidence=['analysis/engine_forensics.py', 'analysis/engine_shims.py', 'analysis/results/engine_forensics/forensics.json', 'analysis/results/engine_forensics/CONTRACT.json', 'analysis/reports/ab03_engine_forensics.md', 'docs/drafts/bug_reports/dodiscover_pc_oracle_cycle.md'],
     checks=[J("analysis/results/engine_forensics/forensics.json", ["engines", "dodiscover_pc", "exact_equivalence_class"], "eq", 597), J("analysis/results/engine_forensics/forensics.json", ["engines", "pgmpy_stable_unbounded", "exact_equivalence_class"], "eq", 720), J("analysis/results/engine_forensics/forensics.json", ["engines", "tigramite_pcmciplus", "exact_equivalence_class"], "eq", 720)],
     due='2026-10-24', blocked_by=None, reproduce='python analysis/engine_forensics.py --python2 <venv with pgmpy, tigramite, dodiscover> --vendored <Causal-Copilot>/externals/causal-learn --out analysis/results/engine_forensics',
     note='P5 refuted as worded (no further wrong skeleton); new defect class: dodiscover PC orients wrongly under an oracle and can return a cyclic graph. Bug-report drafts for EXT-03 in docs/drafts/bug_reports/.'),
item('AUD-36', 'AUD', 'AB-04 Decision-value scoreboard across benchmarks, with the usefulness threshold', 'done', kind='task', criterion='Must show: decision-value table across benchmarks; risk-coverage figure; F1 vs DV scatter. Gate: claims checked against truth; baselines on exactly the files each method finished',
     evidence=['analysis/decision_value_v2.py', 'analysis/dv_chambers_sachs.py', 'analysis/ab04_figures.py', 'analysis/results/decision_value_v2/decision_value_v2.json', 'analysis/results/decision_value_v2/dv_chambers_sachs.json', 'analysis/results/decision_value_v2/risk_coverage.png', 'analysis/results/decision_value_v2/f1_vs_dv.png', 'analysis/results/decision_value_v2/CONTRACT.json', 'analysis/reports/ab04_decision_value.md'],
     checks=[G("analysis/reports/ab04_decision_value.md", r"P6"), J("analysis/results/decision_value_v2/dv_chambers_sachs.json", ["benchmarks", "causal_chambers_lt", "methods", "true CPDAG", "precision_committed"], "eq", 1.0)],
     due='2026-10-28', blocked_by=None, reproduce='python analysis/decision_value_v2.py && python analysis/dv_chambers_sachs.py --causal-learn <upstream causal-learn> ... && python analysis/ab04_figures.py ...',
     note='Five benchmarks: CausalArena semantic, formula, synthetic; Causal Chambers (physical truth, real interventions); Sachs (weak).'),
item('AUD-37', 'AUD', 'AB-05 LIVE (small): agent probes, install and one-run cost per agent ($5 cap)', 'blocked', kind='task', criterion='Must show: per agent: installs, runs, calls, tokens, cost, wall time, failure points. Gate: no key in any log; every call recorded; repo byte-identical',
     evidence=['harness/agent_probe.py', 'harness/probe_llm.py', 'harness/probe_io.py', 'harness/agents/registry.json', 'docker/Dockerfile.probes', 'plans/ab05_probe_causaliq.json', 'plans/ab05_probe_pywhyllm.json', 'plans/ab05_probe_matmcd.json', 'plans/ab05_probe_vashishtha.json', 'plans/ab05_cc_gpt4omini.json', 'analysis/reports/ab05_probe_prep.md', 'tests/test_agent_probe.py'],
     checks=[G("analysis/reports/ab05_probe_prep.md", r"Proposed AB-06 budget"), J("plans/ab05_probe_vashishtha.json", ["budget_check", "sum_max_usd_all_four"], "le", 4.0)],
     due='2026-10-20', blocked_by='Uzair: live probe runs (approved cap $5)', reproduce='',
     note="Offline part done: all four agents run end to end with a stub model; caps total $3.55 + Causal-Copilot second model (~$0.03). Live runs are Uzair's (cc.ps1 probebuild, probe)."),
item('AUD-38', 'AUD', 'AB-06 LIVE: field audit of LLM-using systems under names x layout controls', 'todo', kind='task', criterion='Must show: per agent x arm table; name-reliance figure; provenance shares. Gate: thresholds hashed before the calls; dev split only',
     evidence=[],
     checks=[],
     due='2026-11-14', blocked_by='AUD-37', reproduce='',
     note='Budget proposed in the AB-05 report (about $57 for 4 agents x 3 arms x 10 dev scenarios, or about $29 with PyWhy on gpt-4o-mini); recompute from the first live calls before approval.'),
item('AUD-39', 'AUD', 'AB-08 Name-reliance benchmark with a rho dial (decoupled semantics, B2)', 'done', kind='task', criterion="Must show: rho curve per method; benchmark card. Gate: generator's own sortability and layout reported; columns always shuffled",
     evidence=['analysis/b2_generator.py', 'analysis/b2_score.py', 'analysis/b2_reference_methods.py', 'analysis/reports/ab08_benchmark_card.md', 'analysis/results/b2/b2_reference_scores.json', 'analysis/results/b2/b2_sortability.json', 'analysis/results/b2/CONTRACT.json', 'tests/test_b2_generator.py'],
     checks=[J("analysis/results/b2/b2_reference_scores.json", ["methods", "names_oracle", "by_track_rho", "linear", "1.00", "f1_data_mean"], "eq", 0.0), G("analysis/reports/ab08_benchmark_card.md", r"[Ll]imitations")],
     due='2026-11-14', blocked_by=None, reproduce='',
     note='Benchmark built and validated (2,500 files, 257.7 MB, outside git under external/b2_namereliance; manifest sha256). P11 holds for the reference methods; agent curves come from AB-06.'),
item('AUD-40', 'AUD', 'AB-09 Theory pack: identity, error budget, bounded harm, conflict-rule order dependence, DV ceiling', 'done', kind='task', criterion='Must show: proof notes; numerical checks. Gate: no statement beyond what the references support',
     evidence=['analysis/theory_checks.py', 'analysis/results/theory/theory_checks.json', 'analysis/results/theory/CONTRACT.json', 'analysis/reports/ab09_theory_pack.md', 'tests/test_theory.py'],
     checks=[J("analysis/results/theory/theory_checks.json", ["P12_holds_as_restated"], "true")],
     due='2026-11-07', blocked_by=None, reproduce='',
     note='T1-T4 hold as stated; T5 restated (coverage = constant-answer share minus definite causes without a directed path). F1 = S x a holds per file, not for family means (corrects the AUD-28 wording).'),
item('AUD-41', 'AUD', 'AB-10 Practitioner interviews (C1)', 'blocked', kind='task', criterion='Must show: interview synthesis with quotes paraphrased. Gate: notes stored without personal data beyond role and sector',
     evidence=['docs/interviews/human_subjects_check.md', 'docs/interviews/guide.md', 'docs/interviews/screener.md', 'docs/interviews/consent_script.md', 'docs/interviews/notes_schema.json', 'docs/interviews/synthesis_plan.md', 'analysis/interview_synthesis.py', 'tests/test_interview_synthesis.py'],
     checks=[G("docs/interviews/human_subjects_check.md", r"generalizable knowledge")],
     due='2026-11-07', blocked_by='Uzair: course-staff question, then recruiting and interviews', reproduce='',
     note='Interview kit ready. First Uzair asks course staff whether an IRB determination is needed (path a: course-internal; path b: determination before the first interview).'),
item('AUD-42', 'AUD', 'AB-11 Competitive teardown: open tools hands-on, closed tools by documented claims', 'done', kind='task', criterion='Must show: teardown table. Gate: vendor claims never presented as measurements',
     evidence=['analysis/audits/AB11_vendor_claims.md', 'analysis/audits/AB11_vendor_claims.json', 'analysis/ab11_teardown_run.py', 'analysis/ab11_ledger_adapters.py', 'analysis/results/teardown/teardown.json', 'analysis/results/teardown/CONTRACT.json', 'tests/test_ab11_adapters.py'],
     checks=[G("analysis/audits/AB11_vendor_claims.md", r"Hands-on results"), J("analysis/results/teardown/teardown.json", ["tools"], "len_eq", 10)],
     due='2026-10-31', blocked_by=None, reproduce='',
     note="33 tools by documentation, 10 run by hand. P14 strong form survives narrowed: no tool stores a per-direction source linked to evidence (CausalNex 'origin' and Tetrad verbose text are partial)."),
item('AUD-43', 'AUD', 'AB-12 Vertical probe: root-cause analysis', 'done', kind='task', criterion='Must show: RCA table; what a ledger adds here. Gate: datasets reachable',
     evidence=['analysis/ab12_rca_probe.py', 'analysis/results/rca/rca_probe.json', 'analysis/results/rca/ab12_prereg.json', 'analysis/results/rca/CONTRACT.json', 'analysis/reports/ab12_rca_probe.md'],
     checks=[J("analysis/results/rca/rca_probe.json", ["P15", "verdict"], "eq", "supported")],
     due='2026-11-07', blocked_by=None, reproduce='',
     note='PetShop test (48 issues): declared topology + abstention AC@3 0.93 at coverage 0.92 vs learned-graph (PC) 0.21; P15 supported, almost all of the gap from topology.'),
item('AUD-44', 'AUD', 'AB-13 Regulation and standards map: requirement -> ledger field', 'done', kind='task', criterion='Must show: requirement -> field matrix. Gate: primary texts only; summaries labelled second-hand',
     evidence=['analysis/audits/AB13_regulation_map.md', 'analysis/audits/AB13_regulation_map.json'],
     checks=[J("analysis/audits/AB13_regulation_map.json", ["rows"], "len_eq", 50), G("analysis/audits/AB13_regulation_map.md", r"What this changes")],
     due='2026-10-24', blocked_by=None, reproduce='',
     note='50 requirements, 21 texts; five ledger gaps ranked (plan/deviations, assumptions, lineage, reviews, question/context: BLD-14). Venue: W3C AI Computed Provenance CG.'),
item('AUD-45', 'AUD', 'AB-14 Market and go-to-market hypotheses for two verticals', 'todo', kind='task', criterion='Must show: two one-page vertical briefs. Gate: no number without its inputs',
     evidence=['docs/market/README.md'],
     checks=[],
     due='2026-11-12', blocked_by='AUD-41', reproduce='',
     note='Scaffolding only; waits on AB-10 interviews and uses AB-11 pricing signals.'),
item('AUD-46', 'AUD', 'AB-15 Positioning closure: novelty matrix for L1-L5', 'done', kind='task', criterion='Must show: novelty matrix. Gate: every claim of novelty bounded by the searches recorded',
     evidence=['analysis/audits/AB15_positioning.md', 'analysis/audits/AB15_positioning.json'],
     checks=[J("analysis/audits/AB15_positioning.json", ["rows"], "len_eq", 45), J("analysis/audits/AB15_positioning.json", ["novelty_matrix"], "len_eq", 5)],
     due='2026-10-22', blocked_by=None, reproduce='',
     note='All five claims partly open. Must cite Colombo & Maathuis 2014 (scoops PC order dependence), CARE (single-system name collapse), Li & Russo 2026 (orient-only LLM knowledge).'),
item('AUD-47', 'AUD', 'AB-17 Paper skeleton and pre-registration manifest', "todo", kind='task', criterion='Must show: skeleton; manifest. Gates: manifest committed before any held-out run', due='2026-11-21', note='Bundle AB-17 of plans/audit_dag.json (wedge track); window 2026-11-10..2026-11-21; cost: none.'),
item('AUD-48', 'AUD', 'AB-07 LIVE: knowledge elicitation run (A3, DEC-02): tiers, three phrasings, three name arms', 'blocked', kind='task', criterion='Must show: O1-O5 verdicts; tier accuracy by arm; regression on model tiers vs 0.634 / 0.524. Gate: DEC-02 approved; prompts and thresholds hashed before the calls',
     evidence=['analysis/a3_make_requests.py', 'harness/tiers_runner.py', 'analysis/a3_score.py', 'plans/a3_prereg.json', 'plans/a3_tiers_requests.jsonl', 'plans/a3_scenarios.json', 'analysis/results/a3/selftest.json', 'tests/test_tiers_runner.py'],
     checks=[J("plans/a3_prereg.json", ["requests"], "eq", 900), J("analysis/results/a3/selftest.json", ["oracle_tiers", "verdicts", "O4", "value"], "ge", 0.71)],
     due='2026-10-28', blocked_by='Uzair: live tier run (approved 2026-10-12)', reproduce='',
     note="Ready: 900 requests pre-registered (sha256 in a3_prereg.json), estimate about $3.1 at gpt-4o list; scorer validated with oracle tiers (O4 0.714). Live run is Uzair's: cc.ps1 tiers a3_tiers_requests.jsonl."),
item('DEC-05', 'DEC', 'AB-16 Wedge decision: paper spine, venue and the Q2 build', "todo", kind='decision', criterion='Must show: wedge memo. Gates: decision recorded as a DEC ticket with the evidence it rests on', due='2026-11-14', note='Bundle AB-16 of plans/audit_dag.json (wedge track); window 2026-11-03..2026-11-14; cost: none.'),
item("BEN-01", "BEN", "CausalArena public release inspected (families, files, graph convention)", "done",
     criterion="Layout documented; graph convention checked against graph.json for all 50 semantic scenarios",
     evidence=[R + "bundle1_results.md (section 7)", FR, "external/causalarena/MANIFEST.json"],
     checks=[J(FR, ["errors"], "len_eq", 0)]),
item("BEN-02", "BEN", "Column-order leak: every true edge runs earlier column -> later column in every released file", "done",
     criterion="Checked over every released obs file of all three families; order-reading baseline vs shuffled",
     evidence=[COC, OB, "analysis/column_order_check.py", "analysis/causalarena_order_baseline.py"],
     checks=[J(COC, ["semantic", "share"], "eq", 1.0), J(COC, ["formula", "share"], "eq", 1.0), J(COC, ["synthetic", "share"], "eq", 1.0),
             J(COC, ["synthetic", "true_edges"], "eq", 50421), J(OB, ["families", "semantic", "as_released", "f1"], "approx", 0.68, 0.001),
             J(OB, ["families", "semantic", "columns_shuffled", "f1"], "approx", 0.269, 0.001)],
     reproduce="python analysis/column_order_check.py --root external/causalarena --out analysis/results/causalarena_calibration",
     reopen_if=["CausalArena release files change"]),
item("BEN-03", "BEN", "Identifiable ceilings 0.957 / 0.971 (obs); at least 0.974 / 0.993 with released interventions", "done",
     criterion="Computed per scenario; equivalence-class routine matches the validated one (gate B1)", evidence=[EB, "analysis/error_budget.py"],
     checks=[J(EB, ["gates", "B1_cpdag_equals_cc_graph"], "true"), J(EB, ["families", "semantic", "ceiling_obs_mean"], "approx", 0.957, 0.001),
             J(EB, ["families", "formula", "ceiling_obs_mean"], "approx", 0.971, 0.001)],
     reproduce="python analysis/error_budget.py --root external/causalarena --pc analysis/results/causalarena_calibration/pc_rows_v2.jsonl --out analysis/results/error_budget"),
item("BEN-04", "BEN", "Error budget for PC: 1.000 -> 0.957 -> 0.611 -> 0.335; directions right 54%", "done",
     evidence=[EB], criterion="From stored PC runs in the published configuration",
     checks=[J(EB, ["pc_semantic_n1000", "pc_skeleton_with_perfect_orientation_f1"], "approx", 0.611, 0.001),
             J(EB, ["pc_semantic_n1000", "accuracy_of_committed_directions"], "approx", 0.544, 0.001)]),
item("BEN-05", "BEN", "Value of oracle order knowledge (inputs only: 0.470; full depth + regression: 0.714)", "done",
     evidence=[OV, "analysis/order_value.py"], criterion="Table over 5 granularities of tier knowledge",
     checks=[J(OV, [1, "PC skeleton re-oriented, F1"], "approx", 0.47, 0.001), J(OV, [5, "regression on earlier tiers, F1"], "approx", 0.714, 0.001)]),
item("BEN-06", "BEN", "Repo datasets vs CausalArena index: Auto MPG does not match", "done",
     evidence=[DMC, "analysis/dataset_match_check.py"], criterion="Variables, edges, rows compared for all four families",
     checks=[J(DMC, ["autompg", "match"], "false"), J(DMC, ["abalone", "match"], "true"), J(DMC, ["concrete", "match"], "true"), J(DMC, ["dwd", "match"], "true")]),
item("BEN-07", "BEN", "Do CausalArena's wrappers shuffle columns; are top methods affected?", "in_progress", kind="question",
     criterion="For every method we can run, F1 on released vs shuffled column order measured; whether CausalArena's own wrappers shuffle stated from their code or recorded as unknowable",
     evidence=[PROT, MV + "bnd06_verdicts.json", MV + "bnd06_families.json", MV + "pc_skeleton_order_vendored.json", MV + "pc_skeleton_order_upstream.json",
               R + "bnd06_interim.md", R + "bnd06_families.md", "plans/bnd06_prereg.json"],
     checks=[J(PROT, ["facts", "P2_liberal_orientation", "found"], "true"), J(MV + "bnd06_verdicts.json", ["Q4c", "verdict"], "eq", "REFUTED"),
             J(MV + "pc_skeleton_order_vendored.json", ["files_with_different_skeleton"], "eq", 21),
             J(MV + "pc_skeleton_order_upstream.json", ["files_with_different_skeleton"], "eq", 0)],
     note="Authors' runners do not shuffle and orient undecided edges by column index. Released vs shuffled measured for PC, GES, FCI, "
          "DirectLiNGAM, NOTEARS on semantic, formula and synthetic100: only PC moves (|diff| 0.093 / 0.051 / 0.106). Mechanism located: "
          "Causal-Copilot's vendored causal-learn 0.1.3.8 skeleton changes with column order in 21 of 24 files, upstream 0.1.4.8 in 0 of 22. "
          "Open: AVICI (pretrained; checkpoint download blocked)."),
item("BEN-08", "BEN", "SHD definition mismatch (see REP-06)", "done", kind="question",
     criterion="The SHD variant that reproduces the published 33.5 identified on the stored PC outputs, or every candidate variant shown not to",
     evidence=[PROT, PCC, "analysis/shd_variants.py"],
     checks=[J(PROT, ["facts", "P1_shd_formula", "found"], "true"), J(PROT, ["ours_public_50_by_rule", "lower", "shd_within"], "true")],
     note="The authors' SHD counts a reversal once (metrics.py: sum(diff) - 0.5*sum(diff*diff.T)), which is our pair-level SHD; with their "
          "orientation rule it gives 35.43 on the public 50 (within tolerance of 33.52). F1 then does not match (REP-06)."),
item("BEN-09", "BEN", "Replay sampler: which declared interventions are interventions in name only", "done",
     criterion="For every declared intervention in the replay sampler's data, whether the target's distribution moves (KS, Holm 1%); the in-name-only count reported",
     evidence=["analysis/intervention_audit.py", IA],
     checks=[J(IA, ["families", "semantic", "declared_target_instances"], "eq", 945), J(IA, ["families", "semantic", "in_name_only"], "eq", 252),
             J(IA, ["families", "formula", "declared_target_instances"], "eq", 1520), J(IA, ["families", "formula", "in_name_only"], "eq", 1354)],
     reproduce="python analysis/intervention_audit.py --out analysis/results/intervention_audit/intervention_audit.json",
     note="On the released obs+int files (produced by the same generator spec the replay sampler executes): no detectable shift in the target "
          "or any child for 252 of 945 declared interventions (semantic) and 1,354 of 1,520 (formula), KS with Holm at 1%. About 28 "
          "intervened rows per target, so shifts below roughly KS D 0.4 go undetected: 'no detectable effect', not proof of none. "
          "Most targets are roots (655 / 1,200), resampled per the release's semantics."),
item("BEN-10", "BEN", "Causal Chambers: map 8 datasets to ground-truth graphs; check 'one layer deep'; build obs+int sample", "done",
     evidence=[FR, "analysis/results/chambers/mapping.json", "analysis/results/chambers/one_layer_deep.json", "analysis/results/chambers/sample/obs_int_sample.npz", "analysis/results/chambers/sample/README.md",
               "analysis/chambers_map.py", "analysis/chambers_validate.py", "analysis/chambers_sample.py", "analysis/reports/bnd07_chambers.md",
               "manifests/evidence/chambers_extracted_2026-10-12.sha256"],
     checks=[J(FR, ["extracted"], "len_eq", 8), J("analysis/results/chambers/one_layer_deep.json", ["part_a_our_check", "lt_validate_v1", "children_shift"], "eq", 57),
             J("analysis/results/chambers/one_layer_deep.json", ["part_a_our_check", "lt_validate_v1", "non_descendants_shift"], "eq", 0),
             J("analysis/results/chambers/one_layer_deep.json", ["part_a_our_check", "wt_validate_v1", "non_descendants_shift"], "eq", 0),
             J("analysis/results/chambers/sample/sample_status.json", ["built"], "true"), {"t": "manifest", "path": "manifests/evidence/chambers_extracted_2026-10-12.sha256"}],
     note="All 8 datasets use the 'standard' configuration: lt 38 variables / 57 edges, wt 32 / 42, every edge input -> output (longest "
          "path 1). On the validation data: lt 57/57 children shift, wt 40/42 (load_out -> pressure_intake p 0.082; osr_downwind -> "
          "pressure_downwind fails only after Holm over 868 tests); 0 non-descendant shifts in either. Sample: 6,200 rows, 53 regimes."),
item("BEN-11", "BEN", "Error budgets for GES, FCI, pretrained models; formula and synthetic families", "in_progress",
     criterion="Error budgets (ceiling -> skeleton -> direction) for GES, FCI, DirectLiNGAM, NOTEARS and CPU-runnable pretrained models on semantic, formula and a 100-file synthetic sample",
     evidence=[MV + "error_budget_gesbic.json", MV + "error_budget_fci.json", MV + "error_budget_lingam_semantic.json", MV + "error_budget_notears_semantic.json",
               MV + "error_budget_pc_semantic.json", MV + "error_budget_gesbic_formula.json", MV + "error_budget_fci_formula.json",
               MV + "error_budget_lingam_formula.json", MV + "error_budget_notears_formula.json", MV + "error_budget_gesbic_synthetic100.json",
               MV + "error_budget_fci_synthetic100.json", MV + "error_budget_lingam_synthetic100.json", MV + "error_budget_notears_synthetic100.json",
               R + "bnd06_families.md"],
     checks=[J(MV + "error_budget_lingam_semantic.json", ["files"], "eq", 250), J(MV + "error_budget_notears_formula.json", ["files"], "eq", 250)],
     note="Done for PC, GES, FCI, DirectLiNGAM, NOTEARS x semantic, formula, synthetic100 (15 budgets; failed files scored empty and counted). "
          "Open: pretrained models (AVICI checkpoint blocked by the egress allowlist; Uzair can download two files by hand)."),
item("BEN-12", "BEN", "Reliability of real-data reference graphs", "done",
     evidence=["analysis/reference_reliability.py", "analysis/results/reference_reliability/reliability.json", "external/bnlearn_sachs/sachs.bif.gz"],
     checks=[J("analysis/results/reference_reliability/reliability.json", ["families", "sachs", "tier"], "eq", "contested"),
             J("analysis/results/reference_reliability/reliability.json", ["families", "sachs", "repo_vs_bnlearn", "shared_adjacencies"], "eq", 16),
             J("analysis/results/reference_reliability/reliability.json", ["families", "autompg", "tier"], "eq", "mismatched"),
             J("analysis/results/reference_reliability/reliability.json", ["families", "s2_01", "tier"], "eq", "exact")],
     reproduce="python analysis/reference_reliability.py",
     note="Sachs: repo 19 edges vs bnlearn 17 (16 shared adjacencies, 1 reversed: PIP3-Plcg) vs CausalArena 20 (edge list not "
          "available here). Auto MPG mismatched. Abalone, concrete, DWD: provenance only. S2: exact (simulator graph)."),
# ---------------- 5 Targets
item("TGT-01", "TGT", "Semantic, numbers only: reach 0.634 (FoundCause); GIES 0.552; ceiling 0.957", "todo", kind="target", evidence=[LB, EB]),
item("TGT-02", "TGT", "Semantic, numbers + interventions: reach 0.568 (GIES); ceiling >= 0.974", "todo", kind="target", evidence=[LB, EB]),
item("TGT-03", "TGT", "Formula, numbers only: reach 0.524 (FoundCause); ceiling 0.971", "todo", kind="target", evidence=[LB, EB]),
item("TGT-04", "TGT", "Formula, numbers + interventions: reach >= 0.534 (TabCausal; check other rows); ceiling >= 0.993", "todo", kind="target", evidence=[LB, EB]),
item("TGT-05", "TGT", "Real data: 0.391 observational (CDFM); 0.462 with interventions (TabCausal, 7 sets)", "todo", kind="target", evidence=[RL]),
item("TGT-06", "TGT", "Causal Chambers alone: 0.727 reported by CDFM (second-hand; check subset)", "todo", kind="target"),
item("TGT-07", "TGT", "Numbers + declared knowledge: >= 0.634 semantic, >= 0.524 formula, columns shuffled", "blocked", kind="target",
     blocked_by="AUD-48 (AB-07 live tier run, waits on Uzair)"),
item("TGT-08", "TGT", "Derived requirement: skeleton F1 x direction accuracy >= 0.634 (e.g. 0.80 x 0.79)", "open", kind="target", evidence=[EB]),
item("TGT-09", "TGT", "Never below the system's own data-only output", "in_progress", kind="target",
     criterion="BND-10: frozen refinement v1 keeps adjacency F1 >= the algorithm's own output - 0.02 in >= 90% of held-out files (R1), on the test replay and the live S2 tables",
     evidence=["analysis/results/refinement_v1/test_replay.json", "analysis/results/refinement_v1/test_live_s2.json",
               "analysis/results/refinement_v1/access_log.jsonl", "analysis/reports/bnd09_bnd10_refinement.md"],
     checks=[J("analysis/results/refinement_v1/test_live_s2.json", ["pooled_test", "R1", "verdict"], "eq", "INCONCLUSIVE"),
             J("analysis/results/refinement_v1/test_live_s2.json", ["mode"], "eq", "test")],
     note="Not met by v1: pooled held-out R1 40 of 55 (0.73; replay 23/25, live S2 17/30). v1 drops true edges with low resample frequency "
          "under FCI+RCIT. Carried to v2 in BND-11 (DAG changed 12 Oct)."),
item("TGT-10", "TGT", "Zero change when columns are shuffled", "todo", kind="target"),
item("TGT-11", "TGT", "Bounded harm when names are wrong", "todo", kind="target"),
item("TGT-12", "TGT", "Calibration better than raw bootstrap frequencies on held-out scenarios", "todo", kind="target"),
item("TGT-13", "TGT", "Zero crashes from malformed model output", "in_progress", kind="target",
     evidence=["harness/names_runner.py", "tests/test_refinement_v2.py"], checks=[G("harness/names_runner.py", r"never raised")],
     note="BND-11 names runner: invalid reply -> one retry -> abstention; API errors recorded the same way. Offline stub with injected "
          "malformed replies: 25 invalid replies, no exception. Closes on the live names run (crash count 0)."),
item("TGT-14", "TGT", "Within the scoreboard's 1-hour budget per graph", "todo", kind="target"),
item("TGT-15", "TGT", "Held-out interventional predictions better than regression on all variables", "todo", kind="target"),
item("TGT-16", "TGT", "Experiment choice better than random on recorded Causal Chambers experiments", "todo", kind="target"),
# ---------------- 6 Capabilities
item("CAP-01", "CAP", "Skeleton recall at variables with many causes (joint test per candidate edge)", "todo"),
item("CAP-02", "CAP", "Direction from the numbers (PC: 54%)", "todo"),
item("CAP-03", "CAP", "Use intervention data", "todo"),
item("CAP-04", "CAP", "Declared knowledge as tiers, never edges", "blocked", blocked_by="AUD-48 (AB-07 live tier run, waits on Uzair)"),
item("CAP-05", "CAP", "Invariance to column order", "todo"),
item("CAP-06", "CAP", "Keep 'direction unknown' edges", "done",
     criterion="Refinement v1 keeps the algorithm's undirected edges unless the data contradict them; survival rate reported against the pipeline's 15-31%",
     evidence=["analysis/refinement_v1.py", "analysis/results/refinement_v1/dev.json", "analysis/results/refinement_v1/RULE.json", "analysis/reports/bnd09_bnd10_refinement.md"],
     checks=[J("analysis/results/refinement_v1/dev.json", ["summary", "all_edges_sourced"], "true"),
             J("analysis/results/refinement_v1/dev.json", ["summary", "nondirected_survival", "survive_v1"], "ge", 600),
             J("analysis/results/refinement_v1/RULE.json", ["KEEP"], "eq", 0.5)],
     note="Frozen 2026-10-11 (RULE.json sha256 da3cb260...). Dev (92 files: 69 live tables + 23 CausalArena dev replays): v1 keeps 663 of 697 "
          "non-directed algorithm edges (95%), the pipeline's bootstrap step 206 (30%). Test replay (25 files): 109 of 117 vs 61."),
item("CAP-07", "CAP", "Calibrated confidence per claim", "todo"),
item("CAP-08", "CAP", "Abstention / selective claims", "todo"),
item("CAP-09", "CAP", "Provenance per edge with an independent checker", "todo"),
item("CAP-10", "CAP", "Robustness to malformed model output", "in_progress",
     evidence=["harness/names_runner.py", "analysis/refinement_v2.py", "tests/test_refinement_v2.py", "analysis/reports/bnd11_prep.md"],
     checks=[J("tests/last_run.json", ["ok"], "true")],
     note="Schema-validated replies, one retry, then abstain; built and unit-tested (parse rule shared with refinement_v2). Closes on BND-11's live names run."),
item("CAP-11", "CAP", "Determinism (same inputs, same ledger hash)", "todo"),
item("CAP-12", "CAP", "Runtime at 20-40 variables", "todo"),
item("CAP-13", "CAP", "Nonlinear and mixed-type dependence", "todo"),
item("CAP-14", "CAP", "Hidden common causes (PAG marks)", "todo"),
item("CAP-15", "CAP", "'What if we set X?' with identification status and bounds", "todo"),
item("CAP-16", "CAP", "Choose the next experiment", "todo"),
item("CAP-17", "CAP", "Scoreboard packaging (CPDAG->DAG rule, summary.csv, validator)", "done",
     criterion="Every Q1 row packaged in CausalArena's submission format (summary.csv, predictions, manifest.json) and passed through tools/validate_submission.py",
     evidence=["analysis/package_submission.py", "analysis/results/submission/validator_output.txt", "analysis/results/submission/packages.json"],
     checks=[G("analysis/results/submission/validator_output.txt", r"exit code 0"), G("analysis/results/submission/packages.json", r"notears__shuffled")],
     note="10 packages (PC, GES, FCI, DirectLiNGAM, NOTEARS x released / shuffled columns), 600 rows each (semantic 250, formula 250, "
          "synthetic100); the official validator exits 0 on all 10. Nothing submitted."),
item("CAP-18", "CAP", "Cost per run measured at 25 variables", "todo"),
# ---------------- 7 Research questions
item("RQ-01", "RQ", "P1-P3 (pass 4b, Sachs): supported", "done", kind="question", evidence=[P4B, R + "pass4b_results.md"],
     criterion="Verdicts computed by pre-registered thresholds in stability.py",
     checks=[J(P4B, ["predictions", k, "verdict"], "eq", "SUPPORTED") for k in ("P1", "P2", "P3")]),
item("RQ-02", "RQ", "N2 (bundle 1): supported", "done", kind="question", evidence=[B1], checks=[J(B1, ["predictions", "N2", "verdict"], "eq", "SUPPORTED")]),
item("RQ-03", "RQ", "N1, N4, P3 (bundle 1): tested, inconclusive", "done", kind="question", evidence=[B1, R + "bundle1_results.md"],
     checks=[J(B1, ["predictions", k, "verdict"], "eq", "INCONCLUSIVE") for k in ("N1", "N4", "P3")],
     note="Closed as tested; the questions themselves remain open."),
] + [item("RQ-%02d" % (4 + i), "RQ", t, "open", kind="question", evidence=[R + "program_v2.md"]) for i, t in enumerate([
    "T1 Order source explains most directed-edge accuracy", "T2 Deployed agents take order from names and layout",
    "T3 Typed, sourced partial order: never below data-only, bounded harm, best published per regime (target)",
    "T4 Calibrated, machine-checkable claims with abstention", "T5 What-if answers with identification status",
    "T6 Experiment choice beats random on recorded experiments"])] + [
    item("RQ-%02d" % (10 + i), "RQ", t, "blocked", kind="question", blocked_by="AUD-48 (AB-07 live tier run, waits on Uzair)", evidence=[R + "program_v2.md"]) for i, t in enumerate([
    "O1 Real names: >=70% of true edges ordered correctly, <=10% contradicted", "O2 Neutral names give no order information",
    "O3 Moved names: tiers follow the labels", "O4 Regression on model tiers reaches 0.634 (semantic)", "O5 Same for formula vs 0.524"])] + [
    item("RQ-%02d" % (15 + i), "RQ", t, "open", kind="question") for i, t in enumerate([
    "Do LLM-written semantic graphs inflate name-based scores?", "Does PC's error pattern hold for other algorithms?",
    "Do results hold for a second model?"])] + [
# ---------------- 8 Build
item("BLD-01", "BLD", "Recording harness and analysis tools", "done", evidence=["manifests/evidence/BLD-01_tools_2026-10-12.sha256", "analysis/README.md"],
     checks=[{"t": "exists", "path": p} for p in ("harness/run_traced.py", "harness/run_plan.py", "harness/cc_trace.py", "analysis/lineage.py", "analysis/stability.py")]
            + [{"t": "manifest", "path": "manifests/evidence/BLD-01_tools_2026-10-12.sha256"}],
     criterion="Every tool listed in analysis/README.md with its gates",
     note="Tool manifest re-taken 2026-10-12 after neutral_leak_scan.py learned label variants and scenario words from MAPPING "
          "(rerun on bundle 1: identical result, 0 leaks); the 10-09 manifest stays as history."),
item("BLD-02", "BLD", "B1 data-only claim ledger with invariants I1-I4, I7", "todo"),
item("BLD-03", "BLD", "B2 interventions as order evidence", "todo"),
item("BLD-04", "BLD", "B3 declared knowledge as tiers", "blocked", blocked_by="AUD-48 (AB-07 live tier run, waits on Uzair)"),
item("BLD-05", "BLD", "B4 confidence, calibration, selective output", "todo"),
item("BLD-06", "BLD", "Drop-in replacement for Causal-Copilot's refinement stage", "in_progress",
     evidence=["analysis/refinement_v1.py", "analysis/refinement_v2.py", "analysis/results/refinement_v2/" + "RULE.json", "analysis/results/refinement_v2/" + "dev.json", "analysis/reports/bnd11_prep.md"],
     checks=[J("analysis/results/refinement_v2/" + "dev.json", ["summary", "all_edges_sourced"], "true"), J("analysis/results/refinement_v2/" + "dev.json", ["summary", "R1", "verdict"], "eq", "SUPPORTED")],
     note="v1 frozen and tested (BND-10). v2 frozen 2026-10-12 (sha256 443354d8...): data part never deletes algorithm adjacencies; dev R1-R3 "
          "supported (92 files). Held-out: formula test replay (compute job) and the live names run (R4-R6)."),
item("BLD-07", "BLD", "C1 what-if answers with identification status and bounds", "todo"),
item("BLD-08", "BLD", "C2 next-experiment choice from recorded pool", "todo"),
item("BLD-09", "BLD", "Scoreboard-format export", "todo"),
item("BLD-10", "BLD", "Evidence tracker for this list (catalogue, verify, Slack List mirror)", "done", evidence=["tracker/verify.py", "tracker/README.md"],
     checks=[{"t": "exists", "path": "tracker/verify.py"}, {"t": "exists", "path": "tracker/status.json"}]),
item("BLD-11", "BLD", "Correlation layer: typed links between dev tickets, prod items, evidence, runs, docs and Slack; agent contract", "done",
     criterion="Typed link registry with prod namespace, immutable IDs, derived prod status, suspect-link reviews and Slack mirror check; "
               "every failure mode in LINKS.md section 6 caught by the self-test; AGENTS.md read by CLAUDE.md",
     evidence=["tracker/trace.py", "tracker/LINKS.md", "tracker/selftest_trace.py", "tracker/selftest_trace.json", "AGENTS.md", "CLAUDE.md"],
     checks=[J("tracker/selftest_trace.json", ["ok"], "true"), J("tracker/selftest_trace.json", ["total"], "ge", 26),
             G("CLAUDE.md", r"@AGENTS\.md"), G("AGENTS.md", r"Never send a message in #causal-discovery")],
     reproduce="python tracker/selftest_trace.py", reopen_if=["trace.py or LINKS.md changes without a passing self-test"]),
item("BLD-12", "BLD", "Prod list in the dev encoding (groups and pass-through rows) and the Slack relay for milestones, summaries and artifacts", "done",
     criterion="Uzair's curation applied as prod rows with derived statuses and overclaim gates; relay.py prepares, records and checks "
               "messages per channel; every new failure mode caught by the self-test",
     evidence=["tracker/relay.py", "tracker/RELAY.md", "tracker/prod_spec.json", "tracker/selftest_trace.json"],
     checks=[J("tracker/selftest_trace.json", ["ok"], "true"), J("tracker/selftest_trace.json", ["total"], "ge", 40),
             G("tracker/RELAY.md", r"A prod message is sent only by Uzair"), G("tracker/prod_spec.json", r"Replicate Causal-Copilot paper claims and results")],
     reproduce="python tracker/selftest_trace.py", reopen_if=["prod_spec.json changes without prod-apply; relay.py changes without a passing self-test"]),
item("BLD-13", "BLD", "Claim-ledger record format, JSON Schema and verifier (V1-V8)", "done",
     criterion="Design names the failures the format prevents; schema generated from one source; verifier passes a toy ledger and catches each of eight corruptions",
     evidence=["ledger/DESIGN.md", "ledger/schema.py", "ledger/schema/ledger.schema.json", "ledger/verify.py", "tests/test_ledger_verify.py"],
     checks=[G("ledger/DESIGN.md", r"What the format must make impossible"), G("ledger/schema/ledger.schema.json", r"cc-claim-ledger/0\.1")],
     reproduce="python ledger/schema.py && python tests/test_ledger_verify.py",
     note="No discovery engine yet; PROV-O export and causal-cmd/Tetrad interop are later steps."),
item('BLD-14', 'BLD', 'Claim ledger v0.2: plan and deviations, assumptions, lineage, reviews, question; verifier reports every check', 'todo', kind='task',
     criterion='Fields for the five gaps AB-13 ranks (plan fixed before data with deviations; identifying assumptions and sensitivity; data lineage pointer; human review records; question / context of use / estimand), the AB-11 findings (verifier reports V2-V8 even when V1 fails; a y->x relation or an explicit orientation convention; knowledge-file import records required edges on unconnected pairs as overrides), each with a verifier test',
     evidence=['analysis/audits/AB13_regulation_map.md', 'analysis/audits/AB11_vendor_claims.md'], checks=[], note='Found 2026-10-13 by AB-11 and AB-13.'),
# ---------------- 9 Evaluation protocol
item("EVL-01", "EVL", "Every score states its regime (D / D+I / D+K / D+I+K)", "done", kind="rule",
     criterion="Every results directory carries a CONTRACT.json stating its regime (per file where mixed) and every new score row states it; analysis/check_scores.py rejects any that do not",
     evidence=[R + "program_v2.md", "analysis/score_record.py", "analysis/check_scores.py"],
     checks=[J("analysis/results/score_contract_report.json", ["nonconforming"], "len_eq", 0), G("analysis/score_record.py", r'REGIMES = \{"D", "D\+I", "D\+K", "D\+I\+K"\}')]),
item("EVL-02", "EVL", "Controls on every score (columns shuffled; names real/neutral/moved; supplier; interventions)", "done", kind="rule",
     criterion="Every score states its controls (column order, name arm, supplier, knowledge source when K is present); the checker rejects any that do not. "
               "A score without a shuffled-column counterpart says so in its controls; the Q1 suite S2 and BND-06 add the shuffled arms.",
     evidence=[R + "program_v2.md", "analysis/score_record.py", "analysis/check_scores.py"],
     checks=[J("analysis/results/score_contract_report.json", ["nonconforming"], "len_eq", 0), G("analysis/score_record.py", r"regime includes K but controls.knowledge_source is missing")]),
item("EVL-03", "EVL", "Metric set: F1, skeleton P/R, direction accuracy, coverage, calibration, interventional error, cost", "done", kind="rule",
     criterion="The metric set is defined once (score_record.STANDARD_METRICS); every reported metric is defined in its directory's contract, with the SHD variant and the orientation rule named",
     evidence=["analysis/cc_graph.py", "analysis/error_budget.py", "analysis/score_record.py"],
     checks=[J("analysis/results/score_contract_report.json", ["nonconforming"], "len_eq", 0), G("analysis/score_record.py", r"an SHD metric is reported but shd_variant is not named")]),
item("EVL-04", "EVL", "Predictions and thresholds fixed in code before every live run", "done", kind="rule",
     evidence=["analysis/stability.py"], checks=[G("analysis/stability.py", r"P1_HI, P1_LO, P1_N"), G("analysis/stability.py", r"N4_HI, N4_LO, N4_N")]),
item("EVL-05", "EVL", "Development / held-out split by scenario number before any tuning", "done", kind="rule",
     criterion="plans/splits.json frozen before any tuning: 25 / 25 scenarios per family, disjoint, regenerable byte-for-byte; earlier data declared dev",
     evidence=["plans/splits.json", "analysis/make_splits.py"],
     checks=[J("plans/splits.json", ["families", "semantic", "dev"], "len_eq", 25), J("plans/splits.json", ["families", "semantic", "test"], "len_eq", 25),
             J("plans/splits.json", ["families", "formula", "dev"], "len_eq", 25), J("plans/splits.json", ["families", "semantic", "s2_test_scenarios"], "len_eq", 10),
             J("tests/last_run.json", ["ok"], "true")],
     reproduce="python analysis/make_splits.py --root external/causalarena --out plans/splits.json (unit test checks byte identity)"),
item("EVL-06", "EVL", "Stage-by-stage scoring of any pipeline", "done", kind="rule", evidence=["analysis/lineage.py", "analysis/partial_stages.py"],
     checks=[{"t": "exists", "path": "analysis/partial_stages.py"}]),
item("EVL-07", "EVL", "Must-show list and gates for every live step", "done", kind="rule",
     evidence=[R + "bundle1_design.md", R + "pass4b_design.md"], checks=[G(R + "bundle1_design.md", r"Must-show list")]),
# ---------------- 10 Infrastructure
item("INF-01", "INF", "Harness v3, Docker image, cc.ps1 commands, stub LLM, plan runner, fetcher", "done",
     evidence=["cc.ps1", "harness/fetch_external.py", "manifests/evidence/INF-01_docker_2026-10-10.sha256"], checks=[G("cc.ps1", r'"fetch"'), G("harness/fetch_external.py", r"begin_source")]),
item("INF-02", "INF", "Analysis tools with gates", "done", evidence=["analysis/README.md"], checks=[G("analysis/README.md", r"Tools and their gates")]),
item("INF-03", "INF", "External data on disk (CausalArena 1.57 GB; 8 Causal Chambers datasets)", "done", evidence=[FR],
     checks=[J(FR, ["errors"], "len_eq", 0), J(FR, ["extracted"], "len_eq", 8)]),
item("INF-04", "INF", "Compute-job command on Uzair's machine (sandbox caps steps at 180 s)", "done",
     criterion="cc.ps1 compute runs a jobkit script in the container with no network, the repo read-only and an empty .env; "
               "J1 (chunked == one-shot output hash, in the shell and in the container) and J2 (no key, no network, empty .env) pass",
     evidence=["harness/compute_job.py", "analysis/jobkit.py", "analysis/smoke_job.py", "cc.ps1", "jobs/gates.json", "jobs/smoke_container/log.jsonl"],
     checks=[J("jobs/gates.json", ["J1_shell"], "true"), J("jobs/gates.json", ["J1_container"], "true"), J("jobs/gates.json", ["J2"], "true")],
     reproduce="powershell -ExecutionPolicy Bypass -File .\\cc.ps1 compute smoke_container.json ; python analysis/job_gates.py",
     note="Container run 2026-10-11 (Uzair): 4 chunks, each stopped by its 4 s budget and resumed; output sha256 84e50886... identical to "
          "the one-shot and shell runs; J2 printed in every chunk: no secret-like variables, no network, /app/.env size 0."),
item("INF-05", "INF", "Unit tests for our code; caching by content hash", "done",
     criterion="Unit tests for the scorer, graph conversions, CPDAG/Meek, job resumption, the score contract and the splits pass; jobkit keys cached results by input sha256",
     evidence=["tests/test_core.py", "tests/run_tests.py", "analysis/jobkit.py"],
     checks=[J("tests/last_run.json", ["ok"], "true"), J("tests/last_run.json", ["ran"], "ge", 18), G("analysis/jobkit.py", r"def input_key")],
     reproduce="python tests/run_tests.py"),
item("INF-06", "INF", "Public repository preparation (no keys, licences, no redistribution, run-record size)", "todo"),
item("INF-07", "INF", "One command reproduces every number in the report", "todo"),
# ---------------- 11 Course
item("CRS-01", "CRS", "TA check-in 1 (TA: Nate)", "todo", kind="deadline", due="2026-10-29",
     note="Rescheduled: Thursday 29 Oct 2026, 10:45 am PT (Uzair, 19 Oct)."),
item("CRS-02", "CRS", "Quarter 1 checkpoint", "todo", kind="deadline", due="2026-11-02"),
item("CRS-03", "CRS", "TA check-in 2", "todo", kind="deadline", due="2026-11-20"),
item("CRS-04", "CRS", "Quarter 1 final (50%)", "todo", kind="deadline", due="2026-12-04"),
item("CRS-05", "CRS", "Quarter 2 proposal: written proposal, weekly schedule, 2-3 min pitch (15%)", "todo", kind="deadline"),
item("CRS-06", "CRS", "Quarter 2 deliverables: public repo, website, PDF report, poster; showcase 2nd week of March 2027", "todo", kind="deadline"),
item("CRS-07", "CRS", "Decision gate G1", "todo", kind="deadline", due="2026-10-16"),
# ---------------- 12 Team
item("TEAM-01", "TEAM", "Causal Discovery section for the shared mentor document", "in_progress",
     evidence=["project:claude/shared-doc-causal-section-draft.md"], note="v3 ready; 'Proposed project' part waits on DEC-01."),
item("TEAM-02", "TEAM", "Plain-language explainer for meetings, saved as a file", "done", evidence=["docs/meeting_explainer.md", R + "bundle1_results.md"],
     criterion="docs/meeting_explainer.md exists and matches current numbers",
     checks=[G("docs/meeting_explainer.md", r"directed-edge F1\) \*\*0\.68\*\*"), G(R + "bundle1_results.md", r"directed-edge F1 0\.09 -> 0\.68"),
             G("docs/meeting_explainer.md", r"\*\*0\.02\*\*; with swapped names to \*\*0\.07\*\*"), G(R + "bundle1_results.md", r"0\.08 -> 0\.02; swapped \(13\) 0\.50 -> 0\.26, 0\.04 -> 0\.07"),
             G(R + "bundle1_results.md", r"real 141 of 152 \(93%\).*swapped 112 of 125 \(90%\)"), G(R + "bundle1_results.md", r"Total crashes: 12 of 84"),
             G(R + "bundle1_results.md", r"100 of 336 \(29\.8%\)")],
     reopen_if=["a newer run set supersedes bundle 1's numbers (the explainer must be regenerated)"],
     note="Written 2026-10-10 for TA check-in 1 (19-23 Oct); each number is tied to its source line by a check."),
item("TEAM-03", "TEAM", "Recruit at least one teammate", "todo"),
item("TEAM-04", "TEAM", "Ask the mentor: group of 2-3 in Q2? Scope of 'replicate, measure, strengthen'?", "todo"),
item("TEAM-05", "TEAM", "Do not count on answers from Prof. Huang's group", "done", kind="rule", evidence=[LED, "project:claude/causal-copilot-research-ledger.md (DECISIONS)"],
     checks=[G(LED, r"do not count on any answer from Prof\. Huang")]),
item("TEAM-06", "TEAM", "Weekly status post", "todo"),
item("TEAM-07", "TEAM", "Tailored public goals post in #causal-discovery", "done", evidence=["slack:C0C8CQK1XME/1791580546.004809", "slack:C0C8CQK1XME/1791613267.243749", "tracker/relay_out/20261010T061713Z_digest_prod.md"],
     checks=[G("tracker/relay_out/20261010T061713Z_digest_prod.md", r"first digest, no earlier baseline")],
     criterion="Goals index, status legend and the first prod digest posted in #causal-discovery",
     note="Index and status legend posted by Uzair on 9 Oct; first prod digest sent by Uzair (ts 1791613267.243749, recorded 11 Oct)."),
# ---------------- 13 External
item("EXT-01", "EXT", "Note to CausalArena's maintainers about column order", "open", kind="decision", blocked_by="Uzair's decision (DEC-03)",
     evidence=[PROT, R + "bnd04_results.md"],
     note="Strengthened by BND-04: the authors' own baseline code orients undecided edges by column index on a topologically ordered release "
          "(PC F1 0.335 -> 0.396, FCI 0.322 -> 0.521 under that rule)."),
item("EXT-02", "EXT", "Scoreboard submission package with regime and controls stated", "todo"),
item("EXT-03", "EXT", "Bug report to Causal-Copilot upstream (cycle-step key; empty startup answer)", "open", kind="decision",
     note="Evidence grows: 15 of 15 live entries into the cycle step crashed at judge_functions.py:562 (9 bundle 1, 6 S2)."),
item("EXT-04", "EXT", "Paper: evaluations track or workshop", "todo"),
item("EXT-05", "EXT", "Course website, poster, report", "todo"),
# ---------------- 14 Stretch
item("STR-01", "STR", "E1 Field-wide audit of agents and LLM-assisted methods", "open", kind="stretch"),
item("STR-02", "STR", "E2 Public agent track", "open", kind="stretch"),
item("STR-03", "STR", "E3 Real experiments via the Causal Chambers remote lab", "open", kind="stretch"),
item("STR-04", "STR", "E4 Learned fusion (pretrained network with unreliable tier statements)", "open", kind="stretch"),
item("STR-05", "STR", "E5 Hidden confounders, time series, 100+ variables", "open", kind="stretch"),
item("STR-06", "STR", "Product angle: auditable causal analyst", "open", kind="stretch"),
# ---------------- 15 Decisions and risks
item("DEC-01", "DEC", "Adopt, redirect or enlarge program v2; which of E1-E5 in scope", "open", kind="decision"),
item("DEC-02", "DEC", "Approve the tier-elicitation test (~900 short calls through Uzair's key)", "done", kind="decision", criterion="Uzair's decision recorded with what it approves", evidence=["docs/decisions/2026-10-12_audit_dag.md"], checks=[G("docs/decisions/2026-10-12_audit_dag.md", r"DEC-02 tier-elicitation test \(AB-07\) \| approved")], note="Approved 2026-10-12 with the audit DAG; the run is AUD-48 (AB-07)."),
item("DEC-03", "DEC", "Whether to tell CausalArena's maintainers about the column order", "open", kind="decision"),
item("DEC-04", "DEC", "Connect Slack; tracker in private #cd-tracker", "done", kind="decision", evidence=[LED, "slack:C0C7Q2CA2G7"],
     checks=[G(LED, r"#cd-tracker \(C0C7Q2CA2G7")]),
] + [item("RSK-%02d" % (1 + i), "RSK", t, "open", kind="risk") for i, t in enumerate([
    "LLM-written semantic graphs make names 'work' for the wrong reason (guard: formula + Causal Chambers alongside)",
    "Data-only system may not reach GIES 0.552 (guard: claim targets only where they hold)",
    "Scope too large for one person (guard: decision gates; tracks shrink in fixed order)",
    "Prior work closes the gap first (guard: dated measurements; positioning kept current)",
    "Benchmark files change (guard: dated result; shuffling stays a required control)",
    "Model snapshot changes mid-study (guard: snapshot per call; one per comparison)",
    "Thresholds tuned after seeing results (guard: thresholds in code, hashed plans, held-out split)",
    "Sandbox limits 180 s per step (guard: compute command on Uzair's machine)"])]


# ---------------- 16 Bundles: definitions come from plans/q1_dag.json (approved 2026-10-10); status and evidence are set here.
# A bundle's must-show list is its closing criterion; it may be marked done only when every ticket it closes is done (trace T11).
BUNDLE_STATUS = {"BND-01": "done", "BND-02": "in_progress", "BND-03": "in_progress", "BND-04": "done", "BND-05": "done",
                 "BND-06": "in_progress", "BND-07": "done", "BND-08": "in_progress", "BND-09": "done", "BND-10": "in_progress", "BND-11": "in_progress", "BND-12": "in_progress"}
BUNDLE_EVIDENCE = {"BND-01": ["jobs/gates.json", "jobs/smoke_container/log.jsonl", "jobs/smoke/log.jsonl", "tests/last_run.json", "plans/splits.json",
                              "analysis/check_scores.py"],
                   "BND-05": ["datasets/suite_q1s2/MAPPING.json", "manifests/evidence/suite_q1_2026-10-10.sha256", "docs/q1/datasets.md",
                              "docs/meeting_explainer.md", "analysis/results/reference_reliability/reliability.json"],
                   "BND-04": [MV + "bnd04_verdicts.json", R + "bnd04_results.md", MV + "gesbic_semantic_obs.json", MV + "fci_semantic_obs.json", PROT],
                   "BND-03": [B3 + "rep04_paper_vs_code.md", B3 + "rep03_headline_claims.md", B3 + "aud12_effect_estimation.md",
                              B3 + "aud14_wrappers_webdemo_report.md", B3 + "aud15_upstream.md", CIT, "analysis/results/bnd03_tree_check.json"],
                   "BND-02": [LB2 + "rep13_claims.md", LB2 + "dom07_deep_reads.md", LB2 + "dom08_calibration_choice.md",
                              LB2 + "dom10_active_design_baselines.md", LB2 + "dom11_pretrained_models.md", LB2 + "rep12_causalman.md"],
                   "BND-08": ["analysis/results/stability_s2/bnd08_summary.json", "analysis/reports/bnd08_s2_results.md", "plans/results/20261012T002122Z_bnd08_live.result.json", "plans/bnd08_stub.json", "plans/bnd08_live.json", "analysis/s2_analysis.py", "analysis/bootstrap_replay_ca.py",
                              "manifests/evidence/bnd08_prereg_2026-10-11.sha256"],
                   "BND-06": [MV + "bnd06_verdicts.json", MV + "bnd06_families.json", MV + "bnd06_c1_recheck.json", R + "bnd06_interim.md",
                              R + "bnd06_families.md", "plans/bnd06_prereg.json", "analysis/notears_linear.py", "analysis/results/submission/validator_output.txt"],
                   "BND-07": ["analysis/intervention_audit.py", IA, "external/causalchamber_pkg/causalchamber-0.2.8-py3-none-any.whl",
                              "analysis/results/chambers/mapping.json", "analysis/results/chambers/one_layer_deep.json", "analysis/results/chambers/rep09_ges.json", "analysis/reports/bnd07_chambers.md"],
                   "BND-09": ["analysis/refinement_v1.py", "analysis/results/refinement_v1/dev.json", "analysis/results/refinement_v1/dev_exploratory.json",
                              "analysis/results/refinement_v1/RULE.json", "analysis/reports/bnd09_bnd10_refinement.md", "jobs/bootstrap_replay_ca_dev/out/replay_dev.json"],
                   "BND-12": ["analysis/results/rep11/rep11_sachs_data.json", "analysis/reports/rep11_sachs_data.md"],
                   "BND-11": ["analysis/refinement_v2.py", "analysis/results/refinement_v2/" + "RULE.json", "analysis/results/refinement_v2/" + "dev.json", "plans/bnd11_names_requests.jsonl",
                              "harness/names_runner.py", "analysis/reports/bnd11_prep.md", "manifests/evidence/bnd11_prereg_2026-10-12.sha256"],
                   "BND-10": ["analysis/results/refinement_v1/test_live_s2.json", "analysis/refinement_v1_test_live.py", "analysis/results/refinement_v1/test_replay.json", "analysis/results/refinement_v1/access_log.jsonl",
                              "analysis/reports/bnd09_bnd10_refinement.md", "jobs/bootstrap_replay_ca_test/out/replay_test.json"]}
BUNDLE_CHECKS = {"BND-01": [J("jobs/gates.json", ["J1_shell"], "true"), J("jobs/gates.json", ["J1_container"], "true"), J("jobs/gates.json", ["J2"], "true"),
                            J("tests/last_run.json", ["ok"], "true")],
                 "BND-05": [{"t": "manifest", "path": "manifests/evidence/suite_q1_2026-10-10.sha256"},
                            {"t": "exists", "path": "docs/meeting_explainer.md"},
                            G("docs/q1/datasets.md", r"### s2_10: ")],
                 "BND-03": [J(CIT, ["ok"], "true"), J("analysis/results/bnd03_tree_check.json", ["ok"], "true")],
                 "BND-04": [J(MV + "bnd04_verdicts.json", ["gates", "C1"], "true")],
                 "BND-08": [{"t": "manifest", "path": "manifests/evidence/bnd08_prereg_2026-10-11.sha256"}],
                 "BND-09": [J("analysis/results/refinement_v1/dev.json", ["summary", "R3", "verdict"], "eq", "SUPPORTED"),
                            J("analysis/results/refinement_v1/RULE.json", ["sha256"], "eq", "da3cb260c1e25bb90e4cc2ad7e766db0f63ca4048fa60c456ed0a8f95287a962")],
                 "BND-11": [{"t": "manifest", "path": "manifests/evidence/bnd11_prereg_2026-10-12.sha256"}],
                 "BND-10": [J("analysis/results/refinement_v1/test_live_s2.json", ["pooled_test", "files"], "eq", 55),
                            J("analysis/results/refinement_v1/test_replay.json", ["summary", "files"], "eq", 25),
                            J("analysis/results/refinement_v1/test_replay.json", ["rule_sha256"], "eq", "da3cb260c1e25bb90e4cc2ad7e766db0f63ca4048fa60c456ed0a8f95287a962")]}
BUNDLE_STATUS.update({b: "todo" for b in ("AB-01", "AB-02", "AB-03", "AB-04", "AB-05", "AB-06", "AB-07", "AB-08", "AB-09", "AB-10", "AB-11", "AB-12", "AB-13", "AB-14", "AB-15", "AB-16", "AB-17")})

BUNDLE_STATUS.update({'AB-01': 'done', 'AB-02': 'blocked', 'AB-03': 'done', 'AB-04': 'done', 'AB-05': 'blocked', 'AB-06': 'todo', 'AB-07': 'blocked', 'AB-08': 'done', 'AB-09': 'done', 'AB-10': 'blocked', 'AB-11': 'done', 'AB-12': 'done', 'AB-13': 'done', 'AB-14': 'todo', 'AB-15': 'done', 'AB-16': 'todo', 'AB-17': 'todo'})

BUNDLE_NOTE = {"BND-01": "Closed 2026-10-11 after Uzair's container smoke run: J1 (shell and container) and J2 pass; 18 unit tests pass; every result directory has a CONTRACT.json (check_scores: none non-conforming).",
               "BND-05": "Built 2026-10-10; gates D1-D11 pass and the rebuild is byte-identical (--check). Marked done 2026-10-11 once BND-01 closed (rule W3).",
               "BND-04": "Built 2026-10-10: RQ-16, REP-06, BEN-08 done; marked done 2026-10-11 once BND-01 closed (W3). BEN-11 continues in BND-06.",
               "BND-03": "Static audit done (gates A1, A2 pass); open: REP-03 live-only claims, AUD-14 one offline stub run of a time-series wrapper.",
               "BND-02": "REP-13, DOM-08, DOM-10, DOM-11, DOM-12 done; DOM-07 waits on CausalArena appendix B (unreadable so far).",
               "BND-08": "Live run 11-12 Oct: 30 runs, 24 completed, 6 crashed at the cycle step, all reached S3. M1 SUPPORTED, M2 REFUTED (5/10), M3 SUPPORTED, M4 SUPPORTED, M5 not run; L1 and Q1-Q3 pass; about $12.7. Open: DLV-02's gap (6 arms without a completed run), Uzair's call.",
               "BND-06": "Q4c refuted (PC order-dependent; mechanism: the vendored causal-learn 0.1.3.8 skeleton). Formula and synthetic100 done for 5 methods; C1 re-established; CAP-17 package validated (10 packages); DOM-09 done. Open only: AVICI (checkpoint only on huggingface.co, blocked) for REP-07, BEN-07, BEN-11.",
               "BND-07": "Done 2026-10-12: BEN-09 (intervention audit), BEN-10 (mapping, one-layer-deep check: no contradiction of the graphs, obs+int sample), REP-09 (GES CPDAG identical to the authors'; CDFM not reproducible here).",
               "BND-09": "Done 2026-10-11. Dev, 92 files (69 live tables, 23 CausalArena dev replays): R1 0.79 INCONCLUSIVE, R2 0.96 SUPPORTED, R3 +0.023 SUPPORTED; non-directed edges kept 95% vs the pipeline's 30%. Frozen: RULE.json sha256 da3cb260..., 01:11:03Z.",
               "BND-12": "Free part started 2026-10-12: REP-11's data-only Sachs numbers reproduced within 0.05 (conditional: Sachs has no data-identifiable direction). Live parts (second model, CARE control, LLM and fused Sachs numbers) wait on Uzair.",
               "BND-11": "Prepared 2026-10-12: v2 frozen (data part never deletes; dev R1-R3 supported), 786 names questions over the 30 S2 tables (under $1), runner with retry/abstain, stub-tested. Waits on Uzair: formula replay jobs (free), names stub (free), names live.",
               "BND-10": "Measured 2026-10-12 (must-show complete; marked done once BND-08 closes, rule W3). Pooled held-out (55 tables): R1 INCONCLUSIVE 40/55, R2 INCONCLUSIVE 47/55, R3 SUPPORTED -0.003. Live S2 alone: R1 REFUTED 17/30, R2 SUPPORTED 30/30. TGT-09 not met; carried to BND-11 (v2)."}


def _bundle_items():
    import json as _json, os as _os
    plan = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "plans", "q1_dag.json"), encoding="utf-8"))
    out = []
    for b in plan["bundles"]:
        out.append(item(b["id"], "BND", b["title"], BUNDLE_STATUS.get(b["id"], "todo"), kind="bundle",
                        criterion="Must show: " + "; ".join(b["must_show"]), due=b["window"][1],
                        evidence=BUNDLE_EVIDENCE.get(b["id"], ()), checks=BUNDLE_CHECKS.get(b["id"], ()),
                        note=(BUNDLE_NOTE.get(b["id"], "") + " " if b["id"] in BUNDLE_NOTE else "")
                             + "Runner: %s. API spend: %s." % (b["runner"], b["llm_cost"])))
    return out


ITEMS += _bundle_items()


# ---------------- Items created in comprehensions, replaced by id (BND-04, 2026-10-10)
_OVERRIDE = {i["id"]: i for i in [
item("RQ-16", "RQ", "Does PC's error pattern hold for other algorithms?", "done", kind="question",
     criterion="Q4a-b verdicts (GES and FCI direction accuracy and the cost of direction errors) from BND-04",
     evidence=[MV + "bnd04_verdicts.json", MV + "error_budget_gesbic.json", MV + "error_budget_fci.json", R + "bnd04_results.md"],
     checks=[J(MV + "bnd04_verdicts.json", ["Q4a", "verdict"], "eq", "REFUTED"), J(MV + "bnd04_verdicts.json", ["Q4b", "verdict"], "eq", "INCONCLUSIVE"),
             J(MV + "bnd04_verdicts.json", ["gates", "C1"], "true"), J(MV + "bnd04_verdicts.json", ["gates", "files_250_each"], "true")],
     reproduce="python analysis/method_error_budget.py --rows analysis/results/methods/gesbic_semantic_obs.json --published GIES --out analysis/results/methods/error_budget_gesbic.json; same for fci; python analysis/bnd04_summary.py",
     note="No. Committed-direction accuracy GES 0.807, FCI 0.798 (PC 0.544): Q4a refuted. Cost of direction errors GES 0.117, FCI 0.228 "
          "(PC 0.276): Q4b inconclusive. FCI's cost is undecided pairs (73% of found true adjacencies), not wrong arrows. "
          "PC's 0.544 is for the released (topological) order; shuffled it is 0.722 (BND-06), so the pattern was order-specific too."),
]}
ITEMS = [_OVERRIDE.get(_i["id"], _i) for _i in ITEMS]


# ---------------- Closing criteria written in BND-01 (2026-10-10) for in-scope tickets that had none
CRITERIA = {
    "AUD-14": "Torch and time-series wrappers, the web-demo path and report generation audited like the discovery path (file:line findings; one stub run where it runs offline)",
    "BEN-07": "For every method we can run, F1 on released vs shuffled column order measured; whether CausalArena's own wrappers shuffle stated from their code or recorded as unknowable",
    "BEN-08": "The SHD variant that reproduces the published 33.5 identified on the stored PC outputs, or every candidate variant shown not to",
    "BEN-09": "For every declared intervention in the replay sampler's data, whether the target's distribution moves (KS, Holm 1%); the in-name-only count reported",
    "BEN-10": "Each of the 8 Causal Chambers datasets mapped to its ground-truth graph and source; 'one layer deep' validation checked; an obs+int sample built under a stated rule",
    "BEN-11": "Error budgets (ceiling -> skeleton -> direction) for GES, FCI, DirectLiNGAM, NOTEARS and CPU-runnable pretrained models on semantic, formula and a 100-file synthetic sample",
    "BEN-12": "Reliability of each Q1 reference graph stated with its source (Sachs variants, Auto MPG mismatch, the others' provenance)",
    "DOM-12": "Scoping note: what Causal-Copilot offers for hidden confounders, time series and 100+ variables, what Q1 covers, what moves to Q2",
    "RQ-16": "Q4a-b verdicts (GES and FCI direction accuracy and the cost of direction errors) from BND-04",
    "RQ-17": "Second model on the S1 arms: N2 and P1 replicated or not (S1, S2 in BND-12)",
    "CAP-06": "Refinement v1 keeps the algorithm's undirected edges unless the data contradict them; survival rate reported against the pipeline's 15-31%",
    "CAP-10": "Every model reply schema-validated with one retry, then abstain; zero crashes over the BND-11 runs",
    "TGT-09": "R1 supported on the test split: v1 adjacency F1 >= algorithm output - 0.02 in >= 90% of files",
    "TGT-13": "Zero crashes from malformed model output over the BND-11 runs",
    "BLD-06": "v1/v2 take the pipeline's recorded inputs and return its output format with a source on every edge; R1-R6 reported",
    "INF-06": "Public tree: secret scan clean, licences stated, no redistributed benchmark data, no classmates' names, run records within size limits",
    "CAP-17": "Every Q1 row packaged in CausalArena's submission format (summary.csv, predictions, manifest.json) and passed through tools/validate_submission.py",
    "INF-07": "One command regenerates every number in the final report on a clean copy, byte-for-byte or within stated tolerance",
}
for _i in ITEMS:
    if not _i["criterion"] and _i["id"] in CRITERIA:
        _i["criterion"] = CRITERIA[_i["id"]]


# Done tickets whose evidence was a directory now pin a dated manifest (2026-10-10); each manifest is also checked file by file.
for _i in ITEMS:
    for _e in _i["evidence"]:
        if _e.startswith("manifests/evidence/") and not any(c.get("t") == "manifest" and c.get("path") == _e for c in _i["checks"]):
            _i["checks"].append({"t": "manifest", "path": _e})
BUNDLE_NOTE.update({'AB-01': 'Controlled leaderboard written; see ab01 report.', 'AB-02': 'gCastle alarm: no causal order. Waits on Uzair: Bayesys download.', 'AB-03': 'dodiscover PC fails the oracle test (cyclic output); pgmpy, tigramite correct.', 'AB-04': "Five benchmarks; learned graphs near 'nothing moves' on CausalArena, clearer lift on Causal Chambers.", 'AB-05': 'Stub runs pass for 4 agents; waits on Uzair: live probes (caps $3.55 + $0.03).', 'AB-06': 'Budget proposed (~$57); needs AB-05 live costs, then approval.', 'AB-07': '900 requests pre-registered (~$3.1). Waits on Uzair: cc.ps1 tiers.', 'AB-08': '2,500-file rho-dial benchmark; reference curves as predicted.', 'AB-09': 'T1-T4 hold; T5 restated; 7,151 rows checked.', 'AB-10': 'Kit ready. Waits on Uzair: IRB question to course staff, then interviews.', 'AB-11': '33 tools by docs, 10 by hand; no tool records evidence-linked direction sources.', 'AB-12': 'PetShop: declared topology + abstention 0.93 AC@3 vs PC graph 0.21 (P15 supported).', 'AB-13': '50 requirements mapped; 5 ledger gaps (BLD-14); venue W3C AI provenance CG.', 'AB-14': 'Scaffold only; waits on AB-10.', 'AB-15': 'All five claims partly open; mandatory citations listed.', 'AB-16': 'Gate on 14 Nov.', 'AB-17': 'After AB-16.'})

# ---- overrides p04 (2026-10-13): live results and follow-ups; applied by id after the items above are built
_P04 = {
    "AUD-48": dict(status="done", blocked_by=None,
                   evidence=["analysis/a3_make_requests.py", "harness/tiers_runner.py", "analysis/a3_score.py", "plans/a3_prereg.json",
                             "plans/a3_tiers_requests.jsonl", "plans/a3_scenarios.json", "analysis/results/a3/a3.json",
                             "analysis/results/a3/selftest.json", "analysis/a3_orient_only.py", "analysis/results/a3/a3_orient_only.json",
                             "analysis/reports/ab07_knowledge_elicitation.md", "tests/test_tiers_runner.py"],
                   checks=[J("plans/a3_prereg.json", ["requests"], "eq", 900), J("analysis/results/a3/a3.json", ["requests_answered"], "eq", 900),
                           J("analysis/results/a3/a3.json", ["verdicts", "O4", "verdict"], "eq", "refuted"),
                           G("analysis/reports/ab07_knowledge_elicitation.md", r"Pre-registered verdicts")],
                   note="Live 13 Oct (gpt-4o-2024-08-06, 914 calls, about $2.08). O1 inconclusive (69.4% correct, 12.1% contradicted), "
                        "O2 supported, O3 supported by data, O4 refuted (0.448), O5 refuted (0.384). Orient-only use of the tiers "
                        "(exploratory): GES 0.528 -> 0.546 semantic."),
    "RQ-10": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json", "analysis/reports/ab07_knowledge_elicitation.md"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O1", "verdict"], "eq", "inconclusive")],
                  note="Answered 13 Oct: no, narrowly: 69.4% of true edges ordered correctly, 12.1% contradicted (semantic, consensus tiers)."),
    "RQ-11": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O2", "verdict"], "eq", "supported")],
                  note="Answered 13 Oct: yes. With neutral names the model puts every variable in one tier."),
    "RQ-12": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O3", "by_data", "verdict"], "eq", "supported")],
                  note="Answered 13 Oct: yes. Moved names: ordering follows the labels (72% correct by label) and is worse than chance by data."),
    "RQ-13": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O4", "verdict"], "eq", "refuted")],
                  note="Answered 13 Oct: no. Regression on the model's tiers 0.448 (oracle depth 0.714)."),
    "RQ-14": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O5", "verdict"], "eq", "refuted")],
                  note="Answered 13 Oct: no. 0.384 on formula (oracle depth 0.615)."),
    "CAP-04": dict(status="todo", blocked_by=None, note="Unblocked 13 Oct by AUD-48: orient-only tiers lift GES 0.528 -> 0.546 (exploratory); wrong tiers cost 0.19, bounded."),
    "BLD-04": dict(status="todo", blocked_by=None, note="Unblocked 13 Oct by AUD-48 (model tiers measured)."),
    "TGT-07": dict(status="todo", blocked_by=None, note="Unblocked 13 Oct by AUD-48."),
    "AUD-37": dict(note="Live 13 Oct: causaliq ok (1 call, $0.004, F1 0.231); Causal-Copilot on gpt-4o-mini crashed at judge_functions.py:562 "
                        "(the upstream key bug that also killed 15 of 114 gpt-4o runs). Remaining: PyWhy-LLM, MATMCD, Vashishtha.",
                   evidence=["harness/agent_probe.py", "harness/probe_llm.py", "harness/probe_io.py", "harness/agents/registry.json",
                             "docker/Dockerfile.probes", "plans/ab05_probe_causaliq.json", "plans/ab05_probe_pywhyllm.json",
                             "plans/ab05_probe_matmcd.json", "plans/ab05_probe_vashishtha.json", "plans/ab05_cc_gpt4omini.json",
                             "analysis/reports/ab05_probe_prep.md", "analysis/reports/ab05_probe_results.md", "tests/test_agent_probe.py"],
                   blocked_by="Uzair: three remaining live probes"),
    "AUD-38": dict(status="blocked", blocked_by="Uzair: live batch (plans/ab06, estimate about $58) and the Causal-Copilot arm (about $1)",
                   evidence=["plans/make_ab06_plans.py", "plans/ab06/BUDGET.json", "harness/agent_batch.py", "analysis/ab06_score.py",
                             "plans/ab06_cc_gpt4omini_s2.json"],
                   checks=[J("plans/ab06/BUDGET.json", ["total", "runs"], "eq", 120)],
                   note="Plans, batch runner (resumable, total cap) and scorer ready; the full grid ran end to end with the stub model."),
    "DEC-05": dict(note="Bundle AB-16: decide once the evidence is in (no date pressure)."),
    "AUD-47": dict(note="Bundle AB-17: after AB-16."),
}
for _i in ITEMS:
    if _i["id"] in _P04:
        _i.update(_P04[_i["id"]])
BUNDLE_STATUS.update({"AB-07": "done", "AB-06": "blocked"})
BUNDLE_NOTE.update({"AB-07": "Model orders 69% of true edges from names (12% contradicted); follows moved labels; tiers alone 0.448.",
                    "AB-05": "causaliq live ok; Causal-Copilot gpt-4o-mini hit the upstream key crash; 3 probes to run.",
                    "AB-06": "120-run agent grid and the Causal-Copilot arm are ready; waits on your live runs.",
                    "AB-16": "Decide once the evidence is in.", "AB-17": "After AB-16."})

# ---- overrides p05 (2026-10-13): AB-02 Bayesys measured; AB-06 batch safety and tests
_P05 = {
    "AUD-34": dict(status="blocked", blocked_by="Uzair: results_noisyPaper.xlsx into external/bayesys (reproduction gate)",
                   evidence=["analysis/reports/ab02_second_scoreboard.md", "analysis/ab02_alarm_order.py", "analysis/results/ab02/alarm_order.json",
                             "analysis/audits/AB02_AB12_data_scouting.md", "analysis/ab02_bayesys.py", "analysis/results/ab02/bayesys.json",
                             "analysis/results/ab02/bayesys_runs.jsonl"],
                   checks=[J("analysis/results/ab02/bayesys.json", ["P3", "verdict"], "eq", "supported"),
                           G("analysis/reports/ab02_second_scoreboard.md", r"reproduction gate")],
                   note="Bayesys measured 13 Oct (6 networks, released vs 5 shuffled orders, PC/maxP/FCI/GES): ASIA, SPORTS, PATHFINDER "
                        "are released in topological order (P3 supported); an index tie-break gains +0.04 to +0.30 there and about 0 on "
                        "ALARM/PROPERTY. P4 inconclusive (conflict-rule gap on 2 of 3 ordered networks). No claim on the published "
                        "numbers until two cells are reproduced. Sortability not computed (discrete data)."),
    "AUD-38": dict(evidence=["plans/make_ab06_plans.py", "plans/ab06/BUDGET.json", "harness/agent_batch.py", "analysis/ab06_score.py",
                             "plans/ab06_cc_gpt4omini_s2.json", "analysis/reports/ab06_prep.md", "tests/test_ab06_batch.py"],
                   note="Plans, batch runner and scorer ready and stub-tested end to end. The batch never pays twice for a crashed run "
                        "(--retry-failed to override), counts every logged attempt, and stops at the total cap before a run (exit 3)."),
}
for _i in ITEMS:
    if _i["id"] in _P05:
        _i.update(_P05[_i["id"]])
BUNDLE_NOTE.update({"AB-02": "Bayesys: 3 of 6 networks in topological column order (P3 supported); index tie-break worth up to +0.30 there. "
                             "P4 mixed. Reproduction waits on the published xlsx."})

# ---- overrides p06 (2026-10-13): AB-14 market research done without waiting on interviews (Uzair's decision)
_P06 = {
    "AUD-45": dict(status="done", blocked_by=None,
                   criterion="Must show: market map; three one-page vertical briefs; H1-H3 public evidence, labelled indirect. Gate: no number without its inputs",
                   evidence=["analysis/reports/ab14_market.md", "analysis/audits/ab14_notes/market_map.md",
                             "analysis/audits/ab14_notes/it_incident_rca.md", "analysis/audits/ab14_notes/marketing_measurement.md",
                             "analysis/audits/ab14_notes/pharma_rwe.md", "analysis/audits/ab14_notes/demand_signals.md",
                             "docs/decisions/2026-10-13_interviews_not_gating.md"],
                   checks=[G("analysis/reports/ab14_market.md", r"Brief 1: IT incident RCA"), G("analysis/reports/ab14_market.md", r"Brief 2: marketing"),
                           G("analysis/reports/ab14_market.md", r"Brief 3: pharma RWE"), G("analysis/reports/ab14_market.md", r"The public evidence on H1-H3 is indirect"),
                           J("plans/audit_dag.json", ["version"], "eq", 2)],
                   note="Done 13 Oct without interviews (Uzair's decision). Start in IT incident RCA as a vendor-neutral audit of AI SRE agents' "
                        "root-cause claims; marketing a close second; pharma third. Obtainable (estimates): RCA $1.8-9M ARR in ~3 yrs; marketing "
                        "$3-67.5M at maturity; pharma core $2.8-11M/yr. 'Causal AI' sizings span $28.9M-$59.2B. H2 best supported; H1 for "
                        "provenance, not abstention; H3 by analogy only."),
    "AUD-41": dict(note="Interview kit ready; interviews run whenever a chance arises. No longer gates AB-14 or AB-16 (decision 2026-10-13); "
                        "P13 can only be decided by interviews."),
    "DEC-05": dict(note="Bundle AB-16: decide once the evidence is in. C1 from AB-14's public evidence (indirect) plus interviews if any."),
    "STR-06": dict(note="AB-14 (13 Oct): sell a vendor-neutral audit of other agents' causal claims, not a causal-AI platform; start in IT incident RCA.",
                   evidence=["analysis/reports/ab14_market.md"]),
}
for _i in ITEMS:
    if _i["id"] in _P06:
        _i.update(_P06[_i["id"]])
BUNDLE_STATUS.update({"AB-14": "done"})
BUNDLE_NOTE.update({"AB-14": "Market map + 3 briefs: start in IT incident RCA (audit AI SRE agents' claims); marketing second; pharma third.",
                    "AB-10": "Kit ready; interviews whenever a chance arises; no longer gates AB-14 or AB-16."})

# ---- additions p07 (2026-10-13): Atlas v2, a guided sequence of pages (design awaiting approval)
ITEMS.append(item("TEAM-08", "TEAM", "Atlas v2: the site as a guided sequence of pages (four acts, thirteen pages)", "blocked", kind="task",
    criterion="Must show (per bundle S1-S5 in the design): pages build; 0 missing numbers; 0 broken links; 0 term-order violations; "
              "no horizontal scroll at 390 px; 'pages to re-read' list works; recentering path Home -> changes -> status",
    evidence=["analysis/reports/site_flow_design.md", "site/build.py", "site/levels/bundles.py", "site/levels/theses.py"],
    checks=[G("analysis/reports/site_flow_design.md", r"Failure modes named in advance"), G("site/build.py", r"max-width: 640px")],
    blocked_by="DEC-06",
    note="Design written 13 Oct. Readability pass done the same day on the current site: dates out of headings, stale DEC-02/A3 text "
         "fixed, audit board follows DAG v2, clipped notes fixed, no phone overflow. Build waits on DEC-06."))
ITEMS.append(item("DEC-06", "DEC", "Approve the Atlas v2 page sequence (and whether the market page is public)", "open", kind="decision",
    criterion="Uzair's decision recorded with what it approves",
    evidence=["analysis/reports/site_flow_design.md"],
    note="Three choices in the design: the 4-act / 13-page sequence; market page public or repo-only; Home leads with research."))
# ---- overrides p08 (2026-10-13): AUD-45 title follows DAG v2
for _i in ITEMS:
    if _i["id"] == "AUD-45":
        _i["title"] = "AB-14 Market map and three vertical briefs (RCA, marketing, pharma RWE), with public demand evidence"

# ---- overrides p09 (2026-10-13): Atlas v2 approved; reliability first; Bayesys reproduced
_P09 = {
    "DEC-06": dict(status="done", evidence=["analysis/reports/site_flow_design.md", "docs/decisions/2026-10-13_atlas_v2_approved.md"],
                   checks=[G("docs/decisions/2026-10-13_atlas_v2_approved.md", r"I also approve of the site structure")],
                   note="Approved 13 Oct: 4 acts / 13 pages on the existing GitHub Pages site; Home leads with the research and links the "
                        "market/wedge; market page public."),
    "TEAM-08": dict(status="in_progress", blocked_by=None,
                    note="Approved 13 Oct (DEC-06). Built on the existing Pages site in bundles S1-S5."),
    "DEC-05": dict(note="Bundle AB-16: decide once the evidence is in. Uzair, 13 Oct: auditing is the more valuable product, but reliability "
                        "comes first (ledger invariants, never below data-only, bounded harm, held-out calibration) before any product "
                        "surface. C1 from AB-14 (indirect) plus interviews if any."),
    "AUD-34": dict(status="done", blocked_by=None,
                   evidence=["analysis/reports/ab02_second_scoreboard.md", "analysis/ab02_alarm_order.py", "analysis/results/ab02/alarm_order.json",
                             "analysis/audits/AB02_AB12_data_scouting.md", "analysis/ab02_bayesys.py", "analysis/results/ab02/bayesys.json",
                             "analysis/results/ab02/bayesys_runs.jsonl", "analysis/ab02_bayesys_repro.py",
                             "analysis/results/ab02/bayesys_repro.json", "analysis/results/ab02/bayesys_repro_runs.jsonl"],
                   checks=[J("analysis/results/ab02/bayesys.json", ["P3", "verdict"], "eq", "supported"),
                           J("analysis/results/ab02/bayesys_repro.json", ["gate_by_alpha", "0.05", "cells_reproduced"], "ge", 2),
                           G("analysis/reports/ab02_second_scoreboard.md", r"Gate: passed at alpha 0.05")],
                   note="Bayesys reproduced (16 of 31 PC-Stable/FCI cells at alpha 0.05; PC 10 of 15). P3 supported (3 of 6 networks in "
                        "topological order); P4 inconclusive. Bayesys's half-credit F1 moves at most 0.03 when columns are shuffled, so "
                        "the layout leak needs an index tie-break (CausalArena's forced choice) to pay. Engine channel: causal-learn GES "
                        "on PROPERTY -0.07 to -0.09 on the released order. gCastle not reproduced, no claim."),
    "EXT-01": dict(note="Backed by two benchmarks (AB-01, AB-02): shuffle released columns, or score with a tie-break-invariant rule."),
}
for _i in ITEMS:
    if _i["id"] in _P09:
        _i.update(_P09[_i["id"]])
BUNDLE_STATUS.update({"AB-02": "done"})
BUNDLE_NOTE.update({"AB-02": "Bayesys reproduced (PC 10/15 cells). Layout in 3 of 6 networks, but Bayesys's half-credit score moves <= 0.03 "
                             "when shuffled; CausalArena's forced choice is what rewards the leak."})

# ---- overrides p10 (2026-10-13): Atlas v2 built
_P10 = {
    "TEAM-08": dict(status="done", blocked_by=None,
                    evidence=["analysis/reports/site_flow_design.md", "site/build.py", "site/pages.py", "site/terms.py", "site/pagekit.py",
                              "site/registry.py", "site/pgs/pg_home.py", "site/pgs/pg_primer.py", "site/pgs/pg_scoring.py",
                              "site/pgs/pg_space.py", "site/pgs/pg_scoreboard.py", "site/pgs/pg_decisions.py", "site/pgs/pg_names.py",
                              "site/pgs/pg_rca.py", "site/pgs/pg_theses.py", "site/pgs/pg_market.py", "site/pgs/pg_status.py",
                              "site/pgs/pg_changes.py", "site/pgs/pg_glossary.py", "site/pgs/pg_evidence.py", "site/pgs/pg_about.py",
                              "tracker/snapshot.py"],
                    checks=[G("site/pages.py", r"SEQUENCE = "), G("site/build.py", r"is taught later, on"),
                            G("analysis/reports/site_flow_design.md", r"## Built \(2026-10-13\)")],
                    reproduce="python tracker/snapshot.py && python site/build.py",
                    note="Built 13 Oct on the existing Pages site: Home + 11 pages in four acts + glossary, evidence index, about. The build "
                         "fails on missing numbers, term-order violations, early results, broken links and unlabelled market $ figures. "
                         "Phone overflow (390 px, 15 pages) checked by hand with Playwright; not yet in CI."),
}
for _i in ITEMS:
    if _i["id"] in _P10:
        _i.update(_P10[_i["id"]])

# ---- additions p11 (2026-10-14): audit close-out
ITEMS.append(item("EXT-06", "EXT", "Note to Vashishtha et al. maintainers: triplet answers cut off at 300 tokens (91% of votes lost on gpt-4o-mini)", "open", kind="decision",
    criterion="Uzair decides whether to send; draft states the measurement (2,096 of 2,300 answers without <Answer>, 113 of 300 pairs to the tie-breaker) and the one-line cause",
    evidence=["analysis/reports/ab05_probe_results.md", "analysis/ab05_live_calibration.py", "analysis/results/ab05/live_calibration.json"],
    checks=[J("analysis/results/ab05/live_calibration.json", ["agents", "vashishtha", "vashishtha", "share_without_tag"], "ge", 0.9)],
    note="Found 14 Oct in the AB-05 live probe: strategies/triplet.py asks for reasoning before the tagged answer with max_completion_tokens=300; "
         "the README's gpt-4o-mini stops at the limit in 2,105 of 2,300 calls. Silent degradation (a printed warning per triplet)."))
ITEMS.append(item("INF-08", "INF", "Transient OSError EIO on the Docker bind mount: harness writes retry", "done", kind="task",
    criterion="Every harness write of a run summary, result or call log retries EIO; a unit test injects EIO; the lost run is re-planned",
    evidence=["harness/cc_common.py", "harness/probe_llm.py", "harness/agent_probe.py", "tests/test_probe_gate.py",
              "plans/ab06_cc_gpt4omini_s2_q042.json", "analysis/reports/ab06_cc_second_model.md"],
    checks=[G("harness/cc_common.py", r"transient OSError EIO"), G("tests/test_probe_gate.py", r"test_eio_on_calls_log_is_retried")],
    note="14 Oct 00:19-00:25 UTC: two AB-06 Causal-Copilot runs hit Errno 5 (q041 lost only its summary and is scored from state; q042 lost the run). "
         "Cause not identified (Windows file locking by sync or antivirus is the usual one). Causal-Copilot's own writes cannot be protected without changing it."))

# ---- overrides p11 (2026-10-14): audit close-out
_P11 = {
    "AUD-37": dict(status="done", blocked_by=None,
                   evidence=["harness/agent_probe.py", "harness/probe_llm.py", "harness/probe_io.py", "harness/agents/registry.json",
                             "docker/Dockerfile.probes", "plans/ab05_probe_causaliq.json", "plans/ab05_probe_pywhyllm.json",
                             "plans/ab05_probe_matmcd.json", "plans/ab05_probe_vashishtha.json", "plans/ab05_cc_gpt4omini.json",
                             "analysis/reports/ab05_probe_prep.md", "analysis/reports/ab05_probe_results.md", "tests/test_agent_probe.py",
                             "analysis/ab05_live_calibration.py", "analysis/results/ab05/live_calibration.json"],
                   checks=[G("analysis/reports/ab05_probe_results.md", r"P8 .* is \*\*supported\*\*"),
                           J("analysis/results/ab05/live_calibration.json", ["agents", "pywhyllm", "status"], "eq", "ok"),
                           J("analysis/results/ab05/live_calibration.json", ["agents", "causaliq", "status"], "eq", "ok")],
                   note="P8 supported 14 Oct: causaliq, PyWhy-LLM (F1 0.329, $1.43) and Causal-Copilot on gpt-4o-mini ran end to end; MATMCD and "
                        "Vashishtha stopped on our stub-based caps, not agent failures (resume about $0.66, caps raised). Live answers longer than "
                        "the stub assumed (MATMCD x1.8, PyWhy-LLM x1.2); Vashishtha loses 91% of triplet votes to its 300-token limit (EXT-06). "
                        "Spent $3.13 of $5."),
    "AUD-38": dict(status="blocked",
                   evidence=["plans/make_ab06_plans.py", "plans/calibrate_ab06.py", "plans/ab06/BUDGET.json", "plans/ab06/TIERS.json",
                             "plans/ab06_prereg.json", "manifests/evidence/ab06_prereg_2026-10-14.sha256", "harness/agent_batch.py",
                             "analysis/ab06_score.py", "plans/ab06_cc_gpt4omini_s2.json", "plans/ab06_cc_gpt4omini_s2_q042.json",
                             "analysis/reports/ab06_prep.md", "analysis/reports/ab06_cc_second_model.md",
                             "analysis/results/ab06_cc/s2_verdicts.json", "analysis/results/ab06_cc/partial_stages.json",
                             "tests/test_ab06_batch.py", "tests/test_probe_gate.py"],
                   checks=[{"t": "manifest", "path": "manifests/evidence/ab06_prereg_2026-10-14.sha256"},
                           J("plans/ab06/BUDGET.json", ["total", "runs"], "eq", 120),
                           J("analysis/results/ab06_cc/s2_verdicts.json", ["M4", "verdict"], "eq", "SUPPORTED")],
                   blocked_by="Uzair: AB-06 tier A live batch (90 runs, about $52, workers=4) and the q042 rerun (about $0.03)",
                   note="Causal-Copilot part scored 14 Oct (gpt-4o-mini): name reliance 0.094 (gpt-4o 0.167); M2 refuted, M3 inconclusive (0.71), "
                        "M4 supported (8 of 9). Agent grid re-planned from live numbers: full grid $92 / 100 h sequential, so tier A (90 runs, $52) "
                        "answers P9/P10; batch v2 runs in parallel with reserved caps. Pre-registration hashed before any live grid call."),
    "RQ-17": dict(status="in_progress", evidence=["analysis/reports/ab06_cc_second_model.md", "analysis/results/ab06_cc/s2_verdicts.json"],
                  note="Causal-Copilot on gpt-4o-mini: structure holds (M4 supported, M2 refuted on both models, bootstrap loss identical), name "
                       "reliance smaller (0.094 vs 0.167); the model review lowers directed F1 even with real names (0.233 -> 0.208)."),
    "BND-12": dict(note="Second-model part done through AB-06's Causal-Copilot arm (gpt-4o-mini, 30 runs, ab06_cc_second_model.md). REP-11's "
                        "data-only Sachs numbers reproduced within 0.05. Remaining live parts (CARE control, LLM and fused Sachs numbers) wait on DEC-05."),
    "EXT-03": dict(note="Evidence grows: 18 of 19 live entries into the cycle step crashed at judge_functions.py:562 (15 gpt-4o, 3 of 4 gpt-4o-mini; "
                        "the one survivor returned both 'nodes' and 'removed_edge')."),
    "DEC-05": dict(status="open", evidence=["analysis/reports/ab16_wedge_decision.md", "analysis/reports/approach_v1.md"],
                   checks=[G("analysis/reports/ab16_wedge_decision.md", r"## 5\. What Uzair decides"),
                           G("analysis/reports/approach_v1.md", r"## 3\. Binding times")],
                   blocked_by="Uzair: decide (ab16_wedge_decision.md section 5)",
                   note="Decision pack ready 14 Oct. L5 met; L1 and L3 partly met (scoped); L2 open (AB-06 tier A); L4 not met (no engine); "
                        "C2 met on PetShop; C1 indirect; C3 desk. Recommended: B, measurement + reliability-first claim ledger (B0-B5 in "
                        "approach_v1.md), with A (measurement only) as the floor. AB-06's outcomes change only the motivation (fixed in advance)."),
    "CAP-10": dict(note="Schema-validated replies, one retry, then abstain; built and unit-tested (parse rule shared with refinement_v2). Widened "
                        "14 Oct in approach_v1.md (G7): truncation and empty answers count as failures and are ledger fields, after the "
                        "Vashishtha finding. Closes on BND-11's live names run."),
    "STR-01": dict(evidence=["analysis/reports/ab06_prep.md", "analysis/reports/ab05_probe_results.md"],
                   note="AB-05 probes done (4 agents + Causal-Copilot on two models); AB-06 tier A pre-registered."),
    "RQ-05": dict(evidence=["analysis/reports/program_v2.md", "analysis/reports/bnd08_s2_results.md", "analysis/reports/ab06_cc_second_model.md"]),
}
for _i in ITEMS:
    if _i["id"] in _P11:
        _i.update(_P11[_i["id"]])
BUNDLE_STATUS.update({"AB-05": "done"})
BUNDLE_NOTE.update({"AB-05": "P8 supported: causaliq, PyWhy-LLM and Causal-Copilot (gpt-4o-mini) end to end; MATMCD and Vashishtha stopped on "
                             "stub-based caps (resume ~$0.66). Vashishtha loses 91% of votes to its own token limit.",
                    "AB-06": "Causal-Copilot arm scored (gpt-4o-mini 0.094 vs gpt-4o 0.167). Grid re-planned from live numbers; tier A "
                             "(90 runs, ~$52) pre-registered; waits on Uzair.",
                    "AB-16": "Decision pack ready (ab16_wedge_decision.md); recommends B with A as floor; waits on Uzair."})

# ---- overrides p12 (2026-10-14): BLD-01 tools manifest re-issued (cc_common EIO retry, INF-08)
for _i in ITEMS:
    if _i["id"] == "BLD-01":
        _i["evidence"] = ["manifests/evidence/BLD-01_tools_2026-10-14.sha256" if e == "manifests/evidence/BLD-01_tools_2026-10-12.sha256" else e
                          for e in _i["evidence"]]
        _i["checks"] = [dict(ck, path="manifests/evidence/BLD-01_tools_2026-10-14.sha256")
                        if ck.get("t") == "manifest" and ck.get("path") == "manifests/evidence/BLD-01_tools_2026-10-12.sha256" else ck
                        for ck in _i["checks"]]
        _i["note"] = ((_i.get("note") or "") + " Tools manifest re-issued 2026-10-14 (harness/cc_common.py: EIO write retry, INF-08); "
                      "the 2026-10-12 manifest stays as the record of the earlier state.").strip()

# ---- overrides p13 (2026-10-14): runs of 14 Oct ingested; AB-06 amendment 1
_P13 = {
    "AUD-37": dict(note="P8 supported, all five systems end to end: causaliq, PyWhy-LLM (F1 0.329), Causal-Copilot on gpt-4o-mini, and "
                        "MATMCD and Vashishtha after resuming on 14 Oct (replayed paid answers; +$0.009 and +$0.651). On the probe scenario "
                        "both hybrids end exactly at their own data-only PC graph (F1 0.407). Vashishtha loses 91% of triplet votes to its "
                        "300-token limit (EXT-06). Spent $3.79 of $5."),
    "AUD-38": dict(evidence=["plans/make_ab06_plans.py", "plans/calibrate_ab06.py", "plans/ab06/BUDGET.json", "plans/ab06/TIERS.json",
                             "plans/ab06_prereg.json", "manifests/evidence/ab06_prereg_2026-10-14.sha256", "plans/ab06_prereg_amendment_1.json",
                             "manifests/evidence/ab06_prereg_amendment1_2026-10-14.sha256", "harness/agent_batch.py", "analysis/ab06_score.py",
                             "plans/ab06_cc_gpt4omini_s2.json", "plans/ab06_cc_gpt4omini_s2_q042.json", "analysis/reports/ab06_prep.md",
                             "analysis/reports/ab06_cc_second_model.md", "analysis/results/ab06_cc/s2_verdicts.json",
                             "analysis/results/ab06_cc/partial_stages.json", "tests/test_ab06_batch.py", "tests/test_probe_gate.py"],
                   checks=[{"t": "manifest", "path": "manifests/evidence/ab06_prereg_amendment1_2026-10-14.sha256"},
                           J("plans/ab06/BUDGET.json", ["total", "runs"], "eq", 120),
                           J("plans/ab06/TIERS.json", ["cost", "A", "runs"], "eq", 80),
                           J("analysis/results/ab06_cc/s2_verdicts.json", ["M4", "verdict"], "eq", "SUPPORTED")],
                   blocked_by="Uzair: resume AB-06 tier A (80 runs, about $48 in all, $7.92 spent; workers=4)",
                   note="Causal-Copilot part complete (q042 rerun 14 Oct): gpt-4o-mini name reliance 0.094 (gpt-4o 0.167), M2 refuted 4/10, M3 "
                        "inconclusive, M4 supported 9/10. Tier A started 14 Oct; a machine restart stopped it after 14 attempts (12 ok, 2 "
                        "Vashishtha cap hits; 4 runs cut short). Amendment 1: Vashishtha ties 85-93% of pairs on 17 variables (each a gpt-4o "
                        "call), so its tier-A runs are cut to the first five scenarios (tier A 80 runs, $48); cap hits resume without a flag; "
                        "spend is read from the call logs. P9/P10 and the scorer unchanged."),
    "RQ-17": dict(status="done", note="Causal-Copilot on gpt-4o-mini (10 families x 3 arms): the structure holds (M4 supported 9/10, M2 refuted on "
                                      "both models, the same bootstrap loss); name reliance is smaller (0.094 vs 0.167), and the model review lowers "
                                      "directed F1 even with real names (0.233 -> 0.208)."),
    "BND-11": dict(status="done",
                   evidence=["analysis/refinement_v2.py", "analysis/results/refinement_v2/RULE.json", "analysis/results/refinement_v2/dev.json",
                             "analysis/results/refinement_v2/test_formula.json", "analysis/results/refinement_v2/names_s2.json",
                             "analysis/results/refinement_v2/access_log.jsonl", "plans/bnd11_names_requests.jsonl",
                             "plans/results/bnd11_names_requests.answers.jsonl", "harness/names_runner.py", "analysis/bnd11_lenient_parse.py",
                             "analysis/results/refinement_v2/names_s2_exploratory_lenient.json", "analysis/reports/bnd11_prep.md",
                             "analysis/reports/bnd11_results.md", "manifests/evidence/bnd11_prereg_2026-10-12.sha256"],
                   checks=[{"t": "manifest", "path": "manifests/evidence/bnd11_prereg_2026-10-12.sha256"},
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "R1", "verdict"], "eq", "SUPPORTED"),
                           J("analysis/results/refinement_v2/names_s2.json", ["R4", "verdict"], "eq", "SUPPORTED"),
                           J("analysis/results/refinement_v2/names_s2.json", ["R6", "verdict"], "eq", "REFUTED")],
                   note="14 Oct. Data part v2d on the held-out formula test replay: R1 22/22, R2 22/22, R3 +0.010, all supported. Names only "
                        "where the data are silent: R4 (neutral adds nothing) and R5 (swapped harmless) supported; R6 (real names help in "
                        ">= 8/10) refuted, 1/10. gpt-4o fenced 1,036 of 1,571 replies, so the strict contract abstained on 251 of 786 "
                        "questions; an exploratory lenient re-read gives R6 5/10, still refuted. $0.47."),
    "BLD-06": dict(status="done",
                   evidence=["analysis/refinement_v1.py", "analysis/refinement_v2.py", "analysis/results/refinement_v2/RULE.json",
                             "analysis/results/refinement_v2/dev.json", "analysis/results/refinement_v2/test_formula.json",
                             "analysis/results/refinement_v2/names_s2.json", "analysis/reports/bnd11_prep.md", "analysis/reports/bnd11_results.md"],
                   checks=[J("analysis/results/refinement_v2/dev.json", ["summary", "all_edges_sourced"], "true"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "all_edges_sourced"], "true"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "R2", "verdict"], "eq", "SUPPORTED")],
                   note="v2 is the drop-in replacement: it never falls below the algorithm on held-out data (formula test 22/22) and "
                        "sources every edge; names add little (R6 refuted) and wrong names cost nothing measurable (R5)."),
    "CAP-10": dict(status="done", evidence=["harness/names_runner.py", "analysis/refinement_v2.py", "tests/test_refinement_v2.py",
                                            "analysis/reports/bnd11_prep.md", "analysis/reports/bnd11_results.md",
                                            "plans/results/bnd11_names_requests.answers.jsonl"],
                   note="0 crashes in 1,571 live calls (BND-11): every malformed reply was retried once or abstained. Lesson for approach v1 "
                        "G7: the strict contract turned gpt-4o's code fences into 251 abstentions; a contract must declare its accepted "
                        "normalisations and count them."),
    "TGT-13": dict(status="done", evidence=["harness/names_runner.py", "tests/test_refinement_v2.py", "analysis/reports/bnd11_results.md",
                                            "plans/results/bnd11_names_requests.answers.jsonl"],
                   note="Zero crashes over the BND-11 live run (786 questions, 1,571 calls)."),
    "TGT-09": dict(note="v1 inconclusive (BND-10). v2's data part meets the rule on the held-out formula test replay: adjacency F1 >= the "
                        "algorithm's - 0.02 in 22 of 22 files (bnd11_results.md)."),
}
for _i in ITEMS:
    if _i["id"] in _P13:
        _i.update(_P13[_i["id"]])
BUNDLE_NOTE.update({"AB-05": "P8 supported: all five systems end to end (MATMCD and Vashishtha after resuming). Vashishtha loses 91% of its "
                             "votes to its own token limit.",
                    "AB-06": "Causal-Copilot arm complete (gpt-4o-mini 0.094 vs gpt-4o 0.167; M4 9/10). Tier A amended to 80 runs (~$48), "
                             "14 attempted before a restart; resumes from the call logs."})

# ---- overrides p14 (2026-10-14): DLV-04 and TGT-09 met by refinement v2
_P14 = {
    "TGT-09": dict(status="done",
                   evidence=["analysis/results/refinement_v1/test_replay.json", "analysis/results/refinement_v1/test_live_s2.json",
                             "analysis/results/refinement_v1/access_log.jsonl", "analysis/reports/bnd09_bnd10_refinement.md",
                             "analysis/results/refinement_v2/test_formula.json", "analysis/results/refinement_v2/access_log.jsonl",
                             "analysis/reports/bnd11_results.md"],
                   checks=[J("analysis/results/refinement_v1/test_live_s2.json", ["pooled_test", "R1", "verdict"], "eq", "INCONCLUSIVE"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "R1", "verdict"], "eq", "SUPPORTED"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "R1", "share"], "ge", 0.9)],
                   note="Met by refinement v2, the frozen successor of v1 (its data part keeps every algorithm adjacency): adjacency F1 >= "
                        "the algorithm's - 0.02 in 22 of 22 held-out formula files (and 30 of 30 live S2 tables, exploratory: read in "
                        "BND-10). v1 itself stays inconclusive (BND-10). The criterion's 'v1' is the means named on 9 Oct; the target is "
                        "the property."),
    "DLV-04": dict(status="done",
                   evidence=["analysis/refinement_v2.py", "analysis/results/refinement_v2/RULE.json", "analysis/results/refinement_v2/test_formula.json",
                             "analysis/results/refinement_v2/exploratory_s2_live.json", "analysis/results/refinement_v2/names_s2.json",
                             "plans/results/bnd11_names_requests.answers.jsonl", "analysis/reports/bnd11_results.md"],
                   checks=[J("analysis/results/refinement_v2/test_formula.json", ["summary", "R1", "verdict"], "eq", "SUPPORTED"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "all_edges_sourced"], "true"),
                           J("analysis/results/refinement_v2/names_s2.json", ["R5", "verdict"], "eq", "SUPPORTED")],
                   note="Refinement v2 (BND-11), frozen 12 Oct, evaluated 14 Oct: adjacency F1 not below the algorithm's (within 0.02) in "
                        "22 of 22 held-out formula files; 0 crashes in 1,571 live model calls; every edge labelled with its source "
                        "(data / names). Under the same controls as BND-08 (columns shuffled, three name arms)."),
}
for _i in ITEMS:
    if _i["id"] in _P14:
        _i.update(_P14[_i["id"]])

# ---- additions p15 (2026-10-14)
ITEMS.append(item("INF-09", "INF", "Provider quota exhaustion is an infrastructure stop, not an agent failure", "done", kind="task",
    criterion="A billing refusal (HTTP 429 insufficient_quota) stops the run as aborted_quota, resumable; the batch stops launching; unit tests",
    evidence=["harness/probe_llm.py", "harness/agent_probe.py", "harness/agent_batch.py", "tests/test_probe_gate.py", "tests/test_ab06_batch.py",
              "plans/ab06_prereg_amendment_2.json"],
    checks=[G("harness/probe_llm.py", r"class QuotaExhausted"), G("tests/test_ab06_batch.py", r"test_quota_stop_ends_launching")],
    note="14 Oct: the OpenAI account ran out of credits mid-batch; 61 AB-06 runs failed in seconds and were recorded as agent failures while "
         "the batch kept launching. Fixed as a class: the gate raises QuotaExhausted (BaseException, so agent retry loops cannot swallow "
         "it), runs end 'aborted_quota' (exit 5), earlier quota 'failed' runs are recognised by message, and the batch stops launching."))

# ---- overrides p15 (2026-10-14)
for _i in ITEMS:
    if _i["id"] == "AUD-38":
        _i["evidence"] = [e for e in _i["evidence"]] + ["plans/ab06_prereg_amendment_2.json", "manifests/evidence/ab06_prereg_amendment2_2026-10-14.sha256"]
        _i["checks"] = [dict(ck, path="manifests/evidence/ab06_prereg_amendment2_2026-10-14.sha256")
                        if ck.get("t") == "manifest" else ck for ck in _i["checks"]]
        _i["blocked_by"] = "Uzair: add OpenAI credits, then resume AB-06 tier A (61 runs left, about $33 more; $12.21 spent)"
        _i["note"] = ("Causal-Copilot part complete (gpt-4o-mini 0.094 vs gpt-4o 0.167; M4 9/10). Tier A (80 runs after amendment 1): 19 ok; "
                      "61 refused by the provider for lack of credits on 14 Oct, recorded as failures; amendment 2 makes such stops "
                      "resumable and halts the batch on the first one. P9/P10, scorer, tiers unchanged.")

# ---- overrides p16 (2026-10-14): the audit chapter closes
_WD = "docs/decisions/2026-10-14_wedge_decision.md"
_CO = "docs/decisions/2026-10-14_audit_closeout.md"
_AB06 = "analysis/results/ab06/ab06.json"
_P16 = {
    "AUD-38": dict(status="done", blocked_by=None,
                   evidence=None,  # extended below
                   checks=[{"t": "manifest", "path": "manifests/evidence/ab06_prereg_amendment3_2026-10-14.sha256"},
                           J(_AB06, ["P9", "verdict"], "eq", "supported"),
                           J(_AB06, ["P10", "verdict"], "eq", "supported"),
                           J("plans/ab06/TIERS.json", ["cost", "A", "runs"], "eq", 80),
                           J("analysis/results/ab06_cc/s2_verdicts.json", ["M4", "verdict"], "eq", "SUPPORTED")],
                   note="Tier A scored 14 Oct (80 runs, 79 ok; $32.11 for the grid, $48.23 with the earlier quota-stopped attempt). "
                        "P9 SUPPORTED: Causal-Copilot (gpt-4o), causaliq and MATMCD lose >= 0.10 directed F1 when names are swapped "
                        "(PyWhy-LLM not entered: 4 paired scenarios < 5). P10 SUPPORTED: MATMCD scores below its own data-only graph "
                        "with neutral or swapped names. Vashishtha is the exception (name reliance 0.020): 89 of 100 directions come "
                        "from data. One PyWhy-LLM run crashed inside the guidance library (negative time-to-first-token); counted as "
                        "an agent failure, not retried (amendment 3). Tier B not run (DEC-05)."),
    "DEC-05": dict(status="done", blocked_by=None,
                   evidence=["analysis/reports/ab16_wedge_decision.md", "analysis/reports/approach_v1.md", _WD,
                             "analysis/reports/ab06_field_audit.md"],
                   checks=[G(_WD, r"B: measurement \+ a reliability-first claim ledger"),
                           G("analysis/reports/ab16_wedge_decision.md", r"## Decision \(14 Oct\)"),
                           G("analysis/reports/approach_v1.md", r"## 3\. Binding times")],
                   note="Decided 14 Oct (Uzair delegated it with AB-06's results in hand): B, measurement plus a reliability-first "
                        "claim ledger, with A (measurement only) as the floor. Venue class: methods with a benchmark contribution. "
                        "B0 and B1 start now; AB-06 tier B not run."),
    "DEC-01": dict(status="done", blocked_by=None, criterion="Program v2 adopted, redirected or enlarged; E1-E5 scoped",
                   evidence=[_WD, "analysis/reports/audit_closeout.md"],
                   checks=[G(_WD, r"DEC-01")],
                   note="Adopted as amended 14 Oct: E1 done in a scoped form (STR-01); E2-E5 deferred behind the Q2 build gates."),
    "AUD-47": dict(status="done", blocked_by=None,
                   evidence=["docs/paper/skeleton.md", "plans/q2_build_prereg.json", "manifests/evidence/paper_prereg_2026-10-14.sha256"],
                   checks=[{"t": "manifest", "path": "manifests/evidence/paper_prereg_2026-10-14.sha256"},
                           G("docs/paper/skeleton.md", r"## Held-out discipline"),
                           G("plans/q2_build_prereg.json", r"AUD-47 \(AB-17\)")],
                   note="Skeleton (claims C1-C10, sections, figures, venue) and the Q2 build pre-registration (gates B0.1-B5.2 with "
                        "thresholds, splits, controls, order) hashed 14 Oct, before any held-out run of the build."),
    "STR-01": dict(status="done", blocked_by=None, criterion="E1 in scoped form: AB-05 probes and AB-06 tier A under name and layout controls",
                   evidence=["analysis/reports/ab06_field_audit.md", _AB06, "analysis/reports/ab06_cc_second_model.md"],
                   checks=[J(_AB06, ["P9", "verdict"], "eq", "supported")],
                   note="Done in scoped form: five systems (four agents and Causal-Copilot on two models), tier A only. Tier B and "
                        "further systems are not part of the audit chapter."),
    "RQ-05": dict(status="done", blocked_by=None, criterion="P9 verdict from AB-06 tier A",
                  evidence=["analysis/reports/ab06_field_audit.md", _AB06, "analysis/results/ab06/name_reliance.png"],
                  checks=[J(_AB06, ["P9", "verdict"], "eq", "supported")],
                  note="Answered: three of the four systems entered lose >= 0.10 directed F1 when names are swapped (Causal-Copilot "
                       "gpt-4o, causaliq, MATMCD). Vashishtha does not (0.020); it takes 89% of directions from data."),
    "DLV-02": dict(status="done", blocked_by=None,
                   criterion="Every dataset in the frozen suite has a recorded live run in each name arm (real, neutral, moved) that "
                             "reached S3; crashes are counted as crashes; every run recorded and the code tree verified before and after "
                             "(restated 14 Oct, docs/decisions/2026-10-14_audit_closeout.md)",
                   evidence=["runs/*/meta.json", "plans/results/", "analysis/results/stability_s2/bnd08_summary.json", _CO],
                   checks=[{"t": "runs", "live": True, "tree_ok": True},
                           J("analysis/results/stability_s2/bnd08_summary.json", ["all_code_identity_ok"], "true"),
                           G(_CO, r"DLV-02")],
                   note="Closed 14 Oct under the restated criterion: 84 live runs on S1 and 30 on S2; every arm reached S3. The 6 S2 "
                        "arms whose only gpt-4o run crashed at the cycle step are not rerun: the crash is the system's own (18 of 19 "
                        "live entries) and is reported as a finding."),
    "AUD-13": dict(status="done", blocked_by=None, criterion="Bundle-1 arms repeated with one other model (S2, 10 families x 3 arms)",
                   evidence=["analysis/reports/ab06_cc_second_model.md", "analysis/results/ab06_cc/s2_verdicts.json"],
                   checks=[J("analysis/results/ab06_cc/s2_verdicts.json", ["M4", "verdict"], "eq", "SUPPORTED")],
                   note="Causal-Copilot on gpt-4o-mini, 30 runs: M4 supported 9/10, M2 refuted on both models; name reliance 0.094 "
                        "vs 0.167 on gpt-4o (RQ-17)."),
    "EXT-06": dict(note="Draft ready (docs/drafts/bug_reports/); AB-06 adds the PyWhy guidance clock crash and MATMCD notes in "
                        "docs/drafts/bug_reports/agents_output_contracts_ab06.md. Uzair decides whether to send."),
    "AUD-41": dict(note="Carried forward past the audit chapter (docs/decisions/2026-10-14_audit_closeout.md): interviews still decide "
                        "P13 and C1; they run whenever a chance arises and gate nothing."),
    "AUD-32": dict(evidence=None,  # extended below
                   note="Approved 12 Oct. The chapter closed 14 Oct: 17 bundles done or closed by decision; see "
                        "analysis/reports/audit_closeout.md."),
}
for _i in ITEMS:
    if _i["id"] in _P16:
        _u = {k: v for k, v in _P16[_i["id"]].items() if v is not None or k == "blocked_by"}
        _i.update(_u)
        if _i["id"] == "AUD-38":
            _i["evidence"] = list(_i["evidence"]) + ["plans/ab06_prereg_amendment_3.json",
                "manifests/evidence/ab06_prereg_amendment3_2026-10-14.sha256", _AB06, "analysis/results/ab06/CONTRACT.json",
                "analysis/ab06_figure.py", "analysis/results/ab06/name_reliance.png", "analysis/results/ab06/name_reliance.svg",
                "analysis/reports/ab06_field_audit.md"]
        if _i["id"] == "AUD-32":
            _i["evidence"] = list(_i["evidence"]) + ["analysis/reports/audit_closeout.md", _CO]
        if _i["id"] == "EXT-06":
            _i["evidence"] = list(_i["evidence"]) + ["docs/drafts/bug_reports/agents_output_contracts_ab06.md"]

_B16 = {"BND-08": "done", "BND-10": "done", "BND-11": "done",
        "AB-06": "done", "AB-16": "done", "AB-17": "done"}
BUNDLE_STATUS.update(_B16)
BUNDLE_NOTE.update({
    "BND-08": "Closed 14 Oct with DLV-02 under its restated criterion: 30 runs, 24 completed, 6 crashed at the cycle step, all "
              "reached S3. M1, M3, M4 SUPPORTED; M2 REFUTED (5/10); M5 not run. Crashes are reported as a finding, not rerun.",
    "BND-10": "Done 14 Oct (BND-08 closed, rule W3). Pooled held-out (55 tables): R1 INCONCLUSIVE 40/55, R2 INCONCLUSIVE 47/55, "
              "R3 SUPPORTED -0.003. TGT-09 met by v2 in BND-11.",
    "BND-11": "Done 14 Oct: v2 R1-R3 SUPPORTED 22/22 held-out formula files; names R4, R5 SUPPORTED, R6 REFUTED (1/10); 0 crashes.",
    "BND-12": "Audit parts done (AUD-13, RQ-17; REP-11 data part reproduced). Remaining live parts (CARE moved-names control, "
              "LLM and fused Sachs numbers, CausalSteward) moved to the Q2 build (B3) on 14 Oct.",
    "AB-06": "Tier A scored 14 Oct: P9 SUPPORTED (3 of 4 systems lose >= 0.10 with names swapped), P10 SUPPORTED (MATMCD below "
             "its own data-only graph). $32.11. Tier B not run (DEC-05).",
    "AB-16": "Decided 14 Oct: B (measurement + reliability-first claim ledger), A as the floor; methods + benchmark venue.",
    "AB-17": "Skeleton and Q2 build pre-registration hashed 14 Oct (manifests/evidence/paper_prereg_2026-10-14.sha256).",
})
for _i in ITEMS:
    if _i["id"] in _B16 and _i.get("kind") == "bundle":
        _i["status"] = _B16[_i["id"]]
        _tail = ("Runner:" + _i["note"].split("Runner:", 1)[1]) if "Runner:" in _i["note"] else ""
        _i["note"] = (BUNDLE_NOTE[_i["id"]] + " " + _tail).strip()
    if _i["id"] == "BND-12":
        _tail = ("Runner:" + _i["note"].split("Runner:", 1)[1]) if "Runner:" in _i["note"] else ""
        _i["note"] = (BUNDLE_NOTE["BND-12"] + " " + _tail).strip()

# ---- overrides p17 (2026-10-15): the Q2 build, first pass (B0-B5 of plans/q2_dag.json)
_Q = "analysis/results/"
_B0R, _B1R, _B2R, _B3R = ("analysis/reports/q2_b0_engines_guards.md", "analysis/reports/q2_b1_data_only_ledger.md",
                          "analysis/reports/q2_b2_interventions.md", "analysis/reports/q2_b3_knowledge_tiers.md")
_B4R, _B5R, _BR = "analysis/reports/q2_b4_confidence.md", "analysis/reports/q2_b5_audit_adapter_rca.md", "analysis/reports/q2_build_results.md"
_HO = _Q + "q2_b1/heldout.json"
_B2S, _B3S, _B4E, _B5T = _Q + "q2_b2/summary_test.json", _Q + "q2_b3/summary_test.json", _Q + "q2_b4/evaluate_test.json", _Q + "q2_b5/rca_test.json"
_LM = _Q + "q2_landmarks.json"
_MAN = {"t": "manifest", "path": "manifests/evidence/q2_build_2026-10-15.sha256"}
ITEMS.append(item("TGT-18", "TGT", "DV-1 precision > 0.80 at >= 50% coverage, both families, held out (landmark ER-2)", "todo", kind="target",
                  criterion="Lower end of the scenario-cluster 95% interval of DV-1 precision of the selective view at >= 0.50 coverage "
                            "> 0.80 on the CausalArena test split, semantic and formula (docs/decisions/2026-10-14_q2_landmarks.md)"))
ITEMS.append(item("TGT-19", "TGT", "Accuracy landmark ER-4a: data-only F1 above GES (route A), or knowledge tiers lift > 0.03 (route B)", "todo",
                  kind="target",
                  criterion="Route A: kernel D minus GES directed F1, lower end > 0 on one family; route B: D+K minus D (real names), "
                            "lower end > 0.03 on one family; held out"))
ITEMS.append(item("TGT-20", "TGT", "RCA through the ledger: AC@3 >= 0.90 at coverage >= 0.5 on PetShop held out (landmark ER-4b)", "todo",
                  kind="target",
                  criterion="Lower end of the 95% bootstrap interval over test issues (2,000 resamples, seed 20261015) of AC@3 on "
                            "answered issues >= 0.90, coverage >= 0.5"))
ITEMS.append(item("BLD-15", "BLD", "Audit adapter: other systems' outputs read as typed claims with violation classes", "todo",
                  criterion="Every flagged violation names a pair, a claim and a source; 0 unknown sources for agents that record "
                            "provenance; Causal-Copilot's provenance reconstructed from stage graphs and labelled as such (B5.1)"))
ITEMS.append(item("EXT-07", "EXT", "Note to causal-learn maintainers: PC's Meek step can return a directed cycle (stale ancestor matrix)",
                  "open", kind="decision",
                  criterion="Uzair decides whether to send; the draft states the measurement and a minimal reproduction",
                  evidence=["docs/drafts/bug_reports/causal_learn_meek_directed_cycle.md", _B1R],
                  checks=[G(_B1R, r"Two engine defects")],
                  note="Found in B1 rung R1 (6 dev and 6 held-out files). The kernel works around it (re-derivation, cycles withdrawn and "
                       "recorded), so nothing waits on the note."))
_P17 = {
    # ---------------- B0
    "CAP-05": dict(status="done", blocked_by=None, criterion="Engines see canonical column order only; claims and evidence identical under "
                   "column permutations (oracle and full reruns)",
                   evidence=[_Q + "q2_b0/oracle_check.json", _Q + "q2_b1/invariance_dev.json", _B0R, _B1R],
                   checks=[J(_Q + "q2_b0/oracle_check.json", ["order_invariant_dags"], "eq", 120),
                           J(_Q + "q2_b1/invariance_dev.json", ["content_identical"], "eq", 50)],
                   note="B0.1: 120/120 oracle DAGs order-invariant (6 orders each). B1 R3: 50/50 dev files identical claims and evidence "
                        "under 6 orders with full engine reruns. Names can still break ties among exactly identical columns (B3 finding; "
                        "docs/design/q2_kernel_v3_proposals.md K3-1)."),
    "CAP-11": dict(status="done", blocked_by=None, criterion="Same inputs, same ledger hash",
                   evidence=[_Q + "q2_b1/invariance_dev.json", _B1R],
                   checks=[J(_Q + "q2_b1/invariance_dev.json", ["hash_repeat_identical"], "eq", 50)],
                   note="50/50 repeat builds give the same ledger hash (B1 R3); single-threaded engines pinned in engines/MANIFEST.json."),
    # ---------------- B1
    "BLD-02": dict(status="done", blocked_by=None, criterion="Data-only ledger (B1) passes I1-I4, I7 on dev and its held-out gate B1.2",
                   evidence=["kernel/", "plans/b1_prereg.json", "plans/b1_prereg_amendment_1.json", "plans/b1_freeze.json", _HO,
                             _Q + "q2_b1/access_log.jsonl", _B1R],
                   checks=[J(_HO, ["B1.2_pass"], "true"), J(_HO, ["ER-F_met"], "true"), _MAN],
                   note="Rule C3 (GES-led, PC-audited) chosen on dev. Held out against plain PC maxP: F1 +0.053 / +0.115, DV-1 +0.073 / "
                        "+0.053 (semantic / formula), every interval above zero; against GES F1 -0.001 / +0.002, DV-1 +0.028 / +0.030. "
                        "One aborted read (build error on an engine defect), fixed as a class by amendment 1 and re-read once."),
    "BLD-14": dict(status="done", blocked_by=None,
                   evidence=["ledger/schema02.py", "ledger/verify02.py", "tests/test_q2_kernel.py", _B1R],
                   checks=[G(_B1R, r"1,250 dev and 500 held-out ledgers pass V1-V13 and K7")],
                   note="Ledger v0.2 fields (plan, deviations, assumptions with sensitivities, lineage, question, orientation convention, "
                        "engine outputs, reviews); the verifier runs every check (V1-V13) even after a failure."),
    "CAP-09": dict(status="done", blocked_by=None, criterion="Every claim cites its evidence; an independent NumPy checker (K7) re-derives "
                   "every claim from the records alone",
                   evidence=["kernel/checker.py", "kernel/derive.py", "tests/test_q2_kernel.py", _B1R, _B2R, _B3R],
                   checks=[G(_B1R, r"removing a load-bearing uncited test fails K7")],
                   note="0 failing ledgers across B1 (1,750), B2 (1,002) and B3 (750 held-out and 750 dev D+K ledgers)."),
    "TGT-10": dict(status="done", blocked_by=None, criterion="Zero change in claims when columns are shuffled",
                   evidence=[_Q + "q2_b1/invariance_dev.json", _Q + "q2_b0/oracle_check.json"],
                   checks=[J(_Q + "q2_b1/invariance_dev.json", ["pass"], "true")],
                   note="Met by construction and measured: 50/50 dev files, 120/120 oracle DAGs."),
    "TGT-19": dict(status="in_progress", blocked_by=None,
                   evidence=[_HO, _B3S, _LM, _B1R, _B3R, "docs/design/q2_kernel_v3_proposals.md"],
                   checks=[J(_HO, ["ER-4a_route_A_met"], "false"), J(_B3S, ["families", "formula", "ER-4a_route_B", "met"], "false")],
                   note="Measured, not met. Route A: F1 against GES -0.001 [-0.007, +0.005] / +0.002 [-0.012, +0.017]. Route B: tier gain "
                        "+0.019 [+0.010, +0.030] / +0.028 [+0.019, +0.037], lower ends below 0.03. Candidates for a v3 kernel in "
                        "docs/design/q2_kernel_v3_proposals.md."),
    # ---------------- B2
    "BLD-03": dict(status="done", blocked_by=None, criterion="Interventions as shift evidence orient adjacent pairs only; B2.1 and B2.2 pass",
                   evidence=["kernel/interventions.py", "kernel/run_b2.py", "plans/b2_prereg.json", "plans/b2_freeze.json", _B2S,
                             _Q + "q2_b2/chambers.json", _Q + "q2_b2/access_log.jsonl", _B2R],
                   checks=[J(_B2S, ["families", "semantic", "B2.2_family"], "true"), J(_B2S, ["families", "formula", "B2.2_family"], "true"),
                           J(_B2S, ["chambers", "B2.2_chambers"], "true")],
                   note="Held out: D+I DV-1 mean per-file gain +0.017 / +0.005 (semantic / formula); Chambers D+I 0.926 vs D 0.925; "
                        "0 failing ledgers."),
    "CAP-03": dict(status="done", blocked_by=None, evidence=[_B2S, _B2R],
                   checks=[J(_B2S, ["families", "semantic", "B2.2_family"], "true")],
                   note="Single-target intervention rows enter as shift evidence (Welch, alpha 0.01); an intervention overrides a data "
                        "direction and the claim records the conflict."),
    "TGT-06": dict(status="in_progress", blocked_by=None, evidence=[_Q + "q2_b2/chambers.json", _B2R],
                   checks=[J(_B2S, ["chambers", "ER-C", "within_0.03"], "eq", [True, True])],
                   note="ER-C met on DV-1 precision: kernel D 0.925, D+I 0.926, GES 0.916, PC maxP 0.887; agreement with held-back rows "
                        "0.985 (true DAG 0.943). The F1 comparison with CDFM's second-hand 0.727 needs its subset confirmed (REP-09) and "
                        "was not pre-registered for B2."),
    # ---------------- B3
    "BLD-04": dict(status="done", blocked_by=None, criterion="Declared knowledge as tiers on open pairs only; B3.1-B3.3 pass held out",
                   evidence=["kernel/knowledge.py", "kernel/run_b3.py", "supplier/tiers.py", "plans/b3_prereg.json", "plans/b3_freeze.json",
                             _B3S, _Q + "q2_b3/access_log.jsonl", _B3R],
                   checks=[J(_B3S, ["families", "semantic", "B3.1"], "true"), J(_B3S, ["families", "formula", "B3.1"], "true"),
                           J(_B3S, ["families", "semantic", "B3.2"], "true"), J(_B3S, ["families", "formula", "B3.2"], "true"),
                           J(_B3S, ["families", "semantic", "B3.3"], "true"), J(_B3S, ["families", "formula", "B3.3"], "true")],
                   note="No new model call: AB-07's recorded gpt-4o replies replayed through the supplier contract. Neutral arm equals D "
                        "125/125 per family; skeleton never moves; moved-arm loss within T3 125/125; 0 failing ledgers."),
    "CAP-04": dict(status="done", blocked_by=None, evidence=[_B3S, _B3R],
                   checks=[J(_B3S, ["families", "semantic", "B3.1"], "true")],
                   note="Tiers orient only pairs the data left open; consensus of the answering phrasings; no propagation; cycles skipped "
                        "and recorded."),
    "TGT-11": dict(status="done", blocked_by=None, criterion="Moved-names loss within the exact T3 bound on 100% of held-out files",
                   evidence=[_B3S, _B3R],
                   checks=[J(_B3S, ["families", "semantic", "B3.2"], "true"), J(_B3S, ["families", "formula", "B3.2"], "true")],
                   note="125/125 per family; realised moved-arm F1 change -0.001 [-0.007, +0.004] / +0.003 [-0.006, +0.013]."),
}
_RV = _Q + "q2_b4/raw_vs_calibrated_test.json"
_AD = _Q + "q2_b5/adapters.json"
_P17.update({
    # ---------------- B4
    "BLD-05": dict(status="done", blocked_by=None, criterion="B4 built (stability, isotonic maps frozen before the held-out read, selective "
                   "view at c/g = 1, 2, 4) and read held out once; gates B4.1 and B4.2 reported",
                   evidence=["kernel/confidence.py", "kernel/run_b4.py", "calibration/", "plans/b4_prereg.json", "plans/b4_freeze.json",
                             _B4E, _RV, _Q + "q2_b4/access_log.jsonl", _B4R],
                   checks=[J(_B4E, ["families", "formula", "dv", "ece"], "le", 0.05), _MAN],
                   note="Held out: B4.1 (ECE <= 0.05) fails on semantic (0.057) and passes on formula (0.036); B4.2 passes (realised >= "
                        "claimed - 0.03 at c/g = 1, 2, 4 on point estimates). The semantic miss is under-claiming: test claims are "
                        "right more often than dev claims at the same stability."),
    "CAP-07": dict(status="in_progress", blocked_by=None, evidence=[_B4E, _RV, _B4R],
                   checks=[J(_RV, ["TGT-12_met"], "true")],
                   note="Every claim carries a calibrated probability (isotonic map on 10-resample stability). Held-out ECE 0.057 "
                        "semantic / 0.036 formula against 0.199 / 0.165 raw; the 0.05 gate is missed on semantic. Proposals in "
                        "docs/design/q2_kernel_v3_proposals.md (K3-4)."),
    "CAP-08": dict(status="done", blocked_by=None, criterion="Selective view: claims kept by calibrated probability at stated cost "
                   "ratios; realised >= claimed - 0.03 (B4.2)",
                   evidence=[_B4E, _B4R], checks=[G(_B4R, r"\*\*B4.2\*\* realised >= claimed - 0.03 at c/g = 1, 2, 4 \| \*\*pass\*\*")],
                   note="Selective view at c/g = 1, 2, 4 (act when p >= 0.5, 0.667, 0.8) and at half coverage; realised precision at "
                        "or above claimed in both families."),
    "TGT-12": dict(status="done", blocked_by=None, criterion="Calibrated ECE below raw bootstrap-frequency ECE on held-out scenarios "
                   "(lower end of the scenario-cluster interval of the difference > 0), both families",
                   evidence=[_RV, _B4R], checks=[J(_RV, ["TGT-12_met"], "true")],
                   note="Raw minus calibrated ECE +0.143 [+0.090, +0.166] semantic, +0.129 [+0.081, +0.167] formula (DV-1 claims), "
                        "computed from the rows of B4's single logged read."),
    "TGT-18": dict(status="in_progress", blocked_by=None, evidence=[_B4E, _LM, _B4R],
                   checks=[J(_LM, ["landmarks", "ER-2", "met"], "false")],
                   note="Measured, not met: semantic 0.812 [0.756, 0.864] at coverage 0.578; formula 0.899 [0.854, 0.939] at 0.615 "
                        "(met for formula alone). 25 scenarios per family set the interval."),
    # ---------------- B5
    "BLD-15": dict(status="done", blocked_by=None, evidence=["audit/adapters.py", "audit/run_adapters.py", "audit/export_cc_stages.py", _AD, _B5R],
                   checks=[J(_AD, ["B5.1", "pass"], "true"), J(_AD, ["B5.1", "unknown_sources_where_provenance_recorded"], "eq", 0)],
                   note="Five systems' AB-06 outputs read as typed claims; Causal-Copilot's sources rebuilt from stage graphs (30/30 equal) "
                        "and labelled. Flags e.g. 384 connections Causal-Copilot's knowledge created against its data floor, 398 MATMCD "
                        "reversals of its own data."),
    "TGT-20": dict(status="in_progress", blocked_by=None, evidence=[_B5T, _LM, _B5R],
                   checks=[J(_B5T, ["ER-4b", "met"], "false"), J(_B5T, ["ER-4b", "answered"], "eq", 44)],
                   note="Measured, not met under the interval rule: AC@3 0.932 [0.841, 1.000] at coverage 0.917 on 44 answered issues "
                        "(reproduces AB-12 exactly). A lower end of 0.90 needs at most one miss at this sample size: more issues, not "
                        "a better ranking."),
})
for _i in ITEMS:
    if _i["id"] in _P17:
        _u = {k: v for k, v in _P17[_i["id"]].items() if v is not None or k == "blocked_by"}
        _i.update(_u)

_B17 = {"B0": "done", "B1": "done", "B2": "done", "B3": "done", "B4": "done", "B5": "done"}
BUNDLE_STATUS.update(_B17)
BUNDLE_NOTE.update({
    "B0": "Done 15 Oct: B0.1 oracle 720/720 exact, 120/120 order-invariant; B0.2 fault suite 7/7; scorer reproduces 102 audit numbers "
          "exactly; baselines on the test splits.",
    "B1": "Done 15 Oct: rule C3 held out beats PC maxP on F1 and DV-1 in both families (ER-F met); ties GES on F1 (route A not met), "
          "beats it on DV-1. 1,750 ledgers verify; one aborted read, fixed as a class.",
    "B2": "Done 15 Oct: D+I >= D on DV-1 held out (both families) and on Chambers; ER-C met (kernel 0.926 vs GES 0.916).",
    "B3": "Done 15 Oct, no live run (recorded AB-07 replies): ER-1 met (neutral = D, skeleton fixed, moved within T3, every ledger "
          "verifies); route B not met (+0.019 / +0.028).",
    "B4": "Done 15 Oct: calibrated ECE 0.057 / 0.036 vs raw 0.199 / 0.165 (TGT-12 met); B4.1 fails on semantic; ER-2 met for formula "
          "only (semantic lower end 0.756); ER-3 not met.",
    "B5": "Done 15 Oct: adapter B5.1 passes on five systems; RCA through the ledger reproduces AB-12 (0.932 at 0.917); ER-4b not met "
          "(lower end 0.841, 44 issues). Held-out read ran after B4.1 failed; B5 uses nothing from B4 (deviation recorded).",
})

# ---- overrides p18 (2026-10-15): kernel v3 (K0-K4), dev experiments, freeze 0cda331ea81cf0dd, second held-out read
_V3 = "analysis/results/q2_v3/"
_V3R, _V3D, _V3K0 = "analysis/reports/q2_v3_heldout.md", "analysis/reports/q2_v3_k1_k2_dev.md", "analysis/reports/q2_v3_k0_engine_cache.md"
ITEMS.append(item("BLD-16", "BLD", "Kernel v3: engine cache, direction view, ledger-feature confidence, pooled-replicates regime", "done",
                  criterion="K0: cache rebuild reproduces v2 dev ledgers hash-for-hash and B4 stability; K1-K4 measured on dev with their "
                            "predictions judged; v3 pre-registered, frozen and read held out once",
                  evidence=["kernel/cache.py", "kernel/harness.py", "kernel/experiment.py", "kernel/v3.py", "kernel/claim_features.py",
                            "plans/v3_prereg.json", "plans/v3_freeze.json", "manifests/evidence/v3_prereg_2026-10-15.sha256",
                            _V3 + "k0_check_v2_semantic.json", _V3 + "k0_check_v2_formula.json", _V3 + "k0_check_b4_semantic.json",
                            _V3 + "v3_test.json", _V3 + "access_log.jsonl", _V3K0, _V3D, _V3R],
                  checks=[J(_V3 + "k0_check_v2_semantic.json", ["pass"], "true"), J(_V3 + "k0_check_v2_formula.json", ["pass"], "true"),
                          J(_V3 + "k0_check_b4_semantic.json", ["pass"], "true"),
                          {"t": "manifest", "path": "manifests/evidence/v3_prereg_2026-10-15.sha256"},
                          J(_V3 + "v3_test.json", ["freeze"], "eq", "0cda331ea81cf0dd")],
                  note="K0: 1,250/1,250 v2 dev ledgers rebuilt hash-for-hash from cache; a dev experiment now takes ~10 s per family "
                       "(30-70 min in v2). K1 link-recovery levers fail on dev (recovered links 33% precise; GES penalty 0.5 lowers F1); "
                       "floor measured (9.0% / 6.8% of true links have no usable signal). K2 weights refuted as a landmark lever. "
                       "v3 = v2 ledger + direction view (Meek R1/R3 not acted on) + feature confidence model; held out (second read): "
                       "ER-2 met for formula (D 0.908 [0.876], DxR 0.911 [0.863]), not semantic (D 0.830 [0.783], DxR 0.866 [0.799]); "
                       "ECE 0.021-0.026, ER-3 not met (upper ends 0.051-0.074)."))
_P18 = {
    "TGT-18": dict(note="v2 (B4, first read): semantic 0.812 [0.756], formula 0.899 [0.854]. v3 (second read, 125 files per family): "
                        "semantic 0.830 [0.783], formula 0.908 [0.876] (met for formula); pooled 5,000 rows: semantic 0.866 [0.799] "
                        "(short by 0.001), formula 0.911 [0.863]. Not met: semantic's lower end is below 0.80 in both regimes. "
                        "Semantic is capped by missed links (analysis/reports/q2_v3_k1_k2_dev.md section 3)."),
    "TGT-19": dict(note="Measured, not met (v2). v3 dev: route A still ties GES even with 5,000 rows (C3 0.551 vs GES 0.559, semantic "
                        "pooled); a lower GES penalty lowers F1 (0.522 -> 0.466). Route B: Meek propagation from knowledge adds "
                        "+0.001; the oracle ceiling of the orient-only rule is +0.060 / +0.044. Needs direction evidence beyond the "
                        "equivalence class (v4)."),
    "CAP-07": dict(note="v3 confidence model (ledger features, isotonic on cross-fitted scores): held-out ECE 0.021 semantic / 0.025 "
                        "formula (v2 0.057 / 0.036); realised >= claimed at every threshold in D; ER-3 not met because the ECE "
                        "upper ends (0.063 / 0.051) exceed 0.05 on 25 scenario clusters."),
    "CAP-11": dict(note="50/50 repeat builds give the same ledger hash (B1 R3) within one host. Across hosts the hash needs the "
                        "OpenBLAS kernel family pinned (OPENBLAS_CORETYPE=SKYLAKEX, threads 1): without it every p-value moves in the "
                        "14th digit (found by K0, 15 Oct); kernel/cache.py keys on both."),
}
for _i in ITEMS:
    if _i["id"] in _P18:
        _i.update({k: v for k, v in _P18[_i["id"]].items() if v is not None})
        if _i["id"] in ("TGT-18", "CAP-07"):
            _i["evidence"] = list(_i["evidence"]) + [_V3 + "v3_test.json", _V3R]
        if _i["id"] == "TGT-19":
            _i["evidence"] = list(_i["evidence"]) + [_V3D]
        if _i["id"] == "CAP-11":
            _i["evidence"] = list(_i["evidence"]) + [_V3K0, "kernel/cache.py"]

# ---- overrides p19 (2026-10-15): stage-by-stage anatomy of the ledger's losses (dev; corrects the dev report's blame table)
_AN = ["analysis/q2_anatomy.py", "analysis/q2_half_anatomy.py", "analysis/results/q2_v3/anatomy_dev.json",
       "analysis/results/q2_v3/half_anatomy_dev.json", "analysis/reports/q2_v3_anatomy.md"]
for _i in ITEMS:
    if _i["id"] in ("BLD-16", "TGT-18"):
        _i["evidence"] = list(_i["evidence"]) + [e for e in _AN if e not in _i["evidence"]]

# ---- overrides p20 (2026-10-15): lever map and headroom ladder (dev)
_LM = ["docs/design/q2_lever_map.md", "analysis/q2_headroom.py", "analysis/results/q2_v3/headroom_dev.json"]
for _i in ITEMS:
    if _i["id"] in ("TGT-18", "TGT-19"):
        _i["evidence"] = list(_i["evidence"]) + [e for e in _LM if e not in _i["evidence"]]

# ---- overrides p21 (2026-10-16): direction signals that do not depend on colliders (dirsig-1, dirsig-2; dev)
_DS = ["kernel/asym.py", "kernel/asym_cond.py", "tests/test_q2_asym.py", "tests/test_q2_asym_cond.py",
       "plans/dirsig_prereg.json", "plans/dirsig2_prereg.json", "manifests/evidence/dirsig_prereg_2026-10-16.sha256",
       "manifests/evidence/dirsig2_prereg_2026-10-16.sha256", "analysis/q2_dirsig.py", "analysis/q2_dirsig_diag.py",
       "analysis/q2_dirsig2.py", "analysis/results/q2_v3/dirsig_dev.json", "analysis/results/q2_v3/dirsig_diag_dev.json",
       "analysis/results/q2_v3/dirsig2_dev.json", "analysis/reports/q2_dirsig_dev.md", "docs/design/q2_lever_map.md"]
for _i in ITEMS:
    if _i["id"] == "CAP-02":
        _i["note"] = ("Measured 16 Oct (dev, two pre-registered rounds): nine collider-free direction signals (non-Gaussian, "
                      "additive-noise, regression-error, IGCI, heteroscedastic, conditional-distribution, and conditional "
                      "variants) are right 0.42-0.64 of the time on found links at 1,000 rows; no licence. Failure classes: "
                      "children with mass points (signals confidently wrong), children with several parents, mechanisms "
                      "outside every model. Lead: IGCI on pooled formula 0.86 on 153 links, to confirm on a fresh family.")
        _i["evidence"] = list(_i.get("evidence") or []) + [e for e in _DS if e not in (_i.get("evidence") or [])]
        _i["checks"] = list(_i.get("checks") or []) + [{"t": "manifest", "path": "manifests/evidence/dirsig_prereg_2026-10-16.sha256"},
                                                       {"t": "manifest", "path": "manifests/evidence/dirsig2_prereg_2026-10-16.sha256"}]
    if _i["id"] == "TGT-19":
        _i["note"] = _i["note"] + (" 16 Oct: route A through pairwise asymmetry is closed at 1,000 rows on CausalArena "
                                   "(analysis/reports/q2_dirsig_dev.md); open direction sources are interventions and knowledge.")
        _i["evidence"] = list(_i["evidence"]) + ["analysis/reports/q2_dirsig_dev.md"]

# ---- overrides p22 (2026-10-16): link filters L8 / L7 (linkfilt-1; dev)
_LF = ["kernel/linkfilt.py", "tests/test_q2_linkfilt.py", "plans/linkfilt_prereg.json",
       "manifests/evidence/linkfilt_prereg_2026-10-16.sha256", "analysis/q2_linkfilt.py", "analysis/q2_linkfilt_diag.py",
       "analysis/results/q2_v3/linkfilt_dev.json", "analysis/results/q2_v3/linkfilt_diag_dev.json", "analysis/reports/q2_linkfilt_dev.md"]
for _i in ITEMS:
    if _i["id"] == "TGT-18":
        _i["evidence"] = list(_i["evidence"]) + [e for e in _LF if e not in _i["evidence"]]
        _i["checks"] = list(_i.get("checks") or []) + [{"t": "manifest", "path": "manifests/evidence/linkfilt_prereg_2026-10-16.sha256"}]
        _i["note"] = _i["note"] + (" 16 Oct (dev): two link filters (triangle order, resampling stability) earn a licence on formula "
                                   "(cut precision 0.81; 25% / 38% of false links cut) and not on semantic, where 55% of true links "
                                   "sit beside a real mediated path; neither can act until an applicability condition exists "
                                   "(analysis/reports/q2_linkfilt_dev.md).")

# ---- overrides p23 (2026-10-19): L16 applicability conditions and L5 interventions as link evidence (dev); BEN-13
_L16 = ["plans/l16_prereg.json", "manifests/evidence/l16_prereg_2026-10-19.sha256", "analysis/q2_l16.py", "tests/test_q2_l16_l5.py",
        "analysis/results/q2_v3/l16_dev.json", "analysis/reports/q2_l16_dev.md", "docs/design/q2_lever_map.md"]
_L5 = ["plans/l5_prereg.json", "manifests/evidence/l5_prereg_2026-10-19.sha256", "analysis/q2_l5.py", "analysis/q2_l5_diag.py",
       "analysis/results/q2_v3/l5_dev.json", "analysis/results/q2_v3/l5_diag_dev.json", "analysis/reports/q2_l5_dev.md"]
for _i in ITEMS:
    if _i["id"] == "TGT-18":
        _i["evidence"] = list(_i["evidence"]) + [e for e in _L16 + _L5 if e not in _i["evidence"]]
        _i["checks"] = list(_i.get("checks") or []) + [
            {"t": "manifest", "path": "manifests/evidence/l16_prereg_2026-10-19.sha256"},
            {"t": "manifest", "path": "manifests/evidence/l5_prereg_2026-10-19.sha256"},
            J("analysis/results/q2_v3/l16_dev.json", ["verdicts", "P-A3"], "eq", "supported"),
            J("analysis/results/q2_v3/l16_dev.json", ["selected_gate", "transfer_guard", "passes"], "eq", False),
            J("analysis/results/q2_v3/l5_dev.json", ["licences"], "len_eq", 0)]
        _i["note"] = _i["note"] + (" 19 Oct (dev): L16, an observable gate (ledger density or triangle share) clears the pooled bar "
                                   "(0.803, 20% of false links) only by acting at a stricter cut-off on denser files; it fails the "
                                   "transfer guard (within-family rho <= 0.33) and its semantic cuts are right 0.735, so it is not acted "
                                   "on. A declared domain-structure statement licensing L8a costs -0.002 DV-1 precision when wrong "
                                   "(analysis/reports/q2_l16_dev.md). L5, interventions as link evidence: no licence; the shadow signal is "
                                   "real (48% vs 7%) but CausalArena's release reaches 20% / 13% of false links with about 40 rows per "
                                   "target (analysis/reports/q2_l5_dev.md).")
    if _i["id"] == "TGT-19":
        _i["evidence"] = list(_i["evidence"]) + [e for e in ["analysis/reports/q2_l5_dev.md", "analysis/results/q2_v3/l5_dev.json"] if e not in _i["evidence"]]
        _i["note"] = _i["note"] + (" 19 Oct: adding missed links from interventions (L5 rule A) is 9-14% precise on dev; no licence "
                                   "(analysis/reports/q2_l5_dev.md).")
ITEMS.append(item("BEN-13", "BEN", "CausalBench (GSK) shortcut audit: how much of each published score is metric echo, edge placement or name recall",
                  "todo", kind="task",
                  criterion=("Two published rows per cell line (K562, RPE1) reproduced within tolerance before any re-score claim; then per "
                             "published method: (a) edge-placement control on mean Wasserstein and FOR; (b) names-only baseline on the "
                             "biological and statistical evaluations under a gene-label permutation; the share of each published score each "
                             "channel accounts for, with intervals; predictions and thresholds hashed before the first re-score"),
                  evidence=["docs/project_snapshots/2026-10-19/benchmark-targets.md"],
                  note=("Opened 19 Oct from the CausalBench deep-dive (project:claude/benchmark-targets.md, update 2026-10-19). Data "
                        "download and long runs on Uzair's machine; the names-only arm needs a small approved model spend. First step "
                        "toward Rung 3 (evidence-typed, calibrated pairs) and the large real testbed for lever L5.")))

