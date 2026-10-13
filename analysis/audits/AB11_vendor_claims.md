# AB-11: Vendor and library teardown. What the documentation claims about outputs and guarantees

Tickets: AUD-42, STR-06, CAP-09
Written 2026-10-12 by an audit agent. All sources were read on that date.

## Where we are now

AU5 typed 42 commercial rows by business model and headline claim. AU6 typed engines by code and maintenance. Neither asked the question the claim ledger (`ledger/DESIGN.md`) needs answered: **for each tool, does its output record why a direction was chosen, can its knowledge interface create a connection, and would it pass V2, V3, V5 and V7?** This audit answers that from documentation.

It covers 33 rows: 16 closed and 17 open. The full typed records are in `AB11_vendor_claims.json`.

Labelling rules:
- Every field is a **documented claim**, or a fact carried over from AU5/AU6 and labelled as such. Nothing here was measured.
- The `would_pass` answers are **my inference** from those claims.
- No code was run.

## Method

- **Sources.** 20 web searches and about 60 fetches, all with WebSearch/WebFetch. I preferred vendors' own docs, API references, pricing pages, GitHub READMEs and, once, a source module on ReadTheDocs (CausalNex 0.4.2).
- **Reuse.** Where AU5 or AU6 already held a fact (prices, licences, code-reading results), I reused it with a pointer instead of re-fetching.
- **Ledger checks applied (DESIGN.md section 3):**
  - V2: every claim cites existing evidence.
  - V3: the final skeleton equals the data-only skeleton, so knowledge never connects.
  - V5: every knowledge statement is either used or listed as overridden, with a reason.
  - V7: the report carries a permutation check that passed.
- **How I applied V7.** It is a reporting requirement. A tool can be order-independent by construction and still fail V7 if it reports no check. I note where an option exists.
- **Tools without graphs.** For effect-estimation and MMM tools (EconML, CausalML, Recast, Haus and others), V3 and V7 have no data-only graph to test, so I mark them "unknown: not applicable".

## Teardown table

Key: **K adds?** = can declared knowledge create a connection the data did not support. Y = yes, N = no, ? = unknown. All V-columns are inference.

| Tool | Kind | Provenance of directions (documented) | K adds? | Uncertainty | Order invariance | V2 | V3 | V5 | V7 |
|---|---|---|---|---|---|---|---|---|---|
| causaLens decisionOS | closed | Not stated; an LLM suggests directions "with accompanying explanations" | Y (required edges "know exist") | not stated | not stated | ? | N | ? | N |
| Causely | closed | Not per edge; BN from a "built-in library of causal knowledge" plus learned dependencies | Y (library is the model) | edge probabilities; "high-confidence" wording; no calibration | not stated | ? | N | ? | N |
| Datadog Watchdog RCA | closed | Not stated ("identifies interdependencies") | ? (no K channel) | none | not stated | ? | ? | ? | N |
| Datadog Bits AI SRE | closed | Per **hypothesis**, not per edge: step log and hypothesis tree; "evidence-backed" or "inconclusive" | n/a | none (abstains as "inconclusive") | not stated | ? | ? | ? | N |
| Dynatrace Davis | closed | Not per edge; Smartscape topology is the causal graph | Y (custom topology rules) | none | not stated | ? | N | ? | N |
| Microsoft (Azure RAI causal; Fabric) | closed | n/a (no graph; DML effects); no causal feature found for Fabric | n/a (all declared) | CIs (method property) | n/a | N | N | ? | ? |
| Amazon (CloudWatch inv.; DevOps Agent) | closed | Per **hypothesis**: user accept/discard plus CloudTrail log of every action | n/a | none | not stated | ? | ? | ? | N |
| Geminos CauseWay | closed | Not stated; models built from expert workshops and an LLM co-pilot | Y | cause probabilities (rail case) | not stated | ? | N | ? | N |
| Xplain Data XCD | closed | Not stated | ? | not stated | not stated | ? | ? | ? | N |
| Howso | closed | Mechanism stated (entropy asymmetry); no per-edge record | ? | per-feature MAE | not stated | ? | ? | ? | N |
| Aitia REFS | closed | Not stated | ? | not stated | not stated | ? | ? | ? | N |
| Lifesight | closed | n/a (MMM and geo-lift); MCP queries audit-logged (AU5) | n/a | not stated | n/a | ? | ? | ? | ? |
| Recast | closed | n/a (MMM); lift results "feed back" into MMM | n/a | Bayesian; intervals not described | n/a | ? | ? | ? | ? |
| Mutinex | closed | n/a | n/a | not stated | n/a | ? | ? | ? | ? |
| Haus | closed | n/a (experiments plus MMM) | n/a | "Confidence Interval" shown | n/a | ? | ? | ? | ? |
| Unlearn.AI | closed | n/a (randomised design) | n/a | power figures; PROCOVA unbiased (AU5) | n/a | ? | ? | ? | ? |
| DoWhy | open | None: edges are inputs; `falsify_graph` can suggest removals | Y (graph is all K) | LMC p-values vs node permutations | no check | N | N | ? | N |
| dodiscover | open | Not stated | ? (Context applied in skeleton phase, AU6) | not stated | not stated | N | ? | ? | N |
| causal-learn | open | Not recorded (`uc_rule`/`uc_priority` set policy only) | ? (docs: "Add prior edges"; issues: ignored) | none (PC) | `stable=True` default | N | ? | N | N |
| PyWhy-LLM | open | LLM (and CauseNet retrieval) is the only source | Y | none | not stated | N | N | ? | N |
| **Tetrad** | open | **Partial**: `verbose` prints "CI-test and orientation decisions" as text; `getChangedEdges` without the rule | Y (required "must appear if compatible") | bootstrap edge and orientation-type frequencies; seedable | `stableFas` option | N | N | ? | N |
| py-tetrad | open | as Tetrad | Y | as Tetrad | as Tetrad | N | N | ? | N |
| causal-cmd | open | Run log plus result in one `.txt`; no per-edge reason | Y (`requiredirect`) | bootstrap options; `seed` | none in listing | N | N | ? | N |
| pgmpy | open | Not recorded; ExpertInLoop LLM orientation not marked in output | Y with `enforce_expert_knowledge=True` | none (PC) | `variant='stable'` default | N | N | N (warns, then ignores) | N |
| bnlearn | open | Not recorded (`debug` output unspecified) | Y (whitelist "always included") | `boot.strength`: frequency, plus direction given presence | `pc.stable` available | N | N | Y | N |
| pcalg | open | Not recorded (`verbose` unspecified) | Y (`fixedEdges` "guaranteed to be present") | none | **stable + conservative/maj.rule + solve.confl: "fully order-independent"** | N | N | Y (fixed sets) | N |
| gCastle | open | Not recorded | ? | none | default PC order-dependent (AU6) | N | ? | ? | N |
| **CausalNex** | open | **Yes, coarse: required edge attribute `origin` ∈ {unknown, learned, expert}** | Y (post-hoc `add_edge`) | none (weights thresholded) | not stated | N | N | ? | N |
| Causal-Copilot | open | Not stated; the LLM prunes and re-directs edges | Y (project measurement) | "bootstrap edge-uncertainty checks" | fork order-dependent (AU6) | N | N | N | N |
| CausalML | open | n/a (CATE) | n/a | not stated on page | n/a | ? | ? | ? | ? |
| EconML | open | n/a (structure declared) | n/a | CIs: OLS, bootstrap, BLB | n/a | ? | ? | ? | ? |
| cdt | open | Not stated | ? | not stated | not stated | N | ? | ? | N |
| **Tigramite** | open | **Partial, by mark**: `x-x` = rules conflicted, `o-o` = undecided | Y (`-->` link "must exist") | p-values for adjacencies, not directions | **PCMCI+ "fully order independent" with majority/conservative + conflict_resolution** | N | N | Y | N |

