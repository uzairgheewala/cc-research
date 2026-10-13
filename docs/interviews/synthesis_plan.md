# AB-10 synthesis plan: from 5-8 notes to verdicts on H1-H3 and P13

Ticket: AUD-41. Written 2026-10-12, **before any interview**. The rules below are fixed now. Any change after the
first interview must be dated and justified at the bottom of this file, and reported in `ab10_interviews.md`.

## Where we are now

The audit DAG gives AB-10 one prediction with thresholds (P13) and three hypotheses without thresholds (H1-H3). This
plan sets the coding rule for all four. It fixes the thresholds: P13's exactly as in the DAG, and H1-H3's by mirroring
P13. It also defines the P13 decision, sets the paraphrase rules and the inter-coder check, and says what the output
looks like.

The computation is `analysis/interview_synthesis.py`. It writes `analysis/results/interviews/synthesis.json`. The
must-show report, `analysis/reports/ab10_interviews.md`, is written from that JSON.

## 1. Coding rule

Each interview gets one code per hypothesis:

| Code | Meaning |
|---|---|
| `supports` | The interviewee said or did something that the "supports when" column below describes. |
| `refutes` | The interviewee said or did something that the "refutes when" column describes. |
| `silent` | The topic did not come up, or the evidence was only hypothetical, mixed in the same breath, or ambiguous. |

General rules:
- Code from the notes record only, not from memory of the call. Claude can code the same thing, and the coding stays
  checkable.
- **Past behaviour outranks hypotheticals.** A statement about what they *would* do counts only together with a past
  practice or a concrete next step (`would_try = yes`). On its own it is coded `silent`.
- **Unprompted outranks prompted.** For H2 and P13, only material from guide sections 1-5 counts, before the cards
  were shown. A reaction to a card cannot make H2 or P13 `supports`.
- Every non-silent code carries an `evidence` paraphrase; the script refuses an empty one.

| | Supports when | Refutes when |
|---|---|---|
| **H1** would use per-claim provenance and abstention | (a) they describe checking where a conclusion came from, or preferring "don't know" to a wrong answer (section 4 or 5), **and** (b) they rate card (i) or (ii) at 4 or more, **or** `would_try = yes` with a reason tied to source or abstention | they rate both cards (i) and (ii) at 2 or less, **or** they say they would not look at sources or would not accept "can't tell" (for example "I need an answer, not a maybe"), with no counter-statement |
| **H2** intervention questions, not graph questions | most of their **real** decisions (`decisions[]`) are typed `intervention` or `rca`, **and** they did not describe a full relationship map as the deliverable they needed | at least half of their real decisions are typed `graph`, **or** they say the map itself is what stakeholders act on |
| **H3** a name/semantic-dependence audit of their LLM tools is worth paying for | they use or evaluate LLM tools for causal or RCA work (5.3), **and** rate card (iii) at 4 or more, **and** name a budget path (`budget_owner_named = yes`) or `would_try = yes` | they use LLM tools but rate card (iii) at 2 or less, **or** they say such an audit is not something their organisation would pay for or run |
| **P13** "which causes, how sure" matters more than the full graph | they name at least one **real** decision meeting the definition in section 4 (that decision has `which_causes_how_sure = yes`; the script enforces this link) | every real decision they described needed the full graph, **or** certainty did not matter to the decision |

A note on H3: interviewees who use no LLM tools for this work are coded `silent` on H3, not `refutes`. They are
counted in N, so many non-users make H3 hard to support. That is intended: H3 claims a payment-worthy need, and
non-users are evidence against its breadth.

## 2. Thresholds and verdicts

**N = all valid interview records.** Silent codes count in N, because a hypothesis needs positive statements. With
`s` = number of `supports` and `r` = number of `refutes`:

