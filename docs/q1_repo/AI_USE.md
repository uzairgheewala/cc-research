# AI use and human contributions

Prepared 6 November 2026 for the DSC 180A code checkpoint.

AI assistance was extensive. ChatGPT/Codex and earlier Claude-assisted project
work supported experimental planning, instrumentation, analysis implementation,
debugging, documentation and review. Exact model versions are not available for
every historical conversation. The retained graphs are outputs of separately
recorded experiments, not new results generated while writing this statement.

Uzair Gheewala chose the project direction, approved designs and run plans,
decided scope and interpretations, reviewed reported results and revised the
documentation and paper. AI produced substantial implementation and drafting
work. Human responsibility does not imply that every line was manually written
or independently inspected by a human.

## Important prompt families

These are reconstructed summaries of substantive instructions, not a claim to
have recovered every original message verbatim.

| Task | Important instruction summary | Validation and limits |
|---|---|---|
| Controlled replication | Run the original causal-discovery system under declared conditions, change variable-name controls while preserving the numerical data, and retain code and input identities. | Dataset cards, mappings, run plans and recorded provenance. The live systems were not rerun for this archive. |
| Instrumentation | Preserve intermediate graphs and model interactions so changes can be located in the pipeline; keep observation separate from changes to the underlying method. | Historical tracing and diagnostic records are in the separate research repository. This reduced repository does not contain every intermediate record. |
| Paired comparison | Compare the original pipeline with the separately developed refinement branch; use matched completed tables for final-score differences; account separately for crashes and costs. | `analysis/bld06_live_compare.py`, `score/paired.py`, the hashed plan and the committed comparison. This is a companion comparison, not the complete Crucis paper. |
| Offline reproduction | Build a small repository that recomputes the comparison from retained graphs without credentials or model calls, and verify hashes of reduced states and datasets. | `python -B run.py reproduce` and `python -B run.py test`. These recompute the recorded comparison, not the original live agent or stage attribution. |
| Review and documentation | Challenge overbroad conclusions, distinguish bootstrap from language-model review, state uncertainty and make setup, scope and commands clear. | Human decisions, AI-assisted reviews and documentary corrections. A passing reproduction test establishes numeric agreement for this comparison only. |

An available exact instruction excerpt from the later report review is:

> “Let's do the same short pass for flow and clarity while keeping the scope and linked numbers intact.”

It illustrates the later editorial process; it is not presented as the original
prompt that produced the analysis code. Older exact implementation/debugging
prompts and model identifiers remain incompletely recovered. The author should
add any important missing task or instruction before claiming complete prompt
coverage. Private research-assistance tooling is summarized by role, without
including its source or unrelated private records.
The author confirmed on 6 November that the disclosed task families cover the
important uses he recalls; this does not recover missing historical transcripts.

## Tests and retained evidence

The reproduction command independently runs the included analysis and compares
its JSON output with the committed result under a numerical tolerance. Tests
also check the plan hash, reduced-state hashes and dataset-card hashes. Inspect
the supplied submission verification receipt for the actual run, environment and
outcome; test definitions alone are not evidence that a run passed.

Full original states, complete interaction logs and stage-specific attribution
require separate research evidence. AI reviewer agreement is not independent
scientific corroboration. One run per table/arm and the declared model and cohort
constraints limit interpretation. The refinement comparison in this repository
is separate from the checkpoint paper's broader framework contribution.
