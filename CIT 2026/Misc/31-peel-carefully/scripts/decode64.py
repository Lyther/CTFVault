import urllib.parse

hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# The hex string is 213 characters long.
# Notice that the first character is '5'.
# What if it's a URL encoded string? No.
# What if the hex string is a sequence of 5-bit numbers?
# 213 * 4 = 852 bits.
# 852 / 5 = 170.4.

# Let's look at the original text again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Is there any other way to decode this text?
# What if we just print it?
print(text)

# What if it's a known cipher?
# Let's search the internet for "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Or maybe the codepoints are indices into some array?
# 21833, 40308, 78703, 40295, 21876, 40308, 77925, 21861, 39543, 39538, 27424, 27189, 27443, 74016, 77935, 78196, 21804, 78690, 21876, 21833, 78695, 78181, 21875, 21833, 38519, 21875, 77943, 67183, 24935, 40480, 21876, 38519, 21875, 27190, 26677, 25397, 15885, 15885, 32323, 131412, 42291, 26722, 37988, 41792, 37996, 67123, 25955, 26212, 40046, 131893

# Wait, what if we convert each codepoint to a hex string, and then decode that hex string as ASCII?
# We did that, and it gave us the 213 character hex string.
# What if we decode that hex string as ASCII?
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# Wait! "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"
# It's a hex string.
# What if we reverse the hex string?
# What if we XOR the hex string with something?
# What if we convert the hex string to a byte array, and then decompress it?
import zlib
try:
    b = bytes.fromhex("0" + hex_str)
    print(zlib.decompress(b))
except Exception as e:
    print(e)

try:
    b = bytes.fromhex(hex_str + "0")
    print(zlib.decompress(b))
except Exception as e:
    print(e)
