# Where the ledger loses: every stage, every number (dev, kernel v2 and v3)

`analysis/q2_anatomy.py` and `analysis/q2_half_anatomy.py` from the engine cache; results in
`analysis/results/q2_v3/anatomy_dev.json` and `half_anatomy_dev.json`. Dev split, 125 files per family (25 scenarios x 5
replicates); regime D is one file of 1,000 rows, D x R is a scenario's five replicates pooled (5,000 rows, 25 tables).
Written 2026-10-15. No model calls; no test split read.

Words used: a *link* is "these two variables are directly connected"; a *direction* is which way a found link points; an
*answer* is "if I set T, does Y move?" (DV-1), answered yes, no, or not at all; a *shadow* is a false link between two
variables that are connected only through others.

**Correction to `q2_v3_k1_k2_dev.md` section 3.** That table blamed each wrong "yes" on the first edge of the claimed
path that is not in the true graph (381 reversed, 370 false, 54 backward shadows). The rule here blames the first edge at
which the claimed path leaves T's true descendants, which is the edge that actually makes the answer wrong. Under that
rule the semantic v2 split is 343 unrelated false links, 231 common-cause false links, 120 reversed true links and 111
backward shadows. The earlier count over-credited reversed links that sat early on a path which was wrong for another
reason. Section 3 of the dev report is superseded by the table below.

## 1. Links (the same for v2 and v3; v3 does not touch links)

| | semantic D | semantic D x R | formula D | formula D x R |
|---|---|---|---|---|
| true links | 5,120 | 1,024 | 4,365 | 873 |
| found | 3,473 (68%) | 781 (76%) | 2,897 (66%) | 625 (72%) |
| missed | 1,647 (32%) | 243 (24%) | 1,468 (34%) | 248 (28%) |
| of all true links: no usable signal (floor) | 9.0% | | 6.8% | |
| of all true links: search gap (a linear oracle test finds it) | 14.2% | | 20.1% | |
| of all true links: nonlinear-only signal | 5.2% | | 4.9% | |
| of all true links: only 5,000 rows find it | 3.8% | | 1.8% | |
| links claimed | 5,506 | 1,309 | 5,609 | 1,258 |
| false links | 2,033 (37% of claims) | 528 (40%) | 2,712 (48%) | 633 (50%) |
| false: shadow of a path | 1,106 (54%) | 318 | 1,468 (54%) | 349 |
| false: common cause only | 538 (26%) | 130 | 621 (23%) | 142 |
| false: unrelated | 389 (19%) | 80 | 623 (23%) | 142 |

Reading: a third of the real links are never found, and more than a third of the claimed links are not real. Half of the
false links are shadows: the variables are connected, just not directly. Pooling five replicates recovers a quarter of
the misses and adds a few false links.

## 2. Directions on found true links

| | sem v2 D | sem v3 D | sem v3 D x R | for v2 D | for v3 D | for v3 D x R |
|---|---|---|---|---|---|---|
| found true links | 3,473 | 3,473 | 781 | 2,897 | 2,897 | 625 |
| direction committed | 2,864 (82%) | 2,547 (73%) | 574 (73%) | 2,462 (85%) | 2,201 (76%) | 484 (77%) |
| committed and right | 2,420 (84% of committed) | 2,217 (87%) | 513 (89%) | 1,979 (80%) | 1,825 (83%) | 420 (87%) |
| committed and reversed | 444 | 330 | 61 | 483 | 376 | 64 |
| left open, truth also open | 194 | 252 | 52 | 130 | 164 | 34 |
| left open, truth orients it | 415 | 674 | 155 | 305 | 532 | 107 |
| committed on a link the truth leaves open (coin flips) | 156 (86 right) | 98 (53) | 22 (13) | 92 (47) | 58 (32) | 9 (6) |
| true links the truth itself leaves open | 435 of 5,120 (8.5%) | | 87 of 1,024 | 240 of 4,365 (5.5%) | | 48 of 873 |

By licence (v2, D): collider patterns 2,507 semantic at 87% right / 2,145 formula at 83%; Meek rule 2: 40 at 75% / 56 at
80%; Meek rule 1: 316 at 64% / 257 at 60%; rule 3: 1 / 4. v3 withdraws rules 1 and 3.

Reading: the data could in principle orient 91-95% of the true links (the truth leaves only 5-9% open), so the
equivalence class is not what caps directions. What caps them is that nearly every direction comes from a collider
pattern, and a collider pattern is only as good as the three links around it: a missed link between two parents, or a
false link next to a child, makes a fake collider and a reversed arrow. Reversed arrows are 13-17% of committed
directions and come almost entirely from this. v3 trades 9 points of commitment for 3 points of accuracy.

## 3. Answers (DV-1: "if I set T, does Y move?")

