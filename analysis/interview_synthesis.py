"""AB-10 interview synthesis (AUD-41): practitioner notes -> H1-H3 and P13 tallies and verdicts.

  python analysis/interview_synthesis.py                       reads docs/interviews/notes/*.json, writes
                                                               analysis/results/interviews/synthesis.json
  python analysis/interview_synthesis.py --export-blind DIR    writes copies with coding removed and the P13 decision
                                                               flag masked, for Claude's independent coding

What it does, in order (docs/interviews/synthesis_plan.md):
  1. Validate each record against docs/interviews/notes_schema.json, plus the cross-field rules the schema cannot express.
  2. Refuse any record with an email address, phone number or capitalised two-word name in a free-text field (regex
     heuristics), naming the record and field.
  3. If any record is refused, write nothing and exit 2. A partial synthesis would look complete.
  4. Tally supports/refutes/silent per hypothesis and apply the thresholds (P13 exactly as in the audit DAG).

The output has no timestamp, so the same notes always give the same bytes.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "docs" / "interviews" / "notes"
SCHEMA = ROOT / "docs" / "interviews" / "notes_schema.json"
OUT = ROOT / "analysis" / "results" / "interviews" / "synthesis.json"
FORMAT = "ab10-interview-synthesis/0.1"

HYPOTHESES = ("H1", "H2", "H3", "P13")
CODES = ("supports", "refutes", "silent")
MIN_N = 5  # AB-10 plans 5-8 interviews; below 5 we report tallies but no verdict
CARDS = ("provenance_table", "abstaining_answer", "name_swap_audit")
COMMUNITY_CHANNELS = ("pywhy_community", "other_causal_community")

RULES = {
    "denominator": "N = all valid interview records; silent codes count in N (a hypothesis needs a positive statement)",
    "P13": "supported if supports >= N/2; refuted if supports < N/4; otherwise inconclusive (audit DAG, AB-10)",
    "H1-H3": ("supported if supports >= N/2 and supports > refutes; refuted if supports < N/4, or refutes >= N/2 "
              "and refutes > supports; otherwise inconclusive (synthesis_plan.md; mirrors P13)"),
    "min_n": f"N < {MIN_N}: verdict 'insufficient_n', tallies still reported",
    "coding_used": "reconciled codes if every record has them (status final); otherwise the student's codes (provisional)",
}

# ----------------------------------------------------------------------------------------------- schema validation

_TYPES = {"string": lambda v: isinstance(v, str), "boolean": lambda v: isinstance(v, bool),
          "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
          "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
          "object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list), "null": lambda v: v is None}


def validate(v, spec, path, errs, root):
    """The subset of JSON Schema 2020-12 that notes_schema.json uses. Appends 'path: message' strings to errs."""
    if "$ref" in spec:
        ref = spec["$ref"]
        if not ref.startswith("#/$defs/"):
            errs.append(f"{path}: unsupported $ref {ref}")
            return
        spec = root["$defs"][ref.split("/")[-1]]
    if "const" in spec:
        c = spec["const"]
        if not (type(v) is type(c) and v == c):
            errs.append(f"{path}: must be {json.dumps(c)}")
            return
    if "enum" in spec and not any(type(v) is type(e) and v == e for e in spec["enum"]):
        errs.append(f"{path}: {json.dumps(v)} not one of {spec['enum']}")
        return
    if "type" in spec:
        types = spec["type"] if isinstance(spec["type"], list) else [spec["type"]]
        if not any(_TYPES[t](v) for t in types):
            errs.append(f"{path}: expected {'/'.join(types)}")
            return
    if isinstance(v, str):
        if "pattern" in spec and not re.search(spec["pattern"], v):
            errs.append(f"{path}: does not match {spec['pattern']}")
        if len(v) < spec.get("minLength", 0):
            errs.append(f"{path}: shorter than {spec['minLength']}")
        if "maxLength" in spec and len(v) > spec["maxLength"]:
            errs.append(f"{path}: longer than {spec['maxLength']}")
    if _TYPES["number"](v):
        if "minimum" in spec and v < spec["minimum"]:
            errs.append(f"{path}: below {spec['minimum']}")
        if "maximum" in spec and v > spec["maximum"]:
            errs.append(f"{path}: above {spec['maximum']}")
    if isinstance(v, list):
        if len(v) < spec.get("minItems", 0):
            errs.append(f"{path}: fewer than {spec['minItems']} items")
        if "maxItems" in spec and len(v) > spec["maxItems"]:
            errs.append(f"{path}: more than {spec['maxItems']} items")
        if "items" in spec:
            for i, item in enumerate(v):
                validate(item, spec["items"], f"{path}[{i}]", errs, root)
    if isinstance(v, dict):
        for k in spec.get("required", ()):
            if k not in v:
                errs.append(f"{path}.{k}: required field missing")
        props = spec.get("properties", {})
        for k, item in v.items():
            if k in props:
                validate(item, props[k], f"{path}.{k}", errs, root)
            elif spec.get("additionalProperties", True) is False:
                errs.append(f"{path}.{k}: field not allowed by the schema")


def cross_field(rec, fname):
    """Rules the schema cannot express. Returns (errors, warnings)."""
    errs, warns = [], []
    if Path(fname).stem != rec.get("interview_id"):
        errs.append(f"interview_id: file must be named {rec.get('interview_id')}.json")
    c = rec["consent"]
    if c["audio_recorded"] and not c["audio_consent"]:
        errs.append("consent.audio_recorded: audio recorded without audio_consent")
    if c["path"] == "b" and not c.get("determination_ref", "").strip():
        errs.append("consent.determination_ref: path b needs the HRPP determination reference")
    for card in CARDS:
        a = rec["artefacts"][card]
        if a["shown"] and a["score"] is None:
            errs.append(f"artefacts.{card}.score: card shown but no score")
        if not a["shown"] and a["score"] is not None:
            errs.append(f"artefacts.{card}.score: card not shown but scored")
    p13_ok = any(d["which_causes_how_sure"] == "yes" and d["real_or_hypothetical"] == "real" for d in rec["decisions"])
    for coder, cs in rec["coding"].items():
        if coder == "reconciliation_note":
            continue
        for h in HYPOTHESES:
            if cs[h]["code"] != "silent" and not cs[h]["evidence"].strip():
                errs.append(f"coding.{coder}.{h}.evidence: a '{cs[h]['code']}' code needs an evidence paraphrase")
        if cs["P13"]["code"] == "supports" and not p13_ok:
            msg = (f"coding.{coder}.P13: coded supports, but no decision is real with which_causes_how_sure = yes")
            (warns if coder == "claude" else errs).append(msg)
    if p13_ok and rec["coding"]["student"]["P13"]["code"] != "supports":
        warns.append("decisions: a real decision is marked which_causes_how_sure = yes but student P13 is not 'supports'")
    return errs, warns

# ------------------------------------------------------------------------------------------------------ PII scan

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<![\d.])(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?![\d.])"
                   r"|\+\d[\d\s().-]{7,}\d")
NAME = re.compile(r"(?=\b([A-Z][a-z]+(?:['-][A-Za-z][a-z]+)?)\s+([A-Z][a-z]+(?:['-][A-Za-z][a-z]+)?)\b)")
# Capitalised pairs that are products, methods or ordinary sentence starts, not people. Matching is case-insensitive.
# Add to this list rather than weakening the regex; lowercase tool names in notes also pass.
ALLOWED_PAIRS = {p.lower() for p in (
    "Google Meridian", "Meta Robyn", "Causal Impact", "Google Analytics", "Adobe Analytics", "Looker Studio",
    "New Relic", "Datadog Bits", "Datadog Watchdog", "Dynatrace Davis", "Jupyter Notebook", "Jupyter Notebooks",
    "Microsoft Excel", "Google Sheets", "Power Query", "Azure Monitor", "Amazon Bedrock", "Tableau Prep",
    "Grafana Loki", "Splunk Observability", "Pager Duty", "Synthetic Control",
    "Marketing Mix", "Mix Modeling", "Mix Modelling", "Target Trial", "Real World", "Root Cause", "Lift Test",
    "Geo Lift", "Bayesian Network", "Granger Causality", "Instrumental Variables", "Propensity Score")}
STOP_FIRST = {w.lower() for w in (
    "The A An We They Our Their It Its This That These Those He She His Her You Your When Then If In On At For After "
    "Before Last Next Most Some Every Each No Not Yes Both Any All Only Also But And Or So Because Once Usually Often "
    "Sometimes Mostly Rarely Never Always Weekly Monthly Daily Quarterly Annually Senior Junior Head Chief "
    "Prefers Wants Needs Uses Used Would Could Should Will Might Asked Said Thinks Thought Rated Liked Disliked"
).split()}
# Keys whose values are fixed by the schema (enums, ids, consts): no free text to scan.
NON_FREE_TEXT = {"schema", "interview_id", "interview_month", "path", "sector", "role_level", "company_size",
                 "recruited_via", "type", "real_or_hypothetical", "which_causes_how_sure", "would_try",
                 "budget_owner_named", "current_spend_band", "code"}


def _mask(s):
    return " ".join(w[0] + "*" * (len(w) - 1) for w in s.split())


def pii_hits(text):
    """[(kind, masked_match)] for one string. The match is masked so the refusal message does not repeat the PII."""
    hits = [("email address", _mask(m.group(0))) for m in EMAIL.finditer(text)]
    hits += [("phone number", re.sub(r"\d", "#", m.group(0))) for m in PHONE.finditer(text)]
    for m in NAME.finditer(text):
        a, b = m.group(1), m.group(2)
        if a.lower() in STOP_FIRST or f"{a} {b}".lower() in ALLOWED_PAIRS:
            continue
        hits.append(("capitalised two-word name", _mask(f"{a} {b}")))
    return hits


def pii_scan(rec, path=""):
    """[(field_path, kind, masked)] over every free-text string in the record."""
    out = []
    if isinstance(rec, dict):
        for k, v in rec.items():
            if k in NON_FREE_TEXT and not isinstance(v, (dict, list)):
                continue
            out += pii_scan(v, f"{path}.{k}" if path else k)
    elif isinstance(rec, list):
        for i, v in enumerate(rec):
            out += pii_scan(v, f"{path}[{i}]")
    elif isinstance(rec, str):
        out += [(path, kind, masked) for kind, masked in pii_hits(rec)]
    return out

# ------------------------------------------------------------------------------------------------------ loading


def load_records(notes_dir, schema):
    """Returns (records, refusals, warnings). records: [(fname, sha256, rec)]; refusals: ['file: field: reason']."""
    records, refusals, warnings = [], [], []
    files = sorted(Path(notes_dir).glob("*.json"))
    seen = {}
    for f in files:
        raw = f.read_bytes()
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError as e:
            refusals.append(f"{f.name}: not valid JSON ({e.msg}, line {e.lineno})")
            continue
        # PII first, on the raw parse, so a record is refused for PII even when it also fails the schema.
        for field, kind, masked in pii_scan(rec):
            art = "an" if kind[0] in "aeiou" else "a"
            refusals.append(f"{f.name}: {field}: contains what looks like {art} {kind} ({masked}); paraphrase or remove it")
        errs = []
        validate(rec, schema, "$", errs, schema)
        if errs:
            refusals += [f"{f.name}: {e.replace('$.', '', 1)}" for e in errs]
            continue
        cerrs, cwarns = cross_field(rec, f.name)
        refusals += [f"{f.name}: {e}" for e in cerrs]
        warnings += [f"{f.name}: {w}" for w in cwarns]
        if rec["interview_id"] in seen:
            refusals.append(f"{f.name}: interview_id duplicates {seen[rec['interview_id']]}")
        seen.setdefault(rec["interview_id"], f.name)
        records.append((f.name, hashlib.sha256(raw).hexdigest(), rec))
    refused_files = {r.split(":", 1)[0] for r in refusals}
    return [r for r in records if r[0] not in refused_files], refusals, warnings

# ------------------------------------------------------------------------------------------------------ verdicts


def verdict_p13(supports, n):
    """P13 exactly as in the audit DAG: at least half -> supported; under a quarter -> refuted."""
    if n < MIN_N:
        return "insufficient_n"
    if 2 * supports >= n:
        return "supported"
    if 4 * supports < n:
        return "refuted"
    return "inconclusive"


def verdict_h(supports, refutes, n):
    """H1-H3: the P13 thresholds, plus a majority-refutes branch (synthesis_plan.md section 2)."""
    if n < MIN_N:
        return "insufficient_n"
    if 2 * supports >= n and supports > refutes:
        return "supported"
    if 4 * supports < n or (2 * refutes >= n and refutes > supports):
        return "refuted"
    return "inconclusive"


def tally(codesets):
    out = {}
    n = len(codesets)
    for h in HYPOTHESES:
        c = {k: sum(cs[h]["code"] == k for cs in codesets) for k in CODES}
        v = verdict_p13(c["supports"], n) if h == "P13" else verdict_h(c["supports"], c["refutes"], n)
        out[h] = {**c, "n": n, "share_supports": round(c["supports"] / n, 4) if n else None, "verdict": v}
    return out


def cohen_kappa(pairs):
    """Cohen's kappa for 3-category codes; None when undefined (expected agreement = 1) or no pairs."""
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    pe = sum((sum(a == k for a, _ in pairs) / n) * (sum(b == k for _, b in pairs) / n) for k in CODES)
    return None if pe >= 1 else round((po - pe) / (1 - pe), 4)


