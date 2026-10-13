"""Write plans/audit_dag.json: the audit program after AU1-AU8 (research landscape, commercial landscape, wedge and paper).
Proposal for Uzair's approval; same schema as plans/q1_dag.json so tracker/plan_check.py can check it.

  python plans/make_audit_dag.py && python tracker/plan_check.py plans/audit_dag.json --mermaid
"""
import json
from pathlib import Path

NONE = "none"
B = []


def bundle(id, title, track, depends_on, window, runner, llm_cost, parts, predictions, gates, must_show, outputs,
           serves, advances=(), closes=(), proposed_tickets=(), uzair_actions=(), risks=(), approval=None):
    B.append({"id": id, "title": title, "track": track, "depends_on": list(depends_on), "runner": runner, "window": list(window),
              "closes": list(closes), "advances": list(advances), "proposed_tickets": list(proposed_tickets),
              "llm_cost": llm_cost, "approval_needed": approval if approval is not None else ("yes" if llm_cost != NONE else None),
              "uzair_actions": list(uzair_actions), "parts": list(parts), "predictions": list(predictions), "gates": list(gates),
              "must_show": list(must_show), "outputs": list(outputs), "risks": list(risks), "serves": list(serves)})


# ------------------------------------------------------------------ research landscape
bundle("AB-01", "Controlled scoreboard, CausalArena complete", "research", [], ("2026-10-12", "2026-10-17"), "Claude (free compute)", NONE,
       ["done 12 Oct: engine oracle (AUD-27), released vs shuffled re-score of PC/GES/FCI/LiNGAM/NOTEARS on semantic and formula (AUD-28), "
        "PC conflict-rule mechanism (AUD-28), sortability (AUD-29)",
        "remaining: synthetic family; the D+I regime (GIES with the released targets, released vs shuffled); PC with maxP and with the "
        "order-free conservative rule on all families; a corrected leaderboard table (published, our released, our shuffled, rule used)"],
       ["P1 GIES with targets gains under 0.01 from shuffling under the expectation rule and 0.01-0.04 under the authors' rule (refuted: |gain| > 0.05 expectation rule)",
        "P2 PC with maxP: released and shuffled within 0.01 in all three families (refuted: > 0.03 in any)"],
       ["every published row we can run has released and shuffled numbers, both orientation rules, files paired"],
       ["corrected leaderboard table", "per-family layout gain by channel (authors' rule, conflict rule, engine copy)"],
       ["analysis/results/rescore/ (extended)", "analysis/reports/ab01_controlled_scoreboard.md"],
       ["L1"], advances=["BEN-07", "REP-07", "EXT-01"], proposed_tickets=["AUD-33 controlled scoreboard complete"])

bundle("AB-02", "Second scoreboard: do the layout and conflict channels exist elsewhere?", "research", ["AB-01"], ("2026-10-14", "2026-10-24"),
       "Claude (free compute)", NONE,
       ["pick two public benchmarks with published per-method numbers and released files (candidates from AU2: CausalBench (Wang et al.), "
        "bnlearn networks as used by LLM papers, CausalTime, CIPCaD); measure column order vs causal order, R2-sortability, and the "
        "released vs shuffled re-score of PC/GES/FCI",
        "record which published numbers can be reproduced within their reported error"],
       ["P3 at least one of the two releases lists columns in an order correlated with causal order (Kendall tau > 0.3) (refuted: both < 0.1)",
        "P4 PC's conflict-rule effect (released vs shuffled q) appears wherever columns follow causal order (refuted: |delta q| < 0.03 there)"],
       ["reproduction of at least two published rows per benchmark within reported error before any re-score claim"],
       ["per-benchmark table: order correlation, sortability, layout gain per method"], ["analysis/reports/ab02_second_scoreboard.md"],
       ["L1"], advances=["BEN-07", "STR-01"], proposed_tickets=["AUD-34 second scoreboard"],
       risks=["release formats differ; a benchmark may not publish per-method numbers we can reproduce"])

