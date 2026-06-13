#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "base65536==0.1.1",
# ]
# ///

from __future__ import annotations

import base64
import pathlib
import re

import base65536

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "challenge.txt"

MORSE = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
}


def decode_morse(text: str) -> str:
    return "".join(MORSE[token] for token in text.split())


def decode_layers() -> tuple[str, str, str]:
    morse = CHALLENGE.read_text(encoding="utf-8").strip()
    dna = decode_morse(morse)

    codons = [dna[index : index + 3] for index in range(0, len(dna), 3)]
    codons = [codon for codon in codons if len(codon) == 3 and codon != "ATG"]

    ordered = sorted(set(codons))
    nibble_map = {
        codon: format((index - 6) % 16, "x") for index, codon in enumerate(ordered)
    }

    base64_text = bytes.fromhex("".join(nibble_map[codon] for codon in codons)).decode(
        "ascii",
    )
    unicode_text = base64.b64decode(base64_text).decode("utf-8")
    decoded_message = base65536.decode(unicode_text).decode("utf-8")
    return base64_text, unicode_text, decoded_message


def recover_flag(message: str) -> str:
    match = re.search(r"CIT\{[^}\r\n]+\}", message)
    if match is None:
        raise RuntimeError("Flag not found in decoded message.")
    return match.group(0)


def main() -> None:
    _, _, message = decode_layers()
    print(recover_flag(message))


if __name__ == "__main__":
    main()
