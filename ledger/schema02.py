"""Claim ledger v0.2 (BLD-14, deliverable D1.4): v0.1 (ledger/schema.py, hashed in the paper pre-registration and left
unchanged) plus the fields AB-13 and AB-11 found missing.

Added to the report:
  plan          {"prereg": path, "prereg_sha256": sha, "fixed_utc": ...}: the plan fixed before the data were read
  deviations    [{"what", "why", "utc"}]: every departure from the plan (empty list when none)
  assumptions   [{"id", "statement", "testable": bool, "sensitivity"}]: identifying assumptions, each with how its failure
                would show (non-empty)
  lineage       {"source", "file", "sha256", "transformations": [...]}: where the data came from and what was done to them
  question      {"text", "context_of_use", "estimand", "cost_ratio"}: what the ledger is for; cost_ratio = c/g for the
                selective view (null when no decision is attached)
  orientation_convention  must be the string CONVENTION below (AB-11: a reader must not have to guess which way x->y runs)
  engine_outputs  the engines' own graphs as recorded (so K7 can re-derive the combination), engine failures, defects
Added at top level:
  reviews       [{"reviewer", "utc", "scope", "verdict", "notes"}]: human review records (may be empty)
Added to variables: data_id (sha256 of the values alone), canonical_index.
Added to claims: engines ("pc", "ges", "both", "none"), conflict (bool: the engines disagreed on this pair),
  derived_from (claim ids an orientation rule relied on).
Added licence: score_search (an adjacency or direction decided by a score search, GES).
"""
import copy, json
from pathlib import Path

import schema as S01

FORMAT = "cc-claim-ledger/0.2"
CONVENTION = "relation 'x->y' means claim.x causes claim.y; 'x-y' adjacent, direction open; 'none' not adjacent"
LICENSES = S01.LICENSES + ("score_search",)
STR, SHA, NUM, BOOL = {"type": "string"}, S01.SHA, S01.NUM, {"type": "boolean"}
obj = S01.obj

VARIABLE = copy.deepcopy(S01.VARIABLE)
VARIABLE["properties"].update({"data_id": SHA, "canonical_index": {"type": "integer"}})
VARIABLE["required"] += ["data_id", "canonical_index"]

CLAIM = copy.deepcopy(S01.CLAIM)
CLAIM["properties"]["licensed_by"] = {"enum": list(LICENSES)}
CLAIM["properties"].update({"engines": {"enum": ["pc", "ges", "both", "none", "intervention", "knowledge"]},
                            "conflict": BOOL, "derived_from": {"type": "array", "items": STR}})
CLAIM["required"] += ["engines", "conflict"]

PLAN = obj({"prereg": STR, "prereg_sha256": SHA, "fixed_utc": STR}, ("prereg", "prereg_sha256"))
DEVIATION = obj({"what": STR, "why": STR, "utc": STR}, ("what", "why"))
ASSUMPTION = obj({"id": STR, "statement": STR, "testable": BOOL, "sensitivity": STR}, ("id", "statement", "testable", "sensitivity"))
LINEAGE = obj({"source": STR, "file": STR, "sha256": SHA, "transformations": {"type": "array", "items": STR}},
              ("source", "sha256", "transformations"))
QUESTION = obj({"text": STR, "context_of_use": STR, "estimand": STR, "cost_ratio": {"type": ["number", "null"]}},
               ("text", "context_of_use", "estimand", "cost_ratio"))
REVIEW = obj({"reviewer": STR, "utc": STR, "scope": STR, "verdict": STR, "notes": STR}, ("reviewer", "utc", "scope", "verdict"))

REPORT = copy.deepcopy(S01.REPORT)
REPORT["properties"].update({"plan": PLAN, "deviations": {"type": "array", "items": DEVIATION},
                             "assumptions": {"type": "array", "items": ASSUMPTION, "minItems": 1}, "lineage": LINEAGE,
                             "question": QUESTION, "orientation_convention": {"const": CONVENTION},
                             "engine_outputs": {"type": "object"}})
REPORT["required"] += ["plan", "deviations", "assumptions", "lineage", "question", "orientation_convention", "engine_outputs"]

LEDGER = copy.deepcopy(S01.LEDGER)
LEDGER["properties"].update({"format": {"const": FORMAT}, "variables": {"type": "array", "items": VARIABLE},
                             "claims": {"type": "array", "items": CLAIM}, "report": REPORT,
                             "reviews": {"type": "array", "items": REVIEW}})
LEDGER["required"] += ["reviews"]


def json_schema():
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": FORMAT, "title": "Claim ledger v0.2 (cc-research)", **LEDGER}


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "schema"
    out.mkdir(exist_ok=True)
    json.dump(json_schema(), open(out / "ledger02.schema.json", "w"), indent=1)
    print("wrote", out / "ledger02.schema.json")
