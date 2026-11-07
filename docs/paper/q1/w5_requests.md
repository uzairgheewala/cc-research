# Requests from W1 (Q1 paper) to W5 (tickets, contract, site), 31 Oct 2026

Tickets: DLV-05, DLV-07, DLV-11, BND-13, BEN-13, PRG-01

1. **DLV-05 evidence and check.** Proposed closing evidence: `docs/paper/q1/report.tex`, `docs/paper/q1/build/report.pdf`,
   `docs/paper/q1/numbers.lock.json`, `docs/paper/q1/lit_claims.json`. Proposed checks: `lint_report.py` exits 0 and
   `build_numbers.py --check` exits 0. Close only after submission on Gradescope (Uzair).
2. **BND-13** still says "(2 Nov)" and pins only the skeleton; the skeleton was re-cut and BND-13 repinned (w1-01). Its due
   date move to 6 Nov is yours (s36 noted it).
3. **Program v3 section 2.3, item 1 wording.** It says CausalBench's "edge placement carries about 7-14% of the above-random
   score". In `analysis/reports/ben13_s1_s2.md` the 0.07-0.14 "placement share" is the part that choosing strongly
   perturbing *parents* alone earns (children rewired): P1 (>= 0.5) fails, so parent choice is not the shortcut. The
   paper instead cites P3 (MeanDifference reaches 0.90-0.95 of the test split's own total-effect ceiling) and the FOR
   result. Suggest rewording the program doc.
4. **Export allowlist (W2 owns it).** The paper's numbers also come from `analysis/results/ab06/ab06.json`,
   `analysis/results/rescore_v2/leaderboard_controlled.json`, `analysis/results/ben13/summary.json`,
   `analysis/results/reference_reliability/reliability.json`, `analysis/results/fork/bld06_cycles.json`,
   `plans/ab06_prereg.json`, `datasets/MAPPING.json`, `datasets/suite_b1/MAPPING.json`. The paper links them in cc-research
   (public); adding them and `docs/paper/q1/` to the Q1 repo would make the checkpoint self-contained there.
5. **refinement_r3 score contract.** `tests/test_core.py::ScoreContract` fails on `analysis/results/refinement_r3`
   (created 31 Oct 04:29-04:37, W3's folder).
6. **The template's bibliography style.** `docs/paper/q1/style/dsc180bibstyle.bst` is absent (the Overleaf project could
   be read but that file not copied byte-exactly); make.sh uses CTAN's econ.bst. Uzair can drop the template's file in
   from Overleaf's "Download source".
7. **Adopted checkpoint boundary, 3 Nov (organization stage 1).** Uzair selected **Crucis** and authorized freezing
   `CHECKPOINT_CONTRACT.md` / `checkpoint_contract.json`. The new `check_checkpoint_contract.py` checks 78 keys,
   13 numerical sources and 19 frozen files. Keep this check in the subsequent commit/CI workflow; do not add it
   to pinned shared policy files until the repository-separation stage reviews their changes. Preserve all current
   numerical source paths and the two external metadata files. The paper is not ported during extraction.
8. **Ownership/inventory for the split.** The active subsystem workstream retains ownership of current `audit/`
   files and `tests/test_audit_*`; this checkpoint freeze does not lock that work tree. Stage 2 must capture and
   recheck an owned-file inventory before moving it. The paper's `checkpoint_evidence/` snapshots survive moves.
9. **Publication scope and receipt reconciliation.** The public Q1 export currently reproduces the companion
   comparison; reconcile its README and broader paper evidence coverage before claiming full reproduction.
   The 31 Oct UTC prod digest was posted at `1793412937.228969` but remains draft-only locally. Preserve the
   actual edited message and record its receipt before regenerating the public feed; do not repost it.

Items 7–9 are coordination handoffs, not changes to ticket status or evidence pins. DLV-05 remains open until the
actual submission criterion is met. Known prose/citation corrections remain in HANDOFF §5.

10. **BND-08 M3 endpoint reconciliation (3 Nov structured review).** Independent
    source-code review found that `analysis/s2_analysis.py`'s pre-run header names
    S3, while the calculation reads `stability.py` N1 from completed final outputs.
    Its denominator includes only distinct scenario/directed-edge pairs adjacent
    in exactly one reference; classification is by adjacency, not correct direction.
    The paper now reports the counts descriptively and discloses the discrepancy.
    No source, threshold, count, endpoint or evidence pin was changed. Please route
    any protocol/implementation reconciliation to its owners under a separate
    reviewed authorization; do not repin merely to make this disappear.
11. **Checkpoint local build/review state.** Actual template bibliography obtained;
    source and 16-page inspected PDF/bundle are bound in
    `verify/research-workbench-review-2026-11-03.json`. Items 1/6 now have local
    validation evidence; submission and any remote publication remain separate.
    The companion still covers its scoped comparison, not whole-paper reproduction.
    Exact Gradescope deadline times and mentor-specific requirements need human
    verification after UCSD sign-in. No shared ticket/site/status changes made.

12. **6 Nov post-submission reader-route audit (DLV-05/DLV-07).** The author
    confirmed submitting the archived PDF; exact upload time/receipt remain
    unavailable. Please reconcile the research site's checkpoint-open/next-
    deliverable text with the confirmed report state after reviewing the additive
    status receipt. The framework site still describes execution/collection as
    in design, while its public default includes scoped S3/S4 implementations.
    Route that source/site change to the framework owner. The audit report and
    public observation receipts are in `audit/2026-11-06/`. Both homepages and all
    21 selected same-origin endpoints returned 200; content currency is separate.
    No public site, shared tracker, snapshot, Slack message or deployment was
    modified by the paper workstream. The stable framework full gate was
    incomplete and a bounded test probe timed out; preserve this qualification.

13. **Companion export disclosure (DLV-07).** Existing DLV-07 evidence pins
    cover `docs/q1_repo/README.md` and `tools/export_q1.py`; the staged gate
    rejected changes to both. Their exact bytes were restored without a repin.
    Review `audit/2026-11-06/companion-export-disclosure.patch` and its additive
    `docs/q1_repo/AI_USE.md` template before adopting an updated export contract.
    Deliberately repin through the owner process if adopted. The current code ZIP
    reads the reviewed companion commit directly and does not depend on rerunning
    the historical exporter or silently changing these pins.

14. **6 Nov follow-up for TEAM-11.** The author confirmed both checkpoint
    submissions. A reviewed landing-page patch uses the additive receipt to
    remove the checkpoint from the upcoming list and links the report, source,
    reproduction guide and AI disclosure. The local research site built with
    zero errors and warnings. The staged gate identified the existing TEAM-11
    pin on `site/pgs/pg_today.py`. Review this as a site-owner change and repin
    via the tracker workflow before deploying it. The scientific evidence pins
    and tracker statuses were excluded from the checkpoint audit milestone.

15. **TEAM-11 homepage repin.** The existing verifier regenerated TEAM-11's
    site evidence pins in an isolated checkout after the homepage patch review.
    The homepage digest changed. The other four TEAM-11 records changed only
    their pin timestamps. The TEAM-11 status record matched exactly.
    The generated pins and site sources are the owned changes. The isolated
    verifier's unrelated status results and log are local scratch outputs.
    The committed snapshot must pass its existing freshness check.
