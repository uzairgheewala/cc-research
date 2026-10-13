# Causal project (shape B) versus WorldReset: weighing (2026-10-06, discussion draft)

Companion to the research ledger and the ceiling-and-positioning note. No decision recorded; Uzair asked for the weighing before any detailed design of shape B.

## Inputs
- WorldReset text pasted by Uzair in chat on 2026-10-06 (shared mentor document). It lists 8 students: Uzair on Causal Discovery; Kyle Zhao, Bryan Nguyen, Juee Deshmukh, Scarlett Scott, Joey Sandoval, Vani Sahjwani, Palina Volskaya on Forecasting. The causal entry is two links (paper, repo). The forecasting entry has motivation, related work in six themes, two positioning tables, references, and a final heading "Candidate Data Sources and Integration Priorities" with nothing under it in what was pasted. The document invites students to "directly put your questions and choices here".
- Course slides `L0 - Intro.pdf` (read 2026-10-06, pages 1-20).
- FutureSim (arXiv 2605.15188), named by the WorldReset text as its closest foundation: replays a date-gated CCNews corpus, 1 Jan to 28 Mar 2026, 330 questions; best agent 25% accuracy, many with worse Brier skill than no prediction; ICML 2026 workshop oral; authors from Tübingen / MPI / Stuttgart.

## Course constraints (from the slides)
- The domain cannot be changed for two quarters; mentors can sponsor multiple projects, so both options sit inside D04.
- Quarter 1 project (50%): individual or group at the mentor's preference; a guided exploration such as a paper replication. Checkpoint due Mon 2 Nov 2026 (intro, data/method description, data processing and initial method code); final due Fri 4 Dec 2026 (results, shortcomings and possible improvements, reproducible code).
- Quarter 2 proposal (15%): written proposal with background research, weekly schedule, 2-3 minute elevator pitch; the mentor approves it.
- Quarter 2 project: "worked on in groups of 2-4. It's up to your mentor to choose the groups." Deliverables: public GitHub repo, public website, PDF report, poster; in-person showcase in the 2nd week of March 2027.
- Participation 15%, of which 10% is a mentor-assigned grade. TA check-ins: 19-23 Oct and 20-25 Nov 2026. D04's TA is Nate.
- Consequences: a solo Quarter 2 project is outside the stated 2-4 rule, so the causal option needs at least one more student or an exception; seven forecasting students cannot be one group, so they must split into at least two groups anyway; the mentor holds proposal approval, group formation and 10% of the grade.

## What the WorldReset text is and is not
- It is a positioning document for an environment: chronological replay of historical evidence (news, numerical series, discussions, multimedia in native form) with a persistent agent workspace, scored against resolved outcomes.
- It states no research question, hypothesis, metric beyond proper scoring, task split, or timeline in what was pasted.
- Its stated novelty over FutureSim is breadth of evidence types and fixed-date plus advancing-time episodes.
- Its acknowledged validity threat is temporal leakage (model already knows outcomes), which forces replay windows after every tested model's cutoff and therefore continuous refresh.

## Weighing
| Axis | Causal, shape B | WorldReset |
|---|---|---|
| Claim | Sharp and falsifiable: agents report recall as discovery; a refinement that is sound by construction wins under name controls | Infrastructure; the finding depends on what agents do once it exists |
| Evidence today | Harness, 30 live runs, three predictions supported on one dataset | Related-work text |
| Nearest competitor | Kitson and Constantinou; Zheng et al. (principle only) | FutureSim, 5 months old, strong group, same mechanism |
| Field | Small, slow | Crowded: about ten benchmarks in two years by the document's own tables |
| Validity threat | Few real datasets with ground truth; memorisation (which we control for) | Temporal leakage; archive availability for discussions and multimedia |
| Engineering | Moderate: add agents, datasets, models to an existing harness | Heavy: multi-source timestamped corpora, time-gated tools, long agent episodes |
| Uzair's share | Whole project | One slice among seven students plus the lab |
| Mentor attention | Low; and the findings criticise the mentor's own system | High; evidently the lab's active agenda |
| Course risk | Needs a teammate or an exception; proposal must be approved | Low |

## Reading
- Lean: stay with the causal project in shape B, on two conditions: at least one teammate (or a written solo exception), and a proposal framed as strengthening Causal-Copilot rather than auditing it.
- Reasons: the claim is sharper, the evidence already exists, the field is less contested, ownership is undivided, and Quarter 1 is essentially done.
- Case for switching: mentor attention and approval power sit with WorldReset; group work is the course default; a hot topic with a large audience.
- What would flip the lean: the mentor declining to approve a causal Quarter 2 proposal, or no teammate and no exception by the first TA check-in (19-23 Oct).
- Bridge worth using in the pitch: both projects face the same question, "is the agent recalling or reasoning". Time-gating is WorldReset's control for it; label permutation is ours.

## Still unknown
- Whether the mentor will allow a solo or two-person causal group.
- Who leads WorldReset in the lab and what each student's slice would be.
- The content of "Candidate Data Sources and Integration Priorities".
