"""Build the Q1 paper on any OS (DLV-05): numbers, checks, PDF, and the Overleaf upload bundle.

Tickets: DLV-05, DLV-07

    python docs/paper/q1/build_paper.py                 numbers from the result files, --check, lint, PDF if XeLaTeX is present
    python docs/paper/q1/build_paper.py --no-numbers    reuse numbers.tex (result files not on this machine)
    python docs/paper/q1/build_paper.py --no-pdf        numbers and checks only
    python docs/paper/q1/build_paper.py --overleaf      also write build/overleaf_upload.zip (the files to replace in the template)

The PDF needs XeLaTeX and BibTeX with the template's fonts (XCharter, Arial, Fira Code). Without them the script says so and
stops after the checks; Overleaf (the course's compile path) is then the PDF. If style/dsc180bibstyle.bst is missing,
CTAN's econ.bst stands in for it and the script says so. make.sh is the same build for bash.
"""
import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
UPLOAD = ["report.tex", "reference.bib", "numbers.tex", "numbers_table.tex"]


def run(cmd, cwd=HERE, log=None):
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if log:
        Path(log).write_text(p.stdout + p.stderr, encoding="utf-8")
    return p


def step(name, cmd):
    p = run(cmd)
    out = (p.stdout + p.stderr).strip()
    print("[%s] %s" % (name, out.splitlines()[-1] if out else "(no output)"))
    if p.returncode:
        print(out)
        sys.exit("FAILED at %s" % name)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-numbers", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--overleaf", action="store_true")
    a = ap.parse_args(argv)
    py = sys.executable
    if not a.no_numbers:
        step("numbers", [py, "-B", "build_numbers.py"])
        step("numbers --check", [py, "-B", "build_numbers.py", "--check"])
    step("lint", [py, "-B", "lint_report.py", "report.tex"])
    build = HERE / "build"
    if a.overleaf:
        build.mkdir(exist_ok=True)
        z = build / "overleaf_upload.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
            for n in UPLOAD:
                f.write(HERE / n, n)
        print("[overleaf] %s: %s (keep the template's style/ folder as it is)" % (z.name, ", ".join(UPLOAD)))
    if a.no_pdf:
        return 0
    xe, bt = shutil.which("xelatex"), shutil.which("bibtex")
    if not (xe and bt):
        print("[pdf] skipped: xelatex/bibtex not on PATH. Compile on Overleaf (python build_paper.py --overleaf gives the files).")
        return 0
    if build.exists():
        for p in build.iterdir():
            if p.name in ("overleaf_upload.zip",):
                continue
            try:
                shutil.rmtree(p) if p.is_dir() else p.unlink()
            except OSError:
                pass  # a shell that cannot delete: files are overwritten below
    (build / "style").mkdir(parents=True, exist_ok=True)
    for n in UPLOAD:
        shutil.copy2(HERE / n, build / n)
    shutil.copy2(HERE / "style" / "dsc180reportstyle.sty", build / "style" / "dsc180reportstyle.sty")
    bst = HERE / "style" / "dsc180bibstyle.bst"
    if bst.exists():
        shutil.copy2(bst, build / "style" / bst.name)
    else:
        kp = run(["kpsewhich", "econ.bst"]).stdout.strip() if shutil.which("kpsewhich") else ""
        if not kp:
            sys.exit("FAILED: style/dsc180bibstyle.bst missing and econ.bst not found; copy the template's .bst in")
        print("[pdf] NOTE: template's dsc180bibstyle.bst absent; CTAN econ.bst stands in (reference formatting may differ)")
        shutil.copy2(kp, build / "style" / "dsc180bibstyle.bst")
    tex = [xe, "-interaction=nonstopmode", "-halt-on-error", "report.tex"]
    for i, cmd in enumerate([tex, [bt, "report"], tex, tex], 1):
        p = run(cmd, cwd=build, log=build / ("step%d.log" % i))
        if p.returncode:
            tail = "\n".join((p.stdout + p.stderr).splitlines()[-25:])
            sys.exit("FAILED: %s (log build/step%d.log)\n%s" % (Path(cmd[0]).name, i, tail))
    log = (build / "report.log").read_text(encoding="utf-8", errors="replace")
    if re.search(r"Citation .* undefined|Reference .* undefined|There were undefined", log):
        sys.exit("FAILED: undefined citations or references (build/report.log)")
    pages = re.findall(r"Output written on report\.pdf \((\d+) pages?", log)
    print("[pdf] build/report.pdf (%s pages)" % (pages[-1] if pages else "?"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
