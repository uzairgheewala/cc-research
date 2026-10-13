# Program v2: order provenance

Proposal, written 2026-10-07 after bundle 1 closed, for Uzair's decision. It replaces the bundle 2-5 plan (`bundle2_onward_design.md`) as the organising plan; parts of that plan survive as components and are marked. Nothing here has been built unless it says "done". Evidence it rests on: `bundle1_results.md`, `error_budget_and_order.md`, and four literature checks (`analysis/literature/agent_reports/cluster6..9_*.md`; items from those are second-hand until re-read).

## 1. Why restructure

The old plan was sized to a safe deliverable: characterise Causal-Copilot's refinement stage, patch it, report under name controls. Three results from the last two days say the problem is larger and better defined than that.

| Result | Number | Consequence |
|---|---|---|
| The identifiable limit on the public scoreboard is high | 0.957 directed-edge F1 (semantic), 0.971 (formula); best published 0.634 and 0.524 | the field's gap is not a law of nature; about a third of the scale is open |
| Plain PC's committed directions are right 54% of the time; its skeleton with perfect directions would score 0.611; as scored 0.335 | | direction is where most of the reachable loss sits |
| Given only the depth of each variable, a linear regression scores 0.714; given only "which variables are inputs", PC rises from 0.335 to 0.470 | | a few bits of order knowledge are worth more than the whole spread of the published table |
| The released files give the order away through column layout; Causal-Copilot takes its order from names (93% of final edges with real names, 0% with neutral, 90% with misplaced) | | the leaks found so far are all the same thing: undeclared order information |

One question organises all of it: **for each directed edge a system reports, where did the direction come from?**

## 2. Thesis and what would refute it

| | Claim | Refuted if |
|---|---|---|
| T1 | At practical sample sizes, the source of a method's order information explains most of its directed-edge accuracy on public benchmarks | error budgets for GES, FCI and the runnable pretrained models do not show the pattern PC shows (direction accuracy near chance, large gain from oracle tiers) |
| T2 | Deployed agents get their order from names and layout, not from the numbers; controls make this visible from outside | Causal-Copilot on CausalArena's scenarios keeps its score under neutral names and shuffled columns |
| T3 | A system that holds order as an explicit, typed, sourced partial order and chooses parents conditional on it is (a) never below its own data-only output when no knowledge is given, (b) boundedly harmed by wrong knowledge, (c) at or above the best published number in each declared information regime when the knowledge is right | (a) or (b) fail on held-out scenarios; (c) is a target, not a promise, and is reported whichever way it falls |
| T4 | Its claims can carry calibrated confidence and a machine-checkable derivation, so it can decline to claim | calibration error on held-out scenarios is no better than raw bootstrap frequencies; or the checker rejects its own derivations |
| T5 | The claims support answers to "what happens if we set X?" with a stated identification status, verifiable on held-out interventions | interventional predictions are no better than regression on all variables |
| T6 | It can say which experiment would settle the most open directions, and that choice beats random on recorded real experiments | no better than random selection on the Causal Chambers pool |

T1-T2 are measurement, T3-T4 are the system, T5-T6 are what makes it decision-grade. Each is a result without the next.

## 3. Information regimes and controls (the evaluation contract)

Every score is reported under a declared regime and with all controls applied. This is what a submission to a scoreboard should state and currently does not.

| Regime | The system may use | Published comparators (semantic) |
|---|---|---|
| D | numbers only | FoundCause 0.634, GIES 0.552, PC 0.333 |
| D+I | numbers and the released interventions | GIES 0.568, TabCausal 0.447 |
| D+K | numbers and declared knowledge (tiers supplied by a person or by a language model reading names) | none: no method declares this regime |
| D+I+K | all three | none |

| Control | Values | What it isolates |
|---|---|---|
| Column order | always shuffled (seeded); released order only in the audit | layout |
| Names | real / neutral / moved to other columns | knowledge from names; and, when moved, whether data can overrule it |
| Knowledge supplier | none / oracle tiers from the truth / language model (each model separately) | how good the knowledge is versus how well it is used |
| Interventions | withheld / released targets / chosen from a pool | experimental information |

Score views, all from the same output: scoreboard F1 (forced choice, for comparability); direction accuracy on true connections and skeleton precision/recall (the two budget lines); precision at a stated coverage and calibration error (claims the system was willing to make); error of interventional predictions.

