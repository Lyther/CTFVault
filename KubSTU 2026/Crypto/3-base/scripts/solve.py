#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import base64
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "3_Base.txt"


def main() -> None:
    encoded = CHALLENGE.read_text(encoding="ascii").strip()
    flag = base64.b64decode(encoded, validate=True).decode("utf-8")
    print(flag)


if __name__ == "__main__":
    main()