### Counts (my tally of the table)

- **V2 evidence closure.** 0 of 33 pass. Partial records exist:
  - pgmpy `separating_sets_`, and sepsets in pcalg and causal-learn, cover non-adjacencies only.
  - The Tetrad verbose log is free text.
  - Datadog Bits and CloudWatch log their investigation steps, for root-cause hypotheses rather than edges.
- **V3 knowledge never connects.**
  - 0 pass and 16 fail; the other 17 are unknown or not applicable.
  - Every mainstream knowledge interface can create an adjacency: Tetrad required edges, causal-cmd `requiredirect`, pcalg `fixedEdges`, bnlearn whitelist, Tigramite `-->`, pgmpy with enforcement on, causaLens required edges, and CausalNex post-hoc edges.
  - Tabu-only use of CausalNex, pgmpy with enforcement off, and bnlearn whitelists that name both directions (adjacency forced, direction left to the data) behave differently. The first two cannot add; the last still forces adjacency.
- **V5 knowledge honoured.** 3 pass (bnlearn, pcalg fixed sets, Tigramite). In all three, constraints are hard: they are always applied, or the call errors. 3 fail:
  - pgmpy ignores a conflict with only a warning;
  - causal-learn ignores knowledge silently (the issues cited in DESIGN.md);
  - Causal-Copilot's GPU PC path drops knowledge (AU6).
  - Tetrad's "enforced where compatible" leaves no override record; marked unknown.
- **V7 order invariance declared.** 0 pass. Four tools document an option that gives order independence by construction: pcalg, Tigramite PCMCI+, Tetrad `stableFas` (skeleton only), and the `stable` defaults in pgmpy and causal-learn (skeleton only). No tool reports a permutation check.

## Finding on P14: "no tool records a per-direction source"

**Verdict: refuted in the weak form, by CausalNex. It survives in the strong form.**

**CausalNex is the counterexample.**
- In CausalNex, every `StructureModel` edge has one required attribute, `origin`, which "describes how the edge was created". Its values are `unknown`, `learned` and `expert` (StructureModel API page).
- `from_pandas` writes `origin="learned"` on every learned edge (0.4.2 source, `notears.py`), and `edges_with_origin()` filters on it.
- Edges are directed, so this is a typed per-direction source.

