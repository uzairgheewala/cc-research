"""The claim-ledger record format as data (ledger/DESIGN.md). One source for the verifier and for the JSON Schema files.

  python ledger/schema.py      writes ledger/schema/ledger.schema.json (JSON Schema draft 2020-12)
"""
import json
from pathlib import Path

RELATIONS = ("x->y", "x-y", "none", "x<->y")
SOURCES = ("data_pattern", "data_form", "intervention", "knowledge", "none")
LICENSES = ("v_structure", "meek_r1", "meek_r2", "meek_r3", "meek_r4", "i_essential", "lingam", "anm", "tier", "declared",
            "adjacency_test", "none")
EVIDENCE_TYPES = ("ci_test", "score_delta", "functional_asymmetry", "intervention_shift", "knowledge_statement")
KNOWLEDGE_KINDS = ("tier", "required_edge", "forbidden_edge", "ancestral", "non_ancestral")
REGIMES = ("D", "D+I", "D+K", "D+I+K")

S = {"type": "string"}
SHA = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
NUM = {"type": "number"}


def obj(props, required):
    return {"type": "object", "properties": props, "required": list(required), "additionalProperties": True}


VARIABLE = obj({"var_id": SHA, "name": S, "position": {"type": "integer"}}, ("var_id", "name"))
ENGINE = obj({"name": S, "version": S, "wheel_sha256": SHA}, ("name", "version"))
EVIDENCE = obj({"id": S, "type": {"enum": list(EVIDENCE_TYPES)}, "variables": {"type": "array", "items": S},
                "conditioning": {"type": "array", "items": S}, "statistic": NUM, "p_value": NUM, "score": NUM,
                "data_sha256": SHA, "engine": ENGINE, "seed": {"type": ["integer", "null"]},
                "supports": {"enum": ["adjacent", "nonadjacent", "x->y", "y->x", "none"]}},
               ("id", "type", "variables", "supports"))
SUPPLIER = obj({"type": {"enum": ["person", "model"]}, "model_id": S, "prompt_sha256": SHA, "phrasing_id": S,
                "shown": {"type": "array", "items": S}}, ("type",))
KNOWLEDGE = obj({"id": S, "kind": {"enum": list(KNOWLEDGE_KINDS)}, "content": {"type": "object"}, "supplier": SUPPLIER},
                ("id", "kind", "content", "supplier"))
CLAIM = obj({"id": S, "x": S, "y": S, "relation": {"enum": list(RELATIONS)}, "direction_source": {"enum": list(SOURCES)},
             "licensed_by": {"enum": list(LICENSES)}, "evidence": {"type": "array", "items": S, "minItems": 1},
             "data_only_relation": {"enum": list(RELATIONS)}, "knowledge": {"type": "array", "items": S},
             "confidence": obj({"bootstrap_frequency": NUM, "calibrated_probability": NUM, "calibration_set": S}, ())},
            ("id", "x", "y", "relation", "direction_source", "licensed_by", "evidence", "data_only_relation"))
OVERRIDE = obj({"knowledge": S, "by": S, "reason": S}, ("knowledge", "by", "reason"))
REPORT = obj({"run_id": S, "created_utc": S, "regime": {"enum": list(REGIMES)}, "data_sha256": SHA,
              "engines": {"type": "array", "items": ENGINE}, "seeds": {"type": "object"},
              "invariants": {"type": "object"}, "permutation_check": obj({"permutations": {"type": "integer"},
                                                                         "identical": {"type": "boolean"}}, ("permutations", "identical")),
              "ledger_sha256": SHA, "unverifiable": {"type": "array", "items": S}, "commentary": S},
             ("run_id", "regime", "data_sha256", "engines", "permutation_check", "ledger_sha256", "unverifiable"))
LEDGER = obj({"format": {"const": "cc-claim-ledger/0.1"}, "variables": {"type": "array", "items": VARIABLE},
              "evidence": {"type": "array", "items": EVIDENCE}, "knowledge": {"type": "array", "items": KNOWLEDGE},
              "claims": {"type": "array", "items": CLAIM}, "overrides": {"type": "array", "items": OVERRIDE},
              "report": REPORT},
             ("format", "variables", "evidence", "knowledge", "claims", "overrides", "report"))


def json_schema():
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "cc-claim-ledger/0.1",
            "title": "Claim ledger (cc-research)", **LEDGER}


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "schema"
    out.mkdir(exist_ok=True)
    json.dump(json_schema(), open(out / "ledger.schema.json", "w"), indent=1)
    print("wrote", out / "ledger.schema.json")
