#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ACKNOWLEDGMENTS = HERE.parent / "other" / "doe-acknowledgments.txt"
FLAG = "CIT{Department_of_Energy}"
NAME_NEEDLE = "Anthony Yannella"
ORG_NEEDLE = "valid vulnerabilities to the Department of Energy"


def main() -> None:
    if not ACKNOWLEDGMENTS.is_file():
        print(f"missing {ACKNOWLEDGMENTS}", file=sys.stderr)
        sys.exit(1)

    text = ACKNOWLEDGMENTS.read_text(encoding="utf-8")

    if NAME_NEEDLE not in text:
        print(f"expected name not found in {ACKNOWLEDGMENTS}", file=sys.stderr)
        sys.exit(1)

    if ORG_NEEDLE not in text:
        print(
            f"expected organization clue not found in {ACKNOWLEDGMENTS}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(FLAG)


if __name__ == "__main__":
    main()
