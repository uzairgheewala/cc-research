"""Page 1: what causal discovery is. Act I, for a newcomer: no result from Act II, no project jargon."""
from pagekit import *  # noqa: F401,F403
import main as L1  # the worked-example drawings

kappa = v("kappa.sem.D")

two_examples = f"""<div style="display: flex; flex-wrap: wrap; gap: 16px">
{box(f'<div style="overflow-x: auto">{L1.exA}</div><p class="prose" style="margin: 0"><b>Every direction can be recovered.</b> Rain and Sprinkler are independent of each other, but once you know the road is wet, learning that it did not rain makes the sprinkler more likely. That signature, two causes meeting in one effect with no link between them, is a {T("collider")}. It fixes both arrows into Wet road. Skids is then forced too: if it pointed into Wet road, Rain and Skids would form a second collider that the data do not show.</p>', flex="1 1 420px")}
{box(f'<div style="overflow-x: auto">{L1.exB}</div><p class="prose" style="margin: 0"><b>No direction can be recovered from the numbers.</b> All three chains imply the same thing: A and C are {T("ci", "independent once B is known")}. Graphs that agree on every such statement form one {T("mec")}, and data alone cannot tell them apart. The data can draw the {T("skeleton")} A — B — C and nothing more.</p>', flex="1 1 420px")}
</div>"""

BODY = "\n".join([
    question("What is being discovered, and why is direction the hard part?"),
    P(f"A dataset has one column per {T('variable')}: temperature, dosage, latency, sales. "
      f"<b>Causal discovery</b> tries to recover the arrows between them, a {T('dag')}. An arrow X → Y means that setting X "
      f"from outside would change Y, with everything else held fixed. That is a stronger statement than \"X and Y move together\": "
      f"it says what would happen if you intervened."),
    P(f"Every arrow hides two questions. First, are X and Y directly connected at all? The set of connections, ignoring direction, "
      f"is the graph's {T('skeleton')}, and each connection is an {T('adjacency', 'edge')}. Second, which way does each edge point? "
      f"That is its {T('orientation')}. The two examples below show why the second question is the hard one."),
    two_examples,
    H2("What the data can and cannot say"),
    P(f"Observational data, rows recorded without anyone setting anything, reveal which variables are independent of which, "
      f"given which others. If we assume {T('faithful', 'faithfulness')} (no independence arises from causes cancelling out "
      f"exactly), those statements determine the skeleton and the colliders, and nothing else. The result is one picture of the "
      f"whole equivalence class, a {T('cpdag')}: an arrow where every member agrees, an undirected edge where they disagree."),
    P(f"So the undirected edges are not a failure of any particular method. No method that reads only these numbers can orient "
      f"them. On the benchmark this project audits, {T('arena')}, {(1 - kappa):.1%} of the true edges in the semantic family are "
      f"of this kind."),
    H2("Two other kinds of evidence"),
    grid([
        box(f'{H3("Interventions")}<p class="prose" style="margin: 0">An {T("intervention")} sets a variable from outside and records '
            f'what happens. Everything downstream of the target can shift; nothing upstream can. One experiment on B settles the '
            f'chain above.</p>'),
        box(f'{H3("Declared knowledge")}<p class="prose" style="margin: 0">{T("knowledge")} is information that is not in the '
            f'numbers: what the variables are called, or an ordering such as "these are inputs, these are outcomes". A {T("tier")} '
            f'ordering says an earlier group may cause a later one but never the reverse. Knowledge is legitimate when it is '
            f'declared, and a hidden shortcut when it is not.</p>'),
    ], min_w=340),
    P("These three kinds of evidence, data, interventions and declared knowledge, return on every page that follows. The next "
      "page asks how a recovered graph is turned into the single number a leaderboard prints, and what the best possible number is."),
    answer("A causal discovery method recovers the connections (the skeleton) and their directions. Data alone settle the skeleton "
           "and the colliders; the remaining directions need an experiment or declared knowledge, whatever the method.",
           "If some directions cannot be recovered, what does a leaderboard score actually measure, and what is the best a method "
           "could score?"),
])
