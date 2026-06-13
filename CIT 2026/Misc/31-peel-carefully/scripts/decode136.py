# The hex string is:
hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# What if we decode it as a sequence of 7-bit characters?
# 213 * 4 = 852 bits.
# 852 / 7 = 121.7 characters.
# Let's decode it as a sequence of 7-bit characters.
bin_str = bin(int(hex_str, 16))[2:].zfill(len(hex_str)*4)
decoded = ""
for i in range(0, len(bin_str), 7):
    chunk = bin_str[i:i+7]
    if len(chunk) == 7:
        val = int(chunk, 2)
        if 32 <= val <= 126:
            decoded += chr(val)
        else:
            decoded += "."

print("7-bit:", decoded)

# What if we decode it as a sequence of 6-bit characters?
# 852 / 6 = 142 characters.
# Let's decode it as a sequence of 6-bit characters.
b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
decoded = ""
for i in range(0, len(bin_str), 6):
    chunk = bin_str[i:i+6]
    if len(chunk) == 6:
        decoded += b64_chars[int(chunk, 2)]

print("Base64:", decoded)

# What if we decode it as a sequence of 5-bit characters?
# 852 / 5 = 170.4 characters.
b32_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
decoded = ""
for i in range(0, len(bin_str), 5):
    chunk = bin_str[i:i+5]
    if len(chunk) == 5:
        decoded += b32_chars[int(chunk, 2)]

print("Base32:", decoded)
