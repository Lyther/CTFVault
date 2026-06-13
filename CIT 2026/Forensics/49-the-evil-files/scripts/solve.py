#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pypdf>=4.2.0",
# ]
# ///

import hashlib
import re
import sys
from pathlib import Path

from pypdf import PdfReader


EXPECTED_SHA1 = "2230cff50d7ae8672ab072d275df7057773f11eb"


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def main() -> None:
    default_pdf = Path(__file__).resolve().parent.parent / "files" / "challenge.pdf"
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_pdf

    if not pdf_path.is_file():
        fail(f"missing PDF: {pdf_path}")

    sha1 = hashlib.sha1(pdf_path.read_bytes()).hexdigest()
    if sha1 != EXPECTED_SHA1:
        fail(f"unexpected sha1: {sha1}")

    reader = PdfReader(str(pdf_path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    match = re.search(r"CIT\{[^}\s]+\}", text)
    if not match:
        fail("flag not found in extracted PDF text")

    print(match.group(0))


if __name__ == "__main__":
    main()
