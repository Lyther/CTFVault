#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Farcical Clones.

Cipher = 25 * clone + core_letter, where `clone` is a random decimal
digit 0..9 ("farcical clone") and `core_letter` is the letter index
in the 25-letter Latin alphabet (no J). Only `core_letter` carries
plaintext; `clone` is a distractor that inflates each letter to
look like a random byte.

On the letter cores the cipher is a Beaufort OTP:

    core = (K - P) mod 25   =>   K = (core + P) mod 25
    P    = (K - core) mod 25

Key length equals plaintext length (55), so there is no keystream
to recover — only the crib + the inferred body wording give P.
"""

from __future__ import annotations

ALPHA = "abcdefghiklmnopqrstuvwxyz"  # 25 letters, J folded into I

CT_PREFIX = [
    95,
    181,
    145,
    39,
    245,
    91,
    212,
    232,
    123,
    220,
    167,
    69,
    91,
    208,
    245,
    164,
    245,
    145,
    123,
    94,
    62,
    150,
    94,
    172,
    83,
    135,
    96,
    153,
    2,
    208,
    96,
    172,
    201,
    5,
    19,
]

FLAG_CT = [
    131,
    91,
    90,
    53,
    95,
    218,
    238,
    211,
    91,
    4,
    201,
    182,
    135,
    245,
    167,
    74,
    90,
    145,
    96,
    238,
]

# Intro crib (spaces/punctuation not encrypted). J folds to I.
CRIB_PREFIX = ("MaytheForcebewithyou" + "youngpadawan" + "CIT").replace("J", "I")
# Body wording guessed from partial crib + two symbol repetitions
# (090 twice, 238 twice) + the challenge title pointing at Sifo-Dyas.
CRIB_BODY = "JediMasterCipherDyas"
CRIB_BODY_25 = CRIB_BODY.replace("J", "I")


def _core(n: int) -> int:
    return n % 25


def derive_key(ct: list[int], pt: str) -> str:
    """Beaufort key from cipher cores + plaintext."""
    return "".join(
        ALPHA[(_core(c) + ALPHA.index(p.lower())) % 25] for c, p in zip(ct, pt)
    )


def decrypt(ct: list[int], key: str) -> str:
    """Beaufort decrypt: P = (K - core) mod 25."""
    return "".join(ALPHA[(ALPHA.index(k) - _core(c)) % 25] for c, k in zip(ct, key))


def main() -> None:
    k_prefix = derive_key(CT_PREFIX, CRIB_PREFIX)
    k_body = derive_key(FLAG_CT, CRIB_BODY_25)
    print("prefix key (35):", k_prefix)
    print("body   key (20):", k_body)
    print("full   key (55):", k_prefix + k_body)

    p_prefix = decrypt(CT_PREFIX, k_prefix)
    p_body = decrypt(FLAG_CT, k_body)
    print("prefix plain   :", p_prefix)
    print("body   plain   :", p_body)

    # "Farcical clone" verification: the per-byte clone digit (ct // 25) is not
    # tied to the plaintext, so the same letter shows up with different clones.
    collisions: dict[int, set[str]] = {}
    for c, p in zip(CT_PREFIX + FLAG_CT, CRIB_PREFIX + CRIB_BODY_25):
        collisions.setdefault(c, set()).add(p.lower())
    multi = {c: sorted(ps) for c, ps in collisions.items() if len(ps) > 1}
    print(
        "byte collisions (proves it is not a plain byte->letter substitution):",
        multi,
    )

    # Flag: un-fold I back to J on the first Jedi letter, preserve capitalisation
    # from CRIB_BODY.
    print("FLAG:", f"CIT{{{CRIB_BODY}}}")


if __name__ == "__main__":
    main()
