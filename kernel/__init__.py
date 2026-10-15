"""The claim-ledger kernel (bundle B1 of plans/q2_dag.json; approach_v1.md sections 1-2).

  canon     variable identity and canonical column order (I1)
  derive    re-derivation of PC-maxP from its recorded tests: skeleton, maxP colliders, Meek R1-R3 with rule labels.
            NumPy only: it is the independent checker (K7) and runs in CI without causal-learn.
  policy    the data-only combination rules over PC and GES (PC, GES, C1, C2, C3)
  build     K0-K6: runs the engines on canonical columns, writes evidence, claims and the run report (ledger v0.2)
  checker   K7: re-derives every claim from the ledger's records and the recorded engine outputs
  views     K6: scoreboard export (expectation rule) and the claim list; DV-1 claims
Tickets: BLD-02, BLD-14, CAP-05, CAP-09, CAP-11, TGT-10
"""
