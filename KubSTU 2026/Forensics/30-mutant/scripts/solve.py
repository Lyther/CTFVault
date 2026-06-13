#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import base64
import pathlib
import re
import zlib

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "30_crypt.pdf"


def extract_hidden_stream(pdf_bytes: bytes) -> bytes:
    match = re.search(
        rb"5 0 obj\s*<<[^>]*>>\s*stream\s*(.*?)\s*endstream",
        pdf_bytes,
        re.DOTALL,
    )
    if not match:
        raise ValueError("hidden object stream not found")

    raw = match.group(1).strip()
    if not (raw.startswith(b"<~") and raw.endswith(b"~>")):
        raise ValueError("object 5 does not look like ASCII85")

    ascii85 = re.sub(rb"\s+", b"", raw[2:-2])
    return zlib.decompress(base64.a85decode(ascii85, adobe=False))


def extract_flag(stream: bytes) -> str:
    text = stream.decode("latin1")
    glyphs = "".join(re.findall(r"\((.*?)\)\s*Tj", text))
    match = re.search(r"KubSTU\{[^}]+\}", glyphs)
    if not match:
        raise ValueError("flag not found")
    return match.group(0)


def main() -> None:
    pdf_bytes = CHALLENGE.read_bytes()
    hidden_stream = extract_hidden_stream(pdf_bytes)
    print(extract_flag(hidden_stream))


if __name__ == "__main__":
    main()
