text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"

# Let's convert each character to its codepoint and then to a string of bits
# How many bits per character?
# The largest codepoint is U+20335, which is 18 bits.
# If we pad each codepoint to 18 bits:
bits = ""
for c in text:
    bits += f"{ord(c):018b}"

print("Length of bits:", len(bits))
# Length is 51 * 18 = 918 bits.
# 918 / 8 = 114.75 bytes. Not a multiple of 8.

# What if we pad each codepoint to 21 bits?
bits = ""
for c in text:
    bits += f"{ord(c):021b}"
print("Length of bits (21):", len(bits))
# 51 * 21 = 1071 bits.

# What if we pad each codepoint to 16 bits? Wait, some are > 65535.
# The ones > 65535 are:
# 𓍯 (U+1336F), 𓁥 (U+13065), 𒄠 (U+12120), 𓁯 (U+1306F), 𓅴 (U+13174), 𓍢 (U+13362), 𓍧 (U+13367), 𓅥 (U+13165), 𓁷 (U+13077), 𐙯 (U+1066F), 𠅔 (U+20154), 𐘳 (U+10633), 𠌵 (U+20335)
# Notice that these are all in the supplementary planes.
# In UTF-16, they are represented as surrogate pairs!
# Let's look at the UTF-16 representation again.
utf16 = text.encode('utf-16le')
print("UTF-16 length:", len(utf16))
# 126 bytes.
# 126 bytes = 63 UTF-16 code units.
# Wait, 126 bytes is 1008 bits.
# What if we decode the UTF-16 bytes as ASCII?
print(utf16)

# What if the UTF-16 bytes are actually a base64 string?
# No, they contain lots of non-printable characters.

# What if we XOR the UTF-16 bytes with something?
