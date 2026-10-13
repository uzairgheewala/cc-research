"""Every technical term the site uses: its definition, the page that teaches it, and the surface forms the build looks for.

The build enforces "no jumping ahead": a page may use a term (marked with pagekit.T, or any of its surface forms in the
page's visible text) only if the term's introducing page comes at or before it in site/pages.py. Home, the generated
Act IV pages and the reference pages are exempt from the surface scan (they link terms to the glossary instead).
Surface forms are regular expressions matched case-insensitively against visible text, on word boundaries.
"""

# id: (display name, definition, introducing page slug, [surface regexes])
TERMS = {
    # ---- page 1, primer
    "variable": ("Variable", "One measured quantity: one column of the data file.", "primer", []),
    "dag": ("Causal graph", "Arrows X → Y meaning: setting X from outside would change Y with everything else held fixed. "
            "No loops, so it is a directed acyclic graph (DAG).", "primer", [r"\bDAGs?\b", r"causal graphs?"]),
    "adjacency": ("Edge, adjacency", "A direct connection between two variables, ignoring which way it points.", "primer", [r"adjacenc(y|ies)"]),
    "skeleton": ("Skeleton", "The graph with arrowheads removed: only which pairs are directly connected.", "primer", [r"skeleton"]),
    "orientation": ("Orientation, direction", "Which way an edge points.", "primer", [r"orientation"]),
    "ci": ("Conditional independence", "X and Y tell you nothing more about each other once Z is known. Observational data reveal "
           "these and nothing else about structure.", "primer", [r"conditional(ly)? independen"]),
    "collider": ("Collider", "X → Z ← Y with X and Y not connected. The one pattern observational data can orient by itself; "
                 "propagation rules then orient more.", "primer", [r"collider", r"v-structure"]),
    "mec": ("Equivalence class", "All graphs that imply exactly the same conditional independencies. Observational data cannot "
            "tell its members apart.", "primer", [r"equivalence class"]),
    "cpdag": ("CPDAG", "One picture of an equivalence class: an arrow where every member agrees, an undirected edge where they "
              "disagree.", "primer", [r"\bCPDAGs?\b"]),
    "faithful": ("Faithfulness", "Every independence in the data comes from the graph, none from causes cancelling out.", "primer",
                 [r"faithful"]),
    "intervention": ("Intervention (I)", "Data recorded after a variable was set from outside. Everything downstream of the "
                     "target can shift; nothing upstream can.", "primer", [r"intervention"]),
    "knowledge": ("Declared knowledge (K)", "Information that is not in the numbers: variable names, or an ordering such as "
                  "'these are inputs'. Legitimate when declared; a leak when silent.", "primer", [r"declared knowledge"]),
    "tier": ("Tier, partial order", "Groups of variables where an earlier group may cause a later one but never the reverse. "
             "Pairs inside a tier stay unordered.", "primer", [r"\btiers?\b"]),
    "arena": ("CausalArena", "The public benchmark this project audits: 100 scenarios per family (semantic: realistic named "
              "systems; formula: physical laws; synthetic), 50 public, 1,000 rows each.", "primer", [r"CausalArena"]),
    # ---- page 2, scoring
    "prf": ("Precision, recall, F1", "Precision: share of claimed edges that are true. Recall: share of true edges claimed. "
            "F1 = 2PR/(P+R).", "scoring", [r"\bF1\b"]),
    "S": ("S, skeleton F1", "F1 over adjacencies: only whether the right pairs are connected.", "scoring", [r"skeleton F1"]),
    "c": ("c, commit rate", "Of the true adjacencies a system found, the share it gave a direction to (right or wrong).", "scoring",
          [r"commit rate"]),
    "q": ("q, commit accuracy", "Of those committed directions, the share that are right. A coin scores 0.5.", "scoring",
          [r"commit accuracy"]),
    "a": ("a, direction accuracy", "a = c·q + (1−c)/2: the share of found pairs pointing the right way once undecided ones are "
          "oriented at random.", "scoring", [r"direction accuracy"]),
    "forced": ("Forced choice", "The scoreboard's rule: every undecided pair is given a direction (at random here). Published "
               "numbers use it.", "scoring", [r"forced[- ]choice"]),
    "strict": ("Strict scoring", "Undecided pairs count as no prediction.", "scoring", [r"strict scoring"]),
    "compelled": ("Compelled edge, κ", "An edge whose direction is the same in every graph of the equivalence class. κ is the "
                  "share of edges that are compelled.", "scoring", [r"compelled"]),
    "limit": ("Limit (ceiling)", "The best score any method could reach with perfect statistics, given only the evidence it is "
              "allowed to read.", "scoring", []),
    "oracle": ("Oracle", "A hypothetical input taken from the true graph, used to price a piece of information, never as a "
               "method.", "scoring", [r"\boracles?\b"]),
    "regime": ("Information regime", "Which evidence a system may read: D (data), I (interventions), K (knowledge). D is always "
               "present, so there are four: D, D+I, D+K, D+I+K.", "scoring", [r"\bregimes?\b", r"\bD\+I\b", r"\bD\+K\b"]),
    "budget": ("Error budget", "1 − F1 split into named losses: not identifiable, wrong skeleton, wrong directions.", "scoring",
               [r"error budget"]),
    # ---- page 3, space
    "arms": ("Name arms", "Controls on the names a system sees: real, neutral (V01, V02, …) and swapped (real names moved to "
             "other columns).", "space", [r"name arms?", r"swapped names", r"neutral names"]),
    "sufficient": ("Causal sufficiency", "Every common cause of two measured variables is itself measured. When it fails, "
                   "methods output a PAG instead of a CPDAG.", "space", [r"sufficiency"]),
    "pag": ("PAG", "The output of FCI when hidden common causes are allowed; a circle mark means that end is not determined.",
            "space", [r"\bPAGs?\b"]),
    "q1": ("The Q1 setting", "The point this project works at first: all variables observed, independent rows, 20-40 variables, "
           "1,000 rows, mixed nonlinear mechanisms.", "space", [r"Q1 setting"]),
    # ---- page 4, scoreboard
    "leak": ("Layout leak", "Released files list columns in causal order, so a method that reads column positions gets the "
             "order for free.", "scoreboard", [r"layout leak", r"column layout"]),
    "indexrule": ("Index tie-break (the authors' rule)", "Orienting each undecided pair from the earlier column to the later one. "
                  "CausalArena's own scoring code does this.", "scoreboard", [r"authors'? rule", r"index (tie-break|rule)"]),
    "conflict": ("Conflict rule", "How PC resolves two colliders that disagree about one edge. The default rule depends on the "
                 "order in which columns are visited; maxP does not.", "scoreboard", [r"conflict rule", r"\bmaxP\b"]),
    "shuffle": ("Column shuffling", "Scoring the same file with its columns in a random order, so that layout cannot help.",
                "scoreboard", [r"shuffl"]),
    "engine": ("Engine defect", "A bug in the library that runs the algorithm, found by feeding it a perfect-information oracle "
               "and checking the answer.", "scoreboard", [r"engine defects?"]),
    "halfcredit": ("Half credit", "Bayesys's scoring: a true connection with the wrong or no direction counts as half right.",
                   "scoreboard", [r"half[- ]credit"]),
    # ---- page 5, decisions
    "dv": ("Decision value (DV-1)", "Asks a graph 'if I set T, does Y move?' for every target and outcome, and scores the "
           "committed answers against the truth.", "decisions", [r"decision value", r"\bDV-1\b"]),
    "emptygraph": ("Empty-graph baseline", "Answering 'nothing moves' to every question. A learned graph is worth acting on only "
                   "if it beats this.", "decisions", [r"empty[- ]graph", r"nothing moves"]),
    "abstain": ("Abstention", "Declining to commit an answer. Under forced choice it is worth exactly ½ per pair, so it pays "
                "whenever q < ½.", "decisions", [r"abstain", r"abstention"]),
    "harm": ("Bounded harm", "If knowledge only orients connections the data already found, wrong knowledge can cost at most the "
             "directions it decided.", "decisions", [r"bounded harm"]),
    # ---- page 6, names
    "stages": ("Stages S0-S4", "Causal-Copilot's pipeline: S0 algorithm output, S1 bootstrap filter, S2 model review using names, "
               "S3 KCI pruning, S4 cycle step.", "names", [r"\bS0\b", r"\bS4\b"]),
    "bootstrap": ("Bootstrap", "Rerunning the algorithm on resampled rows; an edge's bootstrap frequency is the share of reruns "
                  "that keep it.", "names", [r"bootstrap"]),
    "kci": ("KCI", "Kernel conditional independence test; Causal-Copilot uses it to prune edges after the model review.", "names",
            [r"\bKCI\b"]),
    "iso": ("Iso-F1 curve", "All (S, a) points with the same directed F1: a = F1 / S.", "names", [r"iso-F1"]),
    "elicit": ("Knowledge elicitation", "Asking a model for tiers from variable names alone, with no data.", "names",
               [r"elicitation"]),
    # ---- page 7, rca
    "rca": ("Root cause analysis (RCA)", "Ranking which service caused an incident, from monitoring data and the service map.",
            "rca", [r"root[- ]cause"]),
    "acat": ("AC@k", "Share of incidents where the true root cause is in the top k answers.", "rca", [r"AC@\d"]),
    "topology": ("Declared topology", "The service call graph as the operators wrote it down, used as knowledge instead of a "
                 "learned graph.", "rca", [r"declared topology"]),
    # ---- page 8, theses
    "thesis": ("Thesis", "A claim the project commits to, with what would refute it written down before the evidence came in.",
               "theses", [r"\btheses\b", r"\bthesis\b"]),
    "invariant": ("Invariant", "A property every run of the system must satisfy, checked as a test rather than hoped for.",
                  "theses", [r"invariants?"]),
    "ledger": ("Claim ledger", "The planned system: every direction is stored with its source (data pattern, intervention or "
               "knowledge) and re-derived by a checker.", "theses", [r"\bledger\b"]),
    "pillar": ("Pillar", "One of three blocks of the work: P1 measurement, P2 claim ledger, P3 decisions.", "theses",
               [r"\bpillars?\b"]),
    "calib": ("Calibration", "A claim tagged 80% is right 80% of the time across many claims.", "theses", [r"calibrat"]),
    "ident": ("Identified effect", "Data plus graph pin the effect of setting X down to one value, rather than a set of possible "
              "values.", "theses", [r"identified effect"]),
    "ida": ("IDA", "Computes the possible effects of X on Y over every graph in the equivalence class; one value means "
            "identified.", "theses", [r"\bIDA\b"]),
    # ---- page 9, market
    "vertical": ("Vertical", "One industry treated as a market: who buys, from which budget, through which channel.", "market",
                 [r"\bverticals?\b"]),
    "evlabel": ("Evidence label", "Every market figure says what it is: primary, second-hand, vendor claim, analyst claim, survey, "
                "anecdote or estimate.", "market", [r"vendor claim", r"analyst claim"]),
    # ---- page 8 (status vocabulary used by the thesis cards) and page 10
    "bundle": ("Bundle", "A unit of work that closes a set of tickets and is checkable in one run, with a must-show list.",
               "theses", [r"\bbundles?\b"]),
    "gate": ("Gate", "A decision point with a test stated in advance (G1-G4, AB-16).", "theses", [r"\bgates?\b"]),
    "ticket": ("Ticket", "One tracked item (REP, AUD, CAP, BLD, TGT, …) with a criterion and evidence files; mirrored to both "
               "Slack lists.", "theses", [r"\btickets?\b"]),
    "live": ("LIVE / free", "LIVE work spends model calls through Uzair's key and is started only by him; free work runs at no "
             "cost.", "status", [r"(?-i:\bLIVE\b)"]),
}
