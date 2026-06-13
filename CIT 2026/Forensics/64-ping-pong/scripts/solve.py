#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import hashlib
import pathlib
import re
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "challenge.zip"
EXPECTED_SHA1 = "aa50aa4516d0bc7b0aa23139f95d38edd916164a"
PSREADLINE_PATH = (
    "kurt_backup/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/"
    "ConsoleHost_history.txt"
)


def verify_sha1(path: pathlib.Path) -> None:
    digest = hashlib.sha1(path.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA1:
        raise SystemExit(f"sha1 mismatch: {digest}")


def main() -> None:
    verify_sha1(CHALLENGE)

    with zipfile.ZipFile(CHALLENGE) as zf:
        history = zf.read(PSREADLINE_PATH).decode("utf-8", errors="replace")

    match = re.search(r"\$p='([^']+)'", history)
    if not match:
        raise SystemExit("ping target not found")

    website = match.group(1)
    print(f"website={website}")
    print(f"flag=CIT{{{website}}}")


if __name__ == "__main__":
    main()
