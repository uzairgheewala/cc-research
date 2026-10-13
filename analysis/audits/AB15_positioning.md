# AB-15 Positioning closure: closest prior work for claims L1-L5

Tickets: AUD-46, DOM-07. Written 2026-10-12. Table: `AB15_positioning.json` (45 rows, plus 5 works checked but not
tabled). Inputs read first: `AU0_synthesis.md`, `reports/aud27_31_free_steps.md`, `reports/audit_dag.md`.

## 1. Question, method, labels

**Question.** For each candidate claim L1-L5, what is the closest published result, and what exactly is different?

**Method.** I ran 38 web searches (listed in the JSON) and fetched primary sources: arXiv abstract, HTML and PDF pages,
proceedings pages, official READMEs, library source and docs. I started with the ten works the earlier audits left
unread, then covered the six topics in the brief. Every page went through a summarising fetch tool, so section numbers
come from that tool and should be spot-checked before they go into a paper. Quotes are under 15 words.

**Labels.**
- **read (primary):** the statement was found in the work's own text, code or docs.
- **abstract only:** only the abstract or landing page was readable.
- **second-hand:** taken from an earlier audit (AU1-AU8) or a non-primary page. Used only for some venue details, and
  marked where it appears.

Count: 31 rows read (primary), 14 abstract only.

## 2. Novelty matrix

| Claim | Verdict | Closest prior | What is different in ours |
|---|---|---|---|
| L1 Layout and engine channels | **partly open** | Colombo & Maathuis 2014 (PC order dependence, including conflicting v-structures); Kitson & Constantinou 2024 (column order moves F1, up to 0.41 for HC) | **Their work:** variance over random orders, as noise. **Ours:** (a) a signed bias under a public release's causal column order; (b) the size of the benchmark authors' index rule on a leaderboard; (c) shipped engines (Causal-Copilot's copy, gCastle `original`/`stable`) failing a perfect-oracle test on ~36% of problems. No public report of (c) found. |
| L2 Name reliance | **partly open** | CARE (Dong et al., arXiv 2511.16016): permuted names over unchanged data, e.g. GPT-4.1-mini + algorithm outputs 0.858 → 0.137 on ASIA | **CARE:** prompted LLMs on bnlearn graphs (≤37 nodes), layout not varied. **Open:** ≥3 end-to-end agents, names crossed with layout, 20-40-variable non-bnlearn graphs, dose-response. A single system losing F1 under swapped names is not new. |
| L3 Decision value | **partly open** | SID (Peters & Bühlmann 2015), AID (Henckel et al. 2024), Gentzel et al. 2019 (use interventional measures), Petersen (random-guess controls) | Not found in print: the empty graph as a baseline on decision questions for a public leaderboard, with the true CPDAG as ceiling. Measured on one benchmark only. |
| L4 Claim ledger | **partly open** | Li & Russo UAI 2026 (LLMs "cannot add edges"); GENESIS (per-edge "decision traceability", abstract only); DAGForge (per-edge provenance channels) | Not found: a record that types each *direction* by source, plus a verifier for knowledge-never-connects, interventions-outrank-knowledge, order invariance and a data-only floor. GENESIS's full text could narrow this. |
| L5 Theory | **partly open** (per item below) | Colombo & Maathuis (conflict-rule order dependence: **scooped**); Zhang 2008 / Fang et al. (what a CPDAG settles); Chen, Ban et al. (bound for order-consistent prior errors) | **New:** a bound for orientation-only knowledge on a fixed skeleton, via F1 = S × a. The identity itself is elementary algebra. No error-budget prior found. |

## 3. Per-claim findings

### L1 Layout and engine channels

- **PC's conflict rule depends on order: known.**
  - Colombo & Maathuis (JMLR 2014, Sec. 3.3, Example 3) show that overwriting conflicting v-structures makes PC's
    output depend on which triple comes last. Section 4 offers PC-stable, CPC, MPC and bi-directed "lists" as fixes.
    Their simulations look at variance over 20 random orderings.
  - CPC (Ramsey, Zhang & Spirtes, UAI 2006) and maxP (Ramsey 2016) are the standard order-free rules.
  - causal-learn's docs list five conflict priorities and default to "prioritize existing colliders" (uc_priority 2,
    uc_rule 0).
  - What we add: in a release whose columns are in causal order, the default rule loses commit accuracy (q 0.59 vs
    0.74 shuffled), "overwrite" flips the sign, and maxP removes the gap. None of the works read reports a signed
    effect tied to a benchmark's layout.
