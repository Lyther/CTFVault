#!/usr/bin/env bash
# Cartographer's Secret — CIT 2026 OSINT (21, 977 pts)
# Flag lives in the `flag=*` OSM tag on Flock Safety ALPR node 13735855418.
set -euo pipefail
curl -sS --globoff 'https://overpass-api.de/api/interpreter?data=[out:json];node(13735855418);out%20tags;' \
  | python3 -c 'import sys,json; t=json.load(sys.stdin)["elements"][0]["tags"]; print(t["flag"])'
