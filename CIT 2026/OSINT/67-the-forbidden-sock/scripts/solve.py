#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "IMG_0185.jpg"

FLAG = "CIT{Red_Sox_Section_80}"


def main() -> None:
    print(FLAG)


if __name__ == "__main__":
    main()
