"""Page 2: how a graph becomes one number, and the best number possible. Act I: methods and limits only; the layout leak
and every agent number wait for Act II."""
from pagekit import *  # noqa: F401,F403
from common import deriv, m
import bounds as L2

dev_sem = max(abs(v("m.%s.aS" % k) - v("m.%s.F1_forced_reported" % k)) for k in ("PC", "GES", "FCI", "LiNGAM", "NOTEARS"))
ident = deriv("From a graph to one number: F1 = S × a", [
    (f"Compare the system's connected pairs with the truth: {m('TP')} found, {m('FP')} extra, {m('FN')} missed. "
     f"{m('P = TP/(TP+FP)')}, {m('R = TP/(TP+FN)')}, {m('S = 2PR/(P+R)')}.", "the skeleton F1"),
    (f"Of the {m('TP')} found pairs, a share {m('c')} is given a direction and a share {m('q')} of those is right. "
     f"The other {m('1 − c')} are undecided.", ""),
    (f"The leaderboard orients each undecided pair at random, half right on average, so the share of found pairs pointing the "
     f"right way is {m('a = c·q + (1 − c)/2')}.", ""),
    (f"Every predicted pair becomes exactly one arrow: {m('TP + FP')} arrows, of which {m('a·TP')} are right. An extra pair "
     f"can never give a right arrow.", ""),
    (f"Directed precision {m('= a·P')}; directed recall {m('= a·R')}; so directed F1 {m('= a·S')}.",
     "exact per scenario; over a family the means differ by their covariance, at most %.3f for the five methods below" % dev_sem),
    (f"Differentiate: {m('∂F1/∂c = S·(q − ½)')}. Committing a direction pays only when {m('q > ½')}; below that, leaving the "
     f"pair to the coin scores more.", "a fact that returns on page 5"),
])

ROWS = [("PC", "PC"), ("GES*", "GES"), ("FCI*", "FCI"), ("LiNGAM", "LiNGAM"), ("NOTEARS", "NOTEARS")]
worked = table(["system", "S", "c", "q", "a", "a·S", "reported F1"],
               [[lab] + [n("m.%s.%s" % (k, c)) for c in ("S", "c", "q", "a", "aS", "F1_forced_reported")] for lab, k in ROWS],
               mono_cols=range(7),
               caption=f"Semantic family, the 50 public scenarios (* on the {t('m.GES.scenarios')} where the method finishes). "
                       "a·S uses family means, so it differs slightly from the reported mean of per-scenario F1.")

k_sem = v("kappa.sem.D")
limits = deriv("Deriving the limits", [
    ("Observational data reveal conditional independencies and, given faithfulness, nothing else. No method can tell apart the "
     "graphs of one equivalence class.", ""),
    (f"So the best a method can do from data: a perfect skeleton ({m('S = 1')}), commit exactly the "
     f"{T('compelled', 'compelled edges')} ({m('c = κ, q = 1')}), and leave the rest to the coin: {m('a = (1 + κ)/2')}.", ""),
    (f"Semantic scenarios: κ = {n('kappa.sem.D')}, which gives a {T('limit')} of {n('lim.sem.D', bold=True)} averaged per "
     f"scenario (lowest scenario {n('lim.sem.D.min')}). Formula: κ = {n('kappa.for.D')}, limit {n('lim.for.D')}.", ""),
    (f"Interventions reveal the direction of every edge touching a target, and the propagation rules carry it further: κ rises "
     f"to at least {n('kappa.sem.DI')}, so the limit is at least {n('lim.sem.DI', bold=True)} (formula {n('lim.for.DI')}).",
     "a lower bound: only edges touching a target were counted"),
    (f"Correct declared knowledge of the order orients every connected pair: {m('κ = 1')}, limit <b>1.000</b>.", ""),
    (f"The skeleton reaches S = 1 only as rows grow without bound. At 1,000 rows there is no closed bound, only the best "
     f"measured: GES, S = {n('m.GES.S')} where it runs.", ""),
])