- **Order moves structure-learning scores: known.**
  - Kitson & Constantinou (DMKD 2024): worst-to-optimal ordering moves HC F1 by 0.412 and PC-Stable by 0.036. Their
    "optimal" ordering is consistent with the topological order. They give the HC mechanism (score-equivalent ties) but
    none for PC-Stable.
  - Their PGM 2024 paper and arXiv 2504.01740 remove the instability for HC/Tabu and note that PC-Stable "retains a
    considerable amount".
  - L1 must cite these and frame itself as identifying the *channels* on a published scoreboard, not as discovering
    order sensitivity.
- **The authors' rule.**
  - The CausalArena code README confirms the "liberal" rule: undecided edges go from the smaller index to the larger.
  - The paper's Sec. 4.5 defers conversion rules to Appendix B, which I could not read (see section 5).
  - No one reports the size of this rule's effect.
- **Engine copies.**
  - gCastle's source confirms one-sided conditioning sets (`z = adj_i - {j}`) in `original` (the default) and `stable`.
    `parallel` tests both sides.
  - causal-learn issues #133 and #175 show oracle testing and cross-implementation differences are routine. Neither
    reports a skeleton defect.
  - I found no published report of the gCastle or Causal-Copilot defect. I could not search gCastle's GitHub issues
    (blocked).
- **Data-statistics leaks are a different channel.**
  - Varsortability and R2-sortability (Reisach et al. 2021, 2023) leak order through marginal statistics.
  - CausalArena is standardised (varsortability 0.5) and R2-sortable only on average (0.55-0.60). So the layout effect
    is separate from these.
- **Order as an explicit input.** ACDB permutes node indices as a precaution but measures nothing. ReplaySCM varies
  disclosed order on purpose. MosaCD names the exhaustive-search assumption but tests no implementation.

### L2 Name reliance

- **CARE is the scoop risk.**
  - Its "Permuted" condition shuffles names over unchanged data on ASIA, SURVEY, EARTHQUAKE and ALARM (37 nodes).
  - LLMs given algorithm outputs collapse, e.g. 0.858 → 0.137 (Table 2).
  - Column reordering is used in training and is not measured.
- **What is still ours:**
  - agent systems run end to end;
  - names crossed with layout;
  - graphs that are not famous bnlearn networks;
  - the share of swapped names as a dial.
- **Memorisation evidence.**
  - Kıcıman et al. (LLMs work from metadata).
  - CausalGraphBench (ACL SRW 2025): a direct bnlearn memorisation probe. This is the nearest real paper to "LLMs
    memorise BNLearn"; no paper with that exact title was found.
  - Srivastava et al. (post-cutoff graphs).
  - Feng et al. (ACL 2025: recognition tracks pre-training frequency).
  - CausalProbe-2024 (fresh corpora).
- **Name controls, none of which are semantic swaps.**
  - Corr2Cause swaps symbolic names (A, B, C → Z, Y, W).
  - Kitson & Constantinou 2026 (arXiv 2608.27472) use meaning-preserving aliases, with no ablation.
  - Li & Russo ground graphs in CauseNet and defer obfuscated metadata to future work.
  - Causal Ensemble Agent (also checked) removes names.

### L3 Decision value

- **Interventional evaluation exists and is advocated.**
  - Peters & Bühlmann's SID.
  - Henckel, Würtzen & Weichwald's AID: we use their `ancestor_aid`.
  - Gentzel, Garant & Jensen (NeurIPS 2019): interventional measures disagree substantially with structural ones.
- **No one tests learned graphs against the empty graph.**
  - SID and AID use the empty graph only in theoretical examples (Henckel Cor. 8, App. C Ex. 19; Peters Prop. 3).
  - Petersen's negative controls are random graphs for skeleton metrics, and the empty graph is not discussed.
  - ACDB reports a random-DAG floor (23.6% directed F1) and no empty row.
  - None of these compares learned graphs with "nothing moves".
