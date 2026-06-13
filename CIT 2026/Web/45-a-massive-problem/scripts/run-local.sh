#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-5001}"
if [[ ! "${PORT}" =~ ^[0-9]+$ ]]; then
  printf 'error: port must be numeric (got %q)\n' "${PORT}" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/../other/src/a-massive-problem/app" && pwd)"

cd "${ROOT}"
exec env \
  FLAG="${FLAG:-CIT{test_flag}}" \
  SECRET_KEY="${SECRET_KEY:-test-session-key}" \
  DATABASE="${DATABASE:-/tmp/a-massive-problem.db}" \
  uv run --with flask==3.1.0 \
    python -c "import app; app.init_db(); app.app.run(host='127.0.0.1', port=${PORT})"
