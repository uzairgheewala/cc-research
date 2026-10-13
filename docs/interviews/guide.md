# AB-10 interview guide (30 minutes, semi-structured)

Ticket: AUD-41. Written 2026-10-12. For Uzair as interviewer. Read `consent_script.md` aloud before section 1.

## Where we are now

The guide tests four things from `analysis/reports/audit_dag.md`:

| Code | Hypothesis | Refuted if |
|---|---|---|
| H1 | Practitioners would use per-claim provenance and abstention | (rule in `synthesis_plan.md`) |
| H2 | They ask intervention questions, not graph questions | (rule in `synthesis_plan.md`) |
| H3 | A name/semantic-dependence audit of their LLM tools is worth paying for | (rule in `synthesis_plan.md`) |
| P13 | At least half name a decision where "which causes, how sure" matters more than the full graph | under a quarter do |

**Design rule: elicit before showing.** Sections 1-5 ask about the interviewee's own work, with no mention of
provenance, abstention, graphs or LLM audits. The mock-ups come only in section 6, so that H2 and P13 are coded from
what people say unprompted, before our framing can prime them. If you run short of time, cut section 6(iii) or 7.
Never cut sections 2-3.

## Interviewer rules

- **Ask, then wait.** Let silence run for 5 seconds before probing.
- **Never name the hypothesis.** Don't say "provenance", "abstention", "causal graph", "DAG" or "intervention" until
  the interviewee does. Use their words back to them.
- **No pitching.** If they ask what we are building, say: "I'll tell you at the end, so I don't colour your answers."
- **Past over hypothetical.** "Last time you..." beats "Would you...". Treat hypothetical answers as weaker evidence;
  the synthesis plan codes them that way.
- **Neutral probes only** (use these, and nothing that suggests an answer):
  - N1 "Can you say more about that?"
  - N2 "What happened next?"
  - N3 "How did you know?"
  - N4 "Can you give me an example?"
  - N5 "What did you do with that?"
  - N6 "Why was that important to you?" (only after they raise it)
  - N7 "Anything else?"
- **Avoid:**
  - "Wouldn't it be useful if...?"
  - "Do you find it frustrating that...?"
  - "How much would you pay for...?"
  - any question that contains the answer.
- **Confidential details.** If they start to share something confidential, say: "You can keep it at the level of the
  kind of decision; I don't need specifics."

Note-taking:
- Paraphrase as you go.
- Write verbatim fragments only if they are under about 10 words, and mark them with quotes. The notes record will
  paraphrase them later.
- Never write names of people, employers, internal systems or specific incidents.

## Timing

| Min | Section | Maps to |
|---|---|---|
| 0-2 | Consent script (`consent_script.md`) | n/a |
| 2-4 | 1 Warm-up | context |
| 4-10 | 2 Current decision workflow | P13, H2 |
| 10-14 | 3 The questions they actually ask | H2, P13 |
| 14-17 | 4 How they judge trust today | H1 |
| 17-20 | 5 When a tool is wrong | H1, H3 |
| 20-27 | 6 Reactions to three mock-ups | H1, H2, H3 |
| 27-29 | 7 Adoption and payment | H1, H3 |
| 29-30 | 8 Wrap-up | n/a |

## 1. Warm-up (2 min)

| # | Question | Maps to | Notes field |
|---|---|---|---|
| 1.1 | "To start, can you describe your role in a sentence or two, without naming your employer?" | context | `participant.role_level` (coded) |
| 1.2 | "What kinds of decisions does your work feed into?" | context, H2 | `decisions[]` (start list) |

## 2. Current decision workflow (6 min)

| # | Question | Maps to | Notes field |
|---|---|---|---|
| 2.1 | "Walk me through the last time you had to decide what caused something, or whether changing something would make a difference. What was the situation, at the level of the kind of problem?" | P13, H2 | `decisions[0].summary`, `.type` |
| 2.2 | "Who was involved, by role, and who made the final call?" | context | `decisions[0].summary` |
| 2.3 | "What did you look at to decide? What tools or analyses?" | H2, H1 | `current_tools[]` |
| 2.4 | "At the moment of deciding, what did you actually need to know in order to act?" | **P13** | `decisions[0].which_causes_how_sure` |
| 2.5 | "If you could have had only one thing from an analysis for that decision, what would it have been?" | **P13** | same |
| 2.6 | "Is that typical, or was that case unusual? Tell me about one more, briefly." | P13, H2 | `decisions[1]` |

Probes for 2.4 and 2.5: N1, N3, N4. If they mention a complete map of how things connect, ask N6: "Why was the whole
picture important there?" Don't add your own alternatives.

## 3. The questions they actually ask (4 min)

