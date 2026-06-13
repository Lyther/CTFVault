#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://23.179.17.92:5559}"
OUT_DIR="$(cd "$(dirname "$0")/../other" && pwd)/fetched"

mkdir -p "${OUT_DIR}"

curl -sS "${BASE_URL}/" -o "${OUT_DIR}/home.html"
curl -sS "${BASE_URL}/api/flag?guess=C" -o "${OUT_DIR}/api-flag-rate-limited.json"
curl -sS "${BASE_URL}/api/flag/?guess=C" -o "${OUT_DIR}/api-flag-slash-correct.json"
