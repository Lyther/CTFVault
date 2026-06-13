#!/usr/bin/env bash
# Help! I've forgotten my password and I can't login! — CIT 2026 Misc (36, 986 pts)
# Blocker: stock john-1.9.0-jumbo's keepass2john rejects KDBX4.
# Fix: john bleeding-jumbo + KeePass-opencl (PR #5574, Nov 2024).
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
FILES="$HERE/files"
JOHN="${JOHN_DIR:-$HOME/john-bleeding/run}"

# 1. build john bleeding-jumbo once
if [[ ! -x "$JOHN/john" ]]; then
  git clone --depth 1 -b bleeding-jumbo https://github.com/openwall/john.git "$(dirname "$JOHN")"
  ( cd "$(dirname "$JOHN")/src" && ./configure --enable-opencl && make -sj )
fi

# 2. grab a wordlist
if [[ ! -f rockyou.txt ]]; then
  curl -sSL -o rockyou.txt https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
fi

# 3. extract KDBX4 hash
"$JOHN/keepass2john" "$FILES/Database.kdbx" > help.hash

# 4. crack on GPU
"$JOHN/john" --format=KeePass-opencl --wordlist=rockyou.txt help.hash

# 5. show the password, then the flag
PW=$("$JOHN/john" --show help.hash | head -1 | cut -d: -f2)
echo "master password: $PW"

python3 - "$FILES/Database.kdbx" "$PW" << 'PY'
import sys
from pykeepass import PyKeePass
kp = PyKeePass(sys.argv[1], password=sys.argv[2])
for e in kp.entries:
    if e.password and e.password.startswith("CIT{"):
        print(e.password)
PY
