hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# Wait, the length is 209 chars. It's odd!
# Let's check the original hex representation of the codepoints.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
hex_str = "".join(f"{ord(c):x}" for c in text)
print("Hex length:", len(hex_str))
if len(hex_str) % 2 != 0:
    hex_str = "0" + hex_str

try:
    decoded = bytes.fromhex(hex_str)
    print("Decoded:", decoded)
except Exception as e:
    print(e)
