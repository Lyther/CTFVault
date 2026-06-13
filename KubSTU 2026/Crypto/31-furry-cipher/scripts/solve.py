#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import pathlib
import string
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "31_Furry_Cipher.zip"
WEIRD_TEXT = "Furry Cipher/Weird_Furry_text.txt"
KNOWN_PREFIX = "KubSTU("
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits
MULTIPLIERS = (13, 17, 19)


def extract_sparse_ciphertext() -> str:
    allowed = (string.ascii_letters + string.digits + "()_").encode()
    delete = bytes(byte for byte in range(256) if byte not in allowed)
    pieces = []

    with zipfile.ZipFile(CHALLENGE) as archive, archive.open(WEIRD_TEXT) as stream:
        while chunk := stream.read(1 << 20):
            pieces.append(chunk.translate(None, delete))

    return b"".join(pieces).decode("ascii")


def derive_additions(ciphertext: str) -> dict[int, int]:
    char_to_num = {ch: i for i, ch in enumerate(ALPHABET)}
    additions = {}

    for i, (plain, encrypted) in enumerate(zip(KNOWN_PREFIX, ciphertext)):
        if plain in "()_":
            continue
        residue = i % 3
        additions[residue] = (
            char_to_num[encrypted] - char_to_num[plain] * MULTIPLIERS[residue]
        ) % len(ALPHABET)

    if sorted(additions) != [0, 1, 2]:
        raise ValueError("could not derive all three cipher additions")

    return additions


def decrypt(ciphertext: str) -> str:
    char_to_num = {ch: i for i, ch in enumerate(ALPHABET)}
    num_to_char = dict(enumerate(ALPHABET))
    additions = derive_additions(ciphertext)
    result = []

    for i, char in enumerate(ciphertext):
        if char in "()_":
            result.append(char)
            continue
        residue = i % 3
        plain_num = (
            (char_to_num[char] - additions[residue])
            * pow(MULTIPLIERS[residue], -1, len(ALPHABET))
        ) % len(ALPHABET)
        result.append(num_to_char[plain_num])

    return "".join(result)


def main() -> None:
    ciphertext = extract_sparse_ciphertext()
    print(decrypt(ciphertext))


if __name__ == "__main__":
    main()
