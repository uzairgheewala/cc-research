# After-submission reproducibility and public communication audit

Tickets: DLV-05, DLV-06, DLV-07. Recorded 6 Nov 2026.

The [initial audit](audit/2026-11-06/REPORT.md) and
[follow-up](audit/2026-11-06/FOLLOWUP.md) record the work against this plan.

Start after Uzair confirms submission. First retain the actual submitted PDF hash,
code link, submission timestamp and receipt outside the automatically publishable
tree. Do not infer submission from a local build or a successful course-page visit.

The checkpoint archive is the comparison baseline. Inspect current instructions,
ownership and dirty/index state in each repository before doing any work. Preserve
active Crucis subsystem work. No automatic pushes, site publication, paid runs,
protocol changes or new raw/native campaigns are authorized by this audit plan.

## Order and acceptance evidence

1. **Reader route and identity.** Inspect `cc-research`, `crucis` and
   `causal-copilot-q1`, their READMEs, linked docs, GitHub defaults and both research
   and framework sites. List every paper-facing link with the destination, exact
   observed commit/version and what a reader can find there. Distinguish local,
   default-branch, deployed and submitted versions. Must show a navigable route
   from paper to framework, evidence, bounded reproduction and limitations.
2. **Full finding ledger.** Enumerate every displayed result, figure, table and
   substantive finding, including caveats and the combined argument. Map each to
   its registry key, reference/cohort, scoring rule, frozen source bytes, analysis
   command, software identity and required excluded inputs. Include qualitative
   claims and missing records; coverage is counted against this explicit inventory.
   Must show no unassigned finding, and no missing input disguised as reproduction.
3. **Reproduce in increasing cost order.** Recheck the frozen contract and all
   selectors/operations; independently recompute reportable findings from supplied
   snapshots; run the public companion command in isolation; then examine which
   analyses can be rerun from publicly obtainable raw records. Separate numeric
   readback, snapshot recomputation, analysis rerun, native execution and scientific
   validation. For every row, retain command, environment, hashes, outcome, expected
   tolerance, skipped/unavailable reason and actual access. Keep failures visible.
   Native/paid experiments needing approval become concrete proposals, not reruns.
4. **Scientific reconciliation.** Check same-graph scoring versus actual layout
   dependence; disjoint name-control cohorts, stages and scoring; paired completion
   selection and crash accounting; bootstrap versus model-review attribution;
   MATMCD point rule versus its interval; BND-08 specified versus computed endpoint;
   disputed references, licences and CausalBench test-informed reference. Verify
   latest implementation scope independently of historical empirical results.
   Must show each conclusion no stronger than its available evidence.
5. **Communication repair.** Propose focused README and documentation changes so
   readers know what each repository does, exact setup and commands, result scope,
   excluded data/access conditions, known failures, and what remains in development.
   The companion must not claim reproduction of the whole paper. Route tracker/site
   changes through their ownership process; inspect local site builds before any
   separately authorized publication. Must show clean-checkout instructions tested
   by execution where feasible, rather than copied from earlier prose.
6. **Review and handoff.** Produce a per-finding coverage matrix, link audit,
   reproduction receipts, discrepancies and justified dispositions. Review material
   changes and make local validated milestone commits in their owning repositories.
   Record what is public, local-only, unavailable or still awaiting a human decision.
   Complete coverage means every inventory row has an honest disposition; it does
   not mean every historical experiment can be natively reproduced.

The framework's broader validation and final empirical study remain separate
from this checkpoint audit. Treat website promises, software conformance, retained
run compatibility and scientific validity as different claims with different tests.
