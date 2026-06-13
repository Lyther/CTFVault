#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "50_ancient_note.txt"

ZERO_WIDTH_SPACE = "\u200b"
ZERO_WIDTH_NON_JOINER = "\u200c"


def extract_flag(text: str) -> str:
    bits = "".join(
        "0" if ch == ZERO_WIDTH_SPACE else "1"
        for ch in text
        if ch in (ZERO_WIDTH_SPACE, ZERO_WIDTH_NON_JOINER)
    )

    decoded = "".join(
        chr(int(bits[index : index + 8], 2)) for index in range(0, len(bits), 8)
    )

    start = decoded.find("KubSTU{")
    end = decoded.find("}", start)
    if start == -1 or end == -1:
        raise RuntimeError("flag not found in zero-width payload")

    return decoded[start : end + 1]


def main() -> None:
    text = CHALLENGE.read_text(encoding="utf-8")
    print(extract_flag(text))


if __name__ == "__main__":
    main()
