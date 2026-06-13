hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# The hex string has 213 characters.
# What if it's 7-bit encoded?
# 213 * 4 = 852 bits.
# 852 / 7 = 121.7 characters.
# 852 / 8 = 106.5 characters.

# Wait, what if we decode the hex string as bytes, but we just prepend a 0?
data = bytes.fromhex("0" + hex_str)
print(data)

# Wait, what if the hex string is base64 encoded? No, it's hex.
# What if it's a string of hex digits, and we need to decode it to ASCII?
# 55 49 9d 74 ...
# 55 = U, 49 = I.
# 74 = t.
# 6f = o.
# 67 = g.
# 65 = e.
# 77 = w.
# 72 = r.
# 6b = k.
# 20 = space.
# 6a = j.
# 35 = 5.
# 6b = k.
# 33 = 3.
# 6f = o.
# 74 = t.
# 52 = R.
# 62 = b.
# 55 = U.
# 74 = t.
# 55 = U.
# 49 = I.
# 67 = g.
# 65 = e.
# 55 = U.
# 73 = s.
# 55 = U.
# 49 = I.
# 77 = w.
# 55 = U.
# 73 = s.
# 77 = w.
# 6f = o.
# 61 = a.
# 67 = g.
# 20 = space.
# 55 = U.
# 74 = t.
# 77 = w.
# 55 = U.
# 73 = s.
# 6a = j.
# 36 = 6.
# 68 = h.
# 35 = 5.
# 63 = c.
# 35 = 5.
# 3e = >.
# 0d = \r.
# 3e = >.
# 0d = \r.
# 7e = ~.
# 43 = C.
# 20 = space.
# 4a = J.
# 53 = S.
# 36 = 6.
# 29 = ).
# 46 = F.
# 4a = J.
# 34 = 4.
# 46 = F.
# 33 = 3.
# 65 = e.
# 63 = c.
# 66 = f.
# 64 = d.
# 6e = n.
# 20 = space.
# 33 = 3.
# 35 = 5.

# Look at the ASCII characters in the hex string!
for i in range(0, len(hex_str)-1, 2):
    b = int(hex_str[i:i+2], 16)
    if 32 <= b <= 126:
        print(chr(b), end="")
    else:
        print(f"[{b:02x}]", end="")
print()