**Why it is weak.**
1. It has three values. It cannot separate a v-structure from a Meek propagation, a functional-form asymmetry or an intervention, and it does not distinguish a person from a model.
2. It links to no evidence.
3. `add_edge` defaults to `unknown`. CausalNex's own tutorial adds domain-knowledge edges with `sm.add_edge(...)` and no origin, so in the documented workflow expert edges are labelled `unknown`. That is exactly the "absence absorbed by a default" failure that DESIGN.md prevents by making `none` a value and absence invalid.
4. CausalNex declared end of life on 2026-06-24 (AU6).

**The strong form still holds.** No tool read records a **typed, rule-level direction source linked to evidence** (data pattern, functional form, intervention, knowledge, none, plus a `licensed_by` rule). The nearest partial records are:
- **Tetrad.** `verbose` "print[s] detailed CI-test and orientation decisions" (free text, not stored on edges). `MeekRules.getChangedEdges` keeps the before/after of each edge but not the rule (javadoc 7.6.9).
- **Tigramite.** The `x-x` mark records that orientation rules conflicted and `o-o` that they could not decide. These are typed outcomes, not sources.
- **Commercial investigation agents (Datadog Bits, CloudWatch investigations, AWS DevOps Agent).** They log steps, hypotheses, evidence and human accept/discard decisions for root-cause claims, not for graph directions, and with no published claim-to-evidence schema.

**Action.** Restate P14 as P14′: "no maintained tool records a typed, rule-level, evidence-linked source for each direction." Cite CausalNex `origin` as prior art in DESIGN.md, section 1, row 1. That row currently says "every library", and that is no longer accurate.

## Other findings

1. **Knowledge interfaces are built to connect.**
   - The docs say so in plain terms: Tetrad required edges "must appear if compatible"; pcalg `fixedEdges` are "guaranteed to be present"; bnlearn whitelisted arcs are "always included"; Tigramite `-->` "must exist".
   - pgmpy is the only library documenting both modes (`enforce_expert_knowledge` True or False).
   - V3 is therefore not a property any of these tools aims for. It is the ledger's own position.
2. **Silent non-enforcement is documented, not just reported in issues.**
   - pgmpy ExpertKnowledge: on conflict, "the edge is ignored and a warning is raised".
   - Tetrad: knowledge is "enforced where compatible".
   - Neither writes an override record, which is the gap V5 fills.
3. **Order-independent options exist, but no one reports a check.**
   - pcalg (`stable` + `conservative`/`maj.rule` + `solve.confl`) and Tigramite PCMCI+ (`majority`/`conservative` + `conflict_resolution=True`) document full order independence.
   - Tetrad, pgmpy and causal-learn document stable skeletons only.
   - None emits a permutation result.
4. **Uncertainty is bootstrap frequency, explicitly not validation.**
   - Tetrad: "Bootstrapping does not validate assumptions". It reports edge and orientation-type frequencies.
   - bnlearn calls bootstrap strength "confidence" and adds direction-given-presence probabilities.
   - Tigramite's p-values cover adjacencies "not ... contemporaneous directionality".
   - No tool documents calibration.
5. **LLM contributions are not separable in any output read.**
   - pgmpy ExpertInLoop (default `gemini/gemini-1.5-flash`, cached) and causaLens (an LLM "offers directional causality suggestions") orient edges.
   - Geminos' co-pilot proposes structure. Causal-Copilot re-directs and prunes.
   - None documents marking LLM-sourced directions in the result.
   - pgmpy's orientation function can return `None`, meaning "no edge", so an LLM can delete a candidate edge there.
6. **Commercial RCA has provenance at the investigation level.**
   - Bits AI SRE either gives an "evidence-backed conclusion" or marks the case "inconclusive". This is the only documented abstention besides the AU5 cases.
   - CloudWatch logs every action in CloudTrail and records human accept/discard.
   - Causely mixes a built-in knowledge library with learned dependencies inside one Bayesian network, with no per-edge source. That is a direct ledger use case.
   - Dynatrace claims "deterministic, causation-based analysis" over topology, with no confidence on root causes.

## Pricing signals (for later market sizing)

All prices are vendor claims or second-hand. Per-investigation figures marked "arith." are my arithmetic from the vendor's own units.

**IT incident analysis / AIOps RCA**

