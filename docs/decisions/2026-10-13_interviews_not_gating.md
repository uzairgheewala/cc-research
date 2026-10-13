# Decision record: interviews no longer gate the market work or the wedge decision (2026-10-13)

Tickets: AUD-45 (AB-14), AUD-41 (AB-10), DEC-05 (AB-16).

Uzair, in chat on 2026-10-13 (Pacific):

> "that market research would really help here do we have to gate it on interviews? I don't know when I'll get that
> chance if ever so could you please just do all that now?"

## What changes in `plans/audit_dag.json` (version 2)

| Bundle | Before | After |
|---|---|---|
| AB-14 Market | depends on AB-10 and AB-13; two verticals | Depends on AB-11 and AB-13. Its scope grew to a market map plus three vertical briefs (IT incident RCA, marketing measurement, pharma RWE). It also gathers public demand evidence on H1-H3, labelled indirect. |
| AB-16 Wedge decision | depends on AB-10 among nine bundles | AB-10 is no longer a dependency. C1 is scored on AB-14's public evidence, labelled indirect, and on AB-10 if any interviews have happened by then. |
| C1 criterion | "interviews, teardown" | "interviews if any, teardown, public demand evidence (indirect)" |

## What does not change

- **AB-10** stays in the plan, with its kit ready. Interviews run whenever a chance arises, after the course-staff question on human-subjects review.
- **P13** (its prediction) and the kill rule "product angle shelved if no interviewee values provenance or abstention" can only be decided by interviews. Public evidence can neither trigger nor clear them. Until interviews exist, the product angle at AB-16 rests on indirect evidence, and the wedge memo must say so.
- **Every other bundle and prediction** is unchanged.
