# AB-10 notes template: one record per interview

Ticket: AUD-41. Written 2026-10-12.

- **Format.** Each interview becomes one JSON file, `docs/interviews/notes/PNN.json`. It validates against
  `notes_schema.json`, and `analysis/interview_synthesis.py` reads it.
- **When.** Write it within 24 hours of the call, from your handwritten or typed notes.

## Where we are now

The guide (`guide.md`) produces rough notes. This template turns them into a typed record. The record holds nothing
that identifies the person, and every field the synthesis needs has a fixed type.

## What never goes in a record

The schema rejects any field not listed below. The script refuses any free text that looks like:
- an email address;
- a phone number;
- a capitalised two-word name, such as "Firstname Lastname". Product names on the allowlist in the script pass.

Also keep out, even though no regex catches them:
- employer, client or team names;
- internal system or project names;
- dates or names of specific incidents, campaigns or studies;
- exact figures that could identify a case (use bands);
- city or office location.

If a tool name gets flagged as a "name", write it in lowercase (`new relic`), or add the product pair to
`ALLOWED_PAIRS` in the script, in its own commit.

## Fields

| Field | Type | How to fill it |
|---|---|---|
| `schema` | const | `"ab10-interview-notes/0.1"` |
| `interview_id` | `P01`..`P99` | Next free number. The file name must be `<interview_id>.json`. |
| `interview_month` | `YYYY-MM` | Month only. |
| `consent.path` | `a` / `b` | As agreed with course staff (`human_subjects_check.md`). |
| `consent.verbal_consent` | `true` | Must be true. If they did not consent, there is no record. |
| `consent.audio_consent`, `consent.audio_recorded` | bool | `audio_recorded` may be true only if `audio_consent` is true. |
| `consent.determination_ref` | string | Path (b) only: the OIA determination or protocol reference. |
| `participant.sector` | enum | `it_ops_sre`, `marketing_science`, `rwe_health`, `policy_analytics`, `other` |
| `participant.role_level` | enum | `individual_contributor`, `lead_or_manager`, `director_or_above`, `consultant_or_academic` |
| `participant.company_size` | enum | `1-49`, `50-249`, `250-999`, `1000-9999`, `10000+`, `unknown` |
| `participant.recruited_via` | enum | `tritons_connect`, `take_a_triton`, `hdsi_partner_via_course`, `pywhy_community`, `other_causal_community`, `course_contact`, `other` |
| `decisions[]` | up to 6 | One entry per decision they described in guide sections 2-3. |
| `decisions[].summary` | 10-600 chars | Paraphrase at the level of the kind of decision, for example "whether a config rollout caused a latency regression". |
| `decisions[].type` | enum | `graph` (a relationship map was the deliverable), `intervention` ("if we change X, does Y move"), `rca` ("what caused this event"), `other`. Type by what the decision needed, not by the tool. |
| `decisions[].real_or_hypothetical` | enum | `real` if it happened; `hypothetical` if they described what they *would* do. |
| `decisions[].which_causes_how_sure` | enum | `yes` / `no` / `unclear`, using the P13 rule in `synthesis_plan.md` section 4. |
| `current_tools[]` | strings | Tool or method names, for example `datadog`, `meridian`, `excel`, `an llm assistant`. Generic names only for internal tools ("an internal dashboard"). |
| `trust_practices[]` | strings | Paraphrases of how they judge trust (guide section 4). |
| `when_wrong` | string | Paraphrase of guide section 5: what went wrong, how they found out, what it cost (in bands). |
| `artefacts.<card>.shown` | bool | Cards: `provenance_table` (i), `abstaining_answer` (ii), `name_swap_audit` (iii). |
| `artefacts.<card>.score` | 1-5 or null | The rating they gave at 6.c. Use null if the card was not shown. Do not infer a score they did not give; if they would not rate it, set `shown: true` and ask again, or use the nearest score they named. |
| `artefacts.<card>.paraphrase` | string | What they would use or ignore, and where it would fit. |
| `adoption_signals.would_try` | enum | `yes` (named a concrete next step), `maybe` (conditions only), `no`, `not_asked` |
| `adoption_signals.budget_owner_named` | enum | `yes` if they named a **role** that decides or holds budget |
| `adoption_signals.current_spend_band` | enum | Yearly USD on the last tool adopted in this area: `none`, `under_1k`, `1k_10k`, `10k_100k`, `over_100k`, `unknown`, `not_asked` |
| `adoption_signals.paraphrase` | string | What would have to be true for them to try it (7.4), and how adoption works (7.2). |
| `coding.student` | codeset | **Your** codes for H1, H2, H3 and P13: `supports` / `refutes` / `silent`, each with an `evidence` paraphrase (required unless silent). |
| `coding.claude` | codeset | Added later from Claude's blind coding. |
| `coding.reconciled` | codeset | Added after the two of you compare codes. |
| `coding.reconciliation_note` | string | One line on what changed and why. |