bundle("AB-03", "Engine forensics across the tools agents call", "research", [], ("2026-10-14", "2026-10-24"), "Claude (free compute)", NONE,
       ["extend the oracle check (AUD-27) to every engine an audited agent or library ships: causal-learn GES/CD-NOD/GIN with "
        "oracle scores where defined, pgmpy PC, dodiscover PC/FCI, gCastle PC settings, Causal-Copilot's other algorithm copies; "
        "Tetrad via py-tetrad if Java runs; pcalg only if R installs on Uzair's machine",
        "determinism: same inputs, three runs, threads and processes; time-series engines (Tigramite PCMCI) with an oracle",
        "file upstream-style bug reports as drafts (EXT-03) for Uzair to send"],
       ["P5 at least one more widely used engine besides gCastle original/stable returns a wrong skeleton under a perfect oracle (refuted: all others 100%)"],
       ["every engine version pinned by wheel hash; oracle runs reproducible from one command"],
       ["engine defect table: exact rate, order invariance, determinism, defect class"],
       ["analysis/results/engine_oracle/ (extended)", "analysis/reports/ab03_engine_forensics.md"],
       ["L1", "L4"], advances=["EXT-03", "CAP-05", "CAP-11"], proposed_tickets=["AUD-35 engine forensics"])

bundle("AB-04", "Decision-value scoreboard", "research", ["AB-01"], ("2026-10-14", "2026-10-28"), "Claude (free compute)", NONE,
       ["DV-1 (done 12 Oct on CausalArena, AUD-30) extended to: the synthetic family; Causal Chambers obs+int sample (53 regimes, physical "
        "ground truth); Sachs with its real interventions",
        "DV-2: regret of choosing an intervention target to move a named outcome, vs random and vs the true graph",
        "risk-coverage curves from bootstrap frequencies (no calibration yet); AID next to F1 for every method",
        "the 'nothing moves' and 'everything downstream of inputs' baselines on every benchmark", "usefulness threshold: the precision at stated coverage at which acting on the learned graph beats acting on 'nothing moves' or on a declared topology, measured as DV-2 regret, with the costs of wrong claims taken from AB-10's interviews"],
       ["P6 on every benchmark, at most two of the reproduced methods beat the empty graph's committed-claim precision by more than 0.05 "
        "(refuted: four or more do)",
        "P7 the true-CPDAG ceiling exceeds the best method by at least 0.15 on every benchmark (refuted: < 0.05 anywhere)"],
       ["baselines and ceilings computed on exactly the files each method finished; claims checked against truth; data-checked agreement reported only with the true DAG's own agreement as its ceiling"],
       ["decision-value table across benchmarks", "risk-coverage figure", "F1 vs DV scatter"],
       ["analysis/results/decision_value/ (extended)", "analysis/reports/ab04_decision_value.md"],
       ["L3"], advances=["TGT-15", "TGT-16", "EVL-03", "CAP-15"], proposed_tickets=["AUD-36 decision-value scoreboard"])

bundle("AB-05", "LIVE (small): agent probes, install and one-run cost per agent", "research", [], ("2026-10-14", "2026-10-20"), "Uzair (live)",
       "one run per agent on one public scenario: Vashishtha et al. order elicitor, PyWhy-LLM pairwise, MATMCD, causaliq-knowledge, "
       "Causal-Copilot on a second model; cap $5 in total",
       ["Claude installs each agent in the harness offline, runs it with the stub model, measures calls and tokens per run",
        "Uzair runs one live call set per agent; the plan file caps tokens"],
       ["P8 at least three of the five agents run end to end on a 20-40 variable CausalArena scenario (refuted: one or none)"],
       ["no key in any log; every call recorded; repo byte-identical"],
       ["per-agent: installs, runs, calls, tokens, cost, wall time, failure points"],
       ["analysis/results/agent_probes/", "plans/ab05_probe_*.json"], ["L2"], advances=["STR-01"], proposed_tickets=["AUD-37 agent probes"],
       uzair_actions=["approve the cap", "cc.ps1 plan plans/ab05_probe_<agent>.json for each"],
       risks=["licences: Takayama, ILS-CSL, ArgCausalDisco have none; run for evaluation only, never redistribute wrappers"])

