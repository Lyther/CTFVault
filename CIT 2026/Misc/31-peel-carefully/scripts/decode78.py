# What if the original hex string was NOT 440 characters?
# The original hex string from the codepoints was:
hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"
# It has 213 characters.
# What if we apply ROT47 to this hex string?
# It's just a hex string, so ROT47 will just map 0-9 to O-X, and a-f to 2-7.

# Let's look at the original characters again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"

# What if the codepoints are just Unicode codepoints, and we can convert them to UTF-8 bytes?
utf8_bytes = text.encode('utf-8')
# What if we decompress the UTF-8 bytes?
import zlib
try:
    print(zlib.decompress(utf8_bytes))
except:
    pass

import bz2
try:
    print(bz2.decompress(utf8_bytes))
except:
    pass

import lzma
try:
    print(lzma.decompress(utf8_bytes))
except:
    pass

# What if the codepoints are base64 encoded?
# No, they are Chinese characters.
# Wait, look at the codepoints in hex:
# 5549 9d74 1336f 9d67 5574 9d74 13065 5565 9a77 9a72 6b20 6a35 6b33 12120 1306f 13174 552c 13362 5574 5549 13367 13165 5573 5549 9677 5573 13077 1066f 6167 9e20 5574 9677 5573 6a36 6835 6335 3e0d 3e0d 7e43 20154 a533 6862 9464 a340 946c 10633 6563 6664 9c6e 20335
# Notice that many of them start with '55', '9d', '13', '6b', '6a', '68', '63', '65', '66', '64', '9c', '6e'.
# What if we take the lower byte of each codepoint?
lower_bytes = bytes([ord(c) & 0xFF for c in text])
print("Lower bytes:", lower_bytes)

# What if we take the upper byte of each codepoint?
upper_bytes = bytes([(ord(c) >> 8) & 0xFF for c in text])
print("Upper bytes:", upper_bytes)

# What if we take the top bits?
top_bits = bytes([(ord(c) >> 16) & 0xFF for c in text])
print("Top bits:", top_bits)

