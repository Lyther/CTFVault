#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow"]
# ///

from __future__ import annotations

import io
import pathlib
import zipfile

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "33_capybara_nightmare.png"

ZIP_MAGIC = b"PK\x03\x04"


def extract_overlay_zip(png_bytes: bytes) -> zipfile.ZipFile:
    offset = png_bytes.find(ZIP_MAGIC)
    if offset == -1:
        raise RuntimeError("ZIP overlay not found in PNG")

    return zipfile.ZipFile(io.BytesIO(png_bytes[offset:]))


def extract_lsb_key(image_path: pathlib.Path, length: int) -> str:
    image = Image.open(image_path).convert("RGB")
    bits: list[str] = []

    for channel in image.tobytes():
        bits.append("1" if (channel & 1) else "0")
        if len(bits) == length * 8:
            data = bytearray(
                int("".join(bits[index : index + 8]), 2)
                for index in range(0, len(bits), 8)
            )
            return data.decode("ascii")

    raise RuntimeError("not enough LSB data to recover key")


def xor_decrypt(ciphertext: bytes, key: str) -> str:
    return "".join(
        chr(byte ^ ord(key[index % len(key)])) for index, byte in enumerate(ciphertext)
    )


def main() -> None:
    png_bytes = CHALLENGE.read_bytes()
    with extract_overlay_zip(png_bytes) as archive:
        ciphertext = archive.read("encrypted_flag.bin")

    key = extract_lsb_key(CHALLENGE, length=19)
    print(xor_decrypt(ciphertext, key))


if __name__ == "__main__":
    main()
