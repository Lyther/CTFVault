# The hex string is 213 characters long.
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# Wait, look at the hex string again.
# "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"
# It contains 'f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335'
# What if it's a base 36 string? No, it has characters up to 'f'.
# What if we decode it as a hex string, but we ignore the first character?
# We did that, it gave gibberish.

# What if we interpret the hex string as a sequence of 5-bit values?
# 213 * 4 = 852 bits.
# 852 / 5 = 170.4.
# What if we interpret the hex string as a sequence of 6-bit values?
# 852 / 6 = 142.
# Let's try to decode it as Base64!
# Base64 uses 6 bits per character.
# We can convert the hex string to binary, and then group by 6 bits.
hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"
bin_str = bin(int(hex_str, 16))[2:].zfill(len(hex_str)*4)

b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
decoded = ""
for i in range(0, len(bin_str), 6):
    chunk = bin_str[i:i+6]
    if len(chunk) == 6:
        decoded += b64_chars[int(chunk, 2)]

print("Base64:", decoded)

# What if we decode it as Base32?
# Base32 uses 5 bits per character.
b32_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
decoded = ""
for i in range(0, len(bin_str), 5):
    chunk = bin_str[i:i+5]
    if len(chunk) == 5:
        decoded += b32_chars[int(chunk, 2)]

print("Base32:", decoded)
