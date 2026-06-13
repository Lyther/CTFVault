text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Is the hex string 55499d74... a base encoded string?
# Let's convert it to bytes and try to decompress it?
hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# What if we pad the hex string to be even length?
# It's 213 characters long.
# Let's try prepending a 0.
data = bytes.fromhex("0" + hex_str)
print(data)

# Let's try appending a 0.
data = bytes.fromhex(hex_str + "0")
print(data)

# Wait, the hex string is exactly the hex representations of the codepoints!
# 5549 -> U+5549
# 9d74 -> U+9D74
# 1336f -> U+1336F
# This means the hex string is just a concatenation of the hex values of the codepoints.
# But what if the hex string ITSELF is the data?
# For example, "55499d74..."
# What if it's a hex encoded string?
# But it has an odd length!
# Why does it have an odd length?
# Because some codepoints have 5 hex digits (like 1336f) and some have 4 (like 5549).
# If we just concatenate them, we lose the boundaries!
# BUT we already know the boundaries because we have the original text!
# So the odd length is just a consequence of concatenation.

# What if we interpret the hex string as a big integer?
val = int(hex_str, 16)
# Convert to bytes
b = val.to_bytes((val.bit_length() + 7) // 8, 'big')
print("Big int bytes:", b)

# What if we convert the big integer to base 36? Base 58? Base 62? Base 85?
import base64
# Base 85?
