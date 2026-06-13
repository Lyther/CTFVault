#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import re
import socket
import sys
import time

HOST = "23.179.17.92"
PORT = 5670

HEX_BYTE_RE = re.compile(r"\b[0-9A-F]{2}\b")
FLAG_RE = re.compile(r"^CIT\{[A-Za-z0-9_@$!+\-]+\}$")


def recv_until_prompt(sock: socket.socket, timeout: float = 1.5) -> str:
    sock.settimeout(timeout)
    data = b""
    while True:
        try:
            chunk = sock.recv(4096)
        except TimeoutError:
            break
        if not chunk:
            break
        data += chunk
        if data.endswith(b">"):
            break
    return data.decode("utf-8", "replace")


def send_command(sock: socket.socket, command: str, delay: float = 0.2) -> str:
    sock.sendall((command + "\r").encode("ascii"))
    time.sleep(delay)
    return recv_until_prompt(sock)


def parse_hex_bytes(response: str) -> list[int]:
    data: list[int] = []
    for raw_line in response.replace("\r", "\n").splitlines():
        line = raw_line.strip().upper()
        if not line or line == ">":
            continue
        if ":" in line:
            _, payload = line.split(":", 1)
            hex_text = re.sub(r"[^0-9A-F]", "", payload)
            if len(hex_text) % 2 == 1:
                hex_text = hex_text[:-1]
            data.extend(
                int(hex_text[index : index + 2], 16)
                for index in range(0, len(hex_text), 2)
            )
            continue
        if re.fullmatch(r"[0-9A-F]{2}(?: [0-9A-F]{2})*", line):
            for token in HEX_BYTE_RE.findall(line):
                data.append(int(token, 16))
    return data


def parse_flag(response: str) -> str:
    data = parse_hex_bytes(response)
    start = -1
    for index in range(len(data) - 2):
        if data[index : index + 3] == [0x62, 0xF1, 0xA5]:
            start = index
            break
    if start < 0:
        raise RuntimeError(f"unexpected DID response: {response!r}")
    flag = bytes(data[start + 3 :]).decode("ascii")
    if not FLAG_RE.match(flag):
        raise RuntimeError(f"unexpected flag format: {flag!r}")
    return flag


def main() -> None:
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        time.sleep(0.2)
        recv_until_prompt(sock, 1.0)
        send_command(sock, "ATZ")
        send_command(sock, "ATE0")
        send_command(sock, "ATH1")
        send_command(sock, "ATS0")
        send_command(sock, "ATL0")
        send_command(sock, "ATSP6")
        send_command(sock, "ATSH7E0")
        did = send_command(sock, "22F1A5")
    print(parse_flag(did))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise
