"""2026-10-14: AB-06 tier A resumed: 19 of 80 ok, then 61 runs refused by the provider for lack of credits (HTTP 429
insufficient_quota), recorded as agent failures. Amendment 2 (operational): quota refusals are resumable infrastructure
stops and halt the batch. New INF-09. Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p14" in c, "apply p14 first"
assert "# ---- overrides p15" not in c, "already applied"
block = r'''
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
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p15 applied")
