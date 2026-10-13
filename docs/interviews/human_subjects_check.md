# AB-10 human-subjects check: do the practitioner interviews need IRB review?

Ticket: AUD-41 (bundle AB-10). Written 2026-10-12. Pages read on that date through a fetch tool that summarises
pages, so check each quote on the live page before you rely on it.

> **This is not legal or IRB advice.** It is a student-side reading of UC San Diego's public HRPP pages, written to
> help Uzair ask course staff the right question. Only the course instructor (for the course side) and UC San Diego's
> Office of IRB Administration (OIA, for the regulatory side) can decide. If they say something different from this
> note, follow them.

## Where we are now

AB-10 plans 5-8 thirty-minute interviews with practitioners in IT operations/SRE, marketing science, real-world
evidence and policy analytics. The audit DAG (`analysis/reports/audit_dag.md`) feeds the results into C1 and the wedge
decision (AB-16). The wedge decision in turn shapes a paper (AB-17). The DAG approval record
(`docs/decisions/2026-10-12_audit_dag.md`) makes one condition explicit: Uzair checks with course staff about
human-subjects review **before** the first interview.

## What UC San Diego's HRPP pages say

| # | Page (URL) | What it says (quotes under 15 words) |
|---|---|---|
| 1 | Is IRB Review Required? (hub) <https://irb.ucsd.edu/researchers/is-irb-review-required/index.html> | A hub page that links to the determination, student-research, definitions and "other determinations" pages. There is no separate class-project page and no interactive self-determination tool. |
| 2 | Determining if IRB Review is Required <https://irb.ucsd.edu/researchers/is-irb-review-required/determining-if-irb-review-is-required.html> | Two-part test: is it **research**, and does it involve **human subjects**? If both, it is under IRB oversight. "All human subjects research projects require IRB review, regardless of funding." If in doubt, "err on the side of submitting or consulting with OIA". "IRBs do not have the option of granting “retroactive” approval after research is done." |
| 3 | Student Research <https://irb.ucsd.edu/researchers/is-irb-review-required/student-research.html> (this is UCSD's class-project guidance) | Class projects "conducted for educational purposes and not as research, do not require IRB review". The exemption covers projects "not intended to develop or contribute to generalizable knowledge". But "Student Research that meet the definition of human subjects research, must obtain IRB approval". Instructors carry "an affirmative obligation to ensure that students understand their ethical obligations". The page says nothing about later publication. |
| 4 | Worksheet 310, Human Research Determination (PDF) <https://irb.ucsd.edu/_files/oia_sops/sop_refresh_2023/OIA-310%20WORKSHEET-Human%20Research%20Determination.pdf>, listed at <https://irb.ucsd.edu/researchers/guidance/worksheets-and-checklists.html> | OIA's own checklist. "Research" needs all four: an investigation, systematic, "designed to develop or contribute to knowledge", and that knowledge is *generalizable*. "Human subject" means data about living individuals obtained through intervention or "Communication or interpersonal contact with the individuals" (interviews are interaction). The worksheets page says researchers need not complete or submit it; it shows how OIA decides. |
| 5 | Other Administrative Determinations or Registrations <https://irb.ucsd.edu/researchers/is-irb-review-required/other-admin-determ-or-reg.html> | Projects outside the definition are excluded from IRB review, but you can file an abbreviated application to get confirmation. Publishers "may require documentation of OIA's determination of Not Human Subjects Research (NHSR)". It also defines non-clinical QI/QA: "Examples include teaching evaluations or customer service surveys", where intent "does not extend to developing or contributing to generalizable knowledge". |
| 6 | FAQs <https://irb.ucsd.edu/researchers/faqs.html> | OIA reviews "human subjects research for which UCSD or RCHSD are engaged". To get an official NHSR letter, submit an "Activity Not Human Subjects Research" application in Kuali. Questions go to irb@ucsd.edu. |
| 7 | EBP/QA/QI Projects <https://irb.ucsd.edu/researchers/qi_rchsd.html> | Covers clinical QI at UC San Diego Health and Rady Children's (ACQUIRE and E-QUAL committees). **Not relevant to AB-10**, which is not a health-system improvement project. |

Contacts: OIA at irb@ucsd.edu (FAQ page). The contact page is <https://irb.ucsd.edu/about/contact.html>.

## Reading of these pages for AB-10 (student-side, not a determination)

1. **"Human subjects" is very likely met.** The interviews are "communication or interpersonal contact" with living
   people. Part of the guide also asks for their own views (how they judge trust, their reactions to the mock-ups, and
   whether they would adopt). That is data about the individual, not only about their organisation's processes.
