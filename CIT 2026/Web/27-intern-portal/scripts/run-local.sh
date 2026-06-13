#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-5006}"
if [[ ! "${PORT}" =~ ^[0-9]+$ ]]; then
  printf 'error: port must be numeric (got %q)\n' "${PORT}" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/../other/reconstructed" && pwd)"
DB_PATH="${DB_PATH:-/tmp/intern-portal.db}"
FLAG_VALUE="${FLAG_VALUE:-CIT{test_flag}}"

rm -f "${DB_PATH}"
cd "${ROOT}"
exec env PORT="${PORT}" DB_PATH="${DB_PATH}" FLAG_VALUE="${FLAG_VALUE}" \
  uv run --with flask==3.1.0 python app.py
