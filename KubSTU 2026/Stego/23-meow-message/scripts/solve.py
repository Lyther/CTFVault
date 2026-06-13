#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "23_message.txt"


def trailing_whitespace_bits(line: str) -> str:
    visible = line.rstrip(" \t")
    trailing = line[len(visible) :]
    return "".join("0" if ch == " " else "1" for ch in trailing)


def decode_flag(text: str) -> str:
    chunks = []
    for line in text.splitlines():
        bits = trailing_whitespace_bits(line)
        if bits:
            chunks.append(chr(int(bits, 2)))

    decoded = "".join(chunks)
    start = decoded.find("KubSTU{")
    end = decoded.find("}", start)

    if start == -1 or end == -1:
        raise RuntimeError("flag not found in trailing whitespace")

    return decoded[start : end + 1]


def main() -> None:
    text = CHALLENGE.read_text(encoding="utf-8")
    print(decode_flag(text))


if __name__ == "__main__":
    main()
