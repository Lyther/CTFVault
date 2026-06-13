#!/usr/bin/env bash
# One-liner: the flag is in the JPEG's EXIF ImageDescription tag.
set -euo pipefail
IMG="$(dirname "$0")/../files/flag.jpg"
file "$IMG"             # prints description=CIT{...}
# Alt path: raw bytes near offset 0x68
xxd "$IMG" | grep -a -oE 'CIT\{[^}]+\}' | head -1
