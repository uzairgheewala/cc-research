# AB-10 screener: recruitment message, screening questions, target roles, channels

Ticket: AUD-41. Written 2026-10-12. **Do not send anything until the human-subjects question in
`human_subjects_check.md` has an answer.** Under path (b), use the recruitment wording OIA approves, which replaces
the template below.

## Where we are now

AB-10 needs 5-8 practitioners across four sectors. Each must have made or informed at least one real "what caused
this / should we change that" decision recently. This file covers who to look for, where to find them, and what to
say. Contact details for the people you reach stay in your own inbox or messages. They never go into the repo, the
notes or the project docs.

## Quotas

| Sector | Target | Minimum | Maximum | Why |
|---|---|---|---|---|
| IT operations / SRE (root-cause analysis) | 2 | 1 | 3 | AB-12 and the AB-14 IT brief |
| Marketing science (incrementality, MMM) | 2 | 1 | 3 | AU5 product angle 1 and the AB-14 marketing brief |
| Real-world evidence (pharma or health) | 1-2 | 1 | 2 | regulatory hooks (AB-13) |
| Policy analytics | 1-2 | 1 | 2 | program evaluation decisions |
| Total | 6-8 | 5 | 8 | AB-10 plan |

Other limits:
- At most one person from the same organisation, so that one team's habits do not count twice.
- At most one person who mainly works for a vendor of causal or RCA tools. Tag them `sector = other` if their
  practitioner sector is unclear, and note the vendor role in `role_level` terms only.

## Recruitment message (LinkedIn or email, path a)

Keep it short. Promise nothing you cannot keep, and offer no incentives.

