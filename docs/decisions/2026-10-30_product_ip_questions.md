Tickets: PRD-02 (with PRD-01, PRG-01; P3-4; the written confirmation is CRS-09). Written 2026-10-30 by W4. Desk research
only: no model calls, no API spend.

# Before any product step: IP, licence and private-core questions for Prof. Umesh and Prof. Huang

**This is not legal advice.** It records what the public policy pages and licence files say, which facts about this
project those rules turn on, and which questions need a person who can answer for the university or for the law.
Section 6 lists what needs an expert.

## Where we are now

Program v3 (sections 5-6, decision P3-4) proposes a private repository for B's engine core and a possible pharma product.
Before either, three things must be settled: who owns what the project creates, what Causal-Copilot's licence allows, and
whether the course and the mentor accept the plan. Reading the actual pages changed two of program v3's assumptions:

1. **"MIT-licensed, so a derived product is allowed with its notice kept" is incomplete.** Causal-Copilot's own code is
   MIT, but its tree includes a file marked "License: GPLv2", and it imports tigramite, which is GPL-3.0 (section 3).
2. **The relationship question is larger than authorship.** Causal-Copilot's README gives the contributors' affiliation
   as "UCSD, Abel.ai", and a June 2026 press release names Prof. Huang as founder of Aether AI, a company building "causal
   world models" (section 4).

On ownership, the UC pages point the same way for this project, conditional on facts Uzair must confirm (section 2):
students who are not UC employees and do not use significant university resources generally own their work, and UC's
FAQ says a capstone student will "probably own the IP" absent other obligations. The campus technology transfer office
makes the final determination.

## 1. What the policies say

