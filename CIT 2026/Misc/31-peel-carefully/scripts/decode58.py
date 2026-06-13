import urllib.parse
hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# What if it's base32? No, it has 'f'.
# What if we just decode it as base16? That's what we did.
# Let's look at the original text again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# 5549 9d74 1336f 9d67 5574 ...
# Notice that 5549 is 'U' (55) and 'I' (49).
# 9d74 is not ASCII.
# What if we convert the hex string to binary, and then group by 7 bits?
bin_str = bin(int(hex_str, 16))[2:].zfill(len(hex_str)*4)
for i in range(0, len(bin_str), 7):
    val = int(bin_str[i:i+7], 2)
    if 32 <= val <= 126:
        print(chr(val), end="")
    else:
        print(".", end="")
print()

