#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import base64
import hashlib
import pathlib
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "challenge.zip"
EXPECTED_SHA1 = "aa50aa4516d0bc7b0aa23139f95d38edd916164a"
STARTUP_PATH = (
    "kurt_backup/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"
    "e9fje2.txt"
)


def verify_sha1(path: pathlib.Path) -> None:
    digest = hashlib.sha1(path.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA1:
        raise SystemExit(f"sha1 mismatch: {digest}")


def main() -> None:
    verify_sha1(CHALLENGE)

    with zipfile.ZipFile(CHALLENGE) as zf:
        encoded = zf.read(STARTUP_PATH).decode("utf-8", errors="replace").strip()

    decoded = base64.b64decode(encoded).decode()
    print(f"encoded={encoded}")
    print(f"flag={decoded}")


if __name__ == "__main__":
    main()
