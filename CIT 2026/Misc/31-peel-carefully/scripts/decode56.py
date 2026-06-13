hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"
print(hex_str)

# Is it possible that the hex string is just a big number?
# Or maybe it's a bunch of bytes that got mangled?
# If we look at the UTF-16 bytes:
# 5549 9d74 d80c df6f 9d67 5574 9d74 d80c dc65 5565
# The original hex string we got from ord(c) was:
# 5549 9d74 1336f 9d67 5574 9d74 13065 5565 9a77 9a72 6b20 6a35 6b33 12120 1306f 13174 552c 13362 5574 5549 13367 13165 5573 5549 9677 5573 13077 1066f 6167 9e20 5574 9677 5573 6a36 6835 6335 3e0d 3e0d 7e43 20154 a533 6862 9464 a340 946c 10633 6563 6664 9c6e 20335

# Notice that the hex string is EXACTLY the concatenation of the hex representations of the codepoints!
# "5549" + "9d74" + "1336f" + "9d67" + "5574" + ...
# Wait, let's look at the hex string again.
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335

# What if we just decode this hex string as ASCII?
# 55 = U, 49 = I, 9d = ?, 74 = t, 13 = ?, 36 = 6, f9 = ?, d6 = ?, 75 = u, 57 = W, 49 = I, d7 = ?, 41 = A, 30 = 0, 65 = e, 55 = U, 65 = e, 9a = ?, 77 = w, 9a = ?, 72 = r, 6b = k, 20 = space, 6a = j, 35 = 5, 6b = k, 33 = 3, 12 = ?, 12 = ?, 01 = ?, 30 = 0, 6f = o, 13 = ?, 17 = ?, 45 = E, 52 = R, c1 = ?, 33 = 3, 62 = b, 55 = U, 74 = t, 55 = U, 49 = I, 13 = ?, 36 = 6, 71 = q, 31 = 1, 65 = e, 55 = U, 73 = s, 55 = U, 49 = I, 96 = ?, 77 = w, 55 = U, 73 = s, 13 = ?, 07 = ?, 71 = q, 06 = ?, 6f = o, 61 = a, 67 = g, 9e = ?, 20 = space, 55 = U, 74 = t, 96 = ?, 77 = w, 55 = U, 73 = s, 6a = j, 36 = 6, 68 = h, 35 = 5, 63 = c, 35 = 5, 3e = >, 0d = \r, 3e = >, 0d = \r, 7e = ~, 43 = C, 20 = space, 15 = ?, 4a = J, 53 = S, 36 = 6, 86 = ?, 29 = ), 46 = F, 4a = J, 34 = 4, 09 = \t, 46 = F, c1 = ?, 06 = ?, 33 = 3, 65 = e, 63 = c, 66 = f, 64 = d, 9c = ?, 6e = n, 20 = space, 33 = 3, 5 = ?

# Wait, what if we group it differently?
# The hex string has 213 characters.
# What if it's base64? No, it's hex.
# What if we convert it to an integer and then to bytes?
val = int(hex_str, 16)
b = val.to_bytes((val.bit_length() + 7) // 8, 'big')
print(b)
