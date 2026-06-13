#!/usr/bin/env python3
import re
import socket


def recv_until(s: socket.socket, marker: bytes) -> bytes:
    buf = b""
    while marker not in buf:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk
    return buf


def main(host: str = "133.88.122.244", port: int = 32007) -> None:
    s = socket.create_connection((host, port))

    head = recv_until(s, b"Enter your boring 'favorite' (Hex): ")
    iv_hex = re.search(r"exciting_iv I used!:\s*([0-9a-f]+)", head.decode()).group(1)
    enc_flag_hex = re.search(r"=>\s*([0-9a-f]+)", head.decode()).group(1)
    iv = bytes.fromhex(iv_hex)
    enc_flag = bytes.fromhex(enc_flag_hex)
    print(f"[+] iv       : {iv.hex()}  ({len(iv)} bytes)")
    print(f"[+] enc_flag : {enc_flag.hex()}  ({len(enc_flag)} bytes)")

    favorite = b"\x00" * len(enc_flag)
    s.sendall(favorite.hex().encode() + b"\n")

    recv_until(s, b"Enter your own 'very_exciting' IV (Hex): ")
    s.sendall(iv.hex().encode() + b"\n")

    tail = recv_until(s, b"Enjoy!")
    enc_fav_hex = re.search(
        r"completely EXCITED!!\s*=>\s*([0-9a-f]+)",
        tail.decode(),
    ).group(1)
    keystream = bytes.fromhex(enc_fav_hex)
    print(f"[+] keystream: {keystream.hex()}")

    flag = bytes(a ^ b for a, b in zip(enc_flag, keystream))
    print(f"[+] FLAG     : {flag.decode()}")

    s.close()


if __name__ == "__main__":
    main()