bundle("AB-06", "LIVE: field audit under names x layout controls", "research", ["AB-05", "AB-04", "AB-01"], ("2026-10-21", "2026-11-14"),
       "Uzair (live)", "set from AB-05: about 3 arms x 10 dev scenarios x the agents that ran; Causal-Copilot $0.46/run measured; "
       "budget proposed in the AB-05 report before any spend",
       ["arms: real / neutral / swapped names, all with shuffled columns; each agent's own data-only mode where it has one",
        "scores: F1, S/c/q, DV-1, name-reliance (swapped minus real, per edge provenance where logged)",
        "absorbs BND-12's second-model part for Causal-Copilot"],
       ["P9 at least three agents lose >= 0.10 directed F1 from real to swapped names (refuted: none does)",
        "P10 at least one agent scores below its own data-only output with real names on DV-1 (refuted: all at or above)"],
       ["thresholds hashed into the plan before the calls; dev split only; held-out reserved"],
       ["per agent x arm table", "name-reliance figure", "where each agent's directions come from (provenance shares)"],
       ["analysis/results/field_audit/", "analysis/reports/ab06_field_audit.md"],
       ["L2"], advances=["STR-01", "RQ-05", "RQ-17", "AUD-13"], proposed_tickets=["AUD-38 field audit"],
       uzair_actions=["approve budget from AB-05", "run the plan files"])

bundle("AB-07", "LIVE: knowledge elicitation (A3), what can a model supply?", "research", ["AB-01"], ("2026-10-16", "2026-10-28"),
       "Uzair (live)", "about 900 short calls (DEC-02): tiers only, three phrasings, three name arms, 50 semantic + 50 formula scenarios",
       ["prompt and thresholds hashed before the calls (O1-O5 of program v2)", "post-cutoff and fictitious-name controls from AU2 "
        "(Srivastava graphs, Feng et al. design) on a subset"],
       ["O1-O5 as pre-registered in program v2"], ["DEC-02 approved"],
       ["O1-O5 verdicts", "tier accuracy by arm", "regression on model tiers vs 0.634 / 0.524"],
       ["analysis/results/a3_elicitation/", "analysis/reports/ab07_knowledge_elicitation.md"],
       ["L2", "L4"], advances=["RQ-10", "RQ-11", "RQ-12", "RQ-13", "RQ-14", "CAP-04", "BLD-04"], proposed_tickets=[],
       uzair_actions=["decide DEC-02", "run the plan file"])

bundle("AB-08", "Name-reliance benchmark (decoupled semantics, B2)", "research", ["AB-04"], ("2026-10-21", "2026-11-14"),
       "Claude (free to build); agent runs inside AB-06's budget", NONE,
       ["generator: CausalArena's released SCM sampler (or our own) with names taken from a second plausible system whose graph "
        "disagrees with the data on a set fraction rho of edges (rho = 0, 0.25, 0.5, 0.75, 1)",
        "ArenaShuffle overlay (B1): server-side arms, declared regime, scored confidence matrices",
        "scorer: AB-04's DV metrics plus per-edge provenance"],
       ["P11 for name-reading agents, directed F1 falls monotonically in rho (Spearman <= -0.8) (refuted: no trend)"],
       ["the generator's own sortability and layout reported; columns always shuffled"],
       ["rho curve per method", "benchmark card"], ["benchmarks/name_reliance/", "analysis/reports/ab08_name_reliance.md"],
       ["L2", "L3"], advances=["STR-02", "EVL-02"], proposed_tickets=["AUD-39 name-reliance benchmark"],
       risks=["choosing 'plausible' second systems needs care; an LLM may be used to propose names, recorded as knowledge with hashes"])

bundle("AB-09", "Theory pack", "research", [], ("2026-10-15", "2026-11-07"), "Claude", NONE,
       ["F1 = S x a identity and the three-term error budget (identifiability, finite sample, algorithm), with the per-scenario proof",
        "bounded harm under I5: wrong knowledge can cost at most the directions it decided; tight example",
        "order dependence of PC's collider conflict rules and why maxP removes it; the decision-value ceiling of the CPDAG",
        "each statement checked numerically on CausalArena files"],
       ["P12 every statement holds on all 500 public files to numerical precision (refuted: any counterexample, then restate)"],
       ["no statement beyond what AU3's references support"], ["proof notes", "numerical checks"],
       ["analysis/theory/", "analysis/reports/ab09_theory.md"], ["L5"], advances=["RQ-04", "RQ-06"], proposed_tickets=["AUD-40 theory pack"])