| | Supported | Refuted | Otherwise |
|---|---|---|---|
| **P13** (exactly as in the audit DAG: "half name a decision ... (under a quarter)") | `s >= N/2` (at least half) | `s < N/4` (under a quarter) | inconclusive |
| **H1-H3** (this plan; the DAG gives no thresholds, so P13's are mirrored) | `s >= N/2` and `s > r` | `s < N/4`, or `r >= N/2` and `r > s` | inconclusive |
| any, when **N < 5** | | | `insufficient_n` (tallies still reported) |

Two notes on the thresholds:
- **Boundaries are inclusive exactly as written.** For example, 4 of 8 supports P13, while 2 of 8 is not "under a
  quarter", so it is inconclusive. The script uses integer forms (`2s >= N`, `4s < N`) to avoid rounding.
- **"Refuted" for H1-H3 can occur with zero `refutes` codes.** It then means "under a quarter positively support it".
  The report must show `s`, `r` and `silent` next to every verdict, so a reader can tell "actively contradicted" from
  "not raised".

Worked boundaries for P13:

| N | Supported needs | Refuted when | Inconclusive band |
|---|---|---|---|
| 5 | s >= 3 | s <= 1 | s = 2 |
| 6 | s >= 3 | s <= 1 | s = 2 |
| 7 | s >= 4 | s <= 1 | s = 2-3 |
| 8 | s >= 4 | s <= 1 | s = 2-3 |

What follows from each verdict comes from the DAG kill criteria. If P13 is refuted, the product angle is shelved and
the paper stands on L1-L3. The verdicts feed C1 in AB-16.

**Sensitivity.** The script repeats every tally without interviewees recruited through causal-inference communities
(`pywhy_community`, `other_causal_community`), who are likely to favour H1 and H3. If a verdict changes between the two
tallies, the report states both and treats the verdict as fragile.

**By sector.** Counts only, with no verdicts; sector cells hold 1-3 people.

## 3. How quotes are paraphrased

- **At note time.** Write in the third person, in your own words: "they check whether a rollback reproduces the fix",
  not "I always roll back first".
- **Short fragments.** A verbatim fragment of about 10 words or fewer may be kept in the rough notes, but it is
  paraphrased in the record.
- **Remove identifying detail:**
  - names of people, employers, clients, internal systems, products under development, incidents or studies;
  - dates more precise than the month;
  - locations;
  - figures more precise than a band ("about half a day", "tens of thousands a year").
- **In the report.** `ab10_interviews.md` cites each paraphrase as `(P03, marketing_science)`. Sector is the only
  attribute shown next to a paraphrase; role level and company size appear only in aggregate tables. No paraphrase
  appears if, combined with the sector, it would point to an identifiable organisation (for example "the only RWE
  team at a company of 10,000+ in our sample that does X"). Generalise it or drop it.
- **Path (a) records** (course-internal) may appear in the course-internal report and the AB-16 memo, but **not** in
  any paper (see `human_subjects_check.md`). The script prints a warning while any path (a) record is present.

## 4. What counts as a "decision where 'which causes, how sure' matters more than the full graph" (P13)

A described decision counts, and gets `which_causes_how_sure = yes`, when all four hold:

1. **Real.** It happened, or is underway, in their work (`real_or_hypothetical = real`).
2. **A specific target.** What they needed was one of these:
   - the identity of the cause or causes of a specific outcome or event (RCA type);
   - whether a specific action would move a specific outcome, and by roughly how much (intervention type).
3. **Certainty mattered.** They indicate that how sure the answer was changed what they did. Examples:
   - waiting for more evidence;
   - running a test or rollback first;
   - asking for a confidence figure;
   - acting only above some bar;
   - being burned by a confident wrong answer.
4. **The full graph was not needed, or was secondary.** Their answer to 2.4 or 2.5 ("the one thing you'd want") names
   the cause, the effect or the certainty, not a complete map. A map used only as a means to reach the target counts
   as secondary.

It does **not** count when:
- the deliverable they needed was the full structure (a service topology to maintain, a protocol DAG to submit, a
  driver map for a strategy deck);
- certainty did not matter ("we act on the best guess either way");
- the decision is hypothetical only;
- the only evidence comes from a reaction to a card.

Use `unclear` when conditions 2-4 cannot be settled from the notes. `unclear` does not support P13.

Edge cases fixed in advance:

| Case | Decision |
|---|---|
| RWE protocol needs a DAG **and** the team cares about one exposure-outcome effect | Counts if they say the effect estimate and its uncertainty drove the decision and the DAG served it. Does not count if the DAG itself was the regulatory deliverable they were judged on. |
| SRE uses a topology map daily and wants "which service, how sure" during incidents | Counts: the topology is a means; the incident decision needed the cause and the certainty. |
| Marketing asks "which channels drive sales, how much, how sure" for budget allocation | Counts: multiple causes, but a specific target and certainty. |
| Policy analyst wants "what affects outcome Y" with no action in view | `unclear`, unless certainty changed a real decision. |

## 5. Inter-coder check

1. **Uzair codes first** (`coding.student`), within 24 hours of each interview, from the notes record.
2. **Blind export.** When all interviews are in, Uzair runs `python analysis/interview_synthesis.py --export-blind
   <dir outside the repo>`. That writes copies with all coding removed and every
   `decisions[].which_causes_how_sure` masked to `unclear`, because that flag is the student's P13 judgement.
3. **Claude codes independently** from the blind copies. Claude applies sections 1 and 4 of this plan, fills
   `which_causes_how_sure` for its own reading, and returns a codeset per record. Claude does not see Uzair's codes
   before returning them. Uzair pastes them into `coding.claude`.
4. **Compare.** The script reports, per hypothesis:
   - percent agreement;
   - Cohen's kappa over the three codes (null when undefined, for example when everyone is `silent`);
   - the ids of records with disagreements.

   With 5-8 records, kappa is unstable, so percent agreement is the primary figure and kappa is shown for reference.
5. **Low-agreement trigger.** If any hypothesis is below 70% agreement, or below kappa 0.4 where kappa is defined,
   the coding rule for that hypothesis is unclear. Before reconciling, Uzair and Claude rewrite the "supports when"
   wording here (dated, under "Changes"), and **both** re-code that hypothesis on every record against the new
   wording.
6. **Reconcile.** For each disagreement:
   - Discuss it.
   - Agree a code and put it in `coding.reconciled`, with one line in `coding.reconciliation_note`.
   - If no agreement is reached, the reconciled code is `silent`, the conservative choice for a "supports" claim.
7. **Final run.** Verdicts are `final` only when every record has `coding.reconciled`; until then the script reports
   `provisional` verdicts from the student codes. The report gives the pre-reconciliation agreement figures alongside
   the final verdicts.

## 6. Failure modes named in advance

| Risk | Guard |
|---|---|
| Interviewer primes the answer | Cards come after sections 1-5; H2 and P13 count only pre-card material (section 1). |
| Community recruits inflate H1 and H3 | Sensitivity tally without them (section 2). |
| Polite enthusiasm counted as demand | Hypothetical-only statements code `silent`; H3 needs a budget path or a concrete step. |
| Coder drift between interviews | Coding happens from the record against fixed wording; the blind second coder catches drift. |
| Small N read as a market estimate | Verdicts speak about these 5-8 practitioners only. AB-14 uses them as qualitative inputs, never as adoption rates (`docs/market/README.md`). |
| Notes leak identity | Schema without identity fields; PII refusal; paraphrase rules (section 3). |
| Notes used in a paper without a determination | `consent.path` is recorded per record; the script warns on path (a). |

## 7. Output

- `analysis/results/interviews/synthesis.json`: tallies, verdicts, sensitivity, sector counts, inter-coder figures,
  artefact score distributions, adoption counts, and input file hashes. It has no timestamp, so it is byte-stable.
- `analysis/reports/ab10_interviews.md` (the must-show), written from the JSON:
  - a verdict table with `s / r / silent / N`;
  - the sensitivity result;
  - inter-coder figures;
  - 2-3 paraphrases per hypothesis, cited `(Pnn, sector)`;
  - what changes for C1, AB-14 and AB-16.

## Changes after the first interview

(none yet)

## Where we're going

After the last interview: blind export, then Claude's coding, then the comparison, then reconciliation, then the final
run, then `ab10_interviews.md`. That report goes to AB-16 (the wedge gate on 14 Nov) and to AB-14.
