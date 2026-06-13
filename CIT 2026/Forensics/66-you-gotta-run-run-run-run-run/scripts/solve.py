#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-registry"]
# ///

import hashlib
import pathlib
import sys

from Registry import Registry

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "challenge.dat"
EXPECTED_SHA1 = "cc0060d01e8dc3fe69a8ca888c203bc9e57959e1"
RUN_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
TARGET_PATH = r'"C:\Users\kurt\AppData\Roaming\fj3493.exe"'


def verify_sha1(path: pathlib.Path) -> None:
    digest = hashlib.sha1(path.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA1:
        raise SystemExit(f"sha1 mismatch: {digest}")


def main() -> None:
    verify_sha1(CHALLENGE)

    reg = Registry.Registry(str(CHALLENGE))
    key = reg.open(RUN_KEY)

    for value in key.values():
        if value.value() == TARGET_PATH:
            print(f"name={value.name()}")
            print(f"flag=CIT{{{value.name()}}}")
            return

    print("target Run value not found", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