> **Subject:** 30-minute conversation about how your team decides what caused what (UCSD student project)
>
> Hi [first name],
>
> I'm an undergraduate data science student at UC San Diego. For my capstone I'm studying how practitioners in
> [sector] decide what caused an outcome, or whether changing something will move it, and how they decide whether to
> trust a tool's answer.
>
> Would you be open to a 30-minute video call in the next few weeks? I'd ask about how decisions like that work in
> your role, and show you three short text mock-ups for your honest reaction. I'm not selling anything, and there is
> nothing to prepare.
>
> I'd keep written notes only, recording your general role and sector but not your name or employer. You can skip any
> question or stop at any time. I can't offer payment, but I'm happy to share a short summary of what I learn across
> all the conversations.
>
> [How I found you: e.g. "We're both on Tritons Connect" / "I saw your post in the PyWhy Discord" / "[course contact]
> suggested you"]
>
> Thanks for considering it,
> Uzair
> UC San Diego, DSC 180A capstone. [your ucsd.edu email]

**Path (b) change.** Add this sentence after the notes paragraph (or use OIA's approved wording): *"Anonymised,
paraphrased notes from these conversations may inform a research paper; nothing will identify you or your
organisation."*

**Follow-up.** Send at most one follow-up, after 5-7 days. No reply means no.

## Screening questions

Ask these in the reply thread or in the first two minutes of the call. Record the answers only as the coded fields in
the notes (`participant.*`). Do not record the free-text replies.

| # | Question | Fills | Include if |
|---|---|---|---|
| S1 | Which best describes your work: IT operations or SRE, marketing measurement or science, real-world evidence or health outcomes, policy or program analytics, or something else? | `participant.sector` | one of the four, or "other" within the vendor or academic limit |
| S2 | Roughly what level is your role: individual contributor, team lead or manager, director or above, or consultant or academic? | `participant.role_level` | any |
| S3 | In the last 12 months, have you made or directly informed a decision about what caused something, or whether changing something would move an outcome? | (screen only) | yes |
| S4 | Roughly how many people work at your organisation: under 50, 50-249, 250-999, 1,000-9,999, or 10,000+? | `participant.company_size` | any; record "unknown" if they prefer not to say |
| S5 | Are you comfortable with a 30-minute call where I keep written notes only? | consent pre-check | yes |

Exclude:
- anyone under 18;
- current UC San Diego students in DSC courses (classmates);
- anyone who would need to share confidential employer information to answer S3. Tell them the conversation can stay
  at the level of "a kind of decision", not a specific case.

## Target roles per sector

| Sector | Roles to look for | Decisions they typically own (for S3) |
|---|---|---|
| IT operations / SRE | site reliability engineer, platform or infrastructure engineer, observability engineer, incident commander or on-call lead, engineering manager for reliability | what caused an incident; whether to roll back a deploy; which alert or service to fix first |
| Marketing science | marketing scientist, MMM or measurement analyst, incrementality or experimentation lead, growth data scientist, agency analytics lead | whether a channel is incremental; budget reallocation across channels; whether to run a lift test |
| RWE (pharma or health) | epidemiologist, RWE scientist, HEOR analyst, biostatistician on observational studies, health-system analytics lead | whether an exposure affects an outcome in observational data; study design and confounder choice; what to pre-specify |
| Policy analytics | program evaluation analyst, government or regional-agency data scientist, public-health department analyst, policy think-tank researcher | whether a program moved an outcome; where to expand or cut a program |

## Where to find people (verified 2026-10-12 unless marked)

All of these are opt-in channels where people expect professional contact. Do not scrape, export or compile lists of
named people from any of them. Reach out one at a time, by hand.

| Channel | What it is (verified) | How to use it |
|---|---|---|
| **UC San Diego alumni: Tritons Connect** <https://alumni.ucsd.edu/career/tritons-connect.html> | UCSD's alumni platform, described as "an exclusive UC San Diego platform built to connect". The career page says it supports mentoring and finding Tritons in your field. | Search by field (SRE, marketing analytics, epidemiology, policy). Message people who list themselves as open to helping students. Whether students can message alumni directly is **not confirmed** on the page; check after you join. |
| **Take a Triton to Work** (on the alumni career page <https://alumni.ucsd.edu/career/index.html>) | Alumni and Career Center programme that matches alumni with students for career conversations. | Seasonal. Use it only if a cycle is open. It is for career exploration, so say clearly that you also want to ask about their work decisions. |
| **HDSI Industry Partner Alliance** <https://datascience.ucsd.edu/industry/partnership-programs/> | Exists. The page lists 16 partner organisations, including Deloitte, Dexcom, FICO, Guardian Life, Intel, Qualcomm, SANDAG, SDG&E, Teradata and Viasat. Its only contact is the Industry Relations office, and the page is aimed at companies, not students. | **Go through course staff**, not a cold email to the Industry Relations office. Ask the instructor or your mentor whether a partner contact could forward the recruitment message. Sector fits: SANDAG for policy, Dexcom for health, FICO or Guardian for analytics. |
| **PyWhy Discord** (link from <https://github.com/py-why> and <https://www.pywhy.org/community/discord.html>) | PyWhy's Discord, "a space for like-minded casual machine learning researchers and practitioners". The site says meetings are "held every Monday at 8am PT/11am ET". They alternate every two weeks between Office Hours and Community Discussions (check Discord for the current schedule). | Join, read the server rules, and **ask a moderator before posting a recruitment message**. Post once in the channel they suggest. A community discussion call is a good place to listen first and ask afterwards. |
| **Online Causal Inference Seminar** <https://datascience.stanford.edu/causal/online-causal-inference-seminars> | Mailing list for an online seminar. The Stanford page shows no event after April 2023, so whether it is active is **not confirmed**. Its audience is mostly academic. | Low priority. Only useful for policy or RWE academics-turned-practitioners. |
| **Causal-inference meetups (general)** | **Not verified.** No single current meetup was confirmed. | If you find one (Meetup.com, a local data-science group), attend first and ask the organiser before recruiting. |
| **Course TA / mentor contacts** | The course's own network. | Ask the instructor, TA and domain mentor for one or two warm introductions per sector. Warm introductions answer faster and are less biased toward people who like causal tooling. |

**Selection bias to record.** PyWhy and causal-inference communities over-sample people already interested in causal
methods, which would inflate H1 and H3. Record the channel in `participant.recruited_via`. The synthesis reports
verdicts both with and without community-recruited interviewees.

## Scheduling and logistics

- Use the person's preferred video tool. Do not record by default.
- Keep a private mapping from pseudonymous id (P01, P02, ...) to contact thread in your own email or calendar,
  **outside the repo**. Delete it after the course ends.
- Write the notes record (`notes_template.md`) within 24 hours.

## Where we're going

Once course staff have answered, send 10-14 messages (about 2:1 to reach 6-8 interviews), starting with warm
introductions. Then run the interviews with `guide.md` and `consent_script.md`.
