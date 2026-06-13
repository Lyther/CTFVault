#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_PATH="$ROOT_DIR/other/reconstructed/app.py"
PORT="${1:-5009}"

exec env \
  PORT="$PORT" \
  FLAG_VALUE="${FLAG_VALUE:-CIT{test_flag}}" \
  uv run --with Flask==3.1.0 python "$APP_PATH"
