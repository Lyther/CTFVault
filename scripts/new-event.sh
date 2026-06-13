#!/usr/bin/env bash
# Bootstrap a new CTF event folder.
# Usage: new-event.sh "Event Name 2026" [numbered|categorized]
set -euo pipefail

NAME="${1:-}"
STYLE="${2:-numbered}"

if [[ -z "${NAME}" ]]; then
  printf 'usage: %s "Event Name" [numbered|categorized]\n' "$0" >&2
  exit 2
fi

case "${STYLE}" in
  numbered|categorized) ;;
  *) printf 'error: STYLE must be "numbered" or "categorized" (got %q)\n' "${STYLE}" >&2; exit 2;;
esac

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EVENT_DIR="${ROOT}/${NAME}"

if [[ -e "${EVENT_DIR}" ]]; then
  printf 'error: %q already exists\n' "${EVENT_DIR}" >&2
  exit 1
fi

mkdir -p "${EVENT_DIR}"

# Render event README from template.
sed "s/{{EVENT_NAME}}/${NAME}/g" "${ROOT}/templates/EVENT.md" > "${EVENT_DIR}/README.md"

if [[ "${STYLE}" == "categorized" ]]; then
  for cat in Web Crypto Pwn Reverse Forensics Misc OSINT; do
    mkdir -p "${EVENT_DIR}/${cat}"
    : > "${EVENT_DIR}/${cat}/.gitkeep"
  done
fi

printf 'created event: %s (style=%s)\n' "${EVENT_DIR}" "${STYLE}"
