#!/usr/bin/env -S uv run

import hashlib
import re
import sys
import zipfile
from pathlib import Path

EXPECTED_SHA1 = "e72c9837de62168b2b5cc573a55800ea1e440b42"
TARGET_MEMBER = "ppt/slides/transitions.xml"


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def main() -> None:
    default_pptx = Path(__file__).resolve().parent.parent / "files" / "challenge.pptx"
    pptx_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_pptx

    if not pptx_path.is_file():
        fail(f"missing PowerPoint file: {pptx_path}")

    sha1 = hashlib.sha1(pptx_path.read_bytes()).hexdigest()
    if sha1 != EXPECTED_SHA1:
        fail(f"unexpected sha1: {sha1}")

    with zipfile.ZipFile(pptx_path) as archive:
        try:
            transitions = archive.read(TARGET_MEMBER).decode("utf-8", "ignore")
        except KeyError:
            fail(f"missing OOXML part: {TARGET_MEMBER}")

    match = re.search(r"CIT\{[^}\s]+\}", transitions)
    if not match:
        fail("flag not found in transitions.xml")

    print(match.group(0))


if __name__ == "__main__":
    main()