- **Related results.**
  - IDA (Maathuis et al. 2010) checks predicted effects against knock-outs with a random baseline.
  - CausaLab shows prediction and structure diverging the other way (92% task accuracy, edge F1 0.471).
  - Asiaee et al. (arXiv 2603.02204) learn exactly the "does T move Y" relations for conformal calibration.
  - CausalDS scores abstention on effect questions.
- **Verdict.** The measurement is ours. It rests on one benchmark until AB-04 repeats it, and "barely beat" needs
  file-paired numbers.

### L4 Claim ledger

- **Knowledge never adds a connection: established.**
  - pcalg's `addBgKnowledge` orients existing edges only.
  - Li & Russo (UAI 2026, Sec. 4.2): LLMs "orient surviving adjacencies only; they cannot add edges". They also measure
    harm in low-quality-LLM cells (mean ΔF1 −0.122).
- **Per-edge provenance has close priors.**
  - GENESIS (arXiv 2608.03868; abstract only) requires every edge to trace to statistical evidence, Markov-blanket
    consistency or domain reasoning.
  - DAGForge (arXiv 2607.21859) attaches provenance channels to each edge (literature, UMLS, temporal, user
    constraints, solver, model prior). It lets knowledge add edges and runs no data check.
  - Kitson & Constantinou's fusion keeps per-source distributions but does not record the source in the final DAG.
- **Supporting standards and tools.** PROV-O (W3C 2013) has no causal-claim terms. Tetrad knowledge (tiers,
  required, forbidden) is an input format only. Calibration work (Jabbari et al.; Kummerfeld & Rix) and dataset-level
  abstention (Causal-Audit) cover single components.
- **Not found anywhere:**
  - typing of *directions* by source (data pattern, functional form, intervention, knowledge, none);
  - a verifier over a stored record;
  - a declared order-invariance check;
  - a constructive "never below data-only" guarantee. MosaCD, L2D-CD and RoaDs all lack one; RoaDs names the gap
    itself.
- CausalVerify (arXiv 2609.07944) shares only the word "verify": it checks effect-estimation workflows against
  reference estimators.

### L5 Theory

- **Conflict-rule order dependence: scooped.** Colombo & Maathuis prove it by example. What might be new is only the
  direction of the effect under a causal layout, which needs a proof or should be called an empirical regularity.
- **Decision-value ceiling of the CPDAG: theory is established.** Zhang (JMLR 2008), Fang et al. (arXiv 2207.05067)
  and the IDA line already say what an equivalence class settles. Vashishtha et al. argue that order, not edges, is
  the robust object. Ours is the measured ceiling (precision 1.000 at 92.5% coverage) next to learned graphs.
- **F1 = S × a: not found in print, but elementary.** Directed true positives equal skeleton true positives times the
  share oriented correctly, with undecided pairs worth one half. Present it as an exact bookkeeping identity under the
  error budget, not as a theorem. ACDB's layered metrics and Petersen's random-guess expectations are the nearest
  relatives.
- **Bounded harm.**
  - Chen, Ban et al. (arXiv 2306.07032) show that order-consistent wrong priors raise SHD by at most one up to
    equivalence in hard-constraint HC. Order-reversed priors cause "quasi-circles", with a probabilistic, not
    worst-case, condition.
  - Ours concerns orientation-only knowledge on a fixed data skeleton (wrong knowledge changes a, never S).
  - Constantinou, Guo & Kitson (KAIS 2023) test only correct knowledge.
  - L2D-CD, Long et al., RoaDs and Verma et al. give no harm bound.
- **Error budget:** no prior found.

## 4. What this changes

**Claims to narrow:**
1. **L1:** Do not say PC is order dependent, or that column order changes scores, as if new. Say: *"on a public
   leaderboard, layout enters through three separable channels, with sizes"*. Lead with the engine-copy oracle failure
   and the signed conflict-rule effect under a causal layout.
2. **L2:** Drop any framing of "LLMs rely on names" as a finding. The claim is field-level only: ≥3 agent systems,
   names × layout, 20-40-variable non-bnlearn graphs, dose-response. Cite CARE as the closest prior and contrast its
   prompted-LLM, bnlearn setting.
