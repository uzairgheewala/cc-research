# AU3 Theory and limits: what is identifiable in Q x R x W, at what cost

Tickets: AUD-20, DOM-12, RQ-04
Written 2026-10-12 by an audit agent; sources read on that date.

**Where we are now:** 55 typed rows (C01-C55) over about 70 primary pages. Each row gives the identifiable object, the key theorem, the rate or experiment cost, and the impossibility result or lower bound. Most rows rest on an abstract-level read. Where I read the full text it is marked in `read_level` in the JSON: Meek 1995; Uhler et al. 2013; Kalisch & Buehlmann 2007; Robins et al. 2003; Peters et al. 2014; Gao, Tai, Aragam; Hauser & Buehlmann 2014; Bang & Didelez 2023; Shojaie & Fox 2022; the PCMCI paper; and Malinsky & Spirtes 2016. The shared web-search budget ran out before the conformal-structure search, which is therefore marked as not run.

## Question

For each cell of Q (skeleton, orientation, effects P(Y|do(X)), experiment design) x R (D, D+I, D+K, D+I+K) x W (sufficient iid, restricted functional forms, hidden confounders, selection bias, time series, cycles, high dimension, mixed data), I asked:
- what is identifiable;
- from what evidence and under which assumptions;
- at what sample or experiment cost;
- what the best known bound or impossibility result is.

## Method

