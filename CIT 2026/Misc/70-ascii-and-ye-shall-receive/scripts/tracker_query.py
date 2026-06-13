#!/usr/bin/env python3
"""Query BitTorrent tracker directly via socket."""

import socket
import urllib.parse

HOST = "23.179.17.92"
PORT = 6969
INFO_HASH = bytes.fromhex("0651978ba96851b109d87edaff41133ef2f999f7")


def query_tracker() -> str:
    params = {
        "info_hash": INFO_HASH,
        "peer_id": b"-CC0001-000000000001",
        "port": 6881,
        "uploaded": 0,
        "downloaded": 0,
        "left": 1000,
        "compact": 1,
    }

    query = "&".join(
        f"{k}={urllib.parse.quote(v) if isinstance(v, bytes) else v}"
        for k, v in params.items()
    )

    request = f"GET /announce?{query} HTTP/1.0\r\nHost: {HOST}:{PORT}\r\n\r\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((HOST, PORT))
    sock.sendall(request.encode())

    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    sock.close()

    return response.decode("utf-8", errors="replace")


if __name__ == "__main__":
    print(query_tracker())
