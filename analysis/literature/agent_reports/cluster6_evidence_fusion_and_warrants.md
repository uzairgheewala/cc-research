**Where we are now:** literature check done for all five questions. Direct downloads were blocked, so every primary page was read through a fetch tool. **V** = primary page opened (through a page summariser); **Vq** = verbatim text seen in a raw extract; **A** = snippet or memory.

## (a) Most relevant works

| Work | Fuses | Output / confidence | Max vars | Code | Notes |
|---|---|---|---|---|---|
| Hyttinen, Eberhardt, Järvisalo 2014, UAI ([pdf](https://www.auai.org/uai2014/proceedings/individuals/87.pdf)) | Weighted (in)dependence constraints in ASP; cycles and latents; experimental data in supplement | Single min-violation graph; weights constant, hard-dependence, or Bayesian log-odds; no per-claim score (V) | 6 simulated; "up to seven" (V) | "From authors' websites"; upkeep unverified | MaxSAT successor: Hyttinen, Saikko, Järvisalo, [IJCAI 2017](https://www.ijcai.org/proceedings/2017/90); scale not verified |
| Claassen & Heskes 2012 (BCCD), UAI, [1210.4866](https://arxiv.org/abs/1210.4866) | Bayesian reliability of input statements | Single model, decisions flagged by reliability (V) | Not verified | Not verified | |
| Triantafillou & Tsamardinos 2015 (COmbINE), JMLR 16, [1403.2150](https://arxiv.org/abs/1403.2150) | Overlapping variable sets, multiple interventions, SAT | Summary graph of invariant/variant features; conflicts resolved by p-value-ranked confidence (V) | "Up to 100 variables for relatively sparse networks" (V) | Not found | |
| Magliacane, Claassen, Mooij 2016 (ACI), NeurIPS (venue A), [1606.07035](https://arxiv.org/abs/1606.07035) | CI tests, single-known-target interventions, background knowledge | **Scored ancestral claims**: C(f) = min-loss(¬f) − min-loss(f); input weights from p-values or Bayesian (V) | Synthetic n=6–9; Sachs 11 proteins (V) | [caus-am/aci](https://github.com/caus-am/aci), 15 commits, BSD-2 (V); last-commit date not seen | Closest classic precedent for scored claims |
| Mooij, Magliacane, Claassen 2020 (JCI), JMLR 21, [1611.10351](https://arxiv.org/abs/1611.10351) | Pooled contexts plus context variables | Framework; bootstrapping used for most implementations (V) | ASD-JCI: 4 system + ≤4 context (Vq) | Not verified | |
| Russo, Rapberger, Toni 2024, KR, [2405.11250](https://arxiv.org/abs/2405.11250) | CI tests as defeasible assumptions, strength from p-value and conditioning-set size (Vq) | DAGs as stable extensions | "Cannot process more than 10 variables" (Vq) | [ArgCausalDisco](https://github.com/briziorusso/ArgCausalDisco), 175 commits (V) | No interventions, no LLM |
| Li & Russo 2026, UAI (PMLR 337:3631–3667), [2602.16481](https://arxiv.org/abs/2602.16481) | CI tests plus LLM required/forbidden arrows (hard, 5-run consensus); a required arrow is dropped if data removed its skeleton edge (V) | Single DAG; no per-claim confidence; SHD/F1/SID only (V) | 15 nodes, CauseNet-grounded random DAGs (Vq); bnlearn sizes unverified | "Our repository", no URL seen | Claims it "exposes the provenance of inferred edges" (Vq) as a possibility; anonymising "would remove the signal" (Vq); observational only |
| Russo, Mazzotta, Dodaro, Ricca, Toni 2026, LINDA workshop ([slides](https://linda-workshop26.cs.uni-paderborn.de/wp-content/uploads/2026/08/OptABAPC_LINDA26_Russo.pdf)) | CI facts with release costs | Min-cost correction set, unique DAG (V, slides only) | 5–8 nodes; "does not scale" (V) | — | Nearest thing to "which inputs must be retracted", but global, not per-claim |
| Kitson & Constantinou 2026, [2608.27472](https://arxiv.org/abs/2608.27472) | Structure-learning ensembles plus 3 LLMs, fixed 50/50 average | Per-edge distribution over states; "We do not assess probability calibration" (Vq) | 26 networks, 8–70 nodes (Vq) | None seen | Obfuscated-name audit, LLM-judged and inconclusive (V); no interventions, no provenance |
| Zheng, Verma, Gill, Dai, Spirtes, Zhang 2026, [2606.23608](https://arxiv.org/abs/2606.23608) | Deliberately none: agents must not supply edges or priors | causal-learn+ platform; "provenance… is part of what a graph mark means" (Vq) | Big Five case study only (V) | Hosted site only | Logs run-level choices; audit trails are future work (Vq); no per-mark derivation |
| Thorat et al. 2026 (GENESIS), [2608.03868](https://arxiv.org/abs/2608.03868) | CI/BIC/ANM scores, Markov-blanket agreement, Judge LLM | DAG with "explicit, auditable justification" per edge (Vq) | 5 small bnlearn nets; Child = 20 nodes (A) | None seen | Justification can be LLM free text; no checker, no sensitivity, observational |
| Peng et al. 2026 (CauScientist), [2601.13614](https://arxiv.org/abs/2601.13614) | LLM edits accepted only if intervention-aware BIC improves | DAG; data can overrule LLM (V) | Alarm, 37 (V) | [repo](https://github.com/OpenCausaLab/CauScientist) | Uses interventional data; no name control, no calibration |

Other LLM-plus-data work opened:
- **CauTion** ([2606.03602](https://arxiv.org/abs/2606.03602)): up to 76 nodes; no guarantee, no name control (V).
- **MosaCD** ([2509.23570](https://arxiv.org/abs/2509.23570)): up to 76 nodes; seeds dropped if they contradict CI; no calibration (V).
- **Clivio et al., Learning to Defer** ([2502.13132](https://arxiv.org/abs/2502.13132)): bivariate only (V).
- **Long et al. 2023** ([2307.02390](https://arxiv.org/abs/2307.02390)): abstract verified; the probabilistic guarantee I recall is A.
- **Uehara 2026** ([2605.27477](https://arxiv.org/abs/2605.27477)): "per-edge impossibility certificates" as discrete codes, human oracle, up to 37 variables; single-author preprint with internally inconsistent numbers (V).
- **Srivastava et al.** ([2510.16530](https://arxiv.org/abs/2510.16530)): post-cutoff benchmark graphs plus LLM priors for PC (V, abstract).

**Q3, calibration.** No fusion paper I opened reports ECE or Brier for fused edges. Kumar et al. ([2608.23660](https://arxiv.org/abs/2608.23660)) report both, but for LLM-only edge judgments on graphs up to 186 nodes (V). I found no conformal or e-value method for LLM-assisted discovery; the one conformal hit ([2603.02204](https://arxiv.org/abs/2603.02204)) has no LLM.

**Q5, bootstrap calibration.** The evidence is mixed:
- **Debeire et al., CLeaR 2024** ([2306.08946](https://arxiv.org/abs/2306.08946)): bagged PCMCI+ frequencies track a reference frequency but overestimate in the 40–60% range; "more research is needed" (V).
- **Naeini, Jabbari, Cooper 2017** (workshop): RFCI bootstrap "usually well-calibrated for directed edge types", 500–1000 nodes (V).
- **Kummerfeld & Rix 2019** ([1910.02047](https://arxiv.org/abs/1910.02047)): GES bootstrap underconfident on linear-Gaussian, overconfident on Hepar2 and Child (V).
- **Banerjee, Andrews, Kummerfeld 2025** ([2503.15436](https://arxiv.org/abs/2503.15436)): plain bootstrap persistently miscalibrated (ECE about 0.07–0.08); effective-sample-size adjustment helps (V).
- **Jabbari et al. 2017** ([1712.08626](https://arxiv.org/abs/1712.08626)): post-hoc calibration needs a labelled calibration set (V).
- **Stekhoven et al. 2012 (CStaR)**: not opened (A).

## (b) Not found, as far as this search reached
- No system emits a machine-checkable derivation per edge mark or ancestral claim. Li & Russo assert traceability; GENESIS tags a source; neither has a checker.
- No per-claim sensitivity ("which inputs must flip to retract this"). The correction-set slides are global and stop at 8 nodes.
- No single system fuses CI tests, interventional contrasts and labelled, weighted LLM priors. ACI does the first two plus background knowledge; Li & Russo do CI plus hard LLM constraints; CauScientist does LLM plus interventional BIC without logic.
- No logic or argumentation method demonstrated at 20–40 variables (ceilings: about 9, 10, 15).
- No calibration metrics on fused claims; no column-order leak control anywhere.

## (c) Biggest threats to the novelty claim
1. **Li & Russo, UAI 2026** (with the Causal ABA line and correction sets). Same architecture family, an explicit provenance claim, and a memorisation protocol. Open ground: scale beyond 15, interventions, weighted LLM priors, emitted and checked warrants, name-removed evaluation.
2. **Kitson & Constantinou 2026.** Already holds the 8–70-node public-benchmark slot with obfuscated names and per-edge probabilities. It has no warrants, calibration, interventions, or way for data to overrule the LLM.
3. **GENESIS and Zheng et al. 2026.** They own the "auditable/traceable/provenance" vocabulary. Zheng et al. argue LLM priors should not enter at all, so labelled priors need an explicit defence. ACI means "fusion into scored ancestral claims" is not new by itself.

**Could not verify:** last-commit dates and maintenance for every repo; HEJ, JCI and COmbINE code locations; bnlearn graph sizes in Li & Russo; the Long et al. guarantee; CStaR details; GENESIS variable counts. Anything newer than these search hits may be missed.

**Where we're going:** the defensible claim is the conjunction (checked warrants, three evidence types, 20–40 variables, leak controls), positioned against Li & Russo and Kitson & Constantinou. Worth saving to the research ledger: ACI's scoring formula as the baseline for claim confidence, and the mixed bootstrap-calibration evidence.
