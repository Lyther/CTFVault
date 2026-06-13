#!/bin/bash
# Download files from BBS via ZMODEM
# Usage: ./bbs_download.sh [file_number]

HOST="23.179.17.92"
PORT="2323"
FILE_NUM="${1:-1}"

cd "$(dirname "$0")/../files" || exit 1

# BBS menu navigation: login as GUEST, go to files, select file, download
{
    echo "GUEST"
    sleep 0.5
    echo ""
    sleep 0.5
    echo "4"      # Files area
    sleep 0.5
    echo "$FILE_NUM"  # File number
    sleep 0.5
    echo "d"      # Download
} | nc "$HOST" "$PORT" | rz --disable-timeout -y

echo "Download complete. Check files/ directory."
