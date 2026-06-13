#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "Pillow",
# ]
# ///
import base64
import pathlib

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "cool_car.png"
OUT_DIR = HERE.parent / "solution"


def main() -> None:
    img = Image.open(CHALLENGE).convert("RGBA")
    w, h = img.size
    alpha = img.split()[3]
    px = alpha.load()

    # LSB plane of the alpha channel — bit 0 set => white, clear => black.
    out = Image.new("1", (w, h))
    op = out.load()
    for y in range(h):
        for x in range(w):
            op[x, y] = 255 if (px[x, y] & 1) else 0

    out.save(OUT_DIR / "alpha_plane_0.png")

    # The centered text in that plane is base64; decode it to recover the flag.
    b64 = "Q0lUezRWdTF1MXpofQ=="
    flag = base64.b64decode(b64).decode()
    print(f"base64 (from image center): {b64}")
    print(f"flag: {flag}")


if __name__ == "__main__":
    main()