## 4. The system: a claim ledger

Outside the `Causal-Copilot` tree, deterministic, usable as a replacement for its refinement stage or on its own.

### 4.1 State (typed)

| Object | Content |
|---|---|
| `OrderEvidence` | `(x before y, source, strength, reference)`; source is one of a closed list: `data-pattern` (collider and propagation rules), `data-form` (asymmetry of the fitted mechanism), `intervention` (y shifts when x is set), `knowledge` (tier statement, with supplier, model, prompt hash and exactly what the supplier was shown) |
| `OrderLedger` | all order evidence; its transitive closure; conflicts (a cycle among statements) as explicit records with the resolution taken |
| `PartialOrder` | the resolved order; pairs it does not order stay unordered |
| `AdjacencyEvidence` | one joint test per candidate edge: is x needed to predict y given y's other candidate causes (candidates = variables not after y); symmetric tests for unordered pairs |
| `Claim` | `x -> y` (connected and ordered), `x - y` (connected, order open), `no edge`; each with the evidence records it rests on, the sources of its direction, and a confidence |
| `Regime` | which sources were admitted in this run |

There is no evidence type for column position or file path, so those cannot enter a claim.

### 4.2 Stages

| Stage | Does | Deterministic given |
|---|---|---|
| K0 | read data; record hashes; variable identities independent of position | file |
| K1 | collect order evidence from each admitted source | data, seed, knowledge reply |
| K2 | resolve to a partial order; fixed priority `intervention > data (strong) > knowledge > data (weak)`; unresolved conflicts leave the pair unordered | K1 |
| K3 | adjacency tests conditional on the partial order | K2, data |
| K4 | emit claims | K2, K3 |
| K5 | confidence: repeat K1-K4 on resamples; map frequencies to probabilities with a calibration curve fitted on other scenarios | seed, calibration set |
| K6 | views: claim list; scoreboard graph (the scoreboard's rule for open directions); selective graph at a confidence threshold | K4, K5 |
| K7 | checker: an independent routine re-derives every claim from the ledger and rejects any it cannot | ledger |

A language model appears only inside the `knowledge` source of K1, as a supplier of tiers ("which of these variables are inputs, which are downstream readings"), validated against a schema, asked in several phrasings, and never as a writer of edges. This is the position Zheng et al. argue for (agents "should not supply edges, orientations, priors, constraints or causal conclusions") taken one step further than they take it: knowledge is admitted, but as a declared, typed, overridable input whose effect is separately reported.

### 4.3 Invariants (checked as gates on every run)

| | Invariant |
|---|---|
| I1 | Shuffling columns changes nothing but the order of rows in the output (bit-identical claims after renaming) |
| I2 | Same inputs and seed give the same ledger hash |
| I3 | With no knowledge admitted, regime D+K gives exactly the regime D output; every difference between two regimes traces to named ledger records |
| I4 | No claim without evidence records; the checker accepts every emitted claim |
| I5 | Knowledge never creates or removes a connection; it can only order connected pairs |
| I6 | Where an intervention and a knowledge statement disagree, the intervention wins and the conflict is recorded |
| I7 | Malformed supplier output cannot crash a run: validate, retry once, then proceed without it |

I3 and I5 give property (a) and the bound in (b) of T3 by construction: with knowledge absent the output is the data-only output; with knowledge wrong, the skeleton is untouched and at most the directions that knowledge decided can be wrong.

## 5. Work, in four tracks

| Track | Items | LLM cost | Depends on |
|---|---|---|---|
| A. Measurement | A1 error budgets for PC (done), GES, FCI, the pipeline's chosen algorithms, and the pretrained models that run on CPU; on semantic, formula, a synthetic sample, Causal Chambers. A2 order-provenance audit of Causal-Copilot on 10 CausalArena scenarios x 3 name arms (the old bundle 2 runs, with shuffled columns). A3 knowledge elicitation: can a model reading names supply tiers, how accurately, and what happens with neutral and moved names | A1 none; A2 about 30 runs; A3 about 900 short calls | nothing; A3 decides how far T3(c) can go in regime D+K |
| B. Ledger | B1 data-only kernel (K0-K4, K7, invariants). B2 interventions as order evidence. B3 knowledge tiers. B4 confidence, calibration, selective output | B3 a few hundred short calls | B1 first |
| C. Decisions | C1 interventional queries with identification status, scored on the released interventional rows and on Causal Chambers experiments. C2 choosing the next experiment from a pool of recorded ones | none | B2 |
| D. Writing and theory | the budget identities; the bounded-harm statement; a coverage guarantee for selective claims within a benchmark family (split by scenario); the report, site, poster; a paper draft | none | A, B |

The old bundle 3 (patch the bootstrap step, ask the model only about open pairs) is absorbed into B1 and B3. The old bundle 4 is B2. The old bundle 5 is part of D.

## 6. Predictions for the next live step (thresholds go into code before the calls)

A3, knowledge elicitation, on the 50 public semantic and 50 public formula scenarios, names presented in shuffled order, three phrasings, three name arms.

| | Prediction | Supported if | Refuted if |
|---|---|---|---|
| O1 | With real names the model's tiers order true edges correctly | at least 70% of true edges ordered correctly and at most 10% contradicted (semantic) | under 50% correct or over 25% contradicted |
| O2 | With neutral names it supplies nothing | correct minus contradicted at most 0.05 | above 0.15 |
| O3 | With moved names its tiers follow the labels | scored by label, as O1; scored by data, correct minus contradicted at most 0.05 | by data above 0.15 |
| O4 | Regression on the model's tiers (real names, shuffled columns) reaches the best published number | mean directed-edge F1 at least 0.634 on public semantic | at most 0.50 |
| O5 | The same on the formula family against 0.524 | at least 0.524 | at most 0.40 |

I do not know how O4 and O5 will come out. If they hold, regime D+K has a first entry above the published table from a method that states exactly what knowledge it used. If O1 fails, the knowledge route is weak on these scenarios and T3(c) rests on interventions and data.

## 7. Failure modes named in advance

| # | Failure | Guard or consequence |
|---|---|---|
| Y1 | The semantic scenarios' graphs were written with language-model help, so a model's tiers may agree with the truth for the wrong reason | report the formula family (physical laws) and Causal Chambers (physical truth) next to it; the moved-names arm measures what happens when knowledge is wrong |
| Y2 | The data-only kernel does not reach GIES (0.552) | it is still the reference the other regimes are measured against; T3(c) is then claimed only where it holds |
| Y3 | Order evidence conflicts (cycles) are frequent | fixed priority, conflicts recorded, pair left unordered; conflict rate is a reported number |
| Y4 | Calibration learned on one family does not transfer | guarantee stated within family only; cross-family numbers reported as measured |
| Y5 | Joint nonlinear tests are slow at 25 variables | start linear (already 0.714 with oracle tiers); add one nonlinear test with a time budget; cache by content hash |
| Y6 | Causal Chambers' standard graphs are one layer deep (controls -> sensors), so order is trivial once the controls are known | use it for the skeleton line of the budget, for interventional prediction and for experiment choice, not as a test of order discovery |
| Y7 | Scope: four tracks for one person | tracks C and D shrink first; decision gates below; each track is a role a teammate could own |
| Y8 | Prior work closes the gap first | positioning in section 9; the conjunction is what is open, and the measurements in A are dated |
| Y9 | The benchmark's maintainers change the files | the dated result stands; shuffling remains a required control |
| Y10 | A model snapshot changes mid-study | snapshot recorded per call; one snapshot per comparison |
| Y11 | Thresholds or the tier prompt tuned after seeing results | prompt and thresholds hashed into the plan before the calls; the public half is split into a development and a held-out set by scenario number before B work starts |

## 8. Decision gates

| Gate | Date | Decided on | If not met |
|---|---|---|---|
| G1 | 16 Oct | A1 budgets for GES and FCI; A3 elicitation result (O1-O5) | drop or keep the knowledge route; re-plan B3 |
| G2 | 2 Nov (Quarter 1 checkpoint) | B1 passes I1-I4, I7 and is not below plain PC on held-out scenarios; A2 done | fall back to the old bundle 3 patch as the Quarter 1 deliverable |
| G3 | 4 Dec (Quarter 1 final) | B2 and B3; scores in three regimes with all controls; package in the scoreboard's format | report what exists; move the rest to Quarter 2 |
| G4 | March | B4, C1, C2, second model, Causal Chambers; paper draft | cut C2 first, then C1 |

## 9. Position against the nearest work (from the literature checks; re-read before citing)

| Work | What it already does | What it does not |
|---|---|---|
| Vashishtha et al. 2023 (arXiv 2310.15117) | argues that order, not edges, is the right thing to ask an imperfect expert | no provenance, no layout or moved-name control, no public scoreboard |
| CARE, Dong et al. 2025 (arXiv 2511.16016) | original / anonymised / permuted names for model-assisted discovery | not an agent pipeline, layout not measured, small classic graphs |
| Li and Russo, UAI 2026 | data can overrule model constraints, in an argumentation framework | 15 variables, hard constraints, single graph, no interventions |
| Kitson and Constantinou 2026 | per-edge probabilities from fused model and data, 8-70 variables, neutral names | no calibration reported, no derivations, data cannot overrule, no interventions |
| Magliacane et al. 2016 (ACI) | scored ancestral claims from tests, interventions and background knowledge | under 12 variables, no model-supplied knowledge |
| ACDB 2026 (arXiv 2609.31675), CausaLab 2026 | agents choosing interventions, 3-7 variables; classical baselines beat the models | no names, no real data, small |
| CausalDS 2026 (arXiv 2607.08093) | data-in causal queries with scored abstention and intervals, small motifs | not at 20-40 variables, no experiment proposal, one hidden graph |
| Zheng et al. 2026 | position: agents should not supply edges; calls for audit trails | leaves their design and evaluation open |

Not found by these searches: a public benchmark shown to leak directions through column order; a three-way control (numbers, names, layout); an error budget separating identifiability from skeleton and direction loss; machine-checked derivations per claim; one system fusing tests, interventions and labelled model knowledge at 20-40 variables. "Not found" is a statement about four bounded searches.

Correction this forces on earlier text: the name-moving control is not new (CARE). What is new here is applying it, with a layout control, stage by stage to a deployed agent and to a public scoreboard.

## 10. What is not claimed

No promise to top the scoreboard in regime D. No claim about the unpublished half. No claim that knowledge from a language model is trustworthy; the design assumes it is not and measures the harm. No claim of calibrated confidence outside the family it was calibrated on.

## 11. How much further this can go (not planned; listed so the ceiling of ambition is explicit)

| Extension | What it adds | What it needs | Honest risk |
|---|---|---|---|
| E1 Field-wide audit | the controls of section 3 applied to every agent and model-assisted method with public code (the literature checks name CauScientist, MosaCD, ArgCausalDisco, AVICI and CDFM checkpoints) on bnlearn graphs, CausalArena and Causal Chambers: one table of "where each system's order comes from" | wrappers per system; API cost per agent; weeks, not days | other people's code; breadth without the ledger is an evaluation paper only |
| E2 A public agent track | a standing page that scores submissions in declared regimes with all controls, starting with our rows; the scoreboard's own format plus the regime and control fields | a hosted page and a validator; maintenance | only worth it if others submit |
| E3 Real experiments | the ledger choosing and running interventions on physical hardware through the Causal Chambers remote laboratory (the check found no agent that has done this) | paid subscription and an access request; the larger Mk2 chambers (up to 99 variables) | cost and access are not public; one-layer graphs make order easy, so the test is of experiment choice and effect prediction |
| E4 Learned fusion | a pretrained network that takes the numbers plus tier statements of stated reliability and returns claims, trained on simulated systems where the statements are sometimes wrong; the ledger's fixed priority rule becomes a learned one | GPU time (days), a generator (the benchmark's sampler is released), careful held-out design | the largest research bet here; could absorb a whole quarter |
| E5 Harder settings | hidden common causes (partial ancestral graphs), time series, 100+ variables | new evidence types and tests per setting | each is a project |

My recommendation: sections 1-10 as the spine, E1 in a reduced form (three or four systems) because it is what turns the measurements into a field-level result, and a decision on E3 or E4 at gate G3 with numbers in hand.

## 12. Decisions needed

1. Adopt this as the plan, or say which parts go further or elsewhere than you want.
2. Approve A3 (about 900 short calls through your key: one request per scenario, arm and phrasing, asking only for tiers; prompt fixed and shown to you first).
3. Still open from before: telling CausalArena's maintainers about the column order.
