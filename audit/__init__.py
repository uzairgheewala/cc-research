"""The audit adapter (bundle B5 of plans/q2_dag.json; BLD-15 proposed): read another causal-discovery system's output into
typed claims and report every violation of the ledger's guarantees by class, each traced to a claim and a source.
This is the product core the audit chapter pointed to: it checks other agents' claims, it does not make its own.

  adapters  AB-06 agents (MATMCD, Vashishtha et al., PyWhy-LLM, causaliq) and Causal-Copilot stage graphs
  rca       root-cause ranking over declared topology recorded in a ledger (PetShop), with abstention
Tickets: CAP-09, BLD-15 (proposed), TGT-20 (proposed)
"""
