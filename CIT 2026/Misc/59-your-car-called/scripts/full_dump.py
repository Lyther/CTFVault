#!/usr/bin/env python3
"""Interactive dump of the ELM327 emulator at 23.179.17.92:5670.
Run from a host with unrestricted outbound TCP (local machine is fine once the
challenge IP is reachable; we used the VPS since corporate networks blocked it)."""

import socket
import time

HOST, PORT = "23.179.17.92", 5670


def recv_until_prompt(s, timeout=1.5):
    s.settimeout(timeout)
    d = b""
    while True:
        try:
            b = s.recv(4096)
            if not b:
                break
            d += b
            if b.endswith(b">"):
                break
        except Exception:
            break
    return d


def send(s, cmd, delay=0.25):
    s.sendall((cmd + "\r").encode())
    time.sleep(delay)
    return recv_until_prompt(s).decode(errors="replace")


def main():
    s = socket.socket()
    s.settimeout(10)
    s.connect((HOST, PORT))
    time.sleep(0.3)
    # read banner
    banner = recv_until_prompt(s, 1.0).decode(errors="replace")
    print("=== banner ===")
    print(repr(banner))
    print("=== reset + echo off ===")
    print(repr(send(s, "ATZ")))
    print(repr(send(s, "ATE0")))
    print("=== identifiers / protocol ===")
    for c in [
        "ATI",
        "AT@1",
        "AT@2",
        "AT@3",
        "ATDP",
        "ATDPN",
        "ATRV",
        "ATBI",
        "ATST",
        "ATWS",
    ]:
        print(f"{c}: {send(s, c)!r}")
    print("=== mode 01 supported PIDs + working PIDs ===")
    for p in [0x00, 0x01, 0x05, 0x0C, 0x0D, 0x11, 0x20, 0x21, 0x40]:
        print(f"01{p:02X}: {send(s, f'01{p:02X}')!r}")
    print("=== mode 03 (DTCs) ===")
    print(send(s, "03"))
    print("=== mode 04 (clear) ===")
    print(send(s, "04"))
    print("=== mode 09 VIN ===")
    print(send(s, "0902"))
    print("=== hidden DID ===")
    for c in ["ATH1", "ATS0", "ATL0", "ATSP6", "ATSH7E0", "22F1A5"]:
        print(f"{c}: {send(s, c)!r}")
    s.close()


if __name__ == "__main__":
    main()
