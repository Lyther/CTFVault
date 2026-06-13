#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "21_stego_challenge.pdf"


def extract_widths(pdf_text: str) -> list[int]:
    match = re.search(r"/Widths\s+(\d+)\s+0\s+R", pdf_text)
    if match is None:
        raise RuntimeError("width table reference not found")

    object_id = match.group(1)
    array_match = re.search(
        rf"{object_id} 0 obj\s*\[(.*?)\]\s*endobj",
        pdf_text,
        re.DOTALL,
    )
    if array_match is None:
        raise RuntimeError("width table object not found")

    return [int(token) for token in array_match.group(1).split()]


def decode_flag(widths: list[int]) -> str:
    decoded = "".join(chr(width // 10) for width in widths)
    start = decoded.find("KubSTU{")
    end = decoded.find("}", start)

    if start == -1 or end == -1:
        raise RuntimeError("flag not found in width table")

    return decoded[start : end + 1]


def main() -> None:
    pdf_text = CHALLENGE.read_text(encoding="latin1")
    widths = extract_widths(pdf_text)
    flag = decode_flag(widths)
    print(flag)


if __name__ == "__main__":
    main()
