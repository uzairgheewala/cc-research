#!/bin/bash
# usage: worker.sh <name> <jobsfile>   Pops one line at a time from <jobsfile> (flock) and runs it; stops when the file is empty.
# line = method:family:tag:order:timeout[:extra args, comma-separated]   (order rel|shuf; shuf adds --shuffle-seed 20261010)
cd /home/claude/work/ccr/cc-research
export PYTHONPATH=../Causal-Copilot/externals/causal-learn PYTHONWARNINGS=ignore OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
LOG=analysis/results/methods/logs/$1.log; JOBS=$2
while true; do
  spec=$(flock "$JOBS.lock" bash -c "head -n 1 '$JOBS'; sed -i '1d' '$JOBS'")
  [ -z "$spec" ] && break
  IFS=: read m fam tag order to extra <<< "$spec"
  out=analysis/results/methods/${m}_${tag}_${order}.json
  args="--method $m --family $fam --out $out --file-timeout-s $to"
  [ "$order" = shuf ] && args="$args --shuffle-seed 20261010"
  [ -n "$extra" ] && args="$args ${extra//,/ }"
  echo "START $(date -u +%FT%TZ) python3 analysis/causalarena_methods.py $args" >> $LOG
  t0=$(date +%s)
  python3 analysis/causalarena_methods.py $args >> $LOG 2>&1
  echo "END $(date -u +%FT%TZ) rc=$? wall_s=$(( $(date +%s)-t0 )) $out" >> $LOG
done
echo "WORKER-DONE $(date -u +%FT%TZ)" >> $LOG
