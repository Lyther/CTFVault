#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import io
import pathlib
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "51_bembembem.mp4"
TRAILER_KEY = b"6899efc8f52bffb08c5ac45deee24f64"
ZIP_PASSWORD = b"K0t05t"


def iter_top_level_boxes(data: bytes) -> list[tuple[int, str, int]]:
    boxes: list[tuple[int, str, int]] = []
    pos = 0

    while pos + 8 <= len(data):
        size = int.from_bytes(data[pos : pos + 4], "big")
        kind = data[pos + 4 : pos + 8].decode("latin1", "replace")
        header = 8

        if size == 1:
            if pos + 16 > len(data):
                break
            size = int.from_bytes(data[pos + 8 : pos + 16], "big")
            header = 16
        elif size == 0:
            size = len(data) - pos

        if size < header or pos + size > len(data):
            break

        boxes.append((pos, kind, size))
        pos += size

    return boxes


def xor_repeat(data: bytes, key: bytes) -> bytes:
    return bytes(byte ^ key[index % len(key)] for index, byte in enumerate(data))


def main() -> None:
    data = CHALLENGE.read_bytes()
    boxes = iter_top_level_boxes(data)
    last_end = boxes[-1][0] + boxes[-1][2]
    trailer = data[last_end:]
    zip_data = xor_repeat(trailer, TRAILER_KEY)

    with zipfile.ZipFile(io.BytesIO(zip_data)) as archive:
        flag = archive.read("flag.txt", pwd=ZIP_PASSWORD).decode().strip()

    print(flag)


if __name__ == "__main__":
    main()
