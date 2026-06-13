# There's no room left — Writeup

- Category: Steganography
- Value: 770 pts
- Author: boom

## Challenge

It almost feels like the walls are closing in. Digitally, that is ;)

**SHA1:** `0f425ef58c8922ef1bad11929b317bc9d7b21a73`

## Recon

The provided `flag.txt` is a small text file, but its size is 855 bytes while only containing a short sentence:
> Another year, another steg challenge.. Something-something the flag is hidden in plain sight, but I'll leave it up to you to see if that really is true or not!

Inspecting the file reveals a large number of zero-width characters interspersed throughout the text. Specifically, the file contains:

- `U+200C` (Zero-Width Non-Joiner)
- `U+200D` (Zero-Width Joiner)
- `U+202C` (Pop Directional Formatting)
- `U+FEFF` (Zero-Width No-Break Space / BOM)

## Solve

The presence of exactly 4 distinct zero-width characters strongly suggests a base-4 encoding scheme. This specific combination of characters is the default alphabet used by the popular online tool [Unicode Steganography with Zero-Width Characters](https://330k.github.io/misc_tools/unicode_steganography.html) by Kei Misawa.

The tool encodes text by converting each 16-bit Unicode character into 8 base-4 digits, mapping them as follows:

- `0` ➔ `U+200C`
- `1` ➔ `U+200D`
- `2` ➔ `U+202C`
- `3` ➔ `U+FEFF`

We can extract all the zero-width characters from the file, group them into chunks of 8, and decode the base-4 values back into characters.

```bash
uv run scripts/solve.py
# flag: CIT{ok_maybe_not_plain_sight}
```

## Flag

```text
CIT{ok_maybe_not_plain_sight}
```

## Files

- [files/flag.txt](files/flag.txt) — the stego file containing zero-width characters
- [scripts/solve.py](scripts/solve.py) — script to extract and decode the zero-width characters
- [solution/flag.txt](solution/flag.txt) — the recovered flag
