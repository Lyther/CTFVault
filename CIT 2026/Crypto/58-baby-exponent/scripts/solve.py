#!/usr/bin/env python3
"""Baby Exponent — CIT 2026 Crypto (58, 986 pts).

Textbook small-public-exponent RSA. Because e=3 and the message is short
enough that m^3 < n, the modular reduction in c = m^e mod n never happens,
so c is literally m^3 and plaintext = integer cube root of c.
"""

n = 3975311104658158367804953186451876987828483822427305148759145730088615027289956528884778329789668637386484932183485546402292017850452360645365142100268336371204659887371551551598753305231985601246101574833959356250563521064956134365407699223
e = 3
c = 21208016443347524194488872231478291493949438339558450377152081476869432669496266457076405093626099218034592769060441274220970709748741037953818131469435699367735940032724483543045224740051080037


def icbrt(n: int) -> int:
    """Integer cube root via Newton's method."""
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            return x
        x = y


assert c < n, "c >= n — would need Hastad/Coppersmith, not plain cube root"
m = icbrt(c)
assert m**e == c, "m^3 != c — message was reduced mod n after all"
print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())
