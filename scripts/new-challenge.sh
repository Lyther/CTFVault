#!/usr/bin/env bash
# Bootstrap a new challenge inside an event.
# Usage:
#   new-challenge.sh "Event Name" "challenge-name"                       # numbered (auto NN)
#   new-challenge.sh "Event Name" "challenge-name" "Web"                 # categorized, no NN
#   new-challenge.sh "Event Name" "challenge-name" "Web"      ""         # same as above
#   new-challenge.sh "Event Name" "challenge-name" "Web"      42         # categorized, NN=42
#   new-challenge.sh "Event Name" "challenge-name" ""         42         # numbered, force NN=42
set -euo pipefail

EVENT="${1:-}"
NAME="${2:-}"
CATEGORY="${3:-}"
ID_OVERRIDE="${4:-}"

if [[ -z "${EVENT}" || -z "${NAME}" ]]; then
  printf 'usage: %s "Event Name" "challenge-name" ["Category"] [ID]\n' "$0" >&2
  exit 2
fi

if [[ -n "${ID_OVERRIDE}" && ! "${ID_OVERRIDE}" =~ ^[0-9]+$ ]]; then
  printf 'error: ID must be numeric (got %q)\n' "${ID_OVERRIDE}" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EVENT_DIR="${ROOT}/${EVENT}"

if [[ ! -d "${EVENT_DIR}" ]]; then
  printf 'error: event dir not found: %q (run: make event NAME=%q)\n' "${EVENT_DIR}" "${EVENT}" >&2
  exit 1
fi

slug() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g'
}

SLUG="$(slug "${NAME}")"

next_nn() {
  # Scan a directory for NN-<slug>/ children and return next free NN (zero-padded to 2).
  local scan_dir="$1"
  local next=1 d n
  shopt -s nullglob
  for d in "${scan_dir}"/[0-9]*-*/; do
    n="$(basename "$d" | cut -d- -f1)"
    [[ "${n}" =~ ^0*[0-9]+$ ]] || continue
    n=$((10#${n}))
    (( n + 1 > next )) && next=$((n + 1))
  done
  shopt -u nullglob
  printf '%02d' "${next}"
}

if [[ -n "${CATEGORY}" ]]; then
  if [[ -n "${ID_OVERRIDE}" ]]; then
    printf -v NN '%02d' "${ID_OVERRIDE}"
    CHALL_DIR="${EVENT_DIR}/${CATEGORY}/${NN}-${SLUG}"
  else
    CHALL_DIR="${EVENT_DIR}/${CATEGORY}/${SLUG}"
  fi
else
  if [[ -n "${ID_OVERRIDE}" ]]; then
    printf -v NN '%02d' "${ID_OVERRIDE}"
  else
    NN="$(next_nn "${EVENT_DIR}")"
  fi
  CHALL_DIR="${EVENT_DIR}/${NN}-${SLUG}"
fi

if [[ -e "${CHALL_DIR}" ]]; then
  printf 'error: %q already exists\n' "${CHALL_DIR}" >&2
  exit 1
fi

mkdir -p "${CHALL_DIR}"

CAT_LABEL="${CATEGORY:-?}"
sed -e "s|{{CHALLENGE_NAME}}|${NAME}|g" \
    -e "s|{{AUTHOR}}|?|g" \
    -e "s|{{CATEGORY}}|${CAT_LABEL}|g" \
    -e "s|{{DIFFICULTY}}|?|g" \
    -e "s|{{POINTS}}|?|g" \
    "${ROOT}/templates/DESCRIPTION.md" > "${CHALL_DIR}/DESCRIPTION.md"

sed -e "s|{{CHALLENGE_NAME}}|${NAME}|g" \
    -e "s|{{FLAG_OR_REDACTED}}|[REDACTED]|g" \
    "${ROOT}/templates/WRITEUP.md" > "${CHALL_DIR}/WRITEUP.md"

printf 'created challenge: %s\n' "${CHALL_DIR}"