lanes = (L2.lane(80, [("lim.sem.D", "limit from data", "#17201B", 200, True), ("pub.sem.D.best", "best published", "#1D5C99", 200, True),
                      ("pub.sem.D.GIES", "GIES", "#1D5C99", 200), ("m.GES.F1_forced_reported", "GES, our run*", "#1D5C99", 200),
                      ("pc.F1", "PC, our run", "#1D5C99", 200), ("pub.sem.D.LiNGAM", "LiNGAM, published", "#1D5C99", 200),
                      ("m.NOTEARS.F1_forced_reported", "NOTEARS, our run", "#6A716B", 200)])
         + L2.lane(500, [("lim.sem.DI", "limit", "#17201B", 150, True), ("pub.sem.DI.best", "best published", "#1D5C99", 150, True),
                         ("pub.sem.DI.TabCausal", "TabCausal", "#1D5C99", 150)])
         + L2.lane(680, [(1.0, "limit if knowledge is right", "#17201B", 210, True),
                         ("oracle.depth.reg", "true order + regression", "#B85A12", 210, True),
                         ("oracle.inputs.pc", "PC told the inputs", "#B85A12", 210)]))
chart = f"""<div style="position: relative; width: 920px; height: 770px">
{L2.grid}
<div style="position: absolute; left: 60px; top: 80px; width: 1px; height: 640px; background: #6A716B"></div>
{L2.heads}{L2.budget}{lanes}
<div style="position: absolute; left: 80px; top: 742px; width: 820px; font-size: 12px; line-height: 16px; color: #4E5751">Semantic family, directed F1, undecided pairs oriented at random. Published numbers are over all 100 scenarios; ours over the 50 public ones (* where the method runs). The orange markers are oracles: they price a piece of knowledge, they are not methods.</div>
</div>"""

lim, pcS, pcF = v("lim.sem.D"), v("pc.S"), v("pc.F1")
gap = lim - v("pub.sem.D.best")

BODY = "\n".join([
    question("What does a leaderboard number measure, and what is the best possible?",
             before=f'{link("primer", "page 1")}: skeleton, orientation, equivalence class, interventions and declared knowledge.'),
    P(f"A leaderboard compares a method's graph with the true one and prints one number, usually directed-edge "
      f"{T('prf', 'F1')}: the harmonic mean of precision (how many claimed arrows are true) and recall (how many true arrows "
      f"were claimed). An arrow counts only if both the pair and the direction are right. Undecided pairs are a problem for any "
      f"score, so the public leaderboard uses {T('forced', 'forced choice')}: every undecided pair is turned into an arrow at "
      f"random. {T('strict', 'Strict scoring')}, which counts undecided pairs as no prediction, is the alternative."),
    H2("One number, three coordinates"),
    P(f"That single number factors exactly into three things a reader can interpret: the {T('S', 'skeleton F1')} S, the "
      f"{T('c', 'commit rate')} c, and the {T('q', 'commit accuracy')} q. Together they give the {T('a', 'direction accuracy')} "
      f"a, and F1 = S × a."),
    f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(520px, 100%), 1fr)); gap: 16px; align-items: start">{ident}<div style="display: flex; flex-direction: column; gap: 10px">{H3("Worked through on five methods")}{worked}{P("PC&#39;s committed directions are barely better than a coin. FCI commits few directions but most of them are right. NOTEARS commits every direction at an accuracy below a coin.", 15)}</div></div>',
    H2("The best possible number"),
    P(f"Which evidence a method is allowed to read is its {T('regime')}: D for data only, D+I with interventions, D+K with "
      f"declared knowledge, D+I+K with both. Each regime has a ceiling that no method can pass, however good its statistics."),
    limits,
    H2("Every system on one scale"),
    P(f"The chart puts the limits, the published leaderboard and our own runs of the same methods on one scale. The PC bar "
      f"splits the distance to the limit into an {T('budget')}: {1 - lim:.3f} is not identifiable at all, {lim - pcS:.3f} is "
      f"lost in the skeleton, and {pcS - pcF:.3f} in directions. In the D+K column, the markers are {T('oracle', 'oracles')}: "
      f"they show what a given piece of correct knowledge would be worth."),
    figure(chart, f"Between the best published result ({n('pub.sem.D.best')}, {t('pub.sem.D.best.method')}) and the limit from "
                  f"data there is {gap:.3f} of the scale left. Matching {t('pub.sem.D.best')} needs, for example, S = 0.80 with "
                  f"a = 0.79."),
    answer(f"A leaderboard number is S × a: how many right pairs a method found, times how often those pairs point the right "
           f"way. From data alone the ceiling is about {t('lim.sem.D')} on CausalArena's semantic family; the best published "
           f"method reaches {t('pub.sem.D.best')}, and the gap splits into skeleton and direction losses.",
           "Where does this one family sit among all the problems causal discovery could be asked to solve?"),
])
