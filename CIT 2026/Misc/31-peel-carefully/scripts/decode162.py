# Let's look at the hex string again.
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# What if we map the hex digits to binary?
# 213 * 4 = 852 bits.
# What if we decode the binary as Base64?
# We did that, it gave gibberish.

# What if we decode the binary as Base32?
# We did that, it gave gibberish.

# What if we decode the binary as Ascii85?
# We did that, it gave gibberish.

# What if the binary data is a piece of code?
# What if the binary data is a URL?

# What if the binary data is a piece of text that has been compressed?
# We tried zlib, bz2, lzma.

# What if the binary data is a piece of text that has been encrypted with AES?
# If it's encrypted with AES, it would be random bytes, not printable ASCII.

# Let's count the number of Morse code characters again.
# 1320 characters.
# 1320 / 3 = 440 codons.
# 440 codons.
# 440 hex digits = 220 bytes.
# The 220 bytes end with "CIT{99".
# Wait, "CIT{99" is 6 bytes.
# What if the rest of the flag is hidden in the missing bits?
# We mapped 16 codons to 16 hex digits.
# 16 hex digits = 4 bits per codon.
# But there are 64 possible codons!
# We only saw 16 unique codons.
# Wait, 16 unique codons * 4 bits = 64 bits? No, 4 bits per codon.
# So 440 codons * 4 bits = 1760 bits = 220 bytes.
# But wait!
# We found 3 permutations that give a printable ASCII string.
# What if the string is just a base85 encoded string?
# We checked, it has characters outside base85.
# What if it's base64 encoded?
# We tried to decode it as base64, but it failed.
# Let's try to decode the base64 string again, maybe we need to pad it?
# s3 is 220 bytes long.
# 220 is not a multiple of 4.
# 220 % 4 = 0. Wait, 220 IS a multiple of 4!
# So it SHOULD be a valid base64 string!
# Let's try base64 decoding s3!
import base64
s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
try:
    print(base64.b64decode(s3))
except Exception as e:
    print("Base64 error:", e)

# What if it's Base32?
try:
    print(base64.b32decode(s3))
except Exception as e:
    print("Base32 error:", e)

