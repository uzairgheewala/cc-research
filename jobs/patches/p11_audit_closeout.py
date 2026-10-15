"""2026-10-14, audit close-out pass: AB-05 closed (P8 supported; live calibration), AB-06 Causal-Copilot second-model arm
scored, AB-06 grid re-planned from live numbers and pre-registered (tier A), AB-16 wedge decision pack and approach v1
written for DEC-05. New: EXT-06 (Vashishtha et al. truncation note), INF-08 (EIO on the bind mount). Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p10" in c, "apply p10 first"
assert "# ---- overrides p11" not in c, "already applied"
block = r'''
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
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p11 applied")
