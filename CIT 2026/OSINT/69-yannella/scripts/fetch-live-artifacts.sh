#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${ROOT}/other"
CHALLENGE_ID="69"
CHALLENGE_API_URL="https://ctf.cyber-cit.club/api/v1/challenges/${CHALLENGE_ID}"
DOE_ACK_URL="https://doe.responsibledisclosure.com/hc/en-us/articles/360052066474-Acknowledgments"
DOE_ACK_TEXT_URL="https://r.jina.ai/http://doe.responsibledisclosure.com/hc/en-us/articles/360052066474-Acknowledgments"

mkdir -p "${OUT_DIR}"

curl -fsSL "${CHALLENGE_API_URL}" -o "${OUT_DIR}/challenge-api.json"
curl -sSL "${DOE_ACK_URL}" -o "${OUT_DIR}/doe-acknowledgments.html"
curl -fsSL "${DOE_ACK_TEXT_URL}" -o "${OUT_DIR}/doe-acknowledgments.txt"
