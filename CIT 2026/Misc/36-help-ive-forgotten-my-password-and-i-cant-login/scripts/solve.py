#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pycryptodome",
# ]
# ///

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import hmac
import json
import pathlib
import sys
import xml.etree.ElementTree as ET

from Crypto.Cipher import AES, ChaCha20, Salsa20

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "Database.kdbx"
SALSA20_IV = bytes.fromhex("e830094b97205d2a")

OUTER_CIPHER_AES256_CBC = bytes.fromhex("31c1f2e6bf714350be5805216afc5aff")
KDF_AES = bytes.fromhex("c9d9f39a628a4460bf740d08c18a4fea")


class KeePassError(RuntimeError):
    pass


def parse_variant_dictionary(data: bytes) -> dict[str, bytes]:
    index = 2
    values: dict[str, bytes] = {}
    while index < len(data):
        value_type = data[index]
        index += 1
        if value_type == 0:
            break
        name_len = int.from_bytes(data[index : index + 4], "little")
        index += 4
        name = data[index : index + name_len].decode()
        index += name_len
        value_len = int.from_bytes(data[index : index + 4], "little")
        index += 4
        value = data[index : index + value_len]
        index += value_len
        values[name] = value
    return values


def parse_kdbx4_header(data: bytes) -> dict[str, object]:
    if data[:8] != bytes.fromhex("03d9a29a67fb4bb5"):
        raise KeePassError("unexpected file signature")
    if int.from_bytes(data[10:12], "little") != 4:
        raise KeePassError("expected KDBX4")

    fields: dict[int, list[bytes]] = {}
    index = 12
    while True:
        field_id = data[index]
        field_len = int.from_bytes(data[index + 1 : index + 5], "little")
        value = data[index + 5 : index + 5 + field_len]
        index += 5 + field_len
        fields.setdefault(field_id, []).append(value)
        if field_id == 0:
            break

    header = data[:index]
    stored_header_sha256 = data[index : index + 32]
    header_hmac = data[index + 32 : index + 64]
    payload = data[index + 64 :]

    calc_header_sha256 = hashlib.sha256(header).digest()
    if calc_header_sha256 != stored_header_sha256:
        raise KeePassError("header SHA256 mismatch")

    outer_cipher = fields[2][0]
    if outer_cipher != OUTER_CIPHER_AES256_CBC:
        raise KeePassError("unsupported outer cipher")

    compression_flags = int.from_bytes(fields[3][0], "little")
    master_seed = fields[4][0]
    kdf_params = parse_variant_dictionary(fields[11][0])
    kdf_uuid = kdf_params["$UUID"]
    if kdf_uuid != KDF_AES:
        raise KeePassError("unsupported KDF")

    return {
        "header": header,
        "header_hmac": header_hmac,
        "payload": payload,
        "compression_flags": compression_flags,
        "master_seed": master_seed,
        "kdf_seed": kdf_params["S"],
        "kdf_rounds": int.from_bytes(kdf_params["R"], "little"),
        "encryption_iv": fields[7][0],
    }


def derive_keys(password: str, header_info: dict[str, object]) -> tuple[bytes, bytes]:
    composite = hashlib.sha256(password.encode()).digest()
    composite = hashlib.sha256(composite).digest()

    cipher = AES.new(header_info["kdf_seed"], AES.MODE_ECB)
    transformed = composite
    for _ in range(header_info["kdf_rounds"]):
        transformed = cipher.encrypt(transformed)
    transformed = hashlib.sha256(transformed).digest()

    master_key = hashlib.sha256(header_info["master_seed"] + transformed).digest()
    hmac_base_key = hashlib.sha512(
        header_info["master_seed"] + transformed + b"\x01",
    ).digest()
    return master_key, hmac_base_key


def derive_hmac_key(index: int, hmac_base_key: bytes) -> bytes:
    return hashlib.sha512(
        index.to_bytes(8, "little", signed=False) + hmac_base_key,
    ).digest()


def validate_password(
    password: str,
    header_info: dict[str, object],
) -> tuple[bool, bytes | None, bytes | None]:
    master_key, hmac_base_key = derive_keys(password, header_info)
    header_hmac_key = derive_hmac_key(0xFFFFFFFFFFFFFFFF, hmac_base_key)
    valid = (
        hmac.new(header_hmac_key, header_info["header"], hashlib.sha256).digest()
        == header_info["header_hmac"]
    )
    if not valid:
        return False, None, None
    return True, master_key, hmac_base_key


def collect_encrypted_payload(payload: bytes, hmac_base_key: bytes) -> bytes:
    index = 0
    block_number = 0
    chunks: list[bytes] = []

    while index < len(payload):
        block_hmac = payload[index : index + 32]
        index += 32
        block_len = int.from_bytes(payload[index : index + 4], "little")
        index += 4
        block = payload[index : index + block_len]
        index += block_len

        hmac_key = derive_hmac_key(block_number, hmac_base_key)
        block_message = (
            block_number.to_bytes(8, "little") + block_len.to_bytes(4, "little") + block
        )
        calc_hmac = hmac.new(hmac_key, block_message, hashlib.sha256).digest()
        if calc_hmac != block_hmac:
            raise KeePassError(f"block HMAC mismatch at block {block_number}")

        if block_len == 0:
            break
        chunks.append(block)
        block_number += 1

    return b"".join(chunks)