| Vendor | Price point | Unit | Label |
|---|---|---|---|
| Causely | USD 2,000/month for up to 500 services; Enterprise custom | per account-month | claim (vendor), pricing page |
| Datadog Bits Investigation | USD 500 per 500 credits/month (annual); USD 1.30/credit on demand; ~6.5 credits per investigation, so about USD 6.50–8.45 (arith.) | per credit / investigation | claim (vendor) |
| Datadog Watchdog RCA | bundled with APM | — | AU5 |
| Dynatrace | Full-Stack USD 58/month per 8 GiB host, including automated RCA; Agentic Operations USD 0.10/AI unit, ~30 units per autonomous investigation (≈ USD 3.00) | per host-month; per investigation | claim (vendor), rate card |
| AWS DevOps Agent | USD 0.0083 per agent-second (≈ USD 29.88/agent-hour, arith.); credits included with Support plans (30–100% of the prior month's Support charge) | per agent-second | claim (vendor) |
| CloudWatch investigations | no per-investigation price; quota of 150 enhanced investigations per account per month | quota | read (primary) |
| PagerDuty AIOps (Probable Origin) | from USD 699/month, consumption-based | per month | claim (vendor); added as a buyer signal |
| causaLens decisionOS | ~GBP 240k per licence per year | per licence-year | AU5 (G-Cloud 14) |

**Marketing measurement / incrementality**

| Vendor | Price point | Unit | Label |
|---|---|---|---|
| Haus | median USD 150k/yr (range 132k–168k); redline ~USD 100k; no list price | ACV | second-hand (Vendr) |
| Recast | no list price; costbench median USD 6k/yr from 3 reports, which contradicts its own USD 5k–50k/month category band; GeoLift ~USD 100/month | ACV / month | second-hand, inconsistent |
| Lifesight | no price; one annual subscription priced by "maturity" | annual | read (primary) |
| Mutinex | no price (demo only) | — | read (primary) |
| Meridian / Robyn | free, open source (price floor) | — | AU5 |
| Haus funding | USD 20M raise (investor signal) | — | AU5 |
| EMARKETER/TransUnion survey | 46.9% plan more MMM spend; 52% run incrementality tests | survey | second-hand, AU5 |

What the two verticals look like:
- **AIOps RCA is publicly priced per unit of investigation.** The documented range is about USD 3 to USD 8.45 per autonomous investigation, plus flat platform fees (Causely USD 24k/yr list; PagerDuty from USD 8.4k/yr).
- **Marketing measurement hides prices.** The only usable anchor is Haus at about USD 150k ACV, from a second-hand source with an unstated sample size.

## What this changes

1. **P14 becomes P14′.** Update DESIGN.md section 1, row 1: replace "every library" with "every library read except CausalNex's three-valued `origin`, which has no rule or evidence link and defaults to `unknown`". The novelty claim is now the rule-level, evidence-linked, typed source, plus the rule that absence is invalid.
2. **Reading causal-cmd knowledge files (DESIGN.md section 5) needs a mapping rule for `requiredirect`.**
   - In Tetrad, a required edge creates adjacency. In the ledger it may only orient.
   - When the import meets a required edge on a pair the data-only skeleton left unconnected, it must write an `overrides` entry with the reason "data left pair unconnected", not a claim.
   - Add a verifier test for this case, so that V3 and V5 are exercised by real Tetrad knowledge files.
3. **Use the documented order-independent settings as the default engine configuration, and still run the permutation check.**
   - Settings: pcalg-equivalent `stable` + `conservative`/`maj.rule` + `solve.confl` semantics, and PCMCI+ `majority` + `conflict_resolution=True` for time series.
   - V7's novelty is reporting the check, not achieving invariance.
4. **Keep `confidence` split into frequency and calibration (already in DESIGN.md).**
   - Tetrad and bnlearn give direction-given-presence frequencies we can import as `confidence.bootstrap_frequency`.
   - No tool supplies a calibrated value, so `calibration set id` stays our contribution.
5. **Product angle 2 in AU5 (an SRE provenance layer) gets sharper.**
   - Datadog Bits and AWS already log steps and allow abstention, so "a log exists" is not a differentiator.
   - The differentiator is a typed per-claim source (topology K vs telemetry D vs rollback or feature-flag I) and a check that K never creates a link the telemetry did not support.
   - Causely's knowledge-library-plus-learned Bayesian network is the clearest commercial instance of mixed D/K without per-edge source.
6. **Price anchors for STR-06 sizing.**
   - Use about USD 3–8.45 per investigation and USD 24k/yr flat platform fees for AIOps.
   - Do not size marketing from Recast's costbench figure (it is internally inconsistent). Use Haus's ~USD 150k ACV as a single, labelled second-hand point.
7. **Name-swap and LLM-separability audits (AUD-22).** The tools to add are pgmpy ExpertInLoop (cheap, MIT, cached LLM orientation, default Gemini) and causaLens' LLM suggestions (closed). Both orient edges with an LLM, and neither documents marking those edges.

## Not read

| Source | Reason |
|---|---|
| cmu-phil.github.io/tetrad/manual/ and cmu.edu Tetrad manual | fetch errors; ReadTheDocs manual sources (`.md.txt`) read instead |
| Tetrad bootstrapping HTML page | body not returned; `.md.txt` source read |
| gCastle GitHub tree | robots disallowed; PyPI page and AU6 code reading used |
| getrecast.com/pricing | fetch error; homepage and costbench used |
| CausalNex latest `notears` source module | fetch error; 0.4.2 module read, so `origin="learned"` is confirmed for 0.4.2 only |
| EconML spec overview | navigation only; GitHub README used |
| Datadog pricing page beyond 100k characters | truncated; Watchdog tier not confirmed |
| causal-cmd GitHub README | lacked details; docs site read |
| Datadog Bits "Knowledge sources" page; CloudWatch hypothesis-visualisation page; Aitia "Our Science"; Geminos PathWay; Howso GitHub licence; Tigramite `run_bootstrap_of` API; py-tetrad README | not opened |
| pcalg `verbose` and bnlearn `debug` output content | not documented; would need a run, which is out of scope for a desk audit |
| causal-learn #219/#171/#266, DoWhy #1695, Tetrad #1954 | cited from DESIGN.md, not re-read |
| causaLens G-Cloud 14 listing | AU5 figure reused, not re-read |

## Searches run (20, all 2026-10-12)

The exact strings are in `AB11_vendor_claims.json` under `searches`. They covered:
- CausalNex origin
- Tetrad MeekRules logging and the Tetrad manual
- Datadog Watchdog and Bits AI SRE
- pgmpy ExpertKnowledge (×2)
- Causely docs (×3)
- AWS CloudWatch investigations and DevOps Agent
- Dynatrace Davis
- causaLens decisionOS
- Geminos
- Xplain Data
- Howso (×2)
- Recast pricing
- Microsoft Fabric causal features
- Haus funding

## Where we're going

- Patch DESIGN.md (P14′ wording; the `requiredirect` import rule) and add one verifier test for "required edge on a data-unconnected pair". This is a small edit for the builder workstream.
- Run AU11 under the documented order-independent settings, so the V7 permutation check has an "invariant by construction" control arm.
- If the shared budget allows, open the pages not read above, especially Tigramite bootstrap and the Datadog knowledge-sources page, to settle the remaining V5 "unknown"s.

## Hands-on results (2026-10-12)

Everything in this section was **measured**: each tool was installed, run and probed, and nothing here is inferred from documentation. Code: `analysis/ab11_teardown_run.py` (one command), `analysis/ab11_ledger_adapters.py`, `tests/test_ab11_adapters.py`. Results: `analysis/results/teardown/teardown.json`, `CONTRACT.json`, `raw/<tool>/` (saved output objects, worker logs) and `ledgers/<tool>__<regime>.json`.

### Setup

- **File.** One public CausalArena file: `semantic_cybersecurity_and_it_operations_api_rate_limit_abuse_spillover`, obs only, rep000. It has 25 variables, 1,000 rows and 67 true edges. Data sha256 `ebd592cc…`.
- **Column order.** Columns were always shuffled with `perm = default_rng(seed + crc32(file name))`, the same rule as the AB-05 probe and the baseline runner. The main order uses seed 20261010. For the order check (an empirical V7), each tool also ran on seeds 1 and 2.
- **Settings.** CI-based tools all used alpha 0.05, so that differences reflect behaviour rather than settings. Every tool was run single-threaded under `nice`, and the teardown used about 10 CPU-minutes in total.
- **Knowledge tests.** These ran on the main order, through each tool's documented interface. Each statement was chosen from that tool's own data-only output:
  - (i) **Required edge.** The first true edge the data-only run left unconnected. For most tools this was `legit_burst_attempts_min -> throttled_write_429`.
  - (ii) **Forbidden edge.** The first arrow the data-only run committed, in index order.
  - (iii) **Tiers.** Tier 0 is columns 0–11, which are all exogenous in the truth; tier 1 is columns 12–24.
- **Ledgers.**
  - Built only from what each tool exposes. Evidence records are created only from exposed separating sets and test results.
  - `direction_source` is `none` unless the tool's output itself states why an arrow is there.
  - `verify.py` was run unchanged. It stops after V1, so when V1 fails the other checks are `na`.
  - A diagnostic rerun with V1's `minItems` lifted shows what V2–V8 would say. V2 is counted as failed if any claim cites no evidence.
  - Scope of each check: V3 and V5 are read from the D+K ledgers; V7 and V8 from the D ledger. V4 is `na` because there is no interventional data.
- **No LLM calls.** PyWhy-LLM ran only through the AB-05 probe's `--stub` (an offline fake LLM whose answers are seeded by the prompt's hash), so its graph and scores measure the stub, not the library.

