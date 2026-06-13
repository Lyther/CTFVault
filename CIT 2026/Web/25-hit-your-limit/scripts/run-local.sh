#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-5007}"
if [[ ! "${PORT}" =~ ^[0-9]+$ ]]; then
  printf 'error: port must be numeric (got %q)\n' "${PORT}" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/../other/reconstructed" && pwd)"
FLAG_VALUE="${FLAG_VALUE:-CIT{test_flag}}"

cd "${ROOT}"
exec env PORT="${PORT}" FLAG_VALUE="${FLAG_VALUE}" \
  uv run --with flask==3.1.0 python app.py