| # | Question | Maps to | Notes field |
|---|---|---|---|
| 3.1 | "When you or your stakeholders ask a question of the data in decisions like these, how is the question usually phrased? Can you give me two or three examples, in your own words?" | **H2** | `decisions[].type` |
| 3.2 | "Of those, which ones actually change what someone does?" | H2, P13 | `decisions[].summary` |
| 3.3 | "Has anyone ever asked for a full map or diagram of how everything relates? What was it used for?" | H2 (counter-evidence welcome) | `decisions[].type = graph` if yes |

How to type `decisions[].type`:
- **graph**: the deliverable was a map of relationships (for example a service topology, a DAG for a protocol, or a
  driver map).
- **intervention**: "if we change X, does Y move, and by how much".
- **rca**: "what caused this event or outcome".
- **other**: forecasting, monitoring, reporting.

Type by what the decision needed, not by the tool used.

## 4. How they judge trust today (3 min)

| # | Question | Maps to | Notes field |
|---|---|---|---|
| 4.1 | "When an analysis or a tool gives you an answer about a cause, how do you decide whether to believe it?" | H1 | `trust_practices[]` |
| 4.2 | "What would make you trust an answer more? What would make you trust it less?" | H1 | `trust_practices[]` |
| 4.3 | "When you pass a conclusion to someone else, what do they ask to see?" | H1 | `trust_practices[]` |

Probes: N3, N4. Code H1 only from what they bring up, for example "I want to know where it came from", "I check
whether it's backed by an experiment", or "I'd rather it said it doesn't know".

## 5. When a tool is wrong (3 min)

| # | Question | Maps to | Notes field |
|---|---|---|---|
| 5.1 | "Tell me about a time an analysis or tool pointed to the wrong cause. How did you find out?" | H1 | `when_wrong` |
| 5.2 | "What did it cost, roughly, in time, money or trust?" | H1, H3 | `when_wrong` |
| 5.3 | "Do you use any tools that rely on language models, or AI assistants, for this kind of work? What do you use them for?" | H3 | `current_tools[]` |
| 5.4 | (only if 5.3 is yes) "How do you check what they tell you?" | H3 | `trust_practices[]` |

## 6. Reactions to three mock-ups (7 min)

Say first: *"I'll show you three short text mock-ups. The numbers are made up for illustration. I'm not attached to
them; your honest reaction, including 'I wouldn't use this', is what helps."*

Paste each card into the chat or share the screen. Read the variable legend for their sector aloud, so the letters
mean something to them.

**Sector legend (read aloud before card i):**

| Letter | IT ops / SRE | Marketing science | RWE (health) | Policy analytics |
|---|---|---|---|---|
| T | a config change was rolled out | search ad spend | a new drug | a job-training program |
| M | traffic from a partner | TV spend | a genetic risk score | local unemployment rate |
| Y | checkout latency | site visits | blood-sugar level | earnings after 1 year |
| Z | error rate | brand search volume | number of clinic visits | earlier benefit claims |

(T and Z are chosen so that either direction is plausible: errors can trigger rollouts or be caused by them; spend
can follow search volume or drive it.)

After each card, ask the same three questions:

| # | Question (same for each card) | Maps to | Notes field |
|---|---|---|---|
| 6.a | "What is your first reaction? What on this would you use, and what would you ignore?" | H1 / H3 | `artefacts.<card>.paraphrase` |
| 6.b | "Where, if anywhere, would this fit into the decision you described earlier?" | H1, H2, P13 | `artefacts.<card>.paraphrase` |
| 6.c | "On a scale of 1 to 5, where 1 is 'I wouldn't use this' and 5 is 'I'd use this as is', where does it sit for you, and why?" | H1 / H3 | `artefacts.<card>.score` |

### Card (i): per-edge provenance table

Built from the claim-ledger fields in `ledger/DESIGN.md`: `relation`, `direction_source`, `licensed_by`, `evidence`,
`data_only_relation`, `confidence` and `knowledge`.

```
WHAT THE ANALYSIS CONCLUDED, ONE ROW PER PAIR OF VARIABLES          (illustrative numbers)

Pair   Conclusion      Why this direction        Rule used           Evidence           Data alone said       How sure
-----  --------------  ------------------------  ------------------  -----------------  --------------------  -----------------------
T, Y   T -> Y          data pattern              collider            e1, e2: T and M    T -> Y                0.93 (calibrated)
                                                 (T -> Y <- M)       unlinked, both
                                                                     linked to Y
M, Y   M -> Y          data pattern              collider            e2, e3             M -> Y                0.90 (calibrated)
T, Z   T -> Z          knowledge, supplied by    ordering            k1 ordering;       linked, direction     0.64 (resampling
                       an AI model               ("T before Z")      e5 link test       open                  only, not calibrated)
T, M   no direct link  none                      independence test   e2                 no direct link        0.88 (calibrated)
(+ 2 more "no direct link" rows: Y, Z and M, Z)

Checks:  knowledge added no link the data did not find ........ PASS
         result unchanged when the column order is shuffled ..... PASS
Overridden: 1 ordering statement ("Y before M") conflicted with a recorded intervention on M (e8); intervention kept.
```

