#!/bin/bash
# Attempt ZMODEM upload via BBS 'U' command, then fetch via jailHTTPd.
# Theory: the 1986 manual = ZMODEM (Chuck Forsberg). Upload lands in /UPLOADS
# which may be reachable through jailHTTPd on :2222.

set -e
HOST="23.179.17.92"
BBS_PORT=2323
DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"

# Create a tiny test payload with a distinctive marker.
MARK="CTF_PROBE_$(date +%s)"
TESTFILE="/tmp/probe_${MARK}.txt"
echo "$MARK" > "$TESTFILE"

echo "[*] Test file: $TESTFILE (marker: $MARK)"
echo "[*] Need: lrzsz (sz command) installed."
command -v sz >/dev/null || { echo "[!] Install lrzsz: brew install lrzsz"; exit 1; }

# Script the BBS: login as GUEST, navigate to upload, invoke sz.
# BBS menu: M F D W U C N G  (U = Upload assumed)
# The standard interaction: server sends ZRQINIT, client sz sends ZFIN/ZFILE.
#
# Two-way pipe via a FIFO so sz can talk ZMODEM with the BBS.
FIFO="/tmp/bbs_${MARK}.fifo"
rm -f "$FIFO" && mkfifo "$FIFO"

(
    # Feed credentials/commands, then switch to binary mode for sz.
    echo "GUEST"
    sleep 0.4
    echo ""
    sleep 0.4
    echo "U"                 # Upload menu
    sleep 0.8
    # Filename prompt (if any) - give a safe ASCII name
    echo "probe.txt"
    sleep 0.4
    # Now spawn sz which speaks ZMODEM on our stdout.
    sz -b -e "$TESTFILE"
    sleep 0.5
    echo "G"                 # Goodbye
) < "$FIFO" | nc "$HOST" "$BBS_PORT" > "$FIFO" &

BG=$!
wait $BG || true
rm -f "$FIFO"

echo "[*] Upload attempt finished. Now probing jailHTTPd for the marker..."

PATHS_TO_TRY=(
    "/uploads/probe.txt"
    "/UPLOADS/probe.txt"
    "/uploads/probe"
    "/probe.txt"
    "/probe"
    "/incoming/probe.txt"
    "/pub/incoming/probe.txt"
)

for p in "${PATHS_TO_TRY[@]}"; do
    body=$(printf 'GET %s HTTP/1.0\r\n\r\n' "$p" | \
        ssh -i files/id_ed25519 -p 2222 -o StrictHostKeyChecking=no \
            ctf@$HOST 2>/dev/null || true)
    if echo "$body" | grep -q "$MARK"; then
        echo "[+] HIT: $p -- marker found!"
        echo "$body"
        exit 0
    else
        status=$(echo "$body" | awk '/^HTTP\/1.0 [0-9]/{s=$2} END{print s}')
        echo "    $p -> $status"
    fi
done

echo "[-] Marker not found via tried paths."