Versions: causal-learn 0.1.4.8 with DoWhy 0.12; pgmpy 1.1.2; CausalNex 0.12.2 (CPython 3.10, see Packaging); dodiscover git 6e64456; tigramite 5.2.10.1; gCastle 1.0.4 (torch stub); lingam 1.12.2; py-tetrad 0.1.2 (git 43271a2), which bundles Tetrad 7.6.11-SNAPSHOT; PyWhy-LLM source 66f2d59 (stub).

### Knowledge calls used (the code that ran)

| Tool | Required a->b | Forbidden a->b | Tiers |
|---|---|---|---|
| causal-learn (DoWhy row) | `BackgroundKnowledge().add_required_by_node(GraphNode(a), GraphNode(b))` | `add_forbidden_by_node` | `add_node_to_tier(node, t)` |
| pgmpy PC / HillClimb | `ExpertKnowledge(required_edges=[(a,b)])`, PC with `enforce_expert_knowledge` False (default) and True | `ExpertKnowledge(forbidden_edges=[(a,b)])` | `ExpertKnowledge(temporal_order=[t0, t1])` |
| CausalNex | no in-search interface; `sm.add_edge(a, b, origin="expert")` after `from_pandas` | `from_pandas(..., tabu_edges=[(a,b)])` | none; every later→earlier pair as `tabu_edges` |
| dodiscover | `make_context().included_edges(nx.Graph([(a,b)]))` (also tried as `nx.DiGraph`) | `.excluded_edges(nx.Graph([(a,b)]))` (also as `DiGraph`) | none |
| Tigramite | `link_assumptions[b][(a,0)]='-->'`, `[a][(b,0)]='<--'`, all others `'o?o'` | `[b][(a,0)]='<?-'`, `[a][(b,0)]='-?>'` | `'-?>'` from tier 0 to tier 1 |
| gCastle | `PrioriKnowledge(d).add_required_edges([(a,b)])` | `add_forbidden_edges` | none; later→earlier as forbidden edges |
| LiNGAM | `prior_knowledge[b,a]=1` (a path a→b) | `prior_knowledge[b,a]=0` (no path a→b) | `pk[early, late]=0` |
| Tetrad (py-tetrad) | `Knowledge.setRequired(a,b)`; `Pc.setKnowledge` | `setForbidden(a,b)` | `addToTier(t, n)` |

