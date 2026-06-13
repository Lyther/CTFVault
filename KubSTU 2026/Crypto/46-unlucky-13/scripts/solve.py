#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import hashlib
import pathlib
import re
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "46_Unlucky_13.zip"
OUTPUT = "Unlucky 13/output.txt"
UNLUCKY_NUMBER = 13


def read_output() -> dict[str, int]:
    with zipfile.ZipFile(CHALLENGE) as archive:
        text = archive.read(OUTPUT).decode("ascii")
    return {
        name: int(value)
        for name, value in re.findall(r"^(\w+) = (\d+)", text, re.MULTILINE)
    }


def integer_cube_root(value: int) -> int:
    low = 0
    high = 1 << ((value.bit_length() + 2) // 3)

    while low <= high:
        mid = (low + high) // 2
        cubed = mid**3
        if cubed == value:
            return mid
        if cubed < value:
            low = mid + 1
        else:
            high = mid - 1

    raise ValueError("ciphertext is not an exact cube")


def cursed_prng(seed: int, length: int) -> bytes:
    state = seed
    stream = []
    for _ in range(length):
        state = (state * 1313 + 131313) % 2**32
        stream.append(state & 0xFF)
    return bytes(stream)


def forgotten_cipher(key: bytes, data: bytes) -> bytes:
    sbox = list(range(256))
    j = 0

    for i in range(256):
        j = (j + sbox[i] + key[i % len(key)]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]

    i = j = 0
    out = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + sbox[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
        out.append(byte ^ sbox[(sbox[i] + sbox[j]) % 256])

    return bytes(out)


def main() -> None:
    values = read_output()
    layer2_int = integer_cube_root(values["c"])
    layer2 = layer2_int.to_bytes((layer2_int.bit_length() + 7) // 8, "big")
    key = hashlib.sha256(b"Unlucky13").digest()[:16]
    layer1 = forgotten_cipher(key, layer2)
    flag = bytes(
        byte ^ stream_byte
        for byte, stream_byte in zip(
            layer1,
            cursed_prng(UNLUCKY_NUMBER, len(layer1)),
        )
    )
    print(flag.decode())


if __name__ == "__main__":
    main()
