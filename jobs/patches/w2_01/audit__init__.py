"""The audit package (A3, DLV-09; protocol v1, DLV-08: audit/PROTOCOL.md) and, beside it, the B5 claim checker.

Package (python -m audit; audit/README.md):
  core/ protocol/ metrics/ controls/ trace/ systems/ findings.py report/ run.py collect.py rerun/
  adapters for PC, GES, GIES, MATMCD, Vashishtha et al., PyWhy-LLM, causaliq and Causal-Copilot; L0 scoring, L1 controls,
  L2 stage tracing, typed findings (closed list K01-K15), reports and certificates; the existing audits rerun through it.
B5 claim checker (bundle B5 of plans/q2_dag.json; BLD-15 proposed), unchanged: read another causal-discovery system's
output into typed claims and report every violation of the ledger's guarantees by class, each traced to a claim and a
source. Its violation classes are the evidence rows of finding kinds K07 and K13.
  adapters  AB-06 agents (MATMCD, Vashishtha et al., PyWhy-LLM, causaliq) and Causal-Copilot stage graphs
  rca       root-cause ranking over declared topology recorded in a ledger (PetShop), with abstention
Tickets: DLV-09, DLV-08, DLV-10, CAP-09, BLD-15 (proposed), TGT-20 (proposed)
"""
