#!/bin/bash
# Deliberate change to tracker code or evidence: repin the named tickets, re-run the self-test twice and require a byte-identical
# result, record the reproduction for tickets whose evidence is the self-test, then verify.
#   bash tracker/repin_cycle.sh "why" ID [ID ...]
set -e
why="$1"; shift
python3 tracker/verify.py --repin "$@" > /dev/null
python3 tracker/selftest_trace.py | tail -1
h1=$(sha256sum tracker/selftest_trace.json | cut -d' ' -f1)
python3 tracker/selftest_trace.py | tail -1
h2=$(sha256sum tracker/selftest_trace.json | cut -d' ' -f1)
[ "$h1" = "$h2" ] || { echo "self-test output not reproducible"; exit 1; }
for id in "$@"; do
  if grep -q "\"$id\".*selftest_trace" tracker/catalogue.py || python3 -c "import sys;sys.path.insert(0,'tracker');import catalogue as C;sys.exit(0 if any(i['id']=='$id' and any('selftest_trace.json' in e for e in i['evidence']) for i in C.ITEMS) else 1)"; then
    python3 tracker/verify.py --reproduced "$id" --note "$why; self-test re-run twice, output byte-identical (${h1:0:12})" > /dev/null
  fi
done
python3 tracker/verify.py | head -2
