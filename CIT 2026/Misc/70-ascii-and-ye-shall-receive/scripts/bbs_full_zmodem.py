#!/usr/bin/env python3
"""
Full BBS -> ZMODEM receive bridge.
Drives the BBS menu, then bridges the socket <-> `rz` subprocess so the
real ZMODEM transfer completes and any files land in OUT_DIR.
"""

from __future__ import annotations

import os
import select
import socket
import subprocess
import sys
import time

HOST = "23.179.17.92"
BBS_PORT = 2323

DEFAULT_OVERRIDE_PW = "x"
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "other", "zmodem_out"))


def drive_bbs(s: socket.socket, file_num: str, override_pw: str) -> None:
    """Walk the menu to the point where the server starts ZMODEM."""

    def recv_drain(sock: socket.socket, max_wait: float = 0.5) -> None:
        sock.settimeout(max_wait)
        try:
            while True:
                d = sock.recv(65536)
                if not d:
                    return
        except socket.timeout:
            return

    s.settimeout(2.0)
    time.sleep(0.5)
    recv_drain(s, 1.0)
    s.sendall(b"GUEST\r\n"); time.sleep(0.4); recv_drain(s, 0.5)
    s.sendall(b"\r\n"); time.sleep(0.4); recv_drain(s, 0.5)
    s.sendall(b"F\r\n"); time.sleep(0.8); recv_drain(s, 0.8)
    s.sendall(b"D\r\n"); time.sleep(0.5); recv_drain(s, 0.5)
    s.sendall(file_num.encode() + b"\r\n"); time.sleep(0.6); recv_drain(s, 0.6)
    # If file 4 is in the batch, BBS prompts for override password.
    tokens = file_num.split()
    if "4" in tokens:
        s.sendall(override_pw.encode() + b"\r\n")
        time.sleep(0.2)


def bridge(s: socket.socket, out_dir: str, idle_timeout: float = 6.0) -> None:
    """Bridge socket <-> rz subprocess. Exits when rz exits or idle."""
    os.makedirs(out_dir, exist_ok=True)
    rz = subprocess.Popen(
        ["rz", "-y", "--disable-timeout"],
        cwd=out_dir,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    s.setblocking(False)

    last_activity = time.time()
    try:
        while rz.poll() is None:
            fds = [s, rz.stdout]
            rlist, _, _ = select.select(fds, [], [], 1.0)
            if not rlist and time.time() - last_activity > idle_timeout:
                break
            if s in rlist:
                try:
                    data = s.recv(65536)
                except BlockingIOError:
                    data = b""
                if data == b"":
                    break
                rz.stdin.write(data)
                rz.stdin.flush()
                last_activity = time.time()
            if rz.stdout in rlist:
                data = rz.stdout.read1(65536)
                if not data:
                    break
                s.sendall(data)
                last_activity = time.time()
    finally:
        try:
            rz.stdin.close()
        except Exception:
            pass
        try:
            rz.terminate()
        except Exception:
            pass
        err = rz.stderr.read().decode("utf-8", "replace") if rz.stderr else ""
        if err.strip():
            print(f"[rz stderr]\n{err}", file=sys.stderr)


def run(file_num: str, override_pw: str, tag: str) -> None:
    out_dir = os.path.join(OUT_DIR, tag)
    os.makedirs(out_dir, exist_ok=True)
    s = socket.socket()
    s.settimeout(5)
    s.connect((HOST, BBS_PORT))
    try:
        drive_bbs(s, file_num, override_pw)
        bridge(s, out_dir)
    finally:
        s.close()

    print(f"[{tag}] files received:")
    for name in sorted(os.listdir(out_dir)):
        path = os.path.join(out_dir, name)
        size = os.path.getsize(path)
        print(f"  {name}  ({size} bytes)")


def main() -> None:
    file_num = sys.argv[1] if len(sys.argv) > 1 else "4"
    override_pw = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OVERRIDE_PW
    tag = sys.argv[3] if len(sys.argv) > 3 else f"f{file_num}_{int(time.time())}"
    run(file_num, override_pw, tag)


if __name__ == "__main__":
    main()
