#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import codecs
import pathlib
import struct

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "49_challenge.jpg"

XP_COMMENT_TAG = 0x9C9C


def find_exif_payload(jpeg: bytes) -> bytes:
    if not jpeg.startswith(b"\xff\xd8"):
        raise RuntimeError("not a JPEG file")

    offset = 2
    while offset + 4 <= len(jpeg):
        if jpeg[offset] != 0xFF:
            raise RuntimeError("invalid JPEG marker layout")

        marker = jpeg[offset + 1]
        offset += 2

        if marker == 0xD9:
            break
        if marker == 0xDA:
            break
        if 0xD0 <= marker <= 0xD7 or marker == 0x01:
            continue

        segment_length = struct.unpack(">H", jpeg[offset : offset + 2])[0]
        segment = jpeg[offset + 2 : offset + segment_length]
        offset += segment_length

        if marker == 0xE1 and segment.startswith(b"Exif\x00\x00"):
            return segment[6:]

    raise RuntimeError("EXIF payload not found")


def read_ifd_entries(
    payload: bytes,
    offset: int,
    endian: str,
) -> list[tuple[int, int, int, bytes]]:
    entry_count = struct.unpack_from(endian + "H", payload, offset)[0]
    entries = []
    cursor = offset + 2

    for _ in range(entry_count):
        tag, value_type, count, value_or_offset = struct.unpack_from(
            endian + "HHI4s",
            payload,
            cursor,
        )
        entries.append((tag, value_type, count, value_or_offset))
        cursor += 12

    return entries


def extract_xp_comment(exif_payload: bytes) -> str:
    if exif_payload[:2] == b"II":
        endian = "<"
    elif exif_payload[:2] == b"MM":
        endian = ">"
    else:
        raise RuntimeError("invalid TIFF byte order")

    if struct.unpack_from(endian + "H", exif_payload, 2)[0] != 42:
        raise RuntimeError("invalid TIFF header")

    ifd0_offset = struct.unpack_from(endian + "I", exif_payload, 4)[0]
    for tag, value_type, count, value_or_offset in read_ifd_entries(
        exif_payload,
        ifd0_offset,
        endian,
    ):
        if tag != XP_COMMENT_TAG:
            continue
        if value_type != 1:
            raise RuntimeError("unexpected XP Comment type")

        data_offset = struct.unpack(endian + "I", value_or_offset)[0]
        raw = exif_payload[data_offset : data_offset + count]
        return raw.decode("utf-16le").rstrip("\x00")

    raise RuntimeError("XP Comment tag not found")


def main() -> None:
    jpeg = CHALLENGE.read_bytes()
    exif_payload = find_exif_payload(jpeg)
    encoded_flag = extract_xp_comment(exif_payload)
    print(codecs.decode(encoded_flag, "rot_13"))


if __name__ == "__main__":
    main()
