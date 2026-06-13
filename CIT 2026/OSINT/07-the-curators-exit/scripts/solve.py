#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pypdf>=5.0.0",
#   "cryptography>=3.1",
# ]
# ///

from __future__ import annotations

import hashlib
import pathlib
import sys

from pypdf import PdfReader

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "VF0000000011-Enc.pdf"
PASSWORD = "cherell"
EXPECTED_SHA1 = "c3c8f91ed60e902be482dc26b61a9bc0fa443f26"
FLAG = "CIT{Remy_Beauvillier}"


def main() -> None:
    if not CHALLENGE.is_file():
        print(f"missing {CHALLENGE}", file=sys.stderr)
        sys.exit(1)

    digest = hashlib.sha1(CHALLENGE.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA1:
        print(f"sha1 mismatch: {digest}", file=sys.stderr)
        sys.exit(1)

    reader = PdfReader(str(CHALLENGE))
    if not reader.decrypt(PASSWORD):
        print("decrypt failed", file=sys.stderr)
        sys.exit(1)

    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if "VitrineFox" not in text:
        print("expected dossier handle not found", file=sys.stderr)
        sys.exit(1)

    print(FLAG)


if __name__ == "__main__":
    main()
