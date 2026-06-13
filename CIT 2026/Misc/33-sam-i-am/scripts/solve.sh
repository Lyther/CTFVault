#!/usr/bin/env bash
# Crack 5-character NTLM from dumped SAM hive with a brute-force mask.
# Password policy: 5 chars + complexity (upper/lower/digit/symbol).
set -euo pipefail

HASH="97a3e51e5a006eccac91e0ceabd4965b"
echo "$HASH" > /tmp/sam.hash

# NTLM = hashcat mode 1000. Mask ?a^5 covers all printable ASCII (95^5 ≈ 7.7B).
# On a modest GPU/CPU this finishes in seconds.
hashcat -m 1000 -a 3 /tmp/sam.hash '?a?a?a?a?a' -o /tmp/sam.cracked --potfile-path /tmp/sam.pot
cat /tmp/sam.cracked
# Expect: 97a3e51e5a006eccac91e0ceabd4965b:C1t!!
# Flag   : CIT{C1t!!}
