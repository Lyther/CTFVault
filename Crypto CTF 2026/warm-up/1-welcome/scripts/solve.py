#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Solve Crypto CTF 2026 - Welcome (base64 suffix)."""

import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "challenge.md"


def main() -> None:
    text = CHALLENGE.read_text(encoding="utf-8")
    start = text.find("CCTF{")
    end = text.find("}", start)
    inner = text[start + 5 : end]
    # Strip HTML artifact that appears after the closing brace in the markdown.
    inner = inner.split("<")[0]
    parts = inner.split("_")
    # The final segment is standard base64; the rest is leet-speak.
    last = parts[-1]
    last = last.replace("-", "+").replace("_", "/") + "=" * ((-len(last)) % 4)
    decoded = base64.b64decode(last).decode("ascii")
    # The decoded tail already ends with the closing brace if the base64 string
    # included it; merge it carefully to avoid a double brace.
    if decoded.endswith("}"):
        parts[-1] = decoded[:-1]
        flag = "CCTF{" + "_".join(parts) + "}"
    else:
        parts[-1] = decoded
        flag = "CCTF{" + "_".join(parts) + "}"
    print(flag)
    (HERE.parent / "solution" / "flag.txt").write_text(flag + "\n", encoding="utf-8")
    print("solution/flag.txt updated")


if __name__ == "__main__":
    main()
