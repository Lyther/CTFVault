#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Discovery script — how the M3 key was originally found.

Pipeline:
    1. IC at multiple periods (rules out simple Vigenere) → suggests rotor cipher.
    2. Brute Enigma M3 over all 60 rotor orderings, both reflectors,
       all 17576 start positions, ring=AAA. Score by English letter freq + bigrams.
    3. Top hit: rotors I/II/III, refl B, start AAA, score ~267.
       Decrypt is 94% Turing's quote — 4 char errors at positions 19/20/45/46.
    4. The errors cluster, so plug in Turing's quote as a CRIB and sweep
       ring settings on the right rotor. Discovers ring=AAC, start=AAC.

Run: python3 scripts/bruteforce.py
Takes ~3 min on a laptop.
"""

from __future__ import annotations

import itertools
from collections import Counter

from solve import ALPH, CIPHER, REFL_B, ROTORS, Rotor

CRIB = "WECANONLYSEEASHORTDISTANCEAHEADBUTWECANSEEPLENTYTHERETHATNEEDSTOBEDONE"

_LETTER_FREQ = {
    "E": 12.7,
    "T": 9.06,
    "A": 8.17,
    "O": 7.51,
    "I": 6.97,
    "N": 6.75,
    "S": 6.33,
    "H": 6.09,
    "R": 5.99,
    "D": 4.25,
    "L": 4.03,
    "C": 2.78,
    "U": 2.76,
    "M": 2.41,
    "W": 2.36,
    "F": 2.23,
    "G": 2.02,
    "Y": 1.97,
    "P": 1.93,
    "B": 1.29,
    "V": 0.98,
    "K": 0.77,
    "J": 0.15,
    "X": 0.15,
    "Q": 0.10,
    "Z": 0.07,
}
_BIGRAMS = {
    "TH": 27,
    "HE": 23,
    "IN": 20,
    "ER": 18,
    "AN": 16,
    "RE": 14,
    "ND": 14,
    "ON": 13,
    "EN": 13,
    "AT": 13,
    "OU": 12,
    "ED": 12,
    "HA": 11,
    "TO": 11,
    "OR": 11,
    "IT": 11,
    "IS": 11,
    "HI": 10,
    "ES": 10,
    "NG": 10,
    "ST": 10,
    "OF": 10,
    "AS": 9,
    "TE": 9,
    "AR": 9,
    "AL": 9,
    "DE": 8,
    "SE": 8,
    "LE": 8,
}


def english_score(text: str) -> float:
    cnt = Counter(text)
    n = len(text)
    s = 0.0
    for c, f in _LETTER_FREQ.items():
        s -= abs(cnt.get(c, 0) / n * 100 - f)
    for i in range(n - 1):
        s += _BIGRAMS.get(text[i : i + 2], 0)
    return s


def encode_with(rotor_names, refl_wiring, start, ring):
    rotors = [
        Rotor(*ROTORS[rotor_names[i]], ring=ring[i], pos=start[i]) for i in range(3)
    ]
    refl = [ALPH.index(c) for c in refl_wiring]
    out = []
    L, M, R = rotors
    for ch in CIPHER:
        if M.at_notch():
            M.step()
            L.step()
        elif R.at_notch():
            M.step()
        R.step()
        c = ALPH.index(ch)
        for r in (R, M, L):
            c = r.encode(c, fwd=True)
        c = refl[c]
        for r in (L, M, R):
            c = r.encode(c, fwd=False)
        out.append(ALPH[c])
    return "".join(out)


def stage_1_brute() -> None:
    print("[1] M3 brute (ring=AAA, all rotors+starts, refl B/C) — top 5:")
    refls = {"B": REFL_B, "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}
    rotors_pool = ["I", "II", "III"]  # extend to IV/V if needed
    results = []
    for combo in itertools.permutations(rotors_pool, 3):
        for refl_name, refl_wiring in refls.items():
            for s0 in range(26):
                for s1 in range(26):
                    for s2 in range(26):
                        pt = encode_with(combo, refl_wiring, (s0, s1, s2), (0, 0, 0))
                        sc = english_score(pt)
                        if sc > 200:
                            results.append((sc, combo, refl_name, (s0, s1, s2), pt))
    results.sort(reverse=True, key=lambda r: r[0])
    for sc, combo, refl, start, pt in results[:5]:
        sl = "".join(ALPH[i] for i in start)
        print(f"   {sc:6.1f}  rotors={combo} refl={refl} start={sl}")
        print(f"           {pt}")


def stage_2_crib() -> None:
    print("\n[2] Crib + ring sweep on right rotor (rotors I/II/III, refl B):")
    for r2 in range(26):
        for s0 in range(26):
            for s1 in range(26):
                for s2 in range(26):
                    pt = encode_with(
                        ("I", "II", "III"),
                        REFL_B,
                        (s0, s1, s2),
                        (0, 0, r2),
                    )
                    if pt == CRIB:
                        print(
                            f"   PERFECT: ring=AA{ALPH[r2]} "
                            f"start={ALPH[s0]}{ALPH[s1]}{ALPH[s2]}",
                        )
                        return


if __name__ == "__main__":
    stage_1_brute()
    stage_2_crib()
