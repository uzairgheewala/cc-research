#!/usr/bin/env bash
# Build the Q1 checkpoint PDF (DLV-05). Tickets: DLV-05
#   docs/paper/q1/make.sh            numbers from the result files, lint, XeLaTeX + BibTeX, PDF in build/
#   NO_NUMBERS=1 docs/paper/q1/make.sh   reuse numbers.tex (when the result files are not on this machine)
# Needs XeLaTeX with the template's fonts (XCharter, Arial, Fira Code). If style/dsc180bibstyle.bst (the template's
# BibTeX style) is missing, CTAN's econ.bst stands in for it and the build says so.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
if [ -z "${NO_NUMBERS:-}" ]; then python3 build_numbers.py; fi
python3 lint_report.py report.tex
rm -rf build && mkdir -p build/style
cp report.tex reference.bib numbers.tex numbers_table.tex build/
cp style/dsc180reportstyle.sty build/style/
if [ -f style/dsc180bibstyle.bst ]; then
  cp style/dsc180bibstyle.bst build/style/
else
  echo "NOTE: style/dsc180bibstyle.bst not present; using CTAN econ.bst (reference formatting may differ from Overleaf)"
  cp "$(kpsewhich econ.bst)" build/style/dsc180bibstyle.bst
fi
cd build
xelatex -interaction=nonstopmode -halt-on-error report.tex > xelatex1.log
bibtex report > bibtex.log || { cat bibtex.log; exit 1; }
xelatex -interaction=nonstopmode -halt-on-error report.tex > xelatex2.log
xelatex -interaction=nonstopmode -halt-on-error report.tex > xelatex3.log
if grep -E "Citation .* undefined|Reference .* undefined|There were undefined" report.log; then
  echo "ERROR: undefined citations or references"; exit 1
fi
grep -c "Warning--" bibtex.log >/dev/null && grep "Warning--" bibtex.log || true
echo "built build/report.pdf ($(pdfinfo report.pdf 2>/dev/null | awk '/^Pages/{print $2}') pages)"
