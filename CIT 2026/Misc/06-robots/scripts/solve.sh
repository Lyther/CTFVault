#!/usr/bin/env bash
# Robots — CIT 2026 Misc (06, 877 pts)
# Flag is appended after ~300 blank lines at the bottom of /robots.txt
set -euo pipefail
curl -sS https://ctf.cyber-cit.club/robots.txt | grep -E '^CIT\{.*\}$'