### Observed behaviour against the desk inference

Key:
- **adj ±** = adjacencies the knowledge run added or removed compared with the data-only skeleton.
- **verify.py** = the official result for V1–V8 (p pass, f fail, n na).
- **relaxed** = the diagnostic rerun with V1 lifted.
- **Desk** = the `would_pass` column for V3/V5/V7 from the table above.

| Tool | (i) Required on unconnected pair (V3) | (ii) Forbidden on found arrow (V5) | (iii) Tiers | Same graph over 3 orders (V7) | verify.py V1–V8 | relaxed V1–V8 | Desk V3/V5/V7 | Disagreement |
|---|---|---|---|---|---|---|---|---|
| DoWhy + causal-learn | **dropped silently**: no connection, no warning (adj +0/−0) | honoured: arrow reversed | honoured (adj +0/−0) | **no**: skeleton stable, 11–13 arrows flip (`stable=True`) | f n n n n n n n | p f p n f p f p | ?/N/N | V3: causal-learn cannot connect, but only because it discards the statement without a trace, so V5 fails silently. DoWhy accepted the CPDAG as a cyclic DiGraph, and its `identify_effect` then crashed on networkx 3.6 |
| pgmpy PC, default | ignored, with a logged warning (no connection) | **ignored**, with a warning: arrow kept | orientation honoured, but **adj +43/−1 (13 true, 30 false)** | yes | f n n n n n n n | p f f n f p p p | N/N/N | Desk said V3 was "yes-like" with enforcement off. True for required edges, but **tiers create connections**: pgmpy restricts the candidate separating sets of (u, v) to tiers ≤ min(tier u, tier v), so a later-tier mediator can never separate an earlier-tier cause from a later-tier effect |
| pgmpy PC, `enforce=True` | **connection added** (and one other true adjacency lost) | adjacency deleted | — | — | (in row above) | | | Matches the documented semantics |
| pgmpy HillClimb | **connection added** (adj +6/−7) | adjacency deleted (adj −3) | honoured; adj +19/−27 | yes | f n n n n n n n | p f f n f p p p | (pgmpy) N/N/N | Agrees. Every statement re-routes the greedy search |
| CausalNex | **connection added** (post-hoc `add_edge`, the only way) | honoured (tabu); re-learning moved 20 adjacencies | honoured (emulated); adj +6/−35 | yes | f n n n n n n n | p f f n f p p p | N/?/N | V5: the `origin="expert"` edge lets the ledger cite the statement, so **the required-edge ledger passes V5, the only one that does**. Tabu statements leave no trace and fail V5. `add_edge` without `origin` (the tutorial's form) gives `unknown`, confirmed |
| dodiscover | **connection added** with `nx.Graph` (unoriented; adj +1/−3). As a `DiGraph`, accepted and silently no effect | **ignored silently**, as Graph and as DiGraph: arrow kept, no warning | no interface | **no**: the skeleton itself changes (19 → 11 → 12 adjacencies) | f n n n n n n n | p f f n f p f p | ?/?/N | V3 and V5 resolved: knowledge connects, and exclusions are silently ignored. It is the most order-dependent tool tested |
| Tigramite PCMCI+ τ=0 | **connection added** by `'-->'` (adj +1/−1) | honoured: reversed | honoured (adj +0/−0) | yes (as documented) | **p p f n f p p p** | p p f n f p p p | N/Y/N | V2: `p_matrix` and `sepsets` cover every pair, so V1/V2 pass. V5: behaviour is honoured, but the output never says which link an assumption fixed, so **the ledger fails V5**. Desk "yes" holds for behaviour, not provenance |
| gCastle PC parallel | **connection added** | honoured: reversed | honoured (emulated) | **no**: skeleton stable, 6–10 arrows flip | f n n n n n n n | p f f n f p f p | ?/?/N | V3 resolved: knowledge connects. Separating sets are computed but not kept on the object |
| LiNGAM (DirectLiNGAM) | **connection added**; one path statement moved 54 adjacencies (+24/−30) | honoured: reversed; adj +20/−12 | honoured; adj +36/−36 | yes | f n n n n n n n | p f f n f p p p | no desk row | Prior knowledge works on paths, so every statement re-runs the whole ordering |
| Tetrad PC (py-tetrad) | **connection added** | honoured: reversed (one other adjacency added) | honoured (adj +0/−0) | **no**: seed 2 flips 5–6 arrows, skeleton stable (`fasStable`) | f n n n n n n n | p f f n f p f p | N/?/N | **V2.** With `setVerbose(true)`, Tetrad prints to `System.out` (not `setLogStream`) 259 `Independence accepted: a _\|\|_ b \| S  p = …` lines and 39 `Collider oriented: a -> b <- c` lines. Parsed, these give **typed, evidence-linked `v_structure` sources for all 37 arrows**. V1 fails only on the 4 undirected claims, because dependence tests are not logged |
| PyWhy-LLM (stub) | n/a: no knowledge input (the library is the supplier) | n/a | n/a | no (stub answers change with prompt wording) | f n n n n n n n | p f f n p p f n | N/?/N | Agrees. Every connection comes from the model; with the data-only relation recorded as `none`, V3 fails on the whole skeleton |

### Counts

- **V3 (knowledge never connects), observed.**
  - A required edge created a connection in **7 of the 9 data tools** with their default settings, and in 8 counting pgmpy's `enforce_expert_knowledge=True`.
  - In the other two cases no connection was created: causal-learn discards the statement silently, and pgmpy's default mode refuses it with a warning.
  - **Tiers created connections in pgmpy PC (+43).** In LiNGAM, HillClimb and CausalNex, every kind of statement re-shaped the skeleton (re-learned search).
- **V5 (knowledge honoured), behaviour.**
  - Silently ignored: causal-learn (required edge), and dodiscover (excluded edges in both forms; included edges as a DiGraph).
  - Ignored with a log warning only: pgmpy, default mode.
  - Applied: the rest.
- **V5 in the ledger.** It **fails for every tool** except CausalNex's `origin="expert"` required edge, because no other output links a statement to the claim it changed.
- **V7 (order invariance), observed.**
  - Invariant over 3 orders: pgmpy PC (`stable`), pgmpy HillClimb, Tigramite, LiNGAM, CausalNex.
  - Not invariant: causal-learn (`stable=True`), gCastle `parallel`, Tetrad (`fasStable`), dodiscover. For the first three the orientations change; for dodiscover the skeleton changes too.
  - "Stable" skeleton options do not give order-invariant orientations.
  - No tool reports a check, so the official V7 is never met by the tool itself. The adapter writes the permutation result.
- **verify.py.**
  - Only Tigramite's D ledger passes V1–V8.
  - Every other tool fails V1 because some claim has no exposed evidence. That is 300 of 300 claims for gCastle, LiNGAM, CausalNex, HillClimb and PyWhy-LLM; 41 for causal-learn and pgmpy PC (separating sets cover non-adjacencies only); 19 for dodiscover; 4 for Tetrad.

### Decision value and F1 (data-only run, main order)

DV-1 uses `decision_value_v2.claims` with every variable as a target (600 pairs). On this file the empty graph ("nothing moves") is right on 70.8% of pairs. F1 is directed-edge F1, with undecided pairs oriented by the random rule (CausalArena's stated rule, seeded with the file's crc32).

| Tool | Arrows / undecided | DV-1 precision | Coverage | Lift over empty | F1 (random) | F1 (drop undecided) |
|---|---|---|---|---|---|---|
| Tigramite | 23 / 18 (`x-x`) | **0.820** | 0.352 | **+0.112** | 0.444 | 0.333 |
| pgmpy PC | 37 / 4 | 0.719 | 0.937 | +0.011 | **0.481** | 0.423 |
| causal-learn | 39 / 2 | 0.692 | 0.980 | −0.016 | 0.407 | 0.396 |
| dodiscover | 17 / 2 | 0.690 | 0.993 | −0.019 | 0.046 | 0.024 |
| Tetrad | 37 / 4 | 0.686 | 0.845 | −0.022 | 0.426 | 0.365 |
| gCastle | 41 / 0 | 0.677 | 1.000 | −0.032 | 0.407 | 0.407 |
| pgmpy HillClimb | 97 / 2 | 0.650 | 0.990 | −0.059 | 0.349 | 0.329 |
| LiNGAM | 109 / 0 | 0.520 | 1.000 | −0.188 | 0.261 | 0.261 |
| CausalNex NOTEARS (w ≥ 0.3) | 69 / 0 | 0.448 | 1.000 | −0.260 | 0.118 | 0.118 |
| PyWhy-LLM (**stub**) | 102 / 0 | 0.262 | 1.000 | −0.447 | 0.142 | 0.142 |

- Only two tools beat doing nothing on this file.
- The best, Tigramite, does so by abstaining: its `x-x` conflict marks leave 65% of pairs undecided.
- This is a single file, so these numbers are a measurement and not a ranking.

### Updated P14 verdict

**Weak form ("no tool records a per-direction source"): refuted twice, now by measurement.**
1. **CausalNex `origin`**, confirmed in 0.12.2:
   - `from_pandas` labels every learned edge `learned` (69 of 69).
   - `add_edge(..., origin="expert")` gives `expert`.
   - The tutorial's `add_edge(a, b)` gives `unknown`.
   - The label is three-valued and links to no evidence.
2. **Tetrad's verbose output (new).** With `setVerbose(true)`:
   - Tetrad 7.6.11 prints `Collider oriented: a -> b <- c` for each collider orientation, plus `Independence accepted: a _||_ b | S  p = …` for each separation.
   - A short parser (in `ab11_teardown_run.py`) turns this into a typed, rule-level source (`v_structure`) that cites the CI test which licensed it.
   - That covered all 37 arrows in this file.

**Strong form ("no tool records a typed, rule-level, evidence-linked source for each direction"): survives, narrowed.**
- No tool stores such a source in its output object.
- Tetrad's comes closest, with these limits:
  - It is free text on `System.out` only (`setLogStream` received nothing).
  - It covers collider orientations only. Meek-rule and knowledge orientations are not logged.
  - Dependence tests are not logged, so adjacencies and undirected pairs still have no evidence.
- On a graph that needs Meek propagation, those arrows would have no source.
- Tigramite's typed marks (`x-x`, `o-o`) record outcomes, not sources: its D ledger passes every check with all 23 arrows sourced `none`.

**Restated P14′:** "No maintained tool stores a typed, rule-level, evidence-linked source for each direction. Tetrad prints one for collider orientations, as free text, when verbose; CausalNex stores a three-valued origin label without evidence."

### What this changes

1. **DESIGN.md section 1, row 1 (prior art).**
   - Add Tetrad's verbose collider log next to CausalNex `origin`.
   - The first engine adapter can be Tetrad-backed: the parser already yields `v_structure` claims with cited tests.
   - The ledger's added value is then four things: Meek-rule and knowledge sources; adjacency evidence (dependence tests); storage inside the record rather than the console; and the rule that absence is invalid.
2. **V3 needs a tier test, not only a required-edge test.** pgmpy shows correct tiers creating 30 false connections through a conditioning-set filter. Add an engine rule: tiers may restrict orientation only, never the conditioning sets used for adjacency. Add a verifier test in which a tier statement, not a required edge, changes the skeleton.
3. **V5 is a provenance property, not a behaviour property.**
   - Several tools apply statements correctly (Tigramite, Tetrad, gCastle) and still fail V5, because nothing links a statement to the claim it changed.
   - Silent drops are real and reproducible: causal-learn (required edge), dodiscover (`excluded_edges`; `included_edges` as DiGraph). Cite these as measured cases, not only issue reports.
4. **V7 needs an order-independent orientation rule as well as a stable skeleton.**
   - causal-learn, gCastle and Tetrad keep the skeleton but flip 5–13 arrows across 3 orders.
   - Use PCMCI+-style majority plus conflict marking (Tigramite: invariant here), and keep the permutation check in the report.
5. **Verifier and schema gaps found by running real outputs:**
   - (a) A ledger can pass V1–V8 with every arrow sourced `none` (Tigramite). Add a counted, declared check, "committed arrows without a source", so a pass cannot hide it.
   - (b) `RELATIONS` has no `y->x`, so a reversal between the data-only and final runs cannot be recorded. The adapter writes `x-y` plus `data_only_relation_exact`. Make claims ordered or add `y->x`.
   - (c) `verify.py` stops after V1, so one evidence-less claim hides V2–V8. Run every check and report V1 alongside.
6. **Packaging facts for AU8:**
   - CausalNex 0.12.2 declares `Requires-Python <3.11`, so it does not install on 3.11. On 3.10, pgmpy 0.1.19 pulls CUDA torch (a 5.6 GB venv).
   - DoWhy 0.12 (resolved beside numpy < 2) breaks on networkx 3.6.
   - cdt's discovery methods need R, which is absent, so cdt was not run.
   - py-tetrad installs from git in seconds with a bundled jar.

### Limits

- **One file, one replicate.** The knowledge statements were chosen from each tool's own output, so the edges differ between tools (listed in `teardown.json` under `knowledge_pick`).
- **Knowledge runs were not permuted.** V7 is measured on data-only runs only.
- **PyWhy-LLM numbers are the stub's.**
- **The Tetrad sources depend on a parser of free text,** which may break between Tetrad versions.
- **CausalNex NOTEARS threshold.** w ≥ 0.3 follows the reference implementation; the tutorial's 0.8 would keep 22 of the 69 edges.