Card-specific probe (neutral): "Which column, if any, would you look at first?"

### Card (ii): an answer that sometimes says "can't tell"

```
QUESTION: If we change T, which of Y, Z and M move?                 (illustrative numbers)

  T moves Y:  YES             source: data (pattern e1, e2)                      how sure: 0.93
  T moves Z:  CAN'T TELL FROM DATA
              The data show T and Z are linked, but not which way.
              With the ordering supplied by an AI model ("T before Z"): yes  how sure: 0.64, not calibrated
  T moves M:  NO              source: data (independence test e2)                how sure: 0.88

  Answered from data alone: 2 of 3.   Not answered from data alone: 1 of 3.
```

Card-specific probe (neutral): "What would you do with the 'can't tell' line?"

### Card (iii): name-swap audit of an AI-assisted causal tool

```
AUDIT: does the tool's answer depend on what the columns are CALLED rather than on the data?
Tool: an AI-assisted causal-analysis tool (anonymised).  50 test problems with known answers.
                                                                         (illustrative numbers)
Arm                                    Directions correct (F1)   vs. same tool, data only
-------------------------------------  ------------------------  ------------------------
Real column names                      0.31                      +0.09
Neutral names (V1, V2, ...)            0.23                      +0.01
Names shuffled across columns          0.14                      -0.08   <- worse than ignoring names

Finding: with misleading names, the tool does worse than using the data alone.
41% of its directions flip when only the names change.
```

Card-specific probe (neutral): "Who, if anyone, in your organisation would want to see this?"

Interviewer-only note: these numbers are shaped like our one measured system (directed F1 0.306 / 0.232 / 0.142 with
real / neutral / swapped names). The data-only column and the 41% are invented for the card. Do not present any of it
as a finding.

## 7. Adoption and payment (2 min)

None of these questions names a price or asks "would you pay". They ask how buying works and what has been paid for
before.

| # | Question | Maps to | Notes field |
|---|---|---|---|
| 7.1 | "Thinking about the three cards, would any of them change anything about how you work today? Which, and how?" | H1, H3 | `adoption_signals.paraphrase` |
| 7.2 | "How does a new analysis tool usually get adopted where you work? Who decides, by role, and what do they need to see?" | H1, H3 | `adoption_signals.budget_owner_named` |
| 7.3 | "What's the last tool in this area your team started using? What did it replace, and roughly what band did it cost per year: none, under $1k, $1-10k, $10-100k, over $100k, or you don't know?" | H3 (anchor) | `adoption_signals.current_spend_band` |
| 7.4 | "If something like card (i), (ii) or (iii) existed, what would have to be true for you to try it?" | H1, H3 | `adoption_signals.would_try`, `.paraphrase` |

Code `would_try`:
- **yes**: they name a concrete next step, such as a trial, a pilot or forwarding it to someone.
- **maybe**: conditions only.
- **no**: they decline.
- **not_asked**: the section was skipped.

## 8. Wrap-up (1 min)

| # | Question | Maps to |
|---|---|---|
| 8.1 | "Is there anything about how you decide what caused what that I should have asked and didn't?" | all |
| 8.2 | "Would you like the short summary across all conversations when it's done?" (If yes, note it in your private contact thread, not in the notes.) | n/a |
| 8.3 | Thank them. Now you may explain in two sentences what the project is, if they ask. | n/a |

## Question to hypothesis map (summary)

| Hypothesis | Primary questions | Secondary | Supports when (coded from notes, see `synthesis_plan.md`) |
|---|---|---|---|
| H1 provenance and abstention | 4.1-4.3, 6.a/6.c on cards (i) and (ii), 7.1, 7.4 | 5.1-5.2 | they describe checking where a conclusion came from, or preferring "don't know" to a wrong answer, **and** rate card (i) or (ii) at 4 or more, or give a concrete adoption step |
| H2 intervention, not graph | 2.1, 3.1-3.3 | 1.2, 6.b | most of their decisions are typed intervention or RCA, and they do not describe the full graph as the deliverable |
| H3 name-dependence audit worth paying for | 5.3-5.4, 6 on card (iii), 7.2-7.4 | 5.2 | they use or evaluate LLM tools for causal or RCA work, **and** rate card (iii) at 4 or more, **and** name a budget path or concrete step |
| P13 "which causes, how sure" over the full graph | 2.4, 2.5, 2.6 | 3.2, 3.3 | they name a real decision where what they needed was which causes, or whether an action moves an outcome, with how sure, and the full graph was not needed or was secondary |

## Where we're going

After each interview:
1. Fill `notes_template.md` as a JSON record under `docs/interviews/notes/` within 24 hours.
2. Code H1-H3 and P13 in `coding.student`.
3. Claude codes the blind copy independently (`synthesis_plan.md`).
4. `analysis/interview_synthesis.py` tallies the verdicts.
