# Decision record: closing the audit chapter (2026-10-14)

Uzair, 14 Oct: "closing out everything else to end our auditing chapter here". The wedge itself is recorded in
`2026-10-14_wedge_decision.md`. This record covers what remained open around it.

| Item | Taken | Why |
|---|---|---|
| DLV-02 (BND-08): 6 S2 arms whose only gpt-4o run crashed at the cycle step | **criterion restated as "every arm has a recorded run that reached S3; crashes are counted as crashes"**; no rerun | Every arm reached S3. The crash is the system's own, measured in 18 of 19 live entries, so a rerun would most likely crash again (about $2.5). The analysis already scores S3 (pre-registered primary endpoint, BND-08) |
| BND-08, BND-10 | done | BND-08 closes with DLV-02. BND-10 was waiting only on BND-08 (rule W3) |
| AUD-13 (second model) | done | Causal-Copilot on gpt-4o-mini, 30 runs (RQ-17) |
| AB-06 tier B | not run | DEC-05 |
| AB-10 interviews (AUD-41) | carried forward, not closed | They still decide P13 and C1. They run whenever a chance arises and gate nothing |
| BND-12's remaining live parts (CARE control, LLM and fused Sachs numbers) | moved to the build (B3), not the audit | They test knowledge use, which B3 does under the ledger's controls |
| EXT-01, EXT-03, EXT-06 (notes to maintainers) | drafted, left to Uzair to send | `docs/drafts/bug_reports/` |