# ------------------------------------------------------------------ commercial landscape
bundle("AB-10", "Practitioner interviews", "commercial", [], ("2026-10-14", "2026-11-07"), "Uzair (interviews); Claude prepares and synthesises", NONE,
       ["screener and interview guide (Claude); 5-8 interviews: IT operations / SRE, marketing science, real-world evidence, policy analytics",
        "hypotheses: H1 they would use per-claim provenance and abstention; H2 they ask intervention questions, not graph questions; "
        "H3 a name/semantic dependence audit of their LLM tools is worth paying for",
        "check with the course staff whether informal interviews need any human-subjects review before starting"],
       ["P13 at least half of interviewees name a decision where 'which causes, how sure' matters more than the full graph (refuted: under a quarter)"],
       ["notes stored without personal data beyond role and sector"], ["interview synthesis with quotes paraphrased"],
       ["docs/interviews/ (role-coded)", "analysis/reports/ab10_interviews.md"], ["C1"], advances=["STR-06"],
       proposed_tickets=["AUD-41 practitioner interviews"], uzair_actions=["recruit and run the interviews"], approval="yes")

bundle("AB-11", "Competitive teardown", "commercial", ["AB-04"], ("2026-10-15", "2026-10-31"), "Claude (desk + free compute)", NONE,
       ["hands-on with open tools (DoWhy + causal-learn, Tetrad, pgmpy, PyWhy-LLM, Causal-Copilot) on one public scenario: what each "
        "outputs, what it claims, whether it would pass the ledger verifier's checks, its decision-value score",
        "vendor documentation for closed tools (causaLens, Causely, Datadog, Dynatrace): claimed guarantees and formats only, labelled as claims"],
       ["P14 no tool records a per-direction source (refuted: any does)"], ["vendor claims never presented as measurements"],
       ["teardown table"], ["analysis/reports/ab11_teardown.md"], ["C1", "L4"], advances=["STR-06", "CAP-09"],
       proposed_tickets=["AUD-42 competitive teardown"])

bundle("AB-12", "Vertical probe: root-cause analysis", "commercial", ["AB-04"], ("2026-10-20", "2026-11-07"), "Claude (free compute)", NONE,
       ["RCAEval (or PetShop) incidents: learned-graph RCA vs BARO vs declared topology; add abstention and name-swapped service names",
        "measure top-k accuracy, abstention value, and name dependence"],
       ["P15 declared topology plus abstention beats learned-graph RCA on AC@3 by >= 0.1 (refuted: < 0.03)"],
       ["datasets reachable from the sandbox or from Uzair's machine"], ["RCA table", "what a ledger adds here"],
       ["analysis/results/rca_probe/", "analysis/reports/ab12_rca_probe.md"], ["C2"], advances=["STR-06"],
       proposed_tickets=["AUD-43 RCA vertical probe"], risks=["egress may block the datasets; then Uzair downloads them"])

bundle("AB-13", "Regulation and standards map", "commercial", [], ("2026-10-14", "2026-10-24"), "Claude (desk)", NONE,
       ["FDA RWE guidance, EMA qualification (PROCOVA precedent), ICH E9(R1), EU AI Act record-keeping, SR 26-2, TARGET/STROBE: "
        "requirement -> ledger field matrix",
        "one venue where a claim format could be proposed (a reporting guideline, a W3C PROV profile, a pharma consortium)"],
       ["none (desk map)"], ["primary texts only; summaries labelled second-hand"], ["requirement -> field matrix"],
       ["analysis/reports/ab13_regulation_map.md"], ["C3"], advances=["CAP-09", "EXT-02"], proposed_tickets=["AUD-44 regulation map"])

