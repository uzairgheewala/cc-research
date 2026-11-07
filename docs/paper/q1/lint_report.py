"""Lint for the Q1 paper (DLV-05): no number without a source, no prior-work sentence without a citation.

Tickets: DLV-05

    python3 docs/paper/q1/lint_report.py [report.tex]

Checks, each an error unless stated:
1. Numerals. After removing comments and the commands that carry no prose (\\nm, \\cite..., \\ref, \\label, \\url, \\href's
   target, \\input, \\includegraphics, environment names and column specs, lengths), every token that holds a digit must match
   one pattern of ALLOW (each pattern has its reason). Number words from "two" up are errors too: a count is a number.
2. Macros. Every \\nm{key} is defined in numbers.json; unused registry keys are listed (warning).
3. Citations (section with label sec:prior). Every sentence carries a \\cite... or ends with \\ours (our own statement).
   Every cited key, anywhere in the paper, has an entry in lit_claims.json whose verdict is "confirmed" or
   "corrected-applied", and an entry in reference.bib.
4. Enumerated editorial dispositions may cover grouped attribution or structural
   counts for one exact draft. Their reasons remain visible; any source edit
   invalidates them. They cannot waive undefined keys or unchecked citations.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

ALLOW = [
    (r"F1", "the metric's name"),
    (r"(?i)gpt-4o(-mini)?(-\d{4}-\d{2}-\d{2})?", "model names"),
    (r"L[0-4](-L[0-4])?", "audit levels L0-L4 (the protocol's own names)"),
    (r"S[12]", "suite names"),
    (r"Q[12]", "quarter names"),
    (r"[A-Z]{2,4}-\d{2}", "ticket IDs"),
    (r"4\.0", "licence versions (CC BY 4.0, CC BY-NC-ND 4.0, CC BY-SA 4.0)"),
    (r"2\.0", "licence version (Apache 2.0)"),
    (r"K562|RPE1", "cell-line names"),
    (r"180A", "the course name DSC 180A"),
    (r"R2", "the name R2-sortability"),
]
NUMBER_WORDS = r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|" \
               r"seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|hundred|hundreds|thousand|thousands|dozen|" \
               r"twice|thrice|half|quarter|third|fourth|fifth)\b"
WORD_OK = {"quarter": r"(?i)\bquarter\b(?= [12]| one| two)|Quarter", "half": r"half coverage", "third": r"$^",
           "fourth": r"$^", "fifth": r"$^"}
STRIP = [
    r"\\nm\{[^}]*\}", r"\\cite[a-z]*\*?(\[[^\]]*\])*\{[^}]*\}", r"\\(eq)?ref\{[^}]*\}", r"\\label\{[^}]*\}",
    r"\\url\{[^}]*\}", r"\\href\{[^}]*\}", r"\\input\{[^}]*\}", r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}",
    r"\\(begin|end)\{[^}]*\}(\{[^}]*\})?(\[[^\]]*\])?", r"\\(h|v)space\*?\{[^}]*\}", r"\\setlength\{[^}]*\}\{[^}]*\}",
    r"\\resizebox\{[^}]*\}\{[^}]*\}", r"\\\\\[[^\]]*\]", r"\\(small|footnotesize|scriptsize|tiny|large|Large)\b",
    r"\\(cmidrule|cline)(\([^)]*\))?\{[^}]*\}", r"\\multicolumn\{\d+\}\{[^}]*\}", r"\\multirow\{\d+\}\{[^}]*\}",
    r"[0-9.]+\\(linewidth|textwidth|columnwidth)", r"\\arraystretch\}\{[0-9.]+\}", r"\\ours\b",
    r"\\texttt\{[^}]*\}",  # code and file names are identifiers, not results
    r"\\bibliography(style)?\{[^}]*\}", r"\\usepackage(\[[^\]]*\])?\{[^}]*\}",
]


def body(tex):
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", tex, re.S)
    return m.group(1) if m else tex


def uncomment(s):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in s.split("\n"))


def numerals(text):
    errs = []
    for i, line in enumerate(text.split("\n"), 1):
        s = line
        for rx in STRIP:
            s = re.sub(rx, " ", s)
        for tok in re.findall(r"[A-Za-z0-9.\-]*\d[A-Za-z0-9.\-]*", s):
            t = tok.strip(".-")
            if not t or not any(c.isdigit() for c in t):
                continue
            if any(re.fullmatch(rx, t) for rx, _ in ALLOW):
                continue
            errs.append("line %d: numeral %r without \\nm: %s" % (i, t, line.strip()[:110]))
        for w in re.finditer(NUMBER_WORDS, s, re.I):
            word = w.group(1).lower()
            ok = WORD_OK.get(word)
            if ok and re.search(ok, s):
                continue
            errs.append("line %d: number word %r (use \\nm or rephrase): %s" % (i, w.group(1), line.strip()[:110]))
    return errs


def sentences(sec):
    s = re.sub(r"\b(et al|e\.g|i\.e|cf|vs|Fig|Sec|Eq|resp)\.", lambda m: m.group(0).replace(".", "<DOT>"), sec)
    s = re.sub(r"\\(sub)*section\*?\{[^}]*\}", " ", s)
    s = re.sub(r"\\paragraph\{[^}]*\}", " ", s)
    s = re.sub(r"\\item\b", " ", s)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\\])|\n\s*\n", s)
    return [p.replace("<DOT>", ".").strip() for p in parts if re.search(r"[A-Za-z]{3}", p)]


def reviewed_dispositions(tex, errors, policy):
    """Apply enumerated editorial judgments to one exact UTF-8/LF draft only.

    This is manual attribution/structural-count review, not an entailment check.
    Stale, duplicated or no-longer-triggered dispositions fail closed.
    """
    if policy.get("schema_version") != 1 or policy.get("source_sha256_utf8_lf") != hashlib.sha256(tex.encode("utf-8")).hexdigest():
        return errors + ["reviewed lint dispositions are stale or unsupported"], []
    remaining, notes, seen = list(errors), [], set()
    for item in policy.get("dispositions", []):
        error = item.get("error")
        eligible = (item.get("kind") == "grouped-attribution" and error is not None
                    and error.startswith("prior-work sentence without ")) or (
                    item.get("kind") == "structural-count" and error is not None
                    and re.match(r"line \d+: number word ", error))
        if (not eligible or error in seen or error not in remaining or not item.get("reason")
                or item.get("kind") not in {"grouped-attribution", "structural-count"}
                or not item.get("evidence")):
            return errors + ["invalid or no-longer-triggered reviewed lint disposition"], []
        seen.add(error)
        remaining.remove(error)
        notes.append(item["kind"] + ": " + item["reason"])
    return remaining, notes


def main(argv):
    tex_path = Path(argv[1]) if len(argv) > 1 else HERE / "report.tex"
    tex = tex_path.read_text(encoding="utf-8")
    b = uncomment(body(tex))
    errs, warns = [], []
    errs += numerals(b)
    reg = {e["key"] for e in json.loads((HERE / "numbers.json").read_text(encoding="utf-8"))["entries"]} | {"cc.head"}
    used = set(re.findall(r"\\nm\{([^}]*)\}", b))
    errs += ["undefined number key " + k for k in sorted(used - reg)]
    entries = json.loads((HERE / "numbers.json").read_text(encoding="utf-8"))["entries"]
    inputs = {x["key"] for e in entries for x in e.get("args", []) if "key" in x}
    warns += ["registry key not used in the text: " + k for k in sorted(reg - used - inputs - {"cc.head"})]
    # citations
    keys = set()
    for m in re.finditer(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}", b):
        keys |= {k.strip() for k in m.group(1).split(",")}
    claims_p = HERE / "lit_claims.json"
    claims = json.loads(claims_p.read_text(encoding="utf-8")) if claims_p.exists() else {"claims": []}
    ok_keys = set()
    for c in claims["claims"]:
        if c.get("verdict") in ("confirmed", "corrected-applied"):
            ok_keys |= set(c["keys"])
    bib = (HERE / "reference.bib").read_text(encoding="utf-8") if (HERE / "reference.bib").exists() else ""
    bibkeys = set(re.findall(r"@\w+\{([^,\s]+),", bib))
    errs += ["cited key without a checked claim in lit_claims.json: " + k for k in sorted(keys - ok_keys)]
    errs += ["cited key missing from reference.bib: " + k for k in sorted(keys - bibkeys)]
    m = re.search(r"\\section\{[^}]*\}\s*\\label\{sec:prior\}(.*?)(?=\\section\{)", b, re.S)
    if not m:
        errs.append("no section labelled sec:prior")
    else:
        for snt in sentences(m.group(1)):
            if "\\cite" not in snt and not snt.rstrip().endswith("\\ours") and "\\ours" not in snt[-12:]:
                errs.append("prior-work sentence without \\cite or \\ours: " + re.sub(r"\s+", " ", snt)[:140])
    policy_path = HERE / "verify" / "checkpoint-lint-dispositions-2026-11-06.json"
    if tex_path.resolve() == (HERE / "report.tex").resolve() and policy_path.exists():
        try:
            errs, notes = reviewed_dispositions(tex, errs, json.loads(policy_path.read_text(encoding="utf-8")))
        except (ValueError, TypeError, KeyError) as exc:
            errs.append("invalid reviewed lint dispositions: " + str(exc))
            notes = []
        for note in notes:
            print("reviewed disposition: " + note)
    for w in warns:
        print("warning: " + w)
    for e in errs:
        print("ERROR " + e)
    print("lint: %d errors, %d warnings; %d number keys used; %d citation keys" % (len(errs), len(warns), len(used), len(keys)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
