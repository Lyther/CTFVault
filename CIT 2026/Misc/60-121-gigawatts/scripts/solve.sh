#!/usr/bin/env bash
# 1.21 Gigawatts — CIT 2026 Misc (60, 1000 pts)
# SSTV → QR codes → gzip → KryoFlux floppy stream → FAT12 → FLAG.TXT
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
FILES="$HERE/files"
WAV="$FILES/121gigawatts.wav"

# 1. Decode 5 back-to-back SSTV Martin-1 frames (~114 s each)
for i in 1 2 3 4 5; do
  skip=$(( (i-1) * 114 ))
  sstv -d "$WAV" -s "$skip" -o "$FILES/qr_${i}of5.png"
done

# 2. Scan QR codes (payloads are labeled "N/5:<base64 chunk>")
for i in 1 2 3 4 5; do
  zbarimg -q --raw "$FILES/qr_${i}of5.png"
done | awk -F: '{print $2}' | tr -d '\n' > "$FILES/payload.b64"

# 3. base64 → gzip → KryoFlux raw stream
base64 -d < "$FILES/payload.b64" | gunzip > "$FILES/kryoflux_stream.raw"

# 4. KryoFlux expects track files named trackCC.H.raw. One track only.
cp "$FILES/kryoflux_stream.raw" "$FILES/track00.0.raw"

# 5. Convert single-track KryoFlux stream → 720K IBM MFM floppy image
gw convert "$FILES/track00.0.raw" "$FILES/floppy.img" --format ibm.720

# 6. Read FLAG.TXT out of the FAT12 image
strings "$FILES/floppy.img" | grep -o 'CIT{[^}]*}'
