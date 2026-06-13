#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://23.179.17.92:5555}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${ROOT}/other/fetched"

mkdir -p "${OUT_DIR}"
uv run "${ROOT}/scripts/solve.py" "${BASE_URL}" --out-dir "${OUT_DIR}" --fetch-only