2. **So the question that decides it is whether this is "research", meaning designed to contribute to generalizable
   knowledge.** UCSD's student-research page exempts class projects meant only for teaching. AB-10 is different: it
   tests pre-registered hypotheses (H1-H3, P13), and its verdicts feed a wedge decision that shapes a paper.
   - If any interview content (coded tallies, paraphrases, the P13 verdict) appears in a paper, poster or public
     report beyond the course, it looks like generalizable knowledge on Worksheet 310's terms.
3. **The QI/"customer service survey" route is a weak analogy.** UCSD's non-clinical QI category covers evaluating or
   developing services "at an institution". Market discovery for a tool that does not exist yet is not obviously that.
   Do not rely on it without OIA saying so.
4. **Timing matters more than anything else.** OIA cannot approve retroactively. If there is any chance interview
   content will reach the paper, the determination has to be in hand *before* the first interview, not after.

## What Uzair should ask the course staff

Send this to the instructor (copy your domain mentor if appropriate) before recruiting anyone:

> "For AB-10 I plan 5-8 thirty-minute interviews with industry practitioners (SRE, marketing science, pharma RWE,
> policy analytics) about how they decide what caused what and how they judge trust in causal tools. I'll keep notes
> only, with role and sector, and no names or employers.
> 1. Is this activity designed to contribute to generalizable knowledge, or is it a course-internal exercise? If the
>    tallies or paraphrases might be published in a paper or shown outside the course, do I need an IRB determination
>    (NHSR or exempt review) from OIA first?
> 2. If you consider it course-internal only, can I record that decision in writing, with the condition that no
>    interview data appear in any paper?
> 3. If a determination is needed, who should be listed as faculty sponsor on the Kuali application?"

The core of the question, in one line: **"Is this activity designed to contribute to generalizable knowledge? If the
results may be published in a paper, does it need an IRB determination first?"**

## The two paths

### Path (a): course-internal market-discovery conversations, no publication of interview data

Use this path only if course staff confirm in writing that it is course-internal. Keep the email in
`docs/decisions/` as `YYYY-MM-DD_ab10_hs_path.md`, with the text pasted and without the sender's address.

- **What may use the notes:** AB-16 (the wedge decision memo), course deliverables and internal planning. The paper
  must not cite, tally or paraphrase interview content. It may say that "informal conversations shaped the product
  framing", without data.
- **Consent:** verbal, using `consent_script.md` with the path (a) paragraph. Notes only by default; audio only with
  explicit consent.
- **Notes:** role, sector and size band only (enforced by `notes_schema.json` and the PII refusal in
  `analysis/interview_synthesis.py`).
- **If plans change later** (for example, the wedge picks a product-and-paper spine that wants C1 data in the paper),
  the existing notes cannot be moved into the paper. Get a determination (path b) and run new interviews under it,
  or ask OIA explicitly about secondary use of the existing notes. Do not assume either.

### Path (b): interview content feeds a paper

**Get an HRPP determination first.**

- **Step 1.** Submit through Kuali, the system the FAQ page names. Choose one:
  - an "Activity Not Human Subjects Research" request, if you and the sponsor believe it is not research; or
  - an IRB application, likely for an exemption. The FAQ points to UCSD's exempt information-sheet template for
    interviews with adults.

  Use the protocol material in this folder: the guide, screener, consent script, notes schema and synthesis plan.
- **Step 2.** Students usually need a faculty sponsor or PI. Ask course staff who that is.
- **Step 3.** Wait for the letter before recruiting.
  - If OIA issues an information sheet or consent language, it **replaces** `consent_script.md`.
  - Change the path (b) paragraph to match it, word for word.
- **Records:** set `consent.path = "b"` in each note and put the determination or protocol reference in
  `consent.determination_ref`. The synthesis script refuses path (b) notes without one.

### Which path to default to

Path (b) has the downside of a delay (Kuali turnaround unknown; not read). Path (a) has the downside that C1 cannot
appear as evidence in the paper. AB-10's window is 14 Oct to 7 Nov, and the gate is 14 Nov, so a slow determination
could push interviews past the gate.

Suggested default:
- Ask the course staff question on day 1.
- If they cannot answer within a few days, run path (a) for the wedge decision only.
- File the path (b) determination in parallel, for any interviews that might feed the paper.

## What this note did not establish

- Kuali turnaround time for an NHSR request or an exempt review (not read).
- Whether DSC 180A has a standing course-level arrangement with OIA for capstone interviews (ask course staff).
- Whether interviewing people at named HDSI partner companies needs anything from the company's side. Companies
  sometimes require their own approval for employees to speak about work. That is the interviewee's call; the guide
  never asks for confidential information.

## Where we're going

Uzair sends the course-staff question and records the answer as a decision file. Recruitment (`screener.md`) starts
only after that. If the answer is path (b), the determination letter comes first.
