#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pycryptodome>=3.23.0"]
# ///
"""Peel the Base64 onion, then verify the recovered NTLM plaintext."""

from __future__ import annotations

import base64
import binascii
import pathlib
import re
import sys

from Crypto.Hash import MD4

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "challenge.txt"
HEX32 = re.compile(rb"^[0-9a-f]{32}$")
RECOVERED = "iloveharrypottersomuchthaticouldreadallthebooksintwodaysmostlikely"


def peel_to_hash(data: bytes) -> tuple[str, int]:
    """Base64-decode until the innermost 32-hex digest appears."""
    layers = 0
    while True:
        stripped = data.strip()
        if HEX32.fullmatch(stripped):
            return stripped.decode(), layers
        try:
            decoded = base64.b64decode(stripped, validate=True)
        except (binascii.Error, ValueError):
            raise ValueError("Base64 stopped before the expected 32-hex digest")
        if not decoded.isascii():
            raise ValueError("Over-decoded past the digest layer into binary noise")
        data = decoded
        layers += 1


def ntlm_hex(text: str) -> str:
    h = MD4.new()
    h.update(text.encode("utf-16le"))
    return h.hexdigest()


def main() -> None:
    if not CHALLENGE.is_file():
        sys.exit(f"missing challenge file: {CHALLENGE}")
    blob = CHALLENGE.read_bytes()
    inner_hash, n = peel_to_hash(blob)
    assert ntlm_hex(RECOVERED) == inner_hash, "recovered plaintext does not match"
    print(f"base64_layers: {n}")
    print(f"inner_hash: {inner_hash}")
    print("hash_type: NTLM")
    print(f"plaintext: {RECOVERED}")
    print(f"flag: CIT{{{RECOVERED}}}")


if __name__ == "__main__":
    main()
