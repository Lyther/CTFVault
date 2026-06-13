#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "6_strange_sequence_of_numbers.txt"


def main() -> None:
    numbers = CHALLENGE.read_text(encoding="ascii").split()
    flag = "".join(chr(int(number)) for number in numbers)
    print(flag)


if __name__ == "__main__":
    main()
