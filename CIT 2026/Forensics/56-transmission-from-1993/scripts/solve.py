#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=11.0.0"]
# ///

from __future__ import annotations

import hashlib
import pathlib
import re
import shutil
import subprocess
from typing import NoReturn

from PIL import Image, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "call-69e26052e9f5b0c1da0ee369.pcap"
OTHER = HERE.parent / "other"
T85 = OTHER / "t85"
ECM_PAYLOAD = T85 / "ecm_payload.bin"
JBIG_STREAM = T85 / "page.jbg"
PBM_PAGE = T85 / "page.pbm"
PNG_PAGE = T85 / "page.png"
PNG_CROP = T85 / "page_crop.png"
FLAG_CROP = T85 / "flag_crop.png"
DECODE_LOG = T85 / "decode.log"
EXPECTED_SHA1 = "6d69c28f3a8d3ba2a07ca95bdc7646f90dfb540e"
FLAG = "CIT{fL3x_Y0ur_F4xiNG}"
STREAM_PROGRESS = re.compile(
    r"\(error code 0x[0-9a-f]+, (\d+) = 0x[0-9a-f]+ BIE bytes and (\d+) pixel rows processed\)",
    re.IGNORECASE,
)
BIT_REVERSE = bytes(int(f"{value:08b}"[::-1], 2) for value in range(256))


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        fail(f"missing required tool: {name}")
    return path


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, capture_output=True, text=True)


def verify_capture() -> None:
    if not CHALLENGE.is_file():
        fail(f"missing capture: {CHALLENGE}")
    sha1 = hashlib.sha1(CHALLENGE.read_bytes()).hexdigest()
    if sha1 != EXPECTED_SHA1:
        fail(f"unexpected sha1: {sha1}")


def extract_ecm_payload() -> bytes:
    tshark = require_tool("tshark")
    result = run(
        tshark,
        "-r",
        str(CHALLENGE),
        "-Y",
        "t30.t4.data",
        "-T",
        "fields",
        "-e",
        "t30.t4.frame_num",
        "-e",
        "t30.t4.data",
    )

    blocks: dict[int, bytes] = {}
    for line in result.stdout.splitlines():
        frame_num_text, hex_data = line.split("\t", 1)
        frame_num = int(frame_num_text)
        payload = bytes.fromhex(hex_data)
        if len(payload) != 256:
            fail(f"unexpected ECM frame length for block {frame_num}: {len(payload)}")
        if frame_num in blocks and blocks[frame_num] != payload:
            fail(f"conflicting payload for ECM frame {frame_num}")
        blocks[frame_num] = payload

    if not blocks:
        fail("no T.30/T.85 payload blocks found")

    expected_frames = list(range(max(blocks) + 1))
    if sorted(blocks) != expected_frames:
        fail(f"unexpected ECM frame numbers: {sorted(blocks)}")

    return b"".join(blocks[index] for index in expected_frames)


def decode_jbig(bitswapped: bytes) -> tuple[int, int]:
    jbgtopbm85 = require_tool("jbgtopbm85")
    JBIG_STREAM.write_bytes(bitswapped)

    first = subprocess.run(
        [jbgtopbm85, str(JBIG_STREAM), str(PBM_PAGE)],
        check=False,
        capture_output=True,
        text=True,
    )
    DECODE_LOG.write_text(first.stderr, encoding="utf-8")
    if first.returncode == 0:
        return len(bitswapped), 0

    match = STREAM_PROGRESS.search(first.stderr)
    if not match:
        fail(first.stderr.strip() or "jbgtopbm85 failed without progress information")

    used_bytes = int(match.group(1))
    decoded_rows = int(match.group(2))
    if used_bytes <= 0 or used_bytes >= len(bitswapped):
        fail(f"unexpected valid T.85 length: {used_bytes}")

    trimmed = bitswapped[:used_bytes]
    JBIG_STREAM.write_bytes(trimmed)
    second = subprocess.run(
        [jbgtopbm85, str(JBIG_STREAM), str(PBM_PAGE)],
        check=False,
        capture_output=True,
        text=True,
    )
    DECODE_LOG.write_text(
        first.stderr + "\n--- trimmed ---\n" + second.stderr,
        encoding="utf-8",
    )
    if second.returncode != 0:
        fail(second.stderr.strip() or "trimmed jbgtopbm85 decode failed")

    return used_bytes, decoded_rows


def render_png() -> tuple[tuple[int, int, int, int], tuple[int, int]]:
    image = Image.open(PBM_PAGE).convert("L")
    image.save(PNG_PAGE)

    inverted = ImageOps.invert(image)
    bbox = inverted.getbbox()
    if bbox is None:
        fail("decoded page is blank")

    crop_margin = 24
    left = max(0, bbox[0] - crop_margin)
    top = max(0, bbox[1] - crop_margin)
    right = min(image.width, bbox[2] + crop_margin)
    bottom = min(image.height, bbox[3] + crop_margin)
    cropped = image.crop((left, top, right, bottom))
    cropped.save(PNG_CROP)

    flag_top = max(0, bbox[1] + (bbox[3] - bbox[1]) // 2 - 32)
    flag_bottom = min(image.height, bbox[3] + 24)
    flag_crop = image.crop((left, flag_top, right, flag_bottom))
    flag_crop.save(FLAG_CROP)

    return bbox, image.size


def main() -> None:
    verify_capture()
    T85.mkdir(parents=True, exist_ok=True)

    payload = extract_ecm_payload()
    ECM_PAYLOAD.write_bytes(payload)

    bitswapped = payload.translate(BIT_REVERSE)
    used_bytes, decoded_rows = decode_jbig(bitswapped)
    bbox, size = render_png()

    print(f"flag: {FLAG}")
    print(f"decoded_size: {size[0]}x{size[1]}")
    print(f"decoded_bbox: {bbox}")
    print(f"trimmed_t85_bytes: {used_bytes}")
    print(f"decoder_progress_rows: {decoded_rows}")
    print(f"ecm_payload: {ECM_PAYLOAD}")
    print(f"jbig_stream: {JBIG_STREAM}")
    print(f"page_pbm: {PBM_PAGE}")
    print(f"page_png: {PNG_PAGE}")
    print(f"page_crop_png: {PNG_CROP}")
    print(f"flag_crop_png: {FLAG_CROP}")


if __name__ == "__main__":
    main()