bundle("AB-14", "Market and go-to-market hypotheses", "commercial", ["AB-11", "AB-13"], ("2026-10-27", "2026-11-12"), "Claude (desk)", NONE,
       ["market map of causal AI: segments, vendors, funding, M&A, market-size estimates and their conflicts, platform churn",
        "bottom-up estimates for three verticals (IT incident RCA, marketing measurement, pharma RWE) from public pricing and filings; "
        "buyer, budget line, channel; every figure labelled estimate with its inputs",
        "public demand evidence on H1-H3, labelled indirect (stands in for AB-10 until interviews exist; cannot decide P13)"],
       ["none"], ["no number without its inputs"], ["market map", "three one-page vertical briefs", "H1-H3 public evidence, labelled indirect"],
       ["analysis/reports/ab14_market.md", "analysis/audits/ab14_notes/"], ["C1", "C3"], advances=["STR-06"],
       proposed_tickets=["AUD-45 market hypotheses"])

# ------------------------------------------------------------------ wedge and paper
bundle("AB-15", "Positioning closure", "wedge", [], ("2026-10-12", "2026-10-22"), "Claude (desk)", NONE,
       ["read what AU1-AU8 left unread that touches our claims: CausalArena appendices B-C, CausalVerify, ReplaySCM, CARE, MosaCD, "
        "Kitson & Constantinou 2026, Li & Russo, CausalDS, ACDB, CausaLab",
        "nearest-neighbour matrix: for each of our candidate claims L1-L5, the closest prior result and the difference"],
       ["none"], ["every claim of novelty bounded by the searches recorded"], ["novelty matrix"],
       ["analysis/reports/ab15_positioning.md"], ["L1", "L2", "L3", "L4", "L5"], advances=["DOM-07"],
       proposed_tickets=["AUD-46 positioning closure"])

bundle("AB-16", "Wedge decision (gate)", "wedge", ["AB-01", "AB-02", "AB-03", "AB-04", "AB-05", "AB-09", "AB-11", "AB-14", "AB-15"],
       ("2026-11-03", "2026-11-14"), "Uzair decides; Claude prepares", NONE,
       ["score each landmark criterion L1-L5 and C1-C3 with the evidence in hand; choose the paper's spine and the venue; set the Q2 build",
        "if AB-06 has not finished, decide on its interim results",
        "C1 from AB-14's public demand evidence (indirect) plus AB-10 interviews if any exist; the memo states which"],
       ["none (decision)"], ["decision recorded as a DEC ticket with the evidence it rests on"], ["wedge memo"],
       ["analysis/reports/ab16_wedge_decision.md"], ["L1", "L2", "L3", "L4", "L5", "C1", "C2", "C3"], advances=["DEC-01"],
       proposed_tickets=["DEC-05 wedge and venue"], uzair_actions=["decide"], approval="yes")

bundle("AB-17", "Paper skeleton and pre-registration", "wedge", ["AB-16"], ("2026-11-10", "2026-11-21"), "Claude", NONE,
       ["claims list, figure plan, and the predictions for every remaining run hashed into a manifest before the runs"],
       ["none"], ["manifest committed before any held-out run"], ["skeleton", "manifest"],
       ["docs/paper/skeleton.md", "manifests/evidence/paper_prereg_<date>.sha256"], ["L1", "L2", "L3", "L4", "L5"],
       advances=["EXT-04"], proposed_tickets=["AUD-47 paper skeleton"])

CRITERIA = {
    "L1": "Layout and engine channels: on two public scoreboards, controlled re-scoring moves at least one published method by >= 0.05 "
          "F1 or changes a top-10 rank. Status 12 Oct: met on one board (PC -0.07 / +0.07 by column order; authors' rule +0.2 for FCI; "
          "the agent's PC copy wrong on 36% of perfect-information problems).",
    "L2": "Name reliance across the field: >= 3 of >= 5 LLM-using systems lose >= 0.10 directed F1 from real to swapped names with "
          "shuffled columns, and a rho curve shows the dose response. Status: one system measured (Causal-Copilot 0.306 -> 0.142).",
    "L3": "Decision value: on >= 2 benchmarks with interventions, most methods are within 0.05 of 'nothing moves' while the identifiable "
          "ceiling is >= 0.15 above the best. Status: met on CausalArena semantic and formula (12 Oct).",
    "L4": "A constructive system: never below its data-only output on held-out data, bounded harm under swapped names, and "
          "decision-value precision at stated coverage >= 0.05 above the best reproduced method with calibration error <= 0.05, on "
          ">= 2 benchmarks. Status: format and verifier only.",
    "L5": "Theory that explains the measurements: the F1 = S x a identity and error budget, bounded harm, order dependence of conflict "
          "rules, the decision-value ceiling. Status: identity checked numerically; rest to write.",
    "C1": "Demand evidence: practitioners name decisions where provenance and abstention matter (interviews if any, teardown, "
          "public demand evidence labelled indirect).",
    "C2": "One vertical where order knowledge plus abstention measurably beats learned graphs (RCA probe).",
    "C3": "A regulatory or standards hook that rewards the ledger's guarantees (map, venue).",
}

