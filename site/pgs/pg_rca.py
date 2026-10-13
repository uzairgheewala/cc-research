"""Page 7: where declared structure wins. Act II: AB-12 (PetShop root cause analysis)."""
from pagekit import *  # noqa: F401,F403

rca_table = table(
    ["Method", "Evidence", "Top-3 accuracy (test, 48 incidents)", "Answers given"],
    [["Learned graph (PC) + traversal", "D", n("ab12.b.ac3"), "all (52% of them empty)"],
     ["No graph: rank anomalies by correlation", "D", n("ab12.a.ac3"), "all"],
     ["Declared call graph + traversal", "D+K", n("ab12.c.ac3", bold=True), "all"],
     ["Declared call graph + traversal + abstention", "D+K", f"{n('ab12.d.ac3', bold=True)} on answered incidents", n("ab12.d.cov")]],
    mono_cols=(2,),
    caption="AB-12, AWS PetShop (Hardt et al., CLeaR 2024): 68 incidents, 48 held out for testing. The protocol was frozen "
            "before any test result was computed.")

BODY = "\n".join([
    question("Is there a real setting where stated structure plus abstention beats learning a graph?",
             before=f'{link("decisions", "page 5")} (decision value, abstention, bounded harm).'),
    P(f"Industry already answers one causal question every day: when a web service slows down, which upstream service caused it? "
      f"That is {T('rca')}. Commercial tools do not learn a graph for it; they use the service map the engineers already have, a "
      f"{T('topology')}. The AWS PetShop benchmark is the one public RCA dataset that ships such a map, so we could test the "
      f"choice directly, scored by {T('acat', 'AC@3')}: is the true root cause among the top three answers?"),
    rca_table,
    P(f"The declared map wins by a wide margin, and the learned graph loses even to plain correlation ranking. Abstaining when no "
      f"anomaly path is clear lifts accuracy on the incidents it answers, at {n('ab12.d.cov')} coverage. Shuffling the columns "
      f"changes nothing for the declared map and moves the learned one."),
    H2("What is not solved"),
    box(f"<p class='prose' style='margin: 0'>The abstention rule never fires on normal-period data. On latency metrics, "
        f"{n('ab12.fabricated')} of quiet windows still produce a root cause where there is none. A careful system has to make "
        f"that failure visible and cut it before anyone should rely on it. That is open work, not a result.</p>", tone="red"),
    answer(f"Yes. In incident root cause analysis, a declared service map scores {t('ab12.c.ac3')} top-3 accuracy against "
           f"{t('ab12.b.ac3')} for a learned graph, and abstaining raises it to {t('ab12.d.ac3')} on the incidents answered. The "
           f"same design (knowledge stated, data checked, silence allowed) is what the next page proposes in general. Its weak spot "
           f"is visible too: answers fabricated on quiet periods.",
           "What exactly does this project claim, and what would it build?"),
])
