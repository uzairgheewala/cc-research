# AB-10 verbal consent script

Ticket: AUD-41. Written 2026-10-12. Read this aloud at the start of every interview, before any question.

- It takes about 90 seconds.
- Under **path (b)** (see `human_subjects_check.md`), any information sheet or consent wording OIA approves
  **replaces this script**. Paragraph 4 below is the part that changes, and it is marked.
- Record consent only as `consent.verbal_consent = true` in the notes. Do not record the person's name or a
  signature.

## Where we are now

- **Path (a):** course-internal conversations. The notes are used for the course and internal planning only.
- **Path (b):** an HRPP determination is in hand, and anonymised notes may inform a paper.

The script is written for path (a), with the path (b) replacement given alongside.

## Script

**1. Who I am and why.**
"Thanks for making time. I'm Uzair, an undergraduate data science student at UC San Diego. This conversation is part
of my DSC 180A capstone project. I'm trying to understand how people in your kind of role decide what caused an
outcome, or whether changing something will move it, and how they decide whether to trust an answer. It should take
about 30 minutes."

**2. Voluntary, skip, stop.**
"Taking part is completely voluntary. You can skip any question, and you can stop at any point without giving a
reason. If you'd like me to drop something you said afterwards, just tell me, during the call or by email later, and
I'll delete it."

**3. What I record.**
"By default I'll take written notes only. I won't record audio or video.
- *(Only if you want audio for your own note-taking:)* Would it be OK if I recorded audio, just to check my notes?
  It's fine to say no. If you say yes, I'll delete the recording once my notes are written, within a week.
- I won't write down your name, your employer, or the names of anyone or any system you mention. The only things I
  keep about you are your general role level, your sector, and a rough company-size band.
- Please don't share anything confidential. You can describe things at the level of 'a kind of decision'."

**4. How the notes are used.**
- [PATH (a): read this version]
  "My notes are used only within my course project, to help my team decide what to work on. I'll paraphrase them.
  They won't be published, and nothing will identify you or your organisation."
- [PATH (b): REPLACE paragraph 4 with this version, or with OIA's approved wording if it differs]
  "My notes are paraphrased and stored without your name or employer. Anonymised summaries, for example how many
  people described a certain kind of decision, may appear in a research paper or presentation. No quote will be
  attributed to you, and nothing will identify you or your organisation. This project has been reviewed by UC San
  Diego's Office of IRB Administration [state the determination: 'determined not to be human subjects research' /
  'determined exempt', with reference number]."

**5. Contact.**
"If you have questions later, you can reach me at [your ucsd.edu email]. My course instructor is [instructor name and
ucsd.edu email]."
- *[PATH (b) adds:]* "If you have questions about your rights as a participant, you can contact UC San Diego's Office
  of IRB Administration at irb@ucsd.edu."

**6. Check.**
"Do you have any questions before we start? Are you happy to go ahead on that basis?"

- If they say yes: set `consent.verbal_consent = true`.
- If they agreed to audio: set `consent.audio_consent = true`, and `consent.audio_recorded = true` only if you
  actually recorded.
- If they hesitate or say no: thank them and end the call. Do not keep notes.

## After the call

- **Audio:** if recorded, delete it after writing the notes, within 7 days. Do not upload it anywhere: not the repo,
  not the project docs, not a transcription service, unless path (b)'s determination allows that.
- **Withdrawal:** if someone later asks to withdraw, delete their notes file. The next run of
  `analysis/interview_synthesis.py` recomputes the tallies without them.
- **Contact mapping:** the pseudonymous id to contact mapping stays outside the repo (see `screener.md`).

## Where we're going

Use this script for every interview. If course staff or OIA change any wording, update paragraph 4 (and paragraph 5
if contacts change) here before the next interview, and note the date of the change at the bottom of this file.
