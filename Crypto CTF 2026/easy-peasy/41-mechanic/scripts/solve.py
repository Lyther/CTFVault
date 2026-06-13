#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "kyber-py",
#   "quantcrypt",
# ]
# ///
"""
Mechanic solver.

The server encrypts the flag.png iteratively with ML-KEM-1024 (KryptonKEM).
For each bit of a random 40-bit number `m` it writes a 3168-byte secret key to
`output.raw`.  If the bit is `1` the key is real and encrypts the current
plaintext to `flag_{c}.enc`; if the bit is `0` the key is random.

We are given `flag_22.enc`, so we must decrypt the chain back to `flag.png`.
There are 22 real keys among the 40 blocks in `output.raw`; we identify them by
trying each block's secret key until the KryptonKEM MAC verifies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from kyber_py.ml_kem import ML_KEM_1024
from quantcrypt.internal import constants as const
from quantcrypt.internal.cipher.krypton import Krypton
from quantcrypt.internal.kdf.argon2_kdf import Argon2
from quantcrypt.internal.kdf.common import KDFParams, MemCost

SK_SIZE = 3168
CT_SIZE = 1568


def _kdf_params() -> KDFParams:
    return KDFParams(
        memory_cost=MemCost.GB(1),
        parallelism=8,
        time_cost=1,
        hash_len=64,
        salt_len=32,
    )


def parse_krypton_header(data: bytes) -> tuple[int, bytes, bytes, bytes, int]:
    """Return chunk_size, vdp, header, salt, kem_ct from a KryptonKEM file."""
    h_len = int(data[:10].decode("utf-8"))
    chunk_size = int(data[10:20].decode("utf-8"))
    vdp = data[20:180]
    header = data[180 : 180 + h_len]
    fn_len = int(header[:4].decode("utf-8"))
    salt = header[4 + fn_len : 4 + fn_len + 32]
    kem_ct = header[4 + fn_len + 32 :]
    if len(kem_ct) != CT_SIZE:
        raise ValueError(f"unexpected KEM ciphertext size: {len(kem_ct)}")
    return chunk_size, vdp, header, salt, kem_ct


def try_decrypt_step(
    enc_path: Path,
    out_path: Path,
    blocks: dict[int, bytes],
    allowed: set[int] | None = None,
) -> int | None:
    """Decrypt *enc_path* to *out_path* using one of the secret key blocks.

    Returns the index of the block that succeeded, or None if no block works.
    """
    data = enc_path.read_bytes()
    chunk_size, vdp, header, salt, kem_ct = parse_krypton_header(data)
    h_len = len(header)
    context = const.KDFContext
    params = _kdf_params()

    candidates = allowed if allowed is not None else set(blocks.keys())
    for idx in candidates:
        sk = blocks[idx]
        try:
            ss = ML_KEM_1024.decaps(sk, kem_ct)
        except Exception:
            continue
        argon = Argon2.Key(params=params, public_salt=salt, password=ss)
        kf = Krypton(argon.secret_key, context, None)
        setattr(kf, "_chunk_size", chunk_size)
        try:
            kf.begin_decryption(vdp, header)
        except Exception:
            continue

        out_path.write_bytes(b"")
        offset = 180 + h_len
        with open(enc_path, "rb") as rf, open(out_path, "wb") as wf:
            rf.seek(offset)
            while True:
                chunk = rf.read(chunk_size + 1)
                if not chunk:
                    break
                wf.write(kf.decrypt(chunk))
        kf.finish_decryption()
        return idx
    return None


def solve(files_dir: Path, out_dir: Path) -> bytes:
    """Decrypt the chain and return the final flag.png bytes."""
    raw = (files_dir / "output.raw").read_bytes()
    if len(raw) % SK_SIZE != 0:
        raise ValueError("output.raw length is not a multiple of SK_SIZE")

    blocks = {i: raw[i * SK_SIZE : (i + 1) * SK_SIZE] for i in range(len(raw) // SK_SIZE)}
    remaining: set[int] = set(blocks.keys())

    current = files_dir / "flag_22.enc"
    if not current.is_file():
        raise FileNotFoundError(current)

    for step in range(len(blocks)):
        data = current.read_bytes()
        h_len = int(data[:10].decode("utf-8"))
        header = data[180 : 180 + h_len]
        fn_len = int(header[:4].decode("utf-8"))
        out_name = header[4 : 4 + fn_len].decode("utf-8")
        out_path = out_dir / out_name

        block_idx = try_decrypt_step(current, out_path, blocks, remaining)
        if block_idx is None:
            raise RuntimeError(f"no key found to decrypt {current.name}")
        remaining.remove(block_idx)

        if out_name == "flag.png":
            return out_path.read_bytes()
        current = out_path

    raise RuntimeError("chain did not reach flag.png")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mechanic solver")
    parser.add_argument(
        "--files",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "files",
        help="directory containing output.raw and flag_22.enc",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "solution",
        help="directory to write decrypted files",
    )
    args = parser.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)
    flag_bytes = solve(args.files, args.out)
    print(f"Wrote flag.png ({len(flag_bytes)} bytes) to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
