#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://23.179.17.92:5002}"
OUT_DIR="$(cd "$(dirname "$0")/../other" && pwd)/fetched"

mkdir -p "${OUT_DIR}"

curl -sS "${BASE_URL}/" -o "${OUT_DIR}/home.html"
curl -sS "${BASE_URL}/admin" -o "${OUT_DIR}/admin-debug.html"
curl -sS "${BASE_URL}/flg_bar" -o "${OUT_DIR}/.env"
curl -sS "${BASE_URL}/admin?__debugger__=yes&cmd=resource&f=debugger.js" -o "${OUT_DIR}/debugger.js"
curl -sS "${BASE_URL}/admin?__debugger__=yes&cmd=resource&f=style.css" -o "${OUT_DIR}/style.css"
