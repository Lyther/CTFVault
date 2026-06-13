#!/usr/bin/env bash
# Count events, challenges, and writeups across both naming conventions:
#   - CPCTF style: DESCRIPTION.md + WRITEUP.md
#   - CIT style:   challenge.md / challenge.json + writeup.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

# Events = top-level dirs that aren't infra dirs.
events=0
shopt -s nullglob
for d in */; do
  case "${d%/}" in
    notes|tools|templates|scripts|docs|.*) continue ;;
  esac
  events=$((events + 1))
done
shopt -u nullglob

# Collect unique challenge dirs (any folder containing a marker file).
chall_dirs="$(
  find . -mindepth 3 \
    \( -iname 'DESCRIPTION.md' -o -iname 'challenge.md' -o -iname 'challenge.json' \) \
    -not -path '*/.git/*' \
    -not -path '*/node_modules/*' \
    -not -path './notes/*' -not -path './tools/*' \
    -not -path './templates/*' -not -path './scripts/*' \
    -not -path './docs/*' -not -path './.cursor/*' -not -path './.github/*' \
    -print 2>/dev/null \
  | while read -r f; do dirname "$f"; done \
  | sort -u
)"

if [[ -z "${chall_dirs}" ]]; then
  total=0
else
  total=$(printf '%s\n' "${chall_dirs}" | wc -l | tr -d ' ')
fi

written=0
while IFS= read -r dir; do
  [[ -z "${dir}" ]] && continue
  for w in WRITEUP.md writeup.md Writeup.md; do
    if [[ -f "${dir}/${w}" ]]; then
      written=$((written + 1))
      break
    fi
  done
done <<<"${chall_dirs}"

printf 'events:     %d\n' "${events}"
printf 'challenges: %d\n' "${total}"
printf 'writeups:   %d\n' "${written}"
printf 'pending:    %d\n' "$((total - written))"
