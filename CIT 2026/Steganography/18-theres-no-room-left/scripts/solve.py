#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "flag.txt"


def main() -> None:
    data = CHALLENGE.read_text(encoding="utf-8")

    # The tool uses 4 zero-width characters for base-4 encoding
    # U+200C -> 0, U+200D -> 1, U+202C -> 2, U+FEFF -> 3
    chars = ["\u200c", "\u200d", "\u202c", "\ufeff"]

    # Extract only the zero-width characters
    hidden = "".join(c for c in data if c in chars)

    # Text decode: 8 zero-width characters per 16-bit Unicode character
    res_text = ""
    for i in range(0, len(hidden), 8):
        chunk = hidden[i : i + 8]
        if len(chunk) == 8:
            val = 0
            for c in chunk:
                val = val * 4 + chars.index(c)
            res_text += chr(val)

    print(f"flag: {res_text}")


if __name__ == "__main__":
    main()
