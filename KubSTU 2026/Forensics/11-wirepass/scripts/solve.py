#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pyzipper",
# ]
# ///

import io
import pathlib
import re
import struct
import subprocess

import pyzipper

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "11_challenge.pcap"


def tshark_field(display_filter: str, field: str) -> list[str]:
    cmd = [
        "tshark",
        "-r",
        str(CHALLENGE),
        "-Y",
        display_filter,
        "-T",
        "fields",
        "-e",
        field,
    ]
    out = subprocess.check_output(cmd, text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def rotate(data: bytes, offset: int) -> bytes:
    return data[offset:] + data[:offset]


def xor_with_key(data: bytes, key: bytes) -> bytes:
    return bytes(byte ^ key[index % len(key)] for index, byte in enumerate(data))


def decrypt_slice(
    body: bytes,
    nonce: bytes,
    start: int,
    end: int,
    rotation: int,
) -> bytes:
    return xor_with_key(body[start:end], rotate(nonce, rotation))


def find_rotation(body: bytes, nonce: bytes, offset: int, signature: bytes) -> int:
    for rotation in range(len(nonce)):
        candidate = decrypt_slice(
            body,
            nonce,
            offset,
            offset + len(signature),
            rotation,
        )
        if candidate == signature:
            return rotation
    raise ValueError(f"no rotation matched {signature!r} at offset {offset}")


def load_password() -> str:
    payloads = tshark_field("tcp.dstport == 9999 && tcp.len > 0", "tcp.payload")
    for payload in payloads:
        line = bytes.fromhex(payload).decode("ascii", errors="strict")
        if line.startswith("PASS:"):
            return line.split(":", 1)[1].strip()
    raise ValueError("password leak not found")


def load_transfer() -> tuple[bytes, bytes]:
    payloads = tshark_field("tcp.dstport == 31337 && tcp.len > 0", "tcp.payload")
    blob = bytes.fromhex("".join(payloads))
    header = blob[:24]
    body = blob[24:]
    expected_size = int.from_bytes(header[-4:], "big")
    if expected_size != len(body):
        raise ValueError(f"size mismatch: {expected_size} != {len(body)}")
    return header, body


def parse_tail(body: bytes, nonce: bytes) -> tuple[int, int, int]:
    tail_size = 256
    tail_start = len(body) - tail_size
    tail = body[tail_start:]
    for rotation in range(len(nonce)):
        plain = xor_with_key(tail, rotate(nonce, rotation))
        eocd_index = plain.find(b"PK\x05\x06")
        if eocd_index == -1:
            continue
        eocd = plain[eocd_index : eocd_index + 22]
        if len(eocd) < 22:
            continue
        (
            signature,
            disk_no,
            cd_disk,
            disk_entries,
            total_entries,
            cd_size,
            cd_offset,
            comment_len,
        ) = struct.unpack(
            "<IHHHHIIH",
            eocd,
        )
        if signature != 0x06054B50:
            continue
        if comment_len != 0:
            continue
        if cd_offset + cd_size + 22 != len(body):
            continue
        return rotation, cd_offset, cd_size
    raise ValueError("could not parse encrypted ZIP tail")


def parse_central_directory(
    archive: bytes,
    cd_offset: int,
    cd_size: int,
) -> list[tuple[str, int]]:
    entries: list[tuple[str, int]] = []
    cursor = cd_offset
    end = cd_offset + cd_size
    while cursor < end:
        header = archive[cursor : cursor + 46]
        (
            signature,
            _ver_made,
            _ver_need,
            _flags,
            _method,
            _mtime,
            _mdate,
            _crc,
            _csize,
            _usize,
            name_len,
            extra_len,
            comment_len,
            _disk,
            _iattr,
            _eattr,
            local_offset,
        ) = struct.unpack("<IHHHHHHIIIHHHHHII", header)
        if signature != 0x02014B50:
            raise ValueError(f"bad central directory signature at {cursor}")
        name_start = cursor + 46
        name_end = name_start + name_len
        name = archive[name_start:name_end].decode("utf-8")
        entries.append((name, local_offset))
        cursor = name_end + extra_len + comment_len
    return entries


def rebuild_archive(body: bytes, nonce: bytes) -> bytes:
    archive = bytearray(len(body))

    tail_rotation, cd_offset, cd_size = parse_tail(body, nonce)
    cd_rotation = find_rotation(body, nonce, cd_offset, b"PK\x01\x02")
    cd_plain = decrypt_slice(body, nonce, cd_offset, cd_offset + cd_size, cd_rotation)
    archive[cd_offset : cd_offset + cd_size] = cd_plain

    eocd_offset = cd_offset + cd_size
    eocd_rotation = find_rotation(body, nonce, eocd_offset, b"PK\x05\x06")
    archive[eocd_offset:] = decrypt_slice(
        body,
        nonce,
        eocd_offset,
        len(body),
        eocd_rotation,
    )

    entries = parse_central_directory(bytes(archive), cd_offset, cd_size)
    offsets = [offset for _, offset in entries] + [cd_offset]
    for index, start in enumerate(offsets[:-1]):
        end = offsets[index + 1]
        rotation = find_rotation(body, nonce, start, b"PK\x03\x04")
        archive[start:end] = decrypt_slice(body, nonce, start, end, rotation)

    if bytes(archive[:4]) != b"PK\x03\x04":
        raise ValueError("failed to rebuild local file headers")
    if bytes(archive[cd_offset : cd_offset + 4]) != b"PK\x01\x02":
        raise ValueError("failed to rebuild central directory")
    if bytes(archive[eocd_offset : eocd_offset + 4]) != b"PK\x05\x06":
        raise ValueError("failed to rebuild EOCD")

    return bytes(archive)


def extract_flag(archive: bytes, password: str) -> str:
    with pyzipper.AESZipFile(io.BytesIO(archive)) as zf:
        zf.setpassword(password.encode())
        for name in zf.namelist():
            data = zf.read(name).decode("utf-8", errors="replace")
            match = re.search(r"KubSTU\{[^}]+\}", data)
            if match:
                return match.group(0)
    raise ValueError("flag not found")


def main() -> None:
    password = load_password()
    header, body = load_transfer()
    nonce = header[4:20]
    archive = rebuild_archive(body, nonce)
    flag = extract_flag(archive, password)
    print(flag)


if __name__ == "__main__":
    main()