def inter_coder(recs):
    both = [r for r in recs if "claude" in r["coding"]]
    out = {"n_double_coded": len(both), "by_hypothesis": {}, "low_agreement": []}
    for h in HYPOTHESES:
        pairs = [(r["coding"]["student"][h]["code"], r["coding"]["claude"][h]["code"]) for r in both]
        agree = sum(a == b for a, b in pairs)
        k = cohen_kappa(pairs)
        pct = round(agree / len(pairs), 4) if pairs else None
        out["by_hypothesis"][h] = {"agree": agree, "n": len(pairs), "percent": pct, "kappa": k,
                                   "disagreements": [r["interview_id"] for r in both
                                                     if r["coding"]["student"][h]["code"] != r["coding"]["claude"][h]["code"]]}
        if pairs and (pct < 0.7 or (k is not None and k < 0.4)):
            out["low_agreement"].append(h)
    return out


def describe(recs):
    decisions = [d for r in recs for d in r["decisions"]]
    arts = {}
    for card in CARDS:
        scores = sorted(r["artefacts"][card]["score"] for r in recs if r["artefacts"][card]["shown"])
        m = len(scores)
        arts[card] = {"shown": m, "scores": scores, "n_score_ge_4": sum(s >= 4 for s in scores),
                      "mean": round(sum(scores) / m, 3) if m else None,
                      "median": (scores[m // 2] if m % 2 else (scores[m // 2 - 1] + scores[m // 2]) / 2) if m else None}
    count = lambda vals: {k: vals.count(k) for k in sorted(set(vals))}  # noqa: E731
    return {
        "decisions": {"n": len(decisions), "by_type": count([d["type"] for d in decisions]),
                      "real": sum(d["real_or_hypothetical"] == "real" for d in decisions),
                      "which_causes_how_sure_yes_real": sum(d["which_causes_how_sure"] == "yes"
                                                            and d["real_or_hypothetical"] == "real" for d in decisions)},
        "artefacts": arts,
        "adoption": {k: count([r["adoption_signals"][k] for r in recs])
                     for k in ("would_try", "budget_owner_named", "current_spend_band")},
        "participants": {k: count([r["participant"][k] for r in recs])
                         for k in ("sector", "role_level", "company_size", "recruited_via")},
        "consent_paths": count([r["consent"]["path"] for r in recs]),
    }


def by_sector(codesets):
    """Counts only: sector cells hold 1-3 interviews, too few for a verdict."""
    return {"n": len(codesets), **{h: {k: sum(cs[h]["code"] == k for cs in codesets) for k in CODES} for h in HYPOTHESES}}


def synthesize(records, warnings=()):
    recs = [r for _, _, r in records]
    final = bool(recs) and all("reconciled" in r["coding"] for r in recs)
    key = "reconciled" if final else "student"
    codes = lambda rs: [r["coding"][key] for r in rs]  # noqa: E731
    non_comm = [r for r in recs if r["participant"]["recruited_via"] not in COMMUNITY_CHANNELS]
    sectors = sorted({r["participant"]["sector"] for r in recs})
    warns = list(warnings)
    if any(r["consent"]["path"] == "a" for r in recs):
        warns.append("path (a) records present: their content must not appear in a paper (human_subjects_check.md)")
    return {
        "format": FORMAT,
        "status": "final" if final else "provisional",
        "coding_used": key,
        "n": len(recs),
        "inputs": [{"file": f, "sha256": h} for f, h, _ in records],
        "rules": RULES,
        "verdicts": tally(codes(recs)),
        "sensitivity_excluding_causal_communities": {"n": len(non_comm), "verdicts": tally(codes(non_comm))},
        "by_sector": {s: by_sector(codes([r for r in recs if r["participant"]["sector"] == s])) for s in sectors},
        "inter_coder": inter_coder(recs),
        **describe(recs),
        "warnings": warns,
    }

# ------------------------------------------------------------------------------------------------------ CLI


def export_blind(records, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for fname, _, rec in records:
        r = json.loads(json.dumps(rec))
        r["coding"] = {}
        for d in r["decisions"]:
            d["which_causes_how_sure"] = "unclear"  # masked: it is the student's P13 judgement
        (out_dir / fname).write_text(json.dumps(r, indent=1, ensure_ascii=False) + "\n")
    return len(records)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--notes-dir", default=str(NOTES_DIR))
    ap.add_argument("--schema", default=str(SCHEMA))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--export-blind", metavar="DIR", help="write coding-free copies for independent coding, then stop")
    a = ap.parse_args(argv)
    schema = json.loads(Path(a.schema).read_text())
    records, refusals, warnings = load_records(a.notes_dir, schema)
    if refusals:
        print(f"REFUSED: {len(refusals)} problem(s); nothing written. Fix the notes and rerun.", file=sys.stderr)
        for r in refusals:
            print("  " + r, file=sys.stderr)
        return 2
    if not records:
        print(f"no notes found in {a.notes_dir}; nothing written", file=sys.stderr)
        return 1
    if a.export_blind:
        print(f"wrote {export_blind(records, a.export_blind)} blind copies to {a.export_blind}")
        return 0
    res = synthesize(records, warnings)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, sort_keys=False) + "\n")
    print(f"wrote {out} ({res['status']}, n={res['n']})")
    for h in HYPOTHESES:
        v = res["verdicts"][h]
        print(f"  {h}: {v['supports']} supports / {v['refutes']} refutes / {v['silent']} silent of {v['n']} -> {v['verdict']}")
    for w in res["warnings"]:
        print("  warning: " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
