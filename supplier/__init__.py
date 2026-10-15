"""Supplier contract (deliverable D0.3, guarantee G7): a malformed or truncated model reply can neither crash a run nor
silently degrade it. Shared by the B3 tier supplier, and written to replace the per-script parse rules of
harness/tiers_runner.py and analysis/refinement_v2.py in new code (those files are hashed evidence and stay as they are).
Tickets: CAP-10, TGT-13, BLD-04
"""
