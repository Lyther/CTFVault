#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://23.179.17.92:5001}"
OUT_DIR="$(cd "$(dirname "$0")/../other" && pwd)/fetched"

mkdir -p "${OUT_DIR}"

COOKIE_JAR="$(mktemp)"
trap 'rm -f "${COOKIE_JAR}"' EXIT

USER_NAME="fetcher_$(python3 - <<'PY'
import uuid
print(uuid.uuid4().hex[:10])
PY
)"
PASSWORD='P@ssw0rd!'

curl -sS "${BASE_URL}/login" -o "${OUT_DIR}/login.html"
curl -sS "${BASE_URL}/register" -o "${OUT_DIR}/register.html"
curl -sS -c "${COOKIE_JAR}" -b "${COOKIE_JAR}" -X POST \
  -d "username=${USER_NAME}&password=${PASSWORD}" \
  "${BASE_URL}/register" >/dev/null
curl -sS -c "${COOKIE_JAR}" -b "${COOKIE_JAR}" -X POST \
  -d "username=${USER_NAME}&password=${PASSWORD}" \
  "${BASE_URL}/login" >/dev/null
curl -sS -b "${COOKIE_JAR}" "${BASE_URL}/" -o "${OUT_DIR}/dashboard.html"
curl -sS -b "${COOKIE_JAR}" "${BASE_URL}/report?id=347" -o "${OUT_DIR}/report-347.html"
