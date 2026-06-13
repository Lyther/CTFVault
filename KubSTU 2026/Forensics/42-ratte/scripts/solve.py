#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "42_Ratte.pcap"


def tshark_payloads() -> list[bytes]:
    cmd = [
        "tshark",
        "-r",
        str(CHALLENGE),
        "-Y",
        "tcp.port == 1337 && tcp.len > 0",
        "-T",
        "fields",
        "-e",
        "tcp.payload",
    ]
    out = subprocess.check_output(cmd, text=True)
    return [bytes.fromhex(line.strip()) for line in out.splitlines() if line.strip()]


def extract_flag() -> str:
    payloads = tshark_payloads()
    if not payloads:
        raise ValueError("no payloads found on tcp/1337")
    marker = payloads[0]
    if not marker.startswith(bytes.fromhex("deadbeef")):
        raise ValueError(f"unexpected marker packet: {marker.hex()}")
    key = marker[-1]

    chunks: list[bytes] = []
    for payload in payloads[1:]:
        if len(payload) < 3 or payload[0] != 0xCC:
            raise ValueError(f"unexpected data packet: {payload.hex()}")
        size = payload[2]
        data = payload[3 : 3 + size]
        if len(data) != size:
            raise ValueError(f"truncated data packet: {payload.hex()}")
        chunks.append(bytes(byte ^ key for byte in data))

    flag = b"".join(chunks).decode("utf-8")
    if not re.fullmatch(r"KubSTU\{[^}]+\}", flag):
        raise ValueError(f"unexpected flag format: {flag!r}")
    return flag


def main() -> None:
    print(extract_flag())


if __name__ == "__main__":
    main()