3. **L3:** Present it as a measurement on CausalArena until AB-04 adds a second benchmark. Say "no method beats the
   empty graph on ancestor AID" only with file-paired numbers and the cycle exclusions stated.
4. **L4:**
   - Do not claim "knowledge cannot add edges" as new; it is in pcalg and in Li & Russo.
   - Claim the combination: per-direction source types, a verifier, an order-invariance gate and a constructive
     data-only floor.
   - Read GENESIS in full before AB-16.
5. **L5:**
   - Drop "order dependence of PC conflict rules" as a theory contribution; cite Colombo & Maathuis.
   - Call F1 = S × a an identity.
   - Position the bounded-harm result against Chen, Ban et al., and against Li & Russo's measured harm.
   - Credit the CPDAG ceiling's theory to Zhang and Fang et al.

**Mandatory citations:**
- **L1:** Colombo & Maathuis 2014; Ramsey, Zhang & Spirtes 2006 (CPC); Ramsey 2016 (maxP); Kitson & Constantinou
  DMKD 2024 and PGM 2024 / arXiv 2504.01740; Reisach et al. 2021 and 2023; CausalArena + TabCausal README.
- **L2:** CARE; Kıcıman et al.; CausalGraphBench; Srivastava et al.; Feng et al.
- **L3:** Peters & Bühlmann 2015; Henckel et al. 2024; Gentzel et al. 2019; Petersen.
- **L4:** Li & Russo UAI 2026; GENESIS; DAGForge; pcalg `addBgKnowledge`; PROV-O.
- **L5:** Chen, Ban et al.; Zhang 2008.

**Follow-ups this creates:**
- Add CPC as a third order-free arm in AB-01.
- In AB-03, check whether gCastle has a public issue (from a machine where GitHub is reachable) before calling the
  defect unreported.
- Record uc_rule and uc_priority in every PC run. A maintainer comment in causal-learn #175 says the default is
  PC-Max, which the docs contradict.

**Three most dangerous prior works:**
1. Colombo & Maathuis 2014: scoops the L5 order-dependence item and underlies L1's conflict-rule channel.
2. CARE (arXiv 2511.16016): already shows a permuted-name collapse, so L2 survives only as a field-level result.
3. Li & Russo (UAI 2026): already uses the "cannot add edges" rule and measures harm, which weakens L4 and L5's
   bounded harm. GENESIS is the unread runner-up for L4.

## 5. Not read, or not confirmed

- **CausalArena Appendices B-C.**
  - The HTML the fetch tool returned ends mid-Sec. 6.2, and the PDF has no text layer.
  - The index rule is confirmed from the code README instead.
  - Whether the appendix itself states the rule is unverified.
- **"Kitson & Constantinou 2026 on variable-order sensitivity."** I could not confirm such a paper. The order papers
  are from 2024-2025 (all read). Their 2026 paper (arXiv 2608.27472) is about LLM fusion and does not study order.
- **"LLMs memorise BNLearn".** No paper with this exact title was found; CausalGraphBench was used.
- **gCastle GitHub issues.** Blocked (robots.txt).
- **GENESIS full text.** Abstract only. This is the highest-risk item for L4.
- **arXiv 2606.01789.** Rate-limited on arxiv.org, then read via alphaxiv. It turned out unrelated (benchmark
  consistency).
- **Tetrad PC-Max page.** The body was not extracted.
- **SID publisher page.** Error; the ETH manuscript was read instead.
- **Abstract-only items.** Gentzel et al., Kıcıman et al., Feng et al., Ban et al., ILS-CSL, Takayama et al., Long et
  al., Verma et al., Vashishtha et al., Zhang 2008, Fang et al., Ramsey 2016, CausalDS, CausaLab, ReplaySCM,
  CausalVerify.
- **Not checked.** Perković et al. on MPDAG identification; Tetrad's adjacency and arrowhead precision definitions.
- **Venues taken second-hand.** CausalProbe NeurIPS 2024, Kıcıman TMLR, Vashishtha ICLR 2025, RoaDs AAAI, CPC UAI
  2006.
