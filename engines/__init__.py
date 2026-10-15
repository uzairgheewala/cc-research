"""Engines for the Q2 claim ledger (deliverable D0.1 of plans/q2_dag.json, bundle B0).

Every data-pattern source the kernel uses, pinned and wrapped so that it returns either a typed result or a typed
failure, never an exception:

  pc_maxp     causal-learn 0.1.4.8 PC (stable, Fisher-z, alpha 0.05) with the maxP collider rule (uc_rule 1, priority 3),
              run through causal-learn's own components with a recording CI test, so every test it ran becomes an
              evidence record. Exactly the call pc(X, 0.05, "fisherz", stable=True, uc_rule=1, uc_priority=3).
  ges_bic     GES from the `ges` package 1.1.0 (Gaussian l0-penalised likelihood, lambda = log(n)/2) on z-scored
              columns: the scoreboard's GES (BIC) row.
  gies        GIES from the `gies` package 0.0.3 with the released intervention targets (one environment per
              intervened-cell pattern): the scoreboard's GIES (D+I) row.

Pins and hashes: engines/manifest.py writes engines/MANIFEST.json. The compute environment is the one the audit
chapter used (Python 3.11, NumPy 1.26.4, SciPy 1.13.1). Engines run single-threaded (OMP/OpenBLAS/MKL threads = 1,
set by engines.runner before NumPy is imported in a worker).
Tickets: CAP-05, CAP-11, BLD-02
"""