| | sem v2 D | sem v3 D | sem v3 D x R | for v2 D | for v3 D | for v3 D x R |
|---|---|---|---|---|---|---|
| pairs asked | 10,485 | 10,485 | 2,097 | 16,550 | 16,550 | 3,310 |
| answered | 8,436 (80%) | 7,260 (69%) | 1,355 (65%) | 14,312 (86%) | 12,494 (76%) | 2,561 (77%) |
| right | 0.756 | 0.793 | 0.864 | 0.814 | 0.843 | 0.865 |
| "nothing moves" floor (say no everywhere) | 0.652 | 0.652 | 0.652 | 0.694 | 0.694 | 0.694 |
| yes answers | 2,449 at 0.671 | 1,723 at 0.735 | 383 at 0.807 | 4,045 at 0.698 | 3,021 at 0.754 | 686 at 0.768 |
| no answers | 5,987 at 0.791 | 5,537 at 0.811 | 972 at 0.887 | 10,267 at 0.860 | 9,473 at 0.872 | 1,875 at 0.900 |
| wrong yes: unrelated false link | 343 | 216 | 34 | 630 | 434 | 96 |
| wrong yes: common-cause false link | 231 | 144 | 28 | 197 | 122 | 37 |
| wrong yes: reversed true link | 120 | 58 | 5 | 229 | 98 | 11 |
| wrong yes: backward shadow | 111 | 39 | 7 | 167 | 88 | 15 |
| wrong no: a missed link on the true path | 778 | 742 | 71 | 913 | 838 | 139 |
| wrong no: a reversed link on the true path | 473 | 302 | 39 | 524 | 376 | 49 |

Reading: a "no" is right only if the ledger saw every link on the true path and pointed each the right way. So the
precision of "no" is one minus the chance a path crosses a missed or reversed link, and misses are the larger share.
Wrong "yes" answers are mostly false links between unrelated or merely co-caused variables; reversed links are the
smaller cause (120 of 805), and the earlier report overstated them.

## 4. The confident half (v3, out of fold by scenario)

| | sem D | sem D x R | for D | for D x R |
|---|---|---|---|---|
| kept (half of all pairs) | 5,402 at 0.808 | 1,092 at 0.878 | 8,281 at 0.891 | 1,719 at 0.882 |
| kept yes | 1,053 at 0.752 | 289 at 0.830 | 1,495 at 0.835 | 382 at 0.806 |
| kept no | 4,349 at 0.821 | 803 at 0.895 | 6,786 at 0.903 | 1,337 at 0.904 |
| wrong answers kept | 1,038, 75% of them "no" | 133, 63% | 904, 73% | 202, 63% |
| dropped (the less confident answers) | 1,858 at 0.751 | 263 at 0.806 | 4,213 at 0.750 | 842 at 0.828 |
| probability the model assigns, range that holds 95% of answers | 0.6-0.9 | 0.8-0.9 | 0.6-1.0 | 0.8-0.9 |
| held-out (test) half precision, lower end | 0.830 [0.783] | 0.866 [0.799] | 0.908 [0.876] | 0.911 [0.863] |

Reading: the confidence model separates the halves by only 6-14 points. The kept half is four fifths "no" answers,
and three quarters of the wrong answers it keeps are wrong "no"s: wrong because of a link the ledger never saw, for
which no feature exists. This is not a feature-extraction problem; the features describe what the ledger has, and
what makes those answers wrong is absent from it by construction. The model is calibrated (section 5 of the dev
report) because it has learned the base rate of that absence, not because it can see it.

## 5. Why each open landmark is open

**ER-2, semantic (0.866 pooled, lower end 0.799; 0.830 single-file).** The half view is mostly "no" answers at
0.82 (D) or 0.89 (pooled). Their precision is capped by misses on the true path (742 of 1,044 wrong "no"s in D) and
reversed links (302). The misses are 9% floor, 14% search gap. Pooling cuts misses to 24% and lifts the half view to
0.866, but 25 pooled tables give an interval +/-0.06 wide, so the lower end lands at 0.799. Three things would move it:
fewer reversed links (an independent direction signal), fewer misses (only pooling has worked), narrower intervals
(more scenarios). Formula clears the bar for a reason that is partly structural: its true graphs are sparser (the
"nothing moves" floor is 0.69 against 0.65), so "no" is right more often, and its kept half is 82% "no".

**ER-3 (calibration).** Point error 0.021-0.026, under-claiming slightly in D. The rule asks for the interval's upper
end <= 0.05 and the realised-minus-claimed lower end >= -0.03; with 25 scenario clusters the intervals are +/-0.04-0.06
wide at a 0.000 point gap. Nothing in the kernel can narrow them. Only scenarios can.

**ER-4a (accuracy above GES).** The kernel's links are GES's links (rule C3 is GES-led, PC-audited), so its directed F1
is GES's up to the audit. Directions are already near what collider patterns can give (the truth leaves only 5-9% of
links open; the ledger's reversals come from fake colliders built on link errors). Beating GES therefore needs either
better links, which every tested lever failed to give, or a direction signal that does not depend on colliders:
pairwise asymmetry (non-Gaussian or nonlinear noise) or interventions. That is kernel v4's job.

**ER-4b (RCA 0.90).** 0.932 at coverage 0.917 on 44 issues; the lower end (0.841) can reach 0.90 only with at most one
miss. A count problem: more issues, not a different method.

## 6. What is right

Floors hold with margin (never below PC, +0.05 / +0.12). Provenance holds on every file. The same inputs give the same
ledger hash on any machine once the BLAS kernel is pinned. The abstention mechanism works as designed: the half it
drops is 6-14 points worse than the half it keeps, and calibration error is 0.02. Pooled replicates are a real lever
(misses -8 points, answers +7). Every dev experiment now takes seconds, and the floor is measured rather than assumed.