def decrypt_outer_payload(
    master_key: bytes,
    header_info: dict[str, object],
    encrypted_payload: bytes,
) -> bytes:
    cipher = AES.new(master_key, AES.MODE_CBC, header_info["encryption_iv"])
    decrypted = cipher.decrypt(encrypted_payload)
    pad_len = decrypted[-1]
    if not 1 <= pad_len <= 16:
        raise KeePassError("invalid PKCS7 padding")
    if decrypted[-pad_len:] != bytes([pad_len]) * pad_len:
        raise KeePassError("invalid PKCS7 padding bytes")
    decrypted = decrypted[:-pad_len]

    if header_info["compression_flags"] == 1:
        decrypted = gzip.decompress(decrypted)
    return decrypted


def parse_inner_header(data: bytes) -> tuple[int, bytes, bytes]:
    index = 0
    stream_id = 0
    stream_key = b""
    while True:
        field_id = data[index]
        field_len = int.from_bytes(data[index + 1 : index + 5], "little")
        value = data[index + 5 : index + 5 + field_len]
        index += 5 + field_len
        if field_id == 0:
            break
        if field_id == 1:
            stream_id = int.from_bytes(value, "little")
        elif field_id == 2:
            stream_key = value
    if not stream_key:
        raise KeePassError("missing inner stream key")
    return stream_id, stream_key, data[index:]


def build_stream_cipher(stream_id: int, stream_key: bytes):
    if stream_id == 2:
        return Salsa20.new(key=hashlib.sha256(stream_key).digest(), nonce=SALSA20_IV)
    if stream_id == 3:
        digest = hashlib.sha512(stream_key).digest()
        return ChaCha20.new(key=digest[:32], nonce=digest[32:44])
    raise KeePassError(f"unsupported inner stream id {stream_id}")


def decrypt_protected_values(
    xml_bytes: bytes,
    stream_id: int,
    stream_key: bytes,
) -> ET.Element:
    root = ET.fromstring(xml_bytes)
    cipher = build_stream_cipher(stream_id, stream_key)
    for value in root.iter("Value"):
        if value.attrib.get("Protected") != "True":
            continue
        encrypted = base64.b64decode(value.text or "")
        plaintext = cipher.decrypt(encrypted)
        value.text = plaintext.decode("utf-8", errors="replace")
        value.attrib.pop("Protected", None)
    return root


def extract_entries(root: ET.Element) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for entry in root.iter("Entry"):
        item: dict[str, str] = {}
        for string_node in entry.findall("String"):
            key_node = string_node.find("Key")
            value_node = string_node.find("Value")
            if key_node is None or value_node is None:
                continue
            item[key_node.text or ""] = value_node.text or ""
        if item:
            entries.append(item)
    return entries


def decrypt_database(
    password: str,
    db_path: pathlib.Path,
) -> tuple[ET.Element, list[dict[str, str]]]:
    header_info = parse_kdbx4_header(db_path.read_bytes())
    valid, master_key, hmac_base_key = validate_password(password, header_info)
    if not valid:
        raise KeePassError("password did not validate")

    encrypted_payload = collect_encrypted_payload(header_info["payload"], hmac_base_key)
    inner_payload = decrypt_outer_payload(master_key, header_info, encrypted_payload)
    stream_id, stream_key, xml_bytes = parse_inner_header(inner_payload)
    root = decrypt_protected_values(xml_bytes, stream_id, stream_key)
    return root, extract_entries(root)


def iter_passwords(args: argparse.Namespace):
    if args.password is not None:
        yield args.password
    if args.password_file is not None:
        for line in args.password_file.read_text().splitlines():
            candidate = line.rstrip("\n")
            if candidate:
                yield candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=pathlib.Path, default=CHALLENGE)
    parser.add_argument("--password")
    parser.add_argument("--password-file", type=pathlib.Path)
    parser.add_argument("--xml-out", type=pathlib.Path)
    parser.add_argument("--json-out", type=pathlib.Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.password is None and args.password_file is None:
        raise SystemExit("provide --password or --password-file")

    matched_password: str | None = None
    root: ET.Element | None = None
    entries: list[dict[str, str]] | None = None

    for candidate in iter_passwords(args):
        try:
            root, entries = decrypt_database(candidate, args.db)
            matched_password = candidate
            break
        except KeePassError:
            continue

    if matched_password is None or root is None or entries is None:
        print("no matching password found", file=sys.stderr)
        raise SystemExit(1)

    print(matched_password, file=sys.stderr)

    xml_text = ET.tostring(root, encoding="unicode")
    if args.xml_out is not None:
        args.xml_out.write_text(xml_text)
    if args.json_out is not None:
        args.json_out.write_text(json.dumps(entries, indent=2))

    print(json.dumps(entries, indent=2))


if __name__ == "__main__":
    main()
