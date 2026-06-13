#!/usr/bin/env bash
# Solve "What's the word?" — crack the encrypted MS Office doc and extract the flag image.
#
# 1. Detect container: file(1) says "CDFV2 Encrypted", i.e. an OLE2-wrapped
#    OOXML with DataSpaces/EncryptedPackage streams -> password-protected Word doc.
# 2. Extract a John-compatible hash via office2john.py (needs olefile).
#    $office$*2013*100000*256*16*...  => Office 2013, hashcat mode 9600.
# 3. Crack with hashcat + rockyou on GPU (local M3: 2.6k H/s, L4: 17k H/s).
#    Password: q1w2e3r4t5  (keyboard walk, found inside the first 262k candidates).
# 4. Decrypt with msoffcrypto-tool, unzip the .docx, read word/media/image1.png.
#    The flag is rendered on top of the image: CIT{b1rd_1s_th3_w0rd}.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
SRC="$ROOT/files/file"
OUT="$ROOT/solution"
mkdir -p "$OUT"

# 1-2) Extract Office 2013 hash.
curl -sL https://raw.githubusercontent.com/openwall/john/bleeding-jumbo/run/office2john.py -o /tmp/office2john.py
uvx --quiet --with olefile python /tmp/office2john.py "$SRC" | cut -d: -f2- > "$OUT/office.hash"

# 3) GPU crack (run on dev-box-gpu / L4). Example:
#    scp "$OUT/office.hash" dev-box-gpu:/tmp/office.hash
#    ssh dev-box-gpu 'hashcat -m 9600 /tmp/office.hash /tmp/rockyou.txt -O -o /tmp/office.cracked'
PASSWORD="q1w2e3r4t5"

# 4) Decrypt + extract embedded image.
uvx --quiet --from msoffcrypto-tool msoffcrypto-tool -p "$PASSWORD" "$SRC" "$OUT/decrypted.docx"
unzip -o -j "$OUT/decrypted.docx" word/media/image1.png -d "$OUT" >/dev/null
echo "Flag image: $OUT/image1.png"
echo "Flag: CIT{b1rd_1s_th3_w0rd}"
