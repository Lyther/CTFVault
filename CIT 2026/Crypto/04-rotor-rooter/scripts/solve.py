#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Rotor Rooter — decrypt with the recovered Enigma M3 key.

Discovered config (via crib + ring/pos sweep — see writeup):
    Rotors:    I (left) - II (middle) - III (right)
    Reflector: B
    Ring:      A A C
    Position:  A A C
    Plugboard: empty

Plaintext is Alan Turing's "We can only see a short distance ahead..."
"""

from __future__ import annotations

import string

CIPHER = "KLEGCKRGGONTBNBVPIIZWXQQEZYAXXWQMGIZDNEWWUTOVZRWOMZKGWNKWZBQXOGZSTVCGU"
ALPH = string.ascii_uppercase

ROTORS = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
}
REFL_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


class Rotor:
    def __init__(self, wiring: str, notch: str, ring: int, pos: int) -> None:
        self.fwd = [ALPH.index(c) for c in wiring]
        self.bwd = [0] * 26
        for i, v in enumerate(self.fwd):
            self.bwd[v] = i
        self.notch = ALPH.index(notch)
        self.ring = ring
        self.pos = pos

    def at_notch(self) -> bool:
        return self.pos == self.notch

    def step(self) -> None:
        self.pos = (self.pos + 1) % 26

    def encode(self, c: int, fwd: bool) -> int:
        i = (c + self.pos - self.ring) % 26
        o = (self.fwd if fwd else self.bwd)[i]
        return (o - self.pos + self.ring) % 26


def decrypt(cipher: str) -> str:
    L = Rotor(*ROTORS["I"], ring=0, pos=0)
    M = Rotor(*ROTORS["II"], ring=0, pos=0)
    R = Rotor(*ROTORS["III"], ring=2, pos=2)
    refl = [ALPH.index(c) for c in REFL_B]
    out = []
    for ch in cipher:
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


def main() -> None:
    plaintext = decrypt(CIPHER)
    print(f"plaintext: {plaintext}")

    words = [
        "WE",
        "CAN",
        "ONLY",
        "SEE",
        "A",
        "SHORT",
        "DISTANCE",
        "AHEAD",
        "BUT",
        "WE",
        "CAN",
        "SEE",
        "PLENTY",
        "THERE",
        "THAT",
        "NEEDS",
        "TO",
        "BE",
        "DONE",
    ]
    assert "".join(words) == plaintext, "word split does not reconstruct plaintext"
    flag_body = "_".join(w.lower() for w in words)
    print(f"flag:      CIT{{{flag_body}}}")


if __name__ == "__main__":
    main()