**Paraphrase rules** (also in `synthesis_plan.md` section 3):
- Write in the third person ("they check whether..."), in your own words.
- No verbatim run longer than about 10 words. Bands, not exact figures.

## Example record (fake; do not copy its content)

```json
{
 "schema": "ab10-interview-notes/0.1",
 "interview_id": "P01",
 "interview_month": "2026-10",
 "consent": {"path": "a", "verbal_consent": true, "audio_consent": false, "audio_recorded": false},
 "participant": {"sector": "it_ops_sre", "role_level": "lead_or_manager", "company_size": "1000-9999",
                 "recruited_via": "tritons_connect"},
 "decisions": [
  {"summary": "whether a configuration rollout caused a rise in checkout latency, to decide on a rollback",
   "type": "rca", "real_or_hypothetical": "real", "which_causes_how_sure": "yes"},
  {"summary": "whether moving a cache to a new region would cut tail latency enough to justify the cost",
   "type": "intervention", "real_or_hypothetical": "real", "which_causes_how_sure": "unclear"}
 ],
 "current_tools": ["datadog", "an internal dashboard", "an llm assistant for log summaries"],
 "trust_practices": [
  "trusts a root cause more when a rollback reproduces the improvement",
  "asks which dashboards or traces a claim came from before escalating"
 ],
 "when_wrong": "an automated suggestion pointed at the database; the real cause was a config change; cost about half a day of on-call time",
 "artefacts": {
  "provenance_table": {"shown": true, "score": 4, "paraphrase": "would read the source column first; wants it inside the incident ticket"},
  "abstaining_answer": {"shown": true, "score": 5, "paraphrase": "prefers a clear can't-tell to a confident wrong answer during an incident"},
  "name_swap_audit": {"shown": true, "score": 2, "paraphrase": "interesting but would not run it; vendor evaluation is someone else's job"}
 },
 "adoption_signals": {"would_try": "maybe", "budget_owner_named": "yes", "current_spend_band": "10k_100k",
                      "paraphrase": "platform lead approves tools after a two-week trial; must not slow investigations"},
 "coding": {
  "student": {
   "H1": {"code": "supports", "evidence": "checks the source of a claim before escalating; rated cards i and ii at 4 and 5"},
   "H2": {"code": "supports", "evidence": "both decisions were about one cause or one change, not a relationship map"},
   "H3": {"code": "refutes", "evidence": "uses an llm assistant but sees auditing it as not their budget; rated card iii at 2"},
   "P13": {"code": "supports", "evidence": "for the rollback, needed which change caused it and how sure, not the full dependency map"}
  }
 }
}
```

## Steps after writing a record

1. Run `python analysis/interview_synthesis.py`. Fix anything it refuses; it names the file and field.
2. When all interviews are in, run `python analysis/interview_synthesis.py --export-blind <scratch dir outside the
   repo>`. Hand the blind copies to Claude for independent coding (`synthesis_plan.md` section 5).

## Where we're going

Records accumulate in `docs/interviews/notes/`. After the last interview, the blind coding, the comparison and the
reconciliation follow, and then the final synthesis run (`synthesis_plan.md`).
