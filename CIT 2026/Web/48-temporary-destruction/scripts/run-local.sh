#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-5004}"
if [[ ! "${PORT}" =~ ^[0-9]+$ ]]; then
  printf 'error: port must be numeric (got %q)\n' "${PORT}" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/../other/src/temporary-destruction" && pwd)"
FLAG_VALUE="${FLAG_VALUE:-CIT{test_flag}}"

rm -f /tmp/flag.txt
printf '%s' "${FLAG_VALUE}" > /tmp/flag.txt
chmod 444 /tmp/flag.txt

cd "${ROOT}"
exec uv run --with flask==3.0.3 --with jinja2==3.1.4 \
  python -c "import app; app.app.run(host='127.0.0.1', port=${PORT}, debug=False)"
