#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pycryptodome",
# ]
# ///

import pathlib
import re
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.number import inverse, long_to_bytes

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "5_output_1.txt"

N1_PATCH_INDEX = 234
N1_BAD_DIGITS = "36"
N1_GOOD_DIGITS = "03"
LOST_BITS_DUMP_A = 72
LOST_BITS_DUMP_B = 80
X1 = 807033928375566434623
X2 = 1069912754115005437856435


def parse_output() -> dict[str, list[str]]:
    text = CHALLENGE.read_text(encoding="ascii")
    values: dict[str, list[str]] = {}

    for name, value in re.findall(r"(?m)^(\w+)\s*=\s*([0-9a-f]+)\s*$", text):
        values.setdefault(name, []).append(value)

    return values


def patch_n1(n1: int) -> int:
    digits = str(n1)
    assert digits[N1_PATCH_INDEX : N1_PATCH_INDEX + 2] == N1_BAD_DIGITS
    patched = digits[:N1_PATCH_INDEX] + N1_GOOD_DIGITS + digits[N1_PATCH_INDEX + 2 :]
    return int(patched)


def main() -> None:
    values = parse_output()

    n1 = int(values["n"][0])
    e1 = int(values["e"][0])
    hint1 = int(values["hint"][0])

    n2 = int(values["n"][1])
    e2 = int(values["e"][1])
    hint2 = int(values["hint"][1])

    assert e1 == e2 == 65537

    fixed_n1 = patch_n1(n1)
    p1 = (hint1 << LOST_BITS_DUMP_A) + X1
    assert fixed_n1 % p1 == 0
    q1 = fixed_n1 // p1
    phi1 = (p1 - 1) * (q1 - 1)
    d1 = inverse(e1, phi1)

    p2 = (hint2 << LOST_BITS_DUMP_B) + X2
    assert n2 % p2 == 0
    q2 = n2 // p2
    phi2 = (p2 - 1) * (q2 - 1)
    d2 = inverse(e2, phi2)

    key = sha256(long_to_bytes(d1) + long_to_bytes(d2)).digest()[:16]

    cipher = AES.new(key, AES.MODE_GCM, nonce=bytes.fromhex(values["nonce"][0]))
    plaintext = cipher.decrypt_and_verify(
        bytes.fromhex(values["data"][0]),
        bytes.fromhex(values["auth"][0]),
    )

    print(plaintext.decode())


if __name__ == "__main__":
    main()