| # | Policy or page (issuer; date) | What it says (short quotes) | Label; link |
|---|---|---|---|
| U1 | **Intellectual Property as a Student at UC** (UC Office of the President; undated page) | "In most cases, students who are not employed by UC own their original academic work." "Under law and policy, UC owns IP made by UC employees in the course and scope of their work." "When University gift/grant/contract funds, resources, or research facilities are used, UC may also own the resulting IP." The campus technology transfer office "would make the final determination." | primary; [UCOP](https://ucop.edu/research-policy-analysis-coordination/policies-guidance/intellectual-property/intellectual-property-as-a-student-at-the-university-of-california.html) |
| U2 | **Student IP FAQ** (UCOP) | On a capstone: absent other obligations, students will "probably own the IP"; company involvement adds complexity, so consult the capstone professor or the office. UC may own an invention if the student was an employee who signed the Patent Acknowledgment or "used University research funds, resources or facilities". Some financial aid (federal work-study, NSF REU, certain fellowships) can carry IP obligations. | primary; [UCOP FAQ](https://ucop.edu/research-policy-analysis-coordination/policies-guidance/intellectual-property/intellectual-property-as-a-student-at-the-university-of-california-faq.html) |
| U3 | **UC Copyright Ownership Policy** (UC; issued 1 Feb 2021) | "copyright ownership of works prepared by University students (including graduate students) resides with such students", except works made primarily in University employment, with Significant University Resources, or sponsored, contracted or commissioned. Significant University Resources means resources "beyond the usual support provided by the University"; financial aid does not count. Software is listed among scholarly works. | primary; [UC copyright page](https://copyright.universityofcalifornia.edu/resources/copyright-ownership.html), [policy PDF](https://copyright.universityofcalifornia.edu/files/documents/copyright-ownership-2021.pdf) |
| U4 | **UC Patent Policy** (UC; issued 2 Feb 2024, effective 1 Jul 2024) | Applies to "All University employees, non-employees using University Research Facilities", and non-employees working under gift, grant or contract funds. Employees sign the Patent/IP Acknowledgment at hire; non-employees using facilities or funding sign before access. Covered persons must "promptly report and fully disclose all Inventions". Software is covered only where UC retains the copyright; student-owned works are excluded. | primary; [UCOP policy](https://policy.ucop.edu/doc/2500493) |
| U5 | **UCSD Office of Innovation and Commercialization (OIC): IP policies list** (UCSD; updated 4 Oct 2022) | A list of links to the UC policies above, plus UCSD's Copyright Guidelines (PPM 500-5) and Ownership of Course Materials. No student-specific text. | primary; [Blink](https://blink.ucsd.edu/sponsor/oic/ip-policies.html) |
| U6 | **UCSD OIC: Copyright** (UCSD) | "Copyrightable works include software (code/executable)"; the UC Copyright Ownership Policy "applies to all employees and students at all UC locations". Contact: oic-commercialize@ucsd.edu, (858) 534-2230. | primary; [OIC](https://innovation.ucsd.edu/disclose-patent/copyright.html) |
| U7 | **UCSD OIC: Using AI in research and invention** (UCSD; undated) | Unpublished inventions are Protection Level P3 and should "stay out of public and third-party AI tools"; doing otherwise "may count as a public disclosure and can permanently forfeit patent rights", especially outside the US. Paid or enterprise accounts are not automatically safe; TritonGPT is the approved option. "Only natural persons can be inventors under U.S. law." | primary; [OIC FAQ](https://innovation.ucsd.edu/disclose-patent/ai-and-intellectual-property.html) |
| U8 | **UC open-source guidance** (UCOP) | UC staff and faculty releasing UC-owned software as open source work through their campus licensing official. Students are not addressed. | primary; [UCOP OSS](https://security.ucop.edu/resources/open-source-software-licensing.html) |

Not read: UCSD PPM 500-5 (the link redirects to a login-gated policy system); the Ownership of Course Materials policy
(about instructors' materials); any DSC 180 course agreement, if one exists.

## 2. The facts the rules turn on (Uzair to confirm)

| Fact | What the files show | Why it matters (rule) |
|---|---|---|
| Employment by UC (TA, tutor, reader, research assistant) while doing this work | **none** (Uzair, 31 Oct) | Employees' work in the course of employment belongs to UC (U1, U3); employees sign the Patent Acknowledgment (U4) |
| Signed a Patent/IP Acknowledgment for any role | **none** (Uzair, 31 Oct) | It assigns inventions under U4 |
| Machines | the project runs on Uzair's two laptops (`claude/w5-restart-2026-10-30.md`, `docs/hosts.md`) | Personal machines are not University resources |
| Compute or data from UCSD (the course's DSMLP cluster, lab servers, lab data) | **none** (Uzair, 31 Oct) | Use beyond "the usual support" can make UC an owner (U3); research facilities bring U4 in |
| Model API spending | Uzair's own key (project memory; AGENTS.md rule 5) | Paid by the student, not the University |
| Funding: grants, fellowships, research stipends, beyond ordinary financial aid | **none, and no financial aid** (Uzair, 31 Oct) | Some aid carries IP terms (U2); ordinary aid does not count (U3) |
| Course agreement: anything signed for DSC 180 about IP or industry partners | **none** (Uzair, 31 Oct) | A sponsored or commissioned capstone changes ownership (U2, U3) |
| Ideas from the mentor or her group | unknown; the mentor framed the Q1 task (project memory) | Joint inventorship and co-authorship follow who conceived what (U2) |
| Public disclosure | cc-research is a public GitHub repository, kernel included (program v3, section 6); the fork is public | Published ideas are prior art; patent options on them are limited (expert question X3) |
| AI tools in development | the system is developed with Claude, a third-party AI tool | OIC treats this as a possible public disclosure for unpublished inventions (U7) |

Uzair confirmed on 31 Oct that the first, second, fourth, sixth and seventh rows (employment, acknowledgment, compute,
funding, course terms) are all "no". On that basis the policies read as: Uzair owns the copyright in his own
code and writing (U3), the patent policy does not reach him (U4), and the office still makes the final determination
(U1). That is a reading for discussion, not a determination.

## 3. Licences

**Causal-Copilot itself (primary; `../Causal-Copilot/LICENSE`, upstream a31aa7c).** MIT License, "Copyright (c) 2026
Causal-Copilot contributors". Use, copying, modification, sublicensing and sale are permitted provided "The above
copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."
The README says "Distributed under the MIT License"
([GitHub](https://github.com/Lancelot39/Causal-Copilot)).

**What else is in the tree (project measurement; read from the local copy on 30 Oct):**

| Component | Licence found | How Causal-Copilot uses it | Label |
|---|---|---|---|
| `externals/causal-learn` | MIT ("Copyright (c) 2022 cmu-phil") | vendored | primary (its LICENSE file) |
| `externals/pyCausalFS` | No LICENSE file in the tree. Three files carry GPL text; `CBD/MBs/common/g2test.py` says it is "logically copied and pasted from the pcalg package for R" and "License: GPLv2" | vendored; loaded by `causal_discovery/wrappers/bamb.py` and `hiton_mb.py` | primary (file headers) |
| tigramite 5.2.7.0 | GPL-3.0 | imported by `causal_discovery/wrappers/pcmci.py` (PCMCI) | primary; [GitHub](https://github.com/jakobrunge/tigramite) |
| `externals/notears`, `externals/pc_adjacency_search`, `externals/acceleration` | no licence file or header found | vendored | project measurement (absence) |
| The other ~120 pinned packages (gcastle, lingam, dowhy, econml, causalnex, semopy, xges, ...) | not checked | installed from `requirements_cpu.txt` | not checked |

What this means, in plain terms and pending an expert (X1):

- Code that B writes from scratch and that does not include or link these GPL parts is not affected by them.
- Shipping a product that includes the GPL files, or that imports tigramite, may bring GPL conditions on what is
  distributed. Whether running it as a hosted service counts as distribution under these licences (GPL, not AGPL) is a
  question for an expert.
- The simplest engineering answer is an allowlist: the private core imports no GPL package and copies no file from
  `externals/pyCausalFS`. W3 can check this mechanically on every build.
- The data licences (CausalBench and Replogle files, CausalArena, Causal Chambers) for product use were not checked. That
  is experiment E0 in `analysis/reports/product_pharma_bars.md`.

## 4. Relationships

- **Prof. Huang is a core contributor to Causal-Copilot** (README, "Core Contributors: Xinyue Wang, Kun Zhou, Wenyi Wu,
  Biwei Huang"; primary). The README lists the affiliation as **"UCSD, Abel.ai"** and links a hosted demo at
  causalcopilot.com (primary). Abel.ai's role is not stated anywhere read.
- **A press release of 6 June 2026 names Prof. Huang as founder of Aether AI**, "a frontier AI company building causal
  world models", focused on robotics and physical AI; pharma is not named as a target (primary;
  [ACCESS Newswire](https://www.accessnewswire.com/newsroom/en/business-and-professional-services/beyond-correlation-aether-ais-prof.-biwei-huang-introduces-causa-1173787)).
  A $20M seed round is reported (second-hand;
  [Runtime Wire](https://runtimewire.com/article/aether-ai-biwei-huang-20m-causal-world-models-seed)).
- Why it matters: a product built from her group's software, in a neighbouring field, may meet a commercial interest of
  hers or of Abel.ai, and her views on credit, competition and conflict of interest should be heard before anything is
  built. Asking directly is the respectful route (Uzair is in her group). The plan must not depend on her answer.

## 5. The questions

### 5.1 For Prof. Umesh (course; send with the CRS-09 confirmation email or straight after it)

1. **Private core.** Q2 requires a public repository, a website, a report and a poster. Would this satisfy it? The
   public Q2 repo holds the paper's code, the ledger format, a public verifier that re-derives every published claim
   from its evidence, a baseline engine, and every result's ledger. The engine core (decision logic, confidence models)
   sits in a private repository shared with course staff on request. If not, the fallback is that the engine stays
   public for the course, and any product work starts after March from a clean, separately written core.
2. **Course terms.** Does DSC 180 have any agreement, sponsor or industry partner whose terms cover IP made in this
   capstone? Is anything signed by students that would?
3. **Course resources.** Does the course treat DSMLP or other course-provided compute as "usual support" under UC's
   copyright policy? (This matters only if Uzair used them.)
4. **Grading and publication.** Is grading based on a private repository acceptable when the paper's claims can be
   re-checked from the public verifier? Does showing the private repo to course staff count as publishing it?
5. **Who to ask.** Does the course send students to OIC (U6) for capstone IP questions, or is there a course contact?

Default if there is no reply by the Q2 repo decision: take the fallback in question 1 (engine public for the course; clean
core after March). This is the default program v3 already lists for P3-4.

### 5.2 For Prof. Huang (mentor; Causal-Copilot author)

1. **Commercial plans.** Do you, Abel.ai or Aether AI have commercial plans for Causal-Copilot or derivatives of it,
   especially in pharma or biostatistics? Would a product built on a separately written core conflict with them?
2. **Credit.** How do you want your group's work credited in a Q2 paper about a system that started from Causal-Copilot's
   shell? On which parts would you expect co-authorship?
3. **Ideas from the group.** Has anyone in the group contributed ideas to the kernel or the ledger that should be
   recorded as theirs? (Inventorship follows who conceived an idea; U2.)
4. **Lab resources.** Is there anything the project has used, or might use, that counts as the lab's: data, compute,
   unpublished code?
5. **Interest.** Would you or your company want to be involved in, or told about, a product step? Do you see a conflict of
   interest in mentoring it?
6. **Licence intent.** Was the MIT release meant to allow commercial derivatives? Are you aware of the GPL parts in
   `externals/pyCausalFS` and the tigramite import?

Default if there is no reply: proceed as if the answer to 1 were "yes, possible conflict". No product step uses any
Causal-Copilot code, the core is written from scratch, and the Q2 paper credits Causal-Copilot as the starting system.

## 6. What needs an expert (flagged)

| # | Question | Who | Why it cannot be settled here |
|---|---|---|---|
| X1 | Do the GPL components (a GPLv2 file in pyCausalFS, tigramite under GPL-3.0) affect a product, and does a hosted service count as distribution? | an independent attorney, or a campus licensing official | Licence interpretation |
| X2 | Given the answers in section 2, who owns the code and ideas of B's core? | UCSD OIC (oic-commercialize@ucsd.edu, (858) 534-2230) | The office makes the final determination (U1) |
| X3 | Are patents realistic for anything already in cc-research's public history, or developed with a third-party AI tool? Is the realistic protection for a new private core copyright plus keeping it confidential? | OIC, then a patent attorney | U7 says AI-tool use may count as public disclosure; public GitHub history is prior art |
| X4 | Does a product used in FDA submissions need 21 CFR Part 11 validation (FDA's 2023 RWD/RWE guidance, III.B.6, [PDF](https://www.fda.gov/media/171667/download)), and what would that cost? | a regulatory-affairs or quality specialist | P2-8 in the pharma bars report |
| X5 | Forming a company, conflict of interest with a mentor's company, and any equity or licence-back terms | an attorney; the campus conflict-of-interest office | Beyond course and policy pages |
| X6 | Product-use terms of the data files (CausalBench and Replogle, CausalArena, Causal Chambers) | the data owners' licence pages first; an attorney if unclear | Not yet read (E0) |

## 7. What changes for W5

- Program v3, section 5: the licence point needs the GPL caveat (section 3), and the IP point needs the relationship
  facts (section 4). Proposed wording is in `analysis/reports/product_pharma_bars.md`, section 8 (C2, C5).
- PRD-02's evidence is this file once Uzair has confirmed section 2 and sent the questions. CRS-09 (Prof. Umesh's written
  confirmation of the one-person group) is a natural place to attach question 1.

## Where we're going

1. Done 31 Oct: the five deciding rows of section 2 are all "no". Still open there: ideas from the mentor's group (row 8).
2. The Umesh questions go out with, or right after, the CRS-09 email; the Huang questions go at the next mentor meeting,
   asked directly.
3. X2 (OIC) is still worth one email to confirm the reading in writing before any commercial step; it is no longer urgent.
4. W3 adds a licence allowlist check to the private core's build (no GPL imports, no files copied from `externals/`).
