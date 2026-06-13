#!/usr/bin/env python3
"""Car Crash — CIT 2026 Steganography (22, 980 pts)

The PNG hides 6 tEXt chunks that look like base64 decoys (red herrings).
The real payload lives in the bit-0 (LSB) planes of the RGBA channels.
XORing the G and A LSB planes and rendering the result as a 1-bit image
makes a base64 string visible to the eye:

    Q0lUezdFM3FVNHdFfQ==  ->  CIT{7E3qU4wE}

Other channel XORs (R, B, RGBA, ...) produce visibly noisy planes; only
G XOR A cancels the carrier noise enough to expose the rendered text.
"""

import base64
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent.parent
SRC = HERE / "files" / "car_crash.png"
OUT = HERE / "files" / "extractions" / "ga_xor.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC)
w, h = img.size
px = list(img.getdata())

# Bit 0 (LSB) of Green XOR Bit 0 of Alpha, rendered as 1-bit image
out = Image.new("L", (w, h))
out.putdata([((p[1] ^ p[3]) & 1) * 255 for p in px])
out.save(OUT)
print(f"wrote {OUT}")

# The base64 token visible in that image:
token = "Q0lUezdFM3FVNHdFfQ=="
print(f"token:  {token}")
print(f"flag:   {base64.b64decode(token).decode()}")
