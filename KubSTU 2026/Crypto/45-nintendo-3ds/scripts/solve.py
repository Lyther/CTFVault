#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pycryptodome",
# ]
# ///

import base64
import pathlib
import re

from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "45_output_2.txt"


def main() -> None:
    text = CHALLENGE.read_text(encoding="ascii")
    values = dict(re.findall(r"^(\w+)\s*=\s*(.+)$", text, re.MULTILINE))

    key = b"".join(
        [
            base64.b64decode(values["1"]),
            bytes(int(item) for item in values["2"].split()),
            bytes.fromhex(values["3"]),
        ],
    )
    ivx = bytes.fromhex(values["ivx"])
    ivm = values["ivm"].encode("ascii")
    iv = bytes(left ^ right for left, right in zip(ivx, ivm))
    ciphertext = bytes.fromhex(text.strip().splitlines()[-1])

    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    flag = unpad(cipher.decrypt(ciphertext), DES3.block_size)
    print(flag.decode())


if __name__ == "__main__":
    main()
