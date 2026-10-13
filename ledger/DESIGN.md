# The claim ledger: record format and verifier (design, before any engine code)

Tickets: BLD-13, BLD-02, CAP-09, CAP-11, EXT-02
Written 2026-10-12. Inputs: program v2 (`claude/program-v2-order-provenance.md`), AU3 (theory: what licenses each mark),
AU6 (engines), AU8 (output contract, regulator and user requirements). Status: schema and verifier written and tested;
no discovery engine yet.

## 1. What the format must make impossible

| Failure (seen in the field or in our audits) | Where seen | How the format prevents it |
|---|---|---|
| A direction with no stated source | Causal-Copilot report; every library | `direction_source` is required and typed; `none` is a value, absence is invalid |
| Knowledge that silently adds or deletes a connection | refinement v1 (dropped 120); Causal-Copilot S1/S2 | I5 check: final skeleton must equal the data-only skeleton |
| Declared knowledge ignored without a trace | causal-learn #219, #171, #266; Tetrad #1954 | every knowledge statement is either applied by a claim or listed as overridden with a reason |
| Output that changes with column order | AUD-27 (engine copy), AUD-28 (PC orientation), DoWhy #1695 | variables are identified by content hash, not position; the run report carries the permutation check |
| Unreproducible runs | unseeded bootstrap; no model id in reports | engine name, version and wheel hash, seeds, data hashes and the model snapshot are required fields |
| LLM prose presented as a result | Causal-Copilot's report | the report is generated from the records; free text lives only in `commentary` and is never a claim |

## 2. Objects

- **Variable**: `var_id` = sha256 of the column's values (as float64 little-endian) and its name; `position` is recorded
  but never used to identify it.
- **Evidence record**: one test or observation. `type` in {`ci_test`, `score_delta`, `functional_asymmetry`,
  `intervention_shift`, `knowledge_statement`}; the variables, conditioning set, statistic, p-value or score, the data
  hash it was computed on, the engine that computed it, the seed.
- **Knowledge statement**: `kind` in {`tier`, `required_edge`, `forbidden_edge`, `ancestral`, `non_ancestral`}; content;
  supplier (`person` or `model` with model id, prompt sha256, phrasing id, and exactly what the supplier was shown).
  Ancestral statements are kept as residual clauses (Fang et al. 2025: not reducible to edge orientations).
- **Claim**: one unordered pair. `relation` in {`x->y`, `x-y` (connected, direction open), `none`, `x<->y` (latent
  confounding, PAG only)}; `direction_source` in {`data_pattern`, `data_form`, `intervention`, `knowledge`, `none`};
  `licensed_by` (the rule: `v_structure`, `meek_r1`..`meek_r4`, `i_essential`, `lingam`, `anm`, `tier`, `declared`);
  evidence ids; `data_only_relation` (what the data-only kernel said); confidence (bootstrap frequency, calibrated
  probability, calibration set id); knowledge ids used.
- **Run report**: inputs and their hashes, regime (D / D+I / D+K / D+I+K), engine stack, seeds, the data-only output,
  the final output, invariant results (I1-I7), counts, `ledger_sha256`, and an optional `commentary` string.

Binding times: variables and evidence are bound when computed; knowledge when supplied (before resolution); claims at
resolution (K2-K4 of program v2); confidence after resampling (K5); the report and hash last. Nothing earlier may be
rewritten by a later stage; a later stage may only add records.

## 3. The verifier (`ledger/verify.py`)

Runs on the records alone, without the data, and says what it cannot check.

| Check | Invariant | Fails when |
|---|---|---|
| V1 schema | | a required field is missing or a value is outside its type |
| V2 evidence closure | I4 | a claim cites no evidence, or cites an id that does not exist |
| V3 knowledge never connects | I5 | the final skeleton differs from the data-only skeleton, or a knowledge-sourced claim is on a pair the data left unconnected |
| V4 interventions outrank knowledge | I6 | a pair has intervention and knowledge evidence that disagree and the claim follows knowledge, or the override is not recorded |
| V5 knowledge honoured | | a knowledge statement is neither used by a claim nor listed in `overrides` with a reason |
| V6 hash | I2 | the recomputed canonical sha256 of variables, evidence, knowledge and claims differs from `ledger_sha256` |
| V7 order invariance declared | I1 | the report has no permutation check, or the check found a difference |
| V8 floor declared | I3 | the regime admits no knowledge and the final output differs from the data-only output |

Not checkable without the data: that each statistic was computed correctly, that a supplier saw only what is
recorded, and that calibration holds outside its calibration set. The report must say so (`unverifiable` field).

## 4. PROV-O mapping

`prov:Entity` = variable, evidence record, knowledge statement, claim, run report; `prov:Activity` = a test, a
resolution step, a calibration fit; `prov:Agent` = engine (software agent), supplier (person or model).
`claim prov:wasDerivedFrom evidence`; `evidence prov:wasGeneratedBy test`; `test prov:wasAssociatedWith engine`;
`knowledge prov:wasAttributedTo supplier`. `ledger/prov_export.py` (later) writes this as JSON-LD.

## 5. Interoperability (AU8)

Read causal-cmd knowledge files (tiers, required, forbidden); write Tetrad JSON graphs and DAGitty strings from the final
output. Cost about a day; not in this step.
