# Quarter 1 checkpoint (due Fri 6 Nov 2026): the auditor paper's title, abstract, introduction and code link

Tickets: DLV-05 (checkpoint, W1), DLV-07 (public Q1 repository), DLV-11 (benchmark audits, cited), DLV-06 (final, 4 Dec),
PRG-01 (framing). Re-cut 31 Oct by W1 to program v3 (`claude/program-v3-2026-10-29.md`, section 2): the Q1 paper is the
auditor paper. The earlier outline (27 Oct) framed Q1 as a controlled replication of Causal-Copilot's review step; that
framing now appears as the worked case inside the audit, and refinement v2 belongs to the Q2 paper.

Status: **drafted and compiled.** The source of truth is `docs/paper/q1/` (design: `docs/paper/q1/DESIGN.md`):

| File | What it is |
|---|---|
| `report.tex` | the checkpoint in the course template (title, abstract, introduction, prior work, data, code link, appendix A) |
| `numbers.json` → `numbers.tex`, `numbers_table.tex`, `numbers.lock.json` | every number, with its result file and JSON pointer (`build_numbers.py`) |
| `lit_claims.json`, `reference.bib`, `verify/` | every citation: the claim, the passage read, the verdict of a checker who did not write it |
| `data_facts.md` | licences and citations of the data, checked on the licensor's page |
| `lint_report.py` | fails on any numeral not printed through `\nm{key}`, and on any prior-work sentence without `\cite` or `\ours` |
| `build/report.pdf` | the compiled PDF (XeLaTeX; CTAN `econ.bst` stands in for the template's `dsc180bibstyle.bst`) |

What the course asks for (dsc-capstone.org/2026-27/assignments/projects/q1, read 27 and 30 Oct):
- **Report, graded by the mentor:** title, abstract and introduction (an introductory paragraph, a literature review and
  discussion of prior work, a description of the relevant data), in LaTeX on the course's Overleaf template, as a PDF on
  Gradescope.
- **Code, graded by the TA:** a link to a public GitHub repository with the code so far (DLV-07).

Rules (unchanged): every number comes from a result file named next to it, now enforced by the registry and the lint;
prior work comes from the literature clusters, each claim checked against its paper; results sections wait for the final
report.

## Title
Chosen: **"Auditing Causal-Discovery Systems: An Open Protocol and a First Audit of the Field"**.
Alternative: "Where Do the Arrows Come From? An Open Protocol for Auditing Causal-Discovery Systems".

## Abstract (as drafted; numbers are registry keys)
1. **Problem.** Systems are judged by one benchmark score; agents run the whole analysis; neither says where an answer
   comes from (numbers, names, layout, the system's own rules).
2. **What we do.** An open audit protocol: names and column order change while the numbers stay fixed, every intermediate
   graph is traced, failures are typed, scores are reported within a regime and against a reference of stated tier.
3. **Findings, one per level.** Benchmarks reward layout (`ab01.fci.gain`); agents read names (`ab06.p9.losing` of
   `ab06.p9.entered` lose at least `ab06.p9.threshold`); an agent's steps undo its data (`cc.s0-adj` → `cc.final-adj`;
   `cc.cyc.entered` of `cc.cyc.entered` runs reaching the cycle step crash).
4. **Release.** Protocol, recorded runs and scripts are public.

## 1. Introduction
1. Why causal structure matters, and what agents promise (Causal-Copilot and the systems of the field audit).
2. The gap: a score does not say where an answer came from; known shortcuts (varsortability, column order, memorised
   graphs); the call for audit trails.
3. The protocol in one paragraph: levels L0-L2 now (L3 claim provenance and L4 adversarial search designed, later), typed
   findings from a closed list, regimes, truth tiers, pre-registered thresholds, the certificate. This is the A2 outline;
   the full specification goes to the final report (DLV-08).
4. The first audit, three bullets: benchmarks reward shortcuts (AB-01, BEN-13), agents read names (AB-06, BND-08), an
   agent's own steps undo its data (AB-06 P10, BLD-06 main control).
5. The bar the audit sets (AB-14: no vendor publishes precision or abstention for causal claims).
6. Contributions; the companion Q2 system is audited through the same interface and not reported here.

## 2. Prior work (section label `sec:prior`; 38 checked claims plus 9 data facts)
1. How causal discovery is evaluated, and what benchmarks reward (PC/FCI, GES, varsortability, R2-sortability, column
   order, Sachs as ground truth, CausalArena, CausalBench).
2. Language models as a source of causal knowledge, and memorisation controls (Kiciman, Causal Parrots, imperfect
   experts, causal order, Kitson and Constantinou, Srivastava, Li and Russo, CARE). The last is the name control we use;
   what we add is layout controls and application to deployed agents and benchmarks.
3. Causal agents and how they are evaluated (Causal-Copilot, ALCM, MATMCD, Causal Modelling Agents, causaliq-knowledge,
   PyWhy-LLM, CausalSteward, behavioural consistency, the position paper).
4. How much an edge can be trusted (bootstrap, its calibration, LLM edge confidence).
5. Auditing practice the protocol borrows (metamorphic testing, CheckList, model cards, datasheets, internal audits,
   PROV-DM).

Checker corrections applied (15 of 38; `lit_claims.json`): GES's large-sample result is conditional; R2-sortability is
"common settings"; column order matters more than sample size only typically; CausalBench's screens are not genome-scale
for RPE1; Long et al. do not say the model "violated" the error model; Srivastava's models were given dataset and node
names; CARE's collapse is under both permuted and anonymised names; Li and Russo treat consensus directions as hard facts
in practice; CausalSteward steered Causal-Copilot "when necessary"; Kummerfeld and Rix tested GES only; Kumar et al.'s
agreement advantage is not significant; CheckList's invariance tests are a test type.

## 3. Data
- **CausalArena semantic suite (S2):** `s2.families` test scenarios × `s2.arms-per` name arms = `s2.tables` tables,
  `s2.rows` rows, `s2.vars.min`-`s2.vars.max` variables, `s2.edges.min`-`s2.edges.max` edges; exact tier; CC BY 4.0.
  Public files used by the layout audit: `ab01.files.*`.
- **Named datasets (S1):** Sachs (contested: 19 / 17 / 20-edge versions) and the four UCI/DWD tables (provenance;
  Auto MPG mismatched with CausalArena's version). Licences: UCI and DWD CC BY 4.0; Sachs none stated.
- **CausalBench:** K562 and RPE1 after CausalBench's filtering (cells, controls, perturbed genes from
  `external/causalbench/*.npz.json`, which match CausalBench's Table 1); data CC BY 4.0, code Apache 2.0. BEN-13 cited.
- **Recorded runs:** what a run keeps; BND-08 and the BLD-06 main control.
- **Limits:** simulated scenarios, one run per arm, one model family, expert references.

## 4. Code link (DLV-07)
- `https://github.com/uzairgheewala/causal-copilot-q1`: public; CI "reproduce" green on 43d0c75 (27 Oct).
- A dry-run export from cc-research `cf536c1` (31 Oct, to a scratch folder) reproduced exactly and differs from the
  pushed repo only in the README's commit line and export time.
- Before submission: commit cc-research (the commit that adds `docs/paper/q1/`), re-run `py -3 tools\export_q1.py`,
  commit and push the Q1 repo, check CI is green.

## 5. Submission steps (Uzair)
1. Commit cc-research with `docs/commit_msgs/q1_checkpoint_cc-research.txt`.
2. Re-export the Q1 repo, push, CI green.
3. Overleaf: copy the course template; replace `report.tex` and `reference.bib`; add `numbers.tex` and
   `numbers_table.tex`; fill the two email macros; recompile; compare with `docs/paper/q1/build/report.pdf`.
4. Gradescope: the PDF and the repo link.

---

# Outline for the final report (Fri 4 Dec, DLV-06; parent of DLV-08..11)

## 1. Introduction and prior work
From the checkpoint, tightened after the mentor's feedback.

## 2. The audit protocol v1 (DLV-08, W2)
Finding kinds (closed list), regimes, truth tiers, development and sealed batteries, pre-registration, the certificate.

## 3. The audit package (DLV-09, W2)
Adapter interface (designed against the five audited systems plus PC and GES), controls L0-L2, report generator; one
command per system.

## 4. Results: the field under the protocol (DLV-10)
Per system: L0 scores, L1 name and layout reliance with intervals, L2 stage traces where code is open, L3-lite provenance
by arm differences. Sources today: `analysis/results/ab06/ab06.json`, `analysis/results/stability_s2/bnd08_summary.json`,
`analysis/results/fork/bld06_live_compare.json` (main control only), reruns through the package (W2).

## 5. Benchmarks audited (DLV-11, appendix)
CausalArena layout channels (`analysis/results/rescore_v2/`), CausalBench metric audit (`analysis/results/ben13/summary.json`).

## 6. Limits and what comes next
Single runs per arm; one model family; rebuilt images (comparisons within one image); hashes per CPU family; the adversary
loop with the Q2 system (ADV-01) as the next source of findings.

Every number in the final report goes through `docs/paper/q1/numbers.json`.
