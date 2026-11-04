#!/usr/bin/env bash
# Tickets: DLV-05, DLV-07. Use the same preserving builder on every OS.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
args=()
if [ -n "${NO_NUMBERS:-}" ]; then args+=(--no-numbers); fi
exec python3 -B build_paper.py "${args[@]}" "$@"
