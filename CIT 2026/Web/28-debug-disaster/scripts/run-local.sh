#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-5002}"
if [[ ! "${PORT}" =~ ^[0-9]+$ ]]; then
  printf 'error: port must be numeric (got %q)\n' "${PORT}" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/../other/reconstructed" && pwd)"
FETCHED_ENV="${ROOT}/../fetched/.env"

if [[ -f "${FETCHED_ENV}" ]]; then
  cp "${FETCHED_ENV}" "${ROOT}/.env"
elif [[ ! -f "${ROOT}/.env" ]]; then
  cat > "${ROOT}/.env" <<'EOF'
SECRET_KEY=supersecret
FLAG=CIT{test_flag}
DATABASE_URL=sqlite:///prod.db
EOF
fi

cd "${ROOT}"
exec env PORT="${PORT}" uv run --with flask==3.1.0 python app.py