CLOSES = {"AB-01": ["AUD-33"], "AB-02": ["AUD-34"], "AB-03": ["AUD-35"], "AB-04": ["AUD-36"], "AB-05": ["AUD-37"],
          "AB-06": ["AUD-38"], "AB-07": ["AUD-48"], "AB-08": ["AUD-39"], "AB-09": ["AUD-40"], "AB-10": ["AUD-41"],
          "AB-11": ["AUD-42"], "AB-12": ["AUD-43"], "AB-13": ["AUD-44"], "AB-14": ["AUD-45"], "AB-15": ["AUD-46"],
          "AB-16": ["DEC-05"], "AB-17": ["AUD-47"]}
for _b in B:
    _b["closes"] = CLOSES[_b["id"]]
    if _b["id"] == "AB-07":
        _b["proposed_tickets"] = ["AUD-48 knowledge elicitation run (A3)"]
        _b["gates"] = ["DEC-02 approved (done 2026-10-12)"] + [g for g in _b["gates"] if not g.startswith("DEC-02")]
    if _b["id"] == "AB-05":
        _b["approval_needed"] = "approved 2026-10-12 ($5 cap)"
    if _b["id"] == "AB-07":
        _b["approval_needed"] = "approved 2026-10-12 (DEC-02)"

dag = {"plan": "Audit program DAG: research landscape, commercial landscape, wedge and paper", "version": 2, "drafted": "2026-10-12",
       "amendments": [{"date": "2026-10-13", "record": "docs/decisions/2026-10-13_interviews_not_gating.md", "note": "AB-14 finished on 13 Oct, ahead of its plan window",
                       "change": "AB-14 and AB-16 no longer wait on AB-10 interviews; AB-14 widened to a market map and three verticals"}],
       "status": "approved by Uzair 2026-10-12 (docs/decisions/2026-10-12_audit_dag.md)", "relation_to_q1": "runs alongside plans/q1_dag.json; BND-12's second-model part "
       "moves into AB-06; AB-07 is DEC-02 (A3); AB-16 feeds DEC-01",
       "scope": {"audit_program": sorted(t for v in CLOSES.values() for t in v), "outside_bundles": []},
       "scope_note": "each bundle closes exactly one ticket (AUD-33..48, DEC-05), issued on approval 2026-10-12",
       "landmark_criteria": CRITERIA,
       "kill_criteria": ["if P9 is refuted (no agent loses >= 0.10 with swapped names), drop L2 as a headline and lead with L1 + L3",
                         "if P6 is refuted on a second benchmark (most methods clearly beat 'nothing moves'), L3 becomes a CausalArena-specific note",
                         "if no interviewee values provenance or abstention (P13 refuted), the product angle is shelved; the paper stands on L1-L3"],
       "bundles": B, "milestones": [
           {"id": "AM-1", "title": "Controlled scoreboard and decision value published internally", "date": "2026-10-28", "requires": ["AB-01", "AB-04"]},
           {"id": "AM-2", "title": "Wedge decision", "date": "2026-11-14", "requires": ["AB-16"]},
           {"id": "AM-3", "title": "Paper skeleton and pre-registration", "date": "2026-11-21", "requires": ["AB-17"]}]}

if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "audit_dag.json"
    json.dump(dag, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote %s: %d bundles" % (out, len(B)))
