#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pycryptodome"]
# ///
import pathlib
import re
from math import gcd

HERE = pathlib.Path(__file__).resolve().parent


def parinad(n: int) -> int:
    return bin(n)[2:].count("1") % 2


def main() -> None:
    with open("/tmp/vinad_tmp/output.txt") as f:
        content = f.read()

    r_match = re.search(r"R = \[(.*?)\]", content, re.DOTALL)
    R = [int(x.strip()) for x in r_match.group(1).split(",") if x.strip()]

    n = int(re.search(r"n = (\d+)", content).group(1))
    c = int(re.search(r"c = (\d+)", content).group(1))

    nbit = 512

    a = [parinad(ri) for ri in R]
    A = int("".join(str(ai) for ai in a), 2)
    A_comp = A ^ ((1 << nbit) - 1)

    full_mask = (1 << nbit) - 1
    sR = sum(R)

    for label, p in [("A", A), ("~A", A_comp)]:
        if n % p == 0:
            q = n // p
            print(f"Found p ({label})")
            phi = (p - 1) * (q - 1)

            for mask_val in (0, full_mask):
                e_cand = p ^ mask_val
                if gcd(e_cand, phi) == 1:
                    d = pow(e_cand, -1, phi)
                    m_shifted = pow(c, d, n)
                    m = (m_shifted - sR) % n
                    try:
                        flag = m.to_bytes((m.bit_length() + 7) // 8, "big")
                        print(f"Flag: {flag}")
                        flag_file = HERE.parent / "solution" / "flag.txt"
                        flag_file.write_text(flag.decode(errors="replace").strip())
                    except Exception as ex:
                        print(f"Decode error with mask={mask_val}: {ex}")
                    return

    print("Failed to factor n")


if __name__ == "__main__":
    main()