- **Starting point.** I read the shared context and the prior notes first: cluster5, cluster7, dom09, scope_note, and the relevant parts of cluster3, cluster6, cluster8, cluster9 and bnd02/dom08. Results already covered there are cited, not re-derived. Bootstrap calibration, Meek/MPDAG/tiers and Strieder-Drton were in cluster3. Varsortability was in cluster8. IDA and adjustment timing were in dom09.
- **Primary sources.** I used arXiv abs pages or PDFs, PMLR, JMLR, NeurIPS proceedings and PMC. Fetches went through a summarising tool, so quotes are as the tool returned them. Re-check any quote before it goes into a mentor document.
- **Inclusion rule.** A result enters the table only if it is a theorem or a formal characterisation stated by its authors on a page I opened. Empirical-only works appear only where they mark the edge of theory: partial orders (C20), conformal (C54) and large random graphs (C55).
- **Labels.** All numbers are `reported` (the authors' own statement) unless marked `second-hand` (from a project note). Project numbers are quoted from `audit_context.md` and labelled `project (measured)`. I did not re-verify them.
- **Venues.** A venue is given only where the page showed it, or where it is inferable from the DOI. In the latter case I say "per DOI".

## Findings

### F1. Causally sufficient iid, observational (D): population identifiability versus finite-sample recovery (item 1)

**Population object.** Under Markov plus faithfulness, D identifies the skeleton and the CPDAG, and nothing more.
- Meek's rules R1-R3 applied to the pattern give the maximally oriented graph (Meek 1995, Thm 3; full text read). [arXiv 1302.4972](https://arxiv.org/pdf/1302.4972)
- GES identifies the same class in the large-sample limit (Chickering 2002, JMLR 3:507-554). [jmlr](https://www.jmlr.org/papers/v3/chickering02b.html)
- Edges inside undirected chain components are unidentifiable at any n.
- **Project (measured):** on CausalArena semantic scenarios this ceiling is directed F1 0.957 (91.8% of edges compelled).
- **Linear-Gaussian equals nonparametric here.** In the linear-Gaussian case the population object is exactly the same CPDAG. Gaussianity adds no orientation information unless error variances are equal or known (C15).

**Gap 1: pointwise, not uniform, consistency.** Robins, Scheines, Spirtes and Wasserman (Biometrika 90(3):491-515, 2003; full text read) prove the following:
- Under Markov plus faithfulness with a possible latent confounder, consistent tests and estimators exist only pointwise.
- No uniformly consistent test (Thm 1), no uniformly consistent estimator (Thm 3) and no consistent confidence map (Thm 4) exist. The result extends to inferring time order (Thm 5).
- In the normal linear case there is "no nontrivial uniformly consistent test" (Thm 6).
- In the tool's words, no finite n can "ever be guaranteed to approximate the asymptotic results".
- With an observed discrete confounder and known order, uniformly consistent tests do exist. Randomised experiments also restore uniform consistency (Remark 3).
- Zhang & Spirtes (UAI 2003) place the impossibility in "time order unknown and/or latent confounders". They show that strengthened faithfulness restores uniform consistency. [biometrika2003.pdf](https://www.cmu.edu/dietrich/philosophy/docs/spirtes/biometrika2003.pdf), [arXiv 1212.2506](https://arxiv.org/abs/1212.2506)

**Gap 2: strong faithfulness is what finite-sample results buy, and it often fails.**
- Kalisch & Buehlmann (JMLR 8:613-636, 2007; theorem read) prove that PC recovers the skeleton with probability 1 - O(exp(-C n^{1-2d})). Their assumptions:
  - Gaussian and faithful distributions;
  - p = O(n^a);
  - neighbourhood size q = O(n^{1-b});
  - nonzero partial correlations bounded below by c_n with 1/c_n = O(n^d), d < b/2.
  
  The c_n bound is a strong-faithfulness-type condition. [arXiv math/0510436](https://arxiv.org/pdf/math/0510436)
- Uhler, Raskutti, Buehlmann and Yu (Ann. Statist., DOI 10.1214/12-AOS1080; full text read) show that the set of lambda-strong-unfaithful distributions has positive measure. Their lower bounds:
  - trees: 1-(1-lambda)^{p-1};
  - cycles: exponential in p^2;
  - K_{2,p-2}: exponential in 2^p.
- In their simulation of 10-node DAGs with expected degree 2, the share that is lambda-strong-unfaithful is nearly 1 at lambda = 0.1, about 0.9 at 0.01 and about 0.7 at 0.001 (reported).
- With lambda_n ~ sqrt(deg log p / n), the lower bound vanishes only if p_n = o(sqrt(n/(deg log n))) for trees, o((n/(deg log n))^{1/4}) for cycles, and o(log n) for bipartite graphs. The authors conclude that even trees cannot have p >> n. [arXiv 1207.0547](https://arxiv.org/abs/1207.0547)
- **Caveats.** The parameters are uniform on [-1,1] with unit error variances. "Strongly unfaithful" means at least one (i, j, S) partial correlation falls below lambda. So the result predicts that some test errors occur in almost every graph. It does not predict how many edges are wrong.
- **What this implies for us (my arithmetic, not a reported number).** At n = 1,000, p = 20-40 and degree 2-4, lambda_n is roughly sqrt(2*3.4/1000) to sqrt(4*3.7/1000), about 0.08-0.12. That is the regime where Uhler et al. simulate near-universal strong unfaithfulness. Some finite-sample PC errors are therefore expected on CausalArena-sized problems even when the population CPDAG is identifiable.

**Weaker conditions and their limits.**
- **k-Triangle-Faithfulness.** Spirtes & Zhang (Statist. Sci. 29(4), 2014) give a uniformly consistent estimator of the MEC and of identifiable coefficients under it. They say strong faithfulness "may be false with high probability in many domains". [arXiv 1502.00829](https://arxiv.org/abs/1502.00829)
- **Sparsest permutation.** SP is consistent under conditions strictly weaker than faithfulness (Raskutti & Uhler). [arXiv 1307.0366](https://arxiv.org/abs/1307.0366)
- **No faithfulness at all.** Lin & Zhang (ALT 2020) show that no learner converges on all networks. Any learner with the best achievable convergence mode must converge on all faithful ones, so faithfulness is "a requirement, not an option". [PMLR 117](https://proceedings.mlr.press/v117/lin20a.html)

**Gap 3: CI tests have no free lunch.** Shah & Peters (Ann. Statist., DOI 10.1214/19-AOS1857) prove that a valid CI test has no power against any alternative. Every constraint-based guarantee therefore inherits assumptions on the regression or test used. [arXiv 1804.07203](https://arxiv.org/abs/1804.07203)

**Sample-complexity floor.**
- Exact BN structure recovery needs Omega(k log m + k^2/m) samples for sparse BNs and Omega(m) for non-sparse ones (Ghoshal & Honorio; venue not confirmed). [arXiv 1601.07460](https://arxiv.org/abs/1601.07460)
- For equal-variance Gaussian DAGs, n ~ q log(d/q) is minimax optimal (Gao, Tai, Aragam; full text read; venue not confirmed). [arXiv 2201.10548](https://arxiv.org/pdf/2201.10548)
- GES and ARGES are consistent in sparse high-dimensional settings (Nandy, Hauser, Maathuis, Ann. Statist. 46(6A), 2018). The conditions are in the full text, which I did not read.

**Counting.** Most MECs are "half completed" with small average size, and sparse class sizes grow roughly exponentially in p (He, Jia, Yu, JMLR 16, 2015). [jmlr](https://www.jmlr.org/papers/v16/he15a.html)

### F2. Restricted functional forms (D, W = mechanism class)

Each of the following makes the full DAG identifiable from D alone. Each holds only for its own model class.
- **LiNGAM:** linear with non-Gaussian errors (Shimizu et al., JMLR 7, 2006).
- **Additive noise models:** nonlinear ANMs, where the bivariate exceptions satisfy a differential-equation condition and linear-Gaussian is the classic one. Restricted multivariate ANMs and nonlinear Gaussian ANMs are identifiable (Peters, Mooij, Janzing, Schoelkopf, JMLR 15, 2014, Thm 27 and Cor 30; full text read).
- **Post-nonlinear:** identifiable except for enumerated cases (Zhang & Hyvarinen, UAI 2009).
- **Equal-variance Gaussian:** Peters & Buehlmann (Biometrika per DOI); known variance ratio (Loh & Buehlmann, JMLR 15, 2014).

The equal-variance result is exactly the property that varsortability exploits in simulated benchmarks. Reisach, Seiler and Weichwald show that it disappears after standardisation. [arXiv 2102.13647](https://arxiv.org/abs/2102.13647)

**Caution for the report.** Any claim to "beat the identifiability limit" on CausalArena from D alone must name which of these restrictions it assumes. Otherwise it is exploiting a benchmark regularity, such as column order or variance, not a theorem.

### F3. Background knowledge (item 2)

What each kind of knowledge buys, in increasing strength:

1. **Required/forbidden directed edges (Meek 1995, Thm 4; full text).**
   - Imposing the knowledge and closing under R1-R4 gives the maximally oriented graph, the MPDAG.
   - Perković, Kalisch and Maathuis (UAI 2017) add ancestry reading, an adjustment criterion and IDA on MPDAGs. In their simulation, effects become more identifiable as knowledge grows.
   - The knowledge is assumed correct. Inconsistent knowledge is outside these results.
2. **Tiers, i.e. a temporal partial order (Bang & Didelez, UAI 2023, PMLR 216:119-129; full text).**
   - Every cross-tier edge is directed, and only Meek R1 is needed to finish.
   - The result is a chain graph with chordal components, so CPDAG adjustment and IDA carry over unchanged (Cor 2-3).
   - Fully shielded within-tier edges stay undirected (Example 5).
   - Tiers give the absence of ancestral relations, never their presence.
   - Earlier tier knowledge is more informative (Cor 4).
   - Under latent confounding, FCI with tiers is sound and complete (Andrews, Spirtes, Cooper, AISTATS 2020). For other knowledge types, completeness of FCI is "not known". Wang, Qin and Zhou (NeurIPS 2022) give sound and complete rules for local background knowledge with latents.
3. **Pairwise direct, ancestral and non-ancestral knowledge (Fang, Zhao, Liu, He, JMLR 26, 2025).**
   - Any consistent set decomposes uniquely into a causal MPDAG plus a minimal residual set of "direct causal clauses".
   - Consistency and equivalence checks run in polynomial time.
   - Effect identifiability depends only on the MPDAG (necessary and sufficient).
   - Consequence: ancestral knowledge is not fully representable as edge orientations. A ledger that stores only edge directions loses information.
4. **Partial orders in continuous optimisation (Ban et al., NeurIPS 2024).** Constraint equivalence is claimed, plus an empirical sample saving. I found no identifiability theorem beyond that.
5. **A total causal order.**
   - Orientation becomes free and the problem reduces to per-node variable selection (Shojaie & Michailidis, Biometrika 97(3), 2010).
   - Gao, Tai and Aragam (Sec. 4, Props 4.1-4.2) show the known-order problem has the same n ~ q log(d/q) rate as undirected graphical-model selection, with a matching lower bound.
   - **Project (measured):** "true depth + plain regression = 0.714" fits this theory. Once the order is given, the remaining error is a skeleton/selection problem, which has the same statistical difficulty as an undirected graph.
6. **Order knowledge and uniformity.** Robins et al. and Zhang & Spirtes tie the uniform-consistency impossibility to unknown time order and/or latents. Declared order knowledge in a causally sufficient world is one of the few assumptions with a published route to uniform (not merely pointwise) guarantees. I read this from the abstracts plus the Robins example, not a general theorem for PC. State it as "the impossibility results do not apply", not "uniform consistency holds".

### F4. Hidden confounders and selection bias

- **PAG.** FCI with Zhang's added rules is complete for the PAG under latent confounding and selection bias (Zhang, AIJ 172:1873-1896, 2008). The MAG-equivalence tail rules complete the characterisation (Zhang, arXiv 1206.5282).
- **Linear non-Gaussian with latents.** Only a finite set of models can be identified (Hoyer, Shimizu, Kerminen 2006).
- **Detecting selection bias.** Kaltenpoth & Vreeken (AAAI 2023) give identifiability conditions and tests for whether selection bias is present.
- **Impossibility.** Robins et al. 2003 apply in full: no uniformly consistent estimator or confidence interval. Any finite-sample confidence claim on PAG marks from D alone therefore needs an extra assumption.

### F5. Interventions (D+I) and experiment design (Q = experiments)

**Identifiable objects.**

| Setting | Object | Source |
|---|---|---|
| Hard interventions, known targets | I-essential graph | Hauser & Buehlmann, JMLR 13:2409-2464, 2012 |
| General/soft interventions, known targets | I-MEC | Yang, Katcoff, Uhler, ICML 2018 |
| Unknown targets | I-MEC, via UT-IGSP; JCI also covers this | Squires, Wang, Uhler, UAI 2020; Mooij, Magliacane, Claassen, JMLR 21, 2020 |
| Soft interventions, unknown targets, latents | Psi-PAG; Psi-FCI is sound and complete in the sample limit | Jaber, Kocaoglu, Shanmugam, Bareinboim, NeurIPS 2020 |

**Experiment cost (worst case).**
- **From nothing:** log2(N)+1 unrestricted multi-target experiments are sufficient and worst-case necessary. Single-target experiments need N-1 (Eberhardt, Glymour, Scheines, UAI 2005).
- **From the CPDAG:** ceil(log2 omega) unbounded targets are sufficient and worst-case necessary, where omega is the largest clique in the undirected part. OptUnb finds them in polynomial time (Hauser & Buehlmann, IJAR 2014, Cor 2 / Prop 5; full text).
- **Atomic interventions:**
  - Universal lower bound of about half the largest clique per chain component (Squires et al. 2020).
  - A universal lower bound within a factor 2 of optimal (Porwal, Srivastava, Sinha, AISTATS 2022).
  - Adaptive search uses O(log n) times the verification number, and this is tight. Size-k interventions cost O(log n log k) (Choo, Shiragur, Bhattacharyya, NeurIPS 2022).
- **Targeted subsets of edges:** search cannot beat the vertex cover of the target edges in the worst case (Choo & Shiragur, arXiv 2301.03180).
- **Costs and budgets:**
  - Cost-optimal sets are polynomial-time given the skeleton (Kocaoglu, Dimakis, Vishwanath, ICML 2017).
  - For k single targets, the expected number of oriented edges is submodular and greedy achieves (1-1/e) (Ghassami et al., ICML 2018).
  - Size-k separating systems are needed on complete graphs (Shanmugam et al., NIPS 2015).
- **With latents:** O(d log^2 n + d^2 log n) interventions suffice (Kocaoglu, Shanmugam, Bareinboim, NIPS 2017).
- **Linear cyclic with latents:** necessary and sufficient conditions on the experiment set (Hyttinen, Eberhardt, Hoyer, JMLR 13, 2012).

**Project relevance.**
- The CausalArena replay sampler only intervenes on declared targets, which are roots in the spec checked by cluster7.
- In the I-essential-graph theory, a hard intervention on X orients the edges incident to X. A root's incident edges are already out-edges in truth, so root targets orient exactly those edges plus Meek propagation.
- This is consistent with the small measured gain: >= 0.974 with released interventions, against 0.957 without (project, measured). I did not check this mechanism against the released files.

### F6. Time series, cycles, mixed data

- **Granger causality** measures predictiveness. It matches causation only with:
  - a complete system;
  - no instantaneous effects;
  - sampling at the causal lag;
  - no measurement error.
  
  The review calls these assumptions unverifiable and "even more unlikely to hold simultaneously" (Shojaie & Fox, Annu. Rev. Stat. Appl. 9:289-319; full text via PMC).
- **PCMCI** assumes sufficiency, Markov, faithfulness, stationarity and no contemporaneous effects. It is consistent, but its finite-sample false-positive control is only empirical (Runge et al., Sci. Adv. 2019; full text via PMC).
- **PCMCI+** adds contemporaneous links. It is order-independent and oracle-consistent (Runge, UAI 2020).
- **LPCMCI** handles latents. It is sound and complete in the oracle case (Gerhardus & Runge, NeurIPS 2020).
- **Restricted model classes:** TiMINo (Peters et al., NIPS 2013) and non-Gaussian SVAR (Hyvarinen et al., JMLR 11, 2010) identify lagged and instantaneous structure.
- **Subsampling:** this yields sets of system-timescale structures, recovered by constraint optimisation (Hyttinen et al., PGM 2016).
- **Summary causal graphs** as background knowledge orient micro-level edges under stated conditions (Loranchet & Assaad, preprint).
- **Cycles:**
  - FCI remains sound and complete for simple sigma-faithful SCMs with feedback (Mooij & Claassen, UAI 2020).
  - Cyclic SCMs may lack unique solutions or a Markov property without solvability (Bongers et al., Ann. Statist. 49(5), 2021).
  - LiNG-D returns a distribution-equivalence class, unique only under stability conditions (Lacerda et al., UAI 2008).
- **Mixed data:**
  - Under faithfulness the object is still the CPDAG. The extra issue is CI-test validity (Shah & Peters).
  - Restricted linear mixed models are identifiable (Zeng et al., CLeaR 2022).
  - Ordinal-to-exponential-family edges are identifiable with at least 3 categories and at least 3 support points, and both conditions are necessary (Mishra & Mitra, Sept 2026 preprint).

### F7. Effects from a CPDAG / MPDAG / PAG (item 3)

**CPDAG.**
- IDA returns the multiset of possible effects, one per allowed parent set of X. The minimum |effect| is a lower bound (Maathuis, Kalisch, Buehlmann, Ann. Statist. 37(6A) per DOI).
- The generalized adjustment criterion is sound and complete for DAG, CPDAG, MAG and PAG, with all valid sets constructible in dagitty (Perković, Textor, Kalisch, Maathuis, JMLR 18, 2018).
- An optimal, minimum-variance adjustment set exists for linear models on DAG/CPDAG/MPDAG (Henckel, Perković, Maathuis, JRSSB per DOI).

**MPDAG.**
- Perković (UAI 2020) gives a necessary and sufficient criterion, strictly stronger than generalized adjustment, with a generalised g-formula.
- Fang & He (UAI 2020) and Fang et al. (JMLR 2025) give local IDA with pairwise knowledge.
- Tiered MPDAGs keep CPDAG adjustment and IDA unchanged (Bang & Didelez).

**PAG.**
- Jaber, Zhang and Bareinboim (ICML 2019) give a complete identification algorithm: it returns an expression or certifies non-identifiability.
- LV-IDA (Malinsky & Spirtes, CMU tech report 194 / PGM 2016) returns multisets with NA entries.
  - In 15-variable linear simulations: MSE 0.022 vs IDA 0.056, and 12.7% NA (reported).
  - In the paper's infinite-sample example, IDA's estimates excluded the true effects, while LV-IDA's included them.

**Project (measured, dom09).**
- On one 25-variable scenario, all 600 pairs ran in 0.06 s.
- 52% of pairs had a single possible value.
- The true parent set was among the candidates for only 7 of 25 variables.
- In finite samples, effect accuracy is bounded by skeleton recall, not by identification theory.

### F8. Confidence, selective and abstaining claims (item 4)

**Resampling and Bayesian scores** (also in cluster3, cluster6 and dom08):
- Bootstrap feature frequencies (Friedman, Goldszmidt, Wyner, UAI 1999) rank features but carry no calibration guarantee. Plain bootstrap ECE is about 0.07-0.08 (second-hand, cluster6 via Banerjee et al. 2025).
- Order-MCMC posteriors (Friedman & Koller, UAI 2000), BCCD (Claassen & Heskes) and ACI (Magliacane et al., NIPS 2016) attach reliabilities. Their validity rests on the model and prior.

**Error control.** PC-p gives edge-wise p-value bounds and Benjamini-Yekutieli FDR control across CPDAG edges (Strobl, Spirtes, Visweswaran; ACM TIST 2019 per index).

**Coverage-guaranteed structure uncertainty** exists only in identifiable restricted classes:
- confidence regions for effects by test inversion (Strieder et al., UAI 2021; Strieder & Drton, JCI 2023);
- confidence sets of causal orderings (Wang, Kolar, Drton), asymptotically valid, giving sub- and supersets of ancestral relations.

**Post-selection inference.**
- Using the same data for discovery and inference inflates miscoverage.
- Chang, Guo and Malinsky give asymptotically valid effect CIs after PC by resampling and screening.
- Gradu, Zrnic, Wang and Jordan (JASA 120(550) per RePEc) give a related method.

**Conformal.** The only causal-discovery conformal method found (CausalGuard, May 2026 preprint) covers a posterior-weighted pseudo-outcome, not graph features or the effect itself. Cluster9 and dom08 also found no conformal structure sets. My planned dedicated search was not run (budget).

**Theoretical floor.** Robins et al. rule out uniformly valid confidence for causal claims from D under plain faithfulness with possible latents. Any abstaining ledger's coverage claim must therefore be either:
- (a) asymptotic, conditional on stated assumptions;
- (b) empirical calibration on a stated benchmark distribution, with exchangeability at the scenario level (dom08: n = 25 scenarios gives 1/26 granularity); or
- (c) backed by interventions or randomisation.

### F9. The strongest "limits" statements a report can make without overclaiming (item 5)

1. **The ceiling.** From observational data alone, with causal sufficiency and faithfulness, no method can identify more than the CPDAG. Every edge in an undirected chain component is a coin flip for any method that does not add assumptions (Meek 1995; Chickering 2002). On CausalArena semantic scenarios this ceiling is 0.957 directed F1 (project, measured).
2. **Exceeding the ceiling needs a named extra assumption.** Scoring above the CPDAG ceiling from data alone requires a functional-form restriction (LiNGAM, ANM, PNL, equal variances) or external order knowledge. Without a named assumption it is evidence of a benchmark regularity, not of identifiability (Peters et al. 2014; Peters & Buehlmann; Reisach et al. 2021).
3. **No uniform guarantee.** Under plain faithfulness, no causal-discovery procedure has a uniform finite-sample guarantee when time order is unknown or latents are possible. Guarantees at fixed n require stronger assumptions, such as strong or k-triangle faithfulness (Robins et al. 2003; Zhang & Spirtes 2003; Spirtes & Zhang 2014).
4. **Strong faithfulness often fails.** It is the usual price of finite-sample PC guarantees, and it fails for a large and growing share of linear-Gaussian parameterisations as p grows. At n = 1,000 and p = 20-40, some test errors are expected even on identifiable graphs (Uhler et al. 2013). Do not convert this into a predicted number of wrong edges.
5. **Order knowledge removes orientation, not selection.** With a correct causal order, orientation is solved and what remains has the same sample complexity as undirected selection, about q log(d/q) (Gao, Tai, Aragam; Shojaie & Michailidis). So "a few bits of order beat every method" is consistent with theory. It is a statement about where the difficulty lies, not a new limit.
6. **Tiers.** Correct tiers orient every cross-tier edge and keep CPDAG-style effect tools valid. They cannot orient fully shielded within-tier edges and cannot assert ancestry (Bang & Didelez 2023). With latents, FCI plus tiers is sound and complete (Andrews et al. 2020).
7. **Experiment cost.**
   - Full orientation from a CPDAG costs ceil(log2 omega) unbounded interventions in the worst case (Hauser & Buehlmann 2014).
   - With atomic interventions it costs at least a clique-size-based bound, which is tight up to a factor of 2 (Porwal et al. 2022).
   - Adaptive search costs O(log n) times the verification number, and no algorithm does better in the worst case (Choo et al. 2022).
8. **Effects.** Graphical criteria decide exactly whether an effect is identified in a CPDAG, MPDAG or PAG (Perković et al. 2018; Perković 2020; Jaber et al. 2019). Answering "not identifiable" with a set of possible values is therefore a theorem-backed output, not a hedge.
9. **Confidence.** No published method gives finite-sample, distribution-free coverage for CPDAG or PAG edge marks. Coverage results exist only for effects or orderings in identifiable restricted model classes, or asymptotically after selection. This is "not found by these searches"; the conformal search was not run.

## Typed table

The full typed table is in `AU3_theory_limits.json` (55 rows, with schema, `evidence_label`, `read_level`, `open_problems` and `sources` per row). Compact version:

| id | Q | R | W (short) | identifiable object | key result | rate / cost | impossibility / lower bound | reference |
|---|---|---|---|---|---|---|---|---|
| C01 | skeleton | D | causally sufficient, iid, acyclic; Markov + adjacency-faithfulness; nonparametric CI tests | skeleton (adjacencies) | Two DAGs are observationally equivalent iff they share skeleton and v-structures, so the skeleton is identified under faithfulness; PC is pointwise consistent. CPC (Ramsey et al.) needs only adjacency-faithfulness for correct adjacencies. | pointwise only under plain faithfulness (see C05); none (observational) | No uniformly consistent skeleton estimator under plain faithfulness when time order is unknown (Robins et al. 2003; Zhang & Spirtes 2003). | Verma & Pearl 1990 (UAI; arXiv 1304.1108); Ramsey, Zhang, Spirtes 2006 (UAI; arXiv 1206.6843) |
| C02 | orientation | D | causally sufficient, iid, acyclic; Markov + faithfulness (adjacency + orientation) | CPDAG (Markov equivalence class) | Meek rules R1-R3 applied to the pattern give the maximally oriented graph (Meek 1995, Thm 3); GES identifies the class in the large-sample limit when a perfect DAG map exists (Chickering 2002). | none for orientation per se; orientation errors propagate through R1-R3; none | Edges inside undirected chain components of the CPDAG are not identifiable from D under any sample size. | Meek 1995 (UAI; arXiv 1302.4972); Chickering 2002 (JMLR 3:507-554) |
| C03 | orientation | D | causally sufficient DAGs, uniform over classes | CPDAG size / share of compelled edges | Sizes of MECs can be counted for sparse DAGs with hundreds of nodes; most classes are 'half completed' (partly oriented) with small average size; sparse class sizes grow roughly exponentially in p. | n/a (population); n/a | Share of non-compelled edges is a hard ceiling for D-only orientation. | He, Jia, Yu 2015 (JMLR 16:2589-2609) |
| C04 | skeleton+orientation | D | Gaussian, causally sufficient, p = O(n^a), max neighbourhood q = O(n^{1-b}), nonzero partial correlations >= c_n with 1/c_n = O(n^d), d < b/2 | skeleton and CPDAG | PC recovers the skeleton (and the CPDAG) with probability 1 - O(exp(-C n^{1-2d})). | P(error) = O(exp(-C n^{1-2d})) under the c_n lower bound (a strong-faithfulness-type condition); none | The c_n condition fails with non-trivial probability for random parameters (C06). | Kalisch & Buehlmann 2007 (JMLR 8:613-636; arXiv math/0510436) |
| C05 | skeleton / effects | D | Markov + plain faithfulness; time order unknown and/or latent confounders | none uniformly | Under Markov + faithfulness, tests and estimators are pointwise but not uniformly consistent; no finite n guarantees approximate correctness, and no valid consistent confidence intervals exist. With an observed discrete confounder and known order, uniformly consistent tests exist. | no uniform rate exists; randomised experiment restores uniform consistency (Robins et al., Remark 3) | IMPOSSIBILITY: no uniformly consistent test/estimator/confidence map (Thms 1,3,4); extends to inferring time order (Thm 5); Gaussian case: no nontrivial uniformly consistent test (Thm 6). | Robins, Scheines, Spirtes, Wasserman 2003 (Biometrika 90(3):491-515); Zhang & Spirtes 2003 (UAI) |
| C06 | skeleton+orientation | D | linear Gaussian, causally sufficient; lambda-strong-faithfulness with lambda ~ sqrt(deg log p / n); edge weights uniform on [-1,1], unit error variances | CPDAG (if strong faithfulness holds) | The set of non-strong-faithful distributions has positive measure and is often large: lower bounds 1-(1-lambda)^{p-1} for trees, exponential in p^2 for cycles, in 2^p for bipartite K_{2,p-2}. Simulated 10-node DAGs (expected degree 2): share lambda-strong-unfaithful nearly 1 at lambda=0.1, ~0.9 at 0.01, ~0.7 at 0.001. | For the lower bound to vanish need p_n = o(sqrt(n/(deg log n))) (trees), o((n/(deg log n))^{1/4}) (cycles), o(log n) (bipartite); none | Authors conclude high-dimensional PC consistency 'seems rather unrealistic' under uniform parameters; even trees cannot have p >> n. | Uhler, Raskutti, Buehlmann, Yu 2013 (Ann. Statist.; DOI 10.1214/12-AOS1080; arXiv 1207.0547) |
| C07 | skeleton+orientation | D | linear Gaussian, causally sufficient; k-Triangle-Faithfulness (weaker than strong faithfulness) | CPDAG and identifiable structural coefficients | A uniformly consistent estimator of the MEC and of identifiable coefficients exists under Markov + k-Triangle-Faithfulness; strong faithfulness 'may be false with high probability'. | uniform consistency (no explicit rate in abstract); none | Robins et al. impossibility under plain faithfulness is the backdrop. | Spirtes & Zhang 2014 (Statist. Sci. 29(4); arXiv 1502.00829) |
| C08 | skeleton+orientation | D | no faithfulness assumed; categorical data | MEC (where learnable) | No algorithm converges for all networks; any algorithm achieving the best achievable mode of convergence must converge on all faithful networks, so assuming faithfulness is 'a requirement, not an option'. Sparsest-permutation methods are consistent under conditions strictly weaker than faithfulness. | n/a; none | No universally convergent learner exists. | Lin & Zhang 2020 (ALT, PMLR 117:554-582); Raskutti & Uhler (arXiv 1307.0366) |
| C09 | skeleton (CI testing) | D | nonparametric conditional independence | n/a (test validity) | A valid conditional independence test has no power against any alternative; finite-sample validity requires restricting the null (e.g. regression rate assumptions, as in the GCM). | rates only under assumptions on regression estimators; none | NO-FREE-LUNCH: every constraint-based guarantee inherits assumptions on the CI tests. | Shah & Peters 2020 (Ann. Statist.; DOI 10.1214/19-AOS1857; arXiv 1804.07203) |
| C10 | skeleton+orientation | D | high-dimensional sparse Gaussian (score-based) | CPDAG | GES and adaptively restricted GES (ARGES) are consistent in several sparse high-dimensional settings; simulations favour them over PC. | consistency (conditions in full text, not read); none |  | Nandy, Hauser, Maathuis 2018 (Ann. Statist. 46(6A); arXiv 1507.02608) |
| C11 | full graph | D | Bayesian networks, m variables, max in-degree k | DAG / structure (information-theoretic) | Exact structure recovery needs Omega(m) samples for non-sparse BNs and Omega(k log m + k^2/m) for sparse BNs. | LOWER BOUND Omega(k log m + k^2/m); none | Lower bound holds for any method. | Ghoshal & Honorio (arXiv 1601.07460; venue not confirmed) |
| C12 | full graph | D | linear, acyclic, non-Gaussian errors, no hidden confounders | full DAG (unique) | LiNGAM identifies the complete causal structure from observational data without a time order. | not in abstract; none | Gaussian errors -> back to MEC. | Shimizu, Hoyer, Hyvarinen, Kerminen 2006 (JMLR 7:2003-2030) |
| C13 | full graph | D | additive noise models (nonlinear f, additive noise), causal minimality, no hidden confounders | full DAG | Bivariate ANMs are identifiable except when a differential-equation condition fails (linear-Gaussian is the classic exception); restricted multivariate ANMs identify the DAG (Thm 27); nonlinear Gaussian ANMs identifiable (Cor 30). | no rate in what I read; none | Non-identifiable cases fall into five classes (Prop 22). | Hoyer et al. 2008 (NIPS 21); Peters, Mooij, Janzing, Schoelkopf 2014 (JMLR 15:2009-2053) |
| C14 | full graph | D | post-nonlinear model X2 = f2(f1(X1)+N), bivariate | causal direction | PNL is identifiable in most cases; the non-identifiable cases are enumerated. | n/a; none | Enumerated exceptional cases. | Zhang & Hyvarinen 2009 (UAI; arXiv 1205.2599; PMLR r7) |
| C15 | full graph | D | linear Gaussian SEM with equal (or known-ratio) error variances | full DAG | Equal error variances make the DAG identifiable (Peters & Buehlmann); with error variances known up to a constant, the true DAG uniquely minimises a reweighted l2 score (Loh & Buehlmann). Optimal sample complexity n ~ q log(d/q). | minimax n ~ q log(d/q) (Gao et al. Thms 2.1, 3.1); none | Lower bound max{log d / beta_min^2, q log(d/q)/(M^2-1)} (Gao et al. Thm 3.1). | Peters & Buehlmann 2014 (Biometrika; arXiv 1205.2536); Loh & Buehlmann 2014 (JMLR 15:3065-3105); Gao, Tai, Aragam (arXiv 2201.10548) |
| C16 | full graph | D+K (total causal order) | linear (Gaussian or not), known topological order, sparse | full DAG (parent selection only) | With the order known, DAG estimation reduces to per-node variable selection; adaptive lasso is consistent; best-subset selection attains n ~ q log(d/q) with a matching lower bound (Gao et al. Props 4.1-4.2). | n ~ q log(d/q), same as undirected graphical-model selection; none | Lower bound matches (Prop 4.2). | Shojaie & Michailidis 2010 (Biometrika 97(3):519-538); Gao, Tai, Aragam (arXiv 2201.10548, Sec. 4) |
| C17 | orientation | D+K (required/forbidden directed edges) | causally sufficient, faithfulness, knowledge correct | MPDAG (maximally oriented PDAG) | Meek rules R1-R4 after imposing the knowledge give the maximally oriented graph (Meek 1995, Thm 4); MPDAGs support reading possible ancestry, an adjustment criterion and IDA; effects become more identifiable with more knowledge (simulation). | n/a (population); none | Knowledge inconsistent with the CPDAG is not handled. | Meek 1995 (UAI; arXiv 1302.4972); Perkovic, Kalisch, Maathuis 2017 (UAI; arXiv 1707.02171) |
| C18 | orientation | D+K (tiers / temporal partial order) | causally sufficient, faithfulness, correct tiers | tiered MPDAG | All cross-tier edges are directed; only Meek R1 is needed to complete; result is a chain graph with chordal components so CPDAG adjustment and IDA apply unchanged; fully shielded within-tier edges stay undirected; tiers give absence, never presence, of ancestral relations; earlier knowledge is more informative. | n/a; none | A complete subgraph inside one tier cannot be oriented by tiers (Example 5). | Bang & Didelez 2023 (UAI, PMLR 216:119-129; arXiv 2306.01638) |
| C19 | orientation / effects | D+K (pairwise direct, ancestral, non-ancestral) | causally sufficient | causal MPDAG + residual direct causal clauses | Any pairwise causal knowledge set decomposes uniquely into a causal MPDAG plus a minimal residual set of direct causal clauses; consistency/equivalence checks are polynomial; effect identifiability depends only on the MPDAG (necessary and sufficient condition). | n/a; none |  | Fang, Zhao, Liu, He 2025 (JMLR 26:229); Fang & He 2020 (UAI, PMLR 124:270-279) |
| C20 | full graph | D+K (partial orders) | differentiable structure learning | graph consistent with the partial order | Partial orders are mapped to equivalent graph-space constraints with claimed correctness and completeness; reported 90% fewer samples on one real dataset. | empirical only; none |  | Ban et al. 2024 (NeurIPS 2024 poster) |
| C21 | orientation | D+K (tiers) | latent confounders allowed (FCI) | PAG refined by tiers | FCI with tiered background knowledge is sound and complete; for other knowledge types it is not known when FCI stays complete. Local background knowledge also has sound and complete rules (Wang, Qin, Zhou). | n/a; none | Completeness of FCI under general (non-tiered) knowledge is open. | Andrews, Spirtes, Cooper 2020 (AISTATS, PMLR 108:4002-4011); Wang, Qin, Zhou 2022 (NeurIPS 35) |
| C22 | orientation | D | latent confounders and selection bias, acyclic, Markov + faithfulness | PAG (MAG equivalence class) | FCI with added rules is complete: it recovers every feature uniquely determined by conditional independence facts; Zhang's tail rules complete the MAG-equivalence commonalities. | uniform consistency impossible (C05); none | No uniformly consistent procedure (Robins et al. 2003). | Zhang 2008 (Artificial Intelligence 172(16-17):1873-1896); Zhang (arXiv 1206.5282) |
| C23 | full graph | D | linear non-Gaussian with latent confounders | finite set of models | With latent confounders uniqueness is lost but at most a finite set of models fits the data. | n/a; none | Non-uniqueness. | Hoyer, Shimizu, Kerminen 2006 (arXiv cs/0603038) |
| C24 | skeleton (selection) | D | selection bias, parametric and non-parametric families | presence of selection bias | Conditions under which selection bias is identifiable from observational data are given, with tests for its presence. | n/a; none |  | Kaltenpoth & Vreeken 2023 (AAAI 37(7):8177-8185) |
| C25 | orientation | D+I (hard, known targets) | causally sufficient, faithfulness | I-essential graph (interventional MEC) | Interventional equivalence partitions DAGs more finely than observational; each class is represented by a chain graph (I-essential graph); GES generalises (GIES). | large-sample; see C29-C34 |  | Hauser & Buehlmann 2012 (JMLR 13:2409-2464) |
| C26 | orientation | D+I (soft/general, known targets) | causally sufficient | general-intervention I-MEC | Characterises the I-MEC identifiable from general (not necessarily perfect) interventions and gives a provably consistent algorithm. | consistency |  | Yang, Katcoff, Uhler 2018 (ICML, PMLR 80:5541-5550) |
| C27 | orientation | D+I (unknown targets) | causally sufficient, nonparametric | I-MEC with unknown targets | Characterises the class identifiable from mixed observational/interventional data with partly or fully unknown targets; consistent permutation search (UT-IGSP). JCI handles unknown targets/types by context variables. | consistency |  | Squires, Wang, Uhler 2020 (UAI, PMLR 124:1039-1048); Mooij, Magliacane, Claassen 2020 (JMLR 21:99) |
| C28 | orientation | D+I (soft, unknown targets) | latent confounders allowed | Psi-PAG | Psi-Markov property; graphical equivalence test via augmented MAGs (skeleton, unshielded colliders, discriminating paths); Psi-FCI sound and complete in the sample limit. | sample limit only |  | Jaber, Kocaoglu, Shanmugam, Bareinboim 2020 (NeurIPS 33) |
| C29 | experiment design | I (worst case, no prior D) | causally sufficient, acyclic, no selection | full DAG | With unrestricted simultaneous randomisation, log2(N)+1 experiments are sufficient and in the worst case necessary; single-variable experiments need N-1. | log2(N)+1 multi-target; N-1 single-target | worst-case necessary | Eberhardt, Glymour, Scheines 2005 (UAI; arXiv 1207.1389) |
| C30 | experiment design | D+I (start from CPDAG / I-essential graph) | causally sufficient | full DAG | ceil(log2 omega(G)) unbounded-size targets suffice and are worst-case necessary, omega = largest clique of undirected components (proves Eberhardt's conjecture); OptUnb finds them in polynomial time; a greedy single-vertex strategy is also given. | ceil(log2 omega) | worst-case necessary | Hauser & Buehlmann 2014 (IJAR; DOI 10.1016/j.ijar.2013.11.007; arXiv 1205.4174); Eberhardt 2008 (UAI; arXiv 1206.3250) |
| C31 | experiment design | D+I (size-k interventions) | causally sufficient, chordal skeleton | full DAG | Any deterministic adaptive algorithm must be a separating system on complete graphs in the worst case; near-optimal separating systems; adaptive algorithm on chordal skeletons is an alpha-approximation (alpha = independence number). | separating-system size | information-theoretic lower bound also for randomized adaptive | Shanmugam, Kocaoglu, Dimakis, Vishwanath 2015 (NIPS; arXiv 1511.00041) |
| C32 | experiment design | D+I (atomic) | causally sufficient | full DAG | Universal lower bound: at least the sum over chain components of half the largest clique size; DCT policy within a log factor (in number of maximal cliques) of optimal; an improved universal lower bound within factor 2 of optimal. | atomic: >= sum_i ceil(omega_i/2)-type bound | LOWER BOUND, within factor 2 of optimum | Squires et al. 2020 (arXiv 2011.00641; venue not confirmed); Porwal, Srivastava, Sinha 2022 (AISTATS, PMLR 151:5583-5603) |
| C33 | experiment design | D+I (adaptive search vs verification) | causally sufficient | full DAG | Minimal verifying set characterised via covered edges; separator-based adaptive search uses O(log n) times the verification number, which is tight (Omega(log n) on some graphs); O(log n log k) for size-k interventions. | O(log n) x verification number | Omega(log n) worst-case ratio | Choo, Shiragur, Bhattacharyya 2022 (NeurIPS 2022; arXiv 2206.15374) |
| C34 | experiment design | D+I (orient a target subset of edges) | causally sufficient | target edges only | Subset verification computable efficiently; for subset search no algorithm beats a ratio of the target edges' vertex cover in the worst case. | subset verification number | vertex-cover-sized gap is unavoidable | Choo & Shiragur (arXiv 2301.03180; venue not confirmed) |
| C35 | experiment design | D+I (costs / budgets) | causally sufficient | full DAG / expected oriented edges | Minimum-cost intervention set identifying any DAG with a given skeleton is polynomial-time; with a capped number, poly-time for trees/clique trees, greedy for chordal. Budgeted k single-target non-adaptive design: objective (expected oriented edges) is submodular, greedy gives (1-1/e). | cost-optimal / (1-1/e) of best k |  | Kocaoglu, Dimakis, Vishwanath 2017 (ICML, PMLR 70:1875-1884); Ghassami, Salehkaleybar, Kiyavash, Bareinboim 2018 (ICML, PMLR 80:1724-1733) |
| C36 | experiment design | D+I | latent variables allowed | full causal graph with latents | O(d log^2 n + d^2 log n) interventions learn the graph with latents (d = degree), versus O(n^2) naive. | O(d log^2 n + d^2 log n) |  | Kocaoglu, Shanmugam, Bareinboim 2017 (NIPS 30) |
| C37 | full graph / experiment design | D+I | linear cyclic with latent variables | full linear cyclic model | Necessary and sufficient conditions on the set of experiments for identifiability are given. | set of experiments satisfying the paper's condition (not read) |  | Hyttinen, Eberhardt, Hoyer 2012 (JMLR 13:3387-3439) |
| C38 | full graph (lagged) | D (time series) | Granger: complete system, no unmeasured confounders, no instantaneous effects, sampling at causal lag, no measurement error | lagged graph (Granger graph) | Granger causality assesses predictiveness; it matches causal structure only under the listed assumptions, which the review calls unverifiable and unlikely to hold together; sub-sampling can make effects unidentifiable and create spurious ones. |  | Omitted variables can reverse Granger conclusions (review's simulation). | Shojaie & Fox 2022 (Annu. Rev. Stat. Appl. 9:289-319; arXiv 2105.02675) |
| C39 | full graph (lagged + contemporaneous) | D (time series) | causal sufficiency, Markov, faithfulness, stationarity | lagged parents (PCMCI); lagged + contemporaneous MEC (PCMCI+) | PCMCI is consistent for lagged links with no contemporaneous effects; finite-sample false-positive control is empirical. PCMCI+ handles contemporaneous links, order-independent and oracle-consistent. | no finite-sample guarantee |  | Runge et al. 2019 (Sci. Adv.; arXiv 1702.07007); Runge 2020 (UAI; arXiv 2003.03685) |
| C40 | orientation | D (time series) | latent confounders, autocorrelation | time-series PAG | LPCMCI is order-independent and sound and complete in the oracle case, with much higher recall than FCI variants on autocorrelated data; SVAR-FCI style methods allow contemporaneous relations and latent processes. | oracle only |  | Gerhardus & Runge 2020 (NeurIPS 33); Malinsky & Spirtes 2018 (KDD workshop, PMLR 92:23-47) |
| C41 | full graph | D (time series) | restricted SEMs (independent noise, e.g. additive) or non-Gaussian SVAR | full summary/instantaneous graph | TiMINo identifies lagged and instantaneous effects, possibly nonlinear and unfaithful, and non-instantaneous feedback; non-Gaussian SVAR is identifiable without prior structure knowledge. |  |  | Peters, Janzing, Schoelkopf 2013 (NIPS 26); Hyvarinen, Zhang, Shimizu, Hoyer 2010 (JMLR 11:1709-1731) |
| C42 | full graph | D (subsampled time series) | measurement slower than causal timescale | set of system-timescale structures consistent with data | Constraint satisfaction/optimisation recovers system-timescale structures consistent with the measured-timescale graph, robust to statistical conflicts. |  | Generally not unique (equivalence set; details not read). | Hyttinen, Plis, Jarvisalo, Eberhardt, Danks 2016 (PGM, PMLR 52:216-227) |
| C43 | orientation | D+K (summary causal graph) | time series, causally sufficient, faithful | micro-level orientations | Conditions under which micro-level edges can be oriented using a summary causal graph, including macro-level cycles or bidirected edges. |  |  | Loranchet & Assaad (arXiv 2508.21742; 2025-2026 preprint) |
| C44 | orientation | D (cycles) | simple SCMs with feedback, sigma-faithfulness | PAG (cyclic interpretation) | FCI output stays correct with feedback: sound and complete for observational data from simple sigma-faithful SCMs; consistent for presence/absence of (direct) causal relations, absence of confounders and of specific cycles. Cyclic SCMs may lack solutions or unique distributions unless solvability holds. |  | Cyclic SCMs need not satisfy a Markov property without solvability. | Mooij & Claassen 2020 (UAI; arXiv 2005.00610); Bongers, Forre, Peters, Mooij 2021 (Ann. Statist. 49(5)) |
| C45 | full graph | D (cycles) | linear non-Gaussian, causally sufficient, cyclic | distribution-equivalence class of SEMs | LiNG-D outputs the distribution equivalence class; under sufficient conditions only one member is stable. |  | Non-unique in general. | Lacerda, Spirtes, Ramsey, Hoyer 2008 (UAI; arXiv 1206.3273) |
| C46 | full graph | D (mixed) | linear mixed continuous/discrete (LiM); ordinal + exponential family linear models | full DAG (restricted models) | LiM is identifiable under sufficient conditions; for ordered-logit and one-parameter exponential-family nodes, every ordinal-to-EF edge direction is identifiable given >=3 categories and >=3 support points, both necessary. |  | Necessity of the 3-category / 3-point conditions (Mishra & Mitra). | Zeng, Shimizu, Matsui, Sun 2022 (CLeaR, PMLR 177:994-1009); Mishra & Mitra (arXiv 2609.17942, Sept 2026 preprint) |
| C47 | effects P(Y/do(X)) | D | linear Gaussian (IDA) / nonparametric (adjustment); causally sufficient | multiset of possible effects; identification status per (X,Y) | IDA returns one effect per allowed parent set of X (min /effect/ is a lower bound); the generalized adjustment criterion is sound and complete for DAGs, CPDAGs, MAGs, PAGs; an optimal (minimum asymptotic variance) adjustment set exists for linear models in DAGs/CPDAGs/MPDAGs. | IDA high-dim consistency (conditions not read) | Effect not identifiable when X has undirected edges whose orientation changes the parent set. | Maathuis, Kalisch, Buehlmann 2009 (Ann. Statist. 37(6A); arXiv 0810.4214); Perkovic, Textor, Kalisch, Maathuis 2018 (JMLR 18:220); Henckel, Perkovic, Maathuis 2022 (JRSSB; arXiv 1907.02435) |
| C48 | effects P(Y/do(X)) | D+K | MPDAG (CPDAG + background knowledge), no latents | identified effect or set | Necessary and sufficient identification criterion in MPDAGs, generalising the g-formula/truncated factorisation; strictly stronger than generalized adjustment. Local IDA with direct-causal knowledge; tiered MPDAGs keep CPDAG adjustment and IDA unchanged. |  |  | Perkovic 2020 (UAI, PMLR 124:530-539); Fang & He 2020 (UAI); Bang & Didelez 2023 (Cor 2-3) |
| C49 | effects P(Y/do(X)) | D | latent confounders (PAG) | identified expression or proof of non-identifiability; bounds | Complete identification algorithm given a PAG (returns an expression or certifies non-identifiability). LV-IDA returns multisets with NA where confounding cannot be ruled out; min/max bound the effect when identifiable. | LV-IDA sim, 15 vars: MSE 0.022 vs IDA 0.056; 12.7% NA (reported) | With latents, no uniformly consistent effect estimator or CI (Robins et al. 2003). | Jaber, Zhang, Bareinboim 2019 (ICML, PMLR 97:2981-2989); Malinsky & Spirtes 2016 (CMU tech report 194 / PGM 2016) |
| C50 | graph-feature confidence | D | any (resampling) | per-feature frequency (edge, direction-given-presence) | Bootstrap frequencies rank features but are not calibrated probabilities; Bayesian model averaging over orders gives posterior feature probabilities; BCCD and ACI attach reliability/confidence to causal statements. | plain bootstrap ECE ~0.07-0.08 (second-hand, project note cluster6, Banerjee et al. 2025) | No coverage or calibration guarantee; posterior validity depends on model and prior. | Friedman, Goldszmidt, Wyner 1999 (UAI; arXiv 1301.6695); Friedman & Koller 2000 (UAI; arXiv 1301.3856); Claassen & Heskes (arXiv 1210.4866); Magliacane, Claassen, Mooij 2016 (NIPS 29) |
| C51 | skeleton (error control) | D | PC with CI tests | edge-wise p-values; FDR across edges | PC-p computes edge-specific p-value upper bounds and controls FDR across edges with Benjamini-Yekutieli. |  |  | Strobl, Spirtes, Visweswaran 2019 (ACM TIST 10(5) per index; arXiv 1607.03975) |
| C52 | orientation / effects (coverage) | D | linear equal-variance or identifiable additive-error SEMs | confidence sets of orderings / effects including structure uncertainty | Test inversion gives confidence regions for effects covering structure uncertainty (two-step intervals are over-optimistic); residual-bootstrap confidence sets of causal orderings are asymptotically valid and yield sub/supersets of ancestral relations. | asymptotic (1-alpha) | Naive bootstrap fails (non-smoothness) per Strieder & Drton (second-hand, cluster3). | Strieder, Freidling, Haffner, Drton 2021 (UAI); Strieder & Drton 2023 (J. Causal Inference); Wang, Kolar, Drton (arXiv 2305.14506) |
| C53 | effects after discovery | D | Gaussian DAGs, PC / constraint-based | valid CI for effect after selecting graph | Double dipping inflates miscoverage; resampling-and-screening over perturbed PC runs gives asymptotically correct coverage for the fixed population effect; Gradu et al. give valid post-discovery inference beating data splitting. | asymptotic coverage |  | Chang, Guo, Malinsky (arXiv 2405.06763); Gradu, Zrnic, Wang, Jordan (arXiv 2208.05949; JASA 120(550) per RePEc) |
| C54 | effects (conformal) | D+K (LLM edge prior) | identification, overlap, posterior concentration | marginal coverage of aggregated pseudo-outcome | Conformal guarantee covers a posterior-weighted pseudo-outcome over candidate DAGs, not the effect or the graph; effect coverage is empirical (>90% on five benchmarks). | finite-sample marginal (pseudo-outcome only) |  | Singh et al. (CausalGuard, arXiv 2605.21928, May 2026 preprint) |
| C55 | orientation (interventions, large graphs) | D+I (single-variable random) | epsilon-interventional faithfulness, latents allowed, random ER / scale-free graphs | orientation of true edges | False-negative rate concentrates at O(log d / sqrt(d)) on sparse ER DAGs. | O(log d / sqrt(d)) concentration; single-variable random interventions |  | Chevalley, Mehrjou, Schwab (arXiv 2511.02536, Nov 2025 preprint) |

## What this changes for the project

1. **Use theorem names, not slogans.** The report's "limits" layer (Atlas back slabs) should use F9 items 1-9 verbatim in substance. Each item has a citation and avoids "100%" or "provably optimal" claims for the ledger.
2. **The claim ledger's evidence types match the theory's evidence types.** The theory supports five source types:
   - CPDAG-compelled (D, C02);
   - functional-form-identified (D plus a named W restriction, C12-C15);
   - knowledge-implied (D+K via Meek R1-R4, tiers or direct causal clauses, C17-C19);
   - intervention-implied (D+I, I-essential graph, C25-C28);
   - undecided.
   
   The ledger should store which theorem licenses each mark. A mark licensed only by name semantics is "declared knowledge" and inherits Meek-closure consequences, so one wrong declaration propagates. That is the reason to store closure provenance.
3. **Store ancestral knowledge separately.** Fang et al. (JMLR 2025) show that ancestral and non-ancestral statements are not reducible to edge orientations. A field such as `residual_clauses` should hold them, because forcing them into edges loses information.
4. **Keep "never below data-only output" as an engineering invariant only.** Robins et al. rule out uniform finite-sample guarantees for D-only marks. The ledger's coverage claims should be empirical (scenario-level calibration, dom08) or interventional, and the report should say so (F8).
5. **Split the CausalArena gap into three parts.** The gap between 0.957 (identifiability) and PC 0.333 is mostly statistical: skeleton F1 0.611 and orientation errors. Uhler et al. and the Kalisch-Buehlmann conditions explain why this is expected at n = 1,000. The error budget should keep three terms:
   - identifiability loss (about 4%);
   - finite-sample loss (strong-faithfulness and CI-test errors);
   - algorithmic loss.
   
   Cluster8 noted that no benchmark reports this split.
6. **For the what-if question (BLD-07),** return the identification status per (X, Y) using Perković 2020 (MPDAG) or Jaber 2019 (PAG), plus the IDA or LV-IDA set when not identified. This is complete in theory and cheap (dom09).
7. **For active design (cluster7 / dom10),** the right baselines and bounds are ceil(log2 omega) (OptUnb), the Squires/Porwal atomic lower bound, and the Choo O(log n) search bound. An LLM agent's experiment count can be scored as a ratio to the verification number (C33), a cleaner metric than F1 after k rounds.
8. **Hidden confounders, time series and cycles (DOM-12 scope)** each change the identifiable object (PAG, time-series PAG, sigma-faithful PAG or distribution-equivalence class). A Q2 extension must score against that object, not against the DAG truth. This matches the scope note's point that the repo's scorer orients undirected edges from the truth.

## Open questions

- No result found for the finite-sample rate of orientation (as opposed to skeleton) recovery, or for how often orientation-faithfulness fails at n = 1,000 and p = 20-40. This could be measured on our suites.
- Erroneous background knowledge with guarantees: Bang & Didelez leave inconsistency handling to future work, and Andrews et al. say FCI completeness for non-tiered knowledge is open. Chen et al.'s quasi-circle detection (cluster3) is the nearest result.
- Coverage for CPDAG/PAG marks: is there a conformal or e-value construction over equivalence-class features? Not searched (budget); cluster9 also found none.
- Question-targeted experiment design for effects (not full orientation): Choo & Shiragur (subset search) and ABCD (cluster7) are the nearest results.
- Exact constants in the Squires et al. 2020 lower bound, and the bounded-k Eberhardt formula, need a full-text read.

## Not read

- **Verma & Pearl 1990:** full text not read; the skeleton+v-structure criterion is not confirmed verbatim from the abstract.
- **Not opened:** Andersson-Madigan-Perlman 1997; Richardson & Spirtes 2002; Ali-Richardson-Spirtes 2009; Spirtes-Glymour-Scheines (book); Kocaoglu-Jaber-Shanmugam-Bareinboim 2019.
- **https://pmc.ncbi.nlm.nih.gov/articles/PMC5305170:** reCAPTCHA page returned.
- **Mixed-data CI and score methods** (copula PC; Andrews-Ramsey-Cooper): not looked up, search budget exhausted.
- **Conformal methods over graph structure** beyond CausalGuard: planned extended search not run, shared web-search budget exhausted.
- **Abstract-level only (exact conditions and constants unchecked):** Nandy et al. 2018; Squires et al. 2020; Kocaoglu et al. ICML 2017; Shanmugam et al. 2015; Strieder & Drton 2023; Malinsky & Spirtes 2018; PCMCI+.
- **Eberhardt et al. 2005 bounded-k bound:** the abstract extraction was garbled ("0 < K < 1/(2N)"); not re-read.
- **Venues not confirmed on a page I opened:** Raskutti & Uhler; Ghoshal & Honorio; Gao-Tai-Aragam; Choo & Shiragur 2023; Wang-Kolar-Drton; Squires et al. 2020; Chang-Guo-Malinsky.

## Searches run

The full list is in the JSON `searches` field: 34 WebSearch queries, the last of which was refused (budget), plus WebFetch of about 70 primary pages. Rows whose sources came from prior notes rather than these searches are marked second-hand.

**Where we're going:** the next steps are AU0 synthesis and the error budget.
- Adopt the three-term error budget in item 5.
- Adopt the per-mark "licensing theorem" field in item 2.
- Read the full text of Perković 2020 and Jaber et al. 2019 before the what-if module is specified.
- Run the conformal-structure search in a fresh turn.
